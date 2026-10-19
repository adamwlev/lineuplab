# A pure-interaction module on the frozen network: protocol — 2026-10-13

Written and committed before any fit of this arm. Adam, 2026-10-13, before
going to sleep: "Feel free to take this further."

## Why

[Screen 5b](nonlinearity_screen5b_protocol_2026_10_13.md) (`frozen_fixed`)
passed its declared Part A criteria, which use in-quarter (oracle)
calibration for accuracy. A post hoc check then calibrated every arm the
way the tool does: forward, from its own earlier quarters only. Under that
calibration it loses real-lineup accuracy. Over the 16 quarters 2023q1–2026q4:

| Own 2022+ calibration, arm minus reference r² | Seed 17 | Seed 23 | Seed 41 | Seeds averaged |
| --- | ---: | ---: | ---: | ---: |
| frozen_fixed | −0.0114 (0.0071) | −0.0101 (0.0095) | −0.0070 (0.0079) | −0.0095 (0.0059) |
| frozen_joint (early-stopped) | −0.0121 (0.0068) | | | |
| pairs, co-trained (screen 1) | +0.0017 (0.0045) | | | |
| pairs_joint, co-trained (screen 4) | +0.0021 (0.0044) | | | |

**Diagnosis.** The frozen module shifts the average level of real-lineup
forecasts by about ±1 point per quarter (SD 1.05–1.14 across quarters).
The shifts are mostly specific to each fit: correlations across seeds run
from −0.06 to 0.46.
- Removing each quarter's level shift, computed from forecasts and not
  outcomes, halves the loss: −0.0095 → −0.0042 (SE 0.0028).
- The rest is spread that does not predict. The calibration slope falls
  from 0.81 to 0.74.

**Reason.** The module is not a pure interaction. Its bilinear form
(U g_i)·Σ_j (V g_j) has main effects whenever the features g have a nonzero
mean:
- a player's average contribution over partners;
- a partner's average effect on everyone;
- a lineup level.

With the network frozen, these terms re-fit player levels and the training
window's level, which the network already fits, and they drift out of
sample. In co-training the network absorbs them. The bolted-on layer avoids
them by construction, using only the part that adding up cannot express.

## The arm: `frozen_pure`

It is `frozen_fixed` (frozen reference, the joint hold, fixed 8 epochs, one
module on each of the five reference checkpoints) with **centered feature
maps**:
- g ← g − ḡ, and h ← h − h̄, before the bilinear products.
- The mean is over the players in each training batch, as batch
  normalization does, with gradient. A running mean (momentum 0.05) is used
  when forecasting and saved with the module.
- U g and V g are then centered too. Given a player, his expected
  contribution over partners is zero to first order, and so is a partner's
  expected effect. Only their combination remains.
- U and P still start at zero, so training starts at the reference exactly.
  The frozen-weights check still applies.

## Criteria

All of screen 5's, plus forward calibration.
1. **Interactions and accuracy.**
   - χ²_H at most 184; χ²_N at most the reference's (1,417 at seed 17).
   - Equal-calibration accuracy at least −0.003 r².
   - **New: own 2022+ forward calibration** (`--own-calibration`; scored
     quarters 2023q1–2026q4): arm minus reference at least −0.003 r².
2. **Fixtures at 20 origins** (primary for pillar 2), as before:
   - five Goberts' offense within +1 per 100 of the reference;
   - legal centers' offense within +1 per 100 of the reference;
   - Jokić/Westbrook's offense against five Goberts above the reference's.
3. **The property suite** at 2026q4, reported. Screen 5b's three
   regressions (spacing_rim, handler_conversion, clone_synergy) are
   compared.

- **Part A:** seed 17, all criteria.
- **Part B:** seeds 23 and 41, fits starting with Part A. All criteria hold
  with the two seeds averaged within each origin; for the χ² criteria, each
  seed must pass.

**Disclosure.** The centering was chosen from the post hoc analysis above,
which included seeds 23 and 41's `frozen_fixed` forecasts. Those seeds'
`frozen_pure` fits are new, and the fix is generic (a zero-mean feature
map) rather than fitted to them, but Part B is not as clean as a never-seen
seed. The reference has no fourth seed. This is now the seventh design on
seed 17.

## What follows

- **If A and B pass:**
  - fits at the release origin (2027q1, three seeds, a new directory; the
    frozen record is untouched);
  - a Python side-by-side with the bolted-on layer on the tool's lineups;
  - a written proposal for Adam. The tool is not changed.
- **If not:** the layer stays and the frozen route closes. The reports say
  so.

## Compute

60 fits of 8 epochs, six at a time, about 1.5 hours. Then measurement,
sweeps, summaries and the forward-calibration check, about 1 hour. Under
six hours.
