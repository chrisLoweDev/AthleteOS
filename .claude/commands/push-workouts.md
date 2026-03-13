# /push-workouts — Push Pending Workouts to Hevy

Push planned weights sessions to Hevy as Routines.

## Steps

1. **Check credentials**
   - Read `.env` and confirm `HEVY_API_KEY` is set
   - If missing, print:
     ```
     HEVY_API_KEY is not set.
     Get your key at: https://hevy.com/settings?developer
     Add it to .env: HEVY_API_KEY=<your-key>
     ```
     Then stop.

2. **Find pending weights files**
   - Glob `workouts/plans/**/*.md`
   - Filter to files where frontmatter `type: weights` and `hevy_routine_id: null`
   - If none found, print "No pending weights sessions to push." and stop.

3. **Push each file**
   For each file:
   - Run: `python3 scripts/push_hevy.py <file_path>`
   - **Exit 0, output is a routine ID** → edit the file's frontmatter: `hevy_routine_id: <id>`. Mark as pushed ✓
   - **Output is "already pushed: <id>"** → skip, note as already done
   - **Exit 2** (no API key) → print the instructions from stderr and stop all remaining pushes
   - **Exit 3** (unknown exercise) → print the error from stderr and stop — the ID dict needs updating before continuing
   - **Other error** → print stderr output, mark as failed ✗, continue with remaining files

4. **Print summary table**
   ```
   File                                    Status
   --------------------------------------  --------------------
   2026-03-11-weights-full-body-a.md       ✓ pushed (abc12345)
   2026-03-14-weights-full-body-b.md       ✓ pushed (def67890)
   ```
