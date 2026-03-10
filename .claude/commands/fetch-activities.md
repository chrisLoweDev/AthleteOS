# /fetch-activities — Sync Strava and Generate Reflection

Syncs Strava data, matches activities to planned workouts, and generates a weekly reflection.

## Steps

### Step 1: Load state

Read `overview/strava-sync.json`. Note:
- `last_sync_timestamp`: the ISO 8601 datetime of the last successful sync (null if first run)
- `seen_ids`: array of Strava activity IDs already processed

Read `athlete/profile.md`. Load FTP, HR zones, threshold pace.

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

### Step 6: Generate weekly reflection

Determine the ISO week(s) of the fetched activities. Create a reflection file for each week involved: `workouts/reflections/YYYY-WXX-reflection.md`

Reflection structure:
```markdown
# Week YYYY-WXX Reflection

_Generated: [today's date]_

## Summary
- **Total sessions:** [N]
- **Total time:** [Xh Ym]
- **Disciplines:** [Cycling: Xh | Running: Y km | Weights: N sessions]

## Session Analysis

### [Date] — [Type]: [Activity Name]
- **Planned:** [duration/distance/intensity from plan file]
- **Actual:** [duration/distance/avg power or pace/avg HR from Strava]
- **Result:** [on target / over / under] (±10% tolerance)
- **Notes:** [AI coaching observation — 1-2 sentences]

[Repeat for each matched pair]

### Unplanned Sessions
[List any unplanned activities with brief note]

### Missed / Skipped Sessions
[List any plans that were not completed, with athlete's explanation]

### Weight Training Detail
[Insert athlete's responses from Step 5]

## Observations
[3-5 bullet points: patterns, trends, what went well, what to watch]

## Fitness Trajectory
[Based on consistency-log: is load trending up/down/stable?]

## Recommendation for Coming Week
[One concrete suggestion based on this week's data]
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
- Weights: session count
- Total hours across all disciplines

Add or update the row for each week. Prune any rows for weeks older than 12 weeks.

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

Print a human-readable summary:
```
Sync complete — [date]
  Activities fetched: [N]
  Matched to plans: [N]
  Unplanned: [N]
  Missed/skipped: [N]

Reflection written: workouts/reflections/[week]-reflection.md
Consistency log updated: athlete/consistency-log.md

[Any issues or action items for the athlete]
```
