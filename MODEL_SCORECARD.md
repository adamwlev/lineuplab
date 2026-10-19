# Current model scorecard

Updated **2026-10-19** with the refresh on the clean data (first section); **2026-10-14** with the learned combinations; **2026-10-13** with the combination layer; **2026-10-12** with the release forecast (below). Earlier tables: updated 2026-10-09 with the completed
[v20 scientific review](reports/joint_capability_v20_scientific_review.md), alongside the
[v19 scientific review](reports/joint_capability_v19_review.md),
[v18 scientific review](reports/joint_capability_v18_codex_review.md),
[v17 independent review](reports/joint_capability_v17_codex_review.md), repaired
[v16 independent review](reports/joint_capability_v16_codex_review.md) and
[point-candidate follow-up](reports/joint_capability_v16_point_followup_review.md).
Research candidates only: **no scorer promotion or overall three-pillar pass**.
The old uncorrected v16 rankings are invalid; use corrected outputs below.
[Previous scorecard](docs/history/archive/2026-09-27_pre_v16_review/MODEL_SCORECARD.md)
preserves v15 and earlier tables, populations and calibration conventions.

## The refresh on the clean data (2026-10-19)

The tool now shows the release with every number refitted on the clean data
([results](reports/refresh_results_2026_10_19.md)). These numbers replace the
earlier-data ones below for the tool; the tables below stay as the record of
the earlier data.

| Measure (population) | Clean data | Earlier data |
| --- | ---: | ---: |
| Calibrated network R, raw r² (lineup quarters, 44 quarters 2016–26) | .1594 | .1615 |
| Same, centered within quarter | .0988 | .1012 |
| Learned module, half strength, previous-centered (24 quarters 2016–21) | +0.0006 (0.0010) | +0.0010 |
| Measured layer, forward (2022–26 game-level pairs) | +0.00001 | +0.00003 |
| Measured combinations held up | 12 | 14 |
| τ² offense / defense / net | 10.43 / 10.04 / 19.80 | 10.25 / 10.45 / 19.83 |

Clean and earlier data differ in their outcomes too, so the first rows are
not a like-for-like comparison.

## Release forecast (Adam, 2026-10-12)

*Note, 2026-10-16:* the tool now shows the release retrained on the possession
table rebuilt from the pages, with exact player ids
([release](reports/clean_release_2026_10_16.md),
[findings](reports/rescrape_pilot_2026_10_14.md)). Every number below was
measured with fits trained on the old data. The retrained release carried the
old calibration until the refresh of 2026-10-19 (first section), which
re-scored it on the clean data. On 120 real 2025–26 fives its
margins correlate 0.994 with the old release's (SD of the change 0.56 points
per 100).

The tool shows the **calibrated network alone**: reference architecture, the
2027q1 fits retrained on the clean data (the frozen record's fits are kept
for the prospective test), three seeds of five checkpoints each (`lineups/release.py`).
The additive half is dropped. The printed trade, on the population below:

| Forecast | Raw r² | Centered r² (within quarter) |
| --- | ---: | ---: |
| J_POINT_BOTH checkpoint-average-half (the previous reference view) | .1630 | — |
| Calibrated network alone (the release) | .1615 | .1012 |
| Difference | −0.0015 | −0.0006 |

The centered figure is per quarter (post hoc,
[addendum](reports/capacity_confirmatory_results_2026_10_12.md)). In exchange,
the tool drops the additive model, which is linear in copies of a player.

**Combination layer (Adam, 2026-10-13).** The forecast adds the measured
combination effects ([results](reports/combination_layer_results_2026_10_13.md)).
Forward check: fitted on 2016–2021 and applied to 2022–2026 game × offense
five × defense five rows (possession-weighted; not the lineup-quarter
population above).

| Forecast | Raw r² | Centered r² |
| --- | ---: | ---: |
| Calibrated network alone | .00746 | .00739 |
| Network + combination layer | .00749 | .00743 |
| Difference | +0.00003 | +0.00004 |

**Learned combinations (Adam, 2026-10-14).** The forecast adds half the
centered learned module, and the layer above is re-measured on top of it
([confirmation](reports/learned_module_confirmation_results_2026_10_14.md),
[release](reports/learned_module_release_2026_10_14.md)). The population is
lineup-quarter broad cells (≥ 50 possessions), per-quarter r² around the
quarter's mean. Each forecast is calibrated forward on its own earlier
quarters, with seeds 17, 23 and 41 averaged. This is not the scorecard's
pooled population below.

| Module at half strength, centered | r² minus the network alone (SE over quarters) |
| --- | ---: |
| 2016–2021, 24 fresh quarters (confirmatory) | +0.0010 (0.0008) |
| 2023–2026, 16 quarters (exploratory; the design was chosen here) | −0.0007 (0.0012) |

The re-measured layer on top of network + module, checked forward as above:
+0.00003 raw r².

The alternative assumption in the band, capacity defense, scores
−0.0024 ± 0.0008 centered on 2016–2026 and −0.0027 ± 0.0014 in the
2007–2013 era ([report](reports/era_backtest_results_2026_10_12.md)).

## What the current numbers measure

Possession-weighted offensive-lineup-quarter outcomes over **44 quarters,
2016–2026**, with 2015 warmup. Three seeds are averaged before scoring.
Broad population: **8,345 cells / 1,013,999 possessions**, every offensive five
with >=50 possessions in its evaluation quarter. “All” is this cohort, not
every possession. Ratings condition on the actual defensive lineups faced.
RMSE/MAE/bias are points per100; r² is weighted1−SSE/SST, not squared correlation.

All controls receive the v16 common prior-only calibration. Half means50/50
calibrated NN and additive_defense. Checkpoint averaging averages predictions.

## v20 broad comparison — latest completed campaign

Primary is now predeclared **checkpoint-average-half**. Same44quarters,
8,345cells/1,013,999possessions as above. No incremental primary point winner.

| Arm | Primary r² | RMSE | MAE | Novel r² |
| --- | ---: | ---: | ---: | ---: |
| P_BASE / J_POINT_BOTH | .162989 | 11.054459 | 8.306363 | .144502 |
| S_BASE | .162149 | 11.060008 | 8.313903 | .143162 |
| P_ADJ | .161838 | 11.062056 | 8.313572 | .142703 |
| P_CONTEXT / C_FULL | .161724 | 11.062813 | 8.309150 | .142634 |
| S_ADJ | .161168 | 11.066479 | 8.320464 | .141493 |
| P_BOTH | .161102 | 11.066916 | 8.313000 | .141687 |
| S_CONTEXT | .160585 | 11.070326 | 8.316551 | .141150 |
| S_BOTH | .159906 | 11.074802 | 8.322819 | .140454 |
| additive_defense | .146023 | 11.165936 | 8.412297 | .118400 |

Novel=3,489cells/361,361possessions. New arms also trail reference on original
transfer/role-change RMSE. P_ADJ−P_BASE RMSE+.007597[−.001066,+.020272],
S_BASE−P_BASE+.005549[−.005019,+.016428]; Holm p=1for both. Three of six new
arms pass the17-test correction against additive_defense; none proves an
incremental point gain. Extra retained R_ALLOC checkpoint-half .163316 is a
descriptive near-tie, not a new selected winner.

14/44conditional event tests pass:11decoder-context and3S5count gains, none
from profile adjustment. All8arms still favor legal centers (+4.72to+6.23blend
margin against two Jokić fixtures), with problematic FTA/renewal. Four new
uncertainty contrasts are null; P_BASE nominal95 U0 coverage93.64%cell/93.27%weighted.
The risk slice has8primarycells, only4supported: underpowered. No three-pillar pass.

Average-opponent reference primary r².146947 vs integrated additive.132160.
Full-calendar P_BASE pureNN checkpoint-average r².161482, below blended .162989;
the partial-run pureNN lead did not persist. See the review for hypotheses,
denominators, uncertainty, independent192-row verification and reproduction.

## v19 broad comparison — historical campaign

All720cases and all analyses complete. Same primary population as above.
Reference integrates nonlinear events over a past-only common context; actual
future context is not an input to this table. No new incremental point winner.

| Arm | Direct r² | Half r² | Checkpoint-average-half r² | Half RMSE | Half MAE |
| --- | ---: | ---: | ---: | ---: | ---: |
| J_POINT_BOTH | .161925 | .162915 | .162989 | 11.054951 | 8.299892 |
| C_FIXED | .161930 | .162937 | .162939 | 11.054805 | 8.299948 |
| C_CLOCK | .154525 | .159471 | .161697 | 11.077670 | 8.317380 |
| C_FULL | .153849 | .159127 | .161724 | 11.079936 | 8.321868 |
| C_ALLOC | .150282 | .158154 | .161263 | 11.086342 | 8.325250 |
| C_MARGIN | .148436 | .156975 | .159602 | 11.094101 | 8.335999 |

All five new half arms beat additive_defense after the registered17-comparison
correction, but none establishes its intended incremental improvement.
C_FIXED−reference half RMSE−.000146[−.000310,+.000003], Holm.888672.
C_CLOCK−reference+.022719[+.008629,+.039520], Holm.064453.
Checkpoint averages are descriptive; they recover much, not all, of joint arms'
loss against the same-view reference. No outer-selected checkpoint policy.

Separate actual-context event evidence: C_FULL improves counts/location/
conversion/recovery against C_CLOCK in11/11seasons, Holm.027344 each across28tests.
Conditional point r² C_FIXED.181401 and C_MARGIN.223626 are **not** new product
records: future realized game context is a different information contract, and
margin is endogenous. Common-environment player estimation remains unproven.

Transfer half RMSE reference6.674457, C_CLOCK6.713951, C_FULL6.721401;
novel half r² reference.144082, C_CLOCK.140155, C_FULL.139961.
All9models still favor legal centers over both Jokić fixtures. Joint models
increase center FTA projections; small margin reductions do not solve coherence.

Automated pooled uncertainty includes2015warmup. The independent review re-pools
original quarterly sufficient statistics over2016–2026: reference U0 half95%
coverage93.47%cell/93.19%weighted; C_FULL93.68%/93.20%, with wider intervals and
slightly worse proper score. U1 offers no new advantage; latent OOD quality
coverage remains unvalidated. Use
`experiments/cache/joint_capability_2026_10_04_v19_review2` for primary-only
uncertainty and270independently verified point metric rows.

## v18 broad comparison — historical campaign

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

To re-score the reference from its saved native predictions (about 40
seconds; checked exactly by `tests/test_scoring_parity.py`):

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m lineups.evaluate --arm J_POINT_BOTH --view checkpoint_average --novel
```

Other arms and the older report commands need the pre-refactor code
(`scripts/legacy_worktree.sh`).

The full [review](reports/joint_capability_v16_codex_review.md) covers architecture,
events, transfer cases, error decomposition, reliability sensitivity and the
recommended next work. The [backlog](MODEL_RESEARCH_ROADMAP.md) owns priorities.

## Historical tables

Exact pre-review scorecard:
[2026-09-27 archive](docs/history/archive/2026-09-27_pre_v16_review/MODEL_SCORECARD.md).
Original v15/v14 and earlier protocols/reports remain unchanged.
