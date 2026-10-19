# Current handoff — v16 analysis and independent review COMPLETE (2026-09-27)

## Current state

**All six stages completed and receipts verified. No active campaign remains.**
Final destination:
`experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.

The last report-formatting failure was a missing optional pandas dependency,
`tabulate`. Installed **tabulate==0.9.0**, without dependency upgrades, into
`/Users/adam/miniconda3/envs/basketball25`. Tested `DataFrame.to_markdown()`,
then resumed the unchanged runner. Finalization succeeded in **6.55 seconds**.
Resume supervisor PID4064 / worker4066 finished successfully.
Original failure logs remain append-preserved; their old tracebacks do not
indicate a new failure. The root receipt and progress report are authoritative.

No NN training, point-scoring changes, database access, producer/protocol edits,
promotion, deployment, delegation or commits. Existing uncommitted work preserved.

## Verified completion

- Full prediction audit and two ensemble/reliability supplements.
- All 48 average-opponent origins and 10 fixture origins.
- All 48 uncertainty quarters, plus real/synthetic summaries and identification
  simulations. Numerical recovery uses the unchanged statistical model and
  convergence check; previous accepted fits remain unchanged.
- All four exact-audit origin groups (16 fixed arm/fixture cases).
- Basketball panel, matching-view ensemble fixtures, three-pillar matrix and
  generated handoffs.
- All six stage receipts, root completion receipt, **20 final provenance files**
  and reused source artifacts independently verified after finalization.
- Acceptance label: **COMPLETE_NOT_PROMOTED**. Completion is not a scientific
  product pass. Exact numerical flags still need review; synthetic latent-quality
  interval coverage remains unvalidated.

## Independent review complete — next decision with Adam

The [completed review](reports/joint_capability_v16_codex_review.md) is now the
entry point for findings and recommendations. Current scorecard/state/backlog
and documentation map were refreshed; previous scorecard/state archived.

New read-only review:
`experiments/cache/joint_capability_2026_09_27_v16_codex_review`.
Reproducer: `experiments/v16_completed_review.py`; log `logs/review.log`.
All201 ensemble score rows independently reconstructed from8,345 saved cells /
1,013,999 possessions; source hashes verified before/after. No new fitting.

Main conclusions:
- J_POINT_BOTH half candidates lead: broad r² .162915/.162989 versus
  additive_defense .146023 and parent blend .156601. Direct NN alone .161925.
- Multiple-NN ensembles do not beat the leading simple half blend.
- Adjusted BOTH beats RAW in allnine matched architecture pairs/four views
  descriptively, but architecture-specific multiplicity caution remains.
- Point loss worsens event-count NLL in11/11 seasons versus J_BOTH.
- All22 direct NN arms favor legal five centers over the Jokić lineup;
  leading checkpoint-half margin+4.810. Additive already favors centers+6.345.
  Diagnose defense aggregation and rebound/FT/coverage mechanisms, do not force
  a named ranking. Mixed-era Korver transport is incomplete.
- Leading finite-quarter bands cover93.86% overall,93.31% novel. U2's joint
  log score is slightly worse than U1 in allnine model/split combinations.
  J_POINT_BOTH's own persistent-uncertainty and full average-opponent
  benchmark remain missing.
- Exact numerical audit passes all64 comparisons. Noise sensitivity is not
  a theoretical ceiling. No overall product pass or promotion.

Recommended next: discuss the review, then a bounded center-matchup diagnosis
plus missing product-mode evaluations of the leading candidate. A focused
loss/channel/calibration experiment may follow under a newly frozen plan.
No next experiment has been implemented or launched. No active run, no commit.

Key generated files beneath the final destination:

- `analysis/HANDOFF.md`, `analysis/three_pillar_matrix.csv`
- `analysis/uncertainty/summary/`, `analysis/fixture_uncertainty/`
- `analysis/basketball/`, `analysis/ensemble_fixtures/`
- `supplements/ensembles/`, `supplements/reliability/`
- `numerics/exact/`, `finalization/acceptance.json`, `finalization/sources.json`
- Root `HANDOFF.md`, `complete.json`, `inventory.json`

Read-only status:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_analysis24 status --run-dir experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired
```

Final log:

```bash
tail -n 20 experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired/logs/run.log
```

Do not relaunch old analysis/training campaigns. The failed analysis24 prefix,
corrected scoring prefix and original native training artifacts remain intact.

## Numerical repair evidence and history

[Solver amendment](reports/joint_capability_v16_uncertainty_solver_repair.md):
828-pair stalled U2 fit recovered from mean gradient .02295378 to 3.81e-9;
independent BFGS agrees on mean NLL7.934544078485402. Replay of 180 accepted
fits differs by at most 1.55e-8 in parameters. Fourteen tests passed.
Evidence: `experiments/cache/v16_uncertainty_solver_2026_09_27/`.

[Pre-completion handoff](docs/archive/2026-09-27_pre_report_completion/SESSION_HANDOFF.md)
preserves the numerical diagnosis, launch and full provenance chain.
