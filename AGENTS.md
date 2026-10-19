# Working agreement

Adam owns the goals. From 2026-10-09, Claude (Opus 5.5, in Claude Code) owns
everything else: research design, implementation, verification,
interpretation, documentation and day-to-day decisions. Codex/Astra is
inactive and nothing is delegated to other agents. Claude is the only editing
agent.

Documents written under earlier lead/worker arrangements are historical
evidence, not instructions. The exact code and documents behind every result
from v2 to v20 are preserved at the git tag `pre-refactor-2026-10-09`.

## What we are building

A lineup tool. You pick two five-player lineups made of player-seasons. The
players can come from any season from 2002 onward, mixed across eras, and the
lineups need not have ever played together. Team B defaults to a
league-average opponent. Active players default to their latest data, and
historical players default to a representative season. The tool returns:

- offense, defense and margin, in points per 100 possessions;
- the basketball reasons: creation, spacing, rim pressure, turnovers, free
  throws, rebounding, defensive coverage, and who is pushed out of their usual
  role;
- an uncertainty band, with the reason it is wide in basketball language
  (thin player data, unusual role, unfamiliar composition, cross-era
  comparison, extrapolated matchup).

Three pillars have equal standing. No single metric is the north star.

1. **Prediction.** The model is accurate forward in time on future lineup
   outcomes, compared with equally informed controls.
2. **Weird lineups.** Unusual and impossible lineups get coherent answers. A
   user must not be able to enter five centers, or five copies of a star, and
   be told it is the best lineup ever. Swapping the two teams must negate the
   margin, and lineup order must not matter.
3. **Uncertainty.** Bands are honest on observed lineups. They widen, with a
   stated reason, as a lineup moves away from anything observed.

Research comes first for now. There is no fixed ship date. Something
publishable around opening night would be welcome but is not required.

## Decisions of record (Adam, 2026-10-09)

- **Accuracy trade-off.** A model may lose up to **0.003 r²** on the primary
  benchmark if it delivers a material, demonstrated gain on pillar 2 or 3. The
  trade must be printed, not hidden.
- **Data first, structure where data cannot reach.** Learn from data when it
  can meet the pillars. Far outside observed lineups it cannot: coaches field
  unusual lineups mainly when they work, so fits on observed lineups
  extrapolate optimistically. In that case use explicit basketball structure:
  - conservation and capacity laws: one ball, one rim, five defenders for five
    attackers, someone must bring the ball up;
  - shape constraints whose direction is declared before fitting.

  Name every such assumption and test it on the closest real analogues.
- **Not allowed:**
  - penalties, caps, multipliers or training labels aimed at a named player
    or lineup;
  - gates that suppress or override the model's number.
- **Weird-lineup checks** are a suite of directional properties, not forced
  rankings. Example: swapping a shooter for a non-shooter must not improve
  teammates' rim finishing.

  Adam's prior is that a lineup with no ball handler, such as five Goberts,
  should fail. Five Jokićs may not, because he handles the ball. The best
  outcome is a model that finds this from data and structure. An acceptable
  outcome is a very wide band with a clear explanation.
- **Uncertainty beyond observed lineups** cannot be validated directly.
  - Validate on held-out real unusual lineups.
  - Beyond that, show the disagreement among models built on different named
    assumptions, labeled as assumption-based.
  - Finite-game coverage and seed spread do not validate this.
- **Identity-free by default.** The main model represents players by their
  capabilities, not by player-ID embeddings or known-pair chemistry. Shared
  pair history may appear only as an optional, labeled layer, and only if all
  of these hold:
  - it improves forward accuracy over the full model;
  - it does not change the mechanism explanations;
  - it does not narrow uncertainty for unrelated or cross-era pairs.
- **Scope.** The 2002-onward corpus is enough for cross-era use. Refreshing
  data for 2026–27 and freezing prospective predictions are in scope.

## Decisions of record (Adam, 2026-10-12)

- **Close-out.** Accuracy research is closed. The work now follows
  [docs/CLOSEOUT.md](docs/CLOSEOUT.md), which runs from the release model to
  the tool.
- **Forecast.** The tool shows the calibrated neural model alone (reference
  architecture). The additive half is dropped, and its cost (−0.0015 raw,
  −0.0006 centered r²) is printed in the scorecard.
- **Capacity.** The capacity-law model is a labeled alternative assumption
  in the band, not the forecast.
- **Cross-era levels.** Player-seasons enter the release model era-relative by
  default: each player is placed relative to his own league. "As they played"
  (as-was) is a user setting.

## Decisions of record (Adam, 2026-10-13)

- **The tool is built around combination effects.** Adam: "The ability to
  extrapolate in a non linear manner is what I want to show off. So let's
  build it around these nonlinear adjustments, however small they are."
  - The printed forecast is the calibrated network plus the measured
    combination layer (`lineups/combinations.py`).
  - The network-alone number stays visible.
  - The layer's forward trade is printed in the scorecard.
  - Only effects that held up on held-out seasons enter the number.
    Suggestive or pre-registered ones (small guards × anchor) appear as
    labeled notes.

## Decisions of record (Adam, 2026-10-14)

- **The learned combination module enters the forecast at half strength.**
  Adam: "Half strength seems prudent … Ok sure let's try it out."
  - The module: a held pairwise module trained on top of the frozen network
    for 8 epochs. Its level is removed against the previous quarter's real
    lineups, and seeds are averaged
    ([confirmation](reports/learned_module_confirmation_results_2026_10_14.md)).
  - The printed forecast is the calibrated network, plus half the centered
    module, plus the measured combination layer. The layer is re-measured on
    top of the module, so nothing counts twice.
  - This amends the 2026-10-13 rule that only held-up effects enter the
    number. The module's learned structure enters at half strength, labeled
    as learned. The layer's 14 effects remain the measured, explained ones.
  - The network-alone number stays visible. The trade is printed in the
    scorecard.

## Decisions of record (Adam, 2026-10-14 and 2026-10-15)

- **Clean data is primary.** Adam: "It's fundamental. I give you permission
  to re-scrape anything that you need to … clean data is primary … you can
  write to the database."
  - Play-by-play events are attributed to players by Basketball Reference
    id, never by printed name (`lineups/pbp_ids.py`, `lineups/names.py`).
  - The possession table is rebuilt from the pages into
    `nba_pages.possessions` (`lineups/page_possessions.py`).
    `nba.possessions` stays as the original scrape.
  - The release is retrained on the rebuilt data. Its calibration is carried
    from the frozen record until history is rerun, and that carry-over is
    stated.
- **Targeted first** (2026-10-15): pages only for the games with problems
  (short, empty, same-name collisions), so the clean release reaches the
  tool by Saturday 2026-10-17. The remaining pages are a later step.
- **The tool's detail layer** (2026-10-15): each player's capability
  estimates sit behind a Details sheet, and the technical text moves to a
  model details page.

## Decisions of record (Adam, 2026-10-19)

- **Publish v1** on its own domain with low-maintenance, cheap hosting. Adam
  buys the domain and owns the hosting account.
- **Author:** "Adam Levin and Claude Code".
- **Open source the project.** The licence, account and repository are
  Adam's to choose; nothing is pushed without his go-ahead.
- **Deferred to v2:** actual results for real lineups.
- **Kept for v1:** the five Goberts colour, and the "relative" setting's
  cross-era translation.
- **On hold:** pages for the remaining 25,850 games.

## Authority

**Without asking:**

- read-only work, including read-only database queries;
- diagnostics on saved models;
- new code, tests and refactors, including removing tracked code and
  documents (git history keeps them);
- fits and runs of up to about six hours of wall time;
- documentation and memory;
- committing this work to `main`.

**Ask Adam first:**

- runs or campaigns expected to take more than about six hours;
- scraping, or any other data refresh;
- database writes or schema changes;
- deleting untracked data, caches or model checkpoints;
- promoting a scorer, publishing, or replacing the public tool;
- anything that costs money, such as renting compute;
- pushing to a remote.

Tell Adam promptly when:

- a result contradicts an earlier conclusion;
- a bug affects reported numbers;
- a run fails;
- a decision of record above looks wrong.

## Rules of evidence

1. **Evaluate forward in time.** Training-row features, normalizers, tuning,
   early stopping and calibration each respect their own cutoff. Inner
   validation is not the outer evaluation.
2. **Label every metric.** Name the target, population, information available
   and weighting beside it. Lineup-quarter r² is not possession-level r².
3. **Compare like with like.** Compare against equally informed controls on
   identical rows. Opponent-aware predictions need opponent-aware controls,
   and calibration is part of the comparison.
4. **Report uncertainty at the season or game level.** Seeds and overlapping
   folds are not new seasons.
5. **Fit everything upstream inside the split.** Check row keys, masks and
   temporal selection steps, not only the final fit.
6. **Audit penalty-grid boundaries, null directions and calibration levels.**
   A near-zero estimate can mean over-shrinkage or a broken control.
7. **Keep different kinds of result separate.** Point results, event results
   and mechanism results are distinct. Accounting decompositions and switched-off
   paths are not causal teammate effects.
8. **Judge all three pillars.** Inspect counterfactual offense and defense
   separately; a sensible margin does not excuse an implausible offense.
9. **Don't overclaim intervals.** Finite-game intervals and seed spread do not
   validate uncertainty about an arbitrary lineup's underlying quality.
10. **Keep failed and partial runs, labeled as such.** A pilot or a post-hoc
    sensitivity is not the registered result.
11. **Design for power.** Before an expensive run, name its one to three
    primary contrasts, the effect size that would matter, and whether the
    design can detect it. Label exploratory work as exploratory. Confirmatory
    runs freeze their protocol before seeing results and are not revised in
    response to them.
12. **Scale rigor to stakes.** Full registration and independent checks are
    for confirmatory results and for anything that changes what the tool
    prints. Exploratory diagnostics need correct arithmetic and honest labels,
    not ceremony.

## Operations

- **Python.** Run code from the repository root with
  `/Users/adam/miniconda3/envs/basketball25/bin/python -u`. The base
  interpreter cannot read some saved numpy caches.
- **Database.** The local Postgres is read through the shared connection
  helper. Credentials come from the environment or `~/.pgpass`, never from
  code, documentation or logs.
- **Code.** Code lives in the `lineups/` package. Extend shared code in place
  behind tests; do not add versioned copies of modules. Run the suite with
  `python -m unittest discover -s tests -t .`. The parity tests pin the
  reference model, its inputs and its scorecard.
- **Old code.** Pre-refactor code is at tag `pre-refactor-2026-10-09`. Run it
  through `scripts/legacy_worktree.sh`, which shares this tree's cache.
- **Local artifacts.** Data, features and checkpoints live in
  `experiments/cache/` (a historical path). They are local and untracked;
  never stage them. Completed run outputs are not modified; new work writes to
  a new output directory.
- **Long jobs.**
  - Run them detached, with unbuffered Python and an append-only log.
  - Don't hold a long job inside a single tool call.
  - Don't poll with a `pgrep -f` pattern that matches the poller itself.
  - Laptop sleep inflates wall-clock times, so compare CPU time before killing
    anything.
- **Compute.** Compute is CPU only. The networks are small enough that a GPU
  does not help. Renting a CPU box is possible with Adam's approval.

## Documentation

| File | Role |
| --- | --- |
| `README.md` | Purpose and navigation |
| `STATUS.md` | The one current state and handoff: what is done, what is running, the next step. Update it at the end of every working session. |
| `MODEL_SCORECARD.md` | Comparable metrics for retained models, with their populations |
| `MODEL_RESEARCH_ROADMAP.md` | The prioritized queue |
| `reports/` | Dated results. Never rewrite a report; add a dated correction instead. |
| `docs/history/` | Superseded plans, journals and reviews, kept for provenance |

Keep documents short and plain. State results with their population and
uncertainty. Replace stale guidance rather than appending to it.
