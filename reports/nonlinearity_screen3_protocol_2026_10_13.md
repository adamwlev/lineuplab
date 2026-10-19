# Pairwise module held at its measured outputs: screen protocol — 2026-10-13

Written and committed before any range is measured or any forecast is made.
Adam approved it on 2026-10-13 ("Yeah let's keep going"). It follows the
[second screen](nonlinearity_screen2_results_2026_10_13.md) and is
exploratory: one seed, the same 20 origins and the same script
(`scripts/nonlinearity_screen.py`), with output in the same directory.

## Why

Clamping the module's inputs (each player's partner sum) failed. Five
Goberts' offense stayed +7.1 per 100 above the reference over 20 quarters;
the bar was +1. Post hoc, there were two reasons:
- the output is a product of a player's own features and his partners', so
  it leaves the real range even when each factor stays inside it;
- every player in a clone lineup receives the effect.

This arm holds the outputs directly, per player and per lineup.

## The arm: `pairs_out`

- **Weights.** The `pairs` arm's saved checkpoints; there is no refit.
  - Early stopping is as in `pairs` (validated without the hold).
  - A refit with the hold active during validation could differ only in the
    selected epoch. In the second screen that happened at 1 of 20 origins.
- **Measured ranges.** One set per checkpoint, from that origin's final
  training rows: the rows the weights were fit on (five-year lookback), with
  inputs built as in training. Each range is the unweighted 0.5% and 99.5%
  quantile over rows, per channel, of:
  - each player's 15 offensive pair outputs (bounded log-rate/logit
    corrections);
  - their sum over the lineup;
  - the defensive lineup shift (15 channels).

  The lineup and defense ranges are widened to include 0, so a lineup with
  no interaction is never moved.
- **Forecasting.**
  - Each player's offensive outputs are clamped per channel.
  - If a channel's lineup sum is still outside its range, all five players'
    outputs in that channel are scaled by one common factor, so the sum
    lands on the nearer bound. This does not depend on order and keeps each
    player's share.
  - The defensive shift is clamped per channel.
- **Not a gate.** This is a shape constraint on the module's own outputs,
  declared before measuring. It names no lineup or player and is the
  analogue of the layer's held counts: "no more combination effect than real
  lineups showed."

## Contrasts

The criteria are those of the second screen.

1. **Interactions and accuracy** (χ²_H, χ²_N, accuracy under both
   calibrations), against the reference and `pairs`.
   - About 1% of real player outputs per channel are clamped, so the gains
     may be slightly smaller than `pairs`.
   - If χ²_H is more than 20% worse than `pairs` (above 184), the hold is
     costing real interactions.
2. **Pillar 2 (primary).** Fixture margins and both offenses at every one of
   the 20 origins, for the reference, `pairs` and `pairs_out`. Reported: the
   mean over origins of arm minus reference, with origin SE.
   - **Success requires all of:**
     - five Goberts' offense against Jokić/Westbrook within +1 per 100 of
       the reference on average;
     - legal centers' offense against Jokić/Westbrook within +1 per 100 of
       the reference on average;
     - Jokić/Westbrook's offense against five Goberts above the reference's
       on average (the defensive direction kept).
   - The origin SE of these differences was about 1 point in the second
     screen. The bar is a point criterion, not a demonstrated bound.
3. **The property suite** at 2026q4 for the reference, `pairs` and
   `pairs_out`.

Files are written under new names (`screen3_*`), so the second screen's
outputs are not modified.

## What follows

If `pairs_out` keeps the real-lineup gains and passes contrast 2, the next
step is a three-seed fit at the release origin and a side-by-side with the
bolted-on layer in the tool. That is Adam's call, and nothing here changes
the tool.

## Compute

No training. For each of the 20 origins: one pass of the pair module over
about 330,000 training rows for five checkpoints, plus the outer forecast.
Then the sweep and the property suite. About an hour in total.
