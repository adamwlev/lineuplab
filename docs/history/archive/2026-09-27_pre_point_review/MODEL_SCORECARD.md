# Current model scorecard

Updated **2026-09-27** from the completed, repaired
[v16 independent review](reports/joint_capability_v16_codex_review.md).
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

## Current broad point comparisons

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

**Uncertainty:** leading forward blend95% finite-quarter bands cover93.86%
overall and93.31% novel, on the broad cohort. U2's held-out joint log score is
slightly worse than U1 in allnine prespecified model/split comparisons.
Synthetic bands widen, but this does not validate latent-quality coverage.
J_POINT_BOTH is not in the fixed U1/U2 set; its own persistent uncertainty
and full observed-lineup average-opponent benchmark remain future evaluations.

**Average opponents:** fixed J_BOTH and J_ALL_BOTH halves reach r².143111/.143782,
versus their integrated additive_defense control.132160. This is not the
known-opponent task above. Only the fixed three-arm subset was evaluated.

**Numerical audit:** all64 exact-reference comparisons pass; maximum native
error at16,384 references.010976 points/100. No numerical issue explains away
the current coherence findings.

## Sources and reproduction

Completed source:
`experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.
Independent read-only review tables:
`experiments/cache/joint_capability_2026_09_27_v16_codex_review`.
All201 supplemental scorecard rows independently reconstructed from saved cells.

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
