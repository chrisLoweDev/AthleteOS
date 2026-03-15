# Athlete

Stores the athlete's personal data, fitness benchmarks, and training history. These files are the source of truth that every command reads before generating workouts or reflections.

## Files

### `profile.md`

The most important file in the project. Contains:

- **Personal stats** — name, weight
- **Training benchmarks** — FTP, running threshold pace, swim CSS, max HR, resting HR
- **Training zones** — pre-computed watts/paces/BPM for cycling, running, swimming, and HR
- **Goals** — primary and secondary training targets
- **Availability** — training days, max hours/week, preferred session times
- **Upcoming races** — used to trigger auto-taper logic in `/plan-workouts`
- **Equipment & preferences** — gym setup, pool access, exercise exclusions
- **Strength PRs** — 1RM estimates (Epley formula) and best working sets

Populate via `/setup` or edit directly. All commands read this file at the start of every session — keep it current.

### `consistency-log.md`

Rolling 12-week training history, broken down by discipline. Updated automatically after every `/fetch-activities` run. Rows older than 12 weeks are pruned.

Tracks per week:
- Cycling: sessions, distance (km), total time
- Running: sessions, distance (km), avg pace, total time
- Swimming: sessions, distance (m), total time
- Strength: sessions, total time
- Weekly totals: combined hours across all disciplines

Use this to spot multi-week trends — volume creep, discipline neglect, recovery deficits.

### `workout-library.md`

Named strength training routines used by `/plan-workouts` when scheduling gym sessions. Contains working weights, set/rep schemes, warm-up and cool-down protocols, and substitution options.

**Important:** Exercise names must exactly match entries in `data/hevy-exercises.json`. A mismatch will cause `/push-workouts` to fail. Run `/sync-hevy-exercises` to refresh the cache, then verify any new exercise name before adding it here.

Update working weights here whenever you progress — this file is the canonical record of where you are strength-wise.
