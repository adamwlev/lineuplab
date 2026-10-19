# Next-day model plan: repair, complete the experiment, inspect the basketball

Prepared by Codex on 2026-09-08 for Adam and the next implementation session
(intended implementor: Sol). Starting revision: `e68c53a`.

**Status: implementation contract, not completed work or scorer promotion.**
This is a post-review repair/reanalysis plan. We have already seen the old
results; this is NOT an untouched holdout or a retrospective pre-registration.
The new comparisons below are specified before seeing corrected results.

## 0. Read this first

The day's objective is to finish with:

1. The two confirmed mix bugs repaired and their downstream consequences measured.
2. A complete, same-population forward comparison against the corrected additive
   model and the structural parent, with readable per-origin logs.
3. A concrete basketball report from the SAME scoring implementation.
4. A first current-candidate finite-batch interval audit, with the remaining
   latent/OOD uncertainty gap explicitly visible.
5. A short recommendation and an exact restart point, not another long list of
   possible experiments.

This is a focused day's work, approximately 8–10 implementation/review hours,
not a promise about model speed. The actual numerical runs should be a small
part of that time: the old full mix run took about 91 seconds, factor run about
30 seconds, and point-scoring passes about 30 seconds each. These are historical
measurements, not guaranteed runtimes for changed code.

**Get the first complete corrected point table by the middle of the session.**
Do not spend the whole day on infrastructure or synthetic tests. Conversely,
do not tune a broken estimator because its scoreboard looks good.

### Authority and working-tree boundaries

- This document alone does not authorize execution. Adam's follow-up asking the
  next agent to implement it should explicitly include the bounded experiments
  and new derived artifacts described here. No experiments are run when merely
  preparing or reviewing this plan.
- Follow `AGENTS.md`, `CLAUDE.md`, and `CONTEXTUAL_MODEL.md` §2. Adam explicitly
  authorized Opus to lead the original influence workstream; do not rewrite
  that history or interpret this review as revoking its authority.
- This is a new, explicitly scoped repair branch of that research. Preserve
  original protocols/results and append corrections instead of rewriting them.
- One editing agent in the shared working tree. No automatic Opus delegation
  or additional agents for this day: Adam intends to use Sol to reduce cost.
  Stop if another editing session is active; resolve ownership with Adam.
- No scraper, network acquisition, database mutation, input-cache rebuild,
  additive refit, original benchmark rerun, production-scorer promotion, page
  changes, deployment, or commit unless Adam separately requests it.
- Never modify a completed run directory or old coefficient/result artifact.
  New derived fits and reports go under a NEW prefix. Missing input caches are
  a prerequisite to report, not permission to regenerate them silently.
- Preserve `MODEL_FEEDBACK_FROM_CLAUDE.md` untouched. Preserve unrelated dirty
  work. Do not stage, stash, reset, clean, or revert the tree.
- Run model code/tests with
  `/Users/adam/miniconda3/envs/basketball25/bin/python -u`.

### Efficient reading order

Read the repository agreement and current handoff first. Then read this plan
completely and the relevant code for the task being implemented. The detailed
historical source is `TEAMMATE_INFLUENCE_EXPERIMENT.md`; use its sections as
needed rather than rereading its entire history at every task boundary.

- Parent/cutoffs: `experiments/asof_point_allocation.py`,
  `experiments/asof_point_calibration.py`.
- Mix: `experiments/mix_influence.py`, `mix_influence_run.py`, `mix_points.py`.
- Integration: `experiments/assembled.py`, `channel_factor_run.py`.
- Shooting diagnostic: `experiments/shot_quality_forward.py`.
- Main old result tables: `experiments/cache/assembled_{metrics,origins}.csv`,
  `assembled_cells.csv.gz`, `mix_points_origins.csv`.
- Existing tests: `tests/test_onfloor_influence.py`.

## 1. Starting evidence and exactly what needs repair

### 1.1 Frozen comparison to reproduce

The workstream's parent is `structural|180|live|recent_live|raw|base`, followed
by its own prior-only affine/assist-deficit calibration. It is NOT the earlier
designated `...calibrated|deficit` arm with MAE 8.1461. Keep that distinction.

Primary: 2016–2026, 44 quarterly evaluation origins, 5,607 cells and 726,364
possessions. The four 2015 origins provide historical warmup: process all 48
scheduled origins in chronological order. Verify the actual saved schedule;
never interpret directory names alone as causal cutoff metadata.

| saved arm | MAE | RMSE | pooled raw r² | novel MAE |
|---|---:|---:|---:|---:|
| workstream parent | 8.1439828452 | 10.9214307921 | 0.1073313941 | 8.8902831104 |
| shooting feature | 8.1321411605 | 10.9048096701 | 0.1100463980 | 8.8745136978 |
| best_three (location + shooting + factor TO) | 8.1386148674 | 10.8964937987 | 0.1114032154 | 8.8612190997 |
| corrected additive | 8.0919525369 | 10.8409940439 | 0.1204320480 | 8.9038988730 |

The novel slice has 2,073 cells / 226,256 possessions. These are raw offensive
rating targets. Opponent-adjusted targets are a separate experiment, not a
different column to substitute into this scoreboard.

Codex independently reproduced these metrics and ran all 606 existing tests
successfully during review. That does not verify the scientific claims below.

### 1.2 Confirmed bug A: own shots enter mix's off group

`mix_influence.teammate_index` correctly excludes the shooter from his own
teammate-on group. But `onoff` defines off as all team shots minus that group.
The player's OWN shots consequently enter his off group.

A synthetic example with a player present for EVERY shot in his only game
returned a nonzero influence and eligible exposure despite zero actual off-floor
shots. This is an observation-accounting bug, not a shrinkage preference.

### 1.3 Confirmed bug B: assembled mix uses turnover's slope

`assembled.py` imports `turnover_points.prior_slopes`, calls it with its default
turnover channel, and scales mix by the result. It does not use the mix point
experiment's historical scaling rule.

| origin | assembled mix scale | intended legacy mix scale |
|---|---:|---:|
| 2015q2 | +0.329442 | −0.158000 |
| 2015q3 | +0.295809 | −0.277023 |
| 2026q4 | +0.431641 | +0.185999 |

The saved assembled scales match turnover's scales to floating-point precision.
Fixing this wiring alone does not change `best_three`. Fixing bug A DOES affect
the shared factor's rim-mix input, and therefore can change factor turnover and
`best_three` indirectly.

### 1.4 Estimation issue C: residual contrast is not an adjusted coefficient

`shot_quality_forward` demeans the outcome by shooter and game, then takes an
ordinary on/off contrast. It does not residualize the presence indicator.
That is a legitimate candidate predictive statistic, but it is not the
coefficient from a shooter/game fixed-effects regression.

A synthetic example with a known effect 0.100 and unequal on/off exposure by
shooter returned 0.036 from the residual contrast, versus 0.100 from the full
within-shooter coefficient. This is not evidence that its saved forward Brier
gain is fictitious; it limits interpretation and transport of its magnitude.

**Day-one decision:** retain the existing shooting feature, clearly labeled as
a residual on/off predictive feature. Do NOT replace every player's estimator
or rerun the entire shooting pipeline today. Build the bounded diagnostic in
§7; decide on a new production estimator later with its own protocol.

## 2. Schedule, priorities, and stopping rules

| Order | Work package | Indicative budget | Required output |
|---|---|---:|---|
| 1 | Input audit + regression fixtures | 30–45 min | prerequisites and three reproducible findings |
| 2 | Correct mix observations and scaling | 90–120 min | tested functions; explicit new output paths |
| 3 | Full repair ladder and point comparison | 90–120 min | complete quantitative scoreboard |
| 4 | Basketball cases and explanations | 60–90 min | actual lineups, coefficients, mechanism table |
| 5 | Finite-batch interval audit | 45–60 min | current-arm coverage and width tables |
| 6 | Bounded FWL diagnostic | 45–60 min | correct interpretation of shooting estimates |
| 7 | Integrate findings and checkpoint | 30–45 min | short results report and next decision |

Budget is a prioritization aid, not a reason to kill a healthy numerical job.
If behind, finish packages 1–3 and a smaller package 4 before adding anything.
Report deferred work explicitly. Do not call the day complete if required
outputs are missing; leave an exact restart command/task instead.

No recency grid, new hierarchical model, tracking-data work, new rebound model,
or full two-team defensive simulator in this day. A role-freshness diagnostic
is allowed in the case report; implementing another model family is not.

Once a complete run begins, let it finish without repeatedly stopping to discuss
partial results. A smoke test checks execution only; it is never a research
finding. Stop for actual errors, cutoff violations, changed input fingerprints,
nonfinite predictions, or unavailable inputs—not a disappointing interim MAE.

## 3. Package 1: small audit, not a new infrastructure project

### Scope

1. Record `git status --short`, HEAD, active editing ownership, and source paths.
2. Verify existing shot/context/channel caches and coefficient files without
   calling a builder that could recreate a missing file. Consult the manifest
   in `HANDOFF_2026_09_08_OPUS.md` for exact existing cache families.
3. Resolve the full 48-origin schedule and window timestamps from saved cells.
4. Recompute the table in §1.1 from `assembled_cells.csv.gz`.
5. Add focused tests for A, B, and C. The C test must distinguish a predictive
   contrast from an adjusted coefficient, not assert that the two are equal.

### Regression fixtures

- **No true off exposure:** two games. Player 0 plays every shot in game 0 and
  does not appear in game 1. His own shots and teammate shots both occur in
  game 0. Another shooter appears in both games with opposite mix residuals.
  His own-shot residuals can average exactly zero. Player 0 must have zero
  true off attempts and be ineligible for an on/off estimate.
- **Hand-calculated contrast:** include own shots, teammate-on shots, and actual
  team-off shots with distinct residuals. Verify both numerators and both
  denominators, not merely a final effect.
- **Scaling provenance:** changing a turnover-slope fixture must leave every
  mix scale unchanged. A mix-origin fixture must yield the same scale as the
  standalone historical mix calculation for the same coefficient source.
- **FWL scale:** two equally sized shooter groups; player-on proportions 0.9
  and 0.1; shooter baselines 0.2 and 0.6; true added outcome 0.1 when on.
  Residual-on/off gives 0.036; adjusted regression gives 0.1. Continuous
  conditional means are sufficient for this algebraic test.

### Acceptance

Existing saved results reproduce within 1e-8; no source artifact changes.
New tests fail for the intended reason on the old semantics and pass for the
new functions. Missing input files produce a concise prerequisite list.
Do not generate a new parser/cache or spend hours rebuilding old controls.

## 4. Package 2: corrected mix estimator

### 4.1 Observation definition — settled, do not reinterpret

For focal player p, use his team's shots in games where he actually appears,
as in the existing roster eligibility rule. Keep the existing attributed-shot
filter and separate two-point/four-bucket and three-point/two-bucket simplexes.

- **Own:** shooter == p. Exclude these shots from BOTH groups.
- **On:** shooter != p AND p is in the offensive five.
- **Off:** shooter != p AND p is NOT in the offensive five, for that player's
  team in one of those eligible games.
- Opponent shots never enter either group. A whole game missed through injury
  is outside this estimator; do not silently infer roster membership for it.

Efficient aggregate implementation: form existing team totals, plus per-game
own-shooter totals and teammate-on totals. Then:

```
off_count = team_count - own_count - teammate_on_count
off_sum   = team_sum   - own_sum   - teammate_on_sum
effect    = teammate_on_sum / on_count - off_sum / off_count
```

Join by explicit `(game, side, player)` keys. Assert nonnegative counts and
the partition identity; do not repair negative counts with clipping.

Keep the existing shooter-mix baseline (including its prior=40 smoothing),
history window, residual definition, moment centering, and eligibility floor
of at least 200 attempts on EACH side. Do not bundle recency or new controls
into this observation repair.

Persist `n_on`, `n_off`, eligibility, raw effects, shrunk effects, per-bucket
sampling variances, and the cutoff per origin. An unsupported effect contributes
zero increment and an explicit support flag; do not delete that lineup from the
point comparison or interpret zero as high confidence.

### 4.2 Sampling variance — a separately identified correction

The old mix shrinker uses only `variance_b / n_on`, although its statistic is a
difference of means. With corrected counts, use the working approximation:

```
sampling_variance[p,b] = residual_variance[b] * (1/n_on[p] + 1/n_off[p])
```

Preserve the original EB centering/spread rule and zero-sum projection of the
shrunk bucket effects. For unsupported estimates use infinite sampling variance
and zero contribution. Do not replace an unsupported player with NaN in scores.

This is an independent-shot working variance, NOT a proven game-clustered
posterior. Label it accordingly. A later cluster-based model may replace it.
Do not claim the game's uncertainty problem is solved by this change.

To keep attribution clear, produce TWO corrected coefficient sets in the same
data pass: (a) corrected groups with legacy on-only variance, and (b) corrected
groups with both-side variance. The latter is the day-one corrected candidate;
the former is diagnostic only, irrespective of which happens to score better.

### 4.3 Scaling — preserve the actual standalone rule first

Use `mix_points.prior_scale`'s existing definition, not turnover slopes and not
an all-season coefficient fitted after the run:

- x = unscaled raw point contribution of mix above the location-only arm.
- y = actual rating minus the parent's genuinely forward calibrated prediction.
- Accumulate the existing UNWEIGHTED sufficient statistics over eligible,
  completed earlier origins. Keep this convention for the repair comparison.
- At the current origin, compute centered Cov(x,y)/Var(x) from that historical
  state. Cold start or zero variance => zero scale, explicitly logged.
- Compute current predictions BEFORE adding this origin to historical state.
- Eligibility is `window_stop <= current_start`, not simply tag ordering.
- Preserve finite negative slopes in the repair arm. Do not clip their sign
  based on basketball preference or the outcome of this run.

The slope is the legacy rule; its units/optimality are not being newly endorsed.
The raw mix score is before final point calibration and y is on the calibrated
rating scale. Do not silently change this definition during a wiring repair.

Persist per-origin scale, historical cell count, sufficient statistics, latest
eligible window stop, and coefficient-source identity. Standalone mix scoring
and assembled scoring must consume the SAME scales for the same source. Factor
turnover may change allocation, but it must not silently refit a different mix
scale; use the declared location-only reference sequence in both.

### Acceptance tests beyond package 1

- Own shots affect neither on nor off totals when teammate residual inputs
  are held fixed. Swapping team labels or lineup order does not change effects.
- No off exposure => ineligible, even with abundant own shots.
- Increasing only off exposure lowers the working variance when on exposure
  and residual variance are fixed; invalid counts cannot produce finite precision.
- Each conditional mix sums to one; effects sum to zero; shifted attempts remain
  nonnegative and preserve the original total for each shot type.
- Changing this or a future origin's outcomes cannot change the current scale,
  current profiles, current coefficient fit, or current point calibration.
- Leave the two-versus-three split, FTA, turnovers, rebound accounting, assist
  coefficient constraints, and all other parent definitions unchanged.

## 5. Package 3: one complete, attributable forward experiment

### 5.1 Minimal implementation shape

Prefer small keyword-only input/output parameters in existing run functions and
a thin `experiments/influence_repair.py` entry point. Reuse allocation,
calibration, scoring and report helpers. No global monkey-patching of file-path
constants; no duplicated independent version of the full scorer.

If a pure scoring helper is needed for the case panel, extract only the
calculation currently nested inside `assembled.run`. It should accept explicit
profiles, environment, coefficient sources, scale, and lineup IDs; return raw
score plus named intermediate components. Calibration remains explicit outside
that helper. Avoid a new model framework or database/schema refactor.

Output root: `experiments/cache/influence_repair_2026_09_09_v1/` if unused.
If it already exists with different code/protocol, choose `_v2`, etc. Never
overwrite it to make a new implementation look like the same run.

A lightweight manifest is enough: protocol version, relevant source hashes,
input identities/hashes, data epoch, schedule, arm definitions, start/end time,
completion state. Hash immutable large inputs once; don't rehash every quarter.
`--resume` may reuse completed stages only if dependencies match. No elaborate
workflow engine, cloud orchestration, or mid-matrix-fit checkpoint system.

Make missing dependencies fail explicitly rather than silently falling back to
another coefficient source or skipping an origin. Joins must match cell IDs,
lineup IDs, dates, possessions, targets and novel flags—not merely row counts.

### 5.2 Experiment ladder

Run all paths on the same cells and raw target; share input loading when useful.
The list is fixed now, not expanded in response to the ranking.

| ID | Coefficient/scaling source | Purpose |
|---|---|---|
| L0 | archived original predictions | historical reference, no refit |
| L1 | old mix coefficients + correct standalone mix scaling; old factor | isolate wiring bug B |
| L2 | corrected mix groups + legacy variance + source-matched scales | isolate observation bug A from variance change |
| L3 | corrected groups + both-side variance + source-matched scales | corrected day-one candidate |

For L2, score location+mix and location+mix+the unchanged shooting feature; a
separate factor refit is unnecessary for this diagnostic. For L3, refresh the
shared factor using corrected mix coefficients and explicit saved mix sampling
variances. Keep all OTHER factor settings and channel inputs fixed. Record this
sampling-input correction; do not bury it inside the observation-only contrast.

The L3 point table contains these arms:

1. parent;
2. location only;
3. unchanged shooting feature only;
4. location + shooting;
5. corrected location + mix;
6. corrected location + mix + shooting;
7. location + shooting + refreshed factor turnover;
8. all four with corrected mix and refreshed factor turnover;
9. corrected additive saved predictions.

Use fixed names, not `best_*` assigned after viewing the results. Reusing old
coefficient files for unchanged mechanisms is required; no additive, shot-quality,
location-skill, or unrelated channel refits are needed for this comparison.

For all structural arms, retain the parent's deficit as the calibration
covariate, matching the existing experiment. Do not quietly recompute it after
a making change. Report this as a limitation; changing the deficit's accounting
is a separate experiment. The pure panel may expose recomputed demand as a
diagnostic but must not substitute it into the benchmark prediction.

### 5.3 Fairness and reproduction checks

- Same 180-day role / 730-day shooting profiles, dated league environment,
  frozen usage budget, location fallback, and source data as the old experiment.
- Old parent RAW score reproduces to 1e-6 per cell; zero-change/nesting identities
  hold to 1e-9. Also compare calibrated parent predictions, not only raw scores.
- Unchanged parent/location/shooting predictions match saved versions to 1e-6,
  allowing only documented numeric serialization differences.
- Final calibration remains `league + a + b*raw_score + d*parent_deficit`,
  using `fit_point_calibration` with eligible completed history, b >= 0, d <= 0.
- Each arm gets its OWN completed-history calibration; no test-season fit.
- Warmup affects later calibration but is excluded from primary headline metrics.
- Expected full population and novel subset match §1.1 exactly. A mismatch is
  a failure to diagnose, not a new comparison population to silently report.
- Keep old missing-history fallback behavior for unchanged arms and disclose
  support/fallback counts for new effects.

### 5.4 Required live logs and saved results

At EACH completed origin, print elapsed time, dates, cells, possessions,
mix scale/support, parent reproduction error, and a compact table containing:

```
arm | MAE | delta MAE vs additive | RMSE | raw r2 | bias | novel MAE
```

Print running primary totals separately from that origin's metrics. State
`warmup` for 2015; do not mingle it with the headline. No unsupported claim of
a winner while the run is incomplete. Flush each update.

Save cell-level predictions/raw scores, calibration parameters, named point
contributions, scales, coefficient sources, per-origin metrics, per-season
metrics, pooled metrics and completion status.

The final report must include:

- Possession-weighted MAE, RMSE, bias and raw r², all and novel.
- Within-origin-centered r²/correlation as a separate diagnostic: subtract the
  actual origin mean from actuals AND predictions, preserving forecast bias.
  Centering here is metric analysis, not information supplied to predictions.
- Season-paired MAE and MSE differences, their SEM and approximate 95% t
  intervals, with n seasons and seasons improved. Bootstrap seasons if desired,
  not possessions as independent evidence. Eleven seasons is still a small,
  temporally related sample; do not present its CI as exact.
- Differences against BOTH parent and corrected additive. Do not cherry-pick
  whichever reference makes the new arm look best.
- Incremental contribution of factor TO over location+shooting; incremental
  contribution of corrected mix over the matching no-mix arm.
- Mix changes attributable to wiring, group definition, and variance separately.
- Original vs refreshed factor correlations and point contribution sizes.
- Explicit note that all historical windows have been used for development;
  they are not a new independent confirmation set.

### Interpretation locked before running

Smaller MAE/RMSE is better; no numerical gain is required for a bug fix to be
correct. Do not revert the accounting repair because a broken arm predicts
better. A tiny best point estimate with overlapping uncertainty is not a winner.
Nine improving seasons out of eleven is suggestive, not a substitute for the
effect size and uncertainty. Novel rotations are not the same as extreme OOD.

If factor TO supplies no clear new benefit over its inputs, keep it in the
research table but prefer the simpler candidate for the case discussion. Do
not spend the rest of the day fitting more factors or changing its channels.

## 6. Package 4: the basketball report must use the actual candidate

Use the pure scorer from §5.1; do not run the old career-state
`structural_counterfactuals.py` and imply it evaluated the new assembly.
Reuse its named fixtures and resolution helpers where appropriate.

### Frozen first-panel scope

Primary diagnostic environment and fit origin: **2026q4**, the latest frozen
origin in this comparison. Print its actual cutoff date. This is not a claim
that the tool already consumes all data through the end of the 2025–26 season.

First run all slots at that origin's snapshot, including last-observed dates
and effective exposure. Retired/stale players must be labeled as such. Do not
quietly call the resulting Korver state “prime Korver.”

Required cases:

- Jokić / Murray / Gordon / Porter with Korver versus Westbrook in the fifth
  slot. Murray remains in BOTH fives, as Adam requested.
- Distinct five centers: Bogut, Gobert, Looney, Mitchell Robinson, DeAndre Jordan.
- Five guards: Paul, Curry, Lillard, Irving, Young.
- Five Goberts and five Jokićs: clearly labeled illegal-copy stress diagnostics.
- One conventional high-exposure real 2026q4 lineup (select by greatest prior
  exposure at the cutoff, not by its later error).
- Denver's Westbrook / Jokić / Murray / Porter / Braun unit from the existing
  disagreement review, at the matching historical origin(s).

If time permits, add historically dated Warriors death-lineup / 2021 Clippers
small-ball cases using the SAME scorer at the corresponding available origin.
Do not compare their absolute levels across eras without labeling environments.

Historical-season overrides are NOT a new product feature to implement today.
For a prime-Korver sensitivity, use an explicit cached 2016q1 state for Korver's
self-profile AND influence coefficients, rebasing location offsets onto the
2026q4 league curve. All other slots stay at 2026q4. This is a mixed-era research
fixture, not a validated transport model. Omit it with a reason if the existing
state inputs cannot be assembled consistently within 30 minutes.

### Required outputs per lineup and swap

- Exact identities, source origins, last observed dates and exposure/fallbacks.
- Final offensive rating and structural-parent rating; league environment.
- Corrected additive rating and per-player centered offensive contributions
  where the saved additive snapshot supports those same states. Show the league,
  reference-centering and calibration terms separately. Their sum must recover
  the additive prediction. A mixed-era fixture with no matching additive state
  must say unavailable, not borrow 2026 coefficients and call it matched.
  Reuse `asof_additive_reference.centered_score` and the saved prior reference /
  additive calibration, or the existing centered per-player ledger. Never sum
  the raw offensive half of the old fit without reference centering: that would
  reintroduce the level-identification bug fixed before this workstream.
- Allocated attempts by player and location; 2PA/3PA/FTA/TO team totals.
- Parent creation/making, location-conversion delta, shooting-feature delta,
  mix delta, factor-TO delta, calibration intercept/slope, and assist term.
- Reconciliation residual. Sequential mechanism contributions are calculated
  in a FIXED stated order: parent -> turnover allocation -> location -> mix ->
  shooting. Report the nonlinear allocation interaction; do not claim a unique
  causal/Shapley decomposition. Hold the final arm's calibration fixed while
  breaking its raw score into calibrated point contributions.
- Swap's total change, additive swap change, and their difference. Separately
  retain the original within-structural freely-additive profile-sum comparator
  if reused; label it distinctly from the fitted additive benchmark.

### Tests and interpretation

Mechanical invariants are hard tests: permutation invariance, finite rates,
nonnegative attempts, preserved budgets, zero-effect nesting, shared parameters
for repeated copies, and exact explanation summation. Audit implied make
probabilities too: if the shooting bonus makes them leave [0,1], flag a real
structural failure. Do not hide it with a new untested rating cap.

Basketball expectations are diagnostic PASS/FAIL/UNRESOLVED rows, not assertions
the implementor should make pass by adding bonuses:

- Korver should receive more favorable complementarity around Jokić than
  Westbrook relative to the declared additive reference; total ranking is not
  prescribed. One paired difference does not separately identify each absolute
  complementarity residual without a defined zero reference.
- Westbrook should retain his distinct creation/rim-pressure contribution;
  “not a shooter” must not mean “not useful.”
- Five centers should expose missing creation/spacing; five guards expose
  defensive/rebounding limitations. If this offense-only scorer cannot test a
  defensive claim, mark UNMEASURED, not passed.
- Legitimate small-ball is not automatically malformed.
- A location change on an otherwise fixed opportunity should affect scoring
  through the location-specific conversion curve, not disappear algebraically.

Adams/Robinson/Hart are **rebounding attribution diagnostics**, not a demand
to rank their complete lineups. Use the existing channel readouts to show own
boards versus teammate/whole-team influence and note which pieces affect this
candidate's rating. The current assembly does not integrate a new physical
rebound loop: do not pretend otherwise or implement one during this package.

### Failure cases for Adam

For parent, location+shooting, and the two corrected combined arms, rank cells
by possession-weighted squared-error disadvantage versus additive. Restrict
the displayed diagnostic set to >=200 possessions; retain all cells in metrics.
Take the top five from the union, deduplicated; show names, dates, possessions,
actual rating, each prediction, additive player terms, mechanism decomposition,
and available observed channel counts. Also show five largest improvements.

These are deliberately selected failures/successes, not independent evidence.
Reuse existing chronological-half diagnostics only if their data can be joined
without a new possession pipeline. Otherwise do not invent persistence/error
bars. Ask Adam at most two focused basketball questions grounded in these rows.

## 7. Package 6: a bounded shooting-estimator diagnostic

This package is AFTER the full point comparison; it must not block it.

At the 2026q4 cutoff, analyze Jokić, Curry, Murray, Westbrook, Draymond Green,
and Gobert, separately for field goals and free throws. Use all strictly prior
data, as the old feature does; no recency change in this diagnostic.

For each focal player:

1. Restrict to his team's shots in games he appeared in and EXCLUDE his own
   attempts from both groups. Check real on/off overlap.
2. Define y as made minus the strictly-prior isotonic distance expectation
   (FG) or prior league FT mean (FT). Fit the nuisance curve once per cutoff,
   not once per player. Do not use the descriptive full-corpus curve.
3. Define z as the focal player's on-floor indicator for that shot.
4. Residualize BOTH y and z by shooter and game on this SAME eligible sample,
   using alternating projections to convergence, not a fixed eight sweeps.
   Require maximum remaining group-mean error <=1e-10; cap at 1,000 sweeps
   and report nonconvergence rather than returning a coefficient.
5. Estimate beta = dot(z_tilde,y_tilde)/dot(z_tilde,z_tilde). Report no
   identification if residualized presence has effectively zero variance
   (sum(z_tilde**2) <= 1e-10), irrespective of raw exposure.
6. Compare original saved raw statistic, explicit teammate-only residual
   contrast, and FWL coefficient. Changes in eligible population are part of
   the comparison and must be printed, not attributed solely to FWL.

For a cheap uncertainty diagnostic, use a game-cluster sandwich SE for beta:
game scores are sum(z_tilde * residual) within game; sum their squared scores,
divide by dot(z_tilde,z_tilde)^2, with G/(G-1) finite-cluster correction when
G>1. Label this conditional on the fitted nuisance function, not a full
bootstrap of every stage. Report games and exposure alongside the SE.

Validate the implementation against explicit dummy-variable least squares on
small synthetic data, including no within-shooter/game overlap and multiple
teammates correlated with presence. Do not claim game effects control varying
score/clock state or the particular defensive five. FWL is not randomized
assignment and does not by itself solve attribution among co-playing teammates.

Deliver a small table, not a new all-player leaderboard or production fit.
Decision: preserve the existing feature under its correct description, or
recommend a separately designed estimator experiment. No feature replacement
based only on which six names look most basketball-plausible.

## 8. Package 5: honest first interval audit for the current candidates

This is a **future finite-batch outcome interval**, not an interval for a
lineup's latent ability, a causal player effect, or an impossible lineup.
Existing older coverage numbers cannot be copied onto the new scorer.

Use saved genuinely forward residuals for parent, corrected additive,
location+shooting, and the L3 combined arms. No model refits are necessary.

At each origin:

- Use ONLY eligible completed earlier origins' residuals from that same arm.
- For nominal 50/80/95% intervals, use the corresponding empirical quantile
  of absolute residuals as a symmetric radius around the current prediction.
  Use the conservative `higher` quantile convention consistently.
- Stratify calibration by the fixed possession bins [0,100), [100,200),
  [200,400), [400,infinity). Require >=200 historical cells in a bin; otherwise
  fall back to that arm's all-exposure pool, with an explicit flag.
- If the overall pool has <200 cells, mark the interval as unavailable/warmup.
  Do not borrow current outcomes or another arm's narrower residuals.
- Report cell-unweighted coverage and mean width as the primary interval
  statistics; possession-weighted coverage separately. Metrics must include
  counts, fallback rates, all/novel slices, and the fixed possession bins.
- Compare arms on the intersection of interval-eligible cells and print how
  many cells were excluded from this interval diagnostic. The POINT benchmark
  remains the full population; interval warmup is not a product coverage gate.

No claim of formal conformal/time-series coverage: this is a simple rolling
empirical baseline to measure, not a theorem. No minimum-coverage threshold is
chosen after seeing outcomes. If intervals miscover, report it; do not inflate
them on the same evaluation data and announce validation.

Alongside the synthetic basketball panel, provide a support/uncertainty ledger:
source age, effective exposure, unsupported coefficient count, unfamiliar role
assignment, missing defensive/matchup information, and whether any displayed
interval applies to that question. Do not convert these flags into an arbitrary
distance multiplier or fabricated OOD interval. State explicitly: **latent/OOD
uncertainty for the assembled scorer remains incomplete, so no promotion.**

This is progress on the third pillar, not completion of it. If the full day
cannot accommodate it, name it as unfinished rather than reusing old coverage.

## 9. Execution interface and commands for the implementor

The following is the CLI CONTRACT TO BUILD, not a set of commands that exists
at the time this document was written. The final handoff must replace proposed
commands with commands actually exercised.

```
python -u -m experiments.influence_repair --stage preflight --run-dir PATH
python -u -m experiments.influence_repair --stage core --run-dir PATH
python -u -m experiments.influence_repair --stage panel --run-dir PATH --resume
python -u -m experiments.influence_repair --stage intervals --run-dir PATH --resume
python -u -m experiments.influence_repair --stage fwl --run-dir PATH --resume
python -u -m experiments.influence_repair --stage report --run-dir PATH --resume
```

`core` = baseline audit, corrected mix coefficient sets, corrected mix pricing
and source-matched scales, refreshed factor, full point ladder, quantitative
report. No partial-origin research defaults. `preflight` is read-only and must
not initialize the run directory or create a cache. A single `--stage all` may
chain every required stage if already implemented, but it must not add research.

After tests/preflight, a foreground command Adam can run and watch is:

```bash
cd /Users/adam/Documents/basketball
set -o pipefail
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage core --run-dir experiments/cache/influence_repair_2026_09_09_v1 2>&1 | tee /tmp/influence_repair_2026_09_09_v1.log
```

Use a new log name if occupied; do not truncate another running session's log.
An optional detached launch should use the same command without `tee`, e.g.
`nohup ... > UNIQUE_LOG 2>&1 &`, immediately record the real PID, and view it
with `tail -f UNIQUE_LOG`. Give Adam the literal tested command, not ellipses.
Do not poll by `pgrep -f` matching a command line containing its own pattern.
Do not burn model turns waiting for minutes-long jobs: let Adam monitor a
detached run if requested, or perform independent read-only review meanwhile.

## 10. Verification and delivery checklist

Run targeted tests after each coherent code change. Run the full suite once
before the core experiment and once at final integration if code changed.
Do not repeatedly invoke 606 tests for documentation-only edits.

Expected new/changed files are narrowly scoped:

- mix estimator/shrinker and explicit-input runner;
- mix pricing and assembled scoring input/scale handling;
- factor runner's explicit new mix input and variance provenance;
- small reusable scoring/report functions where necessary;
- `experiments/influence_repair.py` and focused tests (split into a small helper
  module if needed for clarity; no generic framework);
- one results write-up, one compact current scorecard, and handoff links.

Before declaring completion:

- [ ] Confirmed A/B failures are reproduced, fixed, and regression-tested.
- [ ] C is accurately labeled; bounded FWL result reported or explicitly deferred.
- [ ] Every required numerical origin finished; no silent missing source/arm.
- [ ] Parent and unchanged mechanisms reproduce; additive comparison is matched.
- [ ] Complete L0/L1/L2/L3 attribution table exists, not only the latest winner.
- [ ] At least the required basketball cases have actual numbers and reconciling
      explanations; qualitative failures remain visible.
- [ ] New finite-batch interval coverage is measured, or listed as unfinished;
      no claim of synthetic/OOD calibration or scorer readiness.
- [ ] All relevant tests pass; actual diff and changed paths reviewed.
- [ ] Old artifacts, data, protocols, feedback file, and page remain untouched.
- [ ] New results include code/input provenance and fully completed run status.
- [ ] Session handoff states editing ownership, what ran, what failed, paths,
      exact next command/task, and whether any job is still running.

Write the substantive result to `reports/influence_repair_2026_09_09.md` and a
short `MODEL_SCORECARD.md`. The scorecard should have one row per candidate and
columns for prediction, basketball cases, uncertainty, defects/limitations,
and status: research-only / candidate / held / rejected. “Implemented” and
“ready for the tool” are different states.

Append a dated correction pointer to the old experiment record and update the
top of `SESSION_HANDOFF.md`; do not edit its original numeric results in place.
Keep the final user summary short: what changed, the comparative numbers,
which basketball behavior improved/failed, what uncertainty is still missing,
and the next ONE research question. Do not finish with a 20-item wish list.

## 11. Next decision after the day—not additional work to start automatically

Choose based on the evidence collected:

- If corrected mix has stable channel signal but fails point/coherence tests,
  investigate how conversion should change for newly induced shots. Do not
  condition attempts on “assisted” labels available only for MADE shots.
- If shooting attribution is highly exposure-sensitive, design a proper adjusted
  all-player estimator with explicit teammate/opponent controls and a matched
  predictive baseline. The small FWL diagnostic is not that model.
- If named failures mostly involve stale roles, specify one prior-only recency
  contrast next; distinguish faster coefficient updating from changing the
  shooter's baseline or league era at the same time.
- If the mean candidates are close and coherent, prioritize joint parameter/
  structural uncertainty and supported-tail validation over another tiny MAE
  contest. Our three standards remain co-equal.

The desired outcome is a small trustworthy candidate and a sharply defined next
question. It is acceptable to discover that a component should be held. It is
not acceptable to call more code, more tests, or a favorable unqualified decimal
place the result of the day.
