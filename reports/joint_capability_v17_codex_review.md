# v17 independent review — useful mechanism test, no new predictive winner

2026-09-28. Requested by Adam after the run completed. All five new arms,
48 origins and three seeds completed: **720 cases / 1,440 inner-final fits**.
Supervisor wall time was **90,977 seconds / 25.27 hours**, including automatic
post-training work; accumulated training worker time was 66.33 hours.
No new fits, data access, source changes, promotion or deployment in this review.

## Bottom line

v17 largely preserves v16's predictive performance. O_ORDER is a plausible
conceptual cleanup with a tiny descriptive gain, not an established improvement.
Shared creation flow responds coherently to capacity and mildly reduces some
extreme offenses, but does not resolve the center-matchup failure. Removing
defensive action-volume effects sacrifices useful event information without
an established point benefit. Keep the v16 point candidate as the retained
research reference; no overall three-pillar pass or scorer promotion.

The automatic U0 uncertainty summary contains a **status-label bug**, repaired
in new derived outputs here. Training, predictions, interval bounds and U1
fits were unaffected. Do not use the old packet's all-unidentified U0 table.

## Verification and provenance

Sources: `experiments/cache/joint_capability_2026_09_27_v17_prod` and its
`_scored`, `_average`, `_basketball`, `_uncertainty`, `_summary`, `_handoff`
siblings. Original artifacts and producer fingerprints remain unchanged.

New outputs: `experiments/cache/joint_capability_2026_09_28_v17_codex_review`.
Producer: `experiments/v17_completed_review.py`; regression checks:
`tests/test_v17_completed_review.py` (two tests passed).

- Recursively checked **34,923 source files** against completion receipts,
  including all720 native cases; checked frozen native/summary producer hashes.
- Independently recomputed **460 point-metric rows** from saved cell forecasts
  across the two reported populations, five slices and available views/controls.
  RMSE, MAE, r², correlation, bias, counts and weights match to1e-8 tolerance.
- Verified identical broad keys/targets/exposures across arms and half arithmetic.
- Checked U0 status/bounds, coverage and nominal95% interval-score arithmetic
  on every saved quarter; primary corrected summaries match models by cell ID.
- Added quarter-level versus within-quarter error decomposition and descriptive
  season-wise event contrasts. No new significance family or outcome-selected
  acceptance population.

The registered16 contrasts remain those in the frozen plan:10,000 season-block
draws, exact2,048 season swaps and Holm over16. Repeated historical development
is not a fresh prospective test. Seeds are not independent seasons.

## 1. Prediction: tied with the established contextual candidate

Primary: possession-weighted offensive-five quarter ratings against the actual
defenses faced,44 quarters in2016–2026,2015 calibration warmup excluded,
**8,345 cells /1,013,999 possessions**, three-seed prediction means.
RMSE/MAE/bias units are points/100. Half is50/50 calibrated NN and additive_defense.

| Model | Direct r² | Half r² | Half RMSE | Half MAE |
| --- | ---: | ---: | ---: | ---: |
| O_ORDER | .162077 | .163049 | 11.054064 | 8.297513 |
| O_FLOW | .161042 | .162637 | 11.056783 | 8.300601 |
| D_SHAPE | .161258 | .162669 | 11.056576 | 8.301090 |
| O_FLOW_D_SHAPE | .161674 | .162923 | 11.054898 | 8.299261 |
| O_FLOW_EVENT | .154608 | .158784 | 11.082190 | 8.342255 |
| J_POINT_BOTH (v16) | .161925 | .162915 | 11.054951 | 8.299892 |
| J_BOTH (v16) | .154150 | .158193 | 11.086086 | 8.346621 |

Equally informed controls: additive_defense r².146023 /RMSE11.165936;
parent_half_defense .156601 /11.096562. Offense-only additive .132848 /11.251737
is orientation, not the sole fair comparator.

Registered half-view RMSE deltas (negative favors left):

| Contrast | Delta | 95% season-bootstrap interval | Season wins |
| --- | ---: | --- | ---: |
| O_ORDER − J_POINT_BOTH | −.000887 | [−.004135, .002210] | 8/11 |
| O_FLOW − O_ORDER | +.002720 | [−.002193, .008493] | 4/11 |
| D_SHAPE − J_POINT_BOTH | +.001625 | [−.012063, .012104] | 4/11 |
| O_FLOW_D_SHAPE − O_FLOW | −.001885 | [−.015410, .009110] | 5/11 |
| O_FLOW_EVENT − J_BOTH | −.003896 | [−.011052, .002611] | 6/11 |
| O_FLOW_EVENT − O_FLOW | +.025407 | [−.000790, .053517] | 6/11 |

None establishes the intended incremental point gain. All five new arms beat
additive_defense after the registered Holm correction (p=.015625 for the four
point-supervised arms; .023438 for event-only). Gains over parent_half_defense
do not clear that correction (point arms p=.064–.086). Those are gains of the
whole contextual system, not proof that v17's new mechanisms caused them.

D_SHAPE checkpoint-average-half has the highest displayed r²,.163188, versus
the v16 checkpoint-half .162989. That is a descriptive view comparison, not
the registered primary winner; the difference is too small to justify selection.
All four views are retained in `point_verified.csv`.

### Novel lineups and error sources

Novel cohort:3,489 cells /361,361 possessions. O_ORDER direct r².148813 versus
J_POINT_BOTH .148573; half .144329 versus .144082. Additive_defense .118400 and
parent_half_defense .134599. Direct still outperforms half on this cohort, but
this repeats the earlier pattern rather than establishing a new flow benefit.
Thin/debut direct scores also generally exceed their half views, with no clear
new-arm win over the existing point control. Do not choose blend weights on
these realized slice outcomes.

O_ORDER's half MSE improvement over J_POINT_BOTH is only .01961; .01842 comes
from quarter-level squared-bias reduction, versus .00120 from within-quarter
error. O_FLOW_D_SHAPE improves within-quarter MSE by .03374 but loses .03257
on quarter levels, leaving an almost zero overall change. This is diagnostic
centering, not a deployable forecast or evidence of a causal mechanism.

## 2. Event fidelity: defensive volume is doing real predictive work

Native event losses are exposure-weighted averages across seed predictions,
not event losses of a three-seed ensemble. Supplemental season-win counts below
are descriptive, not a new corrected hypothesis family.

- D_SHAPE versus J_POINT_BOTH worsens count loss by **.0008027** and conversion
  loss by **.0000981**, both in **11/11 seasons**. O_FLOW_D_SHAPE versus O_FLOW
  similarly worsens counts by.0007879 and conversion by.0001105, both11/11.
  Near-identical point totals hide worse intermediate predictions. Do not
  conclude that defensive effects on turnovers/FTA/FGA are unnecessary.
- O_ORDER changes event losses very little: counts−.0000072 (9/11 season wins),
  conversion−.0000079 (10/11), recovery+.0000057 (only1/11 wins).
- O_FLOW versus O_ORDER is mixed: count delta+.0000042, location+.0000366,
  recovery+.0000266. No broad event advantage for the capacity replacement.
- O_FLOW_EVENT versus O_FLOW improves counts by **.0002602,11/11 seasons**,
  and the other three pooled event losses also improve (9/11 season wins each).
  Point accuracy is worse. The objective tradeoff persists.
- Against event-only J_BOTH, O_FLOW_EVENT is near-identical on counts,
  modestly better on pooled location/recovery and slightly worse on conversion.
  It is a useful mechanism comparator, not a new universal leader.

Median selected epochs: O_ORDER9, O_FLOW8.5, D_SHAPE8, O_FLOW_D_SHAPE8,
O_FLOW_EVENT13 (all48 origins). No cap hits in the primary-period fit metadata.
Training did not fail or simply run every arm to a hard epoch limit.

## 3. Basketball: functioning constraints, incomplete counterfactual solution

All32 registered fixtures at10 dates were processed, including ordered mirrors,
duplicate profiles and independent slot permutations. Original detailed ledgers
and numerical checks remain in `_basketball`; no synthetic ranking was forced.

At2026q4, the legal five-center lineup against the Jokić/Murray/Gordon/Porter/
Westbrook fixture (three-seed means):

| Arm | Centers' direct offense | Opponent direct offense | Centers' direct margin | Centers' half margin |
| --- | ---: | ---: | ---: | ---: |
| J_POINT_BOTH | 120.285 | 115.579 | +4.707 | +5.526 |
| O_ORDER | 119.990 | 115.325 | +4.664 | +5.505 |
| O_FLOW | 118.702 | 114.563 | +4.139 | +5.242 |
| D_SHAPE | 118.957 | 115.387 | +3.570 | +4.958 |
| O_FLOW_D_SHAPE | 118.423 | 114.806 | +3.616 | +4.981 |
| O_FLOW_EVENT | 119.699 | 117.679 | +2.020 | +4.182 |
| J_BOTH | 120.545 | 118.018 | +2.527 | +4.436 |

Flow lowers both teams' offense: O_FLOW versus O_ORDER reduces center offense
by1.288 but opponent offense by.763, shrinking the margin by only.525. Do not
sell the entire offensive reduction as a selective correction of malformed
lineups. All seven still favor the centers in both product views against both
the Korver and Westbrook fixtures. The mixed-era Korver transport caveat remains.

There is a meaningful mechanistic response: native center turnovers rise from
14.78 to16.23/100 in O_ORDER→O_FLOW, while FGA fall89.79→87.86 and renewed
points fall15.43→14.67. Center supply is about.142 versus demand.280 in action-
budget units under O_FLOW, with.138 unmet demand. Rebound capture remains high,
about.478. Missing creation is represented, but the fitted fallback cost and
renewal/defense interactions do not produce a convincing overall extreme forecast.

Across the saved capacity intervention grid0/.5/1/2, no native point decrease
exceeds1e-5pts/100 when capacity increases. The minimum numerical difference
is about−1.76e-6. These interventions alter allocator supply only; they are
not observed player improvements or causal assist effects.

Primary-period O_FLOW median tau=.0927 and kappa=.1018 (initialized .1/.1).
Neither collapses to zero. They remain modest and fairly close to initialization;
this is not evidence that PBP identifies universal creation capacity or fallback
cost. A future initialization/identification sensitivity would need its own plan,
not stronger hand-set penalties to make the center fixture lose.

Against the three saved prior-common opponent fixtures (not512-opponent product
integration), O_FLOW gives Haliburton about+1.626pts/100 over McConnell, close
to O_ORDER's+1.647. It still gives Mitchell Robinson greater team rebound capture
than Adams in the fixed same-four comparison (.321 versus.315). These checks
remain falsifiable predictions, not required rankings or causal facilitation proof.

### Observed unconventional units

Frozen two-big cohort:65 cells /8,471 possessions; low-creation184 /17,976;
intersection only6 cells. Point-half two-big bias remains about+3pts/100:
J_POINT_BOTH+3.048, O_ORDER+2.988, O_FLOW+3.045, D_SHAPE+3.004,
O_FLOW_D_SHAPE+3.002. No meaningful repair of the observed analogue bias.
Low-creation point-half bias is roughly+.54 to+.71 for new point arms, with
RMSE around12.29–12.32. Sparse cohorts do not identify five-center true quality.
All members and outcome-selected top/bottom10 descriptions remain available;
verified bands accompany those descriptions in the new review outputs.

## 4. Product mode and uncertainty

512 prior-reference opponents, same realized targets and broad population:

| Arm | Average-opponent half r² | RMSE |
| --- | ---: | ---: |
| O_ORDER | .148764 | 11.147998 |
| O_FLOW_D_SHAPE | .148402 | 11.150371 |
| J_POINT_BOTH | .148368 | 11.150592 |
| O_FLOW | .148133 | 11.152134 |
| D_SHAPE | .148115 | 11.152247 |
| O_FLOW_EVENT | .143242 | 11.184102 |
| J_BOTH | .143111 | 11.184958 |
| Integrated additive_defense | .132160 | 11.256199 |

Again no large new gain. The first20 cells/date512→4096 sensitivity reaches
about.161pts/100 direct and.151 half across primary origins/arms. This is
numerical sensitivity, not a confidence interval or exact-error bound. Targets
are actual outcomes, not observed neutral-opponent counterfactuals.

### U0 summary repair

`write_u0` emits per-cell valid status `FINITE_GAME_BAND`; `v17_summary` checks
`status == "OK"`, which is the writer's **aggregate** status, not its row status.
Consequently the original summary/packet falsely report zero identified cells.
The saved bounds, coverage indicators and interval scores are valid. Correction
maps only that documented valid row status, rejects unknown/inconsistent rows,
and retains genuinely cold `NOT_IDENTIFIED` rows. No thresholds or fitting change.

All8,345 primary broad cells have valid bands for all16 model/views. At nominal95%:

| Half forecast / control | Cell coverage | Possession-weighted coverage | Mean full width | Mean interval score |
| --- | ---: | ---: | ---: | ---: |
| J_POINT_BOTH | 93.47% | 93.19% | 47.824 | 60.671 |
| O_ORDER | 93.59% | 93.20% | 47.967 | 60.657 |
| O_FLOW | 93.58% | 93.30% | 47.858 | 60.689 |
| D_SHAPE | 93.66% | 93.21% | 48.076 | 60.641 |
| O_FLOW_D_SHAPE | 93.70% | 93.31% | 48.078 | 60.648 |
| O_FLOW_EVENT | 93.80% | 93.39% | 47.977 | 60.639 |
| Additive_defense | 93.71% | 93.01% | 48.591 | 61.115 |

Widths/scores are points/100; coverage is slightly low, and differences are
small. Corrected direct and all five slice tables are saved too. This repair
supersedes the **broad** U0 summary; the archived all-off5 U0 aggregate is also
invalid and has not been replaced here. Its raw bands remain valid. Do not
confuse tiny-cell all-off5 coverage with the broad leaderboard population.

U1 was unaffected:2,037/2,095 primary balanced-game pairs jointly identified,
58 cold/unidentified. Half log scores are very close (higher better):
J_POINT_BOTH−7.86995, O_ORDER−7.87011, O_FLOW−7.86864,
O_FLOW_D_SHAPE−7.86932; coverage about94.1–94.2%. No established uncertainty
breakthrough. These intervals concern finite outcomes and a stable-quarter
discrepancy model; neither validates arbitrary synthetic-lineup latent quality.

## 5. Next decision

1. **Retain the v16 point reference**, with O_ORDER as a candidate accounting
   cleanup and O_FLOW/O_FLOW_EVENT as mechanism comparators. No automatic
   promotion based on a fourth decimal of r².
2. **Keep defensive-volume information in the main research baseline.** D_SHAPE
   is useful diagnostic evidence, not a supported simplification of all channels.
3. **Prioritize representation and role identification over more flow rounds or
   stronger penalties.** The [v18 idea bank](../docs/history/V18_IDEAS.md) already contains
   compact adjusted-first profiles, channel/reliability-specific use, and
   capability-versus-observed-role separation. Decide a bounded design with Adam.
4. Attach predeclared role-change evaluation and honest uncertainty comparisons
   to that design. A separate possession-entry feasibility audit remains promising,
   but is not authorized ingestion or an implemented model.
5. Any future summary producer must use the correct U0 writer contract and
   validate real identified rows, not just successful file creation. The frozen
   v17 producer remains untouched for provenance; use this review's repaired
   broad tables until a separately versioned fuller replay is requested.

Reproduce in a **new** output prefix (do not overwrite the completed review):

```bash
mkdir -p experiments/cache/v17_review_replay/logs
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v17_completed_review \
  --run-dir experiments/cache/joint_capability_2026_09_27_v17_prod \
  --out experiments/cache/v17_review_replay \
  >> experiments/cache/v17_review_replay/logs/review.log 2>&1
```

Original status/leaderboard commands remain valid for point scores. No commit
was made in this review task; earlier literature/v18 notes were preserved.
