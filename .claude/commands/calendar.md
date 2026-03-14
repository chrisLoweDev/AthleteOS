# /calendar — Show Upcoming Training Schedule

Displays all pending planned sessions as a formatted calendar. Also shows recently completed sessions for context.

## Steps

### Step 1: Collect all pending sessions

Glob `workouts/plans/**/*.md`. For each file, read the YAML frontmatter:
- `date`, `type`, `discipline`, `planned_duration_min`, `planned_distance_km`, `key_focus`, `status`, `week_folder`

Filter to only `status: pending`. Sort by `date` ascending.

### Step 2: Collect recently completed sessions

Glob `workouts/completed/**/*.md`. Filter to sessions with `date` within the last 7 days. These provide context.

### Step 3: Display the calendar

Group sessions by ISO week. For each week, render:

```
## Week YYYY-WXX  ([Mon date] – [Sun date])
Total planned: [X sessions, ~Y hours]

| Date | Day | Type | Duration | Key Focus | File |
|------|-----|------|----------|-----------|------|
| 2026-03-11 | Wed | 🚴 Cycling | 75 min | Threshold intervals | [plan](workouts/plans/2026-W11/2026-03-11-cycling-threshold.md) |
| 2026-03-13 | Fri | 🏃 Running | 50 min | Easy aerobic base | [plan](workouts/plans/2026-W11/2026-03-13-running-easy-base.md) |
| 2026-03-14 | Sat | 💪 Weights | 60 min | Lower body strength | [plan](workouts/plans/2026-W11/2026-03-14-weights-lower-body.md) |
```

Type emojis:
- Cycling → 🚴
- Running → 🏃
- Weights → 💪
- Swimming → 🏊

After each week's table, add a brief load note if relevant (e.g., "2 quality sessions this week — ensure recovery between Thu and Sat").

### Step 4: Show count summary

After all weeks:
```
Upcoming sessions: [N total]
  🚴 Cycling: [N sessions]
  🏃 Running: [N sessions]
  🏊 Swimming: [N sessions]
  💪 Weights: [N sessions]
  Spanning [X] days ([start date] to [end date])
```

### Step 5: Flag overdue or today's sessions

If any `status: pending` session has a `date` of today or earlier: flag it:

```
⚠️  You have a session due today or overdue:
- [date] [type]: [key focus]
Run /fetch-activities when you're done to log it.
```

### Step 6: Update overview/pending.md

Write the same session data to `overview/pending.md` (without the coaching notes, just the table):

```markdown
# Pending Workouts

_Last updated: YYYY-MM-DD_

| Date | Day | Type | Duration | Focus | Status | Plan |
|------|-----|------|----------|-------|--------|------|
| ... | ... | ... | ... | ... | pending | [link](...) |
```

### Step 7: Empty state handling

If no pending sessions exist anywhere:

```
No upcoming planned sessions.

Run /plan-workouts to create a new training block.
```

If the completed/ folder has recent sessions but no pending: mention this:
```
Your last [N] sessions have been completed. Time to plan the next block!
Run /plan-workouts to continue your training.
```
