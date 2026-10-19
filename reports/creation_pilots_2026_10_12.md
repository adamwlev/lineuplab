# Creation pilots: residuals by best passer, and a forward correction — 2026-10-12

Both pilots are exploratory and post hoc to the
[confirmatory run](capacity_confirmatory_results_2026_10_12.md). Its
secondary cohorts showed both models overpredicting offenses whose best passer
is below 5 assists per 100 (−2.3 ± 0.5, half blend, row level).

## 1. Row-level residuals grow as the best passer weakens

`scripts/creation_residuals.py`.
- **Rows.** All rows of the 44 primary quarters, actual defenses,
  possession-weighted, points per 100, season SEs.
- **Forecast.** The reference (J_POINT_BOTH) checkpoint average, seed-mean.
- **Best passer.** The lineup's highest origin-dated assist rate.

| Best passer (ast/100) | Possessions | Half | Calibrated neural | additive_defense |
| --- | ---: | ---: | ---: | ---: |
| All rows | 2,760,546 | −0.75 ± 0.13 | −0.46 ± 0.17 | −1.04 ± 0.21 |
| 3–4 | 12,764 | −1.67 ± 1.48 | −0.48 ± 1.47 | −2.86 ± 1.49 |
| 4–5 | 91,826 | −2.40 ± 0.65 | −1.36 ± 0.59 | −3.44 ± 0.73 |
| 5–6 | 176,147 | −1.42 ± 0.35 | −0.51 ± 0.33 | −2.32 ± 0.49 |
| 6–8 | 747,724 | −0.98 ± 0.13 | −0.69 ± 0.18 | −1.27 ± 0.18 |
| 8–10 | 930,938 | −0.66 ± 0.22 | −0.52 ± 0.22 | −0.80 ± 0.29 |
| 10–15 | 791,725 | −0.30 ± 0.15 | −0.06 ± 0.21 | −0.53 ± 0.21 |

The additive half carries most of the gradient. It has no creation term.

## 2. On the scored cells the gradient mostly disappears

Here are the same residuals on the benchmark's own population: offense-five
cells with at least 50 possessions in a quarter, 2016–2026.

| Best passer | Cells | Half | Calibrated neural | additive_defense |
| --- | ---: | ---: | ---: | ---: |
| 0–4 | 21 | −4.23 | −2.74 | −5.72 |
| 4–5 | 179 | −0.57 | +0.44 | −1.58 |
| 5–6 | 391 | +0.15 | +0.81 | −0.51 |
| 6–8 | 2,295 | −0.37 | −0.25 | −0.48 |
| 8–10 | 3,337 | −0.08 | −0.11 | −0.05 |
| 10–15 | 2,842 | +0.44 | +0.44 | +0.45 |

**Reading.**
- The row-level gradient lives in short-lived lineups. A creation-poor
  lineup that struggles is pulled before it reaches 50 possessions, so its
  rows stay overpredicted. One that survives is forecast about right.
- This is in-quarter deployment selection, the same mechanism as the
  first-25-possessions effect. It is not a forecast bias that a forward model
  can exploit.
- **Caveat on the confirmatory report.** Its "real unusual cells" residuals
  are row-level, so they carry the same selection.

## 3. A forward-fitted creation correction does not help

`scripts/creation_correction_pilot.py`.
- **Correction.** forecast + c × max(0, log 10 − log best passer).
- **Fit.** c is fitted at each origin on earlier quarters' forward residuals,
  either all rows or the scored cells. Only the slope is applied.

| Fitted on | c at 2026q4 (half) | Pooled Δ half r² | Seasons positive |
| --- | ---: | ---: | ---: |
| All rows | −2.2 | −0.0007 | 4/11 |
| Scored cells | −1.5 | −0.0028 | 3/11 |

Correcting each half separately gives the same results.

## What follows

- **The extrapolation can't be estimated from the scored population.** Real
  lineups that last show no creation shortfall the models miss, apart from 21
  cells below 4 assists per 100.
- **It stays an asserted assumption.** An offense-side law for lineups
  without a handler belongs in the assumption band, as already planned. It
  should be a declared hinge beyond the observed range, labeled as an
  assumption, not fitted.
- **Not a pillar-1 lever.** Neither correction improves the benchmark.
