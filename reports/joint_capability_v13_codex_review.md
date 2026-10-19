# v13 independent post-run review

Codex, 2026-09-15. Saved-results review, no delegation or training. All three
product standards remain co-equal. No scorer promotion or commit.

## Bottom line

There is useful progress: a role-aware, creation/load-constrained NN combined
with additive produces the best pooled point forecast in this campaign. The
improvement over the old blend is modest and not established on season RMSE;
it is more convincing against additive alone. The incremental gain is mostly
on recurring lineups, not novel ones. Creation constraints make extreme-lineup
behavior more intelligible, but do not finish that problem. Latent-mean OOD
uncertainty remains open.

Keep **J_ROLE_SUPPLY_LOAD + additive** as the leading research candidate and
**B_SUPPLY_LOAD** as an informative alternative for basketball behavior. Neither
replaces the existing scorer. Do not call this a confirmed architecture winner.

## 1. Completion, provenance, and independent checks

Source: `experiments/cache/joint_capability_2026_09_14_v13_prod/`.
Status `ANALYSIS_COMPLETE`; wrapper exit 0, elapsed 58,614.6 seconds (16.28 hours).
Twenty trajectories completed all 48 origins: 960 arm-origins / 1,920
inner/reset-final fits. Automatic reports and 1,020 fixture/intervention rows
are complete. 2015 is calibration warmup, not primary evaluation.

Independent producer: `experiments/v13_postrun_audit.py`.
Successful derived prefix:
`experiments/cache/joint_capability_2026_09_15_v13_codex_review_v2/`.
Durable log `audit.log`, provenance and output hashes `receipt.json`.

Verified all 77 frozen code/protocol hashes, 30 source hashes, every completed
output receipt and gzip CRC, all inner/final checkpoint hashes, and the report
receipt's output hashes. Matched every arm's cell keys, exposure, outcomes,
novelty and saved controls. Independently recomputed weighted MAE, RMSE, r²,
correlation and bias; all 192 all/novel/recurring metric rows reproduce the
automatic scorecard with maximum numeric discrepancy zero.

Per-player native points, additive components, B/R/native readouts, secondary
halves, and affine calibration reconstruct saved forecasts within their stated
tolerances. Calibration training counts match completed prior cells and latest
stops do not exceed forecast starts. Interval sources also precede forecasts.
Every selected epoch equals the saved inner-curve minimum; final-curve lengths
equal the selected counts. These are saved-output/accounting checks, not a
retraining or full checkpoint-forward replay. The existing preceding-quarter
validation / later-quarter evaluation split was not changed.

The first audit attempt used the wrong units when reading per-player points
(per possession rather than per 100); corrected in the audit reader only.
Its incomplete prefix is preserved. It was not a training/scoring failure.
No original run artifact, frozen producer, database or input cache was changed.

## 2. Prediction: the important comparison is with the old blend

Primary population: **44 quarterly origins, 2016–2026; 5,607 lineup-quarter
cells, 726,364 possessions**. Metrics weight each cell by possessions; this is
not r² on individual possession outcomes or all available NBA possessions.
The cells include 2,073 novel fives / 226,256 possessions and 3,534 recurring
fives / 500,108 possessions. Novelty is the existing prior-exposure definition,
not proof of unfamiliar player roles or unusual basketball composition.

| Forecast | MAE | RMSE | r² | Correlation |
|---|---:|---:|---:|---:|
| Additive | 8.09195 | 10.84099 | .12043 | .35326 |
| Previous V9 NN | 8.14018 | 10.86667 | .11626 | .34617 |
| Previous HALF: 50% additive + 50% V9 NN | 8.07273 | 10.80812 | .12576 | .35789 |
| Previous prequential GLOBAL blend | 8.07069 | 10.80970 | .12550 | .35785 |
| B_SUPPLY_LOAD, best direct trained forecast | 8.06789 | 10.81579 | .12452 | .35600 |
| J_ROLE_SUPPLY_LOAD, standalone NN | 8.06710 | 10.82915 | .12235 | .35360 |
| 50% additive + 50% J_ROLE_SUPPLY_LOAD | **8.03415** | **10.79364** | **.12810** | **.36104** |

The last row is a predeclared secondary forecast, not a post-hoc fitted weight.
Identifying it as the best of many rows is still post-selection interpretation.
It improves RMSE by 0.04736 versus additive and 0.01448 versus old HALF. The
latter is about 0.13% RMSE reduction. Its MAE improvement is 0.05781 and 0.03859,
respectively. No directly trained arm beats old HALF on pooled RMSE.

The winning forecast really is half additive and half the **prior-calibrated**
new NN. B arms already contain additive inside their trained readout; their
secondary halves add another additive contribution. Do not confuse those two.

### Robustness beyond the leaderboard

Added independent season comparisons for secondary forecasts, which the
automatic primary-arm contrast table did not include. Lower differences favor
the new blend; these are equal-season averages, not pooled metric differences.

| New role/constraint blend versus | Metric | Mean difference | Nominal 95% t interval | Favorable seasons |
|---|---|---:|---:|---:|
| Additive | RMSE | −.04567 | [−.08029, −.01104] | 8/11 |
| Old HALF | RMSE | −.01282 | [−.03333, +.00769] | 6/11 |
| Additive | MAE | −.05541 | [−.09601, −.01480] | 10/11 |
| Old HALF | MAE | −.03495 | [−.06607, −.00382] | 9/11 |

The new blend wins 29/44 quarterly RMSE comparisons against HALF, 28/44 against
additive. Removing any one season leaves its equal-season RMSE advantage over
HALF negative (−.01627 to −.00709). However, 2016 and 2017 account for most of
that average gain: excluding **both** leaves −.00077. It loses each season
2020–2024 on RMSE against HALF, then wins 2025 and 2026. The combined 2024–2026
slice improves RMSE from 10.96112 to 10.94945, while 2020–2023 worsens from
11.17522 to 11.18794. This is not a uniform era-independent advance.

These intervals are nominal, not corrected for 18 designs, multiple metrics,
and repeated research on these years. Overlapping training prefixes and shared
historical environments further limit a simple independent-season inference.
We have encouraging development evidence, not untouched confirmation.

### Novel versus recurring

| Forecast | Novel RMSE | Recurring RMSE |
|---|---:|---:|
| Additive | 11.85302 | 10.35068 |
| Previous V9 NN | 11.77283 | 10.43087 |
| Previous HALF | **11.76624** | 10.34554 |
| J_SUPPLY_LOAD NN | 11.77258 | 10.39296 |
| Half additive / J_SUPPLY_LOAD | 11.76842 | 10.32904 |
| J_ROLE_SUPPLY_LOAD NN | 11.78460 | 10.36800 |
| Half additive / J_ROLE_SUPPLY_LOAD | 11.77519 | **10.31894** |

The table compares selected relevant controls, not every arm's minimum in each
slice. The leading overall candidate preserves most of the NN's historical
novel-lineup advantage over additive, but does **not** improve that advantage
over old HALF. Its recurring improvement extends across all three positive
prior-exposure bins. At high composition distance it is essentially tied with
old HALF (11.17129 versus 11.17055). Do not describe this as a broad OOD win.

### Is this just a mean correction?

No, but calibration is important. The winning NN's raw RMSE is 10.88503;
prior-only point calibration gives 10.82915, then blending gives 10.79364.
The raw decoder should not inherit the final ensemble's accuracy claim.

Decompose cell error within each quarter into squared quarter-mean error plus
centered residual MSE. Versus old HALF, the winning blend reduces MSE by
0.31279: 0.08388 from quarter-level bias and 0.22891 from centered error. Thus
about 27% is level improvement and 73% is improvement beyond that level.
The latter includes scale/discrimination changes, not necessarily causal synergy.
Correlation also improves, .35789 to .36104.

Quarter-mean error remains substantial: RMS bias is 1.92 points/100 for A,
1.87 for old HALF and 1.85 for the new blend. The new blend's quarter biases
range from −4.74 to +4.76. Adam's seasonal-level hypothesis remains worth a
separate causal test; this audit did not fit or apply a calendar correction.

## 3. What the ablations teach us

**Role information is the most interesting direction.** J_ROLE_SUPPLY_LOAD
beats J_BASE on the event objective in 37/44 quarters and all 11 seasons
(equal-quarter difference −.0003984). J_ROLE alone does so in 35/44 quarters
and 9/11 seasons. This supports better intermediate predictions as well as a
better point blend. Constraints alone have a much smaller event improvement.

But ROLE is not yet identified as learned adaptability. The extra head reads
the player's own current state plus eight dated recent/long and historical
teammate features. It does not receive the proposed other four inside that
extra head. It can act as a richer individual state correction, alongside the
existing contextual network. J_SELF lacks the same eight inputs, so that
comparison does not isolate placement versus new information. A matched-input
individual-head versus receiver/context-head test is warranted before claiming
we captured Westbrook's ability to change roles.

**Creation/load has a useful basketball effect but fragile accuracy evidence.**
Seed17 constraints improve standalone pooled RMSE versus J_BASE by .01390;
seed23 constraints worsen it versus J_BASE_S23 by .00740. The half-blend
contrast likewise changes sign. Constraints improve novel RMSE at both seeds,
but recurring performance offsets that at seed23. The best ROLE combination
has only one seed. Its small improvement over ROLE alone is not established
by season intervals.

**Training the blend is viable, not decisively superior.** B_BASE and
B_SUPPLY_LOAD are the best direct forecasts, but both trail the old external
blend. B_SUPPLY_LOAD versus B_BASE is only −.00227 pooled RMSE, with an
equal-season interval spanning zero. Keep it as a useful alternative rather
than declaring the B family the final solution.

**Event supervision earns its place.** Removing it in B_POINT worsens both
point RMSE (10.83074 versus B_BASE 10.81805) and the event objective in all
44 quarters. Optimizing only the point target did not solve value integration.

**Attention/covariance/capacity did not lead this campaign.** The tested
one-head attention gives small changes; covariance is worse than J_BASE on
pooled direct RMSE. SELF and dropout are modest. This closes neither all
attention architectures nor all individual-state models. It says the tested
extra representations were less productive than the role inputs here.

**The message-off residual is not the best interface.** R_BASE/R_SUPPLY_LOAD
trail the B forecasts and old HALF. F−F_off is a particular intervention on
this model, not a uniquely identified basketball complementarity quantity.

### Complete arm comparison

Direct forecasts below include prior-only calibration. Secondary is half
additive / half that forecast. Same primary population throughout.

| Arm | Direct RMSE | Direct r² | Secondary RMSE | Secondary r² |
|---|---:|---:|---:|---:|
| B_BASE | 10.81805 | .12415 | 10.80549 | .12618 |
| B_POINT | 10.83074 | .12209 | 10.81227 | .12509 |
| B_SUPPLY_LOAD | 10.81579 | .12452 | 10.80518 | .12623 |
| E_BASE | 10.86691 | .11622 | 10.80742 | .12587 |
| E_SUPPLY_LOAD | 10.86296 | .11686 | 10.80602 | .12610 |
| J_ATTN | 10.84778 | .11933 | 10.80508 | .12625 |
| J_ATTN_SUPPLY_LOAD | 10.84365 | .12000 | 10.80334 | .12653 |
| J_BASE | 10.85544 | .11809 | 10.80494 | .12627 |
| J_BASE_S23 | 10.84549 | .11970 | 10.79824 | .12736 |
| J_COV | 10.86647 | .11629 | 10.80716 | .12591 |
| J_DROPOUT | 10.85317 | .11846 | 10.80500 | .12626 |
| J_LOAD | 10.85384 | .11835 | 10.80421 | .12639 |
| J_ROLE | 10.83934 | .12070 | 10.79843 | .12732 |
| J_ROLE_SUPPLY_LOAD | 10.82915 | .12235 | 10.79364 | .12810 |
| J_SELF | 10.84997 | .11898 | 10.80392 | .12644 |
| J_SUPPLY | 10.84205 | .12026 | 10.79864 | .12729 |
| J_SUPPLY_LOAD | 10.84154 | .12034 | 10.79799 | .12740 |
| J_SUPPLY_LOAD_S23 | 10.85289 | .11850 | 10.80278 | .12662 |
| R_BASE | 10.82766 | .12259 | 10.81663 | .12438 |
| R_SUPPLY_LOAD | 10.82798 | .12254 | 10.81675 | .12436 |

## 4. Basketball coherence: progress without a pass declaration

Latest-quarter five-Gobert fixture:

| Model | Five Goberts native F | Five Goberts final | Conventional real five final |
|---|---:|---:|---:|
| J_BASE | 121.62 | 121.25 | 118.79 |
| J_SUPPLY_LOAD | 119.35 | 119.73 | 118.86 |
| J_ROLE_SUPPLY_LOAD | 118.94 | 119.36 | 119.32 |
| B_SUPPLY_LOAD | 114.41 | 114.76 | 119.38 |

Constraints in the saved J_ROLE_SUPPLY_LOAD fit lower five-Gobert native F by
3.36 and final offense by 2.32 versus disabling constraints. Disabling messages
raises native F by 7.02 and final offense by 4.85. Their intended negative
effect survives the readout, unlike v12's anchor-subtraction reversal. The
conventional unit is unaffected by the explicit constraints in this fixture.

However, standalone ROLE's five Goberts remain essentially tied with the real
unit. Its external blend makes the gap 115.58 versus 119.19 partly by relying
on additive's lower center rating. Even B_SUPPLY_LOAD still assigns 38.84 FTA
per 100 to five Goberts; ROLE_SUPPLY_LOAD assigns 39.55. The explicit constraint
helps but has not resolved the model's generous extrapolation of foul-drawing
opportunities. This is an opportunity-generation/role-allocation problem, not
evidence we should hand-code a desired center score.

In the Jokić/Murray comparison, ROLE's final NN forecast is 123.60 with Korver
and 121.50 with Westbrook; additive is 124.71 and 125.79, respectively. The
adjustment relative to additive favors Korver, but both adjustments are
negative. Meanwhile the message-off intervention boosts Westbrook's version
more than Korver's (+5.20 versus +2.28 native points). These are different
baselines, not interchangeable definitions of chemistry. We should retain
Adam's willingness to be surprised rather than train toward named signs.
The separate historical-Korver injection retains its mixed-era/additive-state
disclosure; it is not a fully transported player-season comparison.

Some largest observed failures are useful discussion material. The new blend
raises the 2018q1 Westbrook/George/Anthony/Adams/Roberson five from old HALF's
114.55 to 115.67, versus observed 102.02 over 494 possessions. It lowers the
2019q4 Curry/Thompson/Durant/Iguodala/Green five from 122.00 to 120.03, versus
126.62 over 402 possessions. Conversely it improves the 2016q4
Durant/Westbrook/Ibaka/Adams/Roberson five from 109.92 to 111.21, versus 114.56
over 1,003 possessions. These are selected residual cases, not causal proofs
or training constraints. Full ≥100/≥200-possession benefit/harm tables and
player/event/additive ledgers are in `winner_cases.csv`.

No arm models the actual opposing five or defense. Thus small-guard rim
protection and five-center perimeter defense still cannot be tested by these
offensive predictions. Rebound possession renewal is unchanged. Do not infer
the original two-lineup product is complete from point-forecast progress.

## 5. Uncertainty remains a separate unfinished standard

For the leading blend, primary 80% finite-outcome coverage is 79.15% by cell /
79.06% possession-weighted, with mean full width 31.84 points/100. At 95%,
coverage is 94.60% / 94.36%, width 49.58. Old HALF is 79.49% / 79.35% at 80%
and 94.54% / 94.13% at 95%. Novel-lineup weighted coverage for the new blend is
79.59% and 93.99%. This is broadly similar finite-batch calibration, not a new
validated uncertainty capability.

Sixteen MC-dropout passes have SD .30 on the conventional fixture and .56 on
five Goberts; the clone ladder grows roughly .30/.42/.50/.52/.56. This is a
useful sensitivity direction, but a .56-point SD must not be presented as our
confidence about a never-observed five-center lineup's true offense. These
draws concern J_DROPOUT, not the winning ROLE model. Seed disagreement likewise
is not a calibrated latent-mean posterior. No coverage gate is proposed.

## 6. Epoch selection and Adam's recent questions

No fit reached the 96-epoch cap. Selected counts span 1–57; the longest inner
curve ran 65 epochs including patience. Median selections: E_BASE 21, J_BASE
13, J_ROLE_SUPPLY_LOAD 12, B_SUPPLY_LOAD 14.5, B_POINT 5.5. Merely raising the
cap would not change these runs.

The concern about nearly tied epochs is real but not pervasive at the existing
1e-5 tolerance: 63/960 fits have an earlier epoch within 1e-5 of the selected
minimum; 29 differ by at least five epochs, maximum eight. This is a diagnostic
of saved curves, not a tested alternative stopping rule. Broader validation
noise and seed effects may be larger than these tiny threshold ties. Only
best-inner/reset-final weights are saved, so genuine late-checkpoint prediction
averaging needs new fits/checkpoint collection. Do not simulate it by averaging
scalar validation losses or selecting a new epoch using outer performance.

## 7. Recommended next decision, not an authorized launch

1. **Replicate and identify the role improvement.** Matched seeds for J_BASE,
   J_ROLE, J_SUPPLY_LOAD and J_ROLE_SUPPLY_LOAD; retain B_SUPPLY_LOAD as the
   basketball alternative. Freeze seed averaging before evaluation. Separate
   the extra dated information from individual-head versus contextual-head
   placement using equal-input controls. This tests an actual ambiguity exposed
   by v13, rather than simply increasing capacity.
2. **Repair opportunity generation, not the fixture score.** Investigate why
   centers retain so many FTs when creation is missing, and distinguish being
   assisted from supplying creation. Diagnose count/role allocation on held-out
   observed lineups before changing the supply proxy or its penalty. Keep the
   good real small-ball units and detailed event ledgers as controls.
3. **Test current league level/season stage as a shared causal layer.** Compare
   a prior-years stage curve and a recent completed-games level update against
   the existing calibration, equally for additive and NN. Never estimate a
   forecast-season mean from its future games. This is a separate source of
   error from player complementarity, so do not give its gains to the NN.
4. **Use replication to evaluate training stability.** If adding checkpoint
   averaging/EMA, predeclare checkpoints and inner-only selection. Do not make
   optimization smoothing the explanation for every architectural null.
5. **Keep the larger product work visible:** aligned actual-opponent inputs,
   defensive mechanisms, offensive-rebound possession renewal, and calibrated
   uncertainty about hypothetical *mean* quality. These require separate
   designs/authorization; v13 did not settle them. Prefer one coherent product
   extension over another undirected architecture sweep.

No new fits or model selection rules were implemented during this review. Next
step is discussion with Adam, then a frozen follow-up design if authorized.

## Handoff and reproduction

Read this report before historical launch notes. Original production remains
read-only. Codex has finished editing; no training or worker is active.

Derived files: `scores.csv`, `seasons.csv`, `quarters.csv`, `contrasts.csv`,
`stopping.csv`, `ledger_errors.csv`, `winner_cases.csv`, `fixture_summary.csv`,
`dropout_summary.csv`, `coverage.csv`, `receipt.json`, `audit.log`, all under
the successful `_v2` review prefix above. The contrast file includes both seed
controls and secondary-half comparisons. It contains post-hoc diagnostics,
not new preregistered acceptance tests.

To reproduce the audit, choose a **new nonexistent** output directory:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v13_postrun_audit --output-dir experiments/cache/joint_capability_v13_review_recheck
```

This verifies/reads saved artifacts and writes only the new derived directory;
it does not retrain. Its durable log is `<output-dir>/audit.log`. No commit,
scrape, database access, cache rebuild, deployment or scorer promotion occurred.
