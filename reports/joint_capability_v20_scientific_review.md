# V20 scientific review — 2026-10-09

## Decision

Retain **P_BASE / J_POINT_BOTH** as the point reference. No new scorer promotion
or overall three-pillar pass. V20 does not establish an incremental gain from
clock-adjusted capability profiles or S5 checkpoint selection in the primary
point forecast, transfer performance, counterfactual coherence or uncertainty.
This is a bounded null for these estimators, not proof that context is irrelevant.

There are narrower positive findings: decoder clock context improves conditional
event prediction, and S5 improves count likelihood in three registered comparisons.
Neither becomes a demonstrated improvement in the common-environment tool output.

The most useful next work is a bounded diagnosis of **defensive coverage and
possession renewal**, followed by a focused structural experiment if justified.
Do not follow this result with an automatic width/profile/epoch sweep.

## Completion, provenance and population

- 864/864 new-arm case slots complete (including eight reusable pilots); two
  retained controls bring the full eight-cell panel to 1,152 origin/arm/seed cases.
- 48 scored quarters; primary evaluation is **44 quarters, 2016–2026**. 2015 is
  warmup, not included in the headline metrics.
- **8,345 offensive-lineup-quarter cells / 1,013,999 possessions**: each offensive
  five has at least 50 evaluation possessions. This is not all NBA possessions.
- Predictions condition on actual opposing defensive lineups, then aggregate
  to the offensive-five cell. Reference game-clock mix is past-only; actual
  future clock mix is a separate conditional diagnostic, not a product input.
- Primary view: three-seed prediction means, checkpoint-average-half (50/50
  calibrated NN and equally informed additive_defense). RMSE/MAE/bias: points/100.
- All 19 analysis stages completed, including independent native, point,
  uncertainty, integration, fixture, risk and downstream audits. The continuation
  took **16.53 hours**; average-opponent integration 5.58h and risk census 8.49h.
  Training/scoring took 48.88h. Original failed status is historical; do not restart.
- Independent review re-pools **192 point rows** from saved cell predictions and
  matches the official table within 1e-8 absolute / 1e-10 relative tolerance.
  Exact keys, targets, weights and shared baseline columns match across eight arms.
  No fits, inference, database access or changes to original artifacts.
- All **73 v20 tests** pass, including the independent weighted-metric checks;
  durable results are in the review directory's tests.log. Git whitespace checks pass.

The frozen [plan](../docs/history/JOINT_CAPABILITY_V20_PLAN.md) specifies 17 point, 44 event
and four uncertainty contrasts. Season-block intervals and exact 11-season swaps
are used; seeds are not independent seasons. Holm correction is separate for each
family. These are repeatedly used historical development seasons, not untouched
prospective confirmation. Descriptive slices/views below are not extra wins.

## 1. Forward prediction

| Arm | Primary RMSE | MAE | r² | Bias |
| --- | ---: | ---: | ---: | ---: |
| P_BASE (retained reference) | 11.054459 | 8.306363 | .162989 | +.015328 |
| S_BASE | 11.060008 | 8.313903 | .162149 | −.004349 |
| P_ADJ | 11.062056 | 8.313572 | .161838 | −.020158 |
| P_CONTEXT (retained C_FULL) | 11.062813 | 8.309150 | .161724 | +.046479 |
| S_ADJ | 11.066479 | 8.320464 | .161168 | −.003846 |
| P_BOTH | 11.066916 | 8.313000 | .161102 | +.067074 |
| S_CONTEXT | 11.070326 | 8.316551 | .160585 | +.006690 |
| S_BOTH | 11.074802 | 8.322819 | .159906 | +.026561 |
| additive_defense | 11.165936 | 8.412297 | .146023 | +.072193 |
| additive (offense-only control) | 11.251737 | 8.458718 | .132848 | −.138087 |

BASE/CONTEXT use original adjusted profiles; ADJ/BOTH use new clock-adjusted
profiles. CONTEXT/BOTH have the full clock decoder. P uses previous selection;
S selects the five-checkpoint averaged forecast in inner validation.

Every new mechanism contrast has a numerically positive (worse) primary RMSE
delta. No incremental point improvement is established:

- P_ADJ − P_BASE: **+.007597**, 95% season-bootstrap interval
  **[−.001066, +.020272]**, Holm p=1; wins in 3/11 seasons.
- S_BASE − P_BASE: **+.005549 [−.005019, +.016428]**, Holm p=1;
  wins in 4/11 seasons.
- P_BOTH − P_CONTEXT: **+.004103 [−.002448, +.010219]**, Holm p=1.
- All six new arms numerically beat additive_defense, in 10/11 seasons each;
  P_ADJ, P_BOTH and S_BASE pass the registered multiplicity correction. The other
  three do not pass it. Beating additive is useful, but not new evidence of beating
  our already stronger contextual reference.

Old descriptive controls remain near-tied: R_ALLOC checkpoint-half r² .163316,
O_ORDER .162999, C_FIXED .162939. Do not select a new winner from those small,
reused-history differences. They are not new v20 arms.

### Views, novel lineups and transport

P_BASE pure-NN checkpoint-average r² **.161482**, versus its blended **.162989**.
Its direct r² is .161925 and half .162915. The partial-run pure-NN lead did not
persist over the full calendar; there is no reason here to discard the blend.

Novel cohort: **3,489 cells / 361,361 possessions**. P_BASE primary r² **.144502**
versus additive_defense **.118400**. Best new arm S_BASE is .143162; P_ADJ .142703
and S_BOTH .140454. No new novel-lineup win.

The original special cohorts are unchanged:

| Cohort | Cells / possessions | P_BASE RMSE | P_ADJ RMSE | S_BASE RMSE |
| --- | ---: | ---: | ---: | ---: |
| Transfer | 146 / 47,419 | 6.702041 | 6.734827 | 6.743904 |
| Large observed role changes | 2,139 / 254,582 | 11.330504 | 11.339820 | 11.338192 |
| Two nonspacing bigs | 65 / 8,471 | 11.044572 | 11.024866 | 11.006402 |

All six new arms trail P_BASE on transfer and role-change point RMSE. The small
two-big slice has some descriptive improvement, but bias stays around +3 points/100
(P_BASE +3.073, P_ADJ +3.012, S_BASE +3.062); it is not five-center validation.

Average-opponent mode also retains P_BASE: primary r² **.146947**, S_BASE .146310,
P_ADJ .146210, S_BOTH .144584; integrated additive_defense .132160. This uses 512
past-opponent draws, not actual future opponents. Against 4,096 draws on the fixed
880 sensitivity cells, P_BASE blend changes by .0612 points/100 RMS, max .1537.
Realized outcomes are not neutral-opponent ground truth. The extra integral cost
is real, but the final output is numerically reasonably stable at the tested scale.

### Bias and selection stability

The early negative leaderboard bias was not a permanent −2 point level error.
P_BASE pooled bias is **+.0153**, but weighted RMS quarterly bias is **1.5861**;
quarter values range −3.161 to +5.521. P_ADJ quarterly bias RMS is 1.6178,
S_BASE 1.6281. Global cancellation is not local calibration.

S5 trains later and eliminates short averaging windows: P_BASE mean selected
epoch 9.41, S_BASE 13.87; P_CONTEXT 13.34, S_CONTEXT 17.26. P_BASE has 22/132
primary cases with fewer than five checkpoints; S arms have none. No cap hits.
Mean within-quarter, across-seed primary RMSE SD decreases modestly (.0300→.0288
BASE; .0291→.0238 CONTEXT). This is score variability, not a full decomposition
of prediction variance. More stable/event-faithful selection is not automatically
more point-accurate selection.

## 2. Event fidelity and persistent errors

Of 44 registered actual-context event comparisons, **14** pass Holm p<.05:

- 11 decoder-context improvements: P_BOTH vs P_ADJ and S_CONTEXT vs S_BASE
  improve all four families (counts, location, conversion, recovery). S_BOTH vs
  S_ADJ passes for three; location has Holm p=.058594, not a corrected pass.
- Three selection improvements: S_BASE vs P_BASE, S_ADJ vs P_ADJ, and S_BOTH
  vs P_BOTH improve count loss, Holm p=.042969. S_CONTEXT count p=.058594.
- **No profile-adjustment event contrast passes correction.** The adjustment
  does not supply the intended mechanism gain hidden behind tied point totals.

Examples: P_BOTH−P_ADJ conditional count loss −.002267; S_BASE−P_BASE count loss
−.000102. These have different event-specific denominators; neither is a
points/100 effect or identified causal player contribution.

Role-allocation changes are tiny. In the reference role-change diagnostic,
P_BASE/P_ADJ FGA allocation loss is 1.578239/1.578207; team FTA bias is
+2.347/+2.451 attempts/100. Do not mistake nearly identical role-share losses
for evidence of useful new role adaptation.

Persistent-error evidence still points more toward opportunities than hot
shooting. For P_BASE, the chronological disjoint-game correlation is **.0182**
for FG conversion versus **.1820** for FTA; after the shared CLOCK adjustment,
FTA correlation is .0972. Random-game split11 gives .0441 FG conversion and
.2283 FTA (.1330 after CLOCK adjustment). These are the saved diagnostic
populations (at least two games and20possessions per half), not the entire point
leaderboard. A naive residual correction need not improve forecasts; no new
correction is fitted or proposed as established by these correlations.

## 3. Basketball coherence

**All eight arms still favor the legal five-center lineup against both Jokić
fixtures**, in the pure NN as well as the primary blend. Seed-mean blended margin
ranges **+4.72 to +6.23 points/100** across these comparisons.

P_BASE centers vs Jokić/Korver: NN offense120.90, opposing offense117.52,
NN margin+3.38, blended margin+5.19. P_ADJ gives blended+5.52, S_BASE+5.46,
P_BOTH+5.65. The problem is not merely that additive blending undoes a coherent NN.

The event ledger remains informative about the failure: P_BASE centers project
32.97 FTA/100 against Jokić/Korver; P_CONTEXT38.39 and P_BOTH38.64. Context changes
can improve observed conditional events while making an extreme composition's
FTA forecast worse. Upstream profile adjustment does not fix this.

Against the same prior_common_1 opponent, P_BASE centers have substantial renewal
(.153 usage-budget units per possession) and offensive capture .478, versus .261 for the common real
unit. The same center output has17.32 turnovers/100 and role stretch .521 vs .189
for that real unit: the model notices some stress, but does not translate it into
a credible overall matchup. These are diagnostic computations, not causal effects.

Other checks do not establish a new broad coherence pass: small guards allow
130.77 points/100 vs that opponent and have a −3.54 blended margin; Adams/Robinson
fixed-comparison capture remains .313/.319 in the reference. We should not impose
an Adams ranking, but team facilitation is still unvalidated. Haliburton/McConnell
reference offense differs by1.90, while defense largely offsets the margin change.
That is not validation of the real injury narrative. Real small-ball, mixed-era
Korver, clone, thin and stale fixtures remain in the complete output tables.
Do not infer total rankings or causal complementarity from these snapshots alone.

## 4. Uncertainty and deployment risk

No registered transport-discrepancy comparison passes correction:

| Mean | Added descriptor | Joint log-score delta (higher better) | 95% interval |
| --- | --- | ---: | ---: |
| P_BASE | Role stretch vs constant U1 | −.000105 | [−.000396, +.000312] |
| P_BASE | Clock mismatch beyond role | +.000283 | [−.000130, +.000650] |
| P_ADJ | Role stretch vs constant U1 | −.000074 | [−.000353, +.000326] |
| P_ADJ | Clock mismatch beyond role | +.000308 | [−.000251, +.000827] |

These use the same2,037eligible disjoint-game pairs and prior-only calibration.
They do not compare directly with U0's full-quarter8,345-cell population.
P_BASE U0 nominal95% coverage is **93.64% by cell /93.27% weighted**. U1's
balanced-date split coverage is94.16% /95.96% on its own eligible half-game units.
The new role/clock model barely changes these proper scores/coverage measures.

At2026q4 against prior_common_1, role+clock synthetic discrepancy width increases
from15.98points/100 for the common real lineup to18.90 for the five centers.
U1 is17.26 for both. This is a useful monotonic response, **not validated latent
quality coverage**; no finite-game noise is included in these particular fixture
bands. A fitted slope is not proof that it detects the structural center failure.

### The expensive census is mostly an underpowered test here

The full outcome-independent historical95th-percentile census flags1,597 of
220,381 future lineup-quarter compositions (967supported). But only **eight of
8,345 primary cells**,644possessions, are high stretch; **four**,388possessions,
have adequate descriptor support. Independent raw-membership joins reproduce
these counts exactly. No meaningful arm ranking or error-discrimination claim
can be made from four supported observations.

This is a reference-population/measurement problem, not a compute failure. The
unweighted distribution of all historical compositions is unlike the repeatedly
deployed >=50possession primary cohort. The 8.49h census bought a precise threshold
but very little comparison power. **Do not routinely repeat it unchanged.**
Preserve this registered null; any next design should freeze a relevant prior
reference cohort and/or evaluate continuous descriptors with an exposure-aware
noise model. Do not move today's threshold until a favorable result appears.

## 5. What this changes about the next direction

1. **Keep the point reference and bounded context diagnostics.** No strong reason
   to adopt the more expensive adjusted-profile bank or S5 for point scoring.
   Keep S5/count evidence for event-focused work, not as an unqualified winner.
2. **Diagnose the defensive/renewal route with saved weights first.** Separate
   volume, shot conversion/location and rebound recovery; inspect attacker-level
   responses and saturation across real and synthetic units. The previous
   defense-off result locates influential computations, not an identified causal
   mistake. This review authorizes no new model campaign.
3. **If supported, design one focused defensive-coverage experiment.** Compare
   existing broadcast defense, an attacker-specific response control, and a
   constrained shared-capacity/assignment model. Preserve explicit baseline
   nesting and help/switching flexibility; uniform assignment does not automatically
   reproduce the current nonlinear mean/SD operator. No named-lineup penalties.
4. **Make unfamiliar compositions empirically testable.** Freeze forward
   withheld-composition tests and prospective, past-known cohorts alongside the
   unchanged historical benchmark. Keep the October6selection-bias diagnosis in
   view: future final exposure is not an input, and shooting residuals do not
   become predictable merely because their accounting contribution is large.
5. **Scale analysis cost to information.** Retain all three standards, but avoid
   universal full-history censuses. Design useful support populations before
   paying to calculate an extremely precise, nearly empty tail.
6. **Allow a parallel product track in scope, not an automatic promotion.** A
   private research interface can expose retained forecasts, additive baseline,
   event explanations and caveats. Public deployment and new-data acquisition
   require separate authority. Further r² sweeps should not be prerequisites for
   every piece of useful product work.

V20's central lesson is not “the NN failed.” The retained NN remains useful,
including on novel lineups. It is that **better observed-situation modeling has
not supplied the missing compositional basketball structure** in this experiment.
That shifts the next question from more feature cleanup toward how capabilities
are constrained and interact when ten players are placed on a court.

## Reproduction and artifact cautions

Original summary:
`experiments/cache/joint_capability_2026_10_08_v20_posttrain1_summary`.
Independent re-pooling:
`experiments/cache/joint_capability_2026_10_09_v20_review1` (review.log, provenance.json,
point_checks.csv and descriptive tables). New consumer:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
 /Users/adam/miniconda3/envs/basketball25/bin/python -u \
 -m experiments.v20_scientific_review --out <fresh-output-directory>
```

Original summary's `bias_within_quarter.csv.gz` does not retain the environment
label although it contains reference and conditional rows. Do not mix those rows.
This review independently recomputes `quarter_bias.csv` from explicitly reference
cell predictions. Original output is preserved; this does not affect the point
leaderboard or registered contrasts. All numerical review inputs are hashed.
Frozen protocols, trained parameters and original producer fingerprints unchanged.
