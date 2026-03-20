# /journal — Capture Subjective Training Data

Records how the athlete is feeling — energy, fatigue, mood, stress, sleep, soreness — and automatically flags whether upcoming sessions need adjustment. Journal entries provide the subjective layer that Strava data cannot.

**Arguments:** `$ARGUMENTS` may contain context — e.g., `/journal post-ride feeling wrecked`. If present, use it to pre-fill context. If empty, ask.

## Steps

### Step 1: Load context

Read `athlete/profile.md` for current goals, availability, and any noted injuries.

Read `overview/pending.md` to know what's coming up.

Glob `journals/**/*.md` sorted by date descending — read the most recent entry (if any) to note any continuity (e.g., a soreness that was flagged before, a recovery trend).

State briefly: "Most recent entry: [date] — [one-line summary]" or "No previous entries found."

### Step 2: Session context (optional)

Ask:

```
Is this journal entry linked to a specific session?
A) Yes — it's about a session I just completed
B) Yes — it's about a session coming up
C) No — general check-in

(Or type the session date/type directly)
```

If A or B, display a combined list of recent sessions:
- Completed: last 3 files from `workouts/completed/**/*.md` (date + type + key_focus)
- Pending: next 3 files from `overview/pending.md`

Ask the athlete to pick one, or say "none" to skip linking.

Set `session_ref` to the relative path of the linked file, or `null`.

Set `context` to:
- `post-session` if they picked a completed session
- `pre-session` if they picked a pending session
- `general` if no session linked

### Step 3: Collect subjective data

Ask all questions in a single prompt:

```
How are you doing right now? Answer each:

1. Energy (1–5): 1 = completely depleted, 5 = excellent
2. Fatigue (1–5): 1 = very fatigued/heavy legs, 5 = fresh/recovered
3. Mood (1–5): 1 = low/flat, 5 = great
4. Stress (1–5): 1 = calm, 5 = high stress
5. Sleep last night (hours): e.g. 7.5
6. Any soreness or pain? (describe area + severity, or "none")
7. Anything else to note? (open text — training notes, life context, nutrition, travel, etc.)
```

Wait for the athlete's response. Parse each field. If a value is missing or ambiguous, ask a single follow-up for just that field before proceeding.

### Step 4: Write journal file

Determine the ISO week using the date: `journals/YYYY-WXX/`

Create the directory if it doesn't exist.

Filename: `journals/YYYY-WXX/YYYY-MM-DD-journal.md`

If a file already exists for today, append a `-2` suffix (e.g., `2026-03-11-journal-2.md`) rather than overwriting.

Write the file:

```markdown
---
date: YYYY-MM-DD
time: HH:MM          # omit if athlete didn't provide
session_ref: null    # or relative path to linked workout file
context: pre-session | post-session | general
energy: [1–5]
fatigue: [1–5]
mood: [1–5]
stress: [1–5]
sleep_hours: [X.X]
soreness: null       # or description
adjustment_triggered: false   # updated in step 6 if needed
---

## Journal — [Day, DD Month YYYY]

**Context:** [pre-session / post-session / general]
[If linked session: **Session:** [session name + date]]

**How I'm feeling:** [brief narrative summary drawn from the athlete's responses — 2–3 sentences, coach tone]

### Notes
[Athlete's open-text response verbatim, or "None."]
```

### Step 5: Update overview/journal-summary.md

Read `overview/journal-summary.md` if it exists.

Append a new row for today's entry (or update today's row if one already exists):

```markdown
# Journal Summary

_Last updated: YYYY-MM-DD_

| Date | Day | Context | Energy | Fatigue | Mood | Stress | Sleep | Session | Highlight |
|------|-----|---------|--------|---------|------|--------|-------|---------|-----------|
| YYYY-MM-DD | [Day] | [context] | [1–5] | [1–5] | [1–5] | [1–5] | [X]h | [session name or —] | [one-line summary from notes] |
```

Keep the last ~84 rows (12 weeks × 7 days maximum). If the file exceeds this, prune rows from the top.

If the file doesn't exist, create it with the header and first row.

### Step 6: Analyse signals vs pending sessions

Apply the following rules to the collected data. Evaluate all signals, then combine into a **single coherent recommendation** — do not issue multiple separate proposals.

**Signal rules:**

| Signal | Threshold | Proposed Adjustment |
|--------|-----------|---------------------|
| Fatigue | ≤ 2 | Shorten next hard session (Z3+) 20%, drop intensity one zone |
| Energy | ≤ 2 | Swap next quality session to Z2 equivalent, or defer next weights session |
| Stress | ≥ 4 | Scale remaining week volume −20% across all pending sessions |
| Sleep | < 6h | Treat as Fatigue ≥ 4 (same rule) |
| Soreness (specific area) | any | Flag next session loading that area; propose modification or substitution |
| Fatigue ≤ 2 AND Energy ≤ 2 | combined | Propose inserting a rest day; archive next pending session |

**Hard session definition:** cycling sessions with Z3+ main set, running with Z3+ pace target, or any weights session.

**If no signals trigger:** skip to Step 7 with a note: "No adjustment needed based on today's signals."

**If one or more signals trigger:**

Identify the specific pending session(s) affected. State which signal triggered which rule. Present a before/after diff:

```
Signals detected:
- Fatigue: [value]/5 (low = fatigued) → next hard session should be shortened and dropped one zone
- Sleep: [value]h → treated as high fatigue (same rule)

Proposed adjustment:

[date] [Type] — [Session Name]
  BEFORE: [current main set description, duration, targets]
  AFTER:  [modified description — shorter, lower zone, or archived]
  Reason: [signal(s) that triggered this]

Apply this adjustment? (yes / no / modify)
```

Wait for confirmation. If "no", note `adjustment_triggered: false` and proceed. If "modify", accept clarification, revise, re-present. Only apply after "yes".

### Step 7: Apply adjustment (if confirmed)

For each approved modification, follow the same edit pattern as `/edit-plan`:

**Intensity / duration change:**
- Edit the workout file body: update main set targets (watt ranges, paces, durations)
- Add to YAML frontmatter: `edit_note: "Adjusted YYYY-MM-DD — journal signal: [brief reason]"`
- Do NOT alter original `planned_duration_min` or `planned_distance_km` — these represent the original plan

**Archive session (rest day proposal):**
- Edit frontmatter: `status: archived`, `edit_note: "Archived YYYY-MM-DD — journal: fatigue + low energy"`
- Do not delete the file

**Update the journal file:**
- Set `adjustment_triggered: true` in frontmatter
- Add a line at the bottom: `**Adjustment applied:** [brief description of what changed]`

**Regenerate `overview/pending.md`** from all remaining `status: pending` files, sorted by date ascending:

```markdown
# Pending Workouts

_Last updated: YYYY-MM-DD_

| Date | Day | Type | Duration | Focus | Status | Plan |
|------|-----|------|----------|-------|--------|------|
| ... | ... | ... | ... min | ... | pending | [link](../workouts/plans/...) |
```

### Step 8: Confirmation summary

```
Journal saved: journals/YYYY-WXX/YYYY-MM-DD-journal.md

Today's snapshot:
  Energy [1–5] · Fatigue [1–5] · Mood [1–5] · Stress [1–5] · Sleep [X]h

[If adjustment applied:]
  Adjustment: [date] [type] — [brief change description]
  Run /calendar to see your updated schedule.

[If no adjustment:]
  No adjustment needed — signals look fine for your upcoming sessions.

[If context = post-session AND session was linked:]
  Linked to: [session name]
  This will be visible in the next /review reflection.
```
