# The neural model: current reference and historical foundation

## Current reference — 2026-10-09

The retained research model is **v16 J_POINT_BOTH**, called **P_BASE** in v20.
V17–v20 experiments are complete; their architectures were tested but not
automatically adopted. This is not the [shipped additive page](CURRENT_MODEL.md).
The [v20 review](../../reports/joint_capability_v20_scientific_review.md) owns the
current evidence and limitations; the sections below describe the v14/v15
foundation, not all inputs or fitting choices of the retained model.

The changes from that foundation are:

- **Adjusted player-capability inputs on both sides**, alongside raw dated
  profiles. The offensive bank has 97 coordinates: own and teammate-influence
  coefficients, their opportunity/support and curvature descriptors, and staleness.
  The defensive bank has 49 coordinates for its single coefficient bank and
  analogous metadata. These are upstream regularized estimates, not player-ID
  embeddings or known-pair chemistry. Curvature descriptors are not guaranteed
  calibrated posterior uncertainty.
- **Joint adaptation.** Small centered, tanh-bounded heads read own adjusted
  offense, other-four mean/SD, adjusted rebound-donor inputs, and the opposing
  five's adjusted mean/SD. The raw offense/rebound networks and defensive adapter
  are trainable. A frozen parent supplies unsupported assisted-fraction and own
  FT-conversion outputs; these cannot drift merely through shared hidden weights.
- **Pooled defense, not assignments.** J_POINT_BOTH uses D_MAIN_RB, plus the
  adjusted-defense head. Channel-specific defensive shifts are broadcast across
  the attackers; each attacker's different baseline probabilities still produce
  different percentage/point responses. There is no learned one-to-one assignment,
  shared coverage capacity, attention block, separate phase head or explicit action
  allocator in this particular retained arm. Those were separate ablations.
- **Event and point training.** The four normalized event-family losses are
  supplemented by a normalized team-point term with coefficient .25. Training
  observations are game × offensive-five × defensive-five aggregates; they are
  not equally weighted quarter-average outcomes. The inner validation quarter
  precedes and does not overlap the outer evaluation quarter. Final fits restart
  on the complete prior prefix for the selected duration.
- **Explicit accounting remains.** Positive action rates share a usage budget;
  creation/load constraints, defensive channel changes, recovery and stationary
  renewal produce event counts and expected points. Ordering and phase variants
  have been evaluated, not all adopted. This is not possession-by-possession
  simulation or a tracking-derived shot-quality model.
- **Prediction pipeline.** Direct and checkpoint-average neural predictions get
  their own prior-only calibration. V20's registered primary averages checkpoint
  predictions and seeds, then blends equally with additive_defense. The older
  single-checkpoint half remains reported. Neither a blend nor a calibration
  coefficient is a learned player profile. Neutral-opponent mode integrates over
  historical opponent lineups, not a single zero-feature team.

Code: [arm specification](../../experiments/joint_capability_v16_protocol.py),
[joint model](../../experiments/joint_capability_v16_model.py),
[equivalent optimized forward pass](../../experiments/v16_fast_model.py),
[loss/selection](../../experiments/joint_capability_v16_fit.py),
[v20 scoring](../../experiments/v20_report.py). V20's optional upstream clock adjustment,
clock decoder and S5 selection are distinguished in the
[frozen factorial plan](JOINT_CAPABILITY_V20_PLAN.md); P_BASE does not acquire
those changes merely because it appears on that leaderboard.

## Historical foundation — v14/v15, 2026-09-18

The remaining sections preserve the earlier description of v14 `RB_RENEW_FAC`
offense plus v15 defensive adapters. Their references to v16 as planned, and
their loss/freeze descriptions, are historical. The exact prior page is
[archived](archive/2026-10-09_v20_closeout/NEURAL_MODEL.md). They must not be
read as the current training or acceptance status.

Use the [scorecard](../../MODEL_SCORECARD.md) for results and
[CONTEXTUAL_MODEL.md](CONTEXTUAL_MODEL.md) for the product contract. Architecture
alone does not establish basketball coherence or OOD calibration.

## 1. What goes in

The model represents players with **dated statistical profiles**, not learned
player-ID embeddings or known-pair chemistry. Player-state histories for training
examples stop before their game; outer-quarter state inputs are frozen at the
quarter's start. Thin/no-history players receive pooled prior states and
disclosed support, not zero ability.

The main offensive state has 18 coordinates:

| Coordinates | Meaning |
| --- | --- |
| 3 log rates | FGA, FTA and turnovers per possession |
| 6 centered location logits | Rim, paint, midrange, long midrange, and two three-point buckets |
| 6 make logits | Conversion conditional on those location buckets |
| 1 FT make logit | Own free-throw shooting |
| 1 log assist rate | Passing-supply descriptor |
| 1 assisted-make logit | Finishing-demand descriptor |

Rate/mix profiles emphasize recent history (180-day half-life); shooting uses
730 days and empirical-Bayes shrinkage. The initial location-conversion profile
uses pooled two-/three-point player offsets around dated league bucket rates,
not six unconstrained independent skill estimates. These are play-by-play
location categories/proxies, not tracking-derived shot difficulty or openness.

The retained role head also reads eight dated descriptors: four recent-minus-
long contrasts (usage, three share, turnovers, assists), and four historical
other-teammate averages (usage, assists, three attempts, assisted share).
The rebound head reads 28 inputs: the 18 standardized states, those eight role
descriptors, and two rebound prior/support features. Input standardization is
fit inside the appropriate training prefix.

Sources: [v3 states](../../experiments/joint_capability_v3_data.py),
[v14 input assembly](../../experiments/joint_capability_v14_inputs.py).

## 2. How the five offensive players affect one another

For each player, a shared small network reads his standardized state plus the
other four players' **mean and standard deviation**. The mean describes the
available teammate capabilities; the spread distinguishes varied from
duplicated skill sets. It produces a correction to his anchored state.

The retained block is equivalent to a 54-input, 32-hidden-unit tanh network
with 18 outputs (the SD contribution enters the same hidden layer).
A separate 26→32→18 head reads own state plus the eight role descriptors.
A learned coordinate-wise affine decoder converts contextual states to event
parameters. There is no free player lookup table in these heads.

Parameters are shared across players, so permuting lineup slots only permutes
player outputs. The FT-conversion context correction is masked: teammate or
defender context does not change a player's own free-throw percentage.
Removing messages is a diagnostic intervention; it is **not** the fitted
additive model or a clean causal estimate of “chemistry.”

Sources: [v9 pooling](../../experiments/joint_capability_v9_model.py),
[v13 role/constraints](../../experiments/joint_capability_v13_model.py),
[v14 backbone](../../experiments/joint_capability_v14_model.py).

## 3. Positive actions, finite usage, and creation/load constraints

The decoder produces positive FGA/FTA/TO rates, a softmax over locations, and
sigmoid make probabilities. The five players share a finite opportunity budget:

```text
U = sum over players (FGA + 0.44 × FTA + TO)
```

The 0.44 factor is an accounting convention, not a simulated whistle sequence.
Rates are rescaled to conserve U; five high-usage players do not each keep an
entire historical workload.

Learned nonnegative coefficients penalize conversion when implied assisted-
finishing demand exceeds passing supply, or assigned load exceeds the player's
historical load. The retained supply constraint also reduces FTA under shortage
and routes the removed usage units to turnovers. A separate FGA-versus-turnover
routing variant was tested in v14, but is **not** the retained RB_RENEW_FAC parent.

These are explicit structural assumptions fitted on observed events. They are
not a fully identified optimizer assigning basketball roles, and they have not
solved all-center offense.

## 4. Offensive rebounds create more opportunities

An offensive player's recovery score combines his rebound prior, a learned
own-capture head, and the average learned facilitation contributions from the
other four. The facilitation contribution excludes the collector himself.
The five collector scores compete with one defensive-recovery category through
a six-way softmax.

Let r be predicted team offensive capture probability, m the eligible-live-miss
rate per usage unit, and B the prior-fitted non-rebound opportunity budget.
The stationary renewal decoder uses:

```text
U = B / (1 − m × r)
ORB = U × m × r
U − ORB = B
```

More offensive recoveries therefore produce more attempts; a board receives no
separate arbitrary point bonus. The eligible-miss adjustment and B are fitted
from prior data. The current decoder assumes renewed offense repeats the same
action/location/conversion process. A distinct post-rebound process is a
**planned v16 experiment**, not an implemented feature.

Source: [ReboundHead, renewal_budget and Model14](../../experiments/joint_capability_v14_model.py).

## 5. What v15 adds about the opposing five

Each defender has 19 strictly dated descriptors: own steals, blocks, defensive
rebounds and committed fouls; opponents' on-floor turnover/FTA rates; six allowed
location shares; six allowed conversion rates; and log exposure. These use
365-day decay and pooled-prior shrinkage. The committed-foul numerator is the
available total committed-foul field, not a demonstrated defense-only measure.

Raw on-floor opponent rates confound teammates, opponents, scheme and
deployment. These are **descriptors, not individually deconfounded defensive
skills**. The adjusted-capability proposal in v16 addresses that distinction.

| Adapter | Learned addition |
| --- | --- |
| D_MAIN | Defensive mean/SD (38 inputs) → 32-unit tanh head → 15 corrections: 3 action, 6 location, 6 conversion |
| D_CROSS | MAIN plus a rank-8 interaction between each attacker's 18-state profile and the defensive summary |
| D_MAIN_RB | MAIN plus a defensive recovery-strength head |
| D_CROSS_RB | Both cross interaction and recovery |

Effects subtract the head's zero-reference value and are bounded with tanh.
They change pre-renewal actions/mix/conversion, conserve the opportunity
accounting, then recompute missed shots and renewal. Stronger defensive
recovery lowers offensive collectors' odds. No adapter modifies FT conversion.

**v15 freezes the entire offensive parent.** Only these new defensive adapters
are trained. It is not joint offense/defense retraining, does not infer
individual defensive assignments, and is not a transformer. Matched inner and
final parent checkpoints have the corresponding historical cutoffs.

Sources: [defensive states](../../experiments/joint_capability_v15_data.py),
[adapter](../../experiments/joint_capability_v15_model.py),
[frozen-parent fitting](../../experiments/joint_capability_v15_fit.py).

## 6. Points, calibration and the half forecasts

Native points are the accounting identity: sum predicted makes at two/three
points each, plus expected made free throws. Native event contributions
reconcile to this score. A separate affine calibration maps it to observed
points per 100 using only **previously completed** evaluation windows:

```text
calibrated = league_reference + intercept + slope × (native − league_reference)
```

Calibration is not additional shot creation. A player/event explanation must
show any calibration adjustment separately rather than claim native
contributions directly sum to the final calibrated or blended forecast.

The v15 leaderboard notation is:

| Name | Forecast |
| --- | --- |
| additive | A: corrected additive offense |
| additive_defense | A+D |
| nn | N: calibrated frozen v14 RB_RENEW_FAC offense |
| nn_defense | N+D |
| parent_half_defense | .5(A+N)+D |
| prediction | P: the new adapter's calibrated forecast |
| half | .5(A+D+P) |
| half_offense_A | .5(A+P), an opponent-blind additive-side sensitivity |

D is centered/calibrated prior additive defense; positive D means an easier
opponent. Adding D retains A/N's old offensive calibrations, whereas P gets
its own. The resulting comparison is not calibration-neutral; the
[v15 review](../../reports/joint_capability_v15_codex_review.md) measures that issue.

Sources: [controls](../../experiments/joint_capability_v15_controls.py),
[runner/calibration](../../experiments/joint_capability_v15_run.py).

## 7. How learning and evaluation work

The retained v14 offense was trained with normalized event-family losses,
native team-point loss, six-way rebound likelihood and regularization.
Its learned parameters include context/role networks, diagonal decoder,
creation/load penalties and capture/facilitation heads. Profile construction,
probability links and the accounting identities are not free NN parameters.

v15 trains on **game × offensive five × defensive five aggregates**, retaining
individual action counts and exposure. These are sufficient-count likelihood
targets, not unweighted quarter-average ratings or one SGD example per
possession. The four equally weighted, prefix-normalized families are Poisson
action counts, multinomial location, binomial conversion and six-way recovery.
v15 adds **no new team-point loss** while fitting its adapter.

v15 uses Adam (learning rate .001, weight decay .0001), game-group batches,
gradient clipping at 5, a five-year training lookback and 730-day example
decay. For each quarterly origin:

1. Fit the inner model on the prefix before the most recent completed quarter.
2. Use that completed quarter for early stopping: cap 96 epochs, patience 8,
   meaningful-improvement tolerance 1e-5. Save the actual minimum-loss epoch;
   the tolerance controls patience, not which minimum is selected.
3. Start a fresh final adapter fit on the full pre-origin prefix for exactly
   that selected number of epochs.
4. Evaluate the next, disjoint outer quarter with origin-date states and
   prior-window point calibration. Outer outcomes do not select epochs.

There are 48 origins (2015–2026), three seeds and four adapters; the primary
scorecard uses 44 quarters after warmup. Training groups, point-evaluation cells,
and bootstrap season blocks are different units. The
[scorecard](../../MODEL_SCORECARD.md) specifies the matched and broader populations.

## 8. Two-lineup use, explanations and uncertainty

The same offensive scorer can be evaluated in both directions against the
opposing five, then differenced for a matchup margin. Average-opponent mode
integrates over prior observed defensive lineups; zero standardized features
are not automatically the league-average nonlinear prediction. Reference
sampling/convergence still needs work before fine user-facing comparisons.

Saved event responses and controlled interventions support basketball-readable
explanations. They do not identify causal player credit. Reasonably calibrated
finite-game residual bands do not establish uncertainty about a synthetic
lineup's true mean; neither do three-seed disagreement or integration error.

Current gaps: implausibly strong all-center offense, action/role transport,
deconfounded capabilities, separately modeled post-ORB actions, stable
average-opponent integration and latent-quality/OOD uncertainty. Rich tracking
and explicit assignments are absent. None is hidden by a coverage gate.
See the [backlog](../../MODEL_RESEARCH_ROADMAP.md) and
[v16 plan](JOINT_CAPABILITY_V16_PLAN.md) for proposed work, not claims of
implemented capability.
