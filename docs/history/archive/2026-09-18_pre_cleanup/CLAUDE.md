# Working in this repository

**Next experiment planned, 2026-09-18:** v15 source/tests/reviews committed as
**e438a4a** after 59 focused tests. Read `JOINT_CAPABILITY_V16_PLAN.md`: 22
designs covering strictly dated adjusted player profiles, joint offense/defense,
two-sided attention with capacity controls, action allocation, two-phase renewal
with supervision controls, and prespecified integrations. Common calibration,
broad plus historical primary cohorts, checkpoint-average sensitivity and an
explicit persistent-discrepancy uncertainty experiment are required. Planning
only: no v16 code, feature fits, pilots or launch yet. Implementation must measure
multi-day runtime/storage in pilots and deliver verified background commands;
production launch awaits Adam. New plan/context changes follow the v15 commit
and are uncommitted. No delegation, scorer promotion or deployment.

**Completed/reviewed, 2026-09-18:** v15 finished all576cases in13h36m.
Read `reports/joint_capability_v15_codex_review.md` and the latest handoff.
Independent hashes, cutoffs,54scorecards and134,568interval rows pass. Best
registered MAIN_RB half RMSE10.72573/r².13904 versus old HALF+D10.73215/.13801;
incremental RMSE difference−.00642 [−.04077,+.02369], not established. Old NN+D
still leads novel RMSE11.68172. Cross/rebound channel gains occur11/11seasons,
but point gain is mostly level calibration and common prior-affine sensitivity
reverses the tiny blend ranking. Five-center offense, reference integration
(up to~1pt/100 at128vs256) and latent OOD uncertainty remain open. Primary is
the inherited profile-supported matched cohort, not all>=50lineups; a separate
broader analysis is now available. No promotion, new fits or commit. No active
run; all older RUNNING/NOT_STARTED notes below are historical.

**Latest discussion, 2026-09-17:** Adam has launched v15 and asked to leave it
running. Historical NOT_STARTED notes below are superseded; check status before
resuming and never launch a duplicate. He also asked to park lineup-adjusted
offensive/defensive capability profiles as a possible future NN input upgrade.
Read `MODEL_RESEARCH_ROADMAP.md` R16 and the latest SESSION_HANDOFF. This is
documentation only, not a new experiment or authority to change the frozen run.

**Launch-ready, 2026-09-17:** v15 actual-opponent adapters are implemented and
verified. Read `reports/joint_capability_v15_launch_checkpoint.md` for the full
protocol/commands and latest SESSION_HANDOFF. Eight final pilots,46tests,
independent54card audit and production preflight pass; all16repeated pilot fits
are bit-identical. Production `...v15_prod` is`NOT_STARTED`, no active training.
Adam has not launched the full576case run; do not launch without his request.
No model/protocol retuning from pilots, no old artifact edits or commit.
Read `reports/joint_capability_v15_companion_review.md` for Cleveland action
allocation/rebound diagnosis and residual persistence; latent OOD uncertainty
and five-center offense remain unresolved. Older in-progress notes follow.

**In progress, 2026-09-17:** Adam approved actual-opponent modeling. New
`JOINT_CAPABILITY_V15_EXPERIMENT.md` freezes four defensive event adapters over
saved RB_RENEW_FAC offense (main/cross × defensive recovery), three seeds and48
origins. Implemented directly; new labels reconcile6,059,380possessions exactly,
and strictly dated defensive profiles pass independent prefix replay. Fair
opponent-aware additive control RMSE10.78699 vs blind10.84099. Full-length
eight-case pilots are running at `...v15_pilot`; **not yet launch-ready**.
See latest SESSION_HANDOFF for current process, pending operational checks and
companion findings. Do not launch production or edit frozen training producers.

**Latest, 2026-09-17:** committed completed diagnostics as **5e90381**. Read
`reports/model_stocktake_2026_09_17.md` for the holistic review requested next.
Recommend actual-opponent/defense as the next main campaign, with bounded
offensive action-failure and latent-uncertainty work.2.76Mprimary possessions
already have both valid fives; matchup grouping increases rows1.751×. Reuse
audited additive defensive controls; don't confuse V5 profile deconfounding
with actual-opponent NN conditioning. Direction is proposed, no new training
or frozen experiment. Subsequent stocktake/context docs remain uncommitted.

**Latest, 2026-09-17:** shared game-situation diagnostic implemented/completed;
read `reports/game_situation_diagnostic_review.md` and latest handoff. No
fan-facing game-state input or NN/additive refit. Prior-only ENV/CLOCK/MARGIN
rates cover19targets/44origins. Combined NN substantial FTA bias4.010→.995→.913;
point HALF advantage over A survives, but2016Cleveland remains a major failure.
All original forecasts/artifacts intact;80tests and independent score/lineage
checks pass. Output `...game_situation_2026_09_17_v2`, COMPLETE. No process,
promotion or commit. New diagnostic and prior FTA work remain uncommitted.

**Latest, 2026-09-17:** benchmark work committed as **929f8dd**. Read
`reports/v14_free_throw_situation_review.md`: new read-only neural FTA audit
finds global bias+0.098/100 but common>=200 bias+4.010, with low-exposure and
late-game underprediction cancelling early-game/common-lineup overprediction.
Coarse state mix contributes1.909 and within-state remainder1.507/100 to the
substantial common-lineup error; descriptive, not causal or a fitted correction.
All3retained arms share the pattern.67tests pass; no fits or active processes.
Proposed next: bounded context-aware opportunity control, then joint decoder
under an explicit prior-only environment reference. This new audit is uncommitted.

**Latest, 2026-09-17:** committed the completed v14 review as **f7e89aa**,
then implemented the authorized transfer benchmark and repeated-failure audits.
Read `reports/transfer_role_benchmark_review.md` and latest SESSION_HANDOFF.
On146substantial q1team-change cells, ROLE_SL direct RMSE6.58670 vsA6.85781;
combined SHIFT6.68083 is not the cohort winner. Zero-shift channel replay gives
only a small uncertain difference. The broad available-cell slice favors old
HALF among retained forecasts. Large-lineup FTA overprediction is a concrete
next diagnostic (23.20 vs18.71/100). No new fits/promotion; all90frozen v14
producers intact. New benchmark source/output block remains uncommitted.

**Completed/reviewed, 2026-09-17:** v14 finished successfully (44h12m).
Read `reports/joint_capability_v14_codex_review.md` and the latest handoff.
All2,304 cases,90 code/38 input/678 report hashes verify. Best three-seed
RB_RENEW_FAC_SHIFT direct RMSE10.79367/r².12809; its half blend
10.77978/.13034 versus additive10.84099/.12043 and old HALF10.80812/.12576.
Retain ROLE_SL (best blend MAE), RB_RENEW_FAC (renewal/mechanism candidate),
and RB_RENEW_FAC_SHIFT (RMSE challenger); no promotion or new fits.
Matched-seed shift/renewal gains are encouraging; five-Gobert offense and
latent OOD uncertainty remain unresolved. Primary persistent-error summary
was corrected in a new derived prefix to exclude2015 warmup. Originals intact.
No training is active. Earlier RUNNING/launch notes below are historical.

**Running/source checkpoint, 2026-09-15:** Adam launched v14 successfully and
authorized a source/documentation commit. Production metadata says `RUNNING`,
PID18738, started09:52:30 local; do not launch a duplicate or edit frozen
producers. Generated caches/live outputs remain local and outside this commit.
Read the latest `SESSION_HANDOFF.md` entry; it supersedes pre-launch notes below.

**Launch-ready, 2026-09-15:** Codex implemented v14 directly. All16 prescribed
full-length pilots and reports completed;21 tests and the independent artifact,
ledger/cutoff/selection/reuse/resume audits pass. Production preflight is
`NOT_STARTED`, exit0, zero training cases. Adam has not launched the full run.
Read `reports/joint_capability_v14_launch_checkpoint.md` for exact commands,
acceptance evidence and cost estimate (roughly50–75h;80–100GiB headroom).
Do not launch without Adam's request, edit frozen producers mid-run, delegate,
promote a scorer or commit. Pilot results did not change the registered design.

**Implementation history, 2026-09-15:** Codex implemented v14 directly.
Adam explicitly retired the Opus-worker workflow; see the override in AGENTS.md.
No worker was launched. Read-only extraction reconciled all6,059,380 original
possessions; new labels contain2,216,895 eligible FG recoveries, including
516,768 ORBs, without removing any of897,778 point-training groups. New dated
states and phase diagnostics are separate v14 artifacts. Core models/fit/runner
and reports exist;21 focused tests and14 real-control replays/7 exact one-epoch
fit-parity checks pass. Both48-arm/seed smokes completed, including6,392 fixture
rows. The prescribed16 full-length pilot cases subsequently completed in
`...v14_pilot`; final acceptance is recorded in the launch checkpoint above.

**Next design, 2026-09-15:** `JOINT_CAPABILITY_V14_EXPERIMENT.md` defines the
requested large role/rebound-facilitation/renewal campaign:16 designs,3 matched
seeds,48 origins, with verified v13 control reuse where equivalent. It is now
implemented and launch-ready as recorded above. Adam welcomes read-only local
database access; do not carry earlier cache-only restrictions into new designs.
Use new frozen extracts for reproducibility, preserving old artifacts and DB
contents. Raw rebound sequences are available; v14 should use them instead of
limiting labels to the old aggregate cache. See latest handoff before acting.

**Current result, 2026-09-15:** v13 is complete and independently reviewed. Read
`reports/joint_capability_v13_codex_review.md` and the latest handoff before
the historical launch notes below. All 960 arm-origins and frozen hashes verify.
Half additive / J_ROLE_SUPPLY_LOAD leads pooled RMSE at 10.79364, r² .12810,
versus old HALF 10.80812/.12576 and additive 10.84099/.12043. Improvement over
HALF is mainly recurring, not novel; its season-RMSE interval includes zero.
Role+constraints improve event loss in all 11 seasons versus J_BASE, but the
best arm lacks seed replication and constraints' overall gain flips by seed.
Center behavior improves without being solved; latent OOD uncertainty and
actual opponents remain open. No promotion. Discuss the follow-up design;
no new run is authorized or active. Completed originals remain read-only.

**Current next experiment, 2026-09-14:** Adam authorized a large v13 campaign,
implemented directly by Codex without delegation. Read
`JOINT_CAPABILITY_V13_EXPERIMENT.md` and
`reports/joint_capability_v13_launch_checkpoint.md`. Twenty trajectories test
objectives/readouts, creation/load constraints, richer teammate summaries and
dated role inputs. All-arm smoke and four full-length pilots pass; production
preflight is `NOT_STARTED`. Adam has the background command; do not launch it
unless asked. No scientific arm was changed after seeing pilot results. The v12
rerun below remains on hold; it is not the next launch target.

**Current decision, 2026-09-14:** read
`reports/joint_capability_v12_partial_codex_review.md` and the latest handoff.
The full rerun is on hold after Adam requested analysis of the partial evidence.
The anchored residual loses predictive accuracy and can reverse the apparent
meaning of a learned center penalty. Original NN novel-lineup signal survives.
Discuss the design before further training; the launch-ready notes below are
historical. No new fit or scorer promotion occurred in this review.

**Next neural work, 2026-09-14:** read
`reports/joint_capability_v12_launch_checkpoint.md` and
`reports/joint_capability_v12_handoff.md`. Day6's two trained additive-anchored
hybrids, causal replay, Day5 audit closeout and prescribed pilots are complete.
The first production run preserved 74/96 outputs before a float32 ledger
tolerance stopped it; the repaired fresh prefix passes preflight but remains
`NOT_STARTED`. Use only the new command in the launch checkpoint and obtain
Adam's authorization before launching. The pilots are operational evidence only.
After production, inspect the automatic outputs and write the independent v12
scientific review before any model decision.

**Current neural checkpoint, 2026-09-13:** v11/Day5 is complete. Start with
`reports/joint_capability_v11_review.md` and the latest `SESSION_HANDOFF.md`.
Frozen replacement of the NN main effect with additive value does not improve
the registered recurring-lineup target. Retaining full projected context is tied
overall and slightly improves novel RMSE, but the extracted interaction gives
five Goberts a positive adjustment and five Jokics a large negative one; it is
not a transferable basketball complementarity mechanism. Additive and HALF/GLOBAL
remain the research controls. A jointly adapted residual is the possible next
experiment, not another frozen recombination. Five-Gobert final offense,
latent-mean uncertainty,
and actual-opponent defense remain unfinished. Older v9 ceiling/power statements
below are historical conclusions qualified by the independent reviews.

Research codebase for NBA possession prediction. Read this first. If
`SESSION_HANDOFF.md` exists, read it next for the latest uncommitted session,
then read **`CONTEXTUAL_MODEL.md`** for the current product and research contract.
`CURRENT_MODEL.md` documents the incumbent additive page, term by term,
`STRUCTURAL_MODEL.md` does the same for the structural arm, and
`RESEARCH_OVERVIEW.md` §8–9 records how the additive one was established.

**START HERE for the neural workstream: `JOINT_CAPABILITY_STATE.md`** is the
single-file synthesis across v2-v9 -- what the model is, what is established, what
is closed, whether a non-additive model can beat the additive one (pooled no,
NOVEL fives yes at 9/12 seasons), and why a point evaluation with power now comes
before any further model work.

**Latest, 2026-09-12 (Opus + Adam): teammate VARIETY is real, and the
architecture was not a dead end.** Read `reports/joint_capability_v9_review.md`.
288/288 arm-origins. v9 exists because Adam pushed back on my claim that the
architecture was closed -- that claim generalised from three CAPACITY axes (width,
encoder, pair pooling) to the architecture as a whole, and the best-supported
single change in the workstream came out of an axis I had never tested.

The message network's teammate summary was a leave-one-out MEAN and nothing else,
so four teammates at {+2,-2,+2,-2} and four at {0,0,0,0} sent a byte-identical
message. **`V9_SPREAD` adds the leave-one-out STANDARD DEVIATION -- 576 parameters
on 1,814 -- and improves the training objective in 12 of 12 seasons and 45 of 48
origins** (event loss -2.46e-04 +- 2e-05; location -2.56e-04, counts -1.68e-04;
conversion unmoved, coherently). **Stacked with v8's standardisation it reaches
-6.58e-04 against `V8_BASE`, 12/12 seasons** -- the most consistent improvement in
eight versions. Phase 0 predicted it with no fits: teammate sd is 98.1%
orthogonal to teammate mean.

Three architectural negatives, all informative because every block GREW: a second
message round is established HARM (+4.05e-05, 3/12) even though round two reached
45% of round one; a rank-3 decoder correction is null with `U` at 4.7% of the
diagonal slope, so the diagonal's bias costs nothing; and min/max matches sd with
a 26% larger block, so the finding is "the second moment", not capacity.
`BACKLOG.md` 0ak carries the do-not-re-run list.

**In POINTS it is a wash and that is now the binding constraint on the project.**
`V9_ALL - V8_BASE` = -0.0008 +- 0.0254 while the objective moved -6.6e-04 at
12/12. v8 diagnosed this as RESOLUTION rather than misalignment (slope
-3.68 +- 21.39 over 288 paired deltas) and v9 retested it with a 1.6x larger
effect. **Until a point evaluation with power exists, no further architecture or
objective arm can be graded** and the additive gap (+0.0302 +- 0.0393, unchanged
since v7) stays unresolvable. That is 0ak item 1 and it comes before tracking.

**Latest, 2026-09-12 (Opus + Adam): the message inputs were never standardised,
and fixing it moves every event family in 12/12 seasons.** Read
`reports/joint_capability_v8_review.md`. 336/336 arm-origins. v8 froze the
architecture again, made the OBJECTIVE'S CONDITIONING the factor, and rebuilt the
measurement first: v7 normalised each event family by the untrained model on that
ARM'S OWN training rows, so any arm that reweights moved its own denominator --
the artifact was 3.5x the effect. v8's shared baseline is identical to
**0.00e+00** across all 336 arm-origins, and `V8_BASE` reproduces `V7_FULL`
bit-identically.

**`V8_STD` standardises what the message network reads -- nothing else -- and
improves the training objective in 47 of 48 origins and 12 of 12 seasons on ALL
five families** (event loss -4.12e-04 +- 4e-05; location -7.35e-04; counts
-2.06e-04; conversion -1.39e-04). The 18 coordinates had means from -3.663 to
+1.307 and a 9.7x sd range and went into `Linear(36, 32)` raw for eight versions.
**Conversion moved for the first time in seven versions.** In POINTS it is worth
nothing: +0.0125 +- 0.0233, 5/12, RMSE and r2 indistinguishable from base.

Three routes closed. **v7's `HOLDX2` lead did not survive** -- a continuous
extremity trim at a matched footprint is worse than base on both readouts, so
v7's one two-sem contrast was probably the coin flip its 7/12 implied.
**The message penalty's units were mis-set and the wrongness was free**
(`V8_SCALE` moved the budget exactly as diagnosed and bought nothing).
**The 730-day row half-life survives its audit** and the additive/neural time
asymmetry was costing nothing. `BACKLOG.md` 0aj carries the do-not-re-run list.

**The apparent objective/target conflict is RESOLUTION, not misalignment**, and
v8 settled it internally. Across six arms the event-loss and MAE gains look
inversely ranked (Spearman -0.886), but that is six points chosen after seeing
them; pooling all **288 (arm, origin) paired deltas** gives slope
**-3.68 +- 21.39, r = -0.0102**, and `V8_STD` alone reads r = +0.038 over 48
origins. The benchmark cannot see gains this size -- `BACKLOG.md` 0's standing
calibration. **So do not change the objective in v9**; the choice is between
accepting event-level improvement as the deliverable and finding a point
evaluation with more power.

**Latest, 2026-09-11 (Opus + Adam): v7 finds the extrapolation gradient v6 could
not, and fits a mechanism.** Read `reports/joint_capability_v7_review.md`.
288/288 arm-origins. v7 froze the architecture again and pushed the holdout from
v6's lineup quantile to **donor extremity** -- withhold the players whose
five-clone lineup sits furthest from anything ever played. Two results.
**v6's "no composition-distance gradient" is qualified, not confirmed:** past the
observed range a model disagrees with the full model about donors it never
trained on by **1.64 pts/100 against 0.51 on the rest**, rising monotonically
with distance (+0.0616 per unit). Correlation stayed at 0.9958 the whole way --
**correlation is blind to exactly the level shift a tool that prints a number
cares about.** That gradient is the first MEASURED distance signal with dynamic
range, and it makes the distance-aware interval the best-supported open item.
**And 8.1's overload response fits:** `k_make_over` non-zero in **48/48**
origins, `k_to_over` exactly zero in **47/48** -- overloading a player costs his
shooting and not his turnovers, fitted rather than asserted, though worth only
-0.0026 +- 0.0025 in points. Removing the top 2% of donors beats its matched
random control by -0.0164 +- 0.0077 (7/12) UNIFORMLY across regions, so it is
outlier trimming on a shared fit, not better extrapolation -- and it is a defect
report, not a configuration, since it works by deleting Gobert, Capela and Zubac
from training. Removing the top 5% is established HARM. **And a correction found the same day: the
fixture-magnitude guardrail has been read backwards since v3.** The five-clone
context swing is 255% of the in-range maximum, but nobody checked its SIGN. It is
NEGATIVE, and it is a composition penalty rather than score shrinkage -- at
matched no-message score, clones in the far half by composition distance are
pulled down **3.004 +- 0.432 pts/100** more than the near half, **8/8 origins**,
while real lineups sit at **+0.196**. The model has learned from EVENT data the
duplication penalty `tool/five.html` asserts, and it escapes
selection-on-the-outcome because the message is never fitted on lineup points --
the bias that made floor geometry, index curvature and defensive coverage all
extrapolate the wrong way pushes AGAINST this result. Direction established;
**magnitude uncalibrated**, and that is the shortest path from this workstream to
the northstar. **And `V7_SHOT` finally ran** after two versions in a secondary block nobody launched: it is established HARM on the channel it was built for (conversion +0.000033 +- 0.000008, better in 1 of 12 seasons), so the §10 route into conversion is closed and the live route is ROLE, via `k_make_over`. `BACKLOG.md` 0ah carries the do-not-re-run list, 0ag the measured v8 candidates (the message penalty's units, and recency), 0ai the tracking investigation. **`JOINT_CAPABILITY_V8_PLAN.md` is the next experiment**: Phase 0 cashes the two northstar results above with no fits, then a seven-arm sweep at the objective's conditioning. Tracking is v9.

**Latest, 2026-09-11 (Opus + Adam): v6 shows the model EXTRAPOLATES across the
observed range.** Read `reports/joint_capability_v6_review.md`. v6 froze the
architecture and made the training population the factor: withhold the unusual
quartile of lineups and the model prices them anyway. HOLD75 has the best
withheld-region MAE of five arms, beats the full model there, and its five-clone
ratings correlate **r = 0.9966** with the full model's donor by donor, with no
gradient in composition distance. **The selection-on-the-outcome objection --
why the coverage gate is asserted rather than fitted -- does not appear to bind a
model with no lineup, pair or identity parameters.** Limit: 99.5% of withheld
cells sit at or below the clean real maximum, so this validates extrapolation
ACROSS the observed range, not beyond it; the fixtures sit at 1.8-3x. Nothing is
statistically established. `BACKLOG.md` 0af carries the do-not-re-run list; next
is to withhold by DONOR EXTREMITY to reach the range that matters.

**Latest, 2026-09-11 (Opus + Adam): v5 closes the INPUT route.** Read
`reports/joint_capability_v5_review.md` and `JOINT_CAPABILITY_LEARNINGS.md`.
v4 settled the architecture (mean pooling carries the whole teammate effect,
11/11 seasons on novel lineups; pair pooling and the learned encoder are dead).
v5 froze that backbone and varied only the inputs and the objective six ways --
opponent-deconfounded states, height/position, offensive rebounding as a 19th
coordinate, the 46 unused features into the message, all four, and
points-leverage family weights. **Every one is null or harmful.** V5_BASE, the
unchanged 1,814-parameter backbone, has the best novel MAE/RMSE/r2 of eight arms
and ALL is the exact sum of its parts. Two contrasts are established AGAINST the
intervention, and with v4 they make **lambda .01 an interior optimum**. The
opponent arm worked mechanically -- 36% of the residual asymmetry removed -- and
bought nothing in points, exactly as a no-fit Phase 0 had sized it. Conversion
has not moved in five consecutive versions. `BACKLOG.md` 0ae carries the
do-not-re-run list; the open work is the two product standards that are NOT
accuracy problems: fixture magnitudes at validated scale, and a support measure
with dynamic range.

**Latest, 2026-09-08 (Opus): the workstream is assembled; read §15-§16 of
`TEAMMATE_INFLUENCE_EXPERIMENT.md` and `STRUCTURAL_MODEL.md`.** §14b/§14c found
the influence channels correlate 0.33-0.37 and that the WELL-measured ones lend
to the thin ones (rim share predicts a player's future turnover influence 92% as
well as his own turnover coefficient, 12/12 seasons, placebo dead). §15 built
that lender -- one factor over six coefficients, sampling variance recovered by
inverting each channel's own shrinkage. It rescues turnovers (r2 471->515,
calibration 0.434->~1.0, and in points MAE 8.1406 vs parent 8.1440 with every
metric moving right) and DAMAGES both rebound channels, so do not extend it
there. **But borrowed strength must be scored against the lender:** the improved
turnover coefficient correlates +0.518 with the shot-quality term and prices
-0.239 orthogonal to parent AND shot quality, so most of the rescue is shot
quality wearing a turnover hat.

§16 scores everything together. **Best three (location + shot quality + factor
turnover): MAE 8.1386, RMSE 10.8965, r2 0.11140, novel 8.8612** -- best RMSE, r2
and novel on record. Adding the MIX makes all four worse, confirming §13b's hold
on a fourth independent scoring. Location and shot quality are ORTHOGONAL
(-0.030) and genuinely add. Honest significance: novel vs parent -0.0298 +-
0.0194 with **9/11 seasons** (the one convincing comparison); pooled vs additive
+0.042 +- 0.033, still behind; novel vs additive -0.045 +- 0.074, NOT
established. Best pooled MAE is still shot quality ALONE at 8.1321. 606 tests
pass; no scorer or page change.

**Previous, 2026-09-08 (Opus): LOCATION-SPECIFIC CONVERSION WORKS.** Read
`TEAMMATE_INFLUENCE_EXPERIMENT.md` §12/§12b and `STRUCTURAL_MODEL.md`. §8j found
the model asserts a player's FG% is the same wherever he shoots (`self_2p` is a
scalar), which cancels the shot mix. §12 measures the replacement forward on 44
origins with the profile's own 730-day recency: **the current per-attempt
predictor is WORSE than ignoring the player and using the league's rate at that
bucket** -- Brier 0.2414 vs 0.2343, 12/12 seasons. Adding a per-player offset
reaches 0.2334; the player-BY-location interaction is real (-0.000323 +- 0.000020,
12/12) but an order of magnitude smaller.

§12b prices it as an EXACT making-term replacement, nested to 1.4e-14 (feed the
profile's scalar into all six buckets and the delta is zero). Best arm
`pbp_offset`: MAE 8.1428, RMSE **10.9120**, r2 **0.10888**, bias **-0.495**
(better than the parent's -0.680), novel 8.8812. With shot quality: MAE
**8.1374**, RMSE **10.9016**, r2 **0.11056** -- the best structural numbers on
record. Residual slope orthogonal to the parent **+0.635** (shot quality
+0.637), orthogonal to parent AND shot quality +0.641, 9/12 seasons; placebo
**+0.004**. **corr with the shot-quality term is -0.030**, so unlike turnover
influence (+0.435, §11d) this ADDS rather than re-prices.

Two lessons: the player-by-location interaction beats `offset` per attempt and
LOSES to it per lineup (+0.449 vs +0.635) -- aggregation kills it, ship
`offset`. And per-bucket conversion is necessary but NOT sufficient for a
lineup-dependent location effect: the mix is still each player's own history, so
**§8i's lineup-dependent mix is worth building now and was not before**. 589
tests pass; no scorer or page change.

**And §13/§13b: teammates DO move where you shoot, but it does not convert yet.**
Measured with §10's design, not §11's -- one ATTEMPT with a known shooter,
residual against the shooter's OWN mix, and only TEAMMATES' attempts counted, so
there is no own-rate artifact to strip. All six buckets forecast 12/12 seasons
on 2.66M held-out attempts; one sd of teammates moves a player's RIM SHARE by
**4.3 percentage points**. A parameterisation error was caught by the corner
three refusing to forecast (-0.077, 0/12): the model normalises `two_mix` and
`three_mix` SEPARATELY and gives the 2-vs-3 split to `r3pa`, so pooling the six
let "takes more threes" leak in. Fixed, all six forecast.
§13b demonstrates §8j on the SAME shift rather than arguing it: applied to the
parent's flat curve the mix moves the score **0.069 pts/100**, on the per-bucket
curve **1.230** -- eighteen times. But the mix term prices at slope **+0.185**
orthogonal to parent and location (8/12, placebo -0.086), about five times
over-scaled, and costs 0.019 MAE. Prior-only slope scaling recovers most of the
loss (MAE +0.0064 +- 0.0134) and with shot quality sets the best structural RMSE
**10.8986** and r2 **0.11106** on record -- but it does NOT calibrate the term,
it only shrinks it: the scaled slope falls to +0.120 (7/12) and the prior
estimate ranges -0.277 to +0.580, too unstable to be a calibration. **Ship
`location` (§12b), hold `location_mix`.** No arm dominates -- shot quality alone
has the best MAE 8.1321, the location family the best RMSE/r2/novel -- which is
§10c's point restated: this population resolves ~0.04 MAE and these are 0.005.
Next try conditioning the mix on `assisted`: a shot created for you is not one
you create. 596 tests pass.

**SHOT QUALITY IS MEASURABLE FROM THIS DATA (§10, Adam's test, 2026-09-08).**
The raw shot distance was always in the play-by-play and had never been kept;
`shot_quality.py` keeps it -- 6,846,563 attempts, distance on 100% of the
5,372,539 field goals, shooter matched on 98.9%. Isotonic FG% on distance, then
on/off residuals. **Jokic: the same shooters make +1.69 +- 0.36 pp more of their
field goals from the same distance with him on**, after shooter AND game fixed
effects, while the FREE-THROW placebo reads +0.38. The raw number is +4.80 and
is mostly personnel -- Denver's FT% is also +4.63 with him on, and a free throw
has no defender. Across 933 players the placebo's mean is +0.068 and its
correlation with the field-goal effect is +0.099, so the fixed effects do remove
the confound. Jokic is 4.5 true sd above the mean, 99.2nd percentile; Murray,
Baron Davis, Curry, Embiid, Wembanyama and Draymond follow. **True between-player
sd is only 0.396 pp with reliability 0.397**, so most of the spread is noise and
only extremes resolve. Worth ~2.2 pts/100 per percentage point, so ~0.86 for a
one-sd player -- comparable to the opponent and location levers and ENTIRELY
absent from a model that carries a fixed self_2p and self_3p. **IT FORECASTS (§10b).** Refitting the curve, the shooter
baselines and the coefficients strictly before each of 44 origins and predicting
the shots after: slope on the teammate term **1.082 +- 0.084, positive in 12/12
seasons**, over 2.66M out-of-sample field goals. Slope 1.0 means the shrinkage is
correctly calibrated. **Shrinkage is not optional** -- raw coefficients make the
Brier score WORSE (-27.3e-5), shrunk ones better (+7.07e-5); EB keeps 20% of the
raw field-goal spread and **1%** of the free-throw placebo's, having been told
nothing about which was which. Worth **0.91 pts/100 of lineup spread**, the same
order as the opponent lever and absent from the model. **Priced in points (§10c)**, it moves every metric the
right way -- MAE 8.1440 -> 8.1321, RMSE -0.017, r2 +0.0027, novel -0.016 -- with
the placebo identical to the parent and the UNSHRUNK version worse than nothing.
**The MAE gain is not established** (-0.0103 +- 0.0158). That calibrates the
evaluation rather than the mechanism: this population establishes a lever worth
~0.04 MAE (the opponent adjustment did, 9/11) and cannot establish one worth
~0.01 (on-floor influence and shot quality both). It forecasts -- settled at the
shot level on 2.66M attempts -- and prices correctly; whether it ships is a
mechanism judgement the point benchmark cannot make at this size.

**On-floor influence workstream, complete 2026-09-08 (Opus, at Adam's request):**
read `TEAMMATE_INFLUENCE_EXPERIMENT.md`; every section below is a numbered part
of it. The structural model now carries a per-player on-floor influence injected
through `asof_point_allocation` itself. MAE 8.1440 -> 8.1333, r2 0.1073 ->
0.1117; **the MAE gain is NOT established** and it does not close the corrected
additive's lead. The prior-only calibration prices the influence at c ~ 0.39 in
44/44 origins and the free-throw placebo at exactly 0 in 44/44.

**Additive versus structural is the wrong frame (§8b-8c).** The gap between them
IS on-floor influence, placebo-clean; transplanting it closes 21-38% of it. But
their forward errors correlate at **0.9856** and neither arm's score explains
the other's error (0.50% and 0.00% of what each explains), so they are REDUNDANT:
the whole prize from optimal ensembling is 0.15% of RMSE and a fixed 50/50
average nearly reaches it. Blend MAE 8.0763. **Do not look for further gains
from combination**; more accuracy needs information neither arm has.

**Opponent adjustment (§8d-8f), the one lever that paid.** Strength of defences
faced explains 14% of what either arm explains and neither uses it. Correcting
the TARGET at coefficient 1 (no fitting) removes 83% of it: blend 8.0763 ->
**8.0417**, r2 0.1219 -> 0.1276, novel 8.8668 -> 8.8229, 9/11 seasons. A fitted
kappa scores worse than kappa=1. `onfloor_influence_swap --opponent` prices a
five against a NAMED defence, which is the two-lineup product.

**Shot mix (§8g-8h): mechanism real, points null, and the reason is structural.**
Composition coefficients are basketball-legible -- rim pressure raises teammates'
three-point share, SPACING (Curry/Korver/Ray Allen/Dirk) raises rim share,
playmakers raise assisted share, which is spacing appearing in the shot-mix
channel where the points channel always read null. `onfloor_mix.py` makes the
mix lineup-dependent inside the allocation (reproduces the parent to 1e-12 at
zero shift) and it is NULL forward: best arm beats a permuted-identity placebo
by 0.0057 +- 0.0049. **The model prices moving one attempt from a two to a three
at 0.0137 points**, so that arm moved a channel worth nothing. **§8i then over-corrected, and
§8j corrects IT (2026-09-08).** §8i priced a long-two-to-rim move at +0.548 from
the VALUATION COLUMN ALONE. The model also carries a making term subtracting the
league make rate at the player's own locations, and the two nearly cancel.
Perturbing real profiles and re-scoring through `asof_point_allocation.predict`
itself: long mid -> rim is **+0.006 per attempt moved, not +0.548**, and mid ->
rim is NEGATIVE. The two-point score decomposes EXACTLY (2.2e-14) as
`2*2PA*self_2p + sum_b 2PA_b*(value_b - 2*pct_b)`; the first term has no mix in
it, so location reaches the score only through the spread of the second, which
is **0.079** against the valuation's 0.548. **The mix is 90% priced out by
construction, so a lineup-dependent mix is a null before it is built**, and
§8i's 1.354 pts/100 sizing uses the same valuation-only arithmetic. THE REAL
DEFECT: `self_2p` is ONE NUMBER per player, so the model asserts a man converts
a rim attempt and a long two at the same personal rate. Next build is
**location-specific conversion** (`self_2p_rim/_paint/_mid/_longmid`,
`self_3p_c3/_ab3`), making a long-two-to-rim move worth
`2*(self_2p_rim - self_2p_longmid)` ~ +0.54, EARNED by the player's own skill.
Data is cached: `shot_quality.build()` has 5,372,539 field goals, distance 100%,
shooter 98.9%. Tracking data remains unnecessary for this.

**Defence is scored (§9)** on a population built for it, 8,340 fives / 1,010,779
possessions: additive defensive half 8.3398 and influence channels 8.3984
against a league null of 8.6219, both 11/11 seasons, defensive FT placebo
identical to the null to 1.6e-16. Caruso/Thybulle/Tony Allen top turnovers
forced; Wembanyama/Holmgren/Gobert top two-point suppression. Roughly a third
the effect size of the offensive side.

**Two identification failures are recorded, not hidden (§7, §8, §8g):** a smooth
role control does not transfer forward; the own/teammate split identifies ONLY
for two-point conversion (91% on the other four, placebo 88% the other way) and
not for volume (zero-sum inside a lineup) or composition (the teammate block is
better conditioned and the selector annihilates the own block). 559 tests pass.
No scorer or page change; no completed run directory touched.

**Latest continuation, 2026-09-08:** the four factors are now measured as
INFLUENCE, per opportunity, in `TEAMMATE_INFLUENCE_EXPERIMENT.md` §10-§11c. The
structural profile carries only `rtov`/`rorb` as own per-possession rates and no
`stl`/`drb`/`blk`/fouls, and is offence-only. Five channels forecast forward
(44 origins, strictly prior, EB shrunk). **The load-bearing test is
`channel_influence_orth`:** a coefficient linear in the man's OWN rate is an
accounting correction to a mis-specified additive expectation, because rebounds
are competitive; raw defensive rebounding scores 1.210 with 12/12 seasons and an
inverted face list. Orthogonal slopes: turnover 0.434 ± 0.024, def rebound
0.908 ± 0.037, off rebound 1.031 ± 0.264, steal 0.512 ± 0.100, FT rate
0.271 ± 0.014. Turnovers are the one clean, face-valid channel; the rebound channels need a
contested-rebound expectation; FT rate has an open garbage-time confound.
**PRICED IN POINTS (§11d), turnover influence does NOT convert.** The
forward slope IS the calibration factor -- 0.434 means 2.3x too large, and
the point calibration `b` cannot rescale one term inside the score; a
prior-only refit lands at 0.431. Scaled, MAE is +0.0025 +- 0.0150 and shot
quality alone (8.1321) beats turnover-plus-shot-quality (8.1394). The parent
residual's slope on the term is **-0.028 once what the parent already prices
is removed** (shot quality reads +0.637), and 5/12 seasons positive. The
player-level ATTRIBUTION is new; the lineup TOTAL is not, and points see only
the total. Recorded, not shipped. Two pre-registered predictions did hold:
orthogonal beats un-orthogonalised, and both beat a permuted-identity placebo. Separately, §6's point-residual turnover channel
correlates −0.003 with the direct count fit at identical spread: **fit a
mechanism on its own events, then price it -- and believe neither the channel
forecast nor the point score alone.** 582 tests pass; no data, scorer or
page change.

**Previous continuation, 2026-09-08:** the full48-origin experiment, additive
offensive-reference fix, complete saved-fit replay and disagreement review are
DONE. Read `ASOF_ADDITIVE_REFERENCE_RESULTS.md` and the latest handoff. Corrected
additive MAE8.0920 versus structural8.1461; pooled r² .12043/.10719. MAE gap is
small/inconclusive across seasons; additive ranking/squared-error advantage is
more consistent, while novel-lineup errors remain tied. The three standards are
unchanged. All530 tests and real audits pass; no jobs or workers remain. No
refits, source changes or scorer/page promotion. Do not rerun completed work.
Use the new centered scoring helper for future comparisons; the original
benchmark is frozen bug evidence, not a valid unanchored offensive comparator.
Next separate count versus conversion/valuation failures in the new high-exposure
review, then choose one role-response experiment. Original run and both protocol
documents are pinned; put new results in separate docs.

**Previous continuation, 2026-09-07:** the **quarterly point runner is working**.
Read `ASOF_POINT_BENCHMARK_STATUS.md` and
the latest handoff first. 2015 Q1/Q2 real warmup origins complete in 61.59/65.01s;
all 267 cells / 36,380 possessions retained across 50 arms. Resume preserved
all Q1 files, independent arithmetic/provenance checks pass, and 515 tests pass.
At handoff there is no primary-season result or production/data change.
Adam will self-run **all remaining origins** via `experiments.asof_point_run.py`;
the STATUS document has background/live-log commands. Seven additional focused
launcher tests and a saved-result preview pass; no new fit was started by the
assistant. Check the run's log/manifest before starting anything on return.
The next deliverable is predictive results, not another infrastructure batch.
Do not edit the pinned `ASOF_POINT_BENCHMARK.md` to append results; use its STATUS
document. The existing run and scientific code hashes are unchanged.

**Previous continuation, 2026-09-07:** the additive prior-edge follow-up and
structural point-accounting bridge are complete. The sensitivity changes
predictions <=0.000495 pts/100; retain prior=1 with original grid flags intact.
`ASOF_POINT_INTEGRATION.md` specifies and implements within-category allocation,
recomputing shooting and assisted demand from the same attempts. All saved
cells reconstruct, no exclusions; 446 tests pass. No actual point comparison
yet. Next build the resumable quarter point runner with explicit shared
calibration/league controls and per-origin tuning checks, not another channel
audit. All jobs finished; scorer/page/source data unchanged. Read the latest
handoff for Adam's explicit Anthropic worker-content authorization and details.

**Previous continuation, 2026-09-07:** `ASOF_ADDITIVE_TUNING.md` implements the
quarter-matched selector; one real 2026 Q3 pilot completed 5,760 candidates and
the January 15 refit in 253.7s. No target score. Prior-penalty low edge remains;
last grid change is 0.004438 pts/100, so tuning stays provisional. 387 tests
and independent artifact checks pass; all jobs complete, scorer/page/data
unchanged. Next is the document's pre-specified 90-second one-axis sensitivity
(not yet run), then explicit player/location accounting and matched league/
calibration controls for the quarter point factorial. Do not repeat the pilot
or launch the 44-origin sweep from this checkpoint.

**Previous continuation, 2026-09-07:** `ASOF_ADDITIVE_FOUNDATION.md` is complete.
The chemistry-free additive fitting helper now supports strict date cutoffs,
prefix-only normalization/profiles and short current-season delta blocks.
No new estimator or tuned point comparison yet. 318 tests pass; a bounded
24-game smoke is invariant to later-data mutations. All jobs complete; no
scorer, page, source data or existing result changes. Next: prior-window
penalty/carry selection and the quarter point factorial, with explicit
player/location accounting and matched league/calibration controls.

**Previous continuation, 2026-09-06:** `ASOF_OPPORTUNITY_EXPERIMENT.md` is complete.
Prior-only joint share calibration improves recent180 FTA MAE 6.366→5.195 and
3PA 4.630→4.286 (both 11/11 seasons), with a tiny TO MAE loss 2.483→2.491.
FTA bias +3.351→−0.171; recent365 confirms the broad result. This is generic
calibration on recurring lineups, not teammate synergy or a point-score result.
278 tests pass; no jobs remain; scorer/page/source data unchanged. Retain both
raw/calibrated controls. Next: quarter point factorial with explicit player/
location accounting and equally refreshed chemistry-free additive comparison.

**Deployment checkpoint, 2026-09-06:** `ASOF_DEPLOYMENT_AUDIT.md` is complete.
Common fives overrepresent Q1/Q3 and have fewer FTs; coarse clock/score mix
reduces the full/common descriptive FTA gap from 2.228 to 1.037/100. This is
not a causal explanation or a correction for forecasts. All 5,607 cells
reproduce; 245 tests pass; no jobs remain. Read the latest handoff, then
`ASOF_OPPORTUNITY_EXPERIMENT.md` for the now-completed prior-only joint-share
calibration control. Keep empirical calibration distinct from
complementarity. Quarter point factorial and equally fresh additive remain
owed. No scorer, page, database, or source-cache change.

> **Direction agreed 2026-09-03:** forward prediction, basketball-coherent
> counterfactuals, and out-of-distribution calibration are co-equal standards.
> A small loss in forward r² is acceptable for material gains in either of the
> other two. The product should compare two five-man lineups (Team B defaults
> to league average), default each player to his latest season, expose
> mechanism-level explanations, and return wider data-driven uncertainty
> outside support rather than refuse to answer. Known-pair chemistry is off in
> the primary model; it may return only as a clearly labeled observed-history
> residual if it improves accuracy without weakening the other standards.

**Current checkpoint, 2026-09-04:** the 2,492-game update is complete and
database-verified; caches and offensive evaluations are refreshed through
2025-26. The assist-deficit mechanism improves forward MAE from 7.600 to 7.497
pts/100 over calibration alone. Latest-season state is roughly tied with
cumulative state (7.474 versus 7.497), and its held-out finite-batch intervals
cover 50.2/79.8/95.1% at nominal 50/80/95%. These are not verified intervals
for impossible lineups' latent means. Haliburton's same-four mechanism check
is complete; the Pacers team audit covers only 44.9% of all possessions.
Read `SESSION_HANDOFF.md` §15–18 before starting another run. Next: isolated
rebounding/opportunity-budget coherence, thin-history state coverage, then
remaining uncertainty and defense. The HTML is still the incumbent.

**Reporting correction:** historical contextual `truth_rho` headlines averaged
unstable split-wise ratios. Refreshed point/state reports pool covariance and
variance first and flag impossible ratios; old rho levels are superseded, not
directly comparable. MAE, ordinary correlation, raw r² and fitted means were
unaffected by that reporting fix. See `RESEARCH_OVERVIEW.md` §39.

**2026-09-05 continuation:** read `REBOUND_EXPERIMENT.md` before further rebound
work. Three experiments are complete. Miss-conditioned capture with competition
improves rebound prediction and independent coherence, but latest-state point
MAE is 7.528 versus accepted 7.474, and five centers still score about 117.
The full offensive counterfactual is not solved; the scorer is unchanged.
Next investigate team-rebound residuals and shot/creation-role transport, not
another rebound penalty or an arbitrary ORB% cap. Adam's examples and review
are recorded with useful concerns and factual qualifications. 107 tests pass.

**Creation continuation, 2026-09-05:** `CREATION_EXPERIMENT.md` records two
completed prior-only intermediate tests. Teammate passing support adds signal
for assisted-made share (Brier improves 11/11 seasons) and modestly for
turnovers; shooting improvements are not established. A softmax repair fixes
the linear shot-mix probability boundary failure. Workload improves shot-mix
cross-entropy 10/11 seasons; extra passing beyond workload remains inconclusive.
Coverage is only 36.7% of player-possession exposure. No point-scorer promotion,
named-player bonus or OOD claim. Next: matched pre-origin additive/structural
benchmark, then supported channel transport with explicit accounting. Read
the experiment's decisions before any new sweep. 119 tests pass; no jobs run.

**Latest, matched benchmark completed 2026-09-05:** read
`MATCHED_BENCHMARK.md` and `SESSION_HANDOFF.md` §20. Same future lineups and
raw-point targets: chemistry-free additive MAE 7.454 versus structural 7.474,
no established gap; ordinary correlation 0.252 versus 0.205, additive higher
10/11 seasons. The pattern persists on novel lineups and the shared league-
offset sensitivity. Adding deficit to the additive core does not improve it.
The structural control reproduces to <1e-15. Residual finite tuning boundaries
move estimates <0.000025 pts/100 when expanded further. Coverage is 32.22% of
future possessions. Both finite-half interval methods calibrate similarly;
latent/OOD means remain unverified. Preserve both controls and investigate
their quality-prediction disagreements before integrating supported mechanisms.
128 tests pass; all benchmark jobs finished; scorer/HTML unchanged.

**Latest diagnostic review, 2026-09-05:** `DISAGREEMENT_AUDIT.md` and
`reports/matched_disagreement_review.md` answer Adam's request for high-exposure
failure cases with exact additive player coefficients and structural ledgers.
258 cells qualify at >=500 possessions / 20 games. All top-six gaps persist in
both chronological halves, but most descriptive individual gap intervals
include zero. Assist deficit is zero in all six. Across all 258, FTA bias is
+4.87/100 (11/11 seasons positive), and 3PA is underpredicted. Same-five repeats
include a Denver reversal favoring structural. Discuss before naming causes;
audit FTA/3PA accounting/transport next. Corner-shot labels are distance proxies,
not x/y locations. 134 tests pass; no scorer/page/source-benchmark changes.

**Latest as-of-date milestone, 2026-09-05:** Adam approved current league
conditions, fresher player states and intraseason evaluation. Read
`ASOF_MODEL_EXPERIMENT.md`. Strict-date snapshots, correct weighted effective
exposures and causal quarter/eighth starts are implemented. The quarter-only
intermediate run is complete: refreshing the same weighted player profiles
improves 3PA in 11/11 seasons (recent-180 paired MAE −0.461 ± 0.063), with
modest TO gains. FTA bias persists. Updating only league usage worsens shot
counts; full era-aware valuation/mix is still pending, as are point-score
evaluation and an equally refreshed additive control. No OOD/role-adaptation
claim or bandwidth promotion. 147 tests pass; no running jobs; scorer unchanged.

**Latest, 2026-09-06:** `ASOF_ACCOUNTING_AUDIT.md` records the completed
date-aware league valuation and matched raw/EB accounting diagnostic. FTA bias
stays +3.351 → +3.348/100 with raw counts; removing shrinkage worsens 3PA/TO
MAE 11/11 seasons. Keep EB. Recent league 3PA share is 40.77% versus the legacy
28.36% at the 2025–26 fourth-quarter cutoff; input drift is not a point-score
gain. A post-hoc population check finds 22.58 FTA/100 in all possessions versus
20.36 in matched evaluation cells (gap positive 11/11), not a causal explanation
or an authorized mean correction. Next: joint opportunity mix with prior-only
league/deployment reference, then the point factorial and equally refreshed
additive. Lead repaired worker integration defects before the real run;
192 tests pass, all jobs complete, scorer/page/data unchanged.

## The northstar

**A tool that compares any two theoretical five-man lineups** — including
lineups that have never played — in points per 100 possessions, explains the
basketball mechanisms behind the estimate, and reports honest uncertainty.
Team B may be a league-average placeholder. The incumbent one-lineup baseline
exists at `tool/five.html`, published at
https://claude.ai/code/artifact/02d5d0e3-d698-495f-97ce-af20074cf1f3

Everything else is in service of that. Concretely it means:

- **A model must be able to price a lineup it has never seen.** This is the
  constraint that rules out trees, and the reason the `novel_off5` slice matters
  more than `all`.
- **Both sides of the ball ship**, even where the best defensive model is one
  coefficient per player. A tool that only rates offense is not the tool.
- **Broadly understandable output.** Points per 100 possessions, not r².
  "This unit generates 3 more rim attempts per 100" beats a coefficient.
- **Incumbent 5-Shaq workaround — not the accepted contextual solution.** A user
  must not be able to break the tool by typing in five Shaquille O'Neals and
  being told it is the best lineup of all time. Refusing to answer is not
  gracefulness; the requirement is a NUMBER that is sane.

  Three things settled it. **First, it had been argued about in the wrong
  units.** Every number on the record came from `five_shaq_audit.py`, which
  prices with the RAW additive model; the page prints something else.
  `tool_audit.py` reimplements the page's own arithmetic and prices all 18,071
  real units the same way (`RESEARCH_OVERVIEW.md` §20). **Second, the failure
  is REPETITION, not excellence.** The five best DISTINCT offensive players
  print +16.04 against a real maximum of +17.24, which is a defensible answer;
  five Jokićs printed +26.26. The raw duplication curve is exactly linear in
  the number of copies. **Third, no fitted structure can supply the fix, in
  principle.** Four have been tried — floor geometry, index curvature,
  defensive coverage, usage conservation — and the two with clean controlled
  forward signal both extrapolate the WRONG way, because lineups are selected
  on the outcome: a coach fields an unusual five only when it works, so in
  range "unusual" correlates with "good" and every fit inherits that sign
  (§20.5). `distance_shrink.py` had already shown the schedule cannot be fitted
  on this corpus; selection says it cannot be fitted from observational lineup
  data at all, and names the direction of the bias.

  So the incumbent tool ships a **coverage gate**: a five's rating is scaled by its
  internal variety in play style, height and position, exactly 1.00 above the
  1st percentile of real units, with a floor set so the worst five-copy lineup
  lands at the 99th percentile rather than above everything ever played.
  **Cost in range, measured rather than argued: of 18,071 real units 1.00%
  move at all and the mean absolute change is 0.0012 pts/100.** Five Jokićs
  now print +14.34, below the death lineup's +18.47. The page says in its own
  words that this one number is asserted and why.

  What it does NOT do is apply a blanket cap to five distinct specialists. The
  best distinct offensive five prints +20.75 against a real max of +21.64 and
  is untouched. The best distinct defensive five prints +18.64 after the
  position-ends portion of the coverage rule recognizes that it lacks a guard.

- **Honest error bars are part of the deliverable, not a caveat.** The
  incumbent horizon-0 shrink is 0.61 offense and 0.70 defence. Its existing
  global interval is not the finished answer: the contextual model must widen
  uncertainty as a lineup moves outside observed role and composition support.
  A number the data cannot support must not be printed as if it can.

A research result that cannot reach the tool is worth less than one that can.
When choosing what to work on, prefer whatever moves a lineup's number or its
error bar.

**One-line state of the project:** the additive (linear) model was always the
bigger half — its measured ceiling is +0.002759 r², we reach +0.002334, and the
whole non-additive/synergy budget is +0.00017 on top. **Those are RANDOM-SPLIT
numbers and the headroom they imply is roughly double the real one:** measured
forward on the same rig the gap is +0.000262 rather than +0.000499, and the
α→0 limit that defines a "ceiling" is not readable forward at all
(`RESEARCH_OVERVIEW.md` §26). Better estimation of β is worth about half what
the record says; freshness keeps its standing. The largest lever found
since the debut-year data fix is on that additive side and needed no new
modelling: **height and position in the box-score prior, +0.000043 forward on
the full stack (t=+3.88, 13/16), +0.000028 against a fresh baseline** —
`RESEARCH_OVERVIEW.md` §21. It ships, and the full additive stack measured
season-ahead with it is **+0.001799** (`fwd_exp_shared.csv`, 16/16 origins).

On the non-additive side, three things reach the budget
forward, all measured against a baseline at most a quarter-season stale
(`fractional_pairs.py`, 45 origins): **free teammate pairs +0.000034**
(t=+3.98), **usage demand +0.000007** (t=+4.03) and **floor geometry +0.000008**
(t=+3.50) — but geometry must not be shipped: it helps accuracy and breaks the
5-Shaq rule, and no sign-constrained subset of it predicts anything (§18.3).
Everything built on the profile bilinear is a powered null at every width and
sparsity, including a jointly-fitted quadratic prior and a flexible
random-feature pair function.

**The one thing to know before trusting any interaction number:** give the
baseline THIS season's δ and free pairs fall to +0.000005 (t=+0.60) alone, and
to −0.000004 (t=−0.49) measured over usage demand — while usage demand itself
survives at +0.000006 (t=+2.48). Measured chemistry is largely the same
information as "both players are playing well this year"; the conservation
constraint is not (`RESEARCH_OVERVIEW.md` §19.4–19.5). Caveat: with δ on, the
block sits on a partly in-sample residual, so all of these are lower bounds —
the ORDERING is the finding, not the levels.

---

## Environment

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python      # ALWAYS this interpreter
```

The base interpreter cannot unpickle the numpy-2 possession caches. Postgres
must be running: `dbname=local user=adam password=<redacted>`, schema `nba`
(`possessions`, `games`, `players`).

Everything is run as a module from the repo root:

```bash
cd /Users/adam/Documents/basketball
/Users/adam/miniconda3/envs/basketball25/bin/python -u experiments/additive_stack.py --seeds 3
```

**Always `-u`.** Piped Python stdout is block-buffered; without it a live job
looks hung for minutes. Long jobs: `nohup ... > log 2>&1 & disown`, then poll
the log in a *separate* command — a wait whose timeout fires SIGTERMs the whole
process group and kills the job.

**Do not wait with `pgrep -f <pattern>`** where the waiter's own command line
contains the pattern: it matches itself and hangs forever. Wait on the PID
(`while kill -0 $PID; do sleep 20; done`). Hit five times now, twice on
2026-09-02 in waiters written hours after this line was added — the pattern
sneaks in through the log path, not just the process name. Two further rules
earned the same night: a log sentinel is only durable if nothing later truncates
that log with `>`, and every waiter should be BOUNDED (`for i in $(seq 60)`, not
`until`) so the worst case is a stale check rather than an immortal shell.

Runtimes on this machine: full-corpus (5.57M possessions) Gram-based fits are
1–6 minutes; anything with an α-sweep over season blocks is 3–8 minutes.
Apparent per-step slowdowns in a long job are usually laptop sleep — compare
CPU time to elapsed before killing anything.

---

## The rules of evidence

This project has repeatedly been fooled. These are non-negotiable.

1. **Route every claim through a cross-fit or the harness.** A bespoke script
   missing the per-(season,week) detrend once produced t=+16.91 where the truth
   was +0.72.
1b. **Rank levers forward-in-time, never on a random game split.** A random
   split hands any (player, season) parameter the answer for the season it is
   scored on, and simultaneously makes shared structure look redundant.
   Time-varying delta read +0.000099 that way and is +0.000000 forward. Use
   `forward_eval.py`. Random splits are for variance components only.
2. **Effects here are ~10⁻⁴ r².** That is not failure, it is the scale of the
   phenomenon. Report with a standard error, always.
3. **Fold-level t-stats overstate significance.** Folds share training data and
   adjacent test weeks. A fold-level t=+3.3 was p=0.06 at the window level.
   Seeds that share a corpus and differ only in the split are the same trap.
4. **A point estimate ≈ 0 *and* a sem ≈ 0 means over-shrinkage, not absence.**
   Pin the penalty and re-check before concluding null.
5. **Selection noise vs. real effect:** if a variant loses on *validation* too,
   it is not selection noise — it is a bug or a genuine loss. Check which.
6. **5 folds is screening only.** A 5-fold t=+2.35 collapsed to +0.30 at 10.
7. **Never write a memory from a partial run.** A 6-fold interim said
   "capacity hurts, t=−2.78"; the full 10 folds said t=−0.96, not significant.
8. **Measure the ceiling before building the model.** Phases 1–7 spent months
   inside a budget nobody had measured.
9. **Refit the upstream model inside the split.** When two estimates of the
   same quantity are compared across a split, everything upstream must be
   fitted inside it. One global additive fit biased pair reliability from 0.25
   down to 0.08, and turned it to −0.14 with per-season δ on: the global model
   absorbs each half's noise and returns it with the opposite sign.
10. **A control arm on a grid boundary is not a control.** A nested control must
   be free to absorb everything the arm above it could; cap its capacity and the
   difference stops being "the new structure" and becomes "the new structure
   plus what the control was not allowed to reach." This inflated a pair result
   2x on four configurations. Prove interiority by widening the grid TWICE and
   getting the same answer.
11. **A mask handed to `_cells` is per-POSSESSION; a mask handed to `_design`
   is per-CELL.** Converting is always `cell_mask[code]`, never
   `poss_mask[code]` — `code` holds cell indices, so the wrong one silently
   reads the first n_cells possessions, which are all from 2002-03, all inside
   every fit window, and the mask comes back 100% True. That leaked the test
   seasons into the sparse bilinear's BASIS SELECTION and was worth 95% of
   what was then the project's live lead (+0.0000153 → +0.0000008). The fit
   and the scoring were both clean, which is why "is this forward?" passed:
   **check the selection step too.** It was caught because two rigs disagreed
   on the same protocol — a gap between two implementations of one quantity is
   evidence, not noise.
12. **A DEFAULT penalty grid is un-audited until some run has walked off it.**
   `forward_pairs --lam-cr` defaulted to a floor of 1e5 while the usage-demand
   block wants 0 to 100; run on the default, a +0.0000103 (t=+4.99) effect
   reads +0.0000000 (t=+2.09). Every published run happened to pass an explicit
   widened grid, so nothing on the record was damaged — which is the point: a
   hand-passed grid is visible in the command line and in the write-up, and a
   default is visible in neither. Print the selected penalty against BOTH ends
   every run. This is rule 10's fourth appearance in three sessions.
13. **When two implementations of one quantity disagree, run the CONTROL before
   assuming the new code is at fault.** Re-running the OLD flag alone on the
   NEW code localised the grid bug above in a single run, by reproducing the
   failure and so exonerating everything new.
14. **Before paying for a fresh-baseline re-fit, score the test season in
   quarters.** `slice_horizon.py` holds one fit constant and reads the arm gain
   per quarter: a composition effect is flat in the slice index, a block that
   is really re-levelling a drifted baseline rises. It costs one extra scoring
   pass and it correctly predicted all four outcomes that the expensive
   `fractional_pairs.py` re-fit later confirmed.

---

## The measurement toolkit (this is the valuable part)

| module | what it measures |
|---|---|
| `lineup_variance.py` | non-additive lineup ceiling, four-way game-disjoint cross-fit |
| `additive_ceiling.py` | the **linear** ceiling, and how much of it ridge reaches |
| `timevarying_ceiling.py` | the ceiling once coefficients may vary by season |
| `channel_ceiling.py` | which outcome channel the non-additive effect lives in |
| `lineup_scoreboard.py` | the **product** metric: ρ with true lineup quality, calibration slope, top-k lift |
| `basis_screen.py` | ~10s screen of a candidate basis, in harness units |
| `forward_eval.py` | **the** lever ranking: rolling-origin, fit < T, score T |
| `forward_pairs.py` | free teammate pairs forward, with the un-shrinking control |
| `pair_readout.py` | what a pair effect is made of: team control, bilinear R², faces |
| `lineup_uncertainty.py` | posterior covariance of the ratings; per-lineup error bars |
| `usage_load_response.py` | prior-composition load versus held-out player-game role and efficiency |
| `role_support_validation.py` | whether assigned-role distance orders persistent lineup error |
| `role_allocation_validation.py` | direct held-out test of who consumes a fixed team usage total |
| `role_channel_validation.py` | direct assignment for FGA, 3PA, turnovers, assists and creation/finishing roles |
| `channel_totals_validation.py` | whether prior profiles predict held-out lineup opportunity totals |
| `channel_points_validation.py` | training-only shot creation + separate making versus the box-score point identity |
| `assist_residual_validation.py` | prior-only, sign-constrained point cost of assisted demand beyond passing supply |
| `structural_counterfactuals.py` | Jokić swap, five-center/guard and repeated-player offensive stress panel |
| `context_profile.py` | whether teammate context bends the box-score profile (placebo: `ft_pct`) |
| `slice_horizon.py` | **composition or staleness?** one fit, scored per quarter of the test season. Cheap; run it FIRST |
| `fractional_pairs.py` | the same blocks against a FRESH baseline: fit through slice j−1, score slice j, 45 origins |
| `distance_shrink.py` | whether the calibration slope decays with distance from the support (it does not) |
| `five_shaq_audit.py` | what the model actually says about a degenerate lineup, in pts/100, every block on |
| `nonlinear_prior.py` | is the box-score → value map nonlinear? (the SELF basis, fitted jointly) |
| `page_calibration.py` | **the only end-to-end check on the tool**: is what `five.html` PRINTS calibrated, and does the top-3 decision lift improve? Run it after any change to the page's arithmetic |
| `era_comparability.py` | is a +5 in 2003 a +5 in 2024? (the cross-era premise the tool rests on) |
| `tool_audit.py` | **what the TOOL actually prints**, reimplementing `five.html`'s own arithmetic on its own data, against every real five-man unit. Run it before arguing about the 5-Shaq rule |
| `tool_safety.py` | the duplication gate: its shape, its floor, and its cost on 18,071 real units |
| `shrink_by_role.py` | is one ridge penalty right for every player? τ² of the prior residual by role, split-half |
| `index_curvature.py` | curvature in the lineup total — **run it per side**, the pooled arm hides a clean split |

**The core trick, used everywhere.** A lineup's prediction is constant across
its possessions, so naive designs manufacture the answer: score both halves
with one β and the shared error lands in both with the same sign (biased up);
score half A with β fit on B and B's absorbed noise returns with a minus sign
(biased down — measured ρ=−0.12). The fix is a **four-way game-disjoint split**:
fit β₁ on F1 and β₂ on F2, score E1 with β₁ and E2 with β₂, then
cov(m₁,m₂) is clean. Split by *game*, never by possession — possessions in one
game share the opponent's game plan, rest and pace.

The estimator is validated: −0.000049 (t=−0.53) on a synthetic null over 10
seeds, and recovers a known effect to 4% at the operating scale.

---

## Model code

`additive_stack.py` is the current best model and the one to build on:

```
theta_{p,s} = Z_p gamma + beta_p + delta_{p,s}   +   eta_{experience bin}
              box-score    career   this season      shared career-stage curve
```

Four separately-penalised blocks; every corner is nested (send a penalty to
1e18 and that block disappears), so comparisons are one argument wide.

**Why it is fast.** A player-season column is nonzero only inside its season, so
`X'X` is *exactly block diagonal by season*. The Schur complement collapses via
`G − G D⁻¹ G = α_d G D⁻¹` into a 4,886² assembly instead of 30,000². Exact, not
iterative, no CG tolerance to argue about. `G_{A∪B} = G_A + G_B` also makes the
double-data fit free, which is how the ceiling extrapolation was *verified*
rather than assumed.

Other live modules: `prior_ridge.py` (box-score prior, `raw_profile`,
`profile_matrix`), `experience_curve.py`, `synergy_decomp.py` (LIN/SELF/CROSS),
`export_ratings.py` (writes the tool's JSON), `possession_outcomes.py`
(play-by-play → outcome channels).

`forward_pairs.py` carries every composition block behind a flag, all nested
over the same free-per-player un-shrinking control: `--demand` (usage
conservation), `--geom` (shot-map geometry, `--geom-cols` to subset it,
`--geom-shuffle` for its placebo), `--coverage` (height/position spread),
`--named`, `--cross [--cross-topk]`, `--cont`, `--rff`. `--with-demand` and
`--cross-pair` stack two of them so one is measured OVER the other rather than
beside it.

**Gotcha — recency and era were one knob.** `profile_matrix` set `era=True`
whenever a `halflife` was given, so every recency number ever measured was
era-adjustment-plus-decay — and the two point opposite ways. Pass
`zscore=False` (or `--profile-no-era`) for decay alone. Era alone costs the
prior −0.000081 paired; decay alone gains **+0.000068 at a 0.4-season
half-life** (t=+3.47, 14/16), an interior optimum. A knob that bundles two
changes measures neither.

**Gotcha — shared bases.** `profile_matrix` orthonormalises by SVD *per call*.
If several profile matrices are meant to share one γ, they must all be pushed
through **one** rotation (pass `rmap=`, or build with `raw_profile`). Getting
this wrong cost −0.000197 and looked like a real finding.

---

## Conventions

- Target is always detrended by (season, week) league mean, then home/away
  residualised. Skipping either invents signal.
- Slices: `all`, `novel_off5`, `novel_def5`, `novel_10`. `novel_*` = the five-man
  set never appeared in training — the extrapolation the project cares about.
- Penalties are selected on a held-out set and evaluated on a third disjoint
  set. **Nothing with a pinned penalty is deployable.**
- `experiments/cache/*.pkl` are large possession caches; `*.csv` are results.
  Both survive compaction and are worth reading before re-running anything.
- The source database ended at 2024-11-10 before the 2026-09-04 update.
  `experiments/bref_ingest.py` is the only supported updater; do not rerun the
  non-atomic `scrape_br.ipynb`. It is rate-limited, page-cached and resumable.
  The update and cache rebuild are complete: 32,190 games, 6,059,380
  possessions, latest game 2026-06-13. `bref_audit --verify-saved` checks all
  2,492 updated games without network access. Do not repeat the refresh.
- Scratch scripts go in the session scratchpad, not the repo.

---

## The design on the table

**`CONTEXTUAL_MODEL.md`** is the active contract. Its first prototype separates
the total lineup rating from the context adjustment: Jokić plus Westbrook may
still rate above Jokić plus Korver because Westbrook is the stronger individual
player, while the Westbrook pairing should be adjusted downward relative to
its additive expectation and the Korver pairing upward.

**`ROLE_MODEL.md`** is an earlier supporting proposal. Basketball has roles
that must be filled, so a player's profile confounds what he is good at with
what he was asked to do; the same lineup variation that contaminates the
profile identifies aptitude. Three stages — aptitude, assignment, value at the
assigned role — were proposed so that a five of centres is penalised because
the model hands one of them 30% usage and prices a centre there.

Two reasons it is worth the build rather than an eighth composition feature.
It **factors into a well-identified part and a hard part**: the assignment is
directly observed on 5.6M possessions, not fitted on a 1e-4 residual. And a
hierarchical treatment makes **graceful degradation derived rather than
asserted** — the posterior reverts to the prior exactly where there is no data,
which is what the coverage gate currently asserts and what `distance_shrink.py`
could not fit.

The context projection work now supplies a narrower first path. Follow the
kill-test sequence in `CONTEXTUAL_MODEL.md` §6 before committing to the full
role-model build.

That path now has a viable offensive mean. Direct held-out allocation selects
alpha 1, intermediate shot/rebound/turnover channels forecast, and a
training-only creation + making score is essentially tied with the box-score
point benchmark. A separately measured assist-deficit residual improves
ordinary ranking correlation in 10/11 refreshed future origins. Latest-state
five Goberts scores 106.69 without the coverage gate, with a deliberately
wide diagnostic interval. Held-out finite-batch interval coverage and the
Haliburton mechanism check are now measured; latent/OOD coverage,
valuation uncertainty, complete player coverage and defense remain open.
Use `CONTEXTUAL_MODEL.md` and `SESSION_HANDOFF.md` for current results, not
historical rho headlines or the unchanged HTML.

## What to work on next

`BACKLOG.md` is the running list of open questions, unrun experiments and
observations worth chasing, each with why it matters and what would settle
it. It also has a **do-not-re-run** section; check it before starting
anything, because several attractive-looking ideas are already closed.

## Where things stand

Read `SESSION_HANDOFF.md` first. The old `memory/phase9_summary.md` and
`phase8_summary.md` references are not present in this checkout.
Phase 10 (teammate context) is `RESEARCH_OVERVIEW.md` §10. The research
memo is `RESEARCH_OVERVIEW.md` (§8 = the non-additive ceiling, §9 = the linear
ceiling and the current model).

The tool lives in `tool/` — `five.html` (the page), `build.py` (re-inject a
fresh ratings export), `README.md` (how to rebuild and republish to the same
URL). Republish to the EXISTING url or the user's link breaks.

**`CURRENT_MODEL.md` is the single-file answer to "what is the model and what
is each term worth"** for the ADDITIVE model in `tool/five.html`, and
**`STRUCTURAL_MODEL.md` is its counterpart for the structural arm** -- the five
pipeline stages with file references, what every arm scores on the centered
population, what each mechanism is worth in pts/100, what is deliberately absent,
and the six honest weaknesses. Keep both current when a lever moves; each has a
provenance table tying every number to a module and a cached result.

Read `RESEARCH_OVERVIEW.md` §17 (the staleness caveat, discharged), §18 (floor
geometry, and predicting vs extrapolating) and §19 (the fresh-baseline
re-grade) for the incumbent model's frontier, then `BACKLOG.md` §0ac and
`CONTEXTUAL_MODEL.md` for what to do next. The tracked artifact currently uses
known-pair chemistry, usage demand, the asserted coverage gate, and horizon-0
shrink (0.61 offense / 0.70 defence). Those describe the baseline to beat, not
the intended final representation of complementarity or uncertainty.
