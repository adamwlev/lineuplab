# v15 seed sensitivity and the v16 runtime tradeoff

2026-09-19. Post-hoc descriptive analysis; no fits, protocol changes or launch.

## Bottom line

Three seeds add very little aggregate point accuracy in v15, but are useful
insurance against treating tiny architecture differences as real. Quarter
difficulty dominates raw score variation; it does not follow that seed noise
is negligible in **paired arm differences**. A single-seed v16 screen could be
economical, but is not a substitute for replication of close comparisons.
The current frozen 22-arm/three-seed v16 schedule is unchanged.

## Population and definitions

Original matched offensive-five/quarter cohort: 44 quarters in 2016–2026,
5,607 cells, 726,364 possessions; 2015 warmup excluded. Point scores and
prediction disagreement are possession weighted. Original prior-only calibrated
forecasts are retained. This is not the broader v16 population.

We interpret within-seed variation as score variation across quarters at a fixed
seed, and between-seed variation as score variation across seeds on the **same**
quarter/cells. We also examine arm contrasts, since that is more relevant to
an ablation campaign than raw quarterly difficulty.

Across-quarter SD is the square root of the mean of the three within-seed
sample variances over 44 quarters. Within-quarter seed SD is the square root
of the mean of 44 sample variances over three seeds. Quarters receive equal
weight in these descriptive variation summaries (each quarterly score itself
is possession weighted). They are not independent-seasons confidence intervals.

## Raw quarterly variation: D_MAIN_RB

Standard deviations of quarterly RMSE, in points/100:

| Variation source | Direct NN | Half blend |
|---|---:|---:|
| Across quarters, holding seed fixed | 0.8732 | 0.8348 |
| Across seeds, holding quarter fixed | 0.0761 | 0.0366 |

For the half model, quarterly SD is approximately 23× seed SD. A balanced
quarter × seed descriptive sum-of-squares decomposition attributes 99.87% of
raw quarterly RMSE variation to quarter means; direct NN is 99.48%. These are
fractions of **quarterly metric variation**, not fractions of prediction error
or a claim that random initialization has no research consequence.

## Pooled seed results and averaging benefit

| D_MAIN_RB half forecast | Pooled RMSE | Pooled raw r² |
|---|---:|---:|
| Seed17 | 10.727044 | 0.138825 |
| Seed23 | 10.731257 | 0.138149 |
| Seed41 | 10.725725 | 0.139037 |
| Mean prediction of all three | 10.725732 | 0.139036 |

The pooled RMSE SD across the three seeds is 0.002889; range 0.005532.
For the direct NN, pooled RMSE SD is 0.007861; range 0.014338.

Relative to mean single-seed RMSE, three-seed averaging improves D_MAIN_RB
by 0.009058 direct / **0.002277 half**. Relative to mean RMSE of the three
possible two-seed ensembles, the third seed adds just 0.002265 direct /
**0.000569 half**. This compares average seed choices, not a hindsight-selected
best seed. Averaging need not beat the best individual seed on a realized sample.

Across all four arms, one-to-three averaging gains are 0.00853–0.00963 direct
and 0.00215–0.00242 half. Mean two-to-three half gains are 0.00054–0.00061.
For novel cells, D_MAIN_RB half RMSE is 11.697901/11.708776/11.707367 for
seeds17/23/41 and 11.702397 for the three-seed mean.

Average lineup-specific sample SD across seeds for D_MAIN_RB is 0.4651 direct
and 0.2325 half; root-mean-square sample SD is 0.5414/0.2707. For novel lineups
the RMS figures are 0.5665/0.2832. These are forecast variation, not uncertainty
about the true lineup quality. The exact MSE decomposition was verified:
mean individual-seed MSE minus ensemble MSE equals the possession-weighted
population variance of predictions across those three seeds.

## Research comparisons: seeds matter more here

The best pooled half arm is D_MAIN_RB for seeds17 and41, but D_CROSS_RB for
seed23. D_MAIN_RB versus D_MAIN three-seed RMSE difference is only -0.002035,
smaller than D_MAIN_RB's single-seed RMSE range. The stronger check is paired:
for the quarterly **D_MAIN_RB minus D_MAIN half RMSE contrast**,

- across-quarter SD at fixed seed: **0.02781**;
- across-seed SD at fixed quarter: **0.02584**.

These are comparable. Removing common quarter difficulty changes the conclusion
substantially. Only **13/44 quarters** have the same best half arm for all three
seeds. All of these are descriptive near-tie rankings, not identified winners.

Against the seed-matched old HALF+D control, D_MAIN_RB half RMSE differences
are -0.001074/-0.009469/-0.010361 for seeds17/23/41: same favorable sign,
different magnitude. D_MAIN and D_CROSS_RB change sign across seeds. The earlier
season-block interval for the ensemble D_MAIN_RB advantage includes zero;
running seeds does not manufacture independent seasons or eliminate that
uncertainty.

## Transfer to v16 and the three standards

v15 froze a seed-specific offensive parent and trained a relatively small
defensive adapter. The measured variation therefore includes the parent seed,
adapter initialization, optimization and stopping, not an isolated adapter-only
randomization. v16 jointly retrains offense and defense and tests attention,
allocation and phase mechanisms. Its seed sensitivity may differ materially;
these v15 numbers are not a proven v16 bound.

- Prediction: one seed can screen large changes; close ablation claims need
  paired replication. Two seeds buy most of v15's observed averaging benefit,
  while three give a better check on instability than two.
- Basketball coherence: original v15 fixture ensemble output has median
  seed SD 0.336 and 95th percentile 1.022 pts/100 across its diagnostic rows.
  Mechanism signs near zero should not be certified from one trajectory.
- Uncertainty: seed spread is only one numerical/training sensitivity; it does
  not validate latent/OOD intervals. Fewer seeds cannot be hidden by relabeling
  finite-game intervals or dispensing with the uncertainty pillar.

If runtime dominates, a **new explicitly registered staged protocol** could use
one fixed seed for the broad screen, then replicate controls and candidates
under a predeclared selection/reporting rule. Selected candidates remain
exploratory on these repeatedly inspected outer periods. Completing one seed
for all 22 arms would require 1,056 cases instead of 3,168, roughly one third of
seed-dependent fitting work, not necessarily one third of total elapsed time.
It would also require launcher/reporting/uncertainty changes; merely dropping
two seeds from today's command would violate its frozen acceptance contract.
No such change is authorized or implemented in this analysis.

## Evidence and reproduction

New derived outputs: `experiments/cache/v15_seed_variance_2026_09_19_v1/`:
`scores.csv`, `quarters.csv`, `prediction_variability.csv`,
`variance_components.csv`, frozen `protocol.json`, `sources.json`, and completed
`receipt.json`. Durable log: sibling `v15_seed_variance_2026_09_19_v1.log`.

Producer: `experiments/v15_seed_variance.py`. It reads 528 original cell files,
checks each against its original receipt, checks identical keys/outcomes/weights
and seed-invariant additive predictions, and verifies the exact ensemble MSE
identity. All 144 matched individual-seed score rows reproduce the independent
v15 review to 1e-10. Original artifacts are unchanged. The script refuses an
existing output directory; any rerun must use a new output prefix.

Existing comparison evidence:
[v15 independent review](joint_capability_v15_codex_review.md) and its original
seed/fixture CSVs under `experiments/cache/joint_capability_2026_09_18_v15_codex_review`.
