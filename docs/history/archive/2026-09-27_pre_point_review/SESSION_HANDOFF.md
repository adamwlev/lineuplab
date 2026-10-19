# Current handoff — saved-weight point-candidate follow-up RUNNING (2026-09-27)

## Current task and commit

Adam approved the reviewed next steps and requested a commit first.
Completed prior v16 repair/analysis/review committed as **3eede4cb**:
`Complete v16 scoring repair, numerical analyses and independent review`.
47 source/report/test/doc files; generated caches excluded.37 precommit tests
passed. This turn's new follow-up code/docs/tests remain **uncommitted**.
No delegation, neural refits, database access, input rebuild, source-output
mutation, scorer promotion or deployment.

## Active process — full analysis, not neural training

Run: `experiments/cache/joint_capability_2026_09_27_v16_point_followup`.
Detached supervisor PID **5558**, launched with caffeinate in its own session.
Three one-thread average-opponent workers, then one chronological uncertainty
worker. Last verified:3/48 average quarters complete, three active, zero failed.
Pilot-based rough runtime45–90minutes; inspect actual logs rather than treating
this as a guarantee. The job continues independently after the assistant turn.

Two shell-background attempts (PIDs5403/5543) exited before work began.
Both were checked absent before the successful detached launch; no duplicate
campaign. The successful process is emitting JOB_START/JOB_END and receipts.

Read-only status:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_point_followup status --run-dir experiments/cache/joint_capability_2026_09_27_v16_point_followup
```

Live supervisor log:

```bash
tail -f experiments/cache/joint_capability_2026_09_27_v16_point_followup/logs/run.log
```

Per-quarter state/checkpoint progress:
`queues/average/logs/average_2026q4.log` (substitute active quarter).
Later uncertainty log: `queues/uncertainty/logs/uncertainty.log`.
Status prints complete-quarter counts and active/pending/failed jobs.
Logs are append-preserved; verify receipts instead of inferring success from
an old traceback or an empty process list.

Resume only if this process has ended; kernel locks prevent duplicate writers:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_point_followup run --run-dir experiments/cache/joint_capability_2026_09_27_v16_point_followup --workers 3
```

This runner automatically summarizes average-opponent results, runs U0/U1/U2
for the candidate, matches old uncertainty controls and seals the root receipt.
It does not generate a new independent research interpretation or edit docs.

## Completed before launch

Protocol: [fixed follow-up](reports/joint_capability_v16_followup_protocol.md).
Findings: [matchup diagnostic](reports/joint_capability_v16_matchup_followup.md).

- Four frozen2026q4 fixtures, all16 ordered pairs including mirrors, four arms,
  three seeds, ten direct-state switches; J_POINT_BOTH checkpoint replay too.
- All144 available archived forecasts reproduced; first+renewed and2PT+3PT+FT
  ledgers reconcile; mirror margins zero. Added per-player demand/conversion
  fields reproduce the prior team outputs exactly.
- Point model's center-native edge decomposes into−1.580 first-chance points
  and+7.976 renewed points. Disabling defense changes direct center margin
  from+4.707 to−6.777; disabling teammate messages raises it to+14.872.
  These are accounting/model interventions, not causal effects or preferred
  basketball rankings. Additive already favors centers+6.345.
- Fixed observed analogues:65 two-nonspacing-big cells/8,471 possessions;
  additive bias+2.836, point-half+3.048. Low-creation184cells/17,976poss favors
  point-direct RMSE12.179 vs additive12.643. Zero three-big cells; six cells
  have both two bigs and low creation. Missing descriptors disclosed.
- Early/late average pilots:52.65s/99.34s, three seeds and actual checkpoint
  lists; identical control keys/values, sensitivity max0.06448pts/100.
- Six chronological uncertainty pilot quarters complete, including fitted
  U1/U2, matching controls and112 existing U0 summary rows reproduced to1e-10.
- Sixteen focused tests pass; real reporting pilot succeeds. Source receipts
  and producer snapshots preserved. Production code unchanged since launch.

Diagnostic root:
`experiments/cache/joint_capability_2026_09_27_v16_followup/`.
Use `matchups_v2/`, `analogues_v2/`, `acceptance/`, `logs/`, `provenance/`.
Earlier development failures/results remain untouched.

Pilots:

- `...2026_09_27_v16_point_pilots_v2`: completed early/late average cases.
- `...2026_09_27_v16_point_uncertainty_pilot_v3`: six-quarter uncertainty pilot.
- `...2026_09_27_v16_point_acceptance`: verified summary using linked pilot cases.

The initial uncertainty pilot discovered that the combined forecast archive
does not retain J_POINT_BOTH per-seed columns. The final adapter reads verified
per-fit scored/groups.npz, checks row order and ensemble means, and uses
checkpoint-half seed forecasts for checkpoint-half disagreement. No forecast
or statistical specification changed. The final eight local tests plus eight
existing uncertainty tests cover this and numerical/temporal behavior.

## Precise next step when the run completes

1. Verify root and stage receipts, logs, source hashes and completeness48/48.
2. Read `analysis/average/summary/scorecard.csv`, paired contrasts and integration
   sensitivity. Four views, three fixed controls, all/novel/recurring/thin/debut;
   44primary quarters, three-seed means. Do not conflate average-opponent targets
   with actual realized defensive schedules.
3. Read `analysis/uncertainty/summary/` and
   `analysis/uncertainty_comparison/matched_controls.csv`. These are finite
   outcomes and stable-quarter working-model errors, not validated coverage
   of arbitrary hypothetical lineup quality. Original uncertainty controls
   remain separate and untouched. Higher joint log score is better.
4. Independently verify representative metrics and update the review,
   three-pillar state/scorecard/backlog. Synthetic candidate discrepancy bands
   and consistent mixed-era profile transport remain explicitly deferred.
5. Discuss a targeted point/channel, defense-capacity/renewal and
   equal-information seasonal-level experiment. No next NN experiment frozen
   or launched; do not add a forced five-center penalty or named-player bonus.

Existing final v16 source (COMPLETE, never relaunch or mutate):
`experiments/cache/joint_capability_2026_09_27_v16_uncertainty_repaired`.
[Independent review](reports/joint_capability_v16_codex_review.md) remains the
authority for completed v16 predictive conclusions.
[Previous handoff](docs/archive/2026-09-27_pre_point_followup/SESSION_HANDOFF.md)
preserves the completed repair/review checkpoint and numerical provenance.
