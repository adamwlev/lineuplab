# Status

**Updated 2026-10-19 (evening).** v1 is live. The next work is the v2 research. Claude took
over the project on 2026-10-12; see [AGENTS.md](AGENTS.md). Run-by-run detail is in the dated
reports linked below and in git history.

## Live

- **The tool:** https://lineuplab.dev (and www). It is shared with friends first.
  - **What runs it:** an assets-only Cloudflare Worker, `lineuplab`, at version 35f470a8,
    built from `paths.CLEAN/site_2026_10_19_github`.
  - **To rebuild:** `tool/build_lineups.py --site --out DIR`, then
    `node scripts/page_check.mjs DIR index.html` (34 checks).
  - **To redeploy:** the command in `tool/wrangler.jsonc`. Wrangler is signed in to Adam's
    account on this laptop.
- **The code:** https://github.com/adamwlev/lineuplab, public, MIT licence, with a fresh
  history (first commit 753f774).
  - **To update it:** run `scripts/publish_repo.sh ../lineuplab "message"`, read the commit,
    then push with Adam's go-ahead.
  - **What stays private:** the downloader, the golden fixtures and `tool/five.html`.
  - **This repository stays private** because of its history: it holds the old database
    password, scraped caches and a personal email.
- **The private review copy:** https://claude.ai/artifact/WC4QmzeJshrnneQ4HXzk8G, version 14,
  matching the site. Republishing it is pre-approved; list its files before each publish.

The record of the launch, covering decisions, hosting, open source, Sports Reference and the
data at launch, is [reports/v1_launch_2026_10_19.md](reports/v1_launch_2026_10_19.md).

## What v1 is

- **The forecast:** the calibrated network (arm R, three seeds), plus half the learned
  pairwise module, plus 12 measured combination effects. Every number is fitted on the clean
  data.
- **The source:** `lineups.sources.DATA = "refresh"`, the default since 2026-10-19
  ([results](reports/refresh_results_2026_10_19.md)).
- **Accuracy:** the network alone scores r² 0.1594 raw and 0.0988 centered, on 44 quarters
  of 2016–26 lineup quarters.
- **The range:** τ about 3.2 per side and 4.4 on net, plus cross-era variance. Capacity
  defense and two combination alternatives are labelled assumptions.

For readers, [tool/model.html](tool/model.html) explains the model. For the code, see
[NEURAL_MODEL.md](NEURAL_MODEL.md) and [tool/README.md](tool/README.md). The numbers are in
[MODEL_SCORECARD.md](MODEL_SCORECARD.md).

**The data at launch:**
- Every play-by-play event is attributed by Basketball Reference id.
- 6,285 of 32,190 games come from re-downloaded pages: every game since November 2024, plus
  the old games with problems. About 25,900 older games keep the original scrape, with clocks
  repaired.
- 55 games failed to parse.
- No 2026–27 games are in yet.

([clean release](reports/clean_release_2026_10_16.md),
[findings](reports/rescrape_pilot_2026_10_14.md))

## Next: v2

Adam (2026-10-15): after v1, "return to all this feedback and use this review to direct the
research." The review is [reports/fable_review_101526.md](reports/fable_review_101526.md).
Its order, kept in [MODEL_RESEARCH_ROADMAP.md](MODEL_RESEARCH_ROADMAP.md):

1. **Cheap diagnostics on saved models:**
   - a simulation check of the discovery pipeline under coach selection (Adam: a negative
     result would itself be worth an article);
   - the forced-lineup cohort;
   - band coverage.
2. **Uncertainty that moves:** state posteriors, and τ by support.
3. **Structure that binds in range:**
   - who-guards-whom;
   - slot offense;
   - a best-passer creation term;
   - possession chaining;
   - monotone pooling.
4. **One model across eras.**

The product items for v2:
- **Actual results for real lineups.** Adam deferred them until the UI design is worked out.
- **The "relative" setting's cross-era translation.**
- **The polish left from the persona QA:**
  - the 13.7 MB download;
  - accent-sensitive suggestions;
  - share links.

Rule 12 applies: anything that changes what the tool prints gets a protocol before its
results.

## Waiting on others, or on Adam

- **Sports Reference's reply** to the permission request (sent 2026-10-19). The 2026–27 data
  refresh and the prospective scoring depend on it.
- **The EC2 box** (34.210.88.47) is stopped. Adam terminates it.
- **The legacy page's artifact**
  (https://claude.ai/code/artifact/02d5d0e3-d698-495f-97ce-af20074cf1f3) is still up. Whether
  to retire it is Adam's call.
- **Scoring the frozen 2026–27 prospective record**
  ([protocol and freeze](reports/prospective_2027q1_protocol_2026_10_09.md)), after the
  season's games and a data refresh. Never modify `experiments/cache/prospective_2027q1` or
  the store `lineups_store_2027q1_library`.
- **On hold (Adam, 2026-10-19):** pages for the other 25,850 old games, and parser work for
  the 55 failures.
- **Adam's call, optional:**
  - refit the straight-line control on the clean data (about a day; it changes only the
    −0.0015 line);
  - a second discovery round (56 of 511 type-pair cells show a missed interaction).
- **Advised:** rotate the old database password. It is in this repository's history, though
  in no public one.

## Recent history

- **2026-10-19:**
  - v1 launched, with the code open-sourced ([launch](reports/v1_launch_2026_10_19.md));
  - the refresh of every tool number on the clean data
    ([protocol](reports/refresh_protocol_2026_10_16.md),
    [results](reports/refresh_results_2026_10_19.md)): 384 fits and the downstream, with seven
    stops, each fixed. Net moved by an SD of 0.04 points on 120 real fives. The layer went
    from 14 effects to 12.
- **2026-10-18:**
  - first-time-user QA with five personas and two fix passes
    ([report](reports/qa_personas_2026_10_18.md));
  - an overall-quality limit for the missing-piece search;
  - the label "Combinations, both teams" against Team B.
- **2026-10-16:** clean data in the tool ([release](reports/clean_release_2026_10_16.md)).
  The library was rebuilt on a rented box.
- **2026-10-14 and 15:**
  - the name-matching fix ([first stage](reports/name_matching_fix_2026_10_14.md),
    [pages and ids](reports/rescrape_pilot_2026_10_14.md));
  - the learned module at half strength
    ([confirmation](reports/learned_module_confirmation_results_2026_10_14.md));
  - overall quality, the Details sheet, the model page, and "Find the missing piece".
- **2026-10-13:** the tool is built around combination effects
  ([layer](reports/combination_layer_results_2026_10_13.md),
  [discovery](reports/interaction_discovery_results_2026_10_13.md)).
- **2026-10-12:** the close-out ([docs/CLOSEOUT.md](docs/CLOSEOUT.md), complete
  2026-10-19):
  - the network alone ships;
  - capacity is the band's alternative;
  - era-relative inputs are the default;
  - the 2026–27 prospective test is frozen.

## Where things are

| What | Path |
| --- | --- |
| Rebuilt possession table; per-game sources | `nba_pages.possessions`, `nba_pages.game_sources` (database); `nba.possessions` is the original scrape |
| Page cache (play-by-play and box scores) | `experiments/cache/bref_raw/` |
| Exact-id anchors; per-player counts with ids | `experiments/cache/pbp_ids_2026_10_14/`; `experiments/cache/game_player_stats_ids_2026_10_14.pkl` |
| Clean rebuild root (`paths.CLEAN`) | `experiments/cache/rebuild_pages_2026_10_14/experiments/cache/` |
| The refresh (under `paths.CLEAN`): history refits; record; band constants; overall quality; export; comparison | `history_2026_10_16/`; `prospective_2027q1/release_record_refresh.json`; `band_constants_refresh.json`; `player_values_refresh/`; `release_export_refresh/`; `compare_refresh/` |
| Refresh logs and failed partial outputs | `paths.CLEAN/logs/refresh_*.log`; `paths.CLEAN/logs/refresh_failed_2026_10_18/` |
| Site and review builds | `paths.CLEAN/site_2026_10_19_github/` (live); `paths.CLEAN/review_page_v1_2026_10_19_github/` (review copy v14) |
| Public repository clone | `../lineuplab` |
| What the tool shows (switch) | `lineups/sources.py` (`DATA`: names, clean or refresh) |
| Frozen 2026–27 prospective fits and record (never modify) | `experiments/cache/prospective_2027q1/`, store `lineups_store_2027q1_library` |
| v16 store, reference fits, v14 parents | `experiments/cache/lineups_store_v16`, `joint_capability_2026_09_19_v16_fast2_ready/`, `joint_capability_2026_09_15_v14_prod/` |
| Era backtest | `experiments/cache/era_backtest_2026_10_12/`, `lineups_store_era`, `capability_library_era_extension` |
| Persona QA screenshots and findings | `experiments/cache/qa_2026_10_18/` |
| Box bundle and logs | `experiments/cache/box_2026_10_15.tar`; `experiments/cache/rescrape_2026_10_14/box_logs/` |
| Name-fix rebuilds (partial or test, kept) | `experiments/cache/names_fix_2026_10_14/` |
| Worktrees pinned for provenance | `../basketball-legacy` (old code; `scripts/legacy_worktree.sh`), `../basketball-refresh-run` (eb9c97ae), `../basketball-refresh-downstream` (9a214367), `../basketball-era-run`, `../basketball-capacity-run`, `../basketball-missing-piece` (merged) |
