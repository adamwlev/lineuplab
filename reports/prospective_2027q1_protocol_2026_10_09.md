# Prospective 2026–27 test: protocol — FROZEN 2026-10-12

**Status: frozen on 2026-10-12, before any 2026–27 game.** The record is
below. Nothing in this protocol, the fits, the calibrations or the scorer
changes from here on. Any later analysis is labeled post hoc. Scoring needs the 2026–27 data
refresh, which needs Adam's go-ahead.

## Why

Every result so far is a backtest on 2016–2026, a window that years of
research decisions have already seen. A forecast frozen before any 2026–27
game is the only evidence that has not been seen. Opening night is Tuesday,
2026-10-20.

## Inputs

- **Store.** `experiments/cache/lineups_store_2027q1_library`, built by
  `scripts/build_prospective_store.py --library-extension` from data through
  2026-06-13:
  - origin 2027q1, starting 2026-10-20;
  - states as of opening night;
  - prefix normalizers and environment;
  - the capability library extended past 2026-03-02 with the legacy chain
    code (`scripts/library_extend.py`), so origin queries read a 2026-10-20
    snapshot.

  The first store, `lineups_store_2027q1`, stops the library at 2026-03-02.
  That costs about 0.007 r² in backtests
  ([preparation report](prospective_preparation_2026_10_09.md), section 3), so
  it is not used.
- **Players without history.** Rookies and others without history get the
  origin's population fallback state (neural arms) or count as the average
  player (arm A).
- **Team changes don't matter.** Inputs are player states, not teams.

## Arms (frozen before tip-off)

| Arm | Model | Training |
| --- | --- | --- |
| R | Reference architecture (broadcast defense, J_POINT_BOTH) | two-phase from scratch, seeds 17, 23, 41 (`scripts/prospective_fit.py`) |
| C | CapacityDefense version 2 | two-phase from scratch, seeds 17, 23, 41 (`scripts/prospective_fit.py`) |
| A | additive_defense (`lineups.additive`) | as-of ridge snapshot fitted on every possession before 2026-10-20 (`scripts/additive_origin_fit.py`, legacy code) |

- **Why two-phase.** It is the only way to train at an origin without v14
  parents. At four backtest origins it matched or beat the reference (mean
  +0.0017 half r²), and self-references reproduced the saved-reference fits
  ([preparation report](prospective_preparation_2026_10_09.md), section 1).
- **Fit references.** Each phase is normalized by its own starting model
  (`lineups.train.self_references`).
- **Calibration of R and C.** For each arm and seed, the prior-only affine
  (`lineups.evaluate.affine`) on every 2015–2026 quarter's broad cells. It
  uses the architecture's checkpoint-average history: the saved J_POINT_BOTH
  fits for R, and the confirmatory capacity run for C. League is arm A's
  dated league level at 2026-10-20.
- **Arm A.** Arm A is fixed by:
  - the snapshot;
  - centering on exposure before 2026-10-20;
  - its three stacked calibrations on 2015–2026 cells.

  `lineups.additive` reproduces the saved per-row additive_defense to 5e-13
  at the origins checked.
- **Primary forecast: the neural model alone.** Each arm's calibrated
  forecast, with seeds averaged per row.
  - Adam's direction (2026-10-12): pillar-2 fixes come more easily through
    the neural model alone, and the additive half need not be permanent. In
    the half blend, half of any change the neural model makes at the extremes
    is cancelled by the additive half, which is linear in copies of a player.
  - In the 2016–2026 backtest the neural model alone loses 0.0015 pooled r²
    to the half blend (reference), and −0.0006 per quarter in centered r².
- **Half blends** (secondary). 0.5 × A + 0.5 × the arm's calibrated forecast.

## Population and contrasts (scored after the refresh)

- **Primary population.** The realized 2027q1 window, defined as the first
  300 league games.
  - Cells: offense fives with at least 50 possessions.
  - Forecasts use the actual defenses faced.
  - Results are possession-weighted, in points per 100 possessions.
- **Secondary population.**
  - *Whole season:* every 2026–27 regular-season game, forecast with the
    same opening-night models, states and calibrations, and scored per
    quarter-window cell. This uses only opening-night information and needs
    no refit. It is stale for later quarters, but equally so for every arm.
- **Primary metric: centered r².** This is r² after each forecast's own
  possession-weighted mean error over the population is removed, so it
  measures how well a forecast ranks and separates lineups. A single
  quarter's raw r² is dominated by one level miss. For example, at 2026q1
  the reference was 5.2 points too low on average, while ranking better than
  A (correlation .323 vs .295). Raw r² and the mean bias are reported beside
  every centered value.
- **Primary contrast 1.** Centered r², R (neural model alone) vs A: does the
  neural model's edge hold prospectively?
- **Primary contrast 2.** Centered r², C vs R (both the neural model alone),
  with non-inferiority at −0.003.
- **Secondary.** The same contrasts for the half blends, and raw r² and bias
  for every forecast.
- **Uncertainty.** A game-level block bootstrap: 1,000 resamples of games
  within the population, on the observed cells.
  - Each contrast's interval comes from the resampled difference in
    (centered) mean squared error, divided by the observed outcome variance.
  - Recomputing r² per resample would shrink every difference toward zero.
  - One quarter is one season-block, so these are not season-level SEs.
- **Scorer.** `scripts/prospective_score.py`, committed before the freeze.
  Its `--dry-run` reproduces the 2026q4 scorecard values for the reference
  (calibrated .1104, half .0972) and additive_defense (.0728).
- **Expectations from the backtest** (2016–2026, per quarter, centered r²;
  `scripts/nn_alone_check.py`, which is post hoc to the confirmatory run):

  | Contrast | Quarters | Mean | SD | Positive |
  | --- | --- | ---: | ---: | ---: |
  | R alone − A | all 44 | +0.012 | 0.025 | 32 |
  | R alone − A | opening 11 | +0.025 | 0.014 | 11 |
  | C alone − R alone | all 44 | −0.0024 | 0.0064 | 17 |
  | C alone − R alone | opening 11 | −0.0040 | 0.0073 | 3 |
  | R half − A | opening 11 | +0.021 | 0.007 | 11 |
  | C half − R half | all 44 | −0.0011 | 0.0034 | 16 |

  - **Contrast 1.** One opening quarter should detect the edge on centered
    r² (mean/SD about 2). On raw r² it cannot (SD 0.07).
  - **Contrast 2.** The backtest expects the capacity model to rank lineups
    slightly worse, about −0.002 to −0.004. A single quarter is therefore
    likely to land near the −0.003 margin. The prospective result is read as
    agreeing or disagreeing with that expectation, not as a new finding.
  - The whole-season population is the larger sample for both.
- **Recorded at freeze, no outcomes needed** (`scripts/prospective_freeze.py`):
  - fixture forecasts and named matchup margins for R, C and A;
  - property-suite pass rates for R and C;
  - out-of-support reasons.

  The property suite's base lineups are 2026q4's real fives, looked up with
  2027q1 states.

## Freeze record (2026-10-12)

Written by `scripts/prospective_freeze.py` to
`experiments/cache/prospective_2027q1/freeze/`. `record.json` has sha256
`495d24368e3d2c794daca862b2a855a916bf91267e60d842e1ba191f49dbf32a`.

**Code.**
- Fits launched at commit `fd60bcec`.
- Freeze run at commit `e608b2d4`, clean tree.
- `lineups/` is unchanged between them.

**Inputs.**
- Store `lineups_store_2027q1_library`: manifest sha256 `437b915e…fb3a`,
  `library_offense.npz` `3f32b0c8…fd7c`, `library_defense.npz` `25c6c569…f805`.
- Arm A snapshot
  (`experiments/cache/additive_origin_fits_2026_10_09/2027q1/fit.pkl`): sha256
  `4c1b4e93…28f9`. League level at 2026-10-20: 115.83.

**Fits** (`experiments/cache/prospective_2027q1/<arm>_s<seed>.pt`, sha256
prefix; selected epochs for phase A / phase B):

| Arm | Seed 17 | Seed 23 | Seed 41 |
| --- | --- | --- | --- |
| R | `7813b952` (7 / 7) | `c45cad44` (13 / 16) | `629f70cd` (6 / 6) |
| C | `b211862a` (7 / 22) | `b37a716f` (13 / 16) | `e833a548` (6 / 25) |

**Calibrations** (league + intercept + slope × (native − league), on 9,105
history cells per arm and seed):

| Arm | Seed 17 | Seed 23 | Seed 41 |
| --- | --- | --- | --- |
| R | 0.878 + 0.797 x | 0.830 + 0.786 x | 0.906 + 0.783 x |
| C | 0.840 + 0.797 x | 0.796 + 0.814 x | 0.678 + 0.826 x |

**Named matchups at 2027q1.** Margin = A's offense minus B's offense, points
per 100. Native and calibrated are the neural model alone; half is the blend
with A.

| Matchup | A | R native | R calibrated | R half | C native | C calibrated | C half |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Legal centers vs Jokić/Westbrook | +0.5 | +3.5 | +2.7 | +1.6 | −4.5 | −3.6 | −1.6 |
| Legal centers vs Jokić/Korver | +0.4 | +5.9 | +4.6 | +2.5 | −3.4 | −2.8 | −1.2 |
| Five Goberts vs Jokić/Westbrook | +3.7 | +8.8 | +7.0 | +5.3 | −1.5 | −1.2 | +1.2 |
| Five Jokićs vs Jokić/Westbrook | +15.6 | +18.8 | +14.8 | +15.2 | +13.2 | +10.7 | +13.2 |
| Limited centers vs Jokić/Westbrook | −3.8 | −9.5 | −7.5 | −5.6 | −12.9 | −10.5 | −7.1 |
| Small guards vs Jokić/Westbrook | −1.7 | −12.6 | −9.9 | −5.8 | −11.4 | −9.3 | −5.5 |
| Highest-exposure 2026 five vs Jokić/Westbrook | −3.2 | +2.1 | +1.6 | −0.8 | +1.0 | +0.8 | −1.2 |

Out-of-support reasons fire for the three center lineups. Five Goberts get
both "composition beyond every trained lineup" and "no ball handler".

**Property pass rates at 2027q1** (2026q4's real fives, 2027q1 states,
three-seed checkpoint mixtures):

| Property | R | C |
| --- | ---: | ---: |
| spacing_rim | 1.00 | 1.00 |
| handler_conversion | .96 | .94 |
| handler_teammate_turnovers | .99 | .99 |
| clone_synergy | .98 | .83 |
| rim_synergy | 1.00 | .96 |
| rebound_synergy | 1.00 | 1.00 |
| permutation | 1.00 | 1.00 |
| perimeter_coverage | .98 | .55 |
| coverage_targeting | .86 | .39 |
| handler_turnovers | .39 | .42 |

**Scoring needs Adam's go-ahead** for the 2026–27 data refresh. Then run
`scripts/prospective_score.py` on the refreshed matchup rows, with the
realized 2027q1 stop date and the season's quarter windows.
