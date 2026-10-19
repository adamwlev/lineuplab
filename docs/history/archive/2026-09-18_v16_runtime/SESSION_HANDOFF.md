# Current handoff — v16 runtime/library implementation, 2026-09-18

## Scope and current result

Adam asked to continue v16 and explore three simultaneous training processes.
Codex implemented directly; no agents. The [22-arm plan](JOINT_CAPABILITY_V16_PLAN.md)
still governs the science. Three CPU workers × one thread is now the operational
target, subject to the remaining adjusted-feature memory/pilot acceptance.

**Full-prefix timing: 324 seconds serial versus 142 seconds with three workers,
2.28× throughput, exactly identical parameters.** These are six fixed one-epoch
timing jobs, not selected NN fits or outer accuracy results.

**The full campaign is not launched or launch-ready.** No database access,
scraping, old-cache rebuild, promotion or deployment occurred. Adam subsequently
authorized a checkpoint commit of the implementation, tests and documentation.
The authoritative detailed progress report is the
[runtime/library checkpoint](reports/joint_capability_v16_runtime_library_checkpoint.md).
Earlier foundation evidence remains in the
[initial checkpoint](reports/joint_capability_v16_implementation_notes.md).
The exact preceding handoff/report are preserved under
`docs/archive/2026-09-18_v16_foundation/`.

## Completed since the preceding checkpoint

- Monthly/exact-origin library builder, annual prior-quarter penalty selection,
  raw reference channels, opportunity/Kish support, cold/stale/shared-unknown
  feature lookup and prefix-only normalization.
- Immutable numeric memory-mapped training layout, real inner/final data bridge,
  shared references, deterministic game-complete training, fresh final fitting,
  bounded checkpoint retention and exact interrupted/resumed optimization.
- Independent native case stage and a bounded CPU queue with per-job logs,
  locking and fail-stop behavior. Completed shared contexts support simultaneous
  read-only reuse; shared preparation must precede dependent fit jobs.
- ADJUSTED_CHANNEL event accounting and U0/U1/U2 statistical primitives.
  Real uncertainty pairs/noise forecasts and the final reporting lifecycle remain.
- Short-batch 1/2/3-worker benchmark and full-prefix 1/3-worker benchmark.
  The latter covers 346,149 training groups / 1,337,350 possessions. Three times
  the maximum worker RSS is 6.48 GiB; that is a conservative worker-only bound,
  not full system/pilot memory acceptance.
- Separate exact-Hessian factor/draw acceleration: on late offensive snapshots,
  all 32 count draws 324.6→11.82 s, conversion 104.3→19.49 s, recovery
  68.8→5.69 s. Maximum difference from saved reference draws 1.63e-8.
  The large location Hessian still uses full matrix-free CG.

## Important partial failure and separate correction

`v16_library_dev1` is a **two-cutoff diagnostic**, not complete historical
features. Four offensive chains and defensive location completed. Late defensive
counts failed:
L-BFGS used all 500 iterations, leaving projected gradient .00664 rather than
<1e-5. The queue stopped launching more chains; defensive conversion/recovery
are pending, not complete. The already-started defensive-location job subsequently
finished successfully, and the queue has exited with its recorded failure.

`v16_solver_dev1` independently checks the repair on that exact failed case:
switch earlier to Newton refinement, keep the identical objective and penalty,
both convergence requirements, and **total cap 500**. It passes in 282 iterations,
projected gradient 8.33e-11. The original failed snapshot is untouched.

The old audit's fingerprinted producer set is:
`v16_library`, `profiles`, `inputs`, `curvature`, `protocol`, `runtime`,
`storage`. The new `v16_solver.py` and `v16_draws.py` are separately verified,
**not yet wired into that producer**. The old job has now exited. Integrate under
a new library prefix; do not try to resume dev1 with changed source hashes.

The raw-vs-adjusted audit is mixed, not a predictive NN win. Offensive counts
improve slightly; location/conversion/recovery are worse than the matched
monthly own-only EB reference at both dates. Preserve all registered controls
and arms. See the report's exact numbers and comparator limitations.

## Processes and artifacts

All artifact suffixes below begin
`experiments/cache/joint_capability_2026_09_18_`.

| Suffix | Status / role |
| --- | --- |
| `v16_library_dev1` | Ended partial: five chains complete, defensive counts failed, two chains unstarted; no active jobs |
| `v16_training_inputs_dev2` | Completed accepted numeric layout; dev1 preserved/incomplete after text-schema export error |
| `v16_bridge_dev1` | Completed real prefix normalizer/label/parent replay checks |
| `v16_perf_packet_dev1`, `v16_parallel_dev1` | Completed fixed-step throughput/parity checks |
| `v16_fullprefix_packet_dev1`, `v16_fullprefix_parallel_dev1` | Completed five-year one-epoch throughput/parity checks |
| `v16_direct_curvature_dev1`, `v16_direct_conversion_dev1`, `v16_direct_recovery_dev1` | Completed exact-factor four-RHS checks |
| `v16_fast_draws_dev1` | All three applicable families' 32-draw parity/timing checks complete |
| `v16_solver_dev1` | Completed repaired failed-case fit, original artifacts preserved |
| `v16_checkpoint_dev2` | Integrity audit at checkpoint; not scientific launch acceptance |

**No bounded or production training jobs remain active.** The old library queue
finished in 3,720.76 seconds (62.0 minutes). Its five completed chains include
defensive location; defensive counts failed and conversion/recovery were never
started. The queue's final error is the expected fail-stop result of that earlier
failure, **not a new NN training failure**. Former driver PID 75076 and wrapper
PID 75397 are historical, not status indicators. No restart process was launched.

Verified read-only status and logs:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.joint_capability_v16_checkpoint_audit status

tail -n 50 experiments/cache/joint_capability_2026_09_18_v16_library_dev1/logs/chains.log
tail -n 35 experiments/cache/joint_capability_2026_09_18_v16_library_dev1/queue/logs/defense_location.log
```

Status prints recorded queue state/mtime, not a process-liveness guarantee.
Timing results are in `v16_fullprefix_parallel_dev1/audit.json`; no need to
rerun a completed benchmark to read it. Earlier accepted artifacts remain
phase_dev2, controls_dev1, integration_dev1, replay_dev2 and fixed-lambda
profile_dev2. Never train from rejected phase_dev1.

## Verification and tree

**64 tests pass**:
`v16_development/logs/foundation_tests_11.log` (with the dated prefix above).
The new checkpoint audit verifies **256 original v13–v15 source hashes** plus
**2,287 artifact-hash checks / 549 receipts** at audit time.
`git diff --check` passed. The authorized checkpoint commit includes source,
tests and documentation only; generated caches remain untracked and untouched.
All 64 tests and 256 original source hashes were rechecked before committing in
`commit_tests_01.log` and `commit_frozen_sources_01.log` under the same log folder.
Completed earlier reports/protocols and original research inputs remain intact.

## Precise restart order

1. Read the completed library queue summary: five successful chains, one failed,
   two unstarted. Do not interpret the two-cutoff diagnostic as complete history.
2. Integrate `v16_solver.fit` and `v16_draws.joint_draws` into the **new-prefix**
   library; fingerprint those dependencies. Preserve the original implementation
   and diagnostic receipts. Audit the missing defensive families and revised
   numerical path. For the eventual three-worker full-library queue, start
   both expensive location chains early; all dates/penalties remain fixed.
3. Prepare full historical coverage: 254 snapshots × eight bank/family chains
   plus annual tuning. Scope and estimate this long preparation explicitly;
   it has not been launched. Do not assign final-prefix coefficients backward
   to historical rows or replace missing months with the two audited dates.
4. Finish frozen fixed fixtures and cohort/uncertainty descriptors, real U1/U2
   pairs and prior-only noise forecasts, chronological common NN calibration,
   scorecards/statistics and independent end-to-end audit/lifecycle.
   Out-of-order fit completion cannot omit prior calibration windows.
5. Freeze complete scientific manifest before meaningful pilot forecasts.
   Complete all-arm smoke and **all 48 full-stopping operational pilots**.
   Check adjusted-library working-set memory, long-fit/inference time and disk;
   retain three workers only if the complete pipeline passes.
6. Provide verified full background-launch/log/status/leaderboard commands
   only after preflight. **Do not launch the 3,168-case campaign without approval.**

No three-pillar or scorer-promotion decision changes. Forward prediction,
basketball coherence and honest OOD uncertainty remain co-equal.
