# Current handoff — v20 chronological uncertainty integration verified (2026-10-06)

## Authority and current job

Adam authorized the prescribed prelaunch work after the profile library finished.
Direct implementation only; no delegation. All eight NN pilots are complete.
**Full neural campaign remains unlaunched and needs separate approval.** Adam
authorized an appropriate checkpoint commit in the latest task. No historical
cleanup, source rebuild, scraping, database mutation or promotion authorized.
Adam subsequently approved lifecycle cleanup for NEW production cases, preserving
original pilots. Implemented and rehearsed on disposable copies; no originals deleted.

Pilot root: `experiments/cache/v20_nn_pilots_2026_10_06`.
Completed in28.07minutes, all workers exit0; no active job.16inner/final fits,
selected7–23epochs, no cap hits, peak1.97–2.70GiB/worker.42receipts verified;
all selected-inner score replays exactly match. Do not restart completed pilots.
The pilot runner cannot launch the full campaign.

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

No supervisor is needed now. Original pilot outputs and restart files remain
intact. Exact RNG/optimizer/selection-window restart remains available for unfinished
future fits; new production cases will retire temporary files only after verification.

## New storage lifecycle — approved and verified

Read [storage policy/evidence](reports/v20_storage_lifecycle.md) before implementing
the remaining full runner or any forecast consumers. New entry point:
`experiments.v20_case_storage.fit_case`; do not call the frozen pilot producer
directly for production. Manifest must opt into `v20-new-case-retention-1` and
have explicit full-launch authority. New wrapper cases contain `native/` fits.

After verified case completion, durable retirement records permit deletion of
new-case optimizer slots and inner forecast arrays, and replace duplicate outer
containers with an exact shared-array archive. Retain all weights, curves, source
references, metrics and original receipts. No science changes or precision loss.
Use `verify_case`, `load_forecast` and `native_directory` from the new modules;
the old verifier correctly refuses undeclared missing files.

Rehearsal `experiments/cache/v20_storage_rehearsal_2026_10_06` is complete:
all8cases /48logical forecasts byte-exact; original pilots remain unchanged.
Copied payload2.506→.445GiB, **82.22% reduction**,46.47seconds. Only new disposable
copies were purged, recoverable from untouched originals.35tests pass in8.10s,
including interruption recovery, active locks, corruption and unsafe-path refusal.
No active storage job; completed producers are now fingerprinted and must not change.

Adam freed more space and authorized continuing prelaunch work. Filesystem now
shows196.55GiB free, superseding the51GiB storage hold. Calendar-scaled forecast:
856remaining cases45.12GiB, scorecards3.65GiB;25%size stress, three active temporary
cases and13GiBreserve total75.32GiB. Remaining downstream outputs are excluded;
space looks comfortable, but full readiness is not yet established.

## Matched-scoring rehearsal now complete

[Evidence and commands](reports/v20_scoring_rehearsal.md). New derived roots:
`v20_pilot_scored_2026_10_06`, `v20_pilot_scoring_audit_2026_10_06`,
`v20_pilot_native_audit_2026_10_06`, `v20_resources_2026_10_06` under cache.
Scoring25.4s, four reference/conditional panels, all six views/five slices.
Independent3,840sufficient-row checks and50calibration checks pass; error0.
Eight native pilot cases ×two windows ×two environments pass event arithmetic,
including conditional checkpoint-average states; maximum event error4.44e-16.
Read-only case preview matches both panels;16targeted tests pass. All42original
pilot receipts and producer fingerprints remain intact. No active process.

Pilot checkpoint-average-half r² early: P_BASE.102575, P_CONTEXT.119116,
P_BOTH/S_BOTH.120455, additive_defense.048843. Late: P_BASE.104917,
P_CONTEXT.109637, S_BOTH.105562, S_ADJ.102486, additive_defense.072761.
One seed, isolated cold calibration for EVERY NN, not production rankings;
do not select arms from these numbers. Coherence/uncertainty still pending.

Partial remaining training forecast44.38hcentral/52.69h1.2×training-stress,
226.76hcap scenario; excludes downstream time. Three-slot queue simulation,
not an implemented full supervisor. Original profile build is not repeated.
Durable logs in `v20_implementation_2026_10_04/logs/`: scoring, scoring_audit,
native_audit, resources, case_preview, scoring_final_verification2.

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

## Latest completed stage: chronological uncertainty integration

[Evidence](reports/v20_uncertainty_integration.md) and
[frozen rehearsal](reports/v20_uncertainty_integration_protocol.md).
Full254-date empirical R/C library is complete (128.84s,117.68MiB), no GLM/NN
refits. Fixed12-quarter retained-reference rehearsal finished in75.73s; two
isolated V20 pilot dates in18.49s. All jobs finished. No full launch.

Primary reference balanced-date pairs:416pairs/105,110poss,2016q2–2017q4.
U1 nominal95coverage94.351%, joint log score−7.789989; U_ROLE_CLOCK94.351%,
−7.789628. Essentially tied; implementation evidence, not a new scientific win.
Chronological sensitivity coverage92.428%. Uncertainty fit leaves point means
unchanged; arbitrary hypothetical latent-quality coverage is NOT validated.

Independent12-quarter audit passes98identified fits/72penalty subfits; separate
cold-pilot audit confirms allNOT_IDENTIFIED/no gate.49tests pass in7.21s.
All254descriptor snapshots,42original pilot receipts and producer hashes pass.
Source-bound consumers must not be edited after these completed outputs.
Two audit-only invocation/schema failures are preserved and explained in report;
no training, uncertainty outputs, historical artifacts or tolerances changed.

New cache roots: `v20_descriptor_library_2026_10_06`,
`v20_uncertainty_retained_rehearsal_2026_10_06`, `v20_uncertainty_pilot_2026_10_06`,
`v20_uncertainty_retained_audit_2026_10_06_v2`, `v20_uncertainty_cold_audit_2026_10_06`.
Logs in implementation root: `descriptor_library.log`,
`uncertainty_retained_rehearsal.log`, `uncertainty_pilot.log`,
`uncertainty_retained_audit2.log`, `uncertainty_cold_audit.log`,
`uncertainty_checkpoint_tests.log`, `uncertainty_final_verification.log`.

Previous checkpoint commit **1354646a** includes profiles, pilots, storage,
scoring and first transport rehearsals. Latest integration source/tests/docs
are the next authorized checkpoint, never generated cache artifacts.

## Earlier completed prelaunch evidence

Latest [transport rehearsal](reports/v20_transport_rehearsal.md): new strict-date
empirical R/C descriptors and bounded U_ROLE/U_ROLE_CLOCK variance primitives.
Two-date history has797/1,068players;12arm/date queries, original/compact actor
counts equal. Full254-date calendar is now complete, as recorded above.

20replicate signal/constant synthetic worlds (120final fits) completed:
signal U_ROLE_CLOCK NLL6.401705vsU1 6.423660 (delta−.021955,MCSE.002795),
variance RMSE3.0527vs8.4829. Constant case no clear gain, worse variance recovery.
Signal95coverage94.325%; slopes2.16/9.30vs true3/12. No retuning or NBA claim.
Real cold rehearsal26/14models,1,508/728model-pair rows, allNOT_IDENTIFIED;
points remain available. No late P_ADJ pilot/residual history invented.
Independent moments/histograms20players/date and120matrix-form NLLs pass.
46V20tests pass in7.06s with all thread env settings1. All jobs finished.

New cache roots: `v20_descriptor_rehearsal_2026_10_06`,
`v20_transport_synthetic_2026_10_06`, `v20_transport_cold_2026_10_06`,
`v20_transport_audit_2026_10_06_v2`. Timings7.20/1.53/13.84/2.47seconds,~77MiB.
Logs in implementation root: descriptors, transport_synthetic, transport_cold,
transport_audit2, v20_checkpoint_tests_single_thread. First audit float32 pandas
accumulation corrected only in independent consumer, new prefix, same tolerance.
Full tests initially stalled in OpenBLAS thread initialization; own process
stopped and rerun with OMP/OPENBLAS/MKL/VECLIB/NUMEXPR/BLIS thread env=1.
Other user project untouched. Frozen rehearsal protocol:
`reports/v20_transport_rehearsal_protocol.md`.

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

All8NN pilots are complete; total2.506GiB original artifacts preserved. Largest
validation ring137.18MiB. Late S5 fits selected9/13epochs; no errors. New-case
retention size measurements above supersede the original unbounded extrapolation.

## New implementation and next work

New consumers: `v20_library_audit.py`, `v20_feature_audit.py`, `v20_case.py`,
`v20_pilot.py`; tests `test_v20_case.py`.
Cases save original/reference context provenance, selected-inner and final direct
and five-checkpoint ledgers in both reference/conditional environments, including
state-level ledgers for nonlinear seed-mixture event loss. Selected-inner objective
must replay within1e-10absolute/1e-12relative. Fit pending flags are resolved in
new case receipts, never by rewriting fit files. Plateau near-minimum count/span
and memory/disk/timing are recorded.

1. Pilot completion and new storage rehearsal verified. Preserve their frozen
   fingerprints. Use the new production case entry point/reader/verifier contract.
2. Core scoring/report/preview now implemented and rehearsed. Add remaining
   descriptive controls and full-run orchestration; matched production comparisons
   use chronological calibration, not cold pilot rankings. Existing consumer
   modules are now fingerprinted: extend with new versions/output prefixes.
3. Full strict-date calendar and prior-only NBA U0/U1/transport integration now
   complete and rehearsed with chronological sensitivity. Next: fixture
   uncertainty/as-of risk thresholds, registered contrasts/coherence/persistence.
4. Next implement the fixture/average-opponent adapter with each arm's own saved
   adjusted normalizer/library and complete checkpoint-ledger mixture. The old
   v19 adapter's common library/context and direct-only forecasts are insufficient.
   Rehearse controls, all views, event-mixture losses, fixtures, average opponent,
   covariance and contrast schemas. Cold/identified uncertainty checks are done.
5. Measure central/1.2×training-stress/cap runtime and storage forecasts; provide
   **verified** launch/status/live-log commands, then await full-run approval.
   No full production runner command exists yet.

Do not call the whole plan complete after pilots. Quantitative pilot comparisons
now exist, but no full-campaign or three-pillar conclusion exists at this handoff.

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
and new output prefixes. Never blindly stage caches. A checkpoint commit is
authorized: reviewed V20 source/tests/docs only, not generated artifacts.

[Prior checkpoint](docs/archive/2026-10-06_pre_v20_transport/SESSION_HANDOFF.md)
preserves previous implementation, storage and launch history.
