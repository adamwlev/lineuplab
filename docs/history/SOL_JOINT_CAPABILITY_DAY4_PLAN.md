# Day 4: connect basketball mechanisms, team points, and individual value

Written by Codex/Astra, 2026-09-12, after reviewing the completed v5–v9 sprint.
Read `reports/joint_capability_v5_v9_codex_review.md` for the independent review.

**Status: implementation and experiment plan, not a launched experiment.** Adam
asked for a plan for Sol. When asked to implement this document, Sol may do the
bounded implementation, saved-artifact analyses, and smoke/parity checks below.
Give Adam verified background commands for the full training run and wait for
his explicit launch instruction. No delegation. No commits.

## 1. Purpose, priority, and authority

Answer three questions, in order:

1. Where do the standardization/spread event improvements go when converted
   into team points: useful changes, cancellation, calibration, or noise?
2. Can a simple forward-only blend reliably retain additive's individual-value
   information and the NN's useful contextual signal?
3. Does explicitly supervising the basketball decoder's TEAM point total help,
   while retaining the event losses and the same structural architecture?

The outcome is a completed comparison and a basketball-readable explanation,
not a test-count milestone. Do not spend the day building a general framework.
Do not make a statistically significant win a condition of completing the work.

This is the next-work ordering, superseding the recommendations that a more
powerful point benchmark is a prerequisite for all further work and that the
objective/points disconnect is proved to be resolution rather than alignment.
It does NOT retroactively change any v5–v9 protocol, result, or user decision.
The new objective below belongs only to a new experiment. The five original
event families remain present with unchanged relative weights.

Three co-equal standards remain in force (`CONTEXTUAL_MODEL.md` §2): forward
prediction, basketball-coherent counterfactuals, and honest OOD uncertainty.
Adam has deferred page/gate work; do not turn this into deployment or a new
coverage-rule project. Research diagnostics for the latter two standards are
mandatory, not grounds for imposing a favorite player's ranking.

### Boundaries

- No delegation, Opus run, parallel editing agent, scraping, network fetch,
  database access/mutation, input-cache rebuild, scorer promotion, deployment,
  staging, or commit. Establish sole editing ownership before starting.
- Preserve all completed run directories, original feedback, and old plans and
  reviews. Read frozen inputs in place. Derived reports and predictions go to a
  NEW prefix. Do not invoke a historical preflight that builds missing inputs.
- No new player-ID parameters, known-pair effects, named-player bonuses,
  synthetic-label training, architecture search, or additive refit.
- Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u` and durable logs
  for numerical scripts, tests, and training. Print actual command/exit status.
- Scientific code/protocol changes after production starts require a new prefix
  and an explicit record. Never resume stale work under a revised fingerprint.

## 2. Starting evidence and immutable inputs

Read AGENTS.md and required context, then this plan and its review. Consult
`JOINT_CAPABILITY_STATE.md`, `JOINT_CAPABILITY_LEARNINGS.md`, `BACKLOG.md`
§0ae–0ak, and `MODEL_RESEARCH_ROADMAP.md` for historical evidence, subject to the
qualifications in the new review. Do not reread every old experiment before
working. Route to relevant code as needed.

Primary sources:

- `experiments/cache/joint_capability_2026_09_09_v3/derived/`:
  `game_lineups.npz`, `player_game_states_v3.npz`; fixture definitions are in
  that run's root `fixtures.json` and `diagnostics/basketball_derived_fixtures.json`.
- `experiments/cache/joint_capability_2026_09_10_v4e/`: E0M_L2 and E1P_L2
  historical controls, where requested below.
- `experiments/cache/joint_capability_2026_09_11_v8/`: V8_BASE, V8_STD.
- `experiments/cache/joint_capability_2026_09_12_v9/`: V9_BASE, V9_SPREAD,
  V9_ALL, and saved depth/decoder fits for the bounded correctness diagnosis.
  Reuse its existing sidecar/rebound inputs when using JointDataV9.
- `experiments/cache/asof_points_centered_2026/`: corrected additive reference,
  calibration, and per-player contribution ledgers; follow recorded provenance
  to existing original additive fit snapshots only when needed for replay.

No guessed ID mapping, no joining frames by row position alone. Assert unique
keys and identical outcomes, exposures, dates, league references, and novelty
flags on shared cells. A directory called complete is not proof of validity.

Historical primary population: **2016–2026, 44 quarter origins, 5,607 cells,
726,364 possessions; novel 2,073 cells / 226,256 possessions**. Four 2015 origins
are calibration warmup. Also reproduce the 2015–2026 descriptive summary
(6,179 cells / 803,447 possessions), clearly separate from primary inference.

Useful primary-population checks (rounded; derive unrounded values from files):

| Model | MAE | RMSE | Novel RMSE |
|---|---:|---:|---:|
| corrected additive | 8.091953 | 10.840994 | 11.853019 |
| v4 E0M_L2 | 8.122390 | 10.879681 | 11.799056 |
| V9_SPREAD | 8.140175 | 10.866667 | 11.772833 |
| V9_ALL, historical unmodified | 8.130058 | 10.854637 | 11.768008 |
| half additive + half historical V9_ALL | 8.066906 | 10.801115 | 11.763034 |

V9_SPREAD, not V9_ALL, is the new backbone: standardized mean+sd senders, one
round, diagonal decoder, 2,390 parameters, no encoder. V9_ALL is a historical
predictive reference with an FT-isolation caveat, not the chosen architecture.

## 3. P0 — establish trustworthy replay; then move on

Use new modules/adapters. Do not edit the historical scientific implementations
just to make old assertions pass or change a frozen code hash.

### P0.1 Score and provenance reconciliation

Reproduce the table above, plus V8_BASE, V8_STD, V9_BASE, and v4 E1P_L2.
Save exact common keys, source hashes, population receipts and paired metrics.
Confirm V8_STD and V9_BASE parity. Account for every absent origin or cell;
never silently intersect away a failure in a required primary arm.

### P0.2 Two v9 diagnostic issues

1. `joint_capability_v9_run.predict_rows(zero_message=True)` zeros only round
   one. Build a read-only replay helper that really disables ALL message rounds,
   without changing the checkpoint. It must restore parameters/mode even on an
   exception. Produce corrected derived no-message diagnostics for V9_DEPTH
   and V9_ALL at 2016q1, 2021q1, 2026q4. Preserve original saved columns.
2. `joint_capability_v9_model.decode` mixes contextual coordinates into the FT
   output in rank-positive arms. Demonstrate this on saved fits at those same
   origins by fixing a receiver's state and changing the other four players.
   Record the probability delta; do not call it a change in observed FT skill.
   Future Day4 models use rank=0 and must pass the FT-isolation test AFTER a
   nonzero message has been learned, not just at zero initialization.

Do NOT repair/retrain V9_ALL or retrospectively substitute altered forecasts
into its original scorecard. Mark its ordinary predictions as historical and
its old no-message decomposition as invalid for that purpose. Those issues do
not invalidate V9_SPREAD. A fixed legacy decoder is outside this day's scope.

Limit this phase to the relevant regression tests and replay. If it exposes an
unrelated substantial defect, document the blocker and continue independent
work; do not launch a general cleanup campaign.

## 4. P1 — explain the event-to-points disconnect on actual data

No fitting of new neural models. Replay saved fits in batches where player
predictions were not saved. Write derived player/channel outputs under the new
prefix, never into the source run. Reuse that replay for later case/fixture work.

### P1.1 Exact prediction-change and loss-change accounting

Mandatory contrasts: V8_STD−V8_BASE, V9_SPREAD−V9_BASE, and
V9_SPREAD−V8_BASE. Evaluate on the frozen primary cells; also show the full
eligible grouped event population separately. Do not compare event improvements
on one population with points on another without printing the distinction.

For each model reconstruct native points from player predictions:

    N = 100 * [sum_i,k FGA_i * location_ik * make_ik * value_k
                + sum_i FTA_i * FTmake_i]

Use four blocks: team FGA/FTA totals; their within-team player allocation
shares; conditional shot-location mix; conditional FG/FT conversion. Compute
the exact four-block Shapley decomposition of A→B using all 16 combinations
(equivalently average all 24 orders), without model refitting. This is an
arithmetic attribution, not a causal or physically realizable intervention.
Turnovers influence volume through the budget; do not add a second turnover
point credit on top of the identity. Report turnover changes alongside it.

Aggregate predictions/components by possession exposure before scoring a cell.
Account for affine calibration separately. With a common league level L:

    P_m = L + a_m + b_m * (N_m - L)
    point_component_k = (b_A + b_B)/2 * native_component_k
    calibration_component = (a_B-a_A) + (b_B-b_A)*((N_A+N_B)/2-L)

These sum exactly to P_B−P_A. For every component d_k of that difference,

    squared_loss_component_k = d_k * [(P_A-y) + (P_B-y)]

Their sum is exactly squared_error_B−squared_error_A. This reveals whether
volume, allocation, location, conversion, or calibration helps/hurts the point
forecast and whether contributions cancel. Do not force an analogous additive
breakdown of MAE; report MAE normally. Save components, cross-component
covariance, per-season contributions, and native versus calibrated results.

Use float64 accounting; assert its identities to numerical tolerance (1e-8 in
the derived arithmetic). Saved Torch/native prediction replay may differ by
float32 roundoff: report max discrepancy, require <=1e-4 points/100, and
investigate larger discrepancies rather than loosening tolerance post hoc.

### P1.2 Locate the residual individual-value gap

Compare additive and V9_SPREAD on ALL/novel/recurring primary cells, plus fixed
bins of prior exact-five exposure: 0, 1–99, 100–499, >=500 possessions. Compute
history strictly before the origin, using the frozen index/cached groups, not
the current evaluation window. Match the original novelty definition.

Show signed bias, MAE, RMSE, prediction disagreement, and the contribution of
each stratum to the pooled loss gap. Also summarize by minimum player-history
support and by era (2016–2019, 2020–2023, 2024–2026). This is descriptive
localization, not a causal test that additive memorizes recurring lineups.

Publish 12 basketball-readable cases: six largest exposure-weighted excess
squared-error contributors where NN loses and six where it wins, with at most
one cell per exact five in each list (deterministic key tie break). No new
exposure threshold. Show each case's possessions/games and its other available
quarters so a one-window extreme is visible. These are outcome-selected
diagnostic cases, not a confirmation sample.

For each: names/season/date; actual/additive/NN/half-blend; all five additive
base/carry/experience contributions and calibration/reference terms; NN player
attempts/location/conversion/points and team calibration. Add no-message
prediction and label it an ablation, NOT a pure additive baseline or identified
synergy. Note that even no-message scoring retains finite-budget interactions.

### P1.3 Evaluate more data without promising more power

Build a SECONDARY evaluation from every positive-exposure (origin, offensive
five) in the frozen grouped data in 2016–2026, not just the qualifying common
cells. Reuse saved origin NN fits/predictions and replay existing corrected
additive snapshots with their original reference and calibration. No additive
refit, no new population-specific calibration, no new player states.

Require replay equality on original common cells before scoring the expansion.
Report unfamiliar-player handling and population coverage. If a source needed
for additive replay is absent, mark this output blocked without manufacturing
a baseline or rebuilding a cache; the primary experiment still proceeds.

Report lineup-quarter MAE/RMSE and game-lineup weighted MSE differences, with
explicit units/estimands. Show exposure bands 1–19, 20–79, >=80 and novelty.
Do not select a new floor because it gives a favorable winner. The expanded
population remains secondary and may have different difficulty/coverage.

Two required arithmetic checks:

- Subtracting the SAME league baseline from y and prediction leaves MAE/MSE
  invariant. R² changes denominator; it is not a precision improvement.
- For predictions constant within a cell, possession-level paired squared-loss
  differences aggregate to the exposure-weighted cell-mean loss difference.
  Regrouping the same observations does not conjure independent observations.
  If predictions vary within the cell, report the changed estimand explicitly.

Primary uncertainty: equal-season paired differences, SEM, Student-t 95% CI
(11 primary seasons), favorable-season count, with pooled exposure-weighted
point estimates separately. A 2,000-replicate paired game-cluster bootstrap,
seed 17, stratified within season is a secondary conditional test-sampling
diagnostic: resample whole games jointly for both models and reconstruct cell
outcomes. It does not capture model-training uncertainty or create more
independent seasons. Compare precision descriptively, not by p-value shopping.
If the full bootstrap is too costly, report that limitation; do not replace it
with an IID possession bootstrap. It is not a prerequisite to P3.

## 5. P2 — a small, honest ensemble experiment (no neural refits)

Primary constituents are corrected additive A and calibrated V9_SPREAD N.
Run three controls/candidates on exactly the frozen cells:

| ID | Prediction | Role |
|---|---|---|
| A / N | the original two predictions | unchanged controls |
| HALF | A + 0.5*(N-A) | fixed blend; no fitted weights |
| GLOBAL | A + beta_t*(N-A) | one globally shared, prior-only weight per origin |

At origin t, fit GLOBAL on matched predictions/outcomes from COMPLETED earlier
windows only (`window_stop <= origin.start`). A constituent forecast must have
been made before its own outcome window; never replace it with an in-sample
prediction from the current fitted model. Use expanding history, possession
weights, no intercept or additional recalibration:

    beta = clip(sum w*(N-A)*(y-A) / sum w*(N-A)^2, 0, 1)

Require >=30 prior cells AND >=4 completed prior origins; otherwise use .5 and
mark cold start. Use .5 if the denominator is numerically zero, with a flag.
The [0,1] bound defines the convex-blend model, not an unexplored penalty grid.
Print all weights, endpoint selections, history windows/counts and cutoff dates.
There is no novelty-conditioned switch, hidden feature model, or OOD gate.

2015 contributes warmup, not primary evaluation. Also show historical HALF
with V9_ALL as a reference, but do not optimize a weight for it or select it
over SPREAD using these results. An all-years oracle best weight may be printed
only as a clearly labeled nondeployable diagnostic, not the headline forecast.

Report ALL/novel/recurring, the same paired uncertainty, and leave-one-season-
out influence on the reported mean contrast (not on fitting future weights).
No claim of universal optimal blending or fresh-holdout confirmation.

Explain the hybrid honestly: its arithmetic ledger is a weighted combination of
two models, not a new NN event forecast. With fixed beta, the NN-only context
increment is multiplied by beta; the additive contribution has no learned
contextual mechanism. Show how much of the basketball response is retained.
Do not hide unexplained additive value in an invented shooting mechanism.

## 6. P3 — one bounded neural experiment: supervise the team total

This is a direct test of an unresolved possibility, not an assertion that the
event objective is broken. V5's points-leverage weighting changed relative
event-family weights; it did NOT test a loss on the joint team-point identity.

### Architecture and arm matrix

Everything is V9_SPREAD unless stated here: same profiles, standardized message
inputs, one mean+sd message, width 32, diagonal decoder, FT mask, opportunity
budget, five event families, row weights, and penalty definitions.

| Arm | Team-loss coefficient alpha | Execution |
|---|---:|---|
| BASE | 0 | reuse verified V9_SPREAD controls, all 48 origins |
| TEAM_01 | 0.1 | NEW primary intervention, all 48 origins |
| TEAM_1 | 1.0 | NEW dose sensitivity, all 48 origins |

No point-only model, learned scalar point head, decoder change, new input,
lambda search, seed sweep, or extra fourth arm. TEAM_01 is the predeclared main
contrast; TEAM_1 is a dose test, not a result-selected replacement winner.

### Exact loss

Grouped row g is a (game, offensive five), with n_g possessions, cached TOTAL
points S_g, and existing training decay weight h_g (not h_g*n_g twice).
Let mu_g = model.points100_g / 100 and y_g = S_g/n_g.

    L_team = sum_g h_g*n_g*(mu_g-y_g)^2 / sum_g h_g*n_g
    J = L_event + alpha * L_team / B_team
        + existing_network_penalty + existing_decoder_penalty

Use `data.g['points']` for total points; `JointData.arrays` currently does not
return it, so pass it explicitly in new code. Do not reconstruct labels solely
from located field goals and free throws: missing/unattributed events can make
that a different target. Audit and report that accounting gap, but do not
correct the source labels or train on an oracle-imputed target.

B_team is the positive weighted team MSE of the SAME untrained, seed-17
backbone on the SAME fitting-prefix reference used by all arms. Compute once
per inner/final fit and share unchanged across arms; freeze it during training
and validation. The event baselines/exposures remain exactly v9's. Fail on a
nonfinite/zero baseline; do not choose a normalizer using validation/test data.

Minibatch team numerator uses the GLOBAL fitting exposure denominator and the
same n_batches multiplier convention as the existing event loss. Verify the
full-pass mean equals the specified global objective on a fixed model. Use
float64 in the reference test; preserve the established training dtype.

This squared rate loss is a valid conditional-mean training criterion. With a
constant prediction within a group its gradients equal those of possession-
level squared error up to the common normalizer; the omitted within-group
variance is parameter-independent. It is not a generative points likelihood,
and adding it is composite supervision of overlapping outcomes, not independent
evidence. Reweighting team covariance can help or hurt event calibration.

### Temporal protocol, training, and stopping

- Reuse the exact 48-origin schedule (2015–2026), five-year fitting windows,
  inner-window choice, beginning-of-game training states and origin-frozen
  inner/outer evaluation states in `joint_capability_v3_run.split_for_origin`.
  No same-day/future state updates. Do not change update cadence today.
- Seed 17; Adam lr .001, weight decay .0001, clip norm 5; target 4096 grouped
  rows with whole-game batching; gamma .01, lambda .01, 730-day row decay.
- Maximum **48 epochs**, patience **3**, absolute min_delta **1e-5**. Keep the
  minimum finite TRAINED validation checkpoint; do not select epoch zero.
- Inner validation criterion for each arm is `L_event + alpha*L_team/B_team`,
  with UNWEIGHTED-by-recency validation exposures, no penalties. Log both
  components and raw point MSE every epoch. BASE alpha=0 reproduces v9's rule.
- Final refit starts from the same initialization, uses all permitted prefix
  rows, and runs exactly the selected epoch count. No outer early stopping.
- Alpha is fixed by arm. No selecting alpha, changing patience, raising the
  cap, or changing normalizers based on outer results. Cap hits/poor metrics
  are reported, not quality-triggered aborts. Correctness failures still stop.
- Calibrate each new trajectory with its OWN completed earlier-window native
  forecasts using the existing affine procedure. Train all four 2015 warmup
  origins; never borrow another arm's calibration history. Save native and
  calibrated metrics, and record every calibration source cutoff.

The contrast changes the training objective AND its matched epoch-selection
criterion. It does not isolate which of those two mediates a gain; state that.
Always report unchanged event losses separately from the composite criterion.

### Verification and computational budget

Before the long run: alpha=0 FULL parity at **2016q1 and 2026q4**, each with an
inner fit and final refit; deterministic parameter/checkpoint parity should
hold against saved V9_SPREAD under the same environment. Inspect any mismatch;
do not silently accept a different baseline. Also run one small two-epoch
train/validation smoke for each positive-alpha arm in a separate smoke prefix.
These are correctness/runtime checks, not effect-size screens.

Production budget: **96 new arm-origins, 192 optimizer fits**, plus the four
parity fits and two tiny smokes. No other training authorized by this plan.
Use observed smoke/parity timing to estimate wall time; historical v9 was
~2.54 hours for 288 arm-origins, only a rough guide. If the forecast exceeds
four hours for this smaller production run, report why before launch; do not
silently shrink the population. Completion means all scheduled origins, not
the point at which a favorable intermediate result appears.

Run origin-major, both arms each origin; print common-completed-origin
scorecards after every origin. A final orchestration step MUST run the reports,
fixtures, intervals, and handoff checks automatically after training; do not
leave a secondary command block that nobody launches. Stop on genuine data/
numerical corruption and save the exception and completed progress.

## 7. P4 — basketball coherence and honest uncertainty

Use the existing resolved fixture states/definitions; record their provenance.
Do not invent a current Korver state or silently substitute historical seasons.
Replay BASE, TEAM_01, TEAM_1, additive, HALF and GLOBAL after completion. GLOBAL
uses the relevant saved prior-only beta, not a fixture-specific choice.

Required panels:

- Existing Jokić/Korver/Westbrook comparison, with Murray in the supporting
  lineup. Report totals AND changes relative to the additive comparison and
  no-message ablation. Adam explicitly accepts that the original sign
  hypothesis may be wrong. No sign-fitting or favorite-player bonus.
- Five limited centers, five Goberts, five Jokićs, existing distinct-player
  high-quality and conventional/small-ball controls, and a clone ladder on the
  frozen donor panel. Use saved fixture dates and slots, not name guesses.
- Report available creation/attempt/mix/conversion/turnover quantities and
  calibration contribution. Mark defensive coverage and rebound facilitation
  as unmodeled here; do not fabricate mechanisms to satisfy the prose contract.
- Permutation invariance, receiver FT-conversion isolation after learning,
  opportunity conservation, finite probabilities, exact points reconstruction,
  and true all-message-off restoration. These are correctness tests. A fixture
  direction or magnitude that disappoints is an experimental finding, not an
  assertion that kills a completed sweep.

Show whether an accuracy gain materially weakens the learned extreme-lineup
response, especially in blends. Neither a high absolute score nor a negative
context increment alone proves the whole lineup prediction is coherent.

For each new mean forecast (including HALF/GLOBAL), run one simple matched
finite-batch interval benchmark on the primary cells: from prior completed
windows, take the unweighted higher empirical quantiles at .80 and .95 of
`abs(actual-prediction)*sqrt(possessions)`; divide by sqrt(current possessions).
Use >=200 prior cells and >=4 prior origins, else report interval unavailable.
Use the same eligible history keys across arms and forecasts that were genuinely
prequential at their own origins. No tuning distance functions or quantiles.

Report cell-weighted coverage (matching the calibration estimand), possession-
weighted coverage as secondary, mean width and interval score, broken out by
novelty, exposure, and existing composition-distance bins. Freeze distance-bin
edges using prior data, not future residuals. This is empirical observed-lineup
forecast coverage, not a distribution-free temporal guarantee or an interval
for a synthetic lineup's latent mean. Do not extrapolate sqrt(n) to claim
certainty with infinite possessions. Ensemble disagreement is sensitivity,
not automatically a calibrated posterior SD. OOD mean uncertainty stays OPEN.

## 8. Output, logging, and handoff contract

Suggested fresh root: `experiments/cache/joint_capability_2026_09_12_v10/`.
If occupied, use a new explicit suffix before beginning. Keep smoke outputs
separate. New code can use `joint_capability_v10_*` names; share pure helpers
where safe without changing historical experiment behavior.

Required artifacts under the new root (equivalent names allowed if indexed):

- `protocol.json`, source/code hash manifest, run status, exact commands and
  receipts; explicit reused-control references, not fabricated new completions.
- Reconciled primary/descriptive scorecards; per-origin/per-season metrics and
  paired comparisons; common keys and coverage/missingness receipts.
- Event/point transfer components and loss-contribution tables; additive-gap
  strata; 12-case narrative plus machine-readable player contributions.
- Expanded-population report, or exact source blocker; bootstrap report or
  explicit runtime limitation. Neither silently replaces the primary target.
- Prequential blend forecasts/weights/source windows and their scorecards.
- All new checkpoints, inner curves, raw/composite validation values, epoch
  decisions, group/player forecasts, cell predictions and calibrations.
- Fixture outputs, interval forecasts/calibration sources, integrity checks.
- `reports/joint_capability_v10_review.md` and
  `reports/joint_capability_v10_handoff.md` at repository level.

Durable training log must show: origin/arm/stage; train/validation cutoff dates;
epochs current/cap/best; event, team, composite and penalty losses; gradients;
elapsed time; origin and common-cumulative MAE/RMSE/r² against additive, BASE,
HALF, and each completed new arm; ALL and novel exposures. Print `warmup` or
`unavailable` with a reason, not misleading 0/nan scorecards. Print final
calibration weights and flags. Flush output. No polling loop that consumes an
agent turn just to watch unchanged training output.

Provide tested background-launch, `tail -f` live-log, status, and safe resume
commands before the long run. Use durable PID/status/exit receipts and an
atomic final success marker written ONLY after training and required reports
finish. Verify gzip magic bytes, not just filename suffixes, for every new
compressed artifact; write compression explicitly when using temporary names.
Test reporting and resume paths on smoke data; do not launch full training just
to test the launcher. Ask Adam to launch/authorize launch, then stand down.

After completion update MODEL_SCORECARD.md and prepend a SESSION_HANDOFF.md
checkpoint linking the new review and remaining work. Add a concise BACKLOG
entry distinguishing tested-null, uncertain, and genuinely untested routes.
Do not rewrite historical claims in place. The handoff must state:

1. Exact completed/reused counts, population, commands/logs, and source hashes.
2. Quantitative answers to the three questions, including effect uncertainty.
3. Counterfactual and interval results beside predictive gains, with omissions.
4. Any defect, protocol deviation, cap hit, blocked output or incomplete run.
5. Exactly one recommended next experiment and why the evidence motivates it.
6. Clean/dirty tree status, uncommitted paths, and that Sol has stopped editing.

Success is not necessarily a new winning model. A trustworthy blend, an exact
explanation of the event/points disconnect, and a completed bounded test are
useful outcomes even if TEAM_01 loses. Do not describe an unlaunched or partial
run as complete, and do not claim an entire modeling class is impossible.

## 9. Holistic roadmap after this bounded day (NOT authorized experiments)

| Priority | Direction | Why still promising / what would distinguish the next test |
|---|---|---|
| Next candidate | Separate individual value from contextual response | If the blend keeps helping, investigate a cross-fitted, shrunk individual-value residual with an explicitly retained NN context path. Not known-pair chemistry; do not simply add two overlapping ratings. Quantify whether ordinary blending suppresses useful context first. |
| Next candidate | Dated creation/off-ball tracking inputs | Potential assists, touches, catch-and-shoot/pull-up and role descriptors can distinguish self-creation from assisted finishing. Full-season cached aggregates cannot describe an earlier quarter of that same season. A future authorized pilot needs DateTo snapshots or strictly previous-season features, robust identity joins, missingness control, and a matched no-tracking arm. Investigate the recorded 2024–25 definition breaks. |
| Next candidate | Opponent-conditioned offense / actual two-team model | v5 corrected historical schedule in player profiles; it did not model the opposing five's current capabilities and assignments. Start with a shared prior-only opponent control on both models, then one explicit interaction. No unrestricted off×def ID block. |
| Next candidate | Role-state adaptation, then learned flexibility | Shortening training-row half-life failed; that does not test faster role-state updating, partial pooling after a role change, or separating skill from historical teammate context. These require a separately authorized state experiment, not a hidden cache rebuild. |
| Open, evidence-led | Joint capability combinations beyond marginal spread | Mean+sd still loses which skills coexist in the SAME sender. A small predeclared cross-capability summary (e.g. creation together with shooting) tests different information from width/depth/minmax. Size conditional information and mechanism need before designing an arm; orthogonality alone is not predictive value. |
| Required product research | OOD/latent-mean uncertainty | Population-holdout disagreement and distance are useful stress tests, not validated extreme-lineup coverage. Future work should propagate state/response uncertainty and measure real support-shift coverage with matched controls. No distance multiplier dressed up as data-proved certainty. |
| Required mechanism research | Rebounds and possession renewal | Adding an ORB coordinate is not a physical miss/recovery/extra-attempt loop, nor Adams-style teammate facilitation. Retain the earlier negative point results; pursue a bounded mechanism for basketball value, not an assumed large accuracy prize. |
| Later | Defensive mechanisms, injuries/thin histories, user explanations and two-team UI | Necessary for the full product, but not smuggled into this day's offense experiment. Injured/missing is not zero ability; no health prognosis from box scores. |

Do not make success on pair-effect prediction a prerequisite to testing
individual tracking descriptors in this NN. Pair-passing data may be useful
measurement, but turning it into known-pair bonuses conflicts with the primary
model contract and does not solve novel-pair transport.

Do not rerun the same raw-feature bundle, extremity trim, row-decay factorial,
width/penalty sweep, or depth/minmax/rank experiment without a changed hypothesis
and an explicit new plan. Conversely, their results do not establish that all
features, all architectures, recency, defense or conversion are dead ends.
