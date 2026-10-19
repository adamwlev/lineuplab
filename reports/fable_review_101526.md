# Review of the model and tool, with a v2 direction — 2026-10-15

Adam asked for a critical review of what the project has arrived at: whether
the architecture makes sense for a tool meant to extrapolate to unseen lineups
while capturing nonlinear combinations, what is unexplored, how rigorous the
modeling is, and what a v2 should change. This is a reading of the repository
as of 2026-10-15 (commit 69a1abb0), not a new result. Every number below is
quoted from a report or the code it names. Claude wrote most of what is under
review, and tried to be harder on it for that reason.

## The short version

1. **The engineering and evidence discipline are the project's real asset.**
   Forward-in-time evaluation with per-origin normalizers and calibration,
   pre-registered protocols, frozen scorers, hash-checked fits, parity tests
   pinning the browser port to Python, and a frozen prospective record. Few
   sports models are built this carefully.
2. **The evidence says lineup outcomes are nearly additive in the model's
   inputs, at the resolution this corpus allows.** The network beats a linear
   model on the same inputs by +0.013 centered r² (11/11 seasons), but no
   pairwise points interaction survived confirmation (median detectable
   effect about 0.5 points per 100 per pair), and the 14 measured event
   interactions are worth +0.00003 r² and 0.24 points per 100 on a typical
   lineup. The tool is "built around combination effects" that the project's
   own tests find small. That tension should be stated to users as plainly as
   the scorecard states it.
3. **Pillar 2 is not solved; the band is carrying it.** Against the
   league-average opponent, the release gives five Goberts a net of about +5
   and five legal centers about +1, while the highest-exposure real five is
   about +2. In the frozen record, five Goberts beat Jokić/Westbrook by +7.0
   (calibrated R). The layer and the learned module move these by under a
   point each. The out-of-support reasons fire, and the capacity arm pulls
   the other way, so the band is honest. But the printed number on the
   flagship weird lineup is still wrong in the direction Adam's prior says.
4. **Pillar 3's band does not widen with distance from the data.** `lineups/band.py`
   uses a constant model-error variance (τ² ≈ 10 per side) plus a cross-era
   term. "Thin player data" and "composition beyond every trained lineup" add
   a sentence, not width. The 80% band's coverage has not been checked on
   held-out seasons; τ was estimated on the same 2016–2026 window as
   everything else.
5. **A v2 should stop trying to learn extrapolation from a 5-year window of
   coach-selected lineups and build the two structures the history points to
   but never built:** a role-slot offense (someone must bring the ball up, as
   an assignment, not a penalty) and a measured who-guards-whom defense.
   Alongside: one model trained across 2002–2026 with league context, and
   uncertainty that propagates the player-state posteriors the pipeline
   already computes and then throws away.

## 1. Does the architecture make sense?

**What is right.** An expected-event ledger with conservation laws (one
usage budget, renewal through offensive rebounds, points as an accounting
identity) is the right skeleton. Identity-free inputs make hypothetical and
cross-era lineups possible at all. The deconvolved capability banks (the
97/49-wide GLM library) were the single largest accuracy gain in the
project's history. Forward calibration per seed is correct. Two-phase training
from scratch removed a dependency on old parents. All of this should stay.

**What does not fit the stated goal.**

- **Moment pooling is the wrong set representation for weird lineups.** Each
  player reads the other four's mean and SD; the defense reads the five
  defenders' mean and SD. For five copies of a player the SD is exactly zero,
  a region no real lineup occupies, and the tanh heads extrapolate along it.
  Clone lineups are ill-posed under this architecture by construction, not
  because of a weight. The same holds for five distinct centers: the mean of
  five centers' states describes "the average lineup that contained a
  center", and the heads never saw a mean that far out. Order-statistic
  pooling was tried only for accuracy ("settled") and found nothing to add on
  real lineups. For pillar 2 it is a different question: the best passer's
  assist rate is a coordinate on which "no ball handler" is a real, bounded
  value, and on which a declared monotone shape can act.
- **The training window is five years for a tool that spans twenty-five.**
  The release model has seen 2022–2026 lineups only (335,763 rows,
  2021-10-20 onward). The tool offers player-seasons from 2002. The
  cross-era check found a model forecasting another era keeps 56–66% of its
  in-era centered r² (−0.045 in both directions). The era with ten times
  more three-big support (2002–2013) is used only in side backtests, never
  in the shipped model.
- **Defense is a broadcast shift.** One 15-number effect from the defenders'
  mean and SD, applied identically to all five attackers. This was diagnosed
  in the 2026-10-06 review and is still the release. Every learned coverage
  variant since (matched defender by sorted position, tethered help) learned
  nothing, for a reason the pilots report states: "learned terms leave the
  extremes alone". The assignment those variants read was a sort on listed
  position, not a measured matchup.
- **The two halves of a margin are independent.** A live-ball turnover
  never costs points at the other end. Possession start types are in the
  play-by-play (points per possession after a steal 1.27 vs 1.06 after a
  score, by the ideas report's quick count). This is roadmap P3 and has never
  been built. It is the one mechanism by which "no ball handler" would cost a
  lineup twice by accounting rather than by assertion.
- **The creation constraint is a soft proxy that the data say is too soft in
  range.** Supply is the sum of the five assist rates; shortage is a log
  ratio; the fitted k_supply is about 0.1. At full strength (k = 1) it costs
  −0.02 r², so it was dropped as an assumption arm. But the capacity
  confirmatory report also finds that both models **over-predict real
  offenses whose best passer has under 5 assists per 100 by 2.3 ± 0.5
  points** (105,323 possessions). That is an in-range, measured creation
  shortfall the network has not learned. The fix need not be an assumption:
  a creation term that reads the best passer (an order statistic), fitted on
  real lineups, can be checked forward on that cohort. The creation-law
  report rejected a hinge because a threshold "would be fitted to the
  answer"; a term fitted to the 2.3-point in-range residual is fitted to
  data, and whatever it then says about five Goberts is a consequence.
- **Player-state uncertainty is computed and discarded.** The state sweep
  does empirical-Bayes shrinkage with per-coordinate effective exposure; the
  capability library carries coefficient SDs and 32 joint draws per
  snapshot. None of this reaches the band. "Thin player data" is a string.
- **The model is small and the signal is small.** 25,106 trainable parameters
  in the event model, 4,528 in the pairwise module. That is appropriate for
  the data, and it explains why width, attention and extra message rounds
  never helped. It also means the architecture debate is not about capacity;
  it is about which structure is imposed where the data end.

Smaller observations: the calibration slopes are 0.78–0.83, so native
forecasts are about 25% over-dispersed and every hypothetical lineup's
deviation is shrunk by that factor; it would be worth checking calibration by
native-forecast decile rather than assuming one slope. The role features
include each player's historical teammates' averages, which is dated and
legitimate for prediction but means a player's "capability" input partly
encodes who he played with. Home court is not an input anywhere in the event
model, although `nba.games` has it; as a nuisance covariate it would cut cell
noise.

## 2. The nonlinearity thesis against the evidence

Adam's direction (2026-10-13): "The ability to extrapolate in a non linear
manner is what I want to show off." The evidence base for nonlinearity in this
corpus is:

| Finding | Source |
| --- | --- |
| Network vs linear on identical inputs: +0.013 centered r², 11/11 seasons | nn_vs_linear |
| Best/worst player rates explain under 0.2% of the network's residual | nn_vs_linear addendum |
| No pairwise type interaction on points confirmed; MDE about 0.5 per pair | interaction discovery |
| 14 event interactions held up, worth 0.1–0.3 points per 100 per pair | interaction discovery |
| Layer in the forecast: +0.00003 r²; mean adjustment 0.24, 99th pct 0.9 | combination layer |
| Learned module, half strength: +0.0010 (0.0008) on 2016–21, −0.0007 (0.0012) on 2023–26 | confirmation |
| Familiar defensive fives beat the forecast by about 2 points in both eras | era backtest, familiarity check |

Two readings are consistent with this, and the project has not separated them:

- **Basketball is close to additive in capability space**, and the network's
  edge over linear models comes from the ledger's accounting nonlinearities
  (budget, renewal, softmax mixes) rather than from teammate interactions.
- **The test is blind.** Interactions are measured between coarse type
  dummies (20th/80th percentiles) on lineups coaches chose. Coaches avoid
  combinations that fail, so the observed range of combinations is narrow and
  the observed interactions are biased toward zero or positive. The
  selection-on-the-outcome memory says exactly this, and it cuts against the
  "additive" conclusion as much as against optimistic extrapolation.

The cheapest decisive experiment in the whole backlog is the **simulation
check** (ideas report, idea 6): simulate a league with known synergies and a
coach who keeps what works, run the discovery pipeline on it, and see what it
recovers. Until that is done, "the data say additive" is an observation about
the pipeline as much as about the game.

Meanwhile, the largest measured non-additive effect in the data, familiarity
(about 2 points, replicated in both eras), is excluded by the identity-free
rule, while 0.1–0.3-point type effects are featured. AGENTS.md allows shared
history as an optional labeled layer. The tool could at least show it as a
note on real units.

## 3. Pillar 2: where the flagship lineup stands

Release model, era-relative inputs, against the league-average opponent
(combination layer report; learned module release report):

| Lineup | Network net | With layer | Learned adds |
| --- | ---: | ---: | ---: |
| Highest-exposure real five | +2.22 | +2.08 | +0.43 (Timberwolves) |
| Five legal centers | +1.01 | +0.83 | −0.84 |
| Five Goberts | +5.04 | +4.90 | −0.14 |
| Five Jokićs | +14.30 | +13.59 | −1.51 |

Frozen record, calibrated R: five Goberts beat Jokić/Westbrook by +7.0; legal
centers by +2.7. Capacity (C): −1.2 and −3.6.

So the printed forecast still says five Goberts are a better lineup than any
real one. The reasons fire ("no ball handler", "composition beyond every
trained lineup"), C disagrees by 6–8 points, and the band spans both. That is
the "acceptable outcome" of AGENTS.md, as the creation-law report says, "not
the best one".

Why every learned attempt was inert is now well understood and worth stating
as a design principle for v2: **a structure that only binds off-support gets
no gradient.** Every real lineup has a handler, so no learned creation term is
ever pushed; every real defense has at most three bigs, so rim saturation
beyond three is unidentified. The two ways out are (a) structures that bind
*in range* on identifiable cohorts (the 2.3-point low-passer residual; the
0.5-point-per-big defensive residual in 2007–2013), fitted there and carried
by their declared shape, and (b) structures whose extrapolation is fixed by
construction (assignment, conservation), initialized to reproduce R exactly
and judged on in-range non-inferiority. The capacity arm was (b) and was
contradicted in range because its particular assertion (two inside
defenders) was wrong, not because the approach is.

## 4. Pillar 3: the band

What the band is (`lineups/band.py`): interval = [min over assumptions − Z·sd,
max + Z·sd], Z = 1.28, sd² = τ² (10.25 offense, 10.45 defense, 19.83 margin)
+ cross-era variance × share of pre-2022 player-seasons. Assumptions: R, C,
K (pairs keep adding), N (no learned module).

Problems:

- **Width is constant on the in-support part.** CLOSEOUT step 4.1 planned τ
  as a function of novelty, thin data and composition-distance percentile,
  fitted on earlier seasons and checked on later ones. That was not built.
  The only things that widen a band are the assumption spread and the
  cross-era share. For five Goberts the assumption spread does the work; for
  a thin rookie or an unusual but non-extreme five, nothing does.
- **Coverage of the shipped band is unvalidated forward.** τ comes from
  split-half residuals over all of 2016–2026. There is no report of the 80%
  band's coverage on a held-out season, by support bin.
- **The cross-era term uses one direction's evidence.** `CROSS_ERA_VARIANCE`
  is 4.0 (relative) and 5.3 (as-was), from direction A, where translation
  helped. In direction B translation hurt. The decision rule declared before
  scoring chose as-was; the tool's default is era-relative (Adam's choice,
  documented). A default that the pre-declared test rejected, with a band
  term that cites only the direction where it looked good, is the one place I
  found where the documentation is cleaner than the decision.
- **Assumption disagreement is a sensitivity, not a probability.** The band
  is labeled that way, which is right. But with two arms that share the same
  offense, "no ball handler" cannot widen the offensive side at all, as the
  capacity report notes. The band needs an offense-side arm that is not
  contradicted in range (section 1, creation term on the best passer).

## 5. Rigor

Strengths: forward evaluation with inner/outer separation; protocols
committed before runs and deviations reported (the layer's hold/continue
swap, the module's level diagnosis); independent reviews of v16–v20; frozen
scorers; hashes; parity tests at 1e-4 to 1e-13; honest labeling of
exploratory versus confirmatory; the prospective 2026–27 freeze.

Soft spots:

- **One window, reused.** The 44 quarters of 2016–2026 have judged v2–v20,
  eight nonlinearity screens, the discovery, the layer and the band. The
  learned-module confirmation on 2016–2021 is called "fresh quarters"; it is
  fresh relative to the 2022–2026 screens, not to twenty versions of
  architecture development. The report acknowledges the held-up cells were
  discovered there. The prospective record is the only truly unseen test and
  it has not been scored.
- **Differences at the noise floor decide things.** Arms differ by
  1e-4–1e-3 r² against a season SE of about 1e-3. The project usually says
  "noise" and decides on other grounds, which is fine. But the module
  entered the forecast on +0.0010 (0.0008) and −0.0007 (0.0012): no evidence
  either way, decided by preference at half strength. Preference is a
  legitimate basis for a product decision; it should not be described as
  confirmed.
- **Decisions of record that override declared rules.** Era-relative default
  (rule said as-was); module in the number (rule said only held-up effects);
  layer held at measured counts (protocol said continue). Each is documented
  and reasoned. Collectively they mean the shipped forecast is about one
  third protocol and two thirds judgment, and the scorecard should say so in
  one line.
- **The calibration carried into the clean release** is from fits on the old
  data; stated, and the right call for Saturday, but the clean release is
  not re-scored.
- **Confounded property.** handler_turnovers passes 39–55%: swapping the best
  passer for a low-assist player often lowers forecast turnovers because the
  incoming player's own turnover rate is lower. The suite notes this and
  added the teammate version. A property that an additive model can fail by
  construction is a weak property.

## 6. What I would do in v2, in order

**A. Cheap diagnostics that change what the rest should be (days).**

1. Simulation check of the discovery pipeline under coach selection
   (section 2). Decides whether "additive" is the game or the test.
2. Forced lineups as natural experiments: games where a regular is out
   (injury, ejection, foul trouble) produce fives not chosen for performance.
   Build that cohort from box scores and score the release on it. It is the
   closest thing to a selection-light test of unusual lineups with outcomes.
3. Coverage of the shipped band on 2022–2026 by support bin; calibration by
   native-forecast decile.
4. The five-Gobert ledger channel by channel against Jokić/Westbrook, with
   each channel's in-range analogue beside it (the low-passer cohort, the
   3+-big defensive residual). Shows which channel carries the +7.

**B. Uncertainty that moves (a week).**

5. Propagate player-state posteriors. The EB sweep has per-coordinate
   effective exposure; the library has coefficient SDs and joint draws.
   Sample or linearize through the ledger. The browser model now evaluates a
   warm lineup in about 90 ms, so 16–32 samples are affordable, and the
   `alone()`/`split()` projections already give a cheap delta-method route.
   Then "thin player data" widens the band by a computed amount.
6. τ as a function of support features, fitted 2016–2021, coverage checked
   2022–2026; conformal adjustment by distance bin.
7. Report the assumption spread as a function of composition distance on
   real lineups, so users can see the band's claim that it grows.

**C. Structure that binds in range and extrapolates by construction (the
core of v2; weeks).**

8. **Who-guards-whom from the play-by-play.** Blocks, shooting fouls and
   steals name a defender and an attacker (about 1.4M pairs). Fit an
   assignment model P(j guards i | heights, positions, roles), validate on
   held-out pair events, then let per-attacker defense read the measured
   assignment. This gives the coverage structure a real target instead of a
   sort on listed position.
9. **Slot-filling offense.** Soft-assign five players to five functional
   slots (initiator, screener/roller, two spacers, finisher) with Sinkhorn,
   each slot filled exactly once; slot fit reads capabilities; initialize at
   uniform assignment so the model starts at R. Slot-conversion curves are
   fitted on the role-change library (907 large observed shot-share changes)
   and on the low-passer cohort, where they bind in range. Five Goberts then
   put a Gobert in the initiator slot at a Gobert's initiator fit, which is
   thinly measured and therefore wide.
10. **Creation term on the best passer**, the minimal version of 9: an
    order-statistic input with a declared monotone shape, fitted to the
    2.3-point in-range residual, checked forward on that cohort.
11. **Possession chaining.** Predict each lineup's ending distribution and
    each lineup's offense by start type; compute the margin from the
    two-team chain. Live-ball turnovers then cost points at the other end by
    accounting.
12. **Monotone and ordered pooling as architecture, not as a test.**
    Properties with declared directions (spacing_rim, handler_conversion, rim
    saturation) can be built into monotone networks or lattice layers instead
    of checked afterward with 40–98% pass rates. This is a different class of
    model from anything tried: shape-constrained by construction, nested at R.

**D. One model across eras (weeks, mostly CPU).**

13. Train on 2002–2026 with league-environment covariates (pace, three-point
    rate, era normalizers as inputs). Judge it on the era backtest and the
    2016–2026 benchmark together, with the 0.003 r² trade printed. This is
    the only route by which the three-big support of 2002–2013 reaches the
    shipped forecast, and it is a prerequisite for the tool's cross-era
    promise to rest on more than a 56–66% transport number.

**E. Product honesty (days).**

14. Show the disagreement, not only the point: for lineups beyond support,
    lead with the assumption range and the reasons, and demote the point.
15. State the size of combination effects where they are shown: "worth about
    a quarter of a point on a typical lineup; the model's edge over adding up
    players comes mostly from its possession accounting".
16. Offer the familiarity note on real units as a labeled layer.

**Classes I would not spend on:** generic capacity (width, attention, more
message rounds; settled), a possession-sequence transformer (loses the ledger
and cannot fix extrapolation), identity embeddings or pair chemistry as the
main representation (ruled out and at the noise floor). Simulation-based
inference of a full agent-based possession model is the one heavy idea that
could extrapolate by mechanism; I would keep it as a later bet behind 8–12.

## 7. Smaller fixes

- Add home/away (and possibly rest) as nuisance covariates in training; they
  cut cell noise and cost nothing at forecast time.
- Finer shot geography (distance in feet, dunk/layup/jumper) so rim
  deterrence is a shift in a distribution rather than a bucket.
- Rookie fallback from draft slot or college priors instead of the
  population mean.
- Replace the type-dummy discovery with a continuous interaction screen
  (products of standardized capabilities) when the second discovery round
  runs; the 20/80 cut discards power.
- Score the prospective record as soon as the refresh is allowed; it is the
  only unseen evidence and every argument above would be sharpened by it.

## Closing

The project has built the measurement apparatus to find out whether lineup
value is additive, and the apparatus says: on observed lineups, nearly so,
with the network's edge coming from its accounting. The product promise is
about where observed lineups are not. That gap cannot be closed by learning
on the same window with more capacity; the history of v4–v20 and eight
screens shows that. It can be closed, partly, by structures that bind on
identifiable in-range cohorts and extrapolate by construction, by a model
that sees the eras where unusual lineups were common, and by uncertainty
that is computed rather than narrated. That is what v2 should be.
