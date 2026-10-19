# Joint capability and contextual-role model: build, experiment, and test plan

Prepared by Codex for Adam and Sol, 2026-09-09.

**Status: prospective implementation contract; no implementation or new experiment
has been performed by writing this document.** The historical benchmark has been
examined repeatedly. This is a new frozen comparison protocol on that benchmark,
not an untouched holdout or a claim of causal identification.

## 0. The assignment

Build a small, jointly trained, basketball-constrained model of **what players
can do and how their production changes together**. Learn from observable event
channels, then derive points from those channels. Test whether this improves
player estimation, contextual response, or both. Preserve the incumbent and all
original research artifacts.

The ambition is a coherent replacement architecture, not another independently
estimated bonus added to the existing score. The implementation must nevertheless
reach real data early. A completed negative experiment is useful; a large pile of
untested machinery is not the deliverable.

Sol owns implementation of this contract, verification, execution of its bounded
experiments when Adam authorizes implementation, and the factual handoff. Product
requirements and the scientific contrasts below are fixed. Do not delegate to
Opus or another agent. Do not reinterpret a failed result by changing the target,
cutoffs, comparison population, named fixtures, or selection rule.

### Authority and boundaries

- This planning request does not start training. Adam's subsequent implementation
  request should explicitly include the bounded experiments and new derived
  outputs in this document.
- Read `AGENTS.md`, `CLAUDE.md`, the latest `SESSION_HANDOFF.md` checkpoint, and
  `CONTEXTUAL_MODEL.md`, then this plan completely. The three co-equal standards
  are forward prediction, basketball-coherent counterfactuals, and honest OOD
  uncertainty. A modest accuracy loss can be acceptable; print the tradeoff.
- One editor in this tree. Establish ownership with Adam before implementation.
  Preserve existing dirty work. No staging, commits, branches, stashing, resets,
  cleaning, or reverts unless separately requested.
- No scraping, network acquisition, database access, input-cache rebuilding,
  package installation, production scorer/page changes, or deployment. Existing
  cache loaders may silently build missing data: do not invoke that fallback.
- New derived joins, strictly historical features, tensors, model fits,
  predictions, and reports ARE part of the authorized implementation scope.
  Put them under the new experiment prefix. They do not replace source caches.
- Do not modify completed run directories or invalidate a frozen protocol.
  Scientific changes after execution starts require a new version/prefix and a
  written explanation; retain the old run and its results.
- Preserve `MODEL_FEEDBACK_FROM_CLAUDE.md` and Opus's original influence protocol.
  This is a separate Codex-designed research branch, not a rewrite of that work.
- Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u`. Torch is installed
  according to a read-only availability check; record its actual version/device
  during preflight. Do not assume a GPU, a runtime, or permission to install one.

### Definition of a successful implementation session

At minimum: a tested joint-model implementation; all four core arms; a complete
48-origin core experiment or an explicitly paused, resumable job; exact matched
point comparisons; a basketball panel; a first support/interval audit; and a
documented decision. A paused run is NOT a finished experiment.

The extended program adds opposing-five context, competitive rebounding, and
stronger uncertainty. Those extensions have explicit dependency and compute
gates below. Do not mark them complete when only their interfaces exist.

## 1. Starting evidence and research questions

### 1.1 What we already know

The current architecture separately estimates historical own rates, allocation,
conversion, and teammate influence. That has produced useful channel evidence,
but also overlap, scaling mismatches, and a shot-location cancellation. The new
architecture must address those failure modes explicitly.

Historical bilinear/profile-quadratic and set-attention experiments failed to
deliver useful forward gains. See `RESEARCH_OVERVIEW.md` phases 3–5 and §§18.4,
20.5; `ROLE_MODEL.md` records the capability/assignment distinction and earlier
failed role-response assumptions. These results constrain optimism. They are not
a theorem that every event-supervised constrained model must fail.

The new hypothesis is **joint estimation + direct event supervision + constrained
allocation**, not merely a more flexible function of ten identities. An ablation
must tell us which of those ingredients matters.

### 1.2 Unresolved repairs are a separate work package

`SOL_INFLUENCE_REPAIR_FOLLOWUP.md` remains outstanding unless a later checkpoint
documents its completion. The v2 mix/factor eligibility and panel-ledger defects
must not become dependencies of the new model.

- Do not run that entire repair first merely to begin this branch.
- Use the independently reproduced **parent**, **location+shooting**, and
  **corrected additive** predictions as frozen controls.
- Do not import v2 mix/factor coefficients, its panel renderer, or its inaccurate
  interpretation as ground truth.
- If Adam separately wants the repair completed, keep its outputs and accounting
  separate. This plan does not authorize completing an unrelated repair sweep.

Verified primary historical comparison (raw offensive rating, not neutralized
for defenses faced):

| Frozen control | MAE | RMSE | Pooled raw r² | Novel MAE |
|---|---:|---:|---:|---:|
| workstream structural parent | 8.1439828452 | 10.9214307921 | .1073313941 | 8.8902831104 |
| location + shooting | 8.1312316259 | 10.8964039646 | .1114178671 | 8.867432 approximately |
| corrected additive | 8.0919525369 | 10.8409940439 | .1204320480 | 8.9038988730 |

Source: `experiments/cache/influence_repair_2026_09_09_v2/` for unaffected
predictions and `experiments/cache/asof_points_centered_2026/` for the corrected
additive. Verify exact arm/key provenance, not this table's rounded values.

Primary cohort: 2016–2026, 44 quarterly origins, 5,607 lineup-quarter cells,
726,364 possessions; novel offense: 2,073 cells, 226,256 possessions. Four 2015
origins are warmup, making 48 total. These counts are for the archived common
cohort, not the full event-training population.

### 1.3 Questions, in order

1. Can a shared learned transformation improve dated player profiles without any
   learned teammate interaction?
2. Does teammate context improve conditional allocation and event forecasts over
   equally fresh own-profile controls?
3. Does learning states and contextual response together outperform learning
   either alone?
4. Do the changes carry into points and coherent counterfactuals, or only improve
   allocation among teammates while leaving team totals unchanged?
5. Does any gain survive controlling for defenses faced, era, and deployment?
6. Where are forecasts uncertain, and which parts of that uncertainty can we
   actually validate?

No player name, favorite ranking, or positive result is an acceptance criterion
for training. Named cases are held-out mechanism diagnostics.

## 2. Architecture: a small constrained set model

### 2.1 Deliberate limits of version 1

Use a shallow, shared, directed teammate-message network and an explicit event
decoder. No free player-ID embeddings, pair-ID tables, team-ID embeddings,
lineup-ID parameters, attention stack, or black-box points residual in v1.
Player IDs join histories and name outputs; they are not numeric model features.

This restriction allows a literal invariance test: identical historical states
and support metadata must receive identical treatment regardless of the name or
whether two identities have played together. It also keeps the new experiment
distinct from the old identity-attention work.

Jointly learned "capability" here means a predictive representation anchored to
historical event rates. It is not identified intrinsic talent or a causal skill
estimate. Coaches' selection and unobserved responsibilities remain confounders.

### 2.2 Causal history features

For each player at a prediction date, construct features solely from games on
earlier dates. Begin with the existing EB snapshot definitions: 180-day role
half-life and 730-day shooting half-life. Keep era level separate from player
change. No half-life sweep in the core experiment.

Required feature groups:

- own FGA, FTA, TO, assist, and offensive-rebound rates with explicit denominators;
- six location shares and location-conditioned make estimates, plus FT%;
- assisted-made share, correctly labeled as conditional on a MADE field goal;
- effective exposure, missingness, elapsed time since observation;
- recent-role contrast: 180-day versus 730-day versions of usage, 3PA share, TO
  rate, and assist rate, computed from the same strictly prior sufficient stats;
- a past-teammate reference: exposure-weighted mean of teammates' historical
  usage, assist rate, 3PA rate, and assisted-made share over the player's prior
  180-day-weighted possessions. Each teammate feature itself precedes its game.

Do not use current full-season height/position/roster facts as though known in
2004. Static metadata is optional only if its temporal provenance is established.
The required path works without it.

Location conversion initialization: prefix-only league bucket logit plus a
shrunk player shooting offset; this follows the useful location-offset control.
Do not substitute a constant scalar personal FG% across all distances. Refit the
initialization inside each training-history cutoff. Cached final-origin location
coefficients cannot be used for earlier training games.

Player profiles for historical TRAINING rows must also precede those rows. It
is leakage to attach a 2026 snapshot to that player's 2022 outcomes while fitting
the 2026 model. Implement chronological sufficient-statistic updates; do not call
a full-corpus groupby afresh for every possession. Same-day games all use the
same beginning-of-day state, followed by an end-of-day update.

Thin-history and new players get prefix-only population priors, missingness and
low support, not exclusion or an all-zero "bad player". No future debut roster
or future player-type information. Retired states retain their last-observed
date and a staleness label; do not automatically call them prime seasons.

### 2.3 Player state encoder

Define an 18-coordinate anchored state:

- 3 log event rates: FGA, FTA, TO;
- 6 centered location logits;
- 6 location-conditioned make logits;
- FT make logit;
- log assist rate;
- assisted-made logit.

Zero denominators use explicit priors before taking logs. Numerical epsilons
are recorded constants, not tuning knobs. Additional own rebound/support inputs
may feed the encoder without pretending they are already a fitted rebound model.

Let `b_i(t)` be that baseline state and `x_i(t)` its complete historical feature
vector. Learned state:

    h_i(t) = b_i(t) + E_theta(x_i(t))

`E` is a shared two-linear-layer MLP: input -> 32 tanh units -> 18 outputs.
Initialize the final layer to zero. The encoder-off arm is exactly `h=b`.
Use no batch normalization, dropout, per-ID parameters, or recurrent state in v1.
Feature standardization is fitted on training rows only and saved with the fit.

Use a squared state-correction penalty, stronger where the corresponding
historical exposure is thin. Precisely: mean over rows/coordinates of
`delta² * (1 + 200/(200+n_eff_coordinate))`; absent exposure means zero effective
exposure. This is regularization, NOT a posterior variance formula. Save mappings
from coordinates to exposures. Coefficient selection is specified in §5.

### 2.4 Directed teammate messages

For each recipient i and each of the other four players j:

    m_ij = M_phi(concat(h_i, h_j))
    c_i  = mean over j != i of m_ij
    z_i  = h_i + c_i

`M` is a shared MLP: 36 inputs -> 32 tanh units -> 18 outputs. One message pass
only; initialize its final layer to zero. Mask the FT-make coordinate to zero:
the production model does not explain FT skill through teammate presence.

Do not mask repeated identities in synthetic clone tests: exclude the same
SLOT, not every slot with the same player ID. Five identical profiles should
still make a well-defined five-node set.

The encoder sees prior teammate-reference features; messages see the new
composition. This supplies information for distinguishing historical assignment
from new context. It does not mathematically identify the decomposition or
eliminate double counting. Report how much own state and context offset each
other, sensitivity across seeds, and their combined forecast. Do not interpret
raw hidden coordinates or message weights as causal explanations.

Normalize categorical logits to zero mean before logging them. This fixes their
irrelevant common shift. Penalize both encoder corrections and message outputs;
do not let a weakly penalized intercept shift masquerade as capability.

### 2.5 Shared event decoder and finite opportunity allocation

The decoder is the same in every core arm. It has small trainable per-channel
intercepts and positive slopes on the corresponding state coordinates, with
slopes initialized to one. It must not contain a second general-purpose MLP
capable of hiding all interactions in the "no-context" control.

Compute positive unnormalized player FGA, FTA, TO propensities `q_i,k` from
their log-rate coordinates. Allocate a SINGLE team usage-unit budget U:

    Z = sum_i (q_i,FGA + 0.44*q_i,FTA + q_i,TO)
    lambda_i,k = U * q_i,k / Z

Then split each player's FGA across six locations with a softmax, and compute
per-location conversion and FT conversion with sigmoid links. All probabilities
are valid by construction. A six-way mix allows 2-versus-3 share to change;
do not accidentally renormalize 2s and 3s separately while claiming to learn it.

**U is not literally one possession.** It is expected
`FGA + 0.44*FTA + TO` per possession. The 0.44 coefficient is an inherited
accounting approximation, not an exact free-throw-trip likelihood. Multiple
shots, and-ones, technical FTs, and rebounds prevent a categorical interpretation
of these counts. Unit labels must say "usage units", not "probability".

For the four core arms, U is the SAME prefix-estimated league usage budget at
the prediction date, using a 365-day half-life and all eligible prior possessions.
It does not depend on the arm, learned h, actual future lineups, or future points.
Its inadequacy for contextual extra possessions is a disclosed v1 limitation.
This makes the first test about player state and mixing, not a secretly learned
team-volume correction. Do not add predicted ORBs as extra points or opportunities
yet; the explicit feedback experiment is §8.2.

Assisted-made share is an auxiliary head. Predicting it does not observe touches,
potential assists, pass paths, primary ball handling, or whether a MISSED shot
was created for someone. Never manufacture those labels from absence of an
assist tag. Shot-distance buckets called corner threes remain distance proxies,
not measured x/y locations.

### 2.6 Points, without a cancellation or duplicate influence bonus

Native offensive points per 100:

    100 * [sum_i,b value_b * lambda_i,FGA * p_i,b * make_i,b
           + sum_i lambda_i,FTA * ft_make_i]

`value_b` is 2 or 3. This is the expected made-shot accounting identity. Do not
also add league shot-location valuation, an old shooting surplus, teammate
shooting coefficients, or an ORB coefficient. That would double count channels.

Use this single decoder/scorer for evaluations, panels, perturbations, and
explanations. Native points and all components must be saved before calibration.
Use each arm's prior-only affine calibration as a separately printed layer
(§5.5). No free black-box points residual. Do not transplant the old assist
deficit into the primary joint model; compare the old parent as a control.

### 2.7 Learning objective

Train the connected model jointly through the constrained decoder using Adam,
learning rate 0.001, target batch size 4096 grouped lineup rows (keep games
intact for the auxiliary loss below), gradient norm clip 5, float32 training;
metric aggregation/reconciliation in float64. CPU is the reproducible default.
An optional device must pass a small numerical parity check and be recorded.

Use grouped sufficient statistics per `(game, off5)` for core offense-only
training when exactly equivalent to event-wise likelihood; do not average the
player identities, exposures, or targets before aligning slots. This makes a
small full-data experiment practical. For the opponent extension retain def5.

Five head-family losses:

1. FGA/FTA/TO player counts: composite Poisson negative log likelihood with
   rate `n_possessions * lambda_i,k`. Include zero-event players. Count rates
   are not five separate possession probabilities.
2. Six-way location: multinomial cross-entropy on attributed attempts.
3. FG conversion: binomial loss on attempts/makes per player/location.
4. FT conversion: binomial loss on attributed FT attempts/makes.
5. Assisted-made share: binomial loss conditional on attributed made FGs.

**Available-label detail:** `shot_events2` has no per-shot assisted flag; the
existing `game_player_stats` cache has `own_shot_ast` and own FGM at player-game
level. Use that auxiliary label at PLAYER-GAME level only. Aggregate each
player's predicted assisted makes and predicted total makes across his actual
lineup exposures, take their ratio as the predicted conditional assisted share,
and compare with that game's observed assisted-FGM/FGM counts. Count the label
once per player-game. Do not copy the game total into every lineup or treat
unknown individual shots as unassisted. Batch complete games so this aggregation
is exact. Zero observed makes gives zero auxiliary exposure, not a failed shot.
If that player's game coverage cannot be reconciled, mask this auxiliary label
and print the lost exposure. The other four families remain usable.

Divide each family loss by its eligible exposure and by that family's
training-only baseline loss, then average the five families equally. Save those
normalizers; a missing family is missing, not zero loss. This is a composite
predictive objective, not a claim that the event counts are conditionally
independent or that a possession-level joint likelihood was observed.

No points loss in the primary training run. Points are an external check on
whether better mechanisms translate. FT conversion has no teammate message;
the separate unrestricted FT-context negative control is specified below.

Training is end-to-end: gradients from these heads reach both E and M in the
joint arm. Test this explicitly, including allocation-denominator gradients.

## 3. Input and label audit before training

Create a read-only input registry with explicit paths and hashes. Useful existing
sources, to inspect rather than blindly call:

| Source/code | Intended reuse | Trap |
|---|---|---|
| `asof_state.py`, `game_player_stats.pkl` | prior sufficient stats/EB definitions | final-cutoff profiles on earlier labels leak |
| cached `context_*.pkl` | dates, games, exact ten players, point targets | loader can access DB; duration is an outcome |
| cached `shot_events2_*.pkl` | shooter, distance, attempt, make, FT | shooter match failures; no fabricated miss assists |
| cached `possession_channels_*.npz` | slot TO/ORB/DRB/steal, misses | IDs/order must be joined; rebound denominators approximate |
| cached `outcomes_*.pkl` | team event reconciliation | no silent rebuilding via `build()` |
| `asof_points_2026/schedule.csv` | frozen quarter boundaries | quarters are game-count windows, not calendar quarters |
| centered benchmark and unaffected v2 cells | frozen point controls | uncentered additive offensive half is invalid |
| `asof_point_calibration.py` | pure calibration/metric definitions | fit using completed prior windows only |

Do not select a glob's first cache. Resolve configuration/data epoch, inspect
manifest metadata, and require exact joins. Names may come only from existing
saved exports; do not query Postgres merely to render a case.

Required output `input_audit.json` and coverage tables:

- source rows, date ranges, games, unique possession IDs, matching rates;
- shooter/acting-slot match rates by season and channel;
- attributed counts plus unassigned remainder reconcile to team counts;
- FGM <= FGA and FT makes <= attempts; six locations plus unknown reconcile;
- exact definition and eligible denominator for every target;
- rebound counts vs missed-FG counts: report violations, do not silently cap;
- point identity from shots/FTs vs cached possession points, with a distribution
  of discrepancies and a list of categories that cannot be explained;
- distribution of priors/support/missing states, including rookies and retirees.

Missing attribution masks the affected loss only. Retain the possession's other
usable labels and its team target. Unknown FGA location gets an explicit unknown
label/mask and does not become a long two. If unattributed events exceed 2% of
FGA or points overall, or 5% in any season, flag the population problem before
full training and report both full and attributed diagnostics. Do not silently
lower those warning thresholds. A warning does not authorize new data work.

Derived daily states must have an audited causal join, a feature schema, source
fingerprint, and exact recurrence-vs-brute-force tests. Save them under the new
prefix; do not rewrite `PlayerHistory` or existing caches for speed.

## 4. Core comparison arms and identification controls

All four core arms share data, priors, U, decoder family, training objective,
selection rules, calibration, and evaluation populations.

| Arm | Learned own-state correction E | Teammate messages M | Question |
|---|---|---|---|
| H0 historical | off | off | finite-allocation event control |
| H1 learned state | on | off | better player estimates? |
| H2 fixed-state context | off | on | better mixing alone? |
| H3 joint context | on | on | benefit of learning both together? |

"No context" still shares the finite opportunity denominator. It means no
learned teammate response beyond that mechanical competition, not additivity.
The corrected additive remains the actual additive point comparator.

Primary contrasts: H1-H0, H2-H0, H3-H1, H3-H2. For loss, negative is better.
Report the factorial interaction `(H3-H1)-(H2-H0)` as a descriptive measure of
joint-training benefit. H3 is the designated research candidate, not the
best-looking arm chosen after the fact. If H1 wins, say so without relabeling it
as learned complementarity.

Bounded controls on development and pilot origins:

- Frozen-teammate counterfactual: hold own features fixed, change only the other
  four, and recompute through the actual scorer. No teacher-forced actual usage.
- Context shuffle: train an H3 control with teammate message inputs shuffled
  among examples with the same feature cutoff and coarse prior-usage bin
  (training: same game date; validation: same frozen quarter-start cutoff);
  keep the real five for the allocation denominator and own labels. Shuffle
  only within each training/validation partition, using a fixed recorded seed.
  Never give an earlier row a later game's updated player states. Singleton
  strata remain unchanged and their fraction is reported.
  Evaluate the trained control with real context. This is a negative control
  for learning meaningful matching, not an alternative product lineup.
- FT-context diagnostic: fit the same message mechanism to FT conversion in a
  separate diagnostic head, using fixed historical shooter baselines. Compare
  against its no-context head. A surviving effect flags context/confounding;
  a null does not prove FG effects causal. Never add it to the point candidate.
- Shared-output diagnostics: encoder/message correction norms, correlations,
  cancellation, seed stability, and changes after zeroing M without retraining.
  Zeroing M is a diagnostic, not a substitute for the refitted H1 control.

Do not add a dozen new architectures after seeing these results.

## 5. Forward protocol, fitting, and calibration

### 5.1 Time and cohort contract

Use the saved 48 quarter origins, 2015–2026, with identical boundaries and
2016–2026 as the primary 44. Quarters are approximately 300-game league windows,
not four equal calendar intervals. Every fit, normalization, prior, state,
reference population, hyperparameter choice, and calibrator stops before its
prediction cutoff. A window is usable for calibration only after its stop date.

Core outer forecasts freeze the model AND player states at the quarter start.
Aggregate predicted events/points onto future lineup-quarter cells. Do not
silently update states daily during testing and compare against quarter-frozen
archived arms. A daily-update sensitivity is a later named experiment, not v1.

Use all eligible training events, not just future common lineups. Core training
lookback is 5*365 days before the relevant fitting cutoff. Feature histories may
use all earlier data with the prescribed decay. Training examples carry a
730-day time weight common to all five losses and all arms; it is distinct from
role-state recency. Report effective event/game counts.

Intermediate evaluation includes all available future events, including
thin-history players; additionally print the archived common-cell restriction.
Point headline comparisons use EXACTLY the frozen common keys and weights.
Any extra coverage enabled by fallback states is a separate expansion table.

Never filter on a candidate's success, support, actual role change, or error.
If a forecast is nonfinite, that arm has failed the cell; do not quietly create
a smaller "common" comparison. Novel-off5 labels come from strictly prior
observations, not first appearance in the training lookback alone. Also report
novel within the five-year lookback separately if useful.

### 5.2 Development selection, before the main benchmark

Use 2014q3 and 2014q4 as development evaluation windows. Inputs/training for each
still stop before its start. These precede all primary evaluation seasons.
Choose separately for H0/H1/H2/H3 from this THREE-value grid for lambda:
`0.001, 0.01, 0.1`. It multiplies the sum of applicable encoder/message-output
penalties and squared log decoder slopes/intercept deviations. Use fixed
optimizer weight decay `0.0001` for all learned networks. Normalize penalty
blocks by their number of coordinates/parameters so size alone is not decisive.

Selection score is the mean of the five exposure-normalized, baseline-scaled
validation family losses, averaged equally across the two development origins.
For a difference <= 0.0001, prefer the larger lambda. No development point
metric or named case selects lambda. No architecture/width/half-life search.

One permitted grid expansion, determined solely by development loss: when the
best lambda lies at an edge, evaluate the next decade at that edge for that arm
on both development windows. Then stop expansion and disclose any remaining
boundary. This is a bounded research setting, not deployable tuning evidence.
Freeze selected lambdas before the first 2015/primary prediction is inspected.

### 5.3 Optimization inside an origin

Primary seed is 17. For each outer origin, use the most recent completed saved
quarter as an inner early-stopping window. Fit before that window, validate on
it, select an epoch by the same five-family objective, then refit from the same
initial seed on all eligible data before the outer cutoff for that many epochs.
Maximum 12 epochs; early-stopping patience 2; minimum improvement 0.0001.

Validation player states precede the INNER window start and stay frozen, matching
the outer deployment. All inner priors/scales exclude inner validation. During
the final refit, regenerate only the affected training-prefix normalizers;
historical row states retain their own causal dates. Never warm-start from a
later-origin model or carry optimizer state backward in time.

Save epoch curves, gradient norms, selected epoch, fit/validation date ranges,
penalties, parameter count, normalization constants, and final checkpoint.
Unconverged fits are reported as such. Do not call a timeout or zero-gradient
model a scientific null.

### 5.4 Pilot, full run, and seeds

After development selection, run the four arms on 2015q1 and 2015q2 first.
These are genuine warmup-origin forward predictions, not a synthetic smoke.
Produce event and point tables immediately, even if cold-start calibration
makes those numbers unattractive. Target this milestone before building
defense, rebound feedback, or extensive plotting.

Then run the ENTIRE core schedule in chronological order. Do not stop every
quarter for a new conversation. Stop only for a correctness failure, a runtime
bound, missing permission/input, or user interruption—not because the next
result could be unfavorable. Milestone output should say provisional until all
required origins finish.

Seed sensitivity after the full primary-seed run: seeds 29 and 43 on the fixed
four origins 2016q1, 2019q1, 2023q1, 2026q1, all four arms. This checks instability;
it is not an independent sample for significance and cannot establish full-run
ensemble coverage. Do not choose the best seed or average a partial seed cohort
into the primary scoreboard.

Run the context-shuffle and FT diagnostic on these same four origins with seed
17. Those are bounded diagnostics, not a search for favorable seasons.

### 5.5 Point calibration and fair comparisons

For each new arm, save native P in points/100. Define R = P - prefix league
points/100 and fit `actual - league = a + b*R`, b >= 0, using that arm's saved
forecasts from completed PRIOR windows. Reuse the existing cold-start threshold
of 30 cells; below it use a=0,b=1 and disclose the fallback. No fitted deficit
term in these arms. Never calibrate on in-sample fitted training predictions.

Primary displayed prediction is `league + a + b*R`; also publish native metrics
and a,b. Calibration is empirical correction, not a basketball mechanism.
Do NOT use development-window forecasts chosen retrospectively by their winning
lambda as calibration history: that selection has seen development outcomes.
Begin calibration history with the first 2015 forecast after lambda is frozen;
2015q1 therefore cold-starts. Retain the 2015 outcomes for later windows only
after their stop dates. Never include a future window because it happens to
share the season label.

The frozen parent, location+shooting and additive retain their OWN archived
calibration, with verified cutoff metadata. Do not recenter or recalibrate them
on the outer targets to make the levels line up. Print that their native
parameterization differs; the four H arms provide the tightly controlled
architecture comparisons.

### 5.6 Metrics and uncertainty of comparisons

For every origin/arm, print eligibility, exposure, all five head losses, native
and calibrated point MAE/RMSE/r²/bias, and delta to corrected additive and
location+shooting. Add conditional allocation share error, TO/FTA/3PA per-100
count error, location cross-entropy, FG/FT Brier, and reliability-bin tables.

Pooled point MAE/RMSE/r² are possession-weighted. Print raw pooled r² and
within-quarter-centered r² separately: era-level variation can inflate the
former. Do not compare these levels with old single-possession or annual r².

For paired inference, compute each arm contrast within each of the 11 primary
seasons, then report equal-season mean, SEM, 95% t interval, and number of
seasons favorable. Seeds, shots, and overlapping origins are not independent
replicates. Include a paired season-block bootstrap sensitivity (2,000 draws,
fixed seed 20260909); with 11 years its limitations must be explicit.

Report all, novel-off5, exposure bins <100/100–200/200–400/400+, and season/era
slices with denominators. New support bins use prior-only thresholds. Never
turn subgroup discovery into a retrospective primary win.

## 6. Basketball and explanation acceptance suite

### 6.1 One scorer, exact ledgers

The callable must return native/calibrated points, U, player/channel attempts,
mix, conversion, expected makes, player point contributions, and state/context
support. Decoder calculations are shared by training evaluation and inference.
No second formula in a report or notebook.

For any replacement report, decompose the native point difference through a
fixed four-block path: budget -> player opportunity allocation -> shot mix ->
conversion. Sum of block deltas must exactly equal the total. Also run the
reverse path and print attribution sensitivity. Nonlinear decompositions are
path-dependent; neither is a unique causal explanation. Calibration delta is
separate. H0–H3 and additive comparisons accompany the ledger.

Show actual numerical channel changes, not attention weights. An explanation
may say "the model predicts 1.2 additional rim attempts/100" if the ledger does;
it may not invent "gravity" or "better passing lanes" from a hidden coordinate.

### 6.2 Freeze fixtures before model fitting

Create a JSON fixture list, with IDs, player-season/cutoff selection, and expected
mechanism directions, before development training. Reuse existing named fixture
definitions and print full five-player names to make errors visible.

- Jokić/Korver/Westbrook same-three comparison MUST retain Jamal Murray. Use the
  existing other two fixed teammates and record them. Report H3's context effect
  over H1 as well as the structural-vs-additive replacement contrast. The latter
  includes baseline estimation differences and is not pure pair interaction.
  Korver's fitted role/spacing compatibility should be more favorable; do not
  enforce his total lineup ranking or impose a player-specific sign.
- Repeat at 2026q4's true cutoff, 2026-03-02, for continuity. Korver is stale in
  this current-date comparison. Add a separately labeled historical-season
  override; choose the season before reading outputs. Never backfill that
  season's future games into its selected player date.
- Haliburton same-four removal/replacement and Westbrook's changed teammate
  context: inspect assignment, TO, mix, and conversion separately. Use no
  post-injury outcomes to fit a pre-injury forecast. Team wins/finals placement
  are not the lineup model's causal target.
- Steven Adams, Mitchell Robinson, Josh Hart: own-board vs teammate-board vs team
  capture only when §8.2 provides those outputs. Until then mark this mechanism
  unimplemented; do not rename an own ORB rate as facilitation.
- Five limited-creation centers, five small guards, five Gobert clones, and five
  Jokić clones as DISTINCT tests. Five Jokićs are not five non-creators.
- A documented Warriors small-ball five and 2021 Clippers small-ball five, with
  states drawn from their selected seasons. No automatic center-position rule.

Fixtures do not select hyperparameters. A basketball failure remains visible
even if prediction improves. If H3 assigns five limited creators efficient
offense, report that the role/creation mechanism is not yet adequate; §8.1 is the
predefined follow-up, not permission for a post-hoc five-center multiplier.

### 6.3 Structural invariants

Permutation of slots leaves team forecasts unchanged and permutes player
ledgers correspondingly. Same states/different IDs give equal outputs. Missing
states produce disclosed priors, not NaNs. Duplicate synthetic slots work.
Probability sums, count nonnegativity and budget identity hold. Changing make
probability alone affects points by the exact attempts-times-shot-value identity;
relocating shots is not canceled by another making term. Setting E or M to zero
is exactly nested at the forward-function level, with decoder parameters held
fixed. H1 is still separately refitted for scientific comparison.

## 7. Uncertainty: deliver something useful without claiming the impossible

Keep three outputs distinct:

1. **Finite-batch prediction interval:** uncertainty in a future lineup-quarter
   observed offensive rating, including outcome noise.
2. **Model/mean sensitivity:** uncertainty from estimated states/parameters and
   alternative plausible assumptions; initially diagnostic, not calibrated.
3. **Unsupported-role/composition warning:** a quantitative support measure and
   reason, not a gate that refuses to score.

First required audit: rolling empirical absolute-residual intervals at 50/80/95%
for H0, H3 and frozen additive/location+shooting on completed prior cells. Use
the existing repaired/independently verified interval method where possible;
verify radii from saved rows independently. Calibration pools/bins are selected
using prior information only. Report unconditional and exposure/support-binned
coverage, widths, effective calibration size and fallback source. Do not pool
future residuals to print retrospective "rolling" intervals.

Support vector: minimum per-player effective exposure, staleness, distance of
predicted assignment from that player's pre-cutoff assignment distribution,
and distance of the lineup's mean/spread of profiles from prior lineups.
Fit distances/scales on prefix data. Previously, assigned-role distance failed
to order persistent error: do not assume the new distance works without a test.

Fit a nondecreasing residual-scale relationship to support distance on PRIOR
completed cells only, with constant-width fallback if there is no usable history.
Compare against the exposure-only interval. Do not add a tuned widening factor
based on future coverage. Beyond observed support, show the extrapolated interval
and an explicitly labeled assumption-sensitivity range; no empirical arbitrary-
lineup coverage guarantee. A bounded observed-residual quantile cannot, by itself,
validate five-center latent-mean uncertainty.

Seed sensitivity from §5.4 is not a posterior. The bounded stronger extension
is five game-block reweighted refits of H1/H3 at 2026q1 only, sharing the selected
protocol. Sample ONE weight per game for all its rows. Shared player uncertainty
must be shared across every occurrence and synthetic copy of that player;
do not create independent pseudo-players to narrow a clone lineup's error bar.
Report model spread and finite-batch interval separately. Implement only within
the compute budget and label its one-origin scope.

Uncertainty is a co-equal research standard: if the empirical support adjustment
does not work, that is a major unfinished result, not a footnote or a license to
call the model production-ready.

## 8. Controlled extensions after the complete core result

Do not build all extensions before seeing the complete core comparison. Implement
in the order below, with separate protocol sections/output subdirectories and
one changed mechanism at a time. The full architecture can fail gracefully as a
research program without disguising a partial model as a finished product.

### 8.1 Explicit responsibility/efficiency response

Core messages may learn role changes but do not guarantee a penalty when every
player lacks creation. Test a constrained overload response, not a position rule.

Define assigned load as the predicted player's share of team usage units.
Historical reference is his prior share in his actual past lineups, with its
effective exposure and dispersion. It is NOT usage/100 mislabeled as a share.
Standardized positive excess is `max(0, assigned-reference)/max(prior_sd,0.05)`.
The 0.05 floor is fixed and disclosed in share units.

In a new H3-load arm, add `k_TO * excess` to the conditional TO-versus-FGA log
odds and subtract `k_FG * excess` from FG make logits. Both k >= 0 via an explicit
nonnegative parameterization, with zero as an exact boundary; fit these common
two parameters on training events with the same regularization protocol. Keep
allocation from the base H3 forecast fixed for computing excess (one pass), then
renormalize the event budget after the TO adjustment. No unstable circular fixed
point. Freeze the base H3 fit in this first follow-up, and label it a two-parameter
extension, not joint-training evidence.

The sign restriction is an assumption that excess responsibility can be costly,
not proof that the observed proxy is primary creation. Fit against real events;
never tune k to make Gobert's offensive rating cross a chosen number. Report
losses for high-load stars and small-ball units as well as the center fixture.
If k fits zero or the mechanism fails, record it. Do not force a positive value.

Run at the four fixed diagnostic origins first. If it gives at least one
measured basketball improvement with no numerical failure, run all 48 (subject
to budget) even if channel accuracy is slightly worse, so the trade is known.
Otherwise stop this extension with its factual diagnosis. No automatic promotion.

### 8.2 Rebound competition and the opportunity budget

Separate two questions: who captures a rebound, and how a team gains additional
opportunities. Existing own ORB rates and miss denominators are insufficient to
silently claim a fully observed renewal process.

First implement a conditional MISS-OPPORTUNITY head only where source accounting
can reconcile the eligible opportunities. It predicts offensive-team capture,
defensive-team capture, and other/unresolved outcome; conditional player shares
within each team sum to that team's probability. All ten players compete for
one opportunity. The network may improve TEAM capture without giving the named
player all the extra boards. This is the Adams/Robinson distinction to test.

If the existing cache does not distinguish live missed-FT, dead-ball/team rebound
and missed-FG opportunities sufficiently to reconcile those classes, do not
manufacture labels or cap observed counts. Complete a descriptive denominator
audit and mark the physical capture model blocked on new source derivation.
Such data work is outside this plan. Core work continues.

If labels reconcile, fit shared logistic team-capture and softmax within-team
share heads from dated states, with strongly pooled coefficients. Compare own-
rate normalized competition, learned team capture, and learned team+player
allocation. Evaluate conditional log loss/calibration and team/individual counts
separately on the four fixed diagnostic origins before a 48-origin run.

For the budget experiment, first define the observable residual accounting
quantity `B = FGA + 0.44*FTA + TO - ORB` per possession. Publish its era and
lineup dispersion and exceptions; it is an approximate accounting base, not
exactly one possession. A controlled mean-feedback arm uses prefix-only E[B]
and predicted ORB to set U = E[B] + E[ORB]. Solve any U-dependent miss/capture
feedback analytically when linear, otherwise by a documented contraction with
a convergence check. Print denominator/dynamic stability and uncertainty.

Do not use a hidden clip when the implied feedback has no finite stable
solution. Diagnose it and leave the existing U path intact. Do not add both
extra attempts from ORBs and an ORB point bonus. First compare the rebound-only
head with unchanged U to isolate estimation, then enable budget feedback. No
claim of a literal possession simulator follows from the 0.44 approximation.

An exact live-ball/FT-trip renewal simulator is a later architecture milestone
requiring an event-sequence audit. It is explicitly NOT a v1 deliverable.

### 8.3 Actual opponents and two-lineup inference

Build a typed opposing-five context path, distinct from teammate messages, after
the core offense result. Reuse existing dated defensive own/allowed event
features only when their provenance is audited. No inferred defender positions,
assignments, contests or tracking coordinates from box-score proxies.

Opponent experiment arms:

- O0: fixed H3 offense, league-average opponent placeholder;
- O1: O0 plus the saved corrected additive defensive estimate with its explicit
  offensive-rating reference/sign, using the existing opponent-control code;
- O2: same player states with additive pooled opponent-feature effects in event
  logits (no offense-dependent receiver);
- O3: O2 plus directed offense-recipient/opponent-sender messages, one pass with
  the same small architecture as teammate messages.

O2 and O3 refit their event heads on identical training data; same priors,
opportunity budget and losses. O3-O2 isolates matchup-dependent response from
generic opponent strength. O1 is an essential strong conventional control, not
an obsolete baseline. Do not confuse its ORtg adjustment with a full net rating.

Evaluate per-possession predictions against actual opposing fives, then average
by the same offensive lineup-quarter cells. Retain the raw point target. A
separate neutralized-target sensitivity applies the SAME correction to every
arm/target and is clearly labeled; never compare raw and neutralized r² as one
leaderboard. Using actual future opponents estimates performance conditional on
the schedule faced, not an unconditional pre-season schedule forecast.

Research inference API:

    predict_matchup(team_a_states, team_b_states_or_reference, environment)

Return A offense vs B and B offense vs A, and margin = their difference at equal
possessions. Swapping A/B negates margin exactly. League-average opponent means
averaging over a saved prefix-only representative lineup distribution; nonlinear
models generally cannot replace that with five average vectors. Sample 128
reference fives with fixed seed and record weights; use the SAME reference
distribution across comparisons. Publish Monte Carlo sensitivity on a bounded
case panel. The placeholder represents a team distribution, not a fictitious
five-shooter average player.

A two-lineup interface alone is not proof of learned defensive assignments.
First run four diagnostic origins, then the full 48 if stable and within budget.
Even a null O3 is useful: the product can retain O1/O2 as its defensive component.

## 9. Tests: prioritize scientific failure modes, not test count

Required before the two-origin pilot:

1. Future mutation: changing/appending later games cannot change prior features,
   fit, selection, calibration, support bins, or predictions at the audited
   cutoff. Separately mutate inner-validation future data.
2. End-of-day update and strict cutoff; no train/validation game overlap; shuffled
   input rows and numeric IDs preserve joins/results.
3. Hand-counted five-player/two-game labels: zero-event players, unmatched
   shooter, multiple shots, and-one, missing location, assisted MADE only.
4. Brute-force-vs-incremental histories, correct decay/effective exposures,
   prefix-only priors, rookie fallback, and stale state selection.
5. Permutation/identity/clone invariance and exact E/M zero nesting.
6. Finite probability/count/budget identities and nonzero gradients through
   encoder, messages and the shared allocation denominator.
7. Tiny synthetic additive generator: context should not systematically improve
   truly independent held-out data. Synthetic complementarity generator:
   H3 can learn a known event-level interaction with adequate controlled signal.
   Judge predictions, not recovery of nonidentified latent coordinates.
8. Save/load equality and grouped-vs-event-wise loss equality on a small fixture.

Required before full result acceptance:

- Independent metric recomputation from saved predictions, including within-
  quarter r², seasonal pairing, all common keys and novelty labels.
- Same score through batch, single-lineup, and panel entry points; native and
  calibrated ledgers reconcile <=1e-8 pts/100 in float64 reference arithmetic.
  Float32 training parity may use a separately documented looser tolerance;
  do not weaken exact accounting assertions because the network is approximate.
- Calibration cutoff sentinel and all-input-fingerprint resume tests.
- An interrupted origin resumes without duplicating calibration history or
  treating an incomplete checkpoint as a completed forecast.
- Location perturbation, conversion perturbation and count perturbation match
  their intended point effects; no scalar-making cancellation.
- Every completion status is derived from expected artifacts/origins, not merely
  process exit code. Reports generated from data, no hardcoded winner prose.
- Full repository test suite after integration; compare with the starting suite
  and preserve unrelated failures instead of silently rewriting old tests.

Extension tests: overload zero nesting and role-unit audit; rebound conservation
including unresolved classes and feedback instability; opponent reference/sign
and swap antisymmetry; shared uncertainty draws for clones; prior-only interval
calibration and correct exposure/support-bin fallback reporting.

Keep synthetics small. Passing 100 new unit tests is not a substitute for the
two-origin data milestone or the complete forward experiment.

## 10. Implementation layout and interface contract

Prefer new modules rather than changing hash-pinned scientific code:

- `experiments/joint_capability_data.py`: explicit read-only inputs, label joins,
  chronological states, grouping, coverage and fingerprints.
- `experiments/joint_capability_model.py`: E/M/decoder/losses and pure inference.
- `experiments/joint_capability_fit.py`: training, development selection and
  strictly nested early stopping/refit.
- `experiments/joint_capability_run.py`: resumable schedule, frozen controls,
  predictions, calibration, metrics and live logging.
- `experiments/joint_capability_diagnostics.py`: basketball ledgers, negative
  controls, support, intervals and disagreement review.
- `tests/test_joint_capability_*.py`: focused tests above.

Keep small helpers together where that reduces duplication; this list is not a
request for a framework. Extension modules may be separate after the core is
measured. Do not refactor the entire existing experiment stack.

Implement and verify these CLI interfaces (they DO NOT exist yet):

    python -u -m experiments.joint_capability_run preflight --run-dir <prefix>
    python -u -m experiments.joint_capability_run develop --run-dir <prefix>
    python -u -m experiments.joint_capability_run core --run-dir <prefix> --resume
    python -u -m experiments.joint_capability_run diagnostics --run-dir <prefix>
    python -u -m experiments.joint_capability_run extensions --run-dir <prefix> --resume
    python -u -m experiments.joint_capability_run report --run-dir <prefix>

Support `--max-seconds` and `--max-origins` as operational pause controls; they
must not change scientific fingerprints or silently change fitting samples.
`report` must be read-only with respect to fits/predictions and must not train.
Provide a `--dry-run` schedule/cost summary. Preflight must not train a model.

Default new prefix: `experiments/cache/joint_capability_2026_09_09_v1/` if
absent, otherwise select a new explicit version. Required output structure:

    manifest.json                 # sources, code/protocol, environment, state
    protocol.json                 # resolved constants/fixtures; frozen before fit
    input_audit.json
    coverage.csv
    derived/                      # new versioned labels/states only
    development/                  # every candidate, not just winner
    origins/<tag>/<arm>/           # checkpoint, curves, predictions, complete marker
    diagnostics/                  # cases, placebo, seeds, support, intervals
    extensions/                   # separate extension manifests/results
    reports/                      # generated tables, derived only from saved outputs
    logs/                         # append-only logs / PID metadata

Hash all imported scientific helpers as well as new files and input artifacts.
Record git HEAD plus dirty-file hashes; HEAD alone does not identify this tree.
Include protocol, feature schema, split boundaries, model configuration, seeds,
dependency versions and optimizer settings. Scientific identity differs from
operational wall-time limits. Refuse incompatible resume. Save atomically and
never overwrite a completed origin. Reuse matching completed work by manifest,
not by guessing from a filename.

Log every completed origin/arm, including this information (values are examples
of FORMAT, not results):

    origin=... arm=H3 fit_end=... test=[...,...) cells=... poss=...
    event_loss=... FG_Brier=... mix_CE=... TO_MAE100=...
    MAE=... additive=... delta=... location_shot=... delta=...
    RMSE=... r2_raw=... r2_within_quarter=... bias=... novel_MAE=...
    epoch=... lambda=... seed=... elapsed=... calibration_fallback=...

Every few origins print the cumulative common-population table and completion
count. Explain MAE versus RMSE/r² disagreements rather than selecting one.

## 11. Execution priorities, compute bounds, and decisions

### 11.1 Priority order

1. Read-only prerequisites and artifact preservation; freeze fixtures/protocol.
2. Causal data builder plus smallest E/M/decoder and critical tests.
3. Development selection and TWO REAL warmup origins, including point tables.
4. Complete core 48-origin comparison; do not detour into extensions.
5. Basketball panel, high-exposure disagreements, finite-batch interval audit,
   seed/placebo diagnostics; write a core result checkpoint.
6. Responsibility response, conditional rebound audit/head, opponent experiment,
   and stronger uncertainty, in that order subject to data/compute gates.
7. Integrate report and handoff. No scorer promotion.

Have useful quantitative output before completing all optional diagnostics.
Keep user updates about results and next decisions, not a running test-count
celebration. If training is long, give Adam a verified background command and
`tail -f` command; do not burn usage polling a healthy process.

### 11.2 Bounded work, not an unlimited sweep

Default authorized experiment budget on implementation: 12 aggregate wall-clock
hours of numerical fitting, 10 GiB peak resident memory target, no more than
600 optimizer-fit invocations across development/core/diagnostics/extensions,
and the 12-epoch maximum above. Track consumption in the manifest. These are
ceilings, not targets or runtime promises. Feature preparation gets a separate
2-hour bound; if exceeded, checkpoint its progress and diagnose complexity.

Count inner fits and final refits individually. After the first real origin,
project remaining runtime and disk/memory use and report it. If the full core
would exceed the bound, pause before starting an unfinishable sweep and provide
the exact resume command and measured estimate; do not shrink the historical
cohort, tune fewer arms opportunistically, or call two origins a final result.
Adam may authorize a longer background run. Do not leave healthy work repeatedly
restarting after one-origin timeouts. Operational resumes must reuse completed
work and carry a truthful status.

Extensions are lower priority than finishing core inference and reporting. If
the remaining budget cannot cover their specified comparisons, mark them
deferred with estimated cost and exact prerequisites. No open-ended architecture,
random-seed, width, embedding, half-life or learning-rate sweeps.

### 11.3 Interpretation rules

- H1 improves and H3 does not: evidence for better player estimation, not
  complementarity. Keep the useful estimator and report the contextual null.
- Channels improve but points do not: inspect allocation vs team-total effects,
  conversion calibration and budget limitations. Do not multiply channel effects
  by a favorable retrospective point coefficient.
- Points improve but basketball fails: not an acceptable finished product.
- Basketball improves with modest accuracy loss: a legitimate candidate trade;
  print magnitude/uncertainty and ask Adam for a product judgment, no automatic
  r²-only rejection.
- Support does not explain persistent error: no validated role-based OOD claim.
- Point accuracy is similar and explanations are shorter/more faithful: that
  architectural simplification is valuable, but not a statistical accuracy win.
- No meaningful improvement on any pillar: stop this architecture version with
  a diagnosis, not another unregistered net. A bounded negative result is done.

No numeric promotion gate is invented here. The only automatic gates are data
integrity, numerical validity, scope, and budget. Scientifically informative
negative core predictions are still completed and reported.

## 12. Final deliverables and restart handoff

Write `reports/joint_capability_2026_09_09.md` (or matching versioned report)
from saved outputs. Include:

1. What was built, parameter counts, exact learned/fixed components, and a small
   diagram of history -> player state -> context -> events -> points.
2. Full common-population scorecard, all H contrasts, frozen controls, seasonal
   uncertainty, novel results, native/calibrated metrics, and coverage expansion.
3. Channel and allocation results with units and denominators. Separate
   player redistribution from changed team production.
4. Actual named five-player cases, states/dates, additive player contributions
   where available, and exact new-model point/event ledgers.
5. High-exposure failure review: top 10 cases where H3 loses most to additive,
   and top 10 where H3 loses to H1, at >=200 possessions and >=5 games. Show
   actual ORtg, predictions, all five players, coefficients/ledgers, and two
   chronological descriptive halves. Rank by weighted squared-error difference;
   add the MAE difference. This is selected-case diagnosis, not a significance
   test. If fewer qualify, print all and the shortfall, do not change thresholds.
6. Negative controls, seed stability, identifiability/cancellation diagnostics.
7. Interval coverage/width by exposure and support, model sensitivity, and the
   remaining unsupported uncertainty claims.
8. Extension results or explicit deferred/blocked statuses and prerequisites.
9. Reproducible commands, runtimes, source/run hashes, tests, and known defects.
10. One recommended next decision, with what evidence would reverse it.

Append a clearly labeled research entry to `MODEL_SCORECARD.md` and
`MODEL_RESEARCH_ROADMAP.md`; do not erase the earlier review corrections.
Prepend `SESSION_HANDOFF.md` with exact code/run status, completed origins,
remaining obligations, active PID/log if any, immutable artifact locations,
changed-file summary, and the FIRST command/action on restart. Say who has
editing ownership. A long-running job and an incomplete model are never hidden
behind "all tests passed" or "implementation complete."

### Suggested request Adam can give Sol

> Read `JOINT_CAPABILITY_MODEL_PLAN.md` and implement its staged research build,
> including the bounded experiments and new derived outputs. Prioritize the
> complete four-arm quarterly experiment and quantitative comparisons, then
> follow the extension gates and compute bounds. Preserve all original artifacts
> and existing work. Do not delegate, scrape, access/change the database, rebuild
> input caches, promote a scorer, or deploy. Keep me updated with actual results
> and finish with the documented handoff. If the run needs more time than the
> bound, give me the measured estimate and exact background/resume command.

## References and design provenance

Repository sources are the primary evidence for what has/has not worked here:
`CONTEXTUAL_MODEL.md`, `ROLE_MODEL.md`, `STRUCTURAL_MODEL.md`,
`RESEARCH_OVERVIEW.md`, `CREATION_EXPERIMENT.md`, `REBOUND_EXPERIMENT.md`,
`SOL_INFLUENCE_REPAIR_FOLLOWUP.md`, and the manifests cited above. Historical
claims in them are qualified by the latest review, not automatically accepted.

Architecture background, not evidence of an NBA accuracy gain:
[Interaction Networks](https://arxiv.org/abs/1612.00222) and
[Set Transformer](https://proceedings.mlr.press/v97/lee19d.html).
Uncertainty caution:
[Can You Trust Your Model's Uncertainty?](https://arxiv.org/abs/1906.02530).
V1 intentionally uses a much smaller message-passing model and stronger explicit
accounting than an unrestricted attention-to-points architecture.
