# Interaction discovery: protocol — 2026-10-13

Written and committed before any outcome is scored. Adam approved the study on
2026-10-12. It is exploratory, with a discovery / confirmation / replication
split fixed here. Script: `scripts/interaction_discovery.py`. Output:
`experiments/cache/interaction_discovery_2026_10_13/`.

## Question

Which combinations of player types do better or worse than the sum of their
players' individual values, and hold up on seasons the search never saw?

## Rows and baselines

- **Rows.** Game × offense five × defense five rows:
  - 2016–2026: the benchmark rows;
  - 2007–2013: the era rows.
- **Points.** The residual is actual points per 100 minus the best additive
  approximation of the calibrated network's forecast. That approximation is
  one value per player per side, fitted within each quarter to the forecasts
  (`scripts/synergy_check.additive_projection`). Weight: possessions.
- **Events.** Each event has its own residual: actual rate minus the
  additive approximation of the network's forecast rate, fitted the same way
  with the event's exposure as weight. Rates are scaled by 100.

  | Event | Rate | Exposure |
  | --- | --- | --- |
  | `three_fg` | three-point makes / attempts | 3PA |
  | `rim_fg` | rim makes / attempts | rim FGA |
  | `tov` | turnovers per possession | possessions |
  | `fta` | free-throw attempts per possession | possessions |
  | `orb_rate` | offensive rebounds / rebound chances | chances |
  | `rim_share` | rim attempts / FGA | FGA, location observed |
  | `three_share` | three-point attempts / FGA | FGA, location observed |

  Forecasts come from different sources in each period:
  - 2016–2026: the reference network's native event ledger, three seeds
    (`nn_vs_linear_2026_10_12/rows`).
  - 2007–2013: the era R fits, seeds 17 and 23 (`era_diagnostics_2026_10_12/rows_s17_23`).

  The replication of events therefore rests on two seeds.

## Player types

Every type is prior-only, from origin states at the quarter's start and listed
heights. "Top" and "bottom" are the 80th and 20th percentiles among the players
appearing in that quarter's rows.

**Offense, 9 types.**

| Type | Definition |
| --- | --- |
| `O_big` | height in the top 20% |
| `O_small` | height in the bottom 20% |
| `O_shooter` | 3PA rate (FGA rate × three-point share) in the top 20% |
| `O_nonshooter` | 3PA rate in the bottom 20% |
| `O_passer` | assist rate in the top 20% |
| `O_creator` | unassisted share of makes in the top 20% |
| `O_slasher` | rim-attempt rate (FGA rate × rim share) in the top 20% |
| `O_crasher` | offensive-rebound capture prior in the top 20% |
| `O_usage` | usage (FGA + 0.44 FTA + TO) in the top 20% |

**Defense, 5 types.**

| Type | Definition |
| --- | --- |
| `D_big` | height in the top 20% |
| `D_small` | height in the bottom 20% |
| `D_rim` | own block rate in the top 20% |
| `D_hawk` | own steal rate in the top 20% |
| `D_glass` | own defensive-rebound rate in the top 20% |

## Candidates (105)

- **Offense teammate pairs:** all 45 unordered pairs of the 9 offense types,
  same-type pairs included. The feature is the number of distinct-player
  pairs (i ≠ j) with i of the first type and j of the second.
- **Defense teammate pairs:** all 15 pairs of the 5 defense types, defined the
  same way.
- **Matchups:** the 45 combinations of an offense type with a defense type.
  The feature is n_offense × n_defense.

**Model.** Each candidate's outcome residual is regressed on its main effects
(the type counts) and the pair feature. The data are centered within quarter
and weighted by the outcome's exposure. The pair coefficient is the
interaction. SEs are cluster-robust by game.

**Families.** Points plus the 7 events: 8 outcome families, each with the 105
candidates.

## Split and selection

1. **Discovery, 2016–2021 (6 seasons).** Two-sided p-values. Benjamini-
   Hochberg at q = 0.10 within each family.
2. **Confirmation, 2022–2026 (5 seasons, held out).**
   - Test the k = 5 BH survivors with the smallest discovery p in each
     family (fewer if fewer survive), one-sided in the discovered direction.
   - Apply Holm at α = .05 within each family's confirmed set.
   - Also report the number of confirmation seasons with the discovered sign.
3. **Replication, 2007–2013 (7 seasons).** Every confirmed candidate is
   tested one-sided in the discovered direction:
   - **replicates** if p < .05;
   - **same sign** if the sign matches without significance;
   - **reverses** otherwise.

## Labels

- **Held up:** discovered, then confirmed after Holm.
- **Held up across eras:** also replicates in 2007–2013.
- **Discovery-only:** passed BH but not confirmation. Reported, never used.

## Within-player checks

These cover confirmed offense pairs whose outcome is a shot event:
three_fg, rim_fg, rim_share or three_share.
- For each player of the first type, his own event rate on each row
  (per-player loc_attempt / loc_make) is compared with and without a
  teammate of the second type.
- Rates are demeaned within player × quarter and weighted by his own
  exposure, with game-clustered SEs.
- This removes his individual level and most of the between-lineup
  selection.

## Sanity check

The defense pair D_small × D_rim on points should show up in discovery with a
negative sign. That is the small-guards-with-an-anchor effect, already found in
2016–2026, with its definitions loosened here to percentiles. Its discovery
rank and p are reported whatever they are.

## Power statement

The report gives the median minimum detectable effect (2.8 SE) per family in
discovery and in confirmation. With 105 candidates per family and BH at 0.10,
a null family means no effect larger than about that size was detectable. It
does not mean there is none.

## Limits, declared in advance

- **Profiles.** They are measured in the contexts players actually played in,
  which pulls results toward no synergy.
- **Deployment.** Coaches choose lineups partly on in-game results, which can
  mix with interactions.
- **Baseline.** The additive baseline is the network's own approximation; an
  interaction the network already models in events is not counted as one here.
  Points showed the network is nearly additive (`reports/synergy_check_2026_10_12.md`).
  Events were not checked.
- **Nothing here changes the tool or the forecast.**
