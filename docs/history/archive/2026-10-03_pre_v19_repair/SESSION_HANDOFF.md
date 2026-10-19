# Current handoff — v19 launched (2026-09-30)

## Current state and authority

The frozen v19 production campaign is running. Full launch was already approved
conditional on readiness; all readiness checks now pass. Adam accepts roughly65h
and explicitly deferred the optional reference-validation optimization.
Direct implementation only; no delegation, new scraping/database access,
input rebuilds, promotion or deployment. Adam authorized a checkpoint commit
after launch. This checkpoint records the downstream/launcher implementation,
tests and documentation on top of32ab995d; generated run artifacts stay local.

Read [launch report](reports/joint_capability_v19_launch.md) for exact commands,
pipeline stages, acceptance evidence, resource caveats and preserved failures.
[Runtime amendment](reports/joint_capability_v19_runtime_authorization.md) and
[frozen plan](JOINT_CAPABILITY_V19_PLAN.md) remain unchanged.
Previous [prelaunch checkpoint](reports/joint_capability_v19_prelaunch.md) is
historical, not the current launch status.

## Live operation

Root: experiments/cache/joint_capability_2026_09_30_v19_prod.
Detached supervisor73644, caffeinate73645. Verified three initial2015q1control
workers. Two earlier shell background attempts exited without work; no duplicate
supervisor. Do not launch another process while this one owns the run lock.

```bash
tail -f experiments/cache/joint_capability_2026_09_30_v19_prod/logs/run.log

bash experiments/run_joint_capability_v19.sh status \
  --run-dir experiments/cache/joint_capability_2026_09_30_v19_prod

bash experiments/run_joint_capability_v19.sh report \
  --run-dir experiments/cache/joint_capability_2026_09_30_v19_prod \
  --sort r2 --slice all --view half
```

Case epoch logs: <run>/queues/<origin>_train/logs/<origin>_<arm>_s<seed>.log.
Stage/active-job details: status.json and queues/<stage>/status.json.
On error inspect failure.json and the corresponding child log before restarting.
The report requires a complete origin; primary2015warmup exclusion means NO_ROWS
at first is correct. Read-only case preview is documented in the launch report.

## Frozen scope and resources

720cases/1,440fits, seven original pilots reused by explicit mappings,713new
cases. Five arms,48origins, seeds17/23/41; three CPU processes/one thread.
Fitter, epoch cap96, patience8, min_delta1e-5 and scientific protocol unchanged.
No pilot-result model selection. Reference, CLOCK and margin panels are separate.

All-in estimate58.04h selected /68.71h at1.2× native training stress.
Includes4.68h controls/downstream/barriers. Cap scenario232.85h is not expected.
Training concurrency scaling is not divided a second time by the2.542× benchmark.

Storage:54.48GiB additional including7.22GiB controls/derived/temp/logs.
Readiness free65.10GiB -> projected10.63GiB free, required reserve10GiB.
Tight, not guaranteed:20% native storage sensitivity would leave1.18GiB.
The supervisor checks before each origin/post stage and stops below10GiB.
No additional deletion authorized; preserve original artifacts and discuss
capacity if stopped. Peak measured individual training worker4.02GiB on16GiB host.

## Verified evidence

Common prefix experiments/cache/joint_capability_2026_09_30:

- _v19_pipeline_pilot1 and siblings: complete production downstream graph
  rehearsed in324.39s, no new NN fits. All output/audit stages passed.
- _v19_control_parity1:1,152 full-history retained calibration checks,
  max prediction difference2.84e-14points/100.
- _v19_native_review_pilot1: both estimators/environments audited, including
  checkpoint-average conditional re-inference. Max late event error3.59e-13.
- _v19_fixture_precision1: all seven models on all eligible pilot observed
  high-support matchups; physical-ledger and permutation checks pass.
- _v19_launch_readiness1: final PASS, resource/test/source receipts.
- experiments/cache/v19_production_tests2.log:51tests PASS.

All earlier foundations/pilots and original downstream outputs remain intact.
Source/labels/replay/micro/pilot evidence lives in _v19_sources2,_v19_labels1,
_v19_replay1,_v19_micro1,_v19_pilot1. Initial pilots took30m18s; no cap hits.
No new scientific winner or overall three-pillar pass.

Versioned fixture adapter v19_basketball_v2.py accounts for mixed-float32 phase
point re-association (max5.57e-7points/100 on audited cohorts), while retaining
strict float64 physical-ledger/value/loss/gradient guards. No training or saved
forecast changed. See report for precise interpretation and preserved failed
observed_pilot1/no-registered-early-fixture prefixes.

## Retention mode — mandatory

Completed restart cleanup retired19,420optimizer payloads from9,792v16–v18fits.
Final/averaging weights, predictions, original receipts and frozen code remain.
Ledger: experiments/cache/completed_resume_retention_2026_09_30.
Plan SHA256:825e76b9b847ab3b3ea046b5b302cac772d093a4c6f32be6e3319be7af826cd2.

Read [operations](docs/ARTIFACT_RETENTION.md). Every Python process consuming
these sources uses artifact_retention exec; children use its python_job helper.
The v19 shell wrapper does this automatically. Never use legacy strict checks
to conclude the intentionally retired restarts are corruption.

## Automatic completion and next action

After training the script automatically runs average-opponent integration,
event/conversion diagnostics, fixed role/transfer/analogue analysis, all eligible
context curves/support/saturation, fixtures in both directions, independent
native audit, own-candidate U0/U1, persistence/full covariance, registered17/28
contrasts, point audit and final supporting tables. All original populations,
three standards and no-promotion boundaries remain unchanged.

The background script runs independently of chat; no automatic assistant wakeup
is promised. At next check: inspect process/status/logs, not old prelaunch HOLDs.
After COMPLETE, review the registered scientific results and all acceptance
receipts, write reports/joint_capability_v19_review.md, and update scorecard,
state, roadmap and handoff. No commit without new authority. Finite-game bands
do not establish latent arbitrary-lineup coverage. Named basketball checks are
falsifiable, not forced rankings. Missing2014q4 additive inner diagnostic remains
explicitly unavailable only for2015q1warmup; never substitute a future fit.

## Review/planning direction — 2026-10-02

Adam explicitly favors considering game-situation context in **player-profile
estimation** for v20 and agrees with the broader design reflection. The canonical
[roadmap framing](MODEL_RESEARCH_ROADMAP.md#v19-review-and-v20-framing--agreed-2026-10-02)
records upstream versus decoder adjustment, identifiability/recoverability checks,
training stabilization, and concrete transport/latent-uncertainty work. Use these
to frame the completed v19 analysis and subsequent v20 proposal. They do not amend
v19, establish a winner from interim tables, or authorize new fits/input rebuilds.

[Previous checkpoint](docs/archive/2026-09-30_pre_v19_launch/SESSION_HANDOFF.md)
preserves the prelaunch integration state.
