# A learned, held combination module on the frozen network: protocol — 2026-10-13

Written and committed before any fit starts. Adam, 2026-10-13: "I'd like to
keep going. I think we're on to something. Let's keep going as long as
you're ok with it."

## Why this is a new design, not a fifth bound

The [fourth screen](nonlinearity_screen4_results_2026_10_13.md) failed, and
its declared rule stops the co-trained ("in-network") route. Its post hoc
split points somewhere else. With the module held, the module's own
contribution to the clone-big offense is about zero: five Goberts −0.0 ± 0.4,
legal centers −0.1 ± 0.4.
- The remaining excess (+2.0 ± 0.4 for five Goberts) is in the rest of the
  network, which trained differently alongside the module.
- It is not refit noise. The reference's own seeds 23 and 41 differ from
  seed 17 by +0.1 and −0.6 (SE 0.6).
- It is not the epoch count. It is positive at all 8 origins where both fits
  chose the same epoch.

So this design freezes the network and trains only the held module. It is a
learned counterpart of the bolted-on layer:
- it is fit to the network's own residual, as the layer is;
- by gradient descent on the full likelihood;
- from the same identity-free capability inputs;
- held at its measured range, as the layer is held at measured counts.

## Part A: the arm `frozen_joint` (seed 17)

- **Network.** The saved seed-17 reference at each origin, frozen.
  - The module is trained in the inner phase against the reference's saved
    inner state, and in the final phase against its saved final state.
  - A run is invalid if any network weight in its final state differs from
    the saved reference. This is checked.
- **Module.** `PairInteractions(hold="joint")`, with the same
  initialization as the `pairs` arm.
  - U and P start at zero, so training starts at the reference exactly.
  - Only the module trains: no decay on it, the reference's FitConfig, and
    early stopping on the inner validation (unclamped, as in screens 3 and
    4).
- **Holds.** As in the fourth screen: per player and per lineup channel,
  then the joint ellipsoid at 99.5%. They are measured on the final training
  rows.
- **Forecast.**
  - The module's final-epoch state is added to each of the reference's five
    checkpoints, and the five are averaged as the reference is.
  - The module reads only lineup inputs, so its outputs and ranges do not
    depend on the checkpoint.
  - With the module at zero, the forecast *is* the reference. So arm minus
    reference is the module's effect alone.
- **Criteria**, as in screens 2–4:
  1. **Interactions and accuracy.** χ²_H at most 184 (20% above `pairs`).
     χ²_N no higher than the reference's. Equal-calibration accuracy no
     worse than −0.003 r².
  2. **Primary: fixtures at all 20 origins.** All three must hold:
     - five Goberts' offense against Jokić/Westbrook within +1 per 100 of
       the reference on average;
     - legal centers' offense against Jokić/Westbrook within +1 per 100 of
       the reference on average;
     - Jokić/Westbrook's offense against five Goberts above the reference's
       on average.
  3. **The property suite** at 2026q4.
- **A Part A pass is not the result.** It licenses Part B.

## Part B: confirmation on fresh fits (evaluated only if Part A passes)

- **Fits.** The same arm on the reference's seeds 23 and 41 at all 20
  origins, each on its seed-matched frozen reference. These 40 fits start
  together with Part A, so they cannot respond to its results.
- **Confirmation requires, averaged over the two seeds per origin:**
  - Part A's three fixture conditions;
  - χ²_H at most 20% above the first screen's `pairs`, and no higher than
    the seed-matched reference's χ²_N;
  - equal-calibration accuracy no worse than −0.003 r².
- **Reported without a bar.** Offense and margin against Jokić/Westbrook,
  vs the reference, for limited centers, five small guards and the Gobert
  clone ladder (one to five).
- **If confirmed:**
  - I propose fits at the release origin (2027q1, three seeds) and a
    side-by-side with the bolted-on layer in the review copy.
  - The module's pairwise form gives per-pair contributions, so it can
    explain itself pair by pair, as the layer does.
  - The printed number changes only by Adam's decision.
- **If Part A or B fails,** the layer stays and the learned route closes.

## Compute

Sixty module-only fits, each about 4–10 minutes (only the module's
gradients), seven at a time: about 1–1.5 hours. Then measurement, sweeps,
summaries and the property suite. Well under six hours.
