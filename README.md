# Lineup Lab

The code and research record behind **[Lineup Lab](https://lineuplab.dev)**, by Adam Levin and
Claude Code. MIT licence ([LICENSE](LICENSE)). Questions and bug reports are welcome as issues.

**No data is included.** The model is trained on play-by-play from
[Basketball Reference](https://www.basketball-reference.com/) (Sports Reference LLC), which is
not redistributed here. The scripts that downloaded it, the golden test fixtures (rows derived
from it) and the retired `tool/five.html` page are not in the public repository
(`scripts/publish_repo.sh` lists what is left out). Most scripts and tests need that local data,
so this repository is for reading and reuse rather than a one-command rebuild.

Pick two five-player lineups and ask how they would do against each other, not
just how their individual ratings add up. Players are player-seasons from 2002
onward. Lineups may mix eras and need not have ever played together. The
opponent defaults to a league-average five.

The output is offense, defense and margin per 100 possessions, the basketball
reasons behind them, and an honest uncertainty band.

Three goals have equal standing:

- forward predictive accuracy;
- coherent answers for weird lineups;
- uncertainty that widens, with a stated reason, outside observed lineups.

## Where to look

| Question | Page |
| --- | --- |
| Goals, decisions of record, authority and working rules | [AGENTS.md](AGENTS.md) |
| What is happening now and what is next | [STATUS.md](STATUS.md) |
| How retained models compare | [MODEL_SCORECARD.md](MODEL_SCORECARD.md) |
| The research queue | [MODEL_RESEARCH_ROADMAP.md](MODEL_RESEARCH_ROADMAP.md) |
| How the retained neural model works | [NEURAL_MODEL.md](NEURAL_MODEL.md) (code) and [tool/model.html](tool/model.html) (for readers of the tool) |
| The tool, its build and publishing | [tool/README.md](tool/README.md) |
| Dated results | [reports/](reports/) |
| Superseded plans, journals and reviews | [docs/history/](docs/history/) |

## Layout

| Path | Contents |
| --- | --- |
| `lineups/` | The package. **Model:** `model` (reference, plus optional coverage, capacity-law defenses and the pairwise module), `features`, `train`, `evaluate`. **Release and tool:** `release`, `sources` (which data the tool shows), `players` (player-seasons), `band`, `explain`, `combinations` (measured layer), `learned` (learned module), `support` (out-of-support reasons), `coherence`, `properties`. **Upstream builders:** `schedule`, `states`, `normalizers`, `additive`, `legacy` (readers for old artifacts). **Data:** `bref_pages` (Basketball Reference page parsers), `ingest` (the database updater that downloads the pages; not in the public repository), `page_possessions` (the possession table rebuilt from the pages), `pbp_ids` and `names` (exact player ids for the play-by-play text), `player_counts`, `data_version`, `db`, `paths` |
| `scripts/` | One-off runs and generators |
| `tests/` | Unit and parity tests, plus small golden fixtures |
| `experiments/cache/` | Local data, features and checkpoints. Untracked; this path is historical. |
| `tool/` | Lineup Lab: the page, its browser port of the model, the model details page, the build and parity harness ([tool/README.md](tool/README.md)); `five.html` is the older additive page (not in the public repository) |

**Data.** Possessions come from Basketball Reference play-by-play in the local
PostgreSQL. `nba_pages.possessions` (2026-10-15) is the table rebuilt from the
pages where they were re-downloaded; `lineups.pbp_ids` aligns every stored event
with its page, which identifies its players by id. `nba.possessions` is the
original scrape and stays as it is. Rebuilds of the
legacy data chain run in their own roots (`scripts/rebuild_legacy_chain.sh`);
`LINEUPS_CACHE` points the package at one.

The exact code behind every v2–v20 result is at git tag
`pre-refactor-2026-10-09`. `scripts/legacy_worktree.sh` makes that code
runnable beside this tree. See [docs/REFACTOR.md](docs/REFACTOR.md).

Run code and tests from the repository root with the project interpreter:

```bash
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
$PY -m unittest discover -s tests -t .        # about 90 s; parity tests need local caches
$PY -u -m lineups.evaluate --arm J_POINT_BOTH  # re-score the reference from saved predictions
```
