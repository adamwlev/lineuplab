# v16 post-training repair protocol — 2026-09-26

Implementation correction, not a new model experiment. Adam authorized all
post-training steps. No neural refits, original-artifact edits, input rebuilds,
scraping, database mutation, promotion, deployment or commit.

## Sources and destination

Source: `experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`.
Derived destination: `experiments/cache/joint_capability_2026_09_26_v16_repaired`.
Separate bounded test prefixes may be used; never substitute partial results
for this full campaign. Preserve original code, receipts, data and reports.

The derived tree links only verified immutable native artifacts and contexts.
It owns its manifest, scored histories, analyses, diagnostics and audit. Do not
invoke trainers or the deterministic-channel producer against this tree.
New producers and the original source manifest/receipts are fingerprinted.

## Corrections

1. Use `forecast`, never player-ID column `p0`, for the native point prediction
   in the broad offensive-five calibration history. Validate identity, exposure
   and outcome aggregation independently. Rebuild every origin/arm/seed/view
   chronologically; all 2015 histories remain warmup and all 44 2016–2026
   quarters remain primary. No original scored history is reused.
2. Preserve the registered expanding, possession-weighted, nonnegative-slope
   affine calibration with identity below 30 completed prior cells. No new
   thresholds, penalty, alternate fitting population or evaluation-period fit.
   A legitimately zero slope remains allowed; constant forecasts are flagged,
   not assigned an invented correlation.
3. Preserve every native/checkpoint ledger, common-calibrated historical control,
   cohort, blend weight, seed average and original experiment definition.
4. Explicitly map v16 `recovery` to v15 `rebound` when reading archived event
   NLL/exposure summaries. Verify field presence/finite values and matched
   exposure. Do not silently omit a family or replace missing fields with zero.

## Execution and acceptance

- Prepare a separate resumable derived namespace only after verifying source
  cases, inner/final receipts and the fixed 22×48×3 schedule.
- Regression tests cover the original column collision, repeated same-five
  rows, independent numpy aggregation, identity preservation, cutoff filtering,
  cold starts, nonnegative slopes, constant flags, event-schema failure and
  deterministic interrupted/resumed calibration without original writes.
- Reproduce the documented 2025q1/J_POINT_BOTH diagnostic across three seeds;
  require 7,747 prior cells and matching numerical predictions/metrics.
- Recompute sufficient statistics and cells for every registered population,
  seed and view. Check native forecasts and controls unchanged on the same
  rows; verify 8,345 broad cells / 1,013,999 possessions and 5,607 legacy cells /
  726,364 possessions across primary quarters.
- Report before/after all/novel/recurring scorecards and quarter/season changes.
  Do not treat the prior leaderboard as a valid scientific baseline.
- Regenerate registered point analyses. Run event/profile/native-channel
  diagnostics (not affected by point calibration), and complete the previously
  unreached fixture, average-opponent, uncertainty and saved-state audit stages.
  Anything that consumes calibrated outputs uses the derived histories.
- Independently check histories against native row keys/weights, in addition to
  the saved-state and temporal audit. Report prediction, basketball coherence
  and uncertainty independently; no score alone establishes a product pass.
- Durable append-safe logs, progress by stage/origin, resumable receipts. Do not
  wait silently on a long analysis; provide its live-log/status commands.

## Subsequent studies

Reliability/noise-ceiling and multi-NN+additive ensemble studies remain separate
supplemental experiments under roadmap R15. Freeze their detailed bounded
protocols before running them; use the repaired baseline and earlier quarters
only for any member/weight/hyperparameter selection. This correction does not
authorize choosing new NN designs or modifying the frozen v16 comparisons.
