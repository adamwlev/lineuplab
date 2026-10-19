# V20 downstream integration and batching rehearsal — 2026-10-06

This is prelaunch engineering evidence, not a new model comparison or scorer
promotion. Original neural fits, profiles and scientific protocol are unchanged.
Full campaign launch still requires Adam's explicit approval.

## What is implemented

- Physical-count checkpoint/seed mixtures for reference and actual-clock event
  losses; probabilities are derived from mixed masses, not averaged losses.
  Missing retained C_FULL averaged conditional-state exports are reconstructed
  into a new sibling output, with archived pooled-forecast replay checks.
- Five additional descriptive point controls: C_FIXED, C_CLOCK, R_ALLOC,
  O_ORDER and J_BOTH, using the same strictly prior-only calibration.
- Event/share/role, original transfer cohorts, all eligible observed context
  curves, game-partition persistence and cross-channel covariance diagnostics.
- Fixed 17 point, 44 event and four uncertainty comparison schemas, season-level
  inference, primary-only pooling and explicit cold/unidentified results.
- Fixture discrepancy sensitivities and the fixed P_BASE-based as-of risk slice.
  No coverage gate or change to point forecasts; no validated hypothetical
  latent-quality coverage claim.
- A three-slot training/scoring queue, with at most one chronological scorer;
  a 19-stage analysis/audit graph; explicit approval/readiness/disk guards.
  Existing eight pilots are reused, leaving856new case slots.

## Numerical evidence, not arm selection

The late2026q4 retained-control rehearsal mixes all three seeds and selected
checkpoints before scoring. Actual-clock losses are:

| Event | P_BASE | P_CONTEXT |
| --- | ---: | ---: |
| Counts | .76683998 | .76484504 |
| Location | 1.29627710 | 1.29569138 |
| Conversion | .65283161 | .65234009 |
| Recovery | .90775080 | .90710993 |

This reproduces the existing conditional-context story on one quarter, not a
new v20 win. Independent NumPy/Torch event arithmetic agrees. Two isolated pilot
dates have different arm rosters and cold neural calibration; do not pool them
into a production leaderboard. The previous product rehearsal still finds all
four late-date pilot candidates favor legal centers over both Jokić fixtures,
with primary margins+5.69to+7.62; context-model center FTA~36–40/100. No coherence
pass follows. Cold fixture discrepancy intervals remain NaN, not zero width.

## Exhaustive risk check: keep the science, remove repeated work

The registered check asks whether unfamiliar predicted roles identify difficult
future lineup deployments. At each origin, P_BASE predicts player FGA/FTA/TO
shares against512common prior-opponent draws. R is the maximum player-level RMS
standardized deviation from prior empirical shares. The threshold is the
unweighted95th percentile across all distinct historically observed offensive
compositions, rescored with current-origin frozen inputs. Future outcomes do not
set this threshold. Every future composition is scored; support flags remain
separate. This is a diagnostic slice, not a causal role-change label or gate.

Increasing the old batch size alone did not help. The optimization caches the
lineup-only graph/constraint computation and defender-only terms, then batches
the remaining count/conversion/renewal operations. Input construction is also
vectorized. The decoder specialization rejects unsupported architectures.

- Two dates ×three seeds ×five batching variants:30measurements. Typical64-five,
  512-opponent batches fell from2.8–3.0seconds to~.20–.23seconds.
- Measured optimized counts and R matched the original path exactly across
  those comparisons. Current, duplicate-slot and unknown-player input tensors
  were byte-identical to the original constructor.
- End-to-end1024-five tests, including construction:2.00–3.01seconds per seed;
  source/model setup is reported separately. Larger512-five resumable blocks
  retain8192-matchup inference chunks.
- The saved64-five old/new census probe matches byte-for-byte for IDs, FGA,
  FTA, TO, R, thin support and unknown-player flags.
- A deliberately interrupted1024-five disposable probe resumes without
  changing its completed first block. A completed full early-date census
  resumes without changing any result file or its timestamp.

The two full-size pilot-date censuses and independent slow-decoder replay are
part of the final graph rehearsal. No historical-lineup sampling amendment was
made. The earlier rough week-long cost estimate described the inefficient
implementation, not an unavoidable scientific cost.

## Resume defect discovered by the graph rehearsal

The first controls consumer lacked a completed-root early return. Replaying it
rewrote only `v20_extra_controls_pilot_2026_10_06/status.json` with a new elapsed
time, invalidating that file's original root receipt. Both quarter receipts and
all numeric predictions/tables were preserved. Do not claim that root still
passes its original receipt or silently repair it.

`v20_controls_v2` returns after verifying a completed root, before loading data
or writing status. The repaired graph uses a new control output prefix. The
original producer, failed rehearsal, receipt and numeric outputs remain as
evidence. A regression test prevents completed-root status rewrites. The graph
also uses the dedicated cold-uncertainty audit for isolated pilots; production
uses the identified chronological audit.

## Reproduction and status

All roots below are under `experiments/cache/`:

- `v20_mixture_rehearsal_2026_10_06`
- `v20_risk_batch_benchmark_2026_10_06_v2`
- `v20_risk_endtoend_benchmark_2026_10_06`
- `v20_risk_cached_probe_2026_10_06`
- `v20_risk_census_pilot_2026_10_06/{2016q1,2026q4}`
- `v20_risk_resume_rehearsal_2026_10_06`
- `v20_pipeline_rehearsal_2026_10_06_v2` and its derived siblings

Logs are in `v20_implementation_2026_10_04/logs/`: `risk_census_<origin>.log`,
`risk_resume_rehearsal.log`, `pipeline_rehearsal_v2.log`,
`downstream_batching_tests_v2.log`, `launcher_commands.log`. The recorded unit
suite passed64tests; separate real-model and full-size inference rehearsals
provide empirical evidence beyond tests.

The final19-stage graph is complete, independent audits pass, and the sealed
[launch readiness](joint_capability_v20_launch_readiness.md) includes the full
remaining-resource forecast and verified commands. Final suite:65tests pass.
No full NN launch; explicit approval remains required.
