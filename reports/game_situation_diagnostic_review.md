# Game-situation diagnostic: completed first build and readout

2026-09-17. Protocol: `GAME_SITUATION_DIAGNOSTIC.md`. Implemented directly,
without delegation. This is a diagnostic layer, not a new basketball scorer or
an added user-facing input. Existing predictions and original scores remain
unchanged. No neural/additive refits, database access, scraping, input rebuild,
deployment, promotion or commit.

## What was built

Three nested shared situation models, fitted separately before each of44
evaluation quarters (2016–2026):

- **ENV:** dated league environment only. Its standardized target is exactly
  the original observed target; it is the unchanged comparison control.
- **CLOCK:** period and six fixed remaining-clock bins, separately for each
  regulation period and overtime.
- **MARGIN:** CLOCK plus five offense-perspective pre-possession margin bins
  interacting with period/clock. Kept separate because margin may mediate
  lineup quality rather than being a pure external confounder.

Fixed historical window1,095days, half-life365days; hierarchical partial pooling
with500 clock-parent and250 margin-parent exposure units. No tuning/sweep.
Training ends strictly before each origin. Unknown context and unsupported
children fall back to their parents. Each contextual effect is centered to
zero under its target's historical exposure distribution, defining that
origin's average environment. The variables contain no player identity,
opponent, realized foul, duration or future outcome.

Nineteen targets: points, FGA, FTA, turnovers, 3PA, FG%, FT%, six location
shares and six within-location make percentages. Rates/percentages preserve
their own original observation masks and denominators. All point cells remain.

For a held-out cell, subtract its estimated actual-context-versus-reference
offset from its observed target, then compare every frozen model against the
**same** adjusted target. This is equivalent for MAE/RMSE to adding the same
offset to every prediction, but we retain predictions unchanged in the outputs.
Because actual evaluation-period context is used, these are **conditional
diagnostic scores, not improved pre-quarter forecast results**.

## 1. Most substantial-lineup FTA bias is sensitive to clock adjustment

Combined RB_RENEW_FAC_SHIFT NN. Bias in attempts per100 possessions:

| Population | Original / ENV | CLOCK | MARGIN |
|---|---:|---:|---:|
| All matched common cells | +2.652 | +0.734 | +0.694 |
| Common cells >=200poss | +4.010 | +0.995 | +0.913 |
| Frozen primary transfer cohort | +4.496 | +1.207 | +1.090 |

Substantial-lineup FTA RMSE moves5.947→3.851→3.774 under those targets.
The diagnostic no longer points to a universal4FTA excess in intrinsic lineup
foul drawing. There is a residual roughly1FTA/100 bias, and individual errors
remain. Do not convert this readout into a flat correction.

This differs from the previous audit's1.909 state-mix component: the previous
decomposition used coarser two-clock-bin states and contemporaneous full-group
rates; this fitted diagnostic uses finer clock bins and a prior-only historical
reference. They are different reference-specific quantities, not contradictory
estimates of one causal fraction. No causal fraction is established here.

FGA also changes materially: substantial-lineup bias **-1.699→-0.369→-0.415**.
That reinforces why subtracting FTA points alone would be wrong: opportunity
channels shift together with game state.

Other channels do not all improve. Substantial-lineup3PA bias becomes
**-0.892→-1.169→-1.187**, with RMSE4.066→4.167→4.167. Turnover bias
+0.119→-0.037→+0.005, with essentially unchanged/slightly worse RMSE.
Overall FG% bias improves from-0.679 percentage points to-0.219/-0.177,
but that does not identify within-location shot quality. Location-specific
tables are retained: rim make bias, for example, remains about-0.59pp with
CLOCK; long-three mix is underpredicted by about1.13pp. Keep the original
distance-based bin definitions; the c3 label is only the existing <=22ft proxy.

## 2. The relative NN/blend advantage survives

Same5,607 cells and726,364 possessions throughout; pooled point RMSE:

| Frozen model | Original / ENV | CLOCK diagnostic | MARGIN diagnostic |
|---|---:|---:|---:|
| Additive | 10.84099 | 10.78877 | 10.80199 |
| Old HALF | 10.80812 | 10.74994 | 10.76083 |
| ROLE_SL direct | 10.81348 | 10.75293 | 10.76287 |
| ROLE_SL half | 10.78859 | 10.73201 | 10.74363 |
| Renewal FAC direct | 10.80733 | 10.74542 | 10.75486 |
| Renewal FAC half | 10.78462 | 10.72735 | 10.73873 |
| Combined SHIFT direct | 10.79367 | 10.73081 | 10.74068 |
| Combined SHIFT half | 10.77978 | 10.72205 | 10.73364 |

Combined-half advantage versus additive is0.06121 original,0.06672 CLOCK,
0.06834 MARGIN. Equal-season RMSE differences are respectively
-0.05905±0.01331 SEM (9/11 favorable), -0.06489±0.01340 (11/11), and
-0.06656±0.01335 (11/11). These are season summaries, not independent
possession-level significance claims or grounds for scorer promotion.

This does not establish that additive's coefficients encode deployment, but
the NN's advantage is not erased by this shared adjustment. It is slightly
larger. OldHALF remains narrowly ahead of combined-half on novel lineups
(CLOCK11.70566 vs11.70834); combined-half retains its recurring advantage
(10.24470 vsoldHALF10.28844). On the frozen transfer cohort ROLE_SL direct
still leads these candidates: CLOCK6.53424 vsadditive6.79423 andcombined-half
6.62687. The earlier tradeoffs survive rather than producing a new winner.

Do not compare r² across adjusted targets as if the target variance were fixed.
For example combined-half raw r².13034 becomes CLOCK.11882 even though RMSE
falls: standardization also reduces the variation being predicted. Within a
given adjustment all models share the same target and denominator.

## 3. Cleveland remains a real case to investigate

The 2016 Irving/LeBron/Smith/Love/Thompson five remains the largest repeated-unit
weighted HALF-versus-additive squared-error harm in all three diagnostics.
Across its1,564 possessions:

| Combined direct error | Original | CLOCK | MARGIN |
|---|---:|---:|---:|
| Points /100 | -7.502 | -7.977 | -7.960 |
| FGA /100 | -5.673 | -4.067 | -4.209 |
| FTA /100 | +5.647 | +2.031 | +1.801 |
| 3PA /100 | -3.239 | -4.058 | -3.985 |
| FG%, percentage points | -1.340 | -0.869 | -0.705 |

Each event uses its own valid-label exposure, not automatically all1,564.
The situation offset for points is slightly negative, so moving outcomes to
the common reference makes the point underprediction slightly worse. It does
**not** disappear when deployment is accounted for.

Q4's889poss: actual119.460, CLOCK-adjusted119.827, additive116.676,
combined direct111.791, combined-half114.233. Toronto2026 andUtah2019 also
remain second/third in repeated-unit weighted harm. The entire fixed case
library is saved, not just examples selected after this readout.

## 4. What this supports next

Retain this diagnostic alongside the original scoreboard. No need to expose
game-state inputs in the tool or immediately retrain the NN with them.

The next basketball-mechanism review should focus on **persistent action-volume
and shot-mix errors after shared clock adjustment**. Cleveland still gets far
too few FGA/3PA; coarse FT overprediction was partly a distraction from that
remaining failure. Examine the own-profile starting rates, learned context
messages, allocation normalization and renewal budget in those fixed cases,
with both benefits and harms represented. Do not infer a need for a star bonus.

Bonus status and FT-trip attribution remain useful later audits for the
remaining FTA error. Opponent inputs and latent-quality uncertainty remain
larger product directions. This diagnostic does not validate extreme-center
means, causal teammate credit, or OOD intervals. All three standards remain
co-equal; no model is promoted.

## Limits and verification

- Clock/state effects are observational and can absorb lineup-composition
  differences. No weighting can create missing lineup-state overlap. These
  shared partial-pooled models are a sensitivity analysis, not identification
  of context-free player value.
- State uses possession-start clock and reconstructed pre-possession margin.
  Recorded completion lineups and untracked technical points remain caveats.
  Bonus and actual opposing players are not modeled.
- Context-adjusted counts/percentages are residualized diagnostics, not a
  physical event generator.7,280 of308,490 supported target/mode cell entries
  lie outside their physical range after adjustment, mostly sparse percentages;
  they are not clipped. Do not assemble these independently adjusted targets
  into a point ledger. The six adjusted location shares still sum to100.
- Nuisance-only held-out group-state FTA RMSE44.034→43.549→43.258 uses much
  smaller units than lineup-quarter metrics and is not comparable in scale.
- Effective-support fallback is disclosed: no unsupported clock exposure for
  point/FTA targets; one held-out point possession and one FTA possession have
  an unseen fine margin state. One location-conversion attempt has an unseen
  clock state. These inherit parents rather than being removed.

**80 tests pass**, including13 new tests and the existing deployment,
free-throw, transfer and leaderboard suites.3,493,890 source possessions map
to1,539,050 diagnostic group-state rows; point/FGA/FTA/FTM/TO/location ledgers
reconcile exactly on eligible groups.836 dated target fits have strict prior
cutoffs. Independent recomputation verifies all1,116 scorecards, historical
effect centering, raw point/FTA baselines, source/output hashes and six-share
identities. All90 frozen v14 producer hashes unchanged.

## Files and resumption

Source: `experiments/game_situation_diagnostic.py`.
Tests: `tests/test_game_situation_diagnostic.py`.
Completed prefix: `experiments/cache/game_situation_2026_09_17_v2/`:

- `run.log`: durable per-origin progress and final point comparisons, COMPLETE.
- `manifest.json`, `receipt.json`: protocol/code/input/output lineage.
- `fit_rates.csv.gz`, `support.csv`: every shared rate/effect and cutoff/support.
- `nuisance_by_origin.csv`: conditional environment-only diagnostics.
- `cell_diagnostics.csv.gz`: unchanged predictions, raw/adjusted targets,
  context offsets, masks expressed through target exposure, and cohort labels.
- `scorecard.csv`, `by_season.csv`, `point_season_contrasts.csv`.
- `case_library.csv.gz`: fixed transfer/repeated case diagnoses and harm scores.

The failed v1 prefix is preserved. A pandas Series/MultiIndex alignment error
in the FT-percentage output adapter stopped its first origin; fixed by returning
positional arrays, with a regression test. No protocol, input or model changed.
Test log: `/tmp/basketball-game-situation-tests-2026-09-17-final.log`.
Independent audit: `/tmp/basketball-game-situation-independent-audit-2026-09-17.log`.

Reproduce only with a **fresh** output prefix:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.game_situation_diagnostic --output-dir experiments/cache/game_situation_NEW
tail -f experiments/cache/game_situation_NEW/run.log
```

No active process remains. No commit made; preserve the prior uncommitted FTA
audit as well as this new block. Future work should start with the review above,
not rerun this diagnostic or modify completed v14 artifacts.
