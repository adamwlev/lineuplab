# v14: role transport, rebound facilitation, and possession renewal

Codex, 2026-09-15. Experiment design requested by Adam after the v13 review.
**DESIGNED, NOT IMPLEMENTED OR LAUNCHED.** This document specifies the scientific
choices for implementation. Freeze its hash with the implementation before
pilots; document any necessary design amendment before seeing v14 results.

Read `AGENTS.md`, its required context, `reports/joint_capability_v13_codex_review.md`,
`JOINT_CAPABILITY_V13_EXPERIMENT.md`, `REBOUND_EXPERIMENT.md`, and
`CREATION_EXPERIMENT.md`. Historical claims that all richer inputs or rebound
budgets are closed do not supersede the narrower tests defined here.

## 1. Questions and product scope

The campaign asks five distinct questions:

1. Does v13's role improvement survive matched seeds? Is the useful information
   recent player change, historical teammates, or the difference between a
   proposed lineup and the player's accustomed context?
2. When creation is short, should forgone free throws become only turnovers,
   or a mixture of turnovers and field-goal opportunities?
3. Can a model distinguish collecting an offensive rebound from increasing
   the other four players' chance of collecting it?
4. Does predicting rebound recovery and allowing the resulting extra attempts
   improve the complete offense, rather than merely its rebound feature?
5. How much remaining error belongs to league-level seasonality or training
   instability rather than the basketball interaction model?

Prediction, coherent counterfactuals and honest OOD uncertainty remain co-equal.
Improved basketball mechanisms can justify a modest accuracy trade, which must
be printed. No synthetic score targets, known-pair/identity chemistry, named
player bonuses, coverage gate, or automatic promotion.

This is a large **development** experiment on repeatedly used years, not fresh
confirmation. More seeds reduce optimization uncertainty; they do not create
new independent seasons or erase selection from v13.

Authorized by the present turn: design/documentation and read-only database
inspection. Adam explicitly clarified that local database access is welcome.
A subsequent implementation task may extract a new versioned snapshot from
the local database and derive v14 labels/states from it. Database access is
not an optimization to avoid at the expense of scientific quality. Keep the
old caches immutable; no database mutation, scraping, model export, deployment
or commit is included. Full training requires a separate launch request after
verified commands are ready.

## 2. Size, seeds, and controls

**16 designs × seeds {17, 23, 41} × 48 quarter origins.** Three seeds for every
design, not just for the successful ones. 2015 warms calibration; primary
evaluation remains 2016–2026, 44 quarters, exactly the existing 5,607 cells /
726,364 possessions. Intermediate event evaluations have their own disclosed
opportunity populations. No rebound-label filter may shrink the point table.

There are 2,304 arm-seed-origins. Seven complete seed trajectories already
exist in v13 and are candidates for explicit reuse: BASE17/23, ROLE17,
SL17/23, ROLE_SL17, B_SL17. With verified reuse this leaves **1,968 new
arm-seed-origins / 3,936 new inner/reset-final fits**. Without reuse, the total
would be 4,608 fits. Do not copy a fit across changed objectives or inputs.

At v13's average throughput, new fits alone imply roughly 33 hours; allow
approximately 36–60 hours for planning, pending actual pilot timing. This is
not a promised runtime. Report CPU, wall time, forecast/report overhead and
disk estimates from the pilots before handing Adam a command.

Retain exact saved additive, V9 NN, old HALF/GLOBAL, and v13's single-seed
ROLE_SL half-blend as historical controls. Matched-seed comparisons within v14
are the architecture evidence; improvement from seed averaging is separate.

### Registered model matrix

All unqualified backbones are v13 joint event+point native decoders. ROLE is
the v13 dated-feature head; SL is its supply/load mechanism. New module details
are binding in the following sections.

| ID | Design | Difference / main comparator |
|---|---|---|
| C0 | BASE | Exact J_BASE; shared baseline |
| C1 | ROLE | Exact J_ROLE; C1−C0 replicates dated-feature effect |
| C2 | SL | Exact J_SUPPLY_LOAD; C2−C0 replicates constraint effect |
| C3 | ROLE_SL | Exact J_ROLE_SUPPLY_LOAD; v13 leading native design |
| C4 | B_SL | Exact B_SUPPLY_LOAD; trained-blend basketball alternative |
| T0 | RECENT_SL | C3 head sees only four recent-minus-long features |
| T1 | HISTORY_SL | C3 head sees only four historical teammate features |
| T2 | CURRENT_SL | Replace historical teammate features with proposed other-four context |
| T3 | SHIFT_SL | Replace historical teammate features with proposed-minus-historical context |
| F0 | FTA_ROUTE | C3; learned FG/TO routing of opportunities removed from FTs |
| R0 | RB_AUX_DIRECT | C3 + own-capture rebound head; fixed opportunity budget |
| R1 | RB_AUX_FAC | R0 + leave-self-out facilitation; fixed budget |
| R2 | RB_RENEW_DIRECT | R0 + miss/recovery/renewal loop |
| R3 | RB_RENEW_FAC | R1 + renewal loop; main rebound candidate |
| X0 | RB_RENEW_FAC_ROUTE | R3 + F0 routing; comparison against both parents |
| X1 | RB_RENEW_FAC_SHIFT | R3 with T3 role head; comparison against both parents |

Do not choose a different parent for X1 after inspecting T0–T3. Do not add
attention/covariance/depth/width sweeps, new loss-weight grids, or an anchored
F−B residual. Negative component results still complete their registered runs;
stop for correctness/nonfinite/provenance failures, not discouraging r².

## 3. Data feasibility and rebound-label contract

### Existing controls remain immutable; new measurements can use the database

Reuse the v13 manifest's v3 grouped labels/states, schedule, v9 sidecar,
additive offsets and saved controls. For new targets, extract `nba.possessions`
texts, IDs, game IDs, period/clocks, possession orientation and ten player IDs,
plus game dates and player-name lookup, in a **read-only, repeatable-read**
transaction. Write the extraction and its manifest under a fresh v14 prefix.
Restrict the comparative experiment to the original possession-ID population;
assert cached IDs, game/date, lineup orientation and point targets reconcile.
Database changes since the old snapshot must be reported, never silently
mixed into a supposedly matched experiment. No need to query the database
again for each seed/epoch once this extraction is frozen.

On 2026-09-15, read-only schema inspection confirmed `texts` plus clocks and
lineups are stored. Six bounded recent samples include an explicit FG miss →
named ORB → dunk, a missed final FT → named ORB → new foul/FT trip, repeated
miss/rebound chains, and team rebounds. Sequence is present in the text, though
individual event timestamps and exact substitution-time lineups still need
parser audits. This is materially richer than the aggregate rebound cache.

Use the following immutable caches for alignment and reconciliation, not as a
restriction on new information:

- `experiments/cache/possession_channels_ba7aeb377198_5.npz`;
- matching cached possession context and `shot_events2` file;
- v3 `derived/game_lineups.npz` and `player_game_states_v3.npz`;
- existing player-name/fixture registries, for reporting only.

Resolve and fingerprint every actual filename, extraction query/schema,
database snapshot metadata, data epoch and alignment map in v14's manifest.
Do not invoke old builders that overwrite source caches. Missing inputs may
be obtained by explicit read-only extraction into the new prefix; if old and
new populations cannot be reconciled, report that before fitting.

### Why the old rebound labels cannot simply be reused

Read-only feasibility inspection on 2026-09-15 found 6,059,380 cached possession
rows, 647,852 attributed offensive rebounds, 2,040,599 attributed defensive
rebounds, and 2,911,228 missed FGs. There are 12,052 rows with ORB greater than
FG misses, including 9,738 credited ORBs on rows with no FG miss. Some rebounds
follow FTs; mismatched/missing attribution also requires an audit. The old v5
label uses all ORBs over FG misses and clips targets. Do not interpret that as
a clean binomial target. This does **not** invalidate v13, whose core objective
did not use that rebound family.

A provisional channel-only no-FT mask with positive FG misses and
ORB+DRB≤misses retains 2,448,948 rows, 2,421,968 named live recoveries, and
537,293 ORBs (22.184% capture). Another 1,947 no-FT rows have more recorded
recoveries than FG misses. These are corpus-level feasibility counts, not the
v14 modeling population or evidence of predictive signal. That mask was a
cached-only fallback considered before Adam clarified database access; **it is
not the final eligibility rule**. New event-level extraction avoids discarding
every mixed FG/FT possession merely because the aggregate cache loses order.

### New target: clean, credited FG recovery opportunities

Produce a **new** v14 event table and grouped labels. No changes to v3/v5 labels.

1. Join source/context by exact `poss_id`, asserting uniqueness, orientation
   and sorted-offense slot correspondence. Retain ordinal position within
   texts, raw segment, shot type/location, shooter, rebounder, preceding miss,
   FG versus FT, FT attempt number/total, and post-ORB phase where identifiable.
2. Match each named rebound to an unambiguously pending missed attempt in
   source order. Distinguish missed FG from missed final FT. New shots, made
   shots, terminal events, ambiguous FT trips and period boundaries close or
   invalidate pending opportunities; no matching to an arbitrary earlier miss.
   A technical/non-live FT cannot create a live rebound. Normalize special FT
   text using the existing parser rules, but test them on the raw extraction.
3. Primary capture labels use unambiguous **FG** miss/rebound pairs, even in
   possessions that also contain FTs. Store FT rebound opportunities separately
   for audit, not under the FG denominator. Require valid collector/offense
   attribution to the original five. Initially exclude mechanism events in
   possession rows containing substitutions unless exact event-floor parity
   with the grouped five is proved; do not exclude their point outcomes.
4. The opportunity count is L = attributed FG ORB + attributed FG DRB. Six
   categories are the five offensive collectors and an aggregate opponent.
   Team/unattributed/dead-ball rebounds are separate retained records, never
   automatically counted as DRBs or named-player facilitation. L=0 has no
   capture loss, not five false negative collection labels.
5. Aggregate eligible counts onto exact v3 `(game_id, sorted offensive five)`
   rows, retaining all existing rows. Preserve eligible FG misses, recoveries,
   five credited ORBs, DRBs, FT/team/ambiguous events and rejection reasons.
   Assert six counts sum to L and no miss is consumed by two rebound matches.
6. Compare raw/event/grouped/cache totals by season and inspect balanced parser
   cases: FG, final/nonfinal/special FT, blocks, multiple ORBs, team/dead-ball
   recoveries, substitutions, and period-end misses. Report eligible exposure
   by history/novelty/rebound strength/named players. No score-based filtering.

This estimates **credited FG rebound capture on resolved event-floor support**.
It does not observe box-outs or contested status. Team retention and FT boards
remain outside the first modeled renewal loop but are now measured separately.
Use post-ORB sequence labels to audit how subsequent shot mix, conversion,
FTA and turnovers differ from the stationary-loop assumption in §7; do not
discard those labels merely because the first loop has no separate putback
decoder. All primary point targets remain unchanged.
If accurate slot/live-chance labels cannot be obtained, stop that block and
return to Adam; do not silently substitute the old clipped denominator.

### Dated rebound inputs, built only under v14

Create beginning-of-day and quarter-origin states from the eligible counts:
each player's credited ORBs divided by his team's L while on court. Use
180-day exponential decay and a fixed 50-live-opportunity beta prior. Its mean
is the strictly prior league capture rate divided by five. Before any league
evidence, use a disclosed neutral .05 player share. No data-driven prior-grid
selection this campaign. Store numerator, denominator, squared-weight exposure,
effective sample size and provenance dates. These are new derived states, not
alterations to existing profiles. Same-day games update only after all that
day's forecasts; inner validation and outer prediction use their own frozen
cutoff snapshots. Unknown players get the dated prior, not a dropped row.

## 4. Role information: do not fit two algebraically identical arms

v13 ROLE adds `h(own_state, recent4, historical_context4)` into a masked state
correction before decoding. Moving that exact same correction to an identically
masked “own” slot without changing its inputs or downstream use gives the same
forward function. **Do not spend fits pretending those are two architectures.**

T0–T3 keep the 26→32 tanh→18 head, initialization and penalties identical to
C3. T0 zeroes the standardized historical block; T1 zeroes the standardized
recent block. T2/T3 keep recent4 and change only the last four coordinates.

Compute current other-four context from the same as-of raw base states, before
learned corrections, exactly matching v3's historical metric definitions:

- mean `exp(logFGA)+.44 exp(logFTA)+exp(logTO)`;
- mean `exp(logAssist)`;
- mean `exp(logFGA) × three-point location share`;
- mean sigmoid of assisted-made logit.

T2 uses those four levels. T3 uses current minus stored historical four levels.
Subtract in raw basketball units **before** standardization. Means/SDs for
each representation use only its inner/final training prefix with the existing
standardization weighting; floor SD at1e-6. A player with no prior history has
zero shift plus the existing prior state, and is explicitly flagged in reports.
Do not subtract independently standardized quantities.

C3/T2/T3 have matched head size but different information. They test historical
state versus current context versus transport distance, not causal identification
of an individual player's adaptability. FT conversion stays teammate-invariant.
The usual message-off intervention and an extra **role-head-only-off**
intervention must both be reported.

## 5. FTA opportunity routing

F0 changes one v13 assumption: currently every .44 usage unit removed from
FTA by shortage is transferred to turnovers. Retain the same learned
nonnegative supply/FTA attenuation and the same preliminary shortage proxy.

Let preliminary fixed-budget allocations be FGA_i, FTA_i, TO_i and
`removed_i = .44 × (FTA_i − attenuated_FTA_i)`.
Predict `failure_i = sigmoid(b + w · [standardized own18, role8])` using one
shared linear head, initialized w=0 and b=logit(.9). Route:

```
new_TO_i  = TO_i  + failure_i × removed_i
new_FGA_i = FGA_i + (1 − failure_i) × removed_i
new_FTA_i = attenuated_FTA_i
```

Then recompute load from these counts and apply v13 make-logit penalties to the
final attempts. Shortage remains the explicitly reported preliminary proxy;
do not introduce an implicit iterative supply solver. Recompute expected
makes, assisted demand for reporting, points, and every per-player ledger.
Turnover and FGA event labels supervise routing through the existing objective.
Regularize the added weight vector with the existing Adam weight decay; its
intercept has no weight decay. Report initialization-to-fit changes/saturation.

This does not assume every failed foul draw yields a good shot, nor promise
lower FTA simply because the arm is new. It tests whether the old all-turnover
cost inhibits a useful learned attenuation. Perfect old routing is nested at
failure=1 in an algebra test, not by changing its finite initialization.
No fixed FTA cap, predetermined five-center score or teammate change to FT%.

## 6. Competitive collection and facilitation

The rebound head reads **raw as-of player information**, not player IDs:
standardized own18, role8, logit of the new rebound prior p_i, and
log1p(rebound effective exposure): 28 inputs, hidden16 tanh, scalar output.
It does not borrow current labels, realized opposing fives, or height/draft
information. Population standardization is training-prefix-only. Inputs are
shared between direct and facilitation arms.

For direct capture, use scores
`s_i = log(p_i) − log(1 − league_capture) + 2 tanh(own_head_i)`.
The opponent category has score0, fixing the softmax reference. At zero own
correction, five average priors p_i=league_capture/5 reproduce league capture.
Use eps1e-6 only for logs, record boundary activation, and preserve exact zero
rebound/no-miss behavior in the event loop.

Facilitation adds a separate same-width donor head:

```
f_j = 2 tanh(donor_head(v_j) − donor_head(0))
s_i_fac = s_i + mean(f_j for j != i)
[P(collector1), ..., P(collector5), P(opponent)] = softmax([s_1,...,s_5,0])
r = sum(P(collector_i))
```

Both final head layers initialize to zero using an RNG separate from backbone
initialization and minibatch order. Direct and facilitation designs start with
identical capture. The donor anchoring avoids an arbitrary constant facilitator
intercept; regularize weights with .0001 decay and add .01 times training-weighted
mean squared own correction / donor contribution. Print both penalty parts.
The bounded log-score corrections are disclosed regularization, **not** a
35% team ORB cap or a claim that extrapolated probabilities are calibrated.

The donor's facilitation does not directly increase his own collection score.
Because recovery is competitive, improving the other four can lower his own
share while improving the team. This is exactly the distinction the current
sum-of-own-rates representation lacks. It is a statistical mechanism hypothesis,
not a measured causal box-out coefficient. Parameter uncertainty and substitution
confounding remain; do not print “Adams causes X” from these heads.

Use six-category multinomial negative log likelihood on **all** L opportunities,
with opponent recoveries included. Also decompose evaluation into team capture
binomial loss and collector allocation conditional on offensive recovery.
Fitting only collector shares among ORBs cannot learn whether the team wins
more rebounds. Independently report teammate-only observed/predicted credits.

Rebound head inputs are fixed cached states. Auxiliary arms therefore do not
backpropagate rebound gradients through the offense backbone; their extra loss
can still alter composite early stopping. Renewal arms additionally allow point
and count gradients through r. Report that distinction; R0−C3 is not solely
an “extra input” test. Inspect whether point gradients damage capture calibration.

## 7. Possession renewal: replace the budget, never add free points

Use a deliberately bounded stationary mean-field process. This is **not** a
full play-by-play simulator or a putback model.

At each inner/final cutoff, use exactly the prior rows and 365-day decay of
v3's `usage_budget` (all earlier rows, not the 730-day training-loss weights).
Let U_ref be that existing FGA+.44FTA+TO budget, O_ref the eligible credited
FG ORBs per possession from §3 on the same weighted rows, and
`B = U_ref − O_ref`. Require B>0. Other renewals, FT bookkeeping and unattributed
recoveries remain absorbed in this prior non-modeled budget; they are not
silently learned as extra FG rebounds.

Let `eta = eligible named live FG recoveries / total cached FG misses` on those
same weighted prior rows, with matching observed-FG support in numerator and
denominator. Require 0≤eta≤1 and print exclusion mass; no silent clipping of
accounting failure. Keep a declared cold-start eta=0 if there is no evidence.
This estimates opportunity availability for the **modeled** eligible population,
not a universal claim about the probability any individual miss is live.

1. Evaluate the offense including its role/supply/load/FTA routing at U_ref.
2. Divide final FGA_i, FTA_i, TO_i and expected makes by U_ref to obtain
   per-opportunity-cycle rates. Let
   `m = eta × sum_i,b (FGA_i/U_ref) × location_ib × (1−make_ib)`.
3. With team recovery probability r from §6, set
   `continuation = m r`, `U = B/(1−continuation)`, and
   `ORB = U × continuation`.
4. Scale all first-pass event counts and expected makes by U/U_ref. ORB
   collector credits equal `U m P(collector_i)`. Recalculate point totals from
   made FGs and made FTs only. Rebounds receive no independent point coefficient.

Thus **U = B + ORB**, including the misses generated by renewed opportunities.
When r=0 or there are no misses, modeled ORB=0 and U=B, not U_ref. Ordinary
reference values m_ref/r_ref must reconstruct U_ref when
O_ref=U_ref m_ref r_ref. This subtraction is essential: retaining U_ref as the
non-rebound baseline would pay for existing average rebounds twice.

The first-pass role/conversion response is held fixed during the renewal sum.
Print both first-pass and final implied load/shortage. This assumes a renewed
opportunity has the same action mix and efficiency. The new extraction allows
us to measure departures from that assumption; this first loop deliberately
does not fit a separate post-rebound decoder. Report those phase-specific
errors rather than claim putback quality or a new creation state is solved.
We are testing one coherent replacement of the fixed budget, not introducing
an untested implicit fixed-point solver. A separate first-chance/second-chance
decoder can be designed from the new labels in a subsequent registered block,
not silently added after observing this campaign's performance.

Compute the denominator in float64/log space using the opponent-reference
softmax; never silently cap ORB% or the final score. Assert 0≤m≤1 and
continuation<1, print proximity to1, and fail clearly on numerical invalidity.
Good rebounding can raise a center lineup's offense; that is not a reason to
reverse rebound value to force a desired total.

R0/R1 keep U_ref while estimating the same rebound probabilities. R2−R0 and
R3−R1 test budget feedback separately from adding the supervised head; R3−R2
and R1−R0 test facilitation with and without renewal. X0 and X1 test the two
predeclared combinations, not a winner-selected “everything” arm.

### What the earlier negative rebound work does and does not say

The September4–5 capture/renewal model improved rebound prediction and isolated
coherence but worsened point prediction. v5's added rebound coordinate did not
create new opportunities. v14 differs through joint event/point training,
proper collector/opponent competition, and other-player facilitation.

The v5 marginal correlation between realized U and offensive rating is useful
descriptive context, not an upper bound on a conditional miss/recovery mechanism:
U mixes attempts and turnovers, and their association can cancel. Neither that
statistic nor a positive physical derivative establishes an accuracy gain.
The matched point and opportunity evaluations here decide the empirical result.

## 8. Fitting, stopping, and reuse

Preserve v13's five-year lookback, 730-day row-loss decay, shared V9 five-family
normalizers, shared team denominator, Adam .001, weight decay .0001, gradient
clip5, network/decoder penalties .01, one CPU thread, whole-game batches.
Keep event and team weights1, apart from the already specified native/blend
readout distinction. Missing additive labels affect only the same eligible team
loss; do not remove rows from event supervision.

For rebound arms add **one** normalized rebound NLL term of weight1; do not
renormalize the five existing families from1/5 to1/6. The rebound denominator
is the untrained direct capture reference on that prefix, shared across all
rebound arms/seeds; weighting/exposures use the same causal training rows.
No available rebound labels means zero rebound contribution with exposure0
printed. Evaluate team-capture and collector parts separately without giving
each another implicit unit of training weight.

Inner validation is the previous complete quarter. No model, head normalizer,
rebound state, season-stage estimate, hyperparameter or stopping decision may
use the outer quarter. Max96 epochs, patience8, min_delta1e-5; retain exact
minimum validation composite as in v13. Reset/full-prefix fit for exactly the
selected epoch count. No epoch extension based on outer results. Do not use a
rebound head trained through the outer cutoff during inner validation.

Original v13-compatible seeds may be reused only after code-path/data/objective
equivalence tests, checkpoint/receipt hashes, and replay of 2016q1/2026q4 controls.
Use an immutable reference registry, not rewritten/copied completion records
that make old fits look newly trained. Freeze the seven allowed trajectories
before launching. If parity fails, diagnose before launch; any fallback refits
need an explicit manifest amendment and new cost estimate. Never partially
reuse phases from a different scientific objective.

### Fixed seed ensembles and stopping sensitivity

Primary model-level forecasts average the **three separately prior-calibrated
seed predictions**, with equal weights fixed in advance. Also print every seed
and seed-paired component difference. External half means half additive and
half that seed-averaged forecast. No best-seed selection, outcome-fitted seed
weights, or extra ensemble-level affine calibration.

Save every new inner/final epoch checkpoint with hashes. The existing best-epoch
rule is primary. A bounded secondary training-stability comparison uses only
**seed41**, which is newly fit for every design: average predictions from final
epochs max(1,e−2)…e, where e is the inner-selected epoch. This costs saved
checkpoints/replay, not extra epochs or new fits. Give that forecast its own
prior-only point calibration and compare against seed41's exact-best forecast.
No averaging of scalar losses or weights masquerading as prediction averaging.

Average complete expected event counts/points; reconstruct effective conversion
probabilities from summed expected makes/attempts where needed. Report individual
checkpoint budgets and their mixture, not an invented single renewal state.
Only best weights exist for reused v13 seeds, so they are excluded from this
secondary comparison, never silently assigned duplicate “late checkpoints.”

## 9. Separate causal league-level experiment: no additional NN fits

Apply four predeclared corrections to the same completed forecast paths:
NONE, STAGE, RECENT, BOTH. Primary architecture rankings always use NONE.
Apply the same league-level delta to additive, saved controls, every new NN,
and every half-blend; a common shift commutes with blending. Do not credit a
generic league correction to a neural mechanism.

Use the frozen grouped population's actual points/possessions, not a scraped
league table or an in-sample model-residual series. These are grouped-population
environment estimates, not automatically the whole NBA. All calculations stop
before the forecast quarter; no intraquarter updating in this campaign.

Stage is the known quarter-of-season index. From at most the last five fully
completed seasons with all four schedule windows, fit weighted points/100 on
season intercepts plus quarter effects s_q constrained to sum zero. Use a fixed
ridge penalty `50,000 × sum(s_q²)` with possession-sum SSE; season intercepts
are unpenalized. This is 50,000 pseudo-possession shrinkage, not a selected grid.
No complete season means s=0. Do not estimate a current-season intercept from
its future games. Only seasons represented by the frozen schedule qualify;
print which, including the 2020/2021 irregular seasons rather than deleting
them after results.

Let L be the saved shared league baseline for this origin and define a reference
grouped mean G and average stage effect s_bar on all strictly prior grouped
rows with 365-day decay. This explicit G avoids assuming L was constructed with
the same weighting. Let G28 and s28 be their unweighted-possession counterparts
over the last28 calendar days before origin, with W28 possessions and
`h = W28/(W28+10,000)`; no observations means h=0.

```
NONE:   delta = 0
STAGE:  delta = s_current_quarter − s_bar
RECENT: delta = h × (G28 − G)
BOTH:   delta = (s_current_quarter − s_bar)
               + h × [(G28 − s28) − (G − s_bar)]
forecast_new = forecast_existing + delta
```

Only a **change** relative to G is transported onto L/the existing calibrated
forecast; do not replace L with a differently selected population mean. Prior
dates outside the schedule contribute stage0 to the reference and are disclosed.
Keep all functions/penalties fixed; no selecting the best correction from the
outer years. Forecast date/quarter is known without future game results or
observed future schedules. A more granular daily-update regime is separate work.

Report raw versus corrected quarter bias, centered MSE, r²/correlation, and
direct/half comparisons under each policy. Recompute causal finite-outcome
intervals for each corrected path, not reuse the uncorrected residuals.

## 10. Endpoints, contrasts, and all three standards

### Prediction

Print possession-weighted MAE, RMSE, raw r², Pearson correlation, bias and
exposure for all/novel/recurring; per quarter, season, era, prior lineup exposure,
composition distance, player history and new rebound support. Include raw native
F, direct calibrated forecasts, individual seeds, fixed seed ensemble, and
external half. Original A/V9/HALF/GLOBAL and v13 winner remain visible rows.

For every arm compare with C3, additive, old HALF and its listed direct parent.
Primary scientific contrasts use seed-averaged NONE forecasts; fixed external
halves are equally mandatory reporting, not something run only if direct NN loses.
Core planned contrasts: C1−C0, C2−C0, C3−C1/C2, T0/T1/T2/T3−C3, F0−C3,
R1−R0, R2−R0, R3−R1/R2/C3, X0−R3/F0, X1−R3/T3, and C4−C2.

Report equal-season differences, nominal t95 intervals, favorable seasons,
leave-one-season-out and era summaries. For the above direct-forecast all-cell
RMSE contrasts, additionally provide Holm-adjusted p-values as descriptive
multiplicity accounting. Seeds/quarters are not independent replications of
historical basketball. Do not imply these corrections turn reused years into
a confirmatory test. Same-season component effects by seed must be explicit.

Rebound endpoints: live-opportunity multinomial NLL, team-capture Brier/NLL,
collector-conditional NLL, calibration plots/slopes, ORB per100, expected live
opportunities, total U, FGA/FTA/TO and points. Rebound head NLL alone is insufficient:
assess whether renewal predicts the actual event totals and complete score.
Report eligible and all-population opportunity errors separately.

### Counterfactuals and explanations

Carry forward all v13 fixtures, native and final readouts. Add a frozen same-four
rebound panel: current Jalen Brunson / Mikal Bridges / OG Anunoby / Josh Hart
with Adams versus Robinson versus Gobert; and Hart versus a guard replacement
beside a fixed rebounder. Resolve player IDs from the pinned registry, never
silently substitute names. Use available quarter-origin states, flag thin/missing
support and historical overrides; do not create synthetic training outcomes.
The guard replacement is Donte DiVincenzo, fixed here before v14 outputs.

Report own ORB, other-four ORB, total capture, modeled eligible recoveries, U,
first-pass/final attempts and points. Adams may improve the team through other
players' collection without leading the individual count. Robinson and Hart
are qualitative probes, not mandated rankings. No forced Korver/Westbrook
signs; the two baselines (relative to additive and message-off) remain separate.

Saved-fit interventions for all models: messages off, role head off, constraints
off; rebound models additionally facilitation off, recovery odds perturbations,
and renewal off with U_ref restored. Hold other modules fixed during an
intervention; do not refit or inadvertently change the point calibration.

Required mathematical invariants: permutation equivariance/invariance; neutral
donor gives no facilitation; donor raises only other collection scores before
competition; collector/opponent probabilities sum1; zero misses or recovery
gives no ORBs; U=B+ORB; more recovery at fixed shot-cycle quality cannot lower
native points; perfect shooting earns no FG rebound bonus; no double-counted
baseline renewals; FTA routing conserves FGA+.44FTA+TO; all player/event/point
ledgers reconstruct. Nonnegative point-calibration slopes and positive blend
weights must preserve isolated monotonic effects. Entire-player swaps need not
be monotonic because creation/shooting changes too.

Export largest weighted error harms/benefits at ≥100 and ≥200 possessions for
both direct and half predictions, with full player ledgers. Do not restrict
the explanation audit to the best observed arm.

### Uncertainty

Retain separate prior-only 80/95 finite-outcome intervals, correct nullable
booleans and full coverage/exposure by support. Add rebound support (minimum
live-chance effective exposure, capture strength tail, continuation proximity)
and role-shift magnitude. Freeze support-bin thresholds from each training
prefix, not future distributions. Print seed/checkpoint disagreement as
sensitivity, not a latent posterior or fabricated wide OOD interval.

Bounded persistent-error diagnostic, C3/R3/X0/X1 and additive/old HALF only:
within each outer lineup cell, sort whole games chronologically and alternate
games between halves; require ≥4 games and ≥50 possessions per half. With one
quarter-frozen forecast, compute half residual products and report them by
prior support bins, pooled and by season with season-level uncertainty. This
is noisy persistent-error evidence, not latent coverage; shared opponent/era
effects can survive game splitting. Never clamp negative cell products to zero
before aggregation. Do not use this result to tune support widening in v14.

There is no automatic promotion criterion based solely on r². The final report
must give a three-pillar decision for each family, preserving genuine mechanisms
even if their point effects are small and acknowledging unvalidated means.

## 11. Implementation stages and operational acceptance

1. **Source/label audit first, read-only database extraction allowed.** Produce
   the frozen raw snapshot, new labels and dated rebound states under a fresh
   v14 preparation prefix, with durable logs and provenance. Audit joins,
   event sequences, opportunity/FT attribution, coverage and forecast dates.
   No “quick” rerun of an old input builder or mutation of completed caches.
2. **Model/fit/report implementation.** New v14 modules import unchanged v13
   behavior where possible. Keep old frozen producers byte-identical. Unit tests
   focus on the invariants and cutoff/reuse risks above; do not postpone real
   pilots for unrelated cleanup or whole-repository refactoring.
3. **All-design/seed smoke.** Small whole-game cached batches,1 epoch, every
   design/seed, all forecast/calibration/report paths including seed averaging,
   checkpoint averaging, intervals and all three scoreboard slices. No numeric
   zeros substituted for unavailable results.
4. **Full-length operational pilots.** Seed41,2016q1 and2026q4 for C0,C3,T2,T3,
   F0,R1,R3,X0:16 arm-origins. Audit gradient flow, learned-head growth, budget
   magnitude, selection, receipt reuse, figures/ledgers and memory/runtime.
   Pilots validate mechanics, not select arms. Changed scientific behavior
   requires a new prefix/fingerprint and a documented amendment.
5. **Freeze/preflight and handoff for launch.** Registry contains16 designs,
   three seeds, all48 origins,7 eligible reused trajectories, full source/code
   hashes and derived-label receipts. Estimate cost/disk from real pilots.
   Supply verified background, live-log, status, resume and read-only leaderboard
   commands. **Do not launch the full run until Adam requests it.**
6. **One full run then automatic analyses.** Interleave designs/seeds within
   origins so complete-quarter comparisons become available. Save each inner,
   final and epoch artifact before reporting. Reporting failures must not
   retrain successful fits; use fresh derived-only report prefixes when needed.
   Completion includes all contrasts, four level policies, checkpoint sensitivity,
   basketball and intervals, not just training.
7. **Independent review and documented handoff.** Verify actual hashes/diffs,
   recompute matched metrics and sampled model outputs, inspect all three
   pillars and seed contrasts. New review, scorecard/backlog/roadmap/checkpoint;
   no scorer promotion or commit unless separately requested.

### Required artifacts and live visibility

Designated new modules: `joint_capability_v14_data.py`, `*_model.py`, `*_fit.py`,
`*_run.py`, `*_report.py`, `*_league.py`, and a standalone read-only leaderboard;
reuse small pure primitives where justified instead of cloning every old file.
New runner `experiments/run_joint_capability_v14.sh`; matching focused tests.
These are proposed implementation paths, not files/commands that exist yet.

One durable `logs/train.log`, atomic status/process metadata, real run lock,
PID/start time, verified exits, and human-readable failed phase/origin/seed.
Per epoch: train event/team/rebound components and exposure; validation composite
and components; selected epoch/patience; gradients; elapsed; capture/donor/routing
parameter growth. At each complete origin: additive, old HALF, C3, each arm,
seed ensemble and external-half MAE/RMSE/r²/correlation/bias, novel/recurring,
budget/ORB/FTA errors. Warmup prominently labeled. Partial tables use identical
completed origins/seeds, never compare a three-seed model to a one-seed partial
result without labeling it. No monitor that invents summaries from stale logs.

Save source and reuse manifests; label/state coverage and cutoff audits;
checkpoints and curves; complete per-game and per-cell forecasts with component
ledgers; calibration histories and four league-policy deltas; seed/checkpoint
scores; primary/secondary season contrasts; rebound team/collector diagnostics;
fixture interventions; named residual cases; uncertainty source rows and
coverage; persistent-error diagnostics; report receipts; implementation handoff
and independent scientific review. No silent exclusions or altered old artifacts.
