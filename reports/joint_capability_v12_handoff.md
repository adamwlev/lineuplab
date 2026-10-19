# Joint capability v12 operational handoff

**Superseding decision, 2026-09-14:** Adam authorized analysis of the partial
results. Read `reports/joint_capability_v12_partial_codex_review.md`. The full
rerun is on hold; no training was launched. The following launch-ready state is
an operational record, not the current recommendation to repeat all fits.

Date: 2026-09-14  
State: repaired production prefix `NOT_STARTED` after successful preflight

Read `SOL_JOINT_CAPABILITY_DAY6_PLAN.md` and
`reports/joint_capability_v12_launch_checkpoint.md`. The Day5 audit closeout,
v12 implementation, causal replay, focused verification and both prescribed
pilots are complete. The first production attempt stopped after 74/96 outputs
on a float32 ledger tolerance, not a training failure. The correction and
targeted 2024q2 validation are documented in the launch checkpoint. The clean
production prefix is frozen at
`experiments/cache/joint_capability_2026_09_14_v12_prod_ledgerfix/`; do not change a
scientific producer or source artifact in place.

The exact launch/live/status commands and quantitative pilot table are in the
launch checkpoint. Adam has not authorized or launched the production run in
this session. Expected wall time is 43--81 minutes. The wrapper writes
`logs/process.json`, durable stdout/stderr, an atomic `logs/exit.json`, and the
runner writes `completion_status.json`. Running the same command after a stopped
process resumes only from verified completed arm-origin receipts.

When the run finishes, do not stop at `ANALYSIS_COMPLETE`. Inspect all 96
arm-origin receipts and the generated scorecards, reconciliation ledgers,
weighted failure cases, intervals and basketball panel. Write
`reports/joint_capability_v12_review.md`, update this handoff and the top-level
research indexes, and explicitly evaluate all three product standards. No
promotion or commit is authorized by the Day6 plan.

Known limitation: the implemented resume guarantee is at completed-fit
boundaries, not inside an interrupted optimizer fit. The full repository suite
has one expected-but-real failure because the new scientific producers remain
untracked under the explicit no-stage/no-commit restriction; 759 other tests
pass, including all 17 directly relevant v11/v12 tests.
