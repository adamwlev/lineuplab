# Pairwise module with a joint bound: screen results — 2026-10-13

Results of [Part A of the protocol](nonlinearity_screen4_protocol_2026_10_13.md),
committed (d4fdd768) before any range was measured. This is an exploratory
screen: one seed (17) at the 20 quarters of 2022–2026, on the `pairs` arm's
weights.
- Script: `scripts/nonlinearity_screen.py`.
- Output: `experiments/cache/nonlinearity_screen_2026_10_13/`
  (`pairs_joint_*`, `screen4_*`, `backbone_diagnostic_pairs_joint.*`).

## Summary

- **Part A fails, so Part B was not evaluated.** Against Jokić/Westbrook:
  - five Goberts' offense is +2.0 (SE 0.7) per 100 above the reference;
  - legal centers' offense is +1.3 (SE 0.6);
  - the bar for both was +1.
- **The joint bound barely binds.** Results are within 0.2 of screen 3
  (+2.1, +1.5). At 2026q4, five Goberts' offensive sum lies at distance 8.30
  against a radius of 8.60. The module's channels are strongly correlated,
  so being at the per-channel bound in ten channels is one direction, not
  ten, and the ellipsoid admits it.
- **Real-lineup gains are kept.** χ²_H is 157 (bar 184) and χ²_N does not
  rise. Accuracy does not move: +0.0005 ± 0.0025 r² with equal calibration.
- **Per the declared rule, the co-trained ("in-network") route stops
  here.** The 40 fresh-seed fits started for Part B were stopped unfinished
  once Part A failed. None of them wrote results.
- **Post hoc, the remaining excess is not in the module.**
  - With the holds, the module's own contribution to the clone-big offense
    is about zero: five Goberts −0.0 (SE 0.4), legal centers −0.1 (0.4).
  - The excess is in the rest of the network, which trains alongside the
    module: +2.0 (0.4) and +1.4 (0.4).
  - This shift is not refit noise. The reference's own seeds 23 and 41
    differ from seed 17 by +0.1 and −0.6 (SE 0.6). It is not the epoch count
    either: it is positive at all 8 origins where both fits picked the same
    epoch.
  - This motivated a different design, declared separately:
    [screen 5](nonlinearity_screen5_protocol_2026_10_13.md), a held module
    trained on the frozen reference.

## Contrast 1: interactions and accuracy

| | reference | pairs | pairs_out | pairs_joint |
| --- | ---: | ---: | ---: | ---: |
| Non-additive share of points-forecast variance | 0.0110 | 0.0193 | 0.0184 | 0.0183 |
| χ²_H, residual, 14 held-up cells (lower = learned) | 253.5 | 153.5 | 156.4 | 156.8 |
| χ²_N, residual, 511 other cells (higher = invented) | 1,417 | 1,136 | 1,135 | 1,136 |
| Accuracy vs reference, equal in-quarter calibration | — | +0.0002 (0.0025) | +0.0005 (0.0025) | +0.0005 (0.0025) |
| Accuracy vs reference, reference's prior calibration | — | −0.0039 (0.0050) | −0.0035 (0.0051) | −0.0035 (0.0050) |

Accuracy is calibrated points r² on outer broad cells: the mean of arm minus
reference over 20 origins, with origin SE. Contrast 1 passes: χ²_H is 2% above
`pairs`, and the bar was 20%.

## Contrast 2 (primary): fixtures at all 20 quarters

Native points per 100: mean over 20 quarters of arm minus reference, with
origin SE.

| Fixture | Side | Reference | pairs | pairs_out | pairs_joint |
| --- | --- | ---: | ---: | ---: | ---: |
| Five Goberts vs Jokić/Westbrook | Goberts' offense | 113.0 | +9.6 (1.4) | +2.1 (0.7) | **+2.0 (0.7)** |
| | Jokić/Westbrook's offense | 107.3 | +8.7 (1.1) | +4.3 (0.7) | +3.7 (0.6) |
| | margin | +5.7 | +0.9 (1.9) | −2.1 (0.8) | −1.7 (0.7) |
| Legal centers vs Jokić/Westbrook | centers' offense | 113.0 | +5.5 (0.9) | +1.5 (0.6) | **+1.3 (0.6)** |
| | Jokić/Westbrook's offense | 112.8 | +5.2 (0.7) | +4.0 (0.6) | +3.9 (0.6) |
| | margin | +0.3 | +0.3 (1.1) | −2.5 (0.7) | −2.6 (0.6) |
| Legal centers vs Jokić/Korver | centers' offense | 114.4 | +6.6 (1.1) | +2.6 (0.7) | +2.4 (0.7) |
| | margin | +0.6 | +2.4 (1.1) | −0.7 (0.7) | −0.7 (0.7) |
| Five Jokićs vs Jokić/Westbrook | Jokićs' offense | 132.8 | +1.6 (0.9) | +0.9 (0.7) | +0.6 (0.6) |
| | margin | +20.6 | −1.1 (0.8) | −1.7 (0.5) | −2.0 (0.4) |

**By the declared criterion, the arm fails.** Both named offenses exceed +1.
The defensive direction is kept.

## Contrast 3: property suite at 2026q4

| Property | Reference | pairs | pairs_joint |
| --- | ---: | ---: | ---: |
| spacing_rim | 0.999 | 0.994 | 0.995 |
| handler_turnovers | 0.410 | 0.374 | 0.374 |
| handler_conversion | 0.985 | 0.985 | 0.985 |
| handler_teammate_turnovers | 1.000 | 0.995 | 0.995 |
| clone_synergy | 0.988 | 0.921 | 0.904 |
| rim_synergy | 1.000 | 1.000 | 1.000 |
| rebound_synergy | 1.000 | 1.000 | 1.000 |
| perimeter_coverage | 0.658 | 0.763 | 0.763 |
| coverage_targeting | 0.342 | 0.574 | 0.574 |
| permutation | 1.000 | 1.000 | 1.000 |

## Post hoc: where the remaining excess sits

From `--backbone-diagnostic`. The arm's fixture offenses are recomputed with
its module switched off (`model.pairs = None`) at every origin. This is an
accounting split of the arm's change, not a causal effect.

| Fixture, side | Arm vs reference | Co-trained network alone | Module (held) |
| --- | ---: | ---: | ---: |
| Five Goberts' offense | +2.0 (0.7) | +2.0 (0.4) | −0.0 (0.4) |
| Jokić/Westbrook's offense vs Goberts | +3.7 (0.6) | +1.8 (0.5) | +1.9 (0.4) |
| Legal centers' offense | +1.3 (0.6) | +1.4 (0.4) | −0.1 (0.4) |
| Jokić/Westbrook's offense vs centers | +3.9 (0.6) | +1.7 (0.4) | +2.2 (0.3) |
| Five Jokićs' offense | +0.6 (0.6) | +1.2 (0.5) | −0.6 (0.4) |
| Jokić/Westbrook's offense vs Jokićs | +2.6 (0.6) | +1.5 (0.4) | +1.0 (0.5) |

**Is the network shift just a different fit?** Two controls say no.
- *Training parity:* refitting the reference with the same trainer
  reproduces it (2020q1/s17: weights within 1.2e-6, the same selected
  epoch; docs/REFACTOR.md, rung 4a). So the shift comes from training
  alongside the module.
- *Seed spread:* the reference's own seeds, fixture sweep at the same 20
  quarters (`screen4_reference_s23/s41.*`):

  | Seed 23 or 41 minus seed 17 | Five Goberts' offense | Legal centers' offense |
  | --- | ---: | ---: |
  | Seed 23 | +0.1 (0.6) | +0.4 (0.4) |
  | Seed 41 | −0.6 (0.6) | +0.1 (0.5) |

  A fit-to-fit difference averages out over 20 quarters (per-quarter SD
  about 2.5). The co-trained shift of +2.0 (SE 0.4) does not.
- *Epochs:* the pairs fits chose the same epoch as the reference at 8 of 20
  quarters. The network shift is positive at all 8 (mean +1.5).

**Reading.** The holds now do their job on the module. The leftover
optimism is the familiar selection-on-the-outcome hazard, entering through
the shared weights. Training the network jointly with a module that explains
part of the real-lineup interactions frees the rest of the network to fit
differently. That change carries off-support, where no bound on the module
reaches it.

## What follows

- **The tool keeps the bolted-on layer.**
- **The co-trained route stops,** by the declared rule.
- **The fifth design** freezes the network and trains only the held module
  ([protocol](nonlinearity_screen5_protocol_2026_10_13.md), committed
  before any fit). With the module at zero it equals the reference, so its
  effect is the module's alone. It is a learned counterpart of the layer.

## Run notes

- **The first Part A/B queue launch was malformed.** An unsplit shell
  variable produced broken lines. It was stopped within a minute, before
  any arm wrote output, and its stray argparse logs were removed. It was
  relaunched with a correct queue.
- **The Part B fits were stopped** after Part A failed. Seven had started;
  none finished or wrote outputs.
