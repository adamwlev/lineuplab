# V19 production launch — 2026-09-30

The complete pipeline is implemented, rehearsed and launched under Adam's
recorded authorization. Original protocols, fitters, completed artifacts and
seven native pilots are unchanged. No additional neural fits were used in this
prelaunch work. No model promotion, deployment, database access, scraping or
commit.

## Scope and measured readiness

Five arms (C_FIXED, C_CLOCK, C_FULL, C_ALLOC, C_MARGIN), 48 origins, three seeds:
720 cases / 1,440 inner-final fits, with seven compatible completed cases reused
and **713 newly trained cases**. Three CPU workers, one numerical thread each.
Epoch cap96, patience8, min_delta1e-5 and all scientific cutoffs remain frozen.
The optional reference-validation speedup remains deferred.

The new `v19_launch_readiness1` receipt reports:

| Item | Estimate / measurement |
| --- | ---: |
| Remaining native training, including origin scheduling | 53.36h |
| Controls, downstream analysis, scoring and barriers | 4.68h |
| All-in selected-epoch projection | **58.04h** |
| All-in with1.2× native training time | **68.71h** |
| All cases at epoch cap, not expected runtime | 232.85h |
| Additional native storage | 47.26GiB |
| Additional controls/derived/log/temporary allowance | 7.22GiB |
| Free storage at readiness | 65.10GiB |
| Projected remaining free space | **10.63GiB** |
| Required reserve | 10GiB |
| Largest measured individual training worker | 4.02GiB |

The approximately65h [runtime amendment](joint_capability_v19_runtime_authorization.md)
supersedes the original48h/54h targets. 58h is a projection, not a completion-time
promise;69h is the training-stress scenario. Neither is a hard process timeout.
The projection uses measured pilot workloads, unchanged native timings, an
explicit three-slot schedule and completed v18 full-history U1 timing (not the
unidentified pilot's zero fitting cost). It does not divide native costs again
by the measured2.542× parallel speedup.

Storage is tight. An additional20% native compression/size sensitivity would
leave only1.18GiB, so the central estimate is not a bound. The supervisor stops
before the next origin or post-training stage if free space is below10GiB;
there is no automatic deletion. It also rechecks projected capacity before the
initial launch. The1GiB temporary allowance is included above. Do not authorize
new cleanup implicitly if the guard stops the run.

## Evidence and checks

New prefixes below `experiments/cache/joint_capability_2026_09_30`:

- `_v19_control_parity1`: all1,152 retained-control calibrations reproduced
  across48origins ×4models ×3seeds ×2views; max prediction discrepancy
  2.84e-14points/100. Both calibrated direct and half match the archives.
- `_v19_pipeline_pilot1` and its derived siblings: the actual production
  downstream graph completed in324.39s. Uses the two existing pilot dates,
  all seven fits, no new training, and retention-aware child processes.
- `_v19_native_review_pilot1`: independent numpy/scipy event and point arithmetic,
  including saved-checkpoint conditional event re-inference. Max late event
  discrepancy3.59e-13; point ledger identity8.53e-14.
- `_v19_fixture_precision1`: all7models on1,139early/1,391late eligible observed
  matchups, exact physical-ledger integration and permutation checks. Max
  phase-point re-association5.57e-7points/100; max permutation6.27e-5points/100.
- `_v19_launch_readiness1`: completed resource/provenance/test acceptance.
- `experiments/cache/v19_production_tests2.log`: **51tests pass**, including
  future/calibration contracts, full17/28 contrast families with11season units,
  mask-aware proper scores, child failure propagation, reuse/grid checks and
  unchanged float64 guards. Shell syntax and launch/status/report CLI verified.

The rehearsal independently reproduces all five pilot scoring panels. Its
statistics remain isolated one-seed cold starts: no pooled partial-arm tournament,
new winner or fresh scientific confirmation. Earlier pilot numbers and all
original reports remain preserved in the [previous checkpoint](joint_capability_v19_prelaunch.md).

### Diagnostic precision correction

The original fixture diagnostic compared a weighted sum of per-state point
totals to points reconstructed from mixed expected ledgers at a float64-only
tolerance. The NN's phase computations can contain float32 products; their
re-association can differ by sub-micro-point amounts. This is not a training,
calibration or saved-prediction change.

`v19_basketball_v2.py` explicitly permits one float32 scale epsilon **only for
this point re-association when the decoded dtype is float32**, and records the
actual discrepancy. This applies to any mixed-dtype arm, not only C_FIXED (where
it was first noticed). Float64 physical-ledger comparisons retain1e-8/1e-10
guards, and the zero-context training value/loss/gradient proof is unchanged.
The product's native reference point value comes from the exact mixed ledger.
Conditional observed curves are exported directly, without reinterpreting their
possession-weighted capture averages as live-ball mixture capture.

Preserved failed prefixes: `_v19_observed_pilot1` (old point re-association
assertion) and `_v19_basketball_pilot3/2016q1` (no registered fixture at that
date, correctly rejected). Corrected outputs use new prefixes; the production
fixture roster remains32fixtures on10dates. No added pilot fixture or ranking.

## Automatic stages and derived outputs

For each origin: fit three dated point-control jobs; train remaining new cases;
advance strictly earlier-origin calibration; print a matched reference-half
leaderboard and completed-case count. Every fitting subprocess uses the
[retention wrapper](../docs/history/ARTIFACT_RETENTION.md). Reuse mappings point to
unchanged pilots; nothing is copied over a completed artifact.

After all48origins, the supervisor runs:

1. Average-opponent512 integration, fixed first20cells/date at4096.
2. Native conversion/count proper scores, game residuals and unchanged
   transfer/retrospective role labels.
3. All observed high-support lineups (>=200possessions, >=5games), per-state
   response curves, context coefficients/support/saturation for every seed.
4. Additional role-share forecasts versus the unchanged role-change library;
   location/renewal/capture ledgers and exact point/budget accounting.
5. Registered fixture matchups in both directions, separate native/calibrated/
   additive/half values. No enforced center, Adams or Jokić ranking.
6. Independent native point/event audit, both estimators and environments.
7. Candidate-specific prior-only U0/U1,80/95coverage, proper scores and transfer.
8. Fixed random-game/chronological persistence splits and full cross-channel
   covariance. CLOCK target adjustment only for reference errors, never twice.
9. Primary17point and28event contrasts,10,000season bootstrap draws and exact
   2^11season swaps with separate full-family Holm corrections; all seasonal,
   quarter, original-population, transfer and analogue tables.
10. Independent point/calibration audit and additional role, conversion,
    native/calibration-bias, covariance and context-support evidence tables.

Reference and realized-context scoreboards remain physically separate. The
unchanged primary population is8,345cells/1,013,999possessions over44quarters;
transfer146cells/47,419possessions. Unknown latent hypothetical quality remains
explicitly unvalidated even if finite-game coverage or fixture means improve.
The2015warmup is not part of the primary leaderboard. Missing2014q4 additive
inner-control diagnostics remain explicitly unavailable, not replaced by future
fits. No scientific design change follows from partial results.

## Operations

Run root: `experiments/cache/joint_capability_2026_09_30_v19_prod`.
Sibling directories use `_controls`, `_scored`, `_average`, `_diagnostics`,
`_observed`, `_event_roles`, `_basketball`, `_native_review`, `_uncertainty`,
`_persistence`, `_summary`, `_audit`, `_evidence`.

Detached supervisor **73644**, caffeinate helper73645; initially verified three
2015q1point-control workers. The first two shell-background attempts did not
survive the tool session and produced no work. A separate-session subprocess
launch succeeded; process listing confirmed no duplicate supervisor.

Live supervisor log:

```bash
tail -f experiments/cache/joint_capability_2026_09_30_v19_prod/logs/run.log
```

Status (receipt-presence progress, with active queue status):

```bash
bash experiments/run_joint_capability_v19.sh status \
  --run-dir experiments/cache/joint_capability_2026_09_30_v19_prod
```

Leaderboard (only completed-origin comparisons;2015excluded):

```bash
bash experiments/run_joint_capability_v19.sh report \
  --run-dir experiments/cache/joint_capability_2026_09_30_v19_prod \
  --sort r2 --slice all --view half
```

Also supports `--view direct`, `checkpoint_average`, `checkpoint_average_half`,
`--sort corr|rmse|mae|bias`, `--slice novel|recurring|thin|debut`, and diagnostic
`--environment conditional_clock|conditional_margin`. No completed primary
origin legitimately prints `NO_ROWS`, not fake zero metrics.

Per-case epochs live in
`<run>/queues/<origin>_train/logs/<origin>_<arm>_s<seed>.log`.
Controls have corresponding `<origin>_controls/logs/` files. Post-training
queues have their stage names. Locks reject concurrent writers.

Read-only single-case preview after its fit and all earlier scoring histories:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u \
  -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v19_case_preview \
  --scoring experiments/cache/joint_capability_2026_09_30_v19_prod_scored \
  --origin 2016q1 --arm C_CLOCK --seed 17
```

If the supervisor has stopped, investigate `failure.json` and the failed queue
log first. To resume the unchanged campaign **only after confirming no active
writer**, the normal terminal background command is:

```bash
nohup /usr/bin/caffeinate -i bash experiments/run_joint_capability_v19.sh run \
  --run-dir experiments/cache/joint_capability_2026_09_30_v19_prod \
  >> experiments/cache/joint_capability_2026_09_30_v19_prod/logs/run.log 2>&1 < /dev/null &
```

After completion: inspect all acceptance/failure receipts and registered results;
write `reports/joint_capability_v19_review.md`, update the scorecard and current
state on all three standards, and discuss the next experiment. Automatic stages
do not write a scientific conclusion or promote a scorer. No automatic agent
wakeup or monitoring is promised; the background supervisor itself runs the
queued stages without the chat session remaining open.
