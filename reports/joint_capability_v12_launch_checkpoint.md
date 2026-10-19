# Joint capability v12 launch checkpoint

Date: 2026-09-14  
Status: ledger repair preflight complete; clean production rerun **not launched**

## Frozen experiment

Day6 tests two jointly trained additive-anchored hybrids on the unchanged
quarterly forward protocol:

- `ADAPT_CONTEXT`: `H = A + b + C_theta`
- `ADAPT_VALUE_CONTEXT`: `H = A + b + G_psi + C_theta`

`A` is the saved, corrected and calibrated causal additive forecast. `C` is the
exact interaction residual from the synthetic prior-365-day exposure-weighted
anchor. The flexible arm adds an identity-free nonlinear player-profile value
head `G`; it has no player IDs or known-pair terms. Both arms train the V9_SPREAD
backbone against event labels and the combined team forecast. Inner validation
selects epochs; outer-quarter outcomes never select or stop training. There is
no post-hoc calibration or outer-driven rescue arm.

The run is frozen at 48 origins x 2 arms, with an inner selection fit and a reset
full-prefix fit for each arm-origin: 96 arm-origins / 192 optimizer fits. The
four 2015 origins are descriptive warmup; 2016--2026 is primary.

## Day5 audit closeout

The new, non-mutating follow-up prefix is
`experiments/cache/joint_capability_2026_09_13_v11_audit_followup/`. It contains
present-day hashes of the actual inputs, exact SSE attribution, possession-
weighted case lists and ledgers at 100/200-possession thresholds, slice
scorecards, independent centering diagnostics and the historical Korver
injection. The original v11 production artifacts remain untouched.

The 256-five product residual mean (estimate +/- Monte Carlo SE) was
`+0.0286 +/- 0.0352` for 2016q1 EXPOSURE, `-0.1039 +/- 0.0372` for 2016q1
UNIFORM, `-0.0171 +/- 0.0259` for 2026q4 EXPOSURE and `-0.0444 +/- 0.0275`
for 2026q4 UNIFORM. These finite draws are diagnostics, not exact orthogonality
tests. The 2015 Korver-state injection into the 2026q4 fixture is explicitly an
unmatched-vintage mechanism check, not a matched forecast.

## Preflight and pilots

Production preflight passed under `no_database()`:

- 897,778 grouped rows
- 447,735 rows with causal saved additive offsets
- 48 additive source origins
- complete replay reconciliation against overlapping saved additive cells
- 2016q1 inner/final point-supervised rows: 26,013 / 37,443
- 2026q4 inner/final point-supervised rows: 199,112 / 199,303

The original clean two-origin pilot prefix is
`experiments/cache/joint_capability_2026_09_13_v12_pilot_final5/`. All four
completion receipts, file hashes and gzip CRCs verify. It took 134.4 seconds.

| origin | arm | selected epoch | MAE | RMSE | raw R2 | bias | novel RMSE |
|---|---|---:|---:|---:|---:|---:|---:|
| 2016q1 | ADAPT_CONTEXT | 2 | 8.74042 | 11.27813 | .07054 | +1.53047 | 10.38115 |
| 2016q1 | ADAPT_VALUE_CONTEXT | 2 | 8.73698 | 11.28242 | .06983 | +1.53484 | 10.37276 |
| 2026q4 | ADAPT_CONTEXT | 4 | 8.84588 | 11.98072 | .02215 | +1.06612 | 13.33220 |
| 2026q4 | ADAPT_VALUE_CONTEXT | 4 | 8.88294 | 11.99398 | .01998 | +1.13201 | 13.38800 |

On the two pooled pilot origins, strict/flexible/additive RMSE was
11.63518/11.64409/11.64977. HALF and GLOBAL were better at 11.56910 and
11.56929. The flexible head therefore did not help either pilot origin. These
origins were prescribed for correctness and cost and are far too small a sample
for efficacy selection. The alternate uniform anchor changed individual pilot
predictions by as much as 1.22 points in 2016q1 and 2.71 points in 2026q4; this
is labeled sensitivity, not calibrated latent-mean uncertainty.

The measured ETA is 43--81 minutes. Later origins are costlier; automatic
reporting runs after all training and needs no second training launch.

## 2026-09-14 production incident and repair

The first production launch stopped after 74/96 completed arm-origins while
saving 2024q2 `ADAPT_CONTEXT`. Training was finite; a post-fit event-accounting
assertion required the aggregated decoder total to equal the separately
aggregated five player allocations within `2e-5` points/100. Among the 74 saved
origins the maximum was `1.90735e-5`; the failing deterministic cell was
`2.09808e-5`. Both are float32 summation-order noise at a roughly 110-point
scale, not missing offense or a model discrepancy.

The repair raises only this accounting tolerance to `5e-5`, records the exact
maximum discrepancy in every completion receipt and log, and changes no model,
objective, data, epoch selection, prediction or report formula. A fresh 2024q2
two-arm validation completed under the repaired fingerprint: strict error
`2.09808e-5`, flexible error `1.52588e-5`. The old partial production prefix is
preserved unchanged. To honor the frozen fingerprint rule, its 74 fits are not
transplanted; the clean rerun uses
`experiments/cache/joint_capability_2026_09_14_v12_prod_ledgerfix/`.

The interrupted prefix contains 33/44 primary origins (4,284 cells / 558,579
possessions), so its numbers are informative but incomplete and not the frozen
final comparison. On that partial primary population, RMSE is 10.8614 strict,
10.8506 flexible, 10.8065 additive and 10.7627 HALF. Novel RMSE is
11.8348/11.8217/11.7990/11.6945 in the same order. The flexible head is modestly
better than strict so far, while both trail the baselines; missing late origins
can still change the registered season-level comparisons.

## Verification

- Relevant v11/v12 suite: 17/17 passed.
- Full repository suite: 759/760 passed. The sole failure is the expected
  reproducibility guard reporting ten untracked v11/v12 producer files. The
  task forbids staging/committing, so this is recorded as a failure, not waived
  or called a pass.
- Real-data training smoke exercised nonzero backbone, flexible-head and scalar
  bias gradients.
- Report generation completed successfully against the pilot-shaped smoke
  population after its integration issues were corrected.
- Wrapper shell syntax, production protocol/code/source fingerprints and the
  fresh production causal-offset artifact all verify.
- A deliberately preserved failed pilot attempt demonstrated semantic
  `FAILED` status with error type, message, elapsed time and completed-fit count;
  the corrected attempt used a new prefix and completed normally.

## Deliverable checklist

- [x] Day5 source-manifest, SSE, weighted-case, slice, centering and historical
  Korver follow-up outputs under a new prefix.
- [x] Exact anchored `F=B+C` implementation and both registered trained arms.
- [x] Quarter-causal additive replay with per-row provenance, component ledgers,
  known-player flags, source hashes and saved-cell reconciliation.
- [x] Inner validation selection followed by reset/full-prefix refit; no outer
  outcome enters stopping or calibration.
- [x] Frozen A/N/HALF/GLOBAL, v11, TEAM_1 and anchored-reference controls wired
  into generated reports.
- [x] Both prescribed origin pilots, gradient/accounting telemetry, alternate
  anchor sensitivity, measured cost and durable logs.
- [x] Run locking, atomic fit receipts, hash/CRC validation, completed-fit resume,
  PID/command/exit records and semantic run states.
- [x] Automatic scorecards, season contrasts, event readout, exact SSE
  attribution, weighted cases/ledgers, prior-only outcome intervals and dated
  basketball panel implemented and smoke-tested without database access.
- [x] Focused and repository-wide verification run with the untracked-producer
  guard reported honestly.
- [ ] Full 96-arm-origin training and full-population reports: awaiting Adam's
  explicit launch authorization.
- [ ] Independent scientific review and final product decision: necessarily
  deferred until the full results exist.

The test suite exercises the central algebra, initialization, gradient,
permutation, chronology, gzip/receipt and inherited runner invariants. It does
not claim mid-optimizer resume, and no separate exhaustive fault-injection test
was added for every prose scenario in Day6 section 10. The run's actual failed
pilot path, full historical suite and fresh no-database preflight supplement
those focused tests. This limitation does not change the frozen estimand.

Durable logs are under `reports/joint_capability_v12_*.log`; the authoritative
pilot log is `reports/joint_capability_v12_pilot_final5.log`, the repair
validation log is `reports/joint_capability_v12_ledger_repair_2024q2.log`, and
the authoritative preflight log is
`reports/joint_capability_v12_production_preflight_ledgerfix.log`.

## Commands

Launch from the repository root only after Adam authorizes it:

```bash
cd /Users/adam/Documents/basketball
nohup bash experiments/run_joint_capability_v12.sh experiments/cache/joint_capability_2026_09_14_v12_prod_ledgerfix > experiments/cache/joint_capability_2026_09_14_v12_prod_ledgerfix/logs/production.log 2>&1 & echo $!
```

Follow the durable live log:

```bash
cd /Users/adam/Documents/basketball
tail -f experiments/cache/joint_capability_2026_09_14_v12_prod_ledgerfix/logs/production.log
```

Read semantic status:

```bash
cd /Users/adam/Documents/basketball
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.joint_capability_v12_run status --run-dir experiments/cache/joint_capability_2026_09_14_v12_prod_ledgerfix
```

If the process stops between completed arm-origins, rerun the exact launch
command. Verified completion receipts are hash-checked and skipped. Resume is at
the completed-fit boundary; mid-fit optimizer continuation is not claimed.

## What remains

The production run, automatic full-population analyses, independent scientific
review and final `reports/joint_capability_v12_review.md` do not exist yet. They
must not be inferred from the two pilot origins. After production reaches
`ANALYSIS_COMPLETE`, review prediction, basketball behavior and uncertainty on
equal footing and then update the model decision. No scorer is promoted
automatically.
