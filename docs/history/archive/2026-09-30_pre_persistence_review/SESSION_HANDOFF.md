# Current handoff — v18 role/volume diagnosis complete (2026-09-30)

## Current checkpoint

Adam approved the saved-output diagnosis and separate observed-role library.
Both are complete for all 44 primary quarters. No job remains running. No new
fits, inference, database access, scraping, input rebuild, promotion, deployment
or commit. The completed v18 campaign remains unchanged (1,008 cases / 2,016 fits,
41.188 supervisor hours).

Read the [new diagnosis](reports/v18_role_volume_diagnostic_review.md), then the
[v18 scientific review](reports/joint_capability_v18_codex_review.md) as needed.
The [diagnostic protocol](reports/v18_role_volume_diagnostic_protocol.md) was
frozen before these new calculations; it is exploratory historical analysis.

## Findings and retained decision

- No new scorer selected. Original broad half r² remains J_POINT_BOTH .162915,
  O_ORDER .163049, R_ROUTE .162308; additive_defense .146023. No established
  incremental winner or complete three-pillar pass.
- New library: 20,712 player-quarters, 12,290 supported comparisons, 907 large
  FGA-share changes. Reference share MAE is 4.367 percentage points on large
  changes versus 6.396 for carrying forward prior share; R_ALLOC 4.314.
- On all original cells containing a supported large shot-share changer:
  2,139 cells / 254,582 possessions. Reference half RMSE 11.3217 / r² .18102,
  R_ALLOC 11.3252 / .18051; additive defense 11.4201 / .16671.
- Conversion is the largest absolute point-accounting residual in both factor
  replacement orders. Team FGA/FTA errors offset. Oracle component removal is
  not an attainable gain, and allocation attribution is order-sensitive.
- Mechanism decomposition uses 8,292 joint-label cells / 874,715 possessions,
  not the original 8,345 / 1,013,999 point population. Keep those separate.
- Reference role-change finite-band coverage is 92.80% cell / 93.09% weighted
  at nominal 95%. Retrospective outcome-selected membership is not prospective
  calibration; synthetic latent quality and legal-center coherence remain open.

## Outputs and verification

Under experiments/cache/:

- joint_capability_2026_09_30_v18_role_volume1: all 44 origin calculations
  complete. Final summary failed on duplicate cells keyword; no top-level
  completion. Preserve it and its frozen producer, not a successful full run.
- joint_capability_2026_09_30_v18_role_volume_summary2: successful versioned
  summary-only completion; exact components, player library, role metrics.
- joint_capability_2026_09_30_v18_role_volume_review1: successful independent
  checks and authoritative all-original-cell role point/interval tables; restores
  18 role-change cells without joint labels. Named lineup and player forecasts.

Each prefix has a durable sibling .log. Eight focused tests passed in
joint_capability_2026_09_30_v18_role_volume_tests3.log (final rerun). Independent review checks
82,920 component rows, exact point identities, 44 strict pre-origin histories,
unique player/arm joins and completed receipts. Sources:
experiments/v18_role_volume.py, v18_role_volume_finish.py, v18_role_volume_review.py.
Do not edit frozen completed producers; use fresh versioned outputs for changes.
The original runner retains its summary defect; the finisher reuses its verified
origin outputs without recalculation.

Original v18 root: experiments/cache/joint_capability_2026_09_28_v18_prod;
all automatic siblings are complete/immutable. Prior independent review:
experiments/cache/joint_capability_2026_09_30_v18_codex_review. Its 22 tests,
264 transfer metric checks and 8,118 fixture-margin checks remain valid.

## Next decision

Propose a frozen, bounded conversion-residual persistence study using
game-disjoint splits and opponent/environment sensitivities. Inspect FGA/FTA
jointly, not an isolated FT correction. Then decide whether a targeted dated
role-state/conversion refit is warranted. Do not interpret large realized
shooting residuals as learnable signal or automatically start a v19 sweep.
Refits are acceptable to Adam when justified; none launched or authorized here.
Keep the original transfer cohort separate from the new retrospective library.

## Dirty work and preservation

No commit in this task; last requested commit remains 095183b1. V18 implementation,
plan, previews, reviews, new diagnostics/tests/docs and current navigation remain
uncommitted. Numerous cache directories are untracked: never blanket-stage.

[Displaced handoff](docs/archive/2026-09-30_pre_role_volume_review/SESSION_HANDOFF.md)
and adjacent state/roadmap/navigation snapshots preserve the prior checkpoint.
Original research reports and frozen protocols were not rewritten.
