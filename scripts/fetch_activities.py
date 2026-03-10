"""
Fetch Strava activities and output as JSON to stdout.

Usage:
    python scripts/fetch_activities.py --after 2026-03-01
    python scripts/fetch_activities.py --after 2026-03-01 --before 2026-03-10
    python scripts/fetch_activities.py --after 1740787200  # Unix timestamp also accepted

Output: JSON array of activity objects to stdout.
Errors: printed to stderr (so Claude can distinguish data from errors).
"""

import argparse
import json
import sys
import os
from datetime import datetime, timezone

# Make scripts/ importable regardless of working directory
sys.path.insert(0, os.path.dirname(__file__))

from strava_client import StravaClient


def iso_to_timestamp(value: str) -> int:
    """Convert ISO 8601 date/datetime string or Unix timestamp string to int Unix timestamp."""
    # If it's already a number, return as-is
    if value.isdigit():
        return int(value)

    # Try various ISO formats
    formats = [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d',
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except ValueError:
            continue

    raise ValueError(f"Cannot parse date: {value!r}. Use ISO format like 2026-03-01 or Unix timestamp.")


def normalize_activity(activity: dict) -> dict:
    """
    Extract and normalize key fields from a Strava activity dict.
    Always includes all fields (null if missing) for consistent parsing by Claude.
    """
    return {
        'id': activity.get('id'),
        'name': activity.get('name'),
        'sport_type': activity.get('sport_type') or activity.get('type'),
        'start_date_local': activity.get('start_date_local'),
        'moving_time_seconds': activity.get('moving_time'),
        'elapsed_time_seconds': activity.get('elapsed_time'),
        'distance_meters': activity.get('distance'),
        'total_elevation_gain': activity.get('total_elevation_gain'),
        'average_heartrate': activity.get('average_heartrate'),
        'max_heartrate': activity.get('max_heartrate'),
        'average_watts': activity.get('average_watts'),
        'weighted_average_watts': activity.get('weighted_average_watts'),
        'average_speed_mps': activity.get('average_speed'),
        'max_speed_mps': activity.get('max_speed'),
        'kilojoules': activity.get('kilojoules'),
        'description': activity.get('description'),
        # Detail-only fields (null in summary mode)
        'splits_metric': activity.get('splits_metric'),
        'laps': activity.get('laps'),
        'segment_efforts': activity.get('segment_efforts'),
    }


def main():
    parser = argparse.ArgumentParser(description='Fetch Strava activities as JSON')
    parser.add_argument('--after', required=True,
                        help='Fetch activities after this date (ISO 8601 or Unix timestamp)')
    parser.add_argument('--before', default=None,
                        help='Fetch activities before this date (ISO 8601 or Unix timestamp)')
    parser.add_argument('--detail', action='store_true',
                        help='Fetch detailed data for each activity (slower)')
    args = parser.parse_args()

    try:
        after_ts = iso_to_timestamp(args.after)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        client = StravaClient()
    except EnvironmentError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Refresh auth token before making requests
    try:
        client.refresh_auth_token()
    except Exception as e:
        print(f"ERROR: Token refresh failed: {e}", file=sys.stderr)
        print("Try running: python scripts/strava_auth.py", file=sys.stderr)
        sys.exit(1)

    # Fetch activities
    try:
        raw_activities = client.get_activities_after(after_ts)
    except Exception as e:
        print(f"ERROR: Failed to fetch activities: {e}", file=sys.stderr)
        sys.exit(1)

    # Optional: filter by --before
    if args.before:
        try:
            before_ts = iso_to_timestamp(args.before)
            raw_activities = [
                a for a in raw_activities
                if a.get('start_date_local') and
                iso_to_timestamp(a['start_date_local'].split('T')[0]) < before_ts
            ]
        except ValueError as e:
            print(f"WARNING: Could not apply --before filter: {e}", file=sys.stderr)

    # Optional: fetch detailed data for each activity
    if args.detail and raw_activities:
        print(f"Fetching detailed data for {len(raw_activities)} activities...", file=sys.stderr)
        detailed = []
        for activity in raw_activities:
            try:
                detail = client.get_activity_detail(activity['id'])
                # Merge summary into detail (detail has all summary fields plus more)
                detailed.append(detail)
            except Exception as e:
                print(f"WARNING: Could not fetch detail for activity {activity['id']}: {e}",
                      file=sys.stderr)
                detailed.append(activity)
        raw_activities = detailed

    # Normalize and output
    normalized = [normalize_activity(a) for a in raw_activities]
    print(json.dumps(normalized, indent=2))


if __name__ == '__main__':
    main()
