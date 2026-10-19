# v16 analysis execution override — 2026-09-26

Adam explicitly removed the hard runtime limit and authorized background launch.
The 24-hour target is a planning goal, not a stopping rule. No overall or
per-stage timeout is active under `experiments.v16_analysis_continue`.

All scientific producers, samples, arms, seeds, cutoffs, statistical methods,
completion checks and the accepted three-worker preflight are unchanged.
The original bounded launcher/protocol and prepared manifest remain intact.
This orchestration-only addition has a separate hashed `execution/manifest.json`
inside the prepared, not-yet-completed analysis tree. It reuses completed
preparation/preflight outputs and requires no repeat benchmarking or refitting.

Run stages in their established order to completion. Prediction audit gates
statistical supplements; numerical escalation remains bounded to 16384, as
specified scientifically, not by time. Stop launching on failure; finish any
already-running independent jobs, report failure and do not silently skip a
stage. User interruption terminates owned workers. Resume requires authorization.
No training, original-artifact edits, promotion, deployment or commit.
