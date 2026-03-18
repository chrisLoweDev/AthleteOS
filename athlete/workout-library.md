# Workout Library

_Extensible library of named strength routines for use by `/plan-workouts`. When scheduling strength work, select the appropriate session from this library. Alternate Full Body A and Full Body B each week unless context suggests otherwise (e.g. upper-only if legs needed fresh for a key ride). Update working weights here as you progress._

> **Important:** Exercise names in this library must exactly match entries in `data/hevy-exercises.json`. If you add a new exercise, verify the name against the cache (or run `/sync-hevy-exercises` then search the JSON) before adding it here — a mismatch will cause `/push-workouts` to fail with exit code 3.

**Archetype:** Athletic/Hybrid — full-body sessions, 2× per week, double progression model.

**Equipment note:** Chris has no dumbbells. All exercises use barbell, EZ bar, pull-up bar, or bands only. No dumbbell exercises.

**Working weights last updated:** 2026-03-16

---

## Full Body A — Squat Focus

**Patterns covered:** Squat, Horizontal Push, Horizontal Pull, Vertical Pull, Core
**Duration:** ~70 min
**Key focus:** Lower body strength (squat pattern) + horizontal push/pull balance

### Warm-Up (10 min)

- 2 min: Glute Bridge × 15 reps (bodyweight, activate posterior chain)
- 2 min: Band Pullaparts × 20 reps (shoulder health, set scapulae)
- 2 min: Goblet Squat × 10 reps (band or bodyweight — thoracic mobility + hip opener)
- 2 min: Dead Bug × 8 reps/side (core activation, breathing pattern)
- 2 min: Empty-bar squat × 10 reps (movement primer)

### Main Lifts

| Exercise | Warm-Up Sets | Working Sets | Reps | Working Weight | Notes |
|----------|-------------|--------------|------|----------------|-------|
| Squat (Barbell) | 2 (40kg×8, 60kg×5) | 3 | 4–8 | 80kg | Double progression: add reps → add 5kg when 3×8 achieved 2 sessions in a row |
| Bench Press (Barbell) | 1 (50kg×5) | 3 | 4–8 | 80kg | Double progression: same rule |
| Bent Over Row (Barbell) | 1 (50kg×5) | 3 | 4–8 | 70kg | Overhand grip; brace hard; keep back flat |
| Pull Up | — | 3 | max (target 5–9) | BW | Rest 2–3 min; note reps per set |

_Rest 2–3 min between working sets on all main lifts._

### Accessory Block (superset pairs — 60–90 sec between supersets)

**Superset 1:**
| Exercise | Sets | Reps | Weight | Notes |
|----------|------|------|--------|-------|
| Bulgarian Split Squat | 2 | 8/side | BW | Rear foot elevated; focus on balance and depth |
| Band Pullaparts | 2 | 20 | light band | Squeeze shoulder blades at end range |

**Superset 2:**
| Exercise | Sets | Reps | Weight | Notes |
|----------|------|------|--------|-------|
| Back Extension (Hyperextension) | 2 | 12 | BW | Controlled; squeeze glutes at top |
| Bench Press - Close Grip (Barbell) | 2 | 10–12 | 50–60kg | Tricep emphasis; elbows tucked |

### Core Block

| Exercise | Sets | Reps / Duration | Notes |
|----------|------|-----------------|-------|
| Hanging Leg Raise | 2 | 8–12 | Controlled; no swinging |
| Ab Wheel | 2 | 8–10 | From knees; full extension only if lower back allows |

### Mobility Close (10 min — non-negotiable)

- 2 min: Hip flexor stretch (kneeling lunge), 60 sec/side
- 2 min: Pigeon or figure-4 glute stretch, 60 sec/side
- 2 min: Thoracic extension over bench/roller
- 2 min: Doorframe pec stretch, 60 sec/side
- 2 min: Hamstring stretch (standing or lying), 60 sec/side

### Substitutions

| Normal Exercise | Substitute | When to Use |
|-----------------|-----------|-------------|
| Squat (Barbell) | Goblet Squat (band) | Acute knee issue or technique reset day |
| Bent Over Row (Barbell) | EZ Bar Row | Lower back fatigued from squats |
| Pull Up | Band-Assisted Pull Up | High-fatigue week or deload |
| Bulgarian Split Squat | Glute Bridge (weighted, barbell) | Balance/stability issue |

---

## Full Body B — Hinge Focus

**Patterns covered:** Hinge, Vertical Push, Vertical Pull, Core
**Duration:** ~70 min
**Key focus:** Posterior chain (hinge pattern) + vertical push/pull balance

### Warm-Up (10 min)

- 2 min: Glute Bridge × 15 reps (bodyweight — activate glutes and hamstrings)
- 2 min: Band Pullaparts × 20 reps (shoulder prep)
- 2 min: Dead Bug × 8 reps/side (core activation)
- 2 min: Back Extension (Hyperextension) × 10 reps (BW — prime erectors)
- 2 min: Empty-bar Romanian Deadlift × 10 reps (hip hinge primer, feel the hamstring load)

### Main Lifts

| Exercise | Warm-Up Sets | Working Sets | Reps | Working Weight | Notes |
|----------|-------------|--------------|------|----------------|-------|
| Romanian Deadlift (Barbell) | 2 (50kg×8, 65kg×5) | 3 | 4–8 | 80kg | Hinge at hips; feel hamstring stretch; keep bar close |
| Overhead Press (Barbell) | 2 (30kg×8, 40kg×5) | 3 | 4–8 | 50kg | Brace core; no lumbar hyperextension; press straight up |
| Pull Up | — | 3 | max (target 5–9) | BW | Note reps per set; use band assist if needed |

_Rest 2–3 min between working sets on all main lifts._

### Accessory Block (superset pairs — 60–90 sec between supersets)

**Superset 1:**
| Exercise | Sets | Reps | Weight | Notes |
|----------|------|------|--------|-------|
| Back Extension (Hyperextension) | 3 | 12–15 | BW | Add load (hold plate) when 15 reps easy |
| Band Pullaparts | 3 | 20 | light band | Rear delt and rotator cuff health |

**Superset 2:**
| Exercise | Sets | Reps | Weight | Notes |
|----------|------|------|--------|-------|
| Bulgarian Split Squat | 2 | 8/side | BW | Single-leg work transfers to cycling |
| Hanging Leg Raise | 2 | 8–12 | BW | Controlled; full hang |

### Core Block

| Exercise | Sets | Reps / Duration | Notes |
|----------|------|-----------------|-------|
| Russian Twist | 2 | 20 (10/side) | BW or light plate; controlled rotation |
| Dead Bug | 2 | 8/side | Exhale on extension; lower back stays flat |

### Mobility Close (10 min — non-negotiable)

- 2 min: Standing hamstring stretch, 60 sec/side
- 2 min: Hip flexor stretch (kneeling lunge), 60 sec/side
- 2 min: Lat stretch (arm overhead, side-lean against wall), 60 sec/side
- 2 min: Thoracic rotation (seated or quadruped), 60 sec/side
- 2 min: Child's pose with reach (full spinal decompression)

### Substitutions

| Normal Exercise | Substitute | When to Use |
|-----------------|-----------|-------------|
| Romanian Deadlift (Barbell) | Back Extension (Hyperextension) loaded | Lower back fatigue or technique reset |
| Overhead Press (Barbell) | EZ Bar Upright Row | Shoulder niggle (acute, not chronic) |
| Pull Up | Band-Assisted Pull Up | High-fatigue week or deload |

---

## Global Substitutions

| Situation | Modification |
|-----------|-------------|
| Deload week (every 4th week) | Reduce working weights by 15%; keep sets/reps the same |
| Legs needed fresh for Z4+ ride next day | Switch to Full Body B upper-emphasis: skip Squat and Bulgarian Split Squat; add extra Pull Up set |
| Time-limited (<50 min) | Drop one accessory superset and shorten mobility to 5 min |
| Back soreness (non-acute) | Replace all hinge work with Back Extension (Hyperextension) bodyweight only |
