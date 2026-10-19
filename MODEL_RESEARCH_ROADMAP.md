# Research roadmap

Updated 2026-10-15. Priority sets the order of work, not the standing of the
three pillars. The previous long-form backlog, including its R01–R16
discussion, is preserved at
[docs/history/MODEL_RESEARCH_ROADMAP_2026-10-09.md](docs/history/MODEL_RESEARCH_ROADMAP_2026-10-09.md).

## Queue

| Priority | Work | Pillar | Notes |
| --- | --- | --- | --- |
| Done 2026-10-16 (P0) | Clean data into the tool | all | Adam, 2026-10-14/15. The tool's default is the clean release; the review copy shows it ([release](reports/clean_release_2026_10_16.md)). Next: Adam's go-ahead to publish v1. |
| After v1 (Adam, 2026-10-15) | Research direction for v2 | all | Adam: publish v1 first, then "return to all this feedback and use this review to direct the research." The review is [reports/fable_review_101526.md](reports/fable_review_101526.md): cheap diagnostics first (simulation check of the discovery pipeline, forced-lineup cohort, band coverage; Adam: if the simulation shows real synergies cannot be found under coach selection, that negative result is itself worth an article), then uncertainty that moves (state posteriors, τ by support), then structure that binds in range (who-guards-whom, slot offense, best-passer creation term, possession chaining, monotone pooling), then one model across eras. |
| Running (Adam, 2026-10-16) | Refresh every tool number on the clean data | 1, 2, 3 | Adam: "refresh all the components that produce numbers for the tool"; two laptop cores. The history, era fits, modules, discovery, layer, band and record refitted on the clean data, then a `refresh` source ([protocol](reports/refresh_protocol_2026_10_16.md)). |
| P1 (Adam) | Second discovery round for measured combination effects | 2 | 56 of 511 type-pair cells show a missed interaction in 2022–26. Select in one era, replicate in another, and fit the survivors jointly into the layer. |
| P2 | Remaining pages and parser cases | 1 | Pages for the other 25,850 old games (one parser everywhere, a box-score check of every season; about 50 h at the site's rate). The 55 parse failures: scorer absent at his scoring event (29), substitution inconsistencies (15), unresolved period starters (5), the score check (4), players missing from `nba.players` (2). |
| P2 (Adam) | Data refresh for 2026–27 and scoring the frozen prospective record | 1, 2, 3 | After the season's games; `lineups.ingest` with Adam's go-ahead. |
| P2 | "Find the missing piece" | product | Built and merged 2026-10-15: a screen, then exact forecasts until the screen's error rules out the rest, then ranges, against a league-average lineup or Team B's five. Under a second for 2025–26 players on two cores ([tool/README.md](tool/README.md)). Publishes with the clean release. |
| P2 | Port the capability library | 1 | Code health. It still runs the legacy code, now in parallel season blocks (`scripts/library_blocks.py`). A cold start equals the sequential chain to 1e-10. |
| P2 | Perimeter coverage and offensive creation laws | 2 | Learned versions are inert, and real lineups bound the coverage cost (under about a point at shortfall 2). Only asserted magnitudes or era support remain; keep them as named assumption models. The band still has no offense-side alternative, so "no ball handler" adds no width. |
| P3 | Possession-entry coupling | 1, 2 | Live-ball turnovers lead to transition; crashing the offensive glass trades against transition defense. |
| P3 | Dynamic player state | 3 | A latent state, Kalman-style, so that player-state uncertainty propagates, especially for rookies and thin histories. |
| P3 | Slot-filling offense, possession chaining, who-guards-whom, familiarity layer | 1, 2 | Ideas 7, 2, 1 and 4 in the [ideas report](reports/architecture_and_ideas_2026_10_12.md). Pillar-2 bets for a later version; the [headroom check](reports/nn_vs_linear_2026_10_12.md) expects no accuracy payoff. Familiar defensive fives beat the forecast by about 2 points in both eras (candidate optional layer). |
| P3 | Rebound facilitation, tracking inputs | 1, 2 | These carry over from the earlier backlog. |

**Done since 2026-10-09**, with reports:
- [Refactor](docs/REFACTOR.md), saved-weight diagnosis, property suite and coverage screen.
- [Capacity confirmatory](reports/capacity_confirmatory_results_2026_10_12.md) and [era backtest](reports/era_backtest_results_2026_10_12.md): capacity is the band's alternative.
- Two-phase training; the frozen [2026–27 prospective test](reports/prospective_2027q1_protocol_2026_10_09.md).
- [Cross-era check](reports/cross_era_2026_10_12.md) and the close-out to Lineup Lab ([docs/CLOSEOUT.md](docs/CLOSEOUT.md)): release, player-seasons, band, explanations, export, and the private review copy.
- [Interaction discovery](reports/interaction_discovery_results_2026_10_13.md), the [measured combination layer](reports/combination_layer_results_2026_10_13.md) and the [learned module](reports/learned_module_confirmation_results_2026_10_14.md) at half strength.
- Overall quality; the [name-matching fix](reports/name_matching_fix_2026_10_14.md).

## Settled for now (reopen only with a new hypothesis)

- **Generic capacity sweeps.** Width, attention, extra message rounds, free
  phases and multi-NN ensembles gave no gain (v4–v9, v16).
- **Learned coverage and creation terms fitted on 2016–2026 rows.** A
  per-attacker matched defender, tethered help and a best-passer/best-shooter
  teammate head were non-inferior but learned almost nothing (2026-10-09
  screens). Reopen with more support, such as the 2002–2013 era, or
  with an asserted magnitude.
- **Defense-side capacity laws on in-range data.** The era backtest shows
  big defenses do better than forecast in range, not worse. Reopen only for
  four or more bigs, which no data reach.
- **Order-statistic pooling for accuracy.** Best and worst player rates
  explain under 0.2% of the network's residual for every event
  (exploratory, 2026-10-12).
- **v20.** Clock-adjusted capability profiles and S5 checkpoint selection gave
  no point, transfer, coherence or uncertainty gain. S5 does improve count
  likelihood.
- **Decoder clock context (v19–v20).** It improves conditional event
  prediction, not common-environment ratings.
- **The full-history deployment-risk census as run in v20.** It left four
  supported cells, so it is underpowered.
- **Identity-based off×def matchups and pair bilinear/embedding chemistry.**
  These are at the noise floor or caused by selection leaks.
- **Previous-quarter shooting-residual corrections.** They worsen all 11
  seasons.
- **Fitted distance-based shrinkage schedules.** They cannot be fitted on this
  corpus.
