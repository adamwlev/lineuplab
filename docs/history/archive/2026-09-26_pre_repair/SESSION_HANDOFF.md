# Current handoff — v16 training complete; postprocessing repair next, 2026-09-26

## Decision / processes

Adam asked to shut down v16 and optimize it. The supervisor and three workers
were stopped and shutdown verified. Four completed cases and three interrupted
epoch journals remain in `...2026_09_19_v16_hashfix`. No original artifacts or
producer fingerprints changed. Adam subsequently authorized committing that
checkpoint and launched the optimized run himself. No delegation.

All bounded profiling/equivalence/pilot/benchmark/preflight jobs completed.
**Accepted new destination:** `experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`.
Training complete through 2026q4: all 3,168 native cases and all 6,336 inner/final
checkpoint directories pass receipt/file-hash verification. All fit queues
have zero failures/pending jobs. Postprocessing crashed with `KeyError: 'recovery'`
when reading the v15 event schema (`rebound`); this is separate from the known
calibration bug. All 576 archived-control event exposures match after an explicit
schema alias. See the [completion audit](reports/joint_capability_v16_completion_audit.md).
Full analysis/final audit are incomplete; no NN retraining indicated. Do not
relaunch the old supervisor. Repair/replay implementation is the next task;
neither repair nor remaining analyses has been launched in this status check.
The optimization acceptance measurements below are the September 19 checkpoint,
not the current campaign progress. User's old live-log tail was left alone.

## First post-training task: repair calibration before interpreting v16

**Adam's decision, 2026-09-25:** let training finish unchanged, then fix the
calibration bug and regenerate the leaderboard. Do not stop/restart training or
edit frozen producers while it runs. This is a documented queue, not an
automatic repair job or monitor.

Confirmed defect in `experiments/joint_capability_v16_report.py`,
`calibrate_case`: `row_frame.assign(p0=p0, league=league)` overwrites the first
player ID with the prediction before `aggregate(f, FIVE, ["p0", "league"])`.
This corrupts the native forecast histories used for prior-only calibration.
The shared path affects new v16 arms (including ADJUSTED_CHANNEL), both direct
and checkpoint views, and their half blends. Historical controls do not use
this faulty grouping path. Training does not consume these scored histories;
saved native forecasts/checkpoints remain reusable. No retraining is indicated
by this defect; this is not a blanket certification of the full campaign.

Evidence: 2025q1/J_POINT_BOTH, seeds 17/23/41, all raw forecasts finite and
varying. Each calibrator saw only **42 malformed prior cells**, selected slope
zero, and produced constant forecasts (undefined correlation). A read-only
in-memory reconstruction preserving player IDs produced **7,747 prior cells**,
direct slopes 0.71746–0.76998 and checkpoint slopes 0.80244–0.82483. Latest
history stop was 2024-06-18; no target-quarter outcomes entered calibration.
Diagnostic three-seed results on broad/all (166 cells, 19,870 possessions):

| View | RMSE | MAE | r² | corr | bias |
| --- | ---: | ---: | ---: | ---: | ---: |
| Corrected direct | 10.972889 | 8.522169 | .095253 | .313316 | -.593111 |
| Corrected checkpoint average | 11.043360 | 8.611098 | .083595 | .314698 | -1.364748 |
| Corrected half | 10.975555 | 8.458892 | .094813 | .316909 | .782229 |
| Corrected checkpoint-average half | 10.948036 | 8.441942 | .099347 | .317791 | .396410 |
| Unchanged additive_defense | 11.232222 | 8.586618 | .051982 | .297225 | 2.157569 |
| Unchanged parent_half_defense | 11.047293 | 8.498273 | .082942 | .319757 | 1.555159 |

These are diagnostic reconstructions only; no corrected output artifacts were
saved. The earlier preview parity test matched two consumers of the same bad
history and was not an independent semantic check. Current v16 calibrated
rankings, including earlier partial comparisons, are not reliable evidence
for model selection. The completed v15 tables are not superseded by them.

After training completes, execute the
[P0 repair checklist](MODEL_RESEARCH_ROADMAP.md#post-v16-calibration-history-repair-first).
Rebuild from native predictions into a new versioned derived destination;
preserve all original receipts/outputs. Only then interpret the full three-pillar
results and run the queued reliability and ensemble studies. Registered
automatic end-of-run analyses may still run on faulty scores: preserve them,
mark affected conclusions superseded, and regenerate dependent outputs.

## Read-only per-case results and subsequent queued analyses

**Warning:** the existing preview and report commands below still use faulty
calibration histories until the post-training repair is implemented.

**Queued follow-up (Adam, 2026-09-23):** after v16 training finishes, perform a
same-population empirical reliability/noise-ceiling sensitivity using existing
game-level data, with uncertainty and split-method/opponent-mix caveats. Scope
is in [roadmap R15](MODEL_RESEARCH_ROADMAP.md#post-v16-empirical-reliability--noise-ceiling-sensitivity).
Do not start it during training or alter the frozen v16 protocol. No automatic
monitor or analysis job was launched by recording this request.

**Also queued (Adam, 2026-09-23):** test multiple NN arms plus additive against
single-NN blends after v16 finishes. See
[ensemble scope](MODEL_RESEARCH_ROADMAP.md#post-v16-multi-model-neural--additive-ensembles).
Reuse saved predictions, choose members/weights from prior quarters only, and
separate hindsight-best exploratory mixtures from forward-tested ensembles.
Include novel-lineup results, coherence, uncertainty and inference cost. No
analysis launched; this addition is not part of the earlier checkpoint commit.

New standalone viewer (not a frozen producer dependency):

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_case_preview --run-dir experiments/cache/joint_capability_2026_09_19_v16_fast2_ready --origin 2018q3 --arm J_POINT_BOTH
```

Uses all three seeds by default; `--seed 17` inspects one finished seed.
Prints all four prediction views and matched controls, with explicit view labels.
Reconstructs registered prior-only calibration in memory; no writes, training,
database access or advancement of the official complete-origin frontier.
Requires earlier per-arm calibration histories; never silently drops a seed or
quarter. Supports broad >=50 and `--population legacy_primary`.
Two tests pass, including parity with every corresponding official control/view
on completed 2016q4 (ensemble/broad and seed17/legacy). Live 2018q3 preview and
unfinished-arm refusal verified. Adam authorized a checkpoint commit on
2026-09-23 covering the viewer/tests, noise-ceiling backlog, this handoff and
his new `OPUS55_LAUNCH_ROADMAP.md`. The latter is preserved unchanged as an
advisory proposal, not adopted execution instructions or launch authorization.
Two preview tests were rerun successfully for the checkpoint. Cached artifacts
are excluded; no original producer or run artifact changed. See git log for
the commit ID.

## What changed / results

[Full review](reports/joint_capability_v16_speed_review.md).
[First protocol](reports/joint_capability_v16_speed_protocol.md) and
[second protocol](reports/joint_capability_v16_speed2_protocol.md).

- Singleton execution for disabled zero banks; their parameters and optimizer
  bookkeeping remain. Skip unused adjusted-bank lookups.
- Context/arm/parent-scoped RAM memo of immutable frozen decoder and defender/
  allocation/phase summaries. Joint offense and learned action allocation still
  recompute. No changed data, precision, losses, shuffles, stopping or science.
- Versioned `v16_fast2_*` files inherit/reuse `v16_fast_*`; both original and
  first candidate remain. Only training changes; original reference, inference,
  calibration, diagnostics and audit paths are retained.

Paired warmed one-thread timings (16 batches, median of 3, alternating order):
RAW **2.35×**, BOTH **1.34×**, ALL_BOTH **1.86×** faster. Epoch-equivalents
12.69→5.39s, 12.62→9.42s, 60.64→32.62s. Excludes validation/checkpoint IO/first
memo population. No whole-campaign ETA or new 3-worker throughput claim.

Evidence: `experiments/cache/v16_speed_2026_09_19_v1/`, durable `logs/`.
Three all-arm early/late batteries (44 cases each: first small/full + second
full) show zero point/loss/gradient/state differences across six Adam steps.
Additional all-arm nonzero-weight/messages-off/reordered-memo tests pass.

Full RAW replay (`pilot2`): 25 inner/select17 + 17 final epochs, exactly equal
validation curves, selected/final parameters and outer forecasts. 145.47+90.70s
versus original 404.27+254.62s; original had three workers, pilot one, so use paired
benchmark for fair speedups. Candidate2's RAW path/trainer equivalence is tested;
no full-stopping ALL_BOTH replay. `pilot1` failed strict tolerance because thread
environment differed; preserved. Matching ALL launch environment settings made
the repeat exact; no tolerance relaxed.

## Acceptance and exact commands

104 tests pass. Disk 245.63 GB free / 209.69 GB required. Conservative RAM allowance
14.60 GB / 17.18 GB physical includes 1 GiB extra per worker + 2 GiB system headroom.
Original resource JSON wall-hour projection is inherited PRE-optimization worst
case, not a new ETA. Three workers, three seeds and 22×48×3 cases retained.

Acceptance:
`...v16_fast2_ready/preflight/{acceptance,complete}.json` and `tests.log`.
Production gate exercised with queue launch intercepted: zero jobs launched,
correct worker routing (`release_launch_probe.json`). Status/report verified.

**Use the release wrapper below, NOT old fast/fast2/hashfix wrappers.**
The earlier `...v16_fast2` preflight attempt missed the receipt's manifest field;
caught before launch, preserved and superseded. No model/training change.

```bash
cd /Users/adam/Documents/basketball
mkdir -p experiments/cache/joint_capability_2026_09_19_v16_fast2_ready/logs
nohup /usr/bin/caffeinate -i bash experiments/run_v16_fast2_ready.sh run >> experiments/cache/joint_capability_2026_09_19_v16_fast2_ready/logs/launcher.log 2>&1 < /dev/null &
echo "Launcher PID: $!"
```

```bash
tail -F experiments/cache/joint_capability_2026_09_19_v16_fast2_ready/logs/launcher.log
bash experiments/run_joint_capability_v16.sh status --run-dir experiments/cache/joint_capability_2026_09_19_v16_fast2_ready
bash experiments/run_joint_capability_v16.sh report --run-dir experiments/cache/joint_capability_2026_09_19_v16_fast2_ready --sort rmse --slice all --view half
```

The launch command above is historical, **not** the post-run repair command.
Check-only: `bash experiments/run_v16_fast2_ready.sh check`.
Adam has launched this full run. It recomputes the few
first-origin cases in the new provenance namespace; retains all originals, reuses
the existing historical library, inputs and controls, and automatically runs
registered secondary analyses/audit. No scorer promotion.

## Preservation

This authorized checkpoint includes the accumulated v16 implementation,
acceptance/analysis tooling, metadata repair, runtime benchmarks, optimization,
tests and documentation since 7206b51. Cached data and run artifacts are excluded
from the commit and remain intact locally; their untracked files are expected.
Original library (2,032 snapshots), 44 smoke and eight full pilots remain.
Some diagnostic candidate files are intentionally retained for provenance,
not alternative current routes. See git log for this checkpoint's commit ID.
[Previous checkpoint](docs/archive/2026-09-19_speed_optimization/SESSION_HANDOFF.md)
preserves original launch/metadata repair details. No predictive/coherence/OOD
claims or product-standard changes.
