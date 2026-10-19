# Current handoff — v17 core implemented; bounded pilot running (2026-09-27)

## Authority and commits

Direct implementation only; no delegation. Adam asked to proceed while
documenting and committing progress. No scraping, database mutation, input-cache
rebuild, scorer promotion or deployment. **Do not launch full v17 without Adam's
authorization.** The currently authorized run is the prescribed bounded pilot.

- **3fb8f1cb**: completed v16 matchup diagnosis, point-candidate follow-up,
  independent review, tests and documentation.
- **e9f994ec**: frozen v17 opportunity experiment plan and fixed arm registry,
  committed before pilot outcomes.
- Core implementation/tests/current docs form the checkpoint commit titled
  `Implement v17 opportunity models and launch bounded pilot`. Keep generated
  caches out of git; preserve unrelated untracked work.

Read [v17 plan](JOINT_CAPABILITY_V17_PLAN.md), then the
[implementation checkpoint](reports/joint_capability_v17_implementation_checkpoint.md).
Prior completed findings remain in the [point follow-up review](reports/joint_capability_v16_point_followup_review.md).

## Implemented and verified

Five new arms: O_ORDER, O_FLOW, D_SHAPE, O_FLOW_D_SHAPE, O_FLOW_EVENT.
Ordering correction, explicit shared creator capacity, defensive-volume
ablation, combined arm and event-loss control. These are hypotheses, not fixes
known to improve predictions. No forced five-center or named-pair ranking.

New model, receipt-checked source reader, fixed engineering micro-pilot,
versioned fresh-inner/final trainer and native-case exporter; pilot-only CLI.
Frozen v16 code and completed artifacts untouched.

**19 tests passed**, including exact control parity, action/rebound accounting,
independent slot permutations, finite gradients, flow caps/no self-assists,
checkpoint-average ledger, exact resume and changed-provenance rejection.

Real-input micro-pilot:14 cases,168 optimizer batches,26.82seconds.
Largest action-ledger error2.43159e-7 (limit3e-6); all losses/gradients finite.
Flow compute overhead16–18% versus point control on prefetched batches.
No validation or outer outcomes scored; **no predictive conclusion**.
Artifacts: `experiments/cache/joint_capability_2026_09_27_v17_core_dev1`.
Tests log: its `logs/fit_tests.log`; micro receipt and log: `micro/`.

## Active process

Bounded full-epoch pilot:
`experiments/cache/joint_capability_2026_09_27_v17_pilot1`.

Five arms ×2016q1 ×seed17 =5 cases/10 inner-final fits.
Three independent CPU workers, one thread each. Normal cap96/patience8.
Two shell-background launches did not survive and started no worker.
Detached-session supervisorPID**7222** is verified running, with initial
workers7224/7225/7226. Verify current queue/process state rather than assuming
these PIDs remain current. This pilot does not start a full run on completion.

Status:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v17_pilot status --out experiments/cache/joint_capability_2026_09_27_v17_pilot1
```

Supervisor log:

```bash
tail -f experiments/cache/joint_capability_2026_09_27_v17_pilot1/logs/launcher.log
```

Epoch-level log example:

```bash
tail -f experiments/cache/joint_capability_2026_09_27_v17_pilot1/queue/logs/2016q1_O_FLOW_s17.log
```

Native results: `origins/2016q1/<arm>/s17/fit_summary.json`, with event losses
and matching v16 control losses. These are **uncalibrated operational pilot**
comparisons, not a full-history leaderboard. Do not choose/drop arms from them.

## Precise restart

1. Check pilot queue and per-case logs; do not start a duplicate. If complete,
   verify all receipts and review timing, temporal cutoffs and export consistency.
2. Complete corrected chronological calibration/control reuse and live report
   integration. New v17 reporting files only; no frozen v16 producer edits.
3. Wire the frozen average-opponent, analogue/fixture and U0/U1 analyses.
4. Production preflight and runtime/storage estimates; verified launch/log/status
   commands for Adam. No production command exists yet.
5. Commit verified milestones, update this handoff/state rather than prepending
   competing checkpoints.

The plan contains720 new cases/1,440 fits,48 quarters/three seeds. Those have
**not** been launched. Current pilot prepares only five cases.

Current scientific limitations: assist rates and assisted fraction are proxy
assumptions; allocation is not a causal assist network; finite-game coverage
does not validate hypothetical true-quality uncertainty. Keep all three product
standards co-equal and preserve unsuccessful arms.

[Previous handoff](docs/archive/2026-09-27_pre_v17/SESSION_HANDOFF.md) preserves
the completed v16 review details. No completed research artifacts were removed.
