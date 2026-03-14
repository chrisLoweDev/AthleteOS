# /sync-hevy-exercises — Refresh Hevy Exercise Cache

Fetches the full Hevy exercise library and writes it to `data/hevy-exercises.json`.

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

2. **Run the sync script**
   ```
   python3 scripts/fetch_hevy_exercises.py
   ```

3. **Report result**
   - On success (exit 0): print the output line (e.g. "Synced 342 exercises to data/hevy-exercises.json") and the timestamp from `data/hevy-exercises.json`
   - On HTTP error (exit 1): display the error from stderr and stop
   - On missing API key (exit 2): display the credential instructions and stop
