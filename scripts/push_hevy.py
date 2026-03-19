"""
Push a weights workout file to Hevy as a Routine.

If the file already has a hevy_routine_id, the existing routine is updated (PUT).
If not, a new routine is created (POST) and the ID is written back to the file.

Usage:
    python scripts/push_hevy.py workouts/plans/2026-W11/2026-03-11-weights-full-body-a.md

Output: routine ID to stdout on success.
Errors: printed to stderr.
Exit codes:
    0 — success (created or updated)
    1 — general error
    2 — HEVY_API_KEY not set
    3 — unknown exercise name not in cache
    4 — exercise cache (data/hevy-exercises.json) not found
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=ENV_PATH)

HEVY_BASE = "https://api.hevyapp.com/v1"
CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'hevy-exercises.json')
CACHE_STALE_DAYS = 7


def load_exercise_ids():
    """Load exercise name→ID mapping from local cache."""
    if not os.path.exists(CACHE_PATH):
        print(
            "ERROR: data/hevy-exercises.json not found.\n"
            "Run: python3 scripts/fetch_hevy_exercises.py\n"
            "Or use the /sync-hevy-exercises command.",
            file=sys.stderr,
        )
        sys.exit(4)

    with open(CACHE_PATH) as f:
        data = json.load(f)

    last_synced = data.get("last_synced", "")
    if last_synced:
        try:
            synced_dt = datetime.strptime(last_synced, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - synced_dt).days
            if age_days > CACHE_STALE_DAYS:
                print(
                    f"WARNING: data/hevy-exercises.json is {age_days} days old. "
                    "Run /sync-hevy-exercises to refresh.",
                    file=sys.stderr,
                )
        except ValueError:
            pass

    return data["exercises"]


HEVY_EXERCISE_IDS = load_exercise_ids()


def parse_frontmatter(text):
    """Return dict of YAML frontmatter key-value pairs (strings only)."""
    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ':' in line:
            key, _, value = line.partition(':')
            fm[key.strip()] = value.strip().strip('"')
    return fm


def parse_table_rows(text, section_header):
    """Extract rows from a markdown table under the given section header."""
    pattern = rf'## {re.escape(section_header)}\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return []

    rows = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| ---'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if cells and cells[0].lower() == 'exercise':
            continue
        if len(cells) >= 3:
            rows.append(cells)
    return rows


def parse_weight_kg(value):
    """Convert weight string like '65kg', 'Bodyweight', 'Bodyweight (84kg)' to float kg."""
    value = value.strip()
    if value.lower().startswith('bodyweight'):
        return 0.0
    match = re.search(r'([\d.]+)', value)
    if match:
        return float(match.group(1))
    return 0.0


def parse_sets_info(sets_str):
    """
    Parse the Sets column into (total_count, warmup_count).

    Handles:
      "5"                    → (5, 0)   plain integer, no warm-ups
      "2"                    → (2, 0)
      "2 warm-up + 5 working"→ (7, 2)   first 2 are warmup type
      "—" or "-"             → (1, 0)   fallback
    """
    sets_str = sets_str.strip()
    if sets_str.isdigit():
        return int(sets_str), 0

    # "2 warm-up + 5 working" or "2 warm-ups + 5 working sets"
    m = re.match(r'(\d+)\s*warm[- ]?ups?\s*\+\s*(\d+)\s*working', sets_str, re.IGNORECASE)
    if m:
        wu = int(m.group(1))
        working = int(m.group(2))
        return wu + working, wu

    # Fallback: extract the first number found
    m = re.search(r'(\d+)', sets_str)
    if m:
        return int(m.group(1)), 0

    return 1, 0


def parse_reps_list(reps_str, total_count):
    """
    Parse the Reps column into a list of ints with length total_count.

    Handles:
      "5"                         → [5, 5, 5, ...]  repeated
      "6 / 6 / 5 / 5 / 5 / 5 / 5"→ [6, 6, 5, 5, 5, 5, 5]
      "5 working"                 → [5, 5, 5, ...]
    """
    reps_str = reps_str.strip()

    if reps_str.isdigit():
        return [int(reps_str)] * total_count

    if '/' in reps_str:
        parts = [p.strip() for p in reps_str.split('/')]
        result = []
        for p in parts:
            m = re.search(r'(\d+)', p)
            result.append(int(m.group(1)) if m else 0)
        # Extend to total_count using the last value
        while len(result) < total_count:
            result.append(result[-1] if result else 0)
        return result[:total_count]

    # "5 working" or any string containing a number
    m = re.search(r'(\d+)', reps_str)
    val = int(m.group(1)) if m else 0
    return [val] * total_count


def parse_weights_list(weight_str, total_count):
    """
    Parse the Target Weight column into a list of floats with length total_count.

    Handles:
      "80kg"               → [80.0, 80.0, ...]
      "50kg / 50kg / 80kg" → [50.0, 50.0, 80.0, 80.0, ...] (last value repeated)
      "Bodyweight (84kg)"  → [0.0, 0.0, ...]
    """
    weight_str = weight_str.strip()

    if '/' in weight_str:
        parts = [p.strip() for p in weight_str.split('/')]
        result = [parse_weight_kg(p) for p in parts]
        while len(result) < total_count:
            result.append(result[-1] if result else 0.0)
        return result[:total_count]

    val = parse_weight_kg(weight_str)
    return [val] * total_count


def build_exercises(main_rows, accessory_rows):
    """
    Build Hevy exercise objects from parsed table rows.

    Main Lifts table columns:  Exercise | Sets | Reps | Target Weight | Actual Weight | Notes
    Accessory Work table cols: Exercise | Sets | Reps | Target Weight | Actual Weight

    Both sets/reps columns accept plain integers OR compound strings
    (e.g. "2 warm-up + 5 working", "6 / 6 / 5 / 5 / 5 / 5 / 5").

    Returns list of exercise dicts ready for the Hevy API payload.
    Raises SystemExit(3) if an exercise name is not in HEVY_EXERCISE_IDS.
    """
    exercise_sets = {}   # name → list of set dicts
    exercise_order = []

    def add_row(cells, has_notes):
        name = cells[0]
        sets_str = cells[1] if len(cells) > 1 else "1"
        reps_str = cells[2] if len(cells) > 2 else "0"
        weight_str = cells[3] if len(cells) > 3 else ""
        notes = cells[5].strip() if has_notes and len(cells) > 5 else ""

        total_count, warmup_count = parse_sets_info(sets_str)
        reps_per_set = parse_reps_list(reps_str, total_count)
        weights_per_set = parse_weights_list(weight_str, total_count)

        if name not in exercise_sets:
            if name not in HEVY_EXERCISE_IDS:
                print(
                    f"ERROR: '{name}' not found in data/hevy-exercises.json.\n"
                    "Check the exercise name matches the Hevy library exactly, "
                    "or run /sync-hevy-exercises to refresh the cache.",
                    file=sys.stderr,
                )
                sys.exit(3)
            exercise_sets[name] = []
            exercise_order.append(name)

        for i in range(total_count):
            # Determine set type
            if warmup_count > 0:
                set_type = "warmup" if i < warmup_count else "normal"
            else:
                set_type = "warmup" if "warm-up" in notes.lower() else "normal"

            exercise_sets[name].append({
                "type": set_type,
                "weight_kg": weights_per_set[i],
                "reps": reps_per_set[i],
            })

    for cells in main_rows:
        add_row(cells, has_notes=True)

    for cells in accessory_rows:
        add_row(cells, has_notes=False)

    exercises = []
    for name in exercise_order:
        exercises.append({
            "exercise_template_id": HEVY_EXERCISE_IDS[name],
            "notes": "",
            "sets": exercise_sets[name],
        })
    return exercises


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to weights workout markdown file")
    args = parser.parse_args()

    api_key = os.getenv("HEVY_API_KEY", "").strip()
    if not api_key:
        print(
            "HEVY_API_KEY is not set.\n"
            "Get your API key at: https://hevy.com/settings?developer\n"
            "Then add it to .env: HEVY_API_KEY=<your-key>",
            file=sys.stderr,
        )
        sys.exit(2)

    with open(args.file) as f:
        text = f.read()

    fm = parse_frontmatter(text)

    existing_id = fm.get("hevy_routine_id", "null").strip()
    if existing_id == "null":
        existing_id = None

    key_focus = fm.get("key_focus", os.path.basename(args.file)).strip('"')
    date_str = fm.get("date", "").strip()
    title = f"{date_str} - {key_focus}" if date_str else key_focus

    main_rows = parse_table_rows(text, "Main Lifts")
    accessory_rows = parse_table_rows(text, "Accessory Work")
    core_rows = parse_table_rows(text, "Core")

    if not main_rows and not accessory_rows and not core_rows:
        print("ERROR: No exercise tables found in file.", file=sys.stderr)
        sys.exit(1)

    exercises = build_exercises(main_rows, accessory_rows + core_rows)

    payload = {
        "routine": {
            "title": title,
            "folder_id": None,
            "exercises": exercises,
        }
    }

    headers = {"api-key": api_key, "Content-Type": "application/json"}

    if existing_id:
        # Update the existing routine
        resp = requests.put(
            f"{HEVY_BASE}/routines/{existing_id}",
            json=payload,
            headers=headers,
        )
        if not resp.ok:
            print(f"Hevy API error {resp.status_code}: {resp.text}", file=sys.stderr)
            sys.exit(1)
        print(f"updated: {existing_id}")
    else:
        # Create a new routine
        resp = requests.post(
            f"{HEVY_BASE}/routines",
            json=payload,
            headers=headers,
        )
        if not resp.ok:
            print(f"Hevy API error {resp.status_code}: {resp.text}", file=sys.stderr)
            sys.exit(1)

        result = resp.json()["routine"]
        routine_id = result[0]["id"] if isinstance(result, list) else result["id"]
        print(routine_id)


if __name__ == "__main__":
    main()
