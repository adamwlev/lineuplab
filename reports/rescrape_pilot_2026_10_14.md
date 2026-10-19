# Re-scrape of the play-by-play pages: pilot findings and plan — 2026-10-14 (night)

Adam (2026-10-14): "Please continue sorting out this data issue. It's
fundamental. I give you permission to re-scrape anything that you need to."

This follows the [name-matching fix](name_matching_fix_2026_10_14.md) and its
[rebuild](name_matching_rebuild_progress_2026_10_14.md). That fix repairs
accents, mis-decoded names and printed aliases. Some errors are beyond what
the stored text can fix, so the pages are being downloaded again. The
Basketball Reference pages link every printed name to the player's id.

## What was downloaded

- `scripts/rescrape_pages.py` downloads the play-by-play and box-score pages
  of every game in `nba.games` into the existing page cache. It uses
  `lineups.ingest.CachedClient`: under 20 requests a minute, atomic files,
  never fetched twice. Nothing is written to the database.
- **Pilot:** 20 games a season, both pages, 500 games (926 pages, 52
  minutes, no failures).
- **Running:** every game's play-by-play (29,234 pages, about 26 hours,
  started 19:13), then every box score (about 26 hours more). The 1,551
  games with a same-name collision come first, in about 80 minutes.

## Exploratory audit (`scripts/rescrape_pilot.py`)

The audit covers the 500 pilot games, 10,331 player-games, and compares
them with the official box scores.

### 1. The stored text still matches the pages

- 99.8% of stored lines are identical to a page row after folding accents
  and mis-decoded characters.
- The rest are page edits made after the original scrape (a changed
  distance, for example). They are paired by similarity.
- Only 2 lines of about 220,000 could not be aligned.
- Every linked player is in `nba.players`.
- The alignment is `lineups/pbp_ids.py`, 0.1 s a game.

### 2. Same-name collisions are real, and only ids resolve them

In 70,228 possessions (1.16%, 1,551 games), two of the ten players on the
floor print the same name. The worst seasons are 2013–15 (the Morris twins)
and 2023–24. On one five it is 0.27%. Box scores, 2024–25:

| Player | Prints as | Play-by-play FGA / box-score FGA |
| --- | --- | ---: |
| Jaylin Williams (OKC) | j. williams | 1.254 |
| Jalen Williams (OKC) | j. williams | 0.942 |
| Jeff Green (HOU) | j. green | 0.669 |
| Jalen Green (HOU) | j. green | 1.005 |

The text gives each such event to whichever player comes first in the
recorded lineup.

**Exact ids.** `lineups/names.py` replaces each linked name with a token
unique to its player. A shared canonical name gets the player's Basketball
Reference id: "j. williams-willija06". The legacy readers then match
exactly. Results on the pilot, against the box scores:

| Matching | FGA ratio, all | FTA | Steals | Player-games off by 2+ FGA |
| --- | ---: | ---: | ---: | ---: |
| Legacy names | 0.9886 | 0.9681 | 0.9945 | 87 |
| Name fix (2026-10-14) | 0.9910 | 0.9713 | 0.9980 | 61 |
| Exact ids | 0.9911 | 0.9714 | 0.9982 | 52 |

- In the 2025–26 sample, player-games off by 2 or more go from 6 to 3 to
  0.
- The remaining shortfall is the same under all three methods. It comes
  from events not recorded in the stored text (see §4).
- FTA stays at 0.97 because technical free throws are dropped by design.

### 3. One player stored under two ids

- Taylor Hendricks is `hendrita01` (id 2292) in 2023–24 and `hendrta01`
  (id 2436) from 2025–26. Basketball Reference renamed his id between the
  two scrapes.
- The model therefore sees his 2025–26 season without his history.
- The audit detects such splits from data: a linked player is absent from
  the stored ten while a stored player there prints the same name and is
  linked on no page (`pbp_ids.merges`).
- The id rebuild maps 2292 to 2436 in every player column.
- Of the 18 names with two rows in `nba.players`, the other 17 are
  different people (fathers and sons, two Mike Jameses).

### 4. The stored possessions have gaps; this fix does not touch them

These come from the original scraper (`scrape_br.ipynb`). The current
ingest (`lineups.ingest`, used since November 2024) has none of them.

- **Quarter-start clock.** The first possession of each quarter after the
  first starts at the previous quarter's last clock.
  - 89,733 possessions (1.6% of the old seasons) end later than they start.
  - Their texts, lineups and points are right. Only their duration and
    time remaining are wrong.
  - The possession context uses both: a duration filter, and the seconds
    left in the score state.
- **Lost possessions.** The old seasons miss 0.89% of official points,
  against 0.31% since November 2024. The 0.31% is technical free throws,
  unassigned by design.
  - The difference is concentrated in a few games. In 335 games (1.1%) the
    old scraper stopped early, more than 20 points short. It skipped the
    rest of a game, or a quarter, when it could not follow a substitution.
  - 17 games have no possessions at all.
- **Lineups themselves are right.** Where both cover a second, the stored
  ten and the ten re-derived from the pages by the current parser agree
  99.9% of the time. The exception is Hendricks's id.
- **Re-deriving from the pages recovers the gaps** (pilot):

  | Measure | Stored | Parsed from pages |
  | --- | ---: | ---: |
  | Official points short | 0.60% | 0.48% |
  | Games off by more than 5 points | 9 | 1 |
  | On-floor minutes vs box score, mean absolute gap | 0.75 min | 0.29 min |

  4 of 500 old pages fail the current parser and would need parser work.

## Plan

1. **Exact ids everywhere.** This is decided and needs only the downloads.
   - When every play-by-play page is in, build the anchors for all games
     (`python -m lineups.pbp_ids`).
   - Then rebuild through the legacy runner in `--ids` mode
     (`scripts/legacy_names.py`): shots, channels, v14 extract, v3, v14 and
     v15, v16 inputs, the library, the stores, the player seasons and the
     release.
   - The per-player counts: `python -m lineups.player_counts --ids`.
   - This supersedes the name-fix-only rebuild now running. That run can
     still serve as an interim model.
   - Checks:
     - fix-off parity, as before;
     - with ids, changes confined to collision possessions, alias and
       folding cases, and the Hendricks merge;
     - box scores for every season once the box pages are in.
2. **Decision for Adam: rebuild the possession table from the pages?**
   - This would fix the quarter-start clocks, the 335 truncated games and
     the 17 missing games.
   - It changes possession ids, so everything is rebuilt from the
     possession table up, including the possession context and the as-of
     point inputs.
   - It needs a new database table, so it needs Adam's approval.
   - If wanted, it is cheapest done together with step 1, since both
     rebuild everything downstream.

## Addendum, 2026-10-14 (late): the test rebuild in id mode, and the possession builder

Adam: "yes continue with the rebuild. clean data is primary … you can write
to the database." So the possession table is rebuilt from the pages as well
(`lineups/page_possessions.py`, into `nba_pages.possessions`).

**The test rebuild with exact ids.** The root is
`experiments/cache/names_fix_2026_10_14/ids_partial2`. It ran on the old
table, with pages for 4,357 games (every collision game). Games without pages
fall back to the name fix. It used `scripts/rebuild_legacy_chain.sh` and
finished in 33 minutes. Against the name-fix rebuild (`scripts/compare_rebuilds.py`):

| Artifact | What changed |
| --- | --- |
| shots | 4,149 of 6.8 M shots change shooter (0.06%) |
| channels | a few hundred to 1,400 counts per channel; about 1,900 possessions carry Hendricks's merged id |
| v3 per-slot labels | 1,797 of 897,778 rows change FGA; unmatched FGA 46,777 → 46,533 |
| v14 rebound labels | 5,718 rows (5,402 in collision games) gain 9,790 rebounds |
| player states | the merge removes 3 player-origin rows; league rates move slightly, so most states change in the last digits |

The rebound labeler refuses a name that two players on the floor share. It
was therefore dropping rebounds in collision games, which exact ids recover.

**Two pipeline fixes found by the test:**
- The possession context must be rebuilt in each root. The v14 extract checks
  the database rows against it, and the Hendricks merge changes player ids.
  The chain now has a `context` step. Rebuilt with the fix off, the context
  equals the original exactly.
- The legacy runner reads another table with `--table`.

**Possession builder dry run** (`python -m lineups.page_possessions --check`):

| Games checked | Parse and match official score | With page repairs | Fall back |
| ---: | ---: | ---: | ---: |
| 3,524 | 3,524 | 6 | 0 |

- "Match official score" is exact once technical free throws are added.
- The 2,492 games ingested since November 2024 reproduce their stored
  possessions exactly.
- The 626 old-scraper games recover 287 points the old table lost.
- The two page repairs (a missing possession-change row, a repeated
  substitution) are labeled per game and off by default in the ingest.

## Addendum, 2026-10-15 02:20: the targeted rebuild of the possession table

Adam: "switch to targeted for now. Make the most consequential fixes … into
the tool end to end (with any retraining) by Saturday."

**Targeted pages.** 3,393 old-scraper games, downloaded in 3.3 hours with
no failures:
- 2,068 more than 3 points short of the official score;
- 17 empty;
- 1,308 same-name collision games.

Together with the pages already cached, 6,340 games have both pages.

**`nba_pages.possessions`** (`lineups.page_possessions --write`):

| | Games | Possessions | Points short of official |
| --- | ---: | ---: | ---: |
| From pages | 6,285 | — | technical free throws only, every game exact |
| Kept from `nba.possessions` (clock repaired, Hendricks merged) | 25,905 | — | — |
| of which pages failed to parse | 55 | — | — |
| Whole table | 32,190 | 6,073,442 (+14,062) | 0.57% (old table 0.88%) |

- Of the 2,068 short games, 2,018 now come from pages. The other 50 are
  among the parse failures and keep their old rows, 2,548 points short in
  total.
- 14 of the 17 empty games now have possessions.
- 39 games needed a labeled page repair.

The 55 parse failures are left for later parser work:
- a scorer absent at his scoring event: 29;
- a substitution removing a player who is not on the floor: 9;
- a substitution leaving the wrong number of players: 6;
- a period's starters not inferable: 5;
- the score check: 4;
- players missing from `nba.players`: 2.

**Exact ids** for the new table: no merges were needed (pages already carry
Hendricks's page id; stored rows were merged). Per-player counts match
98.771% of 40 million events, against 98.756% on the old table.

The chain (id mode, library in parallel blocks) started at 02:13 into
`paths.CLEAN`.

## Addendum, 2026-10-15 (morning): the capability library in parallel blocks, and the rented box

**Blocks.** The legacy library fits each monthly snapshot warm-started from
the previous one, one process per bank and family. The two location chains
alone took 15–17 hours. Each snapshot is a fit to the data before its cutoff
with that season's penalty. The tuning and the last-seen history depend only
on the data, so the warm start only moves the optimizer's starting point.
`scripts/library_blocks.py` cuts each chain into contiguous blocks:
- cuts fall at season boundaries, or anywhere before the first tuned season;
- each block starts cold;
- the ordinary chain command then verifies every snapshot and writes the
  chain's receipt.

A cold-started snapshot against the sequential one, on the name-fix rebuild's
inputs:

| Snapshot | Coefficients, max abs difference | Standard errors | Ids and history |
| --- | ---: | ---: | --- |
| offense counts, 2011-10-01 | 1.6e-10 | 1.9e-12 | equal |
| defense location, 2009-09-01 | 7.7e-11 | 1.5e-12 | equal |

The era and 2027q1 extensions, run inside a rebuild root on the original
inputs, reproduced 349 saved snapshots bit for bit.

**On this laptop the blocks thrashed.** 20 processes held 3 GB resident with
23 GB of swap in use, and other workloads ran on the machine too. In 5¾ hours
they finished location 18 of 508 snapshots, counts 149, conversion 58 and
recovery 461.
- Adam asked to stop (08:25) and rented a box: 16 vCPU, 61 GB, Ubuntu 26.04.
- The bundle (`scripts/box_bundle.sh`) carries the prepared library with
  every finished snapshot, the schedule, and the 21 legacy modules the
  library imports.
- The two modules that open database connections are stubbed, and the
  bundle is checked for credentials before packing.
- Checksums matched after the upload.

**Rebalanced after measuring.** After 28 minutes on the box:
- location had finished 13 snapshots on 12 processes;
- counts 26 on 2 processes;
- conversion 17 on 2 processes, about 3 minutes a snapshot (4× the laptop);
- single-process conversion chains would have taken about 12 hours.

Counts and conversion were stopped and restarted as 2 and 4 blocks per chain
(at most the snapshots in progress were lost). The box's tail,
`box_run.sh finish`, waits for every block, verifies the chains and runs the
extensions. `scripts/box_return.sh` then copies everything back and finishes
the release here.

**Tool, built for the clean release** (Adam: "behind a player card if someone
wants to dig into the details … a model details page … the nitty gritty stuff
from the main page can be cleaned up"):
- a Details sheet per player (own, on teammates, when defending; readable
  units, standard errors, season percentiles; a parity test against the
  player-season table);
- `tool/model.html`.
