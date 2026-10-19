# Current handoff — local CPU command prepared, storage still short, 2026-09-19

## Current decision

Retain the frozen three-worker CPU v16 campaign. Adam requested preparation of
the local launch command for him to run; do not launch it on his behalf. Implement directly;
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
- New local production destination:
  `experiments/cache/joint_capability_2026_09_19_v16_local`.
  Its manifest is prepared; that is not acceptance or launched training.
  The old `v16_prod` destination and its failed preflight remain unchanged.
- Saved supervisor receipts:
  `experiments/cache/joint_capability_2026_09_19_v16_prelaunch3/status.json`,
  `commit_status.json`, `commit_result.json`.

The saved resource projection is 198,954,348,640 bytes new outputs plus 10 GiB
reserve (approximately 210 GB decimal / 195.29 GiB total required). The latest
read-only filesystem check showed 196.89 GB free, **12.81 GB short**; Adam reports
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

## Prepared command and next action

Latest read-only research question: completed a
[v15 seed-sensitivity analysis](reports/joint_capability_v15_seed_variance.md)
in `experiments/cache/v15_seed_variance_2026_09_19_v1`. Three-seed averaging
adds only 0.00228 RMSE over an average single seed for MAIN_RB half, but paired
MAIN_RB-minus-MAIN quarterly contrasts have seed SD 0.02584 versus quarter SD
0.02781. Seeds matter for near-tied ablations even though raw quarter difficulty
dominates. A staged single-seed screen is only a possible new protocol; **the
current launch remains 22 arms / three seeds / 3,168 cases**. No fits launched
and no seed-count change made. 528 original prediction files were receipt-
verified; 144 individual-seed score rows match the prior independent review.

New operational wrapper `experiments/run_v16_local.sh` /
`experiments/v16_local_launch.py` reuses the audited smoke and pilots, checks
frozen sources and available storage, then runs the unchanged eight-pilot
preflight against a new production destination. `check` never trains; `run`
hands off to the original production CLI only after PASS. Failed check attempts
have their own timestamped receipts/logs; the old failed preflight is untouched.
No scraping, input rebuild, pilot refits, or commits. Four launcher tests pass;
the real `check` exits safely on the measured 12.81 GB storage shortfall. Status
and report commands were exercised against the prepared destination.

Adam should free at least 13 GB more (preferably 20–30 GB extra headroom), then
run the following from the repo root. It exits rather than training if storage
or acceptance still fails. The command has **not** been launched here:

```bash
mkdir -p experiments/cache/joint_capability_2026_09_19_v16_local/logs
nohup /usr/bin/caffeinate -i bash experiments/run_v16_local.sh run >> experiments/cache/joint_capability_2026_09_19_v16_local/logs/launcher.log 2>&1 < /dev/null &
echo "Launcher PID: $!"
```

Optional acceptance-only check: `bash experiments/run_v16_local.sh check`.
Logs: `tail -F experiments/cache/joint_capability_2026_09_19_v16_local/logs/launcher.log`.
Full training writes its own `logs/run.log`; per-worker epoch logs are under
`queues/<origin>_fits/logs/`. Overall status:

```bash
bash experiments/run_joint_capability_v16.sh status --run-dir experiments/cache/joint_capability_2026_09_19_v16_local
bash experiments/run_joint_capability_v16.sh report --run-dir experiments/cache/joint_capability_2026_09_19_v16_local --sort rmse --slice all --view half
```

Do not mistake command readiness for preflight PASS. The previous commit
continuation is terminal; any renewed commit requires authority and review of
the enlarged dirty tree. The pre-launch checkpoint is preserved in
[the local-launch archive](docs/archive/2026-09-19_local_launch/SESSION_HANDOFF.md).
[State](JOINT_CAPABILITY_STATE.md), [roadmap](MODEL_RESEARCH_ROADMAP.md), and
the frozen [v16 plan](JOINT_CAPABILITY_V16_PLAN.md) retain their assigned roles.
