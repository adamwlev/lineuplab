# Refactor parity checks, 2026-10-09

The `lineups/` package replaces the pre-refactor research code (tag
`pre-refactor-2026-10-09`) for the retained reference, J_POINT_BOTH. Each
layer was checked against saved production artifacts. All checks are
repeatable: tests under `tests/`, scripts under `scripts/`.

| Layer | Check | Result |
| --- | --- | --- |
| Model (`lineups/model.py`) | Golden 2020q1/s17 batch: 276 rows, 5 games | Final fit and five-checkpoint mixture match the old model and the saved production predictions to 1e-6. Usage ledger conserved; slot order invariant. |
| Scoring (`lineups/evaluate.py`) | Full 44-quarter broad cohort, from saved native predictions | Checkpoint-average-half r² .162989 / RMSE 11.054459; direct-half .162915; pure NN .161482; additive_defense .146023; novel .144502. All identical to the published scorecard; about 40 s per view. |
| Inputs (`lineups/features.py`, 418 MB store) | Outer (origin), training (history) and inner-validation rows of 2016q1, 2020q1, 2026q4 | Bit-identical to the old `TrainingData.batch` (max abs diff 0.0) |
| Training (`lineups/train.py`) | Refit 2020q1/s17 from the saved v14 parent | Same selected epoch (12) and the same validation curve to 7 digits. Weights within 1.2e-6; outer forecasts within 4.7e-5 pts/100. 9 minutes. |
| Matchups (`lineups/coherence.py`) | Five legal centers vs Jokić/Westbrook, 2026q4/s17 | 123.8736 vs 116.1737 (final fit) and 121.2157 vs 115.6240 (mixture), matching the saved v16 follow-up |

## Single-stage training from scratch: exploratory, not equivalent yet

The reference starts each origin from a separately trained v14 offense.
`EventModel.fresh` instead trains everything in one stage, with the same
objective and protocol. The table compares outer-quarter native losses for
seed 17 on identical rows, direct view: single-stage minus reference, so lower
is better for single-stage.

| Origin | Selected epoch | Counts | Location | Conversion | Recovery | Point MSE (pooled by game and offense five) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2016q1 | 7 | −0.00037 | −0.00009 | −0.00010 | +0.00009 | −1.05 |
| 2019q3 | 16 | +0.00002 | +0.00013 | −0.00002 | −0.00006 | −0.08 |
| 2022q2 | 11 | +0.00024 | +0.00118 | +0.00021 | +0.00099 | +10.26 |
| 2025q4 | 5 | −0.00008 | +0.00024 | −0.00008 | +0.00014 | −0.10 |
| Mean | | −0.00004 | +0.00037 | +0.00000 | +0.00029 | +2.26 |

Single-stage is close at three origins and clearly worse at 2022q2. With one
seed, four origins, no calibration and no checkpoint averaging, this neither
establishes equivalence nor rules it out.

**Decision:** keep `EventModel.from_parent` (the exact two-stage path) as the
default for experiments on 2015–2026 origins; saved v14 parents exist for all
48. Before the 2026–27 origins, either port the v14 offense training or
establish single-stage equivalence over all origins and seeds.

Artifacts: `experiments/cache/lineups_single_stage_2026_10_09/` (fits,
predictions, `results.jsonl`) and log
`experiments/cache/lineups_single_stage_2026_10_09.log`.
