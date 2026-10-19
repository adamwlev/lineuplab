# V20 bounded artifact lifecycle — 2026-10-06

Adam approved implementing automatic retirement of unneeded **new production**
artifacts while preserving completed pilots. No existing run/pilot was purged;
no full training campaign, refit, database operation or commit was launched.

## Measured result

All eight NN pilots completed in28.07minutes:16inner/final fits, no cap hits,
selected7–23epochs, peak1.97–2.70GiB per worker.42completion receipts and frozen
producer/source hashes verified. Selected-inner replay errors were exactly zero.

Their original2.506GiB storage comprised approximately1.173GiB restart state,
.693GiB inner forecasts,.626GiB outer forecasts and.013GiB weights/contexts.
S5's two transactional restart slots each hold the five-epoch validation-ledger
window. This dominates checkpoint size; model parameters themselves are small.

Rehearsal: `experiments/cache/v20_storage_rehearsal_2026_10_06`.
All eight cases were independently copied into new wrapper directories, compacted
and audited. **All48logical outer forecasts reconstruct with identical keys,
dtypes, shapes and data bytes.** Original pilots reverified after each case.

| Measure | Result |
| --- | ---: |
| Original copied payload | 2,690,487,809bytes /2.506GiB |
| Retained cases, including new receipts | 478,273,671bytes /.445GiB |
| Reduction | 82.22% |
| Rehearsal wall time | 46.47seconds |
| Naive864-case retained extrapolation | 48.11GiB |
| With25% size stress and13GiB reserve/temporary headroom | 73.13GiB |

This is a **two-date size extrapolation**, not the required full-calendar forecast.
It excludes additional scoring/uncertainty/diagnostic outputs and assumes future
cases use the new entry point. Original pilots are retained in place and can be
reused read-only. At rehearsal end approximately51.23GiB was immediately free:
the stressed estimate still exceeds that by about22GiB before downstream outputs.
Do not declare full-launch storage readiness or silently remove more data.

A read-only compression probe on one FULL archive found byte-shuffling reduces
compressed array payload78.91→71.90MiB (~9%). Not implemented; not enough to
resolve the remaining budget by itself. No precision reduction was considered.

## New lifecycle and scientific equivalence

`experiments/v20_case_storage.py` is the **new production case entry point**.
The future full runner must use it; no full runner has been launched. It requires
a production manifest with `artifact_policy="v20-new-case-retention-1"`, explicit
launch authority and the exact registered origin/arm/seed path. It cannot adopt
an existing pilot directory or upgrade old receipts in place.

1. The wrapper owns a new case directory from creation. Its `native/` child runs
   the unchanged, frozen `v20_case`/`v20_fit` implementation. Partial cases retain
   the original two-slot optimizer/RNG/selection-window restart machinery.
2. After the full case succeeds, verify all native/fit/context receipts, selected
   inner-score replay, final length and retained selected/averaging checkpoints.
3. Pack outer ledgers **losslessly**. Byte-identical arrays across exports share
   one compressed copy. For no-context models, conditional-state forecasts are
   exact row gathers from matchup forecasts, with the gather and original state
   keys saved. Every reconstructed array is checked against its original hash.
4. Fsync retained data and publish a durable `retention.json` recording the
   exact original paths/hashes/sizes, replacement archive hashes and audit.
5. Under case/native/fit writer locks, unlink only the allowlisted restart slots,
   detailed inner forecast NPZs and the outer NPZs now represented by the verified
   archive. Publish `storage_complete.json` after verifying retained artifacts.

The original `native/complete.json` and child receipts are never rewritten.
The explicit new verifier distinguishes declared retirements from corruption;
ordinary legacy verification remains strict. All original files are checked if
still present during interrupted cleanup. Cleanup resumes from its durable record
without re-entering the native trainer. Unexpected loss of weights, curves,
receipts, metadata or replacement forecasts is always an error.

Retain final/averaging weights, selected inner weights, contexts/source references,
all curves and event metrics, selected-score replay, original receipts and the
exact outer forecast views required for event/point/role/uncertainty analysis.
There is no change to training, early stopping, calibration, cohorts, seeds,
registered comparisons or any of the three acceptance standards.

This is an authorized **artifact-retention amendment** to the frozen plan, not
a rewrite of it. Detailed inner forecasts remain regenerable from retained
selected weights and contexts. Completed optimization cannot resume from retired
optimizer slots; reproducing the training trajectory requires a fresh fit with
the saved sources/configuration. No claim of recoverable optimizer history.

## Consumer contract

- Use `v20_artifact_lifecycle.verify_case(case)` for compact completion. A
  `storage_complete.json` marks finished compaction; native completion alone does
  not. Full scheduling/scoring must respect this distinction.
- Use `v20_artifact_store.load_forecast(case, logical_npz_name)` for the original
  six logical outer forecast dictionaries. It also reads old pilot layouts.
- Use `v20_case_storage.native_directory(case)` for retained fits, curves and
  context paths. Do not ask the old strict fit verifier to ignore missing restarts.
- Existing v16–v18 consumers still require the original retention wrapper. This
  policy neither replaces nor broadens that older authorization.
- No automatic outer scientific-output retirement is implemented. All outer
  forecasts remain available through the lossless archive for later analyses.

## Verification and operations

35combined foundation/case/storage tests pass in8.10seconds. New tests cover
both decoder types, byte-exact replay, idempotence, interrupted unlink recovery,
active-writer exclusion, missing/corrupt weights or archives, illegal retirement
entries, symlink/hardlink rejection and refusal to adopt old cases. A toy
production entry-point run completes and reuses without refitting.

Logs under `experiments/cache/v20_implementation_2026_10_04/logs/`:
`artifact_lifecycle_tests2.log`, `storage_all_tests.log`, `storage_rehearsal.log`.
The first test log is preserved: macOS `/var` aliases required canonicalizing
temporary test paths; production path checks were not relaxed.

The rehearsal removed **only temporary copies** of artifacts. Their originals
remain intact, so those particular copies can be recreated. New production
retirement will be intentionally irreversible for optimizer restart state.

Reproduction, using a fresh disjoint output prefix:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v20_storage_rehearsal \
  --pilot experiments/cache/v20_nn_pilots_2026_10_06 \
  --out experiments/cache/v20_storage_rehearsal_NEW \
  > experiments/cache/v20_implementation_2026_10_04/logs/storage_rehearsal_NEW.log 2>&1
```

Next: finish downstream scoring/uncertainty/rehearsal integration using this
consumer contract, calculate calendar-aware storage/runtime needs, then request
full-run launch approval. No broader historical cleanup is authorized here.
