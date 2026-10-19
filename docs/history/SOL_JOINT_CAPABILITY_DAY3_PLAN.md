# Day 3: what teammate representation does the model actually need?

Written by Codex/Astra on 2026-09-10 after independent review of the complete v3
run and `CLAUDE_MODEL_FEEDBACK_3.md`. Read
`reports/joint_capability_v3_codex_review.md` for the evidence behind the design.

**Status: prospective implementation/experiment contract, not a launched run.**
This becomes an execution task when Adam asks Sol to implement it. It does not
authorize modifying completed results or changing this protocol after seeing
its results. Codex has finished editing; establish sole editing ownership first.

## 0. The deliverable and the boundaries

Answer one architectural question with a complete rolling-origin experiment:

> Does the model need nonlinear messages from each teammate separately, or is a
> receiver-dependent response to their collective capability profile sufficient?

At the same time, measure whether the learned own-state encoder adds anything
over anchored profiles, **with regularization held fixed**. Deliver real point
scores, event scores, basketball explanations, and a qualified uncertainty
comparison. Do not turn this into an infrastructure project or an architecture
search. The complete experiment, not an extra test-count milestone, is the
principal outcome.

Priority order:

1. Preserve/reproduce the v3 controls and establish the pooling variants.
2. Complete the common-lambda 2×3 comparison across all 48 origins.
3. Finish its event, point, basketball, and interval readout.
4. Complete the two-arm low-lambda sensitivity, then optional bounded seeds.
5. Write the documented handoff and recommend exactly one next research step.

Constraints:

- No delegation, Opus worker, other editing session, or additional agents.
- No scraping, database access/mutation, source-cache or v3 derived-input
  rebuild, scorer/page promotion, deployment, or git commit.
- Every completed `experiments/cache/` run stays untouched, including v3's
  diagnostics and reports. Preserve all feedback and earlier plans verbatim.
- No raw player-ID parameters, known-pair coefficients, named-player bonuses,
  coverage gate, forced Korver/Westbrook ranking, or synthetic-outcome training.
- Retain all three co-equal standards in `CONTEXTUAL_MODEL.md` §2. A modest
  predictive cost may be worthwhile for coherence or uncertainty, but print it.
- Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u` and durable logs
  for every numerical command, test run, and training job.

## 1. Starting evidence: read and reuse, do not refit to rediscover it

Frozen v3 root: `experiments/cache/joint_capability_2026_09_09_v3/`.
Independent review artifacts: `experiments/cache/joint_capability_v3_review_2026_09_10/`.

- 240 completed v3 arm-origins; five arms × 48 quarters. Primary scoring is
  2016–2026, **44 quarters**, with four 2015 quarters for calibration warmup.
- Every primary arm: 5,607 cells / 726,364 possessions. Novel: 2,073 / 226,256.
- H2/H3/additive MAE: 8.122802 / 8.122903 / 8.091953.
  RMSE: 10.876790 / 10.870128 / 10.840994.
  Raw r²: .114614 / .115698 / .120432.
- H3–H3F season-average RMSE -.052315 ± .020334 SEM (9/11 favorable).
  H3–H2 -.005838 ± .045960. These are not equivalent statistical claims.
- H3 improves proper FG Brier over H3F by -.00005603 ± .00001300 SEM across
  seasons, favorable 10/11. Conversion is not a demonstrated null.
- Saved H2 already gives the useful center/clone directions: native limited
  centers 105.662, five Goberts 116.370, five Jokics 133.115. Do not rerun a
  separate H2 training experiment to obtain its fixtures.
- Existing H3/H3F use network lambda .0001/.01; common decoder gamma is .01.
  H3's boundary flag is historical evidence and remains unchanged.

These historical outcomes have already informed model development. The new
selection/execution protocol is prospective, but the historical evaluation
sample is **not a newly untouched holdout**. Say so in the final report.

## 2. Architectural specification

For player i, let b_i be the existing dated 18-coordinate anchored state and x_i
the existing 64 inputs, standardized exactly as in v3. Let e denote the encoder
switch, and h_i = b_i when e=0, or b_i + E(x_i) when e=1.

Three context modes:

    F (fixed): c_i = M(h_i, r_training)
    M (mean):  c_i = M(h_i, (sum_j h_j - h_i) / 4)
    P (pair):  c_i = sum_{j != i} M(h_i, h_j) / 4

All use z_i = h_i + c_i, the same 36→32→18 tanh message M, zero-initialized
final layers, the same FT-conversion message mask at coordinate 15, the same
decoder and opportunity conservation. The encoder remains 64→32→18 tanh.
`r_training` remains the v3 decayed-possession-weighted **baseline** reference
from the fitting prefix, frozen within that fit; it is not recomputed with the
encoder or current lineup. All state/exposure/reference rules are unchanged.

M excludes the receiver's own slot, not all slots with the same identity. Four
identical copies are still four senders. Average in anchored/encoded STATE
coordinates, not after converting logits to probabilities. Do not silently
change the averaging space.

F/M/P with the same encoder switch have exactly the same parameter shapes and
initial parameter draws at a given seed. No extra layers, learned pooling,
attention, extra moments, standardization, message residual centering, or
new features today. Sharing the decoder implementation is mandatory.

Interpretation rules:

- M is a nonlinear contextual model, not an additive player-value mean.
- P−M measures the usefulness of preserving separate sender states through the
  message nonlinearity. It does not test known-pair chemistry or causal identity.
- M and P are not generally nested function classes at fixed width. With an
  encoder, even mean(h) can contain nonlinear summaries of original features.
- F still sees the real five in the finite opportunity allocator and in its
  receivers; it removes sender information only from the message path.
- Equal raw parameter count is a useful control, not equal effective function
  complexity; a constant sender changes the effective function class.

## 3. Exact experiment matrix: reuse three existing arms, fit six new ones

Use explicit names carrying encoder/mode/lambda, not an ambiguous new "H3".
Common gamma_decoder=.01, primary seed=17.

### 3.1 Primary matrix, lambda_network=.01 everywhere

| Arm | Encoder | Context | Source |
|---|---|---|---|
| E0F_L2 | off | fixed | NEW, 48 origins |
| E0M_L2 | off | mean | NEW, 48 origins |
| E0P_L2 | off | pair | verified v3 H2 |
| E1F_L2 | on | fixed | verified v3 H3F |
| E1M_L2 | on | mean | NEW, 48 origins |
| E1P_L2 | on | pair | NEW, 48 origins |

L2 denotes 10^-2, not a change in penalty definition. This common value was an
interior v3 development choice for H2 and H3F. It is a fixed diagnostic
regularization level, **not a newly optimized/deployable global hyperparameter**.

Four new trajectories × 48 origins × (inner fit + final refit) = **384 fits**.

### 3.2 Secondary matched low-lambda comparison, lambda_network=.0001

| Arm | Encoder | Context | Source |
|---|---|---|---|
| E1F_L4 | on | fixed | NEW, 48 origins |
| E1M_L4 | on | mean | NEW, 48 origins |
| E1P_L4 | on | pair | verified v3 H3 |

Two new trajectories = **192 fits**. This addresses v3's candidate/control
lambda difference and tests whether the pooling conclusion depends on it.
No E0 low-lambda grid today. No new gamma selection, development grid, or
post-result extension. Preserve .0001's original boundary caveat.

The intended core cost is **576 new optimizer fits**, not 576 epochs.
Train all 48 origins for EVERY new arm: skipping 2015 would change its prior-only
point calibration. Never splice a new arm onto another arm's warmup history.

### 3.3 Mandatory contrasts

Primary: E0P−E0M and E1P−E1M (pair versus mean); E0M−E0F and E1M−E1F (real
mean versus fixed); encoder-on minus encoder-off within each context mode.
Also show pair−fixed in each encoder branch and the encoder×(pair−mean)
difference of metric differences. Keep that factorial statistic separate from
per-cell prediction interactions.

Secondary: E1P_L4−E1M_L4, E1M_L4−E1F_L4, E1P_L4−E1F_L4, and L4−L2 within
each E1 mode. No cherry-picked lambda headline. Compare every new arm with
corrected additive, location+shooting, and its relevant frozen v3 parent.

## 4. What is frozen and what can be repaired without contaminating this test

Consume v3's existing `derived/game_lineups.npz` and
`derived/player_game_states_v3.npz` read-only. Hash and reference them; do not
call any `build_*` helper or copy-and-rebuild state files. Missing required input
is a blocker to report, not permission to rebuild it. New train-prefix
normalizers, fit files, predictions and report tables belong under the NEW run.

Freeze v3's actual training semantics, including all five supervised families,
730-day example weighting, decoder/network penalties, pooling of training
exposures, historical-state dates, input standardization, U, and batch schedule.
Do not simultaneously repair/reweight the objective, remove assisted supervision,
add shot-quality coefficients, normalize messages, or change recency.

Explicit objective-documentation amendment: the implemented v3 count family is

    sum_channel weighted_NLL_numerator / sum_channel eligible_weighted_possessions

not the sum of three separately normalized per-channel losses described in
Day2 §3.1. Retain the IMPLEMENTED formula and its baseline normalization for this
architecture experiment; record all three component numerators/denominators as
new diagnostics. If masks are identical, baseline scaling cancels the factor of
three; unequal masks need not give identical effective weighting. This is a
disclosed deferred objective question, not a silent correction or a claim that
Day2's text was implemented exactly.

Allowed derived-report repairs, applied identically to saved and new arms:

- Proper per-attempt Brier via `M*(1-p)^2 + (A-M)*p^2`; retain the original
  grouped-fraction squared-error column under its accurate name.
- Actual common keys, native/calibrated/within-quarter metrics, exposure slices,
  event denominators and all season contrasts, which v3 did not fully deliver.
- Broad actual-versus-predicted channel biases over all qualifying cells, not
  unweighted means of predictions over all groups.
- Single authoritative support-column mapping. Verify duplicate v3 `_x/_y`
  fields instead of assuming they agree; never mutate the saved files.
- Honest exposure, staleness, fixture source-date and uncertainty labels.

A material defect in the training/scoring code discovered during the parity
check is different: preserve evidence, stop the affected experiment, explain
which controls cannot be reused, and request a revised scope. Do not silently
rerun every control on a changed model.

## 5. Implementation shape, parity, and stopping

Keep v3 scientific files unchanged. Prefer a small versioned v4 model adapter
and driver importing frozen pure helpers. Do not monkeypatch module globals,
patch ARMS at runtime, or duplicate the point decoder for the mean arm. If a
training-loop copy is necessary to inject a model factory, keep the changes
small and verify it against v3. Suggested new modules:

- `experiments/joint_capability_v4_model.py`: encoder/context mode and one
  shared inference path;
- `experiments/joint_capability_v4_fit.py`: versioned fit factory/adapter;
- `experiments/joint_capability_v4_run.py`: immutable aliases, new trajectories,
  progress, fit-start accounting and resume;
- `experiments/joint_capability_v4_diagnostics.py`: read-only old-run adapter,
  new common reports and controls;
- `experiments/run_joint_capability_v4.sh` and focused tests.

Exact training policy: Adam lr=.001, weight_decay=.0001, gradient clip=5,
complete-game target batches=4096 rows, seed=17. **Maximum 24 epochs, patience 3,
minimum patience-reference improvement 1e-5.** Select the lowest finite validation
checkpoint actually trained, even if a smaller improvement did not reset patience.
Log epoch zero for comparison but retain v3's trained-checkpoint policy.

For each outer quarter T: inner training ends at the preceding completed
quarter's START, validates on that whole prior quarter with states frozen at its
start, and uses its own five-year history. Reinitialize the final model at the
same seed and fit exactly the selected epoch count on the five-year prefix before
T. Outer outcomes never select epochs, lambdas, loss scales, or thresholds.
Arm-specific early stopping remains allowed: the estimand compares the same
learning procedure, not fixed identical epoch counts. Report selected epochs and
cap hits; do not extend 24 epochs after looking at primary results.

Parity before the full run:

1. Load existing H2/H3/H3F weights through the v4 equivalent mode and reproduce
   saved native scores, per-player tensors and losses on a fixed small set of
   stored groups plus fixtures. No training required.
2. Refit only **H2-equivalent 2016q1** and **H3F-equivalent 2019q1**, with original
   seed/lambda, as two bridge checks (four optimizer fits). Require identical
   selected epochs and outer native predictions within 1e-4 points/100, with
   family losses within 1e-7. Log exact maximum differences and environment.
   These bridge outputs are audits, not replacements for original references.
3. If numerical tolerance fails, inspect the changed implementation and data
   before proceeding. Do not loosen tolerance merely to admit the new driver.

Start the real matrix after these focused checks pass. Do not accumulate another
large test-only phase or do repeated partial primary-origin pilots.

## 6. Required result package

### 6.1 Point forecasting, population, and attribution

Pin exact v3 keys, targets, possession weights, schedule, novelty flags, league
levels and comparison cohorts. Require one-to-one joins and exact population
reproduction; never silently intersect away a difficult cell. Use each new
arm's OWN expanding completed-window calibrator, minimum 30 historical cells
and existing cold-start rule. Persist every calibration source-window list.

Report native AND calibrated MAE, RMSE, signed bias, raw r² and clearly labeled
possession-weighted correlation. Report all and novel, each season and quarter,
and <100 / 100–200 / 200–400 / 400+ possession bins with explicit nonoverlapping
boundaries ([0,100), [100,200), [200,400), [400,infinity)). Preserve empty slices
as count=0 and NA, not a fake score of zero.

Within-quarter diagnostic: subtract each origin's actual weighted mean from
both prediction and actual (preserves prediction bias). If additionally removing
each prediction's own origin mean, label that as a different bias-removed
diagnostic. Neither may become the deployable league reference.

For mandatory contrasts report equal-season mean, SEM, 95% t interval, favorable
seasons, and 2,000 season-block bootstrap draws, seed=20260910. Use the actual
number of paired seasons. Quarters, individual shots, and random seeds are not
independent uncertainty units. Show all predefined contrasts, including losses.

### 6.2 Event prediction and how it becomes points

For each arm/origin save sufficient numerators, denominators, labels, masks and
predictions to reconstruct:

- FGA/FTA/TO counts and 3PA rate, actual/predicted/bias per 100;
- six-location CE and true per-attempt FG/FT Brier/NLL with calibration bins;
- assisted conditional loss, player shot allocation and team totals;
- native point conversion from the very same player-level predictions.

Provide full eligible-event and common-cell-restricted tables. Common-cell
restriction is by exact offensive-five/quarter membership, not arbitrary row
position. For assisted player-game labels, either use directly attributable
labels or restrict to player-games whose required groups are all within the
restriction. Do not attach a whole-game assisted count to a partial game's
common-cell groups. Print its separate eligible exposure and losses; do not
pretend a restricted assisted loss has the full-shot cohort.

Add a saved-prediction **point-transfer diagnostic** for P versus M and M versus F
in both primary encoder branches, and original H3 versus H3F. Starting from one
arm's native ledger, substitute opportunities, location and conversion from the
other in a fixed path and its reverse. Report team-total and player changes,
spread and signed bias of each contribution, with exact reconciliation. U is
identical here; budget contribution is explicitly zero. The hybrid ledgers are
diagnostic arithmetic, NOT newly calibrated forecast arms or extra optimizer
targets. Report correlations/residual associations descriptively; do not fit an
outer-data coefficient and call it a performance improvement.

This is how we test "event gains do not reach points". Do not infer it by
dividing a Brier change by total irreducible make/miss noise, or by assuming
assisted supervision cannot influence shared point-bearing parameters.

### 6.3 Basketball: same fixtures, all relevant models

Use the frozen v3 fixtures and the documented deterministic prior-highest-
exposure real lineup. Carry the same all-five IDs, source dates and assumptions.
Include all six primary arms; H0/H1 and the low-lambda E1 comparisons remain
reference/sensitivity columns. Use 2026q4, 2025q4, 2021q4 and 2016q4 fits as
appropriate; do not score an older fixture with a later model inadvertently.

For each fixture print native and calibrated ORtg separately, exact five-player
opportunity/location/make/FT ledgers, additive swap comparison, per-player
coordinate exposures, last-seen dates and model-mode sensitivity. Use float64
saved-weight inference; ledger and path errors <=1e-8 points/100, float32 parity
<=1e-4. Reproduce permutation, batch/singleton and duplicate-slot behavior.

Print each fixture's context correction relative to real-cell q50/q90/q99/max
for the SAME arm contrast and origin where available. A directionally sensible
OOD mean is useful but not validated. Include real small-ball units so a model
cannot win the qualitative review simply by depressing every unusual lineup.

The old mixed-era Korver override uses a beginning-of-game state dated
2015-05-22; it is not an exact post-season state immediately before July 1.
Keep it under that explicit actual-state label, or mark exact July-1 evaluation
deferred. Do not rebuild historical inputs for this ablation. An additive
comparator with current Korver state is not matched to that historical override;
label it unmatched rather than implying the original additive number used the
same state. The ordinary current-state swap remains directly comparable.

Hypotheses remain fallible. Do not optimize for Korver, Westbrook, Haliburton,
Adams, Robinson or any other named example. Report total swap, relative-to-
additive swap, and within-NN context contrasts as different estimands.

### 6.4 Failures: informative, not selected proof

Primary failure population is seasons 2016–2026 only, >=200 possessions AND
>=5 games. First report possession-weighted actual/predicted channel biases
over ALL qualifiers. Then report top-ten weighted squared-error disadvantages
for each pair-versus-mean branch, and new-arm versus additive, with names,
predictions, additive player coefficients and exact NN player ledgers. Preserve
the existing H3 failure tables as historical, including their 2015 contamination.

Give chronological halves with the original unchanged forecast. Add a separate
selection-on-first-half-only diagnostic: among the same exposure/game-qualified
cells, rank by first-half weighted squared-error disadvantage (first half must
have >=100 possessions and >=2 games), then show second-half disadvantage and
residual sign. Do not select cases using full-window errors for that diagnostic.
Future exposure eligibility and our previous inspection of these data still
limit its interpretation; it is stronger than reusing both halves to select,
not an untouched confirmatory test. Fewer than ten eligible cases is a result,
not a reason to relax filters. Finish with at most three quantified patterns.

### 6.5 Uncertainty: isolate what the existing interval improvement means

Do not design a new OOD distance to make clones look far today. First independently
replay v3's saved empirical radii from original cells in a new output directory,
including source-window eligibility, quantile definition, split, floor and bins.
Report any discrepancy rather than overwriting originals.

For every primary arm plus additive compare three finite-outcome methods on
identical eligible cells at 50/80/95%:

1. Existing prior-only exposure-bin empirical intervals.
2. **Constant-scale control:** identical older/newer completed-window split and
   1/sqrt(n) scaling as the composition method, but use a constant older-half
   scale `mean(abs(error)*sqrt(n))`, floored at 1e-6. Calibrate the same higher
   quantile of normalized residuals on the newer half. The constant cancels in
   the final radius; it is equivalent to a newer-half quantile of |error|sqrt(n).
3. Existing nondecreasing isotonic distance scale, fitted to the older half,
   quantile calibrated on the newer half, with the unchanged floor and constant
   tail extrapolation. Use the fixed v3 baseline composition distance; do not
   substitute encoder outputs whose geometry differs between arms.

For methods 2/3 require >=200 cells in each chronological half of completed
prior windows. Emit explicit exposure-method fallback rows otherwise, and show
both all-available and identical non-fallback comparisons. Current-window
outcomes must never enter any radius fit. Save stable cell keys, actual/predicted
values, every source-window list, isotonic knots, residual quantiles and fallback
reason so every radius is independently reproducible.

Report cell- and possession-weighted coverage, mean width, distance from nominal,
and interval score: width + (2/alpha)*outside-distance, where alpha=1-nominal.
Give season-paired interval-score contrasts and prefix-defined support slices.
Near-nominal flat coverage across distance is desirable, not a failed ordering.
Wider intervals alone are not a success. These are finite observed-quarter
outcome intervals conditional on n, not latent-mean guarantees.

For synthetic fixtures give numerical forecasts, per-coordinate thinness,
staleness, fixed-distance reference quantiles and cross-model sensitivity; do
not manufacture a calibrated latent-mean band from cross-arm spread. Keep the
>2 role-stress slice for comparability and report its zero count. Add raw role
share changes and denominator distributions, explaining that historical SD
includes noisy short game-lineup outcomes. New de-noised role support or
Mahalanobis/neighborhood intervals require a subsequent specified experiment.

## 7. Bounded optional work after the complete main results

### Seed check, not model/epoch selection

If numerical budget remains, run primary E0M/E0P/E1M/E1P at seed 29 for the fixed
origins 2016q1 and 2026q1 (at most 16 fits). Reuse an exactly matching existing
seed control if its full metadata, arrays and hashes establish equivalence.
Optionally add 2026q4 for these same four arms (eight fits) for the current
fixtures. No seed 43 extension today. Use each seed's own inner stopping.
Report native/event/fixture sensitivity; do not invent calibrated point metrics
from a seed with no complete prior forecast trajectory or choose a best seed.

### Opponent diagnostic, saved-only and secondary

If time remains, inspect `onfloor_opponent_cells.csv.gz` and its provenance for
a one-to-one matching, already computed opponent adjustment. If usable, join it
to the common cohort and show the same fixed adjustment for all forecasts at
coefficient 1, with the original raw-target headline retained. Verify the sign
convention: a defense that lowers expected observed offense lowers the forecast
against that defense. No fresh defensive fit, database load, or cache rebuild.

Label this conditional on the defenses ACTUALLY faced in the future quarter,
not a quarter-start forecast of an unknown rotation/schedule. Equal adjustment
to all arms does not guarantee unchanged relative errors. If cached provenance
or population does not match, defer it explicitly; do not expand the experiment.
Do not add it to the mean-arm training or use it to select the winner.

## 8. Focused tests that must precede interpreting the experiment

Use existing tests where applicable. A repository-wide pass count does not show
these properties; link each to a specific test or real-data audit.

1. P reproduces v3 and F reproduces v3 H3F where applicable; reference mappings
   and saved-model reload work in float64 and float32.
2. M excludes the own SLOT; slot permutation preserves the team score and
   permutes player outputs, including repeated identical players.
3. For four identical sender states, P and M agree at identical weights.
   For an affine M they agree generally; for a chosen nonlinear M construct a
   same-mean/different-distribution example that separates P from M at the
   message level. Do not assert a full-score invariance when other recipients
   or the opportunity denominator changed.
4. Zero messages/encoders nest exactly with a shared decoder. Output shapes,
   probability normalization, opportunity conservation, point identity and the
   FT-conversion mask hold for every mode.
5. Every epoch/selection/reference/normalizer/calibrator respects its cutoff;
   mutating later outcomes cannot alter a prior fit input, epoch choice or
   prediction. Tests must check selector inputs, not just fit masks.
6. Global family evaluation is batch-invariant, with missing-channel and
   zero-exposure cases; fixed-parameter batch-gradient averaging reproduces the
   declared full-data objective. Test the IMPLEMENTED count formula explicitly.
7. Proper grouped-count Brier matches expansion into Bernoulli attempts, and
   its model difference equals the original grouped-fraction-loss difference.
8. New point histories use the new arm's 2015 warmup, never an aliased control's
   history. Restricted event/assisted cohorts cannot borrow excluded outcomes.
9. Constant-scale and isotonic intervals use disjoint prior windows, have exact
   quantile/fallback behavior and reproducible radii; interval-score arithmetic
   matches a hand-computed inside/outside case.
10. Resume skips complete results without changing file bytes, detects source or
    protocol drift, records a failed fit start, rejects incomplete aliases, and
    handles warmup displays and empty metric slices honestly.

Run the full suite once before handoff. Stop on a real leakage/accounting defect;
do not stop a healthy full experiment merely because an early origin loses.

## 9. Budget, durable output, and launch interface

Fresh numerical allowance, activated only by Adam's implementation request:
**640 optimizer-fit starts and 6 hours of measured active numerical-command
wall time**, including checks, retries, diagnostics and training. A killed or
failed optimizer invocation consumes a fit start. Record analytical calibration/
isotonic calls separately; they are not NN optimizer fits. Full-run core=576,
bridges=4, at most four fitting smokes/tests=4, optional seed fits<=24: planned
ceiling 608, with at most 32 starts reserved for disclosed debugging/retries.
This is a ceiling, not a target. Do not spend remaining budget on another sweep.

Complete all primary origins before secondary trajectories. Estimate remaining
time from measured medians and reserve at least 30 minutes for reports/handoff.
If the cap prevents completion, stop at a durable boundary, mark unfinished arms
and required outputs honestly, and give an exact resume command. Do not label a
partial trajectory comparable or mark the whole task complete.

Proposed run prefix: `experiments/cache/joint_capability_2026_09_10_v4/` (choose
a new suffix if it already exists with incompatible contents). Do not initialize
or overwrite anything under v3. Save:

- frozen protocol, plan hash, dependency/source hashes including diagnostics,
  input hashes, environment and git/dirty-state provenance;
- read-only alias registry with old source paths/hashes, source arm/lambda/seed,
  exact population and calibration lineage; distinguish reused from fitted;
- append-only `fit_ledger.jsonl` with start BEFORE optimizer creation and explicit
  completion/failure, origin/arm/seed/stage/cutoffs and elapsed time;
- separate inner/final curves, selected epoch/stop reason, fit metadata, model,
  baseline scales, per-head exposure statistics and parameter/output penalties;
- per-origin cell/group/player predictions, calibrated scores, point-transfer
  and fixture ledgers, interval-source details, report tables and completion map.

Fingerprint every executed scientific dependency before a stage starts,
including control/diagnostic modules, not only the training model. Never update
a frozen hash just to make resume accept edited code. Use a new derived-report
prefix for a later reporting fix, or a new study for a scientific change.

Implement CLI stages `audit`, `run-primary`, `report-primary`, `run-secondary`,
`controls`, `report`, `status`, and a resumable `pipeline`. A suggested sequence:

    audit -> run-primary -> report-primary -> run-secondary -> report

Keep optional controls explicit; do not let a completed report launch them.
Status must not initialize or modify a run. Give Adam a summary with completed
new/reused origins, fit starts, elapsed time, current stage and log location.

The launcher must run unbuffered, durable unique logs, capture exit status even
through tee, write the real PID, survive detachment, and refuse a concurrent
editing/training launch into the same run. At each epoch print train/inner-val
total and family losses, epoch number/max, best epoch, patience state and ETA.
At each origin print cutoff, lambda/gamma, selected epochs, cohort sizes, and
quantitative MAE/RMSE/r² differences versus additive and the relevant P/M/F arm.
After each completed origin update cumulative PRIMARY all/novel metrics. During
2015 print "calibration warmup; primary sample not started" instead of zero/nan
scorecards. If a comparator is not yet fitted, say pending, not zero.

**When the long run is ready, give verified background-launch, live-log and
status commands.** Verify them with a tiny bounded fixture/smoke, not by claiming
an unbuilt command works. Do not launch the full training job until Adam chooses
to run it or asks you to launch it. If asked to launch and stand down, start it,
verify PID and the first real progress lines, then hand back without polling away
the usage window. Logs/status must make progress understandable without an agent.

## 10. Decision rules and final handoff

The primary hypotheses concern representation, not beating additive at any cost.
Report point/event effects and the two other pillars before recommending a
backbone. Use 0.05 points/100 MAE/RMSE as a predeclared **practical reporting
margin**, not a statistical equivalence claim. A wide interval spanning that
margin is inconclusive even when point estimates nearly tie.

- M matches P's useful event/point behavior and preserves the coherent fixtures:
  prefer mean pooling provisionally for simpler computation and interpretation.
  Keep P as a reference; do not call the context effect additive or causal.
- P adds consistent material gains: retain sender-resolved messages and identify
  the benefiting channels/distributions. No known-pair chemistry claim follows.
- Encoder benefit remains small/uncertain without a clear coherence advantage:
  prefer E0 as the simpler research default, explicitly a pragmatic decision,
  not proof that learned player-state correction can never help.
- Context gains disappear at matched lambda: report that; distinguish it from
  the valid v3 tuned-system result and retain both sets of evidence.
- Point gains and coherence disagree: show the trade and leave the final
  product decision open. Do not select the lowest five-center score as a winner.
- No variant advances the model: record the null and recommend the strongest
  diagnostic-led next step, not another unbounded hidden-width/seed search.

Write `reports/joint_capability_v4_review.md`, update `MODEL_SCORECARD.md`, prepend
the checkpoint to `SESSION_HANDOFF.md`, and update the top of
`MODEL_RESEARCH_ROADMAP.md`. Keep historical entries, old protocols and feedback
intact. The completion record must distinguish completed fitting from unfinished
required diagnostics; tests passing is not experiment completion.

The final handoff must include: every arm's source/fit status; exact counts;
all/novel point table; mandatory paired contrasts; event and point-transfer
findings; basketball successes/failures; interval-score/coverage comparison and
remaining latent/OOD gap; selected epoch/cap-hit summaries; actual fit/time budget;
verification commands/results; absolute log/artifact paths; any known mismatch
or deferred output; current process/editor status; exact resume commands if
needed; and **one** recommended next experiment with the evidence motivating it.

Preserve later architectural options without implementing them here: message
input standardization; assisted-loss ablation; points-leverage weighting (which
needs a specified scale, not just decoder derivatives); prior-only measured
shot-quality sender coordinates; explicit creator/finisher responsibility;
opponent conditioning; rebound-dependent opportunities; de-noised role support
and latent-mean uncertainty. One controlled change at a time.

### Suggested request for Adam

> Read SOL_JOINT_CAPABILITY_DAY3_PLAN.md and implement it, including its bounded
> experiment and derived outputs. Preserve all original artifacts, do not
> delegate, and use durable verbose logs. Give me verified background commands
> when the long run is ready; finish with the documented handoff after it runs.
