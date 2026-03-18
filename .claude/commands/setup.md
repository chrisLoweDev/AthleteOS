# /setup — First-Time Onboarding

Run this command once to set up your Athlete OS profile and verify Strava connectivity.

## Steps

### Step 1: Check profile status

Read `athlete/profile.md`. Look for lines containing `[` characters (unfilled placeholders).

- If the profile appears complete (no `[` characters), skip to Step 3.
- If placeholders exist, proceed to Step 2.

### Step 2: Interactive profile setup

Collect the following information via dialog with the user. **Ask questions one at a time, in sequence. Each question should be sent as a separate message — do not batch multiple questions together. Wait for the user's answer before asking the next question.** Only write the completed profile once all relevant questions have been answered.

**A. Start with basics:**

1. "What's your name?"
2. "What's your current body weight in kg? (or press Enter to skip)"

**B. Discipline selection — ask this before any sport-specific questions:**

3. "Which of the following do you include in your training? Select all that apply:
   - Cycling
   - Running
   - Swimming
   - Weight training"

Wait for the answer, then proceed through sections C–F only for the disciplines the athlete selected.

**C. Cycling (only if selected):**

4. "What's your current Cycling FTP in watts? (if you don't know, we can estimate later)"
5. "When did you last test your FTP? (date, or 'never')"

**D. Running (only if selected):**

6. "What's your Running Threshold Pace? (e.g., 4:45/km — this is your sustainable 1-hour race pace)"

**E. Swimming (only if selected):**

7. "How would you describe your swimming background? (e.g., 'complete beginner', 'comfortable recreational swimmer', 'ex-club swimmer', 'triathlon background')"
8. "Do you have regular access to a pool? If so, is it a 25m or 50m pool? Any open water access?"
9. "What's your comfortable sustained swim pace per 100m? If you don't know, describe a recent swim (e.g., '1km in 22 minutes') and I'll estimate it. Or say 'unknown' — we can establish it with a CSS test set."

**F. Weight training (only if selected):**

10. "Do you train at a commercial gym, home gym, or somewhere else? Describe your setup briefly — e.g. 'full commercial gym', 'home garage with barbell and rack', 'apartment with dumbbells only'."
11. "What equipment do you have regular access to? List anything relevant — e.g. barbell + rack, dumbbells (and up to what weight), pull-up bar, cable machine, kettlebells, resistance bands, machines (leg press, Smith, etc.)."
12. "Any exercises you prefer to avoid, can't do, or have strong preferences about? E.g. 'no Smith machine', 'bad shoulder so no overhead press', 'prefer barbell over machines for compounds'."

**G. General (ask for everyone, after discipline-specific questions):**

13. "What's your Max HR in bpm? (or press Enter to skip)"
14. "What's your Resting HR in bpm? (or press Enter to skip)"
15. "What are your primary training goals? (e.g., complete a triathlon, improve cycling FTP, run a half marathon)"
16. "Which days of the week are you available to train? (e.g., Mon, Wed, Thu, Sat, Sun)"
17. "What's your maximum training hours per week? (e.g., 8)"
18. "Anything else I should know? (injuries, upcoming races, travel, etc.)"

After collecting all answers, fill in `athlete/profile.md` with the provided values, replacing all `[placeholder]` values. For disciplines not selected, leave the relevant profile sections as TBD/N/A. Write Q10 as free text under "Gym Setup", Q11 as a bullet list under "Available Equipment", and Q12 as a bullet list under "Exercise Preferences & Exclusions" (use "None specified" if no answer given). Write Q8 as free text under "Pool Access". If CSS (from Q9) is known or can be estimated from a recent swim, compute and fill in swim zones; otherwise leave as TBD.

Compute training zones from the provided FTP and max HR (for selected disciplines) and fill in the zone tables.

### Step 3: Test Strava connectivity and optional historical sync

Run:
```
python3 scripts/fetch_activities.py --after [30 days ago date in YYYY-MM-DD format]
```

- If it exits with an error: display the error message, then handle as follows:
  - If `STRAVA_REFRESH_TOKEN` is missing, invalid, or the error mentions auth/credentials: offer to run the authorization for them. Say something like:
    > "Strava isn't authorized yet. I can run the authorization flow for you — a browser window will open and you'll just click Authorize on Strava's site. To do this, I'll need your AthleteOS Client ID and Client Secret (provided by whoever shared this with you). Paste them here and I'll take care of the rest."
  - Once the user provides the CLIENT_ID and CLIENT_SECRET, run: `python3 scripts/strava_auth.py --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET>`
  - On success: confirm "Strava authorized as [name]. Credentials saved." and re-run the fetch to confirm connectivity before proceeding to Step 4.
  - On failure: display the error and refer them to `setup/SETUP.md` Step 1 for troubleshooting.
  - Do **not** tell the user to register their own Strava API app.
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
