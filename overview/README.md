# Overview

System-level state files that commands use to track what's planned, what's been synced, and how you've been feeling. These are machine-maintained — you shouldn't need to edit them directly.

## Files

### `pending.md`

Master table of all upcoming (status: `pending`) workout sessions. Regenerated automatically by `/plan-workouts`, `/fetch-activities`, and `/calendar` whenever workout files change.

Columns: Date, Day, Type, Duration, Focus, Status, link to plan file.

Use `/calendar` to view this in a clean format. Do not edit manually — it will be overwritten on the next command run.

### `journal-summary.md`

Rolling table of the last ~12 weeks of journal entries, one row per entry. Updated automatically by `/journal`.

Columns: Date, Day, Context (pre/post/general), Energy, Fatigue, Mood, Stress, Sleep, linked session, Highlight note.

Used by `/plan-workouts` and `/review` to surface fatigue and stress patterns before generating new sessions. The rolling window means old entries age out automatically — no manual pruning needed.

### `strava-sync.json`

Tracks Strava sync state between `/fetch-activities` runs. Contains:

- `last_sync_timestamp` — ISO 8601 datetime of the most recent sync; used as the `--after` cutoff for the next fetch
- `seen_ids` — array of Strava activity IDs already processed; prevents duplicate matching across runs

Updated automatically after every successful `/fetch-activities` run. If you need to re-process an activity, remove its ID from `seen_ids`. If you want to re-sync from scratch, reset `last_sync_timestamp` to an earlier date.
