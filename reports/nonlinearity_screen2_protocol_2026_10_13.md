# Pairwise module held at the measured range: screen protocol — 2026-10-13

Written and committed before the arm is trained. Adam approved it on
2026-10-13 ("Great yeah let's give it a try"). It follows the
[first screen](nonlinearity_screen_results_2026_10_13.md) and is exploratory:
one seed, the same 20 origins and the same script
(`scripts/nonlinearity_screen.py`), with output in the same directory.

## Why

The pairwise module learned real interactions on real lineups (χ²_H 254 →
154) without inventing (χ²_N fell), at no accuracy cost. But it carried
bigs-together offense to five Goberts: offense 123 → 134, FTA 34 → 48 per
100. The bolted-on layer avoids this by holding type counts at the measured
maximum. This arm gives the module the same structure, declared before
fitting.

## The arm: `pairs_held`

This is `PairInteractions(hold=True)`; everything else is as in `pairs` (no
decay, the same seeds and protocol).
- **What is held.** Each player's partner sum, Σ_{j≠i} V g_j on offense and
  Σ_{j≠l} Q h_j on defense, per component, is clamped to its measured range.
  That is the continuous analogue of "at most three of a type measured
  together".
- **Measured range.** The 0.5% and 99.5% quantiles over training rows, kept
  as running values during training (exponential average of batch quantiles,
  momentum 0.05, stored with each checkpoint).
- **When.** The clamp applies in forecasting (eval mode). Training rows are
  real lineups and lie inside the range by construction.
- **Defense.** The lineup shift is written per defender, so the clamp has a
  meaning:
  ½ Σ_l Σ_r (P h_l)_r · clamp(Σ_{j≠l} (Q h_j)_r).
  Unclamped, it equals the first screen's form.
- **Not a gate.** This is a shape constraint on the module's own inputs,
  declared before fitting, the same as the layer's held counts. It names no
  lineup or player.

## Contrasts

1. **Interactions and accuracy:** as in the first protocol (χ²_H, χ²_N,
   accuracy under both calibrations), against the reference and against
   `pairs`.
   - Expected: about the same as `pairs`, since the clamp rarely binds on
     real rows.
   - If χ²_H is more than 20% worse than `pairs`, the clamp is costing real
     interactions.
2. **Pillar 2 (primary for this arm).** The four fixture margins and the
   attacking offense at **every one of the 20 origins**, for the reference,
   `pairs` and `pairs_held` (single-quarter fixtures are noisy; the reference
   itself swings by several points across origins).
   - Reported: the mean over origins of arm minus reference, with origin SE.
   - **Success:** five Goberts' and legal centers' offense against
     Jokić/Westbrook no higher than the reference's on average (mean
     difference ≤ +1 point per 100), and the defensive direction kept.
3. **The property suite** at 2026q4 (lineups.properties) for the reference,
   `pairs` and `pairs_held`.

## What follows

If `pairs_held` keeps the real-lineup gains and passes contrast 2, the next
step is a three-seed fit at the release origin and a side-by-side with the
bolted-on layer in the tool. That is Adam's call, and nothing here changes
the tool.

## Compute

20 fits of about 8 minutes, five at a time, plus fixture and property-suite
inference: about 45 minutes.
