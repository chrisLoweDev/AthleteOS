# /fetch-activities — Sync Strava and Generate Reflection

Syncs Strava data, matches activities to planned workouts, and generates a weekly reflection.

## Steps

### Step 1: Load state

Read `overview/strava-sync.json`. Note:
- `last_sync_timestamp`: the ISO 8601 datetime of the last successful sync (null if first run)
- `seen_ids`: array of Strava activity IDs already processed

Read `athlete/profile.md`. Load FTP, HR zones, threshold pace, and `coaching_mode` (default: `coach` if missing).

If `last_sync_timestamp` is null (first sync): ask the athlete "How far back should I look for activities? (e.g., 30 days, 90 days)" and compute the `--after` date from their answer.

Announce: "Last sync: [date or 'never']. Fetching new Strava activities..."

### Step 2: Fetch from Strava

Run:
```
python scripts/fetch_activities.py --after [last_sync_timestamp or computed date]
```

Parse the JSON output. If the command exits with a non-zero status, display the error and stop.

Filter out any activities whose `id` is already in `seen_ids` (already processed).

If the resulting list is empty: say "No new Strava activities since [date]" and stop.

### Step 3: Match activities to planned workouts

Glob `workouts/plans/**/*.md` and read frontmatter from all files with `status: pending`.

For each Strava activity, attempt to find a matching planned workout by:
1. Same calendar date from `start_date_local` (date part only, e.g., `2026-03-10`)
2. Same discipline: map Strava `sport_type` to plan `type`:
   - `Ride`, `VirtualRide`, `EBikeRide` → `cycling`
   - `Run`, `VirtualRun`, `TrailRun` → `running`
   - `WeightTraining`, `Workout` → `weights`
   - `Swim`, `OpenWaterSwim` → `swimming`
3. If multiple planned sessions on the same date with the same type: ask the athlete which Strava activity matches which plan

Track:
- **Matched pairs**: Strava activity + planned workout file
- **Unplanned activities**: Strava activity with no matching plan
- **Unmatched plans**: pending plans whose date has passed with no Strava match

### Step 4: Handle gaps and ambiguity

For each unmatched planned workout whose date is more than 1 day in the past:
- Ask: "I don't see a Strava activity matching your [type] session planned for [date]. Did you:
  a) Complete it (but forgot to save to Strava)
  b) Modify it significantly
  c) Skip it
  What happened?"
- Record the answer for the reflection.

For each Strava activity with no matching plan: note it as "unplanned session".

### Step 5: Weight training dialog

For each matched or unplanned activity where `sport_type` is `WeightTraining` or `Workout`:
- Ask: "I see a weight training session on [date] lasting [duration formatted as Xh Ym]. What did you work on? Please describe:
  - Muscle groups / focus
  - Main exercises, sets, reps, and weights (if you remember)
  - How it felt (RPE or notes)"
- Record the response. Do not block the sync if the athlete declines to provide detail ("I don't remember" is fine — write "No detail provided" in the reflection).

### Step 5a: Evaluate strength PRs (weight training sessions only)

Skip this step if no weight training activities were processed in Step 5.

**5a-1: Parse athlete's response** from Step 5 into per-exercise structured data:
- Normalize exercise names to canonical names: Back Squat, Romanian Deadlift, Bench Press, Overhead Press, Bent-Over Row, Pull-Ups
- For each set: weight (kg), reps completed, and any qualifier ("clean", "conservative", "failed", "dropped to N reps")
- Ignore accessory work (curls, lateral raises, core twists, etc.)

**5a-2: Read current PR table** from `athlete/profile.md` under `## Strength PRs`.

**5a-3: Evaluate PR conditions for each canonical exercise:**

| PR Type | Rule |
|---------|------|
| 5×5 Best | **Confirmed (no prefix):** all 5 sets × ≥5 reps clean, no drops, not conservative weight. **Estimated (`~` prefix):** ≥3 sets clean and no set drops below 4 reps — record `~weight`; conservative/return weight still disqualifies |
| Best 10-Rep Set | Highest weight for ≥10 reps in any single set; conservative sets excluded |
| Est. 1RM (Epley) | `weight × (1 + reps/30)` from best clean set; pick max across all clean sets; skip conservative sets; skip Pull-Ups |
| Pull-Ups | Track best single-set rep count as "BW × N reps"; no 1RM estimate |

**5a-4: Update `athlete/profile.md`** for any new PRs:
- Update the relevant columns (Est. 1RM, 5×5 Best, Best 10-Rep Set), set Last Updated to today's date, and update Notes
- Do not modify rows where no PR was achieved
- If a set was attempted but failed (e.g., "attempted 85kg — failed sets 4-5"), update Notes only

**5a-5: Compile PR summary** for use in Step 6 and Step 11:
```
New PRs this session: [list, or "none"]
No new PRs: [brief reason per exercise where attempted]
```

### Step 5b: Update working weights (weight training sessions only)

Skip this step if no weight training activities were processed in Step 5.

**5b-1: Read the workout library**

Read `athlete/workout-library.md`. If the file does not exist or is empty, skip this step and add a note to the reflection: "Workout library not found — working weights not updated. Run /setup to generate it."

**5b-2: Identify the routine**

For each completed weights session processed in Step 5:
- Identify which named routine it corresponds to (Full Body A or Full Body B) by checking the workout file's `key_focus` frontmatter field or filename slug
- If the routine cannot be determined, note it and skip progression checks for that session

**5b-3: Extract actual weights and reps**

From the athlete's Step 5 response and the completed workout file's tables:
- For each main lift, extract: exercise name, weight used, reps completed per set, number of sets

**5b-4: Double progression check**

For each main lift in the routine:
1. Did the athlete hit the **top of the working rep range** on **all working sets** in this session?
   - Working rep range is defined in the library's Main Lifts table (e.g., "4–8" means top is 8)
   - All working sets must hit the top number (warm-up sets excluded)
2. If yes for this session: glob `workouts/completed/**/` for the most recent prior file matching the same routine type (same Full Body A or Full Body B slug), sorted by date descending
   - Read that file and check whether the same exercise also hit the top of the rep range on all working sets
3. **Two consecutive sessions both at top of range → progression triggered:**
   - Increment that exercise's Target Weight in `athlete/workout-library.md` by **2.5 kg** (not 5 kg — conservative for Athletic/Hybrid archetype)
   - Add a note next to the updated weight: `(progressed [date])`
4. **Only one session qualifies:** no change to the library, but record a "near-progression" note for the reflection: "One more qualifying session at [weight] → triggers progression to [weight + 2.5 kg]"
5. **Neither session qualifies:** no change, no note needed

**5b-5: Update library header**

After processing all exercises, update the `**Working weights last updated:**` line in `athlete/workout-library.md` to today's date.

**5b-6: Compile progression summary**

Record for use in Step 6:
```
Weight progressions this sync:
  Triggered: [exercise → old weight → new weight, or "none"]
  Near-progressions: [exercise → current weight → next target, or "none"]
```

---

### Step 6: Generate weekly reflection

Determine the ISO week(s) of the fetched activities. Create a reflection file for each week involved: `workouts/reflections/YYYY-WXX-reflection.md`

**Adherence calculation:** Before writing the reflection, compute:
- Sessions planned (all pending files for this week at sync time)
- Sessions completed within ±10% tolerance of planned duration/distance
- Adherence = completed / planned, expressed as X/Y (Z%)
- Note any specific shortfalls (e.g., "Long ride: 84 min of 135 planned, 62%")

**Coaching tone:** Apply `coaching_mode` from profile.md to all narrative sections (Observations, Fitness Trajectory, Recommendation). The Session Analysis Notes per session should also reflect the mode. Mode definitions are in CLAUDE.md under Core Behaviors → Coaching Mode.

Reflection structure:
```markdown
# Week YYYY-WXX Reflection

_Generated: [today's date]_

## Summary
- **Total sessions:** [N]
- **Total time:** [Xh Ym]
- **Plan Adherence:** [X/Y sessions (Z%)] — [brief note on shortfalls, or "all sessions on target"]
- **Disciplines:** [Cycling: Xh | Running: Y km | Swimming: Z m | Weights: N sessions]

## Session Analysis

### [Date] — [Type]: [Activity Name]
- **Planned:** [duration/distance/intensity from plan file]
- **Actual:** [duration/distance/avg power or pace/avg HR from Strava]
- **Result:** [on target / over / under] (±10% tolerance)
- **Notes:** [AI coaching observation — 1-2 sentences, tone per coaching_mode]

[Repeat for each matched pair]

### Unplanned Sessions
[List any unplanned activities with brief note]

### Missed / Skipped Sessions
[List any plans that were not completed, with athlete's explanation]

### Weight Training Detail
[Insert athlete's responses from Step 5]

**Strength PRs:** [Insert Step 5a PR summary — "New PRs: ..." or "No new PRs this session"]

### Strength Progression
[Insert Step 5b progression summary — triggered progressions and near-progressions, or omit section if no weight training this week]

## Observations
[3-5 bullet points: patterns, trends, what went well, what to watch — tone per coaching_mode]

## Fitness Trajectory
[Based on consistency-log: is load trending up/down/stable? — tone per coaching_mode]

## Goal Trajectory
[Only include if Performance Targets are defined in athlete/profile.md. For each target: current status vs goal, gap, and whether on track. In accountability mode, name the gap plainly.]

## Recommendation for Coming Week
[One concrete suggestion based on this week's data — tone per coaching_mode]
```

If a reflection file already exists for a week (from a previous partial sync), append a new dated section rather than overwriting.

### Step 7: Update workout statuses and move files

For each matched workout (athlete confirmed completed):
1. Edit the plan file: change `status: pending` → `status: completed`, add `strava_activity_id: [id]`
2. Move the file from `workouts/plans/YYYY-WXX/filename.md` to `workouts/completed/YYYY-WXX/filename.md`
   - Create the `completed/YYYY-WXX/` folder if it doesn't exist

For confirmed missed/skipped workouts: change `status: pending` → `status: missed` (keep in plans folder).

For athlete-confirmed-completed workouts with no Strava data: change `status: pending` → `status: completed`, add a note in frontmatter: `note: "completed without Strava"`.

### Step 8: Update consistency log

Read `athlete/consistency-log.md`. For the synced week(s), compute:
- Cycling: session count, total distance (km), total duration
- Running: session count, total distance (km)
- Swimming: session count, total distance (meters), total duration
- Weights: session count
- Total hours across all disciplines
- **Plan Adherence:** sessions completed within ±10% tolerance / sessions planned (e.g., "3/4 (75%)"). Note any specific shortfalls in the Notes column (e.g., "Long ride: 62% duration").

Add or update the row for each week. Ensure the Weekly Totals table has a `Plan Adherence` column. Prune any rows for weeks older than 12 weeks.

### Step 9: Update sync state

Write updated `overview/strava-sync.json`:
```json
{
  "last_sync_timestamp": "[ISO 8601 datetime of now]",
  "seen_ids": [existing IDs + new activity IDs from this sync]
}
```

### Step 10: Regenerate pending table

Glob all `workouts/plans/**/*.md` files with `status: pending`. Regenerate `overview/pending.md` as a sorted table.

### Step 11: Summary to athlete

Print a human-readable summary. Apply `coaching_mode` tone to the narrative portions.

```
Sync complete — [date]
  Activities fetched: [N]
  Matched to plans: [N]
  Unplanned: [N]
  Missed/skipped: [N]
  Plan adherence: [X/Y sessions (Z%)]

Reflection written: workouts/reflections/[week]-reflection.md
Consistency log updated: athlete/consistency-log.md
[If at least one PR value changed: Strength PRs updated: athlete/profile.md]

[Narrative summary — tone per coaching_mode:
  coach: brief encouraging pattern observation + forward look
  accountability: plain statement of adherence and gap vs event requirements (name shortfalls directly)
  data: bullet list of key numbers only — no narrative]

[Any issues or action items for the athlete]
```
