# Player names in the play-by-play: the bug and the fix — 2026-10-14

Found while ranking Bridges replacements in the Knicks lineup: Bub
Carrington, Hugo González and Vít Krejčí topped the "combination effect"
ranking because the model saw them as players who never shoot.

## The bug

The play-by-play text names each event's actor ("v. krejčí makes 3-pt jump
shot"). Every parser of that text assigns the event to one of the ten
players on the floor by comparing the name with "first initial. last name",
built from nba.players and lowercased. When the text prints the player
differently, the event is dropped. It is still in the team totals but not
in the player's own counts. The mismatches:

| Kind | Examples |
| --- | --- |
| Accents | Krejčí, Şengün, Quiñones |
| UTF-8 mis-decoded in nba.players | Micić ("MiciÄ"), Petrušev |
| UTF-8 mis-decoded, then lowercased, in some games' text | Jokić, Bogdanović, Valančiūnas, Nurkić |
| Other names in the text | "b. carrington", "h. gonzález peña", "d. ilunga-mbenga", "a. vezenkov", "j. navarro", "j. mcadoo", "v. faverani", "l. datome", "n. williams" (Jeenathan), "n. hayes-davis", "m. louzada silva" |
| A single name | Nenê ("n. hilario") |

**Size of the loss.** Of 40.0 million parsed events, the legacy matcher
placed 98.46%. The fix places 98.76%, recovering 119,387 events for 22
players:
- Nenê: 68,565 events (every season 2003–2019 read as a non-shooter);
- Carrington: 10,396;
- Şengün: 10,058 (2023–24 read at 3.6 FGA per 100 possessions, really 22.1);
- Krejčí, Navarro, Micić, Mbenga and others.

The other 1.24% are events by a player absent from the recorded five, often
around substitutions. That is a separate issue and is unchanged.

## Where the bug lives

Four legacy parsers match names this way:

| Artifact | What it feeds | Status |
| --- | --- | --- |
| `game_player_stats.pkl` | offensive states, roles, defensive descriptors | **fixed** (`lineups/player_counts.py`) |
| `rebound_labels.npz` (v14 labels) | offensive-rebound prior | not yet |
| `game_lineups.npz` (v3, per-slot `fga`, `loc_*`, `unmatched_*`) | the network's per-player training labels | not yet |
| `shot_events2` → v15 inputs → capability library | the adjusted offense and defense banks | not yet |

Rows with an affected player are 1.5% of all possessions, and 2.0% of the
2022–2026 window the release networks trained on.

## The fix (done)

- **`lineups/player_counts.py`** ports the counts builder.
  - With the fix off it reproduces the legacy file exactly: 668,380 rows,
    maximum difference 0.
  - With it on, names on both sides are folded: mis-decoded UTF-8 repaired
    (also after lowercasing), accents stripped.
  - The remaining unmatched names are learned as aliases from the data. An
    alias needs:
    - 20 or more events;
    - one player on the floor for at least 95% of them, and no other
      player for 85% or more;
    - that player almost without events under his own name in those games
      (at most 0.1 per alias event, counting events already credited
      through his larger aliases).

    The last condition rejects events by players missing from the recorded
    lineup ("d. ewing" would otherwise have gone to Elton Brand) and a
    stray "j. reese".
  - Twelve aliases were accepted; all were checked by hand.
  - Tests: `tests/test_player_counts.py`.
- **`lineups.states.origin_states`** now holds the store scripts' shared
  origin-state code.
  - Rebuilt from the legacy counts, it reproduces both stores' saved origin
    states exactly.
  - `scripts/rebuild_player_states.py` rebuilds the era and 2027q1 stores'
    origin states from the fixed counts. Every other file is linked from the
    originals: normalizers, environment, game tables, library.
  - Only the affected players move by more than 0.05: 3 of 1,231 players in
    the era store, 18 of 2,513 in the release store.
- **The tool's player-season table** is now
  `experiments/cache/player_seasons_2026_10_14`.
  - 55 player-seasons' FGA per 100 moved by more than 0.5. Examples:
    - Nenê 0.2 → 13–20;
    - Carrington 0.3 → 15.5;
    - Krejčí 0.6 → 14.1;
    - González 0.5 → 11.7;
    - Micić 0.4 → 16–17.
  - Display names are repaired (Micić, Petrušev).
- **`lineups.release.STORE`** is the rebuilt store. `FROZEN_STORE` keeps the
  original, and `tests/test_release.py` still reproduces the frozen 2027q1
  fixture table from it. The prospective scoring reads its own store
  (`scripts/prospective_fit.py`), so the frozen record is untouched.

## Effect on the Knicks search (Bridges swapped out, ≥ 500 possessions)

| Player | Combination effect, before → after | Forecast net, before → after |
| --- | --- | --- |
| Carrington | +1.62 → +0.65 | +7.2 → +3.6 |
| González | +1.48 → +0.65 | +8.9 → +6.0 |
| Krejčí | +1.45 → +0.59 | +8.1 → +6.6 |

The new top five are Vanderbilt +1.41, Murray-Boyles +1.37, Butler +1.25,
Bona +1.20, and Gill and Cody Williams at +1.12. The lowest five are
unchanged. For the other players, totals before and after correlate 0.98.

## Still to do

1. **Rebound labels:** offensive-rebound priors for the affected players are
   still undercounted.
2. **The capability library:** its adjusted banks for those players still
   lack their own shots. It is built by legacy chain code (about 50 minutes
   per 87 monthly snapshots in parallel).
3. **The per-slot training labels.**
4. **Retraining the release** on the fixed data: about 1 hour for the six
   fits, plus the module, the layer and calibration. This is separate from
   the frozen record, which stays as it is.

Items 1–3 need the shared resolver in the remaining parsers, ported or run
through the legacy worktree. With item 4 this is a multi-hour campaign that
waits for Adam's go-ahead. It fits naturally with the 2026–27 data refresh.
