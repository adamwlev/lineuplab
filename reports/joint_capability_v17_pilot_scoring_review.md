# v17 pilot and scoring integration — 2026-09-27

**The bounded pilot and scoring integration pass; production is not ready yet.**
No new scientific winner, scorer promotion or full-run launch.

Design: [frozen v17 plan](../docs/history/JOINT_CAPABILITY_V17_PLAN.md).
The prior [core checkpoint](joint_capability_v17_implementation_checkpoint.md)
was committed as91be8b52. This report supersedes its running-pilot status,
not its recorded micro-pilot findings.

## Completed training pilot

Five cases /ten inner-final fits,2016q1/seed17, three CPU workers:
**552.08seconds (9.2minutes), zero failures**. Individual cases took256–295
seconds. Four point-loss arms selected7 epochs; O_FLOW_EVENT selected9.
No cap hits. Fresh final initialization, prior validation and outer export
were verified separately. The completed pilot occupies about124MiB locally;
later origins and longer trajectories may cost more.

All original pilot/v16 artifacts remain unchanged. Audit replayed1,280 saved
prediction rows and independently checked row hashes, dated parents,
normalizers, references, checkpoint selection and final lengths. It then
reconstructed192 archived calibrations: two NN controls ×48 quarters ×two
views, seed17, including2025q1. An independent weighted least-squares solution
matches corrected archived forecasts within1e-8pts/100.103 consumed source
receipts remained unchanged. Other seeds will additionally be checked by
production control replay; this bounded audit is not an all-seed audit.

## Scoring implementation

New `v17_report.py` writes a separate derived namespace, never into completed
native cases. It implements the corrected prior-only calibration, all four
views, exact half blending, prediction-level seed means, five dated cohorts,
a complete-origin chronological barrier and read-only sorted leaderboards.
Missing periods and future calibration outcomes are errors, not silently
omitted rows. Player-ID fields cannot become prediction columns.

Production replays J_POINT_BOTH/J_BOTH against corrected archived forecasts
and requires all720 scheduled cases. The isolated pilot uses the same cold-
start identity NN calibration for both its new and control NN arms, because
new-arm2015 forecasts do not exist. Additive/parent controls retain their
existing historical calibration. These are therefore **operational pilot
numbers, not a comparably calibrated production tournament**.

The [scoring conventions](joint_capability_v17_scoring_conventions.md) specify
the additional seasonal-level diagnostic: a strictly prior same-quarter-index
broad-cell residual mean over the dated league reference, with fixed fallbacks.
No current outcomes tune this control, and it is not a new registered arm.

## Quantitative pilot sanity check

2016q1 only;187 identical off5-quarter cells>=50poss,23,039 possessions,
seed17, half-additive view. RMSE units: **points per100 possessions**.
No arm selection or protocol changes follow from this table.

| Model | Actual-opponent RMSE | Average-opponent RMSE |
| --- | ---: | ---: |
| J_POINT_BOTH control | 10.824984 | 10.814384 |
| O_ORDER | 10.826559 | 10.815550 |
| O_FLOW | 10.824773 | 10.814491 |
| D_SHAPE | 10.813383 | 10.813633 |
| O_FLOW_D_SHAPE | 10.807248 | 10.814282 |
| O_FLOW_EVENT | 10.897163 | 10.964526 |
| J_BOTH event control | 11.194326 | 11.159708 |

The new point-loss arms are close to the point control here. The event-only
arm's large improvement over the event control also includes ordering and
replacement of the old supply penalty; it is not isolated evidence for a
causal creation mechanism. Point-versus-event objectives have different scales.
We need the registered multi-origin comparison and all three product standards.

## Product-mode and uncertainty integration

- Batched average-opponent inference completed all seven arms at the pilot
  origin in28.27seconds. Reference remains the identical prior365-day-weighted
 512 defensive units, plus4096 sensitivity on the first20 broad cells.
  Production reuses completed control outputs instead of retraining them.
- New batching agrees with independent per-cell inference in tests. Inputs
  are shared across arms; learned model outputs are not reused between arms.
- Maximum pilot half-view512-versus4096 difference is.15078pts/100 across140
  arm/cell comparisons. This is numerical sensitivity, not exact convergence
  or a statistical uncertainty interval. It exceeds.1 and must remain visible.
- Direct and half have separate U0/U1 paths. Sixteen model/view forecasts,
  including controls, generated58 common balanced-date lineup pairs each
  (928 model/pair records). Pair identities, bootstrap draws, noise shrinkage
  and the constant U1 likelihood match the original recipe in tests.
- With no earlier new-model forecasts in this isolated pilot, all16 U1s and
  U0 bands correctly remain **NOT_IDENTIFIED**. This is not a coverage gate:
  point forecasts remain available. No U2 fits or invented uncertainty values.
- Realized average-mode outcomes are not neutral-opponent ground truth. U1
  describes stable-quarter persistent discrepancy, not arbitrary synthetic
  lineup-quality coverage. The five-center problem is not yet reevaluated.

Independent scoring review reconstructed140 metrics from saved matchup
predictions using numpy grouping, checked exact blend identities and all
187 broad keys/exposures, validated140 integration sensitivity rows, and
verified missing-history uncertainty statuses.

## Verification and artifacts

**27 tests passed** across v17 model, fit, scoring, averaging, uncertainty and
the existing v16 model tests. No full historical v17 experiment yet.

| Artifact prefix under `experiments/cache/` | Role |
| --- | --- |
| `joint_capability_2026_09_27_v17_pilot1` | Completed native pilot; immutable |
| `joint_capability_2026_09_27_v17_pilot_review1` | Fit/temporal/control audit; PASS |
| `joint_capability_2026_09_27_v17_scoring_dev1` | New scored pilot and logs |
| `joint_capability_2026_09_27_v17_average_dev1/2016q1` | Average-mode pilot; PASS |
| `joint_capability_2026_09_27_v17_uncertainty_dev1` | U0/U1 pipeline pilot, correctly unidentified |
| `joint_capability_2026_09_27_v17_scoring_review1` | Independent integration arithmetic; PASS |

Test log: scoring prefix `logs/integration_tests.log`.
Fit audit: pilot-review prefix `logs/review.log`.
Scoring audit: scoring-review prefix `logs/review.log`.
All jobs in this checkpoint finished; **no active process**.

Read-only pilot leaderboard:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v17_report report --out experiments/cache/joint_capability_2026_09_27_v17_scoring_dev1 --sort r2 --slice all --view half
```

## Remaining before the full-run command

1. Connect frozen fixture/mirror/creation-capacity diagnostics and the unchanged
   real analogue definitions, including successful unconventional units.
2. Finish pooled/season/cohort summaries,16 registered contrasts and matched
   uncertainty comparisons. Do not confuse the working per-origin producers
   with completed full-run analyses.
3. Assemble the production supervisor and preflight: bounded three-worker
   scheduling, scoring frontier, downstream stages, resume and source guards,
   storage/runtime estimate, verified launch/live-log/status commands.
4. Review whether pilot reuse is provenance-identical; otherwise preserve it
   separately rather than silently reclassifying pilot artifacts.
5. Give Adam the command and wait for explicit full-run authorization.

No new refits are needed to finish this integration. The experiment design,
seeds, stopping rule and comparison family remain frozen.
