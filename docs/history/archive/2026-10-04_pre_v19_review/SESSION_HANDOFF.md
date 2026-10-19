# Current handoff — v19 post-training resumed (2026-10-03)

## State and authority

All720 native cases and48 rolling scorecards completed. Training/scoring took
49.24hours; average-opponent integration completed in2.39hours. The original
supervisor stopped at diagnostics2015q1. Its status.json still says RUNNING;
that is stale. Do not restart the original supervisor.

Adam authorized diagnosis, a downstream fix and resumption. No new neural fits,
database access, input rebuilds, scraping, scorer promotion, deployment or commit.
Direct implementation only. Preserve prior uncommitted roadmap/planning notes.

Read [repair report](reports/joint_capability_v19_accounting_repair.md) for the
cause, implementation, exact audit evidence and commands. The frozen v19 plan,
original producers, training, predictions and all prior outputs remain unchanged.

## Repair and verification

The inherited decomposition assumed recorded points equal points reconstructed
from FG/FT labels. Full immutable-input audit found3 discrepant matchup rows
among1,472,157 event-valid rows, and the same3 among2,772,306 state rows.
One is from2014training; two are2015evaluation warmup. **Zero discrepancies in
primary2016–2026 evaluation.** The original ingestion cause is not established.

New versioned diagnostics expose observed_accounting = observed event points
minus recorded total points. It is a data component, not a learned mechanism.
Point errors keep the original target; no rows removed, targets changed or
tolerances widened. Covariance and evidence retain the extra component.

13 targeted/existing production tests pass. Repaired2015q1/2015q4 complete for
all9models/both environments; game decomposition error <=1.78e-14points.
Unaffected2015q2 has exact dataframe parity with all6old tables; error1.95e-14.
Evidence/logs: experiments/cache/v19_accounting_repair_2026_10_03.

## Active process and operations

New root: experiments/cache/joint_capability_2026_10_03_v19_posttrain1.
Detached caffeinate launcher/supervisor3955, verified running diagnostics with
three workers. No duplicate original campaign was launched. Check current
status/logs rather than assuming a PID remains alive.

It reuses original _scored and _average read-only; all other outputs use the new
prefix with stage suffixes. Three successful bounded diagnostic replays are
reused. No neural training or average integration is repeated.

```bash
tail -f experiments/cache/joint_capability_2026_10_03_v19_posttrain1/logs/run.log

/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v19_posttrain_resume status \
  --source experiments/cache/joint_capability_2026_09_30_v19_prod \
  --out experiments/cache/joint_capability_2026_10_03_v19_posttrain1

bash experiments/run_joint_capability_v19.sh report \
  --run-dir experiments/cache/joint_capability_2026_09_30_v19_prod \
  --sort r2 --slice all --view half
```

Pending automatic stages: diagnostics, observed context, event_roles,
basketball, native_review, uncertainty, persistence, summary, audit, evidence.
The new supervisor writes FAILED/COMPLETE explicitly. It stops at failures or
below10GiB free disk before a stage. About14GiB free before resumption; no
additional cleanup authorized. Durable per-job logs: <newroot>/queues/<stage>/logs.

## Retention mode — mandatory

Completed v16–v18 optimizer restarts were deliberately retired. Final/averaging
weights and original manifests remain. Every consumer process must enter the
retention wrapper; the new supervisor wraps all children.

Ledger: experiments/cache/completed_resume_retention_2026_09_30.
Plan SHA256:825e76b9b847ab3b3ea046b5b302cac772d093a4c6f32be6e3319be7af826cd2.
See [operations](docs/ARTIFACT_RETENTION.md). Do not weaken legacy verification.

## Review and next decision

After the new root is COMPLETE, independently review the registered17point/
28event contrasts and all three standards, then write
reports/joint_capability_v19_review.md and update state/scorecard/roadmap.
Do not claim the scientific review is complete from the interim leaderboard.
Primary remains8,345cells/1,013,999possessions; original half r²:
J_POINT_BOTH.162915, C_FIXED.162937, C_CLOCK.159471, C_FULL.159127,
C_ALLOC.158154, C_MARGIN.156975. Conditional/reference evidence stays separate.

Adam favors context-adjusted player-profile estimation for v20, plus stronger
identifiability/recoverability checks, training stabilization and actual modeling
effort on transport/latent-quality uncertainty. The canonical
[roadmap framing](MODEL_RESEARCH_ROADMAP.md#v19-review-and-v20-framing--agreed-2026-10-02)
records these priorities. They do not authorize a profile rebuild, new fit
campaign or mid-run tuning. Finite-game coverage is not hypothetical latent
coverage; named basketball examples remain falsifiable, not forced rankings.

New code: v19_observation_accounting, v19_diagnostics_v2, v19_persistence_v2,
v19_evidence_v2, v19_posttrain_resume; tests/test_v19_accounting_repair.py.
No old frozen source file changed. No commit made.

The [prior checkpoint](docs/archive/2026-10-03_pre_v19_repair/SESSION_HANDOFF.md)
preserves launch details and earlier planning notes. The background process runs
independently; no automatic assistant wakeup is promised.
