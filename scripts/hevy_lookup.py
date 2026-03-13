"""
Look up Hevy exercise template IDs by search term.

Usage:
    python scripts/hevy_lookup.py deadlift
    python scripts/hevy_lookup.py "cable row"

Maintenance utility — run this when adding a new exercise to HEVY_EXERCISE_IDS in push_hevy.py.
Never called automatically.
"""

import os
import sys

import requests
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=ENV_PATH)

HEVY_BASE = "https://api.hevyapp.com/v1"


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/hevy_lookup.py <search term>")
        sys.exit(1)

    api_key = os.getenv("HEVY_API_KEY", "").strip()
    if not api_key:
        print(
            "HEVY_API_KEY is not set.\n"
            "Get your API key at: https://hevy.com/settings?developer\n"
            "Then add it to .env: HEVY_API_KEY=<your-key>",
            file=sys.stderr,
        )
        sys.exit(2)

    term = " ".join(sys.argv[1:]).lower()
    headers = {"api-key": api_key}

    page = 1
    matches = []
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
            if term in e["title"].lower():
                matches.append(e)

        if page >= data["page_count"]:
            break
        page += 1

    if not matches:
        print(f"No matches for '{term}'")
        sys.exit(0)

    print(f"{'ID':<12} {'Title':<45} {'Equipment':<20} Muscle")
    print("-" * 90)
    for e in matches:
        print(f"{e['id']:<12} {e['title']:<45} {e['equipment']:<20} {e['primary_muscle_group']}")


if __name__ == "__main__":
    main()
