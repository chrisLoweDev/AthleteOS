# /set-goals — Define Measurable Performance Targets

A dialog command that pushes vague goals into measurable targets and writes them to `athlete/profile.md`. Without this step, accountability-mode coaching has no anchor.

**Arguments:** `$ARGUMENTS` may contain context — e.g., `/set-goals sailing trip`. If present, use it to pre-focus the dialog.

## Steps

### Step 1: Load current state

Read `athlete/profile.md`:
- Upcoming events and their dates
- Current goals (note which are measurable and which are feelings/intent)
- Strength PRs table
- Any existing Performance Targets

If Performance Targets already exist (and are not just the placeholder row), display them:
```
Current Performance Targets:
[table]

Would you like to:
A) Review and update existing targets
B) Add new targets
C) Replace all targets with a fresh dialog
```
Wait for answer. If A or B, preserve existing rows (A: edit in place; B: append). If C: start fresh.

If no targets exist (or only the placeholder row): proceed directly to Step 2.

### Step 2: Events dialog

For each upcoming event in the athlete's profile, ask in a single prompt:

```
Let's define what success looks like for each upcoming event.

[Event 1: Sailing trip — end of May 2026]
On the boat, what specifically do you need to be able to do?
Think about: lifting/carrying loads, overhead reaching, sustained physical work, posture under fatigue, balance.
What does "feel strong and mobile" actually mean — what would you be able to do that you can't do now, or struggle to do?

[Event 2: Bike-packing trip — July/August 2026]
For the riding, what specifically does "strong on the bike for consecutive long days" mean?
Think about: longest single day you need to sustain, number of consecutive days, terrain (flat/hilly), daily distance target, power or pace you need to hold.
```

Wait for the athlete's response. If their answer is still vague (e.g., "just want to feel good"), probe once:
> "What would you be doing on day 3 of the trip that would tell you the training worked? Give me one concrete thing."

Parse the responses into draft measurable targets. Examples of what to extract:
- "I need to be able to carry a 20kg sail bag up a dock ladder" → target: Loaded carry / farmer's walk with 20kg per hand, 20 reps step-ups
- "5 consecutive days of 5h riding" → target: Complete a 5h Z2 ride (165–195W NP) as a single session
- "Not be wrecked after day 2" → probe for what "wrecked" means; likely maps to aerobic base (Z2 volume) and recovery rate

### Step 3: Strength targets dialog

```
For strength, what working weights do you want to hit, and by when?
(Current PRs are shown below for reference)

[Insert current Strength PRs table from profile.md]

For each lift you care about, tell me:
- Target weight for 5×5 (or rep scheme you prefer)
- Target date
- Any lifts you're NOT focused on right now (I'll skip those)
```

Wait for response. Parse into per-exercise targets with dates.

If the athlete doesn't know what's realistic, suggest based on current PRs and typical progression:
> "Based on your current ~80kg 5×5 squat, 100kg 5×5 by June is achievable with consistent double-progression — roughly 2.5kg every 2 sessions, ~12 progressions needed over ~6 months. That's tight but realistic if you're consistent."

### Step 4: Mobility targets dialog

```
For mobility, what movements are currently limiting you?
And what does "fixed" look like — what specifically should you be able to do?

Common reference points:
- Hip hinge: full RDL depth with a neutral spine at working weight (no lumbar rounding)
- Hip flexor / squat depth: full squat to parallel or below with heels on floor, no forward lean
- Thoracic rotation: relevant for sailing — can you rotate 45° each way without compensation?
- Overhead: arms fully vertical overhead without lower back arching
- Hamstring: can you touch your toes (standing forward fold)?
```

Wait for response. Convert to measurable criteria (e.g., "full RDL depth at 100kg", "arms overhead vertical", "toes reachable from standing").

### Step 5: Draft and confirm targets

Compile all collected targets into a draft table:

```
Here are the Performance Targets I've drafted:

| Target | Metric | Goal | Deadline | Status |
|--------|--------|------|----------|--------|
| [each target from Steps 2–4] |

Does this look right? Any changes before I write it to your profile?
(Confirm, or describe changes)
```

Wait for approval. Adjust and re-present if needed.

### Step 6: Write to profile.md

Replace the `## Performance Targets` section in `athlete/profile.md` with the confirmed table.

If a target was previously "Not yet tested" and now has a current value from PRs, use "In progress (current: [value])".

### Step 7: Confirmation summary

```
Performance Targets saved to athlete/profile.md.

[N] targets defined:
[bullet list: target name + deadline]

These will be used in accountability-mode /review and /fetch-activities to track your progress against what the events actually require.

To switch to accountability mode, edit coaching_mode in athlete/profile.md:
  coaching_mode: accountability
```
