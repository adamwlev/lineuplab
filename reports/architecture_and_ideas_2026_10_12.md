# Architecture overview and new ideas — 2026-10-12

Adam asked for an architectural overview and a brainstorm of brand-new ideas.
This is a planning document, not a result. Numbers marked "quick count" come
from one read-only query each and have not been audited.

## 1. The current architecture

### Data

- **`nba.possessions`**: 6.06M possessions in 32,173 games, 2001–2026, each
  with:
  - the ten players on the floor;
  - the clock and points scored;
  - play-by-play text: shot type and distance, assists, blocks, fouls,
    steals, turnover type and substitutions.
- **Training rows.** 1.59M rows of game × offense five × defense five, with
  per-player counts: FGA, FTA, turnovers, six-zone attempts and makes, and
  rebounds.
- **Listings.** Height and position (`nba.players`).

### Inputs

Inputs are per player and dated. No player identity enters the model.

- **Offensive state.** 18 coordinates:
  - FGA, FTA and TO log rates;
  - six location logits and six make logits;
  - FT%, assist rate and assisted-make share.

  They are empirical-Bayes shrunk with 180/730-day decay
  (`lineups/states.py`). The state also carries 8 role contrasts and a
  rebound profile.
- **Defensive descriptors.** 19 per player.
- **Capability library.** Monthly snapshots of lineup-adjusted (deconvolved)
  GLM coefficients: a 97-wide offense bank and a 49-wide defense bank.

### Model

`lineups/model.py`, `EventModel`: the expected event ledger of one
possession.

1. **Offense.**
   - Inputs: each player's state, the leave-one-out mean and SD of the other
     four, and role history, plus bounded heads on the adjusted capabilities.
   - Output: the player's shifted state.
2. **Usage conservation.** FGA + 0.44 FTA + TO is rescaled to a shared
   budget.
3. **Creation constraint.** Assisted-finishing demand is set against passing
   supply. The penalties are soft, and the fitted coefficients are small.
4. **Defense.**
   - *Reference.* The mean and SD of the five defenders produce one shift
     of 15 effects (actions, location, conversion), identical for all five
     attackers, plus a rebound-recovery strength.
   - *Capacity v2.* A top-two inside pool and a sorted-position pairing.
5. **Rebounds and renewal.** Offensive-rebound collector scores give a
   geometric series of renewed possessions.
6. **Output.**
   - Points per 100 and the per-player ledger.
   - Margin = A's offense against B minus B's offense against A.

### Training and scoring

- **Training.**
  - Two-phase: offense alone, then the defense.
  - Loss: event likelihoods plus 0.25 × the point loss.
  - Data window: a 5-year lookback with a 2-year half-life.
  - Inner-quarter early stopping, then the average of the last five
    checkpoints, over three seeds.
  - About 20 CPU-minutes per fit.
- **Scoring.**
  - 44 quarterly origins, 2016–2026.
  - Prior-only affine calibration; broad offense-five cells.
  - Raw and centered r².
- **Pillar tools.**
  - The property suite (`lineups/properties.py`);
  - support reasons (`lineups/support.py`);
  - the assumption band, reference vs capacity.

## 2. What the architecture cannot see

| Built-in assumption | Consequence |
| --- | --- |
| A row is a bag of possessions | No possession start type (transition), clock, score or stint length. The two halves of a margin are independent, so a turnover never costs points at the other end. |
| A lineup is summarized by moments of its players | Five copies of a player look like one player's profile; no role has to be "filled once". |
| No who-guards-whom | Per-attacker defense is broadcast or a heuristic sort; the learned versions had nothing to learn from. |
| Training rows are what coaches chose | Optional stopping and keep-what-works. Established units carry information the model ignores: familiar defensive fives are about 2 points better than forecast (`scripts/familiarity_check.py`). |
| One five-year window at a time | Cross-era use is untested; big-lineup support lives in 2002–2013. |
| Uncertainty = seeds + finite games | Nothing widens with distance from the data except the assumption band. |

## 3. New ideas

### A. Signal the model does not use (the play-by-play text)

1. **Who guards whom, from the play-by-play.**
   - *Signal.* Blocks, shooting fouls and steals each name a defender and an
     attacker. Quick count: 312k blocks, 627k shooting fouls and 488k
     steals, about 44 pairs per game and 1.4M in all.
   - *Model.* Fit an assignment model, P(defender j acts on attacker i |
     both lineups' heights, positions and roles). Validate it on held-out
     pair events. Then let per-attacker defense read the measured
     assignment.
   - *Why it's new.* The coverage screen learned nothing because its pairing
     was a sort by position. This gives it a real signal. It also makes
     "a center ends up on Murray" a measured quantity, not an assumption.
2. **Possession chaining: the margin as a two-team game.**
   - *Mechanism.* Every possession's ending sets the next one's start.
     Quick count of points per possession by start:

     | Start | Points per possession |
     | --- | ---: |
     | After a steal | 1.27 |
     | After a dead-ball turnover | 1.05 |
     | After an opponent score | 1.06 |
     | After an opponent miss | 1.10 |

   - *Model.* Predict each lineup's offense by start type and its
     distribution of endings, then compute the margin from the two-team
     chain.
   - *Payoff.* Live-ball turnovers then cost about 0.2 points each at the
     other end. A lineup with no ball handler pays twice, by accounting
     rather than by assertion.
   - This is on the roadmap as P3 and has never been built. I would promote
     it.
3. **Finer shot geography.**
   - Use distance in feet and shot type (dunk, layup, hook, jumper) instead
     of six zones.
   - Rim deterrence then becomes a shift in the distance distribution.
   - This is a smaller lever.

### B. Selection as information, and tests free of selection

4. **Deployment as a signal.**
   - Today's familiarity result generalizes. How much coaches play a unit,
     and where its minutes are trending, is information about real lineups.
   - A hypothetical lineup has none of it, so the tool reports it as an
     untested unit.
   - It must be an optional, labeled layer (AGENTS.md).
   - Already measured: +0.0013 centered r² on 2016–2026 and +0.0032 on
     2007–2013, forward and prior-only.
5. **Forced lineups as natural experiments.**
   - When a regular is out (injury, rest, foul trouble, ejection), coaches
     field lineups they did not choose for performance. Box scores identify
     those games.
   - This gives a selection-light test set for unusual lineups.
   - It also measures how optimistic in-range fits are, instead of assuming
     it.
6. **Simulation check of the whole pipeline.**
   - Simulate a league with a known capacity law and coaches who keep what
     works, then run our pipeline on it.
   - This shows which structure can be identified at all, and how biased
     the extrapolation is, before spending more fits.

### C. Structure for pillar 2

7. **Slot-filling offense.**
   - Every possession needs an initiator, a screener or roller, spacers and
     a finisher. Soft-assign the five players to five functional slots, each
     filled exactly once (Sinkhorn), and learn slot fit from data.
   - Five Goberts must put a Gobert in the initiator slot. Five Jokićs do
     not suffer.
   - "Someone must bring the ball up" becomes a conservation law, not a
     gate.
8. **The offense best-responds to the defense.**
   - Instead of learning how a defense shifts shot location, the offense
     chooses its shot mix so that marginal points per shot are equal across
     zones, given the defense's resistance in each zone.
   - Against five slow centers, the offense moves to threes until it stops
     paying. The extrapolation comes from optimization.
9. **Property-regularized training.**
   - The property suite becomes a training penalty on random synthetic
     lineups, including extremes. Directions are declared before fitting.
   - Its cost is measured against the 0.003 r² allowance.
10. **Ordered pooling for every resource.**
    - This generalizes today's P1. Rim protection, ball handling, shooting
      and rebounding each read the players sorted by that skill, with
      learned weights constrained to be non-increasing.
    - Diminishing returns hold where the data show them. The fourth and
      fifth copies are bounded by the third.
    - The era shows the third big still worth about 0.7 points.

### D. Uncertainty and transport

11. **Cross-era transport as an out-of-support test.**
    - Use the era models (2002–2013) to forecast 2016–2026 lineups, and the
      reverse.
    - Errors at real compositional distances that in-era data never reach
      give how error grows with distance from support.
    - This is the only route I see to validating a band beyond observed
      lineups with outcomes. The models already exist.
12. **One model for 2002–2026, with era context.**
    - The league environment (pace, three-point rate) is an input, and the
      model trains on 25 years of support.
    - This is a prerequisite for the tool's cross-era promise.

### Moonshot

13. **A possession-sequence model.**
    - A small transformer over possessions, with lineup tokens and game
      context.
    - It uses everything, but it loses the interpretable ledger unless its
      outputs feed the ledger.

## 4. Recommended order

| Order | Idea | First step | Cost |
| ---: | --- | --- | --- |
| 1 | Who guards whom (1) | Parse the pair events; fit and validate an assignment model on held-out games | About a day, read-only |
| 2 | Possession chaining (2) | Measure how much lineups differ in live-ball turnovers and in transition points allowed, beyond the current ledger | Hours |
| 3 | Cross-era transport (11) | Forecast across eras with existing fits; error vs composition distance | Hours |
| 4 | Forced lineups (5) | Flag games with a regular absent; build a test set of unusual lineups | Hours |
| 5 | Slot-filling offense (7) | Prototype after 1–2; the biggest pillar-2 bet | Days |
| 6 | Deployment layer (4) | Fold the familiarity correction into the model as an optional input | Hours |
