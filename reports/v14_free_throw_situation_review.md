# v14 free throws: conditional miscalibration, not a global excess

2026-09-17, Codex. Requested benchmark checkpoint committed as **929f8dd**.
This subsequent investigation is read-only analysis of frozen predictions,
not a new fit, corrected scorer, deployment or change to the experiment.

## Answer

The NN is almost unbiased for FTA across all evaluated possessions, but its
errors have a strong deployment pattern: too many for frequently used fives
and early-game situations, too few for fleeting fives and late-game situations.
These errors cancel in the aggregate. This holds for all three retained arms,
not just the new role-shift/rebound model, and is not specific to team changes.

The relevant target is **attempts**, not free-throw shooting accuracy. These
are the direct NN's event forecasts. Additive predicts points, not a separate
FTA count; HALF has no independently defined blended FTA forecast.

## Population and accounting

All 44 held-out season-quarter windows, 2016–2026; three-seed mean predictions
for ROLE_SL, RB_RENEW_FAC, and RB_RENEW_FAC_SHIFT. Forecasts were already frozen
before each evaluation window. 2,760,546 total possessions; 2,746,029 have valid
grouped FTA labels (99.47%). Keep the original target-specific label mask.

Raw free-throw shot events were joined to cached possession identity and then
to the original game/offensive-five groups. Their counts exactly reproduce
the grouped labels on every eligible group. All 132 arm/origin global bias
values reproduce the original ensemble opportunity report within 1e-7.
This rules out a mismatch between these accounting paths, not upstream
play-by-play attribution error. No database or input builder was called.

Exposure bins use total realized possessions of a five within a season
quarter, including label-ineligible possessions when defining the bin. They
are descriptive outcome-period selection strata, never deployable features
or a coverage gate. Rates below use only FTA-valid possessions.

## Where the overprediction lives

Leading combined arm, RB_RENEW_FAC_SHIFT; FTA per 100 possessions:

| Quarter-lineup exposure | Eligible possessions | Observed | Predicted | Bias | Seasons with positive bias |
|---|---:|---:|---:|---:|---:|
| All | 2,746,029 | 22.504 | 22.602 | +0.098 | 5/11 |
| <50 | 1,739,610 | 23.920 | 22.438 | -1.482 | 0/11 |
| 50–99 | 355,481 | 21.413 | 22.733 | +1.320 | 10/11 |
| 100–199 | 264,579 | 19.875 | 22.768 | +2.893 | 11/11 |
| 200–499 | 285,389 | 18.854 | 23.047 | +4.193 | 11/11 |
| 500+ | 100,970 | 19.169 | 23.278 | +4.109 | 11/11 |

The equal-season mean bias ± season SEM is -1.468 ±0.188 below50,
+4.102 ±0.330 at200–499, and +3.964 ±0.289 at500+. These are descriptive
season summaries, not independent possession-level significance claims.

The primary matched point-evaluation population has 721,190 eligible
possessions and bias **+2.652**. Thus the all-group event scorecard and the
common-lineup point scorecard describe meaningfully different populations.
This does not invalidate either scorecard; it changes how we interpret them.

| Arm | All bias | Matched common bias | Common >=200 bias | Primary transfer bias |
|---|---:|---:|---:|---:|
| ROLE_SL | -0.106 | +2.479 | +3.870 | +4.475 |
| RB_RENEW_FAC | -0.040 | +2.539 | +3.926 | +4.439 |
| RB_RENEW_FAC_SHIFT | +0.098 | +2.652 | +4.010 | +4.496 |

All three overpredict substantial common fives in **11/11 seasons**.
Among q1 common fives with >=200 possessions and no eligible observed opening
team change, combined bias is **+4.533** on30,767 valid possessions. The
transfer primary is **+4.496** on46,848. This is not a matched causal comparison:
the no-move comparator does not impose the transfer protocol's separate
five-game condition and cannot exclude every unobserved/ineligible move.
Nonetheless, the problem plainly exists beyond the transfer cohort.

## Game situation matters substantially

Here Q1–Q4 mean **basketball periods**, not season-quarter evaluation windows.
Early means >120 seconds remaining in that period; late means <=120.

| Situation | Eligible possessions | Observed FTA/100 | Predicted | Bias |
|---|---:|---:|---:|---:|
| Q1, first ten minutes | 586,622 | 16.084 | 22.806 | +6.723 |
| Q2, first ten minutes | 568,256 | 21.239 | 22.441 | +1.203 |
| Q3, first ten minutes | 561,540 | 21.697 | 22.804 | +1.107 |
| Q4, first ten minutes | 536,349 | 23.549 | 22.362 | -1.188 |
| Q4, final two minutes | 129,446 | 40.537 | 22.411 | -18.126 |
| OT, final two minutes | 6,864 | 46.285 | 23.017 | -23.268 |

Each displayed sign except Q2/Q3 early (10/11 positive) holds in all11 seasons.
The most basketball-interpretable large state: offense leading by4–9 in the
final two minutes of Q4 has **75.584 observed vs22.989 predicted FTA/100** on
19,221 possessions. This is consistent with endgame intentional fouling;
foul intent and bonus status are not directly labeled, so it is not proof.

The model supplies a date-frozen lineup forecast, not a clock/score-conditioned
forecast. Its failure to move from early-game rates to endgame rates is therefore
an omitted-context limitation, not an arithmetic bug. This still matters:
lineups experience different mixtures of those contexts, which contaminate
both learned player profiles and interpretation of complementarity.

Q1/Q3 supply50.11% of all eligible possessions,65.25% of matched common,
73.75% of common>=200, and74.91% of primary transfer possessions.
Late Q4/OT supplies4.96%,3.77%,3.17%,2.91% respectively.

This is not just an endgame outlier explanation. A post-readout sensitivity
excluding late Q4/OT leaves common>=200 bias **+4.908** and transfer bias
**+5.235**. Removing the situations where the model underpredicts makes its
remaining overprediction larger. This does not justify dropping those rows.

## How much is the mix, and what remains?

Reuse the prior deployment audit's fixed period × early/late × five
pre-possession margin bins (50 states). Within each evaluation window,
reweight full-population observed state rates to the selected population's
state weights. Aggregate decompositions with selected eligible possession
weights; no future state/rate enters any forecast.

Exact accounting identity for selected-population bias:

`(pred_selected - pred_full) + (pred_full - actual_full)`
`+ (actual_full - state_reweighted_actual_full)`
`+ (state_reweighted_actual_full - actual_selected)`.

| Combined-arm selected population | Predicted composition | Window-weighted full bias | State mix | Within-state remainder | Total bias |
|---|---:|---:|---:|---:|---:|
| Common | +0.296 | +0.155 | +1.180 | +1.020 | +2.652 |
| Common >=200 | +0.370 | +0.223 | +1.909 | +1.507 | +4.010 |
| Primary transfer | +0.246 | +0.344 | +2.187 | +1.719 | +4.496 |

Window-weighted full bias differs from the pooled +0.098 because each selected
population weights calendar windows differently. Coarse state mix accounts
arithmetically for roughly half the selected-population error, but this is
**not a causal fraction explained or a measured forecast improvement**.
The remainder may include finer clock/bonus state, opponents, deployment
selection, player-role misspecification and recording conventions. It is not
identified synergy. The older `ASOF_DEPLOYMENT_AUDIT.md` already found the
same broad issue; this analysis links it directly to the completed neural
campaign's held-out errors and the new substantial-lineup cases.

Margins are reconstructed before each possession from recorded possession
points, not independently verified scoreboards; technical points can be absent.
Ties use possession-id order. All unknown states would remain included.
Raw lineups are generally recorded at possession completion, so substitutions
during an FT trip remain an attribution caveat. No rescrape is justified by
this analysis alone.

## Proposed next experiment: separate environment from foul drawing

I would prioritize a bounded context-aware opportunity experiment before
another large architecture search, then extend to actual opponents.

1. **Freeze a neutral reference.** Distinguish realized-deployment forecasting
   from a product rating under a common game environment. Clock, score and
   team-foul/bonus state describe the environment, not intrinsic player value.
   Estimate any marginalization distribution using strictly prior games.
2. **Start with a simple control.** Fit a shared clock/period/pre-possession
   margin FTA adjustment using historical data only. Retain current player
   inputs and networks; compare with a global-only calibration control.
   Actual future game-state mix may be used in a labeled conditional diagnostic,
   never silently substituted into the frozen pre-quarter lineup forecast.
3. **Then test joint adjustment.** Train a context-conditioned event decoder
   so player foul-drawing and teammate messages need not absorb game state.
   Score all hypothetical fives under the same reference. A constant subtraction
   of4FTA is not acceptable. Preserve FGA/.44FTA/turnover accounting: changing
   FTA changes the available opportunity allocation, not just the point total.
4. **Keep the residual question live.** Inspect remaining errors by prior
   support, role and opponent. Audit bonus availability/FT-trip attribution
   before deciding whether finer labels are worth extracting. Context alone
   has not been shown to solve the within-state deficit or five-center means.
5. **Preserve all three acceptance standards.** On the same causal44-origin
   protocol, report A, oldHALF, retained NN and new direct/half point metrics;
   event errors across exposure/state strata; named and malformed-lineup
   counterfactuals at a common reference; finite-game coverage and separately
   the still-unresolved latent OOD uncertainty. Do not optimize only this cohort.

This is an experiment recommendation, not a frozen specification or launch
authorization. Any refits, new derived training groups and extraction should
be defined in a new protocol/prefix. Do not edit v14 producers or completed
inputs. No model correction is implemented here.

## Reproduction and handoff

New helper `experiments/fta_situation_audit.py`;4 focused tests plus existing
deployment, benchmark and leaderboard tests: **67 pass**. Independent summation
reproduces every saved summary bias; new output receipt and helper hash verify.
All90 original v14 producer hashes pass before analysis.

Completed output: `experiments/cache/fta_situation_2026_09_17_v1/`:
`summary.csv`, `by_origin.csv`, `states.csv`, `coverage.csv`,
`decomposition_by_origin.csv`, `decomposition_summary.csv`, `receipt.json`;
durable verbose `run.log` ends COMPLETE. The receipt hashes all396 read seed
prediction files and other inputs. Original artifacts are untouched.

Reproduction requires a **new** output directory:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.fta_situation_audit --output-dir experiments/cache/fta_situation_NEW
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest tests.test_fta_situation_audit tests.test_asof_deployment_audit tests.test_transfer_role_benchmark tests.test_joint_capability_v14_live
```

No training/background process remains active. Commit929f8dd contains the
preceding benchmark work; this subsequent audit source/tests/docs are a new,
uncommitted block. Generated research caches remain local and unstaged.
