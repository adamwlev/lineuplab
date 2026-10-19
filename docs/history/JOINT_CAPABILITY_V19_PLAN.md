# V19 — separate game environment from lineup capability

Design dated **2026-09-30**. **Planning checkpoint, not implemented or approved
for full launch.** Adam requested reflection, a synthesized experiment and
documentation first. Implement directly when authorized; no delegation.

This is the proposed implementation contract. Freeze its executable protocol,
source manifests and any justified preflight amendments before full training.
Pilots may establish correctness and cost, not select arms on outer results.
Do not change the experiment after inspecting its evaluation outcomes.

## 1. Why this experiment, and why now

The product remains a date-specific, two-lineup tool, defaulting to a league
average opponent. Fans should not have to specify a score or time remaining.
Prediction, basketball coherence and honest OOD uncertainty have equal standing.
No known-pair chemistry, forced named-player rankings or coverage gate.

The research has made real progress. Adjusted player capabilities and learned
teammate context are useful; the NN is not merely a complicated additive model.
But v17–v18 did not establish another primary point winner. The retained
J_POINT_BOTH half has broad r² .162915 versus additive_defense .146023, on
8,345 lineup-quarter cells / 1,013,999 possessions. These are historical
development results, not fresh prospective confirmation.

The evidence now points to a more specific deficiency than network capacity:

| Evidence | Design consequence |
| --- | --- |
| v16 adjusted profiles helped; extra width/attention/phases did not establish a compelling gain | Keep the profile backbone; do not repeat an architecture sweep |
| v18 R_ALLOC improves count likelihood in all 11 seasons, without improving primary point accuracy | Compare context with/without that existing allocator; inspect coupled errors, not just count loss |
| Removing learned teammate information worsens several event families in all 11 seasons | Retain learned complementarity; do not collapse to pure bookkeeping |
| NN shooting log loss .657272 beats dated player50 .658250; previous-quarter residual correction worsens it to .658115 | Keep the useful conversion estimator; no recent-shooting correction sweep |
| Conversion residual correlation .0367 across random game halves, .0188 chronologically | Large realized shooting errors are not demonstrated large recoverable signal |
| CLOCK changes broad FTA bias +1.890 to −.025 attempts/100, and transfer +4.296 to +.961 | Test shared game environment during fitting, not only after-the-fact target adjustment |
| Persistent component diagonals sum to 19.235, but cross terms offset −8.703 | Diagnose the whole FGA/FTA/TO/renewal/points ledger; do not independently subtract FT errors |
| All tested candidates still favor the legal-center fixtures; finite-game coverage does not establish synthetic-quality coverage | Coherence and uncertainty remain mandatory experiments, not assumed benefits of a point gain |

Sources: [v16 review](../../reports/joint_capability_v16_codex_review.md),
[v17 review](../../reports/joint_capability_v17_codex_review.md),
[v18 review](../../reports/joint_capability_v18_codex_review.md),
[role/volume diagnosis](../../reports/v18_role_volume_diagnostic_review.md), and
[persistence/coupling review](../../reports/v18_residual_persistence_review.md).

**Hypothesis:** part of the apparent player/lineup opportunity pattern reflects
when a lineup is deployed. Learning a small shared situation effect alongside
capabilities may improve the capability estimate and its transport. This is not
established by the diagnostic: clock effects also absorb lineup composition;
margin is additionally a potential consequence of lineup quality.

## 2. Questions and three distinct prediction contracts

Let F(L,D,s) be a complete expected event ledger for offense L, defense D and
pre-possession situation s. Points are derived from expected makes, not a new
unrestricted point head. Let w_t(s) be a strictly historical reference distribution.

1. **Reference-environment rating:** sum_s w_t(s) F(L,D,s). The same w_t applies
   to every lineup at that date. This is the intended fan-facing meaning and
   requires no game-state input. Average over complete ledgers, then derive
   rates/probabilities; do not evaluate at mean inputs or average logits.
2. **Original benchmark comparison:** reference-environment predictions pooled
   over the same realized defensive matchups and possessions as the old
   off5-quarter benchmark, compared with its original points. This preserves
   the predictive scorecard, but actual deployments need not follow w_t. It is
   opponent-conditioned historical evaluation, not a fully specified pre-quarter
   schedule forecast or causal quality ground truth.
3. **Actual-context conditional prediction:** F(L,D,s_actual), pooled back to
   the same cells. Future clock/margin and exposure are supplied for this
   diagnostic only. Use equally context-informed controls. Never mix these
   scores into the original leaderboard or advertise them as forecast gains.

Also retain the existing average-opponent product readout: integrate the
reference-environment ledger over the same prior opponent bank. Use a common
reference product distribution w_t(s) × p_t(D), not a lineup-specific future
deployment distribution. This standardization deliberately removes the observed
association between opponent identity and situation; it is not a causal claim.

For each new model report all three contracts. A conditional-only gain means
we modeled situation successfully, **not** that we learned better player values.
Do not describe a reference-environment rating as predicting a lineup's actual
future deployment policy. Retain original raw outcomes alongside every adjusted
diagnostic target.

## 3. Data and temporal contract

Reuse the verified v16/v18 possession, shot, dated feature, adjusted-capability,
parent-fit and opponent artifacts. No scraping, database mutation, upstream
profile/input-cache rebuild or modification of a completed producer. New context
labels are a **new derived training view**, written to a new namespace, not an
overwrite of old caches. Read-only database access is permissible only if a
specific mapping gap warrants it; document any such use before proceeding.

### 3.1 Context labels and grouping

Use the already audited **pre-possession** period, time remaining and offensive
margin mappings from the situation/persistence work. Preserve possession and
lineup attribution conventions. Do not substitute shot-time or end-of-possession
score, realized fouls, shot result, possession duration or final outcome.

- CLOCK: regulation periods 1–4 and OT; remaining-time bins [0,30], (30,60],
  (60,120], (120,240], (240,480], (480,720]. Preserve the existing 31-category
  schema including unknown; impossible OT bins have no learned effect.
- MARGIN: additionally <=−10, −9..−4, −3..3, 4..9, >=10. Preserve existing
  missing-value semantics. Missing margin falls back to CLOCK, not a learned
  missingness shortcut. Missing CLOCK uses the base environment.
- Split each existing game×off5×def5 row by possession-start state, retaining
  its original parent key. Counts, locations, makes, points and rebound labels
  must come from the corresponding actual possessions, not copied parent means.
- Carry all original channel-observation masks through the split. Do not gain
  apparently clean labels by discarding the unobserved portion of a masked
  parent. Preserve every point row, including unknown context.
- Sum back exactly to original parent counts, masks/exposures and points.
  Preserve original game×off5 auxiliary point groups. No duplicated possessions
  or attempt-weighted accidental replacement of possession weights.
- Context describes the start of the possession; stationary renewal does not
  simulate elapsed clock or changing margin after an offensive rebound.

The main point population remains 8,345 cells / 1,013,999 possessions, 44 primary
quarters. The 8,292 / 874,715 joint-label diagnostic population is separate.
Full attempt-level proper scores use their separately recorded support, not the
broad-cell count. Keep the fixed transfer cohort (146 / 47,419) and original
novel/thin/debut definitions. The role-change library is retrospective diagnosis,
not a prospective input or a new way to select the primary population.

### 3.2 Cutoffs, reference distributions and leakage

Retain 48 quarterly origins, 2015 warmup, 2016–2026 primary evaluation, seeds
17/23/41, existing five-year training window and 730-day training half-life.
For each origin use the existing preceding-quarter inner validation; final
fit is fresh from its proper dated parent using all eligible pre-origin data,
for the selected number of epochs. No outer label selects epochs or penalties.

Every feature bank, teacher, normalizer and shared nuisance component must
respect the **inner or final cutoff it serves**. Completed final-origin NN or
additive coefficients must not initialize an earlier inner fit. Audit exact
teacher dates/rows rather than assuming a file named `inner` is safe.

For reference weights use the fixed trailing 1,095-day context distribution,
365-day half-life, possessions as exposure, ending strictly before the relevant
fit cutoff. Save counts, effective exposures, fallbacks, cutoff and hashes.
All historical context labels are allowed as training labels/features inside
their proper fit. No precomputed outer-origin nuisance fitted on later outcomes
may be smuggled into earlier row inputs. The old diagnostic nuisance tables are
evidence/controls, not automatically valid dated NN features.

Reference centering/support statistics for inner training exclude validation.
After selection, recompute them on the allowed final prefix. Serving uses the
final prefix's reference distribution. Unknown context contributes its measured
reference mass but receives zero context displacement. Unsupported categories
fall back to zero displacement; no synthetic support is invented.

## 4. Model: small shared situation effects, existing basketball machinery

The foundation is J_POINT_BOTH: existing raw and adjusted player profiles,
teammate messages, opposing defense, supply/load constraints, and stationary
rebound renewal. Keep its widths, message rounds, point weight .25 and training
recipe. No player/team/pair identities in the context branch.

### 4.1 CLOCK opportunity branch

Learn a small shared category table, initialized to zero:

- Two independent action-log-rate contrasts, represented as three FGA/FTA/TO
  shifts with zero sum. Add them to the three decoded action logits **before**
  the existing allocation and supply/load operations. This removes the common
  shift that would disappear under normalization.
- One log initial-opportunity-scale shift. Apply it to the `non_rebound`
  first-entry mass used by renewal, not to a `budget` that is immediately divided
  out. This allows situation-dependent total event exposure as well as its mix.
  It must still produce finite, positive, terminating expected ledgers.

Use bounded raw displacement .75*tanh(theta), then center over the supported
known-context reference weights; unknown/unsupported effects stay zero.
Centering can expand the bound to 1.5: test and document that fact. No extra
uncentered global intercept. This identifies a reference gauge, not causal
player-versus-deployment separation. Print action Jacobian/rank and perturbation
checks so a normalized-away parameter cannot silently become a new arm.

The .44 FTA factor remains the inherited accounting approximation. It is **not**
an exact mutually exclusive possession-event probability. In particular,
intentional and technical FT sequences may violate its usual interpretation.
Report context-dependent approximation residuals; do not claim a newly exact
free-throw-trip model. No changing .44 or rebuilding trip labels in this campaign.

Use a fixed context regularizer in normalized objective units:
1e−3 × mean_c,k [500/(500+n_eff,c) × theta_c,k²], in addition to unchanged
optimizer weight decay. n_eff comes only from training exposure. Exclude
unsupported parameters from optimization, and export support, coefficients,
penalty and bound saturation. This is one predeclared regularizer, not a sweep.

### 4.2 Broader context and margin extensions

C_FULL additionally applies shared CLOCK effects to six location logits,
six location-conditioned make logits, and a single team ORB-vs-no-ORB recovery
log-odds shift. Location shifts have zero sum. Use the same bounded/centered
construction and regularization; do not alter frozen FT conversion or assisted
fraction. Place location/conversion effects before existing creation constraints;
place recovery on the existing team capture score path. Zero effects must
exactly recover the parent computation.

C_MARGIN adds only action/entry-scale effects, as CLOCK plus margin-within-clock
deviations. Center these deviations within their historical clock groups; use
250 rather than 500 in the margin penalty factor. Unknown/unsupported margin
falls back to clock. Integrate over the common historical joint clock/margin
distribution at serving. This is an **endogeneity sensitivity**, not the default
product candidate or evidence that controlling away score margin is causally right.

### 4.3 Exactly five trained arms

| Arm | What changes | Main comparison |
| --- | --- | --- |
| C_FIXED | Freeze a verified, same-split completed J_POINT_BOTH NN; learn only the CLOCK opportunity branch | Is a shared nuisance correction sufficient without relearning capability weights? |
| C_CLOCK | Jointly learn the J_POINT_BOTH backbone and CLOCK opportunity branch | C_FIXED: does adaptation add value? J_POINT_BOTH: does context help at all? |
| C_FULL | C_CLOCK plus context effects on location, conditional conversion and team capture | C_CLOCK: is count-only context leaving material situation effects in player capabilities? |
| C_ALLOC | C_CLOCK using the existing R_ALLOC action allocator, otherwise identical | C_CLOCK and R_ALLOC: does joint allocation become useful once situation is separated? |
| C_MARGIN | C_CLOCK plus the margin-within-clock branch | C_CLOCK: sensitivity to score context; explicitly not the primary candidate |

C_FIXED requires matched inner and final frozen teachers with verified cutoffs.
Its context-only inner fit selects context epochs; its final context fit is
fresh with the proper final teacher. It does not import the teacher's optimizer
or use final weights in inner selection. If the necessary teachers are missing,
stop and document the additional refits required before altering the contract.
Frozen NN weights do not mean fixed final conversion probabilities: changing
action load can still change the inherited supply/load penalty.

All joint arms start from the same dated parent initialization as the retained
rig, not from a completed final-origin winner. C_ALLOC uses the existing zero-
initialized allocator. No routing/gating sweep, no additional phases, no new
pair residuals or learned embeddings. No sequentially adding arms after results.

Five arms × 48 origins × 3 seeds = **720 cases / 1,440 inner and final fits**.
C_FIXED fits only the small context parameters. Reused teachers/controls are not
counted as newly trained NN cases; report any additional work separately.

## 5. Mandatory controls and objective-preserving replay

Reuse original J_POINT_BOTH, J_BOTH, R_ALLOC, O_ORDER, additive_defense and
parent_half_defense forecasts, with exact original and matched-population rows.
Keep additive as an additional historical row, not the opponent-aware comparator.

**No-context replay is a correctness gate, not another trained arm.** Splitting
Poisson observations changes log-factorial constants and thus can inadvertently
change family scaling. Use original parent-level constants:

    sum_state [n_s * rate_s − y_s * log(rate_s)]
        − Y_parent * log(N_parent) + lgamma(Y_parent + 1)

Apply this per actor/action with original masks/decay. When state rates are equal,
it equals the old parent Poisson NLL (with matching numerical clamp conventions).
Location, conversion and recovery likelihood numerators/exposures must also
sum to the old objective. Pool context predictions by possession weight back to
game×off5 **before** point MSE. Never compute a separate point MSE for each state.
Keep original shared prefix normalizers and family weights.

Prove predictions, loss and gradients agree with the legacy no-context path in
float64 tests and real micro-batches; require <=1e−8 absolute numerical difference
for ordinary finite test inputs, plus reported relative error for large sums.
If numerical behavior needs a different tolerance, justify/freeze it before
training. Do not quietly compensate for a failed replay by retuning loss weights.
Observe the usual common-valid-mask rules when joining rebound/shot ledgers.

For conditional point evaluation, add two low-cost controls:

- additive_defense + shared CLOCK point residual table;
- frozen J_POINT_BOTH + shared CLOCK point residual table.

Fit the residual table on the appropriate training prefix, using same-prefix
baseline predictions, the historical 500-possession shrinkage to zero and the
same reference centering. No lineup identities in this table. Its margin version
uses the hierarchical 250-possession shrinkage solely for the C_MARGIN readout.
Validate on held-out quarters. Since the table is centered, its reference-
environment additive displacement integrates to zero. These controls separate
generic context predictability from the value of a structural context branch.
They are point controls, not coherent event-ledger models. Their in-prefix fits
are training, not out-of-sample accuracy claims; inner/final fits remain distinct.

## 6. Fitting, inference, calibration and stopping

Retain Adam's current epoch rule: maximum 96, patience 8, minimum significant
validation improvement 1e−5, and the existing best-checkpoint versus patience
semantics. Adam optimizer lr .001, weight decay 1e−4, gradient clipping 5,
deterministic seed/game-batch ordering as inherited. Report actual selected
epochs, cap hits and near-tied validation curves; no epoch sweep.

Use actual historical situation in both training and inner validation, with
the original event-plus-game/off5-point objective. Report marginal inner point
scores as diagnostics, but do not introduce a second epoch selector. Final
weights never see outer outcomes. Last-min(5, selected) checkpoint predictions
are averaged as complete ledgers; they are not parameter averaging or extra
epochs after early stopping.

At outer evaluation save native outputs before calibration for both reference
and conditional views. Independently prequential-calibrate each view using only
earlier completed origins, with the repaired common v16 calibration convention.
Keep nonnegative slope constraints, centered columns and warmup rules. Do not
reuse a conditional calibrator for reference predictions, or recalibrate a
current quarter with its own labels. Record intercept, slope, spread and bias
before/after calibration, with explicit view-qualified column names.

Primary view remains calibrated 50:50 NN/additive_defense (`half`) for continuity;
also direct, checkpoint_average and checkpoint_average_half. Blend equally
informed conditional predictions in the conditional panel. The integrated
product uses integrated additive defense. No learned blending grid or model-
selection ensemble; calibration and half blending must not be mistaken for a
pure structural event ledger. Report native event fidelity separately.

## 7. Evaluation and interpretation — all three standards

### 7.1 Prediction and mechanism diagnosis

On original broad cells report RMSE, MAE, r², weighted correlation and
predicted-minus-observed bias in points/100. Show counts/exposure, per-season,
per-quarter and original novel/thin/debut/transfer slices. Keep conditional and
reference scoreboards physically separate, including their log headers.

Predeclare seven mechanism contrasts:
C_FIXED−J_POINT_BOTH; C_CLOCK−J_POINT_BOTH; C_CLOCK−C_FIXED;
C_FULL−C_CLOCK; C_ALLOC−C_CLOCK; C_ALLOC−R_ALLOC; C_MARGIN−C_CLOCK.
Add five arms against additive_defense and five against parent_half_defense:
17 primary reference-half RMSE contrasts. Use 10,000 season-block bootstrap
draws, seed 190930, and exact 2^11 paired season sign swaps with Holm across17.
Keep all cells in each sampled season together. The seven contrasts × four
event families form a separate28-test Holm family on actual-context event
likelihoods; the old models simply have no context dependence. Report conditional
point controls descriptively as a separate information contract, not another
route to a significant primary result. Other views/slices are descriptive.

Alongside NLL, report interpretable FGA/FTA/TO per100, location mix, FG/FT make
calibration, ORB/capture and exact point accounting. Use the common parent-
constant likelihood definition above for all event comparisons. Protect the
shooting diagnostic with attempt-weighted log loss/Brier and calibration by
location/season; an allocation gain that degrades useful conversion must be visible.

Repeat the existing random-game and chronological persistence partitions on
the fixed supported cohorts; export the **full cross-channel covariance matrix**
and total point covariance. Keep raw, model-conditional and diagnostic CLOCK
adjustments separate. Do not add a CLOCK target adjustment to a prediction that
already conditions on CLOCK. Do not sum component variances as independent noise.

Reference integration can improve common-environment meaning without improving
prediction of actual deployments. Conversely a conditional win without a
reference win does not prove transport. Explain both, not just the largest r².
No automatic selection of C_FULL or C_MARGIN from a favorable retrospective slice.

### 7.2 Basketball coherence and transport

Reuse the fixed 32 fixtures /10 dates and three seeds, existing actual-opponent
and average-opponent checks, same-season observed two-big analogues, and the
immutable transfer/role libraries. Report offense in both directions separately,
not only net margin. Preserve the documented cross-era Korver feature limitation.

For every fixture show native reference events/points, calibrated points,
additive and half, and context-integration sensitivity. Compare legal-center,
creation/spacing, Adams/Robinson/Hart and replacement responses as falsifiable
mechanism checks. No player bonus, hard-coded center penalty, or fixture-target
training/selection. A more plausible center result would be encouraging but
not proof that context solved an unsupported counterfactual.

Export late/early-game context response curves for the same fixtures and high-
support observed cases. Are context effects shared and bounded? Does changing
clock accidentally switch off player differences or inflate renewal? Inspect
load/shortage, initial mass, ORB continuation and constraints. Preserve the
Denver FTA-underprediction and Houston/GSW examples, alongside the complete
eligible cohort; named tails are not newly independent tests.

### 7.3 Uncertainty

Run candidate-specific U0 finite-game and U1 constant-discrepancy controls on
reference direct/half predictions, under the established prior-only protocol.
Intervals must use each candidate's own prior residuals, not copied parent
bands. Report nominal80/95 coverage, weighted coverage, width and proper scores
on broad, debut, novel/thin and transfer cells. Include native mean versus
calibration contributions to bias and the known status-contract tests.

These bands evaluated on actual games include deployment mismatch relative to
the common reference. Label that estimand explicitly. A separate conditional
residual-variance readout tests how much context explains, but is not substituted
for reference product intervals. Report residual channel covariance and seed/
context-reference sensitivity; neither constitutes synthetic latent coverage.

No new U2 network, no OOD coverage gate, no claim of calibrated arbitrary-lineup
quality. If latent uncertainty remains unidentified, the handoff must say so,
even if point accuracy or center ordering improves.

### 7.4 Decision table, not a single winner

| Outcome | Interpretation / next action |
| --- | --- |
| C_FIXED accounts for gains; joint C_CLOCK adds little | Prefer the simpler nuisance decomposition as research direction |
| Joint model improves reference prediction and/or defensible coherence without hidden event/uncertainty costs | Evidence for context-aware capability learning; quantify predictive tradeoffs, no automatic promotion |
| Only actual-context scores improve | Situation is predictive; common-environment player estimation remains unproven |
| C_FULL improves conditional shooting as well as reference behavior | Count-only nuisance was too narrow; retain conversion evidence, not a blanket conversion freeze |
| C_ALLOC helps counts but not total points again | Allocation remains an explanation/mechanism gain, not a predictive win |
| Margin alone helps | Investigate endogenous conditioning; do not adopt it as the default on that basis |
| No useful gain despite correct nuisance behavior | Revisit deployment-contaminated profiles/role state or possession-entry data, rather than add NN width |

Small predictive costs may be acceptable for meaningful gains on the other
standards, per the product contract. Do not invent an r²-only acceptance threshold.
No arm is promoted or deployed by this experiment.

## 8. Runtime engineering and bounded preflight

Planning target: retain **54 hours for the complete campaign**, subject to
measured preflight and Adam's launch approval. This is a proposed budget, not a
newly measured estimate or a hard process kill. V18's seven arms plus analyses
took41.188 supervisor hours; v19 has fewer arms but more state computation.
Do not extrapolate runtime from arm count alone.

- Compute expensive player/profile/message representations once per original
  matchup row. Expand only the differentiable context/ledger portion to state
  rows. Cache only immutable or genuinely frozen calculations; never detach
  learnable shared features. Accumulate gradients before the inherited optimizer
  step. Keep complete games together and avoid training one state per step.
- Enumerate the finite CLOCK categories exactly, chunked. For margin integrate
  only supported joint categories with exact weights. No Monte Carlo clock
  approximation and no replacing integrated ledgers with a mean context.
- Reuse opponent-bank512 integration; check4096 only on the fixed first20
  eligible cells/date, as previously. Benchmark this **with** context integration.
  Batch reuse prevents opponent×context from repeating the expensive encoder.
- Three CPU workers, one numerical thread each, remains the starting point.
  Measure both one and three workers, memory and disk; no unbenchmarked GPU move.
- First audit all source manifests/teacher availability. Then zero-context
  micro-batches for every arm at2016q1 and2026q4, seed17,12batches each. These are
  numerical/runtime tests, not outer model comparisons.
- Run one full inner/final pilot per arm at2016q1/s17. Add late-origin full
  pilots for C_CLOCK and C_FULL at2026q4/s17 for scaling. All7 cases are reusable
  if protocol/source fingerprints stay identical. No pilot-result arm selection.
- Time one complete downstream-origin bundle plus the fixed fixture batch,
  including reference/opponent integration, uncertainty, summary and verification.
  Use an actual late-size workload, not tiny synthetic inference to estimate cost.

Before requesting full launch, report case/fit counts, projected selected/cap
epoch cost,1.2× training stress estimate, downstream wall time, peak RAM and
projected disk with at least10GiB reserve. Target reference estimate <=48h and
stress estimate <=54h. If exceeded, optimize exact computation first; if still
over, return a documented scope/runtime choice to Adam **before** launch. Do not
silently reduce seeds, remove a poor pilot arm or skip uncertainty/coherence.

## 9. Implementation order and acceptance tests

1. **Provenance and derived labels.** New versioned v19 modules; import frozen
   helpers only where source hashes/semantics are verified. Export context join,
   chronology/mask/parent reconciliation and teacher availability audits.
2. **Ledger and objective replay.** Implement the zero branch and efficient
   state pooling; prove value/gradient/objective equality before fitting context.
3. **Five branches and proper fitting.** Explicit feature/channel allowlists,
   support/gauge tests, nested initialization and separate inner/final teachers.
4. **End-to-end small smoke and seven pilots.** Durable logs; prove resume,
   output receipts and expected case counts; independently reproduce metrics.
5. **Launch readiness only.** Deliver verified launch/live-log/status/report/
   case-preview commands. Do not start the full campaign until Adam asks.
6. **After full completion.** Run all frozen analyses, independently audit
   source receipts and arithmetic, write the scientific review and current handoff.

Required tests include:

- Poison future outcomes and validation-only labels: no train-side statistics,
  teacher weights, reference weights or nuisance controls change.
- Boundary/OT/missing clock and offensive-margin sign; no post-possession data.
- Exact possession/actor/event/point reaggregation; masked parents, technical
  FTs and zero-attempt rows; no silent shrinkage of the original point population.
- Zero-context nested outputs and gradients; shared normalizers; game/off5 point
  pooling invariant to state subdivision and row ordering.
- Context gauge removes common action shifts; finite nonzero gradients for every
  intended parameter; unknown/fallback semantics and support penalty behavior.
- C_FIXED backbone stays byte-identical; joint arms get nonzero encoder gradients;
  micro-batch recombination matches the unoptimized reference forward/backward.
- Complete-ledger integration versus explicit category loops; zero effects
  recover original predictions; average probabilities versus counts trap;
  baseline and mixture event-to-point identities; both directions of a matchup.
- Renewal termination and finite rates under extreme legal profiles/context;
  context boundary saturation exported, not hidden by post-hoc clipping.
- Calibration identities/spread, no view-column collision, prior-only fits and
  proper conditional controls; constant-prediction correlation may be undefined
  and must be flagged honestly, never silently rendered as a successful fit.
- Resume equivalence, completed-output refusal, independent summary recomputation,
  failed-child propagation and correct finite-interval status aggregation.

Tests support, not replace, empirical experiments. Correctness failures pause
the campaign; unfavorable scientific outcomes do not justify editing its design.

## 10. Artifacts, logs and final handoff

Reserve new prefixes under `experiments/cache/joint_capability_<date>_v19_*` for
context-derived data, pilots, production and independent analyses. Final exact
paths are established by implementation, not existing runnable paths today.
Never write into a v16/v17/v18 completed directory or change its producer hash.

Expected versioned entry points: `experiments/run_joint_capability_v19.sh`,
`experiments/joint_capability_v19_run.py`, protocol/data/model/loss/fit modules,
and a read-only v19 case preview. These are **to be built**, not commands to run.
Persist durable verbose launcher, supervisor and per-case logs. Print origin,
arm, seed, phase, epoch/cap, best epoch, patience, four event losses, point loss,
elapsed/ETA and completion counts; on completed origins print matched quantitative
comparisons with additive_defense, parent_half_defense, J_POINT_BOTH and C_FIXED.
Use visible reference-versus-conditional labels; no misleading all-zero partial
scorecard. Incomplete comparisons explicitly name missing cases.

Required new derived outputs:

- context/parent/teacher/source manifests and cutoff/support audits;
- native/reference/conditional ledgers, predictions, calibration coefficients;
- separately labeled original-population and conditional scorecards, season
  contrasts and multiplicity tables;
- shared context coefficients/support/saturation and response curves;
- count/location/conversion/recovery diagnostics, full covariance matrices and
  persistence partitions, unchanged transfer and retrospective role slices;
- fixture/average-opponent integration and convergence receipts;
- candidate-specific U0/U1 bands/proper scores and explicit latent-OOD limits;
- runtime/disk report, independent verification and COMPLETE/failed receipts.

Finish with `reports/joint_capability_v19_review.md` and an implementation/
reproduction handoff. Update SESSION_HANDOFF, JOINT_CAPABILITY_STATE,
MODEL_SCORECARD and MODEL_RESEARCH_ROADMAP in their separate roles, archiving
displaced operational context. Preserve original reports/protocols. No commit,
promotion or deployment without current authority.

## 11. What remains on the table after v19

This experiment does not settle all promising directions:

- **Context-adjusted player-profile refits:** raw and ridge-adjusted inputs still
  contain historical deployment. Refit them only in a separately controlled,
  fully dated experiment if decoder context is useful but insufficient.
- **Role state/ability separation:** test prospective roster/role signals and
  multiple timescales, not a correction chosen from outcome-selected role cases.
- **Possession-entry coupling and true FT trips:** transition after opponent
  turnovers/misses, crash-versus-retreat and exact trips need audited additional
  labels; replacing .44 is a different hypothesis.
- **Latent-quality uncertainty:** persistent discrepancy and transport require
  more than finite-game bands, seed variation or context integration.
- **Dated cross-era transport, richer defensive/tracking inputs and tool work:**
  valuable separate scopes; no new ingestion, assignments or public scorer here.

The immediate goal is not to win every leaderboard row. It is to learn whether
separating shared game environment gives us a more useful, coherent estimate of
what players can do together—and to identify precisely what remains if it does not.
