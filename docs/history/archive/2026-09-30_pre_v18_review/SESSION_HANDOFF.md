# Current handoff — v18 ready, not launched (2026-09-28)

## Authority and current status

Adam approved direct v18 implementation and bounded pilots. No delegation,
commit, database access, scraping, input rebuild, scorer promotion or deployment.
Full training has NOT been authorized or launched. All bounded jobs have finished.
Last requested commit remains095183b1 (v17 review/literature/ideas checkpoint).

Read the [frozen plan](JOINT_CAPABILITY_V18_PLAN.md), then the
[implementation handoff and verified commands](reports/joint_capability_v18_implementation.md).
The seven arms, three seeds,48 origins and all three acceptance standards are
unchanged. Production is ready at0/1,008 cases (2,016 inner/final fits).

## Verification

-28 tests passed in the final preflight.
-14 real-data micro cases /168 batches passed in53.52seconds.
-All seven full2016q1/seed17 pilots completed in17.17 wall minutes on three workers.
 Selected7 epochs except A_SELECT/A_ACCOUNT at9; no cap hits.
-14 paired12-step slow/fast real-input checks passed; largest prediction
 difference.00003483pts/100. Gate kernels and selective moments were optimized
 without changing parameter schema or equations. Slow producers remain intact.
-48 archived calibration-view replays match exactly (two dates/four controls/
 three seeds/two views).
-End-to-end pilot scoring/average/role/uncertainty/summary passed. Real historical
 U0 regression has nonzero identified broad and all-off5 bands. Cold pilot U1 is
 explicitly unidentified, not a scientific uncertainty result.
-288 dated contexts and576 retained-control cases checked across48 origins.

Measured planning estimate45.09h all-in;20% longer training53.52h, not a
confidence interval or guarantee. The earlier4h downstream-allowance stress
scenario (54.96h) is retained in preflight.json. Measured downstream reference
is2.512h. See the [runtime measurement note](reports/joint_capability_v18_runtime_measurements.md).
Storage54.19GiB estimated additional+10GiB reserve versus97.30GiB free.

## Implementation and artifacts

Native ready root: experiments/cache/joint_capability_2026_09_28_v18_prod.
Readiness/code/source fingerprints: manifest.json and preflight.json there.
CLI wrapper: experiments/run_joint_capability_v18.sh, using v18_ready_run for
measured preparation and the frozen v18_run supervisor/worker underneath.
Production fits use v18_fast_fit/v18_fast_case and FastModel18. Model18 and
original v18_fit remain the fingerprinted pilot/reference implementations.

Completed bounded prefixes: joint_capability_2026_09_28_v18_micro1,
_v18_pilot1, _v18_fast_bench1, _v18_engineering under experiments/cache.
Pilot derived siblings: _v18_pilot1_scored, _average, _role, _uncertainty, _summary.
Supervisor logs live under each prefix's logs; individual pilots under queue/logs.
No original completed artifact or frozen producer was overwritten.

The full runner automatically produces chronological scorecards,23 point and36
separately corrected event contrasts, player-role/transfer diagnostics, average
opponents,32 fixtures/10dates, real analogues, direct/half U0/U1, independent
source/metric review and a generated HANDOFF.md. The full production downstream
sequence itself is still unexecuted; a pilot is not a campaign-level pass.

## Scientific position retained

The [v17 independent review](reports/joint_capability_v17_codex_review.md) remains
the latest completed campaign interpretation. New point arms essentially tied
J_POINT_BOTH; D_SHAPE worsened count/conversion fidelity, and flow did not solve
five centers. Retain the v16 point reference, not a newly promoted scorer.
The original v17 U0 aggregate-status defect was repaired only in separate
review outputs; its original all-off5 aggregate remains invalid. v18's new
summary validates FINITE_GAME_BAND rows before aggregation in both populations.

No v18 accuracy/coherence/OOD improvement is claimed from engineering pilots.

## Precise next step and dirty work

Read-only monitoring addition: `experiments.v18_case_preview` now previews one
completed arm/origin (all three seeds by default, optional `--seed`), without
waiting for other arms at that origin. [Commands and interpretation](docs/V18_CASE_PREVIEW.md).
Uses corrected v18 prior-only calibration; no frozen producer or run output
changes. Nine preview/report tests pass. New standalone code/test/doc are
uncommitted; no training launch or commit was performed for this addition.

Wait for Adam to launch or explicitly authorize the full run. Verified background
launch/live-log/status/leaderboard commands are in the implementation handoff.
Status and report commands were executed: ready_not_launched,0/1,008 cases,
NO_ROWS (expected). Repeated prepare verified receipts without launching fits.

New v18 code/tests, frozen plan, measurement/scoring/analysis/implementation
notes, and navigation/state/handoff edits are uncommitted. Numerous unrelated
generated cache artifacts remain untracked: never blanket-stage. A commit needs
authority from the current task. Do not edit fingerprinted producers after this
readiness checkpoint; fixes require a new version/output namespace.

[Preceding checkpoint](docs/archive/2026-09-28_pre_v18_ready/SESSION_HANDOFF.md)
preserves the v17 review and v18 in-progress implementation record.
