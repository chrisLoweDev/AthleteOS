# Athlete OS — First-Time Setup Guide

Follow these steps once to get everything working. After setup, use Claude Code slash commands to run the system.

---

## Step 1: Register a Strava API App

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api)
2. Fill in:
   - **Application Name:** Athlete OS (or anything)
   - **Category:** Data Importer
   - **Website:** http://localhost
   - **Authorization Callback Domain:** `localhost`
3. Click **Save** and note your **Client ID** and **Client Secret**

---

## Step 2: Create the `.env` file

In the AthleteOS directory, create a file named `.env`:

```
STRAVA_CLIENT_ID=your_client_id_here
STRAVA_CLIENT_SECRET=your_client_secret_here
STRAVA_REFRESH_TOKEN=
```

Leave `STRAVA_REFRESH_TOKEN` empty — it will be filled in by the auth script.

**Important:** `.env` is gitignored and never committed. Keep it private.

---

## Step 3: Install Python dependencies

```bash
pip install -r scripts/requirements.txt
```

Or with pip3:
```bash
pip3 install -r scripts/requirements.txt
```

Requires Python 3.8+.

---

## Step 4: Run the Strava OAuth setup

```bash
python scripts/strava_auth.py
```

This will:
1. Open your browser to Strava's authorization page
2. Ask you to log in and grant access (scope: `activity:read_all`)
3. Capture the authorization callback on `localhost:8080`
4. Write your `STRAVA_REFRESH_TOKEN` to `.env`

You should see: `Success! Authorized as: [Your Name]`

**Troubleshooting:**
- If the browser doesn't open, copy the URL printed to the terminal and open it manually
- If port 8080 is in use, edit `CALLBACK_PORT` in `scripts/strava_auth.py` — and update your Strava app's callback domain to match
- If you get a 401 error, double-check your Client ID and Client Secret in `.env`

---

## Step 5: Test the connection

```bash
python scripts/fetch_activities.py --after 2026-02-01
```

You should see a JSON array of your recent Strava activities printed to the terminal. An empty array `[]` is fine if you have no activities in that window.

---

## Step 6: Open Claude Code

```bash
cd /path/to/AthleteOS
claude
```

Run the onboarding command to fill in your athlete profile:

```
/setup
```

This walks you through entering your FTP, HR zones, threshold pace, goals, and weekly availability. It also confirms Strava connectivity.

---

## Step 7: Plan your first training block

```
/plan-workouts 7
```

Claude will ask a few questions and then propose a week of training for your approval. After you confirm, it creates the workout files.

---

## Day-to-Day Usage

| When | Command |
|------|---------|
| After completing workouts | `/fetch-activities` |
| When ready to plan ahead | `/plan-workouts [days]` |
| To see your schedule | `/calendar` |
| Weekly check-in | `/review` |

---

## File Structure Reference

```
AthleteOS/
├── CLAUDE.md                    # AI instructions (don't edit unless you know what you're doing)
├── .env                         # Your Strava credentials (never commit this)
├── athlete/
│   ├── profile.md               # Your FTP, zones, goals — edit this directly anytime
│   └── consistency-log.md       # Auto-updated rolling training log
├── workouts/
│   ├── plans/                   # Upcoming sessions (organized by week)
│   ├── completed/               # Done sessions (moved here by /fetch-activities)
│   └── reflections/             # Weekly reflection files
├── overview/
│   ├── pending.md               # Quick view of upcoming sessions
│   └── strava-sync.json         # Sync state (don't edit manually)
└── scripts/
    ├── strava_auth.py           # One-time OAuth (run once)
    ├── strava_client.py         # Strava API wrapper (used by fetch script)
    ├── fetch_activities.py      # Called by /fetch-activities
    └── requirements.txt
```

---

## Updating Your Profile

Edit `athlete/profile.md` directly any time your benchmarks change:
- After an FTP test: update FTP and the watts in the zone table
- After a running time trial: update threshold pace and the pace zone table
- New race on the calendar: add it to "Upcoming Events"

Claude reads this file before every planning session.

---

## Troubleshooting

**`STRAVA_REFRESH_TOKEN` error:**
Re-run `python scripts/strava_auth.py`. Strava tokens are valid until you revoke access.

**"No new activities" when you expect some:**
Check `overview/strava-sync.json` — the `last_sync_timestamp` might be too recent. You can edit it to an earlier date to re-fetch.

**Workout file in wrong place:**
Move it manually to the correct `workouts/plans/YYYY-WXX/` folder. File location doesn't affect Claude's ability to read it (it globs all subdirectories).

**Profile placeholders still in profile.md:**
Run `/setup` to fill them in interactively, or edit the file directly.
