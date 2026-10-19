# v16 completed-run review — 2026-09-27

## Decision in brief

v16 is a meaningful predictive advance, not a finished three-pillar product.
Retain **J_POINT_BOTH** as the leading point-prediction candidate, with both
direct-half and checkpoint-average-half views. Retain **J_BOTH** as the simpler
event/mechanism comparator. Do not promote either yet.

The adjusted input representation looks more promising than added architectural
complexity. The point auxiliary loss helps ratings but sacrifices event-count
fit. Multiple-NN ensembles did not beat the simpler leading NN/additive blend.
Most importantly, the two-lineup fixtures reveal an unresolved center-heavy
matchup failure that average-opponent ratings partly conceal. The richer U2
uncertainty model does not yet outperform its simpler U1 control.

No training, data acquisition, scorer promotion or commit in this review.
All original and repaired artifacts are preserved. These historical seasons
have been repeatedly inspected: this is development evidence, not a fresh test.

## Evidence, definitions and verification

Completed source: `experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.
Review outputs: `experiments/cache/joint_capability_2026_09_27_v16_codex_review`.
Reproduction: `python -u -m experiments.v16_completed_review` using basketball25.
Durable log: review output `logs/review.log`; hashes in `sources.json`.

The review independently reconstructed **201 scorecard rows** from the saved
cell predictions, agreeing on RMSE, MAE, r² and bias to 1e-11 tolerances. All
six campaign stages and root receipt were previously independently verified.
The completed exact-reference audit has **64 comparisons**, all passing the
0.05 points/100 threshold. At n=16,384, maximum absolute native error is .010976
and calibrated error .007824 points/100. At n=4,096, maximum native error .035838.
This validates the tested approximation cases, not every hypothetical input.

Headline population: **8,345 offensive-lineup-quarter cells, 1,013,999
possessions, 44 quarters in 2016–2026**; 2015 supplies history/warmup. Three-seed
prediction means are formed before scoring. Errors are possession-weighted in
points per 100 possessions. “All” means the broad >=50-possession offensive-five
cohort, not every NBA possession. Scores condition on actual defenders faced.
Novel = previously unseen offensive five, not necessarily unseen players.

`half` = 50% calibrated NN + 50% equally informed additive_defense. Checkpoint
average is prediction averaging, not parameter averaging. The two views have
their own prior-only calibration. Old uncorrected v16 tables are superseded.

## 1. Prediction: useful improvement, with an important comparator distinction

| Forecast | RMSE | MAE | r² | Correlation |
| --- | ---: | ---: | ---: | ---: |
| Additive offense only | 11.251737 | 8.458718 | .132848 | .365625 |
| Additive + actual defense | 11.165936 | 8.412297 | .146023 | .382625 |
| Previous neural/additive blend + defense | 11.096562 | 8.354524 | .156601 | .396307 |
| J_POINT_BOTH direct, no additive blend | 11.061484 | 8.301836 | .161925 | .402800 |
| J_POINT_BOTH direct-half | 11.054951 | 8.299892 | .162915 | .403882 |
| J_POINT_BOTH checkpoint-average-half | **11.054459** | 8.306363 | **.162989** | .403778 |
| Forward top-three checkpoint-average NNs + additive | 11.065234 | 8.323669 | .161357 | .401709 |
| Forward nonnegative stack | 11.068186 | 8.323311 | .160909 | .401145 |

The new NN alone beats additive_defense here; the additive blend adds only a
small further improvement. We are no longer describing a neural model that
necessarily trails additive on this matched broad population.

Do not overstate the tiny checkpoint-average versus direct-half difference:
RMSE differs by .000492; direct-half has slightly better MAE and correlation.
On the legacy co-primary 5,607-cell population, direct-half is also slightly
better: r² .147307 versus .146601, compared with additive_defense .133998 and
parent_half_defense .141776. The broad .163 cannot be compared unqualified
with older .13 figures from a different population/calibration.

### Novel lineups and transfers

On **3,489 novel cells / 361,361 possessions**:

- Additive_defense: RMSE12.238726, r².118400.
- Parent_half_defense: RMSE12.125765, r².134599.
- J_POINT_BOTH checkpoint-average-half: RMSE12.056185, r².144502.

The transfer library points in the same direction, but not uniformly. On its
959 available cells, direct-half improves RMSE11.005655 → 10.864578 versus
additive_defense. On the 146 >=200-possession cases, 6.947335 → 6.674457.
On the narrow 67-case >=200/multiple-mover subset, the previous parent blend
is better (6.877970 versus 6.906662). No causal trade effect is established.

### Evidence strength and what is actually improving

The supplemental forward top-one checkpoint selector chooses J_POINT_BOTH in
**every primary quarter**, using only earlier outcomes; it exactly reproduces
the fixed candidate's checkpoint-average-half score. In that nine-method
supplemental family:

| Comparator | RMSE difference | 95% season-bootstrap interval | Seasons won | Holm p |
| --- | ---: | --- | ---: | ---: |
| Additive_defense, all | -.111477 | [-.143084, -.079772] | 11/11 | .017578 |
| Parent_half_defense, all | -.042103 | [-.068045, -.019442] | 10/11 | .061523 |
| Additive_defense, novel | -.182541 | [-.242474, -.128168] | 11/11 | .017578 |
| Parent_half_defense, novel | -.069579 | [-.119189, -.024947] | 8/11 | .087891 |

These are paired historical comparisons, not independent future confirmation.
The original larger arm/control family is more conservative: J_POINT_BOTH
direct-half versus additive_defense has Holm p .085938, and versus the parent
blend .471680. Do not substitute the smaller supplemental family to declare
all original architecture hypotheses confirmed. Named architecture RMSE
contrasts do not clear the registered broad-population family correction.

Decomposing weighted MSE into quarter mean-error² and within-quarter error:

- Versus additive_defense, **70%** of checkpoint-half's improvement is within
  quarters, 30% quarter-level bias. There is genuine relative-lineup progress.
- Versus the stronger parent blend, **66%** is quarter-level bias and 34%
  within-quarter error. For direct-half, the bias share rises to **88%**.

Thus the increment over an already-good blend is smaller and more dominated
by level calibration than the gain over additive alone. This motivates a fair
league/season-level calibration control, not fitting offsets to held-out data.

## 2. What the ablations taught us

**Adjusted profiles are the strongest broad signal.** BOTH beats matched RAW
in all nine RAW/BOTH architecture pairs, in all four reporting views. For
example, direct RMSE J_RAW11.171152 → J_BOTH11.112678; J_POINT_RAW11.181161 →
J_POINT_BOTH11.061484. This consistent descriptive pattern is more compelling
than any particular extra attention/action/phase module, but the nine pairs
share data and are not nine independent replications. Offense-only adjustment
is competitive: J_OFF direct11.103295, half11.083082. Both banks are not proven
necessary in every architecture.

**Point supervision pays off, but not for free.** J_POINT_BOTH is the same
basic joint adjusted design with the registered .25 point-loss weight. Its
half RMSE is .031135 better than J_BOTH (bootstrap [-.057222,-.005725], 8/11
season wins, full-family Holm1.0). But event-count NLL is **.000263 worse**
in **all 11 seasons**, interval [.000210,.000313], Holm .033203. Location,
conversion and recovery contrasts do not establish a compensating event win.
Keep point accuracy and intermediate-target fidelity separately visible.

J_BOTH itself improves count NLL versus J_RAW by .000363, 11/11 seasons,
Holm .033203. Adjusted banks are not universally cleaner: standalone adjusted
profile NLL improves offensive/defensive counts and defensive location, while
conversion and recovery worsen on both sides, and offensive location worsens.
Selective channel use/shrinkage deserves testing; “adjust everything” is not
supported simply because the downstream NN learns to use the combined bank.

**Complexity is not the next default bet.** Attention does not beat the
matched-width BOTH control on point RMSE (half11.079869 versus11.073777).
Free phases barely improve tied phases (half11.075467 versus11.077993).
The all-features model is not the winner (half11.089909). This does not prove
attention or phase modeling can never help; it limits claims about these tests.

## 3. Ensembles: a simple blend wins this bounded experiment

Forward top-three, top-five, equal-all, and the regularized nonnegative stack
all trail top-one checkpoint-average-half. Top-three RMSE11.065234 and stack
11.068186 versus11.054459. Equal-all checkpoint-half is11.080111.

These methods select members/weights using prior quarters; hindsight arm
rankings were not used to construct the forecast. No claim is made that every
possible mixture has been optimized. The tested family gives no reason to
pay the serving/explanation cost of many NNs now. Nor does it justify another
large search for the best historical blend. Retain the simple candidate and
focus on its identifiable weaknesses.

## 4. Basketball coherence: the important unfinished work

### Two-lineup matchup exposes a shared extrapolation weakness

The legal five-center fixture is Gobert/Adams/Robinson/Capela/Allen. All 22
native neural designs' calibrated direct predictions favor that team over
Jokić/Murray/Gordon/Porter/Westbrook. No sign is forced by the frozen test,
but this systematic prediction is a substantial basketball plausibility concern.

For J_POINT_BOTH:

| Forecast mode | Centers offense | Jokić lineup offense | Center margin |
| --- | ---: | ---: | ---: |
| Additive_defense | 116.123 | 109.778 | +6.345 |
| Calibrated NN direct | 120.285 | 115.579 | +4.707 |
| Direct-half | 118.204 | 112.678 | +5.526 |
| Checkpoint-average-half | 117.964 | 113.154 | +4.810 |

This is not only an NN problem: additive's defensive arithmetic already favors
the centers strongly. The NN reduces but does not reverse that effect. Against
this opponent, the native ledger gives centers .487 offensive-rebound capture
versus .183 for the Jokić unit, and 31.16 versus14.19 FTA/100. These are useful
diagnostic leads, not proof of a specific causal or implementation failure.
Inspect defense aggregation, missing perimeter-coverage costs, creation/spacing
constraints and rebound/FT compensation before changing the architecture.

Against an average opponent the same candidate's direct-half rates legal
centers116.760, five Goberts114.792, and the conventional high-exposure real
unit120.196. That ordering is less alarming; however, the calibrated NN gives
legal centers a +.201 residual versus additive, and five Goberts +4.459.
Adjusted point quality has not solved pathological-context penalties. A
reasonable average-opponent ordering cannot excuse an implausible two-team
mechanism. Do not fix this with a “five centers” cap or forced defeat.

### Other named examples are informative, not causal validation

- Korver versus Westbrook: every arm has a positive *relative-to-additive*
  Korver swap residual. For J_POINT_BOTH it is +1.360 points/100 in direct
  scoring; its final direct-half still rates the Westbrook version higher,
  125.055 versus124.658. This respects the distinction Adam originally made.
  **Important limitation:** the Korver fixture injects historical raw profiles
  without a complete matched historical adjusted/defensive/rebound state.
  It is not a clean multi-bank player-season transport experiment or proof
  of actual chemistry. Adam is open to either empirical sign.
- Haliburton minus McConnell: J_POINT_BOTH native +2.137, direct-half +1.767.
  That is not an estimate of an entire Pacers-season absence, rotations, or
  injury effect. The final residual benefit relative to additive is not large.
- Adams versus Robinson: all 22 arms give Robinson higher team capture on
  this fixed context (Adams minus Robinson roughly -.006 to -.013). This does
  not disprove Adam's facilitation example; collector skill, dated state and
  the teammate benefit must be separated in real observed contexts. An extra
  rebounding feature is not itself evidence of learned teammate facilitation.

## 5. Uncertainty: useful infrastructure; U2 has not earned acceptance

The finite-quarter bands for the forward top-one checkpoint blend cover
**93.86% overall**, **93.31% novel**, **94.17% recurring**, versus nominal95%.
Mean full widths are39.57,43.55,37.37 points/100 respectively, possession-
weighted on the same broad cohort. This is mild undercoverage, not perfect
calibration. All primary cells have available bands.

Do not confuse those figures with the generic three-pillar matrix's ~96%
coverage/~215-point widths. That matrix's U0 summary includes **220,381
offensive-five-quarter cells**, including tiny exposures, and is cell-weighted.
Its target/population differs from the 8,345-cell main scorecard.

U1 fits constant persistent-discrepancy variance; U2 lets variance depend on
support/context features. Both use prior data, completed-game splits, and
separately forecast finite-game noise. Neither is an identified causal
lineup-quality posterior.

On the **2,037 scored pairs per model/split**, U2's mean joint log score is
slightly worse than U1 in **all nine model×split combinations**. For balanced
date splits: J_BOTH −7.874326 → −7.874634; J_ALL_BOTH −7.875540 → −7.876971;
parent blend −7.878662 → −7.882255. These are small descriptive differences,
not a new multiplicity-controlled rejection test. They establish no U2 win.
Finite-half coverage is around93–95%, with split-dependent undercoverage.

U2 does widen synthetic discrepancy ranges: J_BOTH conventional unit width
11.62, legal centers35.76, five Goberts114.04 points/100. J_ALL_BOTH gives
11.10/29.44/93.92. That is a desirable qualitative direction but extreme
extrapolation of a log-variance regression, **not validated latent coverage**.
Seed spread remains small by comparison and is not a substitute.

Also, the prespecified U1/U2 model set does **not include J_POINT_BOTH** or its
checkpoint-half view. Do not borrow another model's uncertainty fit to declare
the predictive leader a three-pillar winner. Its own finite-quarter ensemble
bands are evaluated; its persistent/hypothetical uncertainty is still missing.

## 6. Noise, average opponents and remaining headroom

Game-split reliability covers8,330/8,345 cells and1,013,176/1,013,999 possessions.
For the raw target, the global diagnostic ratio is .214–.238 depending on the
split (.230 random-split); within-quarter .143–.169. The >=8-game sensitivity
is .249–.293 globally on a different population. The model-dependent opponent
correction changes these modestly. Role drift, shared-game covariance and
violated stable-mean assumptions make these **not theoretical r² ceilings**.
Do not divide .163 by .230 and claim a measured fraction of attainable skill.

The prior-average-opponent experiment retains only its three fixed arms.
J_BOTH half r² falls from conditional .158193 to average-opponent .143111;
J_ALL_BOTH .157612 → .143782. Their average-opponent additive_defense control
is .132160. Knowing the actual defense schedule matters. This is not a failure
of the average-opponent product, but a different information set.
Calibration is inherited from conditional scoring, not refit to average mode.
The512 versus4096 sensitivity has maximum .1602 and95th percentile .1126
points/100; it is not an exact-error bound. **J_POINT_BOTH's full observed-
lineup average-opponent benchmark remains unmeasured**, despite its fixed
average-opponent fixtures being available.

## 7. Recommended next work, in priority order

1. **Finish the product-facing diagnosis before another large architecture
   sweep.** Explain the center-vs-Jokić result through both directional ledgers,
   defense main effects, renewal, conversions, FT allocation and message-off
   interventions. Add dated, fully consistent player-season transport to the
   backlog; do not repair the Korver result by injecting only selected banks.
   Pair synthetic failures with observed low-spacing/multiple-big contexts.
2. **Evaluate the actual leading candidate in the missing modes.** Reuse its
   saved fits for the average-opponent benchmark and fit its own prior-only
   uncertainty controls for direct-half and checkpoint-half. No NN refit is
   needed for these gaps. This is proposed new analysis, not completed evidence.
3. **Design a smaller targeted learning experiment.** J_BOTH versus
   J_POINT_BOTH, a small prespecified point-loss-strength grid, and selective
   adjusted channels test whether point gains can coexist with good event
   targets. Include an equally informed prior-only seasonal-level calibration
   control: much of the increment over the previous blend is level correction.
   Freeze the budget/design before results; refits are justified if this tests
   a clear mechanism. Do not default to another attention/width/all-features sweep.
4. **Keep U1 as the required uncertainty control; improve U2 only against
   forward evidence.** Diagnose noisy split covariance, scarce high-distance
   examples, shrinkage and stable-quarter assumptions. Test monotonic/support
   structure explicitly if used. No coverage gate, arbitrary variance inflation,
   or claim that synthetic ranges prove true-quality calibration.
5. **Move toward an internal research tool with explicit labels**, not public
   promotion yet. Show the point candidate, additive comparison and mechanism
   caveats; keep channel explanations faithful to their evaluated model. A
   fresh prospective season remains the strongest eventual confirmation.

Bottom line: the adjusted-profile idea and point-supervised NN have earned
continued investment. The next opportunity is making the **stronger scorer
behave sensibly in the two-lineup product**, not adding complexity indiscriminately.
