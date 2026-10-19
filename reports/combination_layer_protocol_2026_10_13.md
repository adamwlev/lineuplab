# Measured combination effects in the forecast: protocol — 2026-10-13

Written and committed before the forward check is run. Script:
`scripts/combination_layer.py`. Output:
`experiments/cache/combination_layer_2026_10_13/`.

## Why

Adam, 2026-10-13, after trying the review copy: "I think we want to emphasize
these discovered non-linearities more. Even though the data doesn't support
very many … I still think that's the whole appeal of this tool … The ability
to extrapolate in a non linear manner is what I want to show off. So let's
build it around these nonlinear adjustments, however small they are."

So the measured combination effects
([results](interaction_discovery_results_2026_10_13.md)) become a labeled
layer on top of the calibrated network, and the tool prints the sum. The
network-alone number stays visible beside it. Changing what the tool prints
calls for a forward check (rule of evidence 12); this is it.

## The layer

**Effects.** The 14 combinations labeled "held up" in the discovery results,
grouped by event:

| Event | Combinations (pair features) |
| --- | --- |
| Rim share of FGA | D_big × D_big, D_big × D_rim, D_rim × D_glass |
| Three-point share of FGA | O_big × O_crasher, O_nonshooter × O_crasher, O_crasher × O_crasher |
| Turnovers per 100 | O_shooter × O_creator, O_slasher × O_usage, O_nonshooter × O_crasher |
| FTA per 100 | O_small × O_small, O_small × O_passer, O_small × O_creator, D_big × D_big, D_small × D_small |

Types and pair features are as defined in the discovery protocol. Small guards
× anchor (H1) is not in the layer. Its pre-registration requires a held-out
accuracy check before it changes what the tool prints, so the tool shows it
only as a labeled note, "being tested in 2026–27".

**Fit.** One weighted least-squares fit per event:
- Rows: 2022–2026, the discovery's confirmation window. The selection never
  saw it, so the estimates carry no winner's curse, and these are the release
  model's own training seasons.
- Rows containing any possession in the last two minutes of the fourth
  quarter or in overtime are dropped, so late-game fouling is not counted as a
  combination effect.
- Outcome: the event residual against the network's own forecast (as in the
  post-hoc check), weighted by the event's exposure.
- Regressors: every type count involved in the event's pairs, plus the pair
  features, jointly, all centered within quarter. SEs are clustered by game.

**Only the nonlinear part.** Each pair feature is replaced by its residual
from a linear projection on the involved type counts, fitted on the same
rows. The layer is then zero on average and orthogonal to the type counts, so
it holds only what a model that adds up players cannot express. The type
counts' own coefficients (the network's type-level misfit) are not used.

**Points.** Event changes are converted to points per 100 by accounting, at
the lineup's own forecast rates:
- rim-share and three-share changes move attempts from the other locations
  in proportion to their shares, valued at the lineup's make rates;
- a turnover costs the lineup's points per non-turnover possession;
- a free-throw attempt is worth the lineup's free-throw percentage, minus
  half the lineup's points per field-goal attempt. A trip of about two
  attempts ends a possession that would otherwise have ended in a shot.
  (Amended before any run: the first draft valued an attempt at the
  free-throw percentage alone, which ignores the displaced shot.)

Offense pairs act on the lineup's offense. Defense pairs act on the offense
it faces: in a matchup, on that offense's rates; against the league-average
panel, at the league-average offense's rates.

**Beyond the measured counts.** Most types reach three players on the floor
in at least 0.5% of 2022–2026 possessions; a few reach four. Past that, there
are no data.
- The forecast continues the pairwise form: every pair interacts as measured.
- The band adds a named alternative, "combination effects stop growing at
  the largest measured count". Under it, each type count is capped at its
  measured maximum. The union of the two goes into the band, with a reason
  whenever they differ.

## Forward check (declared before running)

- **Fit** the same layer, with the same rules, on 2016–2021 rows. Apply it
  forward to every 2022–2026 row, late-game rows included.
- **Points.** Actual points per 100 on game × offense five × defense five
  rows, possession-weighted. Compare the calibrated network alone with network
  + layer:
  - pooled r² and within-quarter centered r²;
  - the difference in each of the five seasons.

  The forward rows lack a ledger, so attempts are valued at the row's
  forecast rim and three-point FG%, and at league constants for other twos,
  free throws and points per possession.
- **Events.** The change in exposure-weighted squared error of each event's
  forecast, network versus network + layer, overall and per season.
- **Decision rule.**
  - The layer enters the printed number if the forward points r² change is
    ≥ −0.003 (raw). That is Adam's accuracy allowance; the pillar-2 gain is
    the nonlinear extrapolation he asked for. The trade is printed in the
    scorecard whatever it is.
  - An event's terms are kept only if its forward squared error does not get
    worse.

## Shape check (secondary)

For the same-type pairs (two bigs and two small players on defense, two
crashers and two small players on offense), estimate separate curvature at
counts 2 and 3. The pairwise form predicts a ratio of 3 (three pairs against
one). The estimated ratio and its interval are reported, to say how well the
form holds at the edge of the data.

## Limits, declared in advance

- **Small effects.** Each is about 0.1–0.3 points per 100 per pair. The
  forward points change is expected to be within ±0.001 r². The layer's case
  is pillar 2 (nonlinear extrapolation with a stated basis), not accuracy.
- **Accounting.** The points conversion is accounting on measured event
  changes, not a measured points effect. No points interaction was
  detectable (detection limit about 0.5 per 100 per pair).
- **Pairwise continuation is an assumption.** It is labeled in the tool, and
  its alternative is in the band.
