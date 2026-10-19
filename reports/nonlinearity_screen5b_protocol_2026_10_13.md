# Frozen-network module trained for fixed epochs (screen 5, variant b): protocol — 2026-10-13

Written and committed before any outcome of [screen 5](nonlinearity_screen5_protocol_2026_10_13.md)
was looked at: no fixture, accuracy, interaction or property result. Only
the training logs' loss curves were read.

## Why

Adam asked why screen 5's early stopping kept only 1–2 epochs ("maybe we
need to lower the learning rate? Or more patience? That seems off"). The
inner curves at five origins (2022q2, 2023q1, 2024q2, 2025q3, 2026q4)
answer it:
- **Training loss falls steadily** through 10–14 epochs, for example
  1.24497 → 1.24401 at 2022q2.
- **The validation objective on the one inner quarter is flat**, wobbling
  about ±0.0005 around its epoch-1 value. It does not rise after epoch 1,
  which is what a learning rate that is too high would show.

So early stopping picks an epoch from noise:
- a single validation quarter cannot resolve gains this small;
- a lower learning rate would only flatten the curve;
- more patience would only keep picking the lowest wobble.

The fix is to stop letting a noisy curve choose.

## The arm: `frozen_fixed`

It is identical to `frozen_joint` except for training length.
- **Training.** The module trains for a fixed **8 epochs** on the origin's
  final training rows, against the frozen saved final reference, with the
  reference's saved loss references. There is no inner phase, because no
  epoch is selected.
- **Why 8.** It is the co-trained `pairs` arm's median selected epoch in the
  first screen, fixed before seeing any frozen-module outcome.
- **Overfitting.** The validation curves show no rise through 10–14 epochs,
  so 8 epochs should not overfit.
- **Unchanged from `frozen_joint`:**
  - the holds: per channel, then the 99.5% joint ellipsoid, measured on the
    final training rows;
  - one module from the final epoch on each of the reference's five
    checkpoints;
  - the frozen-weights check.

## Criteria and confirmation

The criteria and the confirmation design are exactly those of the
[screen 5 protocol](nonlinearity_screen5_protocol_2026_10_13.md):
- **Part A** on seed 17, with the same three contrasts and bars.
- **Part B** on seeds 23 and 41, evaluated only if Part A passes. Its fits
  start with Part A.
- The untuned lineups (limited centers, five small guards, clone ladder) are
  reported without a bar.

## What happens to screen 5 as first declared

- Its Part A (seed 17, early-stopped) finishes and is reported as declared,
  next to this variant.
- Its Part B was stopped when this variant was declared. Two seed-23 fits
  had finished; they are not evaluated. The confirmation goes to the variant
  that would be used, which is this one, because early stopping on one
  quarter is not informative here.
- **Bookkeeping.** This is now the fifth design on seed 17. Only a Part B
  confirmation on fresh seeds counts.

## Compute

60 fits of 8 epochs, each about 7–10 minutes with seven at a time, plus
the 40 reference rebuilds for seeds 23 and 41: about 1.5 hours. Then
measurement, sweeps and summaries. Under six hours.
