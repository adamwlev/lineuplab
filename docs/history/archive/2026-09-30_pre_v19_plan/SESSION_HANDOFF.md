# Current handoff — v18 persistence diagnostics complete (2026-09-30)

## Current checkpoint

Adam authorized further diagnostics to understand the errors and inform direction.
The frozen persistence study and separately frozen, result-motivated coupling
supplement are complete. No job remains running. No NN/additive training, new
inference, database access, scraping, input rebuild, promotion, deployment or commit.

Read the [combined review](reports/v18_residual_persistence_review.md).
The preceding [role/volume diagnosis](reports/v18_role_volume_diagnostic_review.md)
and [v18 scientific review](reports/joint_capability_v18_codex_review.md) remain
unchanged evidence. All three product standards remain co-equal.

## Main findings

- Conditional shooting tests cover 2,214,552 actual attempts. Reference NN log
  loss .657272 beats dated player50 .658250 in all11 seasons. Fixed prior-quarter
  residual correction worsens loss to .658115, losing all11 seasons for all4NNs.
  This rejects the tested correction, not every adaptive state model.
- Reference conversion residual correlation is .0367 across random game halves
  and .0188 chronologically; the latter interval includes zero. Large realized
  conversion error is not demonstrated learnable signal.
- CLOCK reduces broad FTA bias +1.890→−.025 attempts/100; transfer +4.296→+.961.
  FGA bias improves simultaneously. Remaining action-volume persistence survives
  CLOCK and the limited opponent-balance sensitivity.
- Broad joint-label half point RMSE11.776 vs additive defense11.874; CLOCK11.713
  vs11.810. Relative advantage survives. Conditional adjusted-target scores are
  not new forecast leaderboard results.
- Within-origin persistent component covariances sum to19.235; cross-component
  offsets−8.703 leave10.532 total point covariance. Most offset is between other
  FG and other FT error. Do not independently correct FT or sum diagonal noise.
- All650chronological high-support cases per arm are exported. Denver2025q4
  Westbrook/Gordon/Jokić/Murray/Braun has large FTA underprediction in both halves;
  global FTA overprediction is not universal. Named tails are exploratory.
- Legal-center coherence and latent synthetic uncertainty are still unresolved.
  No new coverage/promotion claim; retain J_POINT_BOTH research reference.

## Populations and artifacts

Original broad point population8,345cells/1,013,999possessions was reconciled
against all saved direct/half predictions. Joint-label diagnostic population is
8,292/874,715. Random game splits retain4,235cells/618,044possessions on average;
chronology5,283/708,378. Support selection is disclosed, never a product gate.

Under experiments/cache/, all four new prefixes have completed receipts and
durable sibling .log files:

- joint_capability_2026_09_30_v18_persistence1:44origin game residuals, context
  offsets, shooting controls, probability scores, player records and cutoff audits.
- joint_capability_2026_09_30_v18_persistence_summary1: all tables, six game-split
  pair exports, season moments/bootstrap intervals, environment comparisons.
- joint_capability_2026_09_30_v18_persistence_audit1: independent PASS.
- joint_capability_2026_09_30_v18_coupling1: channel matrices and2,600named arm/cell
  cases with all650reference cases and two descriptive top20 lists.

Source modules: experiments/v18_residual_persistence.py,
experiments/v18_persistence_summary.py, experiments/v18_persistence_audit.py,
experiments/v18_residual_coupling.py. Completed producer hashes are frozen.
Protocols: reports/v18_residual_persistence_protocol.md and
reports/v18_residual_coupling_protocol.md. Do not edit completed sources/outputs.

19tests pass: experiments/cache/v18_residual_persistence_tests4.log.
Full synthetic summary smoke passes in v18_residual_persistence_summary_smoke2.log.
The first synthetic test demanded a correlation for constant errors; its failed
assertion is preserved, not a production failure. Detached launches were terminated
by the execution environment before starting; managed sessions completed all stages.
No real-data stage failed. Original frozen scoring configuration still verifies.

Prior role-volume outputs remain valid. The original _role_volume1 top summary
failed on duplicate cells; use _role_volume_summary2 and authoritative
_role_volume_review1 all-original-cell tables. Do not rerun the defective original
top-level runner. Prior source/history is in the archived handoff below.

## Next decision

We have enough evidence to design a focused experiment, not another generic sweep:

1. Shared game-context nuisance during fitting, integrated over an explicitly
   prior-only reference environment at inference; no clock/score inputs for fans.
2. Joint opportunity/count modeling with coherent FGA/FTA/TO and point accounting,
   compared with retained controls. Do not simply retry phase/routing without a
   distinct hypothesis or subtract flat FT corrections.
3. Preserve the useful conversion estimator as a control; no recent-shooting
   residual chase based on the large future-outcome oracle.
4. Keep game-level noise, persistent channel covariance, mechanism coherence and
   latent uncertainty distinct. No observed-only synthetic calibration claims.

A separate frozen training plan and launch authority are still required. Adam
accepts justified refits; none was launched by this task.

## Dirty work and preservation

No commit; last requested commit remains095183b1. V18 implementation, plans,
previews/reviews, role/persistence/coupling code/tests/docs and navigation remain
uncommitted. Numerous cache directories are untracked: never blanket-stage.

[Displaced handoff](docs/archive/2026-09-30_pre_persistence_review/SESSION_HANDOFF.md)
and adjacent state/roadmap/navigation snapshots preserve the previous checkpoint.
Original research reports and frozen protocols were not rewritten.
