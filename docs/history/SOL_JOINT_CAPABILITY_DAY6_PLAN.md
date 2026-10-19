# Day6 / v12: train the additive-anchored hybrid

Codex/Astra, 2026-09-13. Read AGENTS.md and its required context, then
`reports/joint_capability_v11_codex_review.md` and this entire plan.

## 1. Objective, authority and priorities

Test whether training neural weights **against the combined additive-plus-neural
forecast** improves on frozen recombination, and whether a separate learned
profile-value correction helps. Day5 did not test adaptation. Adam explicitly
welcomes warranted refits; avoiding training is not a research objective.

Priority order:

1. Close the bounded Day5 audit gaps below without rerunning Day5 production.
2. Implement the two precisely defined trainable hybrids and their frozen controls.
3. Verify causal additive training offsets, algebra, gradients and matched inputs.
4. Run the two prescribed pilots, document measured cost, and provide verified
   background-launch/live-log/status commands. Wait for Adam to authorize full run.
5. After launch, complete the entire frozen experiment and automatic analyses.
6. Write a scientific review and operational handoff, explicitly checking every
   deliverable. A successful process is not proof the plan is complete.

No delegation, commits/staging, scraping, database access, input-cache rebuilds,
scorer promotion or deployment. Preserve all existing work and completed outputs.
New derived forecast tables and model fits under a new v12 prefix are authorized.
No additive coefficient refits are needed for this experiment. If a necessary
saved input is missing, report it; do not build an undocumented substitute.
Only one editing session in this tree. Use the basketball25 Python environment.

## 2. Evidence and limits motivating the design

Primary historical population: 44 quarter origins, 2016–2026, 5,607 cells /
726,364 possessions. Novel: 2,073 cells / 226,256 possessions. Preserve the four
2015 origins as descriptive/warmup. These are lineup-quarter outcomes, not
single-possession R² or full-season cells.

| Saved control | all MAE | all RMSE | novel RMSE |
|---|---:|---:|---:|
| corrected additive A | 8.091953 | 10.840994 | 11.853019 |
| V9_SPREAD N | 8.140175 | 10.866667 | 11.772833 |
| HALF | 8.072735 | 10.808119 | 11.766236 |
| GLOBAL | 8.070689 | 10.809699 | 11.773454 |
| v11 exposure VALUE_SWAP | 8.093971 | 10.836656 | 11.842172 |
| v11 exposure CONTEXT_RELEASE | 8.076924 | 10.808078 | 11.758635 |

The independent v11 audit reproduced all 6,179 descriptive N predictions to
1.43e-14. Its symmetric squared-error attribution assigns most HALF improvement
to the main-value change, not context. That is reference-dependent arithmetic,
not a causal fraction. Do not automatically discard profile-based value.

Three standards remain co-equal: prediction, basketball-coherent counterfactuals,
and honest OOD uncertainty. Neither a negative five-Jokic interaction nor a
positive interaction alone establishes failure. Final five-Gobert offense near
a conventional unit remains concerning. No named-player penalties or forced
Korver/Westbrook ranking. Historical years are reused development evidence.

## 3. Bounded Day5 closeout (new derived prefix only)

Use a fresh `...v11_audit_followup` prefix, preserving production and the interval
correction prefix. Reuse the independent audit log; do not repeat 248.9M forwards.

- Hash actual source checkpoints, calibration files, forecast files, fixture
  definitions and imported scientific producers used by the audit. A manifest of
  six upstream files did not cover these. Record present-day hashes as such; do
  not claim they prove what an earlier process read.
- Export the already computed exact SSE attribution by reference and cohort.
- Regenerate case selection using possessions * (error_after²-error_before²):
  eight largest harms and benefits of VALUE_SWAP vs HALF, >=100 possessions;
  also show >=200 results. Include named players and exact point ledgers.
- Export season and existing exposure-bin scorecards, not just contrasts.
- On 2016q1 and 2026q4, both references, run the previously omitted independent
  centering diagnostics: 256 independent product fives and the 16 highest-q
  donors held fixed against 64 independent fours each. Use saved projection
  coefficients and current frozen scorer, seed 20260914 with origin/reference/
  diagnostic identifiers. Report sampled residual means and sampling SE; finite
  Monte Carlo errors are not exact orthogonality failures. No K retuning.
- Complete the historical Korver injection requested in Day5 §8 using the same
  historical state source specified there, under unchanged q. Keep current-state
  and historical-injection results separate. This is not a new historical A fit
  or a matched player-season forecast. If unavailable, identify the exact missing
  source and mark this deliverable incomplete rather than silently omitting it.

These are targeted audits, not a gate requiring favorable basketball signs.

## 4. Architecture: exact anchored separation, not random-reference ANOVA

Keep the V9_SPREAD backbone: 18-state inputs, standardized leave-one-out mean+SD,
one message round, existing diagonal decoder and finite allocation budget.
Keep event labels, FT message mask and existing support penalties unchanged.
No attention, additional message rounds, new inputs or player/pair embeddings.

We deliberately change the *decomposition reference* from v11. Differentiating
its large Monte Carlo projection on every optimization step is unnecessary here.
Use an exact anchored functional decomposition with six batched evaluations per
real lineup (real five plus five one-player insertions), and one shared anchor
evaluation. This is an explicitly new estimand, not an exact implementation of
v11's product-reference projection. Frozen anchored controls below are mandatory.

For each inner/final fit cutoff t:

- Construct the exposure-weighted prior-365-day player distribution as in v11.
- Take the weighted mean of its raw 18-dimensional as-of-t player states as r_t.
  It is a synthetic reference state, not a real player or league-average opponent.
- Save donor IDs, weights, source dates, raw states, r_t and hashes. No future
  roster selection. Normalize r_t with that fit's training-prefix moments.
- Hold r_t fixed through that fit and its validation/evaluation. Training game
  player states remain their existing pregame states, not retrospective t states.

Let F_theta(X) be the native V9 event decoder's points/100 for the five states X,
using the fit's budget and standardization. Define, with all terms differentiable:

    f0 = F_theta(r,r,r,r,r)
    v_theta(x) = F_theta(x,r,r,r,r) - f0
    B_theta(X) = f0 + sum_i v_theta(x_i)
    C_theta(X) = F_theta(X) - B_theta(X)

Properties to test: F=B+C; C=0 at all-anchor and one-player-insertion lineups;
any truly additive F has C=0 everywhere; permutation invariance including clones.
Constants and additive functions added to F cancel in C. Nevertheless this is
anchored separation, NOT zero conditional expectation under a broad q. C can
correlate with individual value on observed fives; report this rather than
claiming statistical independence or causal complementarity.

Two trainable arms, no architecture/dose grid:

    ADAPT_CONTEXT: H(X) = A(X) + b + C_theta(X)
    ADAPT_VALUE_CONTEXT: H(X) = A(X) + b + G_psi(X) + C_theta(X)

A is the fixed, corrected, calibrated additive forecast appropriate to the
historical forecast origin (see §5). b is a learned scalar points/100 offset,
initialized zero, present in both arms and printed separately from context.

The flexible arm's identity-free profile-value head is:

    g_psi(z) = Linear(32,1,bias=False)(tanh(Linear(18,32)(z)))
    G_psi(X) = sum_i [g_psi(z_i) - g_psi(z_r)]

z uses the same standardized raw player state as the backbone. Zero-initialize
the last linear layer. Construct this head with a separate RNG stream (seed 117)
after constructing the backbone so shared initial backbone tensors are identical.
No player ID, additive coefficient, teammate state or outcome enters g. It may
learn nonlinear profile-based corrections; A itself enters only the final sum.
G=0 at initialization, so the two arms start with identical H. The strict arm
has no dormant unused value parameters. Both backbone and permitted head/b are
trained; no detached anchored forwards, frozen backbone or stale cached B.

Important explanation boundary: decoder event totals reconstruct F, not H.
H's exact ledger is A + b + G + C. Print F/B/C and event outputs separately.
Do not relabel G or the additive residual as measured spacing/shot quality.
Preserving event supervision does not magically make hybrid points event totals.

## 5. Causal additive offsets: mandatory before fitting

For each historical training game, use the saved corrected additive model from
the quarter containing that game, fitted strictly before that quarter. Replay it
on every grouped five needed for training, not only qualifying evaluation cells.
Use saved fit, centered reference, league level and `additive|base` calibration;
no deficit arm. Existing `centered_score` / additive replay helpers establish the
unknown-player policy. Save per-player base/carry/experience and calibration ledger.

Forbidden: applying the current outer-origin additive fit retrospectively to its
training games, using in-sample fitted residuals as if out-of-time, nearest-future
coefficients, inner-validation outcomes in inner offsets, or row-dropping joins.
Each offset row must carry game date, source origin, fit cutoff, calibration-history
cutoff, known-player flags and source hashes. With day-resolution dates, require
source cutoff <= target game day, and every fitting/reference observation date
strictly < source cutoff; a quarter's opening-day game may equal its cutoff day.
Calibration windows must have finished by that cutoff and contain no target-game
outcome. Reconcile replay against all overlapping saved A cells to 1e-8.

Saved A begins at 2015q1. Keep earlier rows for event supervision, but assign
zero *team-loss weight* where no causal saved A exists. Do not manufacture offsets
or silently drop their event labels. Report exposure with/without A per fit.
The early 2015 inner fit can have no point-supervised rows: use event-only epoch
selection there, keep b/G exactly zero in such fits, and label warmup explicitly.
All primary 2016+ fits must have positive training and inner-validation A exposure.
If they do not, stop for a source audit.

Validation/outer predictions use that window's saved A and existing origin states.
Training uses pregame neural states with quarter-frozen A: disclose that cadence
difference. Derived replay tables are new outputs, not rebuilt source input caches.
Hash manifests must include all actual files consumed. No database fallback.

## 6. Objective, epochs, fitting and calibration

Reuse v10 training machinery without modifying completed scientific modules:
five-year lookback, 730-day row decay, whole-game batches, shared baseline event
normalizers, Adam lr .001 / weight_decay .0001, gradient clip 5, existing .01
network and .01 decoder penalties, backbone seed 17 and deterministic batch order.
Apply Adam weight decay to the new head, not scalar b. No new penalty search.

Train on:

    existing normalized five-family event objective
    + 1.0 * weighted_MSE(H/100, observed_points/possessions) / D_team
    + existing support/network/decoder penalties

Team loss uses only rows with valid causal A, their same recency weights and
possession exposure, with global-denominator batch scaling as in v10. D_team is
the untrained seed-17 V9 native team's weighted MSE on this same eligible subset;
compute once per fit and share across both arms. Do not use an arm-dependent
denominator. With no eligible rows, omit the term and record its absence.
Event loss/penalties apply to real lineups only, not synthetic insertions. Anchored
forwards affect the team gradient but are not pseudo-labeled basketball examples.
Do not regress cell ORtg with unweighted per-cell losses.

Use D_team from the inner training subset also for that inner validation loss;
never recompute the selection denominator from validation outcomes. Final fitting
uses its own final-prefix denominator. Persist both with their exposure counts.

48 maximum inner epochs, patience 3, min_delta 1e-5 on validation composite
(normalized event + normalized team loss; no training regularization included).
Preserve v10's distinction between the best epoch and patience threshold.
Log both. This inherited cap is a compute bound, not a claim of convergence.
Report cap hits; do not extend after seeing outer results.

Use existing `split_for_origin`: inner training ends before preceding validation
quarter; choose epoch there; reset from the same initialization and refit on the
full prefix for exactly that many epochs. No outer-driven stopping. Final refit
recomputes its own anchor, moments, normalizers and budget from its own prefix.
Do not warm-start from the saved outer V9 fit during inner training.

H already contains calibrated A and a trained b. PRIMARY H gets **no additional
post-hoc calibration or learned blend weight** this round. This avoids silently
recalibrating the calibrated baseline and preserves its exact native ledger.
State this difference from the old neural calibration policy. Print level bias,
spread, b, G and C by origin. Do not add calibration as an unregistered rescue arm.
The plain event F is diagnostic, not a separately selected forecast.

## 7. Controls and scope of fits

Reuse exact A/N/HALF/GLOBAL, both v11 references/arms, and v10 TEAM_1 for background
comparison. TEAM_1 is historical, not a newly matched training control (eligible
point-training rows differ). Do not refit historical controls unnecessarily.

For each source V9 checkpoint, compute anchored B9/C9 using the same outer
anchor recipe. If its saved calibration is L+a+s*(F-L), its calibrated anchored
parts are B9_cal=L+a+s*(B9-L), C9_cal=s*C9. Frozen controls:

    ANCHOR_VALUE_SWAP = A + .5*C9_cal
    ANCHOR_CONTEXT_RELEASE = .5*A + .5*B9_cal + C9_cal
    ANCHOR_FULL_SWAP = A + C9_cal

These isolate reference changes against corresponding v11 forecasts. Compare
ADAPT_CONTEXT against ANCHOR_FULL_SWAP, and both trained arms against HALF/A.
Their difference includes training objective and calibration choices, not a pure
single-factor optimizer effect. The clean nested capacity contrast is trained
ADAPT_VALUE_CONTEXT minus trained ADAPT_CONTEXT.

Full run: 48 origins x 2 trainable arms = 96 arm-origins / 192 inner+final fits.
One seed; no width, alpha, anchor or seed sweep. Process in chronological order.
No full uniform-anchor refit this round. At the two pilot origins only, score
fixed fitted models with the prior uniform-mean anchor as a labeled sensitivity,
not an alternative selected by results. Changing anchors after fitting is not
retraining. Do not claim anchor robustness from this small diagnostic.

## 8. Pilots and operational contract

First implement no-fit preflight and run accounting/model tests. Pilots are
2016q1 and 2026q4, both arms, inner selection plus final refit with the protocol
above. Record every fit duration, forwards, peak memory where available, epochs,
gradient norms for backbone/head/b, parameter changes and maximum replay error.
Use the pilots for correctness and cost, not selecting an arm or changing losses.
If total pilot work exceeds 45 minutes, stop at a safe boundary with resumable
state, report cost and ask about completing it; do not silently reduce training.

Provide a full-run ETA as a measured range, noting late origins cost more. A long
but justified run is acceptable. Correctness failures require a new prefix after
fixing, not changes to a completed pilot's receipts. Completed verified fits may
be imported byte-for-byte into production if protocol, source and code hashes
match; chronological downstream histories must still be built correctly.

Provide and verify commands for background launch, tail/live log, status, and
resume. DO NOT launch production until Adam asks. Wrapper must have a real run
lock, PID + command identity/start time, durable stdout/stderr, atomic exit receipt,
and completion status distinguishing PAUSED/FAILED/TRAINED/ANALYSIS_COMPLETE.
Launch includes automatic analyses; no surprise second training job.

Every epoch: origin/arm/inner-or-final, epoch/cap, selected best, patience,
train/validation event families, team loss, composite, penalties, gradients,
elapsed and remaining fit estimates. Every completed origin: MAE/RMSE/raw R²,
bias, novel/recurring metrics and deltas against A/HALF/GLOBAL/frozen controls.
Cumulative comparisons use common completed keys and print their populations.
No missing values represented as zero; print unavailable with a reason.

## 9. Required analyses and acceptance

Primary contrast: ADAPT_VALUE_CONTEXT minus HALF, overall RMSE. Key secondary:
same on novel and recurring RMSE; flexible minus strict on all three; strict
minus ANCHOR_FULL_SWAP. Print MAE, raw R² and bias everywhere. Equal-season
paired t95 intervals and favorable-season counts; no cell-IID inference and no
claim of independent fresh confirmation from these repeatedly used years.

Reconcile exact keys, exposure, outcomes and novelty against old controls.
Report primary/descriptive, origin, season, novel/recurring, exposure, existing
composition-distance/history and era slices. Include event losses for the actual
decoder, not a fictional event decomposition of H. Export no-calibration H ledgers
and the old calibrated controls with clear labels.

Export exact symmetric squared-error attribution for changes decomposable into
A/b/G/C; for arbitrary before/after use component_delta*(before+after-2*actual),
with components summing to prediction delta. State reference and path dependence.
Select eight largest possession-weighted squared-error harms/benefits versus
HALF at >=100 possessions, plus >=200 sensitivity. Show actual rating/exposure,
names, every additive component, all five g contributions, b, F/B/C, totals and
decoder volume/location/conversion summaries. Verify every ledger reconstructs.

Basketball: reuse dated current-state fixtures and clone ladder, five Goberts,
limited centers, five Jokics, guards, conventional and real small-ball units,
Jokic/Murray/Korver vs Westbrook. Include the separate historical injection.
Show final H alongside A/N/HALF, allocation budget, FGA/FTA/TOV, shot locations,
conversion, per-player allocations, F/B/C/G/b, anchor distance and support.
Mechanism predictions are hypotheses, not synthetic training targets. Flag
five-Gobert total remaining near real offense, but do not impose an arbitrary
point penalty. A negative five-Jokic C can reflect diminishing returns.
The absence of actual opposing-five defense remains explicit.

Uncertainty: reuse the corrected prior-only finite-outcome interval procedure
on H, using only completed windows before each origin. Export boolean coverage
as nullable bool or validated 0/1, aggregate over nonmissing rows. Report 80/95%
coverage, widths and populations across all required support slices, weighted
and unweighted. Explain that outcome coverage and anchor sensitivity do not
calibrate synthetic latent-mean uncertainty. No new uncertainty method is claimed.

No automatic promotion. Prediction gains cannot erase counterfactual or uncertainty
shortcomings; a predictive tie can still justify continuation if those improve.
A null does not reject every adapted hybrid or every contextual architecture.

## 10. Tests, provenance and final handoff

Required focused tests (in addition to relevant existing suites):

- Exact anchored additive-function cancellation, nonlinear pair example, clones,
  permutations, F=B+C, all-anchor/single-insertion C=0, G(r^5)=0.
- Strict/flexible initial predictions and shared backbone tensors match. Head
  initialization leaves backbone RNG unchanged. Gradients through all anchored
  forwards agree with finite differences; actual optimizer updates reach the
  backbone and flexible head on a nontrivial synthetic supervised batch.
- Team objective units/weights/global denominators match hand calculation;
  missing A masks only team loss. No-A warmup keeps b/G zero.
- Synthetic future-outcome perturbation cannot change prior offsets, anchors,
  normalization, epoch selection or final parameters for an earlier origin.
  Inner validation labels may affect selected epochs, outer labels may not.
- Additive replay across known/unknown players and origin boundaries; full
  overlapping saved-cell replay; no missing/duplicate key laundering by joins.
- Epoch reset/refit counts, 48-cap/patience semantics, scalar-b/head ledger and
  zero-correction H=A (before any unrelated reporting transform).
- Complete manifest mismatch rejection including actual checkpoint/calibration
  inputs; corrupted/missing completed output fails resume, not silently skipped.
- Atomic gzip magic and full CRC, lock collision, failed-child exit propagation,
  interrupted-run resume, and report-only mode never writes a completed source.
- Cumulative common-population scores, weighted case ordering, SSE identity,
  interval bool/NaN handling, primary versus warmup separation.

Use new v12 modules rather than editing hashed historical producers. Hash the
transitive scientific inputs actually used, pin versions/seeds and record the
dirty baseline. Run under `no_database()`. Save fit state, optimizer/run state
needed for claimed resume behavior, curves, anchors, additive offsets, calibration
provenance, forecasts, diagnostics and checksums before completion receipts.

End with `reports/joint_capability_v12_review.md` and
`reports/joint_capability_v12_handoff.md`. Update SESSION_HANDOFF, CLAUDE's entry
point, scorecard and backlog without erasing historical records. Include a
deliverable-by-deliverable checklist, limitations/omissions, exact counts, timing,
test exit status, source/output hashes, command/log paths, quantitative comparisons
and a next decision. No staging/commit unless Adam separately asks. Do not mark
an omitted diagnostic completed or treat an expected repository guard as a pass.
