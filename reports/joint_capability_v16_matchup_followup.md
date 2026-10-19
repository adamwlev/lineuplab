# v16 matchup follow-up — 2026-09-27

Status: bounded saved-weight diagnosis completed; candidate average-opponent
and persistent-uncertainty evaluations are separate work, not yet conclusions
of this report. Protocol: [fixed follow-up design](joint_capability_v16_followup_protocol.md).
No new NN fitting, modified deployed scorer, database access or promotion.

## What the center example actually diagnoses

The five centers are Gobert/Adams/Robinson/Capela/Allen. The comparison lineup
is Jokić/Murray/Gordon/Porter/Westbrook, all using the frozen 2026q4 state.
These are hypothetical outputs, not observed outcomes or proof of a true winner.
The matching seasonal cutoffs do not make this extrapolation data-identified.

The three-seed J_POINT_BOTH prediction has the following accounting, in points
per100 starting possessions. Native components precede affine calibration.

| Native component | Centers attacking Jokić lineup | Jokić lineup attacking centers | Center advantage |
| --- | ---: | ---: | ---: |
| Initial chances | 105.086 | 106.667 | −1.580 |
| Renewed possessions | 15.456 | 7.480 | +7.976 |
| Total | 120.542 | 114.147 | +6.395 |
| Two-point scoring | 100.056 | 49.715 | +50.340 |
| Three-point scoring | 1.558 | 53.115 | −51.557 |
| Free throws | 18.928 | 11.317 | +7.611 |

The two sets of decompositions reconcile separately: initial+renewed and
2PT+3PT+FT. They are overlapping explanations, not independent additive causes.
Dropping renewed points is an accounting exercise, not a normalized first-shot
offensive rating or a basketball intervention we can treat as causal.

After the unchanged calibrations, additive_defense favors centers by **6.345**,
the direct NN by **4.707**, direct-half by **5.526**, and checkpoint-half by
**4.810** points/100. Therefore this is not solely a neural interaction defect:
the equally informed additive control starts with an even larger center edge.

## What the saved-weight switches reveal

These are no-refit model interventions with the original calibration retained.
They locate influential computations; they neither identify a causal effect nor
show how a model trained without that component would perform.

| J_POINT_BOTH switch, both directions | Predicted center margin, direct |
| --- | ---: |
| Full model | +4.707 |
| Teammate messages off | +14.872 |
| Adjusted offense off | +10.394 |
| Raw and adjusted defense off | −6.777 |
| Supply/FT/load constraints off | +7.067 |
| Defensive rebound recovery effect off | +2.468 |

The teammate path is helping penalize this roster. Removing it increases the
center edge by10.165 points/100. The adjusted offense path helps too. Simply
adding a stronger version of a generic interaction layer is not the most direct
interpretation of this result.

The combined defensive paths swing the margin by **11.484** points/100:
centers' predicted offense rises3.170 and the Jokić lineup's falls8.314 relative
to the defense-off switch. This includes action rates, locations/conversion,
and recovery, so it must not be labeled “rim defense alone.” Turning off only
defensive recovery changes the margin by2.239; recovery is not the whole story.

The center offense still allocates Allen about36.96 points,26.57 FGA and9.30 FTA
per100 starting possessions, alongside four other finishers. The model reports
substantial creation shortage (mean0.602), rather than failing to detect any.
It nevertheless permits a productive high-volume rim/FT offense and powerful
renewal. Whether those opportunities remain available under such crowding is
the unresolved basketball question.

## Observed analogues, fixed before examining errors

Broad >=50-possession offensive-lineup/quarter cells,44 primary quarters,
actual defensive opponents, possession weighting, mean predictions across
three seeds. Nonspacing big = archived height>=82in and origin-prior raw
3PA/100<1. Low creation = maximum individual prior AST/100<5. This is a simple
role proxy, not a position label: young Giannis can qualify as a nonspacing big.

| Cohort | Cells / possessions | Actual pts/100 | Additive RMSE / bias | Point direct RMSE / bias | Point half RMSE / bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| All | 8,345 /1,013,999 | 113.855 | 11.166 /+0.072 | 11.061 /−0.217 | 11.055 /−0.072 |
| At least two nonspacing bigs | 65 /8,471 | 104.462 | 11.026 /+2.836 | 11.214 /+3.260 | 11.060 /+3.048 |
| Low creation | 184 /17,976 | 107.677 | 12.643 /+1.576 | 12.179 /−0.314 | 12.314 /+0.631 |
| Two bigs + low creation | 6 /495 | 97.778 | 16.027 /+5.225 | 16.224 /+4.219 | 16.090 /+4.722 |
| At least three nonspacing bigs | 0 /0 | — | — | — | — |

Bias is prediction minus observed points/100. These post-hoc diagnostic subsets
do not establish significance or the performance of truly impossible rosters.
The broad table retains212 cells with at least one missing height; such players
cannot count as known bigs, so subset membership may be incomplete. All65
selected two-big cells have complete height information. Prior-state exposure
is recorded separately rather than silently filtering predictions.

The NN improves low-creation forecasts overall, while two-big optimism remains
shared with additive. Six low-creation/two-big cells cannot settle the more
extreme five-center example. The absence of three-big observations is precisely
why a calibrated confidence claim cannot be obtained from this subset alone.

## Next learning experiment: direction, not a frozen training protocol

First complete the candidate's missing average-opponent and U1/U2 evaluations.
Then design a targeted experiment around:

1. **Point/channel tradeoff:** the existing point-loss gain versus worse count
   likelihood deserves an explicit, small loss-weight/channel study. Preserve
   both rating and event metrics; do not silently buy one with the other.
2. **Defensive extrapolation and opportunity constraints:** separate raw versus
   adjusted defense, location/conversion versus volume effects, and renewal.
   Test defensible capacity/saturation assumptions across a fixed diverse
   roster panel and observed overlap cohorts, not a penalty named after centers.
3. **Equal-information level controls:** much of the gain over the incumbent
   blend is quarterly level error. Compare seasonal-level adjustment fairly
   before attributing the gain to better basketball interactions.
4. **Uncertainty about unfamiliar composition:** keep finite-game noise separate
   from persistent model discrepancy; weak support should widen/disclose
   uncertainty, not suppress the prediction with a coverage gate.

Do not choose architectural restrictions merely to flip this one matchup.
The user explicitly allows quantitative evidence to overturn named intuitions.

## Artifacts and verification

Root: `experiments/cache/joint_capability_2026_09_27_v16_followup/`.

- `matchups/`: completed first diagnostic;144 archived matches reproduced,
  all four arms ×three seeds ×16 ordered pairs,10 switches, point checkpoint view.
- `matchups_v2/`: complete, same computation with additional per-player demand,
  expected makes and conversion fields; team outputs equal the original exactly.
- `analogues_v2/`: complete broad/case/quarter scorecards and descriptors.
- `logs/`: durable diagnostic/pilot/test logs; failed development attempts kept.
- `provenance/`: exact producer snapshots for completed earlier outputs.
- Reproducer: `experiments/v16_matchup_diagnosis.py`.
- Original artifacts are read-only. No changes to source scoring, calibrations,
  frozen v16 plan or user-supplied feedback.

## Candidate evaluation readiness

Average pilots used2015q1 and2026q4, all three seeds and the actual saved
checkpoint lists. Runtime52.65s/99.34s excluding startup; all original control
populations, labels and additive/integrated-additive values matched. Maximum
absolute512-versus4096 difference on the specified sensitivity cells was
0.06448 points/100 across the four views. These pilots are operational and
historical diagnostics, not a newly selected favorable accuracy subset.

For context,2026q4 average-opponent RMSE was12.849 integrated-additive,
12.79665 J_BOTH-half,12.73533 D_MAIN_RB-half,12.58088 point-direct,
12.67419 point-half and12.72264 point-checkpoint-half. Await the complete
44-primary-quarter comparison; neither this pilot nor the actual-opponent
leaderboard settles average-opponent performance.

The six-quarter uncertainty pilot (2015q1–2016q2) completed, including
prior-only U1/U2 fits and exact matching against old controls.112 existing
U0 finite-summary rows reproduce to1e-10. The two candidates use their own
seed/view forecasts loaded from verified per-fit archives: the combined
archive did not retain J_POINT_BOTH's per-seed columns. A unit test rejects
row-order or ensemble-mean disagreement and verifies checkpoint-half does
not accidentally use direct-half disagreement.

Sixteen focused tests pass. Acceptance receipt:
`experiments/cache/joint_capability_2026_09_27_v16_followup/acceptance/`.
The full follow-up is separate from these pilots and from the completed v16
run. No scorer is promoted, and synthetic latent-quality coverage remains
unvalidated regardless of finite-band results.
