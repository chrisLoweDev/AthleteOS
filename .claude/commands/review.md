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

Structure:
```
## Weekly Review — Week YYYY-WXX

### Training Load
[Compare this week's total volume and intensity to last week.
E.g., "Volume was up 15% from last week (7h vs 6h). Intensity was similar."]

### Key Wins
- [Specific session that went particularly well]
- [PR or personal milestone if applicable]
- [Consistency streak or other positive pattern]

### Areas to Address
- [Missed sessions or underperformance, stated constructively]
- [Any HR or power trends that suggest fatigue or undertraining]

### Subjective Signals This Week
[Only include this section if journal entries exist for the week. Summarise patterns, e.g.:
"3 of 5 journal entries flagged high stress (≥4/5). Energy trended low mid-week. This likely explains the reduced output on Wednesday's threshold session."
If no entries: omit this section entirely.]

### 4-Week Trajectory
[Based on consistency-log trends: is the athlete building, maintaining, or declining?
Mention each discipline separately if the trends differ.]

### Recommendation for Next Week
[One concrete, actionable suggestion — e.g., "Focus on your long Z2 ride — you've skipped it two weeks in a row" or "You're well-rested; a quality threshold session would be beneficial"]
```

**Tone:** Honest, data-driven, encouraging. Focus on patterns not individual failures. Always end with a forward-looking recommendation.

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
