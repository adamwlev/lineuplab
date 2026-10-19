# Joint capability model: the next day of work for Sol

Prepared by Codex for Adam after independently reviewing the completed v2 run,
2026-09-09. This is a new prospective implementation and experiment contract.
Writing it does not start implementation or training.

## 0. Outcome, authority, and priorities

Produce a corrected, interpretable experiment that answers: does actual teammate
information improve a strong learned player estimator, and does the resulting
model behave sensibly in basketball examples? Deliver the predictive comparison,
basketball explanations, and an initial uncertainty audit together.

Read `CLAUDE.md`, the latest `SESSION_HANDOFF.md`, `CONTEXTUAL_MODEL.md`, and this
document. Read `JOINT_CAPABILITY_MODEL_PLAN.md` for the original architecture and
protocol. This document supersedes that plan ONLY where an amendment is explicit.
`CLAUDE_MODEL_FEEDBACK_2.md` is useful review material, not execution authority.

Adam requested these instructions for Sol. When Adam asks you to implement this
document, that request includes its bounded experiments and new derived outputs.
Proceed with routine work within that scope without asking for approval again.

- Work directly, with no Opus or other agents. Announce sole editing ownership;
  Adam should not have another editing session in this tree during your work.
- Preserve existing dirty work and both feedback files. No staging, commits,
  branches, resets, cleaning, stashing, or reverts without a separate request.
- No scraping, network acquisition, database access, package installation,
  source-cache rebuilding, scorer promotion, page changes, or deployment.
- New joins, corrected derived states/labels, fits, forecasts, and reports are
  authorized. They must not replace source caches or completed result artifacts.
- Preserve all of `joint_capability_2026_09_09_v1/`, `..._v2/`, the centered
  additive benchmark, and the influence-repair runs, including their manifests.
- Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u` from the repo root.
- Every numerical run and test command must have a durable log. No foreground-only
  training output, truncated log on resume, or silent detached process failure.
- The three co-equal standards remain prediction, basketball coherence, and
  honest uncertainty. No numerical promotion gate or coverage gate is introduced.

Work in this order:

1. Reproduce the v2 evidence and preserve its provenance.
2. Correct the data/objective issues and verify the scientific failure modes.
3. Finish development selection; freeze all choices before the new core run.
4. Run the complete five-arm, 48-origin experiment.
5. Complete basketball, error, uncertainty, and bounded negative-control reports.
6. Write the handoff and one recommended next decision.

Do not add responsibility, rebounding, or opponents during this assignment. A
failed creation example is evidence for a later responsibility experiment, not
permission to insert a penalty until that example looks right.

## 1. Established evidence: reproduce, do not rediscover by refitting

v2 is `experiments/cache/joint_capability_2026_09_09_v2/`. It completed 192
arm-origins: four arms across 48 quarters, including four 2015 warmup quarters.
The primary cohort is 44 quarters in 2016–2026: 5,607 cells / 726,364 possessions.
Novel offense is 2,073 cells / 226,256 possessions. Quarters are the saved league
game-count windows, not calendar quarters or full seasons.

| Arm | MAE | RMSE | Pooled raw r² | Novel MAE | Novel RMSE |
|---|---:|---:|---:|---:|---:|
| H0 | 8.1815023103 | 10.9575603158 | .1014154956 | 8.9278369069 | 11.8940307595 |
| H1 | 8.1672909126 | 10.9304945696 | .1058491145 | 8.9243172818 | 11.8879465367 |
| H2 | 8.1606083753 | 10.9051839203 | .1099853110 | 8.9019083881 | 11.8381898555 |
| H3 | 8.1522403556 | 10.8873661801 | .1128912859 | 8.8990624362 | 11.8044787873 |
| location + shooting | 8.1312316259 | 10.8964039646 | .1114178671 | 8.8674317951 | 11.8208144049 |
| corrected additive | 8.0919525369 | 10.8409940439 | .1204320480 | 8.9038988730 | 11.8530185856 |

Codex independently reproduced common keys/targets/weights and every v2 point
calibrator, with zero coefficient discrepancy. Saved code hashes matched. Do
not call these point predictions leaked or invalid merely because other parts
of the experiment need correction.

Season-paired H3–H1 RMSE is -0.043212 ± 0.018655 SEM, favorable 8/11 seasons;
its 95% t interval is [-0.084777, -0.001646]. H3–additive novel RMSE is
-0.052207 ± 0.073498, 7/11, interval [-0.215971, +0.111557]. Novel superiority
is suggestive, not established. No claim of best-ever arbitrary-lineup behavior.

At 2026q4, cutoff 2026-03-02, frozen league reference 115.6315055:

- Five Goberts: calibrated H1 130.3598; H3 118.0382. Native H3 116.0073.
- Five Jokićs: calibrated H1 126.5374; H3 128.6281.
- These were inference-only checks with saved fits, not new training. They show
  a useful direction and an unresolved creation failure, not calibrated OOD means.
- Korver/Bogut and several guards were absent from the saved current-origin
  profile table because it only retained players appearing in that future quarter.

Confirmed issues and qualifications:

1. `evaluate_loss` averages batch-normalized losses using grouped-row counts.
   This differs from globally accumulating each family's eligible exposure.
   On saved 2026q4/H3 predictions, the current 4096-row calculation is 1.02362121;
   global aggregation is 1.02334237. The 0.00027884 difference exceeds the old
   stopping tolerance. Rebatching the same examples must not change evaluation.
2. The specified 730-day training-example time weight is absent. This is separate
   from the implemented 180/730-day recency of player-state inputs.
3. Conversion initialization uses independent player/location EB rates rather
   than a league location curve plus a pooled player shooting offset. The recent
   three-point-share contrast is also missing.
4. Basketball diagnostics, intervals, placebos, seed checks, and the final report
   are absent; the diagnostics entry point imports a nonexistent module.
5. H0 selected epoch 1 at all 48 origins, but it DID update its parameters.
   Both development windows select epoch 1 at every tested H0 lambda, including
   0.001. Larger regularization alone is not a demonstrated explanation.
6. Separately selected lambdas and a shared penalty multiplier followed the old
   plan. Matching decoder regularization below is an explicit DESIGN AMENDMENT,
   not evidence that the worker disobeyed that plan.
7. Small logit corrections need not be small basketball effects. Do not assume
   longer training improves predictions or describe current accuracy as a floor.
8. The current made-shot identity does not have the old shot-mix cancellation.
   Auxiliary supervision can affect shared parameters; equal loss weights do
   not imply equal gradient shares. Do not remove the assisted head on that premise.

Save independently recomputed v2 tables and this audit's metadata under the NEW
prefix's `review_v2/`. Never run a reporting command that writes inside v2.

## 2. Versioning and the new budget

Use `experiments/cache/joint_capability_2026_09_09_v3/` if absent. Otherwise
inspect its protocol and either resume compatible work or choose a new explicit
prefix. Never overwrite completed work because a default path already exists.

Keep the existing `joint_capability_*.py` scientific modules intact so v2 remains
replayable. Implement in small versioned modules:

    experiments/joint_capability_v3_data.py
    experiments/joint_capability_v3_model.py
    experiments/joint_capability_v3_fit.py
    experiments/joint_capability_v3_run.py
    experiments/joint_capability_v3_diagnostics.py

Reuse pure unchanged helpers where appropriate. Copying a small existing module
as the starting point for its corrected version is fine; do not build a generic
experiment framework. Preserve and hash imported helpers too. Add focused tests
under `tests/test_joint_capability_v3_*.py`.

NEW prospective budget, activated by Adam's implementation request:

- 8 aggregate wall-clock hours of numerical fitting;
- 700 new-study optimizer-fit invocations, including inner fits, final refits,
  development, controls, synthetic training checks, failures and retries;
- 2 hours for derived-data preparation; target peak RSS below 10 GiB.

These are ceilings, not runtime promises. The previous manifest's 384 fits
counts only v2 core. Its 28 development candidates add 56 inner/final fits:
v2 used at least 440, before v1 and interrupted work. Do not claim 216 fits
remain from the old 600-fit budget. Record old accounting separately.

The new worst-case scheduled numerical work, excluding small tests/retries, is:

| Work | Maximum fits |
|---|---:|
| H0/H3 development optimization trace, two origins, inner only | 4 |
| H0 decoder grid, four values including one possible extension, two origins | 16 |
| H1/H2/H3/H3F network grids, same bounds | 64 |
| Five arms × 48 origins × inner/final | 480 |
| H3 context shuffle, four origins × inner/final | 8 |
| Three FT diagnostic arms, four origins × inner/final | 24 |
| Seeds 29/43, four original H arms, four origins × inner/final | 64 |
| Total | 660 |

Prioritize the full core and non-fitting basketball/uncertainty outputs. If the
wall-time ceiling threatens completion, preserve full cohorts and defer the
lowest-priority seed checks with measured cost. Do not quietly run fewer primary
years, replace failed forecasts, or select favorable origins. Log every fit
start/end immediately; a crash must not erase compute already spent.

## 3. Correct the data and objective before new selection

### 3.1 A globally defined loss

Implement each head as a numerator and its eligible exposure. Sum those quantities
over batches first, divide once, then apply training-prefix baseline scales and
the equal five-family average. Evaluation must be invariant to batching, input
ordering, and the number of zero-exposure examples. Missing exposure is not a
zero loss to average into the objective.

Retain the five families: composite FGA/FTA/TO count likelihood, location,
FG conversion, FT conversion, and assisted-made share. The count family sums
the three per-channel, per-eligible-possession losses. With fully observed labels
this reduces to the original count formula. Save every denominator explicitly.

For count scaling, use FULL grouped Poisson NLL, including `lgamma(y+1)`, to avoid
dividing by an arbitrary constant-dropped quantity that can be negative. This is
an explicit objective-normalization amendment. The factorial term changes no
unscaled Poisson gradient, but it affects the family scale, which must be recorded.
Keep `(game, off5)` grouping fixed across arms and versions; equivalence to an
event-wise count objective is up to a parameter-independent grouping constant,
not an assertion that all normalized scalings are identical under regrouping.

At an inner or final fitting cutoff T, training example weight is
`2 ** (-(T - game_date).days / 730)`. Apply this to every eligible count/exposure
and all five heads, including each assisted player-game label exactly once. All
rows of one game share its weight. Validation/outer evaluation is unweighted in
time; its natural event exposures supply its weights. Time weighting must also
enter training baseline normalizers, feature standardization and averaged output
penalties. U retains its separate 365-day definition.

Training uses complete-game mini-batches. Its stochastic gradient must estimate
the declared globally normalized training objective. One acceptable implementation:
partition shuffled games into batches, use full-training exposure denominators,
and multiply each batch data/row-penalty contribution by the number of batches.
An epoch's average gradient at FIXED parameters must equal the full-data gradient;
ordinary optimizer updates during the epoch naturally change parameters. Apply
parameter-only decoder/weight penalties once per optimizer step, without an
additional batch-count multiplier. Document the convention and test the identity.

The five baseline scales are computed from zero-correction, identity-decoder
predictions on the weighted fitting prefix. They are common to all arms with
the same split, and never estimated on validation or outer outcomes. Save scales,
weighted exposures and effective sample counts for inner and final fits.

### 3.2 Attribution, identities, and grouped labels

Reconcile new grouped labels against the exact source IDs. Preserve team point
targets even when an event cannot be attributed. Report match rates by season
and channel, not just one overall number.

- Missing shooter attribution is not a known zero for all five players. Where
  the possession is known but its FGA/FTA actor cannot be assigned, mask that
  count channel for the affected grouped lineup; retain the other channels.
  Record lost exposure. Include genuine zero-event players in fully observed rows.
- Unknown location masks location/conversion supervision for that attempt, while
  retaining its known FGA count. Never substitute a location category.
- Reconcile auxiliary player-game FGM with the grouped attributed FGM. Mask the
  auxiliary label when they differ, and report lost FGM exposure. Codex found
  33 inconsistent player-games / 205 FGM in v2; this is small but should be explicit.
- Report shot/FT reconstructed points against cached team points. v2's net
  difference was 20,326 points, 0.307754% of cached points, across 6,006 groups.
  Do not force reconciliation by changing the point target or adding a fitted bonus.
- Retain the original 2% overall / 5% any-season attribution warnings. A warning
  prompts diagnosis and disclosure; it does not authorize new data acquisition.
- Validate integers before joins and retain integer player-game codes throughout.

### 3.3 Shooting offsets and historical state

Restore a pooled player offset across locations, using two offsets per player:
one for two-point buckets and one for three-point buckets. To remove ambiguity
in the original plan's logit-offset wording, use this fixed moment approximation:

1. At each historical state date, get 730-day weighted per-player/location
   attempts A, makes M, and squared-weight attempt sums Q from earlier games only.
2. League bucket probability is `(sum M + 0.5)/(sum A + 1)`. The fixed symmetric
   half-event prior provides a finite startup fallback, not a learned era feature.
3. For a player and shot type, let
   `I = sum_b A_b*l_b*(1-l_b)`, `S = sum_b (M_b-A_b*l_b)`,
   and `J = sum_b Q_b*l_b*(1-l_b)` over its buckets.
   Raw logit offset is `S/I`; approximate sampling variance is `J/I**2`.
4. Among players with positive exposure, estimate
   `tau2 = max(weighted_mean(raw_offset**2 - sampling_variance), 1e-12)`
   using type-level effective-attempt weights `(sum A)**2/sum Q`.
   Shrink offset by `tau2/(tau2+sampling_variance)`. Zero exposure gets offset 0.
5. Baseline make probability is `sigmoid(logit(l_b)+shrunk_offset_type)`.
   Record epsilon 1e-6 at probability/logit boundaries. Save prefix tau2 and
   exposure mappings. This is approximate moment EB, not a posterior guarantee.

This is a declared v3 initialization, not a claim of numerical identity with
`location_skill.player_offset_rates`, which uses probability-scale offsets.
Test it against a brute-force implementation of these exact equations and show
baseline held-out conversion diagnostics. Do not tune its formula on core outcomes.
Conversion-state exposure is the corresponding TYPE-level effective attempts;
the common offset does not create six independently measured player skills.

Restore the four recent-role contrasts specified by the original plan: 180-day
minus 730-day usage units/possession, 3PA share of attributed FGA, TO/possession,
and assists/possession. Use matching denominators at both horizons. The past
teammate reference uses usage units/possession, assists/possession, 3PA/possession,
and assisted-made share, all from the teammate's beginning-of-game state.
Save names/units for all 64 input coordinates and all 18 anchored-state coordinates.

Keep historical training states strictly before their rows; emit beginning-of-day
states, then update after all games that day. Inner-validation and outer states
are frozen at their respective quarter starts. Training prefixes use exactly
5*365 days before THEIR fitting cutoff, including the inner-fit cutoff; this
corrects the current helper's use of the outer lower bound for its inner fit.

Export origin profiles for every player with history BEFORE that cutoff, plus a
generic population-prior fallback. The evaluated future roster must not decide
which historical players can be queried. New entrants use the same fallback
whether or not their later identity was known during preparation. Persist
last-observed date, missingness, effective exposures, and role-share history.

Also save causal mean/SD of each player's actual usage-unit share in historical
game-lineups, weighted by 180-day-decayed possessions. Exclude groups with zero
usage denominator or unresolved component counts from this reference and report
coverage. This reference supports diagnostics, not an extra scoring term.

## 4. A stronger comparison and a bounded optimization protocol

### 4.1 What stays fixed

Keep the shallow E/M architecture, 32 tanh units, 18-state representation,
zero-initialized output layers, finite opportunity budget, explicit made-shot
identity, assisted auxiliary head, masked teammate FT-conversion coordinate,
and no ID parameters. Learning rate remains 0.001, Adam weight decay 0.0001,
gradient clip 5, target batches 4096 grouped rows with games intact.

No learning-rate, width, loss-weight, half-life, or message-standardization search
today. Raw anchored-state message inputs remain as in v2. Conditioning them
differently could help, but that is a separately measured architecture change.

Separate regularization into
`lambda_network * (exposure_weighted_encoder_penalty + message_output_penalty)`
plus `gamma_decoder * (intercept_penalty + log_slope_penalty)`.
Use the same gamma in every primary/control arm. H0 has no network lambda.
Keep zero nesting exact with a shared decoder held fixed in function-level tests.

### 4.2 Epoch policy: explicit amendment, no outer-data selection

Change the policy from max 12 / patience 2 / min_delta 1e-4 to:

    max_epochs = 24
    patience = 3
    min_delta = 0.00001
    seed = 17

This is a modest, fixed optimization audit motivated by H0's very small inner
improvements. It is not a promise that training longer helps. Print epoch zero
validation as a diagnostic, then train. Track the exact best finite validation
checkpoint separately from the patience reference: patience resets only after
min_delta improvement; checkpoint selection keeps the lowest observed validation
loss, with exact numerical ties preferring the earlier epoch. Select among
trained epochs 1–24. Report if all trained epochs lose to initialization.

For each outer origin, fit before the previous completed quarter; select epoch
on that inner quarter; reinitialize from the same seed and refit all eligible
data before the outer cutoff for EXACTLY that many epochs. No training-loss
checkpoint selection during final refit. Outer outcomes never choose epochs.

Before grid selection, run one full 24-epoch INNER trace for H0 and H3 at each
2014 development origin with gamma=0.01 and network lambda=0.01. Disable stopping
only for these four traces and simulate both stopping policies from their curves.
Report what each would select and whether loss/gradients are still moving at the
cap. These traces do not evaluate the primary cohort or authorize changing the
fixed v3 policy. A still-improving cap is disclosed, not silently expanded again.

### 4.3 Development selection

Use only 2014q3 and 2014q4, with the corrected nested process. Score the mean
five-family objective, averaged equally over the two development windows.

1. Select common gamma using H0 alone: grid `[0.001, 0.01, 0.1]`.
2. Freeze gamma for H0/H1/H2/H3 and H3F below.
3. Separately select network lambda for H1, H2, H3 and H3F from the same grid.

For every grid, values within 1e-5 of its minimum are tied; choose the larger
coefficient. If the selected value is at an initial edge, evaluate ONE adjacent
decade at that edge on both development origins. Stop and disclose any remaining
boundary. Save all candidates, curves, scores, selected epochs and timing.
Reuse exactly matching completed candidates, never approximate float-key matches.

The tighter tie tolerance is a declared amendment. It does not manufacture
interiority. Do not insist that H0 choose a later epoch or that H3 win development.
Report the decoder's actual parameter movement and the prediction movement from
initialization. Freeze selection before inspecting any v3 2015/primary prediction.

### 4.4 Fifth full-run arm: H3F, fixed teammate reference

H3F has the same encoder and message-network capacity as H3. Replace actual
sender state in every directed message by ONE fixed reference vector:

    H3:  c_i = mean_j!=i M(h_i, h_j)
    H3F: c_i = M(h_i, b_reference)

`b_reference` is the training-prefix mean baseline state, weighted by decayed
player-possession exposure; save it with the fit. It is a fixed nuisance input
like fitted normalization, not a player snapshot. No validation/test rows enter
its estimate; recompute it for the final training prefix. Do not replace the
actual five players in the opportunity denominator, own inputs or labels.

H3F can improve the recipient's estimate through the additional network but
cannot condition its message on the actual four teammates. Historical teammate
references in its own inputs remain unchanged, as in H1. Match decoder gamma,
optimizer, stopping policy and data; tune its own network lambda by §4.3.

Run all FIVE arms for all 48 origins. H3–H3F is the primary new test of the value
of actual teammate information. H3–H1 remains useful but also changes capacity.
Report original H contrasts and factorial interaction descriptively; do not call
them causal skill identification or choose a new headline arm after the run.
Treat 2015q1/q2 as the initial real-data milestone, print their complete tables,
then continue automatically through the schedule when integrity checks pass.
Do not stop a healthy run just to request feedback on partial accuracy.

v3–v2 compares a PACKAGE of fixes and design amendments. It cannot attribute
the entire change to recency, stopping, initialization, or shared penalties alone.

## 5. Evidence required from the complete run

### 5.1 Prediction and held-out events

Reuse the exact 48-origin schedule and frozen common keys, targets, league levels,
weights and novelty flags. Each new arm has its own prior-completed-window affine
point calibrator. Use 2015 for warmup; development forecasts never enter calibration.
Preserve the original minimum 30 cells and cold-start identity behavior.

Evaluate event heads on genuinely OUTER data for every origin, both full eligible
events and common-cell restriction. Inner losses used for selection are not the
evidence that a head forecasts. Save sufficient prediction/label summaries to
reproduce all point, channel, allocation and calibration tables without refitting.

Report native/calibrated MAE, RMSE, bias, raw r², correlation; counts per 100 for
FGA/FTA/TO/3PA; location CE; FG/FT Brier and calibration bins; assisted conditional
loss; and player allocation error. Distinguish redistribution among players from
changes in the team's count/conversion totals. Tiny relative CE improvements
cannot be compared as though every head has the same irreducible noise.

For within-quarter metrics follow the existing `influence_repair._metric_frame`
definition: subtract the actual possession-weighted origin mean from actual AND
prediction, preserving prediction bias. This is a retrospective diagnostic, not
a deployed reference. An additional version removing each prediction's own origin
mean must be labeled differently; it removes bias and is not a replacement score.

Report all/novel, seasons, and exposure bins <100/100–200/200–400/400+ with counts.
For all planned contrasts use equal-season mean, SEM, 95% t interval and seasons
favorable, plus the original 2,000-draw season-block bootstrap, seed 20260909.
Shots, quarters sharing training history, and random seeds are not independent
replicates. Keep the original raw target; no opponent-neutralized substitution.

### 5.2 Basketball and exact explanations

Freeze a resolved fixture JSON with IDs, all five names, source dates, scoring
origin and expected mechanisms BEFORE new fitting. Resolve names from saved
exports, not the database. Include:

- At 2026q4, Nikola Jokić / Jamal Murray / Aaron Gordon / Michael Porter Jr.
  plus Kyle Korver versus Russell Westbrook. Current Korver stays explicitly
  stale. Compare native, calibrated, H3–H1, H3–H3F and
  corrected-additive swap contrasts; none is automatically a causal pair effect.
- A separate historical override: Korver's state immediately before 2015-07-01,
  with the other four and scoring model at 2026q4. Retain the source-date metadata
  and source-date staleness; label mixed-era transport as an assumption, not a
  measured 2026 ability. Do not silently rescale old inputs to force a result.
- Five limited centers: Andrew Bogut / Rudy Gobert / Kevon Looney /
  Mitchell Robinson / DeAndre Jordan; five guards: Chris Paul / Stephen Curry /
  Damian Lillard / Kyrie Irving / Trae Young; five Goberts; five Jokićs.
- Warriors: Stephen Curry / Klay Thompson / Andre Iguodala / Harrison Barnes /
  Draymond Green using 2016q4 states and model.
- Clippers: Reggie Jackson / Paul George / Kawhi Leonard / Marcus Morris Sr. /
  Nicolas Batum using 2021q4 states and model.
- Tyrese Haliburton versus T.J. McConnell beside Andrew Nembhard / Aaron Nesmith /
  Pascal Siakam / Myles Turner at 2025q4,
  using only pre-cutoff states. This is a same-four mechanism check, not an
  explanation of later team wins or injury consequences.
- The prior highest-exposure actual 2026 lineup, selected using only games before
  2026q4, as a familiar reference. Print the selection exposure.

All historical fixtures use a fitted model whose cutoff is compatible with the
selected date. No later games may enter the earlier state. The separately labeled
mixed-era Korver case deliberately uses a current model to score a historical
player-state selection; it is not a historical out-of-sample prediction.

Use ONE shared inference/decoder path. Return U, each player's attempts, shares,
six locations, make probabilities, expected makes, point contributions, and
support metadata. Canonical reported ledgers use float64 inference from saved
parameters, with exact accounting within 1e-8 pts/100. Separately check/record
float32 training parity (initial tolerance 1e-4 pts/100) rather than confusing
roundoff with a different score formula.

Explain each swap through the fixed native path budget -> player opportunities
-> location -> conversion, plus its reverse ordering. The path sums exactly to
the point difference; attribution sensitivity is printed. Calibration is its
own final layer, not a mechanism. Display effects on the four unchanged players
as well as the replacement player.

Changing conversion alone must obey attempts × shot-value arithmetic. Changing
location must not be canceled elsewhere. Recompute after slot permutation, batch
vs single-case scoring and duplicated slots. Equal states must get equal treatment.
Show failed expectations visibly. Rebounding and defensive mechanisms remain
unimplemented; do not infer them from an offensive-only number.

### 5.3 High-exposure error review

Use the pre-specified >=200 possessions AND >=5 games per lineup-quarter. Show
top 10 H3 losses against additive and top 10 against H3F; retain the original
H3-versus-H1 table as well. Rank by possession-weighted squared-error difference,
show MAE difference, and print all qualifiers if fewer than 10 exist.

Each case needs all player names, actual ORtg, predictions, additive player
coefficients from the centered saved fit, and exact new-model ledgers. Split its
games into two chronological halves DESCRIPTIVELY with the original quarter-start
forecast unchanged. Do not refit or select the halves that support a story.

Report broad channel biases across ALL qualifying cells before discussing the
selected failures. Distinguish count, location, conversion, and point-calibration
errors. Finish with up to three recurring, quantified failure patterns.

## 6. Uncertainty: useful measured output with explicit limits

First reproduce rolling empirical absolute-residual intervals at 50/80/95% for
H0/H3/H3F and frozen additive/location+shooting. Adapt the pure arithmetic of
`influence_repair.run_intervals`, without invoking its old-run manifest writer.
Use prior COMPLETE forecast windows only; require 200 historical cells overall,
use exposure bins when they also have 200, otherwise pool prior cells. Use the
same higher empirical-quantile definition and disclose cold-start ineligibility.
Show unweighted and possession-weighted coverage, width, calibration size,
fallback, and comparison-cohort counts. Independently replay every saved radius.

Required support vector per forecast:

- minimum effective player exposure and maximum staleness;
- per-player assigned usage share minus causal historical mean, divided by
  `max(historical_SD, 0.05)` in SHARE units;
- composition distance defined below.

Composition distance uses the concatenated mean and population SD of the five
18-coordinate baseline states (36 coordinates). Standardize against historical
game-lineups in that origin's training prefix using the prescribed decayed
possession weights; use a 1e-6 variance floor. Distance is RMS standardized
distance from that reference centroid. Save normalizers and prefix distance
quantiles. This is a transparent distance proxy, not a density or causal support
estimator. It deliberately includes era/profile differences.

Bounded new interval test: at each outer cutoff, split available completed prior
windows chronologically into older/newer halves, never split a window. If both
halves have >=200 cells, fit a nondecreasing isotonic mean scale for
`abs(error)*sqrt(possessions)` versus composition distance on the OLDER half.
Use scale floor 1e-6 and constant extrapolation at both ends. Estimate higher
quantiles of `abs(error)*sqrt(n)/scale(distance)` on the NEWER half. The current
radius is `quantile*scale(current_distance)/sqrt(current_n)`. Otherwise use the
exposure-only fallback. No outcome from the current quarter enters either step.

This explicitly separates scale fitting and residual-quantile calibration.
Compare it with exposure-only intervals on identical eligible cells. Report
coverage/width in prefix-defined distance quartiles and the thin/stale/high-role
stress slices; whether distance orders persistent error is an empirical result.
For these descriptive slices, thin means minimum coordinate effective exposure
<200, stale means maximum age >180 days, and high-role stress means maximum
positive standardized role excess >2. These are fixed reporting thresholds,
not exclusions or adjustments to the mean. Report intersections and counts.
Do not search over alternative distances until this version looks calibrated.

The finite-batch evaluation conditions on n possessions; the product's eventual
latent-mean interval is a different quantity. Provide numerical forecasts for
synthetic lineups, their support reasons, and cross-arm/model sensitivity, but
label their empirical interval coverage unvalidated. Constant tail extrapolation
does not establish sufficient widening for five-center means. If this pillar
remains incomplete, say so prominently. No refusal-to-score gate or invented
Bayesian confidence claim.

## 7. Bounded controls after the full core

Use the original fixed diagnostic origins 2016q1, 2019q1, 2023q1, 2026q1.

1. **Context shuffle:** H3 with sender four-tuples shuffled between examples in
   the same training date and coarse prior-own-usage bin. Preserve the recipient,
   actual five for allocation, and all labels. At inner validation use the same
   frozen cutoff, never later-date states. Define bins from training-only own
   usage quartiles, fixed seed 17, record singleton/unchanged fraction. Shuffle
   assignment is fixed within each partition, not a newly selected seed each
   epoch. Train/select under shuffled context, then evaluate the final fitted
   model with REAL outer context as specified in the original plan. Use H3's
   selected gamma/lambda and v3 stopping policy; this four-origin control is a
   diagnostic, not an 11-season significance sample.
2. **FT-context diagnostic:** three separate FT-only models with fixed historical
   baseline states: own FT logit with shared calibrated intercept/positive slope;
   that baseline plus a recipient/fixed-sender 36->32->1 tanh correction;
   and that baseline plus real teammate corrections averaged over other slots.
   Use common selected gamma, H3's lambda, seed 17, v3 nested stopping and the
   same weighted FT loss. Compare on attributed OUTER FT attempts. Fixed-sender
   versus real-sender distinguishes extra recipient capacity from teammate data.
   These heads never alter core predictions. A signal flags residual association
   or confounding; absence does not prove FG effects causal.
3. **Seed sensitivity:** seeds 29 and 43 for H0/H1/H2/H3 on those four origins,
   with frozen development selections and separate per-seed nested stopping.
   Compare native points, event losses, encoder/message corrections and their
   cancellation with seed 17. This is model sensitivity, not independent
   statistical evidence or a posterior. Do not ensemble a partial seed cohort
   into the primary scoreboard.

For the sparse seed/shuffle runs, compare outer event losses and NATIVE point
forecasts on the same four origins. They do not have a full preceding forecast
history for their own point calibrator. Optionally apply the original seed-17
H3 (or corresponding H arm) calibrator unchanged to show sensitivity conditional
on that fixed calibration, labeling it explicitly. Do not fit a new calibrator
from four scattered origins or mix these diagnostics into the primary table.

Generate the non-fitting basketball, failure and interval outputs before starting
these extra fits, so budget exhaustion cannot leave both other pillars unexamined.

Zeroing messages in an existing fit may be an additional cheap diagnostic, but
is not a replacement for refitted H1 or H3F. Finish these controls within the
budget; disclose deferred seeds rather than hiding unfinished required output.

## 8. Verification that earns its cost

Before development, prioritize tests for the actual defects:

1. Full-batch vs differently batched losses and gradients with unequal event
   exposures, zero-event players and missing heads; exact time weights across
   all families, including once-per-game assisted labels.
2. Brute-force vs incremental dated counts, offsets, references and effective
   exposures; same-day handling and the restored recent 3PA contrast.
3. Mutating/appending later games cannot change earlier features, priors,
   normalizers, selection inputs, calibration or predictions. Separately test
   the inner cutoff, retired players and genuinely unseen IDs.
4. Early-stop patience versus exact best-checkpoint selection; final refit keeps
   its last selected epoch; cap and initialization-loss warnings are truthful.
5. Shared gamma across all arms, explicit network lambda, and H3F's independence
   from actual sender inputs within its message path. Its finite denominator
   should still respond when a real player is replaced.
6. Hand-counted attribution and shot/FT/assisted reconciliation; compare grouped
   event supervision to its ungrouped reference with constants handled explicitly.
7. Tiny controlled synthetic independent-outcome and complementarity examples:
   a no-context process need not give real context a systematic advantage; a
   sufficiently strong known interaction must be learnable. Score independent
   samples, report magnitudes, and never require latent weight identification.
8. Save/load equality, single/batch/clone permutation invariants and exact ledgers.

Before accepting the report also verify metric/radius replay, no future window
in calibration/support, immutable resume, completed-origin artifact completeness,
and the expected five-arm common population. Run the full repository suite once
after integration, with logged results and unrelated failures preserved.

Do not replace the experiment with an expansive test-writing campaign. The
tests above have specific scientific failure modes; build the minimum useful
fixtures and proceed to quantitative output.

## 9. Operational interface, logs, and durable output

Implement these entry points under `experiments.joint_capability_v3_run`:

    audit-v2     # saved-data review only; writes exclusively into the new prefix
    preflight    # new derived inputs, schema, fixture IDs, coverage; no model fit
    develop      # the bounded trace and selection stages above
    core         # all 48 origins, all five arms, resumable
    diagnostics  # non-fitting tables/panel/intervals plus bounded controls
    report       # saved-output assembly only; never starts training

Support `--run-dir`, `--resume`, `--dry-run`, operational `--max-seconds`, and
separate diagnostics selectors for saved-output work versus additional fits.
Do not report a stub as implemented or make `report` silently call training.

Freeze scientific configuration and source hashes before fitting. Refuse resume
when sources, scientific code, features, selection, or fixtures differ. Never
replace saved hashes with current ones to make a resume appear compatible.
Freeze grid/stopping/selection RULES in the original protocol before any fit;
save selected coefficients afterward in a separate immutable selection artifact.
Each core fit depends on both hashes. Development results must not rewrite the
protocol or cause a resumed core to select new coefficients.
Different log destinations/time ceilings do not change the scientific identity.
An interrupted origin is recomputed or resumed from an explicitly compatible
checkpoint; completed origins are immutable and cannot enter calibration twice.

Every epoch log prints origin/arm/seed/phase, train and validation cutoffs, frozen
profile dates, weighted exposures, gamma/lambda, epoch/cap, data loss versus
penalty, validation families, gradient norm, elapsed time, best epoch and patience.
Final refit prints `validation=none`, not training loss under a validation label.
Print every origin's native/calibrated metrics and MAE/RMSE/r² deltas versus
additive, location+shooting, and H3F where available. Every completed quarter prints
the cumulative matched primary table and completed/expected counts.

Provide and verify a shell launcher that logs all phases with failure propagation,
unique or append-only stage logs, process IDs, start/end timestamps and final exit
status. Adam can run the entire pipeline in the background and follow one log.
Never give a launcher that continues from failed development into core training.
Show an actual log excerpt and measured runtime estimate before handoff.

If Adam chooses to self-run, supply exact launch, tail, process-status and resume
commands and checkpoint cleanly. Do not consume a session repeatedly polling a
healthy long fit. Resumes must continue the full scheduled experiment without
artificial one-origin limits. A pending user-run stage is pending, not complete.

Required outputs beneath the new prefix:

    protocol.json, manifest.json, source_registry.json, feature_schema.json
    input_audit.json, coverage.csv, fixtures.json
    review_v2/                 # independently reproduced review evidence
    derived/                   # new labels/states/references, original sources untouched
    development/               # full trace and selection evidence
    origins/<origin>/<arm>/    # fit, curves, ledgers/predictions, calibration, completion
    diagnostics/               # controls, cases, failures, intervals and support
    reports/                   # metrics, season pairing, channel tables, comparisons
    logs/                      # append-only or uniquely named logs, PID/exit metadata

## 10. Finish with an evidence-based handoff

Write `reports/joint_capability_v3_review.md` from saved outputs. It must include:

- exact implemented changes versus v2, including which were protocol repairs and
  which were new design choices; actual defaults and learned parameter counts;
- same-population point/channel comparisons, uncertainty of contrasts, and all
  five arms, with v2 and frozen controls clearly labeled;
- results for all three product standards, including failed examples and gaps;
- whether real teammates beat H3F, and what shuffle/FT/seed checks add;
- the high-exposure failure cases and the maximum three recurring diagnoses;
- actual timing/memory/fit counts, commands/log paths, source/protocol hashes,
  tests, completion status, and deferred work with reason and cost;
- ONE recommended next research decision and the evidence that would reverse it.

Update `MODEL_SCORECARD.md`, `MODEL_RESEARCH_ROADMAP.md`, and prepend
`SESSION_HANDOFF.md` without erasing historical entries. Distinguish
`core_complete`, `diagnostics_complete`, and `handoff_complete`; derive completion
from artifacts, not a successful process exit. Name the active editor and any
running process/log. No automatic scorer promotion.

Interpretation rules:

- H3 beats H1 but ties H3F: additional estimation capacity may explain the gain;
  do not describe it as demonstrated teammate complementarity.
- H3 beats H3F on outer events but not points: identify redistribution, conversion
  and team-total effects before choosing another model component.
- Accuracy holds or modestly loses while basketball materially improves: report
  the co-equal tradeoff; do not reject on r² alone.
- Five limited creators still look efficient: report the inadequacy, then propose
  the original responsibility experiment as a separately authorized next step.
- Distance fails to improve interval behavior: report uncertainty as unfinished;
  do not add a retrospective widening multiplier.
- Neither prediction nor basketball nor uncertainty meaningfully improves:
  record the negative result and recommend a different direction without an
  unregistered architecture/optimizer sweep.

### Suggested request Adam can give Sol

> Read SOL_JOINT_CAPABILITY_DAY2_PLAN.md and implement it, including its bounded
> experiments and new derived outputs. Follow its priorities, preserve all original
> artifacts, and use durable verbose logs. Do not delegate, scrape, access the
> database, rebuild source caches, promote a scorer, or deploy. Keep me updated
> with quantitative comparisons and finish with the documented handoff. If I run
> a long stage myself, give me the verified background/log/resume commands and
> record exactly what remains pending.
