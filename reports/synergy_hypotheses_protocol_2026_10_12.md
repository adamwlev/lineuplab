# Synergy hypotheses: protocol — 2026-10-12

Written before any outcome was looked at. These are exploratory tests with
declared directions. H1–H3 are Adam's; H4–H5 are Claude's. Script:
`scripts/synergy_hypotheses.py`.

## Question

Does each combination do better (or worse) than the sum of its parts on real
outcomes? Synergy here means an interaction beyond what each player brings on
his own.

## Common design

- **Outcomes.** Points per 100 possessions, on the game × offense five ×
  defense five rows.
- **Primary population.** 2016–2026: 44 quarters, all rows, possession
  weights.
- **Replication.** 2007–2013: 28 quarters, era backtest forecasts.
- **Baseline.** The best additive approximation of the forward forecast:
  one value per player per side, fitted within each quarter to the
  calibrated network's own forecasts (`scripts/synergy_check.py`). The
  residual is actual minus that baseline.
- **Player profiles.** Prior-only: origin states at the start of each
  quarter, with listed heights. Percentile thresholds are computed among the
  players appearing in that quarter's rows, so they travel across eras.
- **Model.** A weighted regression of the residual on the two main effects
  and their interaction, centered within quarter. The interaction coefficient
  is the synergy.
- **Uncertainty.** The coefficient by season, with mean ± season SE (11
  seasons; 7 in the replication). Holm correction across the five
  hypotheses in the primary era.
- **Readable tables.** The mean residual for each combination group.

## Hypotheses

**H1. Small guards need an anchor (Adam).** Defensive side; the residual is
points allowed.
- *Small defender:* listed 6'3" (75 in) or shorter.
- *Anchor:* a defender 6'9" (81 in) or taller, with own block rate in the
  top 10% of the quarter's players.
- *Prediction:* the interaction n_small × anchor is **negative**. With an
  anchor, each small defender costs fewer points.

**H2. Catch-and-shoot specialists need a playmaker (Adam).** Offensive side.
- *Specialist:* three-point share of FGA in the top 25%, assisted share of
  makes in the top 25%, and assist rate in the bottom 50%, all among the
  quarter's players.
- *Playmaker:* a teammate with assist rate in the top 10%.
- *Prediction:* n_specialists × playmaker is **positive**.

**H3. Transition finishers need a defense that forces live-ball turnovers
(Adam).** Offensive side.
- *Post-steal possession:* the possession right after the opponent's
  turnover credited as a steal, in the same game and quarter.
- *Transition finisher:* over the three prior seasons, the player's points
  per post-steal possession minus his points per other possession, shrunk
  as lift × n/(n + 300) with n his post-steal possessions on the floor. He
  must rank in the top 10% of players with at least 500 prior offensive
  possessions.
- *Steal pressure:* the sum of the five's own steal rates (defensive
  descriptor 0), standardized within the quarter. It is prior-only.
- *Prediction:* n_finishers × steal pressure is **positive**.
- *Mechanism, secondary:* finishers' share of points on post-steal
  possessions, and the five's post-steal points per possession by finisher
  count.

**H4. Two ball-dominant creators clash (Claude).** Offensive side.
- *Ball-dominant:* usage (FGA + 0.44 FTA + TO per on-floor possession) in
  the top 10%.
- *Prediction:* the indicator for two or more is **negative**, controlling
  for having at least one. The second creator adds less than the first.

**H5. A rim-running big needs shooters (Claude).** Offensive side.
- *Rim runner:* 6'9" or taller, three-point share of FGA in the bottom 10%,
  rim share of FGA in the top 25%.
- *Shooter:* three-point attempts per possession in the top 40%.
- *Prediction:* rim runner × n_shooters is **positive**.

## Reading rules

- A hypothesis is **supported** if the primary interaction has the predicted
  sign, Holm p < .05 across the five, and the same sign in the replication
  era.
- It is **suggestive** if it has the predicted sign with an unadjusted
  p < .05.
- Otherwise there is **no evidence at this power**. That is not evidence of
  absence.
- Every result also reports the size in points per 100 for a typical
  combination.

## Known limits, declared in advance

- Player profiles are measured in the contexts players actually played. A
  synergy between regular teammates is partly credited to each player
  individually, so the tests lean toward finding no synergy.
- Coaches choose lineups, partly on in-game success, so interactions can mix
  with deployment.
