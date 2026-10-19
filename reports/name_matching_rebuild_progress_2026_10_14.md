# The name-matching rebuild: progress and checks — 2026-10-14 (evening)

This tracks the [plan](name_matching_rebuild_plan_2026_10_14.md). Everything
lives under `experiments/cache/names_fix_2026_10_14/`:
- `off/`: the legacy builders with the fix switched off;
- `on2/`: the same builders with the fix on;
- `logs/`: one log per run.

Runner: `scripts/legacy_names.py` runs a legacy builder with the fix at the
database boundary. It folds names and texts and rewrites a player's other
printed forms to his canonical one, per possession, never onto another
player's name. The working directory is the root, so the legacy relative
paths land there.

## Parity: the fix off reproduces every original exactly

| Artifact | Fix off vs original | Fix on: what changes |
| --- | --- | --- |
| per-player counts (`lineups/player_counts.py`) | exact (668,380 rows) | 119,387 events recovered for 22 players |
| shot events (`shot_quality`) | exact | 20,070 shots gain a shooter; no matched shot changes |
| possession channels | exact | turnovers, steals, rebounds and FTA gain events |
| v14 extract (texts and names) | exact (content) | folded texts; fixed names |
| v3 per-slot table (`game_lineups.npz`, all 21 arrays) | exact | 6,969 rows gain FGA; 6,584 more rows fully observed |
| v3 player states | exact | 2,520 player-game states move by more than 0.05 |
| v14 rebound labels and events | exact | 8,515 rows gain rebound attributions |
| v14 rebound states | exact | 2,841 player-game rebound rates move by more than 0.005 |
| v15 inputs (matchups, defense states) | exact | labels change as expected (see below) |
| v16 phase labels | exact | 21,689 more possessions qualify for training |
| v16 training inputs (27 arrays) | exact | only label arrays change |
| v16 capability library (first 2–3 snapshots of all 8 chains) | exact | full fix-on run in progress |

**Defense states.**
- For the affected players, their own steal, block, rebound and foul rates
  move by up to 0.08.
- Every other player moves by a median of 0.001 (99th percentile 0.004). The
  cause is shifts in opponent-allowed and league rates, against feature
  spreads of 0.004–0.08.

## Outside check: Basketball Reference box scores

`scripts/box_score_check.py` compares the play-by-play counts with 2,493
cached box scores from 2024–25 and 2025–26, covering 1,146 player-seasons.

| Play-by-play / box score, league total | Legacy | Fixed |
| --- | ---: | ---: |
| FGA | 0.9812 | 0.9877 |
| FTA | 0.9764 | 0.9796 |
| Turnovers | 0.9903 | 0.9987 |
| Offensive rebounds | 0.9799 | 0.9840 |
| Defensive rebounds | 0.9934 | 1.0000 |
| Steals | 0.9938 | 1.0000 |
| Blocks | 0.9689 | 0.9732 |

- **Below 0.95 of box-score FGA.** Among player-seasons with 200+ FGA, 7 of
  679 legacy and 1 of 679 fixed fall below 0.95.
  - Krejčí, Micić, Carrington and González went from 0.000 to 0.986–0.996.
  - Fixed-data median: 0.9885 (1st percentile 0.966).
- **The remaining outlier.** Jalen Williams 2024–25 is at 0.942. Oklahoma
  City's Jaylin Williams prints the same ("j. williams"), and the stored text
  cannot tell them apart.

## Known limits (not fixed)

1. **Same printed name on one five.** Morris twins, the Greens and the
   Williamses: 0.27% of possessions overall, peaking at 1.5% in 2014–15.
   Events go to the first matching player.
   - The cached raw pages (2024–26) carry player links and could resolve
     it.
   - Older seasons would need a re-scrape, which needs Adam's approval.
2. **Events by players absent from the recorded five.** About 1.2% of
   events, often around substitutions. Unchanged.

## Next

1. The fix-on library: 8 chains started at 17:02 with one thread each, as
   the original. The location chains took 14–17 hours originally.
2. Then:
   - the era and 2027q1 library extensions (`scripts/library_extend.py`, run
     on the new library);
   - the stores, using `lineups.states.origin_states` and normalizers;
   - the player seasons;
   - the release retrain (arms R and C, 3 seeds);
   - the learned modules and overall quality (`scripts/player_values.py`);
   - the export and parity tests;
   - an old-vs-new forecast comparison;
   - Adam's decision on rerunning history.

## Correction, 2026-10-14 (night): superseded by exact ids

- The re-scraped pages give every event's players by id
  ([pilot findings](rescrape_pilot_2026_10_14.md)).
- The fix-on rebuild here still leaves two errors:
  - same-name teammates on the floor (1.16% of possessions), credited to
    whoever comes first in the lineup;
  - Taylor Hendricks's two ids.
- The id rebuild (`scripts/legacy_names.py --ids`) replaces it once every
  page is downloaded. The library run started at 17:02 continues as an
  interim.
- **Stopped 20:58** at Adam's request ("kill anything that is no longer
  needed"). The run is partial: chains at snapshots 2010-04 (location),
  2012-05 to 2012-07 (conversion), 2014-10 to 2015-02 (counts), 2019-12 to
  2020-12 (recovery). Its output directory is kept, labeled partial, and is
  not used.
