# Current model scorecard

Updated **2026-09-30** with the completed
[v18 scientific review](reports/joint_capability_v18_codex_review.md), alongside the
[v17 independent review](reports/joint_capability_v17_codex_review.md), repaired
[v16 independent review](reports/joint_capability_v16_codex_review.md) and
[point-candidate follow-up](reports/joint_capability_v16_point_followup_review.md).
Research candidates only: **no scorer promotion or overall three-pillar pass**.
The old uncorrected v16 rankings are invalid; use corrected outputs below.
[Previous scorecard](docs/archive/2026-09-27_pre_v16_review/MODEL_SCORECARD.md)
preserves v15 and earlier tables, populations and calibration conventions.

## What the current numbers measure

Possession-weighted offensive-lineup-quarter outcomes over **44 quarters,
2016–2026**, with 2015 warmup. Three seeds are averaged before scoring.
Broad population: **8,345 cells / 1,013,999 possessions**, every offensive five
with >=50 possessions in its evaluation quarter. “All” is this cohort, not
every possession. Ratings condition on the actual defensive lineups faced.
RMSE/MAE/bias are points per100; r² is weighted1−SSE/SST, not squared correlation.

All controls receive the v16 common prior-only calibration. Half means50/50
calibrated NN and additive_defense. Checkpoint averaging averages predictions.

## v18 broad comparison

All1,008cases/2,016fits and analyses complete. Same population and calibration
as below. Primary half has no established new incremental winner; original
registered23point/36event contrast families remain unchanged.

| Arm | Direct r² | Half r² | Half RMSE | Half MAE |
| --- | ---: | ---: | ---: | ---: |
| O_ORDER | .162077 | .163049 | 11.054064 | 8.297513 |
| J_POINT_BOTH | .161925 | .162915 | 11.054951 | 8.299892 |
| A_GATE | .161247 | .162629 | 11.056837 | 8.301255 |
| R_ROUTE | .159578 | .162308 | 11.058958 | 8.297882 |
| R_ALLOC | .160241 | .162136 | 11.060093 | 8.299963 |
| A_CONTEXT_GATE | .160636 | .161385 | 11.065046 | 8.318314 |
| A_CONTEXT | .160827 | .161092 | 11.066981 | 8.320469 |
| A_ACCOUNT | .152988 | .159740 | 11.075896 | 8.317255 |
| A_SELECT | .153629 | .158480 | 11.084199 | 8.336107 |

Checkpoint-average-half is descriptive: R_ROUTE r².163469/RMSE11.051291,
R_ALLOC.163316/11.052301, J_POINT_BOTH.162989/11.054459. Supplemental
same-view R_ROUTE RMSE difference−.003168[−.011613,+.005321]; not a registered
winner or grounds for promotion. Primary A_GATE versus reference+.001887
[−.002891,+.007627]. All seven new half arms beat additive_defense after the
registered family correction; intended incremental mechanism gains do not.

Event counts improve for R_ALLOC in11/11 seasons (Holm.03516). Accounting-only
A_ACCOUNT worsens counts/location/conversion11/11 (Holm.03516 each), supporting
useful learned teammate information but not causal attribution.
Fixed transfer cohort146cells/47,419possessions: half RMSE A_CONTEXT_GATE6.6488,
reference6.6745, R_ROUTE6.7167, additive_defense6.9473; descriptive, different
population from the broad table. No general role-transport victory.

All eleven models still favor legal centers against both Jokić fixtures. Broad
reference half nominal95% coverage93.47% cell/93.19% weighted, debut90.49%
weighted. Correct U0 status handling is verified in both broad and all-off5;
synthetic latent uncertainty remains unvalidated. See the review for all three
standards, average-mode results, source paths and uncertainty qualifications.

## v17 broad comparison — historical campaign

Same population and calibration conventions below. Primary view is half;
checkpoint comparisons are descriptive. Retain the v16 reference, no promotion.

| Arm | Direct r² | Half r² | Half RMSE | Half MAE |
| --- | ---: | ---: | ---: | ---: |
| O_ORDER | .162077 | .163049 | 11.054064 | 8.297513 |
| O_FLOW | .161042 | .162637 | 11.056783 | 8.300601 |
| D_SHAPE | .161258 | .162669 | 11.056576 | 8.301090 |
| O_FLOW_D_SHAPE | .161674 | .162923 | 11.054898 | 8.299261 |
| O_FLOW_EVENT | .154608 | .158784 | 11.082190 | 8.342255 |
| J_POINT_BOTH | .161925 | .162915 | 11.054951 | 8.299892 |

O_ORDER−J_POINT_BOTH half RMSE−.000887[−.004135,.002210],8/11 season wins,
Holm1.0 in the registered16-contrast family. All new arms beat additive_defense
after correction, but none establishes its intended incremental mechanism gain.
D_SHAPE checkpoint-half r².163188 is a tiny descriptive edge, not a new selected
champion. D_SHAPE worsens counts and conversion in11/11 seasons.

Flow reduces center offense somewhat, but all seven current arms favor the legal
center fixture over both Jokić fixtures. Average-opponent half r²: O_ORDER.148764
versus retained point-half.148368. No new uncertainty breakthrough.

**U0 reporting correction:** original v17 summary rejected valid
FINITE_GAME_BAND rows by checking for OK. Training, point scores and saved bands
are unaffected. Corrected broad point-half nominal95% coverage is93.47% by cell /
93.19% by possession; O_ORDER93.59% /93.20%. Use
`experiments/cache/joint_capability_2026_09_28_v17_codex_review/finite_uncertainty_corrected.csv`.
Original all-off5 aggregate U0 remains invalid; raw bands and U1 are valid.

## Retained v16 broad point comparisons

| Forecast | RMSE | MAE | r² | Correlation |
| --- | ---: | ---: | ---: | ---: |
| Additive offense only | 11.251737 | 8.458718 | .132848 | .365625 |
| Additive_defense | 11.165936 | 8.412297 | .146023 | .382625 |
| Parent_half_defense | 11.096562 | 8.354524 | .156601 | .396307 |
| J_POINT_BOTH direct | 11.061484 | 8.301836 | .161925 | .402800 |
| J_POINT_BOTH direct-half | 11.054951 | **8.299892** | .162915 | **.403882** |
| J_POINT_BOTH checkpoint-average-half | **11.054459** | 8.306363 | **.162989** | .403778 |
| Forward top-three checkpoint-average + additive | 11.065234 | 8.323669 | .161357 | .401709 |
| Forward nonnegative stack | 11.068186 | 8.323311 | .160909 | .401145 |

The forward top-one checkpoint selector chooses J_POINT_BOTH in all44 primary
quarters, exactly reproducing its half blend. More NN members did not improve
on that candidate in this bounded ensemble experiment.

Against additive_defense, that selector's RMSE difference is−.111477
[−.143084,−.079772],11/11 seasons, supplemental-family Holm p=.017578.
Against the stronger parent blend:−.042103 [−.068045,−.019442],10/11,
Holm p=.061523. The original larger arm-comparison family is more conservative;
do not equate this supplemental result with confirmation of every architecture
claim. Repeated historical development is not a fresh confirmatory holdout.

## Novel and legacy populations

Novel offensive fives: **3,489 cells /361,361 possessions**.

| Forecast | Novel RMSE | Novel r² |
| --- | ---: | ---: |
| Additive_defense | 12.238726 | .118400 |
| Parent_half_defense | 12.125765 | .134599 |
| J_POINT_BOTH checkpoint-average-half | 12.056185 | .144502 |

Legacy co-primary: **5,607 cells /726,364 possessions**. Additive_defense
r².133998; parent_half_defense.141776; J_POINT_BOTH direct-half.147307;
checkpoint-average-half.146601. Do not compare these levels with the broad
population or pre-v16 calibration.

## The other two standards and product mode

**Basketball coherence:** all22 direct NN arms favor the five-pure-centers
fixture over Jokić/Murray/Gordon/Porter/Westbrook. The leading checkpoint-half
gives the centers+4.810 points/100; additive itself gives+6.345. This is a shared
matchup extrapolation concern, not a named ranking to force. Korver's positive
relative-to-additive residual is encouraging but its mixed-era profile-bank
transport remains incomplete. J_POINT_BOTH improves point prediction while
worsening count NLL against J_BOTH in11/11 seasons (Holm p=.033203).

**Uncertainty:** the earlier ensemble-specific95% finite-quarter bands cover
93.86% overall and93.31% novel on the broad cohort. The completed candidate
U0 analysis uses all prior offensive-five cells as its calibration history:
on the same broad evaluation cohort, point-half/checkpoint-half possession-
weighted coverage is93.19%/93.27%, novel92.72%/92.67%. These are distinct
interval constructions, not conflicting point forecasts. The generic U0
headline96.07% includes220,381 mostly tiny cells and must not stand in for
the broad-cohort result.

Candidate U1/U2 evaluation is now complete. U2's joint log score is slightly
worse in5/6 candidate/split comparisons (versus9/9 in the original fixed set).
Balanced-date finite-half U1 coverage is94.21%/94.16% on2,037 identified pairs.
Synthetic candidate discrepancy bands remain deferred; none of this validates
arbitrary-lineup latent-quality coverage.

## Average-opponent product mode — completed candidate follow-up

Same8,345 broad cells /1,013,999possessions and44 primary quarters; three-seed
means. Forecasts integrate an origin-prior opponent reference, while outcomes
remain actual realized ratings. This measures prediction without knowing the
future defensive schedule, not observed neutral-opponent ground truth.

| Forecast | RMSE | MAE | r² | Novel r² |
| --- | ---: | ---: | ---: | ---: |
| Integrated additive_defense | 11.256199 | 8.467372 | .132160 | .100727 |
| D_MAIN_RB half | 11.199898 | 8.418045 | .140820 | .113320 |
| J_BOTH half | 11.184958 | 8.414269 | .143111 | .121428 |
| J_ALL_BOTH half | 11.180574 | 8.409198 | .143782 | .121457 |
| J_POINT_BOTH direct | 11.155727 | 8.376836 | .147584 | **.132922** |
| J_POINT_BOTH half | **11.150592** | **8.367238** | **.148368** | .127071 |
| J_POINT_BOTH checkpoint-average | 11.181726 | 8.416647 | .143606 | .130579 |
| J_POINT_BOTH checkpoint-average-half | 11.159892 | 8.381667 | .146947 | .126688 |

Half minus integrated-additive RMSE−.105608 [−.139443,−.074331],11/11seasons,
12-comparison Holm p=.011719. Versus J_BOTH-half−.034367
[−.058237,−.010864],8/11,Holm p=.164062: smaller contextual-control gains are
not established by the corrected family. No retrospective view/cohort selector.

512-opponent estimates are approximate. On880 fixed primary sensitivity cells,
half prediction differences versus4096 reach.1463pts/100; mean.0504. The
half-minus-J_BOTH RMSE difference is−.03266/−.03267 at512/4096 on that subset.
This supports stable sampled contrasts, not exact convergence for every cell.

**Original fixture numerical audit:** all64 exact-reference comparisons pass; maximum native
error at16,384 references.010976 points/100. No numerical issue explains away
the current coherence findings.

## Sources and reproduction

Completed source:
`experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.
Independent read-only review tables:
`experiments/cache/joint_capability_2026_09_27_v16_codex_review`.
All201 supplemental scorecard rows independently reconstructed from saved cells.

Completed candidate product-mode source:
`experiments/cache/joint_capability_2026_09_27_v16_point_followup`.
Independent follow-up review:
`experiments/cache/joint_capability_2026_09_27_v16_point_review`:
40 average metrics and60 persistent summaries verified;248 source files unchanged.

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_repair report --sort r2 --slice all --view half
```

The full [review](reports/joint_capability_v16_codex_review.md) covers architecture,
events, transfer cases, error decomposition, reliability sensitivity and the
recommended next work. The [backlog](MODEL_RESEARCH_ROADMAP.md) owns priorities.

## Historical tables

Exact pre-review scorecard:
[2026-09-27 archive](docs/archive/2026-09-27_pre_v16_review/MODEL_SCORECARD.md).
Original v15/v14 and earlier protocols/reports remain unchanged.
