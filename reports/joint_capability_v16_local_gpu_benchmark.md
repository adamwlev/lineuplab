# v16 local CPU/MPS benchmark — 2026-09-19

## Decision

Keep the frozen three-worker CPU campaign. The tested M1 Pro GPU path offers
only a small steady-state advantage over **one** CPU worker on simple arms,
loses to the measured aggregate throughput of three CPU workers, and cannot
train the combined arm reliably. This is not evidence about NVIDIA/CUDA speed.
No production device/precision, model, estimand, early stopping, or artifact
was changed. No full run or commit was performed.

## Design and preservation

Hardware: Apple M1 Pro, 16 GPU cores, 16 GiB shared system memory; macOS 26.6.2,
PyTorch 2.10.0. Actual MPS tensor execution was verified outside the sandbox.

The saved final-prefix contexts and dated feature library from the eight-pilot
run were read directly. Seed17; origins 2016q1 and 2026q4; arms J_RAW, J_BOTH,
J_ALL_BOTH. Six real-data cases, three modes, two repetitions = 36 attempts.
No database, scrape, input-cache rebuild, or outer-evaluation labels used.

Each repetition starts from the same dated parent and initialized parameters,
performs two untimed warmup steps, resets model and optimizer, then performs
16 timed Adam steps on identical complete-game batches spread through the
training prefix. There are 76/86 complete-game batches in the original early/
late prefixes. The sampling includes the smaller final batch; timing is not a
full epoch measurement. Timed work includes per-batch feature assembly, device
transfer, forward/backward, gradient clipping, Adam, constraint projection,
production-style scalar checks and accumulation. MPS is synchronized at timing
boundaries. Initialization, validation, saved checkpoints, independent numerical
probes, and final analysis are excluded. One CPU thread per process.

Modes: original mixed-precision CPU; explicit FP32 CPU; explicit FP32 MPS.
Benchmark-only source copies use `.float()` instead of `.double()`, float32
instead of explicit float64, and a representable 1e-30 instead of 1e-300 log
floor. Imports bind private copies, not original module replacements. Original
producer fingerprints are checked before and after. Strict deterministic
algorithms are enabled; implicit CPU fallback is not enabled. This is not a
production-compatible precision switch.

Pre-recorded screening limits: initial maximum point difference .005 pts/100,
post-16-step maximum .05, relative loss difference 1e-4, initial gradient relative
L2 difference .005, ledger error 3e-6. These are a diagnostic screen, not full
device acceptance. Original production tolerances have not been relaxed.

## Results

Seconds per **16 training steps**, second repetition (warmed shapes). First
repetition results remain in the original JSON and log.

| Origin | Arm | Original CPU | FP32 CPU | FP32 MPS | GPU speedup vs original single CPU |
|---|---|---:|---:|---:|---:|
| 2016q1 | J_RAW | 2.522 | 2.422 | 2.348 | 1.07× |
| 2016q1 | J_BOTH | 2.473 | 2.405 | 2.158 | 1.15× |
| 2016q1 | J_ALL_BOTH | 12.517 | 11.968 | Failed | — |
| 2026q4 | J_RAW | 2.582 | 2.423 | 2.361 | 1.09× |
| 2026q4 | J_BOTH | 2.566 | 2.461 | 2.172 | 1.18× |
| 2026q4 | J_ALL_BOTH | 11.955 | 11.965 | Failed | — |

First GPU J_RAW passes took 12.039 and 8.021 seconds at the early and late
origins, respectively. Warm shapes are much faster; startup/shape compilation is
a likely contributor, not a profiled causal attribution. Subsequent J_BOTH
passes can reuse earlier compiled shapes. Do not average these into an alleged
steady-state full-run estimate or conceal their cost.

All 32 successfully completed attempts passed the numerical screen. Maximum
post-training point difference from original CPU across successful comparisons:
**0.00005735 pts/100**. Maximum initial gradient relative L2 difference:
**6.36e-6**. Maximum final ledger error: **3.58e-7**. This short trajectory does
not establish identical stopping epochs or long-training behavior.

All four J_ALL_BOTH MPS attempts failed with nonfinite gradients during warmup;
both CPU modes succeeded. A separately saved two-step anomaly probe located a
NaN-producing `LinearBackward0` in the attention block's feed-forward network.
Switching `need_weights=True` to use explicit attention rather than the optimized
scaled-dot-product path still failed. This localizes a backward failure; it does
**not** establish its underlying kernel cause or show that attention itself is
mathematically invalid. No failed training was counted as a speed measurement.

## Actual three-worker CPU comparison

A second benchmark loaded three independent instances of a single arm, with
the same seed/data/initialization, then released a common start barrier. Each
worker performed the same 16 steps. These are throughput replicas, not three
independent statistical seeds. Initialization and warmup are excluded.

| 2026q4 workload | Three simultaneous CPU jobs, measured wall time | Three sequential GPU jobs, projected from warmed single-job timing | CPU throughput advantage |
|---|---:|---:|---:|
| 3 × J_RAW | 3.017 s | 7.083 s | 2.35× |
| 3 × J_BOTH | 3.109 s | 6.517 s | 2.10× |

The GPU column is exactly three times the measured warmed single-job duration,
not a separately measured three-job sequence. Multiple concurrent MPS fits and
mixed CPU/GPU scheduling were not tested. Three-worker CPU timing has one
barrier-released repetition per arm, so precision to milliseconds is descriptive,
not a confidence interval. No full-campaign ETA is inferred from these batches.

## Three product standards and limitations

- **Prediction:** no new forward accuracy evidence. These are training-step
  timings and numerical comparisons, not another predictive experiment.
- **Basketball coherence:** existing accounting is screened numerically, but
  named-lineup or extreme-composition checks were not rerun; no new claim.
- **Uncertainty:** no new coverage or latent/OOD validation. Neither successful
  FP32 replay nor faster training establishes uncertainty quality.

The bounded comparison supports retaining CPU for this campaign, not a claim
that Apple GPUs are generally unsuitable for this architecture. Removing scalar
synchronizations, restructuring kernels, GPU concurrency, and the numerical
failure could be investigated separately; none is required to launch the
already-tested CPU experiment once storage acceptance is resolved.

## Artifacts and reproduction

- `experiments/cache/v16_mps_benchmark_2026_09_19_v1/`: frozen diagnostic
  protocol, exact transformed source variants, row hashes, results, completion
  receipt, durable `benchmark.log` (including failures).
- `experiments/cache/v16_mps_failure_probe_2026_09_19_v1/`: independent anomaly
  probe and explicit-attention variant; both fail.
- `experiments/cache/v16_cpu_parallel_benchmark_2026_09_19_v1/`: protocol,
  per-worker durable logs, start/finish receipts, timings and completion.
- `experiments/cache/v16_device_benchmark_2026_09_19_logs/`: parallel supervisor
  log, anomaly trace, and unit-test log (three tests pass).

All processes completed. Use **new** output/log paths to repeat, since existing
completed directories intentionally cannot be reused or overwritten:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_mps_benchmark --out experiments/cache/v16_mps_benchmark_repeat_NEW --steps 16 --repeats 2
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_cpu_parallel_benchmark --out experiments/cache/v16_cpu_parallel_repeat_NEW > experiments/cache/v16_cpu_parallel_repeat_NEW.log 2>&1
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v16_mps_failure_probe --out experiments/cache/v16_mps_failure_repeat_NEW > experiments/cache/v16_mps_failure_repeat_NEW.log 2>&1
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m unittest tests.test_v16_mps_benchmark -v
```

Run MPS outside an environment that hides the GPU; the sandbox reports it
unavailable even though the host GPU check and this benchmark succeed.
