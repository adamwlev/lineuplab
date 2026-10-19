# Current handoff — point-candidate follow-up and review COMPLETE (2026-09-27)

## State and authority

No active run. All 48 average-opponent quarters and 48 uncertainty quarters
completed, zero failed jobs, roughly 32 minutes. Supervisor PID5558 finished.
Root, stage and quarter receipts verified. Do not relaunch the completed run.

Adam requested analysis after completion and agreed to the bounded
role/opportunity/defensive-coverage research direction. This turn completed
independent verification, interpretation and documentation. No new training,
database access, source-output edits, promotion, deployment or commit.

Previous completed v16 repair/review was committed as **3eede4cb**.
The subsequent matchup diagnostic, point follow-up, review, tests and current
docs are still **uncommitted**. Preserve unrelated/historical untracked caches;
never stage the entire cache tree.

## Findings and decisions

Read [the completed review](reports/joint_capability_v16_point_followup_review.md).

- Average-opponent mode, same 8,345 broad cells /1,013,999 possessions:
  point-half RMSE11.150592, r².148368 versus integrated-additive
  RMSE11.256199, r².132160. Half better in11/11 seasons; Holm p=.011719.
- Smaller gain versus J_BOTH-half (RMSE−.034367) is not established after
  the registered12-comparison correction (Holm p=.164062).
- Pure point-direct is descriptively strongest on novel lineups:
  r².132922 versus half.127071 and additive.100727. Thin/debut cohorts show
  a similar pattern. No retrospective adaptive-blend rule implemented.
- Average-mode targets remain realized ratings with unknown future opponents;
  they are not observed counterfactual neutral-opponent outcomes.
- Integration sensitivity is larger than pilots suggested: primary point-half
  max512-versus4096 difference.1463pts/100. On the fixed880-cell sensitivity
  subset, half-minus-J_BOTH RMSE is−.03266/−.03267 at512/4096. Contrasts stable
  there, but no full-population exact-integration claim.
- Candidate U2 contextual uncertainty is slightly worse than U1 in5/6 splits.
  Candidate scores beat old controls descriptively in all36 matched rows,
  but that combines point-forecast and uncertainty changes.
- U1 balanced-date finite-half coverage about94.2% at nominal95%, on2,037
  identified pairs; thin/debut around93%. First five schedule quarters,
  including2016q1, are explicitly NOT_IDENTIFIED for U1/U2.
- Generic U0 reports96.07% over220,381 mostly tiny cells. Restricting the same
  intervals to the broad cohort yields possession-weighted93.19%/93.27%
  half/checkpoint-half, novel92.72%/92.67%. The earlier ensemble supplement's
 93.86% uses a different calibration-history population; not a contradiction.
- None of the intervals validates arbitrary hypothetical lineup true quality.
  Candidate synthetic discrepancy bands and consistent mixed-era transport
  remain deferred. No overall three-pillar pass or scorer promotion.

The earlier [matchup diagnosis](reports/joint_capability_v16_matchup_followup.md)
still applies: teammate messages already penalize five centers; defense and
renewal strongly influence the center margin. Observed two-big optimism is
shared with additive, with sparse support. No named ranking is enforced.

## Artifacts and verification

Completed follow-up:
`experiments/cache/joint_capability_2026_09_27_v16_point_followup`.

Independent review:
`experiments/cache/joint_capability_2026_09_27_v16_point_review`.

Reproducer:
`experiments/v16_point_followup_review.py`.
Its `logs/review.log` and `acceptance.json` report PASS:
40 independent average score rows,60 persistent summaries,248 consumed files
fingerprinted unchanged, chronological fit cutoffs, seed means, exact blend
identities and original-control keys/values verified. New output only.

Important review outputs:

- `verified_average_metrics.csv`, `average_rmse_contrasts.csv`
- `integration_error.csv`, `integration_cohort_metrics.csv`
- `verified_persistent_metrics.csv`, `uncertainty_increment.csv`
- `uncertainty_controls.csv`, `broad_finite_intervals.csv`
- `verified_temporal_cutoffs.csv`, `runtime.csv`, `sources.json`

The run's own statistics remain in `analysis/average/summary/`,
`analysis/uncertainty/summary/`, and `analysis/uncertainty_comparison/`.
Original completed v16 source remains unchanged:
`experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.

All **18 focused tests passed**. Verification log: review prefix `logs/tests.log`.
Command:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest tests.test_v16_point_review tests.test_v16_point_followup tests.test_v16_uncertainty_numerics tests.test_joint_capability_v16_uncertainty tests.test_joint_capability_v16_uncertainty_analysis
```

## Next step

Formulate a focused frozen learning experiment, not another open architecture
sweep. The approved direction:

1. Real crowded frontcourts, missing initiators, and successful unconventional
   units alongside extreme fixtures; freeze mechanisms/cohorts before results.
2. Separate opportunity creation from finishing; isolate defensive
   volume/location/conversion and rebound recovery. Do not suppress a plausible
   rebound advantage solely to change a synthetic winner.
3. Read earlier v6/v7 composition/overload work before choosing arms. Conversion
   overload already learned in v7; do not rebrand that as an untried mechanism.
4. Carry unchanged point candidate, J_BOTH event control, equally informed
   additive and seasonal-level controls. All three product standards remain
   equal; stop/reconsider if only the five-center example improves.
5. Reliability-dependent blending is a separate future question. Direct's
   persistent uncertainty has not been evaluated; do not borrow half-model bands.

No new NN experiment is frozen, implemented or launched. The next deliverable
is its explicit arm/control/acceptance design for discussion.

[Prior running handoff](docs/archive/2026-09-27_pre_point_review/SESSION_HANDOFF.md)
preserves launch details and pilot provenance.
