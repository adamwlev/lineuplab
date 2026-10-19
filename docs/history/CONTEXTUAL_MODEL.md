# The contextual matchup model

*Design contract agreed 2026-09-03. This supersedes `ROLE_MODEL.md` as the
product direction; that document remains useful as the role-allocation sketch.*

## 1. Product question

**2026-09-17 clarification:** the fan-facing rating is for an average game
environment; users need not specify clock, score or foul situation. Shared
game-state models may be used for research diagnostics and defining a common
historical reference without being inputs to the lineup scorer. The completed
`GAME_SITUATION_DIAGNOSTIC.md` readout is conditional sensitivity analysis,
not a promoted forecast or identified context-free player value.

Build two five-man teams and estimate how they fare against each other. The
second team may default to a league-average placeholder, preserving the simple
"rate this five" workflow, but a user can replace every slot with a real
player.

Players are player-seasons, not timeless names. Active players default to the
latest data available; the user can select another season. Historical players
require a representative-season default and remain selectable by season.

The output must answer both **how good** and **why**:

- offense, defense and expected margin in points per 100;
- changes in creation, spacing, rim pressure, turnovers, free throws,
  rebounding and defensive coverage;
- which players are being pushed away from their usual roles;
- uncertainty, with the reason it is large stated in basketball language.

## 2. Three co-equal acceptance standards

No single metric is the northstar. A model is judged on three pillars with
equal standing.

### A. Forward predictive accuracy

Rolling-origin evaluation on future possessions and future five-man units.
Report the current points target and the persistent outcome channels. A
contextual model may be tied or modestly worse in r² if it is materially better
on the other two pillars; the trade must be printed, not hidden.

### B. Counterfactual coherence

Pre-register basketball expectations before reading model output. These are
mechanism checks, not demands that a favored lineup win:

- Jokić + Korver versus Jokić + Westbrook: this is a test of the
  **complementarity residual**, not a requirement that the Korver lineup have
  the higher total rating. Relative to a simple additive model, Korver should
  receive a positive adjustment for spacing and off-ball finishing around
  Jokić, while Westbrook should receive a negative adjustment for spacing and
  usage competition. Westbrook's much greater individual value may still leave
  his lineup ahead overall. His version should also show more on-ball creation
  and rim pressure. The final total point estimate is for the data to decide.
- Five centers: the model must expose missing primary creation and perimeter
  coverage, reassign somebody into an unfamiliar role, and lower the mean
  without a post-hoc multiplier.
- Five small guards: creation may be plentiful, but rim protection, size and
  defensive rebounding must be stressed.
- Real small-ball units such as the 2021 Clippers and the Warriors death lineup
  must not be mistaken for malformed lineups.
- Lineup order must not matter. Swapping Team A and Team B must negate the
  expected margin.

These checks should be a tracked executable suite, not prose remembered after
the fit.

### C. Out-of-distribution calibration

Uncertainty must widen with unfamiliar **player-role assignments**, profile
combinations, eras and opponent matchups. Validate interval coverage on held-out
real lineups grouped by support distance. Synthetic extremes cannot validate
coverage, but they can verify monotonic behavior: five centers should be less
certain than a conventional real unit.

A Bayesian hierarchy can derive this uncertainty. It cannot derive the correct
out-of-support mean without structural assumptions; those assumptions must be
named and tested rather than described as assumption-free.

## 3. Model decomposition

### Player-season state

Estimate current ability and play style from the latest available box score and
play-by-play data, partially pooled toward career and player-type priors. Thin
or partial seasons shrink more. Career averages remain available but are not
the default state for active players.

**In-season refinement agreed 2026-09-05:** current means **as of a date**, not
only the last completed season. Update evidence within the season; separate
update cadence, historical weighting and forecast horizon. Role/shot-selection
states may update faster than shooting ability. League environment, observed
player-state change and response to a new teammate context are separate layers.
Quarter-origin evaluation is the next primary research regime, with eighths
as a later same-population sensitivity. All estimation stops before the cutoff.
`ASOF_MODEL_EXPERIMENT.md` records the completed snapshot/channel foundation and
the still-pending point factorial, era-aware valuation and fresh additive test.
The subsequent `ASOF_ACCOUNTING_AUDIT.md` completes the strict-date league
conversion/valuation helper, but not its point-model integration. Raw-count
substitutions leave FTA bias intact; retain EB. A descriptive full-league versus
common-lineup population gap motivates distinguishing deployment/game-context
effects from complementarity before fitting joint opportunity-share responses.
No target-population offset is to be learned from future evaluation outcomes.
The completed `ASOF_DEPLOYMENT_AUDIT.md` shows that coarse clock/score mix
reduces the full/common descriptive FTA gap by 1.190/100, leaving 1.037/100
within-state. Common fives heavily overrepresent Q1/Q3; this is deployment,
not identified synergy. The completed `ASOF_OPPORTUNITY_EXPERIMENT.md` supplies
a prior-only joint-share calibration control: FTA and 3PA MAE improve 11/11
seasons for both profile bandwidths, while TO MAE gets slightly worse. Generic
mean-bias correction must not be called complementarity. Point integration and
the equally refreshed additive comparison remain pending; none of these
intermediate results changes the three acceptance standards.

`ASOF_ADDITIVE_FOUNDATION.md` now supplies strict-date additive fitting and
completed-window validation primitives, including short current-season effects.
This removes an implementation obstacle to the equally refreshed comparison;
it is not a tuned benchmark, point-score improvement or scorer promotion.

`ASOF_ADDITIVE_TUNING.md` adds quarter-matched prior-window selection and one
completed 2026 Q3 pilot. The outer fit uses all games before January 15, 2026;
the selection window is in 2024–25. The remaining prior-penalty edge changes
validation predictions by 0.004438 pts/100 in the last expansion and is labeled
provisional, not silently accepted. The full quarter point comparison is still
pending; this verifies the additive control's operation, not a new accuracy
gain, contextual mechanism or OOD result.

The completed one-axis follow-up finds <=0.000495 pts/100 remaining sensitivity
at this origin and retains prior=1 without changing original grid flags.
`ASOF_POINT_INTEGRATION.md` now supplies the player/channel accounting bridge:
calibration preserves player shares within each shot/FT/TO category, allows
total player usage to change, and recomputes shooting and passing demand from
those same attempts. All saved common cells reconstruct; this is accounting
verification, not a new role-response mechanism or point-prediction result.

The full quarter point experiment and additive-reference correction are now
complete. `ASOF_ADDITIVE_REFERENCE_RESULTS.md` supersedes the warmup status and
the original contaminated comparison. Corrected additive MAE8.0920 versus
structural8.1461 is a small, inconclusive season-paired gap; additive has more
consistent ranking/squared-error advantages, while novel-lineup errors remain
tied. Pooled raw r² .12043/.10719 includes era-level differences and is not an
annual within-season or single-possession metric. Structural assist deficit
retains its own gain; other point-level era/opportunity gains are unestablished.
No known pairs, scorer promotion or change to the three standards. Counterfactual
means, context-dependent role adaptation and latent/OOD uncertainty remain open.
The completed high-exposure review directs the next diagnosis toward separating
opportunity-volume errors from conversion/valuation and role/context errors.

### Role and resource allocation

Predict which players consume creation, shots and rebounding opportunities in
this five. Team resources are constrained: one possession's usage and shot
opportunities cannot be independently granted to all five players. A player's
output is evaluated at the assigned role, not simply added at his historical
role.

### Offensive outcomes

Predict persistent intermediate outcomes before total points: turnovers, twos
and threes attempted, shot location, free throws and offensive rebounds. Value
those outcomes with training-period conversion rates. Shot making remains a
separate, more strongly shrunk component.

### Defense and the opponent

The opponent is part of the input. Allocate defensive assignments and price
the mismatch between the offense's demands and the defense's available
coverage. The incumbent has no offense-by-defense term; its two-team margin is
only one lineup's net rating minus the other's.

### Uncertainty

Propagate player-state, role-allocation and outcome uncertainty to the final
margin. Report both the interval and its main cause: thin player data, unusual
role, unfamiliar composition, cross-era comparison or extrapolated matchup.

## 4. Known-pair chemistry policy

The structural model is **identity-free by default**: two players who never met
must receive the same treatment as players with the same observable profiles
who did. Known-pair chemistry may survive only as an optional current-season
residual layer if all of the following hold:

1. it improves forward accuracy over the full contextual model;
2. turning it on does not change counterfactual mechanism explanations;
3. it does not narrow uncertainty for unrelated or cross-era pairs;
4. the tool labels it as observed shared history rather than general chemistry.

It is never the primary representation of complementarity.

## 5. Prototype zero: what exists now

**Read historical measurements below as a research sequence.** The refreshed
2026-09-04 checkpoint at the end of this section supersedes older point-model
rho headlines: those averaged unstable reliability ratios. MAE, raw r² and
ordinary correlations were not affected by the reporting correction.

`context_projection.py --compare` is the first narrow prototype. It uses the
strict-new-pair context matrix by default, excludes known-pair chemistry and the
asserted coverage gate from its numeric baseline, and compares projected player
rates in basketball units.

For Jokić/Murray/Gordon/Porter with Korver versus Westbrook, career-state
prototype output currently says:

- incumbent identity-free net: **+13.63 → +14.38**, so the Westbrook lineup is
  **+0.75 pts/100**;
- Westbrook version: **+7.82 assists, −4.08 threes, +3.69 turnovers per 100**;
- beyond the raw player swap, the stable context cells assign the Westbrook
  version **−2.46 team usage events and −0.51 assists per 100**; each shared
  player gives up about 0.60 usage events;
- after enforcing a finite team usage pool, the estimated contextual part of
  the Westbrook-for-Korver swap is **−0.40 offensive pts/100** using only
  context cells with |t| ≥ 3 (**−0.52** using the complete matrix);
- the Korver version's maximum context shift is **4.11 standard deviations**
  versus 2.66 for Westbrook, so both contextual estimates are extrapolations and
  must eventually receive a wide interval.

The context matrix was regenerated with its intended condition-number cap and
now ships its own-profile and teammate-context scales separately. The original
projection incorrectly applied it with marginal player-profile scales; the
sign above survived that correction. It remains a local conditional
association, not a causal promise.

The two point values answer different questions and must stay separate in the
tool: **+0.75** is the incumbent's total additive-plus-usage lineup difference,
while **−0.40** is the stable-cell prototype's contextual adjustment to the
Westbrook-for-Korver swap. A successful model can report both without claiming
that Korver is the better player or that his lineup must win.

The mechanism is only partly complete. The measured assist/finisher and usage
competition effects support Korver's off-ball fit around Jokić. The four fewer
threes in the Westbrook lineup are a player-profile difference, not yet a
separately estimated *spacing interaction*. The current data do not justify
calling the latter causal or assigning it extra points.

### First forward kill test

`contextual_validation.py` tests 2022–2025 lineups using player profiles built
strictly before each held-out season. Across 259,116 qualifying possessions:

| points construction | corr. with cross-fit true quality | calibration slope | predicted sd | true sd |
|---|---:|---:|---:|---:|
| unconstrained sum of five historical usage profiles | 0.205 | 0.087 | 10.67 | 4.48 |
| fixed, training-period team usage pool | **0.285** | **0.477** | **2.66** | 4.48 |

The unconstrained point identity is rejected: it lets five players manufacture
or destroy possessions and is drastically over-dispersed. Usage conservation
is a material structural improvement, but 0.285 remains well below the
incumbent additive model's roughly 0.57 established lineup-scoreboard
correlation. The channel model is therefore a promising explanatory layer, not
yet a replacement scorer.

### Exploratory usage-allocation screen

Uniformly rescaling all five players is not the only way to divide a fixed
usage pool. An exploratory 2015–2024 screen assigned usage in proportion to
each player's historical usage raised to an exponent. The possession-weighted
cross-fit true-quality correlation rose from **0.433 at exponent 1** to
**0.473 at exponent 3**, then flattened to 0.470 at exponent 4. Descriptive
calibration r² followed the same shallow shape (0.0376 → 0.0433 → 0.0427),
while raw r² and MAE were essentially unchanged and poor.

This is evidence that *who absorbs the finite offensive workload matters*; it
is not a selected production constant. The same held-out origins were used to
screen the exponent, individual season estimates are noisy, and the partial
2025 sample prefers less concentration. Do not set the exponent to 3 globally
from this screen.

The follow-up uses each origin's observed lineup-ranking correlation only to
choose later origins. An expanding-history selector improves cross-fit
true-quality rho by **+0.0365** over exponent 1 across 2016–2024 (8/9 seasons,
paired t=2.91) and descriptive calibration r² by **+0.0047** (9/9, t=2.91).
A prior-season-only selector points the same way but is noisier (+0.0279 rho,
t=1.86). Raw r² and MAE do not materially improve. Thus concentration survives
an honest forward hyperparameter protocol as a **ranking** improvement, not as
a calibrated standalone point model. `contextual_allocation_rolling.csv`
contains the fixed arms, chosen alphas, and selection histories.

### Assigned-load response

`usage_load_response.py` supplies the missing stage-3 test without using the
outcome as the role assignment. For every held-out season from 2015 through
2024 it builds usage profiles from earlier seasons only, allocates the fixed
team pool from the five players' prior profiles, aggregates that assignment to
player-game, and asks how the same player's realized output moves as the
composition-driven assignment changes. Across the ten held-out origins:

| held-out player-game outcome | player FE slope | player + team-game FE slope |
|---|---:|---:|
| realized usage | +0.410 (t=23.99) | +0.331 (t=14.30) |
| assist rate | +0.0215 (t=15.26) | +0.0104 (t=3.45) |
| points per usage event | **−0.0785 (t=−7.23)** | **−0.1845 (t=−11.82)** |
| turnover share | +0.0183 (t=6.26) | +0.0276 (t=5.58) |
| eFG | −0.0405 (t=−6.99) | −0.0987 (t=−10.90) |
| assisted share | −0.1185 (t=−12.30) | −0.1208 (t=−9.18) |
| FT% placebo | +0.0103 (t=1.11) | −0.0120 (t=−0.61) |

The assignment therefore predicts a real role change: more load, more assists,
more turnovers, less efficient and less assisted scoring. This is much stronger
mechanism evidence than the old residual `role_stretch` feature. It is still a
conditional association—coaches and opponents select the observed lineups—so
the point translation is tested independently.

A single response coefficient is too crude. The composition-driven log-load
was therefore decomposed, exactly within each lineup, into (a) the five's mean
load relative to all five players' native usage and (b) each player's deviation
from that mean. With player fixed effects, points per usage falls with both the
common component (**−0.1014 ± 0.0199, t=−5.10**) and the relative component
(**−0.0654 ± 0.0072, t=−9.08**). Turnovers rise and eFG and assisted share fall
on both channels; both FT% placebos are null.

### Strictly prior point transport

For every scored season, the response slopes are averaged only over earlier
origins. Applying one undifferentiated player+team-game slope to the full load
change fails: at alpha 3 it moves true-quality rho **0.464 → 0.439**, raw r²
**−0.156 → −0.263**, and MAE **8.30 → 8.70**. The within-team residual slope
cannot be transported as the cost of moving the whole lineup.

Applying the separately measured common and relative slopes passes its first
point test. Against fixed alpha 3 over 2016–2024 it moves the
possession-weighted summaries:

| metric | alpha 3 | + prior-only decomposed response | paired season delta |
|---|---:|---:|---:|
| cross-fit true-quality rho | 0.4636 | **0.4813** | +0.0212 ± 0.0109 (7/9) |
| descriptive calibration r² | 0.0397 | **0.0421** | +0.0027 ± 0.0014 (7/9) |
| raw r² | −0.1558 | **−0.1354** | +0.0217 ± 0.0162 (4/9) |
| MAE | 8.299 | **8.155** | −0.150 ± 0.082 (5/9) |
| ordinary lineup correlation | 0.1795 | **0.1874** | +0.0088 ± 0.0036 (8/9) |

The two earliest cold-start seasons lose cross-fit rho; every origin from 2018
through 2024 improves it. This is a promising candidate component, not yet a
shipped scorer: the evidence is modest, alpha 3 and the response were developed
on the same historical era, and its pathological-lineup mean is only partly
solved.

On career profiles, the candidate makes the correct *relative-to-additive*
Jokić distinction. Alpha 3 changes the Westbrook-minus-Korver offensive gap by
−2.08 pts/100 versus uniform allocation; the load response gives 1.47 back,
leaving a net **−0.61 structural residual** for Westbrook before the separately
labeled −0.40 context readout. It lowers the named five-center lineup from
120.86 under uniform allocation to **115.31**, while a five-guard offense rises
to 119.51. That offense/defense asymmetry is basketball-coherent.

The unresolved failure is equally important: five copies of Gobert still score
126.97 in this accounting because the population curve lets him retain too much
of the finishing efficiency earned in an assisted role. A pre-registered
interaction with prior assisted share points the expected way but is not
measured: common interaction −0.0124 ± 0.0148 (t=−0.83), relative interaction
−0.0140 ± 0.0152 (t=−0.92). Do not ship or tune that interaction. The next
allocator must distinguish creation from finishing more directly and attach a
wide role-specific posterior when it extrapolates.

Two cheap follow-ups are closed. First, enforcing the literal identity that
assisted makes cannot exceed the five profiles' summed assist supply is far too
hard: it penalizes ordinary real lineups by 2.84 pts/100 on average, expands
predicted SD 3.12 → 5.73, moves raw r² −0.156 → −0.621 and MAE 8.30 → 9.92.
Career profiles were observed in different teammate contexts; their raw assist
supply and assisted-finish demand are not simultaneous promises. Do not soften
this failed cap into an unvalidated multiplier.

Second, `role_support_validation.py` asks whether a held-out lineup becomes
less predictable when its players' assigned common/relative load is far from
their own training history. It uses prior profiles, prior response slopes,
prior-origin affine calibration, and the product of game-disjoint half-sample
residuals to remove shot noise. Centered persistent-error SD across increasing
role-distance quartiles is **3.95, 3.94, 3.50, 3.87 pts/100**. The Q4−Q1
error-variance difference is **−0.58 ± 3.76 (t=−0.15, 4/9 positive)**. This
distance does not support an interval-widening schedule inside the observed
range. A synthetic extreme may still be far away; that proves extrapolation,
not calibrated coverage. Uncertainty must come from the richer role model's
posterior rather than this distance heuristic.

### Direct roles, opportunity channels and the first structural point score

The literal assignment question rejects the earlier alpha-3 interpretation.
`role_allocation_validation.py` conditions on actual held-out team usage and
asks only who consumed it. Alpha 1 wins every rolling origin: event-weighted
NLL is 1.81635 versus 1.87346 at alpha 3 and share correlation is 0.931 versus
0.882. `role_channel_validation.py` finds the same honest alpha-1 assignment
for usage, FGA, assists and assisted makes. Self-created makes have a small
alpha-1.5 MAE improvement but no NLL/correlation confirmation. Alpha 3 remains
a point-ranking diagnostic, not the role allocator.

The next layer predicts the team total rather than conditioning it out.
`channel_totals_validation.py` gets split-half corrected rho of 0.710 for
twos, 0.693 for threes, 0.541 for turnovers, 0.322 for free throws, 0.620 for
offensive rebounds and 0.558 for self-created makes under the alpha-1 usage
ledger. Shot mix and rebounding are real, forecastable lineup mechanisms.

`channel_points_validation.py` values rim/paint/midrange/corner-three/above-
break-three/FTA/ORB/turnover creation with training-only coefficients and adds
player shooting above league expectation for that shot mix. Adding making
improves true-quality rho over creation alone in all 10 origins (paired
+0.2559 ± 0.0484, t=5.29). With prior-only calibration, the structural score
is essentially tied with the alpha-1 box-score identity: MAE 7.561 vs 7.576,
raw r² −0.0132 vs −0.0141, true-quality rho 0.413 vs 0.430.

### Assist supply-demand is the first passing structural residual

Passing supply alone predicts assisted makes less well than finishing demand
(true-quality rho 0.282 vs 0.452), but their positive mismatch is informative.
`assist_residual_validation.py` fits
`max(assisted-finish demand - assist supply, 0)` on completed origins only,
with a nonpositive coefficient. Against calibration alone on 2016–2024, it
improves rho **0.413 → 0.482** (+0.0739 ± 0.0175, t=4.22, all 9 origins), raw
r² by +0.01284 (t=3.11), and MAE by 0.0855 (t=−2.78). The latest honest model
is `30.454 + 0.7154 × structural score − 0.4168 × assist deficit`.

This is not the failed hard cap in softer clothing. The hard cap assumed every
unsupported finish becomes a miss and destroyed calibration. Here the point
cost is measured directly from future real lineups, retains ordinary lineups,
and improves every ranking origin.

The career-state panel now scores the named distinct five-center offense
100.69, five guards 122.97, five Goberts 106.75 and five Jokićs 116.17 without
a gate. It scores Jokić/Korver 119.92 and Jokić/Westbrook 115.62; before final
calibration the finite ledger changes Westbrook's +9.92 freely additive gap to
−6.62, a −16.54 complementarity residual. That magnitude is not yet a product
claim. The real-lineup p99 assist deficit is 12.25, while the five-center and
five-Gobert diagnostics are 19.04 and 23.82. Their means extrapolate and their
intervals must say so.

### What the first uncertainty decomposition does and does not support

`assist_support_validation.py` estimates persistent lineup error with
game-disjoint residual products, so make/miss noise is not mistaken for
uncertainty in the lineup mean. Persistent SD is 3.88 at zero assist deficit,
3.69 in the positive-low band, 3.19 in positive-mid and 5.15 in positive-high.
The high-minus-zero variance contrast is only t=0.91. Beyond the prior p99 the
point estimate rises to SD 7.23, but only 4.4 reliable lineups per split-season
occupy that tail and its season contrast is t=1.24. This licenses a disclosed,
conservative tail uncertainty floor—not a claimed calibrated schedule.

`profile_bootstrap_uncertainty.py` adds game-cluster sampling error for the
players' profiles and shares a player's draw across repeated copies. It is
small for the named legal lineups (0.34–0.51 points/100) and 0.79–0.83 for the
five-copy diagnostics. The remaining interval work is held-out coverage plus
shot-valuation, point-calibration and assist-slope uncertainty.

### Latest observed player state

`player_season_profiles.py` now defines the representation required by the
product contract: one EB-shrunk profile per player-season, an exact season
override, and otherwise the latest sufficiently observed state at or before an
as-of season. A player who misses a season does not become league average;
Haliburton in a 2025-26 counterfactual defaults to his 2024-25 state. This
plumbing has now passed the rolling-origin representation comparison below:
approximately tied overall, not a uniform recency improvement. Explicit
`--profile-mode latest` runs the current-state diagnostic panel; historical
career-mode scripts remain available for comparison.

### Context scoring upper bound

`contextual_upper_bound.py` deliberately leaks the full corpus into player
profiles, historical contexts and the context matrix before scoring 2022–2024.
It is a favorable screen, not a valid forward score:

| leaked arm | corr. with cross-fit true quality | calibration slope |
|---|---:|---:|
| usage-normalized profiles | 0.497 | 0.865 |
| + complete context matrix | **0.505** | 0.848 |
| + only context cells with \|t\| ≥ 3 | 0.495 | 0.852 |

The complete matrix adds only 0.008 even with leakage, and the stable named
mechanisms add nothing. There is no present evidence for putting this context
projection into the scoring mean. It remains useful as a separately labeled
explanatory/counterfactual readout while a better constrained role allocator is
developed.

### Refreshed checkpoint through 2025-26 (2026-09-04)

All 2,492 newly targeted games now reconcile exactly to official scores after
explicit technical-point accounting, and every stored possession signature
matches the repaired cached-page parse. Derived channels consistently exclude
bookkeeping team rebounds and include nontechnical special free throws.

On 2016–2026 future origins, adding assist deficit to calibration improves MAE
7.600 → 7.497 pts/100, raw r² −0.0075 → +0.0100 and ordinary correlation
0.164 → 0.199. Season-paired MAE changes by −0.10685 ± 0.03309. Corrected
pooled-moment reliability rho is 0.410 → 0.499; some individual seasons remain
unidentifiable, so headline the ordinary metrics. Latest-state profiles are
roughly tied with cumulative profiles: MAE 7.474 versus 7.497, paired
difference −0.01879 ± 0.05154. They lose MAE in 2025 and 2026. The representation
is useful under the product contract, not selected as a universal accuracy win.

Latest-state intervals achieve 50.2%, 79.8%, 95.1% coverage at nominal 50/80/95%
on held-out 2019–2026 finite-batch outcomes. This is not latent synthetic-lineup
coverage. A sparse, noisy tail cannot lower the diagnostic variance below the
conservative tested tail floor. Five Goberts scores 106.69 with diagnostic 95%
range 91.75–121.62; Jokić/Korver scores 122.60 with 114.82–130.38. Valuation,
defensive and matchup uncertainty are still incomplete.

Jokić/Westbrook scores 119.48, with a −3.27 relative-to-additive interaction
residual before final calibration. The exact-2025 Haliburton-for-McConnell
swap beside Nembhard/Nesmith/Siakam/Turner adds 2.75 points/100 and has a +0.80
interaction residual before calibration. On supported actual 2026 Pacers fours,
healthy-2025 Haliburton for Nembhard adds 5.05 points/100 and relieves assist
deficit by 5.58/100. Only 44.9% of all Pacers possessions qualify for that
preseason-state observed-rotation audit; it is not a whole-team or causal
explanation of their decline.

The next coherence audit is offensive rebounding: the creation regression
conditions on attempts and gives ORB a negative coefficient, but the fixed
usage budget does not grant the extra shot opportunity a rebound creates.
Test a rebound-dependent budget before treating this as a faithful independent
mechanism. Add thin-history/rookie states and real small-ball cases next.
Full results and reproduction commands are in `SESSION_HANDOFF.md` §15–18.

**2026-09-05 update:** that rebound audit and two follow-ups are complete; see
`REBOUND_EXPERIMENT.md`. A miss-conditioned, competing-capture model improves
direct ORB prediction and gives better rebounding positive value while making
no boards from nonexistent misses. Latest point MAE is 7.528 versus the
accepted 7.474. It reduces the direct-budget five-center score from 125 to 118,
but this remains too respectable (2026 database league offense is 116.38).
The rebound component is promising; the complete offensive counterfactual is
not solved. Creation-role/shot-opportunity transport and unexplained team
rebounding remain open. Neither the accepted scoring path nor HTML is changed.

**Creation follow-up, 2026-09-05:** `CREATION_EXPERIMENT.md` separates a player's
workload change from a change in his four teammates' projected passing supply,
both centered on his prior profile-season context. Forward across 2016–2026,
passing improves assisted-made share (Brier 11/11; cross-entropy 9/11) and
modestly improves turnover prediction (cross-entropy 10/11). Shooting benefits
are not established. A properly normalized softmax model lets workload improve
shot-mix cross-entropy 10/11; extra passing's shot-mix gain is inconclusive.
The failed linear/projection arm is saved. Only 36.7% of player-possession
exposure qualifies; these are not all-player, causal or OOD results. Do not
price an assisted-share increase as an additional make. Supported channels
are candidates for controlled point transport, not adopted score components.
The matched additive/structural benchmark is still owed because old rigs used
different targets, coverage and held-out-season detrending.

**Matched benchmark completed:** `MATCHED_BENCHMARK.md` repairs that comparison.
Chemistry-free additive MAE is **7.45360** versus structural **7.47420** on
5,774 identical future season-lineup cells; paired gap +0.01430 ± 0.07616
is not established. Ordinary correlation is **0.25226 versus 0.20506**, with
the structural model lower 10/11 (paired −0.04660 ± 0.01075). Novel-lineup
MAE is also tied, while the quality-signal gap persists. Adding the same
deficit term to the additive core does not improve it. This supports continued
contextual work under the coequal standards without dismissing the additive
core's stronger player-quality information. No hybrid or point-scorer promotion.
Only 32.22% of future possessions meet the matched sample criteria; comparable
finite-half coverage is not synthetic latent/OOD calibration.

**Concrete disagreement review completed:** `DISAGREEMENT_AUDIT.md` and
`reports/matched_disagreement_review.md` reconstruct both frozen scores for
258 high-exposure cells. All top-six gaps persist in chronological halves,
but most individual error-gap intervals include zero. Assist deficit is zero
in all six. Broad FTA overprediction (+4.87/100, positive 11/11 seasons) and 3PA
underprediction deserve a prior-profile/opportunity-accounting audit. Some
star-lineup misses coincide with better-than-prior realized shooting; same-five
reversals prohibit a simple named-player fix. Discuss with Adam before assigning
mechanisms. Distance-derived three-point buckets are not tracking coordinates.

## 6. Immediate sequence and kill tests

1. **Completed:** reject the unconstrained rate sum; retain the
   training-period usage-pool constraint as the new baseline.
2. **Completed:** workload concentration survives rolling-origin selection as
   a lineup-ranking improvement, though not in raw point accuracy.
3. **Completed:** composition-predicted load measurably changes realized role
   and efficiency. A prior-only common/relative response modestly improves the
   alpha-3 point model; a single transported slope fails.
4. **Completed nulls:** prior assisted share does not identify type-specific
   response; a hard assist-supply cap destroys real-lineup calibration; and
   empirical assigned-load distance does not order persistent forecast error.
5. **Completed:** direct role allocation selects alpha 1; persistent opportunity
   channels support a shot-creation + shooting decomposition that is tied with
   the box-score point benchmark.
6. **Completed:** a prior-only, sign-constrained assist-deficit residual improves
   ordinary ranking correlation in 10/11 refreshed origins and produces coherent
   offensive stress-test means without a gate. Next audit isolated mechanism
   changes, starting with a rebound-dependent opportunity budget.
7. **Partly completed:** game-split persistent error, shared player-profile
   uncertainty and held-out finite-batch interval coverage are measured. Propagate
   shot-valuation/calibration/assist-slope uncertainty, validate latent error, and
   widen beyond the observed assist-deficit range without asserting coverage
   synthetic data cannot verify.
8. Do not promote the current context matrix into the point mean. Refit it and
   both standardization scales inside forward origins only if a new constrained
   role formulation first beats the fixed-pool baseline.
9. **Representation validated, cases run:** latest observed player-season state
   ties cumulative profiles overall; exact overrides and Jokić/Haliburton cases
   work. Add partially pooled rookie/thin-history states and real small-ball
   cases. Career-only output and silent missing-player exclusions are not the
   product.
10. Test whether contextual rate changes improve or hold forward prediction.
   Creation transport has supported workload/shot-mix and passing/turnover
   intermediate channels, not an established shooting-efficiency response.
   The matched pre-origin benchmark is complete: near-tied MAE, but an additive
   quality-correlation advantage and no gain from additive+deficit. The concrete
   disagreement review is complete; discuss it and audit FTA/3PA accounting,
   then test supported channel integration against
   the additive, accepted structural and rebound controls.
   A small loss is acceptable, but its size must be known.
   **Updated priority:** date-aware snapshots and the first quarter-channel test
   now support within-season refresh (3PA improves 11/11 seasons). Finish dated
   league valuation/joint opportunity mix and a quarter point comparison with
   an equally fresh additive control before assigning gains to role adaptation.
11. Add the defensive assignment layer against the actual opposing five, then
   evaluate matchup margin and uncertainty.
12. Only after those pass, replace the HTML tool's scoring path.

Stop if the projected intermediate outcomes are not calibrated or if
out-of-support uncertainty does not widen. Do not compensate with another
unvalidated output multiplier.

## 7. Supporting code

- `experiments/asof_state.py`, `asof_channel_validation.py`: strict-date
  structural profiles with weighted effective exposure, online-observable
  intraseason origins and matched intermediate freshness diagnostics. These
  do not yet replace the point scorer or full additive-profile schema.
- `experiments/tool_model.py`: database-free reference implementation of the
  incumbent tool, including a two-lineup interface and an identity-free arm.
- `experiments/context_projection.py`: measured teammate-context readout and
  side-by-side prototype, with fit-scale and usage-pool corrections.
- `experiments/contextual_validation.py`: forward lineup validation of the
  intermediate point construction, including game-disjoint cross-fit truth,
  prior-origin alpha selection and prior-only load-response transport.
- `experiments/player_season_profiles.py`: epoch-aware player-season profiles,
  latest-observed selection and exact historical-season overrides.
- `experiments/bref_ingest.py`: rate-limited, raw-page-cached and atomic current
  data updater; `experiments/data_version.py` prevents silent stale-cache reuse.
- `experiments/usage_load_response.py`: strictly prior composition assignment
  joined to held-out player-game outcomes; player and team-game fixed effects,
  common/relative load decomposition and the assisted-share heterogeneity kill
  test.
- `experiments/creation_transport_validation.py`: profile-context-centered
  workload and teammate passing, within-player diagnostics, and prior-only
  intermediate probability forecasts; linear and softmax shot-mix controls.
- `experiments/matched_benchmark.py`, `matched_additive.py`,
  `matched_boundary_audit.py`: prefix-refitted chemistry-free additive core
  against the structural scorer, common targets/cells/calibration protocol,
  novel-lineup checks, finite-half intervals and numerical boundary stability.
- `experiments/role_support_validation.py`: rolling assigned-role distance and
  game-disjoint persistent-error calibration; the first distance schedule is
  null.
- `experiments/role_allocation_validation.py`,
  `experiments/role_channel_validation.py`: direct held-out assignment tests.
- `experiments/channel_totals_validation.py`,
  `experiments/channel_points_validation.py`: lineup opportunity totals and the
  training-only creation + making point decomposition.
- `experiments/assist_residual_validation.py`: rolling, sign-constrained assist
  supply-demand residual in points.
- `experiments/structural_counterfactuals.py`: named offensive mechanism and
  pathological-lineup panel.
- `experiments/possession_outcomes.py`, `experiments/shots_target.py`: outcome
  channels and leak-free training-period valuation.
- `experiments/context_profile.py`: within-player context sensitivity.
- `experiments/page_calibration.py`: end-to-end calibration of the incumbent.
- `tests/test_tool_model.py`, `tests/test_context_projection.py`,
  `tests/test_contextual_validation.py`, `tests/test_usage_load_response.py`:
  golden product arithmetic, symmetry, fit-scale, resource conservation,
  prior-only selection and fixed-effect diagnostic checks.
