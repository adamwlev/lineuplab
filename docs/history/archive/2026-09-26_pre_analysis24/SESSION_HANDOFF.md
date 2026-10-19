# Current handoff — v16 post-run analysis stopped by request, 2026-09-26

## Decision and current checkpoint

Adam requested stopping the analysis after the unchanged serial implementation
was estimated at roughly nine additional days (planning range 7–12 days).
SIGTERM sent to analysis PID 96909 and waiting supplement PID 97047;
both processes and their caffeinate helpers (96910, 97048) verified exited.
**Do not restart or optimize until discussion with Adam.** No source producers,
cached outputs or completed receipts were changed by the stop.

Saved checkpoint: 48/48 corrected scored origins; point, event, profile and
factual-channel analysis receipts; five average-opponent origins; 14 completed
fixture cases. Interrupted case: 2016q2/F_DEF/s41 (no completion receipt).
Full independent audit, remaining diagnostics and supplements remain pending.
The supplement `followthrough_status.json` still says WAITING; it is a stale
last-written record, not a live process. The sequence below is pending work,
not an active or automatically restarting queue.

Adam authorized all next steps: repair calibration/event reporting, regenerate
the leaderboard, finish registered analyses and independent audit, then run
the bounded reliability and multi-model ensemble supplements. Implement directly;
no delegation, NN refits, original-artifact edits, promotion, deployment or commit.

- Original: `experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`.
  All 3,168 native cases and 6,336 inner/final checkpoint directories verified.
  Its final event-report crash and contaminated calibration outputs remain intact.
- Corrected: `experiments/cache/joint_capability_2026_09_26_v16_repaired`.
  Preparation verified all 3,312 native/derived cases and 288 contexts. Only
  receipt-bound native artifacts/contexts are linked; scored/analysis/audit
  outputs belong to the new directory.
- Repair/registered-analysis background PID **96909**: stopped and verified absent.
- Supplement follow-through PID **97047**: stopped and verified absent.
  Output: `experiments/cache/joint_capability_2026_09_26_v16_supplements`.
- First shell background attempt (PID96900) did not run because background
  niceness was sandbox-blocked. It was confirmed absent before the successful
  detached launch. No duplicate repair process.
- No jobs are continuing; discuss equivalent-computation optimization and
  review the completed point evidence before choosing a restart path.

## First post-training task: repair calibration before interpreting v16

Implemented in separate `v16_repaired_*` producers, orchestrated by
`experiments/v16_repair.py`. The `p0` player-ID/prediction collision is replaced
with `forecast`; histories preserve IDs and are rebuilt chronologically.
Registered nonnegative-slope calibration, cold starts, cutoffs, all cohorts,
seeds, blends and native ledgers are unchanged. Constant predictions are flagged,
not prohibited. Archived event reading explicitly maps recovery to rebound.

[Repair protocol](reports/joint_capability_v16_repair_protocol.md).
[Original completion audit](reports/joint_capability_v16_completion_audit.md).
[Earlier diagnosis and exact 2025q1 reconstruction](docs/archive/2026-09-26_pre_repair/SESSION_HANDOFF.md).

Verification so far: **21 regression tests pass**, with a durable log. Independent
numpy reconstruction of 24 real histories in
2015q1–q3; all native/control sufficient statistics identical on those three
quarters. Regression tests cover grouping collision, prior-only fitting, resume,
source preservation and event alias. Full-panel validation automatically checks
population counts and unchanged controls/native scores, and reproduces the
7,747-prior-cell 2025q1/J_POINT_BOTH diagnostic before registered analyses.
The new read-only preview has already reproduced that real diagnostic: direct
RMSE10.972889/r².095253/corr.313316; checkpoint-average half
RMSE10.948036/r².099347/corr.317791, on 166 cells / 19,870 possessions.
This is one quarter, not the final cumulative leaderboard.

The repaired event analysis has already completed separately (48 quarters,
all arms/views/seeds); the main pipeline will verify/reuse that receipt.
J_BOTH versus J_RAW action-count NLL delta −0.000363, season interval
[−0.000461,−0.000273], 11/11 season wins, Holm p=.033203 (34 comparisons).
Location/recovery improvements do not survive that full-family correction.
Event evidence is independent of point calibration; it is not a product pass.

## Pending sequence / remaining work (not running)

1. Finish all 48 corrected origins; validate every point population and original
   control/native parity; print all/novel/recurring leaderboards for all four views.
2. Registered point contrasts, native events/profile/channel audits, fixed
   basketball panels, prior-average opponent evaluation, U0/U1/U2 uncertainty,
   synthetic uncertainty sensitivity and independent saved-state/date audit.
   No stage is presumed complete merely because training finished.
3. Follow-through runs the separately frozen
   [supplement protocol](reports/joint_capability_v16_supplement_protocol.md):
   nine forward-selected/regularized NN+additive ensemble methods and empirical
   reliability split sensitivities. No current-quarter weight selection.
   Direct-view fixture mixtures and own prior-error U0 bands are included;
   absent checkpoint fixture evidence and unmatched numerical references remain
   NOT_EVALUATED. Reliability is assumption-dependent, not a theoretical ceiling.
4. Inspect actual resulting files and all three pillars. Write the final factual
   research review/handoff, update state/scorecard/backlog, discuss next choices.
   No automatic winner promotion. This interpretive step remains pending.

Supplement code/tests are ready, but no real supplement result has been computed
at this checkpoint. Original v16 rankings remain invalid until corrected
validation passes; do not treat live partial repaired rankings as final.

## Live commands (read-only)

```bash
tail -F experiments/cache/joint_capability_2026_09_26_v16_repaired/logs/launcher.log
```

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_repair status
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_repair report --sort r2 --slice all --view half
```

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_repaired_preview --run-dir experiments/cache/joint_capability_2026_09_26_v16_repaired --origin 2025q1 --arm J_POINT_BOTH
```

Preview requires that quarter and its corrected earlier histories; do not use
the old preview with these histories. Supplement progress:

```bash
tail -F experiments/cache/joint_capability_2026_09_26_v16_supplements/logs/launcher.log
cat experiments/cache/joint_capability_2026_09_26_v16_supplements/followthrough_status.json
```

Logs: repair `logs/{prepare,run,events_validation,regression_tests}.log`;
supplements `run.log` after the waiting stage. Executable entrypoints have
resumable receipts; after a failure inspect the exact error and preserve the
failed prefix before deciding how to repair it. Do not edit fingerprinted
producers while these jobs run.

## Working tree

Pre-existing documentation edits and original Opus feedback are preserved.
New repair/supplement modules, tests, protocols and this checkpoint are
uncommitted. No frozen original producer changed. Cached artifacts remain local
and untracked; do not add them to git. Historical runtime/launch instructions
are in the archived handoff, not the current operating sequence.
