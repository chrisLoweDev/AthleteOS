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
11. "Do you train at a commercial gym, home gym, or somewhere else? Describe your setup briefly — e.g. 'full commercial gym', 'home garage with barbell and rack', 'apartment with dumbbells only'."
12. "What equipment do you have regular access to? List anything relevant — e.g. barbell + rack, dumbbells (and up to what weight), pull-up bar, cable machine, kettlebells, resistance bands, machines (leg press, Smith, etc.)."
13. "Any exercises you prefer to avoid, can't do, or have strong preferences about? E.g. 'no Smith machine', 'bad shoulder so no overhead press', 'prefer barbell over machines for compounds'."
14. "Anything else I should know? (injuries, upcoming races, travel, etc.)"
15. "Do you include swimming in your training, or plan to? (Y / N / maybe)"

If answer to Q15 is **N**: skip Q16–Q17.
If answer is **Y or maybe**: ask:

16. "How would you describe your swimming? (e.g., 'complete beginner', 'comfortable in the pool — recreational', 'ex-club swimmer', 'triathlon background')"
17. "Do you have regular access to a pool? If so, is it a 25m or 50m pool? Any open water access?"
18. "What's your comfortable sustained swim pace per 100m? If you don't know, describe a recent swim (e.g., '1km in 22 minutes') and I'll estimate it. Or say 'unknown' — we can establish it with a CSS test set."

After collecting answers, fill in `athlete/profile.md` with the provided values, replacing all `[placeholder]` values. Write Q11 as free text under "Gym Setup", Q12 as a bullet list under "Available Equipment", and Q13 as a bullet list under "Exercise Preferences & Exclusions" (use "None specified" if no answer given). Write Q17 as free text under "Pool Access". If CSS (from Q18) is known or can be estimated from a recent swim, compute and fill in swim zones; otherwise leave as TBD.

Compute training zones from the provided FTP and max HR and fill in the zone tables.

### Step 3: Test Strava connectivity and optional historical sync

Run:
```
python3 scripts/fetch_activities.py --after [30 days ago date in YYYY-MM-DD format]
```

- If it exits with an error: display the error message and guide the user:
  - Check that `.env` has `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, and `STRAVA_REFRESH_TOKEN` set
  - If `STRAVA_REFRESH_TOKEN` is missing or empty: tell them to run `python scripts/strava_auth.py`
  - Refer them to `setup/SETUP.md` for step-by-step instructions
  - Then proceed to Step 4.

- If it succeeds (outputs a JSON array):
  - Count the activities in the array. Report: "Strava connection successful — found X activities."
  - If the array is empty (`[]`): note "No activities in the past 30 days." and proceed to Step 4.
  - If the array is non-empty: ask the user:

    > "I found X Strava activities from the past 30 days. Would you like me to sync them now to build a training history baseline? This will generate a weekly reflection and update your consistency log — useful context before your first /plan-workouts session.
    >
    > Y / N"

  - If **N**: note "Strava connected. Historical sync skipped." and proceed to Step 4.
  - If **Y**: run the full `/fetch-activities` workflow inline using the already-fetched activity JSON (do **not** re-run the fetch script — reuse the data from the successful call above). After the sync completes (reflection written, consistency log updated, `overview/strava-sync.json` updated, `overview/pending.md` regenerated), proceed to Step 4.

### Step 4: Hevy connectivity (optional)

Ask:
```
Do you have a Hevy Pro account? (Hevy Pro is required for API access — it enables pushing
workout routines directly to your Hevy app.)

Y / N / skip for now
```

- If **N or skip**: note "Hevy: skipped" and proceed to Step 5.
- If **Y**: proceed to Phase 2 below.

**Phase 2 — Collect API key:**

Ask:
```
Get your API key at: hevy.com/settings?developer
→ Log in → Settings → Developer → Generate Key

Paste your Hevy API key here:
```

- Write `HEVY_API_KEY=<key>` to `.env` (append if file exists, create if not — use the Edit tool)
- Run `python3 scripts/fetch_hevy_exercises.py` to populate the exercise cache
  - On success: note "Hevy: connected (X exercises cached)"
  - On failure: note the error message and tell the user to re-check the key or retry with `/sync-hevy-exercises`

### Step 5: Confirm and next steps

Print:
```
Profile saved to athlete/profile.md
Strava: [connected / needs setup]
Hevy:   [connected (X exercises cached) / skipped / needs setup]

Next steps:
- Run /plan-workouts to create your first training block
- Run /fetch-activities after completing workouts to log progress
- Run /push-workouts to sync weights sessions to Hevy
- Run /calendar to see your upcoming sessions
```
