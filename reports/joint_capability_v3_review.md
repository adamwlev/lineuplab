# Joint capability v3: completed review

Completed 2026-09-09 by Sol/Codex execution of
`SOL_JOINT_CAPABILITY_DAY2_PLAN.md`. The immutable scientific run is
`experiments/cache/joint_capability_2026_09_09_v3/`. No scraper, database,
source cache, scorer, page, or deployment changed. No candidate is promoted.

## Decision in one paragraph

Keep H3 as the structural research backbone, while keeping corrected additive
as the predictive baseline. Actual teammate information has now passed two
meaningful controls: H3 beats the same-capacity fixed-sender H3F on outer event
loss in all 44 primary quarters, and beats a date/role-bin context shuffle in
all four pre-specified diagnostic origins. H3 also beats H3F on season-paired
RMSE and r². It does not beat corrected additive on pooled point prediction,
and the new composition-distance intervals do not improve calibration. The
architecture is therefore promising and interpretable, but not ready to score
the public tool.

## What changed from v2

Protocol repairs:

- Losses accumulate global numerator/exposure pairs before division, so
  validation is invariant to batching and zero-exposure examples.
- A 730-day half-life now weights every training family, its baseline scale,
  standardization, and output penalties. Outer evaluation remains unweighted.
- FGA/FTA attribution and location masks preserve known labels without treating
  unknown actors or locations as zeros. Assisted player-games are masked when
  they do not reconcile.
- Conversion initialization is a league location curve plus pooled, moment-EB
  two-point and three-point player offsets. The four recent-role contrasts,
  including recent 3PA share, were restored.
- Inner training uses its own five-year prefix. Origin exports include every
  player with pre-cutoff history plus one generic fallback, rather than being
  selected by the future roster.
- Early stopping distinguishes the exact best finite checkpoint from the
  patience reference. Final refits use exactly the selected epoch and never use
  outer outcomes.

Prospective design choices:

- Decoder regularization is separated from network regularization. Development
  selected common decoder gamma 0.01. Network lambdas are H1=.01, H2=.01,
  H3=.0001, H3F=.01; H3 remains on its extended low boundary and this is a
  qualification, not an invitation to extend the grid after seeing results.
- Maximum epochs/patience/minimum improvement are 24/3/1e-5, seed 17.
- H3F provides H3's encoder/message capacity but replaces each real sender with
  the training-prefix reference state. H3-H3F isolates the value of actual
  teammate inputs more cleanly than H3-H1.
- The uncertainty audit adds the pre-registered older-half isotonic distance
  scale/newer-half residual quantile, plus four-origin context-shuffle, FT, and
  alternate-seed controls.

## Model and learned parameters

All arms decode five players into FGA, FTA, turnovers, six shot-location shares,
six conditional make probabilities, FT make probability, and assisted-made
share under one finite opportunity budget. H1 learns a 64→32→18 tanh own-state
encoder. H2 learns an 36→32→18 directed teammate message. H3 learns both. H3F
has H3's parameter count but supplies a fixed sender to the message network.
There are no player IDs or known-pair coefficients.

| arm | learned parameters | interpretation |
|---|---:|---|
| H0 | 36 | 18 decoder intercepts and 18 positive slopes |
| H1 | 2,710 | H0 plus 2,674 encoder parameters |
| H2 | 1,814 | H0 plus 1,778 message parameters |
| H3 | 4,488 | decoder, encoder, and real-teammate message network |
| H3F | 4,488 | same capacity as H3, fixed sender reference |

Optimization is Adam at learning rate .001, weight decay .0001, gradient clip
5, and complete-game mini-batches targeting 4,096 grouped rows. Training states
and features are strictly dated. Model selection uses only the prior completed
quarter; the evaluated quarter never chooses a coefficient or epoch.

## Forward prediction

The common primary cohort is 5,607 lineup-quarter cells and 726,364 possessions
from 2016–2026. These are quarter-of-season forecasts, not full-season fits.

| model | MAE | RMSE | raw r² | bias |
|---|---:|---:|---:|---:|
| H0 | 8.1754 | 10.9445 | .10355 | -.4543 |
| H1 | 8.1586 | 10.9183 | .10784 | -.4294 |
| H2 | 8.1228 | 10.8768 | .11461 | -.0250 |
| H3 | 8.1229 | 10.8701 | .11570 | -.2739 |
| H3F | 8.1604 | 10.9230 | .10707 | -.3471 |
| corrected additive | **8.0920** | **10.8410** | **.12043** | -.5483 |
| location + shooting | 8.1312 | 10.8964 | .11142 | -.4619 |

H3 is the best structural arm by RMSE/r², but additive remains best overall.
Season-paired H3-H3F RMSE is -.05232 ± .02033 SEM, favorable in 9/11 seasons,
with t interval [-.09762, -.00701] and block-bootstrap interval
[-.09311, -.01901]. Its r² difference is +.00936 ± .00361, favorable 9/11,
with t interval [.00132, .01740]. MAE favors H3 by -.03749 ± .02301 but its
interval crosses zero. Against additive, no H3 point contrast is established:
MAE +.02658 and RMSE +.02756 with both intervals crossing zero.

On 2,073 novel-lineup cells / 226,256 possessions, H3 MAE/RMSE/r² is
8.9033/11.8169/.10582; additive is 8.9039/11.8530/.10035. The point estimates
slightly favor H3 on all three measures, but the advantage is small and not an
independent significance result. H2 has marginally higher novel r² (.10591).

Relative to v2, H3 improves pooled MAE by .02934, RMSE by .01724, and r² by
.00281. Novel H3 RMSE worsens by .01244 and r² by -.00188. This is a package
comparison across repairs and design amendments; it does not identify which
change caused the movement.

### Outer event evidence

H3 beats H3F's common baseline-scaled event loss in all 44 primary quarters,
mean difference -.001546 (range -.002894 to -.000230). Mean raw family-loss
differences H3-H3F are counts -.00050 (43/44 favorable), location -.00327
(44/44), conversion -.00012 (33/44), FT -.000014 (24/44), and assisted share
-.00257 (44/44). This points to real teammate information primarily improving
shot allocation/location and assisted-share modeling, not FT conversion.

Across the full primary outer events, H3's actual/predicted rates per 100 are:
FGA 88.581/88.225, FTA 22.504/22.744, turnovers 13.673/13.871, and 3PA
32.883/32.664. H3 has the best location cross-entropy (1.36044), FG Brier
(.170116), assisted conditional loss (.606269), and player FGA/point allocation
errors among the five arms. Full tables and calibration bins are in
`reports/outer_event_metrics.csv` and `reports/conversion_calibration_bins.csv`.

## Controls

### Fixed versus real teammate context

H3-H3F is favorable on point RMSE/r² and every primary outer event loss as
described above. H3F's near equality to H1 in pooled points—8.1604 versus
8.1586 MAE—also shows that merely adding the extra network is not sufficient.

### Context shuffle

Sender four-tuples were shuffled within training date and a training-defined
own-usage quartile, then the fitted model was evaluated with real outer context.
Only .45–.63% of assignments remained unchanged; singleton fractions were at
most .00023%. Shuffled-minus-real-H3 event loss was +.001151, +.001771,
+.002279, and +.001749 at 2016q1, 2019q1, 2023q1, and 2026q1. H3 is favorable
4/4, mean +.001738. Native mean shifts range from -.67 to +2.11 points/100,
so the event result is not one common intercept shift. Four origins are a
diagnostic, not an 11-season uncertainty sample or proof of causal chemistry.

### FT negative control

Real-minus-fixed sender outer FT NLL is +.000004, -.000070, +.000084, and
-.000217: mixed 2/4, mean -.000050. The same Brier differences are tiny. This
supports the explicit basketball restriction that teammate messages do not
directly alter FT conversion, while not proving that the FG context effects are
causal.

### Seed sensitivity

Across seeds 29/43 and four fixed origins, H3's event-loss change from seed 17
has mean -.000011, SD .000226, and maximum absolute value .000321. H3 native
mean changes have mean -.004, SD .640, maximum absolute 1.171 points/100.
Thus the predictive event result is stable at this scale, but the decomposed
point level is not deterministic enough to mistake one fit's mechanism ledger
for a uniquely identified causal allocation. H0 is much more stable in event
loss (maximum absolute change .000056).

## Basketball coherence and falsified expectations

All figures below are native offensive points/100 unless labeled calibrated.
They do not include defense or rebounding.

- Five limited centers: H1 119.51, H3F 118.99, H3 **101.40**. Real context
  supplies the missing creation/fit penalty without a player-specific rule.
- Five Goberts: H1 135.27, H3F 134.42, H3 **113.98**; calibrated H3 is 116.83.
  Five Jokićs move the other way: H1 126.35, H3F 126.13, H3 **132.37**.
- Five elite small guards: H1 117.75, H3F 117.36, H3 **127.44**. That may be a
  coherent offensive result, but the absent defense is decisive for a matchup.
- Haliburton versus McConnell with the same four teammates: H3 is 121.50 versus
  118.20. H1's gap is 2.56 and H3's is 3.30; real context adds about .75 to the
  Haliburton advantage. This is consistent with a force-multiplier hypothesis,
  not evidence about the injury season or team wins.
- The highest-exposure real pre-2026q4 lineup (1,277 possessions) scores 119.33
  under H3 versus 119.21 H3F and 119.06 additive. This deterministic fixture was
  accidentally omitted from the frozen fixture JSON and is disclosed as a
  post-freeze application of the pre-registered rule.

The Jokić/Korver/Westbrook expectation is not imposed on the model. Current
stale Korver scores 125.40 with the common Jokić/Murray/Gordon/Porter group;
Westbrook scores 123.95, a +1.45 Korver total advantage. Additive instead favors
Westbrook by 1.08. But H3's increment over H1 is +2.94 for Korver and +6.02 for
Westbrook: the learned teammate mechanism favors Westbrook relative to the
capacity control. The same conclusion holds against H3F. This contradicts our
original qualitative expectation about the *context increment*, and is retained
as evidence rather than tuned away.

The exact Korver-minus-Westbrook H3 decomposition is +1.509 opportunity,
-1.264 location, and +1.203 conversion = +1.448. Reverse ordering gives +1.922
conversion, -.520 location, and +.045 opportunity = +1.448, displaying the
interaction/order sensitivity. Transporting Korver's pre-2015-07-01 state into
the 2026 model raises the H3 difference to +3.056; that is a mixed-era modeling
assumption, not observed 2026 ability. All path residuals are exactly zero and
the player ledgers show changes to the four unchanged players.

Every synthetic fixture is labeled with support reasons. The clone, center,
guard, and both Korver cases lie above the historical composition q95 or are
thin/stale. Their point means are useful mechanism probes, not calibrated OOD
truth.

## High-exposure error review

The pre-specified filter retained lineup-quarters with at least 200 possessions
and five games. The top-ten tables versus additive, H3F, and H1 include names,
actual/predicted ratings, channel totals, exact additive base/carry/experience
coefficients, H1/H3/H3F player ledgers, and two chronological realized halves.

Three selection-conditioned patterns recur:

1. In the ten worst cases versus additive, H3's mean absolute error is 13.77
   versus 8.92 for additive; H3 underpredicts 6/10. Several exceptional real
   lineups are shrunk too hard, including 2023q1 Curry/Thompson/Green/Wiggins/
   Looney (actual 137.19, H3 114.64, additive 117.42) and 2017q4 Cleveland
   (122.95, 114.30, 119.00).
2. In the ten worst cases versus H3F, H3 moves by an average absolute 2.62
   points/100 and is above H3F in 5/10. Context can therefore overshoot in both
   directions; examples include 2020q4 Houston and Toronto, where a positive
   H3 context move worsens already-high predictions.
3. Across 20 unique selected failures, the H3 residual keeps the same sign in
   both chronological halves in 19/20 cases. Median absolute errors are 11.22
   and 14.57. These are not merely one-half spikes, though selection makes them
   diagnostic rather than independent evidence.

Opponent strength remains absent. These failures should not be attributed
entirely to offensive ability until the common prior-only opponent diagnostic
is run.

## Uncertainty

Rolling intervals use only complete prior forecast windows and the prescribed
higher empirical quantile. On the identical 5,607 H3 cells eligible for both
methods:

| nominal | exposure coverage / width | composition coverage / width |
|---|---:|---:|
| 50% | 51.76% / 17.41 | 49.63% / 17.14 |
| 80% | 80.22% / 33.13 | 79.67% / 32.38 |
| 95% | 95.27% / 52.08 | 95.06% / 50.53 |

The composition model is slightly narrower, but possession-weighted 80%
coverage drops from 84.04% to 78.96%; at 95% it drops from 96.41% to 94.88%.
At 80%, composition coverage ranges from 77.42% in prefix-defined distance Q1
to 79.91% in Q4, so distance does not cleanly order persistent error. No cell
crosses the fixed >2 role-stress threshold, which is reported as a zero-count
slice rather than silently omitted. Per protocol, no retrospective widening
factor is added.

These are intervals for a finite observed lineup-quarter outcome conditional
on its possessions. Coverage for a synthetic lineup's latent mean is not
validated. Honest arbitrary-lineup/OOD uncertainty—the third product pillar—
therefore remains incomplete.

## Operational record and verification

- Core: 240/240 arm-origins, 480 inner/final fits, 7,631 fit seconds and 7,644
  wall seconds. The original pipeline returned exit 1 only after core completion
  because duplicate support attachment produced `_x/_y` diagnostic columns.
  Diagnostics now select the correct saved `_y` values; no completed origin was
  rewritten. Early all-zero/NaN scoreboards were a warmup-display defect.
- Development: 68 fit invocations and 1,161 fit seconds.
- Controls: 96 fit invocations, 1,634 wall seconds. Two logged smoke fits make
  the prospective total **646**, below the 700-fit ceiling. Combined measured
  development/core/control wall time is about 2.89 hours, below eight hours.
- Peak RSS was not instrumented, so the <10 GiB target cannot be certified.
  Derived input files total roughly 202 MiB and no memory failure occurred.
- Final suite: **631 tests passed in 31.063 seconds**. Focused v3/control tests:
  6 passed. Artifact audit confirms 240 complete directories × seven required
  files, 5,607 common primary cells per arm, 139,143 interval forecasts, all
  4/12/32 shuffle/FT/seed rows, exact path reconciliation, and maximum float
  scoring discrepancy .000032 points/100.

Durable logs:

- `logs/pipeline_20260909_182422.log` — development/core pipeline
- `logs/diagnostics-controls_20260909_211330.log` — all bounded controls
- `logs/diagnostics_saved_final_20260909.log` — final saved-output replay
- `logs/full_test_suite_final_20260909.log` — repository suite
- `logs/final_artifact_audit_20260909.log` — immutable artifact/hash audit

Scientific hashes: plan
`eaaa5f3071b387f0233a94ad2d30c7f39517e76f7778799294fdc7b27ddad771`,
protocol `c6568e3d044e2c71b703be9f1bed58b75318d858b2cd20be1b53526819d19000`,
selection `5290e96f133e1409a2687670b571ef011459d5ba0013f98855fe0b233a28f5ed`.
All seven frozen source hashes match the manifest. Git HEAD at fitting was
`e68c53a7cdb63b26ced9c9f20583233338a05324`; the tree was already dirty and
remains uncommitted.

## One recommended next decision

Run the already-roadmapped, prior-only opponent-strength diagnostic on these
same saved forecasts and high-exposure failures before changing H3's mean
architecture. It is the smallest next step that advances both prediction and
the eventual two-lineup matchup product: it can tell us whether persistent
errors reflect offensive context, the defenses actually faced, or both.

Reverse this recommendation if the common opponent adjustment barely changes
H3-versus-additive/H3F contrasts and does not materially reduce the persistent
failure residuals. In that case, the next mean-model experiment should directly
target H3's level shrinkage/transport rather than add defensive conditioning.
Regardless, uncertainty needs a separately pre-registered latent-mean method;
the failed composition-distance interval should not be retrospectively tuned.
