# Open questions, unrun experiments, and directions

**2026-09-17 shared situation diagnostic complete:** see
`reports/game_situation_diagnostic_review.md`. Adam prefers average-environment
tool ratings without user-entered game state. Diagnostic ENV/CLOCK/MARGIN uses
strictly prior shared rates, never new lineup forecasts. Substantial FTA bias
4.010→.995→.913; NN/blend relative point advantage survives. Cleveland2016 still
underpredicts badly, with residual FGA/3PA deficits. Next: inspect persistent
action-allocation/shot-mix/renewal errors under shared clock adjustment, with
benefit controls. Do not repeat aggregate audits or globally subtract FTA.
No refit/promotion/commit; bonus/opponents/latent OOD remain open.

**2026-09-17 FTA diagnosis complete:** read
`reports/v14_free_throw_situation_review.md`. Global neural FTA bias is near0,
not a universal surplus. All3retained arms overpredict substantial common fives
in11/11seasons, while underpredicting fleeting fives and late-game situations.
Combined common>=200 bias+4.010 decomposes into+1.909coarse state mix,
+1.507within-state remainder,+0.370predicted composition,+0.223calendar-weighted
full bias. This is descriptive accounting, not causal attribution. Transfer
cases are not uniquely affected. Next proposal: prior-only environment control
and neutral-reference joint opportunity model, not a blanket FTA penalty or
another aggregate audit. Opponent, genuine foul-drawing and latent-OOD work
remain open. No fit launched; benchmark committed929f8dd, audit uncommitted.

**2026-09-17 next blocks completed:** `TRANSFER_ROLE_BENCHMARK.md` and
`reports/transfer_role_benchmark_review.md` document the systematic observed
team-change cohort and repeated-failure/event-accounting library.1,030eligible
moves;146primary cells/47,419poss. Contextual forecasts beat A on that prescribed
substantial cohort, but ROLE_SL/renewal outperform combined SHIFT and oldHALF
leads broader low-exposure slices. Full-vs-zero explicit shift-channel replay
is small/uncertain. This is not yet a verified-transaction or prospective test.

Next focus: large-lineup FT-volume overprediction (23.20vs18.71FTA/100 in the
primary cohort), including repeated cases. Separate game situation/intentional
fouls, opponents, exposure selection and initial action allocation before a
new constrained allocator. Preserve point budgets; no posthoc cohort-specific
FTA subtraction. Actual-opponent work needs matchup grouping and an opponent-
aware additive main-effect control before cross-team interactions. No training
or architecture change was launched. Keep phase/OOD tracks and all3standards.

**2026-09-17 v14 completed and independently reviewed:** see
`reports/joint_capability_v14_codex_review.md`. No active training or new fits
authorized. Retain ROLE_SL, RB_RENEW_FAC and RB_RENEW_FAC_SHIFT; the last leads
pooled RMSE but not MAE, novel performance or extreme-center coherence.
Shift inputs and renewal improve across matched seeds; facilitation improves
recovery NLL in11/11 seasons but does not establish Adams-style causal benefit.
FTA routing is effectively null; registered league corrections mostly hurt;
checkpoint averaging is mixed. Do not adopt them by post-hoc winner selection.

Proposed priorities (discussion/design, not launched):

1. Systematic dated offseason-transfer/role-change benchmark, as Adam suggested:
   all eligible transitions, fixed exposure thresholds, common A/NN/blend cells,
   frozen-old-context control, mechanism diagnostics and team-season uncertainty.
   Separate retrospective development from future evidence and causal trade value.
2. Diagnose repeated large-sample failures (e.g.2016 Cleveland) alongside the
   center FTA/action-generation problem; no name-specific coefficients/bonuses.
3. Actual opposing-five inputs/defense with causal defensive controls and proper
   matchup grouping, advancing the two-lineup product and recovery competition.
4. Bounded first-chance/post-ORB decoder test against stationary renewal; retain
   label masks and distinguish phase-conditional audits from phase forecasts.
5. Latent-quality/OOD uncertainty beyond finite-game coverage and seed spread.

Reporting follow-ups: any new report producer must exclude2015 warmup from its
primary persistent-error summary and clarify first_budget=U_ref, not B. The
corrected derived primary summary is saved separately; do not edit completed
v14 artifacts or its frozen producer. Full review contains quantitative evidence.

**2026-09-15 proposed v14 campaign:** `JOINT_CAPABILITY_V14_EXPERIMENT.md`
turns the priorities below into16 designs ×3 seeds, with direct/facilitated
rebound capture, fixed/renewal budgets, role transport and FTA-routing controls.
Season-level correction and checkpoint averaging are bounded secondary views.
Read-only local DB access is explicitly welcome: create a new raw event snapshot
and resolve FG versus FT recovery rather than being limited by aggregate caches.
Design only; implementation/pilots and a separate full-run launch remain pending.

**2026-09-15 v13 results and proposed priorities:** read
`reports/joint_capability_v13_codex_review.md`. Completed20-arm campaign;
best new additive/role-constraint blend improves pooled RMSE10.80812→10.79364
over old HALF, mainly recurring. This is not yet an established season-RMSE
win, a novel-lineup advance over HALF, or a solved center/OOD product.
Proposed next work, not authorized fits: matched-seed replication of role and
constraints; equal-input individual versus context placement to identify the
ROLE gain; investigate generous FTA/opportunity allocation on creator-poor
units; test prior-only season-stage/recent league level equally for A and NN;
predeclared checkpoint averaging if testing training stability. No96epoch cap
was hit, so simply raising it is not a remedy. Actual opposing fives/defense,
rebound possession renewal and validated hypothetical-mean uncertainty remain
major separate open work. Do not rerun the broad capacity sweep by default.

**Next authorized campaign, 2026-09-14:** `JOINT_CAPABILITY_V13_EXPERIMENT.md`
synthesizes the interface, creation/load, richer teammate summary, role-history
and robustness work into 20 trajectories. Implemented and pilot-verified;
production awaits Adam's launch. See `reports/joint_capability_v13_launch_checkpoint.md`.
Actual opponent inputs, a defensible rebound opportunity loop and validated
latent-mean uncertainty remain separate open work, not claimed v13 deliverables.

**2026-09-14 update:** v12 full rerun is on hold. Read
`reports/joint_capability_v12_partial_codex_review.md` before following the older
launch notes. Saved-fit analysis shows that anchored subtraction can turn a
negative center message effect into a positive C adjustment, and C contributes
most of the observed excess error. Preserve A/V9/HALF, and discuss how to keep
the final forecast connected to the event mechanism before new fits. No new
architecture or continuation run is authorized by this analysis.

**Day6 ready for production, 2026-09-13:** read
[`reports/joint_capability_v12_launch_checkpoint.md`](reports/joint_capability_v12_launch_checkpoint.md).
The jointly trained `A+b+C` and `A+b+G+C` hybrids, causal additive replay,
anchored controls and automatic reports are implemented and pilot-verified.
Production is preflighted but `NOT_STARTED`, pending Adam's explicit launch.
Do not select an arm from the two pilot origins. When complete, the registered
primary question is flexible versus HALF overall RMSE, with strict/flexible,
novel/recurring, basketball and uncertainty evidence all retained. Actual
opponent defense and latent-mean OOD uncertainty remain separate open work.

**Day5 result, 2026-09-13:** see
[`reports/joint_capability_v11_review.md`](reports/joint_capability_v11_review.md).
Frozen reference projection is closed as a promoted recombination: value swap
does not recover recurring performance, and the remaining C term reverses the
basketball meaning of the native message penalty on key center/Jokic fixtures.
Do not repeat with more Monte Carlo samples or select EXPOSURE/UNIFORM by results.
Open: pre-register one jointly adapted additive-plus-context residual that learns
against replacement values while retaining event mechanisms and identity-free
centering. This is not authorized automatically. Actual-opponent defense and
latent-mean uncertainty remain separate priorities.

**Day5 plan ready, 2026-09-13 (Codex/Astra):** implement
[`SOL_JOINT_CAPABILITY_DAY5_PLAN.md`](SOL_JOINT_CAPABILITY_DAY5_PLAN.md) when Adam
asks. It makes the individual-value/context definition explicit before any new
training: a product-reference additive projection of frozen V9_SPREAD, followed
by a fixed value/context replacement factorial using corrected additive.
Two prior-only donor references and numerical integration checks are mandatory.
There are zero new optimizer fits. This supersedes the immediate trainable-mean
arm shorthand below. Keep prediction, final basketball totals and uncertainty
on equal footing; no automatic model promotion or subsequent experiment.

**Current next-work ordering, 2026-09-13 (Codex/Astra):** Day4 is complete; see
[`reports/joint_capability_v10_codex_review.md`](reports/joint_capability_v10_codex_review.md)
for the independent review and qualifications to the initial v10 summary.
The fixed additive/`V9_SPREAD` blend improves prediction, while team-point-loss
doses .1 and 1 do not earn adoption: alpha 1 improves its native team MSE only
0.027%, worsens outer event loss in 11/11 seasons, and attenuates context.

Next, run exactly one bounded experiment separating a cross-fitted, shrunk
individual-value **mean arm** from an explicitly zero-centred `V9_SPREAD`
**context residual**. Test whether their combination retains additive-like
recurring-lineup value and neural novel-lineup behavior. This is not known-pair
chemistry. Do not repeat team-loss dose tuning or reinterpret the post-run
half-`TEAM_1` result as a promoted model. Actual-opponent inputs, adaptive role
states, tracking, rebounds/defense, and latent-mean OOD uncertainty remain
genuinely untested or unfinished after this next decision; see Day4 §9.

Before implementing that proposed experiment, define the additive projection
and reference distribution with saved-model analysis. A message-off NN still
contains budget interactions. Smaller context magnitudes need not be worse,
and these results do not close all team-supervised models. Adam requested
discussion of the next steps; this index does not launch another run.

Working backlog. Read `CLAUDE.md` and `CONTEXTUAL_MODEL.md` first, then
`RESEARCH_OVERVIEW.md` §9–§11. Every item here names *why it matters* and *what
would settle it*, because the expensive failure mode in this project is running
something before knowing what its result would mean.

**The one thing to internalise before touching anything:** every r² measured
before 2026-09-01 came from a **random game split**, which credits any
(player, season) parameter with the answer for the season it is scored on.
Rankings derived that way were wrong, not merely inflated. Use
`forward_eval.py`. Random splits are for variance components only.

---

## 0ad. On-floor influence — closed and opened, 2026-09-08 (Opus)

Full record in `TEAMMATE_INFLUENCE_EXPERIMENT.md`; commits `46d36ed`..`6d56539`.

### The four factors as influence — §11, open

Turnovers, steals, both rebound channels and free-throw rate are now measured
per opportunity with the §10b protocol. Three things to carry forward:

- ~~Price the orthogonal TURNOVER coefficient.~~ **DONE, §11d: it does not
  convert.** Slope-scaled (the forward slope IS the calibration factor; a
  prior-only refit lands at 0.431 against §11b's 0.434) the term is 0.81
  pts/100 and MAE is +0.0025 ± 0.0150. The parent residual's slope on it is
  −0.028 once what the parent already prices is removed, versus +0.637 for shot
  quality, and 5/12 seasons positive. Adding it makes shot quality worse
  (8.1394 vs 8.1321). The player-level attribution is new; the lineup total is
  not, and points see only the total. Use it for tool EXPLANATIONS, not the
  number. Do not re-price it without new structure.
- **A contested-rebound expectation.** Both rebound channels forecast (0.908 and
  1.031 orthogonal) but their face lists are inverted, because `E = d * sum of
  own rates` assumes only one of five can collect a miss when in fact exactly
  one does. This needs an expectation that knows rebounds are competitive, not a
  bigger fit. Until then neither channel should be priced.
- **The free-throw garbage-time test, not yet run.** FT rate has the largest
  spread of the five (5.93 FTA/100 orthogonal, 12/12 seasons) and an
  end-of-bench face list. Demean by (game, score-margin bucket) or drop garbage
  time and re-run `channel_influence_orth`. Cheap. Until then it is recorded,
  not banked.

### Lineup-dependent shot mix — BUILT and held back, §13b

Measured and it works: all six buckets forecast 12/12 on 2.66M held-out
attempts, rim share moves 4.3pp per sd of teammates, and the `flat_mix` control
demonstrates §8j on the same shift (0.069 vs 1.230 pts/100). But priced it reads
slope +0.185 orthogonal to parent and location — about five times over-scaled —
and costs 0.019 MAE. Two ways back in, in order of promise:

1. **Slope-scale it** with `turnover_points.running_slopes`, prior-only. Cheap,
   already written, and the right first move for any term whose forward slope is
   below 1.
2. **Condition on `assisted`.** The arm currently gives a player pushed to the
   rim by teammates the conversion he earns on his OWN rim attempts. The profile
   already carries `assisted`; a created shot and a self-created shot are not the
   same shot. This is the basketball-shaped fix.

### Lineup-dependent shot mix — the earlier reasoning, §12b

Per-bucket conversion is in place (§12b), so the model can finally feel a mix
change: on the old flat curve a long-two-to-rim move was worth +0.006, and on a
per-bucket curve it is worth `2*(rate_rim − rate_longmid)`. Measure teammate
influence on each player's six-bucket mix with the §10 protocol — per ATTEMPT,
with the shooter's own mix as the expectation and only TEAMMATES' attempts
counted, which sidesteps the own-rate accounting artifact that contaminated §11
— then shift `two_mix`/`three_mix` inside the allocation and re-price on top of
`pbp_offset`. This is the pair that must ship together.

### Location-specific conversion — DONE, §12b (kept for the reasoning)

`self_2p` is a scalar per player, so the six location buckets CANCEL out of the
score: verified by perturbing profiles and re-scoring through the allocation
itself, a long-two-to-rim move is worth +0.006 per attempt, not §8i's +0.548,
and mid-to-rim is negative. **Do NOT build a lineup-dependent shot mix on top of
a model that cannot feel one** — that was the previous top-ranked build and it
is a null before it starts.

Build instead: per-bucket make rates `self_2p_rim/_paint/_mid/_longmid` and
`self_3p_c3/_ab3` replacing the two scalars, so moving an attempt to the rim is
worth `2*(self_2p_rim - self_2p_longmid)`, about +0.54 for a league-average
player, earned by the player's own skill at that location. Then and only then is
a lineup-dependent mix worth measuring. This also makes §10's shot-quality
coefficient location-aware.

Data is already cached: `shot_quality.build()` has 5,372,539 field goals with
distance on 100% and shooter matched on 98.9%; `possession_outcomes._bucket2`
has the bucket rule (rim ≤3ft, paint ≤9, mid ≤15, long mid >15, corner three
≤22). The work is a new profile source — the box-score `game_player_stats` has
no per-bucket makes — plus the allocation change.

### Do not re-run

- **The channel parse and the five-channel forward run.**
  `experiments/cache/possession_channels_*_5.npz` and
  `channel_influence_coefficients.pkl` are complete (57s and ~500s
  respectively); the five-channel run reproduces the original four to six
  digits. Re-run only if the channel list changes — the cache key carries the
  channel count for exactly that reason.
- **Fitting a channel on the POINT residual to recover it.** §6's turnover count
  channel correlates −0.003 with the direct count fit at identical spread. The
  point residual cannot identify a channel that is plainly identifiable on its
  own events.

- **Ensembling the additive and structural arms.** Their forward errors correlate
  **0.9856** and neither arm's score explains the other's error (0.50% and 0.00%
  of what each explains). The whole prize from optimal combination is **0.15% of
  RMSE**, and a fixed 50/50 average nearly reaches it. A free joint least-squares
  fit is WORSE than the fixed average — the extra freedom overfits the prior
  windows. Ship the blend if convenient; do not research it.
- **A TWO-VERSUS-THREE mix shift, priced through the current valuation.** Built
  properly (`onfloor_mix.py`, reproduces the parent to 1e-12 at zero shift) and
  NULL: it beats a permuted-identity placebo by 0.0057 ± 0.0049, because a
  two-to-three swap is worth **0.0137 points** on the league mix. Do not redo
  that particular arm. **This does NOT close the location route** — see §8i:
  the model's per-location valuation correlates +0.989 with raw points per
  attempt and a long-two to rim move is worth +0.548. The six-bucket location
  mix is untried and is where the value is.
- **A smooth control on the model's own predictions**, as a correction rather
  than a control: worse than doing nothing forward, and it makes the identity
  coefficients worse when they are partialled against it.
- **The free own/teammate split for volume or composition channels.** Not
  identified, twice, for two different reasons: usage is zero-sum inside a
  lineup, and the teammate block is intrinsically better conditioned than the own
  block. Per-shooter possession attribution would NOT rescue the volume case —
  the constraint is definitional, not a data limit. Only two-point CONVERSION
  identifies (91% on the other four; placebo splits 88% the other way).
- **A fitted coefficient for the opponent adjustment.** A prior-only kappa
  removes more schedule contamination and scores WORSE than kappa = 1.

### Open, in the order I would take them

0. **DONE — shot quality forecasts and is priced (§10, §10b, §10c).** Shot-level
   slope 1.082 ± 0.084 over 2.66M out-of-sample attempts, 12/12 seasons; priced
   in points it improves every metric with a clean placebo, but the MAE gain
   (−0.0103 ± 0.0158) is not established. **The useful generalisation: this
   benchmark resolves a lever worth ~0.04 MAE and not one worth ~0.01.** Levers
   below that threshold need either a lower-noise evaluation population or to be
   judged on mechanism rather than on points.

0b. **Superseded — score shot quality in POINTS.** The forward
   test passed: slope 1.082 ± 0.084 on 2.66M out-of-sample shots, 12/12 seasons,
   EB shrinkage calibrated and essential (raw coefficients make the Brier score
   worse). Worth ~0.91 pts/100 of lineup spread. What remains is feeding it into
   the structural arm's making term and scoring on the completed run's cells —
   the only thing that lets it move a lineup rating.

0b. **Superseded — forward-validate shot quality (§10).** Adam's isotonic-distance test says a
   player raises his teammates' field-goal percentage at the same distance:
   Jokic +1.69 ± 0.36 pp with the free-throw placebo at +0.38, 99.2nd percentile
   of 933 players. Descriptive and in-sample. Estimate the coefficient strictly
   before an origin and ask whether it predicts the window after. Reliability is
   0.397, so heavy shrinkage; the honest prior is that much of it will not carry.
   This is the FIRST thing to do, because it is a mechanism the model has no
   term for at all — `self_2p` and `self_3p` are fixed per player.

1. **A lineup-dependent SIX-BUCKET location mix.** §8i sizes it: the gap
   between predicted and actual located attempts is worth a within-quarter sd of
   2.96 pts/100, of which **1.35 is reliable** (split-half 0.209) — larger than
   the opponent adjustment already banked. Existing data, existing valuation,
   same machinery as the composition channels. Tracking data is NOT a
   prerequisite; the model already prices location at +0.989 against raw points
   per attempt. Roadmap R04's tracking lead is the step AFTER this one, and it
   buys within-bucket openness rather than location.
2. **Attempt-weighted conversion influence.** The conversion influence enters as
   a plain sum over five, which is only right if all five shoot equally; §8's
   identified split gives the attempt-weighted form. Cheap, uses coefficients
   already saved, untried.
3. **A two-sided evaluation population.** Defence is scored (§9) and the swap
   tool prices a named opponent (§8f), but no population evaluates a matchup.
   That is what the northstar product needs measuring on.
4. **The remaining over-dispersion.** Both arms are still too wide after
   calibration; an extra shrink of ~0.79 takes 0.5% off MSE for no modelling.
   Free, applies to both arms, changes no comparison.
5. **Thin-history coverage.** Q1 training coverage is 68% because a five
   containing a player with under 100 prior possessions is dropped.

### Process notes earned

- `tests | tail && git commit` commits on a RED suite: a pipeline returns the
  last command's status. Use `set -o pipefail` or check the exit code separately.
  This put one commit through with a broken test (`13fdab7` repairs it).
- A control block whose columns carry an accounting identity is rank-deficient
  and fakes a failed control. Print `eigvalsh(F'F)` before believing one.

---

## 0ac. Contextual product direction — agreed 2026-09-03

**Current execution checkpoint, 2026-09-08:** full48-origin run, additive level
correction and complete saved-fit replay DONE. Read
`ASOF_ADDITIVE_REFERENCE_RESULTS.md`. Additive MAE8.0920 / structural8.1461;
small inconclusive MAE gap, more consistent additive ranking/squared-error
advantage, novel fives tied. All530 tests and independent real audits pass; no
jobs. Original and corrected runs/protocols are pinned. Do NOT repeat pilots,
fits or replay. Next use `reports/asof_centered_disagreement_review.md` (247
high-exposure cases) to separate opportunity quantity from conversion/valuation
errors and specify one role-response experiment. Existing structural controls
show no established point gain from era/opportunity changes; assist deficit
retains its gain. No numerical tuning sweep is a new automatic prerequisite.

The three standards now have equal standing:

1. forward predictive accuracy;
2. basketball-coherent counterfactuals;
3. calibrated uncertainty, especially out of distribution.

A contextual model may lose a modest amount of forward r² if it makes a
material, measured gain on either of the other two. The fan-facing question is
two five-man lineups against each other, with Team B defaulting to league
average. Players default to their latest season, with explicit historical
seasons a desirable extension.

The Jokić/Korver/Westbrook check is about an **interaction residual**, not which
lineup must win. Relative to a simple additive baseline, Korver beside Jokić
should receive a positive spacing/off-ball adjustment and Westbrook a negative
spacing/usage-competition adjustment. Westbrook's superior individual value
may still make his lineup better in total.

Known-pair chemistry is excluded from the primary model. It may remain only as
an optional, labeled observed-history residual if it improves forward accuracy,
does not change the contextual mechanisms, does not narrow unrelated or
cross-era uncertainty, and remains separately ablatable.

`CONTEXTUAL_MODEL.md` is the full contract. The first kill test is complete.
The paragraphs below retain the research sequence; current measurements and
next actions are at the end of this section. Historical point-model rho
headlines are superseded by the pooled-moment correction in
`RESEARCH_OVERVIEW.md` §39, not directly comparable to refreshed values.

An unconstrained sum of five historical usage profiles is rejected (cross-fit
true-quality rho 0.205, slope 0.087, predicted/true spread 10.67/4.48
pts/100). Enforcing the finite team usage pool raises rho to 0.285, slope to
0.477, and cuts predicted spread to 2.66. Resource allocation is therefore
real structure, but the channel model remains well behind the incumbent's
roughly 0.57 lineup-scoreboard rho.

A 2015–2024 exploratory allocation screen strengthens that conclusion without
settling the allocator. Dividing the fixed usage pool in proportion to
historical usage raised to exponent 3 improves possession-weighted cross-fit
true-quality rho from 0.433 (exponent 1) to 0.473, with a shallow peak before
exponent 4; descriptive calibration r² moves 0.0376 → 0.0433. Raw r² and MAE
do not materially improve, individual seasons are noisy, and the same held-out
origins were used for the screen. **Do not hard-code 3.**

The strictly forward follow-up is now complete. Selecting alpha from expanding
earlier-season lineup-ranking correlation improves cross-fit true-quality rho
by +0.0365 over alpha 1 across 2016–2024 (8/9 seasons, paired t=2.91) and
descriptive calibration r² by +0.0047 (9/9, t=2.91). Last-season-only selection
points the same way but is noisier (+0.0279, t=1.86). Raw r² and MAE are flat.
This validates workload concentration as a ranking mechanism, not the channel
model as a standalone point forecast.

The applied context prototype also had two reproducibility defects. The cached
strict-new matrix was the untruncated, ill-conditioned fit despite the research
memo describing the 0.05 SVD truncation, and projection used marginal
player-profile standard deviations where the regression required separate
teammate-context standard deviations. The matrix has been regenerated at
condition 19.5 and now exports both scales. With those fixes and usage
conservation, the Jokić Westbrook-for-Korver swap is +0.75 in total incumbent
value but −0.40 in stable-cell contextual adjustment (−0.52 with the complete
matrix)—the desired distinction—while the canonical lineup now includes Jamal
Murray as its conventional point guard. The Korver version is flagged 4.11 SD
out of support.

Do **not** promote the current context matrix into the scoring mean. A
deliberately leaked upper bound on 2022–2024 moves true-quality rho only 0.497
→ 0.505 with the full matrix; stable cells move it to 0.495. The context fit is
an explanatory result until a different constrained role formulation proves
otherwise.

The stage-3 kill test is complete. With profiles built strictly before each
2015–2024 test season, composition-assigned load predicts more realized usage
and assists, but lower scoring efficiency, higher turnover share, lower eFG and
less assisted scoring within the same player; both FT% placebos are null. The
negative points-per-usage slope is −0.0785 ± 0.0109 with player fixed effects
and −0.1845 ± 0.0156 after also absorbing team-game effects. Separating the
lineup's common load from each player's relative load gives −0.1014 ± 0.0199
and −0.0654 ± 0.0072 respectively.

Transport matters. Applying the stricter within-team scalar slope to the whole
load worsens the point model. Using prior-origin common and relative slopes in
their matching channels improves alpha 3 over 2016–2024: true-quality rho
0.4636 → 0.4813 (paired +0.0212 ± 0.0109, 7/9), raw r² −0.1558 → −0.1354,
and MAE 8.299 → 8.155. It improves rho in every origin from 2018 onward. This
is a candidate structural mean, not yet a production scorer.

It improves the named five-center offense to 115.31 and leaves the canonical
Westbrook swap −0.61 pts/100 worse than uniform-allocation expectation, but five
Goberts still score 126.97 because finishing efficiency is being transported
into a creation role. Prior assisted share does **not** identify the missing
heterogeneity: its common and relative efficiency interactions are t=−0.83 and
t=−0.92. That cheap route is closed.

The literal assist-resource follow-up is also closed. Capping assisted makes at
the sum of five independent profiles' assist rates penalizes ordinary lineups
by 2.84 pts/100, expands predicted SD 3.12 → 5.73, and moves raw r²
−0.156 → −0.621. The identity is true within one realized lineup, but profiles
from different contexts are not a simultaneous supply/demand ledger.

The first role-distance uncertainty schedule is null. Using strictly prior
common/relative load histories and game-disjoint half-residual products,
centered persistent-error SD by increasing distance quartile is 3.95, 3.94,
3.50, 3.87 pts/100; Q4−Q1 error variance is −0.58 ± 3.76 (t=−0.15). Do not use
assigned-load distance to narrow or widen intervals. A role posterior still
has a structural reason to widen beyond observed support, but it must be
validated separately.

Direct allocation and the first full offensive structure are now measured.
Conditioning on actual held-out team totals, alpha 1 is the correct usage/FGA/
assist/assisted-make allocator; alpha 3's earlier gain is a value/ranking
effect, not literal role assignment. Strictly prior lineup totals strongly
predict shot mix, turnovers, offensive rebounds and self-created makes.

Valuing those channels with training-only weights, then adding player shooting
above the expectation for his shot mix, ties the alpha-1 box-score point model
after honest calibration (MAE 7.561 vs 7.576; true-quality rho 0.413 vs 0.430).
A pre-registered assist deficit—assisted-finish demand beyond passing supply—
then improves rho to **0.482**, raw r² by +0.0128 and MAE by 0.086 across nine
future origins. This is the first candidate that improves prediction and fixes
the pathological mean: distinct five centers 100.69, five Goberts 106.75,
five guards 122.97, without the gate. The center diagnostics exceed the real
p99 deficit support (12.25), so uncertainty is now the binding pillar.

Immediate work remains deliberately narrow:

1. **Completed:** the 2,492-game update, database audit, cache rebuild and
   refreshed forward/interval/latest-state evaluations. Do not repeat them.
2. **Rebound tests completed 2026-09-05:** see `REBOUND_EXPERIMENT.md`. Direct
   budget expansion fails; miss-conditioned capture improves ORB prediction
   and independent coherence, but gives up a little latest-state point accuracy
   and still prices five centers around 117. Investigate team-rebound residuals
   (including Adams's supported-lineup underprediction) and shot/creation-role
   transport. Do not manufacture the center answer with a rebound penalty.
3. **Next coverage test:** partially pool rookies/thin player histories. The
   Pacers observed-rotation audit covers only 44.9% of all possessions. Quantify
   coverage and accuracy together, including low-minute real lineups.
4. Held-out finite-batch interval coverage is measured; finish latent/OOD
   uncertainty including valuation/calibration/assist-slope uncertainty. Test
   real small-ball units alongside the completed latest-state synthetic panel;
5. keep context transformations out of the point mean unless the allocator
   clears its forward baseline;
6. only then build direct opponent/defensive assignment and the two-team page.

Refreshed 2016–2026 results: assist deficit improves MAE 7.600 → 7.497 and
raw r² −0.0075 → +0.0100. Latest state is tied overall (MAE 7.474 versus 7.497;
paired difference −0.01879 ± 0.05154), though worse in 2025 and 2026. Latest
finite-batch intervals cover 50.2/79.8/95.1% at nominal 50/80/95%; this does not
certify latent means of synthetic lineups. Haliburton's exact-2025 same-four
swap adds 2.75 points/100 versus McConnell, with +0.80 uncalibrated interaction
residual. `SESSION_HANDOFF.md` §15–18 records the complete checkpoint.

The Haliburton case must not become anecdotal tuning. Test a same-four lineup
swap, explain assist supply / assisted finishing / shot mix / turnovers, and
score 2025-26 Indiana using strictly preseason states on its observed rotation,
not as an unconditional preseason team forecast. Teammate on/off
effects are an evaluation target only, not known-pair input.

Data source/deployment caveat: Basketball Reference is the historical source
and publishes a 20-request/minute bot ceiling, which the new updater enforces.
Its current data-use terms require a permission/licensing decision before a
public product relies on an automated BRef feed.

The incumbent page is a benchmark, not the target architecture. It currently
uses 0.61/0.70 horizon-0 shrinkage, usage demand, known-pair residuals, and an
asserted coverage gate. `experiments/tool_model.py` is now its database-free
reference implementation and `tests/test_tool_model.py` protects its golden
outputs.

**2026-09-05 creation checkpoint:** `CREATION_EXPERIMENT.md` completes the
workload-versus-teammate-passing test, including a saved failed linear shot-mix
arm and a softmax probability repair. Supported: workload → shot mix;
passing → assisted-made share and a small turnover improvement. Not established:
passing → shooting efficiency or extra shot-mix signal beyond workload.
Coverage is 36.7% of player-possession exposure. Next run a genuinely matched
pre-origin additive/structural benchmark (same cells, target, calibration and
game splits), then test supported channel integration without double-counting
assists or breaking the finite miss/rebound ledger. Do not repeat the completed
screen, fit a named-creator bonus, or treat a changed assisted label as an extra
make. Thin-state coverage and real small-ball checks remain high priorities.

**Matched benchmark now complete:** `MATCHED_BENCHMARK.md` compares 5,774
identical future season-lineup cells. Additive/structural MAE 7.454/7.474 is
effectively tied in this sample; correlations 0.252/0.205 favor the additive
core in 10/11 origins. Novel-lineup and shared league-offset checks preserve
that distinction. Existing assist deficit does not improve the additive core.
Do not rerun this as an open task or assume a hybrid wins. Next inspect recurring
disagreements, then test supported role/turnover transport with coherent rebound
accounting against both fixed controls. Coverage and synthetic latent/OOD
uncertainty remain unfinished. The boundary audit is complete and immaterial.

**Disagreement review completed:** `DISAGREEMENT_AUDIT.md` and the full player/
channel ledgers in `reports/matched_disagreement_review.md` cover 258 cells with
>=500 possessions / 20 games. The top six gaps persist in chronological halves,
but most individual bootstrap ranges include zero. All six have zero assist
deficit. Across the whole screen, FTA is overpredicted by 4.87/100 (11/11 seasons)
and 3PA underpredicted by 3.16. Next discuss cases with Adam and audit this
opportunity/profile-transport bias before integrating more channels. Retain
same-five reversals and shooting variance; no named-player correction is earned.

**As-of-date foundation complete:** Adam approved date-aware league/player
updates and quarterly forward evaluation. `ASOF_MODEL_EXPERIMENT.md` records
the implementation and completed direct channel test (44 future windows,
26.31% matched coverage). Refreshing the same recency-weighted profile improves
3PA 11/11 seasons and TO modestly; the FTA bias survives. Updating only league
usage cannot change shot shares and worsens FGA/3PA. Next finish date-aware
league conversion/valuation and joint opportunity mix, then the quarter point
factorial with an equally refreshed additive model. Role adaptation and OOD
remain separate tests; no point-scorer or bandwidth promotion. 147 tests pass.

**2026-09-06 accounting follow-up complete:** `ASOF_ACCOUNTING_AUDIT.md` rules
out raw-ratio reconstruction/shrinkage as the main FTA explanation: bias
+3.351 → +3.348/100, and removing EB worsens 3PA/TO MAE 11/11 seasons. Keep EB.
Strict-date league conversion/valuation now exists and reproduces the old
no-decay helper. No point-model integration is claimed. A post-hoc common-cell
versus full-league FTA gap (20.36 versus 22.58/100, positive gap 11/11 seasons)
requires care about deployment/game-state populations, not an arbitrary offset.
Next jointly model opportunity shares with prior-only, comparable context,
then run the date-aware point factorial and equally fresh additive comparison.
192 tests pass; all audit jobs complete. Do not repeat the raw-count ablations.

**2026-09-06 deployment follow-up complete:** `ASOF_DEPLOYMENT_AUDIT.md`
reproduces every common cell. Full/common FTA 22.584/20.356; the full league
under common clock/score weights gives 21.394. Mix 1.190 and remainder 1.037
are descriptive, not causal corrections. Q1/Q3 account for 65.27% of common
exposure versus 50.13% league-wide; below-50 units already have much higher FTA.
`ASOF_OPPORTUNITY_EXPERIMENT.md` specifies (not yet implements/runs) the next
CSV-only prior-window four-way opportunity calibration control. Separate its
generic calibration gain from any later teammate-response gain. Then complete
the point factorial/equally fresh additive comparison. 245 tests pass; no jobs,
scorer promotion or source changes. Do not rerun the completed population audits.

**2026-09-06 opportunity calibration complete:** `ASOF_OPPORTUNITY_EXPERIMENT.md`
reports genuine prior-window calibration gains on the same cohort, not a new
interaction mechanism. Recent180 FTA MAE 6.366→5.195, 3PA 4.630→4.286 (both
11/11), with TO 2.483→2.491 worse10/11. Recent365 confirms the broad result.
Keep both raw and calibrated controls. Next substantive task: quarter point
factorial and equally fresh chemistry-free additive comparator; specify how
calibrated team channels feed player/location creation and making first.
No more aggregate FTA audits or post-hoc TO tuning. 278 tests pass; all jobs
finished; no scorer/HTML/source-data changes or OOD claim.

**2026-09-07 additive date foundation complete:** `ASOF_ADDITIVE_FOUNDATION.md`
records the strict-date additive helper and 318-test checkpoint. Prefix-only
normalization/prior fitting, short current-season blocks and completed-window
validation are implemented; a tiny real-cache fit passes future-mutation and
direct-loss checks. No tuned benchmark yet. Next specify prior-window penalty/
carry selection and matched league/calibration controls, then run the quarter
point factorial with explicit player/location opportunity accounting. The
three product standards and the accepted scorer/page are unchanged; no jobs.

**2026-09-07 quarterly additive pilot complete:** `ASOF_ADDITIVE_TUNING.md`
records matching-quarter prior selection and a 5,760-candidate 2026 Q3 pilot,
completed in 253.7s. The prior-penalty edge remains provisional (last RMS shift
0.004438 pts/100); no target-window score. 387 tests and independent artifact
checks pass. Next: documented 90-second one-axis sensitivity, then structural
player/location accounting and matched calibration for the quarter point
factorial. Do not repeat the completed pilot or launch the full sweep yet.
All jobs finished; source data, scorer and page unchanged.

**2026-09-07 additive sensitivity and point bridge complete:** the one-axis
follow-up is numerically immaterial at this origin (max0.000495pts/100); retain
prior=1 and preserve original flags. `ASOF_POINT_INTEGRATION.md` documents the
implemented category allocation and shared creation/making/assist-demand ledger.
Every saved common cell reconstructs, no exclusions. 446 tests pass, no jobs.
Next build the resumable quarter point runner with shared calibration/league
controls and per-origin checks; no new point result or scorer change yet.

---

## 0ab. State after the day session of 2026-09-03

**The 5-Shaq rule is met** and the tool now runs the `CURRENT_MODEL.md` spec.
Read `RESEARCH_OVERVIEW.md` §20–§23 for the reasoning; this is the state.

### The biggest lever of the day was already on disk
`fwd_prior_bio.csv` was written overnight by `run_idea1.sh` and never opened.
Height and position in the box-score prior are worth **+0.000043** forward on
the full stack (t=+3.88, 13/16) — larger than measured chemistry, floor
geometry and usage demand combined. The NUMERIC-position variant
(`which="box+posn"`, 4 columns instead of 21) reads +0.000037 at t=+6.33,
15/16, and confirms on a fresh baseline at +0.000027 (t=+3.63). **It ships.**
*Lesson: read the cache before running anything.*

### The 5-Shaq rule, settled
- It had been argued about in RAW-ADDITIVE units the page does not print.
  `tool_audit.py` reimplements `five.html`'s own arithmetic on its own data.
- **The failure is repetition, not excellence.** Five DISTINCT superstars price
  at +16.04 against a real maximum of +17.24; five Jokićs printed +26.26. The
  raw duplication curve is exactly linear in the number of copies.
- **No fitted structure can supply the fix, in principle** — lineups are
  selected on the outcome, so in range "unusual" correlates with "good" and
  every fit inherits that sign (§20.5). Four have now been tried and the two
  with clean forward signal both extrapolate the wrong way.
- The tool ships a **duplication gate**, disclosed as asserted. In-range cost
  measured on 18,071 real units: 1.00% move at all, mean |change| 0.0012
  pts/100. Five Jokićs now print +11.03, below the death lineup's +14.37.

### Shipped to the tool
prior + height/position; pairs at ≥50 (36,688 instead of 28,446); chemistry at
its own slope of 1.0 instead of the additive 0.447; usage demand; the
duplication gate. `tool/README.md` has the face-validity checks it must keep
passing.

### The result that changes what to work on next
**Half the "linear headroom" is an artefact of the random split.**
`additive_ceiling.py` has carried an unused `--esplit forward` flag since Phase
9. Same code, same data, only E moved to the chronological tail: the gap
between the best noise-free score and the best full-data fit is **+0.000262**
forward against **+0.000504** on a random split (which reproduces the published
+0.000499 to within 1%). And the two differ in KIND — forward, `noisefree`
peaks at an *interior* α ≈ 1000 instead of flattening as α→0, because removing
shrinkage removes shrinkage bias AND increases drift exposure. **The additive
ceiling as defined does not exist in the deployable regime.** So better
estimation of β is worth about half what the record says, and the levers that
fight drift keep their standing (`RESEARCH_OVERVIEW.md` §26).

### Two more that DID work
- **θ-recency is real and must not ship.** Ported into `fractional_eval`,
  nested, 16 matched origins: `base` +0.000169 (t=+7.30, 16/16), `all_nodelta`
  — the tool's configuration — **+0.000092 (t=+4.30)**, `all_cf` +0.000046,
  `all_delta` **−0.000022**. Perfectly monotone in how much current-season
  information the model already has: carry-forward, this-season δ and
  θ-recency are three routes to freshness and substitute almost exactly. It
  must NOT ship, and that is measured: on a full-corpus fit a 2-season
  half-life shrinks the career ratings of players last seen 2002–2007 to
  **0.441×** their flat spread against 0.708× for 2022–2025, while §27 says
  the true spread is flat across eras. §28.
- **Cross-era comparison is sound**, which the tool had been assuming. The true
  spread of player quality drifts 10% (offense) / 17% (defence) across 22
  seasons, less than the season-to-season swing, and half that once roster
  expansion is held fixed. §27.

### Seven things that did NOT work, all cleanly
| | |
|---|---|
| multiplicative usage conservation `I·(D̄/D−1)` | **−0.0000001 ± 0.0000034** over the demand hinges — a powered null |
| multi-lag carry-forward (lags 1–4) | −0.000002, t=−0.42, 10/16 origins identical |
| index curvature, OFFENSE | +0.000000, t=+0.59 — all of it is defensive, and wrong-signed |
| a role-dependent ridge penalty (usage axis) | τ² of the prior residual is flat in usage within a possession tercile |
| career-stage curve split guards/wings/bigs | **+0.000027 (t=+1.66) for the curve ALONE, −0.000017 (t=−2.11, 3/16) in the full stack** — a lever measured alone can reverse in the stack |
| selecting `a_gamma` instead of pinning it at 1e6 | null on every arm, negative on two. The pin was not costing anything |
| widening `a_career` up to 1e6 | −0.000009, t=−1.46, 0/16 better. My own inference from §26 and it was wrong: the ceiling rig's α shrinks θ toward zero, `a_career` shrinks θ−Zγ toward the prior |

### A methodological trap worth knowing
`forward_pairs --lam-cr` **defaulted** to a floor of 1e5 while the usage-demand
block wants 0–100. Run on the default, a +0.0000103 (t=+4.99) effect reads
+0.0000000 (t=+2.09). Every published run happened to pass an explicit widened
grid, so nothing on the record was damaged — but a default is invisible in both
the command line and the write-up. Default is now `[0, 1, 100, 1e4 … 1e10]`.
CLAUDE.md rules 12 and 13.

### THE DESIGN ON THE TABLE: `ROLE_MODEL.md`
Written at the end of 2026-09-03, nothing run. A role-assignment model —
aptitude, assignment, value at the assigned role — so a five of centres is
penalised because the model hands one of them 30% usage and prices a centre
there, rather than because a gate was bolted on. **Do §5 first**: four cheap
kill-tests, the most important being whether a player's value varies with his
assigned load at all. If it is flat the build is dead in an hour.

### TOP OPEN TOOL ITEM: the shipped shrink matches no horizon (§29.2)

The slope is a function of HORIZON — how stale the ratings are when used — and
the shipped 0.447 / 0.591 is a long-horizon offensive number beside a
short-horizon defensive one:

| raw slope | offense | defence | def/off |
|---|---|---|---|
| horizon 0 (contemporaneous, no drift) | 0.563 | 0.677 | 1.20 |
| horizon 1 (first season after the fit) | 0.605 | 0.615 | 1.02 |
| pooled 1–7 seasons | 0.476 | 0.509 | 1.07 |
| **shipped** | **0.447** | **0.591** | **1.32** |

The per-side asymmetry is an artefact of that mismatch, not a property of the
two sides. **The tool has no horizon** — it prices Jordan beside Curry — so the
defensible constant is the horizon-0 one, ~0.56 / ~0.68, which would raise the
page's offensive numbers ~26% and its defensive ones ~15%. A product decision:
it moves every number on the page.

### What to do next
1. **`--a-gamma` was pinned at 1e6 in every rig** and has never been selected.
   The prior is the most robust lever in the project and is now 36 dims a side
   rather than 32. `forward_eval --a-gamma` makes it a real grid; a run was in
   flight at the end of the session (`logs/agamma.log`,
   `experiments/cache/fwd_bionum_agamma.csv`). **Read it first.**
2. **Confirm the shipped prior at K=4** (45 origins) if more power is wanted;
   K=2 already confirms it at 13/16.
3. **Theta recency at fractional origins** was in flight at the end of the
   session (`logs/thl.log`, `experiments/cache/frac_k2_thl.csv`), matched
   against `frac_k2_bionum.csv` — check the `base` column is identical before
   reading it. Season-ahead the lever is +0.000019 (t=+1.89, 11/16) and §26
   says drift is most of what is left, so this is the best-motivated open lead.
4. **The five best DISTINCT defenders still print +19.66** against a real max
   of +17.24. The gate leaves them alone by design, because they are
   differentiated. Whether that is the right answer is a product question, and
   forcing it down needs a second free constant.
5. **Do NOT re-run** the multiplicative conservation column, multi-lag
   carry-forward, offensive index curvature, a usage-dependent ridge penalty,
   a position-split career-stage curve, an `a_gamma` sweep, or a wider
   `a_career`. All forward nulls, most of them powered.
6. `stats.nba.com` still returns 000, verified again 2026-09-03 with the
   sandbox disabled — so it is the host, not the environment. Tracking data
   remains the highest-value unavailable input.

---

## 0aa. State after the overnight session of 2026-09-02/03

Two things were asked: work the northstar, and follow up the joint-NN idea.
Both are answered, and the night's biggest single result is a **bug**.

### The headline: the sparse bilinear was a test-set leak
`forward_pairs` fed a per-POSSESSION mask indexed by `code` (cell ids) into the
top-k cell selection. That reads the mask at positions 0..n_cells-1 -- all from
2002-03, all inside every fit window -- so it returned 100% True and the cells
were chosen using 1.5M test-era possessions. Leaked +0.0000153 (t=+2.70);
**clean +0.0000008 (t=+0.23)**. 95% of the project's live lead. Fixed; rule
recorded in `feedback_cell_vs_possession_mask.md`. **The fit and the scoring
were both clean -- only the BASIS SELECTION was contaminated, which is why
"is this forward?" passed.**

### The staleness caveat is discharged
`slice_horizon.py` holds one fit constant and scores the test season in
quarters: a composition effect is flat in the slice index, a drift-absorber
rises. Every block, against the arithmetic pure-staleness benchmark:

| block | gain | sem from 0 | sem from pure staleness |
|---|---|---|---|
| free pairs (off) | +0.0000279 | 0.4 | **5.0** |
| usage demand (off) | +0.0000075 | −0.0 | **8.3** |
| floor geometry (off) | +0.0000094 | −0.8 | **3.7** |
| **coverage (DEF)** | +0.0000049 | 1.7 | **0.0** |

`fractional_pairs.py` is the deployable version -- fits through slice j-1 of
the test season and scores slice j, 48 origins at ~20s each.

### Two new blocks, one useful and one not
- **Floor geometry** (shot-map diversity), offense: +0.000010, t=+3.37, 15/16;
  jointly with usage demand +0.000020, t=+5.13, exactly additive. Placebo
  clean, interiority proven twice, staleness excluded. **But 3 of 5
  pre-registered signs are inverted, the predictive content is entirely in the
  inverted columns (concentration alone: t=−0.46), and extrapolated it hands
  five copies of anyone a POSITIVE adjustment.** Predicts; unusable for the
  rule. Also absorbed entirely by a (leaked) lineup-minutes control.
- **Defensive coverage** (height/position spread): +0.000005, t=+1.93 on
  points and +0.000017, t=+2.75 on the shot channel. 6/6 marginal signs as
  pre-registered, placebo clean, and five copies of anyone gets +1.16 pts/100
  allowed. **But it is the one block that fails the staleness test.**

### The 5-Shaq rule is a product decision, not a research problem
`five_shaq_audit.py`: real lineups run p1 −8.8, p50 +7.1, max ever +30.2
pts/100. The additive model puts **five LeBrons at +49.6**. Every measured
block combined moves that by **at most 2.6**. And `distance_shrink.py` shows
the calibration slope does NOT decay with Mahalanobis distance (every arm
loses; trend +0.026, flat-to-rising), so Route B cannot be fitted either.
Eval only reaches d≈12 while five Shaqs is 20.9, so no experiment on this
corpus can do better. **Pick a bounded schedule by judgement and disclose it.**
Note five Shaqs (+24.8) is INSIDE the real range -- the corpus starts in 2002
and those are his decline years. Use five LeBrons.

### The joint-NN question is answered, in both halves
- SELF (quadratic prior, 528 extra columns/side, fitted jointly by the exact
  Schur solve): **−0.0000022 ± 0.0000047**, CI excluding the effects that work.
- RFF (128 random Fourier features spanning sum AND |difference|, output layer
  solved jointly with the player block): **−0.000007 ± 0.000007**.
- With CROSS already null, all three profile-based nonlinear routes are closed.
  The remaining route is new INPUTS, not a richer function of these.

### Also settled
- Era-adjusting the profile HURTS: prior +0.000175 → +0.000094. Read the
  half-life runs against the ERA run, not flat -- `profile_matrix` sets
  `era=True` whenever a half-life is given.

### Idea 1 (recency-weighted profiles) works, once unbundled
`profile_matrix` set `era=True` whenever a half-life was given, so every
half-life number ever measured was era-plus-decay, and the two point opposite
ways. `zscore=False` separates them. Paired per origin against the flat career
profile, on the PRIOR lever: era alone −0.000081 (0/16); decay alone +0.000005,
+0.000030, +0.000059, **+0.000068**, +0.000064 at half-lives 3, 1.5, 0.75,
**0.4**, 0.25 — an INTERIOR optimum, t=+3.47, 14/16, a 39% gain on the prior
lever. The full stack does not gain (`all_cf` crosses zero but never becomes
significant), because carry-forward was already doing the recency job.

### What the tool should print
Four arms deep, additive → player → usage demand → demand + free pairs:

| baseline | demand over player | pairs over demand |
|---|---|---|
| static fresh | +0.000007, t=+4.03 | **+0.000025, t=+2.48** |
| fresh + this season's δ | +0.000006, t=+2.48 | **−0.000004, t=−0.49** |

Chemistry is worth printing only when the model does not already know current
form. The tool prices hypothetical lineups from career ratings and has no δ for
a five that never played, so the static row is the relevant one and chemistry
belongs on the page.

### What to do next
0. **Read `logs/frac_recency.log`** — fractional_eval at K=2 with the flat
   profile against the 0.4 half-life one, matched flags. Asks whether the
   better prior helps the DEPLOYABLE model, which the season-ahead rig said it
   does not. Launched at the end of the session; may be partial.
1. **Decide the 5-Shaq schedule as a product question.** It cannot be
   measured. A bounded shrink toward the league mean, disclosed on the page,
   is the whole of Route B.
2. **Resolve defensive coverage.** The fresh-baseline run (`fractional_pairs
   --side def --coverage --slices 4`) is the decisive test: if it survives a
   baseline that is at most a quarter-season stale, the slice test merely
   lacked power; if it dies, it was drift.
3. **Do NOT re-run** the profile bilinear at any width or sparsity, the
   quadratic prior, or an RFF pair function. All powered forward nulls.

---

## 0a. State after the Phase 13 session (2026-09-02, afternoon)

Triggered by a contradiction: the user had been told both that the tool carried
a valuable generalizing chemistry component worth a few points per 100, and
that no non-additive component generalizes. **Both were half-true.** The
distinction nobody had drawn is that an unseen LINEUP is not an unseen PAIR --
`RESEARCH_OVERVIEW.md` §13.

### What is now known
| | |
|---|---|
| free pairs on NOVEL five-man sets | +0.000017, t=+4.00, 13/15 -- they DO generalize to unseen lineups |
| but only 4.1% of possible pairs have shared a floor | a random five from the tool has **0.43/10** pairs known; **65.5%** have none |
| profile bilinear forward, 26 dims, 15 origins | **-0.000001 +- 0.000005** -- a POWERED null whose CI excludes +0.000030 |
| same on 10 dims, same rig | -0.000005 +- 0.000007 (reproduces the known `forward_synergy` null) |
| predicting a pair effect, matched flags | ~2.5% of true variance, **identical at 10 and 26 dims**; net of its additive control ~1.3% = 0.07 pts/100 |
| diminishing returns to stacking scorers | null on the clean split; the forward-only curvature flips sign between splits |
| lineup composition (ord / disp / counts / size) | nothing reaches t=2 |
| theta x teammate profile | +0.000002, t=+0.20, placebo clean |
| chemistry calibration slope, forward | **+1.111** -- the tool's single 0.447 UNDER-shows chemistry ~2x |

### Two tool changes this implies (NOT yet made -- they change the published page)
1. **Give chemistry its own slope.** `five.html` does `(oAdd + chemistry) * 0.447`.
   The additive part earns that shrink; chemistry earns ~1.0.
2. **Export pairs at >=50 shared possessions, not 200** -- 50 is what the
   forward-validated model uses. Coverage 0.43 -> 0.54 of ten pairs known,
   zero-history lineups 65.5% -> 58.4%.

### THE 5-SHAQ RULE — the new northstar requirement (added 2026-09-02)
The tool must not return "best lineup of all time" for five Shaqs, and must
extrapolate gracefully to ALL unseen lineups. `CLAUDE.md` has the statement;
`RESEARCH_OVERVIEW.md` §13.10 has the measurement. Three routes, in the order
they were tried:

- **A. Conservation laws — TESTED, does not separate the case.** Usage is the
  cleanest: one ball, five shares summing to 100%, and the additive model lets
  every player keep his own usage. The hinge in unserved demand is real in
  range (+0.000021, t=+2.88 over a 26-dim profile LIN+SELF control, placebo
  −0.000000) and is being tested forward. But D = Σ career usage is **1.590 for
  five Shaqs against a real-lineup max of 1.631** — five Currys is 1.605. Usage
  is not what is wrong with five Shaqs. Keep the hinge if it survives forward;
  it does not satisfy the rule.
- **B. Distance-aware shrinkage — achievable, satisfies the LETTER.** Shrink
  toward the league mean as a function of Mahalanobis distance from the support,
  as a GP does. Guarantees no absurd number; returns ≈league average with a wide
  bar; knows nothing about *why*. Build it as the safety net regardless.
- **C. One theory-named interaction — satisfies the SPIRIT, and is the bet.**
  What is actually wrong with five Shaqs is nameable: no spacing, nobody to
  initiate, nobody who can guard a guard. The spacing mechanism — *a player's
  rim efficiency depends on his teammates' outside shooting* — IS estimable in
  range, because real lineups vary in how much shooting they carry. Generic
  interaction searches all failed; a single named interaction measured on the
  CHANNEL where it should appear (shot-making, not points, which is ~76% noise)
  is a different and far better-powered question. Then extrapolate the fitted
  slope, which is a disciplined extrapolation rather than a guess.

### TOP OF THE LIST: re-grade every interaction against a FRESH baseline
`forward_pairs` scores a WHOLE season from a model fitted through T-1, so the
additive baseline is an off-season stale by the first game and nearly two
seasons stale by the last. An interaction block on top of that can score by
absorbing staleness rather than composition — and the sparse-bilinear effect
decays exactly as that predicts (2010:+29, 2011:+48, 2012:+43 … 2019:−29,
2020:+3, in 1e-6). `fractional_eval` already has the slice machinery; port the
block builders (`cross`, `demand`, `named`, `rff`, pair, continuity) into it so
each is scored against a baseline at most a quarter-season stale, and difference
the two readings. This does not just add a result — it re-grades every
interaction number in Phase 13.

### Open, raised by Phase 13
- **The global calibration slope disagrees between two estimators.**
  `calibration_by_information` reads +0.742 offense / +0.440 defence
  (per-possession regression of the outcome on the additive index, plain EB
  ridge, 70/30 forward). `lineup_uncertainty.json` ships 0.447 / 0.591
  (lineup-level calibration against estimated true quality, full additive
  stack). Different estimators, but this number multiplies every rating the
  tool prints, so the 1.7x gap should be resolved. Settle it by measuring both
  on the SAME model and the SAME split.
- **Two of the ten `DEFAULT_DIMS` are dead weight** on offense once the others
  are present: `rblk` (-0.07%) and `assisted` (-0.31%) leave-one-out. That set
  drives the bilinear, which is now null anyway, but if it is reused, prune it.

### Do not re-run
- A wider profile bilinear, on any width, on either target. Powered null.
- Order statistics / dispersion / threshold counts of the profile, and height
  and position, as interaction bases.
- Curvature or concentration in the lineup index.
- **`basis_screen`'s forward split.** It fits the basis on the additive model's
  IN-SAMPLE residual, which un-shrinks it; the base r2 comes back NEGATIVE and
  every arm scores for undoing it. Use `forward_pairs` arms instead.
- The era-restricted variant in `run_generalizing_screen`: restricting the
  basis fit but not the eval set drives the base to -0.001 and is meaningless.

---

## 0. State after the overnight Phase 12 session (2026-09-02)

**Nothing is running.** Logs in `logs/`, results in `experiments/cache/`, all
committed. Read `RESEARCH_OVERVIEW.md` §12 for the narrative.

### The two things that worked

| | result |
|---|---|
| **free teammate pairs, forward** (`forward_pairs.py`) | **+0.000030** r², t=+3.64, **15/16 seasons**; +0.000015 on novel fives. ~16% of the forecastable ceiling. The FIRST non-additive structure to survive a forward test. Offense only. |
| **mid-season δ** (`intraseason_eval.py`) | **+0.000090**, t=+5.97, 13/15, where season-ahead it is exactly 0.000000. Best deployable number in any regime: **+0.002114**. |

### The nine things that did not

| question | module | answer |
|---|---|---|
| profile bilinear, forward, both targets | `forward_synergy.py` | +0.000005 each — **null** |
| can anything PREDICT a pair effect? | `pair_predictability.py` | **no** — ~1% of true variance from box-score profiles, half of it additive; bilinear 0.1%, archetypes 0.07% |
| does the low-noise channel give better pairs? | `pair_channel.py` | **no** — shots is −0.000013 WORSE than points |
| defensive chemistry | `forward_pairs.py` | null on points (+0.000003) and on shots once bolted to a good baseline |
| per-lineup error bars | `lineup_uncertainty.py` | measured, **not shipped** — posterior sd varies only 1.3× and orders calibration backwards |
| free triples | `forward_pairs.py --triples` | +0.000000 at 4.5× runtime |
| rest / back-to-backs | `schedule_bias.py` | ratings move 0.7% of their spread. (Keep: fatigue hurts defence ~2× more than offence.) |
| recency-weighting the pair block | `forward_pairs.py --halflife` | **−0.000000**. Pairs drift (31% persistent) but the drift is unexploitable. |
| off×def matchups | `matchup_reliability.py` | **noise floor** — reliability +0.02 vs +0.25 for teammate pairs, half of it team-vs-team |

### Shipped
`tool/five.html`, republished to the existing URL and verified live: 28,446
measured pairs replacing the 10×10 quadratic, honest zero plus a visible count
for pairs with no shared history, and a per-side shrink re-measured forward on
this model (0.447 off / 0.591 def).

### Two methodological rules earned, now CLAUDE.md 9 and 10
- **Refit the upstream model inside the split.** One global additive fit biased
  pair reliability from 0.25 down to 0.08, and to −0.14 with per-season δ on.
- **A control arm on a grid boundary is not a control.** It inflated the
  shots-channel pair result 2× on all four configs. Prove interiority by
  widening the grid TWICE.

**Closed this session:** all of §1, plus §2.2, §3.1, §3.4, §3.5, §4.2.

## 1. Highest value — do these first

Everything that was in this section on 2026-09-01 is now closed; the answers are
in §6b. What follows is what those answers point at.

### 1.1 Tracking-derived aggregates — now unambiguously the top item
The tool prices lineups that never played. Free pairs are worth +0.000030
forward but only for duos with shared-floor history, and **nothing predicts a
pair effect from box-score profiles** — the ceiling is ~1% of its true variance,
and gradient boosting says that is a feature problem, not a functional-form one
(§6b). So the route to pricing a novel pair is better FEATURES, and the obvious
ones exist and are public:

- **potential assists** — passes leading to a shot attempt, made or missed. This
  is the Luka problem solved by measurement instead of algebra: playmaking with
  the teammate-finishing dependence removed at source.
- **screen assists** — pick-and-roll, directly.
- **opponent FG% at the rim while defending** — rim protection.
- drives, touches, contested shots, catch-and-shoot vs pull-up.

`stats.nba.com` returns **000** from the agent sandbox while
basketball-reference and api.github.com both return 200 — verified 2026-09-02,
so it is that host specifically, not a network block.

**The fetch is written and waiting for you:**

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.fetch_tracking
```

78 requests, about 6 minutes, one every 5s, every response cached to
`experiments/cache/tracking/` and never re-fetched, so an interruption is
resumable. Pulls Passing (potential assists), Drives, CatchShoot, PullUpShot,
Defense (opponent rim FG%) and Rebounding, 2013-14 onward.

Coverage starts 2013-14, so it implies a modern-era model — which
`era_is_the_additive_fit` says is the right window for interaction signal
anyway.

**Test it with the rig that already exists:** `pair_predictability.py` scores any
feature set against the measured pair effects out-of-fold in about a minute.
Anything that reaches even 10% where box-score profiles reach 1% would roughly
double what the tool can say about a five that has never played.

### 1.2 A mid-season mode for the tool — a product decision, not a research one
`intraseason_eval.py` settled the research: with the current season's first half
in the fit, this season's δ is worth **+0.000090** (t=+5.97, 13/15) and the
model reaches **+0.002114**, the best in any regime. The tool ships career
ratings only. Adding a "current form" mode is now a design question — what it
should say for a retired player, whether it is the default — and that is the
user's call.

### 1.3 Does adding folds actually buy power? (was §2.1)
Every marginal result in this project lives at 2–4 sem, and tonight produced
several. Split each test season's possessions in half at random and score each
half: spread between halves is test sampling noise, residual between-season
spread is genuine heterogeneity. **If test noise dominates, more origins help;
if season heterogeneity dominates, they do not** and the answer is paired
designs and sign tests. Cheap, and it would price every future experiment.

## 2. Evaluation design

### 2.1 Variance decomposition — PROMOTED, see §1.3
Split each test season's possessions in half at random and score each half.
Spread between halves = test sampling noise; residual between-season spread =
genuine heterogeneity. **If test noise dominates, more folds help; if season
heterogeneity dominates, they don't** and the answer is paired designs and sign
tests (already the workhorses: the experience fix is t=2.03 but 16/16 seasons,
sign-test p≈1.5e-5).

### 2.2 CLOSED (positive) — mid-season, δ comes back
`intraseason_eval.py`, 15 origins: fit seasons < T plus the first half of T,
score T's second half. **This season's δ is worth +0.000090 (t=+5.97, 13/15)**
where season-ahead it is exactly 0.000000. And carry-forward flips the other
way — worth +0.000115 season-ahead, exactly 0 here, because the current partial
season supersedes last season's deviation. Best deployable number in any
regime: **+0.002114**.

Follow-up worth doing: the tool ships career ratings only. A mid-season mode
would use this-season δ. That is a product decision, not a research one.

### 2.3 Strict detrend — the flag DOES NOT EXIST
Corrected 2026-09-02: `forward_eval.py`'s docstring promised a
`--strict-detrend` option and no such option was ever written. The docstring now
says so.

What is actually at stake is narrower than it looks. Every arm is scored against
the same target, so a **contrast** between two arms is untouched by how the
target was detrended — which means every finding in this repo, all of which are
contrasts, is safe. What a global detrend can move is the **levels**: r2 is
measured after season T's own (season, week) means have been removed, which
removes noise the model would otherwise be unable to predict.

Implementing it means refitting the detrender per origin, which means rebuilding
the Gram blocks per origin — the one thing `forward_eval` is designed to avoid
(~25s x 16 origins, so ~7 minutes, not prohibitive). Worth doing before any
LEVEL is quoted outside this project; not worth doing to protect a contrast.

### 2.4 Deployment control in the channel/scheme rigs
`channel_ceiling.py` uses `min_poss=10` and **no deployment control** (score
margin, garbage time). `lineup_variance.py` has `control="margin"` and
`control="pseason"`. The 85–93% player-attributable figure controls for
team-season but not deployment. Re-run with the margin control to close it.

---

## 3. Model structure

### 3.1 CLOSED — off×def matchups are at the noise floor
`matchup_reliability.py` measures the ceiling instead of fitting the model.
Split-half reliability of a free (off i, def j) matchup effect is **+0.009 to
+0.021** with a team-matchup control, against **+0.250** for same-side teammate
pairs measured identically — 12–25× weaker, and about half the raw correlation
was team-vs-team (division rivals meet four times a season). The estimated true
sd falls as the possession threshold rises, the signature of noise rather than
signal. Nothing for an architecture to find; do not build the cross block.

### 3.2 MOSTLY ANSWERED — defence on the shots channel
`ceiling_decomposition`: defensive free pairs are **0%** of their ceiling on
points, versus 15% for offense; 47% of defensive non-additivity is team-season
scheme. But the new scheme decomposition says only **7%** on the shots channel.
**Reconciled, mostly.** Forward, defensive free pairs are null on points
(+0.000003) and null again on shots once the pair block is bolted to a good
points baseline (§6b §1.2/§1.3). So `ceiling_decomposition`'s "0% of their
ceiling" stands. What is still unreconciled is the 47% vs 7% scheme share
between `lineup_variance` and the channel decomposition — different rigs,
controls and targets, and nothing now depends on it.

### 3.3 Weighted matrix completion of Θ — much less promising than it was
"Pair effects are not low-rank" is self-caveated: Θ is structurally zero for the
97.6% of pairs that never played, biasing its spectrum toward high rank by
construction. A proper weighted completion (fit only observed entries) was never tried, and
strictly it is still open. But two results from 2026-09-02 make it a long shot:
a pair coefficient is only **25% reliable** even on the full sample, so a
low-rank fit would mostly be fitting noise; and nothing — including a
nonparametric model — predicts a pair effect from anything observable. Do this
only if §1.1 lands.

### 3.4 CLOSED — free triples add nothing
Screened on one origin (2024, points): +0.000000 overall and +0.000003 on novel
fives, at 4.5x the runtime (201s vs 44s per origin). Not conclusive at one
origin, but the cost/benefit does not justify five hours of compute, and §6b
gives an independent reason to doubt it: if PAIR effects are only 25% reliable
and unpredictable from features, triples are worse on both counts.


### 3.5 CLOSED — archetype × archetype is dead
`pair_predictability.py` scored archetype-pair dummies at K = 6, 10, 16, 24
against the measured pair effects, out of fold: **0.07%** of a pair effect's true
variance, indistinguishable from the permuted-feature placebo and worse than a
ten-parameter linear form. Clustering players into roles does not recover pair
chemistry, which is consistent with it being idiosyncratic to particular people.


### 3.6 Aging curve refinements
Settled: true debut beats observed (+0.000083, 16/16); age ≈ experience; bins
beat splines. Open:
- **CLOSED — why 9 bins beat a smooth spline.** The curve has THREE regimes:
  a sharp rookie jump (+0.696, 2.9x the median later step), a flat plateau from
  year 3 to year 10, and a steep collapse (−0.750 then −1.091). No low-order
  spline represents jump + plateau + collapse at once. Two discontinuities, not
  one, and they are at opposite ends.
- **Age × position/height** — bigs and guards almost certainly age differently.
  `roster_dims` has height and position; `player_bio` now has age.

---

## 4. Data

### 4.1 Tracking-derived aggregates — PROMOTED, see §1.1
Raw tracking is not public; **derived aggregates are**, and several attack our
exact problems:
- **potential assists** — passes leading to a shot attempt, made or missed.
  This is the Luka problem solved by measurement rather than by algebra: it
  measures playmaking with the teammate-finishing dependence removed at source.
- **opponent FG% at the rim while defending** — direct rim protection, the
  defensive shot-selection channel.
- drives, touches, contested shots, **screen assists** (pick-and-roll!),
  catch-and-shoot vs pull-up splits — these encode exactly the role
  distinctions the 10 box-score dims cannot.

`stats.nba.com` is **blocked from the sandbox** (`000`); basketball-reference
is reachable (200). Needs the user to run the fetch or lift the sandbox.
Covers 2013+ only, so it implies a modern-era model.

### 4.2 CLOSED — rest and back-to-backs do not bias the ratings
`schedule.py` + `schedule_bias.py`. Removing 12 schedule columns from the target
and refitting moves the ratings by 0.014 pts/100 against a spread of 2.0
(corr 0.99998); the schedule explains 0.0022% of the target's variance, and as
an r2 lever it reads -0.000012 over 2 origins. Every player on a team shares
that team's schedule, so there is nothing to de-bias.

KEEP the descriptive finding: relative to the modal one-day-off game, a
back-to-back costs the OFFENSE 0.60 points per 100 and the DEFENCE 1.08 — about
2:1. A tired team still runs its offense; it stops guarding.

### 4.3 `nba.players` is thin
id / name / position / height only — no birth date, no debut. `player_bio.csv`
now supplies debut + birth date for 98.8% of players from the BBR index. Worth
folding into the database rather than a CSV.

---

## 5. Observations worth chasing

1. **CLOSED — aging is shot-MAKING, not shot creation.** `aging_readout.py`
   prints the curve by channel: a rookie creates shots at a league-average rate
   (**+0.033**) and cannot finish them (**−0.793**), so the entire rookie
   offensive deficit is finishing. Aging out is both, with creation collapsing
   only after year ten. Defence ages the other way and never goes negative — a
   14th+ defender posts his best shot-selection number of any stage.
2. **CLOSED — carrying δ forward does TWO jobs.** `delta_decompose.py`: the
   optimal carry weight is **+0.157** when θ is fitted on the full corpus and
   **+0.500** when θ is fitted only on seasons < T, which is what a forecast
   must do. A stale θ leaves δ_{T-1} carrying both the recency signal and a
   correction to an out-of-date career coefficient. The AR(1) on fitted δs is
   only +0.049 and the "standing" share only 6.2% — both measured after a
   full-corpus θ has eaten the standing part. 0.31 and 0.6 were never the same
   quantity.

   **Followed up, and it is SUGGESTIVE ONLY.** `theta_recency.py` weights each
   season's Gram block by 0.5^(age/halflife) — free, since X'X is block diagonal
   by season. 16 origins: **+0.000019, t=1.89, 11/16** (p≈0.11). The mechanism
   test passes directionally (chosen ρ falls from 0.6-in-13-seasons to
   0.6-in-9), but t=1.89 is screening, not a result. Not shipped. To settle it
   needs a more powerful paired design, not more origins — 16 is the corpus.
3. **The additive/non-additive dichotomy may be exactly complementary.**
   Additive value: 92% recoverable from shot-making, 45% from shot-selection.
   Non-additive: shot-selection persists 66–82%, shot-making −3%. Is this a
   coincidence or a structural fact?
4. **CROSS season-to-season variance is enormous** (+0.000080 in 2010,
   −0.000088 in 2012). Era/regime effect, or just noise? `era_is_the_additive_fit`
   suggests the former.
5. **LIN+SELF adds +0.000341 against a minimal baseline but +0.000020 against
   the full stack.** A clean measurement of how much of the profile's linear
   value the prior already captures.
6. **The bilinear reaches 1% of the ceiling but is the only interaction model
   with a harness t-stat.** Small enough to estimate, too small to be right.
   Cautionary tale about what "significant" selects for.

---

## 6b. Closed this session — the answers §1 used to ask for

### 1.1 CLOSED (negative) — a pair effect is not predictable from profiles
`pair_predictability.py`, out of fold over pairs, three seeds. Reliability of a
pair coefficient is 0.18–0.20; the best any function of the ten box-score dims
reaches is ~1% of a pair effect's TRUE variance, and an additive control
(`sum only`) takes 0.47% of that. The bilinear is 0.1%; archetype x archetype
is 0.07%; gradient boosting bounds smooth functions of these features at ~1%.
Placebos read ~0.

So `pair_effect(i,j) = f(z_i,z_j) + deviation` cannot work with `f` on box-score
profiles: it is bounded at ~1% of an effect that is itself +0.000030. The tool
is right to contribute zero for a pair with no history and say so.

**The only route left is richer features, not a better f** — see §4.1. That
makes tracking-derived aggregates the highest-value item in this file.

### 1.2 CLOSED — the shots channel does NOT give better pair estimates
`pair_channel.py`, 16 origins, additive baseline held fixed at the good points
model, only the estimation channel for the pair coefficients varying:

| | offense | defence |
|---|---|---|
| pairs from points | **+0.000030** (t=+3.64, 15/16) | +0.000001 (t=+0.16) |
| pairs from shots | +0.000017 (t=+2.30, 10/16) | +0.000001 (t=+0.14) |
| shots over points, paired | **−0.000013** (t=−1.73, 3/16) | −0.000000 |

The apparent doubling in `forward_pairs` was the weaker BASELINE, not the
channel: a shots-fit additive model is +0.000705 against +0.001701, so its
residual leaves more for any block to find. Deployable configuration is the
simple one, and it shipped.

### 1.3 CLOSED — defensive chemistry is not shippable
Null on points (+0.000003, t=+0.81) and null on shots once bolted onto the good
additive model (+0.000001, t=+0.14). The tool claims no defensive chemistry, and
that is correct. Reopen only if §1.1 finds an `f` that predicts pair effects,
since a predicted defensive pair effect is a different estimator from a measured
one.

### 1.4 CLOSED (negative) — recency-weighting the pair block gains nothing
Pair chemistry IS only 31% persistent across a decade, but sweeping a half-life
(0/2/4/8 seasons) on validation over 16 origins gives a paired difference of
**-0.000000** (sem 0.000003, 7/16). Down-weighting old possessions buys a more
current estimate and pays for it in sample size; the pairs that drifted most are
the ones without enough recent data to re-measure, and the two cancel.

Validation picked a decay in 10/16 seasons and was wrong every time — a clean
illustration of the validation noise floor at 1e-5 effect sizes.

If pair recency is revisited it needs a different mechanism than reweighting:
an explicit per-(pair, season) deviation with its own penalty, which is the
intra-season idea (§2.2) one level up.


## 6. Closed — do not re-run

- **Phase 5 architecture search** (attention, two-stream, FM, embeddings) —
  fully explained by `pair_effects_not_lowrank`: rank ~256 needed, rank 8 gives
  zero on novel lineups. No embedding can find it.
- **Prior shape**: heavy tails, position, season-specific profiles — all null.
- **Teammate-context deconfounding** — both directions null forward
  (subtract +0.000001; add +0.000011 ± 0.000015, 8/16 seasons). The
  *measurement* stands (placebo-clean, `rast ← assisted` +0.040 t=3.60); the
  forecasting payoff does not.
- **Time-varying δ as fitted** — exactly zero forward. Use carry-forward.
- **Age vs experience** — a tie. **Splines vs bins** — bins win.
- **20 profile dims** — null; keep 10.

---

## 7. Process (every one of these cost real time)

- **`pgrep -f PATTERN` waiters self-match** — the waiter's own command line
  contains the pattern. Hit **three times** in one session. Wait on a PID
  (`while kill -0 $PID`), or put the waiter in a file.
- **Never launch and wait in the same command** — the tool timeout SIGTERMs the
  process group and `& disown` does not save it. Killed a job this way once.
- **Always arm a watcher immediately** — a completed queue sat unnoticed for
  three hours because a watcher was never re-armed after the previous one fired.
- **Waiters fire early on a just-launched process.** `while kill -0 $PID` returns
  immediately if the shell has not yet exec'd the interpreter; wait on a
  SENTINEL IN THE LOG (`until grep -q "wrote ..."`), which also survives the
  process dying. Cost several wasted round trips tonight.
- **A background monitor reported a result block that was never in the log.**
  It named a summary for a config that had been running 60 seconds and could not
  have finished. Verified against the CSV on disk — the real numbers were
  nothing like it — and stopped the monitor. Trust files, not the event stream.
- **Logs go to `logs/` in the repo** (gitignored), not only the scratchpad —
  `/private/tmp` has been wiped before and took the tool's source with it.
  Mirroring the log is what caught the `--target shots` bug on the first origin,
  before four hours of compute went into a mislabelled run.

---

## 0ae. Joint capability v5 — the input route is closed, 2026-09-11 (Opus)

Read `reports/joint_capability_v5_review.md`, `V5_PHASE0_FINDINGS.md` and
`JOINT_CAPABILITY_LEARNINGS.md`. Run
`experiments/cache/joint_capability_2026_09_10_v5/`, 384 arm-origins verified.

### Do not re-run

- **Feeding the joint-capability model more inputs.** Six ways were tried at a
  frozen architecture — opponent-deconfounded states, height/position,
  offensive rebounding as a 19th coordinate and sixth loss family, the 46
  otherwise-unused features routed into the message, all four together, and
  points-leverage family weighting. Every arm-minus-BASE MAE estimate is
  positive on both slices; BASE has the best novel MAE, RMSE and r² of eight
  arms. ALL is the exact sum of its parts, so there is no combination left to
  find.
- **Points-leverage family weighting.** Established WORSE on novel lineups
  (MAE +0.05244 [+0.00327, +0.10161], 1/10) and it did not move conversion.
- **λ other than .01 for this architecture.** Both directions are now
  established worse on novel lineups from independent runs: .0001 in v4
  (+0.03233 [+0.00912, +0.05554]) and .1 in v5 (+0.02636 [+0.00084, +0.05187]).
  It is an interior optimum; stop sweeping it.
- **An extra over-dispersion shrink on the point predictions.** The
  league-centered out-of-sample slopes are 0.94–1.02, not 0.79; the oracle
  shrink buys ≤0.007 MAE and nothing for the additive, and the deployable
  prior-only version makes EVERY arm worse (+0.008 to +0.019 MAE) because the
  per-origin estimate swings 0.82–1.21. The §0ad item 4 claim does not transfer.
- **ORB budget feedback / variable pace as an accuracy lever.** Real five-man
  units vary in opportunity budget with sd 4.261 per 100 against the model's
  0.204, but that variation explains **0.18%** of offensive-rating variance and
  is worth ≤0.008 pts/100. Estimate rebounding if it is wanted for its own sake,
  not to move the score.
- **Fitting the opponent adjustment across players.** The slopes come out
  negative on the make logits: schedule-faced encodes team identity, not
  inflation. Player fixed effects are required. (The corrected, within-player
  version works mechanically — 36% of the asymmetry removed — and is still worth
  only 0.0024 RMSE.)

### Open, in the order I would take them

1. **Fixture magnitudes at validated scale.** Five Gobert clones move 193–228%
   of the largest context effect the model produces on any real lineup, across
   v3, v4 and v5. The sign and ordering are the achievement; the level is
   unevidenced and is quoted as a result. Well powered, unaddressed.
2. **A support measure with dynamic range.** Real cells span composition
   distance 0.515–3.105 and five Goberts scores 3.191 — 3% beyond the real
   maximum, where the older Mahalanobis scale put five Shaqs at 1.8×. Until the
   measure separates degenerate lineups, "composition distance does not help"
   is a statement about the measure, not the idea. Blocks the uncertainty pillar.
3. **Conversion.** Five consecutive versions, largest v5 change 5.0e-5 of FG
   Brier, while §10's shot-quality effect forecasts 12/12 seasons over 2.66M
   attempts. Either the architecture cannot reach it or the loss cannot see it;
   nobody has separated those.
4. **A holdout with power, or a lower-noise evaluation.** 428 cells could not
   adjudicate 0.03 MAE. Either reserve more, or move the decision to a
   population that resolves what we are arguing about.

---

## 0af. Joint capability v6 — extrapolation measured, 2026-09-11 (Opus)

Read `reports/joint_capability_v6_review.md` and `V6_PHASE0_FINDINGS.md`. Run
`experiments/cache/joint_capability_2026_09_11_v6/`, 240 arm-origins verified.

### Do not re-run

- **Withholding the unusual quartile of lineups from training, at p75.** It is
  free: HOLD75 has the best withheld-region MAE of five arms, beats FULL there
  (−0.0079), is within 0.001 MAE of FULL overall on a quarter less data, and its
  five-clone ratings correlate r = 0.9966 with FULL's donor by donor. There is
  no gradient with distance. Do not re-measure this; measure further OUT.
- **Comparing HOLD against RAND in a single region.** An arm trained only inside
  the support beats its partner there by construction (−0.0241, specialisation).
  Only the difference-in-differences is interpretable.
- **Matching a random control on exposure alone.** It hands the control ~4% more
  distinct lineups, a composition-diversity advantage. Stratify on the row-size
  distribution; `joint_capability_v6_data.assert_matched` enforces it.

### Open, in the order I would take them

1. **Push the holdout to the range that matters.** v6 validated extrapolation
   across the observed range: 99.5% of withheld cells sit at or below the clean
   real maximum of 10.31. The fixtures the tool must survive are at 1.81x (five
   copies of a p99 player) and 3.02x. Withhold by DONOR EXTREMITY rather than by
   lineup quantile — train without ever seeing the players whose five-copy
   lineups sit furthest out, then price those clones. Same machinery, and it is
   the difference between "it extrapolates" and "it extrapolates far enough to
   replace the coverage gate."
2. **The difference-in-differences.** +0.0191 ± 0.0138 at 7/11 is the one number
   leaning against v6's headline. Worth resolving with more seasons or a
   lower-noise population rather than leaving at 1.4 sem.
3. **Conversion, still.** Six versions. `V6_SHOT` is built and smoked but unrun.
4. Unchanged from 0ae: a support measure applied to the INTERVALS (v6 rebuilt
   the measure but the interval work has not been redone on it), and a holdout
   with power for the point benchmark.

## 0ag. Two v8 candidates from mid-v7 diagnostics, 2026-09-11 (Opus)

Both came out of questions Adam asked while v7 was running. Part A is the
message penalty's units; Part B is recency weighting. Diagnostics only — no
arm was run, no fit changed.

### Part A — the message penalty has arbitrary units

Measured mid-v7 from Adam's question: "show me Gobert's raw input vector, I am
wondering if we need some transformation or normalization." Diagnostic only, on
the trained `V7_FULL` fit at origin 2024q3. No arm was run. No fit was changed.

### What the 18 coordinates actually look like going in

`standardization_and_reference` computes a mean and a scale, but applies them
only to `x` — the 64-feature vector the E0 backbone never reads. `message_in` is
`base`, raw. So the message net's `Linear(36, 32)` receives coordinates whose

- **means span −3.663 to +1.307** (none centred), and
- **sds span 0.089 to 0.862 — a 9.7x ratio.**

The six make logits are the narrow end (0.089–0.165); the six location logits are
the wide end (0.541–0.862).

### Ruled OUT: tanh saturation

The first guess, and it is wrong. In the trained model the first-layer
pre-activations run |pre| mean **0.14**, max **1.62** on real lineups, and 0.39 /
1.52 on five Goberts. **0.0% exceed |2|.** The network sits in tanh's near-linear
region even on the most extreme fixture. Do not spend a v8 arm on this.

### The real defect: λ_network is priced in raw coordinate units

`λ_network` does not penalise weights. It penalises the **message itself**:

```python
context = (prediction.context_delta.square() * row_weight[:, None, None]).sum()
network = context / (row_weight.sum() * 5. * n_state)
```

So the cost of moving a coordinate by one of **its own** standard deviations is
`sd_j²`, and that ranges over **93x**:

| coordinate | sd | cost of 1 sd | achieved message, in sd |
|---|---:|---:|---:|
| location_logit_above_break3 | 0.862 | 0.743 (93x) | 0.080 |
| location_logit_rim | 0.699 | 0.489 (61x) | 0.119 |
| assisted_make_logit | 0.805 | 0.648 (81x) | 0.219 |
| make_logit_rim | 0.165 | 0.027 (3.4x) | **0.538** |
| make_logit_above_break3 | 0.089 | 0.008 (1.0x) | **0.459** |

**The model's behaviour matches the price list.** Mean achieved message in units
of each coordinate's own spread: **make logits 0.440, location logits 0.125** —
3.5x apart, in exactly the direction the penalty dictates.

This is backwards relative to what this repo has established. §8g–8h found the
basketball-legible composition mechanism lives in **shot mix**; **conversion has
not moved in six consecutive versions.** The message budget is being spent where
the evidence says there is nothing, and economised where the evidence says there
is something — and the thing setting that allocation is a choice of units nobody
made deliberately.

**Sizing, honestly.** λ·network is 7.8e-5 against the ~0.0020 of data loss the
message buys — **3.9% of the gain**. Not dominant. But v4 and v5 established
λ=.01 is an *interior* optimum from two independent runs, so the penalty binds,
and what it binds is the allocation ACROSS channels. This could still be null in
points; it is a mechanism claim, not a promised MAE gain.

### Marginal extremity and clone extremity agree globally, not at the tail

*Corrected 2026-09-11: the first version of this section named Jokić and Curry
and used ids 1308 and 1051, which are **Steven Adams and Ish Smith**. Jokić is
1458 and Curry 1022. The numbers below are the right players, and they change
the conclusion rather than merely repairing it.*

Mean |z| across the 18 coordinates at 2024q3, against the five-clone distance
that decides withholding:

| player | mean \|z\| | clone distance | percentile | withheld by `HOLDX2`? |
|---|---:|---:|---:|---|
| Jokić | **1.48** | 13.70 | 84.1% | no |
| Curry | 1.31 | 13.14 | 81.4% | no |
| Gobert | 1.26 | 23.39 | 98.6% | **yes** |
| Capela | 1.15 | 26.22 | 99.4% | **yes** |
| Steven Adams | 1.12 | 22.05 | 97.7% | no |
| Ish Smith | 1.07 | 20.21 | 96.3% | no |

Across all 1,035 players the two measures **do** agree in general — corr(mean
|z|, clone distance) = **+0.6393**, corr(max |z|, clone distance) = **+0.8349**.
So a per-coordinate view is a decent global proxy, and the first version of this
entry was wrong to say it "would not have flagged him."

**But they disagree where it matters.** The 21 most extreme players by mean |z|
and the 21 by clone distance **overlap in only 6**. The tail is where withholding
happens, and at the tail the two measures pick largely different people: Jokić
has the highest marginal extremity of the six above and sits at the 84th
percentile of clone distance; Capela has the lowest and sits at the 99.4th.

The implication for v8 is unchanged but better grounded: `V8_SCALE` and `V8_STD`
address how the OBJECTIVE treats coordinates, and `V8_TRIM` addresses which ROWS
carry weight. They are different levers and neither should be sold as the other.

### One dead coordinate, found on the way

`log_assist` (index 16) is decoded but **never read by the forward pass**, which
uses `[:3]`, `[3:9]`, `[9:15]`, `[15]` and `[17]`. Its message-head weight row is
exactly `0.00000` with bias `0.00000` — it has never received a gradient and sits
at its zero init. Index 15 (ft_make) is zero deliberately, by mask; index 16 is
zero by omission. Not damaging, but the decoded state is effectively 17, not 18:
a player's own assist RATE is input-only and no teammate can move it, while
`assisted_make_logit` (index 17) is the single largest consumer of the message
budget at 26.3%.

### What would settle it — two v8 arms, one factor each

1. **Scale-free penalty.** Weight the message penalty per coordinate by
   `1/sd_j²`, prefix-estimated like every other reference, so λ buys the same
   standardized movement everywhere. Weights of 1 reproduce today's model
   exactly, so it is exactly nested with a real control (rule 10).
2. **Standardized message inputs.** Feed `(base − mean) / sd` to the message net,
   leaving `base` itself untouched in the skip path so the decoder is unchanged.

Keep them SEPARATE. "The prior is mis-scaled" and "the features are mis-scaled"
are different claims and bundling them measures neither — the recency/era gotcha
in `CLAUDE.md`, restated.

### Do not re-run

- **Tanh saturation as an explanation for anything.** Measured at 0.0% above
  |2| on real lineups and on the five-Gobert fixture.
- **Per-coordinate |z| as a SUBSTITUTE for the clone-distance ranking.** They
  correlate +0.64 (mean) and +0.83 (max) across 1,035 players, so it is a fair
  global proxy — but the top-21 sets overlap in only 6, and the tail is the only
  place withholding operates. Rank donors by clone distance, as v7 did.

### Part B — recency: three models, three different answers, one pinned default

Adam's question: "when we train for a given origin, are more recent possessions
given more weight?" Nobody had put the three arms side by side on this.

| | training-row decay | state / profile decay | structural time term |
|---|---|---|---|
| **neural** | **730-day half-life** | 180d rates + locations, 730d makes | none |
| **additive** | **none** — `Xs.T @ Xs`, flat | none (`profile_matrix` called with no `halflife`) | per-season δ blocks + `carry` |
| **structural** | n/a — no possession-level fit | 180d role, 730d shooting | none |

Shared by all three: the point calibration is flat by design — its own docstring
says *"No recency weighting at this stage."*

Measured at origin 2015q3 (cutoff 2015-01-18, 170,668 rows, a hard 5.0-season
window), the neural weighting is gentler than it sounds:

| age of row | raw share of possessions | share of TRAINING WEIGHT |
|---|---:|---:|
| last quarter | 9.7% | **19.4%** |
| 2–4 quarters back | 11.5% | 17.7% |
| 1–2 seasons | 21.0% | 25.9% |
| 2–4 seasons | 36.8% | 27.9% |
| older | 20.9% | **9.1%** |

Kish effective sample **60,099 of 170,668 rows**. 2024q3 is near-identical.
Quarter to quarter the tilt is only ~8% (`2^(-90/730) = 0.918`); it bites across
years, not within a season.

**Why this matters beyond bookkeeping.** The neural model down-weights old
possessions and the additive does not. That difference sits underneath every
MAE gap quoted since v2 and has never been raised — the same shape as the
opponent-deconfounding question Adam caught before v5, where the two arms turned
out not to be on equal footing on their inputs. It invalidates nothing; it means
"the additive leads by 0.018" carries an unmeasured time-handling component.

**And 730 is a pinned default that no run has walked off** — `CLAUDE.md` rule 12.
v7's H0.1 audit widened lr, width and γ and proved all three interior; the row
half-life was not in that grid.

**The prior is genuinely two-sided, which is what makes it worth running.**
`profile_recency_works.md` found an interior optimum at a **0.4-season**
half-life (~146 days) once recency was unbundled from era adjustment — five times
shorter than 730, arguing DOWN. But `era_comparability.md` found true rating
spread flat from 2003 to 2024, arguing the league's structure may not drift on
this scale at all — which argues UP, toward flat. Flat is a live outcome, not a
strawman, and it is exactly the additive's convention.

**Arms — a one-factor sweep, exactly nested (∞ = flat = no decay):**

- `V8_HL_FLAT` (no decay), `V8_HL_365`, `V8_HL_180`, with 730 as the base.
  Four points, so 730 is interior between 365 and ∞ if it wins. If 180 wins the
  grid must be widened DOWN to 90 before believing it (rule 10, twice).
- The row half-life and the state half-lives do different jobs and should not be
  swept together: the state half-life is how stale a player's INPUTS are; the row
  half-life is how much old basketball informs the SHARED mapping. Player form
  drifts fast, the structure of the game slowly, so row > state is coherent as a
  starting point. One factor at a time.

### Not worth an arm, recorded instead

- **`asof_additive` calls `profile_matrix(...)` with no `halflife`**, so the
  benchmark additive's box-score prior is a flat career average and does not use
  the +0.000068 profile-recency lever established for `additive_stack`. I can
  find no recorded decision either way in `ASOF_ADDITIVE_FOUNDATION.md`,
  `ASOF_ADDITIVE_REFERENCE_RESULTS.md` or `MATCHED_BENCHMARK.md`. **Do not
  quietly switch it on**: the comparator is frozen, and changing it retroactively
  invalidates every neural-versus-additive gap quoted since v2. If it is ever
  worth testing it must be a separately named comparator reported beside the
  frozen one, never a silent swap.
- **The model carries four different half-lives** — 365 for the usage budget, 180
  for rates and locations, 730 for make logits, 730 for training rows. That is a
  description, not a defect, and turning it into arms without a reason would be
  the un-audited-grid mistake in reverse. Noted so the next reader is not
  surprised by it.

### Budget note for whoever plans v8

Part A is 2 arms, Part B is 3, plus a base: **6 before tracking data**, which was
the original v8 subject. That is at the top of the 4–8 range this workstream runs
per version. Tracking may need v9, or the half-life sweep can be cut to
`FLAT`/`365` at the cost of the downward boundary check. Adam's call.

## 0ah. Joint capability v7 — extremity measured, and v6 qualified, 2026-09-11 (Opus)

Read `reports/joint_capability_v7_review.md`. Run
`experiments/cache/joint_capability_2026_09_11_v7/`, 288/288 arm-origins,
48 origins, 12 seasons.

### Do not re-run

- **Withholding the top 5% of donors.** Established harm: `HOLDX5 − FULL` is
  +0.0596 ± 0.0216 (2/12) on donor5 and +0.0889 ± 0.0355 (2/12) on donor2. The
  dose curve is 2% helps / 5% hurts; both points are now measured.
- **`V7_HOLDX2` as a shippable configuration.** It is the best neural arm on
  three of four regions, and it gets there by deleting Gobert, Capela, Zubac and
  18 others from training. A tool must price those players. The result is a
  DEFECT REPORT about the shared objective, not a model.
- **Correlation as the extrapolation statistic.** r stayed at 0.9955–0.9982
  while mean |difference| tripled on the withheld donors. Report mean |diff| in
  pts/100 beside any correlation, always.
- **Claiming `HOLDX2` prices donor cells better.** It read −0.0311 on donor5 at
  39 origins and −0.0139 ± 0.0218 at 48, with a difference-in-differences of
  +0.0011 ± 0.0178. The benefit is uniform across regions. Do not re-open.
- **Assertion gates as run control** (see §0ag process note). One pair-origin at
  3.22% against a 3% threshold destroyed a 2-hour sweep at origin 39/48;
  dropping that origin moves the headline by 0.0001.
- **Raising the epoch cap again.** 24 → 48 in v7; median selected epoch is 12,
  maximum 30, none at the cap across 288 arm-origins. Adam's v6 observation is
  discharged.

### Open, in the order I would take them

1. **A distance-aware interval, finally with evidence behind it.** v7 measured a
   real gradient: the model's disagreement with itself rises +0.0616 pts/100 per
   unit of composition distance and reaches **1.64 pts/100** on donors it never
   trained on, against 0.51 on donors it did. That is a measured quantity with
   dynamic range — what `distance_shrink.py` could not fit and what the coverage
   gate asserts. It is the best-supported open item in this workstream. Carried
   unchanged since v5; stop carrying it.
2. **The message penalty's units** — §0ag Part A, two nested arms.
3. **Recency and the additive's flat prefix** — §0ag Part B, three nested arms.
4. **Calibrate the learned duplication penalty.** Corrected on the day: the
   fixture swing that three versions reported as a defect is NEGATIVE and is a
   composition penalty, not score shrinkage — −3.004 ± 0.432 pts/100 at matched
   score, far half versus near half by distance, **8/8 origins**, with real
   lineups at +0.196. The model derived from event data what the tool asserts.
   Direction is established; **magnitude is unchecked**. Five clones of the best
   player still print 132.43, 106.6% of the model's own in-range maximum. This is
   the shortest path from this workstream to the northstar and it was found by
   accident — nobody checked the sign of a column reported since v3.
5. **Conversion — the §10 route is now CLOSED HARM, and the live route is role.**
   `V7_SHOT` finally ran (48/48, 1,829 s) and is **worse on the channel it was
   built for**: conversion +0.000033 ± 0.000008, better in **1 of 12 seasons**.
   Points are noise either way (ALL −0.0024 ± 0.0214). Do not route the §10
   shot-quality coefficient into the message again. The one thing that HAS moved
   conversion is `V7_LOAD`'s `k_make_over`, non-zero in 48/48 — overload, i.e.
   ROLE, not teammate identity. `JOINT_CAPABILITY_V8_PLAN.md` P0.3 tests whether
   the loss was double-counting.

### The one suggestive positive

`HOLDX2 − RANDX2` = −0.0164 ± 0.0077 on ALL, 7/12 seasons, robust to dropping
the flagged origin (−0.0164 ± 0.0076). Clears two sem pooled; 7/12 is close to a
coin flip. Read it as "extreme donor states distort the shared mapping" — a lead
for §0ag Part A, not a finding.

## 0ai. Tracking data — investigated, deferred to v9, 2026-09-11 (Opus + Adam)

Read `JOINT_CAPABILITY_V8_PLAN.md` "Not in scope". Cache at
`experiments/cache/tracking/` — 78 files, 4.5 MB, 13 seasons × 6 measures,
pulled read-only via `experiments/fetch_tracking.py`. No database touched.

### What is there

- **First season is 2013-14.** 2010-11 through 2012-13 return a valid schema and
  **zero rows**, so the usable window is 13 seasons, 2013-14 to 2025-26.
- **Schemas are identical every year** for all six measures — Passing 18 cols,
  Drives 25, CatchShoot 16, PullUpShot 16, Defense 14, Rebounding 35, zero
  missing measure-seasons. Row counts track roster size, 482 → 582.
- **Three granularities**, all confirmed live:
  `leaguedashptstats` = player × season (what is cached; **`DateTo` works**, so
  prefix-only pulls are 48 origins × 6 measures ≈ 24 min);
  `boxscoreplayertrackv3` = player × game, 21 stats including speed, distance,
  touches, contested FG and rim defence — but **one request per game**, ~16,000
  requests for the tracking era, and note **v2 returns HTTP 500**, so the parser
  must target v3's `boxScorePlayerTrack` envelope, which has no `resultSets`;
  `playerdashptpass` = **player × TEAMMATE**, passes and assists both directions
  with the teammate's FGM/FGA off those passes.
- **Player join is 99.4%** of player-seasons on normalised names after stripping
  Jr/Sr/II/III/IV suffixes (6,897 of 6,942).
- **No raw x/y.** Every endpoint returns derived aggregates; the SportVU
  coordinate dumps are gone. Tracking means richer counting stats, not geometry.

### Do not re-run

- **The vendor switch as a suspected break.** SportVU → Second Spectrum in
  2017-18 is the obvious worry and it is CLEAN: every definition-invariant ratio
  moves within noise there, and for 8 of 10 raw stats the largest jump in the
  series is elsewhere.
- **Trusting the Drives family across 2024-25.** That is the real break.
  `DRIVES` jumped **+31.9%** in one season after a decade of ~4%/yr; points per
  drive fell **−30.1%** (0.584 → 0.409) against a median year-over-year change of
  1.4%, and FGA per drive **−11.9%**. A loosened detection threshold, not
  basketball. `AST / POTENTIAL_AST` breaks in the same year (−6.7%).
- **"Box-score profiles reach ~1%"** as the bar for a new feature set, which is
  what `fetch_tracking.py`'s docstring says. That is the BILINEAR, and it is dead
  — 0.9%, identical to the additive control and below the boosting placebo. On
  16,221 pairs the real bar is **role overlap at 4.6%** (min/max on ball-and-role
  dims), with |difference| at 3.9%. Pair compatibility is about whether roles
  COLLIDE, not the product of two skill vectors — `the_ball_is_the_interaction`
  restated.

### The screen came back inconclusive, and why

`pair_predictability --side off --tracking` restricts to the 10,483 pairs where
both players have ≥500 tracked minutes and rescores everything on that cohort.
Top line is the tracking bilinear at 2.7%, box-score min/max at 2.2% — but the
placebos on that cohort run to **−2.0%** (|corr| 0.140) against real effects of
0.130–0.166. **Everything is inside the placebo band; nothing is established in
either direction.** The box-score features fall 4.6% → 2.2% under the same
restriction, so the cohort is noisier rather than the features worse. The
restriction costs more power than tracking adds information.

### What would settle it, and the order to do it

1. **Refit the pair block on the tracking era only** (2013-14 on), so the target
   and the features cover the same period and the cohort restriction is free.
   There is no season filter on `pair_predictability` yet; it is a small
   addition and it must come before any tracking build.
2. **Then the pair-level passing pull**, which is the categorically new input.
   Every previous attempt — bilinear, embeddings, attention, boosting — predicted
   a pair effect from two INDIVIDUAL profiles, and `pair_effects_unpredictable`
   and `pair_effects_not_lowrank` are the record of that failing. `playerdashptpass`
   measures the pair directly. It is ~500 players × 13 seasons of requests, so
   price it before starting.
3. Per-game tracking only if something justifies a ~16,000-request overnight pull.

## 0aj. Joint capability v8 — the inputs were never standardised, 2026-09-12 (Opus)

Read `reports/joint_capability_v8_review.md`. Run
`experiments/cache/joint_capability_2026_09_11_v8/`, 336/336 arm-origins,
48 origins, 12 seasons, 9,828 s, zero errors.

### Do not re-run

- **The extremity-trim route.** v7's `HOLDX2 − RANDX2` = −0.0164 ± 0.0077 (7/12)
  does NOT reproduce as a continuous down-weight with a matched footprint:
  `V8_TRIM2` is +8.17e-05 (1/12) on event loss and +0.0117 ± 0.0082 on points,
  `V8_TRIM5` worse still. Either the mechanism was hard row deletion — which
  cannot ship, a tool must price Gobert and Capela — or v7's result was the coin
  flip its 7/12 implied. Treat it as closed.
- **Scale-free message penalty as an ACCURACY lever.** `V8_SCALE` confirmed
  §0ag Part A's diagnosis exactly (location message 0.1052 → 0.1251, make
  0.4809 → 0.4046; location event loss −6.13e-05 at 10/12, conversion +3.40e-05
  at 0/12) and is a net null: +1.21e-05 event, +0.0060 ± 0.0037 points. The units
  were wrong and the wrongness was free. §0ag Part A is CLOSED.
- **Shortening the training-row half-life.** 365 days is established harm on
  event loss (+1.064e-04, 1/12). 730 survives its first audit; do not widen down.
- **The additive/neural time asymmetry as a suspected handicap.** `V8_FLAT`
  adopts the additive's no-decay convention and is worse in points (+0.0143 ±
  0.0207), a wash on events. §0ag Part B is CLOSED.
- **Per-arm event-loss baselines.** They make cross-arm event loss meaningless.
  v8's shared baseline is verified identical to 0.00e+00 across 336 arm-origins;
  any future version must keep it.

### The finding

**`V8_STD` — standardising the message network's inputs — improves the training
objective in 47 of 48 origins and 12 of 12 seasons, on all five families**
(event loss −4.12e-04 ± 4e-05; location −7.35e-04; counts −2.06e-04; conversion
−1.39e-04, every one 12/12). The coordinates had means from −3.663 to +1.307 and
a 9.7x sd range and were fed to `Linear(36, 32)` raw for eight versions.
**Conversion moved for the first time in seven versions.**

It is worth **nothing** in points: +0.0125 ± 0.0233 (5/12), RMSE and r²
indistinguishable from base. Ship it anyway in any future backbone — a model that
fits its own objective better for free is strictly better conditioned — but do
not expect points from it.

### Open, in the order I would take them

1. **ANSWERED inside v8: it is resolution, not misalignment.** The six-arm
   inverse ranking (Spearman −0.886) does not survive the discriminator. Pooling
   all 288 (arm, origin) paired deltas, MAE gain on event gain gives **slope
   −3.68 ± 21.39, r = −0.0102**; `V8_STD` alone reads r = +0.038 over 48 origins;
   per-arm correlations scatter +0.456 to −0.535 at n = 48. The benchmark cannot
   see gains this size — §0's standing calibration. **Do not change the objective
   in v9.** The real choice is: accept event-level improvement as the deliverable,
   or find a point evaluation with more power (more cells, a lower-variance
   target, or a paired design that removes the finite-batch noise a ~84-possession
   cell carries).
2. **Tracking** — §0ai, deferred by decision. Refit the pair block on the
   tracking era first so target and features share a period.
3. The distance-aware interval is a measured null in range
   (`V8_PHASE0_FINDINGS.md` P0.1) and only answerable out of support, where there
   is no forward error to fit against.

## 0ak. Joint capability v9 — teammate variety is real, 2026-09-12 (Opus + Adam)

Read `reports/joint_capability_v9_review.md`. Run
`experiments/cache/joint_capability_2026_09_12_v9/`, 288/288 arm-origins,
48 origins, 12 seasons, 9,145 s, zero errors.

### The finding

**`V9_SPREAD` — giving the message network the leave-one-out standard deviation of
its teammates — improves the training objective in 12/12 seasons and 45/48
origins**: event loss −2.46e-04 ± 2e-05, location −2.56e-04 (11/12), counts
−1.68e-04 (12/12). Conversion does not move (7/12, ns), coherently: variety
changes where and how often you shoot, not how well.

Stacked with v8's standardisation it reaches **−6.58e-04 ± 3e-05 against `V8_BASE`,
12/12 seasons**, for 576 extra parameters on an 1,814-parameter model. The most
consistent improvement in eight versions. **Adopt both in any future backbone.**

Phase 0 predicted it with no fits: teammate sd is 98.1% orthogonal to teammate
mean (median over 18 coordinates, 17 of 18 above 80%).

### Do not re-run

- **Two-round message passing.** Established harm: +4.05e-05 ± 2e-05, 3/12, worse
  on every family, better in only 17/48 origins — and round two grew to 45% of
  round one, so the data used it and it generalised worse. One round is the right
  depth on this data.
- **A non-diagonal decoder.** `V9_DECODER` (rank-3 additive) is null at −1.76e-05
  (8/12) with `U` at 4.7% of the diagonal slope. The diagonal's strong bias costs
  nothing and its interpretability is safe.
- **min/max as a better sender than sd.** `V9_MINMAX` reaches −2.35e-04 (11/12)
  with a block 26% larger. Same idea, less efficient encoding. The finding is
  "the second moment", so use sd.
- **Usage-weighted senders** (killed in Phase 0, §0ak/`V9_PHASE0_FINDINGS.md`):
  within-lineup usage sd is 0.050 around a mechanical mean of 0.197, so the
  weighted sender sits 0.026–0.255 coordinate sds from uniform against the sd
  sender's 3.805.
- **Expecting objective gains to appear in points.** −6.6e-04 at 12/12 converts to
  `V9_ALL − V8_BASE` = −0.0008 ± 0.0254. v8 diagnosed this as resolution; v9
  retested it with a 1.6x larger effect and the answer held.

### Open, in the order I would take them

1. **A point evaluation with power. This is now the binding constraint on
   everything else.** Two consecutive versions have produced real, unanimous
   improvement to the model's objective and the point benchmark has moved 0.0008 ±
   0.0254. An ~84-possession cell is mostly finite-batch noise. Options: many more
   cells (relax the exposure floor and weight properly), a lower-variance target
   (the centered/detrended score rather than raw points), or a paired design that
   differences out the batch noise between arms scored on the same possessions.
   **Until this exists, no further architecture or objective arm can be graded**,
   and the additive comparison (+0.0302 ± 0.0393, unchanged since v7) stays
   permanently unresolvable.
2. **Tracking** — §0ai, still deferred; refit the pair block on the tracking era
   first so target and features share a period.
3. **Is there more in the set summary?** The second moment pays and min/max pays
   about the same. Nobody has tried a third moment, a learned pooling, or a
   quantile summary. Cheap, and v9's Phase 0 recipe transfers directly.

### The correction worth carrying

I told Adam after v8 that the architecture was a dead end. That was generalised
from three **capacity** axes — width, the encoder, pair pooling — to a claim about
the architecture as a whole, and the best-supported single change in the
workstream came out of an axis I had not tested. **"We tried X, Y and Z and they
failed" is not "that class of change fails."**
