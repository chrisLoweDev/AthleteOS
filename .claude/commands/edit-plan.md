# /edit-plan — Edit Existing Training Plan

Adjusts pending workout sessions based on athlete feedback — fatigue, injuries, scheduling conflicts, or specific requests. Edits existing files in place; never creates or deletes files.

**Arguments:** `$ARGUMENTS` may contain the athlete's edit request directly — e.g., `/edit-plan I'm exhausted, tone everything down`. If present, use it directly. If empty, show the pending schedule and ask.

## Steps

### Step 1: Load current state

Read `athlete/profile.md`:
- FTP and running threshold pace (for zone recalculation)
- HR zones
- Any noted injuries or constraints

Glob `workouts/plans/**/*.md` and read all files with `status: pending`. Build a list sorted by date ascending.

**If no pending sessions exist**, stop:
> "No pending sessions to edit. Run `/plan-workouts` to create a training plan."

### Step 2: Gather edit context

**If `$ARGUMENTS` is non-empty:** Use it as the athlete's edit request. Skip the prompt below.

**If `$ARGUMENTS` is empty:** Display the pending schedule and ask:

```
Here's your upcoming schedule:

| Date | Day | Type | Duration | Focus |
|------|-----|------|----------|-------|
| ...  | ... | ...  | ...      | ...   |

What would you like to adjust? Tell me how you're feeling or what you need changed.
(Examples: "I'm exhausted — make it easier", "skip Wednesday", "move Saturday's ride to Sunday", "my shoulder is sore")
```

Wait for the athlete's input before proceeding.

### Step 3: Interpret the request and propose changes

Analyze the athlete's input against the pending sessions. Determine which modifications are needed using these rules:

**Fatigue / intensity adjustments:**
- "Tired / exhausted / fatigued / shattered" → reduce all remaining sessions this week:
  - Shorten duration by 20%
  - Drop intensity one zone (Z4→Z3, Z3→Z2); if already Z2, drop to lower half of Z2 range
  - For weights: reduce sets by 1 and load by ~10–15%; skip accessory work if needed
- "Feeling good / fresh / strong" → optionally suggest upgrading one quality session (e.g., +15 min, bump to upper Z2 or add a Z3 interval)
- "Make [specific session] easier/harder" → adjust only that session's targets

**Scheduling changes:**
- "Skip [day/session]" → mark that session `status: archived`
- "Move [date] to [new date]" → update `date` and `week_folder` in frontmatter, rename file, move to correct week folder if ISO week changes
- "Can't train until [date]" → archive all sessions before that date
- "Add a rest day on [date]" → archive anything scheduled that day

**Injury / niggle handling:**
- "Sore [body part]" → for weight sessions: remove or substitute exercises that stress that area; add a coaching note explaining the substitution
- For cycling with a lower-body niggle: reduce target watts by 10–15% and add a caution note
- "Sick / not well" → offer two options: (A) archive all sessions this week, or (B) push the plan back by N days (archive current sessions; advise to re-run `/plan-workouts` when recovered)

**Structural changes:**
- "Replace [session] with rest" → archive that session, note reason
- "Cancel everything" → archive all pending sessions

**Always compute updated targets from athlete's FTP / threshold pace** in `athlete/profile.md` — don't use approximate numbers.

Show a clear before/after diff for every session that changes. Sessions with no change should be noted briefly:

```
Proposed edits:

1. 2026-03-12 Cycling — Z2 Aerobic (75 min)
   BEFORE: Main set 55 min @ 155–200W
   AFTER:  Main set 44 min @ 151–172W (lower Z2, −11 min)
   Reason: Fatigue — reducing duration and dropping to lower half of Z2

2. 2026-03-14 Weights — Full Body B (75 min)
   BEFORE: RDL 5×5 @80kg, OHP 5×5 @40kg, Pull-Ups 5×5, [accessory work]
   AFTER:  RDL 4×5 @68kg, OHP 4×5 @34kg, Pull-Ups 4×5 — accessory work skipped
   Reason: Fatigue — conservative reduction

3. 2026-03-15 Cycling — Z2 Endurance (90 min)
   No change — Sunday ride; reassess Friday.

Apply these changes? (yes / adjust / cancel)
```

Wait for approval. If the athlete replies "adjust", accept their clarification, revise the proposal, and re-present. Only proceed after "yes" or equivalent confirmation.

### Step 4: Apply changes to files

For each approved modification:

**Intensity / duration change:**
- Edit the workout file body: update main set watt ranges, paces, durations, and TSS estimate
- Add to the YAML frontmatter: `edit_note: "Adjusted YYYY-MM-DD — [brief reason]"`
- Do not alter the original `planned_duration_min` or `planned_distance_km` frontmatter fields — these represent the original plan for reflection comparison

**Skip / archive session:**
- Edit frontmatter: set `status: archived`, add `edit_note: "Archived YYYY-MM-DD — [athlete's reason]"`
- Do not delete the file

**Reschedule (date change):**
- Edit frontmatter: update `date` and `week_folder` (recalculate ISO week using Python's `datetime.isocalendar()` format if needed)
- Rename the file to match the new date (update the `YYYY-MM-DD` prefix)
- Move to the correct week folder if the ISO week changed

**Injury accommodation (weights):**
- Edit the Main Lifts table: remove affected exercises or add a substitute
- Add a coaching note explaining what was removed and why
- Add `edit_note` to frontmatter

**Injury accommodation (cycling/running):**
- Reduce targets in the main set description
- Add a coaching caution note at the bottom of the file
- Add `edit_note` to frontmatter

### Step 5: Regenerate pending table

Rewrite `overview/pending.md` from all remaining `status: pending` files, sorted by date ascending:

```markdown
# Pending Workouts

_Last updated: YYYY-MM-DD_

| Date | Day | Type | Duration | Focus | Status | Plan |
|------|-----|------|----------|-------|--------|------|
| ... | ... | ... | ... min | ... | pending | [link](../workouts/plans/...) |
```

### Step 6: Confirmation summary

```
Plan updated. Here's what changed:

✓ [date] [Type]: [brief description of change]
✓ [date] [Type]: [brief description of change]
✗ [date] [Type]: Archived — [reason]

Your upcoming schedule:

| Date | Day | Type | Duration | Focus | Status |
|------|-----|------|----------|-------|--------|
| ...  | ... | ...  | ...      | ...   | pending |

Run /calendar to see the full view.
```
