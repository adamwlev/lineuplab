# Current handoff — v20 neural pilots running (2026-10-06)

## Authority and current job

Adam authorized the prescribed prelaunch work after the profile library finished.
Direct implementation only; no delegation. Eight bounded NN pilots are running.
**Full neural campaign remains unlaunched and needs separate approval.** No
commit, cleanup, source rebuild, scraping, database mutation or promotion authorized.

Pilot root: `experiments/cache/v20_nn_pilots_2026_10_06`.
Detached caffeinate launcher PID47716 (historical identifier; verify live status).
Three CPU workers, one numerical thread each. Late S_ADJ/S_BOTH cases start first;
the remaining cases fill available slots. Respect Adam's unrelated concurrent project.
The runner cannot launch the full campaign.

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v20_pilot status \
  --out experiments/cache/v20_nn_pilots_2026_10_06

tail -f experiments/cache/v20_implementation_2026_10_04/logs/nn_pilots.log
```

Epoch/batch/validation logs:
`experiments/cache/v20_nn_pilots_2026_10_06/queue/logs/<origin>_<arm>_s17.log`.
Supervisor log records case starts/completions; status shows each fit's epoch,
selected endpoint and patience counter. Inner stopping is adaptive, so epoch/96
is a cap fraction, not a reliable percentage of wall time.

Do not launch a second supervisor. After confirming a stopped job and reviewing
its failure, resume the same immutable pilot with the retention-wrapped
`experiments.v20_pilot run --out <pilot-root>` through the detached logged setup.
Exact RNG/optimizer/selection-window restart is implemented. No automatic assistant
wakeup is implied by background execution.

## Required reading and frozen design

[Plan](JOINT_CAPABILITY_V20_PLAN.md), [implementation evidence](reports/joint_capability_v20_implementation.md),
[state](JOINT_CAPABILITY_STATE.md), [product standards](CONTEXTUAL_MODEL.md) §1–2.

Eight-cell profile × decoder × selection factorial; P_BASE/P_CONTEXT reused from
v16 J_POINT_BOTH/v19 C_FULL. Six new arms: P_ADJ, P_BOTH, S_BASE, S_CONTEXT,
S_ADJ, S_BOTH. Pilot roster: all six at2016q1/s17, plus S_ADJ/S_BOTH at2026q4/s17.
Full roster later:864case slots/1,728inner-final fits, less exact compatible pilots.
Primary checkpoint-average-half for every arm; all other views remain visible.
S5 selects a five-ledger mixture on the prior completed quarter, never outer data.
No selection of arms/epochs/profiles from pilot outer accuracy.

Raw inputs and raw normalizers unchanged; only adjusted97/49profile bank and its
prefix-only normalizers change. Unknown players retain priors, not a coverage gate.
All three product standards remain coequal. No known-pair chemistry or forced rankings.

## Completed prelaunch evidence

- Historical library `experiments/cache/v20_library_full_2026_10_04`:
  **2,032/2,032snapshots**, eight254-date chronological chains, no failures.
  Queue wall120,389.9seconds (**33.44hours**). Do not restart this completed build.
- Deep derived audit `experiments/cache/v20_library_audit_2026_10_06`:
  **4,562receipts verified**,384annual candidates including external pilot reuse;
  all fits converged, temporal/warm-start/gauge/draw checks passed. Snapshot maximum
 238iterations; max draw residual9.9999e-9 (<2e-8). All2,032player penalties match
  old library. Coefficient/SD and392channel panels exported. These are profile
  diagnostics, not NN point accuracy or OOD coverage.
- Real feature audit `experiments/cache/v20_feature_audit_2026_10_06`:
  both pilot dates ×inner/final pass. In-memory offense/defense sentinels change
  actual trained-model predictions through the memo, with raw tensors unchanged.
  Historical training uses47/63distinct snapshots, not final-date backfill.
  Original raw contexts/loss scales stay byte-identical; wrong provenance rejected.
- Saved-control replay `experiments/cache/v20_control_replay_2026_10_04_v4`:
  P_BASE/P_CONTEXT ×two dates, zero refits. New/current evaluators bit-exact;
  archival drift<=1.07e-7pts100 within existing mixed-float32 guard. Original
  float64 objective tolerances unchanged. No archived inner-window weights exist.
- Bounded profile pilots/review completed:96fits,71.5minutes,122receipts.
  `v20_profile_pilots_2026_10_04`, `v20_profile_review_2026_10_04` under cache.
- Synthetic640fits complete: common-environment recovery improves13.2% counts,
 .88%location,.77%recovery; conversion tied. Nominal95coefficient coverage~40%
  due severe fixed-ridge shrinkage/prior mismatch: explicitly **not** an uncertainty
  pass. Do not change generator/penalties to repair inspected results.
- Twelve case/fit/evaluation/selection tests pass in3.60s, including actual toy
  inner/final case serialization, both environments, both checkpoint windows and
  saved selected-objective replay. Log `nn_pilot_tests3.log`; earlier failed logs
  preserved (caught ndarray JSON serialization before any real pilot).
  Consolidated27test suite passes in7.62s (`pilot_launch_all_tests.log`);
  no frozen producer changed.

Immediately free disk about54GiB before pilots. Library-only forecast no longer
describes remaining needs. Full campaign storage/timing still require measured
NN pilots, output-window sizes and downstream rehearsal.
First real early P_ADJ inner fit stopped after15epochs, selecting7; its fresh
final fit is running. Late S5 fits use about58MiB/105MiB validation-window caches
and roughly14–17seconds/epoch at the first check. No worker errors observed.

## New implementation and next work

New consumers: `v20_library_audit.py`, `v20_feature_audit.py`, `v20_case.py`,
`v20_pilot.py`; tests `test_v20_case.py`.
Cases save original/reference context provenance, selected-inner and final direct
and five-checkpoint ledgers in both reference/conditional environments, including
state-level ledgers for nonlinear seed-mixture event loss. Selected-inner objective
must replay within1e-10absolute/1e-12relative. Fit pending flags are resolved in
new case receipts, never by rewriting fit files. Plateau near-minimum count/span
and memory/disk/timing are recorded.

1. Check real pilot logs/errors and measured memory/runtime; do not repeatedly
   poll while idle. Completed pilot source fingerprints are now frozen.
2. Finish versioned scoring/report/preview and full-run orchestration; matched
   comparisons use chronological calibration, not cold pilot rankings.
3. Implement remaining role/clock descriptor and nested discrepancy analyses,
   registered contrasts/coherence/persistence and independent checks.
4. Run production-shaped downstream rehearsal on the two dates: controls,
   all views, event-mixture losses, fixtures, average opponent, U0/U1 cold states,
   identified synthetic uncertainty fit, covariance and contrast schemas.
5. Measure central/1.2×training-stress/cap runtime and storage forecasts; provide
   **verified** launch/status/live-log commands, then await full-run approval.
   No full production runner command exists yet.

Do not call the whole plan complete after pilots. No new quantitative NN
comparison or three-pillar conclusion exists at this handoff.

## Preservation and retained findings

V19 training/post-analysis/review complete; commit **8e8b325f**.
Retain J_POINT_BOTH; no new point winner/promotion:
same8,345cells/1,013,999poss,44primary quarters.
Half r² reference.162915 vs C_FULL.159127 vs additive_defense.146023.
Checkpoint-half reference.162989 vs C_FULL.161724.
C_FULL improves conditional event loss in all four families/11seasons but not
reference point accuracy, transfer or five-center coherence.
Finite95coverage~93–94%; arbitrary hypothetical latent quality remains unvalidated.

Original v19 production RUNNING marker is historical; **do not restart it**.
Completed continuation `joint_capability_2026_10_03_v19_posttrain1`;
independent review `joint_capability_2026_10_04_v19_review2`.
Keep explicit three-row accounting exceptions (none primary) and unavailable
2014q4 additive-inner warmup diagnostic.

Every native consumer and queued child must use:
`python -u -m experiments.artifact_retention exec --ledger
experiments/cache/completed_resume_retention_2026_09_30 <module> ...`.
Retired optimizer restarts intentionally absent; never rewrite original manifests.

Existing uncommitted v20 files belong to current work. New pilot manifest binds
transitive source hashes; do not edit its producers mid-run. Library/replay/
synthetic producers were already frozen earlier. Fixes need versioned successors
and new output prefixes. Never blindly stage caches; no commit this turn.

[Prior checkpoint](docs/archive/2026-10-06_pre_v20_nn_pilots/SESSION_HANDOFF.md)
preserves previous implementation, storage and launch history.
