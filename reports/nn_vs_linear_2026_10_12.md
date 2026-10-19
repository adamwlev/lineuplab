# How much better than linear is the neural model? — 2026-10-12

Exploratory. Script: `scripts/nn_vs_linear.py`; rows and tables in
`experiments/cache/nn_vs_linear_2026_10_12/`.

## Setup

- **Population.** The primary benchmark: 44 quarters, 2016–2026; 8,345 broad
  offense-five cells (at least 50 possessions per quarter); 2.76M
  possessions.
- **Network.** The reference J_POINT_BOTH, checkpoint average, mean of seeds
  17, 23 and 41.
  - Its event ledgers are rebuilt from the saved checkpoints.
  - The rebuilt points match the saved forecasts.
- **Linear controls.**
  1. additive_defense: the registered ridge player-additive model with
     prior-only calibration.
  2. A new linear model on the network's own inputs:
     - Features: the mean and SD of the five attackers' standardized state,
       the means of their role and adjusted capability rows, and the same
       summaries for the defenders.
     - Fit: weighted ridge (λ = 1, untuned) on the prior five years, with
       the network's 730-day half-life.
     - One model per target, each weighted by its own exposure.
- **Uncertainty.** Season-level SEs (11 seasons) and two-sided t tests with
  10 df. There is no multiplicity correction.

## Points

| Comparison (broad cells, points per 100) | r² | Δ r² ± season SE | p | Seasons + |
| --- | --- | ---: | ---: | ---: |
| Network alone (calibrated) vs additive_defense | .1615 vs .1460 | +0.0155 ± 0.0059 | .025 | 8/11 |
| ... centered (within quarter) | .1012 vs .0884 | +0.0129 ± 0.0033 | .003 | 9/11 |
| Half blend vs additive_defense | .1630 vs .1460 | +0.0170 ± 0.0028 | .0001 | 11/11 |
| Network (native) vs linear on the same inputs, centered | .0990 vs .0860 | +0.0130 ± 0.0019 | <.0001 | 11/11 |

**Every possession** (points per possession, all 2.76M possessions):

| Forecast | r² |
| --- | ---: |
| Network | .0019 |
| additive_defense | .0015 |

The difference is +0.0004 ± 0.0001 (p = .0008, 10/11 seasons). One
possession's points are almost all chance, so every lineup model is near zero
at this level.

**In RMSE terms** (broad cells), the network is 11.06 points per 100 and
additive_defense 11.17. Game-split reliability puts the ceiling for cell r²
at about .21–.24, so the network explains roughly 0.07 more of the
predictable share.

## Events

Network (native) vs the linear model on the same inputs, broad cells. Both
are uncalibrated, so the centered column is the fair comparison.

| Target | Centered r², network vs linear | Δ ± SE | p | Seasons + |
| --- | --- | ---: | ---: | ---: |
| Offensive-rebound share | .196 vs .173 | +0.023 ± 0.005 | .0004 | 11/11 |
| Three-point FG% | .017 vs .006 | +0.012 ± 0.003 | .001 | 10/11 |
| Rim FG% | .086 vs .078 | +0.007 ± 0.003 | .026 | 9/11 |
| Rim share of FGA | .283 vs .271 | +0.012 ± 0.006 | .057 | 7/11 |
| Three-point share of FGA | .445 vs .437 | +0.008 ± 0.006 | .22 | 9/11 |
| FGA per possession | .088 vs .081 | +0.006 ± 0.004 | .12 | 7/11 |
| FTA per possession | .141 vs .137 | +0.005 ± 0.007 | .51 | 8/11 |
| Turnovers per possession | .096 vs .100 | −0.004 ± 0.006 | .53 | 4/11 |

After a Holm correction across the eight event targets, offensive rebounding
and three-point FG% remain significant.

## Caveats

- The new linear control is untuned. A tuned version, or one with pairwise
  terms, might narrow the event gaps.
- The network alone beats additive_defense in 8/11 seasons on raw r². The
  "11/11" in STATUS refers to the half blend.

## Addendum: how much room is left in each event?

Script: `scripts/event_headroom.py`.

**Ceiling.** Each cell's games were split by game-id parity. The
correlation of the two halves across cells within each quarter, stepped up
with Spearman–Brown, estimates the persistent share of within-quarter cell
variance. That is an upper bound for centered r²: it includes in-quarter
context that no forward forecast sees.

**Averaging.** This test regresses the network's residual on the attackers'
best-minus-average and worst-minus-average of the matching player rate.

| Target | Ceiling | Network share of ceiling | Linear share of ceiling | Left unexplained | Residual variance explained by best/worst player |
| --- | ---: | ---: | ---: | ---: | ---: |
| Points | .160 | 62% | 54% | .061 | 0.0% |
| FGA per possession | .154 | 57% | 53% | .066 | 0.2% |
| FTA per possession | .354 | 40% | 39% | .213 | 0.1% |
| Turnovers per possession | .145 | 66% | 69% | .049 | 0.1% |
| Rim share | .392 | 72% | 69% | .109 | 0.0% |
| Three-point share | .581 | 77% | 75% | .136 | 0.1% |
| Rim FG% | .083 | about 100% | 94% | about 0 | 0.0% |
| Three-point FG% | .042 | 42% | 13% | .025 | 0.0% |
| Offensive-rebound share | .292 | 67% | 59% | .096 | n/a |

**Late-game free throws (quick count from `nba.possessions`).**

| Game situation | Share of possessions | FTA per possession |
| --- | ---: | ---: |
| Last two minutes of the 4th quarter and overtime | 5.2% | 0.45 |
| Everything else | 94.8% | 0.23 |

So about 10% of free-throw attempts come late in games, mostly to whichever
lineup is closing.

**Reading.**

- In real lineups, the best and worst player's rates add nothing beyond the
  averages the network already uses.
- Turnovers, FGA, shot mix and rim FG% have little room left, or tie because
  of one-ball accounting.
- Free throws have the largest persistent share left (.21). It plausibly
  comes from game state, which the model has no input for by design.
- The network's turnover path is close to linear in player rates, which is
  why it ties a linear model. That matters for weird lineups (no ball
  handler), not for accuracy on real ones.
