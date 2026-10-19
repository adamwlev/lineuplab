# Additive / structural failure-case review

## Audit design — 2026-09-05

Adam requested concrete, well-sampled lineups where the structural model has
larger error, with each additive player coefficient and the structural scoring
ledger exposed for a joint basketball review. This is diagnosis, not permission
to tune the scorer to named examples.

Use the completed matched benchmark's **raw-point, absolute-calibration** arms.
Keep the original pre-season predictions, profile states and fitted parameters.
Do not refit on the season being diagnosed. A season label is its ending year.

Initial inspection found 271 season-lineup cells with at least 500 offensive
possessions (86 with at least 1,000). The following analysis is exploratory:
the full-season ranking has already been inspected. It is not a preregistered
test on a previously untouched dataset.

- Main screen: at least **500 possessions and 20 distinct games**. Rank by
  `abs(structural − actual) − abs(additive − actual)`, in points/100. Retain all
  screened rows, including cases where structural wins, to expose selection.
- Average all qualifying possessions in the season, rather than combining
  players across years with different pre-season predictions. Count offensive
  possessions, not minutes or both teams' combined possessions.
- Split each lineup's games chronologically at the closest whole-game boundary
  to half its possessions. Show both rates and error gaps, with at least 200
  possessions per half required for a persistence flag. No game crosses halves.
- Separately rank using the first half only and evaluate those selections on
  the second half. This checks regression toward the mean; it does not make an
  already-inspected historical dataset a fresh confirmatory test.
- Bootstrap whole games (2,000 draws, fixed seed) for descriptive 95% ranges
  of the actual rate and error-gap estimate. These are not simultaneous or
  selection-adjusted intervals, causal effects, or synthetic-lineup intervals.
- Show the top six full-season cases, then the strongest remaining cases with
  at least 1,500 possessions and recurring identical fives. Additional cases
  are labeled, not substituted for inconvenient top-ranked examples.
- Reconstruct both predictions exactly. Additive player entries show combined
  profile/career coefficient, carried previous-season residual, career-stage
  term, and their calibrated sum. The checkpoint combines profile and career;
  do not invent separate contributions for those two.
- Structural entries show native usage, finite-budget scaling, each predicted
  channel and its fitted conditional weight, shooting above shot-mix expectation,
  passing supply/demand, and final calibration. Compare predicted event rates
  with observed rates, but do not mistake a conditional regression weight for
  the causal value of generating an event (especially offensive rebounds).

All reconstruction checks must pass before interpreting cases. This work does
not change the accepted scorer, page, database, or source benchmark outputs.

Generated review: `reports/matched_disagreement_review.md`. Complete machine-
readable diagnostic outputs use `experiments/cache/matched_disagreement_2026_*`.

## Completed readout

**258** of the 271 >=500-possession candidates also have >=20 distinct games:
242,128 offensive possessions. All 258 have >=200 possessions in both whole-
game chronological halves. Every score, coefficient sum and observed total
reproduces the frozen benchmark to within 1e-8. No model is refitted here.

The largest six structural-minus-additive absolute-error gaps are:

| Season ending | Five | Possessions / games | Actual | Additive | Structural | Error gap |
|---|---|---:|---:|---:|---:|---:|
| 2025 | Westbrook / Jokić / Murray / Porter / Braun | 766 / 31 | 127.68 | 122.98 | 117.04 | +5.94 |
| 2024 | Irving / Jones Jr. / Dončić / Gafford / Washington | 804 / 39 | 114.93 | 116.44 | 122.12 | +5.68 |
| 2024 | DeRozan / Vučević / Caruso / White / Dosunmu | 923 / 32 | 109.10 | 113.50 | 118.97 | +5.47 |
| 2018 | Valančiūnas / Lowry / DeRozan / Ibaka / Powell | 555 / 35 | 109.19 | 111.93 | 117.16 | +5.23 |
| 2016 | Irving / James / Smith / Love / Thompson | 1,564 / 57 | 119.12 | 117.39 | 112.25 | +5.15 |
| 2024 | Allen / Mitchell / Garland / Strus / Mobley | 854 / 32 | 113.58 | 114.94 | 120.08 | +5.13 |

All six gaps stay positive in both chronological halves. But five of their
six descriptive game-bootstrap gap intervals include zero (Chicago is the
exception). This is useful diagnostic persistence, not six established latent
model failures. The whole-year ranking is selected on the same outcomes.

Separately selecting ten cases by first-half error gap leaves structural worse
in **8/10** second halves; mean gap falls **5.38 → 2.62** points/100. Minnesota
2022 reverses from +6.64 to −6.64, and Chicago 2023 from +6.68 to −1.63. These
reversals belong in the report. The second half is not a fresh prospective
test of a new hypothesis; this historical era has already been examined.

For balance, structural wins 117/258 of all screened cells. Their weighted
MAEs are 3.825 additive and 3.883 structural. These high-exposure, pooled-era
subset values are descriptive and do not replace the season-paired benchmark.

### What the arithmetic establishes

1. **Assist deficit is zero in all six.** None is caused by an overly harsh
   existing assist-deficit penalty. This also exposes how limited that feature
   is: it only prices shortages, not benefits when supply is already ample.
   It does not prove the missing benefit is causal passing value.
2. **Free-throw volume deserves an accounting/transport audit.** Across all
   258 cells, predicted FTA is 24.32/100 versus actual 19.45: bias **+4.874**.
   Season-mean bias is **+4.783 ± 0.416 SEM**, positive 11/11. Total 3PA is
   underpredicted by about 3.16/100. The >22-foot bucket alone has season-mean
   bias −3.151 ± 0.395, negative 11/11. These are the current point scorer's
   intermediate rates, not the separately affine-calibrated channel models.
3. **Dallas/Cleveland 2024 have a visible opportunity error.** FTA forecasts
   are 29.13 versus 17.66 and 22.97 versus 14.17. Both also underpredict TOs.
   Valued with the existing weights, all channel-rate discrepancies sum to
   +3.58 and +2.84 points/100 of their respective +7.19/+6.49 total errors.
   This is an accounting decomposition, not the result of a coherent model
   correction: changing opportunities also changes dependent making terms.
4. **Chicago 2024 is different.** Its channel-rate discrepancies sum to −2.01
   points, despite a +9.87 total overprediction. Its prior-weighted 2P forecast
   is 55.72% versus observed 51.87%, and 3P 36.15% versus 34.23%. Shooting,
   profile transport, valuation/calibration and omitted context—not simply
   opportunity volumes—deserve attention. No mechanism is causally identified.
5. **Do not turn star-lineup misses straight into a “gravity bonus.”** Denver
   2025 shoots 42.54% from three versus a 37.63% prior-weighted prediction;
   Cleveland 2016 shoots 42.57% versus 37.05%. Some of the gap is realized
   shooting above the prior forecast. Sampling, player-state change, shot
   difficulty and teammate effects are not separated by that comparison.
6. **Recurrence is mixed, and all repetitions are retained.** The exact
   Cleveland five is also underpredicted in 2017 (1,525 possessions). Denver's
   Murray/KCP/Porter/Gordon/Jokić five favors additive in 2023 (2,192 possessions,
   gap +3.63) but **structural in 2024** (2,404 possessions, gap −3.02). Cleveland's
   Allen/Mitchell/Garland/Strus/Mobley five has only a +0.12 gap in 2025. A name-
   based permanent correction would already conflict with these examples.

### Two explanation limitations discovered while exposing the ledger

- The code's `c3` label is a **<=22-foot three-pointer proxy**, not measured
  corner coordinates. Many actual corner threes can be in the >22-foot bucket.
  The human review uses distance labels. Do not tell Adam the tool has spatial
  corner-shot or spacing evidence that it does not have.
- The accepted score still uses a negative conditional ORB weight; this is
  not a causal cost of rebounding. The miss-conditioned rebound prototype is
  separate and has not been promoted. Do not silently replace the audited
  scorer with the more coherent experiment.

### Handoff / next decision

The generated review includes **11** detailed cases: top six, three additional
>=1,500-possession cases, and all other screened occurrences of those exact
fives. Each has full additive player coefficients, structural player-state
inputs, channel coefficients and contributions, calibration, chronological
halves, observed shooting, and descriptive bootstrap ranges. Complete CSVs
retain all 258 cases, not just the shortlist.

Discuss the cases with Adam before assigning basketball mechanisms. A useful
next bounded check is the FTA/3PA accounting and prior-profile transport bias,
followed by separately tested supported channel integration. Do not add player
bonuses or tune the structural scorer to this selected list. The original
three coequal standards remain in force.

Implementation: `experiments/matched_disagreement.py`; six database-free tests
in `tests/test_matched_disagreement.py`. **134 tests pass**. Run log:
`/tmp/basketball-matched-disagreement.log`. No jobs remain running after the
completed run; source benchmark, scorer, HTML and database are unchanged.
