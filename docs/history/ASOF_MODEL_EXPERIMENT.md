# Date-aware contextual model — 2026-09-05

## Agreed direction and staged implementation

Adam wants current league conditions, greater weight on recent player evidence,
and quarter/eighth-season forward evaluation that matches an in-season tool.
Recency recognizes an observed role change; context-dependent role response
must separately predict adaptation to a new five. These are not equivalent.
The three standards in CONTEXTUAL_MODEL.md retain equal standing.

The first bounded milestone is **date-safe snapshots and direct intermediate
evaluation**, not a replacement point scorer. Then use those snapshots for the
league/player factorial point comparison, with equally refreshed additive
controls, before promoting role-response mechanisms. No known-pair residuals.

## Dates and information boundaries

- An `as_of` date means **strictly before that day's games**. Every player's
  counts, shrinkage prior and league estimate use only earlier dates. Missing
  dates are an error, not permission to include a row.
- Four evaluation windows start at the season's first observed game and after
  300, 600 and 900 completed league games. Eighths use steps of 150. Complete
  all games on the crossing date before updating the following day. The final
  window includes the rest of the season, including postseason; window sizes
  are approximate quarters, not quantiles chosen from future possessions.
- The trigger is operationally observable at the time. Appending future games
  cannot change already-triggered boundaries. No game/date crosses fit/test.
- Refit dates, history weighting and forecast horizons are separate settings.
  A short forecast window does not discard all older training history.
- Forecasts are compared on identical future window-lineup cells; report
  exclusions and coverage. Use >=50 possessions per window for this diagnostic,
  not the >=500 full-season criterion used to show individual failure cases.
  Aggregate paired differences by season; quarters are not independent seasons.

## Player-state foundation

Retain the original latest qualifying single-season state as the exact frozen
control. New structural-profile snapshots aggregate individual event counts
before the cutoff with exponential calendar-day weights. Candidate role
half-lives are **180 and 365 days**; shooting uses **730 days**. These are
explicit initial research candidates, not selected production settings. A
broader/nested bandwidth selection is still owed before any promotion.

For each rate, account for weighted observations using effective exposure
`(sum(w * denominator))² / sum(w² * denominator)` before empirical-Bayes
shrinkage. Do not mistake a discounted denominator for an independent sample
size. Shrinkage population and fills also come strictly from the prefix.
Each rate gets its own exposure (FGA, 3PA, FTA, makes, possessions, etc.).

Use all available history with declining weight, retaining players absent in
the current season. Report last-observed date and effective exposure rather
than silently excluding injured/thin-state players. This first structural-only
profile schema is not the full additive box-score prior. It does not model
unobserved injury recovery or create calibrated player-state uncertainty.

The same exponential weighting is available for league usage, 3PA/FGA, FTA/FGA
and shooting baselines. The first intermediate experiment changes **only the
league usage budget** when switching its environment setting; it does not
pretend this adjusts the shot-mix composition or conditional channel weights.
Date-aware shot valuation and explicit historical-to-current rate transport
remain the next point-model stage. No generic z-scoring of all profiles.

## First intermediate experiment (specified before running)

2015 supplies a warmup/diagnostic year; report 2016–2026. Profile candidates:

1. Original `annual_latest` profile, frozen before the season.
2. Recent-180 / recent-365 profiles, each frozen before the season.
3. The same two profiles refreshed at every quarter cutoff.

Cross each with (a) original all-prior preseason league usage and (b) 365-day
weighted league usage refreshed at every cutoff. This isolates refreshing
observations from the change in their weighting; in particular, compare a live
recent profile to the **same weighted** preseason profile, not just to the
different annual-state estimator. The experiment is diagnostic, not bandwidth
selection. All common cells use the same actual future possessions.

Report FGA, 3PA, FTA, TO, ORB, assist/assisted-make rates and team usage, plus
3PA/FGA and FTA/FGA. Keep predicted rates in basketball units. The ratio metrics
separate changed mix from simply changing the total budget. No test-window
calibration or point-target normalization. Record per-window means, MAE/bias,
per-season paired results, player-state exposure, coverage, raw era trends and
epoch/configuration. Also save all cell forecasts for a later case review.

## Must-pass checks

- Future rows, future identities and same-day games cannot affect a snapshot.
- Future games cannot move prior rolling-origin boundaries.
- Whole dates stay together; windows partition a season exactly once.
- A no-decay, common-input structural profile reproduces the existing profile
  builder's matching columns to floating-point tolerance.
- Effective exposures are invariant to multiplying all weights by a constant,
  never exceed raw exposure, and reduce to raw exposure under uniform weights.
- The original frozen model's channel predictions reproduce the current helper;
  the finite usage identity and lineup permutation invariance remain intact.
- No database/source-cache rewrite, accepted-scorer/page change or production
  promotion from this intermediate experiment.

## Completed first milestone

`asof_state.py` implements strict-date player/league snapshots, weighted-rate
effective exposure and causal rolling-origin starts. `asof_channel_validation.py`
runs the intermediate factorial. The 2025 smoke and full 2015–2026 run both
completed. The full run took 52 seconds; no job remains running.

No-decay snapshots reproduce the existing structural-profile columns to a
maximum difference of **2.22e-16** on the real-data prefix check. Thirteen new
database-free tests cover future/same-day exclusion, future identities,
effective-exposure invariance, old EB reproduction, missing-date rejection,
inactive-player retention, lineup permutation and usage conservation, causal
quarter/eighth starts, ratio invariance and correct metric weighting.
The complete suite passes **147 tests**.

### Coverage and interpretation

2015 is diagnostic warmup. The 2016–2026 readout contains **44 future windows**,
**5,607 window-lineup cells**, **726,364 / 2,760,546 possessions (26.31%)**.
These are not 5,607 independent fives: the same five can occur in several
windows. Every arm is evaluated on the same cells and outcomes. Counts and
coverage are different from the annual and >=500-possession disagreement
reports; do not directly compare their metric levels.

The live snapshot builder can cover **34.64%** of future exposure after the
same >=50-possession window-lineup threshold, versus 26.31% for the annual
state control. Primary accuracy still uses their intersection. This is not a
full coverage solution or proof of accuracy on the newly covered states.

### Fresh observations improve shot mix

With the original league usage budget held fixed, the 180-day role / 730-day
shooting candidate has the following possession-weighted errors:

| Intermediate target | Same weighted profile frozen preseason | Refreshed quarterly | Paired season MAE difference ± SEM | Improving seasons |
|---|---:|---:|---:|---:|
| 3PA per 100 | 5.09787 | 4.63049 | −0.46147 ± 0.06309 | 11/11 |
| FTA per 100 | 6.49299 | 6.36623 | −0.11642 ± 0.07604 | 9/11 |
| TO per 100 | 2.51974 | 2.48309 | −0.03598 ± 0.01243 | 10/11 |
| 3PA/FGA, percentage points | 5.20208 | 4.70119 | −0.49425 ± 0.06560 | 11/11 |

The 365-day role candidate also improves 3PA when refreshed: paired MAE
**−0.39996 ± 0.05145**, 11/11; turnovers **−0.03126 ± 0.00946**, 10/11.
Thus the refresh result is not confined to one candidate bandwidth.

Against the *original annual latest-season profile*, recent-180-live improves
3PA MAE **5.03821 → 4.63049**, paired **−0.40659 ± 0.05797**, 11/11. Turnover
MAE **2.53437 → 2.48309**, paired **−0.05068 ± 0.01457**, 10/11. FTA gain is
not established: **−0.05880 ± 0.08701**. The recent-365-live comparison against
the annual control is weaker for threes; no bandwidth has been selected for
production, and shooting's 730-day bandwidth has not been selected either.

The pure-refresh 180-day 3PA MAE improvement grows through the season:
quarter 1 **0.000** (identical inputs by construction), quarter 2 **−0.461**,
quarter 3 **−0.611**, quarter 4 **−0.730** points of event-rate MAE. These
are season-mean within-quarter differences, not extra independent trials.

### Fresh total usage is not sufficient era adjustment

Replacing only the frozen all-prior usage pool with a live 365-day league
estimate cannot change either 3PA/FGA or FTA/FGA; the code verifies this
algebraic invariance. For recent-180-live, it improves FTA MAE by
**−0.09090 ± 0.00787**, 11/11, but worsens FGA by **+0.19232 ± 0.02278** and
3PA by **+0.07733 ± 0.00578**, both 11/11. Total-usage MAE is essentially flat.
This is reallocation still needing work, not successful shot-mix era transport.

FTA bias remains **+3.35/100** in the recent-180-live / original-budget arm,
almost identical to annual_latest on this same population (+3.34). This does
not contradict the earlier +4.87 high-exposure audit: it is a different sample.
3PA bias improves from −2.40 to −2.08/100, but is not eliminated.

### What is and is not earned

- Date-aware profile refresh has direct intermediate support. Mere changes to
  frozen profile weighting are not a substitute for observing the new season.
- The result does **not** establish point-score improvement, calibrated OOD
  uncertainty, counterfactual role adaptability or a new winner over additive.
- The current league experiment updates only usage, not conditional shot
  weights, location-specific shooting expectations or profile-to-current-era
  mix transport. Keep that scope explicit in any summary.
- All three product standards, no primary known-pair chemistry, and the fixed
  original scorer/page remain unchanged.

## Resume here

**Latest update 2026-09-07:** the additive prior-edge follow-up is complete
(<=0.000495 pts/100; retain prior=1), and `ASOF_POINT_INTEGRATION.md` implements
and verifies the structural player/channel bridge on every saved common cell.
446 tests pass; all jobs finished. Next is the resumable quarter point runner,
with shared prior-only calibration and league controls, not another accounting
audit. No point comparison or scorer promotion is claimed.

**Latest update 2026-09-07:** `ASOF_ADDITIVE_TUNING.md` completes quarter-matched
selection and one 2026 Q3 fit/selection/refit pilot (253.7s; 5,760 candidates).
387 tests pass. The last prior-penalty expansion moves predictions 0.004438
pts/100 but stays at a finite edge; preserve its provisional label. Next is
the documented 90-second one-axis sensitivity, not a repeat of the full pilot.
No target-window score or structural comparison yet. Player/location accounting
and shared league/calibration controls still require explicit integration.

**Update 2026-09-07:** `ASOF_ADDITIVE_FOUNDATION.md` completes the date-safe
chemistry-free additive fitting/validation primitives, not the benchmark run.
All 318 tests pass and a bounded real-cache smoke passes. Prior-window tuning,
carry policy, league/calibration matching and point orchestration remain to be
specified/integrated. No bandwidth selection or accuracy gain is claimed.

**Update 2026-09-06:** the strict-date league conversion/valuation helper and
joint accounting diagnostic are complete in `ASOF_ACCOUNTING_AUDIT.md`.
Reconstruction/shrinkage does not explain the FTA bias. Read that audit and its
completed follow-up `ASOF_DEPLOYMENT_AUDIT.md`: clock/score reweighting reduces
the descriptive population gap by 1.190 FTA/100, leaving 1.037 within-state.
`ASOF_OPPORTUNITY_EXPERIMENT.md` completes the prior-only four-way opportunity
calibration control (FTA/3PA MAE improve 11/11; small TO loss). Retain both
raw and calibrated controls without labeling the gain complementarity. The point
factorial, equally fresh additive comparator and role-response integration
below remain pending; no original experiment should be rerun without a reason.

1. Add strict-date, recent league shot-valuation/conversion estimates and audit
   the FGA/FTA/TO composition jointly. Do not use total scaling as a substitute
   for shot-mix adjustment or graft a learned FTA correction onto a broken
   opportunity identity. Retain the existing rebound-accounting caveat.
2. Build the quarter-origin point factorial with independently refreshable
   league environment and player states, prior-only calibration and bounded
   bandwidth selection on completed earlier windows.
3. Give the chemistry-free additive comparator the same refresh opportunities.
   Its partial-season Gram block, profile prior, training normalization,
   penalty selection and calibration must all stop at the actual cutoff.
   Do not reuse the old fractional evaluator's global normalization; its
   window/linear algebra ideas are useful, not its unmodified target setup.
4. Only then integrate supported workload/shot-mix and passing/TO response;
   keep refresh effects distinct from adaptation to new teammate contexts.
5. Eighth-season sensitivity requires a same-population comparison: simply
   halving window size and comparing different >=50-possession cells is unfair.
   The origin helper already supports eighths; no eighth-season run is claimed.

Commands (completed results need not be rerun):

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.asof_channel_validation
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest discover -s tests
```

Saved outputs: `experiments/cache/asof_channels_2026_*` (validation, seasons,
paired contrasts, coverage, window starts, league environments, raw era trend,
compressed cell forecasts/player snapshots and a completed epoch/code manifest).
`asof_channels_smoke_*` is separate and not additional evidence. Logs:
`/tmp/basketball-asof-channels.log`, `/tmp/basketball-asof-smoke.log`.
