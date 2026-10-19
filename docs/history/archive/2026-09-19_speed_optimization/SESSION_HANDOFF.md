# Current handoff — metadata repair verified, ready for user restart, 2026-09-19

## Current decision

Adam authorized the metadata fix, not an agent-initiated full relaunch.
Direct implementation; no agents or commits. **Three seeds retained**:
22 arms × 48 quarters × three seeds = 3,168 production cases, three CPU workers.

New production destination:
`experiments/cache/joint_capability_2026_09_19_v16_hashfix`.

**PASS:** repaired preflight; 88 original plus seven new tests; two bounded
first-origin native fits and saved-state replay. Full production has not been
restarted: 0 started/complete cases in the new destination.

## Repair and evidence

[Repair review](reports/joint_capability_v16_metadata_fix_review.md) and
[frozen repair protocol](reports/joint_capability_v16_metadata_fix_protocol.md).

The original `...v16_local` run passed storage/preflight, constructed six
2015q1 shared contexts, then stopped before an optimizer update. The strict
provenance hasher rejected inherited legacy `team_baseline=NaN` with zero
legacy rows/exposure. That denominator is not used by v16.

New contexts explicitly represent only that empty-history sentinel as None.
Original contexts, parent fits, observations, libraries, producer files and
fingerprints are unchanged. Versioned case/runner copies differ only in the
declared canonicalizer and worker routing; exact source parity is enforced.
The original model/trainer/loss/stopping/reporting/analysis/auditor are reused.

- All 288 dated parent contexts scanned; nine valid empty-history sentinels:
  2015q1 inner/final and 2015q2 inner for all three seeds.
- Six first-origin contexts reproduce the old failure. Generated input tensors,
  predictions, losses and gradients are bit-identical after repair for J_RAW and
  J_ALL_BOTH: 12 real-data comparisons.
- One inner + fresh final epoch for J_RAW/s17 and J_ALL_BOTH/s17 at 2015q1
  completed. All native ledgers pass; max saved-state replay difference
  **0.000018601 pts/100**, within original tolerances.
- Seven new regression tests pass; all 88 existing v16 tests pass.
- Storage at successful repaired preflight: **246.33 GB free / 209.69 GB required**.
- Completion evidence: `experiments/cache/v16_metadata_fix_2026_09_19_v1/complete.json`.
  Durable log: `logs/verification.log` there.
- Production acceptance: `v16_hashfix/preflight/{acceptance,complete}.json`;
  test log `preflight/tests.log`, launch-check log `logs/launch_checks.log`.
- All bounded verification/check processes exited. Nothing left running by the
  agent. No new predictive/coherence/OOD claim or scorer promotion.

## Exact restart commands

Run from the repository root. **Use this new wrapper and destination, not the
old `run_v16_local.sh` or `...v16_local` run.**

```bash
cd /Users/adam/Documents/basketball
mkdir -p experiments/cache/joint_capability_2026_09_19_v16_hashfix/logs
nohup /usr/bin/caffeinate -i bash experiments/run_v16_hashfix.sh run >> experiments/cache/joint_capability_2026_09_19_v16_hashfix/logs/launcher.log 2>&1 < /dev/null &
echo "Launcher PID: $!"
```

The wrapper rechecks immutable evidence, source parity and current storage,
then starts the versioned CPU runner only on PASS. Full training includes all
registered secondary analyses and the independent audit.

```bash
tail -F experiments/cache/joint_capability_2026_09_19_v16_hashfix/logs/launcher.log
bash experiments/run_joint_capability_v16.sh status --run-dir experiments/cache/joint_capability_2026_09_19_v16_hashfix
bash experiments/run_joint_capability_v16.sh report --run-dir experiments/cache/joint_capability_2026_09_19_v16_hashfix --sort rmse --slice all --view half
```

Status and report were exercised (all pending / NO_ROWS, as expected).
The old read-only status/report CLI works with the new destination; training
must use repaired routing. Per-worker epoch logs are under
`queues/<origin>_fits/logs/`. Optional check-only:
`bash experiments/run_v16_hashfix.sh check`.

## Preservation / uncommitted work

The failed `...2026_09_19_v16_local` run and six contexts remain intact.
Earlier `...v16_prod` storage failure and `...v16_prelaunch3` stopped commit
also remain. No commit performed; baseline HEAD was `7206b51`.

Reused completed library: `...2026_09_18_v16_library_full1` (2,032 snapshots).
Reused audited smoke: `...2026_09_18_v16_smoke_dev1` (44 cases).
Reused audited pilots: `...2026_09_19_v16_pilot8` (eight full-stopping cases).
Small new production shared contexts will be recomputed in the new namespace;
no historical-library or input-cache rebuild.

New code: `v16_metadata_fix.py`, `v16_hashfix_case.py`, `v16_hashfix_run.py`,
`v16_hashfix_acceptance.py`, `v16_hashfix_verify.py`, `run_v16_hashfix.sh`
under experiments; `tests/test_v16_metadata_fix.py`. Preserve the extensive
pre-existing dirty worktree and prior GPU/seed diagnostics.

[Pre-repair checkpoint](docs/archive/2026-09-19_metadata_fix/SESSION_HANDOFF.md)
preserves the exact first-launch failure. The [GPU review](reports/joint_capability_v16_local_gpu_benchmark.md)
and [seed review](reports/joint_capability_v15_seed_variance.md) remain applicable.
