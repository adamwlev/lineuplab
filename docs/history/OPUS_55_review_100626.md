> **Advisory review — Opus 5.5, 2026-10-06.** Written at Adam's request after a
> read-only review of the repository. This is not current guidance and does not
> authorize any training, data refresh, scorer promotion or change to the running
> v20 campaign. Current state, scores and the backlog remain in
> [JOINT_CAPABILITY_STATE.md](JOINT_CAPABILITY_STATE.md),
> [MODEL_SCORECARD.md](../../MODEL_SCORECARD.md) and
> [MODEL_RESEARCH_ROADMAP.md](../../MODEL_RESEARCH_ROADMAP.md).

# Direction review: critique and fresh ideas

## Scope

I read the following:

- **Guidance and status:** CLAUDE/AGENTS, the current handoff, the product
  contract, the state, the scorecard, NEURAL_MODEL and the roadmap.
- **v20:** the plan and the implementation report.
- **Reviews and diagnoses:** the v16 and v19 reviews, the v16 matchup follow-up
  and the v2–v10 learnings notebook.
- **Planning and feedback:** the 2026-09-27 literature notes, the 2026-09-17
  stocktake, the 2026-09-23 launch roadmap, the earlier external feedback files
  and RESEARCH_OVERVIEW §31.
- **Model code:** v9, v13, v14, v15, v16 and v17.

I ran two read-only pandas checks against existing caches. V20 was running
throughout (13/864 native cases at the time of writing). Nothing here touched it.

## Where things stand

The engineering and evidence discipline is unusually strong. That covers
forward-in-time evaluation, equally informed controls, exact nesting at
initialization, registered contrasts, receipts and independent audits. Three
results are real:

- usage/renewal accounting
- adjusted (deconvolved) profiles, worth about 0.12 RMSE in v16
  (J_POINT_RAW 11.181 → J_POINT_BOTH 11.061, direct)
- a neural model that beats additive_defense in 11 of 11 seasons

Two of the three co-equal pillars have not moved since v16, though:

- **Coherence.** Every evaluated model still favors five legal centers over the
  Jokić/Murray/Gordon/Porter/Westbrook unit. The reference's margin is
  +4.7 pts/100.
- **Latent-OOD uncertainty.** Uncertainty for arbitrary lineups is still
  unvalidated.

## Critique, most important first

### 1. Effort goes to the pillar the benchmark cannot resolve

v17 (25 h), v18 (41 h), v19 (49 h) and v20 (about 63 h projected) each
registered incremental point contrasts. None after v16 cleared its correction.
Two things explain this:

- **Effects at the noise floor.** Arms differ by 1e-4 to 1e-3 in r². Game-split
  reliability of the raw target is only about .21–.24, against r² of .163. In
  v9, an objective gain of −6.6e-4 at 12/12 seasons became
  −0.0008 ± 0.025 MAE.
- **Little room under the corrections.** With 11 season blocks, the exact
  sign-swap test cannot go below p ≈ .001. After Holm across 17 contrasts, an
  effect essentially has to win every season to pass.

The structural reason matters more than the statistics. The arms are nested,
identity-free and regularized, so on real lineups their predictions are nearly
identical. They differ mostly off-support, where there are no outcomes.
In-distribution r² cannot choose between them on the things that matter most.
V20 is a reasonable test of H_profile, since adjusted profiles were the largest
real gain so far. But about 85% of its design is again in-support prediction
contrasts.

### 2. The retained model's defense has no matchup structure

J_POINT_BOTH uses D_MAIN_RB, not CROSS. See `DefenseAdapter.effects` in
`experiments/joint_capability_v15_model.py` and `defense_effects` in
`experiments/v16_fast_model.py`. The defensive effect is a function of the five
defenders' mean and SD, broadcast identically to all five attackers. The
adjusted-defense head in `joint_capability_v16_model.py` does the same. Rim
protection therefore lowers Jokić's and Porter's make logits by the same amount,
and weak perimeter defense helps a non-shooter exactly as much as a shooter.
CROSS was dropped because its event gain did not show up in points, which is the
blind spot described in point 1.

This matters because the v16 matchup diagnosis shows defense is the largest
lever in the coherence failure. Switching the defensive paths off swings the
center margin by 11.5 pts/100.

Two parts of the defensive representation do not fit basketball:

- **Mean pooling has the wrong shape for both defensive resources.** Rim
  protection has diminishing returns, because there is one rim. Perimeter
  coverage fails at a threshold, because every attacker needs a defender.
- **Raw on-floor descriptors don't compose.** They are lineup-level rates, so
  averaging five of them describes the average lineup that contained a center,
  not a lineup of five centers.

### 3. The best structural ideas never reached the neural model

- **The assignment cost.** RESEARCH_OVERVIEW §31 (2026-09-03) is a defensive
  assignment cost. All 4 of its signs came out as pre-registered, its magnitude
  was 9× its placebo, and it extrapolates the right way by construction. Its
  write-up ended: *"put the constraint in the model rather than in a multiplier
  afterwards."*
- **The 2026-09-04 feedback.** MODEL_FEEDBACK_FROM_CLAUDE.md §4 proposed:
  - the rim as a finite resource
  - spacing as a count, not a mean
  - defense as two resources with opposite curvature
  - a threshold for having a ball initiator

Of these, only creation flow (v17) was built in the neural line. Every
structural success in this project has been a conservation law: one ball,
renewal accounting, creation flow. Defense never got one.

### 4. "No forced rankings" has drifted into "no asserted structure"

Contract §2C says out-of-support means need named structural assumptions. Usage
conservation and renewal are already asserted structure. The
selection-on-the-outcome finding explains why in-range fits get extrapolation
signs backwards: coaches field unusual fives only when they work.

I recommend writing the line into the contract explicitly:

- **Allowed:** generic conservation and shape laws that have a pre-registered
  sign, are defined for every lineup, and are tested on in-range analogues.
- **Not allowed:** penalties, caps or multipliers named after fixtures.

### 5. Evaluation cohort and era

**Cohort selection.** The ≥50-possession broad cohort covers about 37% of
possessions (1,013,999 of about 2.76M), and coaches choose which lineups reach
it. A quick read-only check over 2016–2026 compared each offensive
lineup-quarter's first 25 possessions with its later ones. Quarters were
approximated as within-season date quartiles.

| Cell size | First 25 possessions, pts/100 | Later possessions, pts/100 | Difference |
| --- | ---: | ---: | ---: |
| 25–49 | 115.02 | 110.18 | +4.84 |
| 50–99 | 115.12 | 112.73 | +2.38 |
| 100+ | 114.58 | 113.79 | +0.79 |

For cells with ≥50 possessions, the gap is positive in 10 of 11 seasons. The
pattern, largest in the smallest cells, is what optional stopping would produce:
coaches keep lineups that start hot and pull lineups that go cold. Fatigue, game
state and opponent mix confound it, though, so it is a lead that needs a
residual-based test, not a result. If it holds, three things follow:

- The two-big analogue bias (+3.0 pts/100) understates the real penalty.
- The finite-game noise model's exchangeability assumption is violated.
- Models that implicitly track deployment are rewarded.

**Era.** The 2016–2026 primary window is the era with the least support for the
hardest counterfactuals. The table below counts possessions whose offensive five
had at least three players listed at 82 inches or taller. Heights come from
`player_bio.csv`; about 0.5% are missing.

| Seasons | Share of possessions |
| --- | --- |
| 2002–2004 | about 6.2% (roughly 14k possessions per season) |
| 2005–2011 | 2.6–4.7% |
| 2017–2025 | 0.03–1.4% (0.21% in 2017, 0.03% in 2020, 0.08% in 2021) |
| 2026 | 2.3% |

That is roughly ten times more support in the earlier era. The five-year neural
training window and the primary evaluation never use it.

### 6. The additive half brings the worst extrapolator into the product

additive_defense favors the legal centers by +6.3 pts/100 and is linear in copies
of a player. The P2 "reliability-dependent blend" item is also a coherence
question, not only a predictive one.

### 7. Cost and hygiene

- **Scale.** There are 609 modules in `experiments/` (about 100 for v20), 1,126
  cache entries and 309 GB of cache. Each campaign takes days of rehearsal and
  audit to produce a near-tie. The rigor is right, but the cost per decision is
  high.
- **Docs.** Current documents systematically lose spaces around numbers
  ("63.21hcentral", "on2026-10-06"), which hurts readability.
- **Credentials.** `experiments/data.py` contains a committed database password.
- **Launch timing.** The 2026-09-23 launch roadmap aimed to ship the neural tool
  before opening night (about Oct 20). The export/JavaScript port has not
  started. If that goal still stands, it is at risk.

---

## Fresh ideas, ranked by expected value for the unsolved pillars

### A. Defensive coverage as optimal transport: defense's conservation law

Each attacker gets a threat vector built from offensive profile coordinates and
height. Each defender gets a coverage vector built from the adjusted defensive
bank plus height and position. A cost matrix C_ij has a fixed physical anchor
(the §31 position/height mismatch) plus a small learned term. The soft
assignment P = Sinkhorn(−C/ε) is doubly stochastic. The model's terms are:

- **On-ball effect on attacker i:** Σ_j P_ij · g(defender j, attacker i).
- **Help/rim term:** a smooth maximum over defenders' rim protection, so it is
  counted once, scaled by how many non-shooters the offense has. Help defenders
  can leave non-shooters.
- **Nesting:** as ε → ∞, P becomes uniform and the model reduces to today's mean
  pooling. It can therefore be initialized exactly at J_POINT_BOTH, consistent
  with the project's established nesting practice.
- **Training data:** fit on the existing 718,526 game × off5 × def5 aggregates.

Assignments do not need to be identified, because the conservation constraint
and the anchor carry the extrapolation. The expected effect: when five centers
guard a five-out offense, about four bigs end up on wings. Those attackers' 3PA
rate and conversion then rise, and rim deterrence is not counted five times.

### B. Offensive spatial capacity

- **A finite rim.** A team rim/paint budget whose size and conversion fall with
  a soft count of non-shooters.
- **An initiator threshold.** Turnovers and self-created conversion follow a
  monotone function of the lineup's best handler.

Both work through the existing ledger, not as output multipliers. They use
non-saturating monotone heads with declared signs and are coupled to A's help
term. This also replaces the tanh-bounded heads, which may extrapolate flat (see
F.1).

### C. Make coherence partly measurable

- **Big-lineup era backtest.** Run a bounded backtest with origins in 2005–2012,
  when 3-big lineups were about ten times more common and less of an exception.
  They were therefore also less selected on outcome.
- **Leave-structure-out.** Train without fives that meet outcome-free
  definitions (≥3 non-spacers, or no handler), then score those fives.

This turns "does the model penalize crowding?" into forward prediction with real
outcomes. It can then choose between A/B and flat extrapolation, and it tests
the cross-era transport the product requires.

### D. Structural uncertainty from disagreement between named hypotheses

Fit three or four models that agree in range but encode different extrapolation
assumptions: the current neural model, A + B, and additive. Report their spread
as structural uncertainty alongside U0/U1, and scale it using the errors
measured in C.

This is distance-aware by construction without a fitted distance schedule. Such
a schedule could not be fitted on this corpus (`distance_shrink.py`). The
approach is also faithful to contract §2C. An optional Laplace or Gaussian-process
last layer over the structural aggregates would add parameter uncertainty within
one model family.

### E. Settle the cohort question

Using saved forecasts, compare early-versus-late residuals by cell size. If the
effect is confirmed, add an all-possession proper score with no cell threshold
as a co-primary metric (a log score over points, or the event ledgers). Re-read
the analogue cohorts using only each lineup's first k possessions.

### F. Cheap diagnostics on saved weights (hours, no training)

1. **Saturation.** Measure tanh saturation in the teammate-message, defense and
   adjusted heads for fixtures versus real lineups. This shows whether
   extrapolation is flat.
2. **Per-attacker ledger.** Run the per-attacker ledger for the Jokić lineup's
   shooters against the centers, to confirm the uniform-shift diagnosis.
3. **Metamorphic property suite.** Run thousands of perturbations, each with a
   required direction:
   - swap a shooter for a non-shooter with equal usage → the others' rim
     conversion must not rise
   - add a third rim protector → the marginal rim effect must shrink
   - remove the best handler → turnovers must not fall

   Use pass rates as a scalable coherence scoreboard instead of 32 hand-picked
   fixtures. No rankings are forced.

### G. Pre-register a genuinely prospective 2026–27 test now

This is time-sensitive, because tipoff is about Oct 20. Freeze these models with
player states as of 2026-06-13:

- J_POINT_BOTH checkpoint-average-half
- additive_defense
- plain RAPM

Also freeze cohort rules that use preseason information only, including
offseason-changed rosters as natural transport tests. Scoring later needs an
authorized data refresh, but the freeze has to happen before games start. This
is the only genuinely fresh evidence available.

### H. Lower priority

- **Possession-entry coupling.** Live-ball turnovers lead to transition, and
  crashing the offensive glass trades against transition defense. This bears
  directly on the five-center margin and extends literature idea B.
- **Dynamic player state.** A Kalman-style latent player state would allow
  player-state uncertainty to be propagated, especially for rookies and thin
  histories.

## Recommended sequencing

1. Let v20 finish untouched.
2. Run F (hours) and E before designing v21.
3. Build v21 around A + B, with C and D as the evaluation:
   - In-range r² is a pre-specified non-inferiority margin, not a superiority
     test.
   - Coherence-suite pass rates and leave-structure-out/era errors are primary
     for structure arms.
4. Do G this week regardless.

## Reproducing the two read-only checks

Both used `/Users/adam/miniconda3/envs/basketball25/bin/python -u` with
`experiments/cache/possessions_ba7aeb377198.pkl`. They wrote nothing.

- **Era counts** also used `experiments/cache/player_bio.csv`:
  1. Take each possession's offensive five.
  2. Map player IDs to `height_inches`.
  3. Count players ≥ 82 in.
  4. Take the share of possessions with ≥ 3 such players, by season. Season =
     calendar year + 1 if the month is August or later.
- **Early versus later possessions:**
  1. Use regular-season months (Oct–Apr) of the 2016–2026 seasons.
  2. Split each season into four quarters by within-season game-date rank.
  3. Define a cell as a season quarter × sorted offensive five, with
     possessions ordered by date and game.
  4. Compare points per 100 for ordinal < 25 versus ≥ 25, by final cell size.
