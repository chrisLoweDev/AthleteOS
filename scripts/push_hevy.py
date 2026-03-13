"""
Push a weights workout file to Hevy as a Routine.

Usage:
    python scripts/push_hevy.py workouts/plans/2026-W11/2026-03-11-weights-full-body-a.md

Output: routine ID to stdout on success.
Errors: printed to stderr.
Exit codes:
    0 — success (or already pushed)
    1 — general error
    2 — HEVY_API_KEY not set
    3 — unknown exercise name not in HEVY_EXERCISE_IDS
"""

import argparse
import os
import re
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=ENV_PATH)

HEVY_BASE = "https://api.hevyapp.com/v1"

# Verified via API on 2026-03-13
HEVY_EXERCISE_IDS = {
    "Squat (Barbell)":             "D04AC939",  # Squat (Barbell)
    "Bench Press (Barbell)":       "79D0BB3A",  # Bench Press (Barbell)
    "Bent-Over Row (Barbell)":     "55E6546F",  # Bent Over Row (Barbell)
    "Romanian Deadlift (Barbell)": "2B4B7310",  # Romanian Deadlift (Barbell)
    "Overhead Press (Barbell)":    "7B8D84E8",  # Overhead Press (Barbell)
    "Pull-Ups":                    "1B2B1E7C",  # Pull Up
    "Hanging Leg Raises":          "F8356514",  # Hanging Leg Raise
    "Bicep Curl (Barbell)":        "A5AC6449",  # Bicep Curl (Barbell)
    "Russian Twists":              "BB83BDDE",  # Russian Twist (Bodyweight)
}


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
    # Find the section
    pattern = rf'## {re.escape(section_header)}\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return []

    rows = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| ---'):
            continue
        # Skip header row (contains 'Exercise' as first cell)
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


def build_exercises(main_rows, accessory_rows):
    """
    Group table rows into Hevy exercise objects.
    Returns list of exercise dicts ready for the API payload.
    Raises SystemExit(3) if an exercise name is not in HEVY_EXERCISE_IDS.
    """
    # Collect sets per exercise in order
    exercise_sets = {}  # name -> list of set dicts
    exercise_order = []

    def add_row(cells, has_notes):
        name = cells[0]
        sets_count = int(cells[1]) if cells[1].isdigit() else 1
        reps = int(cells[2]) if cells[2].isdigit() else 0
        weight_kg = parse_weight_kg(cells[3]) if len(cells) > 3 else 0.0
        notes = cells[5].strip() if has_notes and len(cells) > 5 else ""
        set_type = "warmup" if "warm-up" in notes.lower() else "normal"

        if name not in exercise_sets:
            if name not in HEVY_EXERCISE_IDS:
                print(f"ERROR: '{name}' not in HEVY_EXERCISE_IDS — run hevy_lookup.py to find the ID and add it.", file=sys.stderr)
                sys.exit(3)
            exercise_sets[name] = []
            exercise_order.append(name)

        for _ in range(sets_count):
            exercise_sets[name].append({
                "type": set_type,
                "weight_kg": weight_kg,
                "reps": reps,
            })

    # Main Lifts: Exercise | Sets | Reps | Target Weight | Actual Weight | Notes
    for cells in main_rows:
        add_row(cells, has_notes=True)

    # Accessory Work: Exercise | Sets | Reps | Target Weight (no Notes col)
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

    routine_id = fm.get("hevy_routine_id", "null").strip()
    if routine_id and routine_id != "null":
        print(f"already pushed: {routine_id}")
        sys.exit(0)

    title = fm.get("key_focus", os.path.basename(args.file)).strip('"')

    main_rows = parse_table_rows(text, "Main Lifts")
    accessory_rows = parse_table_rows(text, "Accessory Work")

    if not main_rows and not accessory_rows:
        print("ERROR: No exercise tables found in file.", file=sys.stderr)
        sys.exit(1)

    exercises = build_exercises(main_rows, accessory_rows)

    payload = {
        "routine": {
            "title": title,
            "folder_id": None,
            "exercises": exercises,
        }
    }

    resp = requests.post(
        f"{HEVY_BASE}/routines",
        json=payload,
        headers={"api-key": api_key, "Content-Type": "application/json"},
    )

    if not resp.ok:
        print(f"Hevy API error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()["routine"]
    routine_id = result[0]["id"] if isinstance(result, list) else result["id"]
    print(routine_id)


if __name__ == "__main__":
    main()
