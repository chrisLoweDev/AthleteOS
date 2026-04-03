# Athlete OS — Project Memory

## What This Project Is
AI personal trainer CLI built on Claude Code. User interacts via slash commands. All data stored as markdown files. Strava API for activity data.

## Key Architecture
- Interface: Claude Code slash commands in `.claude/commands/`
- AI engine: Claude Code itself (no extra API cost)
- Storage: Markdown files + JSON for Strava cache
- Python scripts for Strava API (adapted from palmares_backend)

## Skills
- `/setup` — interactive onboarding to populate athlete/profile.md + Strava connectivity test
- `/fetch-activities` — pull Strava data, compare vs plans, generate reflection
- `/plan-workouts [days] [context]` — dialog-based planning, generates workout markdown files
- `/calendar` — show pending workout table
- `/review` — wraps fetch-activities + narrative weekly summary + option to kick off planning

## Key File Paths
- `CLAUDE.md` — AI system instructions
- `athlete/profile.md` — FTP, HR zones, goals
- `athlete/consistency-log.md` — 12-week rolling tables
- `workouts/plans/YYYY-WXX/YYYY-MM-DD-type-desc.md` — individual workout plans
- `workouts/completed/` — moved here after reflection
- `workouts/reflections/YYYY-WXX-reflection.md` — weekly reflections
- `overview/pending.md` — master table of upcoming sessions
- `overview/strava-sync.json` — last sync timestamp

## Strava Integration
- FULLY STANDALONE — no links to palmares_backend or any other project whatsoever
- Credentials: STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, STRAVA_REFRESH_TOKEN in .env
- One-time auth via `scripts/strava_auth.py` (local OAuth callback server on port 8000)
- Fetch via `scripts/fetch_activities.py --after DATE` → JSON to stdout

## Notable Limitations
- Strava has NO sets/reps/weight data for weight training — always ask user after fetch
- Weight training sessions need manual detail entry in plan files (template has Actual Weight column)

## Virtual Ride Interpretation
- See: `feedback_virtual_rides_erg_mode.md`
- All virtual rides are in ERG mode — elevation, gradients, and segments are meaningless
- Focus on avg watts, NP, HR, and lap structure only

## User Context
- User is Chris (from Dex CLAUDE.md)
- Already has Strava integration in palmares_backend project — likely has Strava API credentials

## Upcoming / In Progress
- **FTP Test (week of 2026-04-07):** Chris wants to do a real FTP test to replace the current assumed value in profile.md. After the test: update FTP, then use `/set-goals` to define annual power targets.
  - See: `project_ftp_test_intent.md`
