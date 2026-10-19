# V19 implementation checkpoint

September 30, 2026. Adam authorized a commit followed by direct implementation
of the [v19 plan](../JOINT_CAPABILITY_V19_PLAN.md). Commit **b7401231** preserves
the completed v18 sources, diagnostics and v19 design; no cache artifacts were
staged. The subsequent implementation is uncommitted.

The first implementation stage is complete: verified teachers, context-derived
labels, all five model branches, objective-preserving loss, reference integration,
and real-data zero-context replay. **The training runner, pilots and full-run
launch commands are not ready. No v19 fit or outer accuracy evaluation was run.**

## What is implemented

- `joint_capability_v19_protocol.py`: five arms, seeds, contrasts, reference
  window, epoch settings and seven prescribed pilot cases. Full-launch permission
  is false; there is no production launch entry point yet.
- `v19_sources.py`: verifies original sources and all 288 C_FIXED inner/final
  teachers, actual training/validation row hashes, context receipts, cutoff,
  parent weights, normalizers, selected epochs and frozen model dependencies.
- `v19_labels.py`: splits original matchup observations by possession-start
  clock/margin, preserving actor slots, masks, dates, outcomes and original parent
  identities. Reads existing extracts only; writes a fresh derived namespace.
- `v19_context.py` / `v19_context_head.py`: strictly historical reference
  distributions, bounded shared clock effects, margin-within-clock deviations,
  support shrinkage, zero-sum action/location contrasts and unknown fallbacks.
- `joint_capability_v19_model.py`: C_FIXED, C_CLOCK, C_FULL, C_ALLOC and C_MARGIN.
  The encoder is evaluated once per matchup; differentiable indexing expands
  only the ledger/allocator. Initial opportunity mass enters actual renewal,
  rather than a budget that is normalized away. C_FIXED preserves teacher values,
  dtype and frozen weights without aliasing the caller's tensors.
- `v19_training_data.py` / `v19_loss.py`: state expansion, original parent-level
  Poisson constants and original game×off5 point pooling. No event-family or
  point-weight changes hidden in context subdivision.
- `v19_integration.py`: exact finite-context expected-event mixtures, preserving
  point accounting and exposure-weighted conditional probabilities. CLOCK models
  collapse redundant margin categories; C_MARGIN integrates supported joint states.
- `v19_replay.py`: the fixed early/late real-data replay, with independent legacy
  prediction/loss/gradient comparisons and no optimizer or outer evaluation.

The context contrast basis has zero column sums and row L1 norm at most one,
so it has the prescribed channel gauge without a normalized-away common action
shift. Each centered branch is bounded by1.5; C_MARGIN adds two such branches
and may reach3 in combination. This is not a new .44 FT-trip interpretation.

## Verified results

| Check | Result |
| --- | --- |
| Dated teachers | 288/288 pass,48 origins,3 seeds,599 source/receipt entries |
| Original matchup population | 1,592,743 rows /6,059,380 possessions |
| New context view | 3,056,123 rows, approximately1.074GiB of numeric arrays |
| Eligible recoveries | 2,216,895, exactly conserved |
| Parent reconciliation | Zero error for possessions, points, FGA, FTA, FTM, TO, location attempts/makes and recovery counts; masks/dates match |
| Real-data replay | 120 comparisons:5 arms ×2 origins ×12 game batches |
| Rows in replay | 97,835 original /191,261 state rows across the24 batches |
| Maximum prediction difference | 2.7756e−17 |
| Maximum raw event-statistic difference | 3.6380e−12 |
| Maximum backbone gradient difference | 2.3717e−19 |
| Focused tests | 29 pass, including existing persistence/coupling regressions |

No unknown clock or margin possessions occur in this derived corpus. Synthetic
tests still cover unknowns and boundary/OT cases.68,334 shot records are not
attributed under the original possession/shooter matching policy; v19 preserves
that policy and reconciles **all** original labels, including masked parents.
This is not a claim that every raw shot record was successfully assigned.

Source audit took6.77s; context derivation/reconciliation52.11s; full real replay
79.69s. These are local engineering timings, not projected epochs or campaign
runtime. Replay includes both old/new forward and backward in float64. Average
comparison time was about.48–.53s except C_ALLOC1.03s. Proper float32 optimizer
trajectories, one-versus-three-worker timing, full pilots and downstream costs
remain to be measured.

## Preserved artifacts and logs

Under `experiments/cache/`:

- `joint_capability_2026_09_30_v19_sources2/`: authoritative source audit,
  teacher registry, manifest and COMPLETE receipt; sibling `.log`.
- `joint_capability_2026_09_30_v19_labels1/`: mmap-ready context labels,
  CSR offsets, exact reconciliation, source manifest and COMPLETE receipt;
  sibling `.log`.
- `joint_capability_2026_09_30_v19_replay_smoke1/`:10-comparison initial smoke.
- `joint_capability_2026_09_30_v19_replay1/`: authoritative120-comparison replay,
  per-batch results, summary and COMPLETE receipt; sibling `.log`.
- `v19_foundation_tests5.log`:29 passing tests.

The first `_sources1` audit failed because the new checker initially interpreted
the legacy manifest's `model` hash as the optimized model file. It actually
names `joint_capability_v16_model.py`; optimized dependencies are separately
registered in the campaign. The checker now verifies both. Original sources
were unchanged, and all teachers passed the corrected audit.

An intermediate synthetic test caught dtype rounding when loading a float64
teacher into freshly constructed float32 submodules. C_FIXED now loads cloned
teacher tensors preserving dtype; exact replay passes. Failed audit/test logs
remain preserved. The precommit attempt to use pytest found it absent; the
existing unittest suite was used without installing dependencies.

Read-only status commands from the repository root:

```bash
cat experiments/cache/joint_capability_2026_09_30_v19_replay1/summary.json
tail -n 20 experiments/cache/joint_capability_2026_09_30_v19_replay1.log
```

No process remains active at this checkpoint. Completed source fingerprints and
outputs must remain intact; further implementation uses new modules/output
namespaces, with versioned corrections if a bound producer must change.

## Next implementation stage

1. Implement the fresh inner/final fitter, immutable resume journals, bounded
   context penalty, checkpoint-ledger averaging and C_FIXED teacher loading.
   Reuse the verified contexts and derived labels, not new upstream fits.
2. Verify actual float32 optimization and checkpoint/resume equivalence, then
   the seven prescribed full pilot cases. Do not select arms on pilot outcomes.
3. Implement separate reference/conditional prediction, prior-only calibration,
   equally informed shared-context point controls and original-population reports.
   Complete average-opponent, fixture, U0/U1, persistence and independent audit
   adapters; source/protocol fingerprints must bind all executed code.
4. Benchmark one/three workers and complete downstream workloads; produce a
   measured all-in runtime/storage estimate against the proposed54h target.
5. Deliver verified launch/log/status/report/preview commands. **Wait for Adam's
   full-launch authorization.** No command for that campaign is supplied yet.

The three product standards have not changed. These checks establish an accurate
implementation foundation, not a predictive win, improved center coherence or
validated hypothetical-lineup uncertainty. Retain all completed v18 conclusions
and the J_POINT_BOTH reference until the actual experiment provides new evidence.

