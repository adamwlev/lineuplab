# Lineup Lab (the new tool) and the legacy page

## Lineup Lab

`lineups.html` is the new tool, built on the release model (docs/CLOSEOUT.md,
AGENTS.md decisions of 2026-10-12 and 2026-10-13). You pick five
player-seasons (2002–2026) against a league-average lineup or another five,
and it shows:
- offense, defense and margin in points per 100 possessions: the network plus
  the combination effects, with the network-alone number beside it. The
  combination effects are the learned module at half strength
  (`lineups/learned.py`, Adam 2026-10-14) plus the 14 measured effects
  re-measured on top of it. The page shows them in one section (Adam's
  feedback: users don't care which kind an effect is), with the learned part
  as one row per column;
- each player's types, and the combination effects the lineup triggers
  (pairings, what adding up implies, event change, points, evidence, and a
  curve for same-type effects);
- a library of all 14 measured combinations;
- an 80% range, with the reasons it widens;
- the capacity-defense and combinations-keep-adding alternatives;
- a breakdown of how the offense gets its points;
- a **Details** sheet behind every player (Adam, 2026-10-15): the capability
  library's three blocks for that player-season. They are his own game, his
  effect on teammates while he is on the floor, and his effect on the
  players he defends. Each is shown in readable units with its standard
  error and season percentile. The browser model's `profile(row)` reads them
  from the player-season matrix;
- **Find the missing piece** (Adam's idea, 2026-10-14; built 2026-10-15 on
  the `missing-piece` branch). It keeps four of Team A and ranks every
  candidate for the fifth spot. The opponent is a league-average lineup or
  Team B's five (Adam: "optionally allow the user to specify a specific
  lineup"). The page says league average is the slower search, because it
  averages 561 opponents. Candidates are 2025–26 players, or every player at
  his default season, with at least 500 offensive possessions. An optional
  limit on overall quality (Adam, 2026-10-18: realistic trade targets, "they
  don't want to see Wemby come up every time") leaves out candidates whose
  net linear-approximation value is above it; it starts at the replaced
  player's value. It works in two steps:
  1. a screen ranks every candidate with one network per seed and 10 panel
     lineups a side (`search.screen`);
  2. the best get the exact forecast (`search.forecast`, the band's point),
     until the screen's observed error rules out the rest; then the range.

  The list shows exact numbers only. `scripts/screen_check.js` checks the
  screen and the stop rule against exhaustive exact forecasts, against the
  league-average opponent or a named five. `scripts/page_check.mjs` drives a
  built page in headless Chrome (two threads) and checks the quality limit,
  the "now" row, the layout at 400 px, forgiving names, stale results,
  Escape and a reload. `scripts/qa_browser.mjs` is a shared headless Chrome
  for first-time-user QA (one browser at a time; phone, slow-3G and slow-CPU
  emulation; screenshots per persona): see
  [reports/qa_personas_2026_10_18.md](../reports/qa_personas_2026_10_18.md).

  Timings in headless Chrome on two cores (the model's worker and one helper):

  | Search | List appears | Ranges done |
  | --- | --- | --- |
  | League average, 2025–26 players, first search | 0.45 s first, 0.55 s final | 0.85 s |
  | League average, same four again | 0.2 s | 0.5 s |
  | League average, every player at his default season | 1.0 s first, 1.3 s final | 1.6 s |
  | Team B's five, 2025–26 players, new four | 0.28 s | 0.33 s |
  | Team B's five, every player | 0.9 s first, 0.95 s final | 1.0 s |

  The page uses up to three helpers on machines with more cores.

`model.html` is the model details page: the stack, data, player
description, capability estimates, network, calibration, combination effects,
range, overall quality, breakdowns, accuracy and what is not checked. The main
page's technical text lives there; the page keeps a short note and links to
it. Its data section describes the possession table rebuilt from the pages, so
it is published with the clean-data release.

A private review copy is at https://claude.ai/artifact/WC4QmzeJshrnneQ4HXzk8G; republish to that URL.
Replacing the legacy page needs Adam's approval.

**The public site** (Adam approved v1 on 2026-10-19; the domain lineuplab.dev is his) is an assets-only
Cloudflare Worker (`tool/wrangler.jsonc`). `build_lineups.py --site --out DIR` writes `index.html` as a
whole document: the frame the artifact host supplied (doctype, base styles), a description, a link
preview (`tool/preview.png`, 1200×630) and the icon (`tool/favicon.svg`). Check it with
`node scripts/page_check.mjs DIR index.html`, then deploy with the command in `tool/wrangler.jsonc`.
Compressed, the data files come to about 14 MB (a gzip estimate; check it on the live site).

Build and check. `lineups.sources.DATA` (or `LINEUPS_RELEASE`) picks the
release: `names` is 2026-10-14's, `clean` is the one retrained on the rebuilt
data (`scripts/release_clean.sh` runs all of this for it):

```bash
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
PYTHONPATH=. $PY -u scripts/export_release.py       # meta.json, weights.bin, players.bin (15 MB)
PYTHONPATH=. $PY -u tool/build_lineups.py           # inlines lineup_model.js into the page; copies model.html
$PY -m unittest tests.test_tool_parity              # JS vs Python: 1,200 matchups, ratings, bands, reasons,
                                                    # breakdowns, combinations, learned module, player details
```

The built pages and data are in the release's export directory
(`lineups.sources.SOURCE["export"]`: `experiments/cache/release_export_2026_10_12/`
for names, `paths.CLEAN/release_export/` for clean). To publish, the page goes
up with `model.html`, `meta.json`, `weights.txt` and `players.txt` beside it.
The two .txt files are base64 copies of the .bin files, because artifacts don't
serve raw binary.

**Files.**
- `lineup_model.js` is a line-by-line transcription of `lineups/model.py`,
  `players.py`, `release.py`, `support.py`, `band.py`, `explain.py` and
  `combinations.py`.
- The combination layer comes from `scripts/combination_layer.py --learned`
  (`experiments/cache/combination_layer_2026_10_14_learned/layer.json`). The
  export carries it with per-player-season type flags.
- The learned module comes from `scripts/release_module.py`
  (`experiments/cache/release_module_2027q1/`). Its weights follow the
  networks in `weights.bin`. `meta.json` carries its scale and each seed's
  level, and the page computes each ledger with and without it.
- The page runs it in a Web Worker. The first lineup takes about 2 seconds,
  to cache the average-opponent panel; each later one takes about 0.1 s. The
  Details sheet asks the worker for a player's profile, which takes about
  20 ms.
- The missing-piece search adds up to three helper workers. They hold only
  what the screen needs, about a third of the memory of the main worker. The
  exact forecasts and ranges run in the main worker. Within one search, the
  ranges share the capacity arm's attacker-against-defender terms.
- **Speed (2026-10-15).** The ledger is split. `prepare` covers what depends
  on the offense five alone; `settle` covers each defense, with the
  defense's effects entering as exp factors. These run once per lineup and
  are shared by the forecast, the learned module and the breakdown:
  - each five's network inputs and outputs (`fiveOf`);
  - each player's terms (`alone`, `moduleAlone`);
  - one pass over the panel (`pass`).

  Warm lineups are about 9× faster than before. The outputs match the
  previous code to 2e-13, and the Python parity tests pass.
- Checkpoint mixtures weight each seed equally, and each seed's checkpoints
  equally within it. That matches `Release.ledger` when a retrained seed
  keeps fewer than five checkpoints.

## Legacy page

`five.html` (built by `build.py`) is the older additive page at
https://claude.ai/code/artifact/02d5d0e3-d698-495f-97ce-af20074cf1f3.
- It carries a coverage gate, which AGENTS.md now rules out.
- Its export script was retired with the pre-refactor code; run it from the
  legacy worktree.
- Its full notes are in this file's git history, before 2026-10-12.
