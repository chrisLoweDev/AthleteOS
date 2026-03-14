"""
Fetch the full Hevy exercise library and cache it locally.

Usage:
    python scripts/fetch_hevy_exercises.py

Writes: data/hevy-exercises.json
    {
        "last_synced": "2026-03-14T12:00:00Z",
        "count": 342,
        "exercises": { "Exercise Title": "TEMPLATE_ID", ... }
    }

Exit codes:
    0 — success
    1 — HTTP error
    2 — HEVY_API_KEY not set
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=ENV_PATH)

HEVY_BASE = "https://api.hevyapp.com/v1"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'hevy-exercises.json')


def main():
    api_key = os.getenv("HEVY_API_KEY", "").strip()
    if not api_key:
        print(
            "HEVY_API_KEY is not set.\n"
            "Get your API key at: https://hevy.com/settings?developer\n"
            "Then add it to .env: HEVY_API_KEY=<your-key>",
            file=sys.stderr,
        )
        sys.exit(2)

    headers = {"api-key": api_key}
    exercises = {}
    page = 1

    while True:
        resp = requests.get(
            f"{HEVY_BASE}/exercise_templates",
            params={"page": page, "pageSize": 100},
            headers=headers,
        )
        if not resp.ok:
            print(f"Hevy API error {resp.status_code}: {resp.text}", file=sys.stderr)
            sys.exit(1)

        data = resp.json()
        for e in data["exercise_templates"]:
            exercises[e["title"]] = e["id"]

        if page >= data["page_count"]:
            break
        page += 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    cache = {
        "last_synced": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(exercises),
        "exercises": exercises,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"Synced {len(exercises)} exercises to data/hevy-exercises.json")


if __name__ == "__main__":
    main()
