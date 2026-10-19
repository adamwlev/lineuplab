# Pairwise module held at the measured range: screen results — 2026-10-13

Results of the [protocol](nonlinearity_screen2_protocol_2026_10_13.md),
committed (da6613ae) before the arm was trained. This is an exploratory
screen: one seed (17) at the 20 quarters of 2022–2026.
- Script: `scripts/nonlinearity_screen.py`.
- Output: `experiments/cache/nonlinearity_screen_2026_10_13/`.

## Summary

- **The arm fails its primary criterion.** Over the 20 quarters, it puts the
  offense of five Goberts against Jokić/Westbrook +7.1 (SE 1.2) per 100
  above the reference, and that of legal centers +4.4 (SE 0.8). The bar was
  +1.
- **The clamp works as built but removes only about a quarter of the
  excess.** Without it, the same weights give +9.6 and +5.5.
- **The defensive direction is kept.** Jokić/Westbrook score +7.3 (SE 1.0)
  more against five Goberts than under the reference (unclamped: +8.7).
- **Real-lineup gains are kept, as expected.** χ²_H is 152 (unclamped 154,
  reference 254) and χ²_N does not rise. Accuracy does not move: +0.0008 ±
  0.0025 r² with equal calibration.
- **Property suite:** the same as the unclamped module.
- **Why it fails (post hoc).** The clamp bounds one factor of a product. With
  the partner sums held, each Gobert's own pair output still lies outside
  what any real player shows in 6 of 15 channels. Summed over the five, it
  lies outside what any real lineup shows in 9 of 15. Holding the partner sum
  does not bound how a Gobert-like player combines with Gobert-like partners,
  because real data never pair those extremes. It also does not bound how
  many players receive the effect.
- **Conclusion.** The tool keeps the bolted-on layer. Holding the module at
  its measured range would mean holding its outputs, per player and per
  lineup. That would be a third screen, not a change to the tool.

## Same weights, clamp only

Training is unchanged by the clamp: it acts only when forecasting, and the
running range has no gradient. Early stopping validates in forecast mode, so
it can pick a different epoch.
- It picked the same epoch as `pairs` at 19 of 20 quarters. At 2022q1 it
  picked 11 instead of 5.
- So `pairs_held` minus `pairs` isolates the clamp, almost exactly.
- On real outer rows, the arm's native points level matches the reference:
  −0.11 per 100 on average (SE 0.14 over quarters). Fixture changes are not
  a level shift.

## Contrast 1: interactions and accuracy

| | reference | pairs | pairs_held |
| --- | ---: | ---: | ---: |
| Non-additive share of points-forecast variance | 0.0110 | 0.0193 | 0.0197 |
| χ²_H, residual, 14 held-up cells (lower = learned) | 253.5 | 153.5 | 152.4 |
| χ²_N, residual, 511 other cells (higher = invented) | 1,417 | 1,136 | 1,115 |
| Implied interactions on N cells, RMS in SE units | 0.36 | 0.36 | 0.36 |
| Accuracy vs reference, equal in-quarter calibration | — | +0.0002 (0.0025), 10/20 | +0.0008 (0.0025), 10/20 |
| Accuracy vs reference, reference's prior calibration | — | −0.0039 (0.0050), 7/20 | −0.0016 (0.0036), 7/20 |

Accuracy is calibrated points r² on outer broad cells: the mean of arm minus
reference over the 20 origins, with origin SE and the count of positive
origins.

- **By the declared criterion, the clamp costs no real interactions.** χ²_H
  is 0.7% *lower* than unclamped; the threshold was 20% higher.
- Accuracy is within noise of the reference under both calibrations.
- Non-inferiority at −0.003 is still not established. The SEs are
  0.0025–0.0036, as in the first screen.

## Contrast 2 (primary): fixtures at all 20 quarters

Native points per 100. Each entry is the mean over the 20 quarters, with the
origin SE of the difference. "> +1" counts the quarters above the bar.

| Fixture | Side | Reference | pairs − ref | pairs_held − ref | held: quarters > +1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Five Goberts vs Jokić/Westbrook | Goberts' offense | 113.0 | +9.6 (1.4) | **+7.1 (1.2)** | 17/20 |
| | Jokić/Westbrook's offense | 107.3 | +8.7 (1.1) | +7.3 (1.0) | 19/20 |
| | margin | +5.7 | +0.9 (1.9) | −0.2 (1.6) | 11/20 |
| Legal centers vs Jokić/Westbrook | centers' offense | 113.0 | +5.5 (0.9) | **+4.4 (0.8)** | 18/20 |
| | Jokić/Westbrook's offense | 112.8 | +5.2 (0.7) | +4.9 (0.7) | 18/20 |
| | margin | +0.3 | +0.3 (1.1) | −0.5 (0.9) | 8/20 |
| Legal centers vs Jokić/Korver | centers' offense | 114.4 | +6.6 (1.1) | +5.5 (0.9) | 19/20 |
| | Jokić/Korver's offense | 113.9 | +4.2 (0.7) | +4.0 (0.7) | 18/20 |
| | margin | +0.6 | +2.4 (1.1) | +1.5 (1.0) | 13/20 |
| Five Jokićs vs Jokić/Westbrook | Jokićs' offense | 132.8 | +1.6 (0.9) | −0.0 (0.9) | 8/20 |
| | Jokić/Westbrook's offense | 112.2 | +2.7 (0.9) | +2.9 (0.8) | 15/20 |
| | margin | +20.6 | −1.1 (0.8) | −2.9 (0.7) | 1/20 |

**By the declared criterion, the arm fails.** Both offenses named in it rise
by far more than +1, at 17 and 18 of 20 quarters. The defensive direction
(opponents score more against clone bigs) is kept.

Two readings beyond the criterion:
- **Margins hardly move.** The module raises both offenses in big-lineup
  fixtures by similar amounts. A margin-only check would have missed the
  inflated offense; AGENTS.md rule 8 is why both sides are inspected.
- **The 2026q4 fixtures in the first report were one noisy quarter.** The
  reference's five-Gobert margin averages +5.7 over 20 quarters, not +11.8.

## Contrast 3: property suite at 2026q4

Pass rates; lineups.properties on real 2026q4 fives.

| Property | Reference | pairs | pairs_held |
| --- | ---: | ---: | ---: |
| spacing_rim | 0.999 | 0.994 | 0.994 |
| handler_turnovers | 0.410 | 0.374 | 0.374 |
| handler_conversion | 0.985 | 0.985 | 0.985 |
| handler_teammate_turnovers | 1.000 | 0.995 | 0.995 |
| clone_synergy | 0.988 | 0.921 | 0.916 |
| rim_synergy | 1.000 | 1.000 | 1.000 |
| rebound_synergy | 1.000 | 1.000 | 1.000 |
| perimeter_coverage | 0.658 | 0.763 | 0.763 |
| coverage_targeting | 0.342 | 0.574 | 0.579 |
| permutation | 1.000 | 1.000 | 1.000 |

- **clone_synergy** falls (0.988 → 0.916). Copies of a lineup's top player
  gain more together than the sum of single swaps: the same off-support
  excess as the fixtures.
- **perimeter_coverage** improves (0.658 → 0.763): swapping a small defender
  for a non-spacing big now raises opponents' three-point accuracy more
  often.
- **coverage_targeting** also rises (0.342 → 0.579). The module's defensive
  term is the same for all five attackers, so this is a larger uniform shift
  read through different base rates, not targeting.
- The clamp changes none of these materially.

## Why the clamp barely binds (post hoc diagnostic)

From `--held-diagnostic` (`held_diagnostic_2026q4.txt`), at 2026q4:

**1. The clamp binds, weakly.**

| Fixture | Offense components clamped | Defense components clamped | Attacking offense, held → unheld |
| --- | ---: | ---: | --- |
| Five Goberts vs Jokić/Westbrook | 29% | 14% | 132.3 → 134.1 |
| Legal centers vs Jokić/Westbrook | 27% | 9% | 126.9 → 127.4 |
| Five Jokićs vs Jokić/Westbrook | 29% | 8% | 142.0 → 142.4 |

The range is set so that about 1% of training-row components fall outside
it. For five Goberts, the clamped offensive components exceed the range by 7%
of its width on average (scratch run, same weights).

**2. What the clamp leaves.** These are offensive pair outputs (bounded
log-rate or logit corrections) from the last checkpoint. They are compared
with 22,522 real outer rows: per player against the real 0.5–99.5% range,
and summed over five against the same range of real lineup totals.

| Channel | Real player range | Each Gobert | Real lineup range | Five Goberts |
| --- | --- | ---: | --- | ---: |
| FGA rate | −0.12 … +0.17 | −0.23 | −0.33 … +0.28 | −1.14 |
| Turnover rate | −0.20 … +0.23 | −0.41 | −0.67 … +0.34 | −2.03 |
| Location logit 2 | −0.15 … +0.19 | −0.26 | −0.37 … +0.45 | −1.29 |
| Location logit 4 (three) | −0.76 … +0.44 | +0.93 | −1.54 … +1.05 | +4.63 |
| Location logit 5 (three) | −0.28 … +0.15 | +0.38 | −0.43 … +0.34 | +1.92 |
| Rim make logit | −0.15 … +0.09 | +0.28 | −0.33 … +0.23 | +1.41 |

Channels outside the real range: 6 of 15 per player, 9 of 15 for the lineup.

Reading:
- **The excess comes from combination, not range.** Each partner-sum
  component is in or near its range. But the module's output is the product
  of a player's own features and his partners'. Real data never put a
  Gobert-like player beside four Gobert-like partners, so the product leaves
  the measured range while each factor stays inside it.
- **It also does not cap breadth.** Every Gobert receives the effect. In real
  lineups, two or three bigs share it.
- **The basketball pattern.** The channels are the learned two-bigs effects:
  - fewer turnovers and field-goal attempts, so free throws take the freed
    budget;
  - better rim finishing;
  - more threes, from "two interior players push one outside".

  With five Goberts there is no one else to take the threes or the ball.

The layer avoids both failure modes because it holds **type counts**, which
bound breadth and combination together.

## What follows

- **The tool keeps the bolted-on layer.** Nothing here changes the tool.
- **A possible third screen.** Hold the module's outputs instead of its
  inputs:
  - each player's pair output, per channel, within the real per-player range;
  - the lineup's summed output within the real lineup range.

  It needs no retraining. The weights are the same, and only two more
  measured ranges are needed. Its criteria would be declared first, as here.
- **Or stop here.** The layer already holds counts at the measured maximum
  and is auditable effect by effect. An output-held module would be a
  learned version of the same constraint, but less interpretable.
