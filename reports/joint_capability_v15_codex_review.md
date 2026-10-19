# v15 independent review — defense helps; the adapter's point advantage is not established

2026-09-18. Completed research review, not scorer promotion. Read alongside
`JOINT_CAPABILITY_V15_EXPERIMENT.md` and `CONTEXTUAL_MODEL.md` §2.

## Bottom line

Actual opponents are useful information. The old offensive NN/blend plus the
shared additive defensive adjustment captures most of the improvement. The new
defensive NN learns useful event responses, particularly defensive rebounding,
but has not established better point prediction than those equally informed
controls. This is progress toward the original two-lineup product, not proof
that a small adapter over frozen offense is its final architecture.

Retain D_MAIN_RB as the simple mechanism candidate and D_CROSS_RB as a channel
challenger. Retain old NN+D for novel-lineup RMSE and old HALF+D as the essential
combined control. No winner is promoted, and no frozen protocol was changed.

## 1. Completion and independent verification

Production `experiments/cache/joint_capability_2026_09_17_v15_prod` completed
all576 cases: four arms × three seeds ×48quarter origins. Its wrapper finished
2026-09-18 at09:16:54 Pacific after48,959seconds (13h36m); final state is
`ANALYSIS_COMPLETE`. No new model fit was needed for this review.

New, separate derived outputs:

- `experiments/cache/joint_capability_2026_09_18_v15_codex_review`:
  independent case/control/calibration/score/interval/fixture audit,
  seed and season comparisons, channel contrasts and calibration sensitivity.
  Durable `review.log`, final `receipt.json` COMPLETE.
- `experiments/cache/joint_capability_2026_09_18_v15_group_review_v3`:
  independently replayed matchup/group populations and matched parent-event
  comparisons. Durable `analysis.log`, final receipt COMPLETE.

Checks passed:89 frozen producer/protocol hashes,1,106 saved-source hashes,
input/control receipts, exactly576 case identities and their file receipts,
prior-only calibration replay, saved inner/final cutoff and normalizer dates,
finite weights, true minimum-validation-loss selection and exact final lengths,
native event/point accounting, zero-adapter parity, permutation invariance,
FT-conversion invariance, monotone recovery, all54 scorecards,134,568 saved
interval rows,2,004 fixture seed rows and margin antisymmetry. Original report
hashes remained unchanged. No selected fit reached the96-epoch cap; median
selected epochs MAIN10.5, CROSS12, MAIN_RB11, CROSS_RB14.

The group reader had two failed analysis-only attempts, preserved under
`...v15_group_review` and `...v15_group_review_v2`. First it compared a
three-seed parent replay against seed17 rather than the mean; second it
incorrectly assumed that every >=50-possession offensive five belonged to the
historical primary cohort. Both assertions correctly stopped those analyses.
Neither was a training bug or an edit to original artifacts. The successful
reader averages matching seeds and explicitly separates the populations below.
Empty ten-player populations in some quarters produce undefined diagnostic
metrics/warnings, not missing fits; pooled sufficient-statistic totals remain
valid. Do not interpret their NaNs as zero error.

## 2. What is being compared?

The frozen offensive backbone is v14 RB_RENEW_FAC. MAIN adds defender-profile
mean/SD effects on action rates, shot location and conversion. CROSS also lets
those changes depend on each attacker's profile. RB adds defensive recovery
competition. This is not a jointly retrained offensive/defensive network, and
there are no inferred individual assignments or known-pair chemistry terms.

Let A be corrected additive offense, N the frozen offensive NN, D the common
prior-centered additive defensive adjustment, and P a new adapter prediction:

- `additive_defense` = A+D; `nn_defense` = N+D.
- `parent_half_defense` = .5(A+N)+D.
- New `half` = .5(A+D+P).

Every forecast here knows the **actual opponents encountered**. The comparison
is conditional on their realized mix, not a pre-quarter schedule forecast or
the fan tool's prior-average opponent. The original A and N retain their
offense-only calibrations when D is added; P has its own prior-only calibration.
That distinction is audited, not hidden, and motivates §4.

### Population qualification

Primary remains the exact historical matched cohort:44quarters in2016–26,
5,607 offensive-lineup-quarter cells,726,364 possessions;2015 is warmup.
There are2,073 novel cells/226,256 possessions and3,534 recurring/500,108.
Novel means the offensive five was not previously observed; it does not mean
an unobserved ten-player matchup or a new player.

This is **not all possessions, nor all >=50-possession offensive fives**.
The inherited source in `asof_channel_validation.py` intersects profile-support
masks across the old profile streams; `asof_point_benchmark.py`, the influence
repair and subsequent NN versions preserve those cell identities. The new
architectures still score broader data. For transparent sensitivity, this
review separately reports all8,345 offensive fives with >=50possessions
(1,013,999possessions) and all718,526 matchup rows (2,760,546possessions).
The original matched cohort is retained for historical comparability, not
endorsed as a future coverage gate. A new broad primary cohort, including thin
and debut support, should be registered before another campaign.

## 3. Forward points: useful opponent information, small incremental NN result

Original registered forecasts, three-seed means, possession weighting. Units
are points/100; lower RMSE/MAE is better. These are pooled metrics, not averages
of quarterly r² values.

| Forecast | RMSE | MAE | r² | Correlation |
| --- | ---: | ---: | ---: | ---: |
| Additive A |10.84099|8.09195|.12043|.35326|
| Additive + defense |10.78699|8.06608|.12917|.36993|
| Frozen NN N |10.80733|8.06304|.12589|.35866|
| Frozen NN + defense |10.75679|8.05367|.13404|.37326|
| Old HALF |10.78462|8.03744|.12956|.36319|
| Old HALF + defense |10.73215|8.01862|.13801|.37881|
| D_MAIN direct |10.78361|8.05035|.12972|.36328|
| D_CROSS direct |10.79839|8.05969|.12733|.36004|
| D_MAIN_RB direct |10.78017|8.05261|.13028|.36395|
| D_CROSS_RB direct |10.80348|8.06541|.12651|.35853|
| D_MAIN half |10.72777|8.00180|.13871|.37664|
| D_CROSS half |10.72990|8.00230|.13837|.37603|
| D_MAIN_RB half |**10.72573**|**8.00072**|**.13904**|.37688|
| D_CROSS_RB half |10.73086|8.00300|.13821|.37528|

D_MAIN_RB half versus old HALF+D is only−.00642 RMSE, with a10,000-resample
season-block95% interval **[−.04077,+.02369]**, and4/11 season RMSE wins.
Its MAE difference is−.01790 [−.04895,+.00995]. Neither is established.
All four direct adapters trail N+D in pooled RMSE; MAIN_RB trails by+.02338.
All12 arm/seed direct comparisons also trail the corresponding N+D control.
MAIN_RB's half improvement versus old HALF+D has the same sign in all3seeds,
but this does not remove season uncertainty. None of the eight main all-cell
direct/half contrasts survives the descriptive Holm sensitivity.

The new blend beats opponent-blind additive by−.11526 RMSE
[−.15389,−.07448],10/11 seasons, but that is not the incremental value of a
learned matchup mechanism. Against A+D the difference is−.06126
[−.11412,−.00981], with7/11 season wins: still useful evidence for retaining
the offensive NN in a blend, not proof of the new adapter over old HALF+D.
Intervals are nominal, correlated historical comparisons with only11season
blocks; selecting the observed best arm adds optimism.

### Novel versus recurring

| Forecast | Novel RMSE | Novel MAE | Recurring RMSE |
| --- | ---: | ---: | ---: |
| Additive |11.85302|8.90390|10.35068|
| Additive+D |11.77930|8.86462|10.30671|
| Frozen NN+D |**11.68172**|8.78505|10.31112|
| Old HALF+D |11.68922|8.77171|10.26990|
| D_MAIN_RB direct |11.75231|8.82379|10.31028|
| D_MAIN_RB half |11.70240|8.76357|**10.25336**|

The new half has slightly better novel MAE but worse novel RMSE than the fair
controls. It is not an across-the-board novel-lineup advance. Its overall
improvement is concentrated in recurring lineups.

### Broader matchup populations

These are separate targets/populations, not interchangeable scorecard rows.

| Population | Cells | Possessions | A+D RMSE | N+D RMSE | Old HALF+D RMSE | MAIN_RB half RMSE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Every matchup row |718,526|2,760,546|59.69766|59.68725|**59.68385**|59.68544|
| All offensive fives >=50 |8,345|1,013,999|11.17892|11.11455|**11.10511**|11.10966|
| Defensive fives >=50 |8,340|1,010,779|**11.11108**|11.16634|11.12453|11.15020|
| Ten-player units >=50 |453|32,664|**14.32182**|14.46913|14.36756|14.43696|
| Game aggregate |14,157|2,760,546|8.56722|8.55190|**8.53649**|8.55415|

All-row errors are large because many matchup rows contain only a few
possessions. The game aggregate pools both teams' offenses and is **not** a
game-margin forecast. Even on the ten-player population, none of the four new
half forecasts beats A+D or old HALF+D in pooled RMSE. There is no hidden
large point win at finer matchup resolution.

## 4. Much of the small headline edge is level calibration

MAIN_RB half's bias is−.59882 versus old HALF+D−.81521. Decompose the MSE
difference within each quarter into centered residual error and squared
quarter bias: total−.137735, within-quarter−.008034, quarter-bias−.129701.
Thus **94.2% of the MSE improvement is the quarter-level bias component**.
This is an accounting identity using outcomes, not an available correction or
a causal explanation. Removing each quarter's residual mean retrospectively
gives10.55480 versus10.55518 RMSE—essentially identical discrimination.

New **post-hoc sensitivity only**: give every completed forecast/control the
same additional affine calibration, fit exclusively on earlier completed
windows, using the established30-cell cold start and nonnegative slope.
No current/future labels enter its fit and no NN weights are changed.

| Forecast | Original RMSE | Common extra prior-affine RMSE |
| --- | ---: | ---: |
| Old HALF+D |10.73215|**10.71303**|
| D_MAIN_RB half |10.72573|10.72143|
| Frozen NN+D |10.75679|10.74505|
| Additive+D |10.78699|10.75612|

This reverses the tiny blend ranking. It does not replace the registered result
or establish a new winning forecaster: the choice to investigate this procedure
was informed by results. It does show that calibration deserves a common,
prospectively specified treatment in the next comparison before attributing
small level improvements to interaction learning.

## 5. Event mechanisms are learning something useful

Matched-seed held-out family losses, pooled within season then compared across
11seasons, improve in consistent directions:

| Controlled change | Family | Mean loss delta | Seasons improved |
| --- | --- | ---: | ---: |
| CROSS minus MAIN | Action counts |−.0002189|11/11|
| CROSS minus MAIN | Shot location |−.0003013|11/11|
| CROSS minus MAIN | Conversion |−.0003098|11/11|
| MAIN_RB minus MAIN | Rebound |−.0006363|11/11|
| CROSS_RB minus CROSS | Rebound |−.0006396|11/11|

The corresponding nominal season intervals exclude zero. CROSS_RB versus
MAIN_RB also improves the first three families11/11. These are losses in their
own units, not points and not mutually comparable magnitudes. CROSS can improve
event likelihood and still lose point RMSE; do not call that a training failure
or infer a proven causal player effect.

Independent parent replay on identical matchup rows adds an encouraging
diagnostic. On the fixed primary offensive-cell population, native MAIN_RB
versus the frozen parent:

| Event | Actual /100 | Parent /100 | MAIN_RB /100 |
| --- | ---: | ---: | ---: |
| FGA |89.8097|88.7180|89.1651|
| FTA |20.3213|22.8602|22.0706|
| Turnovers |13.1932|13.2658|13.1465|

FGA bias shrinks−1.092→−.645; FTA overprediction shrinks+2.539→+1.749.
These are separate inherited event-eligible masks, not a jointly complete
point ledger. The FT problem is reduced, not solved. Across **all** matchup
rows, FTA bias is only+.0366 for MAIN_RB versus−.0400 parent; near-zero global
bias again conceals substantial-lineup overprediction. This is consistent with
the earlier situation-mix finding, not a reason to introduce a global FT cut.

On1,035,863 eligible live rebounds, three-seed team-capture binary NLL improves
.532423→.531752; actual capture22.7014%, parent22.6620%, MAIN_RB22.7493%.
This binary capture diagnostic differs from the training six-way collector
loss. It directly confirms opponent-dependent recovery signal beyond a mere
extra rebounding feature.

## 6. Basketball coherence: genuine defense, unfinished offense

At2026q4, MAIN_RB predicts the conventional offense's eligible ORB capture at
19.0% against five Goberts and31.7% against five small guards. Offensive
efficiency changes111.70→122.76. These are sensible directional responses;
the clone stress cases are not legal real teams and do not validate magnitudes.

Prior-average-opponent offense, three-seed mean:

| Fixture | Frozen parent | MAIN_RB | CROSS_RB |
| --- | ---: | ---: | ---: |
| Conventional real unit |119.72|119.31|119.04|
| Five Goberts |117.85|117.62|119.57|
| Limited-creation centers |113.00|112.67|114.17|
| Five small guards |122.24|121.69|120.07|
| Five Jokics |129.28|128.99|125.83|

CROSS_RB puts five Goberts above the conventional offense. MAIN_RB lowers it
only modestly. Worse, a two-sided MAIN_RB fixture gives five Goberts a+1.27
margin against the conventional unit (CROSS_RB+2.45). Five Goberts attacking
small guards still produces40.32FTA/100. Strong imagined defense does not
resolve implausible offensive opportunity allocation.

The Jokić/Korver/Westbrook panel retains a favorable Korver complementarity
contrast relative to additive; this is not proof of a causal ranking and is not
a constraint to force in subsequent fits. Permutations and swapped margins
pass, but algebraic antisymmetry is not held-out matchup-margin accuracy.

**Average-opponent integration needs work.** Moving the saved reference from
128 to256 prior defensive fives changes some calibrated2025q4 Haliburton/
McConnell panel ratings by about0.9–1.0pts/100; maximum native difference is
1.280, calibrated difference.998. The small sensitivity in the2026q4 launch
pilot did not generalize across origins. Before reporting fine lineup/trade
differences, run a fixed-checkpoint convergence study with larger references
and common samples. Do not silently substitute a new reference into v15.

## 7. Honest uncertainty: useful finite-outcome intervals, OOD gap remains

MAIN_RB half's prior-only finite-outcome intervals have possession-weighted
80%/95% coverage **79.88%/94.19%**. Novel coverage is81.10%/93.84%; average
full widths are25.62/38.52pts per100 overall and28.36/42.66 on novel cells.
These include finite-batch noise; they are not uncertainty about the true
quality of an arbitrary synthetic team.

All primary cells have averaged defensive-distance statistic below2, so this
does not test the synthetic tail. Averaging can also hide individual extreme
matchups. On the low-defensive-support subset (<1000;449cells/36,507possessions),
MAIN_RB half RMSE13.1763 trails old HALF+D13.1156. Three-seed spread is not
a substitute for identified latent uncertainty. Continue reporting unsupported
compositions with honest limitations, not imposing a coverage gate.

## 8. What should happen next?

1. **Make the next comparison cleaner, not larger by default.** Register common
   point calibration for equally informed forecasts, preserve this historical
   primary for continuity, add the broader all-five/debut/thin-support cohort,
   and separate matchup-conditioned versus prior-average tasks. Complete a
   no-refit reference-integration convergence check before fan-facing examples.
2. **Test lineup-adjusted capability profiles (roadmap R16).** This result gives
   that idea a concrete purpose: the defensive inputs are still confounded
   opponent-on-floor rates, while the new channel heads demonstrably learn.
   Compare raw, raw+adjusted defense, raw+adjusted offense, and both with fixed
   architecture, additive channel readouts and temporal cross-fitting. Ridge
   attribution is not automatically causal. Refit the NN for changed inputs;
   do not repeat frozen-value replacement. This remains a proposed experiment,
   not an authorized or frozen arm list.
3. **Then test joint adaptation against the frozen-adapter control.** A frozen
   offense may have already absorbed historical defensive context. Letting both
   sides co-adapt could help; this experiment did not test that hypothesis.
   Distinguish input improvements from joint-training improvements with matched
   controls instead of introducing both in one unidentifiable change.
4. **Keep the two other standards active.** Persistent action allocation/FTA
   and rebound-renewal phase behavior remain targeted offense problems. A
   separate latent-quality uncertainty workstream must test unseen roles and
   composition/support distance rather than merely widen finite-game bands.

Do not discard useful channel mechanisms for failing to win a fourth decimal
of r². Equally, do not label event loss, seed consistency or synthetic
directionality as proof that the full product contract has been met.

## Reproduction and handoff

New source: `experiments/v15_postrun_review.py`,
`experiments/v15_postrun_groups.py`, `tests/test_v15_postrun_review.py`.
Use a **new, nonexistent** output directory for every analysis run:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
/Users/adam/miniconda3/envs/basketball25/bin/python -u \
  -m experiments.v15_postrun_review --output-dir /tmp/v15-independent-review-new

OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
/Users/adam/miniconda3/envs/basketball25/bin/python -u \
  -m experiments.v15_postrun_groups --output-dir /tmp/v15-group-review-new

/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest \
  tests.test_v15_postrun_review tests.test_joint_capability_v15 -v
```

The analyses create durable logs in their output directories and block database
access.21tests pass, including pooled-score reconstruction, historical primary
membership, calibration future-outcome exclusion and the existing17v15 checks.
Final test and unchanged-artifact verification logs are under
`experiments/cache/joint_capability_2026_09_18_v15_review_verification/`.
No scraping, database access/mutation, input rebuild, production refit,
delegation, promotion, deployment or commit. All completed artifacts preserved;
the pre-existing dirty tree is preserved. No long process needs launching.
Next step is agreement on the priorities above, then a new preregistration.
