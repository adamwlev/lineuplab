# v17 implementation checkpoint — 2026-09-27

This is an **engineering checkpoint**, not a model-performance review.
Scientific design: [frozen v17 plan](../docs/history/JOINT_CAPABILITY_V17_PLAN.md), committed
before pilots as **e9f994ec**. The preceding completed v16 follow-up and review
were committed as **3fb8f1cb**.

## Implemented

- Five fixed arms: O_ORDER, O_FLOW, D_SHAPE, O_FLOW_D_SHAPE, O_FLOW_EVENT.
- Reordered constraints, capped no-self creator/finisher flow, learned
  turnover/self-creation fallback, and isolated defensive-volume ablation.
- Existing load and FT-shortage responses and renewal accounting retained;
  frozen FT/assisted outputs retained. No synthetic ranking objective.
- Versioned model and training loop; no edits to frozen v16 producers.
- Read-only context reuse checks row hashes, cutoffs, source receipts and dated
  parents. No database access, scraping or fitted-input rebuilding.
- Deterministic checkpoint resume, bounded last-five averaging and native
  result export, with existing common event references.
- Pilot-only CLI with three CPU workers, durable supervisor/per-case logs and
  status receipts. It deliberately exposes **no production command** yet.

The v17 training loop retains v16's optimizer, batching, early-stop selection
and journal semantics. It is versioned separately to bind the new model and
protocol hashes without mutating imported module globals. New variants only
use the basic stationary pooled architecture; inherited attention/allocation/
phase experiments are not silently reintroduced.

## Verified micro-pilot

Artifact: `experiments/cache/joint_capability_2026_09_27_v17_core_dev1/micro`.
Status: **PASS_ENGINEERING_ONLY**,14 cases,168 optimizer batches,26.82seconds
including setup and verification. Two dates, seed17, five new arms plus the
two unchanged controls. Exactly12 earliest game-preserving inner-training
batches at each date:48,880 rows for2016q1 and48,955 for2026q4. Those are
aggregate training rows, **not** unique evaluation possessions.

| Arm | Active parameters | 2016q1,12 batch seconds | 2026q4,12 batch seconds |
| --- | ---: | ---: | ---: |
| J_POINT_BOTH control | 24,837 | 1.256 | 1.188 |
| J_BOTH control | 24,837 | 1.226 | 1.201 |
| O_ORDER | 24,837 | 1.213 | 1.156 |
| O_FLOW | 24,838 | 1.455 | 1.397 |
| D_SHAPE | 24,645 | 1.219 | 1.202 |
| O_FLOW_D_SHAPE | 24,646 | 1.446 | 1.422 |
| O_FLOW_EVENT | 24,838 | 1.420 | 1.402 |

Times include forward/backward/optimizer work on prefetched inputs, not a whole
fit or three-worker contention. Flow takes about16–18% more than the point
control on these batches. Do not extrapolate final runtime without full pilots.
Active counts are reachable parameter coordinates, not functional rank. Flow
adds two scalar parameters and disables one old shortage scalar, net+1.

All losses and gradients finite. Largest weighted-action ledger error:
**2.43159e-7**, below3e-6. All14 checkpoint reloads reproduced predictions exactly;
source hashes and shared-context receipts remained unchanged. The flow
coefficients moved from .1 during optimization, establishing a reachable
gradient—not support for their scientific value.

No validation or outer outcomes were evaluated by this micro-pilot. Its losses
cannot rank predictive performance. Counts-only and point-augmented objectives
also have different scales; do not compare their raw training losses as scores.

## Tests

**19 passed**:9 new model/flow tests,2 new optimization/resume tests,8 existing
v16 model tests. Tests cover exact control parity, intervention-off specialized
forward parity, independent offensive/defensive slot permutations, finite
gradients, no-self/row/column capacity constraints, fallback identity, ledgers,
zero/full-capacity cases, frozen unsupported outputs, disabled parameter masks,
checkpoint averages, exact resume and changed-provenance rejection.

Log: `experiments/cache/joint_capability_2026_09_27_v17_core_dev1/logs/fit_tests.log`.

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest tests.test_v17_fit tests.test_joint_capability_v17_model tests.test_joint_capability_v16_model
```

## Current bounded run and remaining work

The full-epoch **pilot**, not production, is launched at
`experiments/cache/joint_capability_2026_09_27_v17_pilot1`.
Five arms ×2016q1 ×seed17;10 inner/final fits, at most three workers.
Normal cap96/patience8/prior-quarter validation. Fresh final fit uses the
inner-selected epoch count. Its forecast exports may be inspected for numerical
correctness, not used to alter the registered arms.

Two shell-background launches did not survive; neither started workers.
The detached-session replacement was verified running outside the sandbox,
supervisorPID7222, with initial workers7224/7225/7226. Use status receipts rather
than assuming these PIDs remain current. Completion does not launch production.

Remaining before giving a production command:

1. Inspect all five completed pilot receipts, temporal boundaries, selected
   epochs, native controls and runtime/storage behavior.
2. Implement/test chronological corrected calibration, control reuse and live
   matched scorecards for the new namespace.
3. Connect the registered average-opponent, fixture/analogue and candidate-
   specific uncertainty analyses without repeating the old exhaustive runtime.
4. Finish production manifest, read-only status/report interface and preflight;
   provide verified background commands, then wait for Adam's authorization.

No v17 predictive or three-pillar success claim yet. The unchanged v16 point
candidate remains the leading research candidate; no scorer promotion.
