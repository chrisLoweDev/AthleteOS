# /plan-workouts — Plan Upcoming Training Sessions

Generates a personalized training block through a dialog with the athlete. Creates individual workout markdown files and updates the pending table.

**Arguments:** `$ARGUMENTS` may contain `[days] [context]` — e.g., `/plan-workouts 14 "race in 3 weeks"`. Parse these if present, otherwise ask.

## Steps

### Step 1: Load athlete context

Read `athlete/profile.md`:
- FTP and last test date
- Running threshold pace
- Swim CSS and pool access
- Max HR, resting HR
- Current goals
- Weekly availability (available days + max hours)
- Any notes (injuries, upcoming events)
- `coaching_mode` (default: `coach` if missing) — apply mode tone to session annotations and any advice embedded in workout files

Read `athlete/workout-library.md` for the standard weight training sessions, current working weights, and substitution rules. Always use these when scheduling weights sessions — do not invent exercises or weights from scratch.

Read the `Strength Archetype:` field from `athlete/profile.md`. Look up the matching archetype ruleset in the `## Weight Training Archetypes` section of CLAUDE.md. Apply those programming variables to all weights sessions in this planning block.

Read `data/hevy-exercises.json` if it exists:
- Extract the set of exercise name keys from `exercises`
- For weights sessions, **only use exercise names present as keys in the cache** — these are the exact names Hevy recognises
- If the cache is missing, warn: "data/hevy-exercises.json not found — using workout-library names only. Run /sync-hevy-exercises before pushing to Hevy."

Read `overview/strava-sync.json` to understand recent training history.

Read `athlete/consistency-log.md` to understand the 12-week volume trend across disciplines. Note any patterns (e.g. declining cycling volume, missed weeks) that should influence load targets or session counts in the new plan.

Read the most recent file in `workouts/reflections/` for current fitness context and recent load.

Glob `journals/**/*.md` sorted by date descending — read the most recent 2–3 entries. Note any signals (fatigue ≥ 4, energy ≤ 2, stress ≥ 4, soreness) that should influence the plan structure. Surface these briefly when proposing the training structure in Step 4 (e.g., "Recent journals flag high stress — I've kept quality sessions lighter this week").

### Step 2: Check for pending sessions

Glob `workouts/plans/**/*.md` and count files with `status: pending`.

**If pending sessions exist:** List them in a table:

```
You have [N] pending planned sessions:

| Date | Day | Type | Key Focus |
|------|-----|------|-----------|
| ...  | ... | ...  | ...       |

(Last session: [date])

How should I proceed?
A) Replace all pending sessions with a fresh plan
B) Start planning after the last pending session ([date])
C) Keep existing sessions and plan around them
D) Cancel — keep the current plan as-is
```

Wait for answer:
- **A**: Mark all pending files `status: archived` (edit frontmatter, keep files in place). Then plan from today.
- **B**: Set planning start date to the day after the last pending session's date.
- **C**: Note all booked dates and avoid them when scheduling new sessions.
- **D**: Stop.

**If no pending sessions:** proceed to Step 3.

### Step 3: Gather planning context

If not already provided in `$ARGUMENTS`, ask (you may ask all questions at once):

1. "How many days ahead should I plan? (default: 7)"
2. "What's the context for this training block? (e.g., normal week, race prep, travel, recovery week)"
3. "How are you feeling physically right now? (fresh / normal / fatigued)"
4. "Any days that are completely unavailable for training?"
5. "Any upcoming races, events, or travel I should account for?"
6. "Any muscle soreness, niggles, or injuries I should work around?"

Parse the planning window from `$ARGUMENTS` if present, confirming with the athlete before proceeding.

### Step 4: Design the training structure

Based on the athlete's profile, recent load, fatigue level, and the planning context:

**Distribution principles:**
- **Polarized model**: mostly Z1/Z2 aerobic work with 1–2 quality sessions per discipline per week
- Never schedule hard sessions (Z4+, heavy weights) on back-to-back days
- Z2 cycling or easy running can follow any session
- Easy swimming (Z1/Z2) can follow any session. Do not schedule Z4/Z5 swim intervals on the same day as Z4+ cycling or heavy weights.
- If athlete mentions a race within the window: apply taper in final 5–7 days (−40% volume, −20% intensity)
- Respect the athlete's stated available days from `athlete/profile.md`
- **Weights sessions (Athletic/Hybrid archetype):** Select the appropriate named routine from `workout-library.md` (alternate Full Body A / Full Body B unless context suggests otherwise — e.g., upper-only if legs needed fresh for a ride). Apply double progression: show current working weight from the library and note the rep target range. Always include the Mobility Close block — do not omit it. No heavy lower body (squat, hinge) within 48h before a Z4+ cycling session or long Z2 ride (>2hr). Never schedule weights on consecutive days.

**Compute per-discipline session counts** based on available days and max weekly hours.

**Propose the plan structure** before writing any files:

```
Here's the training structure I'm proposing:

Week YYYY-WXX
| Date | Day | Type | Duration | Key Focus |
|------|-----|------|----------|-----------|
| ...  | ... | ...  | ...      | ...       |

Total: [X sessions, ~Y hours/week]

Does this structure work, or should I adjust anything?
(Reply with changes or just say "looks good" to generate the files)
```

Wait for approval. Adjust and re-propose if the athlete requests changes. Only proceed to Step 5 after confirmation.

### Step 5: Generate workout files

For each approved session:

1. Determine the ISO week folder: `workouts/plans/YYYY-WXX/`
2. Create the folder if it doesn't exist
3. Generate the filename: `YYYY-MM-DD-[type]-[slug].md`

Use the appropriate template based on type. Fill in all targets using values computed from `athlete/profile.md`:

**Cycling file template:**
```markdown
---
date: YYYY-MM-DD
type: cycling
discipline: Ride
status: pending
planned_duration_min: [X]
planned_distance_km: [X or null]
week_folder: YYYY-WXX
key_focus: "[description]"
strava_activity_id: null
---

# [YYYY-MM-DD] Cycling: [Session Name]

**Date:** [Day, DD Month YYYY]
**Duration:** [X] min | **TSS est:** [X]

## Warm Up ([X] min)
- [Specific warm-up instructions with zone/watt targets]

## Main Set
- [Intervals or sustained effort with specific watt ranges computed from FTP]
- [Recovery instructions]

## Cool Down ([X] min)
- [Cool-down instructions]

## Notes
FTP reference: [W]W (from athlete/profile.md)
[Any session-specific coaching notes]
```

**Running file template:**
```markdown
---
date: YYYY-MM-DD
type: running
discipline: Run
status: pending
planned_duration_min: [X]
planned_distance_km: [X]
week_folder: YYYY-WXX
key_focus: "[description]"
strava_activity_id: null
---

# [YYYY-MM-DD] Running: [Session Name]

**Date:** [Day, DD Month YYYY]
**Target Distance:** [X] km | **Duration:** ~[X] min

## Warm Up
- [Warm-up with pace targets computed from threshold pace]

## Main Set
- [Specific intervals or sustained run with pace ranges]

## Cool Down
- [Cool-down instructions]

## Notes
Threshold pace reference: [min/km] (from athlete/profile.md)
[Any session-specific coaching notes]
```

**Weights file template:**
```markdown
---
date: YYYY-MM-DD
type: weights
discipline: WeightTraining
status: pending
planned_duration_min: [X]
planned_distance_km: null
week_folder: YYYY-WXX
key_focus: "[Upper/Lower/Full Body] strength"
strava_activity_id: null
hevy_routine_id: null
---

# [YYYY-MM-DD] Weights: [Session Name]

**Date:** [Day, DD Month YYYY]
**Duration:** ~[X] min | **Focus:** [Upper/Lower/Full Body]

## Warm Up
- [5-10 min activation]

## Main Lifts

**IMPORTANT FORMAT RULE — Hevy push compatibility:**
Sets and Reps MUST be plain integers. Use one row per set group (warm-up sets on
one row, working sets on another). Do NOT use compound strings like
"2 warm-up + 5 working" or slash-separated values like "6 / 6 / 5 / 5 / 5".
The "Warm-up sets" or "Working sets" note in the Notes column determines set type.

| Exercise | Sets | Reps | Target Weight | Actual Weight | Notes |
|----------|------|------|---------------|---------------|-------|
| [Exercise] | 2 | 6 | [warm-up kg] | | Warm-up sets |
| [Exercise] | 5 | 5 | [working kg] | | Working sets |

## Accessory Work

| Exercise | Sets | Reps | Target Weight | Actual Weight |
|----------|------|------|---------------|---------------|
| [Exercise] | [N] | [N] | [kg] | |

## Cool Down
- [Stretching/mobility]

## Notes
Fill in "Actual Weight" during/after the session.
[Any session-specific coaching notes]
```

**Swimming file template:**
```markdown
---
date: YYYY-MM-DD
type: swimming
discipline: Swim
status: pending
planned_duration_min: [X]
planned_distance_m: [X]
week_folder: YYYY-WXX
key_focus: "[description]"
strava_activity_id: null
---

# [YYYY-MM-DD] Swimming: [Session Name]

**Date:** [Day, DD Month YYYY]
**Target Distance:** [X]m | **Duration:** ~[X] min

## Warm Up ([X]m)
- [Easy swimming at Z1/Z2 pace — CSS + 15–20 sec/100m]

## Main Set
- [Intervals or sustained effort with pace ranges in min:sec/100m computed from CSS]
- [Rest intervals between sets]

## Cool Down ([X]m)
- [Easy cool-down at recovery pace]

## Notes
CSS reference: [min:sec]/100m (from athlete/profile.md)
Pool: [25m / 50m / open water]
[Any session-specific coaching notes]
```

### Step 6: Update pending table

After creating all files, regenerate `overview/pending.md`:

```markdown
# Pending Workouts

_Last updated: YYYY-MM-DD_

| Date | Day | Type | Duration | Focus | Status | Plan |
|------|-----|------|----------|-------|--------|------|
| ... | ... | ... | ... | ... | pending | [link](../workouts/plans/...) |
```

Sort by date ascending. Include only `status: pending` files.

### Step 7: Confirmation summary

```
Created [N] workout files:
  [list each file created]

Planning window: [start date] to [end date]
Earliest session: [date + type]
Next up: [date + type + key focus]

Run /calendar to see your full schedule.
Run /fetch-activities after completing sessions to log progress.
```
