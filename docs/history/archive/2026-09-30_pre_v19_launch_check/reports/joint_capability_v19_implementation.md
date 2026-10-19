# V19 implementation checkpoint

September 30, 2026. Adam authorized a commit followed by direct implementation
of the [v19 plan](../JOINT_CAPABILITY_V19_PLAN.md). Commit **b7401231** preserves
the completed v18 sources, diagnostics and v19 design; no cache artifacts were
staged. The subsequent implementation is uncommitted.

The foundation and resumable native fitter are implemented and verified. The
seven prescribed full pilots are now running in `..._v19_pilot1`, three workers,
one numerical thread each. **This is not the720-case campaign. Full-launch
commands and the complete downstream pipeline are not ready or authorized.**
The reference/conditional calibration and point-control kernels are implemented
and tested; their end-to-end reporting integration remains unfinished.

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
- `v19_fit.py`: fresh inner/final trajectories, two-slot resumable Adam journals,
  the declared96/patience8/min_delta1e-5 rule and context support penalty. Inner
  selection uses conditional event+point validation loss, excluding regularizer;
  reference point error is logged separately and cannot select epochs.
- `v19_evaluate.py` / `v19_case.py`: actual-context state likelihoods, possession-
  pooled matchup predictions and exact reference integration, separately named.
  Checkpoint mixtures average expected ledgers, not parameters/probabilities.
  Primary conditional state outputs are retained for later event diagnostics.
- `v19_micro.py` / `v19_pilot.py`: real optimizer/resume engineering checks and
  the seven registered full pilots. Pilot CLI has no production-run option.
- `v19_point_context.py` / `v19_control_fit.py`: training-prefix point residual
  tables for additive_defense and the frozen J_POINT_BOTH teacher, separately
  dated inner/final, CLOCK and margin-within-CLOCK variants. Kernels tested;
  source probes passed, but the real-data control export has not yet run.
- `v19_calibration.py`: view-qualified repaired prequential calibration and
  equally informed half blending. Future/cross-view/duplicate histories and
  mismatched information contracts are rejected. Constant forecasts receive an
  explicit undefined-correlation status. Report integration is still pending.

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

### Training-stage verification

All seven engineering cases passed exact interrupted/uninterrupted three-epoch
resume comparisons on the first two complete training game batches. They cover
all five arms at2016q1 and CLOCK/FULL at2026q4, seed17. Each also scores a real
inner-validation batch in both views. Total27.76s; no outer outcomes were used.
The largest usage-ledger discrepancy was2.20e-7 conditional /6.56e-8 reference.
One-process peak RSS was3.73GB across sequential cases; this is not campaign
peak memory or a three-process measurement.

Synthetic checks also verify C_FIXED teacher tensors remain exactly unchanged,
completed fit immutability, checkpoint-state restoration, game/off5 pooling,
reference-only diagnostic poisoning cannot change the selector, reference
centering, residual-table shrinkage, future poisoning and calibration identities.
See `v19_training_tests2.log`:35combined tests pass in1.91s.

At the live checkpoint,2016q1 C_CLOCK and C_FULL completed successfully, selecting
epoch14 after22inner epochs followed by fresh14-epoch final fits. Worker times
were560.55s/564.12s including startup; case artifact sizes67.68MB/68.24MB.
C_FIXED selected36epochs and is in its final fit; C_ALLOC/C_MARGIN are also
active, with the two late pilots pending. No failed worker.
After setup, joint inner epochs were approximately16s with three workers; final
epochs approximately13s. These partial timings are **not** an all-in campaign
estimate or evidence of a scientific win. Read live progress instead of treating
these checkpoint numbers as current forever.

An independent numpy/scipy audit of the two completed cases reproduced all four
saved game/off5 point scores and reference event likelihoods, plus primary
conditional state likelihoods. Each covers15,832matchups /29,816context rows.
Maximum point-ledger discrepancy5.68e-14; event-rate discrepancy4.44e-16.
The checkpoint-average conditional **event** likelihood is not independently
recomputed by this audit: those state outputs require re-inference (its pooled
point score was verified). No aggregate-all-checks claim hides that limitation.
Original J_POINT_BOTH native game/off5 point MSE1963.779; CLOCK reference1961.402,
FULL reference1961.455, versus conditional1949.367/1949.435. These are one-origin,
one-seed **uncalibrated game/off5** diagnostics, not the broad lineup-quarter
leaderboard or a fair conditional point-control comparison. Do not select arms.

### Point-control implementation detail and source gap

The residual tables use the same five-year training prefix and730-day training
half-life as the NN. Shrinkage is500 effective possessions for clock and250 for
margin residuals around the raw clock fit. Effects are centered using the
declared three-year/365-day reference exposure; margin deviations are centered
within clock. Their integrated additive displacement is exactly zero. Missing
clock gives zero effect; missing/unsupported margin inherits clock. No player
or lineup identities enter these tables.

Read-only probes verified additive sources at2015q1,2015q4,2016q1 and2026q4.
There is **no2014q4 saved additive snapshot/control**, required only for the
first warmup origin2015q1's inner additive diagnostic. The implemented explicit
status is `NOT_AVAILABLE_PRE_2015_INNER_ONLY`: do not substitute a future fit.
The frozen NN inner control remains available;2015q1 final/outer additive
control and every primary-period control remain required. No population is
dropped and no NN epoch selector changes. Disclose this diagnostic limitation
in launch readiness; independently verify all remaining dated sources before
the full run. The frozen plan itself is unchanged.

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
- `joint_capability_2026_09_30_v19_micro1/`: seven passing engineering cases,
  resumable fit receipts, summary and sibling `.log`; not scientific fits.
- `joint_capability_2026_09_30_v19_pilot1/`: seven full pilot cases in progress;
  sibling `.log` records queue transitions; `queue/logs/` contains epoch logs.
- `joint_capability_2026_09_30_v19_native_audit1/`: independent snapshot audit of
  completed CLOCK/FULL cases, COMPLETE receipt and sibling `.log`.
- `v19_fit_tests1.log`, `v19_training_tests1.log`,
  `v19_point_context_tests1.log`, `v19_calibration_tests1.log`,
  `v19_training_tests2.log`: new tests and consolidated regression run.
- `v19_control_sources1.log`: verified dated-source probes plus the explicit
  pre-2015 inner-only missing status.

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
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v19_pilot status \
  --out experiments/cache/joint_capability_2026_09_30_v19_pilot1
tail -f experiments/cache/joint_capability_2026_09_30_v19_pilot1.log
tail -f experiments/cache/joint_capability_2026_09_30_v19_pilot1/queue/logs/2016q1_C_CLOCK_s17.log
```

Pilot supervisor launched with PID67369 under caffeinate, detached with durable
logs; use the status file to verify current process state. It will finish the
seven pilots and stop, without launching full production. Completed source
fingerprints and outputs must remain intact. **Do not edit fitter/case/model/
pilot or transitive producers now bound by the running pilot manifest.** New
downstream modules may be added without changing that frozen dependency set.

## Next implementation stage

1. Check the running seven pilots; independently audit completed cases, source
   receipts, native arithmetic, selected/cap epochs, sizes and actual timings.
   Do not select arms on pilot outcomes or launch the full campaign.
2. Run/audit the point-control export on both pilot dates; resolve/disclose the
   warmup-only missing source above. Connect view-qualified calibration to
   equally informed controls and original-population reports.
3. Complete separate reference/conditional scoring and comparative pilot readouts.
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

