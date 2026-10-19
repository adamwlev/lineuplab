# v18 idea bank

Started 2026-09-27 at Adam's request, following the J_BOTH architecture,
literature, and raw-versus-adjusted-input discussions. **Brainstorming, not a
frozen experiment or authorization to implement/train.** v17 stays unchanged.
The [research roadmap](../../MODEL_RESEARCH_ROADMAP.md) remains the canonical priority
queue; this document develops candidates for the next design discussion.

**2026-09-28 evidence checkpoint:** the [completed v17 review](../../reports/joint_capability_v17_codex_review.md)
finds near-tied point performance, worse count/conversion fidelity when removing
defensive volume, and coherent but insufficient flow responses on the center
fixture. This strengthens the case for representation/role identification over
stronger hand-set flow costs. No candidate below is selected or frozen by this update.

The subsequent [frozen v18 plan](JOINT_CAPABILITY_V18_PLAN.md) narrows this
bank to seven new arms under a54-hour all-in target. Implementation and bounded
pilots are complete; [verified commands](../../reports/joint_capability_v18_implementation.md)
are ready, with no full launch yet. Keep broader ideas below for later; they
are not all scope for the frozen campaign.

## Starting position

Our goal is a useful two-lineup basketball model, not merely a larger NN.
Forward prediction, counterfactual coherence, and honest uncertainty remain
co-equal. Refits are welcome when they answer a worthwhile question; neither
avoiding training nor maximizing the number of arms is an objective.

Evidence to carry forward:

- [v16 review](../../reports/joint_capability_v16_codex_review.md): adjusted profiles
  consistently help matched RAW/BOTH comparisons, but extra attention, width,
  allocation and phase complexity did not establish a compelling advantage.
  Adjusted profiles are not better for every event channel.
- Point supervision improves ratings while degrading event-count likelihood.
  A good point total does not guarantee a faithful basketball explanation.
- [Matchup diagnosis](../../reports/joint_capability_v16_matchup_followup.md): raw
  teammate interactions already reduce center optimism; defense and renewal
  strongly influence the remaining margin. Do not assume all interactions
  are harmful or prescribe a center penalty.
- [v17](JOINT_CAPABILITY_V17_PLAN.md) tests constraint order, shared creator
  capacity, defensive-volume removal and point/event objectives. Its completed
  results must inform v18; no conclusions here depend on an interim leaderboard.
- [Literature notes](../../reports/literature_review_2026_09_27.md) record precedents,
  inspected sources and access limits. Ideas below are our proposals, not
  claims that the cited papers have already validated these implementations.

## 1. Compact adjusted-first inputs

**Question:** Are we making the NN relearn how to combine too many overlapping
descriptions of each player? Adam's concern is plausible, but redundancy is
not itself proof that removing inputs will help.

We have a partial ablation. Corrected v16, broad offensive-five cells with
at least 50 possessions, 8,345 matched cells / 1,013,999 possessions,
three-seed prediction means, 44 primary quarters:

| Arm | Direct r² | Half r² | Checkpoint-average half r² |
| --- | ---: | ---: | ---: |
| J_RAW | .145225 | .153984 | .154316 |
| J_BOTH | .154150 | .158193 | .160058 |
| J_ADJ_CONTEXT | .155356 | .157320 | .158914 |

Source: `experiments/cache/joint_capability_2026_09_27_v16_codex_review/point_scorecard.csv`.
J_ADJ_CONTEXT removes raw teammate/defender context paths but retains own raw
event anchors and some role history. It also changes the pretrained starting
function: it is **not** a complete adjusted-only or perfectly nested test.
Small differences change sign across views; no decisive superiority claim.

Candidate comparison: full inputs versus adjusted capabilities plus a small,
explicit set of raw behavioral anchors, versus a truly adjusted-only model
with a properly defined league baseline/decoder. Specify what replaces every
removed rate, assist and rebound input; zeroing an indispensable anchor is not
a fair compact-model design. Keep support/uncertainty information available.
Match objectives, training opportunity and initialization policy, and report
parameter/runtime differences. Train reduced variants, rather than declaring
feature importance from inference-time masking alone.

Success could be similar accuracy with fewer inputs, clearer explanations and
more stable transport—not necessarily a new r² record. Connects to R04/R12.

## 2. Trust adjusted profiles selectively, by channel and reliability

**Question:** Can the model use adjustment where it helps without importing
noise where it does not? v16 standalone adjusted profiles improve counts and
defensive location but worsen conversion/recovery and offensive location.
These diagnostics motivate a test, not a guaranteed winning feature subset.

Candidate: a small partially pooled gate between comparable raw and adjusted
event predictions, conditioned on strictly prior support, uncertainty and
staleness. Put alternatives on the same link/scale first: a ridge effect is
not interchangeable with a raw probability. Separate effect estimates from
reliability metadata instead of asking one large input layer to infer both.
Start with a fixed channel subset and a simple learned gate, not a large grid.

Distinguish this from idea 1: dimensional simplification versus reliability-
aware estimation. Jointly test them only after their individual roles are
clear. Guard against sample size becoming a proxy for player status, suppressing
rookies, or treating curvature-based uncertainty as a full posterior. Never
drop low-support players. Connects to R02/R04/R09/R10.

## 3. Separate capability, role allocation and conditional success

**Question:** Can we predict how a player changes jobs, rather than mostly
transporting the job he previously performed? Skinner/Guy and the complementary-
skills literature motivate this distinction; public PBP cannot uniquely
identify latent ability or coaching intent.

Candidate: a slowly varying capability representation, a lineup-dependent
allocation module, and success conditional on allocated workload/action type.
Use observed player action shares, shot locations and assisted outcomes as
intermediate supervision where reliable labels exist. Compare against an
identical allocation architecture without the capability/role separation.
Explicit anchoring/partial pooling is essential to prevent the latent branches
from trading arbitrary offsets or encoding the same information twice.

Already tried in part: dated role inputs, overload, v16 action allocation and
v17 donor-to-finisher flow. The new question is the separation itself. v17
historical assists are realized supply proxies, not identified potential-assist
capacity, and its assisted fraction remains frozen. A bounded first extension
could learn that fraction under observed assisted-outcome supervision before
attempting a fully latent ability/policy model. Audit label availability and
selection on made shots first; do not rename assisted makes as shot quality.

Evaluate player-level role changes as well as team totals. This is my highest-
upside structural idea, but more difficult to identify than input ablations.
Connects to R03/R05/R11.

## 4. Couple teams through possession-entry states

**Question:** Do we undervalue a defensive action because we model stopping the
opponent separately from the offensive opportunity it creates? Skills Plus
Minus explicitly distinguishes entry states; this is an established concept,
not a novelty claim.

Candidate: a small process linking live-ball turnovers/steals, defensive
rebounds and dead-ball entries to the next offense. Forecast and integrate the
entry-state distribution internally; preserve the average-game user interface.
First audit sequence links, substitutions and event definitions. Distinguish
the players who caused a turnover from the five who take the next possession.
Live-ball entry is a PBP proxy, not tracking-confirmed transition shot quality.

v16's initial/post-ORB phases already tested within-offense renewal. This idea
is **cross-team** coupling. A fair comparison needs the same entry information
and supervision in a simpler control. Enforce terminating possession accounting
and swap symmetry; do not double-count turnover prevention or use realized
future entry frequencies as forecast inputs. Rebound-crashing versus transition
defense is a later extension, not something ordinary ORB counts identify.
Connects to R06–R08/R14. Largest new data/label and runtime burden in this list.

## 5. Isolate accounting complementarity from learned adaptation

**Question:** How much useful nonadditivity comes from fixed skills combined
through basketball accounting, and how much from learned changes to those skills?

Reuse/audit ADJUSTED_CHANNEL and existing message-off outputs first. If they
do not answer the question fairly, train matched fixed-skill/accounting and
contextual variants with equivalent information, calibration and objectives.
Compare event forecasts, totals, novel/role-change cohorts, and mechanism
responses. An inference-time message-off intervention tests model sensitivity;
it is not the same as a model trained to operate without messages.

This is both an interpretable baseline and a possible simplification, not a
presumption that learned context is unnecessary. It would sharpen the research
claim and tool explanations without asserting causal attribution. Literature
connection: SPM/Kuehn. Connects to R06/R11/R13.

## 6. Make role-change prediction a first-class evaluation

**Question:** Do gains on novel five-player IDs actually mean better adaptation
to new basketball responsibilities?

Extend the existing [transfer library](TRANSFER_ROLE_BENCHMARK.md), rather than
start a second collection. Separate unfamiliar combinations with familiar jobs
from anticipated changes in creator burden, spacing, size and teammate skills.
Define eligibility and change predictors using information available before
the forecast. Realized role changes can be outcomes/descriptive strata, not
silently used to select a prospective test cohort.

Measure predicted versus observed player action/shot-share changes and team
outcomes; include both successful and unsuccessful adaptations. Report cohort
size, support and interval scores. Trades/injuries are observational changes,
not randomized interventions. This evaluation should accompany representation
and role experiments, not compete with them as another NN arm. R05/R15.

## 7. Uncertainty that follows profile uncertainty and transport

**Question:** Can we distinguish noisy game outcomes, uncertain player states
and uncertainty about how a lineup's skills combine?

First use the role-change cohorts to diagnose U1/U2 failures: calibration,
width, proper scores and persistent-error estimates where identifiable. A next
candidate could propagate dated profile uncertainty through the NN and combine
it with separately estimated discrepancy. Preserve shared-player/coefficient
dependence where possible; independent noise on every feature is not a valid
substitute for covariance. Avoid counting profile estimation error twice in
the discrepancy term.

Compare against the constant U1 control; broader bands alone are not success.
Seed spread alone is insufficient. Held-out real transfers can test transport
coverage, but cannot certify five-center latent-quality coverage. Keep every
lineup available with honest uncertainty—no coverage gate. R10/R15.

## 8. Other bounded ideas worth keeping

- **Multi-timescale player states:** role/usage may change faster than shooting
  skill. Compare separate predeclared persistence schedules or a partially
  pooled state model against the same freshest-data control. Earlier decay
  experiments did not settle a clean capability/role split. No outcome-chosen
  change points; keep evaluation dates fixed to isolate freshness. R05/R09.
- **Reliability-dependent additive/NN blending:** test a low-capacity prior-only
  weight based on support/role novelty, versus fixed half and existing global
  blending controls. v16 broad multi-NN ensembles did not beat the simple
  candidate blend; this is not a rationale for repeating unrestricted stacking.
  Assess the final blend's mechanisms and intervals, not just its r². R10/R13.
- **Point/event objective conflict:** inspect which shared channels the point
  objective distorts; consider a bounded event-fidelity constraint or calibrated
  event-loss weighting. v17's event-only control comes first. Do not introduce
  a disconnected point head that leaves explanations describing another model.
  A loss-weight search must be inner-only and budgeted. R02/R06/R11.
- **Shrinkage of context responses:** a compact bottleneck or group penalty on
  learned contextual changes may improve transport while retaining useful raw
  anchors. Compare with an equally sized/regularized control; ordinary weight
  decay and previous narrow/wide tests are not the same hypothesis. No forced
  named-player interaction signs. R04/R11.

## How to turn this into v18, after v17

My tentative preference is an **input/role clarity campaign**, not another
collection of every architecture at once: compact inputs and selective channel
reliability first, with role-change and uncertainty evaluation built in. A
capability/role prototype is the highest-upside next mechanism. Cross-team
entry states deserve a feasibility audit before inclusion in a full campaign.
This ordering is provisional; a clear v17 mechanism finding could change it.

Before freezing anything:

1. Independently review completed v17 on all three pillars, including native
   events and calibrated product output. Do not select only a point winner.
2. Inventory reusable labels/controls and define what each proposed contrast
   can identify. Refits are appropriate; previously completed artifacts stay
   immutable, and changed representations require retraining downstream fits.
3. Choose a coherent, bounded set with named primary contrasts. Freeze
   information cutoffs, populations, objectives, stopping, calibration,
   multiplicity and success/failure interpretations before viewing results.
4. Keep equally informed additive_defense and contextual controls, direct and
   blend views, average-opponent ratings, real/novel/transfer cohorts, event
   fidelity, offense/defense coherence and uncertainty comparisons.
5. Benchmark training **and downstream analysis**. Use reusable contexts,
   bounded integration/fixtures, durable logs and resumable receipts. Budget
   enough seeds to measure instability rather than treating seeds as new data.

No new scraping, labels, fits, model edits or launches are authorized by this
idea bank. A frozen protocol and Adam's launch authorization come later.
