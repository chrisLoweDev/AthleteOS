# Progress Metrics

_Updated automatically by `/fetch-activities`. Cycling activities with both power meter and HR data only._
_Last updated: 2026-07-04_

---

## Efficiency Factor (NP ÷ Avg HR)

**What it measures:** How many watts your heart produces per beat. As aerobic fitness improves, this number rises — the same or more power at a lower heart rate.

**How to read it:** Compare like-with-like. Z2 rides cluster in one band, threshold sessions in another. The trend within each cluster over 6–8 weeks is the signal — not the absolute number or cross-zone comparisons.

**Rule of thumb:** A sustained upward trend of ~5% in EF on Z2 rides over 8 weeks indicates meaningful aerobic adaptation.

**Data quality note:** EF is only logged when Strava confirms device watts (`device_watts: true`). Estimated power (rides without a power meter) is excluded — it's based on speed + gradient and introduces systematic error that would corrupt the trend. Backfilled rows below were sourced from consistency log notes where device_watts status is unknown; treat them as indicative only.

| Date | Activity | Zone | Duration | NP (W) | Avg HR | EF | Notes |
|------|----------|------|----------|--------|--------|----|-------|
| 2026-05-31 | Evening Ride (return from sailing) | Z3 | 1h 04m | 233 | 164.7 | 1.415 | First ride post-sailing. High HR = detraining expected. |
| 2026-06-06 | Epic Ride | Z2 | 6h 35m | 168 | 153 | 1.098 | Long ultra-endurance effort — HR drift over 6h expected. Not a clean Z2 EF baseline. |
| 2026-06-25 | Frankie Weavers group ride | Z3 | 2h 02m | 204 | 157 | 1.299 | Unplanned group ride. Elevated effort vs pure Z2. |
| 2026-06-27 | Morning Ride | Z2/Z3 | 2h 21m | 198 | 149 | 1.329 | Unplanned — best EF so far. Comparable effort to Jun 25, lower HR = positive signal. |
| 2026-06-29 | Ramp Test + Z2 Extension | Mixed | 1h 30m | 203 | 148 | 1.373 | Ramp test session — not comparable to pure Z2 EF. FTP confirmed 276W (best 1-min 368W). |
| 2026-07-02 | MyWhoosh - VO2max 3min #2 | Z5 (interval) | 58m | 194* | 145.6 | 1.332* | VO2max intervals — 6×3min @ 293–295W. *Avg watts (NP unavailable); EF not comparable to Z2 due to recovery lap averaging. |
| 2026-07-04 | Really quite miserable out | Z2 | 3h 52m | 176 | 141.5 | 1.244 | First structured long Z2 baseline of new block. NP squarely Z2 (63.8% FTP). HR well-controlled throughout. Wet conditions ("miserable"). |

---

## 4-Week EF Summary (Cycling)

_Computed at each `/review`. Compares avg EF this 4-week block vs previous 4-week block._

| Period | Rides with EF data | Avg EF (Z2) | Avg EF (all) | vs Prior Period |
|--------|-------------------|-------------|--------------|-----------------|
| W22–W25 (May 31 – Jun 20) | 2 | 1.098* | 1.257 | — (baseline) |
| W23–W26 (Jun 6 – Jun 27) | 3 | 1.098* | 1.242 | +0.0 (insufficient Z2-only data) |
| W24–W27 (Jun 13 – Jul 4) | 4 | **1.244** | 1.295 | Baseline established — first clean Z2 long ride logged (Jul 4: 1.244). Jun 27 morning ride (1.329, Z2/Z3) supports upper end. |

_*Jun 6 epic — long duration with HR drift; not a clean Z2 EF reference. Jul 4 is the first truly structured long Z2 of the new block — use as the EF baseline going forward._

---

## What to Watch From Here

From the new training block (W26+), structured sessions will give cleaner EF readings:
- **Tuesday sweet spot / threshold** — track EF separately; will be ~1.2–1.5 depending on effort
- **Saturday long Z2** — this is the primary EF trend signal; target a rising EF band over 8–12 weeks
- **Sunday easy Z2** — secondary confirmation signal

Once 4+ Z2 rides are logged, a reliable baseline will emerge. The Jun 27 morning ride (EF 1.329) is a reasonable early reference point for Z2/Z3 effort.
