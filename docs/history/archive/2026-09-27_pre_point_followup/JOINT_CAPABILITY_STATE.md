# Current research state

As of **2026-09-27**. All v16 training, repaired post-training analysis and
the independent human review are complete. **No active campaign; no scorer
promoted.** The [scorecard](MODEL_SCORECARD.md) owns comparable metrics;
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
  The point leader lacks its own U1/U2 evaluation and a full observed-lineup
  average-opponent benchmark.
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
- No new refits, database access, deployment, promotion or commit in the review.

## Next decision and operations

Recommended next step: diagnose the center-vs-Jokić matchup using both
directional ledgers and observed multi-big/low-spacing analogues; evaluate
the actual point leader in missing average-opponent and uncertainty modes.
A targeted loss/channel/calibration experiment may follow after discussion,
not an automatically launched architecture sweep.

Read-only completion status:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_analysis24 status --run-dir experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired
```

[Handoff](SESSION_HANDOFF.md) records the precise restart point and dirty work.
[Previous state](docs/archive/2026-09-27_pre_v16_review/JOINT_CAPABILITY_STATE.md)
preserves historical retained-model and runtime information.
