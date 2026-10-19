# V20 prior-only uncertainty integration — 2026-10-06

The full-calendar descriptor producer and chronological uncertainty consumer
are implemented. A fixed 12-quarter retained-reference rehearsal and the two
isolated V20 pilot dates are complete. No neural training, source rebuilding,
historical cleanup or promotion occurred. Full-campaign launch is still held.

## Scope and quantitative evidence

The [pre-execution protocol](v20_uncertainty_integration_protocol.md) fixes
2015q1–2017q4, saved three-seed J_POINT_BOTH predictions under alias P_BASE,
three mean views and two additive/parent controls. It does not choose a new
model or retune the point predictions. The primary view remains
checkpoint-average-half. All uncertainty quantities use completed prior quarters.

- **254 dated empirical snapshots**, 252 newly derived and two exactly reused:
  128.84 seconds, 117.68 MiB. No GLM or NN fits.
- **12 chronological quarters**: 75.73 seconds, 94.63 MiB. Persistent models
  first become identified at 2016q2 (30-pair/two-season minimum); nested penalty
  validation begins at 2016q3. Earlier point predictions remain available.
- **Two isolated pilot dates**: 18.49 seconds, 28.53 MiB. 26/14 mean forecasts,
  3,016/1,456 model-pair rows across two splits. All persistent models correctly
  remain NOT_IDENTIFIED. These totals repeat the same lineups across candidates
  and splits; they are not independent observations.

Matched primary-view repeated-lineup subset, 2016q2–2017q4:
**416 pairs / 832 halves / 105,110 possessions**, >=8 games and >=100 possessions
per off5-quarter, balanced-date split. Nominal 95%; equal-pair likelihood and
equal-half coverage/width. Width units are points/100; tau² units are
(points/100)². Higher log score is better.

| Uncertainty model | Coverage | Mean width | Mean interval score | Joint log score | Mean persistent tau² |
| --- | ---: | ---: | ---: | ---: | ---: |
| U1 constant discrepancy | 94.351% | 46.734 | 59.835 | −7.789989 | 24.203 |
| U_ROLE | 94.351% | 46.762 | 59.732 | −7.789702 | 24.359 |
| U_ROLE_CLOCK | 94.351% | 46.760 | 59.719 | −7.789628 | 24.349 |

The small log-score difference (+.000361 for role+clock versus U1) is not a
substantive improvement claim. This bounded rehearsal exercises identification,
prefix-specific tuning and serialization; it is not the full registered V20
uncertainty comparison. For illustration, the final balanced-date role+clock fit
selects lambda1, role slope .2779 and clock slope .1241. Those are standardized
variance slopes, not basketball effects or point adjustments.

Chronological halves have lower coverage: U1 92.428%, role+clock 92.428%, joint
log scores −7.990135/−7.989581. This sensitivity uses the same games, not an
independent replication. U0 whole-quarter coverage is 93.581% on 1,667 broad
cells / 208,444 possessions across all eight primary quarters; its population
and forecast horizon differ from the pair table, so widths cannot be compared
as if they were the same target. No density is invented for U0.

All these intervals concern finite observed outcomes against actual opponents.
They do **not** validate coverage for arbitrary hypothetical latent lineup quality.
Uncertainty fitting never alters or suppresses a point prediction. The mean
models' accuracy is unchanged; basketball coherence remains a separate pending
analysis, not a conclusion from these numbers.

## Verification

- Independent real-data audit: all12quarters, 98 identified final fits and
  72 penalty subfits, 4.28 seconds. Reconstructs paired residuals from original
  matchup predictions/game assignments; checks temporal/candidate/split history,
  prefix-specific noise and RMS scales, penalty rule, matrix-form bivariate
  likelihood, empirical U0 quantiles, Gaussian intervals, interval scores and
  primary sufficient-statistic pooling with 2015 excluded.
- Dedicated cold audit: empty identified summary is correct; 60/32 unidentified
  variance fits, all point forecasts finite, no fabricated persistent variance
  or gate. Whole-game split disjointness and no-history noise checked.
- **49 V20 tests pass in 7.21 seconds**, including held-out-outcome poisoning,
  future-history rejection, archived bootstrap parity, cold finite fallback and
  common U1/transport export schema.
- All254descriptor snapshots and all42original pilot receipts/producer hashes
  reverified. New completed sources/outputs are now fingerprinted; extensions
  require new modules/output prefixes, not silent edits.

Two audit-only mistakes are preserved: the first independent audit expected a
row-level `actual` column instead of deriving 100×points/possessions; corrected
audit uses a new output prefix. The generic audit then correctly reached the
cold empty summary but rejected its CSV-inferred empty-index dtype. A dedicated
cold-state audit verifies the empty table and unidentified state explicitly.
Neither issue changed uncertainty outputs, original artifacts or tolerances.

## Artifacts and operations

All roots below are under `experiments/cache/`:

- `v20_descriptor_library_2026_10_06`
- `v20_uncertainty_retained_rehearsal_2026_10_06`
- `v20_uncertainty_pilot_2026_10_06`
- `v20_uncertainty_retained_audit_2026_10_06_v2`
- `v20_uncertainty_cold_audit_2026_10_06`

Durable logs: `v20_implementation_2026_10_04/logs/descriptor_library.log`,
`uncertainty_retained_rehearsal.log`, `uncertainty_pilot.log`,
`uncertainty_retained_audit2.log`, `uncertainty_cold_audit.log`,
`uncertainty_checkpoint_tests.log`, `uncertainty_final_verification.log`.
All jobs finished; no polling or training process remains from this stage.

Each uncertainty quarter exports `pairs.csv.gz`, whole-game `assignments.csv.gz`,
`models.json` (including nested selector trace), `support.json`, dated descriptor
NPZs, `finite_intervals.csv.gz`, `joint_details.csv.gz`, `scores.csv` and receipts.
Root `primary_summary.csv` contains pooled sufficient sums and derived metrics.
Candidate histories and the two split methods remain separate.

Generic full V20 consumer is `experiments.v20_uncertainty --scoring ... --library
... --out ...`, with `--retained-rehearsal` only for the fixed archived check.
Native consumers require the documented retention wrapper. Do not rerun completed
stages in fresh directories merely to advance the project.

## Next prelaunch work

1. New fixture and average-opponent inference adapter: explicit per-arm profile
   bank and saved normalizer, retained controls, compact/native case resolver,
   endpoint and five-checkpoint ledger mixtures. Preserve fixed fixtures, mixed-
   date Korver disclosure, exact context integration and512/4096opponent sampling.
   The v19 adapter reads a common old library/context and direct weights only;
   it cannot be reused unchanged for adjusted V20 arms or the primary view.
2. Finish extra descriptive controls, three-seed mixture event scores, fixed
   basketball/average-opponent pilots, dated fixture uncertainty/risk thresholds,
   persistence/covariance and registered comparison schemas.
3. Implement and rehearse the full supervisor/completion graph, include downstream
   time/storage in readiness, then provide verified commands and await launch
   authority. Completed neural pilots and profile libraries must be reused.
