# Current research state

As of **2026-09-28**. v17 training and all automatic analyses are complete,
and the [independent review](reports/joint_capability_v17_codex_review.md)
has verified results and corrected a derived U0 status-summary defect.
v18 implementation and bounded engineering pilots are complete; the full run is
ready but has not been authorized or launched. No scorer promotion.

The [scorecard](MODEL_SCORECARD.md) owns comparable metrics;
the [roadmap](MODEL_RESEARCH_ROADMAP.md) owns priorities;
the [handoff](SESSION_HANDOFF.md) owns operations and dirty work.

## Retained research models

| Component | Present role |
| --- | --- |
| Additive and additive_defense | Individual-value and equally informed opponent controls |
| Parent_half_defense | Strong earlier contextual comparator |
| J_POINT_BOTH half / checkpoint-average-half | Retained v16 point references; not promoted |
| J_BOTH | Simpler event/mechanism comparator |
| O_ORDER | v17 accounting-order candidate; point performance tied with retained reference |
| O_FLOW / O_FLOW_EVENT | Shared-capacity mechanism comparators; no established incremental point win |
| D_SHAPE / O_FLOW_D_SHAPE | Diagnostic evidence; removing defensive volume worsens count/conversion fidelity |
| U1 constant discrepancy | Required uncertainty control; no synthetic-quality validation |
| U2 contextual discrepancy | Earlier research only; no established advantage over U1 |

The NN is profile-based, without known-pair chemistry or player-ID embeddings.
The [existing tool](tool/five.html) still uses its older
[additive-based model](CURRENT_MODEL.md).

## What the completed experiments establish

- v16 adjusted profiles consistently helped RAW/BOTH comparisons. More attention,
  width, phases and multi-NN ensembles did not establish a compelling advantage.
- v17 is a near-tie in primary prediction: O_ORDER half r².163049 versus
  J_POINT_BOTH.162915, additive_defense.146023, parent_half_defense.156601.
  Same8,345 broad cells /1,013,999 possessions,44 primary quarters.
  O_ORDER versus J_POINT_BOTH RMSE−.000887[−.004135,.002210].
- D_SHAPE count and conversion losses worsen11/11 seasons; point totals alone
  would hide that cost. Flow does not establish an event-wide improvement.
- Flow lowers center offense somewhat but all seven models still favor the
  legal-center fixture against both Jokić fixtures. Two-big observed bias remains
  about+3pts/100. No forced rankings and no complete coherence pass.
- Average-opponent half r²: O_ORDER.148764, J_POINT_BOTH.148368,
  integrated additive_defense.132160. Small new differences, not neutral-opponent
  counterfactual ground truth.
- Corrected broad U0 coverage is about93–94% at nominal95%; U1 proper scores
  are very close. These do not certify hypothetical latent-quality intervals.
- Reliability estimates are noise sensitivities, not theoretical r² ceilings.
  Reused historical seasons are development evidence, not fresh confirmation.

## Artifact and repair status

v16: all3,168 cases /6,336 fits preserved; calibration-column collision and
post-analysis issues were repaired in separate outputs. Independent review
commit3eede4cb; saved-weight follow-up3fb8f1cb.

v17:720 new cases /1,440 fits, all48 origins, three seeds; all downstream stages
complete in25.27 supervisor hours. Plan e9f994ec; implementation eb03b572,
91be8b52 and8949128a. No new fits during independent review.

Original prefix: experiments/cache/joint_capability_2026_09_27_v17_prod,
with _scored/_average/_basketball/_uncertainty/_summary/_handoff siblings.
Independent review prefix:
experiments/cache/joint_capability_2026_09_28_v17_codex_review.

34,923 source files receipt-checked and460 point metric rows independently
reproduced. **U0 summary correction:** the original summary expected OK but
valid per-cell bands are labeled FINITE_GAME_BAND. Use the independent review's
finite_uncertainty_corrected.csv for broad U0. Original all-off5 aggregate
remains invalid; underlying bands, point forecasts and U1 are unaffected.
No completed producer or artifact was changed.

## Current work — v18 implementation

v17 review and earlier literature/ideas are committed as095183b1. Adam approved
direct v18 implementation on2026-09-28, retaining a54-hour total runtime target.
The [frozen design](JOINT_CAPABILITY_V18_PLAN.md) specifies seven new arms,
three seeds and48 origins (1,008cases/2,016fits), plus reused controls. It tests
compact/selective/gated capabilities, learned teammate versus accounting paths,
and action/conversion routing with transfer and uncertainty evaluation.
The [implementation handoff](reports/joint_capability_v18_implementation.md)
records28 passing tests, all seven completed full-epoch pilots,14 original
micro-cases and14 optimized-kernel parity checks. Selected7/9 epochs, no cap hit.
Measured planning estimate45.09h all-in;20% longer training53.52h. Not a guarantee.
54.19GiB additional disk+10GiB reserve versus97.30GiB free. Production root:
experiments/cache/joint_capability_2026_09_28_v18_prod,0/1,008 cases.
No active training process. Next: Adam launches the verified command when ready.
The [idea bank](V18_IDEAS.md) preserves broader deferred directions, including
full latent ability/policy learning and cross-team entry-state coupling.
No full v18 launch, data refresh, commit or deployment is authorized by this page.

[Previous state](docs/archive/2026-09-28_pre_v17_review/JOINT_CAPABILITY_STATE.md)
preserves the launch checkpoint; frozen plans and original reports are unchanged.
