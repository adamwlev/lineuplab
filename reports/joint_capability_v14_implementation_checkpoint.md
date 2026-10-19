# v14 implementation checkpoint — 2026-09-15

Codex implemented directly. No Opus or other agent was used. No commit,
scraping, database mutation, old-cache rebuild, scorer promotion or deployment.

## Status

**Superseded by launch acceptance, 2026-09-15:** all16 pilots and automatic
reports completed successfully. Independent acceptance and21 tests pass; full
preflight is `NOT_STARTED`, zero training cases. See
`joint_capability_v14_launch_checkpoint.md` for current commands/evidence.
The historical in-progress checkpoint below is retained for provenance.

The implementation and bounded smoke/reuse checks are complete. **The prescribed
full-length pilots are running; the full campaign is not launch-ready yet.**
No full-campaign fit was launched. The CLI refuses `run`/`preflight` until a
reviewed `reports/joint_capability_v14_launch_acceptance.json` exists and binds
the accepted producer hashes. Do not create that receipt merely to bypass it.

Pilot: `experiments/cache/joint_capability_2026_09_15_v14_pilot`.
Eight registered designs, seed41,2016q1 and2026q4:16 arm-origins/32 inner+final
fits, max96/patience8. At the last check,4/16 cases had completed and2016q1
FTA_ROUTE was running. The first inner fit used170,781 rows.
Managed execution session59082; Python PID17649 at launch, with `caffeinate`
sleep prevention. Two detached-shell attempts exited before creating any run;
their absence was checked before the managed launch. No duplicate worker exists.
Always inspect the actual process/status files before assuming it is still active.

Live log:

```bash
cd /Users/adam/Documents/basketball
tail -f experiments/cache/joint_capability_2026_09_15_v14_pilot/logs/train.log
```

Status:

```bash
cd /Users/adam/Documents/basketball
bash experiments/run_joint_capability_v14.sh status --run-dir experiments/cache/joint_capability_2026_09_15_v14_pilot
```

Read-only leaderboard:

```bash
/Users/adam/miniconda3/envs/basketball25/bin/python -u -m experiments.joint_capability_v14_leaderboard --run-dir experiments/cache/joint_capability_2026_09_15_v14_pilot
```

Resume **only if that process has ended**:

```bash
cd /Users/adam/Documents/basketball
bash experiments/run_joint_capability_v14.sh pilot --run-dir experiments/cache/joint_capability_2026_09_15_v14_pilot
```

The run lock prevents duplicate execution. Completed phases and every epoch
have receipts; interruptions restore optimizer/RNG state. A reporting failure
does not require refitting. New reports from preserved runs use a new prefix:

```bash
bash experiments/run_joint_capability_v14.sh report --run-dir SOURCE_RUN --output-dir NEW_DERIVED_PREFIX
```

## Implemented

- New read-only SQL snapshot; ordered FG/FT recovery attribution; dated rebound
  states; separate source-coverage and post-recovery phase labels.
- All16 registered model designs/three seeds. Exact v13-compatible controls,
  role-history/current/shift contrasts, FTA routing, competitive collector and
  leave-self-out facilitation heads, and stationary possession renewal.
- Original five-family normalization plus the separately normalized rebound
  term; original team loss, stopping protocol, optimizer and regularization.
  Previous-quarter validation only; reset-final fits never stop on the outer data.
- Seven immutable v13 reuse references. Independent seed calibration, fixed
  seed ensembles and external halves; seed41 trailing-checkpoint **prediction**
  mixtures. Shared prequential league-level policies remain separate from NN gains.
- Per-player event ledgers, observed-opportunity masks, ensemble capture metrics,
  phase errors, seed/season contrasts and Holm summaries, largest harms/benefits,
  fixed basketball interventions, support-stratified finite-outcome intervals,
  persistent-error diagnostics, figures and durable reports/logs.

No design, parent, objective, hyperparameter or stopping criterion was selected
from smoke scores. The extra2026q4 smoke exercised the current-origin fixture
registry, which2016q1 did not cover. Reader/serialization improvements after that
smoke were checked under a new derived prefix, preserving its original artifacts.

## Verified evidence

- Full extraction:6,059,380/6,059,380 original possession IDs, dates, games,
  lineups and point targets reconciled in a read-only repeatable-read transaction.
- Labels:2,216,895 eligible FG recoveries =516,768 ORB+1,700,127 DRB. Zero
  unmatched grouped rows. All897,778 point-training groups remain present.
-667,527 aligned player-game rebound states and origin snapshots pass strict
  prior-date checks. FT/team/ambiguous/substitution recoveries remain separate.
- Phase audit:421,072 FGAs follow eligible FG ORBs in resolved-floor sequences.
 54,832 superseded misses disclose omissions/order ambiguity; no imputation or
  separate putback decoder is claimed. New phase targets are diagnostics only.
-21 focused tests pass. The real-data reuse audit reproduces14 early/late
  complete control forecasts to≤1.5e-14 points;7 matched one-epoch fit pairs have
  exactly identical parameters. See `...v14_reuse_audit_release/receipt.json`.
- Intentional interruption after an epoch resumes to **bit-identical** two-epoch
  parameters; a completed resume does no additional batches. See
  `...v14_resume_audit/receipt.json`.
- Both48-case all-arm/seed smokes completed. The current-origin run produced80
  forecast/report paths and6,392 fixture/intervention rows. Independent fixture
  reconciliation: maximum native-point error≈2.6e-5pts/100; ORB error<1.5e-6/100.
  Every isolated recovery increase was nonnegative in native points, and all
  point-calibration slopes were nonnegative. This does not settle whole-player
  swaps or out-of-distribution calibration.
- Current reader/ensemble/phase/calibration-plot outputs also complete at
  `...v14_smoke_report_review`. The calibration figure was visually inspected.
  For mixed seed/ensemble CSVs, read `seed` explicitly as a string; chunked pandas
  inference can otherwise split numeric seed labels across types.

## Next checkpoint

1. Let the bounded pilots finish; verify every receipt and inspect actual curves,
   gradient/head growth, budgets, ledgers and reports. Pilot point calibration
   lacks intervening histories: do not interpret these scores as campaign ranks.
2. Resolve any operational/report issue without changing the registered model
   matrix or overwriting completed fits. Use new derived report prefixes.
3. Record pilot CPU/wall time, selected epochs, report overhead and disk sizes;
   estimate1,968 new arm-seed-origins/3,936 fits plus336 verified reused origins.
   The original36–60h planning estimate is not yet replaced by a verified estimate.
4. Finish acceptance, freeze/preflight, and supply Adam verified full background,
   live-log, status, resume and leaderboard commands. **Do not launch full training
   until Adam asks.** Pilot completion does not chain into the full campaign.

All three product standards remain equal. The mechanism is a statistical
facilitation hypothesis and stationary renewal approximation, not identified
causal box-out value. Finite-game coverage and seed/checkpoint sensitivity are
not calibrated uncertainty for a hypothetical lineup's latent mean.
