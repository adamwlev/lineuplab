# Current handoff — v17 independently reviewed (2026-09-28)

## Current state and authority

Direct implementation only; no delegation. Adam requested completion checks
and appropriate follow-up analysis. v17 is complete:720 cases /1,440 fits and
all automatic downstream stages,25.27 hours total supervisor time.
No new training was launched. No database access, scraping, input rebuild,
scorer promotion or deployment. Adam subsequently requested a checkpoint commit:
the v17 review, prior literature notes and idea bank are committed as095183b1.

Read the [independent review](reports/joint_capability_v17_codex_review.md)
for the scientific conclusion, verified metrics, limitations and reproduction.
The [frozen plan](JOINT_CAPABILITY_V17_PLAN.md) remains unchanged.

## Result

- New point arms essentially tie J_POINT_BOTH. O_ORDER half r².163049 versus
  .162915; registered RMSE difference−.000887,95% interval[−.004135,.002210].
- D_SHAPE removes useful event information: counts and conversion worsen in
  all11 seasons despite near-tied point ratings. Do not promote that ablation.
- Flow has coherent capacity responses and modestly lowers center offense;
  all seven arms still favor legal pure centers over the two Jokić fixtures.
  Observed two-big bias remains about+3pts/100. No three-pillar pass.
- Broad U0 coverage is about93–94% at nominal95%. U1 is nearly unchanged;
  synthetic latent-quality coverage remains unvalidated.
- Retain the v16 point reference. O_ORDER is a candidate accounting cleanup,
  not an established predictive improvement. Discuss v18 before new experiments.

## Verification and derived repair

Producer: experiments/v17_completed_review.py.
Two tests passed: tests/test_v17_completed_review.py.
Recursively checked34,923 source files against receipts, all720 native cases,
frozen producer hashes, and independently reproduced460 point-metric rows.
Verified broad row matching, half arithmetic and original U0 interval arithmetic.

**U0 summary defect:** valid per-cell status is FINITE_GAME_BAND, not OK.
The frozen summary wrongly excluded all bands; the underlying writer, bounds,
training, point forecasts and U1 are unaffected. A new standalone review
corrects broad U0 summaries and validates top/bottom analogue bands.
Original all-off5 aggregate U0 remains invalid; raw bands are valid. Do not use
the original packet's all-unidentified table. Future producers need this
status-contract regression check; no frozen source was edited.

Native run: experiments/cache/joint_capability_2026_09_27_v17_prod.
Original derived siblings: _scored, _average, _basketball, _uncertainty,
_summary, _handoff.
Verified review: experiments/cache/joint_capability_2026_09_28_v17_codex_review.
Durable review log: logs/review.log under that new prefix.
Review completed successfully; no review process left running.
Source receipt hashes and acceptance.json accompany the derived results.

## Dirty work and precise next step

New work after commit095183b1: [detailed v18 proposal](JOINT_CAPABILITY_V18_PLAN.md)
and navigation/state/handoff edits, not yet committed. Seven new arms,
1,008cases/2,016fits, three seeds,54-hour all-in runtime target. Runtime uses
actual v17 worker/wall timing and v16 allocator per-epoch cost (median1.612×
basic BOTH), not an assumption that every arm costs the same. Proposed reference
42.3hours including pilots/analysis,20% training-time stress49.7hours; must
measure at preflight. An eighth event-only routing arm was deferred for budget.

Adam approved implementation after the gate/shrinkage discussion. The v18
scientific plan is now frozen. New versioned model/fit/pilot/scoring/product/
role/uncertainty/summary/review/runner modules are implemented; readiness checks
are still underway. No original producer was edited, no upstream fits or inputs
rebuilt. No full launch, commit or promotion authorized.

Bounded micro pilot: experiments/cache/joint_capability_2026_09_28_v18_micro1,
14cases/168batches passed in53.5seconds. Seven full-epoch pilot cases are running
under experiments/cache/joint_capability_2026_09_28_v18_pilot1. Supervisor log:
logs/launcher.log; individual verbose logs under queue/logs. These are not a
full campaign or an arm-selection tournament.

Engineering checks:23 tests passed;48 archived control-calibration view replays
across two dates/four controls/three seeds have max absolute difference0.0.
Durable logs: experiments/cache/joint_capability_2026_09_28_v18_engineering/logs.
Next: finish pilots, execute v18_preflight end-to-end derived smoke, fix any
engineering failures in new namespaces, measure runtime/storage, then prepare
production and provide verified commands. Do not launch the full run.
Numerous generated cache artifacts remain untracked; never blanket-stage them.

Point scoreboard (unchanged, valid):

```bash
bash experiments/run_joint_capability_v17.sh report --run-dir experiments/cache/joint_capability_2026_09_27_v17_prod --sort r2 --slice all --view half
```

[Previous handoff](docs/archive/2026-09-28_pre_v17_review/SESSION_HANDOFF.md)
preserves the running checkpoint and literature/v18 documentation follow-up.
