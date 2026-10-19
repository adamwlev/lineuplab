# The release on the clean data (2026-10-16)

Adam (2026-10-14/15): "clean data is primary … ready and incorporated into the
tool end to end (with any retraining) by Saturday." This is that release. The
tool's default (`lineups.sources.DATA`) is `clean` from 2026-10-16.

## What it is built from

- **Possessions:** `nba_pages.possessions` (6,073,442 possessions). 6,285 games
  come from re-downloaded pages, each matching the official score once
  technical free throws are set aside. The other 25,905 games keep the old
  rows, with quarter-start clocks repaired and Taylor Hendricks's two ids
  merged; 55 of them are old pages that failed to parse
  ([findings](rescrape_pilot_2026_10_14.md)).
- **Players:** every play-by-play event is attributed by Basketball Reference
  id (`lineups/pbp_ids.py`), not by printed name.
- **Rebuilt from that table** (`paths.CLEAN`): the legacy chain (context, text
  readers, v3, v14–v16 inputs), the capability library (8 chains × 254
  snapshots), the era extension (8 × 87) and the 2027q1 extension (8 × 8), the
  stores and the player seasons.
  - The library ran on a rented 16-vCPU box (2026-10-15 to 00:28 PDT
    2026-10-16; `scripts/box_schedule.py`). The copy-back was checked
    snapshot by snapshot and every chain's receipt is present.
- **Retrained** (`scripts/release_clean.sh`, 00:51–01:55):
  - arms R and C, seeds 17, 23 and 41, on 336,699 training rows (the frozen
    record had 335,763; the difference is the restored short and empty games);
  - the learned combination module, three seeds, level removed on 2026q4;
  - overall quality, the export and the page.
- **Carried, not refitted:** the calibration constants and the league level
  come from the frozen record (2015–2026 backtests on the old data). Slopes
  are 0.78–0.83, identical to the frozen record. Refitting them means
  rerunning the history (about 130 fits), which is waiting on Adam.
- **Not re-scored.** The scorecard's accuracy numbers were measured on the
  old data. The model details page says so.

## Checks

- All 31 release tests pass on the clean root (parity of the browser model
  with Python, the release, players, learned module, band, explanations).
- The full suite (120 tests) passes with `clean` as the default.
- The frozen 2026–27 prospective record was not touched: the retrained fits
  live under `paths.CLEAN/prospective_2027q1`.

## Old release against new

Old: the 2026-10-14 release (frozen fits, name-fixed player states). New: the
clean release. Both as the tool shows them: arm R, calibrated, each against its
own league-average panel. Output: `paths.CLEAN/compare/`.

**Real 2025–26 fives** (120 sampled, at least 150 offensive possessions; points
per 100 possessions):

| | Mean change | SD of change | Largest change | Correlation |
| --- | --- | --- | --- | --- |
| Offense | −0.20 | 0.37 | 1.44 | 0.992 |
| Points allowed | −0.19 | 0.39 | 1.11 | 0.992 |
| Margin | −0.01 | 0.56 | 1.56 | 0.994 |

Forecasts for real lineups barely move. Offense and points allowed both drop
by about 0.2, so margins are unchanged on average.

**Overall quality** (net points per 100 against a league-average lineup,
era-relative; a linear approximation of the network, `scripts/player_values.py`):

- Across all 12,374 player-seasons in both releases: correlation 0.966, mean
  absolute change 0.36; 441 move by more than a point.
- 2025–26 only: correlation 0.97, mean absolute change 0.35.

**Players the fixes touch** (old → new):

| Player | Problem | Seasons | Old | New |
| --- | --- | --- | --- | --- |
| Nenê | Read under another name ("n. hilario") | 2003–2019, mean | −2.64 | +0.46 (each season +1.3 to +4.5) |
| Hugo González | Printed as "h. gonzález peña" | 2026 | −3.94 | −0.56 |
| Carlton Carrington | Printed as "b. carrington" | 2025 / 2026 | −4.87 / −5.58 | −3.29 / −3.18 |
| Vít Krejčí | Accents | 2026 | −3.22 | −1.27 |
| Vasilije Micić | Name mis-decoded in `nba.players` | 2024 / 2025 | −3.30 / −4.74 | −2.49 / −3.57 |
| Jaylin Williams | Same-name teammate (Jalen) | 2023 / 2024 | −3.89 / −2.39 | −2.00 / −0.40 |
| Jalen Williams | Same-name teammate (Jaylin) | 2025 / 2026 | 2.47 / 1.34 | 2.27 / 1.18 |
| Jeff Green | Same printed name as Jalen Green ("j. green") | 2024 / 2025 | −4.41 / −3.91 | −2.69 / −2.96 |
| Jalen Green | Same printed name as Jeff Green | 2025 / 2026 | −1.87 / −1.85 | −1.88 / −2.07 |
| Taylor Hendricks | Two ids, now one | 2024 / 2025 / 2026 | −2.59 / −2.34 / −1.18 | −2.22 / −3.06 / −1.48 |

The players who lost events under name matching rise, mostly by 1 to 3
points. The higher-usage player of each same-name pair (Jalen Williams, Jalen
Green) barely moves, because the swapped events were a small share of his
own. The 2026-10-14 release had already fixed the name matching in the player
states. The clean release also rebuilds the capability library and retrains
the fits on correctly attributed events, which is where the remaining change
comes from.

**Largest 2025–26 movers outside the fixes** are about ±1.4: Luka Dončić +1.40,
Luguentz Dort −1.33, Kyle Lowry −1.26, Alex Caruso −1.15, Zion Williamson
−1.07. These come from retraining on the rebuilt data, not from a named fix.
How much of a change this size a refit alone produces was not measured.

## Where it is shown

The private review copy (https://claude.ai/artifact/WC4QmzeJshrnneQ4HXzk8G,
version 6) shows this release, with the player Details sheet, the model
details page and the missing-piece search. The public tool is unchanged.

## What it does not settle

- The calibration and every accuracy number in the scorecard rest on the old
  data until the history is rerun.
- The other 25,850 old games still use the old scraper's possessions (with
  repaired clocks), and the 55 parse failures keep the original rows.
- The release has no forward score on clean data yet.
