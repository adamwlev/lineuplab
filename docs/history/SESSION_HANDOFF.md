# Current handoff — V20 reviewed and checkpointed (2026-10-09)

## Status and next step

**V20 training, all 19 analysis stages, independent re-pooling and scientific review
are complete. No active v20 job.** Do not relaunch the original supervisor or
completed continuation. Original failed status is preserved historical evidence.

Read the [v20 scientific review](../../reports/joint_capability_v20_scientific_review.md)
and [closeout](../../reports/joint_capability_v20_closeout.md). The closeout distinguishes
completed work, known artifact caveats and unresolved scientific/product work.
Retain P_BASE/J_POINT_BOTH; no scorer promotion or overall three-pillar pass.
Next: discuss a bounded saved-weight defensive/renewal diagnosis and then a
focused coverage/capacity experiment, not another broad architecture sweep.
No new campaign, scraping, database mutation, cache rebuild or deployment authorized.

Direct implementation only; no delegation. All three standards remain coequal,
with no pair chemistry, forced rankings or coverage gate. [Plan](JOINT_CAPABILITY_V20_PLAN.md)
and all original artifacts remain unchanged. Adam explicitly authorized documenting
and committing the completed work on 2026-10-09. That authority does not launch
the proposed next experiment or authorize cleanup/deletion of local artifacts.

## Findings

Primary: 44 quarters / 8,345 cells / 1,013,999 possessions, 2015 warmup excluded.
Checkpoint-average-half r²: P_BASE .162989, S_BASE .162149, P_ADJ .161838,
P_CONTEXT .161724, S_ADJ .161168, P_BOTH .161102, S_CONTEXT .160585,
S_BOTH .159906; additive_defense .146023. No incremental primary point win.
Novel r²: P_BASE .144502 versus additive_defense .118400. New arms do not improve
original transfer/role-change RMSE. All means remain research candidates.

14/44 registered event contrasts pass correction: 11 decoder-context improvements
and three S5 count improvements; none attributable to profile adjustment.
All eight arms still favor legal centers against both Jokić fixtures, +4.72 to +6.23
points/100 primary-blend margin. Pure NN also favors them; inflated FTA/renewal remain.
Four transport-uncertainty contrasts are null. U0 nominal 95% coverage is 93.64% by cell /
93.27% possession-weighted for the reference; synthetic discrepancy widths do not validate
latent-quality coverage. Risk census flags only eight primary cells, four supported:
underpowered, not a useful arm-selection test. Do not repeat unchanged routinely.

P_BASE average-opponent primary r² .146947 vs integrated additive .132160.
Pooled bias +.0153 but quarter-bias RMS 1.5861 points/100; not proof of local calibration.
The prior early pure-NN lead disappeared; full-history blended reference remains
slightly stronger than checkpoint-average NN (.162989 vs .161482).

## Verification and artifacts

Original production: `experiments/cache/joint_capability_2026_10_06_v20_prod`.
Completed continuation: `experiments/cache/joint_capability_2026_10_08_v20_posttrain1`.
Status READY_FOR_SCIENTIFIC_REVIEW is the frozen arithmetic completion record;
this subsequent scientific review does not rewrite it.
Summary: continuation prefix plus `_summary`. Manifest maps reused original stages
and new outputs. [Repair report](../../reports/joint_capability_v20_posttrain_repair.md)
records null-path failure and preserved producer fingerprints.

Independent re-pooling: `experiments/cache/joint_capability_2026_10_09_v20_review1`,
with review.log, provenance.json, tests.log and tables. 192 point rows independently
match saved metrics; exact keys/weights/targets/shared baselines checked.
All 73 v20 tests pass, including new weighted-metric checks. Current edits pass
whitespace checks; four preserved snapshot/frozen-consumer EOF blank-line warnings
are documented in the closeout rather than altering historical bytes.
Original bias_within_quarter.csv.gz omits environment labels; do not pool its
mixed reference/conditional rows. Review's quarter_bias.csv is reference-only.

Training/scoring: 48.88h; resumed analysis: 16.53h (risk 8.49h, average 5.58h).
No new fits or inference during review. Never stage cache artifacts.
The current [scorecard](../../MODEL_SCORECARD.md) and [roadmap](../../MODEL_RESEARCH_ROADMAP.md)
now link the review and decision. Existing launch/bias/Opus-review notes preserved.

This closeout checkpoint includes launch/direction/bias docs and scripts,
repair/continuation/tests, scientific review/consumer/tests, current navigation
and exact historical snapshots. Adam's OPUS_55_review_100626.md is included
unchanged as advisory evidence. Identify the checkpoint with `git log -1 --oneline`
rather than storing a self-referential commit hash here.

The [compact evidence bundle](../../reports/evidence/v20_closeout_2026_10_09/README.md)
records point/contrast/risk/coherence/bias extracts and verified provenance.
The closeout verifier checks 284 frozen dependencies, 104 review inputs, 192 metric
rows and eight bias-summary inputs, plus completed queue receipts. It does not rerun
native inference audits. Generated caches remain local/untracked where already
untracked; the commit is not a backup of model/data artifacts. No deletion.

## Commands

```bash
bash experiments/run_v20_posttrain_continue.sh status
bash experiments/run_joint_capability_v20.sh report --sort r2 --slice all --view checkpoint_average_half
bash experiments/run_joint_capability_v20.sh report --sort r2 --slice novel --view checkpoint_average_half
```

Scientific re-pooling (use a fresh output directory; no fits or inference):
```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
 /Users/adam/miniconda3/envs/basketball25/bin/python -u \
 -m experiments.v20_scientific_review --out <fresh-output-directory>
```

[Previous handoff](archive/2026-10-09_pre_v20_review/SESSION_HANDOFF.md)
preserves the continuation checkpoint and prior history. This is the single
current operational handoff, not authorization to start the proposed next work.
