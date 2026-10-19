# On-floor influence repair and bounded candidate audit

Date: 2026-09-09 protocol date / executed 2026-09-08 Pacific  
Run: `experiments/cache/influence_repair_2026_09_09_v2`  
Frozen point population: 5,607 lineup-quarter cells, 726,364 possessions;
2,073 novel cells, 226,256 possessions.

## Decision

The accounting repair is correct, but neither repaired mix nor the refreshed
shared factor earns inclusion in the current point candidate. The preferred
research candidate is **location-specific conversion + the existing shrunk
teammate shooting feature**. It has MAE **8.1312**, RMSE **10.8964**, and raw
r² **0.11142**, versus parent 8.1440 / 10.9214 / 0.10733 and corrected additive
8.0920 / 10.8410 / 0.12043. Its novel MAE is **8.8674**, ahead of additive's
8.9039 as a point estimate, but the season-paired comparison is not established.

This is research-only. Latent/OOD uncertainty for the assembled scorer remains
incomplete, so no promotion.

## What was repaired

1. Mix now partitions a player's own team's attempts into own, teammate-on,
   and true teammate-off groups. Own shots enter neither on nor off.
2. Mix shrinkage now uses `variance * (1/n_on + 1/n_off)`; the legacy
   `variance/n_on` version remains as a labeled ladder rung.
3. Mix receives its own strictly-prior point scale instead of turnover's scale.
4. The shared factor was refit from the corrected mix input and its stored
   sampling variance.
5. The old shooting estimate is relabeled accurately. A bounded two-way-FE FWL
   diagnostic is reported below; it is not silently substituted into the model.

The corrected mix channel itself still forecasts: rim slope 0.758 (12/12
seasons; 4.26 percentage-point spread), mid 0.870 (12/12), and paint 0.515
(10/12). Signal in a channel is not the same as incremental point value.

## Matched forward prediction

| arm | mae_all | mae_novel | rmse_all | rmse_novel | raw_r2_all | raw_r2_novel |
| --- | --- | --- | --- | --- | --- | --- |
| parent | 8.14398 | 8.89028 | 10.92143 | 11.84660 | 0.10733 | 0.10132 |
| shot_q | 8.13214 | 8.87451 | 10.90481 | 11.83481 | 0.11005 | 0.10311 |
| location_shot | 8.13123 | 8.86743 | 10.89640 | 11.82081 | 0.11142 | 0.10523 |
| l3_mix_shot | 8.14084 | 8.87195 | 10.89773 | 11.81856 | 0.11120 | 0.10557 |
| l3_location_shot_factor | 8.14072 | 8.87503 | 10.90608 | 11.84265 | 0.10984 | 0.10192 |
| l3_all_four | 8.14957 | 8.88045 | 10.91117 | 11.84479 | 0.10901 | 0.10160 |
| saved_additive | 8.09195 | 8.90390 | 10.84099 | 11.85302 | 0.12043 | 0.10035 |

Season-paired MAE deltas versus parent (negative is better):

| arm | mean | sem | ci95_low | ci95_high | seasons_better |
| --- | --- | --- | --- | --- | --- |
| shot_q | -0.01028 | 0.01579 | -0.04546 | 0.02490 | 5 |
| location_shot | -0.00975 | 0.02414 | -0.06353 | 0.04403 | 6 |
| l3_mix_shot | -0.00177 | 0.02446 | -0.05627 | 0.05273 | 6 |
| l3_location_shot_factor | -0.00238 | 0.03458 | -0.07944 | 0.07468 | 8 |
| l3_all_four | 0.00527 | 0.03427 | -0.07108 | 0.08163 | 7 |

Location+shooting versus parent is -0.00975 ± 0.02414 MAE (6/11 seasons), and
versus additive +0.03681 ± 0.03329 (4/11). Corrected mix+shooting is -0.00177
± 0.02446 versus parent. The corrected all-four arm is +0.00527 ± 0.03427.
None is an established mean-prediction win.

The refreshed factor improves turnover's held-out channel r² from 0.000471 to
0.000703 and moves its forward slope from 0.434 to 0.764, but the factor's point
increment does not improve the preferred candidate. It remains a useful
research result, not a scorer component.

## Basketball panel: actual 2026q4 scorer

Cutoff: **2026-03-02**. All rows use the same frozen state and league environment
(115.632 points/100). `research_all_four` is retained
for mechanism inspection; `candidate_location_shot` is the simpler candidate.

| lineup | structural_parent | candidate_location_shot | research_all_four | additive | assist_deficit | raw_factor_delta | raw_location_delta | raw_mix_delta | raw_shooting_delta | probability_violations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Jokic + Korver | 124.505 | 126.755 | 127.108 | 124.709 | 0.000 | 5.532 | -0.135 | 0.673 | 4.832 | 0 |
| Jokic + Westbrook | 120.069 | 122.714 | 124.567 | 125.792 | 0.000 | 6.290 | -0.326 | 0.666 | 5.513 | 0 |
| five centers | 106.057 | 106.943 | 107.612 | 111.161 | 10.194 | -3.783 | 1.562 | -1.463 | -0.580 | 0 |
| five guards | 122.247 | 124.817 | 126.963 | 134.064 | 0.000 | 8.207 | -0.118 | 0.630 | 5.347 | 0 |
| five Goberts (illegal copies) | 112.247 | 113.120 | 113.049 | 111.797 | 20.891 | -0.823 | 0.973 | -1.257 | -0.238 | 0 |
| five Jokics (illegal copies) | 124.026 | 127.491 | 128.371 | 134.663 | 0.000 | 6.007 | -0.009 | 1.727 | 6.700 | 0 |
| highest-exposure real 2026q4 lineup | 119.965 | 119.842 | 119.959 | 119.065 | 0.000 | 1.874 | -0.098 | -0.307 | 0.674 | 0 |

The Jokić/Korver lineup is +4.041 points/100 relative to the
Jokić/Westbrook lineup under the candidate; additive says -1.084.
Thus Korver's complementarity relative to additive is **+5.125**.
This satisfies the intended directional check without forcing Korver to be the
better player. Korver is explicitly a stale current-state fixture: last observed
2020-09-08, 2001 days before cutoff—not
“prime Korver.” The prime-Korver mixed-era transport was omitted because there
is no matched additive state and moving self-profile plus several influence
coefficient systems across origins would not be a validated sensitivity.

Westbrook retains distinct rim/creation allocation rather than being treated as
merely a bad shooter; the detailed attempt ledger is in
`basketball_panel_players.csv`. Five centers score 106.943 and carry a 10.194
assisted-demand deficit, exposing creation/spacing trouble. Five guards score
124.817 on offense, but defense/rebounding are **UNMEASURED**, so this is not a
claim that the lineup is good overall. Five-Gobert and five-Jokić rows are
illegal-copy stress tests. Every implied probability remained in [0,1].

Sequential explanation order is parent → factor turnover allocation → location
→ mix → shooting. These are path-dependent mechanism increments, not causal or
Shapley values. The final arm's calibration is then applied once. Exact
reconciliation, permutation invariance, nonnegative attempts, and the shared
usage budget are executable checks.

Support and uncertainty ledger:

| lineup | oldest_state_days | min_effective_usage | unsupported_mix_sides | interval_applies | missing_defense_matchup |
| --- | --- | --- | --- | --- | --- |
| Jokic + Korver | 2001 | 3439.7 | 0 | False | True |
| Jokic + Westbrook | 38 | 5565.1 | 0 | False | True |
| five Goberts (illegal copies) | 1 | 7976.3 | 0 | False | True |
| five Jokics (illegal copies) | 1 | 8423.0 | 0 | False | True |
| five centers | 2454 | 961.8 | 0 | False | True |
| five guards | 364 | 5513.2 | 0 | False | True |
| highest-exposure real 2026q4 lineup | 1 | 7129.5 | 0 | False | True |

The rolling cell intervals below do **not** apply to synthetic latent lineup
ability or illegal-copy cases. All cases also omit the opposing five and
defensive assignments.

### Historical Denver unit

The Westbrook / Jokić / Murray / Porter / Braun unit appears at 2025q2-q4:

| origin | possessions | actual | prediction_parent | prediction_location_shot | prediction_l3_all_four | saved_additive |
| --- | --- | --- | --- | --- | --- | --- |
| 2025q2 | 280.000 | 129.643 | 118.597 | 120.645 | 121.829 | 124.957 |
| 2025q3 | 264.000 | 125.758 | 118.952 | 121.090 | 122.432 | 124.961 |
| 2025q4 | 205.000 | 124.878 | 119.635 | 122.088 | 123.463 | 123.067 |

## Selected observed failures and improvements

These are deliberately selected >=200-possession cells, ranked by
possession-weighted squared-error disadvantage versus additive; they are not
independent validation evidence.

| selection | origin | lineup | possessions | actual | prediction_parent | prediction_location_shot | prediction_l3_mix_shot | prediction_l3_location_shot_factor | prediction_l3_all_four | saved_additive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| failure | 2017q4 | Kyrie Irving / LeBron James / J.R. Smith / Kevin Love / Tristan Thompson | 928.000 | 122.953 | 114.029 | 114.801 | 114.643 | 115.893 | 115.624 | 119.001 |
| failure | 2024q2 | Spencer Dinwiddie / Mikal Bridges / Cameron Johnson / Nic Claxton / Cam Thomas | 289.000 | 102.768 | 122.228 | 121.477 | 120.867 | 119.634 | 119.223 | 116.971 |
| failure | 2021q2 | Eric Bledsoe / Steven Adams / Brandon Ingram / Lonzo Ball / Zion Williamson | 603.000 | 126.866 | 111.573 | 111.128 | 111.236 | 111.528 | 111.677 | 113.964 |
| failure | 2024q3 | DeMar DeRozan / Nikola Vučević / Alex Caruso / Coby White / Ayo Dosunmu | 440.000 | 105.909 | 118.743 | 119.166 | 119.200 | 118.738 | 118.791 | 114.864 |
| failure | 2023q4 | DeMar DeRozan / Nikola Vučević / Patrick Beverley / Zach LaVine / Patrick Williams | 255.000 | 99.216 | 118.365 | 118.074 | 118.185 | 118.593 | 118.643 | 114.032 |
| improvement | 2018q1 | Carmelo Anthony / Russell Westbrook / Paul George / Steven Adams / Andre Roberson | 494.000 | 102.024 | 109.932 | 109.204 | 109.131 | 110.881 | 110.769 | 116.400 |
| improvement | 2024q2 | Kentavious Caldwell-Pope / Aaron Gordon / Nikola Jokić / Jamal Murray / Michael Porter Jr. | 682.000 | 131.525 | 121.407 | 124.025 | 124.091 | 124.441 | 124.353 | 119.861 |
| improvement | 2020q4 | P.J. Tucker / Russell Westbrook / Eric Gordon / James Harden / Robert Covington | 272.000 | 97.059 | 114.434 | 115.136 | 115.198 | 116.507 | 116.448 | 118.564 |
| improvement | 2020q2 | Rudy Gobert / Bojan Bogdanović / Joe Ingles / Donovan Mitchell / Royce O'Neale | 634.000 | 123.659 | 114.581 | 114.092 | 113.921 | 113.627 | 113.498 | 111.504 |
| improvement | 2017q2 | Thaddeus Young / Jeff Teague / Paul George / Glenn Robinson III / Myles Turner | 588.000 | 115.986 | 109.386 | 109.420 | 109.591 | 109.810 | 109.923 | 106.083 |

Per-player centered additive base/carry/experience terms are preserved in
`failure_additive_players.csv`; their calibrated contributions reconcile to the
corrected additive score. Mechanism terms are in `failure_cases.csv`. Observed
channel counts were omitted because joining them would require a new possession
output pipeline, which this bounded repair forbids.

The failures suggest deployment/form effects the static profiles still miss:
the 2024 Brooklyn and Chicago groups are badly overpredicted, while high-function
Denver and New Orleans units are underpredicted. This is a diagnostic prompt,
not evidence for named-lineup corrections.

## Rebounding attribution—not integrated

| player | channel | own_rate_per100 | full_team_onoff_per100 | own_rate_orthogonal_per100 | exposure |
| --- | --- | --- | --- | --- | --- |
| Steven Adams | offensive_rebound | 13.599 | -1.298 | -0.438 | 21847.000 |
| Steven Adams | defensive_rebound | 16.546 | 0.847 | 2.082 | 22034.000 |
| Mitchell Robinson | offensive_rebound | 15.572 | -0.519 | 0.506 | 9694.000 |
| Mitchell Robinson | defensive_rebound | 17.462 | 0.916 | 2.444 | 9476.000 |
| Josh Hart | offensive_rebound | 4.440 | 0.175 | 0.266 | 18399.000 |
| Josh Hart | defensive_rebound | 18.612 | -3.943 | -2.049 | 18438.000 |

Robinson and Hart look sensible on offensive boards after orthogonalization;
Adams remains wrong-signed at -0.438 despite his 13.599 own ORB/100. Josh Hart's
defensive-rebound residual is also implausibly negative. These rows reinforce
the decision not to add a rebound loop before modeling competition for one
available rebound.

## Bounded shooting FWL diagnostic

Values below are percentage points. The FWL estimate residualizes both outcome
and presence by shooter and game on the same teammate-only sample. Cluster SEs
are conditional on the fitted nuisance curve, not a bootstrap of every stage.

| player | kind | attempts | on_attempts | off_attempts | games | original_saved_raw | teammate_residual_contrast | beta | cluster_se | converged |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nikola Jokic | field_goal | 62921 | 38373 | 24548 | 883 | 1.669 | 2.798 | 2.188 | 0.460 | True |
| Nikola Jokic | free_throw | 14543 | 8066 | 6477 | 883 | -0.149 | 2.834 | -1.388 | 0.844 | True |
| Stephen Curry | field_goal | 83226 | 54482 | 28744 | 1223 | 1.845 | 2.276 | 3.207 | 0.397 | True |
| Stephen Curry | free_throw | 20422 | 12912 | 7510 | 1223 | 0.747 | -0.840 | 0.862 | 0.759 | True |
| Jamal Murray | field_goal | 48008 | 29043 | 18965 | 671 | 2.067 | 3.725 | 2.779 | 0.474 | True |
| Jamal Murray | free_throw | 12450 | 7398 | 5052 | 671 | 0.541 | 1.065 | 0.224 | 0.894 | True |
| Russell Westbrook | field_goal | 96696 | 59990 | 36706 | 1430 | 0.440 | 1.561 | — | — | False |
| Russell Westbrook | free_throw | 26622 | 16535 | 10087 | 1430 | 0.531 | -0.483 | — | — | False |
| Draymond Green | field_goal | 86433 | 50091 | 36342 | 1102 | 1.590 | 2.449 | 1.950 | 0.376 | True |
| Draymond Green | free_throw | 20394 | 11729 | 8665 | 1102 | 0.830 | 3.284 | 1.373 | 0.682 | True |
| Rudy Gobert | field_goal | 73901 | 44524 | 29377 | 972 | -0.102 | 0.045 | -0.477 | 0.419 | True |
| Rudy Gobert | free_throw | 17321 | 9428 | 7893 | 972 | 0.141 | 3.239 | 0.438 | 0.722 | True |

Curry (+3.207 ± 0.397 pp), Murray (+2.779 ± 0.474), Jokić (+2.189 ± 0.460), and
Draymond (+1.950 ± 0.376) retain positive FG estimates. Gobert is compatible
with zero. Free throws are noisy and Jokić's -1.388 ± 0.844 warning shows that
lineup/deployment confounding remains. Westbrook did not satisfy the fixed
1e-10 convergence requirement after 1,000 sweeps (FG max group mean 2.51e-7;
FT 1.82e-7), so no coefficient is returned. FWL controls shooter and game, not
score/clock state, defensive personnel, or correlated co-playing teammates;
it is not randomized assignment.

Decision: preserve the current shooting feature under its correct descriptive
name for this candidate; do not replace it from a six-player diagnostic.

## Rolling finite-batch interval audit

These are symmetric empirical future-cell intervals based only on completed
earlier origins, with fixed possession bins and conservative `higher` quantiles.
They are not formal conformal guarantees.

| arm | nominal | n_cells | coverage | weighted_coverage | mean_width | fallback_rate |
| --- | --- | --- | --- | --- | --- | --- |
| parent | 0.8000 | 5607 | 0.8022 | 0.8386 | 33.1407 | 0.0753 |
| parent | 0.9500 | 5607 | 0.9511 | 0.9632 | 51.9199 | 0.0753 |
| saved_additive | 0.8000 | 5607 | 0.8026 | 0.8409 | 32.8226 | 0.0753 |
| saved_additive | 0.9500 | 5607 | 0.9499 | 0.9627 | 51.1910 | 0.0753 |
| location_shot | 0.8000 | 5607 | 0.8013 | 0.8382 | 33.0459 | 0.0753 |
| location_shot | 0.9500 | 5607 | 0.9497 | 0.9599 | 52.0671 | 0.0753 |
| l3_mix_shot | 0.8000 | 5607 | 0.8013 | 0.8387 | 33.0404 | 0.0753 |
| l3_mix_shot | 0.9500 | 5607 | 0.9501 | 0.9616 | 52.0555 | 0.0753 |
| l3_location_shot_factor | 0.8000 | 5607 | 0.8024 | 0.8412 | 33.1488 | 0.0753 |
| l3_location_shot_factor | 0.9500 | 5607 | 0.9499 | 0.9614 | 52.2182 | 0.0753 |
| l3_all_four | 0.8000 | 5607 | 0.8040 | 0.8443 | 33.1853 | 0.0753 |
| l3_all_four | 0.9500 | 5607 | 0.9502 | 0.9618 | 52.2814 | 0.0753 |

All 5,607 primary cells are common-eligible. At nominal 80%, candidate coverage
is 0.8013 with mean width 33.046; at 95%, 0.9497 with width 52.067. Bin fallback
is 7.53% overall and much higher in the sparse 400+ bin. This quantifies finite
batch outcome noise only. Parameter, latent-quality, and arbitrary-lineup OOD
uncertainty remain unfinished.

## Artifacts and commands actually exercised

- Core and all derived CSV/pickle outputs: `experiments/cache/influence_repair_2026_09_09_v2`
- Detailed player attempts/support: `basketball_panel_players.csv`
- Corrected-additive failure ledgers: `failure_additive_players.csv`
- Report: `reports/influence_repair_2026_09_09.md`
- Current model scorecard: `MODEL_SCORECARD.md`

Commands:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage preflight --run-dir experiments/cache/influence_repair_2026_09_09_v2
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage core --run-dir experiments/cache/influence_repair_2026_09_09_v2
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage intervals --run-dir experiments/cache/influence_repair_2026_09_09_v2 --resume
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage fwl --run-dir experiments/cache/influence_repair_2026_09_09_v2 --resume
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage panel --run-dir experiments/cache/influence_repair_2026_09_09_v2 --resume
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.influence_repair --stage report --run-dir experiments/cache/influence_repair_2026_09_09_v2 --resume
```

No scraper, database mutation, input-cache rebuild, scorer promotion, page
change, deployment, or known-pair chemistry was used.

## Next one research question

Does a pre-registered all-player teammate-shooting estimator with shooter, game,
opponent/lineup and deployment controls retain genuinely forward signal **and**
improve the location+shooting point candidate against its matched current
feature? That question follows directly from the positive FWL examples, the
free-throw warnings, and Westbrook's convergence failure.
