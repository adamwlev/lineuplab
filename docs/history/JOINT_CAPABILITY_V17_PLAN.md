# v17 — opportunity consistency and shared creation capacity

Frozen scientific design, 2026-09-27. Implementation and launch acceptance are
not yet complete. No production run is authorized by this document.

## Question and prior evidence

Can a small, basketball-motivated constraint improve contextual predictions
without prescribing synthetic winners? Retain all three co-equal standards in
[CONTEXTUAL_MODEL.md](CONTEXTUAL_MODEL.md): forward prediction, basketball
coherence, and uncertainty appropriate to hypothetical lineups.

The [v16 follow-up review](../../reports/joint_capability_v16_point_followup_review.md)
retains J_POINT_BOTH and its half-additive view as point candidates; J_BOTH is
the event-loss comparator. The [matchup diagnosis](../../reports/joint_capability_v16_matchup_followup.md)
found that messages already reduce center optimism. Defense changes the
five-center/Jokić margin substantially; rebound renewal accounts for about
8pts/100 of the native center advantage. Neither observation licenses a center
penalty or a cap on legitimate offensive rebounding.

Earlier v7 overload penalties mostly learned conversion effects, not turnovers,
and produced very small predictive gains. This is **not** another usage-overload
feature experiment. The existing load penalty remains unchanged. v16 currently
computes demand/load constraints before defensive changes to action volume,
shot location and conversion. We will isolate that ordering, and then replace
its assisted-conversion shortage response with an explicit shared resource.

## Fixed arms and controls

All new arms use the basic pooled BOTH architecture, stationary rebound renewal,
the same dated profiles, and the same independently fitted dated parent.

| New arm | Difference | Principal comparison |
| --- | --- | --- |
| O_ORDER | Apply defense before measuring demand/load and enforcing the existing creation constraints. No new parameters. | J_POINT_BOTH |
| O_FLOW | O_ORDER, replacing the old assisted-conversion shortage penalty with a capacity-constrained donor-to-finisher allocation and two learned fallback coefficients. | O_ORDER |
| D_SHAPE | Original ordering; disable direct defensive FGA/FTA/turnover multipliers. Keep defensive location, conversion and rebound recovery. | J_POINT_BOTH |
| O_FLOW_D_SHAPE | Shared-capacity arm with the same defensive-volume ablation. | O_FLOW |
| O_FLOW_EVENT | O_FLOW with no auxiliary point loss, retaining all four event losses. | J_BOTH and O_FLOW |

D_SHAPE is a diagnostic channel ablation, **not** a complete defensive-assignment
model. O_FLOW versus O_ORDER tests a mechanism replacement, not just graph
topology: it removes one scalar response and introduces two. Do not attribute
any gain solely to the graph. No other architecture, feature, decay or penalty
search; no player-ID embeddings or pair chemistry.

Reuse verified completed J_POINT_BOTH, J_BOTH, additive_defense and
parent_half_defense controls. Retain offense-only additive for orientation,
not as the sole comparator for opponent-aware forecasts. No control refits.

## Opportunity mechanism, fixed before results

Use the existing final action budget and dated player profiles. Defense acts
before constraints in O_ORDER and flow arms. Demand is measured before the
existing load penalty, consistently with the legacy demand definition, but
after defensive adjustments. Supply is exp(base log-assists), as in v16.
Assisted fraction remains the frozen parent's unsupported assisted output;
FT percentage remains frozen as well.

For player i, demand is expected assisted makes:

`d_i = FGA_i * sum(location_i * sigmoid(conversion_logits_i)) * assisted_i`.

Create a five-by-five nonnegative flow, donor rows and receiver columns. No
self-assists. In **eight fixed rounds**, each donor offers its remaining supply
proportionally to other players' remaining demand. Scale each receiver's
incoming offers down if they exceed its remaining demand. Subtract accepted
flow from remaining supply/demand. Row sums cannot exceed supply; column sums
cannot exceed demand. This is a permutation-equivariant allocation heuristic,
not a maximum-flow solver or identified causal assist network. Report unused
supply and unmet demand; do not hide finite-iteration slack.

Coverage `f_i = incoming_i / d_i`; when demand is zero, set coverage to one.
Let `t_i = assisted_i * (1-f_i)` be the unsupported assisted-opportunity share.
Two global scalar parameters, both initialized at .1:

- `tau`, projected into [0,1]: fraction of unsupported opportunities lost to TO.
- `kappa`, projected into [0,4]: log-odds conversion cost when creating the shot
  without the intended assistance.

After the unchanged load penalty, let p be conversion by location and
`p_self = sigmoid(logit(p)-kappa)`. Set:

```
FGA_new = FGA * (1 - t*tau)
TO_new  = TO  + FGA*t*tau
make_new = [p*(1-assisted + assisted*f) + t*(1-tau)*p_self] / (1-t*tau)
```

An exactly zero retained-shot denominator gives conditional conversion zero;
its expected makes are zero. These changes conserve the weighted action budget.
Both coefficients can learn zero; no positive floor or synthetic ranking loss.
The old `k_supply` is inactive in flow arms. Keep the existing `k_ft` shortage
response (removed FTA transfers .44 action units to TO) and `k_load` response.
No recurrent recomputation of demand after fallback and no learned supply
inflation. Rebound probabilities are unchanged; changes in misses/turnovers
propagate through the existing renewal ledger.

**Identification caveat:** observed assists are context-confounded realized
outcomes, not potential-assist capacity. Assisted-make fraction is being used
as an opportunity-share proxy. Neither existing labels nor this construction
identifies a causal creator effect. Point/count fits and real cohort behavior
must test whether this assumption is useful. A null or adverse result is valid.

## Temporal design, population and training

- Same48 quarterly origins as v16, three seeds17/23/41. 2015 is calibration
  warmup; primary results cover44 quarters, 2016–2026.
- 5 new arms ×48 origins ×3 seeds = **720 cases /1,440 inner-final fits**.
- Reuse immutable v16 training arrays, capability library, dated parents,
  inner/final normalizers and family references. Verify receipts, row hashes
  and cutoffs. Do not construct or refit an input cache.
- Inner: train the prior five-year prefix ending before the preceding quarter;
  validate on that preceding quarter. Final: fresh dated-parent initialization,
  train through the current origin cutoff for the inner-selected epoch count.
  Outer quarter is never used for stopping, tuning or profile normalization.
- Unchanged Adam lr.001, weight decay.0001, gradient norm cap5, epoch cap96,
  patience8, minimum improvement1e-5. Preserve exact existing best-epoch and
  patience semantics. Game-preserving batches and existing training recency.
- Normalized four event losses plus point weight.25 except O_FLOW_EVENT (zero).
- Save direct and last-min(5,selected)-checkpoint mean predictions. Report
  direct, checkpoint-average, half-additive and checkpoint-average-half.
  Primary product view is **half**; direct is co-reported, not selected after
  seeing results. Common prior-completed-quarter nonnegative affine calibration
  uses the corrected prediction-column handling, never the original v16 bug.
- Primary estimand: possession-weighted realized offensive rating of off5
  quarter cells >=50 possessions against their actual defensive opponents.
  Keep the same matched broad population, novel/seen/debut/thin definitions and
  source row keys. Report counts and weights next to every comparison.
- Preserve native per-matchup count losses and game/off5 point losses, not
  merely calibrated leaderboard r². Retain season/quarter bias and an equally
  informed prior-only seasonal-level control; post-hoc within-quarter centering
  is a diagnostic, not a deployable forecast.

## Required analyses across all three standards

### Prediction and multiplicity

For each arm/view: RMSE, MAE, r², correlation, bias; primary/novel/seen/thin/debut;
per quarter and season; event-family losses and selected epoch distribution.
Show direct and half residual correlation against additive and parent.

Prespecify six half-view RMSE contrasts from the comparison column above,
including both O_FLOW_EVENT comparisons. Add five new-arm versus
additive_defense and five versus parent_half_defense: **16** total registered
contrasts. Report paired season-block bootstrap intervals (10,000 draws,
seed170927) and exact season sign-flip tests with Holm over16. Eleven seasons
are not thousands of independent cells; seeds are not extra seasons.
All other slice/view contrasts descriptive. Reused historical evaluation data
are not a new prospective holdout. No significance-based architecture changes.

### Basketball coherence and real analogues

Reuse frozen v16 fixtures and dates, including all ordered matchups and mirrors.
Report each side's offense, first/renewed scoring, FGA/FTA/TO, location/make,
creation supply/demand/flow, fallback mass, capture and calibration effects.
No forced Jokić/Korver/Westbrook ordering or five-center winner. Include no-self
and permutation checks, duplicate-profile cases and capacity intervention
curves. Those are mechanism checks, not observations of counterfactual truth.

Carry the existing dated real-lineup analogue definitions unchanged: at least
two players height>=82in and prior unadjusted3PA/100<1; low creation max prior
AST/100<5; intersection. Keep missing-profile exclusions explicit. Report all
members, not just errors. The v16 sample contained65 two-big cells,184 low-
creation cells and only6 intersecting cells; this limits conclusions.

Add a **descriptive audit**, not a new acceptance population: order analogue
cells by realized rating and show top/bottom10 with >=100 possessions, keeping
original errors and intervals. This explicitly checks successful unconventional
units rather than selecting only failures. Label outcome selection. Do not
invent causal creator-loss conclusions without a separately frozen personnel-
change design. Freeze any such future design separately, not during this run.

### Product mode and uncertainty

Evaluate each new direct and half view against the same dated average-opponent
reference (512 integrated defenders), with the existing first20 cells/origin
4096 sensitivity. Batch shared candidate inference; do not repeat exhaustive
fixture integrations. Reuse completed point/J_BOTH/additive comparisons.
Targets are realized outcomes, not observed neutral-opponent counterfactuals.

Use candidate-specific prior-only U0 finite-quarter intervals and the existing
U1 persistent-discrepancy control for **direct and half separately**. Reuse
balanced-date pair IDs and chronological splits. Compare coverage, widths,
proper scores and identified counts on matched populations. No borrowed half
bands for direct, no new U2 architecture or uncertainty tuning. Do not count
an improved forecast as proof of an improved uncertainty model. Existing OOD
fixtures have no known true quality; neither seed spread nor finite-game
coverage validates arbitrary hypothetical-lineup intervals. No coverage gate.

## Engineering pilots and production gate

Unit tests: baseline parity, all-arm ledgers, independent slot permutations,
finite gradients, frozen unsupported outputs, masks; flow no-self/row/column
caps, zero/full-capacity limits, fallback zero-coefficient identity and action
conservation, checkpoint reload/resume/provenance rejection.

Read-only engineering micro-pilot at2016q1 and2026q4, seed17: first12
game-preserving **inner-training** batches per arm, exactly one pass. This
checks actual-input loss/gradients, timings and serialization, not predictive
accuracy. Do not inspect outer results to revise arms. Then full early-stopping
pilots on the five arms at2016q1, seed17, including fresh final refits and outer
export. These ten fits may become production cases only if all frozen inputs,
code, settings and receipts match exactly. Pilot metrics remain pilot-only.

Launch gate: all tests; source receipts unchanged; both temporal split checks;
real-input finite loss/gradient and ledgers; successful full case/export;
verified chronological calibration/control parity; recovery/resume tests;
runtime/storage estimate from pilots; durable per-case and supervisor logs;
verified launch/live-log/status/report commands. Start at three independent
CPU workers with one thread each; retain the v16 memoized input/frozen-forward
path. Do not silently reduce seeds, epochs or change data for runtime.

No full run before Adam authorizes it. Pause for an actual numerical or data
bug; version/fingerprint any justified repair. Do not stop a valid run because
interim r² is disappointing, and do not tune this frozen design to its outcomes.

## Acceptance and handoff

No metric alone decides acceptance. Quantify predictive costs/gains, real and
synthetic coherence, and uncertainty separately. A meaningful coherence gain
with modest predictive cost is a tradeoff to discuss, not an automatic failure.
Do not call an arm successful solely because five centers became worse. No
scorer promotion, new blend-selection rule, deployment or scraping.

New v17 namespace only. Preserve all completed v16 artifacts and producer
fingerprints. Commit this design before pilots; commit verified implementation
milestones and concise operational documentation. Final report must include
matched tables,16 contrasts, all-arm diagnostics, uncertainty limitations,
failures/null results, runtime, reproducer commands and recommended next step.
