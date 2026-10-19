# V20 — deployment-adjusted capabilities and stable forecast selection

Detailed proposed protocol, **2026-10-04**. Planning is authorized; implementation,
new derived profile fits, production training, storage cleanup and promotion are
not launched or implicitly authorized by this document. Freeze this plan and its
implementation manifest before production. Resolve feasibility amendments before
looking at new outer results, preserving the original text and evidence.

V19 completion checkpoint: **8e8b325f**. Read [AGENTS](../../AGENTS.md),
[product contract](CONTEXTUAL_MODEL.md) §1–2, [v19 review](../../reports/joint_capability_v19_review.md)
and [roadmap](../../MODEL_RESEARCH_ROADMAP.md). Direct implementation; no delegation.

## 1. Decision and hypotheses

Keep the useful profile-based NN, adjusted actor/teammate/defender effects,
physical event accounting and actual opponent inputs. Do not add another broad
architecture search. The central question is whether historical deployment
context is being credited to players upstream, before the NN sees its inputs.

V19 found C_FULL conditional event gains in all four families and all11seasons,
but worse reference forecasts than J_POINT_BOTH. Checkpoint averaging recovered
much of the difference. Transfer/coherence did not improve; center-heavy FTA
projections worsened. These motivate three distinct hypotheses:

- **H_profile:** estimating player effects jointly with shared clock effects
  improves usable capability inputs, especially under changed deployment.
- **H_stability:** selecting the forecast we actually average is more stable than
  choosing the smallest single-epoch validation loss and averaging afterward.
- **H_transport:** unfamiliar predicted roles and historical clock deployment
  contain information about persistent error beyond a constant discrepancy.

None is assumed true. A conditional event gain is not a common-environment point
gain; a small point cost can be acceptable for a material coherence/uncertainty
gain. All three standards get explicit hypotheses, measurements and conclusions.

## 2. Frozen information contracts and non-goals

1. Preserve the48-origin2015–2026 schedule, seeds17/23/41 and2015warmup. Primary:
   44quarters2016–2026,8,345off5-quarter cells/1,013,999possessions, >=50 per cell.
   Aggregate actual opponent matchup forecasts to these same offensive cells.
2. Preserve original native targets, masks, row keys, game/off5 point pooling,
   five-year NN window,730-day NN decay, event normalization and point weight.25.
   Inner validation is the last completed quarter; final fit uses only the prefix
   before the outer quarter and trains for the inner-selected number of epochs.
3. Product prediction integrates expected ledgers over a common past-only game
   environment. Actual future clock/score is available only in separately labeled
   conditional diagnostics. No clock/score inputs are added to the fan-facing UI.
4. Use the completed immutable v16 matchup/phase inputs and v19 state labels;
   derive a **new** profile library. No rebuilding/replacing the source caches,
   scraping or database mutation. Read-only DB access is unnecessary for this plan.
5. No known-pair chemistry, player-ID embeddings, new attention/width/phase arms,
   margin-profile adjustment, decay/grid sweep, free-throw-trip relabeling,
   scorer promotion, deployment or forced basketball ranking.
6. Raw own-player states, raw teammate/defender descriptors, FT%/assist proxies,
   physical priors and parent initialization stay unchanged. Only the adjusted
   GLM bank changes. This is **not** complete purification of every input. A null
   result cannot close raw-profile adjustment or unobserved-context research.
7. Repeated historical seasons remain development evidence. No new prospective
   confirmation claim; do not imply retrospective transfer cohorts are fresh tests.

## 3. Experiment matrix: eight cells, six new neural arms

Use names below consistently in protocol, logs and reports. P means the current
single-epoch selection policy; S means the five-checkpoint selection policy.
Every comparison uses its own prior-only calibration and the same view.

| Arm | Adjusted GLM inputs | NN context branch | Selection | Execution |
| --- | --- | --- | --- | --- |
| P_BASE | Original v16 | None | Current P | Reuse J_POINT_BOTH |
| P_CONTEXT | Original v16 | V19 FULL clock | Current P | Reuse C_FULL |
| P_ADJ | New clock-adjusted | None | Current P | New fit |
| P_BOTH | New clock-adjusted | V19 FULL clock | Current P | New fit |
| S_BASE | Original v16 | None | S5 | New fit |
| S_CONTEXT | Original v16 | V19 FULL clock | S5 | New fit |
| S_ADJ | New clock-adjusted | None | S5 | New fit |
| S_BOTH | New clock-adjusted | V19 FULL clock | S5 | New fit |

Six ×48×3 = **864 new case slots /1,728 inner-final fits**, less exact compatible
pilots reused. The two historical control cells contribute288 reused cases.
They must not be needlessly retrained. Reuse original teacher/parent artifacts,
not a newly selected v19 winner. Retained C_FIXED/C_CLOCK, R_ALLOC/O_ORDER,
additive, additive_defense and parent_half_defense remain descriptive controls.

**Primary view is checkpoint-average-half for every cell**: equal-weight last
min(5,T) complete-ledger forecasts, own prior affine calibration, then50/50 with
additive_defense. This choice is motivated by inspected v19 evidence and is
declared now, not selected after v20. Show the historical reference's .162989
r² beside its usual direct-half .162915. Keep direct, half, checkpoint_average,
checkpoint_average_half and native readouts; do not silently rename one view.

No training-axis result may change this roster during production. If runtime
requires a reduced design, discuss and publish an explicit amendment first.

## 4. Upstream model: jointly estimate player and clock effects

### 4.1 Preserve the existing capability meaning

Current implementation: `joint_capability_v16_profiles.py`, `_inputs.py`,
`_library.py`, `_features.py`. It fits eight chains: offense/defense decay banks
×counts/location/conversion/recovery, with own, other-four and five-defender
effects. Offense uses own+teammate blocks; defense uses the defender block.
There are16 coordinates and97/49 adjusted input features including support,
coefficient uncertainty and staleness. Keep this interface and interpretation.

For actor i in historical matchup g and clock state s, fit:

    eta[g,i,s,k] = dated_league_offset[g,k] + intercept[k]
                   + own[i,k] + sum(other_four effects[k])
                   + sum(five defender effects[k]) + clock[s,k]

Counts use Poisson FGA/FTA/TO links and original observation masks; location uses
six-class multinomial; FG conversion uses six binomials; recovery uses five
offensive collectors plus the original defensive-capture reference category.
FT conversion is **not** a new adjusted channel in this experiment.

The common recovery clock shift changes offensive-versus-defensive recovery,
not relative rankings among offensive collectors. Location retains its class
zero-sum gauge. Count channels remain distinct, not forced into a softmax.

Clock is the existing31-state encoding: period1–4/overtime crossed with six
remaining-time bins, plus unknown. Collapse margin out of existing v19 labels
with exact sums. No shot clock, intentional-foul label, score margin or new data.
Unknown clock and structurally unobserved states have zero nuisance effects.

### 4.2 Identifiability, penalty and covariance

- Preserve the exposure-weighted orthonormal player-block gauges and canonical
  Euclidean ridge, with an unpenalized intercept. Do not omit an arbitrary player
  or recenter an unconstrained penalized fit afterward.
- Represent active clock effects in their own orthonormal, exposure-weighted
  zero-mean basis, using bank/family decayed opportunities. For location also
  enforce zero-sum over classes. Centering is a parameterization convention,
  **not** causal identification under deployment confounding.
- Fix clock ridge **lambda_clock=1000** in summed-NLL units on the canonical
  clock table; do not borrow the nonlinear NN head's .001 penalty. The existing
  player ridge grid is10/100/1000/10000. This is one fixed extra regularizer,
  deliberately not a two-dimensional hyperparameter sweep. Report shrinkage,
  fitted magnitudes, support and boundary sensitivity.
- Fit players and clock together with the appropriate exact gradient/Hessian.
  A league-only first-stage residual subtraction is not an equivalent substitute
  when clock and player deployment are correlated. No subtraction of negative
  pseudo-counts or use of final-window nuisance effects in historical features.
- Keep current solver convergence criteria: projected gradient <1e-5,
  relative objective change <1e-8,500total nonlinear iterations. Version any
  augmented solver; never silently widen tolerances or call ftol convergence.
- Preserve32joint curvature draws per bank/family/snapshot. The player marginal
  covariance must include uncertainty in clock coefficients: use the full joint
  Hessian or its algebraically equivalent Schur complement. Holding clock fixed
  while drawing players understates this source of uncertainty. Retain original
  linear-solve residual checks; no diagonal jitter fallback.
- Draws are joint **within a bank/family**, not a joint posterior across all
  families/banks. Repeated players/clones reuse the same state/draw. Preserve
  zero-history prior means/variances and identity-sharing, not future roster data.

### 4.3 Dates, tuning and feature export

Use the same254required snapshot dates as the original library, monthly plus
exact inner/outer cutoffs, and identical five-year history/decays: offense counts,
location/recovery180days; offense conversion730days; defense365days.

At snapshot d, every label and context exposure is dated strictly before d.
League offsets for historical rows remain emitted before that row's own date.
Annual player-penalty selection uses the same prior-completed-quarter scheme,
paired200game-bootstrap one-SE preference for strongest eligible shrinkage and
cold lambda1000. Fit candidates before the validation quarter, freeze their
parameters/league offset through that quarter, evaluate actual-clock likelihood,
then select for later snapshots. Export reference-integrated audit losses too;
do not select the penalty from the outer quarter or from a reference leaderboard.

Annual tuning now evaluates a different conditional model and may select a
different player ridge. The main contrast tests the **whole adjusted estimator**,
not clock coefficients at a magically fixed optimal penalty. At the two profile
pilot dates, additionally fit the new nuisance model with the old strictly dated
chosen player penalty and report coefficient/prediction differences. This is a
bounded diagnostic, not another production arm or revised penalty choice.

Historical NN row at date t uses its latest required snapshot <=t, itself fitted
strictly <snapshot. Inner/outer evaluation freezes features at that origin.
An outer-cutoff bank must never backfill all five years of NN training rows.
Recompute only adjusted-feature normalizers separately inside each NN prefix.
Raw normalizers, parent model, loss reference scales and all other inputs remain
identical. Joint profiles are deterministic and shared across NN seeds.

Export player coefficients, marginal SDs, opportunity support, staleness and
gauge receipts in the existing dimensions. Also save nuisance coefficients,
state exposures and optimization diagnostics, but do **not** append them as new
NN feature dimensions. The decoder FULL table is fitted independently at its
own prefix; never add the profile nuisance table a second time at prediction.
The new player coefficients are log-link contributions relative to their gauge,
not counterfactual points or universally context-free ratings.

### 4.4 Efficient construction and zero-context parity

Reuse mapped labels read-only. Cache the sparse actor/teammate/defender design
once per parent matchup; gather predictors to child clock rows and reduce
gradients back. Avoid duplicating a ten-player sparse design for every state in
every chain. Use exact sufficient-statistic aggregation where mathematically
valid, not target averaging that changes the likelihood.

With clock coefficients constrained to zero, state splitting must preserve
gradients, Hessian products, fitted player predictions and exposure/gauge support.
Raw summed GLM NLL can differ by a known **parameter-independent label-splitting
constant**; explicitly reconcile it rather than asserting false loss equality.
NN event comparisons continue using the existing parent-constant likelihood
contract. Parent/state count masks, dates, players and opportunity sums must match.

## 5. Training stability: S5 selects an averaged forecast

P policy is unchanged: Adam lr.001/weight_decay.0001, clipping5, cap96,
patience8/min_delta1e-5; choose minimum single-epoch inner validation objective.
Final fitting is fresh and fixed-length T. Preserve game batches/shuffle seeds,
initialization, dtype and physical projections. Profile-changing arms are refit,
not merely fed new inputs through old learned adjusted heads.

For S5, change **selection only**, not the optimizer, data or loss:

1. At each inner epoch e, evaluate its forecast on the same held-out inner
   quarter. Keep a ring of the last five validation **expected ledgers**.
2. Starting at e=5, average complete ledgers over e−4…e. Reconstruct event
   probabilities from averaged numerators/denominators; score that mixture with
   the original normalized event+point objective. Do not average losses, logits
   or probabilities independently. For FULL, mix conditional-state ledgers before
   computing conditional losses and original game/off5 point MSE.
3. Select endpoint T with the smallest mixture objective; earlier endpoint wins
   an exact tie. Apply the same min_delta1e-5/patience8 to this scalar, starting
   at epoch5. Cap96. Never use outer outcomes, final-fit training loss or a
   separately favorable reference leaderboard to select T.
4. Fit the final prefix afresh for exactly T epochs, saving T−4…T. The primary
   forecast is their equal-weight expected-ledger mixture; also save endpoint-T
   direct for diagnostics. Do not average the eight patience epochs after T.
5. Record both single-epoch and mixture validation curves, selected T, plateau
   width, native/reference metrics, saturation and timing. Resume serializes the
   last-five window or its exact replay references, RNG, optimizer, stale counter
   and selected endpoint. Stop/resume must reproduce the same selection/forecasts.

Before epoch5, log partial-window diagnostics but do not select or stop. P arms
retain their original min(5,T) short window. That difference is part of the
declared selection policy; report its frequency. If S5 hits96, complete at its
selected endpoint and flag the cap—do not extend epochs from outer results.

Cache the inner validation ledgers or sufficient exact mixture data rather than
re-inferencing five checkpoints every epoch. Check memory on the largest pilot.
An optimization may skip the unused reference-context integration during ordinary
FULL inner epochs, but must preserve the selection trajectory and compute both
views for selected/final mixtures. Compare against the unoptimized implementation
on bounded pilots; no edits to frozen v19 producers. This is not a scientific arm.

## 6. Recovery of known player effects: a bounded empirical prerequisite

Build a small synthetic laboratory for the **profile estimator**, separate from
basketball outcome validation. Generate64players,2,000matchup-state observations,
five distinct players per side, clock support over12known states,50possessions
per group and known nonzero player/clock effects. Generate valid family-specific
Poisson/multinomial/binomial/recovery labels; do not force NBA fixture rankings.
Use seeds20001–20020; freeze generator coefficients/scales before running.

Four scenarios, each with the original and context-adjusted estimator:

1. Balanced deployment and zero clock effect: negative control.
2. Uneven, overlapping deployment with nonzero clock effects: recovery test.
3. Strong but imperfect player-clock segregation: weak-identification test.
4. Additional hidden player-context interaction absent from the fitted model:
   misspecification test, exposing limits of the additive nuisance decomposition.

Predefine player effects scale.15 and shared clock scale.25 on canonical link
coordinates, alternating favored state groups across player groups; deployment
odds ratios1/4/20 for scenarios1/2/3. Scenario4 uses scenario2 deployment plus
hidden interaction scale.20. Independent latent draws are recentered into each
fit's exposure/class gauge before coefficient comparisons. Use the same fixed
player/clock ridge1000 in the paired synthetic fits, not a truth-selected grid.

Report player/clock coefficient RMSE after gauge alignment, unseen-composition
common-environment prediction error, convergence, condition/overlap diagnostics
and interval coverage/width under the **known synthetic truth**. Use128joint
draws here, not for the entire production library. Report Monte Carlo uncertainty
over20replicates; do not tune until recovery plots look ideal.

Exact arithmetic/temporal failures block implementation. Failure to improve
recovery under overlapping known-model conditions triggers a documented
investigation before expensive profiles; it is not permission to modify the
frozen generator or declare real basketball success. Poor misspecified-case
coverage is valuable negative evidence, not a defect to conceal. Synthetic
coverage does not certify NBA latent quality.

## 7. Uncertainty modeling: small, explicit and separately scored

Retain candidate-specific U0 and constant-discrepancy U1 for **all eight primary
forecasts**, with their own strictly previous residuals. Include direct/half
legacy views for continuity. Re-pool primary2016–2026 explicitly; warmup is used
for calibration, never silently included in primary interval summaries.

Add a bounded **transport discrepancy** experiment only for two preselected mean
forecasts, P_BASE and P_ADJ checkpoint-average-half. Do not choose them by v20
results. This tests new uncertainty structure while holding each mean fixed.

### 7.1 As-of descriptors, never current outcomes

Compute two transparent nonnegative descriptors:

- **R, predicted role stretch.** For each offensive player, compare model-implied
  FGA/FTA/TO shares from the NN's native averaged ledger to that player's prior
  observed share distribution. The additive half has no actor-event ledger and
  must not be assigned an invented share decomposition. Historical
  observations are game×off5 actor shares with730-day decay/five-year window;
  skip a channel's zero-total opportunities. Shrink first/second moments toward
  the prior league actor distribution with200possession pseudo-exposure; SD floor
  .05 share units. R is the maximum across five players of RMS standardized
  deviations over the three channels. Current-quarter observed shares cannot
  enter R. Export channels/players causing the stretch in basketball units.
- **C, historical clock-deployment mismatch.** At each profile snapshot compare
  each player's decayed possession clock distribution to the historical league
  distribution using Jensen–Shannon distance, natural logs, square root of the
  Jensen–Shannon divergence. Use offense possessions for the five offensive players
  and defensive possessions for the five defenders,730-day decay/five-year window
  for this descriptor on both sides. Smooth the player's histogram
  with200possessions of league mass; keep unknown clock explicit. C is the maximum
  distance across the ten specified players. This measures historical deployment
  mismatch, not the unknown distribution of their next game's clock exposure.

For the actual-opponent scoreboard, compute descriptors per given matchup and
aggregate possession-weighted to the off5 cell/pair. These evaluation weights are
the same descriptive opponent schedule used by the point forecast, not a feature
available for an unspecified future schedule. For a tool query, use its specified
opponent or the predeclared prior-opponent integration—never future schedules.
Never-seen players get league role/clock priors and an explicit thin-data label;
C=0 in that case is not evidence of high confidence. Keep U1/U0 and profile prior
variance visible. Clone appearances share one player's history, not independent
new observations.

### 7.2 Models and identification

Use the same disjoint-game pair likelihood/noise estimation as U1, with one common
bias and shared persistent variance. Add nested models:

    U_ROLE:       tau² = exp(a) + b_R * (R / scale_R)²
    U_ROLE_CLOCK: tau² = exp(a) + b_R * (R / scale_R)²
                              + b_C * (C / scale_C)²
    b_R, b_C >= 0

Scale each descriptor by its prior-pair RMS with a1e-6floor, no mean centering;
keep R/C and the squared features in receipts. Bound-constrained optimization
permits exact zero slopes. A prior-only ridge on standardized slopes uses the
existing .1/1/10 candidates, chosen on the last completed calibration quarter
with strongest numerical tie, then refitted on all previous eligible pairs.
During penalty validation, feature scaling and every fitted noise/discrepancy
quantity use only that subfit's earlier history; refit scaling afterward on the
full completed prefix. Historical R/C descriptors remain those emitted at each
forecast's original cutoff, not recalculated using today's profile/history bank.
The log-variance intercept and common bias are unpenalized. Preserve minimum
30pairs/two seasons; before identification return U0 and labeled unestimated
persistent uncertainty, never suppress a point score.

This is a **new restricted test of descriptors/shape**, not an invented discovery
that U2 exists. The earlier six-feature unconstrained log-variance U2 mostly
lost to U1, and an earlier role-distance widening heuristic failed. The changes
are the deployment descriptor, transparent predicted-share stretch and nested
nonnegative additive-variance form; improvement is not presumed. Positive slopes
are a named monotonic assumption, not a guarantee that five centers must be more
uncertain. Zero fitted slopes or failed coverage must be reported honestly.
The R/C moment tables are one separate strict-date descriptor library shared by
both mean-model comparisons; only model-implied query shares differ. They do not
use either model's fitted profile coefficients to define historical role truth.

Score joint log likelihood,80/95finite-outcome coverage, width and interval score
on identical eligible pairs, plus prior-cut support bins, novel/debut/thin/transfer.
Use the balanced-date split as primary; chronological split is a persistence
sensitivity, not extra independent observations. Publish persistent tau separately
from finite-game noise. Do not call an interval for observed quarter outcomes a
validated interval for arbitrary latent lineup quality. No coverage gate.

## 8. Evaluation and registered comparison families

### 8.1 Prediction

Primary metric: possession-weighted RMSE, reference checkpoint-average-half,
same broad population. Report MAE/r²/correlation/bias, all views, perquarter/
season/seed, leave-one-season-out and predeclared original slices. Seeds are
prediction replicates, not33independent seasons.

**Eleven new mechanism edges** of the factorial:

- Profile: P_ADJ−P_BASE, P_BOTH−P_CONTEXT, S_ADJ−S_BASE, S_BOTH−S_CONTEXT.
- Decoder: P_BOTH−P_ADJ, S_CONTEXT−S_BASE, S_BOTH−S_ADJ.
- Selection: S_BASE−P_BASE, S_CONTEXT−P_CONTEXT, S_ADJ−P_ADJ, S_BOTH−P_BOTH.

P_CONTEXT−P_BASE is an already observed historical decoder edge; print it but
do not claim it as a new experiment result. Add the six new arms versus
additive_defense: **17primary point contrasts**, Holm across17. Use10,000
season-block bootstrap draws, seed201004, and exact2^11season swaps for each
paired forecast contrast. Report intervals and adjusted p-values separately.
Profile×decoder interaction contrasts under each selection policy are descriptive
bootstrapped differences-of-differences, not additional confirmatory wins.

The same eleven new edges ×four families form a separate **44-test actual-context
event-loss family**. No-context arms simply have no clock response, but score
against identical state labels/parent constants. Use averaged **ledger** likelihoods
after seed averaging, with per-seed losses also exported. Never compare loss of
an averaged forecast to average loss for another arm. Event exposures and point
populations are printed explicitly. Reconstruct reused-control mixture losses
if only per-seed loss tables are archived; do not pretend loss is linear.

Registered hypotheses are retrospective development tests, not untouched proof.
No extra claim from selecting whichever view/slice/arm has the highest r².

### 8.2 Coherence and deployment transport

Repeat the fixed32fixtures/10dates, three seeds, mirrored two-lineup forecasts
and original average-opponent reference. For every arm report offense in both
directions, margin, additive adjustment, event ledger, role stretch and context
sensitivity. Keep the mixed-date Korver limitation visible. No bonus or fixture
selection, and no demand that a particular player pairing win overall.

Preserve the146-cell/47,419-possession transfer cohort,907large observed role
changes and2,139role-change lineup cells; those are retrospective diagnostics.
Preserve the65two-big cells as a small observed analogue, not true five-center
ground truth. Report centers' FTA/initial opportunities/renewal/creation shortfall,
small-guard defense, genuine small-ball units and Adams/Robinson/Hart facilitation.
Distinguish player coefficients from identified causal teammate effects.

Add one **as-of-feature deployment-risk slice**, not a list chosen
for large realized errors: within each origin, predict R from given lineups and
historical reference opponents; label high stretch above the95th percentile of
that origin's past observed compositions scored with the same origin model and
origin-frozen inputs (no future outcomes). Freeze the threshold before outer
outcomes. Report future supported cells and low-support cells separately, never
replace the original transfer cohort. The queried future lineup is given, just
as on the main benchmark; we are not forecasting which players a coach will use.
This tests prior risk tagging, not verified transaction/injury identification.
For comparison, use the same P_BASE-based
membership for every arm; candidate-specific R is explanatory only.

Export all observed >=200possessions/5games context curves, not just selected
Denver/Houston/GSW tails. Identify clock support, coefficient shifts, shortfall and
renewal separately. A lower synthetic margin with higher implausible FTA is not a
coherence pass. Do not train on fixture expectations.

Average-opponent:512deterministic prior-opponent draws, same common random numbers,
all primary cells;4096sensitivity on the fixed first20lexicographic cells/origin.
Score against realized outcomes with the same known estimand limitation. Cache
perplayer/perlineup encoder work; exact small decoder-state integration remains
separate from opponent sampling. No exhaustive resampling of all combinations.

### 8.3 Uncertainty and empirical stopping rules

For each of the two fixed mean models, compare U_ROLE−U1 and
U_ROLE_CLOCK−U_ROLE on season-pooled balanced-date joint log scores: four contrasts,
Holm across4, same10,000season bootstrap. Higher log score is better. Do not turn
nonidentified origins into zero losses or change eligible rows between competitors.
Coverage/width comparisons and synthetic widths are descriptive, with explicit
denominators. Preserve all U0/U1 candidate outputs regardless of the new result.

Review the three standards jointly:

| Finding | Decision implication |
| --- | --- |
| Adjusted profiles improve points and/or meaningful transfer/coherence | Keep upstream adjustment as a candidate; quantify event/uncertainty costs |
| Only S5 improves | Address estimator selection before richer architecture; do not credit profile adjustment |
| Only conditional event scores improve again | Situation prediction works; common-environment capabilities remain unproven |
| All means remain tied but uncertainty proper scores/transport improve | Real product progress; print predictive tradeoffs rather than dismiss it |
| Center margins fall via inflated FT/renewal or implausible defense | No coherent-mechanism success |
| No gain, with sound recoverability and fits | Reconsider raw state/role dynamics or possession-entry/FT-trip inputs; do not automatically add width |

No fixed r²-only promotion threshold. No automatic promotion at all.

## 9. Build order, audits and bounded pilots

### A. Foundation and recoverability

- New versioned `v20_profiles`, `v20_library`, `v20_features` and declarative
  `joint_capability_v20_protocol`; retain original files untouched.
- Inspect all source manifests/retention receipts; reconcile state→parent labels,
  including explicit observed-accounting exceptions. No repair of original targets.
- Tests: finite-difference gradient/Hessian; nullspaces and penalty invariance;
  unknown/zero-exposure states; zero-clock nested parity; actor permutation;
  joint-vs-dense Schur covariance on small problems; clone-shared draws;
  annual selection, snapshot and normalizer future-poison tests.
- Run the frozen synthetic recovery suite, not only unit tests.
- Real profile pilots:2016q1 and2026q4, all eight bank/family combinations,
  including covariance draws and correct preceding annual tuning. The pilot may
  fit directly at these cutoffs without production warm starts, but must not use
  future optimizer state or be misrepresented as a complete feature library.
  Converged same-protocol fits can be reused when receipts match exactly.

### B. Historical library

- After implementation/storage authority, build254×8=2,032snapshots plus annual
  four-candidate selection fits (original calendar has384; validate the count).
  Separate receipts and logs per snapshot/family. Partial libraries fail loudly;
  no silent missing-month forward fill. Reuse immutable mapped sources.
- Eight independent chronological chains, at most three workers/one numerical
  thread each. Schedule the long location chains early; warm starts remain
  strictly within their earlier-date chain. Free memory before the next bank.
- As-of feature audit exports exact byte/content receipts, metadata, changed
  coefficient distributions and calibrated/conditional channel losses; outer
  audit results cannot choose a profile builder. Changing frozen science requires
  a new protocol, not silently restarting with more favorable features.

### C. NN selection and end-to-end readiness

- New versioned `v20_fit`, `v20_run`, `v20_report`, `v20_uncertainty` consumers.
  Only new caches/contexts use the new profile schema. Keep native memoization,
  event accounting, precision guards and common additive calibration intact.
- Prove old-profile P_BASE/P_CONTEXT zero-change replay against saved controls
  on bounded prefixes; no full retraining of controls. Tests cover selected-epoch
  naming, ring-buffer averaging before scoring, no future inputs, deterministic
  resume, calibration/player-key separation and empty uncertainty status handling.
- Bind profile schema/source hashes in each prefix, memo, fit and forecast. A
  sentinel perturbation test must show new adjusted banks actually reach the NN;
  no hidden fallback to old coefficients, memoized features or normalizers merely
  because the97/49dimensions match. Preserve the documented unavailable2014q4
  additive-inner warmup diagnostic; never fabricate a teacher or control history.
- Full inner/final pilot for all six new arms at2016q1/s17; add S_ADJ and S_BOTH
  at2026q4/s17. Eight full pilots, reusable only under exact final fingerprints.
  Isolated pilot scorecards remain cold-start diagnostics, not partial production
  rankings. No arm selection from pilot outer accuracy.
- Run an actual production-shaped downstream rehearsal on these two pilot dates:
  retained-control parity, all report views, event losses, fixed fixtures available
  on the dates, average mode, U0/U1 cold status, synthetic identified uncertainty
  fit, persistence/covariance, contrast table schemas and independent audit.
- Verify `status`, leaderboard `--sort/--slice/--view`, per-case preview and durable
  launcher/perjob logs before handing Adam any launch command. Do not publish an
  invented shell command for an unimplemented runner.

### D. Full run and post-training work

Launch only after explicit approval. Run six-arm/three-seed cases with auditable
case slots; allow training jobs across origins to fill three worker slots, while
calibration/scoring advances only through **completed chronological prefixes**.
If that scheduling is not implemented, retain origin barriers and price their
idle cost—do not promise nonexistent utilization improvements.

Automatically execute registered analyses and independent audit after training.
Use a completion graph that distinguishes trained, scored, analyzed and reviewed;
write failure/complete states explicitly. Fix implementation defects with versioned
consumers and new outputs, never by editing completed campaign artifacts.

## 10. Runtime, storage and authority

This is a planning estimate, **not** a measured v20 launch forecast:

- Original profile library:254×8snapshots; saved queue wall time16.70h with three
  workers. Snapshot optimization alone sums21.58worker-hours; annual optimization
  adds3.51. Those totals exclude curvature/IO and must not be mistaken for wall
  time. Context expansion and coupled covariance may make the new library slower.
- Old144-case J_POINT_BOTH curves sum11.79worker-hours; v19 C_FULL20.49. These
  are fit timings, not full campaign timing. Six comparable new arms give about
  32.28h at ideal three-slot utilization **before** S5's extra epochs, setup,
  context-profile work, queue imbalance, pilots and analyses.
- Rough planning envelope: profile work17–35h, new NN cases35–55h, pilots/audits/
  analyses5–10h: approximately **60–100hours** overall. Profile solver/memory or
  later S5 endpoints could exceed it. Do not carry over v19's65-hour acceptance
  as authorization. Measure early/late pilots, simulate the actual scheduler and
  report central,1.2×training-stress and cap scenarios before launch. No hard kill
  deadline is requested.
- At planning inspection there is **about12.96GiB free**, only about3GiB above
  the existing10GiBreserve. This is a genuine future-launch blocker, not a reason
  to skip profiles or delete data automatically. Get separate storage/retention
  authority or another output volume, with all scientific artifacts preserved.
- Estimate percase checkpoints/resume/validation-ring storage, library/draws,
  interval detail and temporary peaks from pilots. Reuse sources by reference,
  not copies. New long-run output requirements must include the reserve and a
  compression/size stress margin. No cloud upload/rental, MPS switch or cleanup
  without separate approval.

Every long stage needs verbose append-safe logs with units/cutoffs/model/view,
epoch/batch/queue progress, elapsed/ETA, convergence, memory and free disk. Read-only
status must state completion counts independently for profiles, fits and analyses.
Avoid polling loops that consume assistant usage; give verified background and
monitoring commands once the implementation is ready. Background execution does
not imply an automatic assistant wakeup.

## 11. Required outputs and handoff

Use one fresh production root with linked source hashes; stage siblings and fresh
analysis prefixes. Mandatory deliverables:

- Frozen plan/protocol/arm grid, source/retention/producer hashes, authority record.
- Profile selection/snapshot/library receipts, support/clock effects, covariance
  solve diagnostics, synthetic recovery tables and pre/post deployment examples.
- Perfit curves/endpoint/window/RNG resume metadata, native ledgers for both
  environments, final/checkpoint weights, primary and all alternate-view forecasts.
- Matched reference/conditional scorecards, registered17point/44event contrasts,
  bias/within-quarter/seed/epoch analysis, all original slices plus as-of risk slice.
- Event units/calibration, transfer/role cases, full cross-channel covariance,
  fixed fixtures/context curves, average-opponent sensitivity and original-target
  observed-accounting reconciliation.
- Primary-only candidate U0/U1 and nested transport-uncertainty scores, intervals,
  failures/identification status, descriptor provenance and synthetic limitations.
- Independent metric/key/calibration/ledger/native-event audits, production-shaped
  pilot evidence, runtime/storage readiness and verified operational commands.
- `reports/joint_capability_v20_review.md` after completion: all three standards,
  hypotheses supported/rejected/unresolved, assumptions, result-selection limits
  and next decision. Update the single current handoff/state/scorecard/roadmap;
  archive displaced checkpoints without rewriting original research history.

Completed means experiments and interpretation, not just passing tests. Any
deferred item is named explicitly rather than hidden behind a COMPLETE label.
