# v13 large experiment — implementation checkpoint

Codex, 2026-09-14. Read `JOINT_CAPABILITY_V13_EXPERIMENT.md` for the frozen
scientific design. Implemented directly, without delegation. Full production
training has **not** been launched. Production preflight passes; the verified
launch instructions are below.

## Why this experiment

The useful result from v5–v10 was complementary error: additive is stronger on
established fives, the neural model is stronger on novel fives, and their blend
helps overall. v11–v12 showed that extracting a particular neural subtotal and
putting it on additive value can destroy both that signal and the meaning of a
basketball mechanism. v13 tests that interface explicitly, while also testing
specific limitations of the native decoder and teammate summaries.

- **Objective/readout:** event-only, joint event/team training, training the
  entire additive–NN blend, team-only training, and an intervention residual
  with messages disabled rather than an anchored ANOVA subtraction.
- **Basketball mechanisms:** learned nonnegative creation-shortage and excessive
  workload responses, separately and jointly; the complete event ledger remains
  visible. These are named structural assumptions, not synthetic score targets.
- **Representation:** upstream individual profile correction, cross-capability
  teammate covariance, receiver-specific attention, and dated role-history
  features. Each has a matched simpler comparator.
- **Robustness:** dropout and two fixed second-seed replications. Their spread is
  labeled sensitivity, not a validated posterior interval.

Twenty trajectories means eighteen distinct designs plus two seed replications.
The full run has 48 quarterly origins, 960 arm-origins and 1,920 inner/final fits.
2015 is warmup; 2016–2026 is the primary 44-quarter comparison. Each fit has a
96-epoch ceiling, patience eight and min_delta 1e-5. Inner validation is the
preceding quarter. The model is reset and refit on the full past prefix for the
selected epoch count. Outer evaluation outcomes never select that count.

## Implementation

- `experiments/joint_capability_v13_model.py`: registered models and constraints.
- `experiments/joint_capability_v13_fit.py`: shared causal normalization,
  objectives, epoch selection and reset refitting.
- `experiments/joint_capability_v13_run.py`: manifests, real process lock,
  phase receipts, exact control joins, rolling calibration and verbose logs.
- `experiments/joint_capability_v13_report.py`: automatic point/support
  scorecards, season contrasts, event summaries, disagreement ledgers,
  basketball interventions, finite-outcome intervals and seed/dropout diagnostics.
- `experiments/run_joint_capability_v13.sh`: one-command sequential launcher.
- `tests/test_joint_capability_v13.py`: algebra, symmetry, gradients, receipts,
  causal calibration and interval-boolean regression tests.

Prediction, basketball coherence and honest uncertainty retain equal standing.
No ranking is forced for Jokić/Korver/Westbrook. No chemistry by player identity,
scraping, database access, input-cache rebuild, deployment, promotion or commit.
Actual opposing fives and a defensive rebound opportunity loop remain deferred
because the frozen grouped inputs do not identify those additions.

## Operational guarantees and limits

Each inner and final fit is saved before report validation. Identical-producer
resume verifies hashes and reuses completed phases. Completed origin outputs
also undergo gzip CRC verification. A report-only repair can write a new derived
prefix while leaving original fits/results untouched. Scientific code or input
changes cannot silently reuse an existing production fingerprint.

Logs are append-only. A second launch cannot overwrite the first process's log
or status. This is phase-boundary resume, **not** mid-epoch optimizer recovery:
an interrupted unfinished phase starts over. Do not edit experiment code or
update input data while production is running. Old dirty work is preserved.

This is exploratory development on repeatedly studied historical years, not an
untouched confirmation set. Twenty comparisons do not make the observed winner
conclusive. Synthetic fixtures do not establish OOD interval coverage, and the
model still does not directly price the actual defense faced.

## Verification and pilot results

All twenty one-epoch arm-origin smoke fits completed. Their report exposed a
duplicate `possessions` keyword, fixed without changing training. A separate
derived-only prefix successfully regenerated the report from those saved fits.
Original failed directories remain untouched. All four full-length prescribed
pilots completed under `joint_capability_2026_09_14_v13_pilot_dev1`, including
automatic reports and 39 basketball intervention rows. The final all-arm smoke
also completed, under `joint_capability_2026_09_14_v13_smoke_final`.

| pilot | selected epochs | fit/output seconds | RMSE | additive | old HALF |
|---|---:|---:|---:|---:|---:|
| 2016q1 E_BASE | 17 | 58.6 | 11.20261 | 11.40826 | 11.24254 |
| 2016q1 B_BASE | 12 | 45.9 | 11.19151 | 11.40826 | 11.24254 |
| 2016q1 J_SUPPLY_LOAD | 10 | 45.7 | 11.08361 | 11.40826 | 11.24254 |
| 2026q4 J_SUPPLY_LOAD | 28 | 110.0 | 12.02011 | 11.88578 | 11.88590 |

These are operational pilots, **not** campaign efficacy estimates. Their point
calibration history is only the selected pilot origins; the late pilot's raw
RMSE is 11.99893. Production has all intervening quarters. The latest constraint
fixture reduces five-Gobert offense by 4.28 calibrated points versus constraints
disabled, but its 118.99 still exceeds the conventional reference's 117.83.
Neither the accuracy question nor the five-center mean problem is settled.
No arm, loss, stopping rule or mechanism was changed in response to these results.

The four pilots took 263 seconds including reporting. Linear extrapolation from
arm-origin times is 17.35 hours; budget **18–30 hours**, potentially longer for
slow-converging/heavier arms. This is an estimate, not a runtime ceiling. The
measured saved group-output footprint suggests roughly 5 GB for the campaign,
plus reports and checkpoints; available disk at verification was 261 GiB.

Durable verification log: `reports/joint_capability_v13_verification.log`.
Current targeted suite: 18 passing tests, including all-arm subtests.
`joint_capability_v13_lock_test.log` records rejection of a concurrent launcher;
`joint_capability_v13_resume_test.log` records completed-output verification and
a no-write/no-training resume. The plan, model and fitting-module hashes still
match the full pilots (`joint_capability_v13_scientific_provenance.log`). Later
runner/report changes added input identity checks, additive player ledgers,
named disagreement cases, parameter-growth output and completed-run no-op
handling; no training algorithm changed. The last all-arm smoke exercised the
new ledgers and reports. A separate `...v13_pilot_review` prefix regenerates
the latest reporting from original pilot fits without overwriting them.

## Launch, live log, status and resume

Run from a terminal on this Mac:

```bash
cd /Users/adam/Documents/basketball
nohup /usr/bin/caffeinate -i bash experiments/run_joint_capability_v13.sh run >> reports/joint_capability_v13_launcher.log 2>&1 &
```

The launcher runs **all 20 trajectories and the automatic analyses**. It uses
the already-preflighted `experiments/cache/joint_capability_2026_09_14_v13_prod`.
`caffeinate` prevents idle system sleep while it runs; keep the Mac plugged in
and do not rely on it to override closing the lid or manually sleeping.

Live log:

```bash
tail -F /Users/adam/Documents/basketball/experiments/cache/joint_capability_2026_09_14_v13_prod/logs/training.log
```

Status:

```bash
cd /Users/adam/Documents/basketball
bash experiments/run_joint_capability_v13.sh status
```

Resume after an interruption: rerun the same background-launch command. It
verifies and reuses complete phases. An already-complete campaign is a verified
no-op. A scientific fingerprint mismatch is a stop, not permission to overwrite
or start again indiscriminately; bring that error back for review.

The live log prints each epoch, validation objective, selected epoch/patience,
gradient norm and mechanism coefficients. `RESULT` lines print MAE, RMSE, r²,
bias and RMSE differences versus additive, V9, HALF and GLOBAL for all, novel
and recurring fives. Negative RMSE differences favor the new arm. Cumulative
readouts label their available quarters and primary/warmup population.

## After completion

Status should be `ANALYSIS_COMPLETE` with 960 arm-origins. Read these under the
production prefix:

- `reports/scorecard.csv`, `season_contrasts.csv`: matched predictive comparisons,
  registered contrasts and nominal season uncertainty, including secondary blends.
- `reports/fit_summary.csv`, `parameter_growth.csv`: event families, caps,
  optimization cost and whether added modules actually moved.
- `diagnostics/largest_disagreements.csv.gz`: highest weighted harms/benefits
  versus HALF at 100/200 possessions, names, additive coefficients and NN ledgers.
- `diagnostics/basketball_panel.csv`, `basketball_allocations.csv.gz`: final and
  native ratings, messages/constraints disabled, per-player event mechanisms.
- `reports/interval_summary.csv`, `diagnostics/interval_forecasts.csv.gz` and
  `interval_sources.csv`: prior-only finite-outcome calibration/support slices.
- `diagnostics/seed_disagreement.csv.gz`, `dropout_sensitivity.csv`: limited
  robustness evidence, not validated latent-mean OOD uncertainty.

Review all three standards and the registered contrasts before proposing another
fit or promotion. No automatic winner selection. If only reporting fails, final
fits are already saved. A corrected report can use a new output prefix:

```bash
bash experiments/run_joint_capability_v13.sh report --run-dir experiments/cache/joint_capability_2026_09_14_v13_prod --output-dir experiments/cache/joint_capability_v13_report_repair_1
```

That command requires the output prefix not to exist and never retrains.
