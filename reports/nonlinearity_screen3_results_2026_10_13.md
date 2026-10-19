# Pairwise module held at its measured outputs: screen results — 2026-10-13

Results of the [protocol](nonlinearity_screen3_protocol_2026_10_13.md),
committed (c8174596) before any range was measured or any forecast made.
This is an exploratory screen: one seed (17) at the 20 quarters of 2022–2026,
using the `pairs` arm's weights.
- Script: `scripts/nonlinearity_screen.py`.
- Output: `experiments/cache/nonlinearity_screen_2026_10_13/`
  (`pairs_out_*`, `screen3_*`, `out_diagnostic_2026q4.txt`).

## Summary

- **The arm narrowly fails its primary criterion.** Over the 20 quarters,
  against Jokić/Westbrook:
  - five Goberts' offense is +2.1 (SE 0.7) per 100 above the reference;
  - legal centers' offense is +1.5 (SE 0.6);
  - the bar for both was +1.
- **It removes most of the off-support excess.** Unclamped, the same weights
  give +9.6 and +5.5. Clamping the inputs (second screen) gave +7.1 and
  +4.4.
- **The defensive direction is kept.** Jokić/Westbrook score +4.3 (SE 0.7)
  more against five Goberts than under the reference.
- **Margins now go against clone bigs.**
  - Five Goberts: −2.1 (SE 0.8) vs the reference.
  - Legal centers vs Jokić/Westbrook: −2.5 (SE 0.7).
  - Five Jokićs: −1.7 (SE 0.5).
- **Real-lineup gains are kept.**
  - χ²_H is 156 (unclamped 154, reference 254), and χ²_N does not rise.
  - Accuracy does not move: +0.0005 ± 0.0025 r² with equal calibration.
  - Forecasts are 67% more non-additive than the reference's (1.1% → 1.8% of
    variance).
- **Property suite:** the same as the unclamped module. clone_synergy stays
  at 0.916.
- **Why it still fails (post hoc).** Each bound is per channel. Each clone
  fixture sits at its lineup bound in 10 of 15 channels at once. Only 0.11%
  of real lineups are at their bound in that many.

## Contrast 1: interactions and accuracy

| | reference | pairs | pairs_out |
| --- | ---: | ---: | ---: |
| Non-additive share of points-forecast variance | 0.0110 | 0.0193 | 0.0184 |
| χ²_H, residual, 14 held-up cells (lower = learned) | 253.5 | 153.5 | 156.4 |
| χ²_N, residual, 511 other cells (higher = invented) | 1,417 | 1,136 | 1,135 |
| Implied interactions on N cells, RMS in SE units | 0.36 | 0.36 | 0.35 |
| Accuracy vs reference, equal in-quarter calibration | — | +0.0002 (0.0025), 10/20 | +0.0005 (0.0025), 10/20 |
| Accuracy vs reference, reference's prior calibration | — | −0.0039 (0.0050), 7/20 | −0.0035 (0.0051), 8/20 |

Accuracy is calibrated points r² on outer broad cells: the mean of arm minus
reference over the 20 origins, with origin SE and the count of positive
origins.
- **The hold costs no real interactions** by the declared criterion: χ²_H is
  1.9% above `pairs`; the threshold was 20%.
- On real outer rows, the native points level matches the reference: −0.10
  per 100 on average (SE 0.14 over quarters).

## Contrast 2 (primary): fixtures at all 20 quarters

Native points per 100. Each entry is the mean over the 20 quarters, with the
origin SE of the difference. "> +1" counts the quarters above the bar.

| Fixture | Side | Reference | pairs − ref | pairs_held − ref | pairs_out − ref | out: quarters > +1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Five Goberts vs Jokić/Westbrook | Goberts' offense | 113.0 | +9.6 (1.4) | +7.1 (1.2) | **+2.1 (0.7)** | 15/20 |
| | Jokić/Westbrook's offense | 107.3 | +8.7 (1.1) | +7.3 (1.0) | +4.3 (0.7) | 19/20 |
| | margin | +5.7 | +0.9 (1.9) | −0.2 (1.6) | −2.1 (0.8) | 2/20 |
| Legal centers vs Jokić/Westbrook | centers' offense | 113.0 | +5.5 (0.9) | +4.4 (0.8) | **+1.5 (0.6)** | 13/20 |
| | Jokić/Westbrook's offense | 112.8 | +5.2 (0.7) | +4.9 (0.7) | +4.0 (0.6) | 18/20 |
| | margin | +0.3 | +0.3 (1.1) | −0.5 (0.9) | −2.5 (0.7) | 2/20 |
| Legal centers vs Jokić/Korver | centers' offense | 114.4 | +6.6 (1.1) | +5.5 (0.9) | +2.6 (0.7) | 16/20 |
| | Jokić/Korver's offense | 113.9 | +4.2 (0.7) | +4.0 (0.7) | +3.2 (0.6) | 18/20 |
| | margin | +0.6 | +2.4 (1.1) | +1.5 (1.0) | −0.7 (0.7) | 6/20 |
| Five Jokićs vs Jokić/Westbrook | Jokićs' offense | 132.8 | +1.6 (0.9) | −0.0 (0.9) | +0.9 (0.7) | 11/20 |
| | Jokić/Westbrook's offense | 112.2 | +2.7 (0.9) | +2.9 (0.8) | +2.6 (0.7) | 13/20 |
| | margin | +20.6 | −1.1 (0.8) | −2.9 (0.7) | −1.7 (0.5) | 2/20 |

The `pairs_held` column is from the [second screen](nonlinearity_screen2_results_2026_10_13.md).

**By the declared criterion, the arm fails.** Both named offenses exceed +1:
- five Goberts by 1.1 points over the bar, about 1.6 SE;
- legal centers by 0.5 points, about 0.8 SE.

The defensive direction is kept. The bar is not revised after the fact.

## Contrast 3: property suite at 2026q4

| Property | Reference | pairs | pairs_out |
| --- | ---: | ---: | ---: |
| spacing_rim | 0.999 | 0.994 | 0.995 |
| handler_turnovers | 0.410 | 0.374 | 0.374 |
| handler_conversion | 0.985 | 0.985 | 0.985 |
| handler_teammate_turnovers | 1.000 | 0.995 | 0.995 |
| clone_synergy | 0.988 | 0.921 | 0.916 |
| rim_synergy | 1.000 | 1.000 | 1.000 |
| rebound_synergy | 1.000 | 1.000 | 1.000 |
| perimeter_coverage | 0.658 | 0.763 | 0.763 |
| coverage_targeting | 0.342 | 0.574 | 0.574 |
| permutation | 1.000 | 1.000 | 1.000 |

clone_synergy puts two to four copies of a real lineup's top-usage player
into that lineup. The hold barely changes its pass rate (0.921 → 0.916).
This suggests those partial clones mostly stay inside the measured ranges,
where no range-based hold acts; I did not check this directly.

## Why it still fails (post hoc diagnostic)

From `--out-diagnostic` (`out_diagnostic_2026q4.txt`): last checkpoint at
2026q4, with outputs held.

| Lineup on offense | Channels with the lineup sum at its bound | Real lineups with at least as many |
| --- | ---: | ---: |
| Legal centers | 10 of 15 | 0.11% |
| Five Goberts | 10 of 15 | 0.11% |
| Five Jokićs | 10 of 15 | 0.11% |

Among 22,522 real outer lineups, 86.5% have no channel at its bound and 8.0%
have one.

Each channel's bound is something real lineups reach. Being at the bound in
ten channels at once is something almost none reach. A per-channel bound
cannot express that. The remaining excess is the joint extreme.

## What follows

- **The tool keeps the bolted-on layer.** Nothing here changes the tool.
- **What the three screens show.**
  - In-network learning of real interactions works on real lineups and costs
    no accuracy.
  - Bounding it off-support has needed a sharper constraint each time:
    inputs, then outputs per channel. The next would be a joint bound.
- **One possible last screen: a joint bound.**
  - It would keep the lineup's 15-channel combination effect no more unusual
    than real lineups' (for example, within the 99.5% Mahalanobis radius of
    real lineup totals).
  - Like this screen, it needs no retraining.
  - Any pass would still be one seed after several tries. It would need the
    three-seed confirmation at the release origin before it could matter.
- **Or stop here.** The layer holds type counts exactly and is auditable
  effect by effect.

## Correction during the run

`summary()` gained a `name` parameter for this screen, but a loop variable of
the same name shadowed it. The first summary run therefore wrote its output
as `implied_pairs_out.{txt,json}`.
- The variable was renamed, and the files were moved to
  `screen3_summary.{txt,json}`. Their content is unchanged.
- No earlier screen's file was overwritten. As in the second screen,
  `interaction_coefficients.csv` was rewritten with the new arm added;
  existing arms' values are deterministic.
- The first queue launch passed a relative path and did not start. It was
  relaunched before any output was written.
