# Joint capability v6: can it price a lineup it has never seen?

Prepared by Claude Opus 5 with Adam, 2026-09-11. Successor to
`JOINT_CAPABILITY_V5_PLAN.md`. Read `reports/joint_capability_v5_review.md`,
`V5_PHASE0_FINDINGS.md` and `JOINT_CAPABILITY_LEARNINGS.md` first.

**Status: agreed implementation contract. No v6 experiment has been run.**

Boundaries unchanged: no scraper, no database access, no input-cache rebuild, no
scorer promotion, no page deployment. Never modify a completed run directory.
Use `/Users/adam/miniconda3/envs/basketball25/bin/python -u`.

## Context

Five versions have converged on one model and closed two routes.

- **v4 settled the architecture.** Mean pooling carries the whole teammate
  effect (novel RMSE −0.122, 11/11 seasons); pair pooling and the learned
  encoder are dead.
- **v5 closed the inputs.** Six interventions at a frozen architecture, all null
  or harmful; `V5_ALL` is the exact sum of its parts. λ = .01 is an interior
  optimum from two independent runs.
- **Phase 0 closed four structural defects**, each priced below 0.01 RMSE.

The point benchmark is saturated for this architecture: it resolves ~0.04 MAE,
the gap to the corrected additive is 0.03 and **not established**, and five
versions of work have moved it by less than that. Continuing to optimise it is
the wrong use of the next three hours.

Two of the three co-equal standards remain unmet, and both reduce to one
question. `E0M` produces the right *ordering* on degenerate lineups with no
position rule — five Gobert clones down, five Jokić clones up, five limited
creators down 10–12 points — which is the first fitted structure in this
repository that extrapolates the right way. But the *magnitudes* are **193–228%
of the largest context effect the model produces on any real lineup**, across
three consecutive versions, and they are quoted as results. Meanwhile the support
measure cannot separate five Gobert clones from a real five by more than 3%, so
no interval can widen where it should.

**v6 asks the one question that decides whether any of that is trustworthy: does
this model price a lineup it has never seen, or interpolate from similar ones?**

### Why this is worth testing rather than assumed

`selection_on_the_outcome.md` is the repository's strongest negative result:
lineups are selected on the outcome, so an unusual five is fielded only when it
works, "unusual" correlates with "good" in range, and every fitted structure
inherits that sign. It is why the tool's coverage gate is **asserted** rather
than fitted, and why `distance_shrink.py` could not fit a schedule.

**That argument was made against models carrying lineup-level, pair-level or
identity parameters.** `E0M` has none — no player IDs, no pair tables, no lineup
terms. It prices a five from five dated player states through fixed accounting,
and it cannot memorise a lineup even in principle. Whether the selection
objection binds *this* architecture has never been measured.

It can be measured, by construction, with real labels and no new data: withhold a
region of composition space from training and see whether the model still prices
it.

## The reproducibility contract

Every derived input a v6 arm trains on must satisfy four conditions, enforced by
`experiments/joint_capability_repro.py` rather than promised in prose:

1. **produced by committed code**, inside v6's own preflight — `untracked_code()`
   must return empty, because an untracked producer cannot be rebuilt from a
   checkout whatever its hash says;
2. **from pinned sources**, sha256-recorded in the run's `reproduce.json`;
3. **with no database path reachable** — preflight runs inside `no_database()`,
   which blocks `psycopg2.connect`, the single choke point both
   `experiments.data._conn` and `experiments.shot_quality._connection` go
   through. A cached loader that falls through to its rebuild path then raises
   instead of silently regenerating;
4. **written under v6's own prefix** — never read from a stray artifact of an
   earlier session. `*.pkl` and `*.npz` are gitignored here, so such an artifact
   is invisible to git and to a reader.

This is not hypothetical. **`shot_quality.build()` returns its cache when the
file is present and connects to Postgres when it is not**, and
`shot_quality_forward_coefficients.pkl` — which `V6_SHOT` needs — is gitignored
and was written on 2026-09-08. A run that happens to find that warm file is
indistinguishable from one that rebuilt it from the database, until someone tries
it on a fresh checkout. So **`V6_SHOT` regenerates its coefficients into v6's own
prefix**, under the guard, rather than reading that file.

Verified 2026-09-11 on the v5 inputs, which v6 inherits: both side-cars rebuild
**bit-identically** (all 16 arrays) from committed code in 11.3 s with Postgres
blocked, and `shot_quality.build()` serves 6,846,563 attempts from cache in 0.4 s
under the same guard. Recorded in
`experiments/cache/joint_capability_2026_09_10_v5/reproduce.json`. Four tests
enforce it, including one asserting the guard itself raises.

Phase 0 and preflight both run inside `no_database()`, and the run is not
considered started until `reproduce.json` is written.

## Phase 0 — no fits

**P0.1 — a support measure with range.** The current one is
`sqrt(mean(((v − μ)/σ)²))` over the 36-dim composition vector `[mean over the
five of base, sd over the five of base]` (`joint_capability_v3_run.py:514`). An
RMS over 36 coordinates averages extremes away, which is exactly why five
Goberts scores 3.191 against a real maximum of 3.105. Rebuild as **Mahalanobis**
with the prefix covariance (36 dims from ~900k rows is well conditioned; shrink
the covariance lightly and report the condition number, per
`feedback_rank_deficient_control.md`). Acceptance: the measure must place clone
lineups well beyond the real maximum, as the older profile scale did — real fives
4–11.5, five Shaqs 20.9, roughly 1.8×. Note that five identical players have
**exactly zero** sd on all 18 coordinates, a direction real fives never occupy,
which Mahalanobis sees and an RMS of z-scores does not.

**P0.2 — the clone ladder, on v5's saved checkpoints.** Take real lineups and
replace 1, 2, 3, 4, 5 slots with copies of one player, scoring each rung through
the model's own scorer. The additive's duplication curve is *exactly linear*
(`tool_breaks_on_repetition.md`). Does `E0M` bend, at which rung, and is the bend
consistent with what it does to genuinely unusual *real* fives? A curve that
bends only past the real support is a free parameter; one that bends inside it
is a mechanism.

**P0.3 — define the strata.** From the new measure, compute composition distance
for all ~898k training rows, prefix-referenced per origin, and report how many
rows and possessions each holdout removes.

## Phase 1 — the sweep

Backbone frozen at v5 `BASE` (mean pooling, no encoder, λ = .01, γ = .01, seed
17, 24/3/1e-5, 730-day training weight, shared prefix budget). **The factor is
the training population**, not the model.

| arm | trains on | question |
|---|---|---|
| **V6_FULL** | everything (alias of v5 `BASE`) | control |
| **V6_HOLD75** | composition distance below the prefix p75 | can it price the top quartile it never saw? |
| **V6_RAND75** | a random 75%, matched in rows and possessions | the data-volume control for HOLD75 |
| **V6_HOLD50** | below the prefix p50 | dose–response |
| **V6_RAND50** | a random 50%, matched | its control |
| **V6_SHOT** | everything, plus the §10 shot-quality coefficient as a message input | the last input with a measured forward basis |

Five new arms (FULL is an alias) × 48 origins × 2 fits ≈ **2.8 hours**.

### The primary contrast, pre-registered

**(HOLD − RAND), evaluated in the withheld composition region.** The random arm
holds data volume fixed, so the difference is composition-specific extrapolation
cost and nothing else. Without it the experiment is uninterpretable, because
every holdout arm trains on less data and is worse everywhere.

Secondary, also pre-registered: the dose–response (does HOLD50 − RAND50 exceed
HOLD75 − RAND75, and roughly in proportion?); whether degradation is *ordered* by
the new distance, which is precisely what the interval work needs and what
`distance_shrink.py` looked for in range and did not find; and the same
contrasts for the corrected additive as a reference level in the high-distance
region, noting that it is trained on everything and so cannot join the holdout
comparison itself.

`V6_SHOT` is scored on the conversion channel first — FG Brier and the raw
conversion family — and on points second. It is a long shot after v5, and it is
worth one arm because it is the only remaining input that is a *measured,
forward-validated* teammate effect (Jokić +1.69 ± 0.36 pp, forward slope
1.082 ± 0.084, 12/12 seasons over 2.66M held-out attempts) rather than a
plausible feature. The estimator is strictly prior per origin — `shot_quality_forward.py` refits
the isotonic curve, the shooter baselines and the coefficients on `date < start`
alone — and it regenerates from the pinned `shot_events2` cache with no database
path. It is rebuilt into v6's prefix, **not** read from the gitignored
2026-09-08 artifact; see the contract above.

### Either outcome is decisive

- **HOLD ≈ RAND.** The model extrapolates from structure rather than
  interpolating from neighbours. The fixture magnitudes gain real standing, the
  selection objection does not bind an identity-free architecture, and the
  coverage gate could become **derived rather than asserted** — which is the
  northstar argument `ROLE_MODEL.md` made for the whole hierarchical programme.
- **HOLD ≫ RAND.** Unusual-lineup behaviour is interpolated from similar real
  fives, the fixture magnitudes are unsupported, we stop quoting them, and the
  asserted coverage gate stays. That is a real result and it retires a claim we
  have repeated for three versions.

### On the time holdout

v5 reserved 2026 and it was the right discipline at the wrong size: 428 cells,
r² collapsing to ~0.02, rankings scrambled, unable to adjudicate 0.03 MAE.
**v6 replaces it with a holdout that has power by construction** — the withheld
composition region is roughly a quarter of the training population and is
evaluated on the full cell set. Fit all 48 origins and report the whole decision
sample; the composition holdout is the confirmation slice.

## Phase 2 — diagnostics

The extrapolation degradation curve by distance decile, for every arm. Interval
recalibration on the rebuilt measure — the pre-registered isotonic method from
v4, re-run now that the measure has range, against the matched constant-√n
control and scored by weighted interval score. The clone ladder re-measured on
the held-out arms: does a model that never saw the top quartile still bend the
same way? The standing guardrail columns — fixture swing as a percentage of the
in-range maximum, and event bias on both cohorts. Point-transfer ledger and the
failure review as in v4/v5.

## Phase 3 — learnings and checkpoint

Append a v6 section to `JOINT_CAPABILITY_LEARNINGS.md` under the same five
headings, update `MODEL_SCORECARD.md`, `BACKLOG.md` (do-not-re-run first),
`CLAUDE.md` and `SESSION_HANDOFF.md`, then commit.

## Verification

- `V6_FULL` must reproduce v5 `BASE` to the measured tolerance: median per-cell
  difference zero, pooled MAE gap below 1e-3.
- Holdout masks must be **prefix-only and refit per origin** (CLAUDE.md rule 9);
  a mask built from the full-sample distance distribution is a leak.
- `RAND` arms must match their `HOLD` partner in both row count and possessions,
  asserted, not assumed.
- Every arm: 48 origins, one-to-one join against the frozen benchmark cells.
- `reproduce.json` present, `untracked_code()` empty, and every derived input
  rebuilt under `no_database()`; a Postgres call during preflight is a failure,
  not a warning.
- Full suite against the 658-test starting point; new prefix
  `experiments/cache/joint_capability_2026_09_1x_v6`; v5 immutable.

## Not in scope

Any architecture change. Further input enrichment beyond `V6_SHOT` — v5 closed
that. Defence, the second side, ORB budget feedback. Chasing pooled point
accuracy: the primary contrasts here are extrapolation-cost contrasts, and they
are well powered precisely because extrapolation failure is a much larger effect
than the 0.03 MAE the benchmark cannot resolve.
