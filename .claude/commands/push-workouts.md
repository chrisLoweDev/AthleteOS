# /push-workouts — Push Pending Workouts to Hevy

Push planned weights sessions to Hevy as Routines.

## Steps

1. **Check exercise cache**
   - Check if `data/hevy-exercises.json` exists
   - If **missing**: run `python3 scripts/fetch_hevy_exercises.py` automatically; stop on failure
   - If **present but stale** (last_synced >7 days ago): warn the athlete and ask:
     ```
     data/hevy-exercises.json is X days old.
     A) Refresh now (recommended)
     B) Continue with existing cache
     ```
     Wait for answer; if A, run `python3 scripts/fetch_hevy_exercises.py` before proceeding.

2. **Check credentials**
   - Read `.env` and confirm `HEVY_API_KEY` is set
   - If missing, print:
     ```
     HEVY_API_KEY is not set.
     Get your key at: https://hevy.com/settings?developer
     Add it to .env: HEVY_API_KEY=<your-key>
     ```
     Then stop.

3. **Find pending weights files**
   - Glob `workouts/plans/**/*.md`
   - Filter to files where frontmatter `type: weights` and `hevy_routine_id: null`
   - If none found, print "No pending weights sessions to push." and stop.

4. **Push each file**
   For each file:
   - Run: `python3 scripts/push_hevy.py <file_path>`
   - **Exit 0, output is a routine ID** → edit the file's frontmatter: `hevy_routine_id: <id>`. Mark as pushed ✓
   - **Output is "already pushed: <id>"** → skip, note as already done
   - **Exit 2** (no API key) → print the instructions from stderr and stop all remaining pushes
   - **Exit 3** (unknown exercise) → print the error from stderr and stop — check that the exercise name exactly matches an entry in `data/hevy-exercises.json`, or run `/sync-hevy-exercises` to refresh the cache
   - **Exit 4** (cache missing unexpectedly) → stop; run `python3 scripts/fetch_hevy_exercises.py` to recreate the cache
   - **Other error** → print stderr output, mark as failed ✗, continue with remaining files

5. **Print summary table**
   ```
   File                                    Status
   --------------------------------------  --------------------
   2026-03-11-weights-full-body-a.md       ✓ pushed (abc12345)
   2026-03-14-weights-full-body-b.md       ✓ pushed (def67890)
   ```
