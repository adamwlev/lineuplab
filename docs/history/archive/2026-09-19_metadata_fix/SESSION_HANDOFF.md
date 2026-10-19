# Current handoff — first CPU launch stopped on metadata hash, 2026-09-19

## Current state

Adam freed storage, launched the prepared local command, and reported a failure.
Direct implementation only; no agents. Adam explicitly retained **three seeds**
after the [v15 seed review](reports/joint_capability_v15_seed_variance.md).
Full schedule remains 22 arms × 48 origins × three seeds = 3,168 cases.

Production destination:
`experiments/cache/joint_capability_2026_09_19_v16_local`.

- Storage passed on the second launch attempt: 247.11 GB free versus 209.69 GB
  required. Latest filesystem check approximately 249 GB free.
- Amended preflight **PASS**, including the 44 smoke cases, eight completed
  full-stopping pilots and 88 tests.
- Production PID2107 started, completed all six 2015q1 shared contexts, then
  stopped when the first three J_RAW workers failed (seeds17/23/41).
- Saved queue has no active workers. Zero cases complete, three started,
  3,165 pending. No training journal or optimizer update was reached.
- No agent-initiated restart, code fix, commit, scraping, database work, input
  rebuild, scorer promotion or deployment occurred in the diagnosis turn.

## Verified cause

`content_hash(shared)` in `experiments/joint_capability_v16_fit.py` rejects
the scalar `shared.parent_shared.team_baseline = NaN` through strict JSON
serialization before training.

All six 2015q1 inner/final contexts contain this inherited metadata sentinel:
`team_rows=0`, `team_exposure=0`. The old
`joint_capability_v12_fit.team_baseline` explicitly returns `(nan, 0., 0)`
when no old additive-offset rows exist. v16 does not use that denominator;
its own point references are finite (approximately 1,799–1,800). A recursive
scan of all six shared/reference dictionaries found no other nonfinite field.

This is provenance serialization, not a nonfinite training gradient. The
2016q1/2026q4 smoke/pilot schedule missed the first warmup-origin edge case.

Evidence under the production destination:

- `logs/launcher.log` and `logs/run.log`;
- `queues/2015q1_fits/logs/2015q1_J_RAW_s17.log` (same error for s23/s41);
- `contexts/2015q1/s{17,23,41}/{inner,final}/context.pt`;
- `preflight/acceptance.json` and `queues/2015q1_fits/status.json`.

## Next action

Diagnosis is complete; **no fix has been made**. The current launch command
will fail again. A targeted repair should encode legitimate missing metadata
explicitly while continuing to reject nonfinite model inputs/losses, and add
first-origin regression coverage. Preserve the original frozen producers and
completed receipts through an explicit revised-source/reuse strategy; do not
silently edit fingerprints or sanitize source caches.

Do not repeat the completed 2,032-snapshot library or eight-pilot campaign.
The failed production prefix and six shared contexts must remain preserved.
Verify the repaired first-origin path before giving a restart command; do not
restart on Adam's behalf without instruction.

## Retained context and uncommitted work

- Complete library: `experiments/cache/joint_capability_2026_09_18_v16_library_full1`.
- Audited smoke: `experiments/cache/joint_capability_2026_09_18_v16_smoke_dev1`.
- Audited pilots: `experiments/cache/joint_capability_2026_09_19_v16_pilot8`.
- Earlier storage failure: `...2026_09_19_v16_prod` and `...v16_prelaunch3`,
  preserved. Its guarded commit stopped; baseline HEAD was `7206b51`.
- New local wrapper: `experiments/run_v16_local.sh` /
  `experiments/v16_local_launch.py`; four launcher tests passed.
- [Local GPU benchmark](reports/joint_capability_v16_local_gpu_benchmark.md):
  completed, CPU retained; MPS combined-arm gradients failed. No GPU migration.
- [Seed sensitivity](reports/joint_capability_v15_seed_variance.md): completed
  derived analysis only; Adam chose to keep three seeds.
- Large pre-existing uncommitted v16 implementation plus diagnostic scripts,
  tests and reports remain user-owned. No commit authority in the diagnosis.

[Pre-failure checkpoint](docs/archive/2026-09-19_first_launch_failure/SESSION_HANDOFF.md)
preserves the original command and earlier receipts. Current status must be
read from the local production prefix, not the old storage-failed supervisor.
