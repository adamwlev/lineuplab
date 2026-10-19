# Current handoff — v20 historical profile library running (2026-10-04)

## State and authority

All 720 v19 cases, 48 rolling scorecards and all post-training stages are complete.
Independent scientific review: [v19 review](reports/joint_capability_v19_review.md).
No active v19 work remains. No scorer was promoted.

Adam authorized the completed downstream repair, continuation and review, then
on2026-10-04 requested a documentation/commit checkpoint followed by detailed
v20 planning, then approved implementation while freeing storage. Bounded
experiments/pilots are authorized; full NN launch still needs approval. No
production NN fits, database access, input rebuilds, scraping or deployment.
Direct implementation only. V19 completion is committed as **8e8b325f**. Protocol:
[JOINT_CAPABILITY_V20_PLAN.md](JOINT_CAPABILITY_V20_PLAN.md).
Implementation/evidence: [v20 checkpoint](reports/joint_capability_v20_implementation.md).

Latest authority: Adam requested **all prescribed prelaunch steps**. The full
historical derived-profile build is in scope and now running after Adam freed
storage. No full NN campaign, cleanup or commit is authorized.

## V20 implementation and completed prerequisites

Joint clock/player GLM, exact joint curvature, strict-date pilot library and
97/49-feature bridge implemented. P/S5 trainer primitives pass exact old-policy
toy replay and inner/final resume.22targeted tests pass in5.41seconds
(`storage_prelaunch_all_tests.log`), including native macOS capacity and
immediate-reserve enforcement. Production
case/analysis pipeline remains unfinished; no full-run command exists yet.

Synthetic suite:640/640converged fits in488s;20replicates/scenario/family,128draws.
Overlapping-deployment common prediction error improves13.2% counts,0.88%location,
0.77%recovery; conversion tied. Nominal95coefficient coverage only~40%, including
zero-clock control. Diagnosis documents heavy fixed-ridge shrinkage (conversion
fitted/true projection slope.139); no generator or penalty changes. Lead approved
bounded real profile pilots, not a latent-uncertainty claim. Source arithmetic
audit passes16real-date/bank/family panels.

Completed: `experiments/cache/v20_synthetic_full_2026_10_04`,
`experiments/cache/v20_synthetic_review_2026_10_04`,
`experiments/cache/v20_profile_source_audit_2026_10_04`.
Logs: `experiments/cache/v20_implementation_2026_10_04/logs/`.
Pilot gate: `experiments/cache/v20_profile_pilot_gate_2026_10_04.json`.

Completed bounded pilot: `experiments/cache/v20_profile_pilots_2026_10_04`.
Independent review: `experiments/cache/v20_profile_review_2026_10_04`.
All122receipts verified;96/96fits converged in71.5minutes queue wall time;
max289iterations, projected gradient9.957e-6, joint-draw residual9.979e-9.
All16selected penalties match the original library. Matched parent-grain
reference mean-rate NLL differences range−0.0792% to+.0222%, i.e. near ties,
not a neural point result. Conditional state NLL has different constants and is
not compared directly to the old parent NLL. Twelve chosen penalties remain at
the frozen grid's low edge, in both old/new libraries; no grid changes made.

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v20_profile_pilot status \
  --out experiments/cache/v20_profile_pilots_2026_10_04

tail -f experiments/cache/v20_implementation_2026_10_04/logs/profile_pilots.log
```

Per-chain verbose GLM logs are under the pilot's `queue/logs/` directory.

New `v20_calendar.py` implements the full strict-date build without changing
frozen pilot producers:2,032snapshots,384annual candidate slots,64annual fits
reused read-only. Pilot snapshots are cold-started and are NOT silently reused
as warm-started production snapshots. Three workers, retention-wrapped children,
immutable manifests, resume, progress and fail-stop storage checks. No NN launch.

Storage forecast:16.993GiB additional library,34.241GiB available required
including25% size stress,3GiB temporary headroom and10GiB reserve. After Adam's
cleanup, macOS reports112.23GB/104.52GiB available for user-requested work, but
only22.73GiB immediately free. The original filesystem-only gate refused at
21GiB; read-only Foundation queries explain the discrepancy, not a failed cleanup.
New `v20_storage.py` uses the supported macOS user-requested capacity API for
preflight and falls back conservatively to filesystem free space on API failure.
The unchanged **13GiB immediate-space floor between fits** remains in force:
if OS reclamation does not keep up, stop resumably. No manual purge, deletion or
dummy allocation. Storage helper/policy is frozen in the new library manifest;
original completed pilot producers and the scientific plan remain unchanged.
This requirement excludes the later NN campaign.

Active root: `experiments/cache/v20_library_full_2026_10_04`.
Detached caffeinate launcher PID13402; verify status rather than trusting an old
PID. Three workers/one thread, eight chronological chains, no NN auto-launch.
Preparation passed; first live workers are offense/location, defense/location
and offense/counts. Durable log: `calendar_build.log` under implementation logs.
First offense/counts cold snapshot (2009-03-01) and its warm-start successor
(2009-04-01) are complete and independently receipt-verified:28/24iterations,
32joint draws each, max residual7.44e-15/2.13e-14. Strict prefix dates and prior-
snapshot warm-start metadata pass. Location workers also converged their first
fits and are completing joint curvature/draws. No worker failure at handoff.

Read-only progress and live supervisor log:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v20_calendar status \
  --out experiments/cache/v20_library_full_2026_10_04

tail -f experiments/cache/v20_implementation_2026_10_04/logs/calendar_build.log
```

Detailed GLM iteration/draw/progress logs live under the library's `queue/logs/`.
Do not launch a second supervisor. `run --out <root> --review
experiments/cache/v20_profile_review_2026_10_04` is only for an explicitly checked
resume after the current process exits, through the same logged detached setup.

New `v20_case_inputs` retains raw normalizers/parent/loss scales and replaces
only the new bank's adjusted normalizer. `v20_evaluate` supplies conditional and
reference outputs for no-context and FULL models, including complete-ledger
checkpoint averaging and conditional-state exports. Full case/scoring/rehearsal
integration remains pending, not hidden behind these primitives.

Real saved-control replay passes: `experiments/cache/v20_control_replay_2026_10_04_v4`.
Four cases: P_BASE/P_CONTEXT ×2016q1/2026q4,seed17; zero refits,68.4seconds.
Selected inner objectives and final direct/averaged outputs in both environments
checked. Current unchanged evaluators match bit-exactly. Archive drift max~1.07e-7
points/100 uses the existing v19 mixed-float32 archival guard, not relaxed
float64 objective tests. Earlier over-strict failed outputs are preserved.
Details/limitations in the implementation report. No active replay remains.

## V20 approved design

Eight-cell profile × decoder × selection comparison; two completed controls
reused and six new neural arms (864case slots/1,728inner-final fits before pilot
reuse). New clock-adjusted actor/teammate/defender profile library; raw inputs
unchanged. FULL clock decoder is retained as the contextual comparator.
S5 selects the five-checkpoint forecast on inner validation, keeping optimizer,
objective and outer split unchanged. Primary view: checkpoint-average-half for
every arm, with usual direct/half views preserved.

Also: fixed synthetic recoverability experiments; all original basketball and
transfer checks; candidate-specific U0/U1 and a small nested role/clock-deployment
discrepancy experiment with two prespecified mean models. No forced rankings,
causal deconfounding claim or synthetic latent-coverage certification.

Provisional runtime60–100h including the new254×8snapshot library. This is not a
measured launch estimate or extension of v19's65h approval. See the current
library-only storage requirement above; full campaign needs more space.
No deletions authorized. Follow the staged pilots,
source-preservation rules, temporal audits and empirical comparisons.

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

Let the historical profile build complete, inspect all receipts, then complete feature
sentinel, NN-case/analysis integration, eight NN pilots, downstream rehearsal and
measured full-campaign launch forecast. Preserve frozen producers now bound into
completed pilot/review/replay receipts; corrections need versioned successors.
Do not run a nonexistent full v20 command or change v19 files. The calendar's
`run` command builds profiles ONLY and never queues NN training.

All prior repair/review code, tests and documentation are in8e8b325f. Seven combined
tests passed again before commit; log experiments/cache/v19_commit_verification_2026_10_04.log.
Current uncommitted work includes the v20 plan/navigation and new implementation,
tests and evidence report. No commit was requested in this implementation turn.
Many local cache directories are untracked; never blindly stage the cache tree.
No second commit was made after the requested v19 checkpoint.

[Prior checkpoint](docs/archive/2026-10-04_pre_v20_plan/SESSION_HANDOFF.md)
preserves the resumption details. Background scripts do not imply an automatic
assistant wakeup.
