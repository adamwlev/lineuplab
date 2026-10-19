# Status

**Updated 2026-10-19 (midday).** Claude took over the project on 2026-10-12; see
[AGENTS.md](AGENTS.md). Earlier day-by-day notes are in the dated reports
linked below and in git history.

## Live 2026-10-19: https://lineuplab.dev

v1 is deployed (Cloudflare Worker `lineuplab`, version fed28b97, from
`paths.CLEAN/site_2026_10_19_credit`; www.lineuplab.dev too). Every live file
matches the build byte for byte; a first visit downloads 13.7 MB (brotli); on
an emulated phone the live page forecasts the default five exactly as the
build does, with no page errors. Redeploy: the command in `tool/wrangler.jsonc`
(Wrangler is signed in to Adam's account on this laptop, by device code).
Adam is sharing it with friends first.

## Decided 2026-10-19 (Adam): v1 goes public

- **Publish v1** on its own domain, on cheap, low-maintenance static hosting.
  Proposed: Cloudflare Pages plus Cloudflare Registrar; candidate domains
  checked against the registries on 2026-10-19; Adam bought **lineuplab.dev**
  and owns the Cloudflare account. The site build is ready
  (`paths.CLEAN/site_2026_10_19_credit`, `build_lineups.py --site`; 34 page
  checks pass in standards mode; Wrangler's dry run reads its 7 files). It
  deploys as an assets-only Worker (`tool/wrangler.jsonc`) once Adam runs
  `npx wrangler@4 login`. Adam said go on 2026-10-19 (friends first), with a
  permission request to Sports Reference sent alongside.
- **Author:** "Adam Levin and Claude Code" (page footer, model page; review
  copy version 12).
- **Open source the project** (Adam: a new clean repository, MIT, no scrape
  scripts): https://github.com/adamwlev/lineuplab, a fresh history made from
  this tree by `scripts/publish_repo.sh` (which lists what stays private: the
  downloader, the golden fixtures and the retired five.html), committed under
  Adam's GitHub noreply address. This repository stays private: its history
  holds the old DB password (17 commits), scraped-data caches up to 695 MB and
  a personal email on every commit. The page parsers moved out of
  `lineups/ingest.py` into `lineups/bref_pages.py` so the downloader alone
  stays private.
- **Raised before launch:** Sports Reference's data-use page says "you should
  not create websites or tools based on data you scrape from Sports
  Reference", and its terms bar using site content to train AI models without
  written permission. Adam (2026-10-19): launch, credit them with a link on
  both pages, and ask permission. **Request sent 2026-10-19** through their
  feedback form (free, credited, no raw data, open-source code without the
  data or download scripts, and downloads of 2026–27 games under their rate
  limit). Waiting on their reply.
- **Kept as is:** the five Goberts colour, and the "relative" setting's
  cross-era translation.
- **Deferred to v2:** actual results for real lineups (the UI needs design).
- **On hold:** the re-scrape of the other 25,850 games. Adam terminates the
  EC2 box (already stopped).

## Done 2026-10-19: the refresh of every tool number on the clean data

The refresh finished at 00:11 ([results](reports/refresh_results_2026_10_19.md)).
The tool's default source is `refresh` (commit f0daea7f); the review copy is
version 11. On 120 real 2025–26 fives it moves net by an SD of 0.04 points
against the clean release; the measured layer has 12 effects (the three
turnover effects dropped, bigs beside defensive rebounders added); the
learned module passes and stays at half strength. Notes from the run follow.

Adam (2026-10-16): "go ahead and refresh all the components that produce
numbers for the tool"; compute: "Laptop, 2 cores". Protocol, committed
before any result: [reports/refresh_protocol_2026_10_16.md](reports/refresh_protocol_2026_10_16.md).

- **What it refits:** everything the clean release still carries from the
  2015–2026 history on the old data: the calibration and league level, the
  band's τ and cross-era terms, the combination layer and its evidence, the
  learned module's check, overall quality and the scorecard lines.
- **Fits** (`scripts/refresh_run.sh`, two niced slots, from the worktree
  `../basketball-refresh-run` pinned at eb9c97ae): history R, then history C
  (2015q1–2026q4 × 3 seeds, two-phase from scratch on the clean store), then
  era R (2006q1–2013q4 × 3 seeds): 384 fits. **Done 2026-10-18 17:35, none
  failed** (about 17 minutes a fit, 51 hours). Log: `paths.CLEAN/logs/refresh_run.log`.
- **Running,** `scripts/refresh_downstream.sh` (from
  `../basketball-refresh-downstream`, now at a24ef5b9; log
  `paths.CLEAN/logs/refresh_downstream.log`), same two slots. At 23:30 the
  cross-era step was running; the band's constants and the release (a new
  source `refresh` beside `clean`) follow. The tool's default switches only
  after the comparison is read.
- **Results so far (clean data):**
  - **Module confirmation:** passes. Half strength, previous-quarter centered,
    +0.0006 r² (SE 0.0010) against the −0.003 bar; full strength −0.0007; all
    fixture bars pass. Half strength stays.
  - **Benchmark:** calibrated network R, r² 0.1594 raw and 0.0988 centered
    (old fits on old data: 0.1615 and 0.1012; not like for like).
  - **Discovery:** 12 measured combinations hold up, not 14. The three
    turnover effects drop; bigs beside defensive rebounders (rim share) is
    added. `lineups.combinations.EFFECTS` is the clean list at the clean root
    and for the refresh source.
  - **Layer forward check:** +0.00001 r² (it enters).
  - **τ²:** offense 10.43, defense 10.04, net 19.80 (old 10.25, 10.45, 19.83).
- **Stops on 2026-10-18, each fixed and relaunched:** zsh `$0` in a function,
  the fixture registry under the clean root, the summaries ordered before
  discovery, era rows with arm R alone, the 12-effect list, and an empty event
  family in the layer's forward check (see `logs/refresh_failed_2026_10_18/`).
- **Ports:** `lineups/history.py` serves the history of the active cache root
  (the v16 reference under the main cache, the refits under the clean root),
  and `paths.CLEAN_ROOT` picks the possession table. Each ported producer
  reproduces its saved output under the main cache (calibration 2e-13,
  benchmark 3e-13, network-vs-linear rows and the learned module exactly,
  band constants to their rounding).
- **Incident:** the first launch started all 384 fits at once (a broken slot
  limiter) and the laptop rebooted at 10:27. Nothing completed; the queue
  now runs through `xargs -P 2`. On 2026-10-18 the downstream's first start
  died silently at the module queue (zsh sets `$0` to a function's name, so
  xargs could not find the script); fixed in e74ab33a, with errexit now
  logged, and relaunched three minutes later. At 21:15 it stopped as designed
  when the six 2026q4 module jobs failed at the fixture scoring: the fixture
  registry was read under the clean root, which has none (now
  `paths.FIXTURES`, the main cache's, at every root). The other 280 module
  jobs are kept. The six partial outputs are in
  `logs/refresh_failed_2026_10_18/`; the queue now counts a job done by its
  record (written last). Relaunched 21:20.

## Done 2026-10-16: clean data in the tool

Adam (2026-10-14/15): "clean data is primary … you can write to the database
… switch to targeted for now … ready and incorporated into the tool end to
end (with any retraining) by Saturday."

The tool's default is now the clean release (`lineups.sources.DATA = "clean"`).
Report: [reports/clean_release_2026_10_16.md](reports/clean_release_2026_10_16.md).

**What was fixed** ([findings, with addenda](reports/rescrape_pilot_2026_10_14.md)):
- Play-by-play actors were matched by printed name. Same-name teammates swapped
  events, and accented, mis-decoded and renamed players lost theirs. Every
  event is now attributed by Basketball Reference id (`lineups/pbp_ids.py`,
  `lineups/names.py`; 98.771% of 40 M events match per-player counts).
- Taylor Hendricks's two ids are merged.
- **`nba_pages.possessions`** (`lineups/page_possessions.py`; `nba.possessions`
  untouched), 6,073,442 possessions:
  - 6,285 games from re-downloaded pages, each matching the official score
    once technical free throws are set aside;
  - 25,905 games keep the old rows, with quarter-start clocks repaired;
  - 55 of them are old pages that failed to parse.

**How it was rebuilt:**
- legacy chain in id mode (`scripts/rebuild_legacy_chain.sh`);
- the capability library (8 × 254 snapshots), era extension (8 × 87) and
  2027q1 extension (8 × 8) on a rented 16-vCPU box, finished 00:28 PDT
  2026-10-16 (`scripts/box_schedule.py`). The copy-back was checked snapshot
  by snapshot;
- stores, player seasons and the release (`scripts/release_clean.sh`,
  00:51–01:55): arms R and C × 3 seeds, learned modules, overall quality,
  export and page. All 31 release tests pass.

**Old against new:** on 120 real 2025–26 fives, margins correlate 0.994 (SD of
the change 0.56 points per 100). The players the fixes touch rise, mostly by 1
to 3 points of overall quality (Nenê by 3.1 a season; González, Carrington,
Krejčí, Jaylin Williams, Jeff Green, Micić).

**Carried, stated on the model page:** the calibration constants and league
level come from the frozen record (old data), and the release has not been
re-scored.

**The box** (34.210.88.47) is idle and no longer needed. Adam's CloudWatch
alarm stops it after 2 idle hours (stop, not terminate). Adam can terminate
it.

## The tool

- **Review copy** (private, Adam-approved feedback loop):
  https://claude.ai/artifact/WC4QmzeJshrnneQ4HXzk8G. Version 12 (2026-10-19)
  adds the author line and version 13 the data credit (build
  `paths.CLEAN/review_page_v1_2026_10_19_credit`); version 11 shows the refreshed release; version 10 added the persona QA fixes, version 9
  simplified the opening, and versions 7–8 the changes below. From version 6 it
  has shown the clean release: fits retrained on the rebuilt data, learned
  combinations at half strength, measured combinations, overall quality. New
  in this version (`tool/`; Adam 2026-10-15):
  - a **Details** sheet behind each player: his own estimates, his effect
    on teammates, and his effect on the players he defends, in readable
    units with standard errors and season percentiles;
  - a **model details page** (`model.html`) that holds the technical text,
    including what is carried and not re-scored;
  - **Find the missing piece** (Adam's idea): it ranks every candidate fifth
    for a four-player core, against a league-average lineup (the slower
    search, and the page says so) or Team B's five. On two cores in headless
    Chrome, a 2025–26 search finishes in under 0.9 s
    ([tool/README.md](tool/README.md)). Version 7 adds an optional limit on
    overall quality (Adam, 2026-10-18: realistic trade targets, not the
    league's best every time). It starts at the replaced player's value.
    Version 8 labels the combinations column against Team B "Combinations,
    both teams": in the margin it is Team A's minus Team B's, so a strong
    five's own pairings (the 2017 Warriors' +1.4) sit in every row.
    `scripts/page_check.mjs` checks both in headless Chrome.
- **First-time-user QA (2026-10-18):** five personas (impatient, skeptic,
  mobile on slow 3G, non-native English, breaker) in a real browser; 47
  distinct findings, ranked; two fix passes; round 2 found 45 of 70 per-persona
  findings fixed, 23 partly, 2 left for Adam. Report:
  [reports/qa_personas_2026_10_18.md](reports/qa_personas_2026_10_18.md). The
  review copy is version 10 with these fixes.
  `scripts/page_check.mjs` (34 checks) and `scripts/qa_browser.mjs`.
- **The public tool:** Adam approved publishing v1 on 2026-10-19; it is not
  live yet (see the top section).
- What the tool computes: [tool/model.html](tool/model.html) for readers, and
  [NEURAL_MODEL.md](NEURAL_MODEL.md) and [tool/README.md](tool/README.md) for
  the code.

## After v1: the v2 direction

Adam (2026-10-15): publish v1 first, then return to the review and use it to
direct the research. The review is
[reports/fable_review_101526.md](reports/fable_review_101526.md); the
roadmap's first row summarizes its order.

## Waiting on Adam

- **The other 25,850 old games' pages** (on hold, 2026-10-19), for one parser
  everywhere and a box-score check of every season (about 50 h of polite
  downloading).
- **The 55 parse failures,** which need parser work.
- **Optional:** refit the straight-line control on the clean data (about a
  day, about six hours of it compute); it changes only the −0.0015 line.
- **A second discovery round** for more measured combination effects: 56 of
  511 type-pair cells show a missed interaction in 2022–26.
- **For the launch:** the Sports Reference question, the domain and the
  Cloudflare account, and the open-source repository's licence and name.
- **Terminating the box** (34.210.88.47, stopped); Adam will do it.
- **Scoring the frozen 2026–27 prospective record**
  ([protocol and freeze](reports/prospective_2027q1_protocol_2026_10_09.md)),
  after the season's games and a data refresh.
- **Before any push:** the old database password is in git history; rotate
  it.

## Recent decisions and results

- **2026-10-14:** the learned combination module enters the forecast at half
  strength, and the layer is re-measured on top of it
  ([confirmation](reports/learned_module_confirmation_results_2026_10_14.md),
  [release](reports/learned_module_release_2026_10_14.md)).
- **2026-10-14:** overall quality, a linear approximation
  (`scripts/player_values.py`). Held-out real lineups land within about 1
  point.
- **2026-10-14:** name matching fixed in two stages
  ([first stage](reports/name_matching_fix_2026_10_14.md),
  [rebuild progress](reports/name_matching_rebuild_progress_2026_10_14.md)).
  The name-only rebuild was superseded by exact ids and kept as a partial
  run.
- **2026-10-13:** the tool is built around combination effects
  ([layer](reports/combination_layer_results_2026_10_13.md),
  [discovery](reports/interaction_discovery_results_2026_10_13.md)). Learned
  module designs were screened in eight steps (`reports/nonlinearity_screen*_2026_10_13.md`).
- **2026-10-12:** close-out ([docs/CLOSEOUT.md](docs/CLOSEOUT.md)):
  - the network alone ships;
  - capacity defense is the band's alternative
    ([confirmatory](reports/capacity_confirmatory_results_2026_10_12.md),
    [era backtest](reports/era_backtest_results_2026_10_12.md));
  - era-relative inputs are the default;
  - the 2026–27 prospective test is frozen.

Comparable metrics are in [MODEL_SCORECARD.md](MODEL_SCORECARD.md). The
queue is in [MODEL_RESEARCH_ROADMAP.md](MODEL_RESEARCH_ROADMAP.md).

## Where things are

| What | Path |
| --- | --- |
| Rebuilt possession table; per-game sources | `nba_pages.possessions`, `nba_pages.game_sources` (database) |
| Page cache (play-by-play and box scores) | `experiments/cache/bref_raw/` |
| Exact-id anchors; per-player counts with ids | `experiments/cache/pbp_ids_2026_10_14/`; `experiments/cache/game_player_stats_ids_2026_10_14.pkl` |
| Clean rebuild root (`paths.CLEAN`): chain artifacts, library, stores, player seasons, release | `experiments/cache/rebuild_pages_2026_10_14/experiments/cache/` |
| Box bundle and box logs | `experiments/cache/box_2026_10_15.tar`; `experiments/cache/rescrape_2026_10_14/box_logs/` after the copy-back |
| What the tool shows (switch) | `lineups/sources.py` (`DATA`: names or clean) |
| Release on 2026-10-14's data: store, modules, player seasons, overall quality, export | `lineups_store_2027q1_library_names_2026_10_14`, `release_module_2027q1`, `player_seasons_2026_10_14`, `player_values_2026_10_14`, `release_export_2026_10_12` |
| Frozen 2026–27 prospective fits and record (never modify) | `experiments/cache/prospective_2027q1/`, store `lineups_store_2027q1_library` |
| v16 store, reference fits, v14 parents | `experiments/cache/lineups_store_v16`, `joint_capability_2026_09_19_v16_fast2_ready/`, `joint_capability_2026_09_15_v14_prod/` |
| Era backtest | `experiments/cache/era_backtest_2026_10_12/`, `lineups_store_era`, `capability_library_era_extension` |
| Name-fix rebuilds and rehearsals (partial or test, kept) | `experiments/cache/names_fix_2026_10_14/` |
| Legacy worktree (old code, shared cache) | `../basketball-legacy` (`scripts/legacy_worktree.sh`) |
