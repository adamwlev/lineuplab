# Joint capability v4 pooling-factorial review

2026-09-10. This is the final review of the frozen Day3 experiment specified in
`SOL_JOINT_CAPABILITY_DAY3_PLAN.md`. The fitted source is
`experiments/cache/joint_capability_2026_09_10_v4e/`; the completed,
memory-bounded derived report is
`experiments/cache/joint_capability_2026_09_10_v4e_report_r3/`. Earlier v4,
v4b, v4c, v4d and report-r1/r2 prefixes are preserved as failed or superseded
attempts. No scorer or page was promoted.

## Bottom line

Mean-teammate pooling is the important result. Relative to fixed context it
improves point prediction, event prediction, novel-lineup prediction and the
extreme-lineup basketball checks. Preserving each sender through a separate
nonlinear message adds very little beyond the teammate mean: it provides a
small all-lineup gain with the encoder on at lambda .01, but no dependable novel
gain and essentially no gain at lambda .0001. The learned player-state encoder
also does not establish a useful incremental benefit at matched pooling and
regularization.

The pragmatic structural research default should therefore be **E0M_L2**:
anchored dated player states, no learned own-state encoder, and a nonlinear
receiver response to the mean of the other four players' states. E1P_L2 remains
the strongest neural point arm and a useful reference. This is a research
choice, not a scorer promotion and not proof that individual sender information
or learned state correction can never help.

Corrected additive remains narrowly best on the full observed-lineup sample.
E1P_L2 trails it by only .01768 MAE and .01815 RMSE points/100, while E0M_L2
trails by .03044 MAE and .03869 RMSE. On novel lineups E0M_L2 has the best MAE,
and E1M_L2 has the best RMSE and raw r². The repeatedly inspected 2016–26
benchmark is not a newly untouched holdout, so these differences are research
evidence rather than a final generalization claim.

The third product standard remains unfinished. Rolling future-outcome
intervals are well calibrated on observed lineup-quarter means, but composition
distance does not improve the matched constant-sqrt(n) interval. None of these
intervals validates uncertainty for a synthetic lineup's latent mean.

## 1. Experiment accounting

All nine planned arms have all 48 origins. Six arms were newly fit and three
were exact frozen-v3 aliases:

| v4 arm | pooling / encoder / lambda | source | origins |
|---|---|---|---:|
| E0F_L2 | fixed / off / .01 | new v4e fit | 48 |
| E0M_L2 | mean / off / .01 | new v4e fit | 48 |
| E0P_L2 | pair / off / .01 | frozen v3 H2 alias | 48 |
| E1F_L2 | fixed / on / .01 | frozen v3 H3F alias | 48 |
| E1M_L2 | mean / on / .01 | new v4e fit | 48 |
| E1P_L2 | pair / on / .01 | new v4e fit | 48 |
| E1F_L4 | fixed / on / .0001 | new v4e fit | 48 |
| E1M_L4 | mean / on / .0001 | new v4e fit | 48 |
| E1P_L4 | pair / on / .0001 | frozen v3 H3 alias | 48 |

The final prefix recorded 580/620 optimizer starts: four numerical bridge fits
and 576 core inner/final fits. Twenty starts in preserved superseded prefixes
bring the Day3 total to **600/640**, within the predeclared allowance. Every
start in v4e has a matching completion. Recorded optimizer time is 10,423.68
seconds, or 2.895 hours. The successful final derived report took 4 minutes 59
seconds and performed no fits.

Selected inner epochs show that early stopping, rather than the 24-epoch cap,
usually controlled training:

| arm | selected epoch min / median / mean / max | cap hits |
|---|---:|---:|
| E0F_L2 | 2 / 7 / 7.58 / 13 | 0 |
| E0M_L2 | 5 / 13 / 12.83 / 24 | 2 |
| E0P_L2 (v3 H2) | 5 / 12.5 / 12.96 / 24 | 3 |
| E1F_L2 (v3 H3F) | 1 / 6 / 5.35 / 13 | 0 |
| E1M_L2 | 1 / 10 / 10.50 / 22 | 0 |
| E1P_L2 | 1 / 11 / 10.90 / 22 | 0 |
| E1F_L4 | 1 / 6 / 5.50 / 16 | 0 |
| E1M_L4 | 1 / 9.5 / 9.38 / 17 | 0 |
| E1P_L4 (v3 H3) | 1 / 10 / 10.50 / 24 | 1 |

Alias function parity is exactly zero on the bridge audit. The two fresh bridge
fits selected epochs 24 and 4; maximum saved-score reconstruction discrepancy
was 3.81e-6 points/100 and family-statistic differences were zero.

## 2. Forward point prediction

The primary population has 5,607 lineup-quarter cells and 726,364 possessions;
the novel subset has 2,073 cells and 226,256 possessions.

| arm | all MAE | all RMSE | all raw r² | novel MAE | novel RMSE | novel raw r² |
|---|---:|---:|---:|---:|---:|---:|
| corrected additive | **8.09195** | **10.84099** | **.12043** | 8.90390 | 11.85302 | .10035 |
| E0F_L2 | 8.17135 | 10.93984 | .10432 | 8.94767 | 11.91947 | .09024 |
| E0M_L2 | 8.12239 | 10.87968 | .11414 | **8.85744** | 11.79906 | .10852 |
| E0P_L2 | 8.12280 | 10.87679 | .11461 | 8.88166 | 11.81636 | .10591 |
| E1F_L2 | 8.16042 | 10.92302 | .10707 | 8.92435 | 11.88369 | .09569 |
| E1M_L2 | 8.12341 | 10.86597 | .11637 | 8.87274 | **11.77732** | **.11181** |
| E1P_L2 | **8.10963** | **10.85914** | **.11749** | 8.87239 | 11.78079 | .11128 |
| E1F_L4 | 8.15975 | 10.92342 | .10701 | 8.92854 | 11.88657 | .09525 |
| E1M_L4 | 8.13013 | 10.87414 | .11505 | 8.89975 | 11.80906 | .10701 |
| E1P_L4 | 8.12290 | 10.87013 | .11570 | 8.90332 | 11.81692 | .10582 |

Lower is better for MAE/RMSE. Bold neural entries identify the best neural arm,
not a promoted winner.

The pre-registered paired-season contrasts make the architectural result clear:

- Mean versus fixed improves all-lineup RMSE by -.05950 for E0, 95% t interval
  [-.12247, .00346], and -.05622 for E1, interval [-.10725, -.00518]. On novel
  lineups the improvements are larger: -.12239, interval [-.18206, -.06272],
  for E0 and -.10948, interval [-.19707, -.02190], for E1.
- Pair versus mean at E0 changes all-lineup MAE by +.00041 and novel MAE by
  +.02364; neither favors pair. With E1 at lambda .01, pair improves all-lineup
  MAE by -.01269, interval [-.02277, -.00262], but novel MAE is +.00051 and
  novel RMSE is +.00397. This is a small in-distribution gain, not a broad
  reason to retain individual sender resolution.
- At lambda .0001, pair versus mean is again negligible: all MAE -.00734 and
  novel MAE +.00364. E1P_L4 is worse than E1P_L2 on novel RMSE by +.03578,
  interval [.00429, .06727]. The weaker network penalty does not help this
  architecture on novel lineups.
- Encoder-on versus encoder-off comparisons at matched mean/pair pooling have
  wide season intervals and no stable practical advantage. The point estimates
  trade MAE against RMSE and remain inside the .05 points/100 practical margin.

## 3. Event prediction and mechanism transfer

Mean pooling improves every reported event loss versus fixed context on the
2,760,546-possession full eligible cohort. For E1 at lambda .01, mean-minus-fixed
deltas are: FGA count NLL/100 -.02624, FTA -.09019, turnover -.02975, location
cross-entropy -.003098, FG Brier -.000077 and assisted loss -.002380. E0 gives
the same direction in every channel. Pair-minus-mean changes are roughly one to
two orders of magnitude smaller and mixed in sign. This supports a real shared
context response while providing little evidence that sender identity must be
preserved after the teammate aggregate.

The point-transfer ledger reconciles every comparison to below 3e-14 points/100
and creates zero opportunity budget. Mean versus fixed changes lineup-level
opportunity, location and conversion contributions with standard deviations of
roughly .7–1.1 points/100, while their pooled means are near zero. Pair versus
mean has much smaller dispersion, roughly .1–.3. The mechanism is therefore
heterogeneous reallocation, not a generic level bonus. These are exact model
decompositions, not causal identification of how a real player makes a teammate
better.

## 4. Basketball checks

The numbers below are calibrated offensive points/100. They contain no opponent
defense and no explicit rebound loop. Synthetic-lineup means do not have
validated uncertainty.

| fixture | additive | E0 fixed | E0 mean | E0 pair | E1 fixed | E1 mean | E1 pair |
|---|---:|---:|---:|---:|---:|---:|---:|
| five limited centers | 111.16 | 121.68 | 111.41 | 110.99 | 120.19 | 110.93 | 110.21 |
| five Goberts | 111.80 | 131.13 | 118.84 | 118.09 | 129.77 | 118.61 | 117.63 |
| five Jokics | 134.66 | 126.05 | 128.57 | 129.19 | 124.62 | 127.78 | 128.03 |
| five small guards | 134.06 | 119.67 | 127.00 | 127.16 | 119.18 | 125.20 | 125.32 |
| Warriors 2016q4 | 117.51 | 114.04 | 116.95 | 116.03 | 114.25 | 116.73 | 116.53 |
| Clippers 2021q4 | 121.42 | 118.25 | 120.43 | 120.83 | 117.84 | 119.77 | 119.81 |

Mean pooling supplies almost all of the desired nonlinear response. It removes
10–12 points/100 from the fixed-context center clones and raises five Jokics by
2.5–3.2. Pair messages usually add less than one further point. Five small
guards move upward under mean pooling; that is not inherently an offensive
failure, but the absent defense model means the fixture cannot test the most
obvious small-lineup cost.

The Haliburton same-four lineup exceeds the McConnell same-four lineup by 2.57
points under E0M and 2.28 under E1M, versus 1.94 additively. That is encouraging
for a force-multiplier interpretation, but it is one synthetic swap and not a
causal estimate.

For the named Jokic swaps, E1M rates current-state Korver .765 above Westbrook,
where additive rates Korver 1.084 below Westbrook. Pair-minus-mean is +.080 for
Korver and +.020 for Westbrook, so the incremental pair response favors Korver
by .060. E0 shows the same qualitative ordering. Korver is 2,001 days stale at
this scoring date, however, and no synthetic interval is valid; the signs are a
mechanism check, not proof of the original hypothesis.

## 5. Uncertainty and support

The final reporter independently reproduces 34,557 historical v3 radii with a
maximum absolute difference of 7.11e-15. At nominal 80% on the common 5,607
cells:

| arm | method | cell coverage | possession-weighted coverage | mean width | weighted interval score |
|---|---|---:|---:|---:|---:|
| additive | constant sqrt(n) | .7985 | .7925 | 32.39 | 36.031 |
| E0M_L2 | constant sqrt(n) | .7960 | .7897 | 32.38 | 36.006 |
| E1M_L2 | constant sqrt(n) | .7956 | .7887 | 32.23 | 36.005 |
| E1P_L2 | constant sqrt(n) | .7947 | .7886 | 32.27 | **35.937** |
| additive | composition isotonic | .7960 | .7890 | 32.43 | 36.120 |
| E0M_L2 | composition isotonic | .7974 | .7909 | 32.52 | 36.073 |
| E1M_L2 | composition isotonic | .7951 | .7872 | 32.40 | 36.026 |
| E1P_L2 | composition isotonic | .7963 | .7892 | 32.44 | 35.967 |

The neural and additive intervals are similarly calibrated on future observed
lineup means. The composition-isotonic method is slightly worse than its
identical-split constant control on weighted interval score for every listed
arm and does not isolate useful distance information. Exposure-only intervals
are materially over-covering under possession weights and score worse.

Most importantly, the support fields are inherited from the fixed v3 baseline,
and `interval_validated_for_latent_synthetic_mean` is false for every basketball
fixture. These intervals describe noisy finite future samples around observed
lineups. They do not yet answer how uncertain the model should be about the
underlying quality of five Goberts, stale Korver, or an arbitrary user-built
lineup. Honest OOD uncertainty therefore remains an equal, unresolved pillar.

## 6. Failure review

The largest structural-versus-additive losses are dominated by lineups whose
realized quarter offense is extreme: the 2023q1 Curry/Thompson/Green/Wiggins/
Looney lineup scored 137.19 while both model families forecast roughly 114–117;
several Bulls/Nets/Celtics lineups realized 91–103 against forecasts near
114–121. These cases mix hot/cold shooting, opponent strength, changing player
state and genuine lineup fit.

The first-half-selected/second-half audit does not reveal a stable pair-message
failure. Pair versus mean remains worse in 5/10 selected cases for each of E0,
E1 and the low-lambda E1 comparison, with near-zero or favorable aggregate
second-half disadvantage for the E1 pair arms. Structural-versus-additive
failures persist only inconsistently. This weak persistence argues against
adding player-specific exceptions and points instead toward missing dated
opponent context and better latent-state/uncertainty treatment.

## 7. Verification, defects and decision

The final report status is complete. The historical radius replay passes,
point-transfer ledgers reconcile, alias parity is exact, and the repository
suite passes 640 tests. Durable paths:

- training logs: `experiments/cache/joint_capability_2026_09_10_v4e/logs/`
- final report log: `experiments/cache/joint_capability_2026_09_10_v4e_report_r3/logs/report_20260910_181028.log`
- score tables: `experiments/cache/joint_capability_2026_09_10_v4e_report_r3/reports/`
- mechanism, fixture, uncertainty and failure outputs:
  `experiments/cache/joint_capability_2026_09_10_v4e_report_r3/diagnostics/`

The original pipeline's model work completed, but its old all-in-memory point
transfer report was killed by the OS. The replacement streams each comparison
and writes a fresh derived prefix. Report r2 then exposed an all-NaN placeholder
support-column precedence bug; r3 selects the fully populated, mutually checked
fixed-v3 support copy. Neither repair changes a fit, source cell, protocol
fingerprint or scientific method. The successful radius replay verifies the
interval result against v3.

**Decision:** retain corrected additive as the predictive baseline; make E0M_L2
the provisional structural research backbone; retain E1P_L2 as the strongest
neural reference; do not promote a scorer. Pair pooling, the encoder and lambda
.0001 do not earn their extra complexity on this experiment.

**One next experiment:** pre-register a bounded, prior-only opponent-conditioning
ablation on E0M_L2, with the current league-average-opponent arm as the nested
control and no other architecture or loss change. The model is already within
.04 RMSE of additive, mean pooling handles the central offensive composition
checks, and the largest remaining failures plausibly combine opponent strength
with realized shooting. Opponent conditioning also directly advances the
two-lineup matchup product. Evaluate the same all/novel point tables, event
channels, basketball fixtures and uncertainty disclosures; do not tune it on
the named examples.

