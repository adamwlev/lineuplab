# The name-matching fix through the whole pipeline: plan — 2026-10-14

Adam (2026-10-14): "ok continue the fix. go ahead with the rerun … Please be
thorough in the data fix, we've got to get that right since it's
fundamental."

Background: [the bug and the first fix](name_matching_fix_2026_10_14.md).
Every parser of the play-by-play text matches actors by "first initial. last
name". The counts are fixed, and the tool's player inputs are rebuilt from
them. Three more parsers feed the model, and everything downstream of them
must be rebuilt.

## Rules for every step

- **Nothing completed is modified.** Outputs go to new directories under
  `experiments/cache/names_fix_2026_10_14/`. The frozen prospective record,
  its fits and its store are never touched.
- **Fix off reproduces the original.** Each rebuilt artifact is first
  produced with the fix switched off and must equal the existing file
  exactly. That proves the runner and the inputs are the original ones. For
  the capability library, which took 17 hours, this is checked on sampled
  snapshots.
- **Fix on changes only what it should.** Every changed row is explained by
  a fixed name. Unexplained changes stop the campaign.
- **An outside check.** Per-player totals from the fixed parsers are
  compared with Basketball Reference box scores. These are the cached pages
  of the games ingested since November 2024, about 3,800 games covering
  2024–25 and 2025–26.
- **An audit of what remains.** Events still unmatched after the fix are
  classified as players missing from the recorded five or as name variants
  the alias rule missed.

## Stages

1. **The four parsers of the text.**
   - Per-player counts: done (`lineups/player_counts.py`).
   - Shot events (`shot_quality`), possession channels
     (`possession_channels`) and rebound labels (v14 labels): run in the
     legacy code through a runner that fixes names at the database boundary.
     It folds names and texts and rewrites the learned aliases where their
     player is on the floor.
2. **Derived data.** v3 per-slot labels (`game_lineups.npz`), offense and
   rebound states, v15 inputs, v16 training inputs, the full capability
   library (all snapshots, era and 2027q1 extensions), the three stores and
   their normalizers, and the player-season table.
3. **The release.** Retrain arms R and C (3 seeds each) on the fixed store,
   then the learned modules, the player qualities, the export and the
   parity tests.
   - Compare old and new forecasts on fixtures and on real lineups.
   - Republish the review copy.
4. **Decision for Adam: how much history to rerun.**
   - The release calibration, the scorecard benchmark, the combination
     layer and the learned-module confirmation all rest on 2015–2026
     reference fits trained on the old data.
   - Rerunning them is about 130 fits plus the screens.
   - Stage 3's measured shift tells whether that matters.

## Time

- Stage 1: about 1–2 hours.
- Stage 2: the library dominates. The original full build took 17 hours with
  three chains at a time; with all eight chains in parallel, expect 6–8
  hours.
- Stage 3: about 1–2 hours.
