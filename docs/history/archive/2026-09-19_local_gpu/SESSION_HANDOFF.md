# Current handoff — v16 eight-pilot continuation, 2026-09-19

Adam approved reducing the separate full-stopping acceptance suite from 48 to
eight cases. Implement directly; no agents. **Do not launch full production
training without his separate request.** The 22-arm / 3,168-case experiment,
scientific producers and all three product standards are unchanged.

## First action on resumption: read live state

Supervisor: `experiments/cache/joint_capability_2026_09_19_v16_prelaunch3`.

Read `status.json`, `commit_status.json`, and (when present)
`commit_result.json` / `READY_HANDOFF.md` there. Only actual acceptance and
commit receipts establish readiness. The launcher PID was 93347; this is a
launch receipt, not a future liveness guarantee. No automatic chat resumption
is configured; the scripts continue independently.

The previous `2026_09_18_v16_prelaunch2` supervisors were intentionally stopped
while smoke testing ran. Its stale SMOKE / STOPPED_FOR_REVIEW status is
superseded by the new continuation, not a scientific failure. No old outputs
were deleted or relabelled. Historical handoff:
[before amendment](docs/archive/2026-09-19_v16_pilot_amendment/SESSION_HANDOFF.md).

## Completed and preserved

- All **2,032 historical profile snapshots** complete, with all eight chains
  successful. Library:
  `experiments/cache/joint_capability_2026_09_18_v16_library_full1`.
- All **44 one-epoch neural smoke cases** passed their independent audit in
  about 21 minutes. Maximum 16-row native replay difference: 1.81e-5 pts/100.
  `experiments/cache/joint_capability_2026_09_18_v16_smoke_dev1`.
- **88 tests pass**, including reduced-schedule, unchanged-science/reuse and
  explicit eight-pilot commit-authorization checks.
  `experiments/cache/joint_capability_2026_09_19_v16_pilot_amendment_dev1/logs/tests_02.log`.
- Real manifest parity confirms all **148 original scientific source files**
  and historical-library producers unchanged. Its `parity.json` records
  source/receipt proof and exact eight/3,168-case schedules.
- Previous implementation evidence remains in
  [prelaunch checkpoint](reports/joint_capability_v16_prelaunch_checkpoint.md)
  and [implementation conventions](reports/joint_capability_v16_implementation_conventions.md).
  These are not full-campaign accuracy/coherence/uncertainty conclusions.

## Operational amendment

[Eight-pilot amendment](reports/joint_capability_v16_pilot_amendment.md)
supersedes only the old 48-pilot requirement. Fixed schedule:

- 2016q1: J_RAW/s17, J_BOTH/s17, J_ALL_BOTH/s17, J_BOTH/s23.
- 2026q4: J_RAW/s17, J_BOTH/s17, J_ALL_BOTH/s17, J_POINT_BOTH/s17.

New adapter `experiments/v16_pilot_amendment.py` derives immutable manifests
from the audited smoke configuration, adds its explicit operational provenance,
then calls the **unchanged** original trainers/reporters/auditor. No runtime
monkey-patching or copy/relabel of completed fits. Pilots remain isolated fits,
not automatically reusable production checkpoints.

Original frozen plan/convention/producer files are unchanged. New pilot:
`experiments/cache/joint_capability_2026_09_19_v16_pilot8`.
New production destination:
`experiments/cache/joint_capability_2026_09_19_v16_prod`.
The production manifest may exist; that does not mean training was launched.

After all eight pilots/audit: complete tests, unchanged-science parity, RAM/disk
checks and conservative maximum-observed-case resource projections. Unmeasured
arms and projection limitations are explicit. A failed check stops for review;
no model elimination, tolerance relaxation or cleanup is authorized.

The guarded commit follows only after PASS and unchanged reviewed files,
HEAD and index. Baseline HEAD: `7206b51`. Read `commit_result.json` before
attempting another commit. Generated caches are excluded. Full training is not
launched by either continuation.

## Read-only monitoring

From the repository root:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_pilot_amendment status
tail -F experiments/cache/joint_capability_2026_09_19_v16_prelaunch3/logs/pilot.log
bash experiments/run_joint_capability_v16.sh status --run-dir experiments/cache/joint_capability_2026_09_19_v16_pilot8
```

Each worker's verbose epoch log is under the pilot's
`queues/<origin>_fits/logs/`. The supervisor's launch/progress log is
`v16_prelaunch3/logs/launcher.log`; the guarded commit has `logs/commit.log`.

Use the new adapter for amended acceptance; the old `pilot` and `preflight`
CLI commands intentionally still describe the original 48-case protocol.
The original `run`, `status` and `report` commands work with the new production
manifest, but full `run` requires actual amended preflight PASS and Adam's
authorization. Exact launch commands will be in `READY_HANDOFF.md`.

## Next action

Check live pilot/audit/preflight/commit state. If ready, inspect the actual
receipts and give Adam the full launch commands. If failed, diagnose the exact
failure and preserve all artifacts. Do not edit frozen scientific/adapter
sources during active pilots. No scraping, database work, scorer promotion,
deployment or full-campaign launch was performed for this amendment.
