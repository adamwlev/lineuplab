# A learned, held combination module on the frozen network: results — 2026-10-13

Results of two protocols, each committed before its fits:
- [Screen 5](nonlinearity_screen5_protocol_2026_10_13.md) (74a38899):
  the module trained with early stopping (`frozen_joint`).
- [Screen 5b](nonlinearity_screen5b_protocol_2026_10_13.md) (6637f3e1):
  the same module trained a fixed 8 epochs (`frozen_fixed`), declared
  before any screen-5 outcome was read. It is the variant of record for
  confirmation.

Both are exploratory. Part A is seed 17; Part B is fresh fits on seeds 23
and 41. All use the 20 quarters of 2022–2026.
- Script: `scripts/nonlinearity_screen.py`.
- Output: `experiments/cache/nonlinearity_screen_2026_10_13/`
  (`frozen_*`, `screen5_*`, `screen5b_*`).

## Summary

**Screen 5b fails its confirmation on accuracy, and the frozen module is not a
candidate as built.**
- On fresh seeds it confirms the pillar-2 result: clone bigs' offense is
  held within +1, and their defense is worse.
- It also confirms the interactions learned.
- But it loses real-lineup accuracy: equal-calibration r² −0.0057 on
  average over seeds 23 and 41, against a bar of −0.003.
- A post hoc forward-calibration check (below) finds the same loss and
  traces it to main effects the module should not have.
- That diagnosis motivated [screen 6](nonlinearity_screen6_protocol_2026_10_13.md),
  a pure-interaction module. The tool keeps the bolted-on layer.

- **The design.** The calibrated network is frozen exactly; any weight move
  invalidates a run, and none did. Only a pairwise combination module is
  trained on top.
  - It reads the same identity-free capabilities as the network.
  - It is held at the range real lineups produce: per player, per lineup
    channel, and jointly.
  - With the module at zero, the forecast is the reference. So every
    difference below is the module's alone.
- **Part A (seed 17), `frozen_fixed`: passes every declared criterion.**
  - It learns more of the held-up combination effects than any earlier arm
    (χ²_H 254 → 146) without inventing others (χ²_N 1,417 → 1,093).
  - Five Goberts' offense is +0.5 (SE 0.7) per 100 above the reference;
    legal centers' is +0.6 (SE 0.6). The bar was +1.
  - Defenses of clone bigs are worse: Jokić/Westbrook score +2.3 more
    against five Goberts.
- **Part B (fresh seeds 23 and 41): the fixture criteria are confirmed.**
  - Five Goberts' offense: +0.6 (SE 0.3).
  - Legal centers' offense: +0.3 (SE 0.3).
  - Jokić/Westbrook's offense against five Goberts: +1.1 (SE 0.4).
  - The two seeds agree: Goberts +0.63 and +0.62, centers +0.37 and +0.32.
  - **Accuracy fails.** Equal-calibration r² is −0.0046 (SE 0.0021) at seed
    23 and −0.0069 (SE 0.0029) at seed 41, a mean of −0.0057; the bar was
    −0.003.
  - The interaction criteria pass at both seeds.
- **Early-stopped variant (`frozen_joint`):** passes the fixtures but fails
  contrast 1 (χ²_H 192 > 184). Stopping after 1–2 epochs, chosen by noise,
  leaves it too weak to learn the interactions.
- **Forward calibration (post hoc) agrees with Part B.**
  - With the reference's prior calibration, seed 17 loses −0.0088 (SE
    0.0057).
  - With each arm calibrated forward from its own 2022+ quarters, the three
    seeds lose −0.0095 (SE 0.0059) on average.
  - About half of that loss is a quarter-level shift the module introduces.
- **Property suite.** Three pass rates fall on real 2026q4 lineups; see
  contrast 3.

## How we got here

| Screen | Design | Five Goberts' offense vs reference (bar +1) | Outcome |
| --- | --- | ---: | --- |
| 1 | co-trained module, no hold | +9.6 (1.4) | learns, extrapolates badly |
| 2 | co-trained, inputs held | +7.1 (1.2) | fails |
| 3 | co-trained, outputs held per channel | +2.1 (0.7) | fails narrowly |
| 4 | co-trained, plus joint bound | +2.0 (0.7) | fails; the excess is in the co-trained network |
| 5 | **frozen network**, held module, early-stopped | +0.4 (0.4) | fails χ²_H (learns too little) |
| 5b | frozen network, held module, 8 epochs | +0.5 (0.7); fresh seeds +0.6 (0.3) | passes A; **fails B on accuracy** (−0.0057) |

Each screen's criteria were committed before it ran; the bars never moved.
This is the sixth design tried on seed 17, which is why only the
fresh-seed Part B counts as a result.

## Part A (seed 17)

### Contrast 1: interactions and accuracy

| | reference | pairs (screen 1) | frozen_joint | frozen_fixed |
| --- | ---: | ---: | ---: | ---: |
| Non-additive share of points-forecast variance | 0.0110 | 0.0193 | 0.0160 | 0.0186 |
| χ²_H, residual, 14 held-up cells (bar ≤ 184) | 253.5 | 153.5 | 192.4 ✗ | **145.5** ✓ |
| χ²_N, residual, 511 other cells (bar ≤ 1,417) | 1,417 | 1,136 | 1,147 | **1,093** ✓ |
| Implied interactions on N cells, RMS in SE units | 0.36 | 0.36 | 0.34 | 0.34 |
| Accuracy vs reference, equal calibration (bar ≥ −0.003) | — | +0.0002 (0.0025) | −0.0007 (0.0019) | **−0.0019 (0.0028)** ✓ |
| Accuracy vs reference, reference's prior calibration | — | −0.0039 (0.0050) | −0.0092 (0.0063) | −0.0088 (0.0057) |
| Forecast spread vs reference (SD ratio, real rows) | 1 | — | 1.05 | 1.07 |

Accuracy is calibrated points r² on outer broad cells: the mean of arm minus
reference over 20 origins, with origin SE.

### Contrast 2 (primary): fixtures at all 20 quarters

Mean over 20 quarters of arm minus reference, with origin SE.

| Fixture | Side | Reference | frozen_joint | frozen_fixed |
| --- | --- | ---: | ---: | ---: |
| Five Goberts vs Jokić/Westbrook | Goberts' offense | 113.0 | +0.4 (0.4) | **+0.5 (0.7)** |
| | Jokić/Westbrook's offense | 107.3 | +1.8 (0.4) | +2.3 (0.4) |
| | margin | +5.7 | −1.4 (0.7) | −1.8 (0.9) |
| Legal centers vs Jokić/Westbrook | centers' offense | 113.0 | +0.2 (0.4) | **+0.6 (0.6)** |
| | Jokić/Westbrook's offense | 112.8 | +1.4 (0.4) | +2.1 (0.4) |
| | margin | +0.3 | −1.2 (0.5) | −1.5 (0.7) |
| Legal centers vs Jokić/Korver | centers' offense | 114.4 | +1.1 (0.4) | +1.7 (0.5) |
| | margin | +0.6 | +0.0 (0.5) | +0.1 (0.6) |
| Five Jokićs vs Jokić/Westbrook | Jokićs' offense | 132.8 | −0.2 (0.4) | −0.0 (0.5) |
| | margin | +20.6 | −1.2 (0.4) | −1.7 (0.5) |

- **Passes.** All three conditions hold for both variants.
- **Per quarter it is not uniform.** For `frozen_fixed`, five Goberts'
  offense is above +1 in 7 of 20 quarters and legal centers' in 9.
- **The centers vs Jokić/Korver fixture is not in the criterion.** There
  the centers' offense is +1.7 (SE 0.5).

### Contrast 3: property suite at 2026q4

| Property | Reference | frozen_joint | frozen_fixed |
| --- | ---: | ---: | ---: |
| spacing_rim | 0.999 | 0.986 | 0.974 |
| handler_turnovers | 0.410 | 0.395 | 0.405 |
| handler_conversion | 0.985 | 0.985 | 0.959 |
| handler_teammate_turnovers | 1.000 | 1.000 | 1.000 |
| clone_synergy | 0.988 | 0.983 | 0.908 |
| rim_synergy | 1.000 | 0.997 | 0.997 |
| rebound_synergy | 1.000 | 1.000 | 1.000 |
| perimeter_coverage | 0.658 | 0.737 | 0.732 |
| coverage_targeting | 0.342 | 0.442 | 0.632 |
| permutation | 1.000 | 1.000 | 1.000 |

The suite has no bar in these protocols, but for `frozen_fixed` three
properties fall that should be looked at before any release:
- **spacing_rim** (0.999 → 0.974): swapping a lineup's top shooter for a
  non-shooter more often raises a teammate's rim finishing.
- **handler_conversion** (0.985 → 0.959): removing the top passer more often
  raises the others' shooting.
- **clone_synergy** (0.988 → 0.908): two to four copies of a lineup's
  top-usage player gain more together than separately.

The defensive properties improve (perimeter_coverage 0.658 → 0.732,
coverage_targeting 0.342 → 0.632).

## Part B: confirmation on fresh fits (seeds 23 and 41)

### Fixtures (the declared criterion)

Arm minus seed-matched reference, the two seeds averaged within each
origin, then the mean over 20 origins (origin SE).

| Fixture vs Jokić/Westbrook | Offense | Opponent's offense | Margin |
| --- | ---: | ---: | ---: |
| **Five Goberts** | **+0.6 (0.3)** ✓ | **+1.1 (0.4)** ✓ | −0.5 (0.4) |
| **Legal centers** | **+0.3 (0.3)** ✓ | +1.4 (0.4) | −1.0 (0.3) |
| Legal centers (vs Jokić/Korver) | +0.8 (0.2) | +0.9 (0.5) | −0.1 (0.4) |
| Five Jokićs | +0.1 (0.4) | +1.3 (0.5) | −1.2 (0.3) |

### Lineups no screen looked at (no bar)

| Lineup vs Jokić/Westbrook | Offense | Opponent's offense | Margin |
| --- | ---: | ---: | ---: |
| Limited centers (Bogut, Gobert, Looney, Robinson, Jordan) | −0.9 (0.3) | +3.1 (0.3) | −3.9 (0.4) |
| Five small guards (Paul, Curry, Lillard, Irving, Young) | +0.3 (0.5) | +2.9 (0.3) | −2.5 (0.6) |
| Clone ladder: 1 Gobert | +0.0 (0.5) | −0.3 (0.3) | +0.4 (0.4) |
| 2 Goberts | −0.3 (0.4) | −0.3 (0.4) | +0.1 (0.4) |
| 3 Goberts | +0.1 (0.3) | +0.8 (0.4) | −0.7 (0.4) |
| 4 Goberts | +0.5 (0.3) | +1.1 (0.4) | −0.6 (0.4) |
| 5 Goberts | +0.6 (0.3) | +1.1 (0.4) | −0.5 (0.4) |

- **The clone ladder has the layer's shape.** The module adds nothing up to
  two Goberts. It turns against the lineup at three, then flattens: the held
  range acts like the layer's counts held at three.
- **Big and small lineups both get worse, mostly on defense.** This is
  consistent with the measured effects: rim deterrence saturates with
  several bigs, and small defenders allow more free throws.

### Interactions and accuracy

| | Seed 23 reference | Seed 23 frozen_fixed | Seed 41 reference | Seed 41 frozen_fixed |
| --- | ---: | ---: | ---: | ---: |
| χ²_H (bar ≤ 184) | 260.6 | **170.6** ✓ | 240.2 | **164.1** ✓ |
| χ²_N (bar ≤ the seed's reference) | 1,438 | **1,192** ✓ | 1,384 | **1,193** ✓ |
| Non-additive share | 0.0109 | 0.0196 | 0.0110 | 0.0198 |
| Accuracy vs reference, equal calibration (bar ≥ −0.003 averaged) | — | **−0.0046 (0.0021)**, 5/20 | — | **−0.0069 (0.0029)**, 5/20 |
| Accuracy vs reference, reference's prior calibration | — | −0.0055 (0.0070) | — | −0.0081 (0.0055) |

The two seeds average −0.0057, so **Part B fails the accuracy criterion.**
Seed 17's −0.0019 (Part A) was the favorable draw.

### Post hoc: forward calibration, like for like

Production calibrates forward, so this check calibrates each arm, the
reference included, only from its own earlier 2022+ quarters (expanding,
strictly before each quarter), then scores 2023q1–2026q4 (16 quarters;
`--own-calibration`).

| Arm minus reference r² | Seed 17 | Seed 23 | Seed 41 | Seeds averaged |
| --- | ---: | ---: | ---: | ---: |
| frozen_fixed | −0.0114 (0.0071) | −0.0101 (0.0095) | −0.0070 (0.0079) | −0.0095 (0.0059), 5/16 positive |
| frozen_joint | −0.0121 (0.0068) | | | |
| pairs (co-trained) | +0.0017 (0.0045) | | | |
| pairs_joint (co-trained) | +0.0021 (0.0044) | | | |

**Where the loss comes from.**
- **A level shift.** The frozen module shifts the average forecast of a
  quarter's real lineups by about ±1 point; the SD across quarters is
  1.05–1.14 for each seed. The shift is mostly specific to each fit
  (correlations between seeds −0.06 to 0.46).
- Removing each quarter's shift, computed from forecasts and not outcomes,
  halves the loss to −0.0042 (SE 0.0028).
- **Extra spread.** The remainder is spread that does not predict: the
  forward calibration slope falls from 0.81 to 0.74.

## Reading

1. **Freezing the network fixed the off-support problem.** Every frozen
   variant holds clone bigs' offense within the bar, on fresh seeds too. The
   co-trained network's drift (screen 4) is gone, because the network cannot
   move.
2. **But the module as built is not a pure interaction.** Its bilinear form
   (U g_i)·Σ_j (V g_j) carries main effects whenever the features have a
   nonzero mean:
   - a player's average contribution over his partners;
   - a partner's average effect;
   - a lineup level.

   On a frozen network these terms re-fit what the network already fits,
   and they drift out of sample. In co-training the network absorbs them,
   which is why the co-trained arms keep their accuracy. The bolted-on layer
   avoids them by construction.
3. **The next design follows directly:** center the module's features so
   that only combinations remain. That is [screen 6](nonlinearity_screen6_protocol_2026_10_13.md),
   committed before its fits, with forward-calibrated accuracy added as a
   declared bar.
4. **Confirmation is worth its cost.** Seed 17 alone passed everything
   declared. The fresh seeds caught an accuracy loss that one seed hid.

## Run notes

- Screen 5's Part B was stopped when 5b was declared. Two seed-23
  `frozen_joint` fits had finished; they are not evaluated.
- The frozen-weights check passed at all 60 `frozen_fixed` fits and all 20
  `frozen_joint` fits. A move would have raised an error.
