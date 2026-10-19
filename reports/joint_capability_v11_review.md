# Joint capability v11: frozen value/context separation review

Sol, 2026-09-13, following the protocol in
`SOL_JOINT_CAPABILITY_DAY5_PLAN.md`. This review interprets the completed frozen
run; it does not revise the protocol or promote a scorer.

## Verified run

Production completed 96/96 origin-reference cells: 48 quarter origins, two
prior-only reference distributions, two Monte Carlo panels, and zero optimizer
fits. The run made 248,889,082 frozen-model lineup evaluations in 916.0 summed
origin seconds. K stopped at 256 for 25 cells, 512 for 25, and 1024 for 46.
Thirteen cells reached K=1024 without passing both registered panel-agreement
thresholds and remain marked `integration_limited`.

The independent receipt verifies exit 0, SUCCESS, 96 completion records, all
six source hashes, all five frozen scientific-code hashes, 290 gzip streams,
12,358 joined reference-rows, and exact N=M+C and HALF identities. See
`reports/joint_capability_v11_verification.log`.

The two panels' pooled primary MAE/RMSE differ by at most .00119/.00077 across
new arms, below the registered .005 numerical-resolution warning. Thus pooled
leaderboard differences are not driven by integration noise. Individual
synthetic values at limited origins remain less certain; panel agreement is not
a calibrated epistemic interval.

One derived-report defect was found after completion. The original interval
summary reduced an object column containing numpy booleans and warmup NaNs as
one truthy object, printing coverage near 1/5607. Forecasts, interval radii and
row-level coverage indicators were correct. The completed source directory is
untouched. `joint_capability_v11_postrun.py` regenerated only the aggregation in
the new `joint_capability_2026_09_13_v11_postrun` prefix, with a source hash and
7/7 focused tests. All coverage numbers below use that correction.

## Predictive result

Primary population remains 44 quarters in 2016–2026, 5,607 lineup-quarter cells
and 726,364 possessions. Novel fives are 2,073 cells / 226,256 possessions.

### Exposure-weighted prior reference

| forecast | all MAE | all RMSE | raw r2 | novel MAE | novel RMSE | recurring RMSE |
|---|---:|---:|---:|---:|---:|---:|
| additive A | 8.09195 | 10.84099 | .12043 | 8.90390 | 11.85302 | 10.35068 |
| V9_SPREAD N | 8.14017 | 10.86667 | .11626 | 8.86194 | 11.77283 | 10.43087 |
| HALF | **8.07274** | 10.80812 | .12576 | 8.83865 | 11.76624 | 10.34554 |
| GLOBAL | **8.07069** | 10.80970 | .12550 | 8.84177 | 11.77345 | **10.34422** |
| VALUE_SWAP | 8.09397 | 10.83666 | .12114 | 8.89603 | 11.84217 | 10.34970 |
| CONTEXT_RELEASE | 8.07692 | **10.80808** | **.12577** | **8.83242** | **11.75864** | 10.34939 |
| FULL_SWAP | 8.09979 | 10.83618 | .12121 | 8.89440 | 11.83512 | 10.35262 |

The registered primary contrast is VALUE_SWAP minus HALF on recurring RMSE.
It is +.00538 points/100, nominal season 95% interval [-.02784,+.03860], favorable
in 4/11 seasons. Recurring MAE is +.00745, interval [-.02965,+.04454], 5/11.
Replacing the neural main effect with additive value at the same half-context
dose therefore does not recover the recurring-lineup gap.

CONTEXT_RELEASE is essentially tied with HALF overall: RMSE -.00029,
[-.00551,+.00493], 4/11; MAE +.00378, [-.00408,+.01164], 3/11. It has a small,
consistent novel RMSE gain: -.00720, [-.01352,-.00089], favorable 8/11 seasons;
novel MAE is -.00670, [-.02349,+.01008], 7/11. Against additive its overall RMSE
change is -.03314, [-.06538,-.00089], favorable 9/11, similar to HALF's already
documented blend result. These are reused development years and multiple
comparisons, not fresh confirmation.

### Uniform prior reference

The conclusion is not reversed. VALUE_SWAP recurring RMSE is +.01675 versus
HALF, [-.02290,+.05641], 4/11 favorable. CONTEXT_RELEASE overall RMSE is +.00463,
[-.00974,+.01900], while novel RMSE is -.01063,
[-.02422,+.00296], favorable 8/11. FULL_SWAP is worse than CONTEXT_RELEASE on
overall RMSE by +.04482, nominal interval [.00438,.08526]. Uniform-reference
hybrids also acquire more negative bias. No replacement arm earns adoption.

The fixed decomposition changes materially with its declared population. Across
all 6,179 descriptive cells, EXPOSURE minus UNIFORM has RMS .431 and maximum
1.436 points/100 for M (and the opposite for C); half-dose hybrids have RMS .215
and maximum .718. This is not catastrophic for pooled rankings, but it confirms
that “individual value” and “context” are reference-defined rather than unique
latent basketball truths.

## What the decomposition learned

Under EXPOSURE, the average origin has main-effect cell SD 2.81 and interaction
SD .40; A and M correlate about .80. Under UNIFORM those are 3.07 and .57. On
real cells the mean C is +.029 under EXPOSURE and -.307 under UNIFORM. Exact
zero-centering applies to the synthetic product reference, not the actual lineup
distribution, so these real-lineup means were correctly left untouched.

The key negative is interpretability. Functional ANOVA did mathematically
separate average player insertion value from departure in a particular five, but
that departure is not the message mechanism and does not inherit its basketball
meaning. It includes every nonlinear budget/decoder interaction. The saved NN
was trained jointly with its own value surface; the residual can compensate for
that surface instead of transferring cleanly onto A.

This directly answers Adam's pre-run concern: **the frozen NN weights did not
adapt to the new player values**. v11 is the necessary frozen control, and its
failure cannot reject a model trained against the replacement values.

## Basketball standard

The final totals show why CONTEXT_RELEASE's small novel-lineup gain is not enough.

| EXPOSURE fixture | A | N | projected M | projected C | HALF | CONTEXT_RELEASE |
|---|---:|---:|---:|---:|---:|---:|
| five Goberts | 111.80 | 117.85 | 113.08 | **+4.77** | 114.82 | 117.21 |
| limited centers | 111.16 | 112.02 | 110.35 | **+1.66** | 111.59 | 112.42 |
| five Jokics | 134.66 | 127.21 | 134.78 | **-7.57** | 130.94 | 127.15 |
| small guards | 134.06 | 125.50 | 128.47 | -2.97 | 129.78 | 128.30 |
| familiar real 2026 five | 119.06 | 118.27 | 118.49 | -.21 | 118.67 | 118.56 |

The original native message increments are -15.33 for five Goberts and -10.49
for limited centers. Yet the projected C terms are positive because their low
reference-average main effects absorb more than the message penalty. Conversely,
five Jokics receives a negative C despite a +3.72 native message increment.
There is no arithmetic contradiction; they are different estimands. There is a
product problem: C cannot currently be described to a fan as the learned lineup
complementarity adjustment. Restoring it raises five-Gobert offense back above
117, weakening rather than completing the five-center check.

For Jokić/Korver versus Jokić/Westbrook, EXPOSURE C is -.677/-.737, a tiny .060
Korver relative advantage; UNIFORM is -1.633/-1.626, a tiny -.007 disadvantage.
VALUE_SWAP changes the total comparison relative to additive by only about +.030
under EXPOSURE and -.004 under UNIFORM. This is reference-sensitive and near the
integration scale, not evidence for either qualitative story. The saved native
message increments still favor Westbrook, +6.05 versus +2.89. Adam explicitly
allowed the data to disagree, and no ranking was forced.

The clone ladder is also non-monotone in final N and projected C: projected C
rises from -.21 at one Gobert to +4.77 at five while the native message becomes
steadily more negative. Historical injected Korver remains honestly omitted from
the current-state projection rather than silently substituted; its v10 diagnostic
is preserved. Defense and opposing-five effects remain unmodeled in all values.

## Uncertainty standard

Corrected finite-outcome coverage is near nominal. For EXPOSURE, HALF has
cell/possession coverage .795/.794 at 80% and .945/.941 at 95%; CONTEXT_RELEASE
has .793/.790 and .946/.943. Novel 80% cell coverage is .800 for HALF and .799
for CONTEXT_RELEASE; novel 95% is .938/.939. Differences are small and no new
interval method wins.

This experiment exposes two additional sensitivities rather than solving them:
13/96 integrations reached the numerical cap, though pooled metrics were stable,
and the reference definition moves some lineup decompositions by more than a
point. Neither is a calibrated interval for a synthetic lineup's latent mean.
Finite-game coverage does not complete the product's OOD uncertainty pillar.

## Decision and next work

Keep corrected additive as the predictive baseline and HALF/GLOBAL as the best
pragmatic combined research forecasts. Do not promote VALUE_SWAP, FULL_SWAP or
CONTEXT_RELEASE. Preserve CONTEXT_RELEASE as evidence that more neural context
can help novel RMSE; its extracted context term fails the basketball meaning and
extreme-total checks required for a user-facing mechanism.

The natural follow-up, if we continue this line, is a **jointly adapted residual
model**, not another frozen recombination. Start from fixed corrected-additive
lineup value and train the identity-free neural allocation/context network on
the combined forecast, with the residual zero-centered against a fixed prior
reference during training. Retain the event objectives so the residual has
basketball observables, prevent an unconstrained residual from simply relearning
player identity/value, and compare against A, N, HALF, GLOBAL and this frozen v11
control. Its exact target/calibration and centering need a new pre-registration;
v11 did not authorize or run it.

Actual opposing-five/defensive interaction remains the strongest separate route
toward the stated two-team product. Adaptive role states, dated creation versus
finishing inputs, rebound renewal/facilitation, and latent-mean uncertainty also
remain open. Do not infer from v11 that those mechanisms are closed.

