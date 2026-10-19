# v16 — adjusted capabilities, joint matchups, and a better possession model

Design v1, 2026-09-18. Adam requested a comprehensive, ambitious next experiment
after the completed v15 review. The v15 implementation and review are committed
as **e438a4a**. Codex implements directly; no delegation.

**This document is an implementation/experiment plan, not an implemented runner
or permission to start training in this planning turn.** The next implementation
should finish the prescribed preparation and pilots, then provide verified
background commands and a measured resource estimate. Production launch awaits
Adam's request. Preserve every old artifact and frozen producer.

## 1. The bet

Learn transferable player capabilities after adjusting for the people around
them; let both sides adapt together; give those capabilities a structured way
to interact, compete for actions, and create second chances.

This campaign has **22 new neural designs**, plus archived controls and cheap
non-neural controls. Every design has a named question and comparator. We also
build an actual persistent-error uncertainty experiment, rather than treating
three-seed spread as an answer to hypothetical-lineup uncertainty.

The three standards in `CONTEXTUAL_MODEL.md` §2 have equal standing:

1. Forward point and event prediction, including novel and thin-support units.
2. Basketball-coherent counterfactuals and faithful explanations.
3. Honest uncertainty about unfamiliar lineups, separately from game noise.

A modest prediction tradeoff can be worthwhile for clear gains in the other
standards. No known-pair chemistry, player-ID embeddings in the NN, forced
named-player rankings, synthetic score targets, or coverage gate. Estimating
regularized per-player inputs does not authorize identity lookup tables in the
downstream contextual model.

### What v15 and earlier versions established

- Opponent information helps. On the historical primary, old HALF+D RMSE is
  10.73215, versus opponent-blind old HALF 10.78462.
- MAIN_RB half reaches 10.72573, but its incremental difference is only
  −.00642 [−.04077,+.02369], with 4/11 season RMSE wins. About 94% of its small
  MSE advantage is quarter-level bias reduction; common prior-affine calibration
  reverses the ranking. Calibration must be controlled prospectively.
- Cross interactions and defensive recovery improve their event families in
  all 11 seasons. Event signal exists; it has not become a decisive point win.
- The defensive inputs remain confounded on-floor descriptors. V5's scalar
  opponent-profile correction did not test the proposed multidimensional,
  teammate-and-opponent-adjusted representation.
- Offense was frozen in v15. Joint adaptation has not been tested in that rig.
- V13 already tested offensive profile attention (`J_ATTN` and
  `J_ATTN_SUPPLY_LOAD`). Do not call attention wholly new. This proposal tests
  **two-sided attention with actual defenders and adjusted capabilities**.
- Cleveland's action-allocation error is not fixed by removing creation/load
  constraints. Too much FT/TO usage displaces field-goal attempts; missing
  renewal contributes too. A universal FT subtraction is unsupported.
- First-chance and post-rebound offense need not have the same shot process.
- The historical 5,607-cell primary excludes some units through an inherited
  old-profile support intersection. Keep it for continuity, not as the only
  population. Existing inputs support 8,345 offensive fives with >=50 future
  possessions and 718,526 game×off5×def5 rows in the 44 primary quarters.
- Persistent residuals exist, but neither those residuals nor finite-game
  interval coverage identify arbitrary-lineup latent uncertainty automatically.

Sources: `reports/joint_capability_v15_codex_review.md`, the v15 companion review,
`reports/joint_capability_v13_codex_review.md`,
`reports/game_situation_diagnostic_review.md`, and roadmap R16.

## 2. Scope, stages, and immutability

### Stage A — foundation and feature library

Replay controls; make calibration and population policy common; audit opponent
integration; fit strictly historical adjusted capabilities into a **new** derived
library; derive qualified phase labels from the existing ordered-event archive.
No scraper or new external data is needed. Read-only local artifacts are the
default because this is a fixed-data experiment, not because the database is
expensive. No database mutation, old-cache rebuild, or silent data-epoch change.

### Stage B — models, tests, and launch acceptance

Implement all 22 designs in a common runner, the variance experiment, independent
auditor, durable reporting, and exact resume. Complete finite synthetic tests
and the specified pilots. Freeze a machine-readable manifest before pilot
forecasts are inspected: arm definitions, features, labels, cutoffs, losses,
calibration, stopping, comparisons, and data/code hashes.

### Stage C — one complete campaign

After launch approval, run every declared arm and seed over all 48 origins.
No elimination of poorly scoring arms or adjustment of a model after seeing
outer results. Produce controls and matched cumulative comparisons as it runs.
All analyses and handoff run automatically after fits, without a second launch.

### Stage D — independent review and three-pillar decision

Read actual saved predictions and fitted states, not just the runner's summary.
Report failures as well as wins. No automatic scorer promotion or deployment.

The plan's feasibility checks can reveal missing labels, infeasible computation,
or an invalid nesting assumption. Record any necessary design amendment **before
meaningful pilot results**, with reason and version. After freeze, a substantive
design change requires a new protocol/prefix. Operational fixes must preserve
old producers and prove prediction parity where reuse is claimed.

## 3. Dates, targets, populations, and honest comparison

### Temporal contract

- Same 48 registered quarter origins: 2015q1–2026q4; 2015 is warmup and
  2016–2026 supplies 44 primary quarters. Reuse the saved schedule exactly.
- Inner validation is the last completed quarter before the outer origin.
  Inner training and all its fitted state stop before that validation begins.
- Fresh final optimization uses the final prefix and the selected inner length.
  No outer outcome informs profiles, scaling, losses, stopping, calibration,
  uncertainty fitting, or reference selection.
- NN training retains the five-year window and 730-day observation half-life.
  Keep complete games together in batches and all statistical resampling.
- Historical training rows receive features available **before their own date**.
  Fitting a coefficient bank on the final prefix and assigning those coefficients
  to its earlier training rows is prohibited target leakage.
- Evaluation inputs are frozen at the quarter origin. Live within-quarter state
  updates are a future, separately matched estimand, not mixed into this run.

### Two co-primary point populations

1. `legacy_primary`: the exact 5,607 cells / 726,364 possessions, for continuity.
2. `broad_off5_ge50`: every offensive five with >=50 possessions in that quarter,
   currently 8,345 cells / 1,013,999 possessions. No profile-coverage filter.

Evaluate the **same rows for all models**. A zero-history player receives a
prior and disclosed support, not exclusion. The 50-possession requirement is
an outcome-aggregation screen for this metric, not a product eligibility rule.

Also always report all matchup rows, offensive fives below 50 possessions,
defensive fives >=50, exact ten-player units >=50, and game-level summaries.
Keep low-count rows in point/event totals. Never average quarter r² values to
obtain pooled r². All-row noise is not evidence of poor larger-sample forecasts.

Novel/recurring offense, defense, and ten-player units are different labels.
Report zero-history players, minimum-player support, adjustment-estimation
support, composition distance, role displacement, and stale-player bins. Freeze
bin cutoffs using the training prefix, never current outcomes.

### Two different product/evaluation tasks

- **Known-opponent conditional:** score actual opponents at actual exposure
  weights. This is the primary accuracy task, including A+D controls.
- **Prior-average opponent:** integrate over a dated prior reference, for the
  one-lineup product. Replay this mode on observed offensive cells too, but
  separately: it intentionally lacks the realized opponent schedule.

Do not compare a conditional challenger with an unconditional control and call
the difference synergy. Score both directions with one shared scoring function;
margin(A,B) = offense(A,B) − offense(B,A). Add a real **team-game offensive-rate
and margin** table using team orientation from the existing possession context.
The old `groupby(game_id)` metric averages both teams and is not a margin test.
Realized lineups/minutes make even that margin task conditional, not a forecast
of future rotations or a simulation of a particular coach.

## 4. Common controls and point calibration

Preserve the original v15 table unchanged in an archive view. In the v16 view:

- Include A, A+D, N, N+D, old HALF, old HALF+D, and all four v15 direct/half
  controls. N remains v14 RB_RENEW_FAC, not a newly chosen backbone.
- Reuse saved control group predictions and prior-centered D only after exact
  identity/date/exposure/hash checks. Reconstruct broad and margin populations
  from group predictions; do not fill their scores from the legacy table.
- Fit the **same additional** expanding, prior-completed-window affine point
  calibration to each starting forecast: `league + a + b*(p0 − league)`, b>=0,
  cold-start identity below 30 eligible prior cells. Use the broad >=50 cohort
  as the one calibration population for every contender, including controls.
- For a new NN, p0 is its native event-accounted point output; do not first
  fit another candidate-specific v15 calibration. Archived controls retain
  their archived starting forecast and receive the same new calibration.
  Print that inherited distinction and native/raw sensitivity, not a claim of
  identical historical training/calibration paths.
- The registered secondary forecast for each new NN is exactly 50% calibrated
  A+D plus 50% calibrated NN. No internal additive output is hidden in the NN.
- Print each constituent, affine slope/intercept, and contribution separately.
  Do not calibrate the new half again in the primary comparison.

The experiment compares usable forecasts under a common new procedure; it
cannot retroactively make their entire training history identical. Calibration
must be applied to each origin with only earlier completed outcomes. Recompute
old HALF+D's common-calibration history independently as a strong comparator.

Include two deterministic non-NN readouts of the new regularized channel fits:
`ADJUSTED_CHANNEL` and its calibrated 50% A+D blend. Predict focal-player events
against the specified other nine, enforce the same normalized action budget
and stationary rebound renewal, then price makes at 2/3/1 points. Do not add
the coefficient effects again as separate point bonuses. Compare its native
event/point outputs to the nonlinear combination; good inputs alone may suffice.
Use each channel's **complete offensive-bank GLM**, including that fit's
defender coefficients and intercept. Do not splice own coefficients from one
decay/fit with defender coefficients from another and call it that fitted GLM.
Use dated own FT% for the unmodeled FT-conversion channel. Raw GLM count totals
determine action proportions before normalization; renewal then supplies total
opportunities, so fitted all-event volume is not multiplied by renewal twice.

## 5. Adjusted capabilities: what we actually estimate

### 5.1 Actor/other-four/opponent likelihoods

Fit L2-regularized models to game×off5×def5 sufficient statistics. Each offensive
player becomes the focal actor in turn; distinguish their production from
effects on the other four. Every fit conditions on all ten identities, with
separate **actor**, **teammate influence**, and **defensive** coefficient blocks.

For an actor i and event c, the generic linear predictor is:

`eta_i,c = dated_league_c + intercept_c + own_i,c
           + sum(other_four influence_j,c) + sum(five defense_k,c)`.

| Target | Likelihood and exposure | Interpretation |
| --- | --- | --- |
| Actor FGA, FTA, TO | Three Poisson counts; log possession exposure offset | Own action tendencies and associates' shifts to those tendencies |
| Actor shot location | Six-category multinomial; located FGA exposure | Conditional shot mix, not directly observed shot quality |
| Makes by location | Binomial within each of six locations | Conditional conversion, still mixing skill and unobserved difficulty |
| Eligible FG recovery | Six-way softmax: five offensive collectors versus defense | Collector ability, other-four facilitation, defensive recovery |

For recovery, each collector's log-odds against the defensive class contains
its own coefficient, the other four facilitation coefficients and the five
defensive coefficients. The denominator is eligible live rebounds, not all
possessions; the five collector probabilities sum to team ORB probability.
Retain the observed negative sign convention for good defensive recovery or
transform it explicitly into a positive recovery-strength input.

No contextual FT-conversion coefficient. Dated own FT% stays an own-skill input.
An optional FT-conversion placebo is diagnostic only and can never enter scores.

These are conditional associations stabilized by shrinkage. They are not causal
fractions of credit, measured openness, or proof that Adams causes a specific
number of teammate boards. Persistent teammate/coach confounding may survive.

### 5.2 Anchoring, pooling, and fit controls

- Use dated league offsets generated before each observation date. Include an
  unpenalized residual intercept and enforce exposure-weighted zero-mean
  constraints separately on own, teammate, and defender blocks using only the
  fitting prefix. Enforce the multinomial class gauge as well.
- Constrain the parameterization during fitting; arbitrary post-fit centering
  is not a remedy for penalty-dependent gauges. The corresponding intercept
  transformation must preserve every fitted prediction. Test invariance to
  equivalent coefficient shifts and reconstruct per-side standalone scores.
- Fit the offensive bank at matching raw-feature timescales: 180-day decay for
  action/mix/recovery, 730-day decay for conversion. Fit the defensive bank at
  365-day decay, matching v15 defensive descriptors. Each bank still controls
  both sides; this requires separate weighted fits where decay differs.
- Five-year fit window. Prior mean of coefficients is zero. Export support and
  posterior-style curvature uncertainty as well as coefficients. New players
  have neutral coefficients with prior uncertainty, not perfectly known zero.
- Objective convention is summed decayed NLL plus `lambda/2 * ||beta||²` in
  canonical coordinates. Candidate lambdas: 10, 100, 1,000, 10,000. Shared
  lambda within each bank/family, not an outer-result-tuned value per player.
- Select penalties at each season's first origin using the last completed
  quarter available then; candidate fits stop before that quarter. Choose the
  strongest penalty within one paired game-bootstrap SE of the best validation
  NLL (200 fixed-seed resamples). Freeze that choice for the season. Before a
  usable validation quarter exists, use lambda=1,000 and label the cold start.
- No expanding grid campaign. Print boundary selections and coefficient/prediction
  sensitivity. A serious numerical failure blocks the library; an inconvenient
  predictive result does not authorize changing this rule.
- Warm starts may reuse only an earlier-cutoff coefficient solution. Stopping
  uses convex-objective convergence, not NN outer accuracy: relative objective
  improvement <1e-8 and projected gradient infinity norm <1e-5, cap 500 solver
  iterations. Report nonconvergence; do not silently accept an optimizer code.

### 5.3 Strictly dated library

Generate snapshots on calendar month starts plus every registered inner/outer
origin needed by the run. Historical rows use the most recent available
snapshot at or before the row date, with all fit observations strictly earlier
than the snapshot. Same-date games cannot leak through an update. Snapshots
start early enough to cover the five-year NN prefixes, not just 2015 onward.

Every snapshot records its data cutoff, latest observation, penalty-selection
cutoff, feature schema, centering reference, support, convergence and hashes.
Outer profiles use the exact origin snapshot. The month cadence is a declared
approximation, not an assertion that adjusted states update every game.
Produce matched-timescale **unadjusted** monthly summaries as a diagnostic
reference so cadence/decay effects are not automatically called deconfounding.

Export own and teammate coefficients separately (15 event coordinates plus
recovery each) and 16 defensive coordinates, with feature ordering explicit.
Inputs include log effective opportunity counts, staleness, and curvature
uncertainty summaries. Negative coefficients are valid link-scale features,
not negative probabilities. Normalizers are fitted on each NN training prefix.

For selected covariance queries and 32 fixed-seed joint parameter draws, retain
correlation across players/blocks from the constrained penalized Hessian via
factorization/linear solves. Never independently jitter each player or each
appearance of a cloned player. Label these draws as an approximate working
posterior conditional on the GLM, not empirically validated causal uncertainty.
This preserves covariance **within a fitted bank/family**; separate fits do not
identify cross-family or cross-timescale covariance. Report conditional
bank-at-a-time sensitivities rather than pretending their independent draws
form a calibrated joint distribution over every player attribute.

**Reuse audit:** old `onfloor_influence.py` is a source of design/solver ideas,
not a ready-made skill bank: its coefficients are residuals to an older
structural model. Do not import them as standalone abilities.

## 6. The 22 neural designs

Common starting point: the origin/seed-matched **v14** RB_RENEW_FAC checkpoint
plus a zero-initialized MAIN_RB defense head. Inner initialization uses the saved
inner parent; final uses the saved final parent. Verify dates and receipts.
Never start an inner fit from an outer/final checkpoint. Every final optimization
has fresh optimizer/RNG state; it does not continue the selected inner fit.

`J` means the supported offensive event/recovery parameters and defense are
jointly trained. Own FT-conversion and assisted-fraction/supply outputs without
new direct supervision remain on their frozen parent paths; no opponent or
teammate may directly change FT%. For the nested augmentation designs, prove
that initial event predictions agree with the correct parent, including role
and renewal. The representation-removal exception below is disclosed explicitly.

Adjusted features enter new zero-initialized residual input paths; shared
weights/initialization stay matched. They must be usable by own and other-four
heads, not only by a final point residual. All designs retain current creation/
load constraints and explicit recovery accounting unless a change is named.
RAW/OFF/DEF/BOTH use the same complete input schema and module topology: reserve
the adjusted-feature slots in every variant and zero disabled banks before
their learned projections. Center an adjustment path as `g(z)-g(0)` so a
disabled all-zero bank cannot become a new free intercept. Record nominal and
active parameter counts. Do not give BOTH a different hidden width or an extra
unmatched raw-profile head and attribute that change to the estimated profiles.

| # | Arm | Difference and question | Main comparator |
| ---: | --- | --- | --- |
| 1 | J_RAW | Jointly train the existing raw-profile offense and MAIN_RB defense. Does co-adaptation beat frozen offense? | Archived D_MAIN_RB |
| 2 | J_DEF | Add adjusted defensive capabilities only. | J_RAW |
| 3 | J_OFF | Add adjusted own-production and teammate-influence capabilities only. | J_RAW |
| 4 | J_BOTH | Add both banks; the central capability hypothesis. | J_RAW, J_DEF, J_OFF |
| 5 | F_DEF | Same added defensive bank as J_DEF, but freeze offense exactly as in v15. | Archived D_MAIN_RB; J_DEF |
| 6 | J_ADJ_CONTEXT | Use adjusted features instead of raw on-floor context descriptors in learned teammate/defender messaging; keep own raw decoder anchors and support. | J_BOTH |
| 7 | J_RAW_CROSS | Add the v15 rank-8 attacker-dependent defensive response under joint training. | J_RAW |
| 8 | J_BOTH_CROSS | Same cross-response with both adjusted banks. | J_BOTH; J_RAW_CROSS |
| 9 | J_POINT_RAW | Add a small native team-point objective to the raw joint model. | J_RAW |
| 10 | J_POINT_BOTH | Same point objective with both adjusted banks. | J_BOTH |
| 11 | J_ATTN_RAW | Two-sided set attention over raw capabilities, with the event decoder retained. | J_RAW_CROSS; J_WIDE_RAW |
| 12 | J_ATTN_BOTH | Same attention with adjusted capabilities. | J_BOTH_CROSS; J_WIDE_BOTH |
| 13 | J_WIDE_RAW | Parameter-matched pooled MLP control for raw attention. | J_RAW; J_ATTN_RAW |
| 14 | J_WIDE_BOTH | Same capacity control with adjusted inputs. | J_BOTH; J_ATTN_BOTH |
| 15 | J_ACTION_RAW | Hierarchical team-action/player allocation with workload-dependent type substitution. | J_RAW |
| 16 | J_ACTION_BOTH | Same allocator with adjusted own and facilitation inputs. | J_BOTH; J_ACTION_RAW |
| 17 | J_PHASE_TIED_RAW | Add phase supervision but tie initial and renewal event processes. | J_RAW |
| 18 | J_PHASE_TIED_BOTH | Same tied-phase supervision with adjusted inputs. | J_BOTH |
| 19 | J_PHASE_RAW | Allow distinct initial and post-eligible-ORB processes. | J_PHASE_TIED_RAW |
| 20 | J_PHASE_BOTH | Same two-phase process with adjusted capabilities. | J_PHASE_TIED_BOTH |
| 21 | J_ALL_RAW | Predeclared integration of attention, action allocation and two-phase renewal on raw inputs. | Raw component arms |
| 22 | J_ALL_BOTH | Same integration with both adjusted banks: the moonshot. | J_ALL_RAW; adjusted component arms |

J_ADJ_CONTEXT is deliberately **not** a fully adjusted-only player model; own
event-rate anchors, style and available role history remain. Do not claim its
result settles complete replacement. Mask raw other-four/historical-teammate
context from its learned sender paths and raw defender descriptors from its
defense path; own-only receiver features may remain. Removing a pretrained
path changes its initial function, so this arm is not a zero-residual nesting
test: record the initial prediction change and test that removed inputs have
zero influence. J_ALL is fixed now, not assembled from
the observed winners. Comparisons of a combined arm against individual
components are package comparisons, not every conditional marginal effect.

### 6.1 Attention and capacity controls

Use two typed sets of five players, separate offense/defense input projections,
width 32, four heads, two residual attention blocks and width-64 feed-forward
layers. No positional encoding or order-dependent player slots. Retain
leave-one-out teammate structure; opponent attention sees all five defenders.
Use a zero-initialized output residual into the same 15 event channels and
recovery strength, with FT-conversion excluded. Score the reversed matchup
through the same function, not a second separately learned margin network.

This is a small set-attention module, not a language-model-sized transformer.
Attention weights are learned routing, not observed defensive assignments or
causal explanation weights. The event ledger remains the explanation source.

WIDE arms replace this extra interaction module with pooled mean/SD networks.
Choose their integer hidden width by parameter count alone, within 10% of the
corresponding attention module, and freeze it before pilots. They get identical
features, objectives and data. No accuracy-based width selection.

The architectural rationale is set-equivariant interaction learning, as in
[Set Transformer](https://proceedings.mlr.press/v97/lee19d.html); pooled-set
controls follow the general invariance principle of
[Deep Sets](https://papers.nips.cc/paper/2017/hash/f22e4747da1aa27e363d86d40ff442fe-Abstract.html).
Neither paper establishes an NBA performance gain for this proposed design.

### 6.2 Action allocation: which actions give way?

Replace the single joint normalization of all player/event rates with an
explicit two-level allocation, initially identical to that normalization:

1. Derive initial team action mass from sums of unnormalized FGA, .44×FTA,
   and TO rates; normalize its three entries by softmax in log space.
2. Allocate each action's mass across players using its own normalized actor
   rates. Convert FT usage back to FTA by dividing by .44.
3. Learn bounded residuals to team-type logits and actor-within-type logits
   from own ability, other-four context, defenders, and relative load. The
   current matched profile variant supplies the inputs.

Use one width-32 tanh layer per team/actor residual, zero output initialization,
and ±1 logit residual bounds. This preserves nesting and the opportunity ledger.
Do not implement an unbounded free team-rating correction. Scarce creators can
cause attempts/FTA/TO to change differently; there is no prescribed Cleveland
or Westbrook adjustment. Keep the existing supply/load response, and report
before/after-allocation usage, shortage, conversion and renewal separately.

### 6.3 Two-phase renewal: a rebound need not restart the same offense

The current stationary loop repeats the same event mix after an ORB. The new
decoder has phase 0 (initial opportunity) and phase 1 (after an eligible FG
offensive recovery). A zero-initialized width-32 phase residual changes action
logits, location, conversion and recovery; FT% remains own-only. At zero phase
residual the two processes coincide and must reproduce stationary renewal.

Let B be the frozen non-rebound usage budget, q0 and q1 the event vectors per
unit usage in the two phases, and r0/r1 their eligible-miss×ORB continuation
probabilities. Then:

`renewed_usage = B*r0/(1-r1)`

`total_events = B*q0 + renewed_usage*q1`

`total_usage = B + renewed_usage = B + expected_eligible_ORBs`.

Price the expected makes, not a separate ORB bonus. For identical phases this
reduces to the existing `B/(1-r)` loop. Both r values must be valid probabilities
strictly below 1; use stable arithmetic and fail on nontermination instead of
silently applying a point/ORB cap. This retains the existing .44 bookkeeping
convention; it is not an exact simulator of all FT sequences.

The existing v14 phase arrays are **not sufficient training labels by themselves**:
they are coarse off5 diagnostics with unresolved substitution/other-ORB cases.
Derive new actor- and opponent-aligned phase events from the frozen ordered
event archive, preserving all exclusions and original files. Record phase entry
exposure, repeated recoveries, collector and shot location. Ambiguous ordering,
floor changes and other-ORB pathways get explicit masks, never guessed states.
Every unambiguous phase count must reconcile to the corresponding original
aggregate; unresolved events remain in aggregate point/event training.

Phase models add `.25 * normalized_phase_NLL` to the common objective. Conditional
phase supervision uses observed phase-entry opportunities only for training
and diagnostic likelihood, not for the unconditional scoring call. TIED arms
get the same labels, masks, weight and phase loss but require q1=q0/r1=r0. Thus
PHASE versus TIED isolates phase flexibility, not simply extra supervision.
Define phase NLL as the mean of the same four family losses on the qualified
phase observations, each normalized against the shared stationary parent on
that training prefix; sum numerators/exposures across phases before division.
Counts use their qualified phase-entry exposure, location/conversion their
attempt exposure, and recovery its live-miss exposure. Save every denominator.
Aggregate plus phase supervision intentionally reuses some labeled events;
the .25 weight is explicit, not an unnoticed duplication of the main objective.
ALL arms use the same phase objective and no point auxiliary. If phase entry
exposures cannot be established from saved data, this block is explicitly
blocked before model pilots; do not pretend the old diagnostic counts suffice.

## 7. Objective, stopping, and checkpoint robustness

All arms share v15's four-family aggregate event objective: action Poisson,
shot-location categorical, conversion binomial, and six-way rebound NLL.
Normalize each family by the same zero-adapter parent loss on the same weighted
training prefix; compute that reference once per origin/phase/seed, not once
per changed architecture. Do not silently change masks or weight a row twice
because it is now split by defender or phase.

POINT arms additionally use `.25 * native_point_MSE / prefix_point_MSE_ref`.
Pool predictions back to game×off5 before this auxiliary, use all point rows,
and weight by possessions. This avoids turning sparse matchup-group noise into
a different arbitrary loss weight. The reference is common and prefix-only;
outer additive outputs do not become a fitted target. This is a new test under
opponent conditioning, not a claim that earlier v10/v13 point-loss results did
not happen. Report the event/point tradeoff explicitly.

Default training: Adam lr .001, weight decay .0001, gradient clipping 5,
complete-game batches targeting 4,096 matchup rows. Shared/new residual modules
use matched seeds (17,23,41) and deterministic shuffles. No automatic LR sweep,
architecture search, or data-dependent early arm elimination.

**Epochs:** cap 96, patience 8, meaningful improvement threshold 1e-5, actual
minimum validation-objective epoch selected. This keeps the established rule
for the primary comparison; the cap is a compute ceiling, not a claim that
96 epochs are optimal. Each final fit gets the selected number of optimization
epochs, starting from its own correctly dated parent initialization. Different
objectives legitimately select different lengths; disclose them.

Also produce a prespecified **late-checkpoint prediction average**, using the
last min(5, selected_epoch) checkpoints of that same final trajectory. It needs
no extra optimization and is secondary, not selected from outer results. Average
complete expected event/point ledgers, not independent probabilities that break
accounting. Preserve primary checkpoint predictions. Report both validation
plateau widths and seed/epoch sensitivity; never claim averaging is guaranteed
to improve performance. For these averages, redo prior calibration from that
forecaster's own historical averages rather than borrowing primary coefficients.

Cap hits and a still-falling validation curve are flagged; do not extend only
losing or interesting arms. A cap-extension campaign, if justified later, must
be a new registered comparison. The main runner completes its fixed schedule.

## 8. Average-opponent integration and faithful explanations

Before fitting new models, audit integration with saved v15 checkpoints at
2016q4, 2021q4, 2025q4 and 2026q4 on the existing fixed panel. This is an
outcome-free numerical integration check, not tuning to actual ratings.

Use the same dated prior-defensive-five distribution and exposure weights for
all models and both lineups in a substitution comparison. Evaluate nested
samples at 128,256,512,1,024,2,048,4,096: map base-two radical-inverse quantiles
through the weighted CDF, taking prefixes of one sequence. Use eight fixed
modulo-one shifts for an integration-error estimate. Compare to exact
weighted summation on the finite reference where computationally practical.
For production fixtures use 4,096 (or exact summation if smaller); mark >.10
pts/100 integration discrepancy as unresolved and expand to exact summation
for that reported fixture. Do not hide it in statistical error bars.

To bound the separate broad average-opponent accuracy task, run the prespecified
model set archived D_MAIN_RB, J_BOTH and J_ALL_BOTH (plus their halves and
unconditional additive controls). Use the same fixed 512-reference approximation,
with a saved 4,096-reference sensitivity on an outcome-independent sample of
20 cells per origin. All 22 designs still get the full fixed fixture panel;
the conditional primary scorecard still includes every design. If that
approximation is inadequate, label the broad average-mode result approximate;
do not change the conditional primary task or select model-specific samples.

Retain conditional per-player attempts/makes/FTs/TOs/boards and final affine
calibration as separate accounting contributions. For a swap, use common
reference draws and common coefficient draws. Mechanism-switch ablations are
model interventions, not real-world causal attribution; print interaction/order
dependence instead of forcing all changes into independent additive bonuses.

## 9. Uncertainty experiment — persistent error versus game noise

This is a required deliverable, not an optional end-of-run paragraph. Run it
for the fixed model set old HALF+D, J_BOTH half and J_ALL_BOTH half. These are
chosen now, not the three observed accuracy winners. Do not feed fitted
lineup-ID effects back into the mean forecast.

### U0: existing finite-outcome bands

Rebuild strictly prior residual intervals for every new forecast, with exposure
bins and support reporting. These remain useful controls, not latent-quality
confidence intervals.

### U1/U2: an explicit persistent-discrepancy model

Use only earlier completed out-of-sample windows. Within each offensive
five/quarter with at least 8 games and 100 possessions, deterministically split
games into two disjoint balanced-date halves, at least 4 games each. Compute
actual-minus-forecast errors against the **actual opponents in each half**.
Estimate each half's finite-game noise with 200 game-block bootstrap resamples,
pooled/shrunk using earlier windows where thin. Never use two pieces of the same
game as independent observations.

Fit the joint working model:

`[e1,e2] ~ Normal([b,b], [[tau²+s1², tau²], [tau², tau²+s2²]])`.

Here s is finite-game noise; tau is persistent residual discrepancy shared
between halves, not automatically causal lineup-quality uncertainty. Include a
common intercept b fitted only from prior windows; retain its estimated bias
separately, without silently correcting the mean model. U1 uses constant tau;
U2 uses log tau² linear in log minimum player support, role/composition/opponent
distance, prior coefficient-variance projection, and three-seed disagreement.
Standardize using prior windows. Add L2 regularization to slopes; choose from
{.1,1,10} on the last completed calibration quarter, with all earlier data for
fit and the smallest model/tie rule recorded. No current residuals in its fit.

Evaluate the joint log score, finite-batch coverage/width and interval score,
split-error covariance, and transfer across recurring/novel/support bins.
Report the identification assumption: a stable within-quarter discrepancy
shared by halves and conditionally independent sampling noise. Role drift,
deployment, selection and correlated games may violate it. Check residual
covariance against time separation and opponent changes; compare alternative
odd/even-date and first/second-half splits as labeled sensitivity, not competing
forecasters chosen after the fact.

With fewer than 30 eligible prior pairs spanning two seasons, U1/U2 are explicitly
`NOT_IDENTIFIED`; retain U0 predictions/intervals and show why the additional
quantity is not available. This is not a gate on scoring a lineup. For synthetic
lineups, show the extrapolation assumptions and profile-support limitations.
Do not describe intervals from this working model as validated true-mean coverage
just because finite-game coverage or clone monotonicity looks reasonable.

Use the joint GLM draws to measure capability-estimation sensitivity and swap
covariance. Keep this, seed variation, integration error, finite-game noise and
persistent discrepancy separately named. Do **not** add them all in quadrature
without a model of their dependence; that can double count the same estimation
error. Deep-ensemble variance is a diagnostic, not a posterior certificate; the
[original ensemble paper](https://papers.nips.cc/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html)
motivates testing predictive uncertainty but does not validate this NBA setting.

## 10. Basketball acceptance and case library

Freeze player IDs, dates, support and mechanism hypotheses before pilots:

- Existing Jokić/Korver/Westbrook comparison, with Murray in the common lineup.
  Judge complementarity residual and mechanism differences, not a forced total
  winner. Adam has explicitly said the initial hypothesis can be disproved.
- Haliburton creator removal and the archived McConnell alternative; use a dated
  healthy-player state where appropriate, not an inferred injury recovery.
- Adams, Robinson and Hart: separate team capture, own collector shares and
  teammate capture. No name-specific coefficient/bonus or mandatory ranking.
- Five-Gobert clones and the legal limited-creation center unit; add a fixed
  legal pure-center unit if the existing unit is not actually five pure centers.
  Distinguish legal-composition failures from repeated-player stress tests.
- Five small guards, the real Clippers and Warriors small-ball fixtures.
- Archived Cleveland and Denver repeated-error units; all qualifying transfer
  benchmark cells, not just the success stories or the largest errors.
- Deterministic low-support/debut/stale-player examples, and substitutions
  against multiple fixed defenses. One player's uncertain state is shared
  across every occurrence, including clone diagnostics.

Display native offense, defense, margin, additive expectation, residual,
FGA/FTA/TO, location, conditional conversion, ORB capture/collector, renewal
and uncertainty for every model. Include factual cohort channel tests as well
as synthetic stress tests. No arbitrary center-rating cap. A poor center mean
is not repaired by saying the interval is wide or the opponent scores more.

Keep a three-pillar assessment matrix for every design, not one scalar utility
score that hides tradeoffs. All examples are repeatedly examined research
cases, not untouched confirmation data.

## 11. Statistical readout and decision rules

- Primary reporting is matched three-seed means; retain every seed. All point
  tables include RMSE, MAE, raw r², weighted correlation and signed bias.
- Report within-quarter centered association/error as diagnostics, not forecasts
  corrected with current-quarter means. Print the level-versus-within-quarter
  decomposition that mattered in v15.
- Use 10,000 season-block resamples for paired metric differences, season win
  counts, leave-one-season-out sensitivity, and per-quarter tables. Twelve
  nominal calendar blocks or 44 quarters are not 44 independent experiments.
- Main architecture contrasts are the named table comparators, fixed before
  results. Report nominal and Holm-adjusted season tests separately by outcome
  family and co-primary population, with the actual family size. Do not apply
  correction only to favorable comparisons or quietly choose MAE over RMSE.
- The key profile contrast is J_BOTH−J_RAW, with J_DEF/J_OFF exposing the source.
  The key joint-training contrasts are J_RAW−archived MAIN_RB and J_DEF−F_DEF.
  ATTENTION−WIDE distinguishes routing from parameter count; PHASE−TIED
  distinguishes phase flexibility from its extra supervision.
- ALL_BOTH−ALL_RAW asks whether adjusted capabilities help the integrated
  design. ALL versus individual components is exploratory package interpretation.
- All novel/debut/transfer cohorts and both broad/legacy populations are reported
  even if results disagree. Existing transfer definitions stay frozen.
- Historical years have already informed development repeatedly. Strict dates
  prevent within-run leakage; they do not turn another historical search into
  fresh confirmation. Future acquired games are the eventual prospective test.

Keep a mechanism when it materially improves supported channel prediction or
coherence without hiding a point cost. Call a predictive gain established only
to the extent paired uncertainty and multiplicity support it. Counterfactual
plausibility alone never establishes causal player effects. No automatic
promotion threshold and no requirement to force a winner out of 22 designs.

## 12. Implementation map and acceptance tests

Create new v16 modules; do not edit frozen v13–v15 producers. Suggested split:

| Component | Responsibility |
| --- | --- |
| `joint_capability_v16_profiles.py` | Canonical regularized likelihoods, cutoffs, penalties, joint uncertainty |
| `joint_capability_v16_inputs.py` | Snapshot lookup, raw/adjusted masks, normalizers and qualified phase labels |
| `joint_capability_v16_model.py` | Arm registry, joint model, attention, allocation and phase decoder |
| `joint_capability_v16_fit.py` | Shared objectives, prefix-safe initialization, stopping and checkpoint averages |
| `joint_capability_v16_controls.py` | Verified reuse, expanded cohorts, common calibration and non-NN readout |
| `joint_capability_v16_uncertainty.py` | U0/U1/U2 and separated sensitivity sources |
| `joint_capability_v16_report.py` | Live matched scorecards, channel/coherence/statistical outputs |
| `joint_capability_v16_run.py` | Frozen manifest, resumable lifecycle, background logs/status |
| `audit_joint_capability_v16.py` | Independent saved-artifact and numerical reconciliation |
| `run_joint_capability_v16.sh` | Thin launcher; Python environment and threads explicit |

Reuse existing numerical primitives where their estimands match. Avoid a general
framework rewrite. No test-count target; cover the consequential failures:

1. Future and same-date poison outcomes cannot change earlier features, selected
   penalties, normalizers, predictions, calibration, or uncertainty parameters.
2. Deliberate gauge shifts preserve reconstructions; canonical coefficients stay
   anchored as penalties change. Aliased players stay uncertain, not separated
   by fabricated information. Unknown IDs never index another player's state.
3. Matchup, actor, phase and original ledgers reconcile on named masks. No
   point-row loss, duplicate opponent correction, or ORB double counting.
4. Zero adjusted/attention/allocation/phase heads give their declared parent
   except the explicitly nonnested J_ADJ_CONTEXT removal arm;
   tied phase gives stationary renewal. All probability and budget constraints
   hold. Gradients reach only the intended frozen/trainable modules.
5. Both-team permutations, swapped-margin antisymmetry, FT-conversion invariance,
   stronger recovery competition, clone shared uncertainty, and extreme finite
   outputs are tested. Unsupported extrapolation may fail plausibility even if
   it is numerically finite; report both.
6. Common calibration on a toy sequence excludes the scored window; pool metrics
   correctly; empty slices print `NO_ROWS`, never misleading zeros or warnings.
7. Interrupt/resume a synthetic epoch, a profile snapshot and post-fit analysis;
   resumed results reproduce uninterrupted results and reject corrupt receipts.
8. Capability covariance draws preserve linear constraints and shared-player
   dependence. U1/U2 recover known components on simulated data and disclose
   failures when the assumed independence/stability is deliberately violated.

## 13. Bounded pilots, runtime, and one-command execution

Before any long run: synthetic checks, profile fit/replay at an early and late
cutoff, actor-label reconciliation, integration convergence, broad-control
reproduction, and an all-arm one-epoch smoke. Then **44 full-stopping pilot
cases**: every arm at 2016q1 and 2026q4, seed17. Two extra seed23 repeats of
J_RAW/J_BOTH at those origins (4 cases) check initialization/resume bookkeeping.
These are operational pilots, not a tournament or a model-selection round.
Do not tune to isolated-pilot calibrated scores with incomplete prior history.

Full schedule: 22 × 3 × 48 = **3,168 arm/origin/seed cases**, each with inner
and reset-final optimization, plus shared profile fits and derived U analyses.
This is intentionally large. At v15's per-case cost alone it would be roughly
75 hours; joint backpropagation, attention, profiles and integration change that
cost materially. Expect a multi-day run, possibly longer than a week; do not
promise a precise duration until representative pilots are timed. The machine
had about 190 GiB free during planning, not unlimited storage.

Measure median/worst pilot training and inference times and projected storage
by family. Share immutable input/feature libraries across arms/seeds; do not
duplicate group labels or retain gradients for the entire dataset. Chunk
reference integration and projected-covariance queries. Cache parent outputs
only when that parent is frozen; joint models must recompute their forward pass.
Save resume state, selected checkpoints and the last-five candidates with a
documented retention policy inside new runs. Never delete old artifacts to make
room. If estimates exceed available disk/RAM, resolve that before launch;
do not shrink the data or seed count silently.

Default to one training process, no concurrent editing and no opportunistic GPU
migration. A different device needs tested numerical/determinism acceptance and
its own manifest. No parallel agents. Arm/origin jobs are independently
resumable, but all arms must have matching completed origins for live contrasts.

The implemented CLI must provide `prepare`, `smoke`, `pilot`, `preflight`,
`run`, `status`, `report`, `analyze`, and `audit`. Production `run` must execute
fits, all registered secondary forecasts, uncertainty, fixtures, reports and
independent-audit scheduling without requiring another manual training launch.
Completed immutable inputs/pilots are reused only when fingerprints match;
whether isolated pilot fits are reusable must be demonstrated, not assumed.

Durable logs from the start: launcher, preparation, profile solver, epoch,
per-origin, analysis and audit. Each origin prints direct and half comparisons
against A+D, N+D, old HALF+D, MAIN_RB and its own named comparator; include
RMSE/MAE/r²/correlation/bias, exposure, all/novel/recurring, event losses and
matched cumulative metrics. Warmup is labeled, failed cases remain visible,
and a partial run never compares its cells against a full-run control total.

Required read-only leaderboard options: `--sort rmse|mae|r2|corr|bias`,
`--slice all|novel|recurring|thin|debut`, `--population`, and `--view
direct|half|checkpoint_average`. Bias sorting is by absolute bias but prints
the signed value. Include additive controls as ordinary visible rows.

Give Adam verified launch, live-log, status and leaderboard commands only after
those commands exist and preflight succeeds. Put `echo "Launcher PID: $!"` on
its own line after a background command; no enclosing quotation marks. This
planning document intentionally supplies no pretend-runnable v16 command.

## 14. Required outputs and final handoff

New-prefix artifacts include:

- Frozen design/arm manifest, source/feature schema hashes, all cutoff and reuse
  receipts, process state and completion matrix.
- Profile snapshots, validation choices, convergence traces, support/gauge
  audits, covariance-query/draw receipts and raw-vs-adjusted channel scores.
- Per-case native/calibrated predictions and event ledger, per-game and
  off5/def5/ten-player cells, primary and last-five forecasts, selected epochs,
  family losses, params/gradients and profile sensitivity.
- Matched broad/legacy scorecards, per-origin/season/seed tables, paired and
  multiplicity results, bias decomposition, transfer/debut/support readouts.
- Fixed basketball panels, action/phase/rebound accounting, common-reference
  substitution explanations and integration-convergence reports.
- U0/U1/U2 fitting and validation, covariance/split diagnostics, interval scores,
  independent noise/persistent/seed/profile/integration uncertainty labels.
- A readable review with a three-pillar row for every design, rejected and
  unresolved ideas included; exact count of completed/failed/blocked cases.

Finish by updating `MODEL_SCORECARD.md`, `MODEL_RESEARCH_ROADMAP.md`, the top of
`CLAUDE.md` and `SESSION_HANDOFF.md`. State what's running, what is complete,
what is not identified, where logs live, and the next decision. No silent
transition from research winner to production scorer. Commit only when asked.

## 15. Explicitly deferred, not forgotten

- New tracking, matchup-assignment truth, box-out feeds or scraping; use current
  reproducible data first. A source-access study is a different task.
- Live within-quarter feature refresh/eighth-season evaluation: do it later on
  matched periods, not mixed into quarterly model comparisons.
- Learned game-situation inputs/nuisance branches: preserve the current average-
  environment product and repeat shared clock/margin diagnostics after fitting.
  Do not treat residualized counts as coherent generative targets. A joint
  nuisance model would need its own identifiability/reference experiment.
- Learned player-ID/pair embeddings, arbitrary synthetic labels, bespoke center
  penalties, coaching identity lookup and a giant general transformer.
- Replacing every raw own-skill anchor with adjusted coefficients. This run
  tests augmentation and adjusted-only messaging; full replacement can follow
  if supported. No more frozen-profile swaps into a NN that cannot adapt.
- Claiming true synthetic-mean coverage. This run builds and challenges a
  persistent-discrepancy model; its assumptions remain part of the result.

The ambitious outcome is not merely a slightly higher r². It is a model whose
player descriptions transport better, whose matchup mechanisms predict real
events, and whose explanations and uncertainty survive scrutiny. A complete
negative result in one branch is useful if these comparisons tell us why.
