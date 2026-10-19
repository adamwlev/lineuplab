# Current handoff — v18 reviewed (2026-09-30)

## Current checkpoint

V18 and all automatic stages completed: 1,008 cases / 2,016 fits, 48 origins,
three seeds, 41.188 supervisor hours. Nothing remains running in this campaign.
Adam authorized the scientific follow-up; no new fits, scraping, database access,
cache rebuild, scorer promotion, deployment or commit were performed.

Read the [scientific review](reports/joint_capability_v18_codex_review.md).
The frozen [plan](JOINT_CAPABILITY_V18_PLAN.md) and
[launch handoff](reports/joint_capability_v18_implementation.md) are historical
protocol/operations records, not current pending work.

## Main findings

- Primary half comparison: O_ORDER r² .163049, J_POINT_BOTH .162915,
  A_GATE .162629, R_ROUTE .162308; additive_defense .146023. No established
  incremental point winner. Same 8,345 cells / 1,013,999 possessions.
- Descriptive checkpoint-average-half R_ROUTE .163469 versus reference
  .162989; supplemental season-bootstrap RMSE difference −.003168
  [−.011613, +.005321]. Keep the primary result separate; no post-hoc selection.
- R_ALLOC improves native count loss in all 11 seasons, Holm .03516.
  A_ACCOUNT worsens counts/location/conversion in all 11, Holm .03516 each.
  Learned teammate information contributes beyond accounting, not causal proof.
- Fixed transfer cohort maps exactly: 146 cells / 47,419 possessions.
  A_CONTEXT_GATE half RMSE 6.6488, J_POINT_BOTH 6.6745, R_ROUTE 6.7167.
  Allocator share gains coexist with team-volume error and worse transfer TO shares.
- All eleven models still favor legal centers against both Jokić fixtures.
  A_ACCOUNT makes this worse. No complete coherence pass.
- U0 broad reference coverage 93.47% by cell / 93.19% weighted at nominal 95%.
  Debut weighted coverage 90.49%. U1 close; synthetic latent quality unvalidated.

## Verification and outputs

Original root: experiments/cache/joint_capability_2026_09_28_v18_prod.
Its _scored/_average/_basketball/_uncertainty/_role/_summary/_review/_handoff
siblings are complete and immutable. Automatic audit verified 75,921 files and
220 point metric rows.

Separate follow-up: experiments/cache/joint_capability_2026_09_30_v18_codex_review.
Recomputed all 264 transfer metric rows; checked 8,118 seed-mean fixture margins;
exported all 146 named primary cases per arm, matched benefit/harm tails,
role differences, gate ranges and integration sensitivity.
Log: same review prefix plus .log. Tests: 22 passed; durable log
experiments/cache/joint_capability_2026_09_30_v18_review_tests.log.
Supplemental checkpoint bootstrap method is recorded in the scientific review.

Source: experiments/v18_scientific_review.py. Never rerun it into a completed
prefix. It does not launch inference or training. The read-only
[case preview](docs/V18_CASE_PREVIEW.md) and full report command remain available.

## Next decision

Discuss a bounded role/volume/transport diagnosis using existing per-player
exports, then a separately frozen next experiment if warranted. Preserve the
original transfer cohort; a role-change taxonomy must distinguish retrospective
observed shifts from prospectively available context. Do not automatically
launch a v19 sweep or change the reference based on a descriptive ranking.
Prediction, coherence and uncertainty remain co-equal.

## Dirty work and preservation

No commit in this task. Last requested commit remains 095183b1.
The v18 implementation/plan/notes/tests and new preview/review source/docs remain
uncommitted, along with current navigation edits. Numerous generated cache files
are untracked; never blanket-stage. Frozen producer fingerprints are active.

[Previous handoff](docs/archive/2026-09-30_pre_v18_review/SESSION_HANDOFF.md)
preserves readiness history. The same archive contains the preceding state,
scorecard and roadmap. No original research report or frozen plan was rewritten.
