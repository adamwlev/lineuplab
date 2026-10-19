# v18 per-case preview

Read a completed arm before all arms in that quarter have finished:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v18_case_preview \
  --run-dir experiments/cache/joint_capability_2026_09_28_v18_prod \
  --origin 2018q3 \
  --arm A_GATE
```

Default: average all three seeds' calibrated predictions, then compute metrics.
Add `--seed 17` (or23/41) to inspect a completed seed without waiting for the
others. All requested seeds must be complete. `--arm` accepts the seven v18
arms and retained J_POINT_BOTH/J_BOTH/J_ACTION_BOTH/O_ORDER controls.

Outputs direct, half, checkpoint_average and checkpoint_average_half alongside
the same saved baselines as v18 scoring. Half is exactly50% NN plus50%
additive_defense. Units are points/100 for RMSE, MAE and bias; r²/correlation
are unscaled. This is one quarter, not a cumulative leaderboard.

Options: `--sort r2` (also corr/rmse/mae/bias; bias sorts by absolute size),
`--slice novel` (also all/recurring/thin/debut). The population is offensive
five-man quarter cells with at least50 possessions, predicted against their
actual opponents. Empty slices and undefined correlations remain explicit.

The tool verifies the sibling `<run-dir>_scored` manifest and completed input
receipts. It uses v18's corrected prior-only forecast calibration and refuses
to skip a missing earlier calibration quarter. It does not require the current
origin's scored receipt or any other current arm to finish. No inference,
training, database access, scoring advancement or run-output writes. Immutable
input verification can take a few seconds; non-default slices also reconstruct
dated support labels in memory.

Pilots are supported for engineering checks, but explicitly labeled cold-start
and not comparable to the full-history production experiment. A preview is a
point-score inspection, not a coherence or OOD-uncertainty evaluation.

Implementation is standalone: no frozen v18 producer or artifact was modified.
Tests: `python -m unittest tests.test_v18_case_preview tests.test_v18_report`.
Verified2026-09-28: nine tests passed; all19 preview rows for the completed
2016q1/A_GATE/seed17 pilot reproduce its saved scorecard within1e-9, including
undefined correlations. Production's unfinished2018q3 case correctly reports
PREVIEW_UNAVAILABLE rather than showing partial-seed results.
