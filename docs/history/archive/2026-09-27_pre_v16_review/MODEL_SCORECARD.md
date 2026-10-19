# Current model scorecard

Updated **2026-09-18** from the completed
[v15 independent review](reports/joint_capability_v15_codex_review.md).
Research candidates only; **no scorer promotion and no overall three-pillar
product pass**. Old tables are in the [dated history](#historical-tables), not
mixed into the current winner list.

**v16 warning, 2026-09-26:** all 3,168 training cases are verified complete, but a confirmed
player-ID/prediction column collision corrupts NN calibration histories.
Current v16 calibrated leaderboards/previews and dependent comparisons require
regeneration; do not use their rankings for model selection. End-of-run event
reporting also stopped on the archived `rebound`/`recovery` naming mismatch;
full analysis and final audit are incomplete. Native fits are
reusable. Adam approved finishing training unchanged, then repairing into new
derived outputs while preserving originals. See the [handoff](SESSION_HANDOFF.md)
and [P0 repair checklist](MODEL_RESEARCH_ROADMAP.md#post-v16-calibration-history-repair-first).
The completed v15 table below is unchanged; all three standards remain equal.

The versioned repair has completed all 48 corrected scoring origins and full
point validation in `...2026_09_26_v16_repaired`. The exhaustive diagnostics
were stopped by Adam after their runtime was estimated at nine more days.
A separate bounded analysis amendment is being verified; it reuses corrected
point outputs unchanged. Independent full prediction audit and final three-pillar
review remain pending; see the [handoff](SESSION_HANDOFF.md). Repaired
native event analysis is complete: J_BOTH versus J_RAW count NLL delta −.000363
[−.000461,−.000273], 11/11 season wins, Holm p=.033203 across 34 registered
comparisons. This event result is independent of point calibration and is not
a point-ranking or three-pillar acceptance claim.

## What these numbers measure

- Forward offensive-lineup-quarter outcomes: **44 quarters, 2016–2026**;
  2015 is calibration warmup. Neural forecasts are averaged over seeds
  17/23/41 before scoring.
- Fixed historical matched cohort: **5,607 cells / 726,364 possessions**.
  It inherits the earlier profile-support intersection. “All” below is this
  cohort, not all possessions or every >=50-possession lineup.
- Possession-weighted pooled MAE/RMSE in points per 100; raw
  `r² = 1 − weighted SSE / weighted SST`, not squared correlation or the mean
  of quarterly r². Novel = an offensive five not previously observed, not
  necessarily five new players or a new ten-player matchup.
- Opponent-aware rows condition on the **actual opposing fives encountered**,
  using prior-only states/calibration. Opponent-blind rows are orientation
  controls, not equal-information tests of the defensive adapter.

Let A = corrected additive offense; N = v14 `RB_RENEW_FAC`;
D = shared prior-centered additive defense (positive means easier defense);
P = the specified v15 adapter's calibrated forecast.
Old HALF+D = `.5(A+N)+D`; new half = `.5(A+D+P)`.
N and A retain their prior offensive calibration when D is added; P has its
own prior-only calibration. That asymmetry matters below.

## Current matched point comparisons

| Forecast | Actual opponents? | RMSE | MAE | Raw r² | Correlation |
| --- | --- | ---: | ---: | ---: | ---: |
| Additive A | No | 10.84099 | 8.09195 | .12043 | .35326 |
| Frozen NN N | No | 10.80733 | 8.06304 | .12589 | .35866 |
| Old HALF | No | 10.78462 | 8.03744 | .12956 | .36319 |
| A+D | Yes | 10.78699 | 8.06608 | .12917 | .36993 |
| N+D | Yes | 10.75679 | 8.05367 | .13404 | .37326 |
| Old HALF+D | Yes | 10.73215 | 8.01862 | .13801 | .37881 |
| D_MAIN direct | Yes | 10.78361 | 8.05035 | .12972 | .36328 |
| D_CROSS direct | Yes | 10.79839 | 8.05969 | .12733 | .36004 |
| D_MAIN_RB direct | Yes | 10.78017 | 8.05261 | .13028 | .36395 |
| D_CROSS_RB direct | Yes | 10.80348 | 8.06541 | .12651 | .35853 |
| D_MAIN half | Yes | 10.72777 | 8.00180 | .13871 | .37664 |
| D_CROSS half | Yes | 10.72990 | 8.00230 | .13837 | .37603 |
| D_MAIN_RB half | Yes | 10.72573 | 8.00072 | .13904 | .37688 |
| D_CROSS_RB half | Yes | 10.73086 | 8.00300 | .13821 | .37528 |

D_MAIN_RB half has the smallest observed primary RMSE/MAE, but its RMSE
difference versus old HALF+D is **−.00642, 95% season-block interval
[−.04077, +.02369], 4/11 season wins**. The incremental advantage is not
established. All four direct adapters trail N+D on pooled RMSE.

94.2% of the small half-blend MSE improvement is the quarter-bias component.
A **post-hoc sensitivity**, giving all saved forecasts an additional common
prior-only affine calibration, reverses the ranking: old HALF+D 10.71303 versus
D_MAIN_RB half 10.72143 RMSE. Those are not replacements for the registered
table or proof of a new winner. Repeated historical comparisons and observed
best-arm selection also limit confirmatory claims.

## Novel and recurring lineups

Novel: **2,073 cells / 226,256 possessions**.
Recurring: **3,534 / 500,108**. Same cutoffs/weighting as above.

| Forecast | Novel RMSE | Novel MAE | Recurring RMSE |
| --- | ---: | ---: | ---: |
| A | 11.85302 | 8.90390 | 10.35068 |
| A+D | 11.77930 | 8.86462 | 10.30671 |
| N+D | 11.68172 | 8.78505 | 10.31112 |
| Old HALF+D | 11.68922 | 8.77171 | 10.26990 |
| D_MAIN_RB direct | 11.75231 | 8.82379 | 10.31028 |
| D_MAIN_RB half | 11.70240 | 8.76357 | 10.25336 |

N+D leads novel RMSE; new half's slightly better novel MAE is not an
across-the-board novel advance. Retain both conclusions.

## Separate broader-population sensitivity

These rows are **not comparable in level to the main table**. Full population
construction and other aggregations are in the
[v15 review](reports/joint_capability_v15_codex_review.md).

| Population | Cells / possessions | A+D RMSE | N+D RMSE | Old HALF+D RMSE | MAIN_RB half RMSE |
| --- | --- | ---: | ---: | ---: | ---: |
| All offensive fives >=50 possessions | 8,345 / 1,013,999 | 11.17892 | 11.11455 | 11.10511 | 11.10966 |
| All matchup rows | 718,526 / 2,760,546 | 59.69766 | 59.68725 | 59.68385 | 59.68544 |

Many matchup rows have very small exposure, hence large outcome noise.
The historical restricted primary is retained for comparison, not endorsed as
a future coverage gate.

## Basketball and uncertainty have equal standing

| Standard | Evidence | Still unresolved |
| --- | --- | --- |
| Forward prediction | Opponent information helps; CROSS improves count/location/conversion losses and RB improves rebound loss in 11/11 seasons | New adapter's point increment over fair controls is uncertain and calibration-sensitive |
| Basketball coherence | Opponent strength/recovery responses are useful; native primary FTA bias falls from +2.539 to +1.749 per 100 with MAIN_RB | Five-center offense remains too generous; CROSS can worsen it; observational profiles are not causal attribution |
| Honest uncertainty | MAIN_RB half possession-weighted finite-outcome coverage: 79.88% at nominal 80%, 94.19% at 95% | Not latent-quality or arbitrary-lineup OOD validation; opponent integration at 128 versus 256 references can move some ratings about 1 point/100 |

The free-throw result is **not a global overprediction**: near-zero all-row
bias conceals cohort/deployment differences. See the
[situation diagnostic](reports/game_situation_diagnostic_review.md).
No blanket FT correction, forced fixture ranking or coverage gate follows.

## Historical tables

All original reports remain at their original paths. Their populations,
targets, calibrations and information sets must be checked before comparisons.

| Dated record | Scope |
| --- | --- |
| [Pre-cleanup scorecard, preserved 2026-09-18](docs/archive/2026-09-18_pre_cleanup/MODEL_SCORECARD.md) | Earlier tables and successive updates; former “best” labels are historical |
| [v14 review, 2026-09-17](reports/joint_capability_v14_codex_review.md) | Offense-only campaign, three seeds, same historical primary |
| [Transfer review, 2026-09-17](reports/transfer_role_benchmark_review.md) | Separate substantial q1 team-change cohort: 146 cells / 47,419 possessions |
| [v13 review, 2026-09-15](reports/joint_capability_v13_codex_review.md) | Same historical primary, but leading ROLE design lacks the later three-seed replication |
| [v12 partial review, 2026-09-14](reports/joint_capability_v12_partial_codex_review.md) | Partial run, 33/44 primary quarters; not a completed-campaign leaderboard |
| [v10 independent review, 2026-09-13](reports/joint_capability_v10_codex_review.md) | Earlier V9_SPREAD/half benchmark |
| [v5–v9 synthesis, 2026-09-12](reports/joint_capability_v5_v9_codex_review.md) | Older neural evidence and qualifications of ceiling/power claims |
| [Corrected additive reference](ASOF_ADDITIVE_REFERENCE_RESULTS.md) | Corrected quarterly baseline; distinct from legacy possession-level Δr² |

For reproduction use the [verified read-only commands](JOINT_CAPABILITY_STATE.md#operations).
For next steps use the [backlog](MODEL_RESEARCH_ROADMAP.md), not historical
“next experiment” paragraphs.
