# v15 — actual opponents, without moving the offensive goalposts

Registered 2026-09-17, before new fits. Codex implements directly. This is a
research experiment, not scorer promotion. Existing artifacts remain read-only.

## Question and scope

Can the actual opposing five improve the successful offensive model, and does
profile-based matchup response add value beyond an ordinary defensive main
effect? Preserve the three co-equal standards in CONTEXTUAL_MODEL.md. This is
the first opponent-conditioned NN experiment, **not** a test of a fully jointly
retrained two-sided network or inferred individual defensive assignments.

Freeze the v14 RB_RENEW_FAC offensive/rebound model, separately at its saved
inner and final checkpoints. Learn small defensive event adapters. This isolates
new opponent information from offensive refitting/capacity changes and retains
the simpler successful renewal model. Keep ROLE_SL and RB_RENEW_FAC_SHIFT as
archived references; do not select the backbone again from v15 results.

## Frozen designs

| Arm | Learned change |
| --- | --- |
| D_MAIN | Defender-profile mean/SD changes all attackers' action rates, location mix and location-specific conversion. |
| D_CROSS | D_MAIN plus a low-rank interaction with each attacking player's dated capability vector. |
| D_MAIN_RB | D_MAIN plus opponent-dependent defensive rebound competition. |
| D_CROSS_RB | Both receiver-dependent response and defensive rebound competition. |

All four have the same 15 event outputs: three log action rates, six location
logits, six make logits. All start at zero (exact offensive control). Opponent
effects are bounded to ±1 in log/logit units; a standardized population-mean
profile is the parameterization anchor, **not** the product's average opponent.
One hidden layer of width32, tanh; cross branch rank8. No identity embeddings,
named-pair terms, game-state inputs, unobserved tracking, or new point residual.
Rebound arm adds a bounded ±1 defensive log-strength competing against the five
frozen offensive collector scores. There is no opponent FT-conversion output.

Apply the adapter to the frozen offensive model's pre-renewal event rates;
renormalize FGA+.44FTA+TO to its prior reference budget, then recompute live
misses, rebound capture and renewal from the changed shot outcomes. Use the
same frozen non-rebound budget and eligible-miss fraction. Parent supply/load
penalties stay frozen; this is conditional adaptation after those penalties,
not a claim to have solved joint offensive role adaptation.

## Data, dates and masks

New game×offensive-five×defensive-five rows, sorted independently within sides,
from existing possession/shot caches and the verified v14 parsed rebound
events. New output prefix only. Exact rollup to every original game×off5 point,
attempt, turnover, location and eligible-rebound label is mandatory. Inherit
parent game×off5 mechanism masks even when finer grouping would permit more
labels, so the scored event population does not change. Never discard point
rows because a mechanism label is unavailable.

Build new strictly prior defensive states from dated game-player statistics:
own steals, blocks, defensive rebounds and committed fouls per defensive
possession; opponent-on-floor turnovers, FTA, six location shares and six
location make rates. These are confounded statistical descriptors, not causal
individual defensive effects. Each numerator/denominator is decayed with a
365-day half-life and pooled toward the dated league rate with1000 denominator
units. Include log1p defensive exposure as support. Game states exclude the
entire current date; origin states exclude the outer quarter. Unknown players
get the same prior, zero exposure and no synthetic player-specific information.
Fit normalizers on the training prefix only, weighted by exposure. Freeze
origin inputs for the entire validation/evaluation quarter as before.

48 origins2015q1–2026q4, three matched seeds17/23/41.2015 is calibration warmup;
2016–26 is primary. Same last-completed-quarter inner validation and five-year
training window as v14;730-day row-weight half-life. Saved inner backbone must
predate validation; saved final backbone must predate outer evaluation. No
outer outcomes in feature estimation, fitting, stopping, scaling or calibration.

## Fair controls and calibration

Report archived additive A, frozen RB_RENEW_FAC N, and their HALF. Add A+D and
N+D using exactly the same centered, saved additive defensive coefficients.
Center only against strictly prior defensive exposure (365-day half-life);
never subtract a future evaluation-window opponent mean. Positive D means more
points allowed. Estimate one shared slope from earlier completed offensive
cells' A residuals versus D, through the origin, clipped to[0,2]; default1 until
prior cells exist. Reuse old coefficients, not old hindsight centering.

Each adapter gets the established prior-completed-window point calibration
(no deficit term), and HALF combines its forecast with A+D. Also print the
blend with unadjusted A to isolate any additive-defense contribution. Use the
same common cells and exposures for every arm. Do not tune blending on the
evaluation quarter. The three-seed mean is the design-level report, with
individual seeds retained; no retrospective winner promotion.

## Objective and stopping

Equal-weight mean of four prefix-baseline-normalized losses: masked action
Poisson NLL, location cross entropy, location conversion cross entropy, six-way
eligible-rebound cross entropy. Include rebound loss identically in all four
arms (constant with respect to the adapter when no rebound branch exists).
FT conversion is frozen; assisted fractions have no new supervision/parameters.
No team-point auxiliary loss. Complete-game batches target4096 matchup rows;
Adam lr.001, weight decay.0001, gradient clip5. Zero-initialized output heads.

Maximum96 inner epochs, patience8, significant-improvement threshold1e-5;
select the actual minimum validation-loss epoch. Fresh final adapter, same seed,
trained for exactly that many epochs using final-prefix normalizers/backbone.
Durable epoch logs and resumable optimizer/RNG checkpoints. No full campaign
launch until Adam asks. No hyperparameter change in reaction to pilot outcomes.

## Evaluation and three standards

Primary: exact historical offensive-quarter cells (>=50 possessions), weighted
RMSE, MAE, bias, r² and correlation; season-paired differences; recurring/novel
off5 slices. Separately report defensive-five and ten-player cells (>=50), plus
game-level/all-row exposure and events. These are conditional predictions given
actual opponents; unlike a one-lineup prior-average forecast they know the
realized opponent mix. Name that distinction explicitly. Matchups with little
exposure must not disappear from aggregate point/event ledgers.

Counterfactuals: slot permutations on both teams, team-swap margin antisymmetry,
zero adapter parity, FT-conversion invariance, accounting/renewal identities,
stronger defensive recovery reducing ORB continuation, and finite synthetic
extremes. Replay established conventional/five-center/five-guard and named
offensive fixtures against multiple defenses. Do not impose a named total
ranking; failing five-center offense remains an offensive failure even if its
defense is also bad. Report event-level changes, not only total points.

Average-opponent mode marginalizes over a deterministic exposure-weighted
sample of128 *actual prior defensive fives*, with all profiles dated at the
scoring origin. Publish the sample/reference and sensitivity to256. Do not
equate nonlinear evaluation at five mean profiles with this marginal expectation.

Uncertainty: retain seed variation, support/novelty bins, season-block intervals,
and strictly prior residual finite-game coverage checks. Separate those from
latent-mean uncertainty; synthetic extremes cannot validate coverage. Report
remaining latent-OOD limitation explicitly, without a coverage gate or claiming
seed dispersion solves it. A fitted latent-uncertainty architecture is outside
this bounded first defense experiment.

## Operational acceptance and pilots

1. Hash-check old sources/checkpoints, exact label rollups, defensive date/fallback
   audits, fair-control gauge invariance and identical scored populations.
2. Synthetic tests and a one-epoch all-arm smoke at2016q1/seed17.
3. Eight full-length pilot cases: all four arms, seed17,2016q1 and2026q4.
   Inspect runtime, finite outputs, event/point contrasts, masks and stopping.
   These are implementation/cost checks, not arm selection.
4. Freeze production manifest, provide background-launch/live-log/status/report
   commands and realistic runtime/disk estimate. Stand down for Adam to launch.
5. After completion produce scorecards, contrasts, common/novel/opponent slices,
   event/counterfactual/uncertainty diagnostics and independent scientific review.

Use durable verbose logs for building inputs, pilots and the full campaign.
Completed prefixes are immutable; interrupted work resumes only if fingerprints
match. Do not scrape, mutate DB, overwrite old caches, promote, deploy or commit.
If an implementation blocker requires a scientific change, document it before
new results and use a new protocol/prefix instead of silently changing the run.
