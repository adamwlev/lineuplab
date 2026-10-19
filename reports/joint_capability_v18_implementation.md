# v18 implementation / prelaunch handoff — 2026-09-28

**Ready, not launched.** Adam authorized implementation and bounded pilots, not
the full campaign. Direct implementation, no delegation or commit. No scraping,
database access, input rebuild, control refit, scorer promotion or deployment.
All preexisting producers and completed outputs remain unchanged.

## Frozen science and implementation

[Scientific plan](../docs/history/JOINT_CAPABILITY_V18_PLAN.md): seven arms ×48 quarters ×3
seeds =1,008 cases /2,016 inner/final fits. Four event losses plus point weight.25
in every new arm. Primary half view; direct/checkpoint views remain available.
Three coequal product standards, no forced rankings or coverage gate.

| Arm | Trainable parameters | Structurally reachable parameters | Change |
| --- | ---: | ---: | --- |
| A_CONTEXT | 22,082 | 20,005 | Own raw anchors plus adjusted context; remove redundant raw context |
| A_SELECT | 25,106 | 13,509 | Fixed adjusted-input subset: offense counts; defense counts/location |
| A_GATE | 25,154 | 24,885 | Twelve reliability gates;48 additional scalars |
| A_CONTEXT_GATE | 22,130 | 20,053 | Compact contextual paths plus those gates |
| A_ACCOUNT | 25,106 | 13,317 | No learned current-offensive-teammate messages; accounting/opponents retained |
| R_ALLOC | 54,200 | 53,931 | Existing action allocator trained with the point objective |
| R_ROUTE | 54,200 | 53,931 | Receiver-only raw conversion residual; indirect role routes retained |

Reachability is an input/module mask count, not functional rank. Path-removal
initializations are not claimed nested. Each fit exports initial_function.json
with training-only point/event/frozen-output differences from its reference.

New versioned model/protocol, fit/case, scoring, average, fixture, uncertainty,
role, summary, independent review, handoff and runner modules preserve old code.
The measured-ready adapter uses the validated runner and adds source hashes;
it does not monkey-patch imported globals. The original slow implementation is
retained because the completed pilots fingerprint it. Production uses the
verified vectorized gate/selection kernel with identical checkpoint schema.

## Verified checks and measurements

-28 tests passed in the final preflight. Baseline/allocator parity, gate gradients,
  masks/routing, frozen FT/assisted paths, slow/fast forward/gradient parity,
  action/rebound/point ledgers, slot invariance, clones, exact fit resume,
  temporal/calibration guards, event inference and real-quarter U0 status tests.
-14 original real-data micro cases /168 batches passed in53.52seconds.
-All seven full2016q1/seed17 pilots completed in17.17 supervisor minutes.
  Selected7 epochs except A_SELECT and A_ACCOUNT at9. None hit96. These are
  engineering pilots; no arm selection from their outer errors.
-14 additional bounded slow/fast12-step checks: max forecast difference
  .00003483pts/100. Slower measured early/late gate ratios .8702/.8679;
  selective-input ratio .8351. Other measured ratios, including slowdowns,
  remain in the estimate.
-48 archived calibration-view checks (two dates ×four controls ×three seeds
  ×two views) match exactly, max difference0.0.
-End-to-end pilot scoring, average-opponent, role, U0/U1 and summary completed
  in84.66seconds. Cold-start pilot U1 is correctly unidentified. A separate
  real2016q1 writer/summary regression verifies nonzero identified U0 in broad
  and all-off5 populations. This is not full-run uncertainty validation.
-288 dated contexts /576 retained-control cases across48 origins checked.
  Strict-date rows, normalizers and parents match their frozen receipts.

Runtime reference **45.09h all-in**, including42.18h training,2.51h measured
downstream projection, spent pilots and final readiness allowance. Explicit
+20% training scenario **53.52h**. The initial4h downstream-allowance scenario
is preserved in preflight.json and is about54.96h under training stress. This
is a target, not a guarantee or kill timer; new stopping epochs may differ.
See [measurement details](joint_capability_v18_runtime_measurements.md).

Projected additional storage54.19GiB +10GiB reserve;97.30GiB free at readiness.

## Automatic post-training work

The runner includes all-view/slice/season scorecards,23 registered half-RMSE
contrasts,36 separately corrected event contrasts, native player allocation and
volume diagnostics, frozen transfer mappings/cohorts,512/4096 average-opponent
checks, all32 fixtures/10dates, native gate/action/renewal ledgers, frozen real
analogues, candidate-specific direct/half U0/U1, independent metric/source checks,
and a generated HANDOFF.md. No automatic selection or promotion.

Saved primary.npz already contains player events for the two required role
controls; no extra replay was needed. Compact original-matchup NPZ and
player-quarter/player-off5-quarter CSVs preserve masks and denominators.
The transfer primary's original146cells/47,419poss is checked, not assumed to
survive every join. First pilot mapping has no unmatched registry cells.
Full mapping and three-pillar results remain pending the actual campaign.

The full production run, full-history summary, actual trained-fixture panel and
final independent review have **not** run yet. A pilot smoke is not evidence of
a predictive gain, repaired five-center behavior or validated OOD intervals.

## Artifacts and verified commands

Ready root: experiments/cache/joint_capability_2026_09_28_v18_prod.
Source manifests, measured preflight and all code/data fingerprints are there.
Pilots: *_v18_micro1, *_v18_pilot1 and *_v18_fast_bench1. Derived smoke outputs
are *_v18_pilot1_scored/_average/_role/_uncertainty/_summary. Engineering logs
and complete receipt: *_v18_engineering. Production is at0/1,008 cases.

From the repository root, explicit full launch:

```bash
nohup /usr/bin/caffeinate -i bash experiments/run_joint_capability_v18.sh run --run-dir experiments/cache/joint_capability_2026_09_28_v18_prod >> experiments/cache/joint_capability_2026_09_28_v18_prod/logs/launcher.log 2>&1 < /dev/null &
echo $!
```

Live supervisor log:

```bash
tail -f experiments/cache/joint_capability_2026_09_28_v18_prod/logs/run.log
```

Status and leaderboard:

```bash
bash experiments/run_joint_capability_v18.sh status --run-dir experiments/cache/joint_capability_2026_09_28_v18_prod
bash experiments/run_joint_capability_v18.sh report --run-dir experiments/cache/joint_capability_2026_09_28_v18_prod --sort r2 --slice all --view half
```

Other views: direct, checkpoint_average, checkpoint_average_half. Slices:
all/novel/recurring/thin/debut. Sort: r2/corr/rmse/mae/bias. Readiness recheck is
the same wrapper with prepare; it validates receipts but never starts training.
Verbose epoch/batch logs live in queues/training/ORIGIN/logs/CASE.log; the
supervisor prints per-origin calibrated quantitative comparisons once all21
cases for an origin finish. Same run command resumes verified checkpoints.

No process is left training after the bounded checks. Files remain uncommitted;
never blanket-stage the numerous unrelated/generated cache artifacts.
