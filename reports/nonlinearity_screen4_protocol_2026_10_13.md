# Pairwise module with a joint bound, and its fresh-seed confirmation: protocol — 2026-10-13

Written and committed before any range is measured, any forecast is made, or
any fresh-seed fit starts. Adam approved continuing on 2026-10-13: "I'd like
to keep going. I think we're on to something."

This document declares two things:
- **Part A:** a fourth exploratory screen on seed 17.
- **Part B:** the confirmation that decides whether a Part A pass means
  anything.

## Why

| Screen | Hold | Five Goberts' offense vs reference (bar +1) |
| --- | --- | ---: |
| [1](nonlinearity_screen_results_2026_10_13.md) | none | +9.6 |
| [2](nonlinearity_screen2_results_2026_10_13.md) | inputs (partner sums) | +7.1 |
| [3](nonlinearity_screen3_results_2026_10_13.md) | outputs, per channel | +2.1 (SE 0.7) |

In screen 3, each clone fixture sat at its lineup bound in 10 of 15 channels
at once, against 0.11% of real lineups. Per-channel bounds cannot express "no
more unusual than real lineups" jointly. An ellipsoid can.

## Part A: the arm `pairs_joint` (seed 17)

- **Weights.** The `pairs` arm's saved checkpoints, as in screen 3; there is
  no refit.
- **Holds, in order, when forecasting:**
  1. The screen 3 holds, unchanged: each player's offensive outputs per
     channel, then the lineup sum per channel, then the defensive shift per
     channel.
  2. **The joint bound.** It applies separately to the lineup's 15-channel
     offensive sum T and to the 15-channel defensive shift.
     - The distance is d(T) = √(Tᵀ M⁻¹ T). M is the second moment of T over
       the checkpoint's training rows, measured after step 1, with a 10⁻⁶
       relative ridge.
     - The radius r is the 99.5% quantile of d over those rows.
     - If d > r, all of the lineup's outputs (five players, 15 channels) are
       scaled by r / d. The defensive shift is treated the same way.
- **Properties of the bound.**
  - The ellipsoid is centered on no interaction, so a lineup with no
    interaction is never moved.
  - Each lineup keeps the direction of its effect and each player's share.
  - It is a shape constraint on the module's own outputs and names no lineup
    or player.
- **Criteria.** As in screens 2 and 3.
  1. **Interactions and accuracy.** χ²_H no more than 20% above `pairs` (at
     most 184); χ²_N and accuracy reported.
  2. **Primary: fixtures at all 20 origins.** Success requires all of:
     - five Goberts' offense against Jokić/Westbrook within +1 per 100 of the
       reference on average;
     - legal centers' offense against Jokić/Westbrook within +1 per 100 of
       the reference on average;
     - Jokić/Westbrook's offense against five Goberts above the reference's
       on average.
  3. **The property suite** at 2026q4.
- **A Part A pass is not the result.** This is the fourth variant tried on
  seed 17, with the criteria known. A pass licenses Part B; it does not
  establish anything by itself.

## Part B: confirmation on fresh fits (run only if Part A passes)

- **Fits.** The `pairs` arm refit with seeds 23 and 41 at all 20 origins:
  40 fits under the identical protocol.
  - The reference has saved fits for these seeds, so each comparison is
    seed-matched.
  - These fits start now, before Part A results exist, so neither their
    training nor their selection can respond to Part A.
- **Arm.** `pairs_joint` exactly as in Part A, measured on each fit's own
  training rows.
- **Primary criterion.** Part A's three conditions.
  - For each origin, arm minus seed-matched reference is averaged over the
    two seeds. Then the mean is taken over 20 origins, with the origin SE.
  - **Confirmation requires all three.**
- **Also required.** χ²_H no more than 20% above the same seeds' `pairs`,
  and equal-calibration accuracy no worse than −0.003 r² on average over
  the two seeds.
- **Reported without a bar, because the screens never looked at them.**
  These are lineups' offense and margin against Jokić/Westbrook, vs the
  reference, on the fresh seeds:
  - limited centers (Bogut, Gobert, Looney, Robinson, Jordan);
  - five small guards (Paul, Curry, Lillard, Irving, Young);
  - the Gobert clone ladder with one to five Goberts.
- **What a confirmation licenses.** A proposal to Adam: three-seed fits at
  the release origin and a side-by-side with the bolted-on layer in the
  review copy. The tool's printed number does not change without his
  decision.
- **If Part A or Part B fails,** the in-network route stops here and the
  layer stays. The reports say so.

## Compute

- Part A: about 20 minutes (measuring and forecasting only).
- Part B: 40 fits of about 8–13 minutes, seven at a time, about 1.5 hours.
  Then measurement, the sweep and the summaries, about 30 minutes.

Everything is well under the six-hour limit.
