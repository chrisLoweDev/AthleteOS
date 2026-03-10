# /setup — First-Time Onboarding

Run this command once to set up your Athlete OS profile and verify Strava connectivity.

## Steps

### Step 1: Check profile status

Read `athlete/profile.md`. Look for lines containing `[` characters (unfilled placeholders).

- If the profile appears complete (no `[` characters), skip to Step 3.
- If placeholders exist, proceed to Step 2.

### Step 2: Interactive profile setup

Collect the following information via dialog with the user. Ask all questions, then write the completed profile in one go.

Ask:
1. "What's your name?"
2. "What's your current body weight in kg? (or press Enter to skip)"
3. "What's your current Cycling FTP in watts? (if you don't know, we can estimate later)"
4. "When did you last test your FTP? (date, or 'never')"
5. "What's your Running Threshold Pace? (e.g., 4:45/km — this is your sustainable 1-hour race pace)"
6. "What's your Max HR in bpm? (or press Enter to skip)"
7. "What's your Resting HR in bpm? (or press Enter to skip)"
8. "What are your primary training goals? (e.g., complete a triathlon, improve cycling FTP, run a half marathon)"
9. "Which days of the week are you available to train? (e.g., Mon, Wed, Thu, Sat, Sun)"
10. "What's your maximum training hours per week? (e.g., 8)"
11. "Anything else I should know? (injuries, upcoming races, travel, etc.)"

After collecting answers, fill in `athlete/profile.md` with the provided values, replacing all `[placeholder]` values.

Compute training zones from the provided FTP and max HR and fill in the zone tables.

### Step 3: Test Strava connectivity

Run:
```
python scripts/fetch_activities.py --after [30 days ago date in YYYY-MM-DD format]
```

- If it outputs a JSON array (even empty `[]`): report "Strava connection successful."
- If it exits with an error: display the error message and guide the user:
  - Check that `.env` has `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, and `STRAVA_REFRESH_TOKEN` set
  - If `STRAVA_REFRESH_TOKEN` is missing or empty: tell them to run `python scripts/strava_auth.py`
  - Refer them to `setup/SETUP.md` for step-by-step instructions

### Step 4: Confirm and next steps

Print:
```
Profile saved to athlete/profile.md
Strava: [connected / needs setup]

Next steps:
- Run /plan-workouts to create your first training block
- Run /fetch-activities after completing workouts to log progress
- Run /calendar to see your upcoming sessions
```
