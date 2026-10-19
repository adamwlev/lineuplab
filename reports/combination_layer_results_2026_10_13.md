# Measured combination effects in the forecast: results — 2026-10-13

These are the results of the [protocol](combination_layer_protocol_2026_10_13.md).
It was committed (95b00fad) and amended (7142f238) before any run.
- Script: `scripts/combination_layer.py`.
- Output: `experiments/cache/combination_layer_2026_10_13/` (`layer.json`,
  `forward.json`, `report.txt`).
- Code: `lineups/combinations.py`, with the band and the browser tool.

## Summary

- **The layer enters the printed number.** The forward check is +0.00003 raw
  and +0.00004 centered r², as expected: nothing either way. The trade is
  printed in the scorecard.
- **Every event forecast improves slightly forward.** Squared error falls by
  0.006–0.017% on rim share, three share, turnovers and FTA. All four events
  keep their terms.
- **On real lineups the layer is small.** The mean absolute adjustment is 0.24
  points per 100; the 99th percentile is 0.9.
- **On unusual lineups it bends the forecast.**
  - Five legal centers: net +1.01 → +0.83, defense +0.64 points allowed.
  - Five small guards against the 2017 Warriors: margin +1.03.
- **Deviation from the protocol** (reported, not hidden). The forecast holds
  each type count at its measured maximum. Pairwise continuation is the band's
  alternative. The protocol had these the other way round.

## The layer (fitted on 2022–2026, no late-game rows, all 14 together)

The table gives each effect per pairing beyond what adding up implies, with
SEs clustered by game. Units: pp of FGA for shares, events per 100
possessions otherwise.

| Event | Combination | Per pairing | SE |
| --- | --- | ---: | ---: |
| Rim share (opponents) | bigs × bigs | +0.62 | 0.17 |
| | bigs × shot-blockers | −0.12 | 0.13 |
| | shot-blockers × defensive rebounders | +0.43 | 0.11 |
| Three share | bigs × offensive rebounders | +0.16 | 0.11 |
| | non-shooters × offensive rebounders | +0.40 | 0.14 |
| | offensive rebounders × offensive rebounders | +0.19 | 0.25 |
| Turnovers | shooters × self-creators | −0.12 | 0.05 |
| | slashers × high usage | −0.10 | 0.05 |
| | non-shooters × offensive rebounders | −0.21 | 0.06 |
| FTA | small × small (offense) | +0.30 | 0.15 |
| | small × passers | +0.25 | 0.11 |
| | small × self-creators | −0.15 | 0.11 |
| FTA (opponents) | bigs × bigs (defense) | +0.60 | 0.16 |
| | small × small (defense) | +0.51 | 0.14 |

**Fitted together, two effects that held up alone add nothing.** Bigs beside
shot-blockers and small players beside self-creators reverse sign, and neither
is significant. Their single-pair signal is carried by the bigs-together and
small-pair effects, which share most of their players. They stay in the layer
as the protocol fixed it, and the tool titles them "nothing beyond the bigs
effect" and "nothing beyond the small-player effects".

**Only the nonlinear part is used.** Each term is β × (pairings − the linear
projection of pairings on the type counts). It averages zero on real lineups
and holds only what adding up players cannot express. So the "bigs" effect
barely moves a two-big lineup, which is typical. It acts on lineups with
none, one, or three or more bigs: the first big deters most, and a third adds
little.

## Forward check (declared before running)

The layer was fitted on 2016–2021 and applied to every 2022–2026 game ×
offense five × defense five row, late-game rows included. Points are actual
points per 100, possession-weighted. This is not the scorecard's
lineup-quarter population.

| Variant | Raw r², network → network + layer | Centered r² | Mean \|adjustment\| | 99th pct |
| --- | --- | --- | ---: | ---: |
| Pairwise continued (declared) | .00746 → .00749 (+.00003) | .00739 → .00743 (+.00004) | 0.242 | 0.96 |
| Held at measured counts (the tool) | .00746 → .00749 (+.00003) | .00739 → .00743 (+.00004) | 0.238 | 0.90 |

- r² is low because single game rows carry few possessions.
- **By season** (raw, held at measured counts): 2022 +.00000, 2023 −.00000,
  2024 −.00001, 2025 +.00007, 2026 +.00010.
- **Events** (held at measured counts): squared error changes by −0.017%
  (rim share), −0.016% (three share), −0.006% (turnovers) and −0.009% (FTA).
- **Decision:** the raw change is ≥ −0.003, so the layer enters the printed
  number. All four events are kept.

## Shape check: is the pairwise form right at three players?

These are same-type effects, using count dummies on 2022–2026 rows without
late-game possessions. The pairwise form predicts the count-3 curvature to be
3 × the count-2 curvature.

| Effect | Count 2 | Count 3+ | Ratio | Possessions at 3+ |
| --- | ---: | ---: | ---: | ---: |
| Bigs on defense, rim share | +0.67 (0.24) | +1.91 (0.48) | 2.9 | 3.5% |
| Offensive rebounders, three share | +0.52 (0.23) | +2.29 (0.60) | 4.4 | 1.0% |
| Small players on offense, FTA | +0.74 (0.25) | +1.63 (0.47) | 2.2 | 6.5% |
| Bigs on defense, FTA | +0.88 (0.25) | +1.72 (0.50) | 2.0 | 3.5% |
| Small defenders, FTA | +0.61 (0.25) | +1.72 (0.47) | 2.8 | 6.6% |

The pairwise form holds roughly up to three players. The free-throw effects
grow a little more slowly than pairwise. Beyond three, nothing is measured.

## Deviation: the forecast holds counts at the measured maximum

**What the protocol said.** The forecast would continue the pairwise form,
and the band would carry "effects stop growing at the largest measured count"
as the alternative.

**What happened on the fixtures** (before the swap; the forward check is
unaffected).
- Five Goberts got +4.3 points per 100 from "non-shooters beside offensive
  rebounders: fewer turnovers". That is 20 counted pairings against the 6
  measured, and it is modern-era only (it reverses in 2007–2013).
- Five non-shooting rebounders turning the ball over less contradicts the
  declared one-ball structure. Someone has to bring it up, and the network
  already handles a five with no ball handler.

**What changed.**
- The forecast now holds each type count at its measured maximum: the most
  players of a type on the floor together in at least 0.5% of 2022–2026
  possessions. That is 3 for most types and 4 for shooters, self-creators and
  high-usage players.
- Pairwise continuation is the band's named alternative K. Its spread enters
  the range, with a reason.

**Why it is defensible.** Holding at the measured maximum is the
data-first reading: the effect is known up to there. Beyond it, either choice
is an assumption, and the band now shows the disagreement. The forward check
is the same under both variants.

## Fixtures (release model, relative rule, 2026 player-seasons)

| Lineup | Network net | Layer: offense / defense / net | Forecast net | K moves net |
| --- | ---: | --- | ---: | ---: |
| Highest-exposure real five | +2.22 | −0.09 / +0.05 / −0.15 | +2.08 | 0.0 |
| Five legal centers | +1.01 | +0.46 / +0.64 / −0.18 | +0.83 | −0.6 |
| Five Goberts | +5.04 | +0.50 / +0.64 / −0.14 | +4.90 | −0.9 |
| Five Jokićs | +14.30 | −0.40 / +0.32 / −0.72 | +13.59 | −2.2 |

The layer makes every big-lineup fixture slightly worse on net. On defense,
rim deterrence saturates and free throws rise. That is pillar 2's direction,
for a measured reason. It does not make five centers fail; the band and its
reasons still carry that.

## Where it lives

- `lineups/combinations.py`:
  - player types per player-season (each season's own percentiles under the
    era-relative rule, the latest season's under as-was);
  - the layer, the accounting values, and lineup and matchup outputs;
  - the small-guards × anchor (H1) flag, shown as a note and not in the
    number.
- `lineups/band.py`: the point is the network plus the layer. The union adds
  K, and the reason names the counts past the measured maximum.
- `lineups/explain.py` returns each offense's raw rates for the accounting.
- `tool/lineup_model.js`, `tool/lineups.html`:
  - type badges per player;
  - a combination-effects section listing each effect's pairings, what adding
    up implies, the event change, points and evidence;
  - a curve for same-type effects, measured range against continuation;
  - a library of all 14 effects.

  Parity: `tests/test_tool_parity.py`. Properties: `tests/test_combinations.py`.
- `scripts/interaction_discovery.py` now reads its type definitions from
  `lineups.combinations`; they are identical, checked on 2024q2.
