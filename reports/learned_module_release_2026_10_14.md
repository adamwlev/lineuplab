# Learned combinations in the release: build — 2026-10-14

Adam's decision of record (2026-10-14): the learned module enters the
forecast at half strength, and the layer is re-measured on top of it. The
design is the confirmed one
([results](learned_module_confirmation_results_2026_10_14.md)). This report
covers putting it into the tool.

## Build

- **Fits.** `scripts/release_module.py` fits one module per seed (17, 23,
  41) on top of the frozen 2027q1 release networks:
  - each network is read only and hash-checked against the freeze record;
  - 8 epochs on the 335,763 final training rows;
  - no network weight moved;
  - output ranges measured on those rows.

  Output: `experiments/cache/release_module_2027q1/`. The frozen prospective
  record is untouched.
- **Levels.** Each module's level on 2026q4's real lineups (22,522 rows,
  inputs as of the origin) is −0.45, +0.70 and −0.72 points per 100. These
  are the fit-specific offsets the confirmation found, and they are removed.
- **Forecast.** It is computed for each seed, then averaged over seeds:
  - per seed: slope × ½ × (network with module − network − level);
  - the result is added to every assumption in the band, like the layer.
  - A new assumption N, "only the 14 measured combinations", keeps the
    unvalidated part inside the range.
  - Code: `lineups/learned.py`, `Release.season_learned*` and
    `Band.with_layer`.
- **Calibration.** The record's per-seed affine is unchanged. The
  confirmation calibrated each forecast on its own history. Here the module
  is centered and halved, so the affine fitted to the network alone carries
  over.

## The layer, re-measured on top

`scripts/combination_layer.py --learned` re-measures the layer. The
residuals are taken against the network plus half the module's forward
event changes: the screens' fits for 2022–2026 and the confirmation's fits
for 2015–2021, seed means. Every effect shrinks a little; the module
already carries part of each.

| Effect (per pairing) | Network alone | On top of the module |
| --- | ---: | ---: |
| Bigs on defense: rim share | +0.62 | +0.55 |
| Shot-blockers × defensive rebounders: rim share | +0.43 | +0.38 |
| Non-shooters × offensive rebounders: three share | +0.40 | +0.37 |
| Bigs on defense: FTA allowed | +0.60 | +0.45 |
| Small defenders: FTA allowed | +0.51 | +0.42 |
| Small × small: FTA drawn | +0.30 | +0.29 |

The other eight effects change by 0.04 or less. The layer's forward check
(fitted on 2016–2021, applied to 2022–2026 game rows) is +0.00003 raw r²
on top of network + module, the same as before.

## What it does to lineups

The values below are against the league-average opponent, era-relative
inputs, in points per 100. Positive defense means more points allowed.

| Lineup | Learned: offense | Learned: defense | Learned: net | Measured: net |
| --- | ---: | ---: | ---: | ---: |
| Timberwolves 2026 | −0.11 | −0.54 | +0.43 | −0.14 |
| Nuggets 2026 (Jokić/Westbrook) | −0.22 | +0.70 | −0.92 | |
| Five legal centers | +0.38 | +1.22 | −0.84 | |
| Five Goberts | +0.47 | +0.61 | −0.14 | −0.08 |
| Five Jokićs | −0.22 | +1.29 | −1.51 | |

- **Five Goberts against the 2017 Warriors:** the learned part moves the
  margin −2.0. All combination effects together move it −1.4.
- **The defensive direction matches the measured effects.** Against five
  Goberts, opponents take +1.1 pp more of their shots at the rim and draw
  +1.5 more free throws per 100.
- **The offenses of the big lineups rise a little.** Five Goberts' offense
  is +0.47, inside the confirmation's +1 bar, and a test pins that bar.

## Tool

- **Browser port.** `tool/lineup_model.js` transcribes the module and
  computes each ledger with and without it.
  - Parity with Python (`tests/test_tool_parity.py`, new cases): points
    within 1e-4, event rates within 1e-6, bands and reasons identical.
  - Speed: the first lineup takes about 3 seconds, as before; later ones
    take 0.3–0.5 seconds.
- **The page.** After Adam's feedback ("I don't think the user will care
  about learned vs measured combination effects"), one "Combination effects"
  section carries both.
  - The totals are learned + measured.
  - Each column opens with the learned row ("every pairing … as the model
    learned it"), with its event changes. The 14 named effects follow.
  - The assumptions table adds "only the 14 measured combinations".
- **Tests.** `tests/test_learned.py` is new. The full suite passes (104
  tests).
