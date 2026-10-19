# Current research state

As of **2026-09-30**. V18 training, automatic analyses and the
[scientific review](reports/joint_capability_v18_codex_review.md) are complete.
No new primary predictive winner or overall three-pillar pass. Retain the
J_POINT_BOTH research reference; no scorer promotion or active campaign.

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
| R_ALLOC / R_ROUTE | v18 allocation/routing candidates; count/allocation gains, no established incremental primary point gain |
| A_CONTEXT_GATE / A_GATE | v18 compact-context transfer and reliability candidates; descriptive evidence, not selected scorers |
| O_FLOW / O_FLOW_EVENT | Shared-capacity mechanism comparators; no established incremental point win |
| D_SHAPE / O_FLOW_D_SHAPE | Diagnostic evidence; removing defensive volume worsens count/conversion fidelity |
| U1 constant discrepancy | Required uncertainty control; no synthetic-quality validation |
| U2 contextual discrepancy | Earlier research only; no established advantage over U1 |

The NN is profile-based, without known-pair chemistry or player-ID embeddings.
The [existing tool](tool/five.html) still uses its older
[additive-based model](CURRENT_MODEL.md).

## What the completed experiments establish

- v18 confirms useful learned teammate information beyond mechanical accounting:
  A_ACCOUNT worsens counts/location/conversion in all11 seasons, event Holm.03516.
  R_ALLOC improves counts in all11, Holm.03516, but transfer turnover shares and
  team FTA volume remain problematic. Routing alone does not improve transport.
- Primary half r²: A_GATE.162629, R_ROUTE.162308, reference.162915. Checkpoint-half
  R_ROUTE.163469 is descriptive; its same-view reference RMSE interval crosses0.
- Fixed transfer cohort remains146cells/47,419possessions. A_CONTEXT_GATE leads
  descriptively (half RMSE6.6488 vs reference6.6745); no transfer-selected promotion.
- V18 fixes the U0 summary status contract. Reference broad nominal95% coverage
  is93.47% by cell/93.19% weighted, debut90.49% weighted. All eleven candidates
  still favor legal centers against both Jokić fixtures; no solved OOD mean/band.
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

## Current checkpoint and next decision

V18 completed1,008cases/2,016fits in41.188 supervisor hours; no epoch-cap hits.
Original root: experiments/cache/joint_capability_2026_09_28_v18_prod, with
_scored/_average/_basketball/_uncertainty/_role/_summary/_review/_handoff siblings.
Automatic audit verified75,921files and220point metric rows. Separate follow-up
experiments/cache/joint_capability_2026_09_30_v18_codex_review rechecked264transfer
metric rows and8,118fixture margins;22focused tests passed. Original artifacts
and frozen producers are preserved. Implementation and review are uncommitted.

Next proposed work is a bounded role/volume/transport diagnosis using the saved
player exports, followed by a separately agreed and frozen experiment. An expanded
role-change library must distinguish observed retrospective shifts from forecast
inputs, and keep the existing cohort intact. No new run is authorized here.
The [idea bank](V18_IDEAS.md) retains latent ability/policy and cross-team entry
coupling as hypotheses, not mechanisms implemented or validated by v18.

[Pre-v18-review state](docs/archive/2026-09-30_pre_v18_review/JOINT_CAPABILITY_STATE.md)
preserves launch/readiness details; the [implementation handoff](reports/joint_capability_v18_implementation.md)
and [frozen design](JOINT_CAPABILITY_V18_PLAN.md) remain unchanged historical records.

[Previous state](docs/archive/2026-09-28_pre_v17_review/JOINT_CAPABILITY_STATE.md)
preserves the launch checkpoint; frozen plans and original reports are unchanged.
