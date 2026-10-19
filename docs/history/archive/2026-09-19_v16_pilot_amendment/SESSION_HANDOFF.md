# Current handoff — v16 automated prelaunch, 2026-09-18

Adam requested launch readiness followed by another commit. Direct implementation;
no agents. The 22-arm design remains unchanged. **Do not launch full training
without Adam's separate request.** Historical artifacts and feedback are preserved.

## First action on resumption: read live state

Preparation and its bounded continuation can advance after this checkpoint.
Do not infer the current stage from an old PID or this document's timestamp.

Supervisor:
`experiments/cache/joint_capability_2026_09_18_v16_prelaunch2`

Read these files there, in order:

1. `status.json`: feature wait, smoke, pilot, preflight, ready, or failed.
2. `commit_status.json` / `commit_result.json`, when present: the guarded
   commit's actual result and SHA. **Check this before making another commit.**
3. `READY_HANDOFF.md`, created only after passing acceptance and successful
   commit: measured resources and verified full-run/live-log/status commands.
4. `logs/prelaunch.log`, stage logs, and `logs/commit.log`.

At the last interactive check the historical library was still building;
**no NN pilot or full-campaign accuracy result existed yet**. Baseline commit
was `7206b51`. Do not label the full run ready unless its actual preflight
receipt says PASS. The continuation never launches the full campaign.

## What advances automatically

`joint_capability_v16_prelaunch.py` waits for all eight historical chains,
then runs 44 one-epoch smoke cases, 48 full-stopping pilots, both independent
audits, production-manifest preparation and resource/test preflight. Three CPU
workers × one thread, chronological reporting barrier, no pilot selection.

A separately guarded `v16_finish_prelaunch.py` implements Adam's requested
commit after acceptance. Its explicit `commit_contract.json` binds reviewed
paths/hashes, baseline HEAD and an initially empty index. It stops if acceptance
fails, source/HEAD/index changes, or unexpected tracked edits appear. It cannot
adopt another session's work or stage caches. It writes a new derived handoff,
not predictions or canonical source. No cleanup/reset or automatic retry.

**Source and conventions are now frozen.** Do not edit NN/preparation producers
while this continuation is active. If a real bug needs a fix, first stop only
the affected continuation/owned workers, preserve their outputs, and use an
appropriate new prefix with explicit reuse/parity evidence. Do not restart the
historical preparation while its workers are alive.

## Paths and launch identities

Common prefix below: `experiments/cache/joint_capability_2026_09_18_`.

- `v16_library_full1`: 254 snapshots × eight channels, annual selection and
  joint covariance draws. Launcher 76657 / queue 76660; initial workers
  76661/76662/76664. Read `queue/status.json`, `logs/preparation.log` and
  `queue/logs/*.log`. These PIDs are receipts, not liveness guarantees.
- `v16_prelaunch2`: supervisor launched as PID 79062; read actual state.
  `v16_prelaunch1` was intentionally stopped while waiting, before any NN fit,
  to remove an unnecessary timing wrapper so termination reaches trainers.
- `v16_smoke_dev1`, `v16_pilot_dev1`: scheduled acceptance runs; inspect
  actual receipts rather than assuming they already exist or are complete.
- `v16_prod`: prepared only after pilots; 3,168-case campaign remains unstarted
  by this workflow.
- `v16_training_inputs_dev2`, `v16_controls_dev1`, `v16_phase_dev2`:
  accepted immutable inputs/control replays. Do not rebuild them.

## Completed implementation and checks

See [prelaunch checkpoint](reports/joint_capability_v16_prelaunch_checkpoint.md)
and [implementation conventions](reports/joint_capability_v16_implementation_conventions.md).

- All 22 NN designs and lifecycle; explicit common calibration and half blends;
  native/late-checkpoint sensitivity and all registered populations.
- Fixed offense/defense fixtures, per-player action/phase/rebound ledger,
  shared-draw sensitivity, prior-average integration and separate scorecard.
- U0/U1/U2 with prior-only predictive noise, support/transfer/split diagnostics,
  disclosed hypothetical extrapolation and uncertainty-assumption simulations.
- Factual channel/profile diagnostics, fixed-family season/Holm comparisons,
  three-pillar matrix, derived handoff and independent numerical auditor.
- 81 tests passed in `v16_development/logs/foundation_tests_24.log`, including
  interrupted/resumed uncertainty analysis and commit guards.
- Real inference bridge: exact inputs, additive/A+D agreement within 1.42e-14,
  NN agreement within 1.29e-5 points/100 at early/late cutoffs. Artifact:
  `v16_scoring_bridge_final`; explicitly diagnostic, not a training fit.
- All original v13–v15 producer hashes checked unchanged (102 unique files).
  Active historical-library producer hashes checked unchanged.

Earlier numerical/runtime evidence is in
[the runtime checkpoint](reports/joint_capability_v16_runtime_library_checkpoint.md).
The prior committed handoff is preserved in
`docs/archive/2026-09-18_v16_runtime/SESSION_HANDOFF.md`.

## Next decision

If the continuation passes, read actual pilot audits/resources and its committed
SHA/derived handoff, then give Adam the verified command. Pilots establish
operation, not which architecture wins. Production requires his launch.

If it stops, inspect the exact failure and preserve completed work. An unchanged
source tree is required for exact resume. No scraping, database access/mutation,
old-cache rebuild, scorer promotion or deployment was performed. Generated
cache artifacts remain local/untracked and are not part of the requested commit.
