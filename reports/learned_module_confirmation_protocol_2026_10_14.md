# The learned module on fresh quarters: protocol — 2026-10-14

Committed before any module fit in this era. Confirmatory for the accuracy
contrast; the rest is secondary.
- Script: `scripts/nonlinearity_screen.py` (`--era`, `--out`).
- Output: `experiments/cache/nonlinearity_confirm_2026_10_14/`.

## Why

Adam (2026-10-14): "I will accept some decrease in accuracy for those learned
nonlinear effects … maybe we need some calibration on top? either way let's
continue". The frozen module learns real interactions, about a fifth of each
measured effect
([post hoc](nonlinearity_frozen_learned_2026_10_14.md)). Its −0.01 forward
cost was mostly a fit-specific level.

Exploratory trade curve (post hoc on the screens' own 16 quarters,
2023–2026). Each forecast is calibrated forward on its own earlier quarters,
with seeds 17, 23 and 41 averaged:

| Module in the forecast | r² minus reference (SE) |
| --- | ---: |
| Full strength, raw | −0.0059 (0.0055) |
| Full strength, level removed using the quarter's own lineups (bound) | −0.0029 (0.0028) |
| **Full strength, centered on the previous quarter's lineups** | **−0.0027 (0.0027)** |
| **Half strength, centered on the previous quarter's lineups** | **−0.0007 (0.0012)** |
| Calibrated weight (stacked), centered | −0.0007 (0.0006); weight 0.23 |

- **The cost grows with the square of the strength.** At no strength does it
  improve accuracy.
- **Most of the cost is systematic.** Single seeds average −0.0037 at full
  strength against −0.0027 for three seeds, so more fits would not help much.
- These quarters chose the design, so it needs fresh ones.

## The candidate forecast (frozen now)

- **Network:** the saved reference at each origin, three seeds (17, 23, 41)
  of five checkpoints each, frozen.
- **Module:** `frozen_fixed` as in screen 5b, unchanged:
  - joint hold;
  - fixed 8 epochs;
  - trained on top of each seed's network.
- **Centering:** subtract the module's possession-weighted level on the
  previous quarter's rows, with inputs as of the origin (`--prior-level`),
  per seed. It uses no outcomes and nothing after the origin. In the tool it
  reads: the module's effect relative to the league's current lineups.
- **Strength s ∈ {1, ½}:** native = network + s × (module − level).
- **Calibration:** affine, on each forecast's own earlier quarters
  (expanding), per seed; seeds averaged per row (`--stacked-calibration`,
  the "previous-centered scale" rows). The reference is calibrated the same
  way.

## Era

- **Origins:** 2015q1–2021q4, 28 quarters. The four 2015 quarters only feed
  calibration.
- **Scored:** 2016q1–2021q4, 24 quarters.
- **No nonlinearity screen used them.** The reference network was developed
  on a 2016–2026 benchmark, which is common to both arms. 2016–2021 was the
  interaction study's discovery window.
- **Smoke tests before freezing:**
  - one reference forecast at 2016q1 (no outcomes read);
  - reference fixture values at 2016q1 and 2018q1.

## Primary contrast and bar

- **Contrast:** forward-calibrated points r² per quarter. Rows are broad
  offense-five cells (≥ 50 possessions); possession-weighted; around the
  quarter's mean. The figure is arm minus reference, averaged over the 24
  quarters, with SE over quarters.
- **Bar:** ≥ −0.003, the decision-of-record budget.
- **Decision rule:**
  - the candidate is the larger s that passes this bar and the fixture bars
    below;
  - if neither passes, the learned module does not enter the forecast.
- **Power:**
  - At full strength the expected cost is about −0.0027, with an SE of about
    0.0022 on 24 quarters. It is close to a coin flip.
  - At half strength (about −0.0007, SE about 0.001) a pass is likely.
  - The bar is on the point estimate, as in the screens.

## Secondary bars (pillar 2)

Each figure is the product number (centered, at each s) minus the
seed-matched reference. The three seeds are averaged within each origin, then
averaged over the 24 scored origins (`--confirm` plus `product_fixtures`):

- five Goberts' offense against Jokić/Westbrook ≤ +1;
- legal centers' offense ≤ +1;
- Jokić/Westbrook's offense against the five Goberts > 0.

Raw (uncentered) values are reported beside them.

The fixture rosters are fixed at 2026q4. At early origins some players
(Murray, Porter Jr., Robinson, Allen) have little or no data and enter with
default features. This is an off-support test, not a realistic matchup.

## Reported without a bar

- **Interactions on 2016–2021:**
  - χ²_H and χ²_N, reference against the arm;
  - the correlation of the learned changes with the actual interactions;
  - agreement between seeds.

  The held-up cells were discovered in this window, so their actual
  coefficients are inflated by selection.
- **Untuned lineups** (`--confirm`).
- **Single-seed and stacked variants.**

## Not decided here

- **The printed number does not change on a pass.** Adam decides that.
- **Combining with the combination layer also needs a decision.** The
  module learns part of the layer's 14 effects, so the layer would be
  re-measured on the residuals of network + module.
- **Uncertainty is out of scope.**
