# Current research state

As of **2026-09-27**. All v16 training, repaired post-training analysis and
the independent review are complete and committed as **3eede4cb**. The bounded
saved-weight point-candidate follow-up and its independent review are complete,
committed as **3fb8f1cb**. The frozen v17 design is **e9f994ec**.
**v17 implementation and launch preflight are complete. Ready, not launched;
no active run or promotion.** Core/scoring commits:91be8b52 and8949128a.
The [scorecard](MODEL_SCORECARD.md) owns comparable metrics;
the [review](reports/joint_capability_v16_codex_review.md) owns the evidence
and interpretation; the [roadmap](MODEL_RESEARCH_ROADMAP.md) owns priorities.

## Retained research models

| Component | Present role |
| --- | --- |
| Corrected additive offense and additive_defense | Essential individual-value and equally informed opponent controls |
| v14 neural + additive + defense parent blend | Strong incumbent contextual comparator |
| J_POINT_BOTH direct-half and checkpoint-average-half | Leading v16 point candidates; views effectively tied, no product promotion |
| J_BOTH | Simpler adjusted-profile event/mechanism comparator; count prediction better than J_POINT_BOTH |
| J_OFF and matched RAW/BOTH pairs | Evidence for adjusted representation; both banks are not universally necessary |
| U1 constant persistent-discrepancy model | Required uncertainty control |
| U2 contextual discrepancy model | Research candidate; no held-out joint-log-score improvement over U1 |
| v15 D_MAIN_RB and other archived controls | Historical defensive mechanism/control evidence, not current point leaders |

The primary contextual NN remains profile-based, without known-pair chemistry
or player-ID embeddings. These are research roles, not shipped-model claims.
The existing [page](tool/five.html) still uses its older
[additive-based model](CURRENT_MODEL.md).

## What v16 established and did not establish

- Adjusted BOTH beats RAW across all nine matched architectures and four
  reporting views descriptively. Added complexity is less compelling.
- J_POINT_BOTH's point auxiliary loss improves ratings but worsens count NLL.
  More NN members did not improve on its simple additive blend.
- The broad predictive leader reaches r² .162989 versus additive_defense .146023;
  its incremental gain over parent_half_defense .156601 is smaller and mainly
  quarter-level bias reduction. Historical selection/multiplicity caveats apply.
- Two-team coherence is unfinished: all22 direct NN arms favor the pure-center
  fixture over the Jokić fixture. Additive defense shares the problem. Diagnose
  mechanisms; do not enforce a named result.
- Finite-quarter coverage is useful but slightly low on the broad cohort.
  Wider synthetic U2 bands are not validated latent-quality uncertainty.
  Candidate-specific U1/U2 and the average-opponent benchmark are now complete:
  point-half average-mode r².148368 versus integrated-additive.132160;
  contextual U2 does not convincingly improve on U1 (worse in5/6 comparisons).
  Synthetic candidate true-quality coverage remains unvalidated.
- Split-game reliability is a noise sensitivity, not a theoretical r² ceiling.
- These reused historical seasons are not a fresh prospective test.

The three standards remain co-equal:
[product contract §2](CONTEXTUAL_MODEL.md#2-three-co-equal-acceptance-standards).

## Artifact and repair state

All3,168 native cases /6,336 inner-final fit directories retained. The old
player-ID/prediction-column calibration collision was repaired in separate
scored outputs; old uncorrected v16 leaderboards remain invalid. Neural
training was unaffected.

All six stages now complete: full prediction audit; ensemble/reliability;
48 average-opponent quarters; 10 fixture origins; 48 uncertainty quarters;
final exact audits, summaries and handoff. Bounded optimizer restart fixed
the rejected uncertainty fit without changing its model or acceptance rule.
Installing tabulate==0.9.0 resolved the final Markdown dependency failure.
All64 exact-reference comparisons passed the registered numerical threshold.

- Final source: `experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.
- Independent review: `experiments/cache/joint_capability_2026_09_27_v16_codex_review`.
- Review verified201 metric rows from saved cell forecasts; sources fingerprinted.
- Frozen plans, source producers, failed runs and original feedback preserved.
- No new refits, database access, deployment or promotion. The completed review
  and prior repair work were committed at Adam's request as3eede4cb.

## Next decision and operations

The [bounded follow-up protocol](reports/joint_capability_v16_followup_protocol.md)
is implemented. [Matchup diagnosis](reports/joint_capability_v16_matchup_followup.md):
144 archived predictions replay exactly; teammate interactions reduce the
five-center optimism, while defense and renewal strongly influence its margin.
The65 observed two-nonspacing-big cells show roughly+3pts/100 bias in both the
additive and point-half models; no three-big cells meet the fixed definition.

J_POINT_BOTH's four average-opponent views and its two half-view uncertainty
models completed all48 quarters, zero failures, roughly32minutes.
[Independent follow-up review](reports/joint_capability_v16_point_followup_review.md)
verified40 average metrics,60 persistent summaries and248 unchanged files.
Half beats integrated-additive in11/11 seasons; smaller gains over existing
contextual controls are not established after multiplicity correction.
Original controls reused on matching populations; no neural refits or source changes.
Run: `experiments/cache/joint_capability_2026_09_27_v16_point_followup`.

Adam agreed to bounded role/opportunity/defensive-coverage research rather
than forcing five centers to lose. The [v17 design](JOINT_CAPABILITY_V17_PLAN.md)
is frozen: five new basic BOTH arms isolate defense/constraint order, shared
creator capacity, defensive-volume removal and point/event objectives.
Existing v16 controls are reused; prior overload/composition findings informed
the design.720 production cases/1,440 fits are planned, not launched.

The [launch-readiness report](reports/joint_capability_v17_launch_readiness.md)
supersedes the earlier integration-pending status. All required producers,
fixture/analogue diagnostics,16 registered contrasts, uncertainty summaries and
automatic final review packet are implemented.33 launch-gate tests plus2
report-rendering tests pass. All288 contexts/288 control cases verified;576
production calibration/control-view replays passed. Early/late batched average
replays agree within4.27e-14pts/100; identified-U1 control fits also reproduce.

The [pilot/scoring review](reports/joint_capability_v17_pilot_scoring_review.md)
remains the evidence for five2016q1/seed17 fits in9.2minutes. No arm-selection
claim. Pilot uncertainty is correctly unidentified without prior history;
512/4096 average sensitivity reaches.151pts/100, not exact convergence.

The full720-case experiment is **ready, not launched**. Three CPUworkers,
one thread each, unchanged frozen design. Reference-like stopping estimate
30–32hours including downstream work; doubled-training scenario60–62hours,
not confidence bounds. Estimated additional storage32GiB;123GiB free atpreflight.
Full launch still requires Adam's explicit approval or his own command.

Verified production status (launch and live-log commands in readiness report):

```bash
bash experiments/run_joint_capability_v17.sh status --run-dir experiments/cache/joint_capability_2026_09_27_v17_prod
```

[Handoff](SESSION_HANDOFF.md) records the precise restart point and dirty work.
[Previous state](docs/archive/2026-09-27_pre_v17_launch/JOINT_CAPABILITY_STATE.md)
preserves historical retained-model and runtime information.
