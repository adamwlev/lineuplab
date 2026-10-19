# Era backtest 2006–2013: protocol — 2026-10-12

**Status: frozen before any era fit.** Adam approved the run on 2026-10-12.
The scorer, `scripts/era_score.py`, is committed with this protocol and is not
revised after results are seen. Any other analysis is labeled post hoc. The
motivation is in the [proposal](era_backtest_proposal_2026_10_09.md).

## Why this era

The 2015–2026 benchmark stays the primary accuracy test. In it, lineups with
three or more bigs on defense are 0.1–1.4% of possessions. The reference and
the capacity-law model disagree almost only where there are no outcomes.

In 2006–2013 such defenses are 3–5% of possessions, about 60k in the scored
quarters. Here the two architectures meet real outcomes for the lineup shapes
where they differ. The era also tests training and forecasting outside
2015–2026, which cross-era use of the tool assumes.

## What is run

- **Store.** `experiments/cache/lineups_store_era`, built by
  `scripts/build_era_store.py`:
  - quarter windows for 2002–2013;
  - ported state sweeps, normalizers and environment;
  - library: the era snapshots 2001-12 to 2009-02 (`library_extend.py --era`),
    followed by the v16 library from 2009-03. All snapshots before 2014 use
    the cold penalty, as the saved library does.
- **Training rows.** They start at 2001-12-01, the first snapshot, so the
  2006 origins see about four years instead of five.
- **Arms.** R (reference architecture, broadcast defense) and C
  (CapacityDefense version 2).
  - Each is two-phase from scratch with self-references, as the 2026–27
    prospective arms are (`scripts/era_run.py`).
  - 32 origins, 2006q1–2013q4.
  - Seeds in order 17, 23, 41: all origins finish at seed 17 before seed 23
    starts.
- **Forecast.** The neural model alone, calibrated (Adam's direction). There
  is no additive control in this era.

## Contrasts (`scripts/era_score.py`)

- **Population.** Scored quarters are 2007q1–2013q4 (28 quarters, 7 seasons);
  2006 is calibration warmup.
  - Each forecast is calibrated per seed by the prior-only affine on earlier
    era quarters' broad cells, then averaged over the seeds complete for both
    arms at every origin.
  - The analysis runs with whatever seeds are complete. Seed 17 alone is the
    minimum.

1. **Big-defense gradient.** Residual, actual minus forecast (points per 100),
   on rows whose defense has three or more bigs (82 in or taller), minus the
   residual on rows with at most one big.
   - A model that is right about big defenses has a gradient near zero.
   - Reported: each model's gradient and C − R, with season-level SEs.
   - Selection that affects big lineups equally under both models cancels in
     the paired difference. Neither model's raw gradient is free of
     deployment selection.
2. **Accuracy non-inferiority, C vs R.** Broad offense-five cells (at least
   50 possessions per quarter):
   - raw r² as in the main scorecard;
   - centered r², within quarter.

   Non-inferior if the difference − 1.943 × season SE > −0.003 (t, 6 df).

**Secondary.** Residuals by defensive big count (0, 1, 2, 3+) for each model,
and per-season tables.

## Power

- **Gradient.** About 60k three-big possessions give each model's gradient a
  season-level SE of roughly 0.5–1 points.
  - A dry run of the scorer on 2016–2026, with seed-17 reference and capacity
    forecasts, gave a paired C − R SE of 0.17 from only 26k such possessions.
  - That dry run is post hoc to the confirmatory run and is not an era
    result. It gave R's gradient +0.05, C's −0.35, and C − R −0.40 ± 0.17.
- **Accuracy.** With 7 seasons and the 2016–2026 per-season SD of the
  centered difference (about 0.002), the SE is about 0.0008. A true −0.002
  would fail.

## Pipeline and cost

`scripts/era_pipeline.sh` runs the stages in order. Each stage resumes:

1. library chains;
2. store build;
3. fits, 9 at a time;
4. scoring.

- **Expected time.** About 1.5 hours for the library, then about 1 hour for
  the store, 2.5 hours per seed for the fits, and minutes for scoring.
- **Pinned code.** It runs from a worktree pinned at the commit that adds this
  file (`../basketball-era-run`, with `experiments/cache` shared).
