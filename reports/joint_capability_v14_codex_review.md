# v14 independent review — September 17, 2026

## Bottom line

This is useful progress, not a breakthrough or a finished product. The campaign
supports keeping explicit rebound renewal and studying role transport. It does
not support adding every new component, claiming a solved Adams facilitation
mechanism, or choosing the pooled-RMSE winner as the unquestioned product model.

The leading calibrated neural ensemble, **RB_RENEW_FAC_SHIFT**, has RMSE
10.79367 and r² .12809, versus additive 10.84099/.12043. Its external half blend
has 10.77978/.13034, the best pooled primary score in this campaign. These are
modest improvements: roughly 0.56% lower RMSE / 1.13% lower MSE than additive
for the blend, and 0.26% lower RMSE than old HALF. ROLE_SL still has the best
ensemble-blend MAE, 8.03297 versus the RMSE leader's 8.04230.

The strongest evidence is the combination of matched-seed directions, modest
opportunity-prediction gains, and coherent rebound accounting. The biggest
remaining deficiencies are still extreme-lineup offense, identification of
player-to-teammate influence, actual opponents, and latent-quality uncertainty.

**Research recommendation:** retain ROLE_SL as the simpler control,
RB_RENEW_FAC as the interpretable renewal candidate, and RB_RENEW_FAC_SHIFT as
the point-prediction challenger. Do not promote any scorer or launch another
campaign automatically. The three product standards remain co-equal.

## 1. Scope, population and integrity

Source: `experiments/cache/joint_capability_2026_09_15_v14_prod`.
The process exited 0 after 159,127 seconds (44h12m), with status
ANALYSIS_COMPLETE. There are 2,304 completed design/seed/origin cases:
16 designs × three seeds × 48 origins, including 336 verified reused controls
and 1,968 new cases. The reports contain 80 forecast paths and 7,896 fixture
rows. Completed source artifacts were not edited during this review.

Primary evaluation is the same **44 quarter-season windows, 2016–2026**:
5,607 offensive-lineup/window cells, weighted by 726,364 possessions.
Novel: 2,073 cells / 226,256 possessions. Recurring: 3,534 / 500,108.
2015 supplies calibration warmup, not primary performance. These r² values
describe aggregated lineup offensive ratings, **not individual-possession r²**.
The three seeds share outcomes and are not three independent data replications.

The primary neural forecast averages three **separately prior-calibrated**
seed predictions. “Half” then means 50% corrected additive and 50% that neural
ensemble. B_SL is different: it already contains additive in its trained
readout; applying another external half is not 50% additive / 50% native NN.
All headline comparisons below use the registered NONE league-level policy.

Independent review scripts:

- `experiments/v14_postrun_audit.py`: hashes, completion/epoch receipts, exact
  selected minima/final lengths, calibration cutoffs/counts, point/additive/
  rebound ledgers, seed means, independent weighted metrics, season contrasts,
  interval provenance, fixture mixtures and matched case examples.
- `experiments/v14_postrun_analysis.py`: seed/parent, league, opportunity,
  capture, phase, support, within-quarter, fixture and stability summaries.

Final derived evidence uses new prefixes
`experiments/cache/joint_capability_2026_09_17_v14_codex_review_verified` and
`experiments/cache/joint_capability_2026_09_17_v14_analysis_verified`.
Each has a durable log and a source-linked receipt. No fits, database calls,
scraping, input rebuilding, deployment, promotion, delegation or commit.

Final audit status **PASS**:90 code hashes,38 source hashes,678 report-output
hashes, all2,304 completion/checkpoint records. Largest native scoring-ledger
error2.35e-5pts/100; renewal error5.96e-8opportunities/possession. Prior-only
calibration reconstruction and ensemble scorecards agree to1e-8 or better.

### Reporting qualifications discovered during review

1. The automatic **persistent-error summary includes 2015 warmup** (1,993 cells,
   12 seasons). Its primary-population version is now a separate derived table:
   1,805 cells, 11 seasons. Original outputs remain untouched. Headline
   scorecards and interval summaries already excluded warmup correctly.
2. `first_budget` in saved cells/fixtures is the first-pass **U_ref**, not the
   non-rebound baseline **B**. The correct renewal audit reads B from each
   saved scoring context. The first audit attempt confused these, failed, and
   was preserved; this was an audit-reader mistake, not a model accounting bug.
3. Fixture files already include `ensemble3` alongside the three seed rows.
   Recompute means from seeds only, then verify the saved ensemble; do not
   treat four rows as four independent fits. Mixed seed fields require string
   dtype. The final analysis was rerun with the final helper hash.
4. Tiny tail calibration bins must show exposure. For RB_RENEW_FAC the 40–50%
   predicted-recovery bin contains **three live chances**, not evidence that
   extrapolation to center-heavy units is validated or disproven.

## 2. Forward prediction

### All-arm primary results

Lower RMSE/MAE is better. Every new row is a three-seed ensemble.

| Design | Direct RMSE | Half RMSE | Half MAE | Half r² |
| --- | ---: | ---: | ---: | ---: |
| BASE | 10.83309 | 10.79762 | 8.05485 | .12746 |
| ROLE | 10.83274 | 10.79759 | 8.04634 | .12746 |
| SL | 10.83277 | 10.79740 | 8.05337 | .12749 |
| ROLE_SL | 10.81348 | 10.78859 | **8.03297** | .12891 |
| B_SL | 10.80995 | 10.80338 | 8.05947 | .12653 |
| RECENT_SL | 10.82928 | 10.79637 | 8.05227 | .12766 |
| HISTORY_SL | 10.83016 | 10.79635 | 8.04623 | .12766 |
| CURRENT_SL | 10.81547 | 10.79241 | 8.04762 | .12830 |
| SHIFT_SL | 10.80739 | 10.78426 | 8.04582 | .12961 |
| FTA_ROUTE | 10.81402 | 10.78890 | 8.03339 | .12887 |
| RB_AUX_DIRECT | 10.81782 | 10.79050 | 8.03607 | .12861 |
| RB_AUX_FAC | 10.82068 | 10.79256 | 8.03886 | .12827 |
| RB_RENEW_DIRECT | 10.81414 | 10.78787 | 8.03699 | .12903 |
| RB_RENEW_FAC | 10.80733 | 10.78462 | 8.03744 | .12956 |
| RB_RENEW_FAC_ROUTE | 10.80720 | 10.78446 | 8.03737 | .12958 |
| RB_RENEW_FAC_SHIFT | **10.79367** | **10.77978** | 8.04230 | **.13034** |

Controls: additive MAE8.09195/RMSE10.84099/r².12043/correlation.35326;
old V9 HALF 8.07273/10.80812/.12576/.35789;
v13 single-seed ROLE_SL half 8.03415/10.79364/.12810/.36104.
New best half correlation is .36396, direct .36084.

The three-seed ROLE_SL control already improves on the v13 single-seed result.
Do not credit that averaging improvement to new role transport or rebounding.
The matched new-combination increment over three-seed ROLE_SL half is only
**−.00881 RMSE**; over the simpler renewal half it is **−.00483**.

### Novel versus recurring

| Forecast | Novel RMSE | Recurring RMSE |
| --- | ---: | ---: |
| Additive | 11.85302 | 10.35068 |
| Old V9 HALF | 11.76624 | 10.34554 |
| ROLE_SL direct | 11.76840 | 10.35257 |
| ROLE_SL half | 11.76977 | 10.31407 |
| RB_RENEW_FAC direct | 11.75518 | 10.35002 |
| RB_RENEW_FAC half | 11.76307 | 10.31149 |
| RB_RENEW_FAC_SHIFT direct | 11.76224 | **10.32567** |
| RB_RENEW_FAC_SHIFT half | 11.76679 | **10.30223** |

The combined winner is primarily another **recurring-lineup improvement**.
It is effectively tied with old HALF on novel lineups. The renewal direct
models have the best new novel scores; adding SHIFT is not uniformly helpful.
The route variant is numerically best direct novel at11.75401, but its
near-equivalence to renewal without routing does not justify a new mechanism claim.

### Season-level uncertainty and seed replication

These are equal-season mean RMSE differences, not differences of pooled RMSE.
Intervals are descriptive nominal t95 over 11 seasons; historical data have
been repeatedly examined. They are not fresh confirmatory tests.

| Contrast | Mean season ΔRMSE | t95 interval | Favorable seasons |
| --- | ---: | --- | ---: |
| ROLE_SL half − additive | −.05110 | [−.08269, −.01952] | 9/11 |
| ROLE_SL half − old HALF | −.01826 | [−.03570, −.00081] | 9/11 |
| Renewal FAC half − additive | −.05599 | [−.08756, −.02442] | 9/11 |
| Renewal FAC half − old HALF | −.02314 | [−.04055, −.00573] | 9/11 |
| Renewal FAC+SHIFT half − additive | −.05905 | [−.08870, −.02940] | 9/11 |
| Renewal FAC+SHIFT half − old HALF | −.02620 | [−.05414, +.00173] | 8/11 |
| Renewal FAC+SHIFT half − ROLE_SL half | −.00794 | [−.02302, +.00714] | 8/11 |
| Renewal FAC+SHIFT direct − additive | −.04439 | [−.09802, +.00924] | 8/11 |

None of the **19 registered direct-ensemble architecture contrasts** survives
the report's Holm correction. That qualifies architecture-selection certainty;
it does not mean all mechanisms are useless. In particular, the matched-seed
directions contain information that the earlier single-seed campaign lacked:

| Direct contrast | Seed17 ΔRMSE | Seed23 | Seed41 |
| --- | ---: | ---: | ---: |
| ROLE_SL − ROLE | −.01019 | −.01861 | −.03132 |
| ROLE_SL − SL | −.01239 | −.02893 | −.01080 |
| SHIFT_SL − ROLE_SL | −.00562 | −.00538 | −.00540 |
| RB_RENEW_FAC − RB_AUX_FAC | −.01520 | −.01415 | −.01414 |
| RB_RENEW_FAC − RB_RENEW_DIRECT | −.02771 | +.00083 | +.00340 |
| RB_RENEW_FAC_SHIFT − RB_RENEW_FAC | −.01299 | −.01831 | −.00517 |
| RB_RENEW_FAC_SHIFT − SHIFT_SL | −.02738 | −.00719 | −.00338 |

Thus role+constraints, shift inputs and renewal are reproducible *directions*
here. The incremental point benefit of facilitation over direct capture is
much less secure and is largely seed17 in the renewal contrast.

SHIFT's overall advantage is not equally contemporary. SHIFT half improves
ROLE_SL strongly in2016–17, worsens2019, and is slightly worse in the pooled
2024–26 era (10.94349 versus10.94163). Renewal improves recent-era performance;
combined half10.92824 is close to renewal-only10.93065. Retain chronological
breakdowns rather than extrapolating the all-years winner to today's transfers.
Dropping any one season leaves the combined-half versus old-HALF mean RMSE
advantage negative (range−.03141 to−.01891). It is not a one-season artifact,
even though its full nominal interval still includes zero.

### This is not just a league-level advantage

An explicitly post-hoc diagnostic removes each quarter's outcome and prediction
means solely to measure within-quarter discrimination—not to make new forecasts.
Centered within-quarter r² is .05618 for additive, .06046 for old HALF,
.06265 for ROLE_SL half, .06382 for renewal FAC half, and .06536 for the
combined half. The ranking benefit survives removal of quarter-level bias.
These centered r² values have a different denominator from headline pooled r².

The registered common league corrections mostly hurt. Additive alone benefits
from RECENT (RMSE10.82434 versus10.84099), but best half worsens to10.78411,
STAGE to10.79350, BOTH to10.81665. ROLE_SL half gains only.00081 from RECENT.
This rejects automatic adoption of **these correction formulas**, not Adam's
idea that NBA scoring can have within-season cycles. Do not select different
policies post hoc for different arms and call that the registered comparison.

## 3. What the mechanisms learned

### Role information: retain both history and recent state; investigate transport

Removing either half of the eight role features hurts ROLE_SL:
recent-only direct10.82928, history-only10.83016 versus10.81348.
The experiment therefore does not support “just emphasize recent data more.”
Current-teammate levels alone are also not an improvement (10.81547).
The proposed-minus-historical **shift representation** is more promising.

The new combined model helps the predeclared high-shift stratum relative to
ROLE_SL: direct11.48656 versus11.51760; half11.47247 versus11.48660.
It slightly hurts low-shift: direct10.00653 versus9.99083. This is consistent
with adaptation helping where context changes, but these are broad support
bins, not a test specifically of trades, nor proof of causal role adaptation.

The architecture still lets a small head transform dated own/role inputs.
It does not explicitly solve offensive responsibilities among five players or
model a coach assigning a new role. A historical transfer benchmark remains
important before describing Brown-in-Philadelphia-type answers as validated.

### Rebounding: renewal is the useful point connection

Adding an auxiliary rebound head without changing the possession budget does
not improve pooled points over ROLE_SL. Feeding the recovery process back
into opportunities is the promising step. This also has a measurable target
outside the final rating:

| Three-seed opportunity forecast | FGA RMSE | Usage-budget RMSE |
| --- | ---: | ---: |
| ROLE_SL | 24.04306 | 16.49403 |
| RB_AUX_FAC | 24.04259 | 16.49403 |
| RB_RENEW_FAC | 24.00123 | 16.40455 |
| RB_RENEW_FAC_SHIFT | 24.00032 | 16.40468 |

Units are per100 possessions on game×lineup rows; these are noisier/different
targets from the headline lineup-quarter ratings. Known-FGA/FTA masks are
respected. Modest improvements, not dramatic reductions in noise.

The renewal ledger is `U = B + ORB`, with average existing rebound opportunities
subtracted from U_ref before adding model-specific renewals. No double payment
and no independent rebound point bonus. Continuation averages about.075 and
maxes around.116 on the primary ensemble cells—no near-singular explosion.
Isolated recovery interventions increase native offense as required.

Adding the rebound objective can alter early stopping, even where the auxiliary
head has no direct gradient into the offense backbone. Auxiliary-vs-parent
point changes therefore are not pure evidence that a learned rebound feature
influenced offense. The matched fixed-budget/renewal contrasts are more useful.

### Facilitation: small real predictive signal, unproven basketball attribution

On1,035,863 held-out eligible live recoveries (235,155 offensive), fixed-budget
multinomial NLL improves .848872→.848700 with facilitation; capture NLL
.532531→.532396. Renewal versions give .848910→.848747 and
.532540→.532423. The capture/multinomial improvements have the favorable sign
in **all11 seasons**. Equal-season capture-NLL difference for renewal is
−.000119, nominal t95[−.000180,−.000058]. These are tiny but consistent.

That establishes a little predictive information in teammates for recovery.
It does **not** establish that the donor coefficient identifies box-outs,
Adams's causal influence, or a portable “makes teammates better” effect.
Own and donor heads can trade explanatory credit, and opponent/assignment
variables are absent. Competition can redistribute a team's collector shares.

With Brunson/Bridges/Anunoby/Hart fixed, renewal FAC predicts:

| Fifth player | Team ORB/100 | His ORB/100 | Other four ORB/100 | Direct offense | Half |
| --- | ---: | ---: | ---: | ---: | ---: |
| Steven Adams | 12.038 | 7.382 | 4.656 | 121.488 | 121.367 |
| Mitchell Robinson | 12.198 | 7.594 | 4.604 | 122.047 | 121.818 |
| Rudy Gobert | 9.611 | 4.773 | 4.838 | 120.464 | 120.238 |

Adams narrowly exceeds Robinson for others' credited boards, but trails Gobert;
team totals favor Robinson. Adams's learned donor score is negative (−.165)
relative to the model's zero-input anchor. Do not rename his large **own** ORB
prediction a positive facilitation effect. Turning off the **whole lineup's**
facilitation changes Adams-lineup ORB by only−.060/100; that intervention does
not isolate Adams's own donor contribution. Hart→DiVincenzo reduces team
ORB12.038→11.779; Hart's own prediction1.867 exceeds DiVincenzo's.996.
That is a sensible check, not proof the attribution is causal.

### FTA routing: essentially null, and it misses the larger problem

FTA_ROUTE barely changes ROLE_SL; adding it to renewal changes direct RMSE by
−.00013. It has not solved excessive center free throws: five Goberts still
receive about37.44FTA/100 versus37.42 for ROLE_SL. The learned routing fraction
is about.91 toward turnovers in that fixture, so this path remains close to the
old routing choice. More importantly, it only redistributes the opportunities
removed by the existing shortage rule; it does not establish whether the
original foul-drawing opportunities could be generated at all.

### Renewal's stationary shot-cycle assumption remains a limitation

Across primary phase-labeled shots, observed FG% is46.83% before any ORB and
52.62% after an eligible FG ORB. The current decoder, evaluated conditional on
the observed shot-location counts, predicts about46.07% and53.73% respectively
for renewal FAC. Post-ORB conversion is overpredicted by about1.10 percentage
points, while initial conversion is underpredicted by.76points.

These are conditional audits, not standalone predicted phase FG%. They neither
prove that putbacks should simply get a bonus nor fully separate shot quality
from shooter selection. Nevertheless, the same-mix/same-efficiency renewal
approximation is testable and visibly imperfect. A two-phase decoder is a
reasonable future ablation once label omissions/support are respected.

## 4. Basketball counterfactuals: no overall pass yet

All below use the same saved2026q4 scoring states and calibrated three-seed
forecasts. They are hypothetical model outputs, not observed outcomes.

| Design | Five Goberts direct / half | Conventional real five direct / half | Gobert FTA/100 |
| --- | --- | --- | ---: |
| ROLE_SL | 118.61 / 115.21 | 119.18 / 119.12 | 37.42 |
| SHIFT_SL | 120.96 / 116.38 | 119.41 / 119.24 | 39.86 |
| RB_RENEW_FAC | 117.85 / 114.82 | 119.72 / 119.39 | 36.63 |
| RB_RENEW_FAC_SHIFT | 120.01 / 115.91 | 118.84 / 118.95 | 38.76 |

The best-RMSE native candidate still ranks five Goberts **above** the conventional
five. External blending reverses that partly through additive. Renewal alone
is somewhat better on this probe, but neither has earned a strong basketball
coherence claim. Real limited-center mixtures are penalized more appropriately;
that does not excuse clone extrapolation. Defense is not modeled here, so the
small-guard lineup's high offensive rating is not a forecast of its net strength.

Jokic/Korver versus Jokic/Westbrook still has a contextual difference, but do not
force the desired answer. Renewal FAC direct predicts125.56 versus123.00;
combined direct124.61 versus122.69. Historical Korver-profile substitution
changes renewal FAC to126.15. These are dated/transport-sensitive probes, not
evidence that Korver is a better overall player or that actual substitution
would causally realize the modeled advantage. “NN minus additive” also is not
a purified chemistry parameter: it includes calibration/value differences.

## 5. Honest uncertainty: finite outcomes okay, latent OOD still unfinished

For the leading half,80%/95% interval cell coverage is79.19%/94.63%; average
full widths31.71/49.24pts per100. Novel coverage79.64%/93.83%, recurring
78.92%/95.11%. High-composition-distance95% coverage93.88% versus95.36% in
the low bin. These are reasonably close, with some undercoverage, not perfect.

The interval procedure still scales empirical prior errors by1/sqrt(possessions).
It estimates **future finite-batch offensive-rating outcomes**, not uncertainty
about an arbitrary lineup's true quality. Broad coverage on real lineups does
not validate a five-center mean or justify indefinitely shrinking its interval
as hypothetical possessions increase. Seed disagreement—weighted mean SD.544
pts100 for the leading direct ensemble—is optimizer sensitivity, not an honest
posterior and not a replacement for this missing uncertainty model.

The corrected primary persistent-error diagnostic retains negative products:
equal-season averages are7.65 for additive,7.03 old HALF,6.56 ROLE_SL half,
6.51 renewal half and6.60 combined half, in squared-rating units. All individual
nominal intervals cross zero and are wide (combined[−2.29,15.50]). No positive
“error floor” can be inferred by clipping these or taking an unqualified square
root. Shared opponent/environment noise remains; this is not latent coverage.

## 6. Stability, failures and useful case work

No96-epoch cap was hit. Selected epochs range1–64; arm medians9–15.
The campaign offers no operational argument for simply increasing the cap.
The audited logged inner-fit gradient maximum is1.492, below the clip5 threshold.
Three-seed averaging improves direct RMSE versus average seed RMSE by roughly
.007–.013, but the best individual seed can still beat the ensemble.

The registered seed41 last-up-to-three-epoch **prediction** mixture helps
direct RMSE in11/16 designs and half RMSE in10/16, but not universally.
For renewal FAC direct it helps.02007; for ROLE_SL it hurts.00174 and BASE
.00662. Keep it as a predeclared future training-policy candidate, not a
post-hoc switch applied only to arms where it won. It was not weight averaging.

The saved case library includes both largest improvements and harms with the
fixed >=200-possession threshold. These are exploratory examples, not a new
evaluation population. Improvements include the2016q1 Detroit starters
(811poss: actual107.27, additive112.45, new half109.69) and2017q1 Warriors
with Durant/Pachulia (465poss: actual115.91, additive113.13, half116.32).

A useful persistent failure is **Irving / LeBron / J.R. Smith / Love / Thompson**:

| Origin | Possessions | Actual | Additive | Combined direct | Combined half |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2016q2 | 235 | 121.70 | 117.47 | 111.58 | 114.52 |
| 2016q3 | 440 | 117.05 | 116.74 | 111.28 | 114.01 |
| 2016q4 | 889 | 119.46 | 116.68 | 111.79 | 114.23 |

The last cell spans31 games, not merely a few possessions. All major native
arms are low there: BASE112.26, ROLE_SL110.88, SHIFT111.73, renewal111.19.
Neither creation-shortage nor overload penalties are active for the five in
the combined forecast. This is not solved by weakening those constraints.
On the26 fully observed FG/FT game rows (733poss), seed17 predicts89.81FGA,
24.55FTA,12.86TO per100 versus observed95.09/21.01/13.10. That points toward
opportunity/mix/value misspecification as well as possible conversion effects;
it is not sufficient to blame shooting percentage alone. The full889-possession
rating comparison is retained even though some event labels are incomplete.

The additive player base+carry+experience contributions on that q4 cell are
Irving+3.018, LeBron+6.063, Smith+1.328, Love+1.250, Thompson−1.351.
They are lineup-score contributions in points/100, already multiplied by
the saved calibration slope; adding the common level
reconciles the final forecast. They are not comparable in meaning to each
player's share of all scored points.
No case-specific coefficient or bonus was added.

## 7. Next direction: fewer ambiguities, not more generic capacity

Recommended priorities for discussion; these are **not newly authorized fits**.

1. **Build the systematic transfer/role-change benchmark Adam proposed.** Freeze
   eligibility before examining model errors: offseason team changes, dated
   preseason cutoffs, prespecified substantial-exposure thresholds, all eligible
   transitions rather than famous successes. Keep a broad cohort and report
   multiple exposure thresholds to disclose survival/rotation selection. Compare
   A, old HALF, ROLE_SL, renewal and renewal+SHIFT on exactly the same outcomes;
   include a frozen-old-context control to distinguish new player-value data from
   actual adaptation. Rate/mix/recovery diagnostics and team-season clustered
   uncertainty; development on already-used years, stronger prospective evidence
   on a genuinely future season. This is predictive transport, not causal trade
   value or a health/availability model.
2. **Investigate repeated real-lineup failures and the center action pathway
   together.** Use the pre-existing saved case library, not name-specific fixes.
   Separate profile/main-value, action allocation, conversion and calibration.
   Ask whether each FGA/FTA can be generated by the modeled creators/finishers,
   instead of only changing where already-removed FTA are rerouted. Preserve
   ROLE_SL/renewal controls and all three product criteria when preregistering
   any changed action mechanism.
3. **Actual opponent inputs/defense are the largest distinct product expansion.**
   The model currently has five offensive players against an implicit average
   defense. A ten-player/grouped matchup representation would permit offensive
   strengths × defensive personnel, including live-rebound competition. First
   establish a causal dated defensive baseline and matchup-keyed evaluation;
   do not simply add an opponent embedding and declare defensive assignments
   learned. This advances the original two-lineup product rather than polishing
   only another offensive leaderboard increment.
4. **Two-phase rebound offense is a bounded mechanistic follow-up.** The labels
   now support examining first-chance versus post-recovery mix/conversion.
   Separate this from opponent effects, preserve missing-label masks, and compare
   to the stationary renewal control. Do not force an Adams donor bonus or use
   observed outer-phase outcomes as inputs.
5. **Give latent-quality/OOD uncertainty its own evaluation target.** Separate
   finite-game variation, persistent model error and lack of support; test on
   held-out compositions/transfers with repeated games. Neither ensemble spread
   nor current interval coverage constitutes completion. Avoid a coverage gate;
   the product should still answer, honestly and with wider uncertainty.

Keep the primary three-seed policy. If changing stopping/checkpoint aggregation,
freeze that policy prospectively and apply it to all compared architectures.
Do not revive broad embedding/attention/capacity sweeps without a diagnosed
representation bottleneck. The current evidence points more directly toward
**what opportunities and matchups the model represents**, not a need for a
larger generic network.

## Handoff

Review completed by Codex directly. All original production/pilot artifacts and
the frozen scientific protocol are preserved. New review scripts, derived
tables/logs and this report document the work. No training is running from this
review; there is no new launch command or automatically selected scorer.
Next action is discussion/preregistration of the next bounded workstream, not
resuming v14 or fitting a winner-adjusted variant. Source changes remain
uncommitted; the preceding live-leaderboard changes remain preserved as well.
