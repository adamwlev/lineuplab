# The learned module on fresh quarters: results — 2026-10-14

Results of the [protocol](learned_module_confirmation_protocol_2026_10_14.md),
committed (a3b991f9) before any fit in this era.
- **Era:** 24 scored quarters, 2016q1–2021q4. The 2015 quarters feed
  calibration only.
- **Seeds:** 17, 23 and 41, averaged per row.
- **Script:** `scripts/nonlinearity_screen.py`.
- **Output:** `experiments/cache/nonlinearity_confirm_2026_10_14/`. Driver
  `run_all.sh`; all 84 reference forecasts and 84 module fits exited cleanly.
  Each reference forecast matched the saved one.

## Summary

- **Every declared bar passes at both strengths.** By the decision rule,
  the candidate is the module at **full strength**, centered on the previous
  quarter's lineups.
- **Accuracy at full strength:** +0.0001 (SE 0.0016) against the network
  alone. The bar was −0.003; 12 of 24 quarters are positive.
- **Accuracy at half strength:** +0.0010 (SE 0.0008). Neither is a gain
  beyond noise.
- **Uncentered, the module still costs −0.0058.** That replicates the level
  problem. Centering is what fixes it.
- **Off-support:**
  - Five Goberts' offense is −1.1 (SE 0.4) against the network alone; the
    bar was ≤ +1.
  - Legal centers' offense is −0.2 (0.3).
- **One bar passes in letter only.** Jokić/Westbrook's offense against the
  five Goberts is +0.02 (0.41) (bar > 0). That is effectively zero, so in
  this era there is no evidence that the module adds a crowded-defense
  effect for them.
- **The interactions replicate.** The module removes 28–37% of the held-up
  cells' residual χ². Its learned pattern correlates 0.85 with the actual
  held-up interactions. Seeds agree at 0.83–0.87.
- **Nothing in the tool changed.** Adding the module to the printed number
  is Adam's decision. It also bears on the 2026-10-13 decision of record
  (see the last section).

## Primary: accuracy

Per-quarter points r² is computed on broad offense-five cells
(≥ 50 possessions), possession-weighted, around each quarter's mean. Each
forecast is calibrated forward on its own earlier quarters (expanding from
2015q1). The reference's r² is 0.0925.

| Forecast (seeds averaged) | r² minus reference (SE) | Quarters positive | Bar | |
| --- | ---: | ---: | --- | --- |
| **Full strength, centered** | **+0.0001 (0.0016)** | 12/24 | ≥ −0.003 | pass |
| **Half strength, centered** | **+0.0010 (0.0008)** | 13/24 | ≥ −0.003 | pass |
| Full strength, uncentered | −0.0058 (0.0039) | 11/24 | — | |
| Full strength, level removed using the quarter's own lineups (bound) | +0.0006 (0.0015) | 13/24 | — | |
| Full strength, centered on training rows | −0.0011 (0.0031) | 13/24 | — | |
| Calibrated weight (stacked), centered | +0.0007 (0.0006); weight 0.38 | 14/24 | — | |

Single seeds at full strength, centered: −0.0011 (seed 17), −0.0014
(seed 23) and −0.0020 (seed 41). All are inside the bar.

**Against the exploratory quarters.** On 2023–2026 the same forecast cost
−0.0027. Here it costs nothing.
- The reference is easier to predict in this era: r² is 0.093 against 0.071.
- Neither era shows a gain.

The honest summary across the 40 quarters: centered, the module costs
between nothing and about 0.003.

## Secondary: off-support fixtures (product number at full strength)

Each figure is the product minus the seed-matched reference, seeds averaged
within each origin, mean over 24 origins (SE).

| Fixture vs Jokić/Westbrook | Their offense | Jokić/Westbrook's offense | Margin |
| --- | ---: | ---: | ---: |
| Five Goberts | −1.1 (0.4) ✓ | +0.0 (0.4) ✓ by +0.02 | −1.1 (0.5) |
| Legal pure centers | −0.2 (0.3) ✓ | +2.4 (0.6) | −2.6 (0.6) |
| Five Jokićs | −1.3 (0.3) | +1.1 (0.5) | −2.4 (0.6) |
| Limited centers (untuned) | −0.8 (0.3) | +2.6 (0.4) | −3.5 (0.4) |
| Small guards (untuned) | −0.6 (0.4) | +3.0 (0.3) | −3.6 (0.5) |
| Clone ladder 1 / 3 / 5 Goberts | −0.9 / −0.0 / −1.1 | +1.6 / +3.0 / +0.0 | −2.5 / −3.0 / −1.1 |

At half strength every figure is about half; all bars pass.

**Reading.**
- **The module never inflates an unusual lineup's own offense.** That is
  the pillar-2 property.
- **In this era it raises Jokić/Westbrook's offense** by about 1.5–3 against
  most fixture defenses, but not against the five Goberts.
  - The fixture rosters are fixed at 2026q4. At early origins Murray,
    Porter Jr., Robinson and Allen have little or no data.
  - These margins are therefore off-support behaviour, not a realistic
    matchup.
  - On 2022–2026, with fresh seeds, the same boost was concentrated on the
    unusual defenses: +0.8 against the Goberts, +2.6 to +2.8 against
    limited centers and small guards.

## Interactions on 2016–2021 (no bar)

| Seed | χ²_H, 14 held-up cells: reference → module | χ²_N, 511 others |
| --- | --- | --- |
| 17 | 449 → 281 | 1,324 → 1,128 |
| 23 | 444 → 281 | 1,347 → 1,220 |
| 41 | 453 → 326 | 1,318 → 1,256 |

- **Correlation of the 3-seed learned changes with the actual
  interactions:**
  - 0.85 on the held-up cells, with slope 0.22;
  - 0.28 on the others, with slope 0.10.
- **Agreement between seeds** on the other cells is 0.83–0.87.
- **Share of each held-up effect learned:**
  - free-throw effects 15–41%;
  - rim share 2–23%;
  - three share 12–16%;
  - turnovers −14% to 23%.
- **Caveat on the held-up cells.** They were discovered in this window, so
  their actual coefficients are inflated by selection.

## What this means

The learned route now has a design that meets both requirements on fresh
quarters:
- forward accuracy within the budget (here, no cost at all);
- clone lineups not inflated.

The design is:
- the frozen network;
- a held pairwise module trained on top for a fixed 8 epochs;
- its level removed against the latest real lineups;
- seeds averaged.

**Decisions for Adam.**
1. **The decision of record.** The 2026-10-13 decision says "only effects
   that held up on held-out seasons enter the number." The module's
   interactions on the 14 held-up cells replicate. Its other learned
   structure is real in direction (correlation 0.28–0.52 with actual) but
   not individually validated. Putting it in the printed number means
   amending that decision.
2. **Strength.**
   - Full strength passed and is the rule's candidate.
   - Half strength is safer: about half the off-support shifts, and a
     slightly better point estimate.
3. **The layer.** The module learns about a fifth of each of the layer's 14
   effects. If both enter, the layer is re-measured on the residuals of
   network + module, so nothing counts twice.

**If approved, the work to ship it** (about a day; no data refresh needed):
- fit modules on the release's frozen 2027q1 networks (3 seeds);
- center on 2026q4's lineups;
- re-measure the layer;
- print the trade in the scorecard;
- update the review copy.

The frozen prospective record is not touched.
