# AthleteOS

**AI personal trainer built into Claude Code.**

AthleteOS is a coaching system that lives entirely inside Claude Code. It plans training sessions, syncs with Strava, tracks consistency across cycling, running, swimming, and weights — and generates weekly reflections that read like notes from a coach, not a spreadsheet.

---

## What is AthleteOS?

AthleteOS treats your training data as markdown files and your AI as a coach. You plan sessions with a slash command, sync completed workouts from Strava with another, and get an honest narrative about what's working and what isn't.

The system is built around a **polarized training model**: mostly low-intensity base work (Z1/Z2), with one or two quality sessions per discipline per week. Planning is constraint-aware — it won't schedule back-to-back hard days, won't put heavy lifts before a threshold ride, and will automatically apply a taper if you mention an upcoming race.

Weight training uses an **Athletic/Hybrid archetype**: full-body sessions designed for endurance athletes where the goal is functional strength and injury resilience, not maximum hypertrophy. Weights sessions can optionally push to Hevy (via the Hevy Pro API) for in-gym reference.

Everything is **markdown-native**. No app, no subscription, no dashboard. Your training history is just files in a folder.

---

## Prerequisites

- **Claude Code** installed with API access ([claude.ai/code](https://claude.ai/code))
- **Python 3.9+** and pip
- **Strava account** — free tier is sufficient for activity sync
- **Hevy account + Pro API key** — optional, required only for `/push-workouts`

Install Python dependencies:

```bash
pip install -r scripts/requirements.txt
```

---

## Getting Started

**Step 0 - Launch Claude Code**
Open up a terminal and navigate to the folder where this project lives. Type `claude` to launch Claude Code

**Step 1 — Run `/setup`**
First-time onboarding. Builds your athlete profile (FTP, threshold pace, HR zones, availability, goals) and tests Strava and Hevy connectivity.

**Step 2 — Run `/plan-workouts`**
Dialog-based session planning. Reads your profile and any pending sessions, then generates a week of structured workouts as markdown files.

**Step 3 — Train. After each week (or activity), run `/fetch-activities`**
Pulls Strava data, matches activities to planned sessions, marks them completed or missed, and generates a reflection.

**Step 4 — Run `/review` weekly**
The full weekly ritual: syncs Strava, writes a narrative coaching summary, and offers to kick off next-week planning.

**Step 5 (optional) - Reflect. Before/After activities, run `/journal`**
Journaling is your chance to reflect on how you're feeling, which with then be considered in future planning and reflections.

---

## Slash Command Reference

| Command | When to use | What it does |
|---------|-------------|--------------|
| `/setup` | First time only | Profile creation + integration tests |
| `/plan-workouts` | Planning a new block | Generates session files for the week |
| `/fetch-activities` | After training | Strava sync + session matching + reflection |
| `/review` | Weekly | Full summary + narrative + plan trigger |
| `/calendar` | Any time | Table of upcoming pending sessions |
| `/journal` | Pre/post session or general | Logs fatigue, mood, sleep, soreness |
| `/edit-plan` | Mid-block adjustments | Modifies existing plans (injury, travel) |
| `/push-workouts` | Before a weights session | Pushes routines to Hevy |
| `/sync-hevy-exercises` | When Hevy push fails | Refreshes the local exercise name cache |

---

### `/setup`
Run once. Walks through creating `athlete/profile.md` with:
- FTP (cycling power)
- Threshold pace (running)
- CSS (swimming)
- Max HR
- Weekly availability and preferred session days
- Current goals and any upcoming races

Also tests Strava API connectivity and, if a Hevy API key is present, confirms the Hevy connection.

---

### `/fetch-activities [date]`
Pulls Strava activities since the last sync (or a specified date), matches them against pending workout files by date and discipline, and:
- Marks matched sessions `completed` and moves them to `workouts/completed/`
- Marks overdue unmatched sessions `missed`
- Generates a weekly reflection at `workouts/reflections/YYYY-WXX-reflection.md`
- Updates `athlete/consistency-log.md` with the week's totals
- Regenerates `overview/pending.md`

For weight training activities, Strava has no sets/reps/weight data — the command will ask you to describe what you did before generating the reflection.

---

### `/plan-workouts [days] [context]`
Generates a structured training block. Before creating files, it will:
1. Read `athlete/profile.md` for zones, availability, and goals
2. Check recent journal entries for fatigue or soreness flags
3. Check existing pending sessions — if any exist, present options:
   - **A)** Replace all with a fresh plan
   - **B)** Start planning after the last pending session
   - **C)** Keep existing and plan around them

Optional arguments:
- `days` — number of days to plan (default: 7)
- `context` — free text: "race on April 6", "travelling Tuesday–Thursday", "right knee sore"

All sessions are generated as markdown files in `workouts/plans/YYYY-WXX/` with full frontmatter and prescribed zones/paces.

---

### `/review`
The weekly ritual command. Runs `/fetch-activities` internally, then generates a coaching narrative covering:
- What was planned vs what was done
- Key performance observations
- Consistency trends from `athlete/consistency-log.md`
- Any fatigue or journal signals flagged during the week
- A forward-looking observation

Ends with an offer to run `/plan-workouts` for the coming week.

---

### `/calendar`
Reads `overview/pending.md` and displays upcoming sessions as a formatted table with date, type, key focus, and planned duration/distance.

---

### `/journal [context]`
Records a subjective check-in. Captures:
- Energy (1–5)
- Fatigue (1–5)
- Mood (1–5)
- Stress (1–5)
- Sleep hours
- Soreness (free text)

If fatigue or stress signals are high, the command will propose adjustments to upcoming sessions (e.g., convert a threshold session to Z2, push a weights day).

Saved to `journals/YYYY-WXX/YYYY-MM-DD-journal.md`.

Optional context argument: `pre-session`, `post-session`, or leave blank for a general check-in.

---

### `/edit-plan [request]`
Modify existing planned sessions mid-block. Describe the change in natural language:
- `/edit-plan swap Tuesday cycling and Wednesday weights`
- `/edit-plan cancel Thursday run, I'm travelling`
- `/edit-plan convert Saturday ride to Z2, knee is acting up`

Handles frontmatter updates and regenerates `overview/pending.md` automatically.

---

### `/push-workouts`
Pushes pending weights sessions to Hevy as routines via the Hevy Pro API. Each exercise is matched to the Hevy exercise cache in `data/hevy-exercises.json`. Fills in `hevy_routine_id` in the session frontmatter.

Requires `HEVY_API_KEY` in `.env`.

---

### `/sync-hevy-exercises`
Refreshes `data/hevy-exercises.json` by pulling the current exercise list from your Hevy account. Run this if a `/push-workouts` call fails due to an unrecognized exercise name — usually means you added a new exercise in Hevy since the last sync.

---

## Typical Weekly Workflow

```
Monday
  └── /journal (post-weekend general check-in)

Mon–Fri
  └── Train sessions from overview/pending.md
  └── /journal (optional post-session check-in)

Before any weights session
  └── /push-workouts (send routine to Hevy)

Sunday
  └── /review
       ├── Syncs Strava
       ├── Generates reflection
       └── Offers to /plan-workouts for next week

If new exercises added to Hevy
  └── /sync-hevy-exercises
```

---

## File Structure

```
AthleteOS/
├── athlete/
│   ├── profile.md              # Source of truth: FTP, paces, HR zones, goals
│   ├── consistency-log.md      # 12-week rolling training volume table
│   └── workout-library.md      # Approved strength routines and working weights
│
├── workouts/
│   ├── plans/
│   │   └── YYYY-WXX/           # Pending sessions (ISO week folder)
│   │       └── YYYY-MM-DD-type-slug.md
│   ├── completed/
│   │   └── YYYY-WXX/           # Sessions moved here after Strava sync
│   └── reflections/
│       └── YYYY-WXX-reflection.md
│
├── journals/
│   └── YYYY-WXX/
│       └── YYYY-MM-DD-journal.md
│
├── overview/
│   ├── pending.md              # Master session table (auto-regenerated)
│   └── strava-sync.json        # Last sync timestamp + seen activity IDs
│
├── data/
│   └── hevy-exercises.json     # Hevy exercise name→ID cache
│
├── scripts/
│   ├── strava_auth.py          # One-time OAuth setup
│   ├── fetch_activities.py     # Strava activity fetch (stdout JSON)
│   ├── strava_client.py        # Strava API client
│   ├── push_hevy.py            # Hevy routine push
│   ├── fetch_hevy_exercises.py # Hevy exercise list sync
│   └── hevy_lookup.py          # Hevy exercise name→ID lookup
│
├── .claude/
│   └── commands/               # Slash command definitions
│
├── CLAUDE.md                   # AI system instructions
└── .env                        # Credentials (not committed)
```

---

## Training Philosophy

AthleteOS enforces a **polarized model**: the majority of training volume sits in Z1/Z2 (aerobic base), with at most one or two quality sessions per discipline per week. This mirrors how elite endurance athletes actually train — not "comfortably hard" all the time.

**Hard session rules (automatically enforced):**
- No Z4+ sessions on consecutive days, across any discipline
- No heavy lower-body lifting (squat, hinge) within 48 hours before a Z4+ cycling session or a long Z2 ride (>2hr)
- Never schedule weights on consecutive days

**Race taper:** If you mention a race in the planning context, the system automatically applies a taper in the final 5–7 days: −40% volume, −20% intensity.

**Weight training archetype:** Athletic/Hybrid — full-body sessions 2×/week, compound-first, with a mandatory 10-minute mobility close. Progresssion uses double progression (add reps first, then weight). The focus is functional strength for endurance sport, not maximum size.

**Journal-informed planning:** Fatigue and stress signals from `/journal` feed directly into planning decisions. A week of high-fatigue entries will shift the following week toward recovery volume.

---

## Strava Setup

Each user needs their own Strava API application. All three credentials you need are available in one place — no OAuth flow required.

### Step 1 — Create your Strava API app

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api) (log in if prompted)
2. Fill in the required fields:
   - **Application Name:** anything (e.g. "AthleteOS")
   - **Category:** choose any (e.g. "Training")
   - **Club:** leave blank
   - **Website:** `http://localhost` (a placeholder is fine)
   - **Authorization Callback Domain:** `localhost`
3. Click **Create**

### Step 2 — Note your credentials

On the same settings page you'll find:
- **Client ID**
- **Client Secret**
- **Your Refresh Token** (listed under "Your Access Token" — use the refresh token value)

### Step 3 — Run `/setup`

Run `/setup` in Claude Code. When it reaches the Strava step, paste your Client ID, Client Secret, and Refresh Token when prompted — the setup command will create your `.env` file automatically.

---

## Tips

- **Keep `athlete/profile.md` current.** All zones and paces are derived from FTP, threshold pace, and CSS. If your fitness changes, update the profile and the next planning run will use the correct targets.

- **Journal regularly.** Even a quick check-in once or twice a week meaningfully improves plan quality. Fatigue signals that aren't captured lead to overreaching.

- **Run `/review`, not just `/fetch-activities`.** The Strava sync is the mechanism; the review narrative is the coaching value.

- **Use `/edit-plan` instead of editing files directly.** Direct edits to workout files won't update `overview/pending.md` automatically, and mismatched frontmatter can confuse the sync.

- **If `/push-workouts` fails with an unknown exercise error,** run `/sync-hevy-exercises` first. The most common cause is a new exercise added in Hevy that isn't in the local cache yet.

- **Swimming sessions can follow any other session** — the musculoskeletal load is low enough that they don't count as "hard" for scheduling purposes (unless they're Z4/Z5 intervals, which still can't stack with other quality sessions).
