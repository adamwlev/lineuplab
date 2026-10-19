# Does the network find synergies? — 2026-10-12

Exploratory. Adam asked whether the network has discovered non-linear
synergies between player profiles that a linear model cannot express.

- Script: `scripts/synergy_check.py`.
- Output: `experiments/cache/synergy_check_2026_10_12/`.

## Test

For each benchmark quarter (44 quarters, 2016–2026), the calibrated network's
row forecasts (three-seed mean) are projected onto the most flexible model
that is additive across players: one free value for every attacker and one
for every defender in that quarter. The fit is possession-weighted least
squares on the network's own forecasts, with no outcomes. The projection is
the network's best additive approximation. The remainder is everything no sum
of per-player values can express:
- teammate interactions;
- offense-defense interactions;
- the one-ball accounting.

Scoring uses broad offense-five cells, centered within quarter, with
season-level SEs.

## Result (points)

| | |
| --- | --- |
| Centered r²: network / its additive approximation | .1012 / .1013 |
| Gain from the non-additive part | +0.0000 ± 0.0004 (5/11 seasons) |
| Actual regressed on [additive, non-additive] | coefficients 1.04 and 0.54; non-additive 0.56 ± 0.62 by season, 6/11 positive |
| Size of the non-additive part | 1% of the network's row-level variance; SD 0.21 points per 100 across cells |

## Reading

- **On real lineups, the network's point forecasts are additive across
  players.** Its non-additive part is small and adds no measurable accuracy.
- **Where the network's edge comes from.** It beats a linear model on the
  same inputs (+0.013 centered r², 11/11;
  [report](nn_vs_linear_2026_10_12.md)) by valuing each player better: a
  non-linear function of his profile, through the event ledger. Combining
  players is not where the gain is.
- **This agrees with earlier nulls.**
  - Pair chemistry and matchup terms sat at the noise floor (v2–v16).
  - Best- or worst-player order statistics explain under 0.2% of the
    network's residual.
  - The learned coverage and creation heads were inert.
- **Off support, the network is strongly non-additive.** Clones and five
  centers interact through the one-ball budget, renewal and the creation
  constraint. Those mechanisms are declared accounting, and no outcomes can
  check them there.

## Limits

- **Points only.** Events can interact while points net out. The tool shows
  usage reallocating (Westbrook loses share next to Jokić), but under one
  ball one player's lost shots are a teammate's gained shots.
- **Power.** Interactions of this size (SD 0.2) are far below cell-level
  outcome noise (about 10 points per 100). The test shows the network's
  interactions add nothing detectable. It does not show that no real
  interactions exist: about .06 of the reliability ceiling is still
  unexplained, and some of that could be interactions the network does not
  model.
- **The projection is fitted within each quarter** to that quarter's realized
  matchups. It is a decomposition of the network, not a competing forecast.
