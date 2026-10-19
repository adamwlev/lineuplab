# Creation / finishing transport — 2026-09-05

## Question and protocol, recorded before the first run

Does a change in the other four players' passing supply predict how the **same
player** changes his shot mix, turnover share, assisted-made share, and shooting,
beyond the already measured response to composition-assigned workload?

This is not a repeat of the failed `load × prior assisted share` interaction.
The new predictor is leave-self-out teammate passing supply. It is not a hard
assist cap and does not add a player/pair identity bonus.

At each season T (2015–2026):

1. Select each player's latest observed state with >=400 possessions, at or
   before T−1, using the existing season-state builder. Fix the team usage pool
   using only seasons <T. Retain alpha 1, the validated literal allocator.
2. For each offensive five, project the four teammates' assist rates under
   that usage ledger: `100 × (sum(rast) − own_rast) × U / sum(usage)`.
   Record common log workload `log(U / sum(usage))` separately. The passing
   quantity is an availability proxy, not a simultaneous assist promise.
3. Center both predictors on the player's own profile-season on-floor context,
   evaluated with the same strictly pre-T profiles and usage pool. This avoids
   treating a profile earned next to a creator as context-free. Historical
   context may use information later than that historical game, but never
   from T: this is a forecast made at the end of T−1, not an in-game forecast.
4. Average composition features to player-game using possession exposures,
   without using that game's outcomes as predictors. Require >=90% profiled
   exposure in both reference state and target player-game, and >=10 offensive
   possessions in the latter. These are diagnostic sample restrictions, not a
   product coverage gate. Report excluded exposure.
5. Fit descriptive within-season player-fixed-effect regressions jointly on
   workload and passing; repeat with player + team-game effects. The latter
   removes common game conditions but changes the identifying variation; it
   cannot isolate a lineup-wide creator effect shared by all five players.
   Neither regression is a causal instrument or identification of passing
   gravity: teammate selection, defensive assignments, and coaching remain.
6. Forward-test three **nested** prediction arms: calibrated prior profile;
   profile + workload change; profile + workload + passing change. Fit weighted
   linear probability models on completed earlier origins only, without a
   penalty/sign sweep. Keep raw profiles as a fourth reference. Clip scalar
   probabilities to [0,1]; project shot-mix predictions to the probability
   simplex. These probability constraints are accounting, not five-center
   point penalties. Record how often they activate.

## Targets and decisions

Primary tests: assisted share **of made FGs** and the six-bucket distribution
of classified FGA, scored by exposure-weighted cross-entropy and Brier score.
Secondary: TO / (FGA + .44 FTA + TO), 2P%, and 3P%. FT% is a negative-control
outcome, not a basketball mechanism to transport. Report paired season deltas
for passing versus workload-only, not just a pooled winner. Expected sign:
more passing support should raise assisted-made share; possible changes to
rim attempts and efficiency must be measured, not imposed. No mandatory
location-coefficient signs or named-player ordering.

Assists are tagged only on makes. `self_2p` and `self_3p` are overall shooting
percentages, **not** self-created efficiency. The dataset cannot identify the
creation mode or pass quality of a missed shot. Location buckets are coarse
play-by-play classifications (including a distance-based corner-three proxy),
not tracking coordinates. A change in assisted-made share is not by itself
evidence of more assisted attempts, better shot quality, or causality.

Passing must add forward signal beyond workload, with consistent diagnostic
direction and no comparable FT% placebo pattern, before it is a candidate for
point transport. A partial/negative result stays a partial/negative result.
Even a successful intermediate result does not automatically replace the
accepted scorer, validate five-center extrapolation, or supply calibrated OOD
intervals. No named-panel tuning this round. Preserve all rebound controls.

## Matched additive benchmark requirements

Inspection confirms that `forward_eval.py` globally removes season/week means
and home advantage; `lineup_scoreboard.py` also changes the realized target by
subtracting each arm's estimated opponent effect. The structural experiment
instead uses raw ordinary points on season-specific offensive lineup cells.
Their published correlations are not an apples-to-apples comparison.

A proper benchmark must refit the incumbent on each pre-T prefix, select any
penalties on earlier seasons, use exactly the structural rig's held-out cells
and shared target, and use the same prior-origin calibration and split-game
uncertainty machinery. No all-data exported ratings or held-out-season
detrending. Report an identity-free additive control separately from any
known-pair residual. Raw-point and common opponent-adjusted targets, if both
used, must each be identical across arms. This work is still owed; the present
experiment is an intermediate mechanism test, not that benchmark.

## First result and probability-link follow-up, before the second run

The linear experiment completed all origins. Passing improves assisted-made
share Brier score in 11/11 future seasons and cross-entropy in 9/11. Turnover
cross-entropy improves 10/11, but the effect is small. Shooting gains are not
established and FT% stays null. Shot-mix cross-entropy **worsens 11/11**,
paired +0.002052 ± 0.000387, despite a near-zero Brier change.

Inspection identifies a concrete probability-model defect, not merely an
unfavorable ranking: simplex projection activates on 4.47% of shot exposures
under workload-only and 5.57% with passing. Exactly zero predicted categories
contain 0.01755% and 0.02660% of realized shots, respectively. Their log-loss
contributions are 0.004849 and 0.007350; the difference (+0.002501) exceeds the
overall +0.002049 weighted loss. The 1e-12 log arithmetic floor therefore
materially influences this comparison. Preserve this failed arm.

**One focused follow-up:** replace only the shot-mix linear probability model
with an unpenalized multinomial softmax likelihood. Features remain the same
information: prior shot mix (five log-ratios against the sixth category), then
workload delta, then passing delta. Each player-game supplies counts in all
six mutually exclusive shot categories. All fitting, feature standardization,
and optimization initialization use completed earlier origins only. No sign,
penalty, or output-floor sweep. Use a reference category for identifiability.
Keep the scalar outcome models unchanged and check numerical reproduction of
their results. The raw profile and two simpler fitted controls remain in the
comparison. These are reused research seasons, not a new untouched confirmatory
test set. This repair earns no favorable conclusion unless its forward results
do; it does not authorize a scoring change or synthetic confidence claims.

## Completed results

Both runs completed. 2015 supplies the first response-fitting origin; genuine
next-season evaluations span 2016–2026, **97,640 player-games**. Their retained
player-possession exposure is **36.67%** overall, 31.67–44.20% by season
(2026: 32.15%). Even before the reference/game restrictions, requiring all five
preseason profiles covers only 53.62–64.44% in those evaluation seasons.
These are selected well-observed contexts, not results for every NBA player.
`*_coverage.csv` records the denominator and configuration at every origin.

### Prediction: passing beyond workload

Season-paired cross-entropy differences below compare `workload_passing` with
`workload`. Negative means better; uncertainties are SEM across 11 seasons,
not player-game independence claims. Use the softmax shot-mix result.

| Target | Mean change ± season SEM | Seasons improved | Decision |
|---|---:|---:|---|
| Assisted share of made FGs | −0.001145 ± 0.000317 | 9/11 | Supported intermediate signal |
| Turnover share | −0.0000956 ± 0.0000344 | 10/11 | Small supported signal |
| Shot mix, softmax | −0.000141 ± 0.000158 | 7/11 | Incremental passing gain inconclusive |
| 2P% | −0.0000536 ± 0.0000355 | 7/11 | Not established |
| 3P% | +0.0000021 ± 0.0000080 | 6/11 | Null |
| FT% placebo | +0.0000214 ± 0.0000282 | 4/11 | Null |

Assisted-share Brier improves **11/11**, paired −0.000740 ± 0.000062.
Its exposure-weighted fraction MAE moves 0.174424 → 0.172819. Turnover MAE
moves only 0.073426 → 0.073298; do not oversell a small improvement. Turnover
Brier's paired change is −0.0000156 ± 0.0000119 despite 10/11 positive seasons.
Scalar-target results reproduce **exactly** between the two runs.

### Shot mix: workload matters; extra passing remains tentative

The softmax repair removes the exact-zero boundary problem (no projection
activates) and yields these exposure-weighted shot-distribution cross-entropies:

| Arm | Cross-entropy | Event-level Brier |
|---|---:|---:|
| Raw prior profile | 1.375838 | 0.684747 |
| Calibrated profile | 1.373363 | 0.684102 |
| Profile + workload | 1.372742 | 0.683814 |
| Profile + workload + passing | 1.372612 | 0.683795 |

Workload versus calibrated profile improves cross-entropy **10/11**, paired
−0.000634 ± 0.000161. The full arm versus calibrated profile improves 10/11,
−0.000775 ± 0.000249, but most evidence is for workload; the incremental
passing contrast is not established. No optimizer failures or fitted penalty
search. The failed linear results are preserved, not replaced on disk.

### Basketball interpretation and limits

At a fixed modeled workload, within-player associations with +5 projected
teammate assists/100 are approximately +4.81 percentage points assisted-made
share and −1.17 points turnover share. The signs survive player + team-game
effects. Shot-location associations shift away from non-rim twos toward
threes, with a weaker positive rim association. These are descriptive slopes,
not validated causal swap effects or mandatory coefficients for the scorer.

The 3P% association becomes strong after team-game controls yet does **not**
transport predictively. This is a useful warning against promoting regression
significance into a shooting or “gravity” bonus. Assisted-made share can change
without adding any points. Passing signal alone cannot price a finisher's
self-created attempts, and the play-by-play still does not identify those
attempts on misses.

**Decision:** retain the softmax workload-to-shot-mix model and measured
passing-to-assisted-share/turnover channels as candidates for a controlled
integration test. Do not promote passing-driven shooting efficiency or the
extra shot-mix response. Do not add an assisted-share scoring bonus, which
would confuse the mode of an existing make with an additional make and could
double-count the current assist-deficit term. Point gains, finite usage/miss/
rebound accounting, and OOD calibration all still need their own tests.

Next: (1) run the matched pre-origin additive/structural benchmark described
above; (2) transport only the supported intermediate changes into a separately
labeled arm, preserving the accepted scorer and rebound-capture control;
(3) broaden thin-state coverage and real small-ball checks. The benchmark
helps determine whether our remaining effort belongs in base player-value
estimation or contextual mechanisms. No scorer/HTML or database mutation in
this experiment. No jobs remain running. The suite passes **119 tests**.

**Subsequent checkpoint:** the matched benchmark is now complete; read
`MATCHED_BENCHMARK.md`. Additive and structural average errors are nearly tied,
but the additive core has stronger lineup-quality correlation. Simply adding
the existing deficit to that core does not help. Preserve both controls for
the supported-channel integration test. The current full suite has 128 tests.

## Reproduce

From the repository root, using the basketball25 interpreter:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.creation_transport_validation
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.creation_transport_validation \
  --shot-link softmax --prefix experiments/cache/creation_transport_softmax_2026
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest discover -s tests
```

Result prefixes are `experiments/cache/creation_transport_2026_*` and
`experiments/cache/creation_transport_softmax_2026_*`. Each contains validation,
descriptive fixed-effect slopes, fitted forward coefficients, coverage/source
epoch, and compressed player-game inputs. The latter are repeated across the
two probability-link runs for self-contained reproducibility, not independent
evidence. Logs: `/tmp/basketball-creation-transport.log` and
`/tmp/basketball-creation-transport-softmax.log`.
