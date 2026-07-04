# /review — Weekly Training Review

Runs a full Strava sync and then generates a narrative weekly summary with trends and recommendations. Optionally flows into planning the next week.

## Steps

### Step 1: Run fetch-activities

Execute all steps defined in `.claude/commands/fetch-activities.md`.

This will:
- Sync Strava activities
- Match to plans
- Ask about weight training and missed sessions
- Write `## Actual` sections to completed workout files
- Update the consistency log and sync state

### Step 2: Generate weekly reflection

**Data source:** Read all completed workout files from `workouts/completed/YYYY-WXX/` for the current week. Each file contains both the original plan and an `## Actual` section written by fetch-activities. Derive all planned vs. actual comparisons from these files — do not re-fetch from Strava. Also read missed/skipped plans from `workouts/plans/YYYY-WXX/` (status: missed).

Determine the ISO week(s) covered. Create a reflection file for each week: `workouts/reflections/YYYY-WXX-reflection.md`

**Adherence calculation:** Before writing the reflection, compute:
- Sessions planned (completed + missed files for this week)
- Sessions completed within ±10% tolerance of planned duration/distance (compare `## Actual` duration/distance vs frontmatter `planned_duration_min` / `planned_distance_km`)
- Adherence = completed-within-tolerance / sessions planned, expressed as X/Y (Z%)
- Note any specific shortfalls (e.g., "Long ride: 84 min of 135 planned, 62%")

**Intensity audit (cycling sessions only):** For each cycling session, read the `## Actual` section of the completed file and compare against the plan:

1. **Determine planned zone** — read the plan file to identify the target zone (e.g., Z2 endurance, Z4 threshold intervals).

1. **Determine planned zone** — read the plan file to identify the target zone (e.g., Z2 endurance, Z4 threshold intervals).
2. **Assess actual intensity** — use Avg Power and Normalized Power from `## Actual`, compare against FTP zones from `athlete/profile.md`. Use Peak Efforts (5min, 20min) from `## Actual` to assess whether the athlete spent meaningful time above the planned zone.
3. **Flag and contextualise any divergence:**
   - If avg power is in a higher zone than planned: note this explicitly. Then assess whether it was likely driven by route/terrain (unavoidable climbs), group dynamics, or a deliberate choice — and state the likely cause.
   - If avg power is on target but peak efforts (e.g., 5min power) are well into Z4/Z5: note that average hides intensity spikes. Clarify that brief hard efforts on climbs within an otherwise Z2 ride are normal and generally fine — but flag if they were frequent or prolonged enough to affect recovery.
   - If avg power is below plan (e.g., Z1 when Z3 was planned): flag as underperformance and note impact.
4. **Provide a recovery implication:** state whether the intensity exceedance is likely to require additional recovery time before the next hard session, or whether it is inconsequential. Reference the next planned session in `overview/pending.md` if relevant.

This audit replaces the simple "on target / over / under" Result line for cycling sessions — include it as an **Intensity** sub-field alongside the Result line in the session analysis block.

**Coaching tone:** Apply `coaching_mode` from profile.md to all narrative sections (Observations, Fitness Trajectory, Recommendation). Mode definitions are in CLAUDE.md under Core Behaviors → Coaching Mode.

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
- **Planned:** [duration/distance/intensity from plan file frontmatter and body]
- **Actual:** [from `## Actual` section of completed file — duration, distance, avg power or pace, avg HR]
- **Result:** [on target / over / under] (±10% tolerance on duration/distance)
- **Intensity:** *(cycling only)* [planned zone vs Avg/NP from `## Actual`; note Peak Efforts and recovery implication]
- **Notes:** [AI coaching observation — 1-2 sentences, tone per coaching_mode]

[Repeat for each completed file]

### Unplanned Sessions
[List any completed files with no matching plan — i.e., files in completed/ that were created as unplanned]

### Missed / Skipped Sessions
[List plans in `workouts/plans/YYYY-WXX/` with `status: missed`, with athlete's explanation if recorded]

### Weight Training Detail
[Read from `## Actual → Athlete Notes` in the completed weights file]

**Strength PRs:** [Read from `## Actual → Strength PRs` in the completed weights file]

### Strength Progression
[Read from `## Actual → Progressions` in the completed weights file — omit section if no weight training this week]

## Observations
[3-5 bullet points: patterns, trends, what went well, what to watch — tone per coaching_mode]

## Fitness Trajectory
[Based on consistency-log: is load trending up/down/stable? — tone per coaching_mode]

**Efficiency Factor trend:** Read `overview/progress-metrics.md`. Report:
- Latest Z2 EF vs the prior Z2 EF (or prior 4-week avg Z2 EF if available): improving / stable / declining.
- One sentence interpreting the direction (e.g., "EF rising on Z2 rides suggests cardiac adaptation is underway" or "EF holding flat — may need more Z2 volume to drive further adaptation").
- In `data` mode: list the last 3–4 EF values in chronological order, no interpretation.
- Omit this block if fewer than 2 cycling activities with EF data have been logged.

## Goal Trajectory
[Only include if Performance Targets are defined in athlete/profile.md. For each target: current status vs goal, gap, and whether on track. In accountability mode, name the gap plainly.]

## Recommendation for Coming Week
[One concrete suggestion based on this week's data — tone per coaching_mode]
```

If a reflection file already exists for a week (from a previous partial sync), append a new dated section rather than overwriting.

### Step 4: Load 4-week trend data

Read `athlete/consistency-log.md`. Extract the last 4 weeks of data for each discipline.

Read `overview/progress-metrics.md`. Extract all EF rows from the last 8 weeks. Identify:
- The most recent Z2 EF value and the one prior to it (for direction)
- The 4-week average EF (Z2 rides only, if ≥ 2 data points exist)
- Overall trend: improving / stable / declining

Glob `journals/**/*.md` sorted by date descending — read the entries from the current week. Count and note: how many entries flagged fatigue ≥ 4, energy ≤ 2, stress ≥ 4. This will be surfaced in Step 5.

### Step 5: Generate narrative weekly summary

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

### Efficiency Factor Trend
[Only include if ≥ 2 cycling EF values exist in `overview/progress-metrics.md`.]
[Show a mini-table of the last 4–6 EF readings with date, zone, and EF value.]
[Follow with one sentence on direction — coach/accountability/data tone per coaching_mode.]
[If insufficient Z2-specific data exists yet, note that and say when a reliable baseline is expected (after N more Z2 rides).]

### Recommendation for Next Week
[One concrete, actionable suggestion.
coach mode: forward-looking and encouraging
accountability mode: directly tied to the biggest adherence or goal gap this week
data mode: one sentence — the metric that most needs attention and why]
```

### Step 6: Offer to plan next week

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
