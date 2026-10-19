# Corrected quarterly comparison — completed 2026-09-08

## Outcome

The original 48-origin run completed on Adam's machine. Its apparent structural
lead was caused by the additive offensive-reference defect. The correction and
ALL 48 origins of saved-fit replay are complete under the fixed, post-diagnosis
protocol `ASOF_ADDITIVE_REFERENCE_FIX.md`. No penalty choices or fits were changed.
The replay took **12.56 seconds**, retained **5,607 primary cells / 726,364
possessions**, and preserved all structural predictions exactly. Warmup 2015
is used for chronological calibration, not primary metrics.

| Model | MAE | RMSE | Bias | Pooled correlation | Pooled raw r² |
|---|---:|---:|---:|---:|---:|
| Original additive, retained diagnostic | 8.508273 | 11.267831 | +0.241607 | 0.270083 | 0.049807 |
| Corrected additive | **8.091953** | **10.840994** | −0.548290 | **0.353259** | **0.120432** |
| Structural main, unchanged | 8.146050 | 10.922285 | −0.736273 | 0.337419 | 0.107192 |
| Corrected additive + deficit | 8.092366 | 10.842650 | −0.545233 | 0.352949 | 0.120163 |

Error units are points/100. Pooled r² includes across-era level variation;
it is not directly comparable with annual within-season headlines or older
single-possession detrended r². The centered additive result is not evidence
that the three co-equal product standards should become a single leaderboard.

## Does the small additive advantage hold across seasons?

Structural minus corrected additive, paired over 11 seasons:

| Metric | Mean difference | Season SEM | Descriptive 95% season-t interval | Structural better |
|---|---:|---:|---:|---:|
| MAE | +0.048971 | 0.045073 | [−0.051458, +0.149400] | 5/11 |
| RMSE | +0.080427 | 0.027863 | [+0.018345, +0.142509] | 1/11 |
| Correlation | −0.026206 | 0.007200 | [−0.042249, −0.010163] | 2/11 |
| Raw r² | −0.013933 | 0.004959 | [−0.024982, −0.002883] | 1/11 |

The MAE gap is not established; additive's squared-error/ranking advantage is
more consistent. These paired summaries do not make quarters, shared players
or overlapping training prefixes independent experiments. No multiple-arm
post-hoc winner was chosen.

Pooling covariance and variance after centering within EACH quarter gives
correlation **0.238199 additive versus 0.204000 structural**. Additive has higher
ordinary correlation in 32/44 quarters. Per-quarter correlations are unchanged
by the offset correction; the pooled within-quarter statistic can change
because the rebuilt calibration slopes reweight predicted spreads across
quarters. It is not an average of the 44 correlations.

Novel fives remain essentially tied: **2,073 cells / 226,256 possessions**,
MAE **8.903899 additive / 8.889890 structural**, pooled raw r² **0.100350 /
0.100900**. This slice is particularly relevant to the product, but novelty
among observed lineups does not validate impossible-lineup means or OOD intervals.

## Correction and verification

Each fit's full offensive contribution (identity + rho × season carry + current
experience) is centered on its own strictly prior, offensive-exposure-weighted
league-player reference, using the league baseline's 365-day half-life. Each
past origin retains its OWN coefficients and corrected forecast when calibrating
later origins. Unknown query players remain zero on the centered scale. All
actual query slots were supported; none were filtered. The two corrected
additive arms replace those keys in the NEW run; original additive copies are
retained as `additive_original|base` and `additive_original|deficit`.

The 2022 Q2 failure now has bias **+0.2682**, down from **+12.2365**, and MAE
**8.9523**, down from **15.0146**. Direct possession-level reconstruction, without
the new reference helper, reproduces the reference **35.951474545246604**.
It also reproduces 2026 Q3's **48.811316381768194** reference. The latter high
raw offset demonstrates why merely patching the first bad quarter is insufficient.

**530 tests pass (31.53s).** Eight new focused tests cover the actual failure,
cutoff/future invariance, reference arithmetic, unknown identities, query order,
chronological recalibration and source/output isolation. The full real replay
and independent audit verify all source/fit/bundle hashes, unchanged structural
forecasts/targets/exposures, reference/score arithmetic and calibration histories.
Maximum discrepancies: structural forecasts **0**, prediction formulas
**2.84e-14**, player ledgers **3.55e-15** points/100. The detailed review's channel
ledgers also independently sum to the saved player creation contributions.

Original additive tuning warnings remain: **20/44 primary origins**, 2,586 cells
and 329,013 possessions depend on provisional searches. This correction does
not certify their numerical convergence or retrospectively choose new penalties.
The old source run, original fitting modules and both registered protocol files
are immutable. Future offensive evaluations should use the new centered scoring
helper, not revive the unanchored original runner as a valid comparator.

## Structural mechanisms, without the contaminated comparison

All of these were fixed contrasts and structural predictions did not change:

- Assist deficit over structural calibration: MAE **−0.061910 ± 0.019236**
  season SEM, improves 9/11; correlation **+0.030213 ± 0.006089**, improves 10/11.
- Live versus frozen profiles: MAE **−0.034363 ± 0.020236**, improves 7/11;
  suggestive, not established point-level improvement.
- 365 versus 180 day role weighting: MAE **+0.003348 ± 0.005525**; no bandwidth
  winner established.
- Opportunity calibration over raw: MAE **+0.002408 ± 0.005935**; the earlier
  channel-level gains do not establish an incremental point-level gain here.
- Recent valuation weighting/freshness show no established point improvement.
- Adding deficit to corrected additive is effectively null: MAE paired
  **+0.000395 ± 0.001719**. Keep calibration distinct from complementarity.

## High-exposure disagreement review and next research question

Read `reports/asof_centered_disagreement_review.md`. The screen retains **247
season-five cases / 235,356 possessions** at >=500 possessions and >=20 games.
It averages their quarter-specific predictions and actual rates, not every
possession that lineup played. Screened mean absolute errors are 3.2645 additive
versus 3.5377 structural; structural wins 107/247. This selected high-exposure
population is NOT a replacement for the full forward benchmark.

The report provides the top ten, with exact quarter predictions and full
per-player/reference/channel accounting for the top six. Five of those six
remain worse in early AND late quarters; Minnesota 2022 reverses, so its
full-season gap is not a persistent failure under this check. Selection by
observed errors creates winner's-curse bias; the stability check is descriptive,
not a confidence interval or causal diagnosis.

Largest persistent miss: **2025 Westbrook/Jokić/Murray/Porter/Braun**, 749
possessions / 27 games, actual **126.97**, additive **124.44**, structural
**118.83**. Structural's extra error is **5.61**, present in all three retained
quarters. Its 3PA (30.66 vs 30.04) and FTA (18.62 vs 18.16) forecasts are now
close in this case; turnover is overpredicted (14.10 vs 12.42). Missing scoring
there cannot simply be labeled another blanket three-point/FTA level problem.

Other persistent cases differ: OKC 2019 underpredicts 3PA and FTA substantially;
Chicago 2023 overpredicts FGA/FTA; Atlanta 2016 overpredicts FTA; Cleveland 2016
underpredicts FGA/3PA. They argue AGAINST one universal opportunity offset or a
Westbrook-specific bonus. Next separate opportunity-volume errors from
conversion/shot-quality/valuation errors using this same cohort, then specify
one context/role-response experiment and its contrasting basketball checks.
No new model experiment was launched from these selected outcomes this turn.

## Artifacts and resumption

- Original: `experiments/cache/asof_points_2026/` (48 complete, unchanged).
- Corrected: `experiments/cache/asof_points_centered_2026/` (48 complete, 52 arms).
- Review data: `experiments/cache/asof_centered_review_2026/` (ranked cases,
  quarter players, channel ledgers, opportunity diagnostics and manifest).
- Code: `experiments/asof_additive_reference.py`, `experiments/asof_point_review.py`.
- Logs: `/private/tmp/basketball-centered-replay.log`,
  `/private/tmp/basketball-reference-full-tests.log`,
  `/private/tmp/basketball-centered-review.log`.

The Opus worker hit its subscription session limit (429) after 27 turns and
saved NO edits. No permission denials or spawned agents. Lead implemented and
verified locally; no API fallback. Private audit directory:
`/var/folders/0q/vr0lp8p56s7ddsz7k2d30j100000gn/T/opus-worker-501/run-__jtck1o`.
No worker or model job remains. No commit, push, DB/source-cache mutation,
scrape or scorer/page deployment. Last commit remains `d898865`.
