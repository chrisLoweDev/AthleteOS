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

### Step 2.5: Generate workout library (weight training only)

Skip this step if weight training was **not** selected in Step 2.

**2.5-1: Load sources**
- Read `athlete/profile.md` — get: archetype, gym setup, available equipment, exercise preferences/exclusions
- Read `data/hevy-exercises.json` if it exists — use only exercise names present as keys when referencing Hevy-compatible exercises
  - If the file does not exist: warn inline: "Exercise cache not found — generating library with placeholder exercise names. Run /sync-hevy-exercises and verify names before /push-workouts."
- The archetype ruleset and session structure template are defined in CLAUDE.md under "Weight Training Archetypes" — apply the matching archetype's rules

**2.5-2: Derive available movement patterns from equipment**

Before generating any routines, map the athlete's available equipment (from `profile.md`) to the movement patterns it supports:

| Equipment present | Movement patterns unlocked |
|---|---|
| Barbell + rack | Squat, Hinge, H-Push (bench), H-Pull (row), V-Push (OHP) |
| Pull-up bar / rig | V-Pull |
| Dumbbells | H-Push, H-Pull, V-Push, Hinge (RDL), Squat (goblet) — reduced loading ceiling |
| Cable machine | H-Pull, V-Pull, H-Push (cable), core |
| Resistance bands only | H-Pull (face pull), V-Pull (lat pulldown band), limited H-Push |
| Bodyweight only | V-Pull (if bar available), Squat (BW), Hinge (glute bridge), Core |

Note any movement patterns the athlete cannot train with available equipment. If a pattern is missing entirely (e.g., no vertical pull option at all), flag it: "No vertical pull option available with current equipment — lat development will be limited. Consider adding a pull-up bar or cable attachment."

Also apply any exclusions from the athlete's "Exercise Preferences & Exclusions" field — treat excluded exercises as unavailable and substitute at this stage.

**2.5-3: Generate routines — number and structure by archetype**

The number of routines and session structure varies by archetype:

| Archetype | Frequency | Split | Routines to generate |
|---|---|---|---|
| Athletic/Hybrid | 2×/week | Full body (never split at this frequency) | Full Body A, Full Body B |
| Strength | 3–4×/week | Upper/Lower preferred; PPL acceptable | Upper A, Upper B, Lower A, Lower B (or Push, Pull, Legs if PPL) |
| Hypertrophy | 3–4×/week | Push/Pull/Legs preferred | Push, Pull, Legs |
| Metabolic | 2–3×/week | Circuit format | Circuit A (lower-focus), Circuit B (upper-focus); add Circuit C (full body) if 3×/week |
| General Fitness | 2–3×/week | Full body | Full Body A, Full Body B; add Full Body C if 3×/week |

For each archetype, use only the movement patterns available from the equipment audit above. Map patterns to routines as follows:

**Athletic/Hybrid:**
- Full Body A — Squat primary / Horizontal Push / Horizontal Pull
- Full Body B — Hinge primary / Vertical Push / Vertical Pull

**Strength (Upper/Lower):**
- Upper A — Horizontal Push primary / Horizontal Pull
- Upper B — Vertical Push primary / Vertical Pull
- Lower A — Squat primary + accessory hinge
- Lower B — Hinge primary (deadlift) + accessory squat

**Strength (PPL):**
- Push — Horizontal Push + Vertical Push (chest/shoulder/tricep)
- Pull — Horizontal Pull + Vertical Pull (back/bicep)
- Legs — Squat + Hinge (quad/hamstring/glute)

**Hypertrophy:**
- Push — Horizontal Push + Vertical Push, higher volume (3–5 sets × 8–15 reps)
- Pull — Horizontal Pull + Vertical Pull, higher volume
- Legs — Squat + Hinge, higher volume

**Metabolic:**
- Circuit A — Lower-focus: Squat, Hinge, single-leg, core in superset/circuit format (30–60 sec rest)
- Circuit B — Upper-focus: H-Push, H-Pull, V-Push, V-Pull in superset/circuit format
- Circuit C (if 3×/week) — Full body: mixed patterns, AMRAP or timed sets

**General Fitness:**
- Full Body A — Squat + Horizontal Push + Horizontal Pull + Core
- Full Body B — Hinge + Vertical Push + Vertical Pull + Core
- Full Body C (if 3×/week) — Full body, varied exercise selection from A/B substitutions

If the athlete's available equipment prevents a full pattern from being programmed in a given routine, note it in that routine's Substitutions section and skip the missing pattern rather than inventing an exercise that requires unavailable equipment.

**2.5-4: Section structure for each routine**

Each routine must include all five sections:

1. **Warm Up** — activation drills appropriate for the day's primary patterns (5–10 min)
2. **Main Lifts** — table with columns: Exercise | Sets | Reps | Target Weight | Notes
3. **Accessory Work** — table with columns: Exercise | Sets | Reps | Target Weight | Notes
4. **Core** — table with columns: Exercise | Sets | Duration/Reps | Notes
5. **Mobility Close** — 10 min, listed as bullet drills relevant to the session's movement patterns
6. **Substitutions** — bullet list of swap options for each main lift (equipment or preference alternatives)

**2.5-5: Working weights**

Start conservative:
- Main barbell lifts: ~60% of estimated 1RM (use bodyweight and archetype as reference — if no 1RM data exists, use beginner-appropriate starting weights and note this)
- Pull-ups and split squats: bodyweight (no added load)
- Add a note in the library header: "Starting weights are conservative estimates. Update after first 1–2 sessions."

**2.5-6: Write the library**

Write the completed library to `athlete/workout-library.md`, replacing any existing content. Use this header format:

```markdown
# Workout Library

**Archetype:** [archetype name]
**Working weights last updated:** [today's date]
**Note:** Starting weights are conservative estimates. Update after first 1–2 sessions.

---
```

Write each routine under a `##` heading matching its name (e.g., `## Full Body A`, `## Upper A`, `## Push`).

Confirm: "Workout library generated: [list routine names] written to athlete/workout-library.md"

---

### Step 3: Test Strava connectivity and optional historical sync

Before running the fetch, check whether `.env` contains all three Strava keys (`STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, `STRAVA_REFRESH_TOKEN`):

**If `STRAVA_CLIENT_ID` or `STRAVA_CLIENT_SECRET` are missing:**

Say:
> "Strava isn't connected yet. You'll need to create a free Strava API app — it takes about 2 minutes:
>
> 1. Go to https://www.strava.com/settings/api (log in if prompted)
> 2. Fill in: Application Name (anything), Category (any), Website (`http://localhost`), Authorization Callback Domain: `localhost`
> 3. Click **Create**
> 4. On the same page, find your **Client ID** and **Client Secret**
> 5. Paste both here and I'll set up your `.env` file."

Once the user provides the Client ID and Secret, write them to `.env`:
- `STRAVA_CLIENT_ID`
- `STRAVA_CLIENT_SECRET`

**If `STRAVA_REFRESH_TOKEN` is missing (or after writing Client ID + Secret above):**

Tell the user:
> "Now I'll open the Strava authorization page in your browser. Approve access, then come back here — the token will be saved automatically."

Run:
```
python3 scripts/strava_auth.py
```

Wait for the script to complete. It opens a browser, captures the OAuth callback on port 8080, and writes `STRAVA_REFRESH_TOKEN` to `.env` automatically. Do not ask the user to paste a token — the script handles everything.

If the script exits with an error, display the error and ask the user to verify their Strava app has Authorization Callback Domain set to `localhost`.

**Note:** Do not ask the user to copy a refresh token from the Strava settings page. The token shown there has insufficient scope (`read` only) and cannot be used to fetch activities. The OAuth flow via `strava_auth.py` is the only supported method.

Once `.env` has all three keys, run:
```
python3 scripts/fetch_activities.py --after [30 days ago date in YYYY-MM-DD format]
```

- If it exits with an error: display the error message, then handle as follows:
  - If the error mentions auth/credentials: tell the user to re-run `python3 scripts/strava_auth.py` to refresh the token, then retry.
  - On failure after re-auth: display the error and ask the user to verify their Strava API app has Authorization Callback Domain set to `localhost`.
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
