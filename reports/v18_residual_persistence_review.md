# V18 residual persistence and future direction

September 30, 2026. Completed diagnostics authorized by Adam following the
[role and volume review](v18_role_volume_diagnostic_review.md).
The [persistence protocol](v18_residual_persistence_protocol.md) was frozen before
its calculations. The later [coupling supplement](v18_residual_coupling_protocol.md)
was frozen after inspecting persistence results and is explicitly result-motivated.
No neural/additive fits, inference, database access, scraping, input rebuild,
promotion, deployment or commit. Original artifacts and producers are unchanged.

## What we learned

The previous decomposition's large conversion residual is mostly a poor target
for a simple recent-error correction. Conversion errors repeat weakly across games;
the NN beats a simple dated shooting estimator; carrying yesterday's miss into
tomorrow's probability makes every tested arm worse in all 11 seasons.

Opportunity errors are more persistent, and game context explains a substantial
part of them. Field-goal and free-throw opportunity errors also offset each other.
The next experiment should therefore investigate **joint opportunity modeling
with shared game-environment effects**, preserving the existing useful conversion
estimator. It should not be another generic conversion/attention sweep or an
isolated free-throw correction. These findings narrow the next experiment; they
do not prove its architecture or promise a point-score gain.

## Scope and information boundaries

Four arms: J_POINT_BOTH, R_ALLOC, R_ROUTE, A_CONTEXT_GATE. Three saved primary
seeds per arm; all 44 primary quarters. Conditional shooting probabilities are
averaged across seeds, and evaluated on actual actor/location attempts. This is
a shooting-probability diagnostic, not a forecast that knows future shot locations.
Point accounting still averages seed expected counts correctly.

Original broad point population: 8,345 cells / 1,013,999 possessions. Decomposition
and game-split work require joint FGA/FTA/location labels: 8,292 cells / 874,715
possessions. All original direct/half cell predictions and point labels were
independently reconciled during extraction; the smaller population does not
replace the original leaderboard. No gate is added to the product.

Player shooting comparisons instead use **all joint-label rows**, totaling
2,214,552 observed FGA. They are not restricted to common offensive fives. Their
weights, populations and units differ from lineup-quarter point errors.

## The current shooting estimator passes useful controls

Two fixed, prior-only controls use a trailing 1,095-day window and 365-day half-life:
league location rates, and player-location rates pooled with 50 league-prior
attempts. Neither has the NN's contextual/opponent inputs; this tests whether a
simple shooting estimator would help, not the causal contribution of NN context.

Lower log loss and Brier score are better; these are losses per observed FGA,
not points/100, r² or percentages of correct predictions.

| Conditional probability estimator | Log loss | Brier score |
| --- | ---: | ---: |
| League by location | .660579 | .233948 |
| Dated player by location, 50-attempt pooling | .658250 | .232872 |
| J_POINT_BOTH | .657272 | .232420 |
| R_ALLOC | .657263 | .232416 |
| R_ROUTE | .657247 | .232409 |
| A_CONTEXT_GATE | .657318 | .232442 |
| J_POINT_BOTH plus previous-quarter residual correction | .658115 | .232810 |

Against J_POINT_BOTH, the dated-player control worsens log loss by .000978
(season-block 95% interval [.000775, .001125]), worse in 11/11 seasons.
The previous-quarter correction worsens it by .000843 [.000793, .000897], also
worse in 11/11. The same qualitative result holds for all four NNs and Brier score.
Do not select R_ROUTE on its tiny descriptive conditional-loss advantage; its
original point result did not establish a win.

The residual correction subtracts the previous quarter's player/location mean
probability error, shrunk by prior attempts/(attempts+100). Only the immediately
preceding scheduled quarter is used; no current-quarter outcome enters it.
It applies to 2,051,623 of 2,214,552 attempts. The result rejects this fixed update,
not every adaptive state model or every stronger-shrinkage rule. New NN fits already
incorporate prior outcomes, so an additional residual update can overreact or
double-count information. We did not tune the constant after seeing it lose.

Global NN calibration is close: reference predicted-minus-observed make rate
is +0.011 percentage points across all attempts. This hides seasonal variation
(−0.478pp in 2016, +0.750pp in 2018, −0.342pp in 2026) and population effects.
On common-lineup rows its conditional FG point bias is −1.030 points/100.
Do not treat that common-lineup bias as a universal shooting-rate deficiency.

Player/location residual correlations between adjacent quarters are small for
the reference: rim .049, paint .038, midrange −.006, long midrange .030, and the
longer-three bin −.004. Support requires at least20attempts in each quarter.
No adjacent pair meets that threshold in the sparse <=22ft three-point proxy;
that is unavailable evidence, not zero persistence. The six distance bins are
not tracking coordinates, and the short-three proxy is not verified corner geometry.
These player correlations are descriptive, with repeated-player dependence.

## Shooting errors repeat much less than opportunity errors

Five fixed random game partitions keep every game intact. A separate chronological
split divides each lineup's games into early and late halves. Main support requires
two games and20joint-label possessions per side. The random splits retain on
average4,235.2cells /618,044possessions; chronology retains5,283/708,378.
These are selected subsets of the8,292joint-label cells, not the original population.

Reference error correlations across game halves:

| Residual | Random games | Early versus late | Random after CLOCK | Early/late after CLOCK |
| --- | ---: | ---: | ---: | ---: |
| Total direct points | .0603 | .0342 | .0565 | .0311 |
| FG conversion conditional on observed shots | .0367 | .0188 | .0372 | .0190 |
| FGA count | .0868 | .0660 | .0716 | .0527 |
| FTA count | .2087 | .1786 | .1151 | .0959 |
| Turnovers | .0689 | .0586 | .0694 | .0583 |

Random conversion correlation has a season-block interval [.0157, .0554];
chronological correlation has [−.0126, .0518]. Within-origin-centered conversion
covariance is4.114 [0.014,8.257] squared points/100 for random splits, but1.655
[−3.874,7.114] chronologically. After CLOCK it is4.331 [−.085,8.701] and1.797
[−3.995,7.413]. There may be modest persistent error; there is not evidence that
the roughly8-point absolute conversion residual is an8-point learnable deficiency.

Remaining opportunity persistence is clearer. After CLOCK, within-origin-centered
FGA covariance is3.448 [2.462,4.457] in squared attempts/100; FTA is5.928
[4.310,7.326]. Their raw counterparts are4.326 and13.836. CLOCK reduces the large
FTA persistence but does not eliminate systematic action-volume differences.

Increasing support to100possessions per half retains538random-split cells on
average /205,008possessions. Conversion correlation rises to.0797 (.0748 after
CLOCK), but the fixed cross-half correction still worsens its MSE. The stronger
support is a different selected population, not a sensitivity with identical rows.

A measured-opponent-balance sensitivity retains pairs whose half-to-half
additive_defense-minus-additive descriptor differs by at most1point/100. It leaves
roughly1,889cells /300,013possessions per random split. Conversion correlation
is.0417 raw/.0411 CLOCK; the overall conclusion survives. This limited descriptor
does not match every opposing player, defensive assignment or other game condition.

Subtracting the other half's residual with n/(n+200) shrinkage worsens point and
conversion MSE. Raw FTA MSE improves by5.624 squared attempts/100, but that apparent
benefit disappears after CLOCK: change +.197 [−.440,.992]. This is within-quarter
diagnostic adaptation using outcomes, never an improved pre-quarter forecast.
The fixed correction is too noisy to use broadly; failure does not establish that
every stronger pooling rule must fail.

All bootstrap intervals resample11seasons with2,000draws, preserving the five
partitions together. They are exploratory, not multiplicity-adjusted hypothesis
tests. Repeated players and historical development reuse limit confirmation.
No naive equal-half reliability correction or theoretical r² ceiling is asserted.

## Game environment accounts for much of the systematic bias

The completed prior-only CLOCK/MARGIN model was reapplied to the current v18
observations, not copied as old cohort offsets. Effects use only dates before each
origin; actual future game context enters only this conditional diagnosis.
The average-environment fan-facing product does not acquire a clock/score input.

Reference predicted-minus-observed biases; count channels are attempts/100,
conversion is its conditional contribution in points/100:

| Population/channel | Original | CLOCK | MARGIN |
| --- | ---: | ---: | ---: |
| Broad FGA | −.843 | +.011 | −.007 |
| Broad FTA | +1.890 | −.025 | −.046 |
| Broad FG conversion | −1.030 | −.361 | −.278 |
| Transfer FGA | −1.538 | −.091 | −.114 |
| Transfer FTA | +4.296 | +.961 | +.842 |
| Transfer FG conversion | −2.530 | −1.537 | −1.375 |
| 2026 FGA | −1.661 | −.691 | −.670 |
| 2026 FTA | +2.751 | +.595 | +.594 |
| 2026 FG conversion | −2.409 | −1.482 | −1.404 |

The transfer decomposition is145cells/39,500joint-label possessions; the original
146cell/47,419possession transfer benchmark remains unchanged. This adjustment
does not make every result better. Transfer direct point RMSE worsens7.174→7.204
under CLOCK despite improved component biases.

The reference's advantage over additive survives shared context standardization.
On identical broad joint-label cells, half RMSE is11.776 versus additive defense
11.874 before adjustment, and11.713 versus11.810 after CLOCK. Thus deployment
context does not explain away the contextual model's entire predictive advantage.
These are conditional scores on modified targets, not new leaderboard gains.

The nuisance effects are observational and can absorb lineup composition;
margin may mediate ability. Historical effects were fitted on target-specific
populations and are applied here to joint-label rows as a sensitivity. Independently
adjusted channel targets need not be physically valid and must not be assembled
into a point generator. This study does not identify context-free causal effects.

## Persistent channel errors substantially offset

The subsequent frozen supplement measures cross-game covariance between the five
exact point components. Reference within-origin-centered diagonal covariances:

| Point component | Cross-half covariance |
| --- | ---: |
| FG conversion | 4.114 |
| Other FG error: volume, allocation and location | 5.550 |
| FT conversion | .094 |
| Other FT error: volume and allocation | 8.558 |
| Saved calibration transformation | .918 |
| Sum of diagonal terms | 19.235 |
| Sum of cross-component terms | −8.703 |
| Total point residual covariance | 10.532 |

Units are squared points/100, not RMSE or an amount of recoverable accuracy.
The largest off-diagonal pair is other-FG versus other-FT, −3.665 in each symmetric
entry (−7.330 combined). Thus improving channels independently can remove offsets
and fail to improve points. This is not proof of intentional model compensation.
The calibration component is highly repeatable because it is a deterministic
transformation; that is not a calibration-bug diagnosis or latent skill error.

Count residuals show the same pattern in different units: cross-game FGA–FTA
covariance is−5.727 raw and−2.867 after CLOCK. Some joint error survives context.
All four arms have similar covariance structure. The supplement's matrix sums
reproduce the independently measured total point covariance exactly.

## Named cases are available for basketball inspection

All650chronological high-support cells per arm are retained, not just selected
tails. Two reference top20lists are provided, ranked by persistent point-error
product and CLOCK-adjusted action-error magnitude. They are outcome-selected
illustrations, not validated acceptance cohorts or reliable selected-tail estimates.

- **2022q1 Houston:** Wood/Theis/Porter/Tate/Green is overpredicted by29.47 and23.98
  points/100 in its early/late halves (165/161possessions). Conditional conversion
  contributes+12.89/+15.33. This is a real big-lineup failure to inspect, not proof
  of a universal center penalty.
- **2023q1 Golden State:** Curry/Thompson/Green/Wiggins/Looney is underpredicted by
  17.60/23.70 points/100 (204/257possessions); conversion contributes−15.62/−25.43.
  A striking selected example does not override the weak population-wide persistence.
- **2025q4 Denver:** Westbrook/Gordon/Jokić/Murray/Braun has CLOCK-adjusted FTA
  errors of−15.57/−13.70 attempts/100 (120/134possessions), despite the overall
  positive unadjusted FTA bias. Its FG-conversion errors change sign. This shows
  why a uniform FT reduction is especially inappropriate.

Metadata-only names are used. Unresolved IDs remain visible (for example2460),
not invented. No injury, coaching or causal trade explanation was added.

## What to build next and what not to do

We now have enough diagnostics to design a focused next experiment rather than
repeat broad architecture searches.

1. **Joint environment and opportunities:** test a shared, prior-only game-context
   nuisance component during fitting so intrinsic lineup channels need not explain
   all deployment effects. At inference, integrate over a declared historical
   reference environment, preserving the simple two-lineup interface. Setting
   mean-centered context inputs to zero is not automatically equivalent to
   marginalizing a nonlinear model. This requires a separately frozen experiment.
2. **Preserve coherent channel accounting:** compare a genuinely coupled
   FGA/FTA/turnover opportunity mechanism against the current retained model,
   with matched point/event losses. Do not subtract a blanket FT offset, fit
   independent channel corrections and assume point gains, or merely retry
   the earlier phase/routing architectures under a new name.
3. **Retain conversion as a strong control:** the NN is not broadly losing to
   simple shooting rates. Prioritize noisy-versus-persistent role uncertainty and
   measured opportunity/transport failures over a more flexible shooting head.
   A richer ability/role state remains possible, but the tested recent shooting
   residual update is not its justification.
4. **Keep uncertainty and coherence explicit:** model game-level sampling variation
   separately from persistent channel discrepancy, with prior-only fitting and
   forward proper-score/coverage checks. Do not add independent component
   variances while ignoring their covariance. Observed residuals cannot alone
   certify synthetic latent-quality intervals or fix five-center mean behavior.

Predictive improvement, faithful mechanisms and honest uncertainty remain co-equal.
The prior legal-center failure and roughly93%coverage of nominal95%finite-game
bands are not repaired by this diagnosis. No new training campaign is launched.

## Artifacts and verification

All paths below are under `experiments/cache/`, each with a durable sibling `.log`:

- `joint_capability_2026_09_30_v18_persistence1`:44completed origins; game/off5
  residuals, exact context offsets, dated shooting controls, proper-score totals,
  player/location records and cutoff audits.
- `joint_capability_2026_09_30_v18_persistence_summary1`: probability tables,
  paired season contrasts, calibration bins, adjacent-quarter player records,
  environment metrics, six split-pair exports, coverage, persistence moments
  and bootstrap intervals.
- `joint_capability_2026_09_30_v18_persistence_audit1`: independent PASS; original
  and joint populations, exact accounting, equal probability denominators,
  independent NumPy covariance reproduction and source hashes.
- `joint_capability_2026_09_30_v18_coupling1`: cross-channel matrices, accounting
  identity, FGA/FTA cross-game comparisons and2,600named arm/cell cases.

Sources: [extractor](../experiments/v18_residual_persistence.py),
[summary](../experiments/v18_persistence_summary.py),
[independent audit](../experiments/v18_persistence_audit.py),
[coupling supplement](../experiments/v18_residual_coupling.py). Completed producers
are frozen; subsequent corrections require versioned outputs/producers.

Nineteen focused tests pass in `v18_residual_persistence_tests4.log`. The full
synthetic summary smoke passes in `v18_residual_persistence_summary_smoke2.log`;
the first smoke used constant half-errors and incorrectly demanded a defined
correlation, so its failed assertion is preserved separately. No real-data run
failed. The initial detached launches did not survive the execution environment;
managed sessions completed extraction, summary, audit and supplement. No active
job remains. Parent/context ledgers reconcile across3,493,890possessions; current
joint-label exposure has zero unknown clock/margin possessions. Every context fit
and dated shooting control passes its strict prior-cutoff audit.
