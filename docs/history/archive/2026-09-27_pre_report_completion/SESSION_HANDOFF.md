# Current handoff — v16 uncertainty repair continuation (2026-09-27)

## Current decision

Adam authorized debugging and numerical recovery after stage 5 failed.
The repaired continuation has been launched in a **new derived prefix**.
Supervisor PID **3526**, initial uncertainty worker **3528**.
No duplicate launches, delegation, NN training, source-artifact edits, promotion,
deployment or commits. No overall or stage timeouts.

- Active destination: `experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.
- Preserved failed source: `experiments/cache/joint_capability_2026_09_26_v16_analysis24`.
- Corrected scoring source: `experiments/cache/joint_capability_2026_09_26_v16_repaired`.
- Original trained source: `experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`.
- Source stages 1–4 completed: full prediction audit, ensembles/reliability,
  48 average-opponent quarters, all 10 fixture origins. All shift checks passed.
- Stage 5 saved 15 completed quarters through 2018q3, then failed in 2018q4.
  Stage 6 had not started. All completed outputs are reused by verified links.
  Incomplete 2018q4 outputs and original logs remain in the failed prefix.
- New continuation resumes uncertainty chronologically, then automatically
  finalizes. It stops on errors. No automatic assistant wakeup is promised.

## Diagnosis and numerical repair

U2 / J_ALL_BOTH:half / first_second, 828 prior pairs, penalty10: L-BFGS-B
hit the existing log-variance overflow guard on a trial (absolute eta806),
then falsely declared relative-objective convergence. Its mean gradient was
.02295378, failing the original <1e-5 acceptance check.

Versioned process-local optimizer override leaves accepted fits unchanged.
On failure only, restart with fresh L-BFGS-B history, scaling the entire
objective/gradient (including the penalty) by pair count. One bounded BFGS
fallback follows if necessary. Accept only a nonincreasing finite objective
and the same original gradient threshold; otherwise fail closed.
No changed likelihood, penalty grid, selection window, cutoff or point mean.

- Repaired failing sum NLL **6587.125148 → 6569.802497**.
- Mean gradient **.02295378 → 3.81e-9**.
- Independent BFGS agrees on mean NLL **7.934544078485402**.
- Finite-difference mean-gradient discrepancy **6.38e-11**.
- **180 saved accepted fits** replayed: maximum parameter difference **1.55e-8**.
- All nine model/split fits for the failed quarter pass.
- **14 tests pass**, including original uncertainty, chronology and queue tests.
- Evidence: `experiments/cache/v16_uncertainty_solver_2026_09_27/`
  (`acceptance.json`, `replay.csv`, durable `logs/`).
- [Frozen numerical amendment](reports/joint_capability_v16_uncertainty_solver_repair.md).
- New implementation: `experiments/v16_uncertainty_numerics.py` and
  `experiments/v16_uncertainty_resume.py`. Old fingerprinted producers untouched.
  Source receipts and all their files are verified before/after continuation.

## Current commands

Live detailed uncertainty log:

```bash
tail -F experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired/queues/uncertainty/logs/uncertainty.log
```

Overall log (stage 6 follows automatically):

```bash
tail -F experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired/logs/run.log
```

Read-only stage status:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_analysis24 status --run-dir experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired
```

Already launched; reference only, do not duplicate:

```bash
nohup /usr/bin/caffeinate -i /Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_uncertainty_resume run >> experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired/logs/launcher.log 2>&1 < /dev/null &
```

After completion, inspect the exact numerical audit, uncertainty coverage,
basketball fixtures and ensemble comparisons together; finish human
three-pillar interpretation. No automatic promotion or validated synthetic
latent-quality coverage claim. Existing point leaderboards remain available;
these uncertainty fits do not change their forecasts.

## History

[Pre-recovery handoff](docs/archive/2026-09-27_pre_uncertainty_repair/SESSION_HANDOFF.md)
preserves the optimized-analysis launch and original benchmark evidence.
All pre-existing uncommitted work remains; no commits made.
