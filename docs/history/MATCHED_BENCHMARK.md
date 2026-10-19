# Matched additive / structural benchmark — 2026-09-05

Subsequent diagnostic: `DISAGREEMENT_AUDIT.md` and
`reports/matched_disagreement_review.md` expose high-exposure error gaps and
exact player/channel ledgers from these frozen predictions. They do not
replace this benchmark or establish causal explanations for selected misses.

## Protocol, before looking at results

This answers the overdue accuracy comparison, not all three product standards
at once. It must not compare the old lineup-scoreboard correlation with the
new structural correlation: their targets, dates and support differ.

### Arms

1. **Additive:** the incumbent's chemistry-free additive core: individual
   box-score + numeric height/position prior, career residuals, per-season
   residuals with a selected last-season carry, and true-debut career bins.
   No known-pair effects, usage hinges, or coverage gate.
2. **Structural:** the accepted latest-state finite-usage, channel-valuation +
   making score and measured assist-deficit term. No new rebound or creation
   transport modifications in this comparison.
3. **Additive + deficit:** arm 1 plus the exact same structural assist-deficit
   feature. This measures whether its contextual signal adds to a stronger
   player-value backbone; it is explicitly not a pure additive model.

### Strict origins and fitting

- First generate origin 2015 to initialize point calibration, then evaluate
  2016–2026. Every profile, fitted coefficient and calibration row must predate
  the season it predicts. Actual offensive lineups are given inputs, as in the
  existing structural rig; this does not forecast coaching rotations.
- Additive penalties are chosen using a prefix fit through T−2 evaluated on
  T−1, then refitted through T−1. Select on possession MSE, using both sides
  and a league/home baseline available before the selection season. Carry rho
  minimizes that validation loss on the disclosed shrinkage domain [0,1].
- Search the four regularization blocks, including explicit off corners for
  profile/season/experience. Inspect finite winning grid boundaries and expand
  them twice; record any remaining boundary limitation. No test-T outcomes
  participate in selection. Save candidate losses and selected parameters.
- For fitting only, remove each observed training season's season/week league
  mean and season/offense-is-away residual mean. Season sufficient statistics
  are isolated: a prefix never touches later-season target statistics. Future
  evaluation targets do not undergo their own season/week detrending.
- A master ID table may be used solely as a sparse storage coordinate system.
  Before each fit, compact to players observed in that prefix; build profile
  scaling/SVD and numeric-roster scaling on that prefix map only. Unknown
  players use the zero-effect slot. True-debut/height/position are retrospective
  roster metadata, not point outcomes; no time-varying historical roster table
  exists, which remains a limitation shared with the incumbent.
- Restore the last observed season's ordinary league mean to the additive
  offensive sum before its prior-origin calibration. No future league mean
  is used to locate its raw score on the points scale.
- Reuse the additive Schur-complement formulation. Any faster solver must
  reproduce the existing dense `Stack` solve on controlled test problems,
  including off corners and recovery of season effects.

### Same evaluation and calibration

- Use `channel_points_validation`'s identical ordinary-points possession source,
  offensive-five cells, >=50-possession threshold, five game-disjoint half
  splits, and common latest/cumulative profile coverage. Do not silently drop
  a different set of cells for the additive model.
- Use the same expanding, prior-origin, possession-weighted point-fitting
  protocol and calibration cells for all arms: a free intercept and nonnegative
  score slope; structural and additive+deficit additionally contain the
  nonpositive deficit coefficient as their explicit mechanism. Thus the
  calibration *protocol* is identical, while the contextual arms have one
  additional model feature. Report this distinction, not equal parameter count.
- Primary target: raw observed offensive points/100. Secondary: subtract the
  **same pre-origin additive defense estimate** from each arm's target. This
  secondary target is model-adjusted, not ground truth independent of the
  additive estimator. Do not replace it separately for each arm.
- Primary calibration is the existing absolute-level protocol. Also report a
  predeclared shared prior-league-offset sensitivity: subtract the previous
  season's league mean from both prediction and target before fitting the same
  calibration, then add it back. This diagnoses league-level drift; do not
  select the more flattering policy after seeing results.
- Verify that the structural arm's primary original-level metrics reproduce
  `player_state_validation_2026.csv` (latest) on the matched cells.
- Report MAE, raw r², ordinary correlation, calibration slope/spread, and paired
  season differences with season SEM. Pool reliability covariance/variance
  moments before ratios; retain nonidentifiability flags. Break out lineups
  absent from *all* earlier possessions, with the same masks for every arm.
- Use identical game splits for a simple prior-only finite-half interval
  coverage/width comparison. These do not certify latent synthetic-lineup
  intervals or propagate all profile/parameter uncertainty.

No synthetic-panel tuning or HTML change. A predictive winner does not
automatically win counterfactual coherence or calibrated OOD uncertainty.

## Boundary stability audit, specified before the full-run readout

The end-to-end smoke test reproduced the structural control to floating-point
precision. One experience penalty still preferred the bottom after two grid
expansions. Its selection-loss change from 10 to 1 was only about 1.2e-9 MSE,
but this alone does not establish predictive equivalence.

For every finite boundary remaining in the completed full run, hold the other
selected penalties fixed and move the binding value another factor of ten and
one hundred outward. Recompute carry rho on the same strictly prior selection
season and refit the pre-test prefix. Report selection loss and RMS prediction
movement, plus the largest change in the future season's offensive-lineup
predictions **without consulting those lineups' outcomes**. A change below
0.01 point/100 everywhere is numerically immaterial for this comparison; a
larger movement requires expanded selection before accepting the headline.
This is a stability audit, not a claim that a finite optimum became interior,
and it does not select a model using test outcomes. Preserve the boundary flag.

## Completed forward comparison

All origins completed; 2015 initializes calibration and 2016–2026 supply the
11 evaluation seasons. There are **5,774 matched season-lineup cells**, of
which **4,574** had never appeared as a five in earlier possessions. Matched
cells contain 889,496 possessions, **32.22%** of the 2,760,546 future possessions.
The remaining exposure fails the existing profile/lineup sample criteria. This
does not establish performance for all player states or arbitrary lineups.

The structural control reproduces its saved MAE/r²/correlation to <1e-15.
These are possession-weighted summaries of season metrics, not a pooled-across-
eras correlation or r² that could be inflated by league scoring growth.

### Primary: raw points, original absolute-level calibration

| Model | MAE, points/100 | Raw r² | Lineup correlation |
|---|---:|---:|---:|
| Chemistry-free additive core | 7.45360 | 0.02294 | 0.25226 |
| Accepted structural model | 7.47420 | 0.01389 | 0.20506 |
| Additive + assist deficit | 7.45824 | 0.02206 | 0.25084 |

Structural minus additive, paired by season (mean ± season SEM):

- MAE **+0.01430 ± 0.07616**, structural improves 5/11: no established MAE gap.
- Raw r² **−0.00966 ± 0.01531**, structural lower 8/11: the numerical gap is
  not established across seasons either.
- Correlation **−0.04660 ± 0.01075**, structural lower **10/11**: the additive
  model tracks differences in lineup quality more reliably.

These results support an observed near-tie in average scoring error, not a
formal equivalence claim. Similar MAE does not imply identical quality signal.
Pooled-moment reliability correlations are 0.637 additive versus 0.520 structural;
retain the ordinary metrics as the headline because individual reliability
estimates can be unidentifiable.

Adding the deficit feature to the additive model does **not** improve the
benchmark: paired MAE +0.00442 ± 0.00526, r² −0.00083 ± 0.00086, correlation
−0.00133 ± 0.00117. This does not erase the deficit's measured usefulness within
the structural model. It says that usefulness does not automatically transfer
to a different backbone. No automatic hybrid promotion.

### Newly seen lineups and sensitivity checks

On strictly novel fives, primary MAE is **7.62578 additive versus 7.62209
structural**, again tied. Correlations are **0.23691 versus 0.19819**; the
season-paired difference is −0.03951 ± 0.01279, structural lower 10/11.

The shared prior-league-offset sensitivity improves both models' absolute
scoring errors without closing the quality-signal gap: raw-target MAE becomes
**7.39959 additive versus 7.43653 structural**, correlations 0.25226/0.20482.
The paired MAE gap remains inconclusive (+0.02553 ± 0.06877). Novel-lineup MAE
is 7.56250/7.56043. This policy was predeclared, not selected on these results.

On the common opponent-adjusted target, the additive model's advantage is
larger: original-calibration MAE **7.42957 versus 7.61757**, correlation
0.27520 versus 0.22377. Paired MAE gap +0.17707 ± 0.08659. With the shared
league offset, MAE is 7.40936/7.58246. The target subtracts one shared
pre-origin additive defense estimate; it is **model-adjusted**, not independent
defensive ground truth. It therefore supports a sensitivity check, not a
replacement for the raw-target primary result.

### Same-method interval check

Using only earlier-origin errors to construct intervals for finite future
half-samples, 2019–2026 raw-target, original-calibration coverage is:

| Model | Nominal 50% | Nominal 80% | Nominal 95% | Mean 95% full width, pts/100 |
|---|---:|---:|---:|---:|
| Additive | 49.96% | 79.84% | 94.87% | 44.89 |
| Structural | 50.05% | 80.00% | 94.98% | 45.03 |
| Additive + deficit | 50.11% | 79.90% | 94.89% | 44.91 |

Novel-lineup 95% coverage is approximately 95.0% for all three. These wide
intervals concern noisy batches (minimum 25 possessions per half), **not**
latent lineup means. Repeated game splits do not create independent lineups.
This check does not validate synthetic extremes, all parameter uncertainty,
or the actual two-team matchup layer.

### Interpretation and next work

**Numerical audit passed.** Only 2016 and 2026 retained a finite boundary, both
the experience penalty approaching zero. Moving 1 → 0.1 → 0.01 changed future
offensive-lineup predictions by at most **0.00002451 points/100** (all observed
future fives, not just the scored subset). Selection losses reproduce and
improve by <8e-10 MSE on the additional moves. These limits are immaterial for
the reported comparison. Their finite-boundary flags remain disclosed; no
claim of an interior penalty optimum or changed primary arm is made.

The contextual direction is not paying a demonstrated large MAE cost in this
matched test, which matters under Adam's three coequal standards. But the
additive core has a real advantage in distinguishing better and worse lineups,
including previously unseen ones, and is entirely chemistry-free here.

Preserve both controls. Next inspect the recurring disagreements to identify
player-value information the structural score is missing, and test the supported
workload/shot-mix and passing/turnover transport in separately labeled arms
with the miss-conditioned rebound ledger. Do not infer that adding the existing
deficit to the additive core solves complementarity; this test says otherwise.
Do not change the scorer or page on accuracy alone: the remaining five-center,
real-small-ball, and latent/OOD checks still matter equally.

## Reproduce and resume

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.matched_benchmark
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.matched_boundary_audit
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest discover -s tests
```

The benchmark saves validation, selection, all candidate losses, coverage,
intervals, compressed cell predictions and split detail under
`experiments/cache/matched_benchmark_2026_*`. Per-origin fit `.pkl` checkpoints
are reusable only with matching data epoch and both source-code hashes. The
normal command resumes those fits automatically, then reconstructs the same
earlier-origin calibration sequence. Run logs:
`/tmp/basketball-matched-benchmark.log`, `/tmp/basketball-matched-boundary.log`.
The smoke-test prefix is separate and is not additional evaluation evidence.

Core implementation: `matched_additive.py`, `matched_benchmark.py`, and
`matched_boundary_audit.py`. Database-free tests verify the new solver against
the dense `Stack` reference, prefix independence from future IDs/outcomes,
carry selection against direct predictions, calibration offsets, order-invariant
novelty keys, and interval-width independence from current outcomes. The suite
passes **128 tests**. Database, scoring path, exported ratings and HTML unchanged.
