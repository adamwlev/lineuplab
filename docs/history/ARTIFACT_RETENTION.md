# Completed-run restart retention

Adam authorized removal of obsolete training-resume artifacts on 2026-09-30,
provided verification was fixed first. This is a narrow exception to the normal
immutable-cache rule, not permission to delete other historical outputs.

## What changes, and what does not

Only `resume_0.pt` and `resume_1.pt` inside verified, completed native
`origins/<quarter>/<arm>/s<seed>/{inner,final}` fits are eligible. These contain
optimizer/RNG/restart state. Incomplete fits are not eligible. Final `fit.pt`,
the `checkpoint_*.pt` states used for prediction averaging, all predictions,
training curves, journals, receipts and original manifests remain unchanged.

The original verifier and all frozen producer source files remain unchanged.
Old completion receipts still describe the original full archive. A separate
retirement ledger records exact paths, original SHA256s, original receipt and
run-manifest hashes, byte counts and the specific authorized removal policy.
It is NOT a backup: removed optimizer states cannot be recovered from the ledger.
Completed models remain usable; continuing optimization from a retired restart
slot is no longer supported.

The explicit retention-aware verifier distinguishes a deliberately retired
restart from a missing model. It allows only the ledger's named restart absences;
present restart files still must match their original hashes. Missing or corrupt
retained artifacts, changed original receipts and changed run manifests fail.
Unregistered directories retain strict original verification.

## Required execution mode after retirement

Legacy commands that inspect retired fit receipts must opt into the new verifier.
Plain legacy verification can fail on the intentionally absent resume files;
that does not mean the retained model weights are missing. Do NOT remove receipt
entries or weaken the frozen verifier to make such commands pass.

From the repository root, wrap a Python experiments module like this:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention exec \
  --ledger experiments/cache/completed_resume_retention_2026_09_30 \
  experiments.v16_case_preview \
  --run-dir experiments/cache/joint_capability_2026_09_19_v16_fast2_ready \
  --origin 2016q1 --arm J_POINT_BOTH --seed 17
```

The wrapper installs the verifier in memory BEFORE importing the requested
consumer. It does not change source hashes, suppress corruption checks or alter
scientific calculations. The printed `RETENTION_MODE` line names the ledger and
plan hash, making the exception explicit in logs.

**Child processes do not inherit Python function replacements.** New launchers,
including the forthcoming v19 launcher, MUST construct every affected worker
command with `experiments.artifact_retention.python_job(ledger, module, *args)`.
Bind the ledger plan hash and wrapper source hash into new launcher provenance.
Simply wrapping an old multiprocess supervisor is not sufficient. Existing
frozen supervisor manifests/commands must not be silently rewritten.

For new single-process code, call `install(ledger)` before importing any consumers
that import `verify_complete`. Do not install it late and assume previously
imported aliases have changed. The module wrapper is preferred.

## Audit and cleanup safety

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.artifact_retention audit \
  --ledger experiments/cache/completed_resume_retention_2026_09_30
```

Preparation checks every target fit and its completed case against original
hashes. Apply requires the exact reviewed plan SHA256, verifies again before
authorizing deletion, takes the fit's existing exclusive writer lock, durably
publishes authorization before unlinking, and verifies retained contents after
each fit. Deletion uses explicit recorded paths, not recursive/glob removal.
An interruption is resumable using the same plan; unexpected losses outside the
authorized list still fail. Symlinked targets and hardlinked restart payloads
are rejected. No active model jobs may be present when applying this maintenance.

The first ledger covers only the specified v16_fast2_ready, v17_prod and v18_prod
roots. It does not retire v19 pilots, old failed experiments, capability-library
restart files, model-averaging checkpoints or any other run.

See [maintenance report](../../reports/completed_resume_retention_2026_09_30.md)
for measured counts, reclaimed space, verification and limitations.
