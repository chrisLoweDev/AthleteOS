# Athlete OS — First-Time Setup Guide

Follow these steps once to get everything working. After setup, use Claude Code slash commands to run the system.

---

## Step 1: Authorize Strava

Run the following command, substituting the credentials provided by your AthleteOS administrator:

```bash
python3 scripts/strava_auth.py --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET>
```

A browser window will open. Log in to Strava and click **Authorize**. The script will save your credentials automatically to `.env`.

You should see: `Success! Authorized as: [Your Name]`

**Troubleshooting:**
- If the browser doesn't open, copy the URL printed to the terminal and open it manually
- If port 8080 is in use, edit `CALLBACK_PORT` in `scripts/strava_auth.py`
- If you get a 401 error, double-check that your Client ID and Secret are correct

---

## Step 2: Install Python dependencies

```bash
pip install -r scripts/requirements.txt
```

Or with pip3:
```bash
pip3 install -r scripts/requirements.txt
```

Requires Python 3.8+.

---

## Step 3: Test the connection

```bash
python scripts/fetch_activities.py --after 2026-02-01
```

You should see a JSON array of your recent Strava activities printed to the terminal. An empty array `[]` is fine if you have no activities in that window.

---

## Step 4: Add your Hevy API key (optional)

If you have a **Hevy Pro** account, you can push workout routines directly to Hevy.

1. Go to [hevy.com/settings?developer](https://www.hevy.com/settings?developer)
2. Log in → Settings → Developer → Generate Key
3. Add it to your `.env` file:
   ```
   HEVY_API_KEY=your_key_here
   ```

If you don't have Hevy Pro, skip this step — you can add it later via `/setup`.

---

## Step 5: Open Claude Code

```bash
cd /path/to/AthleteOS
claude
```

Run the onboarding command to fill in your athlete profile:

```
/setup
```

This walks you through entering your FTP, HR zones, threshold pace, goals, and weekly availability. It confirms Strava connectivity and optionally sets up Hevy.

---

## Step 6: Plan your first training block

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
├── .env                         # Your Strava + Hevy credentials (never commit this)
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
├── data/
│   └── hevy-exercises.json      # Hevy exercise name→ID cache (refresh with /sync-hevy-exercises)
└── scripts/
    ├── strava_auth.py           # One-time OAuth (run once)
    ├── strava_client.py         # Strava API wrapper (used by fetch script)
    ├── fetch_activities.py      # Called by /fetch-activities
    ├── fetch_hevy_exercises.py  # Populates hevy-exercises.json cache
    ├── push_hevy.py             # Called by /push-workouts
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
Re-run `python3 scripts/strava_auth.py --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET>` (get the credentials from whoever shared AthleteOS with you). Strava tokens are valid until you revoke access.

**"No new activities" when you expect some:**
Check `overview/strava-sync.json` — the `last_sync_timestamp` might be too recent. You can edit it to an earlier date to re-fetch.

**Workout file in wrong place:**
Move it manually to the correct `workouts/plans/YYYY-WXX/` folder. File location doesn't affect Claude's ability to read it (it globs all subdirectories).

**Profile placeholders still in profile.md:**
Run `/setup` to fill them in interactively, or edit the file directly.
