# Current handoff — v19 scientific review complete (2026-10-04)

## State and authority

All 720 v19 cases, 48 rolling scorecards and all post-training stages are complete.
Independent scientific review: [v19 review](reports/joint_capability_v19_review.md).
No active training/analysis from this task remains. No scorer was promoted.

Adam authorized the completed downstream repair, continuation and review, then
on2026-10-04 requested a documentation/commit checkpoint followed by detailed
v20 planning. This checkpoint contains no new neural fits, database access,
input rebuilds, scraping or deployment. Direct implementation only.
The next step is v20 planning, not an automatically authorized training campaign.

## Main conclusions

Primary: 8,345 cells / 1,013,999 possessions, 44 quarters, 2016–2026.
Half r²: reference J_POINT_BOTH .162915, C_FIXED .162937, C_CLOCK .159471,
C_FULL .159127, C_ALLOC .158154, C_MARGIN .156975; additive_defense .146023.
No new incremental registered point winner. Retain the existing point reference.

C_FULL beats C_CLOCK in all four conditional event families in all 11 seasons,
Holm .027344 each. Situation matters beyond counts, but conditional accuracy
is not better common-environment player estimation. Frozen C_FIXED captures
much of the conditional point benefit; joint retraining does not improve it.

Checkpoint-average-half recovers C_FULL to .161724, versus reference .162989.
This motivates a bounded stabilization comparison, not outer-selected epochs.
Center-heavy free-throw projections worsen in joint arms; all nine still favor
the legal-center fixture against both Jokić fixtures. Transfer results do not
improve. Small allocation gains do not improve role-change point predictions.

Primary-only U0 half nominal95 coverage: reference 93.47% cell/93.19% weighted;
C_FULL 93.68%/93.20%, with wider bands and slightly worse interval score.
Debut coverage remains about90–91% weighted. U1 is near-tied to slightly worse.
No validated arbitrary-lineup latent-quality uncertainty; no coverage gate.

## Artifacts and verification

Original root: experiments/cache/joint_capability_2026_09_30_v19_prod.
Its RUNNING status is stale: the original supervisor stopped after training and
average integration. Do not restart it. Training/scoring took49.24h; average
integration2.39h. All original producers, targets and outputs remain unchanged.

Completed continuation:
experiments/cache/joint_capability_2026_10_03_v19_posttrain1.
All10stages finished in5,792.05s; its status is COMPLETE. Its frozen
scientific_review_pending=true records the automation boundary, not current
human-review status. Do not rewrite that completed artifact.
Stage siblings use _summary, _evidence, _persistence, _audit, etc.
Original _scored and _average are reused read-only.

Independent review:
experiments/cache/joint_capability_2026_10_04_v19_review2; durable log adds .log.
All217 continuation receipt hashes checked; 270 metric rows independently
recomputed, keys/weights/blends checked, 19,926 mirror records consistent.
Native audit720cases: maximum point error1.14e-13, event error6.66e-16.
Point audit144panels/5,472calibration checks: maximum5.68e-14.

Automated pooled uncertainty includes2015warmup. Review2 re-pools saved quarterly
statistics over2016–2026 only, matching earlier reviews; use its
finite_uncertainty_primary.csv and persistent_uncertainty_primary.csv.
Review1 is preserved, superseded by review2's corrected count-table export.
No trained model, interval or source table changed.

Accounting repair evidence:
[repair report](reports/joint_capability_v19_accounting_repair.md),
experiments/cache/v19_accounting_repair_2026_10_03.
Three mismatched input rows, none in primary evaluation. Explicit
observed_accounting preserves original recorded targets and complete covariance.
13 earlier targeted/production tests passed plus exact unaffected-quarter parity.
Seven combined review/accounting tests pass in this session.

## Read-only operations

```bash
bash experiments/run_joint_capability_v19.sh report \
  --run-dir experiments/cache/joint_capability_2026_09_30_v19_prod \
  --sort r2 --slice all --view half

/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest \
  tests.test_v19_completed_review tests.test_v19_accounting_repair
```

The review report gives the verified reproduction command with a fresh output
prefix. No reason to repeat expensive post-training stages merely to read results.

## Retention mode — mandatory

Completed v16–v18 optimizer restarts were deliberately retired. Final/averaging
weights and original manifests remain. Every native consumer process must enter
the retention wrapper, including each child of a future queue.

Ledger: experiments/cache/completed_resume_retention_2026_09_30.
Plan SHA256:825e76b9b847ab3b3ea046b5b302cac772d093a4c6f32be6e3319be7af826cd2.
See [operations](docs/ARTIFACT_RETENTION.md). No further cleanup authorized.

## Next decision and dirty work

Agree a bounded v20 design: context-adjusted player profiles first, separate
profile/decoder effects, equally applied inner-only training stabilization,
recoverability checks and concrete transport/latent-uncertainty hypotheses.
C_FULL's event gains deserve a control, not automatic adoption. Clock and margin
are not interchangeable. No new profile builder or fit is authorized yet.

Uncommitted repair code: v19_observation_accounting, v19_diagnostics_v2,
v19_persistence_v2, v19_evidence_v2, v19_posttrain_resume and accounting tests.
New review code: experiments/v19_completed_review.py and
tests/test_v19_completed_review.py. Repair/review reports and current
handoff/state/scorecard/roadmap/documentation map are updated; archives preserve
displaced checkpoints. Many local cache directories are untracked; never blindly
stage the cache tree. These changes are the authorized v19 completion checkpoint;
the subsequent planning handoff will record its commit hash.

[Prior checkpoint](docs/archive/2026-10-04_pre_v19_review/SESSION_HANDOFF.md)
preserves the resumption details. Background scripts do not imply an automatic
assistant wakeup.
