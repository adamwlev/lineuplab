# Close-out plan: from research to the tool

Agreed with Adam on 2026-10-12. This is a living plan; STATUS.md says which
step is current. Every step is within Claude's authority unless it is marked
**Adam**.

## Decisions (Adam, 2026-10-12)

- **Forecast.** The tool's forecast is the calibrated network alone, using
  the reference architecture with broadcast defense. The additive half is
  dropped. The trade, printed in the scorecard, is −0.0015 raw r² and
  −0.0006 centered against the half blend on 2016–2026.
- **Capacity.** It is a labeled alternative assumption in the band, never the
  forecast. The era backtest contradicts its defense assumption in range.
- **Modeling.** Accuracy research is closed. Remaining ideas are parked in
  the roadmap.

## Progress (2026-10-12, evening)

| Step | State | What it established |
| --- | --- | --- |
| 1 Release model | Done (`lineups/release.py`) | Reproduces the freeze record to 1e-14. The league-average opponent is the 2026 panel of real fives with 100+ possessions, both sides. |
| 2 Player-seasons | Done (`lineups/players.py`, `scripts/build_player_seasons.py`) | 12,376 player-seasons. A season is the player at the next opening night, the release's own convention, read from the existing era and release stores; no new sweep was needed. |
| 3 Cross-era | Done ([report](../reports/cross_era_2026_10_12.md)) | The declared rule picks **as-was** inputs. Transport keeps 56–66% of in-era centered r². Levels across eras are not validated. Adam chose era-relative as the default, with as-was as a setting. |
| 4 Band | Done in Python (`lineups/band.py`) | Arms R and C. τ is about 3.2 per side and 4.5 on the margin, plus cross-era variance, at 80%. The offense-side arm O failed its in-range test and was dropped ([report](../reports/creation_law_screen_2026_10_12.md)). |
| 5 Explanations | Done in Python (`lineups/explain.py`) | Volume, shot mix, conversion and free-throw channels against the league-average offense; usage against usual share; creation demand against supply. |
| 6 Export and page | Built, not published (`scripts/export_release.py`, `tool/lineup_model.js`, `tool/lineups.html`) | The JS matches Python on 1,200 matchups (both rules, both arms), ratings, bands, reason strings and breakdowns (`tests/test_tool_parity.py`). Checked in Chrome on desktop light and phone dark. Private review copy: https://claude.ai/artifact/WC4QmzeJshrnneQ4HXzk8G. |
| 7 Documents | Done | Scorecard prints the release trade; tool README rewritten. |

## After the close-out (2026-10-13 to 2026-10-15)

| Step | State | What it established |
| --- | --- | --- |
| Combination effects | Done (Adam, 2026-10-13 and 2026-10-14) | The forecast adds the 14 measured effects ([layer](../reports/combination_layer_results_2026_10_13.md)) and half of the centered learned module ([release](../reports/learned_module_release_2026_10_14.md)); the layer is re-measured on top of the module. |
| Overall quality | Done (`scripts/player_values.py`) | Each player-season's linear approximation strength, shown as such. |
| Clean data | Running ([findings](../reports/rescrape_pilot_2026_10_14.md)) | Exact player ids from the re-scraped pages; `nba_pages.possessions`; the legacy chain, library, stores and release rebuilt on it (`scripts/after_download.sh`, `scripts/release_clean.sh`). Target: in the tool by 2026-10-17. |
| Player details and model page | Built, published with the clean release (Adam, 2026-10-15) | `tool/lineups.html` Details sheet; `tool/model.html`. |

## Steps

### 1. Release model

- **Models.**
  - The frozen 2027q1 fits: R and C × seeds 17, 23, 41, each a mixture of
    its last five checkpoints.
  - Each seed's calibration comes from the freeze record.
  - Fits are read only and checked against their hashes in `record.json`.
- **Inputs.** `lineups_store_2027q1_library`: states through 2026-06-13,
  with the library extended to opening night.
- **Code.** `lineups/release.py` (new):
  - load the release;
  - score a matchup: offense, defense and margin, calibrated;
  - return the per-player ledger.
- **Opponent default.**
  - Against a league-average defense, use the existing neutral defense (zero
    standardized defensive inputs).
  - A lineup's defensive rating needs a league-average offense, which is not
    yet defined. Define it as five players at the origin's population
    fallback state, and test it.
- **Acceptance.**
  - Reproduces `freeze/fixtures_vs_average.csv` (R native and calibrated)
    exactly.
  - Margins are antisymmetric, and lineup order does not matter.
  - Tests are in `tests/`.

### 2. Player-season inputs, 2002–2026

- **States.** One origin per season, dated the day after the season's last
  game, built with the ported sweeps (`lineups.states`) on that schedule.
  Each season-end state uses data through that season only.
- **Library.** Merge the era snapshots, the v16 library and the 2027q1
  extension into one table covering 2001-12 to 2026-10-20.
- **Capability lookups.**
  - Each player-season reads its own season-end date, not the release
    cutoff.
  - In origin mode, `Store.batch` uses the normalizer's cutoff for this; it
    gains an explicit query-date override, behind tests.
- **Defaults.**
  - Active players use their 2026 season-end state, which is the 2027q1
    origin state.
  - Historical players default to their season with the most possessions,
    and any season can be picked.
- **Thin-data flag.** Uses library opportunities and rebound n_eff, feeding
  the band's "thin player data" reason.
- **Acceptance.**
  - The 2026 season-end states equal the 2027q1 origin states.
  - Any season-end date that coincides with an existing store origin
    reproduces that origin's states.

### 3. Cross-era check (exploratory, decision-relevant)

This is the one remaining modeling experiment. It decides how historical
player-seasons enter the release model and measures how error grows with era
distance.

- **A, the tool's direction.** The release R model scores real 2007–2013
  lineups:
  - inputs are era-store origin states, against the actual defenses;
  - the baseline is the era backtest R forecasts on identical rows.
- **B.** The era 2013q4 R fits score 2016–2026 lineups:
  - inputs are v16 origin states;
  - the baseline is the saved v16 reference.
- **Input rules, declared before scoring.**
  - *As-was:* raw states through the model's own normalizer.
  - *Translated:* each raw coordinate is shifted by the difference between
    the possession-weighted player means at the model's origin and at the
    player's origin.
  - In both rules, the environment (budget, renewal, league) is the
    model's.
- **Metrics.**
  - Within-quarter correlation and centered r², by season, so each
    comparison has a year gap.
  - Errors on lineups by composition distance (`lineups.support`).
- **Decision rule.**
  - Adopt *translated* if it beats *as-was* on centered r² in both
    directions. Otherwise use *as-was*.
  - The loss per year of gap becomes the band's cross-era term.
- **Cost.** A few CPU hours of ledger evaluation, run detached.

### 4. Uncertainty band (pillar 3)

1. **In support.**
   - The model-error SD of a lineup's underlying rating: residual variance
     minus finite-sample variance, as a function of declared support
     features:
     - a novel five;
     - thin player data;
     - composition-distance percentile.
   - Fit on earlier benchmark seasons; check coverage on later seasons with
     the finite-game test.
2. **Out of support.** The spread among three named assumptions:
   - R, the forecast;
   - C, capacity defense;
   - O, a new offense-side alternative.

   O is a declared hinge beyond the observed range of the lineup's ball
   handling and creation:
   - turnovers rise and assisted conversion falls, with directions and slope
     declared before fitting;
   - it is exactly zero inside support;
   - it must not move any observed lineup.
3. **Cross-era term.** From step 3.
4. **Output.**
   - The point forecast, and a band that grows from the in-support interval
     to cover the assumption spread and the cross-era term.
   - Each widening carries its reason (`lineups.support`, plus "cross-era"
     and "thin player data").
5. **Acceptance.**
   - In-support coverage on held-out seasons is within 1.5 points of
     nominal.
   - The property suite, swap antisymmetry and order invariance hold.
   - Fixtures are reported, not forced.

### 5. Explanations

- **Per player.**
  - Usage and shot-mix shifts against the player's own state ("pushed out
    of usual role").
  - Conversion shifts from the defense.
- **Team channels.**
  - Creation, spacing, rim pressure, turnovers, free throws, rebounding and
    renewal, and defensive coverage.
  - The decomposition telescopes: volume, mix, conversion, free throws (as
    in `scripts/era_diagnostics.py`).
- **Labeling.** The decomposition is labeled as accounting, not causal
  effects (rule of evidence 7).

### 6. Export and page

- **Export (`scripts/export_release.py`).** Written as JSON, with player
  tables quantized:
  - the weights of the 30 networks;
  - normalizer, environment and calibration;
  - the player-season table;
  - support statistics and band tables.
- **JavaScript forward pass.**
  - The event model and its ledger.
  - Parity against Python on at least 1,000 matchups (real, fixtures,
    clones) to 1e-4 points per 100, run under node in the test suite.
- **Page (`tool/`).**
  - Pick ten player-seasons by search, with the defaults from step 2. Team B
    defaults to league average.
  - Shows offense, defense and margin, the band with reasons, and the
    explanation panels.
  - At most 16 MB.
- **Adam.**
  - Publish a private review copy.
  - Later, replace `tool/five.html` and its live URL. The old page carries a
    coverage gate that AGENTS.md now forbids.

### 7. Close-out documents

- STATUS, the scorecard (the network alone as the release, with the printed
  trade), the roadmap, README and a rewritten `tool/README.md`.
- **Adam.** Scoring the 2026–27 prospective test needs the data refresh once
  games are played.

## Order and rough cost

| Step | Depends on | Cost |
| --- | --- | --- |
| 1 Release model | — | half a day |
| 2 Player-season inputs | 1 | half a day to a day, plus state-sweep CPU |
| 3 Cross-era check | 1 (A), the era fits (B) | a day, mostly detached CPU |
| 4 Band | 1, 2, 3 | 1–2 days |
| 5 Explanations | 1 | half a day |
| 6 Export and page | 1–5 | 2–3 days |
| 7 Documents | all | hours |

Step 3 runs in the background while steps 2 and 5 are built. A private review
copy by opening night (2026-10-20) is plausible. A finished public page is
tight.
