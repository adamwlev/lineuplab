# Sol follow-up: finish the influence repair

Prepared by Codex after independently reviewing the completed v2 artifacts.
This is a bounded implementation contract, not a new model experiment design.
Read `AGENTS.md`, the latest `SESSION_HANDOFF.md` entry, and
`NEXT_DAY_MODEL_PLAN.md`. This document specifies the remaining corrections;
the earlier plan's scientific definitions remain binding.

## Outcome and scope

Fix the mix eligibility bug, make the basketball panel use the benchmark's
scoring implementation and arm-specific explanations, and correct the result
interpretations. Finish with a new complete result prefix and a clear handoff.

Adam requested these instructions for Sol. This preparation session makes
documentation changes only. When Adam asks you to implement this contract,
that task includes the bounded corrected-mix/factor fits, complete scoring
pass, and new derived outputs described below. Do not ask again for routine
steps inside that authorized scope.

- Work directly; no Opus or other agents. Establish sole editing ownership.
- Preserve all existing dirty work. Do not commit unless Adam requests it.
- Do not modify anything inside the completed v1 or v2 result directories,
  including manifests. Preserve every original input and coefficient artifact.
- Use `experiments/cache/influence_repair_2026_09_09_v3/` if unused, otherwise
  a new versioned prefix. All new numerical results belong there.
- No scraping, database changes, input-cache rebuilds, additive refits,
  location/shot-quality/unrelated channel refits, new tuning grids, scorer
  promotion, deployment, or changes to `MODEL_FEEDBACK_FROM_CLAUDE.md`.
- Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u`.

The valid location+shooting and additive results can be retained. The mix and
factor corrections must be measured before being called complete. A prior core
pass took approximately four minutes; this is a small repair, not another
research campaign. Do not stop a healthy run to discuss partial metrics.

## 1. Evidence already established by review

Source result directory: `experiments/cache/influence_repair_2026_09_09_v2/`.
All 48 origins match the centered benchmark's identities, dates, targets,
possessions, league levels, and novel flags. Primary is 2016–2026:
5,607 cells / 726,364 possessions; novel 2,073 / 226,256. Four 2015 origins
provide warmup. Original input hashes and saved output hashes match.

Independently reproduced primary results:

| arm | MAE | RMSE | raw r² | novel MAE |
|---|---:|---:|---:|---:|
| parent | 8.1439828452 | 10.9214307921 | .1073313941 | 8.8902831104 |
| location_shot | 8.1312316259 | 10.8964039646 | .1114178671 | 8.867432 |
| saved_additive | 8.0919525369 | 10.8409940439 | .1204320480 | 8.9038988730 |

The preferred location+shooting arm does not depend on corrected mix/factor.
Its annual paired novel-MAE difference is -0.0232708 ± 0.0139763 SEM versus
parent, 9/11 seasons improved, 95% t interval [-0.0544119, +0.0078704]. Against
additive it is -0.0380329 ± 0.0787727, 5/11, interval [-0.2135495, +0.1374837].
These annual averages differ legitimately from possession-pooled metric gaps.

All 3,276 distinct saved interval radii independently reconstruct from prior
completed windows to floating-point precision. The diagnostic FWL calculation
and its explicit Westbrook nonconvergence are not the targets of this repair.

## 2. Fix eligibility before shrinkage and factor fitting

Relevant code: `experiments/mix_influence.py` (`onoff`, `shrink_simplex`,
`mix_sampling_variance`) and `experiments/mix_influence_run.py` near lines 110–125.

`onoff` zeros raw estimates below 200 on or 200 off attempts but returns FULL
counts with `return_counts=True`. The runner passes those full counts into the
shrinker, whose live mask is merely `exposure > 0`. Unsupported zero raw
estimates therefore participate in EB centering/spread/noise and get pulled
toward the fitted center, producing nonzero effects and finite precision.

At 2026q4, v2 incorrectly has 537 unsupported two-point-location estimates and
780 unsupported three-point-location estimates with nonzero shrunk effects.
Example: player ID 44 has only 131 teammate-on two-point attempts and 1,300 off;
his stored corrected shift is approximately
`[.00113607, -.00006838, -.00020479, -.00086289]` instead of zero. Correctly
masking the population also changes supported players' shrinkage estimates.
Consequently, zeroing unsupported final outputs alone is insufficient.

Required semantics, identical eligibility for L2 and L3:

```python
eligible = (n_on >= MIN_PRIOR_ATTEMPTS) & (n_off >= MIN_PRIOR_ATTEMPTS)
```

- Compute and persist that boolean for each origin and shot-type simplex.
- Keep full `n_on`, `n_off`, and `n_own` for auditing.
- Only eligible identities contribute to EB center, spread and noise.
- Unsupported identities contribute exactly zero after all projection steps
  and have infinite sampling variance in BOTH corrected coefficient sets.
- L2 uses legacy on-only variance among eligible identities. L3 uses
  `variance * (1/n_on + 1/n_off)` among the SAME eligible identities.
- Use eligible on exposure for any compatibility `exposure` field consumed
  as precision; retain the full on count in its unambiguous `n_on` field.
- Preserve moment formulas, shooter baselines, history, 200-attempt floor,
  zero-sum constraints, and prior point-scale definitions.
- The factor must consume the corrected stored sampling variance. Padding
  absent identities must not manufacture finite precision.

Prefer a small explicit eligibility argument or clearly masked fitting inputs;
do not change unrelated callers' definitions through a hidden global rule.

Tests must cover the whole observation → shrinkage path, not only raw effects:

1. Zero off attempts, with abundant own and on attempts: both variants remain
   zero/infinite-variance. Own attempts never become off attempts.
2. Positive but subthreshold counts (199 on or 199 off) are unsupported;
   200/200 is supported. Include real nonzero eligible effects so EB centering
   can expose the regression.
3. Adding unsupported identities cannot change supported shrunk coefficients.
4. Counts survive serialization unchanged and stored eligibility/variance/
   coefficient arrays agree. Factor input reflects this same support.

After fitting, assert these invariants on EVERY origin and BOTH simplexes.
Report unsupported counts and the number of violations, which must be zero.

## 3. Share the scorer and separate each arm's ledger

Relevant code: `run_point_ladder`, `_score_current_panel`, and `_calibrated` in
`experiments/influence_repair.py`; existing allocation and scoring primitives.

The panel duplicates the benchmark arithmetic and has drifted. Extract one
small pure scoring function used by BOTH call paths. Accept explicit profiles,
environment, lineup IDs, coefficient inputs, scale, and mechanism switches;
return raw score and mechanism/attempt ledgers. Keep chronological fitting and
calibration outside it. This is a bounded extraction, not a framework rewrite.

### Preserve the benchmark's assist-deficit definition

For EVERY arm use:

```text
prediction = league + a + b * raw_score + d * parent_deficit
```

`parent_deficit` is computed before factor/location/mix/shooting changes. This
is explicitly fixed by `NEXT_DAY_MODEL_PLAN.md` §5.2. The panel currently uses
`turned['deficit']` for all-four instead. Do not change the benchmark to match
that error. Recomputed demand/deficit may be exposed only as labeled diagnostics.

Using the old v2 inputs, a compatibility check should reproduce:

| case | parent deficit | displayed v2 deficit | v2 all-four | benchmark-consistent all-four |
|---|---:|---:|---:|---:|
| five centers | 11.029452 | 10.193841 | 107.612257 | 107.326201 |
| five Goberts | 21.08158 | 20.891253 | 113.049173 | 112.984019 |

Those last-column figures isolate the scorer repair on v2 coefficients; final
v3 factor/mix scores may differ after eligibility is repaired.

### Give the candidate its own attempt and point explanation

The current panel CSV writes factor-and-mix-modified attempts even when the
discussion is about the location+shooting candidate. In the Jokić+Korver case,
the candidate has 12.832761 turnovers/100, but the displayed ledger has
8.950565. This changes the basketball explanation materially.

- Emit clearly keyed `(lineup, arm, slot)` ledgers, or separate explicitly
  named candidate and research-arm files. State event-rate units.
- Location+shooting retains parent attempts and parent deficit. Its location
  and shooting terms change scoring; they do not grant factor turnover gains.
- All-four uses factor-modified attempts and mix-modified locations. Preserve
  scoring's fixed order: parent → turnover allocation → location → mix →
  shooting. Keep the calibration covariate as parent deficit.
- For each arm expose league, raw parent creation/making and valuation
  intercept, sequential increments, calibration intercept/slope, assist term,
  final prediction and independent reconciliation residual.
- Include the conditional interaction where factor reallocation changes
  location/shooting increments. Label path dependence; no causal allocation
  or Shapley claims.
- Retain correctly centered additive scoring and per-player contributions.
- Reconciliation should sum independently emitted ledger fields back to the
  actual prediction. Subtracting an expression from the identical expression
  is not an adequate regression test.

Verification must exercise the SHARED function on saved 2026q4 cells for all
relevant arms, including cells with positive parent deficit. Compare raw and
calibrated predictions to v2 before changing coefficient sources (1e-6).
Then verify v3 core versus panel using v3 coefficients/calibrations. Retain
permutation, copy-sharing, zero-effect nesting, budget, nonnegative-attempt,
and implied-probability checks. Test that the candidate ledger gets no factor
or mix contribution even when those sources are nonzero for other arms.

## 4. Correct the interpretation and fill small reporting gaps

### The Korver check already passed in the parent

At the same frozen 2026q4 state:

- Parent Korver-minus-Westbrook swap: +4.436009 points/100.
- Location+shooting swap: +4.041258.
- Centered additive swap: -1.083802.
- Relative-to-additive difference: parent +5.519812; candidate +5.125060.

Report both rows. The candidate passes the desired direction, but the added
location/shooting mechanisms reduce the existing difference by about 0.395.
Do not claim they newly learned this complementarity. A difference between two
models is also not a separately identified causal interaction or proof of each
pair's absolute bonus/penalty. Retain stale-state labels and Murray in both fives.

### Rebound denominators

`channel_influence` uses misses as rebound opportunities. Adams's 13.599 is
own ORBs per 100 own-team missed field goals, not per 100 possessions. The
offensive/defensive residual-influence columns use corresponding miss
denominators. Rename or annotate columns and report text explicitly. These
residuals do not identify clean teammate facilitation. Preserve the negative
Adams result as an unresolved diagnostic, without calling the entire rebound
mechanism integrated into the candidate.

### Interval summaries

Retain the fixed prior-only quantile method and bins. Show the exposure-bin
table alongside pooled/novel coverage. For v2 location+shooting's 80% intervals:

| possessions | coverage | mean width | fallback rate |
|---|---:|---:|---:|
| <100 | .78745 | 37.74477 | .00000 |
| 100–199 | .79416 | 27.39504 | .07186 |
| 200–399 | .83560 | 22.44002 | .22474 |
| 400+ | .94783 | 27.43037 | .76957 |

The overall .80132 coverage is correct, but sparse high-exposure history causes
wide fallback intervals and considerable overcoverage. Explain that limitation;
do not tune the intervals on these outcomes. Latent/extreme-OOD uncertainty
remains incomplete and cannot be replaced by these future-batch intervals.

Include the actual season-paired novel comparisons in the new report, with
both reference arms, SEM, approximate CI and seasons improved. Also state that
the historical windows have been used in development; they are not a fresh
independent confirmation set.

Derive report numbers from the loaded result tables. The current report builder
hardcodes many v2 metrics and conclusions; regenerating its Markdown table alone
would leave incorrect prose after the new fit. Validate prose against tables.
The final evidence can support holding an arm; do not require the corrected
numbers to reproduce the previous conclusion.

## 5. Run only the work affected by the correction

1. Read-only input/preflight checks. Verify the EXACT cache paths required by
   the loaders exist before invoking code that might rebuild them. Check source
   input hashes and completed v2 output hashes once; record the baseline.
2. Focused eligibility and scorer-parity tests. Resolve failures before fitting.
3. New prefix: refit the two corrected mix coefficient variants over all 48
   origins, then refresh the shared factor using L3. No other coefficients refit.
4. Complete the same point ladder over all 48 origins. It is acceptable and
   simpler to rescore the unchanged controls in the same inexpensive pass;
   verify their predictions against v2. Do not fit additive again. Log readable
   per-origin comparisons and final primary/novel comparisons to additive.
5. Recompute the basketball panel and selected failure explanations using the
   shared scorer. Keep the frozen fixtures and failure-selection rule.
6. Recompute rolling interval tables for changed arms. Recomputing all arms
   together is acceptable if cheap; unchanged arms must reproduce v2 exactly.
7. Reuse the v2 FWL diagnostic with explicit source/hash provenance. It needs
   no rerun. Keep Westbrook's nonconvergence and the 1,000-sweep/1e-10 rules.
8. Write the new report and scorecard, verify final integration, and hand off.

Give the corrected run a distinct protocol/implementation identity. Preserve
the v2 fingerprint; record the repair relation instead of retroactively changing
its meaning. A stage resume must verify dependencies and must never silently
overwrite completed outputs. Keep this lightweight.

Acceptance for unchanged arms: parent, location, shot_q, location_shot,
saved_additive, and L1 controls should reproduce v2 to 1e-6 in every cell.
Archived original prediction columns must remain exact saved references. L2/L3
mix and L3 factor descendants are expected to change; report maximum coefficient
and prediction differences plus the full metrics, not only the best row.

Use the existing `experiments.influence_repair` CLI if practical. The intended
first numerical command, after fixes and tests, is:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage core --run-dir experiments/cache/influence_repair_2026_09_09_v3
```

This is a proposed command for the fixed code, not an instruction to run the
current buggy implementation. Record the literal commands actually exercised.

## 6. Deliverables and stopping point

- Updated narrow model/runner code and meaningful regression tests.
- New complete v3 artifacts with unchanged-control parity, support invariants,
  coefficient provenance and final output hashes.
- New `reports/influence_repair_followup_2026_09_09.md`; keep the original v2
  report as history and append a dated correction link rather than rewriting it.
- Correct `MODEL_SCORECARD.md`, add a dated pointer to the experiment record,
  and update the top of `SESSION_HANDOFF.md`. Preserve old numerical history.
- Run focused tests during implementation and the full suite once at final
  integration. The previous suite had 615 tests; passing those alone did not
  catch the eligibility/scorer errors. Record actual results and diff review.
- Handoff must state paths, what changed, numerical deltas, limitations, any
  omitted required task, editing ownership, whether jobs remain, and the next
  single decision. No declaration of completion with missing required outputs.

Stop after this correction and evidence review. Do not start the proposed
all-player shooting estimator, new role model, rebound model, or uncertainty
model. Those require a separate design decision after the repaired comparison.
