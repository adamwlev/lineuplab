# Prior-only joint opportunity calibration

*Specified 2026-09-06, before implementation or results. This is a calibration
control, not a new complementarity mechanism or point-scorer promotion.*

## Why this control

`ASOF_DEPLOYMENT_AUDIT.md` shows a substantial deployment-population component
to the FTA gap. A new teammate-response model must not get credit for simply
lowering every recurring lineup's FT prediction. Establish an empirical
calibration baseline on the same historical evaluation population first.
The baseline is conditional on that recurring-lineup population, not proof of
neutral-game or arbitrary-five validity. All three product standards remain.

## Fixed experiment

Reuse completed `asof_accounting_2026` common cells and its recent180_live and
recent365_live current-EB forecasts with the **same historical-frozen usage
budget**. No profiles, source caches or budgets are rebuilt. Include 2015 as
warmup; report the identical 2016–2026 cells. Preserve raw EB as the control.

Represent each predicted lineup's usage mix by four nonnegative components:
**2PA, 3PA, 0.44 FTA, TO**. Their sum is the existing usage proxy. Reweight
their shares with three global log-odds offsets (2PA reference), then normalize
to the unchanged predicted usage total. The four-way representation is the
joint FGA/FTA/TO ledger with 2PA/3PA separated so current shot mix is visible.
It is not a literal count of mutually exclusive physical possession endings;
0.44 is an approximation and rebound continuation remains unresolved.

Fit each profile arm's offsets using only saved forecast/outcome cells from
windows whose **stop <= current start**. Use a fixed 365-day half-life on the
training window's stop date (all cells in that window get that calendar weight),
disclosed as a research candidate, not selected production recency. This uses
fully completed windows; no future lineup outcomes, future state weights or
future population gaps enter the calibration. The input forecasts are the
ones actually made at their own earlier cutoffs, not retroactive profiles.

Criterion: empirical cross-entropy of the four observed usage components,
weighted by their observed usage-proxy totals and calendar weights. This is a
compositional scoring criterion, not a literal multinomial sampling model or
Bayesian uncertainty estimate. Fit only the three offsets: **no player IDs,
pair terms, workload slopes, clock/margin or named-example adjustments**.
Use a fixed 1e-12 guard for log inputs and stable log-sum-exp arithmetic; disclose
guarded/zero components. No hyperparameter sweep. If fewer than 30 completed
training cells are available, use the raw control and disclose the cold start.
Fail on optimizer failure or incoherent input rather than silently selecting
another estimator. The 2015 warmup should prevent cold starts in primary years.

## Acceptance and readout

- Exact raw-forecast and actual-cell reuse; same counts, exposure and dates.
- Output components finite and nonnegative, 3PA <= FGA, and
  FGA + 0.44 FTA + TO equals the original predicted usage to numerical tolerance.
- Appending or mutating current/future-window outcomes or identities cannot
  change current coefficients or predictions. Adjacent completed windows are
  eligible; overlapping/not-yet-complete windows are not.
- Uniform input scaling leaves shares and offsets unchanged; player-slot
  permutations do not change forecasts. Zero offsets reproduce the control
  apart from the explicitly tested numerical guard.
- Synthetic intercept-only examples recover their known offsets; a supplied
  observed usage total is never substituted for the forecast budget.
- No silent clipping/dropping of cells; use source epoch/hash checks, refuse
  existing output prefixes, and mark complete only after all checks.

Report raw versus calibrated FGA, 3PA, FTA, TO, usage, 3PA/FGA and FTA/FGA
MAE/bias, plus four-way cross-entropy. Preserve existing event/ratio metric
weighting and season-paired means/SEM (quarters are not independent replicates).
Save every cell forecast, each cutoff's coefficients and training boundary,
and guarded-input/cold-start diagnostics. Evaluate both bandwidths; choose
neither after reading this experiment. Synthetic tests, then one full small
CSV-only run; no database, scrape, cache rebuild, expensive sweep or page change.

## What comes after

This establishes the amount obtainable from broad empirical recalibration;
even a large gain is **not** a discovery of teammate complementarity. A later
role-response arm must have this same calibration opportunity and freshness,
with player-role context anchored to the player's actual prior exposure.
Design that extension separately. Do not append raw team-channel adjustments
to the point scorer without a player/channel accounting decision. Proceed
with the already-owed quarter point factorial and equally fresh additive
comparator; deployment checks are not an invitation to keep rerunning audits.

## Completed result — 2026-09-06

The single CSV-only run completed in **2.42 seconds**. All **6,179 source cells
per profile**, including 2015 warmup, are retained. Primary evaluation is the
same **5,607 window-lineup cells / 726,364 possessions / 44 windows** in
2016–2026, separately for each profile. The output has 12,358 wide rows with
both raw and calibrated forecasts, not twice as many independent observations.

Every source key, exposure, raw forecast and actual is preserved. Maximum
predicted-usage drift is **8.53e-14/100**. There are **zero guarded or zero
input components**, zero actual-usage-zero cells, and no primary cold starts.
The only two cold starts are 2015 window one, one per profile; all 94 later
fits succeed. The first primary fit uses 572 prior cells. No input profile,
budget, database, source cache, accepted scorer or HTML changed.

### Broad calibration earns a meaningful intermediate gain

For recent180_live, pooled metrics on the identical primary cells:

| Target | Raw MAE | Calibrated MAE | Season-paired MAE change ± SEM | Improving seasons |
|---|---:|---:|---:|---:|
| FGA /100 | 4.55705 | **4.38155** | −0.16903 ± 0.04243 | 10/11 |
| 3PA /100 | 4.63049 | **4.28575** | −0.33954 ± 0.05096 | 11/11 |
| FTA /100 | 6.36623 | **5.19537** | −1.17128 ± 0.09650 | 11/11 |
| TO /100 | **2.48309** | 2.49121 | +0.00811 ± 0.00182 | 1/11 |
| 3PA/FGA, percentage points | 4.70119 | **4.44559** | −0.25498 ± 0.05650 | 11/11 |
| FTA/FGA, percentage points | 7.85213 | **6.30633** | −1.54245 ± 0.11228 | 11/11 |

Usage MAE remains **3.28891**: the budget is unchanged by construction. Its
machine-precision paired differences are not gains or losses. Ratio metrics
use actual FGA exposure, not the event metrics' possession weights.

The four-component cross-entropy improves **1.154870 → 1.153256**; paired
change **−0.001617 ± 0.000198**, 11/11 seasons. This is the specified
compositional score, not a literal sampling likelihood or a point-rating gain.
Turnover MAE gets slightly worse in 10/11 seasons despite its mean bias moving
closer to zero; retain that tradeoff rather than calling every channel improved.

### The broad mean errors nearly disappear, without a future-derived offset

| Recent180 rate /100 | Actual | Raw prediction | Calibrated prediction |
|---|---:|---:|---:|
| FGA | 90.43496 | 89.14916 | 90.64968 |
| 3PA | 32.99379 | 30.91110 | 33.16714 |
| FTA | 20.35646 | 23.70761 | 20.18584 |
| TO | 13.77945 | 13.71437 | 13.76344 |

Thus FTA bias changes **+3.35115 → −0.17063**, 3PA **−2.08268 → +0.17335**,
FGA **−1.28580 → +0.21472**, and TO **−0.06509 → −0.01602**. The three offsets
were fitted separately at each cutoff from completed earlier windows. None of
the future clock/score reweighting from the deployment audit enters this run.
The calibration reduces systematic errors on recurring fives; it does not
identify why their profiles differ from their deployed outcomes.

### Same conclusion for the other disclosed profile bandwidth

Recent365_live FTA MAE improves **6.44721 → 5.21362**, paired
**−1.23174 ± 0.11132**, 11/11 seasons. 3PA improves **4.97342 → 4.39991**,
paired **−0.56887 ± 0.08831**, 11/11. FGA improves 10/11; TO worsens 8/11
(paired **+0.00518 ± 0.00344**). FTA bias becomes **−0.20782** from +3.48531.
Cross-entropy improves **1.155930 → 1.153531**, paired
**−0.002391 ± 0.000342**, 11/11. Neither bandwidth is selected for production.

### Decision: retain both controls, proceed to the point comparison

Keep raw EB and this prior-only calibrated arm. The latter is the stronger
empirical benchmark a future role-response arm must face on this cohort; a
generic FTA/3PA correction is not evidence of complementarity. Do not tune away
the small TO loss after seeing it, add player-specific bonuses, or use these
sample-specific offsets as a finished neutral-game or OOD model.

**Next substantive work is the quarter-origin point factorial and an equally
refreshed chemistry-free additive comparator**, not another aggregate FTA
audit. Before point integration, explicitly decide how team-channel changes
are assigned to player/shot-location creation and making terms; this experiment
does not supply that allocation. Preserve the raw baseline so refreshed player
state, league valuation and opportunity calibration can be distinguished.
The additive fit's partial-season statistics, profile prior, normalization,
penalty selection and calibration must all stop at its actual cutoff. No point
comparison has yet been run. Defense, new-teammate role adaptation and calibrated
OOD uncertainty remain separate required work; all three standards still apply.

### Implementation and independent verification

Opus implemented only `experiments/asof_opportunity_validation.py` and its
synthetic test file, with 28 passing tests and no permission denials or git
changes. Lead review added finite exposure/budget and cached-ratio checks,
exact final source-cell/value reconstruction, intraday cutoff protection,
per-cell guard diagnostics, and extra regression tests. It also removed a
second floor on predicted probabilities during cross-entropy evaluation and
stopped labeling CE as MAE/MSE/bias. These changes preceded the real run.

The module has **33 tests**; the complete suite has **278 passing tests**.
Independent verification (without refitting) checked every saved training
boundary and cell count, the weighted optimum conditions (maximum gradient
**2.13e-8**), and all predictions via direct multiplicative normalization
(maximum difference **4.27e-14/100**). Direct pooled cell MAEs reproduce the
reported metrics. Manifest code/input hashes still match. No jobs remain.

Results: `experiments/cache/asof_opportunity_2026_*` — cells, coefficients,
window validation, season summaries, paired contrasts, and complete manifest.
For cross-entropy rows, use **`score`**; MAE/MSE/bias are intentionally blank.
`predicted_mean` also carries CE and `actual_mean` its observed entropy lower
bound for compatibility with the existing summary machinery. Do not read
those as point or event-count predictions. Raw/calibrated cell rates are per100.
The manifest's `n_primary_cells` includes two profile rows per cell;
`n_primary_unique_cells` is 5,607.

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.asof_opportunity_validation
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest discover -s tests
```

Do not rerun the completed prefix without a reason; it refuses overwrite.
Logs: `/tmp/basketball-asof-opportunity.log`,
`/tmp/basketball-asof-opportunity-full-tests.log`. Worker audit:
`/var/folders/0q/vr0lp8p56s7ddsz7k2d30j100000gn/T/opus-worker-501/run-57e7rvxq`.
