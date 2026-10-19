# Bounded v16 post-training analysis: implementation and verification

2026-09-26. Prepared, preflight passed, **full run not launched**. No neural
refits, input changes, original producer edits, promotions or commits.

## Why this version exists

The original fixture loop was estimated at ~194 additional serial hours before
other diagnostics. It rebuilt joint-draw features over 157k–309k opponent fives
128 times per enabled bank, per fixture/arm/seed. The new version implements
the [approved numerical/budget amendment](joint_capability_v16_analysis24_protocol.md)
without changing the predictive experiment or dropping named difficult fixtures.

## Components

- `experiments/v16_analysis24.py`: isolated source links, fingerprinted manifest,
  stage dependencies, heavy-origin-first seed-partitioned queues, CLI/status.
- `v16_analysis24_budget.py`: owned process groups, fail-stop, receipt-aware
  resume and deadline cleanup. Main launcher also has an absolute wall alarm.
- `v16_analysis24_sensitivity.py`: sum gradients by player; shared joint draws
  and nonlinear spot checks preserved; cache only small player-level tables.
- `v16_analysis24_fixtures.py`: common 4096/16384 references, all fixed panels,
  shifted numerical checks, complete-origin escalation and 16 exact audits.
  Checkpoint-average means average predictions, not weights; restore primary
  weights after scoring. Additive references are common across all members.
- `v16_analysis24_audit.py`: full prediction/temporal/native-ledger audit from
  the original independent auditor; separates unfinished analysis-presence
  requirements, caches repeated contexts/splits, retains every case/population.
- `v16_analysis24_supplement.py`: unchanged nine statistical methods and noise
  sensitivity, gated by the prediction audit rather than full fixture completion.
- `v16_analysis24_uncertainty.py`: unchanged uncertainty construction, but
  synthetic descriptors share the selected numerical opponent reference.
- `v16_analysis24_finish.py`: refuses partial frontiers; full fixed-panel
  summaries, uncertainty, exact numerical audit, matching-view fixture mixtures,
  three-pillar matrix and final provenance. No automatic model promotion.
- `v16_analysis24_preflight.py`: real early/late comparison, exhaustive saved
  result parity, unseen/clone feature checks and serial/parallel pilots.

Original modules and protocols remain byte-for-byte intact; configuration
fingerprints for both the original training and stopped repair were checked.
The development prefix `...analysis24_dev1` is historical after final queue
refinements; only `...2026_09_26_v16_analysis24` is ready to launch.

## Measured evidence

| Check | Result |
|---|---|
| Unit/regression suite | 23 pass |
| 2016q2 Cleveland, 512-reference sensitivity, old/new | .880s / .498s; maximum shift difference 3.97e-8 PPP100 |
| Full Cleveland 157,079-reference optimized sensitivity | 9.29s; maximum difference from saved exhaustive output 5.59e-8 PPP100 |
| 2026q4 five-Gobert, 512-reference sensitivity, old/new | .844s / .498s; maximum shift difference 3.92e-8 PPP100 |
| Late ALL_BOTH fixture, all three seeds serial/parallel | 92.04s / 35.56s, 2.588x throughput |
| Peak measured worker RSS | 2.10 GB |
| Machine physical RAM | 16 GiB |
| Serial/parallel panel, player, sensitivity and quadrature outputs | Identical for all three seeds |

The old five-minute full fixture duration is **not** an isolated sensitivity
benchmark. Do not claim a measured 30x end-to-end speedup. The new throughput
pilot includes loading and extra checkpoint-average/shift computations; it is
not a measured whole-campaign ETA. Three workers pass the declared speed/memory
gate. Numerical equivalence tolerance was fixed at 5e-5 with 1e-5 relative
tolerance; observed errors were far smaller. Shift samples do not supply
statistical confidence intervals. Full exact-audit comparisons remain pending.

## Artifact locations and remaining work

Ready prefix: `experiments/cache/joint_capability_2026_09_26_v16_analysis24`.
`preflight/{acceptance.json,equivalence.csv,throughput/}` and
`logs/preflight.log` contain real evidence. Test log:
`experiments/cache/v16_analysis24_verification_2026_09_26/logs/tests.log`.
Launch/status/live-log commands are in [the current handoff](../docs/history/SESSION_HANDOFF.md).

Still pending: full independent prediction audit, real statistical supplements,
remaining average-opponent quarters, full sampled fixed panels/exact audits,
uncertainty analysis and human three-pillar interpretation. The completed
corrected point/event/profile/channel artifacts are reused unchanged.

24 hours is an enforced execution limit, not a guarantee every task finishes.
The launcher saves an explicit completion/deferral inventory. No automatic
extension. No accuracy-based arm selection or test-quarter ensemble fitting.
