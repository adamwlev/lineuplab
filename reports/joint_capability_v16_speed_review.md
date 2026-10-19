# v16 runtime optimization — 2026-09-19

## Decision

Adam requested stopping the campaign and optimizing it. The supervisor and its
three workers were stopped; saved cases/journals remain intact. No full restart
or commit was performed. The change is operational, not a new model design.

## Why it was slow

At 2015q1/s23, v15 D_MAIN_RB averaged 1.851 seconds per inner epoch and
D_CROSS_RB 3.126 seconds. v16 J_RAW averaged 16.161 seconds. All use about
301,000 training rows. v15 optimized only an adapter over a cached frozen
offense; v16 differentiates offense too. That explains more work, but not all
the inefficiency.

Profiling found large disabled adjusted-profile banks still going through
MLPs and variance calculations. Raw and adjusted defender summaries were
recomputed despite being fixed inputs. The separately frozen decoder also ran
on every batch/epoch. Initial profiling includes cold library initialization;
only the explicitly warmed alternating-order benchmark supports speedup claims.

## Changes

- Compute centered effects of disabled, all-zero banks on one five-player
  example and broadcast. Preserve their parameters and zero-gradient Adam
  weight decay; do not silently change parameter initialization or topology.
- Avoid unused adjusted-bank feature lookups.
- Memoize exact frozen decoder outputs and fixed defender moments by row in
  process memory. One context/arm/parent per memo; history and origin-frozen
  feature modes cannot be mixed. The joint offensive network is NOT cached.
- Keep original data, precision, objective, optimizer, batches/shuffle, early
  stopping, epoch cap, checkpoints, inference, calibration and analysis.

Versioned model/data/trainer/case/runner files preserve all original producer
fingerprints. The original scorer can read and replay optimized state dicts.
Memo storage is temporary RAM, not a new persistent input library.

## Equivalence

All 22 arms × two cutoffs (2015q1, 2026q4), six paired Adam updates each:

- 512-row checks: 44/44 pass, bit-identical forecasts, losses, gradients and
  updated parameters.
- Full-game-sized checks (up to 4096 rows): 44/44 pass, same exact results.
- Memo values exact across two complete reshuffled inner prefixes; paired
  original/optimized updates exact across both complete epochs.

Full production-case replay, 2015q1/J_RAW/s23:

| Stage | Epochs | Original seconds | Optimized seconds | Equivalence |
| --- | ---: | ---: | ---: | --- |
| Inner selection | 25, selects 17 | 404.27 | 145.47 | Every validation objective and selected parameter exact |
| Fresh final | 17 | 254.62 | 90.70 | Every final parameter exact |

Checkpoint selection is unchanged; outer forecasts match exactly (maximum
difference **0 points/100**). This observed wall-time improvement is NOT a fair
standalone throughput ratio: original ran with three workers, replay with one.
The separate warmed benchmark controls that difference.

First attempt `pilot1` is preserved as **failed acceptance**. It omitted some
production thread-environment settings; validation differed by at most 3.36e-9
and parameters by 2.13e-5, despite same best/stop epochs. Matching all six thread
variables and PYTHONHASHSEED in `pilot2` restored exact full-trajectory parity.
No tolerance was relaxed. These settings must remain in the launch wrapper.

## Scope and caveats

No new predictive, basketball-coherence or OOD claim: outputs are unchanged.
This does not validate arbitrary synthetic lineups or alter the scientific
interpretation of any arm. All three product standards remain coequal.

No original artifacts are overwritten. Four completed native cases and three
interrupted cases stay in the stopped `...v16_hashfix` campaign. The optimized
campaign uses a new destination rather than silently changing old provenance;
it recomputes those few cases if launched. Historical profile library, inputs,
controls and original audited acceptance evidence are reused.

Evidence: `experiments/cache/v16_speed_2026_09_19_v1/`; logs under `logs/`.
Frozen [operational protocol](joint_capability_v16_speed_protocol.md).
## Second candidate and matched timing

The first candidate accelerated RAW 2.49× and BOTH 1.28×, but ALL_BOTH only
1.04×. Profiling ALL_BOTH found repeated allocation/phase input moments taking
2.70 of 5.97 seconds across eight steps (variance alone 2.16 seconds).
Candidate2 reuses those exact immutable summaries and the within-forward
other-four context; phase-specific action allocation remains separately learned.
It does not cache the learned attention projections. See the
[second operational protocol](joint_capability_v16_speed2_protocol.md).

Final matched benchmark: one CPU thread, same real 2015q1 full-game batches,
16 steps per measurement, three repetitions, alternating implementation order.
Medians, with epoch-equivalents scaled to 75 batches:

| Arm | Original epoch-equivalent | Optimized | Speedup |
| --- | ---: | ---: | ---: |
| J_RAW | 12.69s | 5.39s | 2.35× |
| J_BOTH | 12.62s | 9.42s | 1.34× |
| J_ALL_BOTH | 60.64s | 32.62s | 1.86× |

These are warmed assembly + forward/loss/backward/Adam measurements, not full
epoch wall times: exclude validation, checkpoint IO and initial memo population.
Full-prefix RAW pilot above includes those epoch costs. Do not extrapolate one
arm's ratio to the whole campaign; 19 arms lack paired timing measurements and
no new full-campaign ETA is established. The inherited resource JSON's wall-hour
projection is the OLD worst-case pilot estimate, not an optimized ETA.

Candidate2 passed another 44/44 full-sized early/late comparisons with **zero**
forecast/loss/gradient/updated-state differences. Synthetic all-22-arm checks
also cover randomized learned weights, messages-off and reordered memo rows.
Its RAW path and trainer are source-checked equivalents of candidate1, allowing
reuse of the exact full RAW replay. No full-stopping ALL_BOTH replay was run.

## Launch acceptance

- 104 tests pass (88 original v16, seven metadata-repair, nine speed tests).
- Conservative three-worker RAM allowance 14.60GB / 17.18GB physical, including
  an extra 1GiB per worker for full memo population and 2GiB system headroom.
  This is an allowance, not a new full-campaign concurrency measurement.
- Disk 245.63GB free / 209.69GB required (including reserve).
- Production startup gate exercised through the first queue with job launching
  intercepted: zero workers started, correct versioned module and three slots.
- Read-only status/report commands verified: 3168 pending / NO_ROWS.

**Accepted destination:** `experiments/cache/joint_capability_2026_09_19_v16_fast2_ready`.
**Accepted wrapper:** `bash experiments/run_v16_fast2_ready.sh run`.
Full training remains stopped; Adam must launch or authorize a restart.

Do not use the earlier `...v16_fast2` / `run_v16_fast2.sh` attempt: final lifecycle
review caught its missing manifest field in the acceptance receipt. It was never
launched, is preserved, and is superseded by the release wrapper/destination.
The correction changed no model, trainer or equivalence evidence.

Exact background/log/status commands are in [current handoff](../docs/history/SESSION_HANDOFF.md).
