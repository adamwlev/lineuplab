# Current handoff — v19 design ready for discussion (2026-09-30)

## Current checkpoint

Adam requested reflection and a documented v19 plan before implementation.
[JOINT_CAPABILITY_V19_PLAN.md](JOINT_CAPABILITY_V19_PLAN.md) is the proposed
implementation contract. **No v19 code, pilots or full run have been launched.**
No job is running. This task changed documentation only; no fit, inference,
database access, input rebuild, promotion, deployment or commit.

Direct implementation only; no workers. All three standards remain co-equal.
Read the plan before implementing, then freeze its executable protocol and
verified source manifests. Full launch still requires Adam's separate approval.

## Design in brief

- Hypothesis: separate shared game situation from learned lineup capability.
  The fan still supplies players, not score/clock. Integrate complete predicted
  event ledgers over a common strictly historical situation distribution.
- Five arms: C_FIXED (frozen NN + clock opportunities), C_CLOCK (joint learning),
  C_FULL (also location/conversion/capture context), C_ALLOC (clock + existing
  allocator), C_MARGIN (score-margin sensitivity, not default product candidate).
- 720 cases /1,440 inner/final fits,48 origins,3 seeds; original benchmark and
  controls retained. Conditional future-context scores are a separate diagnostic,
  never a replacement for the reference-environment leaderboard.
- First implementation priority: context-label reconciliation and zero-context
  objective/gradient replay. Splitting Poisson rows changes constants unless
  parent constants are preserved; point MSE still pools to game×off5 first.
- Proposed complete-campaign target54h, not a measured estimate. Seven reusable
  pilots plus actual downstream timing precede readiness. Optimize encoder reuse
  across context states; three CPU workers is a measured starting hypothesis.
- No context-profile refit, tracking, shooting-residual sweep, new phase model,
  scorer promotion or automatic claim of solved OOD quality. No runnable v19
  commands exist yet; deliver verified commands at implementation readiness.

## Evidence driving the plan

The [v18 review](reports/joint_capability_v18_codex_review.md),
[role/volume diagnosis](reports/v18_role_volume_diagnostic_review.md) and
[persistence/coupling review](reports/v18_residual_persistence_review.md) are
complete and unchanged. J_POINT_BOTH remains the research reference.

- Broad half r² .162915 vs additive_defense .146023;8,345cells/1,013,999possessions.
- On2,214,552attempts, NN shooting log loss .657272 beats dated player50 .658250;
  previous-quarter residual correction .658115 loses in all11seasons.
- Conversion error repeats weakly: random-game correlation .0367, chronological
  .0188. CLOCK reduces broad FTA bias +1.890→−.025 attempts/100; transfer
  +4.296→+.961. Remaining action-volume error is more persistent.
- Within-origin component covariance diagonals19.235, cross terms−8.703,
  total10.532: do not independently correct FT or add channel noise variances.
- Shared-context diagnostics are observational, not causal deconfounding.
  Legal-center behavior and latent hypothetical uncertainty remain unresolved.

## Completed artifacts and verification

All previous outputs remain under experiments/cache/ with completed receipts:
joint_capability_2026_09_30_v18_persistence1, _persistence_summary1,
_persistence_audit1 and _coupling1 (same date/v18 stem), each with durable logs.
No NN refits were needed for these diagnostics.19focused tests and independent
source/arithmetic audits passed; original frozen scoring configuration verified.
See the persistence review for exact populations, tables and limitations.

The earlier _role_volume1 top-level summary failed; authoritative repaired
summaries are _role_volume_summary2 and _role_volume_review1. Do not rerun the
defective original top-level runner. Original artifacts/producers are frozen.

This planning task verified local Markdown targets and whitespace and preserved
snapshots of the displaced current pages. The archived roadmap's historical body
matches the current body exactly. No model tests were rerun because no model code
changed; no new numerical results are claimed.

## Next action and dirty work

Discuss/approve the v19 design, then implement §9 in order. Begin with source,
teacher and context-label audits; do not start training while those are unresolved.
After pilots provide verified launch/live-log/status/report/preview commands,
including measured runtime and disk projections. Await full-run authorization.

No commit. Last requested commit remains095183b1. V18 implementation, reviews,
diagnostic sources/tests and current documentation are still uncommitted, along
with this plan. Numerous cache directories are untracked: never blanket-stage.
Preserve all pre-existing changes and completed producer fingerprints.

[Displaced checkpoint](docs/archive/2026-09-30_pre_v19_plan/SESSION_HANDOFF.md)
and adjacent state/roadmap/navigation/README snapshots preserve the exact previous
documentation. Original reports and frozen experiment plans were not rewritten.
