# v16 equivalent-computation optimization — 2026-09-19

Adam requested stopping the active campaign and optimizing it. No scientific
amendment: all 22 arms, 48 quarterly origins, three seeds, prefixes, objectives,
precision, initializations, optimizer, shuffles, stopping and forecasts remain.
No promotion, deployment, database access or input-library rebuilding.

## Preserved baseline

`experiments/cache/joint_capability_2026_09_19_v16_hashfix` is stopped and
retained. Four completed native cases and three interrupted cases are preserved.
The optimizer journals remain usable by the original implementation. Queue
status is stale after the supervisor's KeyboardInterrupt; it is not evidence
that the recorded PIDs are still running. Shutdown was verified with the OS.

All original producers and metadata-repair files stay unchanged. New versioned
trainer, model, case and runner files isolate the optimization. Original shared
references, inference, scoring, diagnostics and independent audit are reused.

## Permitted changes

1. Disabled adjusted banks: evaluate their identically zero centered networks
   on one five-player example and broadcast; retain parameters and zero-gradient
   Adam/weight-decay behavior. Full-width zeros remain in joint module inputs.
2. Skip adjusted feature-library lookups for banks disabled by the fixed arm.
3. Memoize frozen decoder outputs and unlearned defender moments by row, within
   ONE prefix/normalizer/arm/frozen-parent context. History and origin-frozen
   rows cannot share memo slots. Recompute all jointly learned operations.
4. In-memory, process-local memo only; no persisted input cache, new fitted
   features, reordered observations or substituted validation data.

## Acceptance

- All-arm, early/late real-data comparisons of forward, objective, gradient,
  and Adam updates, including already-nonzero residual heads. Initial bounded
  checks: six steps, 512 rows; follow with full-game-sized batches.
- Bounds fixed before these checks: maximum point difference 1e-4 points/100,
  loss 1e-8, parameter/gradient difference 2e-6. Exact equality is reported when
  achieved. These are equivalence checks, not new predictive comparisons.
- One full-stopping exact production-case replay, 2015q1/J_RAW/s23: identical
  stopping/selection and checkpoint epochs; full trajectory and forecasts checked.
- Alternating-order warmed CPU measurements for RAW, BOTH and ALL_BOTH. Report
  one-time memo population separately; do not infer campaign-wide speedup from
  the cheapest arm. Inspect memory before retaining three workers.
- Original 95 tests plus new source-parity/schema/context-guard checks.
- No full campaign relaunch during optimization. A new destination and explicit
  launch gate are required; do not splice changed provenance into the old run.

Evidence namespace: `experiments/cache/v16_speed_2026_09_19_v1/`, durable logs
under `logs/`. Original 44 smoke/eight pilot results remain scientifically
applicable only together with the new equivalence evidence; no repeat tournament.
