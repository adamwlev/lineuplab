# Interaction discovery: results — 2026-10-13

Results of the [protocol](interaction_discovery_protocol_2026_10_13.md),
committed (d8c0fc4a) before any outcome was scored. Everything here is
exploratory.

- Scripts: `scripts/interaction_discovery.py`, and
  `scripts/interaction_discovery_posthoc.py` for the post-hoc checks.
- Output: `experiments/cache/interaction_discovery_2026_10_13/`.

**Search.** 105 player-type combinations: 45 offense pairs, 15 defense pairs
and 45 matchups.
- 8 outcomes: points plus 7 events.
- Discover on 2016–2021, confirm on held-out 2022–2026, replicate on
  2007–2013.
- Effects are per pair of players, in residual units: points per 100,
  percentage points for rates and shares, events per 100 possessions.

## Summary

- **No points interaction held up.** Three candidates passed discovery; none
  confirmed. The median detectable size was about 0.5 points per 100 per
  pair.
- **Event interactions did hold up**, several across both eras. Each is
  small, about 0.1–0.3 points per 100 per pair once converted to points,
  which is why points show nothing.
- **The network captures none of them.** The coefficients are the same
  against its own forecast as against its additive approximation.
- **The sanity check failed.** Small defenders × rim protector on points:
  −0.27 (SE 0.20), p .19, rank 39 of 105. With the protocol's looser
  percentile definitions, the small-guards-with-an-anchor effect from
  yesterday (stricter: 6'3" or shorter, and an anchor 6'9"+ in the top 10%
  of blocks) is not rediscovered. That effect depends on its definition of a
  true anchor; its pre-registered 2026–27 test stands.

## By outcome

| Outcome | Pass BH in discovery (q = .10) | Median detectable effect (discovery) | Held up after confirmation |
| --- | ---: | ---: | --- |
| Points (per 100) | 3 | 0.48 | none |
| Three-point FG% | 5 | 0.39 pp | none |
| Rim FG% | 4 | 0.43 pp | none |
| Turnovers (per 100) | 4 | 0.15 | 3 |
| FTA (per 100) | 28 | 0.29 | 5 (of 5 tested) |
| Offensive-rebound share | 11 | 0.30 pp | none |
| Rim share of FGA | 12 | 0.25 pp | 3 |
| Three-point share of FGA | 19 | 0.24 pp | 3 |

## What held up

Columns are confirmation 2022–2026 and replication 2007–2013, each a
coefficient with its SE. The post-hoc columns are labeled.

| Outcome | Combination | Confirmation | 2007–2013 | Label | Post hoc: without late-game rows | Post hoc: against the network's own forecast |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| Rim share | two bigs (D_big × D_big) | +0.73 (0.15), 5/5 seasons | +0.37 (0.13) | across eras | +0.64 / +0.30 | +0.72 / +0.37 |
| Rim share | big × rim protector on defense | +0.36 (0.10), 5/5 | +0.18 (0.10) | across eras | +0.32 / +0.14 | +0.35 / +0.17 |
| Rim share | rim protector × defensive rebounder | +0.45 (0.09), 5/5 | +0.03 (0.09) | held up; era same sign | +0.43 / +0.06 | +0.45 / +0.04 |
| Three share | big × offensive rebounder | +0.32 (0.10), 4/5 | +0.17 (0.09) | across eras | +0.31 / +0.07 | +0.33 / +0.17 |
| Three share | non-shooter × offensive rebounder | +0.51 (0.10), 5/5 | +0.11 (0.09) | held up; era same sign | +0.49 / +0.06 | +0.56 / +0.12 |
| Three share | two offensive rebounders | +0.72 (0.17), 5/5 | −0.05 (0.14) | held up; era reverses | +0.67 / −0.17 | +0.74 / −0.04 |
| Turnovers | shooter × self-creator | −0.13 (0.04), 4/5 | −0.14 (0.04) | across eras | −0.14 / −0.10 | −0.15 / −0.14 |
| Turnovers | slasher × high usage | −0.10 (0.04), 4/5 | −0.03 (0.04) | held up; era same sign | −0.08 / −0.04 | −0.11 / −0.04 |
| Turnovers | non-shooter × offensive rebounder | −0.22 (0.06), 4/5 | +0.07 (0.07) | held up; era reverses | −0.22 / +0.15 | −0.21 / +0.08 |
| FTA | two small players on offense | +0.57 (0.14), 5/5 | +2.60 (0.23) | across eras | +0.41 / +1.83 | +0.57 / +2.61 |
| FTA | small × passer on offense | +0.44 (0.09), 5/5 | +1.25 (0.13) | across eras | +0.24 / +0.79 | +0.44 / +1.24 |
| FTA | small × self-creator on offense | +0.28 (0.09), 4/5 | +0.80 (0.12) | across eras | +0.07 / +0.46 | +0.27 / +0.79 |
| FTA | two bigs on defense | +0.85 (0.16), 4/5 | +0.71 (0.16) | across eras | +0.61 / +0.42 | +0.83 / +0.68 |
| FTA | two small players on defense | +0.61 (0.14), 5/5 | +2.33 (0.24) | across eras | +0.51 / +1.58 | +0.61 / +2.31 |

**Within-player checks** for the three-point-share survivors (2016–2026). Each
row is the player's own share of FGA from three, demeaned within player ×
quarter:

| Player type | Partner type | Own three-point share with vs without partner |
| --- | --- | ---: |
| Big | Offensive rebounder | +2.2 pp (0.2) |
| Offensive rebounder | Big | +2.0 pp (0.2) |
| Non-shooter | Offensive rebounder | +2.1 pp (0.2) |
| Offensive rebounder | Non-shooter | +2.6 pp (0.2) |
| Offensive rebounder | Another offensive rebounder | +2.7 pp (0.2) |

## Reading

1. **Rim deterrence saturates (one rim).** Each additional big deters fewer
   rim attempts than the first.
   - Against two bigs, offenses take 0.4–0.7 pp more of their shots at the
     rim than the sum of the two bigs' individual deterrence implies.
   - Against big + rim protector the excess is +0.4 and +0.2.
   - It holds across eras.
   - This is the capacity-law premise, for shot location. The era backtest
     found that conversion keeps falling with a third big. So big defenses
     saturate in deterrence, not in finishing.
2. **Two interior players: one moves outside.** When two bigs or rebounders
   share the floor, each takes about 2 pp more of his own shots from three
   than he does without the other (within-player). The lineup's three-point
   share rises 0.3–0.7 pp above additive. This is role adaptation, measured
   on the same players.
3. **A shooter next to a self-creator means fewer turnovers.** About 0.13
   fewer per 100 per pair, in both eras, and robust to late-game rows.
   Spacing helps creators keep the ball.
4. **Small players draw (and allow) more free throws together.**
   - Late-game fouling explains part of it: dropping rows with any possession
     in the last two minutes or overtime shrinks the effects by 25–75%.
   - The small × self-creator effect disappears in 2022–2026.
   - The rest remains: two small offensive players +0.4 FTA per 100 per
     pair; two small or two big defenders +0.5–0.6.
   - Bonus and foul-trouble situations outside the last two minutes are not
     removed. Treat these as partly game state.
5. **None of it moves points much.**
   - Converted to points, each effect is about 0.1–0.3 per 100 per pair:
     0.7 pp of FGA shifted to the rim is worth about 0.15; 0.4 FTA about 0.3;
     0.13 turnovers about 0.15.
   - All of these sit under the points MDE of about 0.5, which is consistent
     with no points interaction holding up.

## Correction to the protocol

The protocol says an interaction the network already models "is not counted
as one here". That is wrong: the baseline is the network's additive
approximation, not the network, so such interactions are counted. The post-hoc
column checks the network directly. Its own forecast leaves every held-up
coefficient unchanged, so the network models none of them.

## Power

- **Points.** The median detectable effect is about 0.5 points per 100 per
  pair, in discovery and in confirmation. Pairwise type interactions on
  points smaller than that cannot be seen with these data. Larger ones, for
  these 105 combinations, were not there.
- **Events.** The detectable effects are 0.15–0.43 units. Of the BH-passing
  candidates, about 10% are expected to be false.
- **Discovery-only candidates** passed BH but failed confirmation. They are
  in `discovery_<outcome>.csv` and not used.

## For the tool and the model

- **Labeled "measured combination effects".** These are data-backed, state
  their size and era, and can be shown in the breakdown without touching the
  forecast:
  - two bigs on defense: rim deterrence saturates;
  - two interior players: one plays outside;
  - a shooter beside a self-creator: fewer turnovers;
  - small guards with or without an anchor: modern era, pre-registered for
    2026–27.
- **For the model.** The network is additive in these events. A location
  head that reads the count of bigs (deterrence saturation) and a role term
  for paired interior players are structurally justified. Their expected
  point gain is a few tenths per pair, so an accuracy gain would be hard to
  show. They would matter mainly for the weird lineups (pillar 2).
- **Nothing here changes the tool or the forecast.**
