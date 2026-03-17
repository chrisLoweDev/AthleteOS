# Journals

Daily subjective training logs captured via the `/journal` command.

## Purpose

Journals record how you *feel* — separate from what you *did*. This data feeds into planning and reflection to help surface patterns like accumulated fatigue, stress load, or recovery gaps that raw workout numbers miss.

## Structure

```
journals/
  YYYY-WXX/
    YYYY-MM-DD-journal.md
```

One file per day, organized by ISO week folder. Multiple entries in a day are appended to the same file.

## Frontmatter Schema

```yaml
---
date: YYYY-MM-DD
time: HH:MM          # optional
session_ref: null    # relative path to linked workout file, if applicable
context: pre-session | post-session | general
energy: 3            # 1=depleted → 5=excellent
fatigue: 2           # 1=fresh → 5=very fatigued
mood: 4              # 1=low → 5=high
stress: 2            # 1=low → 5=very high
sleep_hours: 7.5
soreness: null       # or describe: "lower back tight", "quads", etc.
adjustment_triggered: false
---
```

## How to Use

Run `/journal` to capture a snapshot. The command will:

1. Ask about energy, fatigue, mood, stress, sleep, and soreness
2. Write the entry to the correct week folder
3. Update `overview/journal-summary.md` with the new row
4. If signals are poor (e.g., high fatigue + low energy), propose adjustments to upcoming sessions

## How It Feeds Into Planning

- `/plan-workouts` reads the last 2–3 journal entries before generating sessions
- `/review` surfaces fatigue and stress trends from the rolling journal summary
- `overview/journal-summary.md` maintains a 12-week rolling table for quick pattern scanning

## What to Journal

Journal entries are most useful when captured:
- **Pre-session** — to inform intensity decisions for the day
- **Post-session** — to log how the session actually felt vs. what was planned
- **Rest days** — to track recovery quality and stress load on off days
