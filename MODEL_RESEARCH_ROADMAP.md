# Research roadmap

Updated 2026-10-19, after v1 went live. Priority sets the order of work, not
the standing of the three pillars. The previous long-form backlog, including
its R01–R16 discussion, is preserved at
[docs/history/MODEL_RESEARCH_ROADMAP_2026-10-09.md](docs/history/MODEL_RESEARCH_ROADMAP_2026-10-09.md).

## Queue

| Priority | Work | Pillar | Notes |
| --- | --- | --- | --- |
| **Now** (Adam, 2026-10-15) | Research direction for v2 | all | Adam: publish v1 first, then "return to all this feedback and use this review to direct the research." v1 is live (2026-10-19). The review is [reports/fable_review_101526.md](reports/fable_review_101526.md): cheap diagnostics first (simulation check of the discovery pipeline, forced-lineup cohort, band coverage; Adam: if the simulation shows real synergies cannot be found under coach selection, that negative result is itself worth an article), then uncertainty that moves (state posteriors, τ by support), then structure that binds in range (who-guards-whom, slot offense, best-passer creation term, possession chaining, monotone pooling), then one model across eras. |
| v2 product (Adam, 2026-10-19) | Actual results for real lineups | 3 | Deferred from v1: "Need to think about how the UI can neatly display this." Observed possessions, net and the finite-game spread beside the forecast. |
| v2 research | The "relative" setting's cross-era translation | 2 | Kept for v1 (Adam, 2026-10-19). It translates an older player's habits into today's league, so the 2016–17 Warriors take 61–69% threes and older lineups move by about 7 points between the settings ([QA report](reports/qa_personas_2026_10_18.md)). |
| P1 (Adam) | Second discovery round for measured combination effects | 2 | 56 of 511 type-pair cells show a missed interaction in 2022–26. Select in one era, replicate in another, and fit the survivors jointly into the layer. |
| P2 (Adam) | Data refresh for 2026–27 and scoring the frozen prospective record | 1, 2, 3 | After the season's games, with Adam's go-ahead. The downloads depend on Sports Reference: a permission request went out on 2026-10-19 ([launch report](reports/v1_launch_2026_10_19.md)). |
| On hold (Adam, 2026-10-19) | Remaining pages and parser cases | 1 | Pages for the other 25,850 old games (one parser everywhere, a box-score check of every season; about 50 h at the site's rate). The 55 parse failures: scorer absent at his scoring event (29), substitution inconsistencies (15), unresolved period starters (5), the score check (4), players missing from `nba.players` (2). |
| P2 | Tool polish carried from the persona QA | product | Left after two passes ([QA report](reports/qa_personas_2026_10_18.md), [launch report](reports/v1_launch_2026_10_19.md)): the 13.7 MB first download, accent-sensitive browser suggestions, and share links (possible now that the site has its own domain). Rerun the five personas on the exact build before sharing widely. |
| Optional | Refit the straight-line control on the clean data | 1 | Changes only the printed −0.0015 trade (earlier data). About a day, six hours of it compute ([refresh results](reports/refresh_results_2026_10_19.md), "Not refreshed"). |
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
- Overall quality; the [name-matching fix](reports/name_matching_fix_2026_10_14.md); "Find the missing piece" (2026-10-15, with a quality limit from 2026-10-18).
- [Clean data in the tool](reports/clean_release_2026_10_16.md) (2026-10-16) and the [refresh of every number on it](reports/refresh_results_2026_10_19.md) (2026-10-19).
- [First-time-user QA with five personas](reports/qa_personas_2026_10_18.md) (2026-10-18).
- [v1 launch](reports/v1_launch_2026_10_19.md) (2026-10-19): https://lineuplab.dev and the open-source code at https://github.com/adamwlev/lineuplab.

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
