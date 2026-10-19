# The event model

This page describes the retained reference, **J_POINT_BOTH**, as implemented in
[lineups/model.py](lineups/model.py). That file reproduces the saved
production predictions exactly. For results see
[MODEL_SCORECARD.md](MODEL_SCORECARD.md). For the version-by-version
history see [docs/history/NEURAL_MODEL_2026-10-09.md](docs/history/NEURAL_MODEL_2026-10-09.md).

**What the tool runs** (2026-10-15). The release is this architecture with
broadcast defense (arm R), fitted two-phase from scratch at origin 2027q1,
three seeds of five checkpoints each, and calibrated per seed
(`lineups/release.py`). On top of it come half of the centered learned pairwise
module (`lineups/learned.py`) and the 14 measured combination effects
(`lineups/combinations.py`). The range adds capacity defense (arm C) and two
combination alternatives (`lineups/band.py`). Which fits and inputs the tool
uses is set in `lineups/sources.py`: names (2026-10-14), or clean (retrained on
the possession table rebuilt from the pages). The reader-facing description is
[tool/model.html](tool/model.html).

## Inputs: dated player capabilities, no player IDs

Every input is a per-player lookup ([lineups/features.py](lineups/features.py)).
For training rows it is the state as of that game. For forecasts and
hypothetical lineups it is the state frozen at the origin date, and a player
with no history gets the origin's population fallback.

| Input | Per player | Content |
| --- | --- | --- |
| `base` | 18 | Log FGA/FTA/TO rates; 6 location logits; 6 location make logits; FT logit; log assist rate (passing supply); assisted-make logit (finishing demand). Rates use a 180-day half-life, shooting 730 days, with empirical-Bayes shrinkage. |
| `role` | 8 | Recent-minus-long contrasts (usage, 3PA share, turnovers, assists) and historical teammate averages |
| `rb_input` | 28 | Standardized state, role, and rebound prior (logit and support) |
| `adjusted_offense` | 97 | Adjusted GLM capability bank: own effects and influence on teammates, plus log opportunity, log coefficient SD and log staleness |
| `defense` | 19 | Dated defender descriptors: steals, blocks, defensive rebounds, fouls, opponents' on-floor rates, allowed location mix and conversion |
| `adjusted_defense` | 49 | Adjusted GLM defender bank |

Normalizers are fitted on each origin's training prefix only.

## Computation

1. **Teammate context.** Each player's state gets a correction from a small
   tanh network reading his own state and the other four players' mean and
   SD. A role head reads own state plus the role descriptors. Teammates never
   change a player's FT%. A coordinate-wise affine decoder maps state to event
   logits.
2. **Adjusted heads.** Bounded (tanh) corrections come from the adjusted own
   and teammate banks. The adjusted defender bank (mean/SD over the five)
   shifts actions, location, conversion and recovery.
3. **Opportunity ledger.** Each player's FGA/FTA/TO rates are rescaled so the
   five share one budget, `FGA + 0.44·FTA + TO = B`.
   - When implied assisted finishing exceeds the lineup's passing supply,
     make probabilities and FTA fall, and the lost FTA becomes turnovers.
   - Overloading a player beyond his historical load lowers his conversion.
   - The penalty coefficients are learned and kept in [0, 4].
4. **Defense, broadcast.** One 15-number shift (3 action, 6 location,
   6 conversion), computed from the defenders' mean and SD, is applied
   identically to all five attackers. The budget is then re-imposed. There is
   no attacker-specific or assignment structure. This is the main suspect in
   the five-center failure (see the roadmap).
5. **Rebounds and renewal.** The five offensive collector scores (prior odds,
   own head and teammates' facilitation) compete with defensive recovery. The
   result renews possessions: `U = B / (1 − m·r)`. Renewed possessions repeat
   the same process.
6. **Points.** Native points are 2·(two-point makes) + 3·(three-point makes)
   + FTA·FT%.

FT% and assisted share come from a frozen copy of the starting offense; they
are not trained in this stage.

## Training and forecasting

See [lineups/train.py](lineups/train.py). Per origin:

- **Inner fit.** Train on the 5-year prefix before the previous quarter,
  scoring that quarter after each epoch. The best epoch is selected with
  patience 8; there is a 96-epoch cap.
- **Final fit.** Train afresh on the prefix before the outer quarter for
  exactly that many epochs.
- **Forecast.** Use the final weights ("direct") and the mixture of the last
  five checkpoints.

The loss averages four event-family likelihoods (counts, location,
conversion, recovery), each normalized by a shared reference, plus
0.25 × point MSE pooled by game and offense five. The optimizer is Adam with
lr 1e-3, weight decay 1e-4 and gradient clipping at 5. Row weights decay with
a 730-day half-life. The reference starts each origin from a separately trained
v14 offense (`EventModel.from_parent`); single-stage training from
`EventModel.fresh` is being evaluated.

Forecasts are calibrated with a prior-only affine map and blended 50/50 with
additive_defense ([lineups/evaluate.py](lineups/evaluate.py)).

## Known limitations

- Defense has no matchup or coverage structure (step 4).
- Bounded tanh heads may extrapolate flat outside observed lineups; this is
  untested.
- Shot quality is not observed, because there is no tracking data. Location
  buckets come from play-by-play distance.
- Explanations come from ledger accounting and switched-off paths. They are
  not causal player credit.
