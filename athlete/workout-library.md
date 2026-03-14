# Workout Library

_Extensible library of named strength routines for use by `/plan-workouts`. When scheduling strength work, select the appropriate session from this library. Add new routines here as needed (e.g. "Upper Body Focus", "Travel/Minimal Equipment") — the A/B sessions are the current defaults but are not the only options. Update working weights here as you progress._

> **Important:** Exercise names in this library must exactly match entries in `data/hevy-exercises.json`. If you add a new exercise, verify the name against the cache (or run `/sync-hevy-exercises` then search the JSON) before adding it here — a mismatch will cause `/push-workouts` to fail with exit code 3.

**Working weights last updated:** 2026-03-13 (confirmed by athlete — actual training weights, not illness-adjusted)

---

## Weight Training Sessions

### Full Body A — Squat / Push / Pull

**Focus:** Quad-dominant lower body + horizontal push/pull
**Duration:** ~75 min
**Frequency:** Once per week, alternating with Full Body B

#### Warm Up
- 10 min easy jog (activation only, conversational pace)
- 5 min mobility: hip circles, thoracic rotation, shoulder rolls

#### Main Lifts

| Exercise | Warm-Up Sets | Working Sets | Reps | Working Weight | Notes |
|----------|-------------|--------------|------|----------------|-------|
| Squat (Barbell) | 2×6 @ 60kg | 5×5 | 5 | **80kg** | 1RM ~100kg. Neutral spine, brace hard throughout |
| Bench Press (Barbell) | 2×6 @ 50kg | 5×5 | 5 | **80kg** | Full ROM, controlled descent |
| Bent Over Row (Barbell) | 2×6 @ 45kg | 5×5 | 5 | **70kg** | Hinge to ~45°, pull to lower chest |

#### Accessory Work

| Exercise | Sets | Reps | Weight |
|----------|------|------|--------|
| Hanging Leg Raise | 4 | 8 | Bodyweight |
| Bicep Curl (Barbell) | 3 | 10 | 20kg |

#### Cool Down
- 5 min stretching: quad stretch, hamstring, chest opener, lat stretch

#### Substitutions
| Normal Exercise | Substitute | When to Use |
|-----------------|-----------|-------------|
| Bent-Over Row | Lat Pulldown @ 55–60kg | Lower back niggle — eliminates hinged spinal load |
| Squat (Barbell) | Goblet Squat (light) | Lower back niggle — if warm-up sets feel uncomfortable |

---

### Full Body B — Hinge / Pull / Overhead

**Focus:** Posterior chain (glutes/hamstrings) + vertical pull + overhead press
**Duration:** ~75 min
**Frequency:** Once per week, alternating with Full Body A

#### Warm Up
- 10 min easy jog (activation only)
- 5 min mobility: hip hinge practice (bodyweight), band pull-aparts, ankle circles

#### Main Lifts

| Exercise | Warm-Up Sets | Working Sets | Reps | Working Weight | Notes |
|----------|-------------|--------------|------|----------------|-------|
| Romanian Deadlift (Barbell) | 2×6 @ 60kg | 5×5 | 5 | **80kg** | Primary cycling power source — posterior chain |
| Overhead Press (Barbell) | 2×6 @ 30kg | 5×5 | 5 | **40kg** | Strict press, no leg drive |
| Pull Up | — | 5×5 | 5 | Bodyweight (84kg) | Full ROM, controlled descent |

#### Accessory Work

| Exercise | Sets | Reps | Weight |
|----------|------|------|--------|
| Russian Twist (Bodyweight) | 4 | 12 | Bodyweight |
| Hanging Leg Raise | 3 | 8 | Bodyweight |

#### Cool Down
- 5 min stretching: hamstring, hip flexor, lat stretch, thoracic extension

#### Substitutions
| Normal Exercise | Substitute | When to Use |
|-----------------|-----------|-------------|
| Romanian Deadlift | Leg Press or Single-Leg RDL (light) | Lower back niggle — avoid hinged load under bar |
| Pull Up | Lat Pulldown @ 55–60kg | If pull-up volume is too fatiguing mid-block |

---

---

## Swim Sessions

_Paces are computed from CSS (Critical Swim Speed) in `athlete/profile.md`. If CSS is TBD, use RPE guidance until a CSS test is completed._

### Endurance Base Swim (Z2)

**Focus:** Aerobic base — CSS + 5–15 sec/100m
**Target Distance:** ~2,000m
**Duration:** ~45 min
**Frequency:** 1–2x per week as aerobic volume

#### Warm Up (400m)
- 200m easy (Z1 — CSS + 15–20 sec/100m)
- 4×50m with 15 sec rest, building to Z2 pace

#### Main Set (1,300m)
- 5×200m @ Z2 pace (CSS + 5–15 sec/100m), 20 sec rest between
- Or: 13×100m @ Z2 pace, 15 sec rest between

#### Cool Down (300m)
- 200m easy (Z1)
- 100m backstroke or choice (low effort)

#### Notes
- Focus on consistent pace across all reps — not fast, just steady
- If open water: remove rest intervals, hold effort by feel (conversational effort)

---

### Threshold Intervals (Z4)

**Focus:** CSS-pace quality work — CSS − 0–5 sec/100m
**Target Distance:** ~2,000m
**Duration:** ~45 min
**Frequency:** 1x per week maximum; do not schedule same day as Z4+ cycling or heavy weights

#### Warm Up (400m)
- 200m easy (Z1)
- 4×50m @ Z3 pace with 15 sec rest (build into threshold)

#### Main Set (1,200m)
- 6×200m @ CSS pace (Z4 — CSS − 0–5 sec/100m), 30 sec rest between reps
- Or: 12×100m @ CSS pace, 20 sec rest between

#### Cool Down (400m)
- 300m easy (Z1)
- 100m choice/backstroke

#### Notes
- Rest intervals are non-negotiable — the goal is to hold pace, not grind through fatigue
- If 50m pool: adjust distances to nearest 50m multiple (e.g., 6×150m or 4×250m)
- If open water: replace with 4×5 min @ threshold effort with 1 min easy between

#### Substitutions
| Normal | Substitute | When |
|--------|-----------|------|
| 6×200m @ CSS | 8×150m @ CSS | Short-course pool only (25m) |
| Threshold interval session | 45 min steady Z2/Z3 | Moderate fatigue — preserve quality by reducing intensity |
| Pool session | Open water Z2 effort | No pool access — remove rest intervals, hold Z2–Z3 by HR |

---

## Progression Rules

- **Standard progression:** Add 2.5kg to working weight when you complete all sets and reps cleanly with good form
- **Stall (fail to complete sets twice in a row):** Deload 10%, rebuild
- **Post-illness / post-break return:** Start at 65–70% of working weight, rebuild over 2 weeks before resuming progressive load
- **Intensity during recovery weeks:** Reduce sets by 1 (5×5 → 4×5) and drop weight ~10%

---

## Programming Notes

- **Never schedule Full Body A and Full Body B on back-to-back days** — 48h minimum between sessions
- **Weights + hard cycling:** Avoid scheduling a Z4+ cycling session the day after Full Body B (RDL/posterior chain fatigue affects power output)
- **Z2 cycling can follow either session** — low enough intensity that strength recovery is not compromised
- **Goal context:** These sessions support long-day mountain bikepacking — posterior chain strength (RDL, squat), upper body endurance (OHP, rows, pull-ups), and core stability (leg raises, twists) are all directly relevant
