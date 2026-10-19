# Current handoff — local GPU benchmark complete, 2026-09-19

## Current decision

Retain the frozen three-worker CPU v16 campaign. Adam requested and authorized
a bounded local-GPU benchmark, not full production training. Implement directly;
no agents. No commit, production launch, model promotion, database work or
deletion occurred.

[Local GPU report](reports/joint_capability_v16_local_gpu_benchmark.md) contains
the exact methodology, measurements, limitations, logs and reproduction commands.
On the M1 Pro, warmed simple-arm training was only 1.07–1.18× faster than one
CPU worker. Three CPU workers beat projected sequential GPU throughput by
2.10–2.35× on the measured simple-arm workloads. All four combined-arm MPS
attempts failed with nonfinite gradients; an explicit-attention diagnostic also
failed. Successful short FP32 trajectories agreed within 0.00005735 pts/100.
This is not a new predictive/coherence/OOD experiment or production precision
acceptance. Original frozen producers and artifacts are unchanged.

## v16 readiness

- All 2,032 historical profile snapshots complete:
  `experiments/cache/joint_capability_2026_09_18_v16_library_full1`.
- All 44 one-epoch smoke cases passed:
  `experiments/cache/joint_capability_2026_09_18_v16_smoke_dev1`.
- All eight full-stopping pilots completed and independently audited:
  `experiments/cache/joint_capability_2026_09_19_v16_pilot8`.
- 88 existing v16 tests passed; three new isolated benchmark tests passed.
- Full campaign remains 22 arms × 48 origins × three seeds = 3,168 cases,
  each with inner and reset-final training. Production is **not launched**.
- Prelaunch **failed the conservative disk-space check**, not model acceptance.
  The guarded commit stopped before staging/committing. Baseline HEAD remains
  `7206b51`; read actual receipts before any future Git action.
- Current production destination:
  `experiments/cache/joint_capability_2026_09_19_v16_prod`.
  Its manifest/resources exist; that is not acceptance or launched training.
- Saved supervisor receipts:
  `experiments/cache/joint_capability_2026_09_19_v16_prelaunch3/status.json`,
  `commit_status.json`, `commit_result.json`.

The saved resource projection is 198,954,348,640 bytes new outputs plus 10 GiB
reserve (approximately 210 GB decimal / 195.29 GiB total required). The latest
read-only filesystem check showed approximately 197 GB free; Adam reports
Settings shows 150 GB and is freeing storage. Do not declare space resolved
until rechecked. No data were removed. An external output volume remains an
alternative, requiring verified path/manifest handling.

The rough prior pilot-average CPU projection was approximately 17 days with a
50% overhead cushion, not an all-arm ETA. The saved maximum-case stress
projection is 43 days, not the expected duration. The short GPU benchmark does
not replace full-stopping pilot estimates.

## Completed diagnostic artifacts

- `experiments/cache/v16_mps_benchmark_2026_09_19_v1`: 36 attempts, 32
  successful, four combined-arm MPS failures. Durable `benchmark.log`.
- `experiments/cache/v16_mps_failure_probe_2026_09_19_v1`: backward anomaly
  localization; explicit attention does not solve it.
- `experiments/cache/v16_cpu_parallel_benchmark_2026_09_19_v1`: six native
  CPU jobs, two synchronized groups of three, all complete.
- `experiments/cache/v16_device_benchmark_2026_09_19_logs`: tests,
  parallel supervisor and anomaly logs.

No diagnostic processes remain active. New scripts:
`experiments/v16_mps_benchmark.py`, `v16_mps_failure_probe.py`,
`v16_cpu_parallel_benchmark.py`, and
`tests/test_v16_mps_benchmark.py`. They do not match the frozen scientific
producer glob or patch original modules. Generated FP32 copies live only under
their new diagnostic prefixes. Benchmark tests use unittest; pytest is not
installed in the project environment.

## Next action

Recheck storage when Adam is ready, then complete acceptance using the
[eight-pilot operational amendment](reports/joint_capability_v16_pilot_amendment.md).
Do not rerun completed library/smoke/pilots or overwrite failed/completed
receipts. The previous commit continuation is terminal; any renewed guarded
continuation must review the enlarged dirty tree and preserve the failed record.
The full CPU launch still requires explicit authorization. Ensure the production
log directory exists before shell append redirection in any launch command.

The previous checkpoint is preserved in
[the GPU-benchmark archive](docs/archive/2026-09-19_local_gpu/SESSION_HANDOFF.md).
[State](JOINT_CAPABILITY_STATE.md), [roadmap](MODEL_RESEARCH_ROADMAP.md), and
the frozen [v16 plan](JOINT_CAPABILITY_V16_PLAN.md) retain their assigned roles.
