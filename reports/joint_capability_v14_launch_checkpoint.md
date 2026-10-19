# v14 launch checkpoint — 2026-09-15

Codex implemented and reviewed directly; no delegation. The registered campaign
is ready for Adam to launch. **The full run has not been launched.** No model was
selected, promoted or changed in response to pilot scores. No commit, scraping,
database mutation, old-cache rebuild or deployment occurred.

## Acceptance and evidence

The prescribed pilot completed all16 cases/32 inner+final fits in1,500.94s
(25.02min), then produced16 forecast paths and799 basketball intervention rows.
All original pilot artifacts remain intact at
`experiments/cache/joint_capability_2026_09_15_v14_pilot`.

Independent acceptance evidence is at
`experiments/cache/joint_capability_2026_09_15_v14_acceptance_final/receipt.json`;
its detailed case table and21-test unittest log are alongside it. Durable audit
log: `reports/joint_capability_v14_acceptance_final.log`. The launch gate at
`reports/joint_capability_v14_launch_acceptance.json` binds all current producer
hashes and the evidence receipt. It is mechanical acceptance, not a model win.

- Every pilot receipt/epoch artifact, selected minimum, final epoch count,
  training/environment cutoff, point-calibration cutoff and matched cell
  population verified. Final fits have no validation/outer stopping decision.
- Selected epochs2–29 (median16), zero cap hits. Maximum gradient norm0.522,
  below clipping threshold5. The previously zero output weights learned:
  collector norms.055–.109, donor norms.067–.139, routing norms.034–.050.
- All saved single/checkpoint-mixture event, point, usage and recovery ledgers
  reconcile: largest point-scale discrepancy4.16e-5/100. Renewal usage on saved
  checkpoint-mixture groups ranges1.075–1.177 actions/possession; no blow-up.
- Pilot and all-design smoke fixture allocations reconcile; isolated recovery
  increases do not reduce native points. No total player-swap ranking is forced.
  The pilot calibration plot was visually inspected; empty panels correspond
  to designs not included in the bounded pilot, not failed production fits.
- The current-origin smoke's48 arm/seed cases,80 report paths and6,392 fixture
  rows verify. All missing finite-game intervals remain unavailable/nullable;
  these one/two-quarter pilots cannot supply four prior calibration quarters.
-14 complete old-control replays agree within1.5e-14,7 one-epoch old/new fits
  are parameter-identical, and interrupted Adam/RNG continuation is bit-exact.
  Full preflight additionally verifies all336 immutable reused-origin records.

One acceptance-harness attempt used unavailable pytest; it failed before
creating a launch gate. Corrected to the repository's existing unittest runner,
then reran into the fresh `...v14_acceptance_final` prefix. The incomplete
`...v14_acceptance` evidence/log is preserved. No training producer or pilot
artifact changed during this final review.

## Campaign and cost

Frozen design: `JOINT_CAPABILITY_V14_EXPERIMENT.md`.
16 designs × seeds17/23/41 ×48 quarter-season origins. Seven verified v13
trajectories supply336 reused cases, leaving1,968 new cases/3,936 new inner+final
fits.2015 is calibration warmup; primary2016–2026 covers44 quarters,
5,607 cells and726,364 possessions. These are quarterly, not full-season fits.

The four common league-level policies and seed41 trailing-checkpoint prediction
averages add analyses, not extra fits. Three seeds are separately calibrated on
prior completed quarters, then equally averaged; external HALF is half additive
and half that ensemble. No best-seed selection. Frozen96-epoch cap, patience8,
min_delta1e-5; previous-quarter validation selects the final prefix-fit length.

Measured pilot cost:

| Component | Measured / extrapolated |
|---|---:|
| Inner+final fitting |1,350.75s total;46.15h for1,968 cases |
| Per-case forecast/checkpoint/save overhead |116.71s total;3.99h extrapolated |
| Pilot setup, cumulative tables and final report |33.47s |
| New case artifacts |480.35MiB pilot;57.70GiB extrapolated |
| Free space at acceptance |252.43GiB |

Plan for roughly **50–75 hours**, about2–3 days, on this machine with one CPU
thread.50.14h is the direct new-case extrapolation, not a guarantee; other seeds,
quarters, reused scoring, repeated leaderboards, full reports and machine load
can change it. CPU samples tracked wall time approximately1:1. Training RSS
samples were0.58–0.86GiB; these are not peak measurements, and full reports will
use more memory. See `joint_capability_v14_resource_sample.json`.

Allow **80–100GiB free** for production artifacts and reporting headroom;57.70GiB
only extrapolates new case directories, not reused scoring or final reports.
Do not delete original artifacts to make room without discussing it.

## Commands

Run directory (preflight only, zero completed training cases):
`experiments/cache/joint_capability_2026_09_15_v14_prod`.

Launch from Adam's terminal:

```bash
cd /Users/adam/Documents/basketball
nohup /usr/bin/caffeinate -i bash experiments/run_joint_capability_v14.sh run \
  --run-dir experiments/cache/joint_capability_2026_09_15_v14_prod \
  >> experiments/cache/joint_capability_2026_09_15_v14_prod/logs/launcher.log 2>&1 < /dev/null &
echo "Launcher PID: $!"
```

Keep the Mac plugged in with its lid open. The command prevents idle system
sleep while running; it does not promise to override lid closure or reboot.
The shell wrapper fixes the Python environment and single-thread settings.
No database connection is needed during training.

Live log (Ctrl-C exits the viewer, not training):

```bash
tail -F /Users/adam/Documents/basketball/experiments/cache/joint_capability_2026_09_15_v14_prod/logs/train.log
```

Status:

```bash
cd /Users/adam/Documents/basketball
bash experiments/run_joint_capability_v14.sh status --run-dir experiments/cache/joint_capability_2026_09_15_v14_prod
```

Read-only leaderboard, including additive, old controls and v14 direct/HALF:

```bash
cd /Users/adam/Documents/basketball
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.joint_capability_v14_leaderboard \
  --run-dir experiments/cache/joint_capability_2026_09_15_v14_prod
```

Sortable/sliceable live view, added after launch without changing any frozen
producer (same metrics and completed-quarter matching):

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.joint_capability_v14_live --sort r2 --slice novel
```

The live view defaults to the production directory above; `--run-dir` can
override it. Sort choices: `rmse`, `mae` (ascending), `r2`, `corr` (descending).
Slice choices: `all`, `novel`, `recurring`; defaults are `rmse` and `all`, matching
v13. Undefined values sort last. Each seed/ensemble view stays separate, and
additive, historical controls and both direct/HALF forecasts remain visible.

The per-case log prints all/novel/recurring MAE, RMSE, r², correlation and bias.
Cumulative tables wait for matched complete designs/seeds;2015 is labeled
warmup and excluded once primary quarters are available. `WAITING` and blank
interval coverage early in the run are expected. Final-fit `val=nan` is also
intentional: only the inner fit uses validation. Status after preflight is
`NOT_STARTED`, with an exited preflight PID, until the full command is launched.

If interrupted, rerun the **same launch command with the same directory** after
checking that the previous process ended. It verifies completed work and resumes
unfinished epochs, including optimizer/RNG state. An active lock rejects a second
launch without changing metadata or logs. Do not edit frozen producers mid-run.

After training, reports run automatically; final success is `ANALYSIS_COMPLETE`
and process exit0. If only reporting fails, preserve the run and use a fresh
derived-only output prefix (do not refit to repair a report):

```bash
bash experiments/run_joint_capability_v14.sh report --run-dir SOURCE_RUN --output-dir NEW_DERIVED_PREFIX
```

## Next handoff

Await Adam's launch/results; do not launch or broaden the matrix automatically.
After completion, verify hashes and all2,304 cases, review three-seed/parent
contrasts and the four common level policies, then basketball interventions,
opportunity/capture/phase errors and uncertainty diagnostics. Keep prediction,
basketball coherence and honest OOD uncertainty on equal footing.

Pilot scores are **not** a campaign leaderboard: their isolated quarters omit
intervening point-calibration history. Rebound facilitation remains a statistical
hypothesis, renewal a stationary approximation—not identified causal box-out
value or a learned putback decoder. Finite-game intervals and seed/checkpoint
disagreement are not calibrated latent-mean uncertainty for hypothetical lineups.
Actual opponent modeling remains outside this run. No automatic promotion.
