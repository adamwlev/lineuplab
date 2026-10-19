# Current handoff — V20 post-training continuation (2026-10-08)

## Authority and exact next step

Direct implementation; no delegation. Adam approved repairing and resuming the
failed post-training analysis. **Training is complete:864/864native cases,
48/48scored origins.** Training/scoring took48.88h. No retraining or rescoring.

The original production supervisor stopped at stage6/19 (average-opponent
evaluation). Its status remains FAILED_REVIEW_REQUIRED as historical evidence.
Do not restart it. The replacement continuation is running, detached PID65142,
with three numerical workers. Initial active jobs:average_2015q1/q2/q3.
Check current status rather than inferring completion from this checkpoint.

```bash
bash experiments/run_v20_posttrain_continue.sh status
tail -f experiments/cache/joint_capability_2026_10_08_v20_posttrain1/logs/launcher.log
```

The existing leaderboard command is unchanged:
```bash
bash experiments/run_joint_capability_v20.sh report --sort r2 --slice all --view checkpoint_average_half
```

No automatic assistant wakeup. After completion, inspect all19stages' evidence
and write the scientific three-pillar review; arithmetic audits do not imply
scorer promotion or validated hypothetical-lineup uncertainty.

## Repair and preservation

[Repair report](reports/joint_capability_v20_posttrain_repair.md) explains the
null optional compact-directory bug and recovery. New versioned average,
basketball and optional pilot-replay consumers change only the path fallback;
AST regression confirms otherwise identical code. The pilot-only restriction
on the replay utility remains. Frozen producer files and protocols unchanged.

Five completed stages (controls/events/diagnostics/roles/observed) and all scored
origin receipts verified and reused without rerunning. Remaining14stages use
new output prefixes and the unchanged frozen dependency graph, except for the
two repaired consumer module names.70v20tests pass; preflight source fingerprints
and output hashes pass. Output/data overlap protection remains tested.

Original run:experiments/cache/joint_capability_2026_10_06_v20_prod.
Continuation:experiments/cache/joint_capability_2026_10_08_v20_posttrain1.
Its manifest maps reused and new roots; new stage products use that prefix plus
_average, _basketball, _uncertainty, _risk, etc. Original completed outputs stay
under the old production prefix. Original failed logs/status remain intact.
Continuation has single-writer locks, append-safe logs, three total numerical
slots,13GiBdisk reserve and receipt-based resume.71GiBwas free at repair.
Do not run two continuations. If it fails, diagnose before resuming:
`bash experiments/run_v20_posttrain_continue.sh run` resumes saved work.

Prelaunch post-training estimate was18.84hcentral/29.73hstressed, not a fresh ETA;
five quick stages are already complete. Full exhaustive risk census remains;
no sampling amendment, new fits, scraping, cache rebuild, deletion or promotion.

## Scientific and working context

[Plan](JOINT_CAPABILITY_V20_PLAN.md), [state](JOINT_CAPABILITY_STATE.md), and
[product contract](CONTEXTUAL_MODEL.md) govern. Three standards stay coequal.
No known pairs, forced rankings or coverage gates. Primary checkpoint-average-half;
48origins,2015warmup excluded from primary. All final scientific conclusions pending.

[Post-v20 direction notes](MODEL_RESEARCH_ROADMAP.md#post-v20-direction-notes--2026-10-06)
preserve the Opus5.5review discussion. The separate
[bias follow-up](MODEL_RESEARCH_ROADMAP.md#bias-follow-up--exploratory-evidence-2026-10-06)
preserves new diagnostic consumers/outputs: near-zero global FG-conversion error
conceals a persistent final-exposure cohort gap; prior-known exposure has a
smaller gap and early-game shooting residuals barely persist. These are not
causal corrections or changes to v20.

Latest committed checkpoint3fd8bc28. Existing launch/direction/bias documentation,
bias diagnostic scripts and new repair/continuation/tests are uncommitted.
Preserve Adam's OPUS_55_review_100626.md. No commit authority in this repair task.
Never stage generated cache files. Durable repair checks:
experiments/cache/v20_posttrain_repair_2026_10_08/logs/{tests,preflight}.log.

[Previous handoff](docs/archive/2026-10-08_pre_v20_continuation/SESSION_HANDOFF.md)
preserves full launch/readiness details and prior archive links.
