# Current handoff — v19 foundation implemented (2026-09-30)

## Current checkpoint

Adam authorized a commit and implementation. Commit **b7401231** records the
completed v18 sources/reviews/diagnostics and v19 plan, excluding cache artifacts.
The new v19 implementation below is uncommitted. Direct implementation only.

Read [the implementation checkpoint](reports/joint_capability_v19_implementation.md)
and [the v19 plan](JOINT_CAPABILITY_V19_PLAN.md). The source audit, derived context
labels, five model branches, loss replay, exact context integration and first
real-data verification are complete. **No v19 training fit or outer evaluation
has run. The training runner and full launch commands are not ready.**
No job remains running. Full launch still requires separate authorization.

## Completed implementation

- All288 inner/final J_POINT_BOTH teachers pass cutoff, row, normalization,
  receipt and epoch checks across48 origins and3 seeds;599 provenance entries.
- New context labels:3,056,123 rows from1,592,743 original matchups /
  6,059,380 possessions. Exact zero-error rollup on all9 event/point ledgers,
  with unchanged masks and2,216,895 eligible recoveries.
- All five models exist: C_FIXED, C_CLOCK, C_FULL, C_ALLOC, C_MARGIN.
  Shared encoder work is reused across states; live gradients are preserved.
- Reference integration averages complete expected ledgers, not probabilities.
  Conditional future-context scores will remain distinct from reference ratings.
- Real float64 zero-context replay:120 comparisons over24 training game batches
  at2016q1/2026q4.97,835 original rows /191,261 state rows.
  Max prediction difference2.78e−17, event-statistic difference3.64e−12,
  backbone-gradient difference2.37e−19.
-29focused tests pass. This is correctness evidence, not a predictive comparison.
  No revised r², coherence or uncertainty claim; J_POINT_BOTH remains reference.

## Files and durable outputs

New modules: experiments/joint_capability_v19_protocol.py,
joint_capability_v19_model.py, v19_sources.py, v19_labels.py, v19_context.py,
v19_context_head.py, v19_loss.py, v19_training_data.py, v19_integration.py,
v19_replay.py. Four test modules: tests/test_v19_foundation.py,
test_v19_context_head.py, test_v19_model.py, test_v19_labels.py.

Completed prefixes under experiments/cache/:
- joint_capability_2026_09_30_v19_sources2
- joint_capability_2026_09_30_v19_labels1
- joint_capability_2026_09_30_v19_replay_smoke1
- joint_capability_2026_09_30_v19_replay1

Each has a COMPLETE receipt and durable sibling .log.
Tests: experiments/cache/v19_foundation_tests5.log.
The first source-audit attempt misinterpreted a legacy model hash field; it was
corrected in the checker and the old failed output preserved. A synthetic dtype
test caught teacher rounding, corrected before the passing real-data replays.
No frozen old producer was modified. Details are in the implementation report.

Source audit6.77s; label build52.11s; full replay79.69s. Do not extrapolate an
epoch/campaign duration from replay: it runs old and new float64 graphs together.
Numeric derived arrays total about1.074GiB; no upstream cache was rebuilt.

## Exact next step

Implement the resumable inner/final training and prediction runner on this
verified foundation. Preserve existing epoch/cutoff/objective contracts.
Then float32 optimizer/resume checks and the seven prescribed full pilots;
separate conditional/reference calibration and fair context point controls;
complete fixture/average-opponent/U0/U1/diagnostic/report adapters and measured
one/three-worker plus downstream runtime/storage preflight.

The proposed campaign remains720cases/1,440fits and a54h all-in planning target,
not a measured estimate. Do not launch the full run or supply an unverified
training command. Deliver verified launch/live-log/status/report/preview commands
when ready, and wait for Adam's authorization.

All three standards remain co-equal. No pair chemistry, forced fixture ranking,
coverage gate, scraping, database mutation, profile rebuild, promotion or deployment.
Completed artifacts and bound producers are immutable; use versioned corrections
and fresh prefixes if needed. Future summaries must distinguish marginal ratings,
actual-context diagnostics and original-population forecasts.

## Preserved history and dirty work

The completed v18 evidence is committed in b7401231. Its original reports,
protocols and artifacts remain unchanged. Current scientific conclusions are
in [state](JOINT_CAPABILITY_STATE.md) and [scorecard](MODEL_SCORECARD.md).

New v19 code/tests and current documentation are uncommitted after the requested
checkpoint. Numerous cache directories remain untracked: never blanket-stage.
No further commit was made after implementation.

[Displaced planning checkpoint](docs/archive/2026-09-30_pre_v19_foundation/SESSION_HANDOFF.md)
and adjacent state/roadmap/navigation snapshots preserve the prior documentation.

