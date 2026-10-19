# Current handoff — v17 pilot/scoring checkpoint complete (2026-09-27)

## Authority and status

Direct implementation only; no delegation. Adam authorized continued work and
checkpoint commits. No full v17 launch until he approves it. No scraping,
database mutation, input-cache rebuilding, scorer promotion or deployment.

**No active process.** Five-case native pilot and all bounded scoring/audit jobs
finished. Do not relaunch the completed training pilot.

Commits already in history:3fb8f1cb (v16 follow-up),e9f994ec (frozen v17 design),
91be8b52 (v17 core). This checkpoint adds scoring/product-mode/U0-U1 integration,
audits, tests and documentation; generated caches must remain out of git.

Read [v17 plan](JOINT_CAPABILITY_V17_PLAN.md), then
[pilot/scoring review](reports/joint_capability_v17_pilot_scoring_review.md) and
[scoring conventions](reports/joint_capability_v17_scoring_conventions.md).
Do not revise arms from the pilot results.

## Completed and verified

- Five native cases /ten fits,2016q1/seed17,552.08seconds, zero failures.
  Point-loss arms selected7 epochs; event-only selected9; no cap hits.
- Fit audit: row hashes, separate temporal cutoffs, dated parents/normalizers/
  references, selected checkpoints, fresh-final lengths and1,280 forward rows.
- Replayed192 corrected v16 control calibrations over48 quarters, two arms,
  two views, seed17; independent WLS agrees.103 source receipts unchanged.
- New v17 scoring: all four views, corrected prior-only affine, seed prediction
  means, common dated cohorts, complete-quarter frontier, sorted leaderboard.
  Production control forecasts must replay the corrected archive.
- Average-opponent producer batches across lineups; all seven pilot arms in
 28.27seconds.512 reference /first20-cell4096 sensitivity; max half difference
 .15078pts/100. Do not claim exact integration.
- Separate direct/half U0/U1 producers.928 pair records =58 balanced-date
  lineups ×16 model/views. No prior history in this isolated pilot:
  all uncertainty fits correctly NOT_IDENTIFIED, point forecasts retained.
  No U2 fitting; no synthetic-quality coverage claim.
- Independent scoring audit verified140 metrics and140 sensitivity rows.
- **27 tests passed.** No original producer/checkpoint/output edits.

Pilot broad cohort:187 cells,23,039 possessions. Half-view actual-opponent
RMSE:point control10.824984; O_ORDER10.826559; O_FLOW10.824773;
D_SHAPE10.813383; combined10.807248; event-only10.897163.
All NN arms use matching cold-start identity calibration here; additive/parent
retain dated historical calibration. **Not a production accuracy tournament.**

## Code and artifact map

New modules:
`v17_report.py`, `v17_average.py`, `v17_uncertainty.py`,
`v17_pilot_review.py`, `v17_scoring_review.py`.
All under `experiments/`; no frozen v16 files changed.

Prefixes under `experiments/cache/`:

- `joint_capability_2026_09_27_v17_pilot1`: completed native fits.
- `joint_capability_2026_09_27_v17_pilot_review1`: temporal/control audit.
- `joint_capability_2026_09_27_v17_scoring_dev1`: per-origin scoring and logs.
- `joint_capability_2026_09_27_v17_average_dev1/2016q1`: integration pilot.
- `joint_capability_2026_09_27_v17_uncertainty_dev1`: U0/U1 pipeline pilot.
- `joint_capability_2026_09_27_v17_scoring_review1`: independent arithmetic.

Test log: scoring prefix `logs/integration_tests.log`.
Review logs: respective prefixes `logs/review.log`.
Each producer is fingerprinted in its completed output. Further repairs need
a new prefix/version; don't edit frozen files to invalidate existing receipts.

## Verified read-only command

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.v17_report report --out experiments/cache/joint_capability_2026_09_27_v17_scoring_dev1 --sort r2 --slice all --view half
```

Views:direct,half,checkpoint_average,checkpoint_average_half.
Slices:all,novel,recurring,thin,debut. This command prints a PILOT_ONLY warning.

## Precise next step

1. Implement fixture/mirror/flow-capacity and unchanged real-analogue output
   integration. Preserve the32 frozen fixtures/10 dates.2016q1 has no registered
   fixture; don't invent a new scientific acceptance case merely to fit the pilot.
2. Implement full pooled/season/slice summaries,16 registered contrasts,
   uncertainty proper-score/coverage comparisons, descriptive successful-unit
   audit and final handoff generator. Per-origin scoring alone is not this work.
3. Build the production supervisor/preflight with3 CPU workers, durable logs,
   chronological scoring, downstream stages, storage/runtime estimate and
   verified commands. Explicitly decide provenance-safe pilot reuse.
4. Commit the verified checkpoint and provide Adam's full-run command.
   **720 cases /1,440 fits remain unlaunched.**

The pilot native-case writer's summary always calls its output a pilot; when
building production use a versioned production wrapper/producer rather than
editing completed pilot fingerprints or silently carrying that label forward.
The uncertainty producer presently emits per-quarter details and correct
cold-start states; full-run summaries/archived-control comparisons still need
integration. Production branches of average/control reuse need a bounded
archived-input check before launch, not just unit tests.

No scientific outcome selected a different architecture. Assist capacity is a
proxy assumption; all three standards remain co-equal. No scorer promotion.

[Previous handoff](docs/archive/2026-09-27_pre_v17_scoring/SESSION_HANDOFF.md)
preserves the launch checkpoint.
