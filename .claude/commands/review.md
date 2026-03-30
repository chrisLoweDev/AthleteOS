# /review — Weekly Training Review

Runs a full Strava sync and then generates a narrative weekly summary with trends and recommendations. Optionally flows into planning the next week.

## Steps

### Step 1: Run fetch-activities

Execute all steps defined in `.claude/commands/fetch-activities.md`.

This will:
- Sync Strava activities
- Match to plans
- Ask about weight training and missed sessions
- Generate the reflection file
- Update the consistency log and sync state

### Step 2: Load 4-week trend data

Read `athlete/consistency-log.md`. Extract the last 4 weeks of data for each discipline.

Glob `journals/**/*.md` sorted by date descending — read the entries from the current week. Count and note: how many entries flagged fatigue ≥ 4, energy ≤ 2, stress ≥ 4. This will be surfaced in Step 3.

### Step 3: Generate narrative weekly summary

After the reflection is written, produce a human-readable narrative summary (distinct from the reflection's session-by-session breakdown).

Read `coaching_mode` from `athlete/profile.md` (default: `coach` if missing). Apply the corresponding tone to all narrative sections. Mode definitions are in CLAUDE.md under Core Behaviors → Coaching Mode.

Structure:
```
## Weekly Review — Week YYYY-WXX

### Training Load
[Compare this week's total volume and intensity to last week.
E.g., "Volume was up 15% from last week (7h vs 6h). Intensity was similar."
accountability mode: include plan adherence % explicitly here.]

### Plan Adherence
[Only include as a standalone section in accountability mode.
State: X/Y sessions completed within tolerance (Z%). Name each shortfall with specifics — duration %, zone deviation, etc.]

### Key Wins
- [Specific session that went particularly well]
- [PR or personal milestone if applicable]
- [Consistency streak or other positive pattern]
[data mode: bullet list of metrics only, no prose]

### Areas to Address
- [Missed sessions or underperformance]
[coach mode: stated constructively
accountability mode: named plainly — "this is the Nth consecutive week without X"; no softening until the shortfall is named
data mode: numbers only — "N sessions missed, Y% below planned volume"]

### Goal Trajectory
[Only include if Performance Targets are defined in athlete/profile.md.
For each target: where the athlete is now, what the goal requires, and the gap.
accountability mode: state gaps plainly and compare to time remaining before deadline.
data mode: table format — Target | Current | Goal | Gap | Deadline]

### Subjective Signals This Week
[Only include this section if journal entries exist for the week. Summarise patterns.
If no entries: omit this section entirely.]

### 4-Week Trajectory
[Based on consistency-log trends: is the athlete building, maintaining, or declining?
Mention each discipline separately if the trends differ.]

### Recommendation for Next Week
[One concrete, actionable suggestion.
coach mode: forward-looking and encouraging
accountability mode: directly tied to the biggest adherence or goal gap this week
data mode: one sentence — the metric that most needs attention and why]
```

### Step 4: Offer to plan next week

After the summary, ask:

```
Would you like to plan the next training week now?
(yes / no)
```

If yes: immediately run all steps from `.claude/commands/plan-workouts.md`.

If no: print:
```
When you're ready, run /plan-workouts to set up your next training block.
```
