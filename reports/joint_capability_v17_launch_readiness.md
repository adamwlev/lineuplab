# v17 launch readiness — 2026-09-27

**Ready, not launched.** All720 new cases /1,440 inner-final fits remain to run.
Adam must authorize the full run or launch the command below himself.
No scorer promotion, scraping, database access/mutation or input-cache rebuild.

## What is implemented

Five frozen arms, three seeds,48 quarters. Reused J_POINT_BOTH/J_BOTH/additive-
defense/parent controls; no control refits. Original plan and all completed
v16/pilot producers and outputs preserved. The production case writer is a
versioned copy using the **unchanged** v17 training primitives; it corrects
pilot-only output labeling without changing fit behavior.

Three CPU workers, one thread each. Cases within each quarter train concurrently;
the next quarter starts after its predecessor is scored. This retains some
end-of-quarter idle capacity but keeps the chronological scorecard clear.
Completed cases and optimizer journals resume with the same command.

After training, the supervisor automatically runs:

1. Batched512-opponent product-mode evaluation for48 quarters, with first20
   lexicographic broad cells at4096. Reuses verified completed neural controls.
2. All32 frozen fixtures at10 dates, all ordered matchups/mirrors including
   prior-common units, native per-player/location/renewal/flow ledgers, direct/
   half calibration, independent permutations and fixed capacity curves.
3. Separate candidate-specific direct/half U0 and constant U1, prior quarters
   only, on the original balanced-date pairs. No new U2 fits or coverage gate.
4. All-view/all-cohort pooled, quarter and season metrics;16 registered half
   contrasts, season bootstrap/exact swaps/Holm; event losses, stopping epochs,
   residual correlations, bias decomposition, average-mode and uncertainty
   summaries, unchanged real analogues and outcome-selected top/bottom10 audit.
5. A three-pillar Markdown review packet. It preserves null/adverse outcomes
   and requires interpretation; it cannot promote a model automatically.

See [derived-output conventions](joint_capability_v17_analysis_conventions.md).
Capacity interventions change allocator supply only, not the input profiles or
the other shortage responses. No synthetic winner or monotonic rating is forced.
Native budget-unit allocation is not an estimate of causal realized assists.

## Verification and quantitative evidence

- Original five-case pilot:552.08seconds,10fits, zero failures. Point arms
  selected7epochs; event-only selected9. Not a scientific winner-selection run.
- **33 launch-gate tests passed**, including exact interrupted/resumed fit
  equality, source rejection, allocation/accounting and production schedule
  guards. Two additional handoff-rendering tests passed using actual pilot
  tables and an explicitly empty fixture-schema stub in a temporary directory.
- Production preflight verified all288 inner/final contexts and288 reused
  control cases across48dates; exact prefix hashes/cutoffs/normalizer counts
  and dated-parent file identities match. Neither inner validation nor outer
  evaluation overlaps its prohibited training partition.
- Actual production calibration branch reproduced **576 control/view cases**
  (48dates ×2arms ×3seeds ×2views), not only a duplicated test formula.
- Independent batched inference at2016q1 and2026q4, both neural controls,
  all3seeds, first20cells at512/4096 reproduced archived average direct/half
  values: largest discrepancy **4.27e-14pts/100**.
- All seven architectures passed the21 registered2026q4 input probes,
  including duplicate profiles. New-arm probes used archived initialization
  weights, **not** pretend trained v17 scientific results.
- A strict per-player permutation tolerance initially rejected one difference
  of1.67e-6PPP (.000167pts/100) on a repeated/extreme fixture. The updated
  diagnostic tolerance is5e-6PPP absolute plus1e-5relative, with a separate
  total-rating tolerance1e-4pts/100 plus1e-6relative. No model computation or
  training changed. The failed audit is preserved; audit2 passed in71.16seconds.
- The completed pilot passed through the full point/average/U0-U1/analogue
  summary pipeline. All16 contrasts are emitted as **descriptive pilot deltas**,
  without inferential p-values. Production requires the full primary schedule.
- Additional identified-U1 check: current constant-U1 fitting reproduced the
  archived J_POINT_BOTH:half and J_BOTH:half2026q4 parameters from2,249 prior
  balanced-date pairs each, max parameter discrepancy4.45e-16. Cold-start pilot
  uncertainty remains honestly unidentified; this checks the non-cold path.
- Read-only status, empty pre-launch report, repeated preparation and shell
  syntax checked. Second prepare reverified readiness without launching fits.

No production numerical improvement is claimed before the run. The original
pilot broad sample was187cells /23,039possessions; half RMSE ranged10.807–10.897
across the five new arms, versus10.825 for the cold-start point control. The
small single-quarter differences do not decide model direction.

## Runtime and storage

Estimate uses the observed pilot per-epoch slowdown by arm, each corresponding
v16 control's entire48-origin/3-seed stopping trajectory, three workers, and20%
queue/process allowance:

| Scenario | Training | Downstream allowance | Total |
| --- | ---: | ---: | ---: |
| Reference-like stopping |29.24h |1–3h |about30–32h |
| Twice that training work |58.49h |1–3h |about60–62h |

These are scenarios, **not confidence limits**. New stopping trajectories are
unknown. The extreme all96-epoch inner/final scenario is about197training hours;
we do not silently lower the cap/seeds if stopping takes longer.

Estimated additional disk:31.49GiB including derived-output allowance; reserve
10GiB. Preflight physical free space:122.74GiB. Pilot fits are **not reused**:
production campaign receipts differ; redoing five of720 cases costs<1% ofcases.

## Launch and monitoring

Run from `/Users/adam/Documents/basketball`. Preparation already created the
directories. This launches training and all follow-up stages; it has **not**
been executed by Codex:

```bash
nohup /usr/bin/caffeinate -i bash experiments/run_joint_capability_v17.sh run --run-dir experiments/cache/joint_capability_2026_09_27_v17_prod >> experiments/cache/joint_capability_2026_09_27_v17_prod/logs/launcher.log 2>&1 < /dev/null &
```

Live stage/results log (the runner writes this itself even without nohup):

```bash
tail -f experiments/cache/joint_capability_2026_09_27_v17_prod/logs/run.log
```

Progress, active worker PIDs and completed-case percentage:

```bash
bash experiments/run_joint_capability_v17.sh status --run-dir experiments/cache/joint_capability_2026_09_27_v17_prod
```

Matched chronological leaderboard, once a primary quarter completes:

```bash
bash experiments/run_joint_capability_v17.sh report --run-dir experiments/cache/joint_capability_2026_09_27_v17_prod --sort r2 --slice all --view half
```

Views:direct,half,checkpoint_average,checkpoint_average_half.
Slices:all,novel,recurring,thin,debut. Sort:rmse,mae,r2,corr,bias.
2015 supplies calibration history but is excluded from primary metrics.

Verbose individual epoch log example:

```bash
tail -f experiments/cache/joint_capability_2026_09_27_v17_prod/queues/training/2015q1/logs/2015q1_O_FLOW_s17.log
```

Later-stage logs: `queues/average/logs`, `queues/basketball/logs`,
`queues/uncertainty/logs/chronological_u0_u1.log`,
`queues/summary/logs/three_pillars.log`, `queues/handoff/logs/review_packet.log`.
Same launch command resumes verified work after an interruption. Do not edit
fingerprinted producers or delete completed artifacts to force a restart.

## Output and evidence map

Native run prefix:`experiments/cache/joint_capability_2026_09_27_v17_prod`.
Derived sibling prefixes append `_scored`, `_average`, `_basketball`,
`_uncertainty`, `_summary`, `_handoff`. Final packet:
`experiments/cache/joint_capability_2026_09_27_v17_prod_handoff/HANDOFF.md`.

Development evidence under `experiments/cache/`:

- `joint_capability_2026_09_27_v17_production_audit2`: successful full control
  replay, average-mode checks and late fixture input probes; audit1 preserved.
- `joint_capability_2026_09_27_v17_summary_dev2`: complete pilot derived tables;
  dev1 preserved (sufficient-statistic field-name fix, no model change).
- `joint_capability_2026_09_27_v17_integration_audit1/logs`: durable development,
  production replay, identified-U1 and report-rendering test logs.
- Production prefix `preflight.json`, `manifest.json`, `logs/preflight_tests.log`:
  ready-state receipts, full source/code fingerprints and33 passing tests.

After completion: independently inspect all three pillars, registered contrasts,
event/point tradeoffs, real analogues and uncertainty proper scores. Preserve
the v16 candidate until that discussion. No automatic promotion or new tuning.
