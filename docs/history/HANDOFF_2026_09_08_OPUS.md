# Opus session digest, 2026-09-08 — for Astra/Codex

*Written for another agent, not for Adam. The full record is
`TEAMMATE_INFLUENCE_EXPERIMENT.md` (~2,100 lines, §1–§18); this is the digest.
30 commits, `b04c055`..`d092f4a`. 606 tests pass. **No database write, no
scraper, no cache rebuild of an existing artifact, no scorer or page
promotion.** `MODEL_FEEDBACK_FROM_CLAUDE.md` untouched.*

---

## The question Adam asked

> "The current model is lacking a big element of basketball: how much players
> affect the team as a whole when on and off the floor — Jokić raising his
> teammates' shooting percentage, Shai reducing his team's turnovers."

Build it **inside** the structural model, not as a replacement.

---

## New documents

- **`STRUCTURAL_MODEL.md`** — did not exist. `CURRENT_MODEL.md` documents the
  *additive* page; the structural arm had no single-file spec. Five pipeline
  stages with source references, every arm's score with provenance, each
  mechanism in pts/100, what is deliberately absent, six weaknesses.
- **`TEAMMATE_INFLUENCE_EXPERIMENT.md`** — the full workstream record.

---

## What was established, with numbers

All point figures: 5,607 cells / 726,364 possessions, seasons 2016+, the
centered quarterly run. Parent = `structural|180|live|recent_live|raw|base`,
MAE 8.1440, RMSE 10.9214, r² 0.10733, novel 8.8903. Corrected additive 8.0920 /
10.8410 / 0.12043 / novel 8.9039.

### 1. The additive/structural gap IS on-floor influence — and they are redundant

Transplanting the influence layer closes 21–38% of the gap, placebo-clean. But
their forward errors correlate **0.9856** and neither arm's score explains the
other's error. The whole prize from optimal ensembling is **0.15% of RMSE**, and
a fixed 50/50 average nearly reaches it. **Do not look for more gains from
combination.**

### 2. Opponent adjustment — the one lever that paid outright

Strength of defences faced explains 14% of what either model explains and
neither uses it. Correcting the **target** at coefficient 1 (no fitting):
blend 8.0763 → **8.0417**, 9/11 seasons. A fitted κ scores worse than κ=1.

### 3. Shot quality is measurable, and it was never in the data pipeline

Raw shot distance was always in the play-by-play and had never been kept.
`shot_quality.py` keeps it: 6,846,563 attempts, distance on 100% of 5,372,539
field goals, shooter matched 98.9%. Isotonic FG% on distance, shooter **and**
game fixed effects. Jokić: teammates make **+1.69 ± 0.36 pp** more from the same
distance with him on; the **free-throw placebo reads +0.38**. Raw is +4.80 and
mostly personnel. Forecasts at slope **1.082 ± 0.084, 12/12 seasons**, 2.66M
out-of-sample attempts. Shrinkage is not optional — raw coefficients make Brier
*worse*. Priced: MAE 8.1321, still the **best pooled MAE of any arm**.

### 4. The four factors, measured as influence — and the trap in them

Turnovers, steals, both rebound channels and free-throw rate, per **opportunity**
(rebounds per miss, not per possession). All forecast. **Then the face lists
said three of them were measuring the wrong thing:** the "most helpful"
defensive-rebound influencers were Robin Lopez, Hollins, Garza; the least were
Drummond, Camby, Giannis.

**The load-bearing lesson:** the expectation `E = d·Σ own rates` assumes rates
ADD, and rebounds do not — only one of five can collect a miss. **A coefficient
that is a linear function of a man's own rate is an accounting correction to a
mis-specified expectation, and can forecast perfectly while saying nothing about
his effect on the other four.** `channel_influence_orth.py` strips it. Orthogonal
slopes: turnover 0.434 ± 0.024, def rebound 0.908 ± 0.037, off rebound
1.031 ± 0.264, steal 0.512 ± 0.100, FT rate 0.271 ± 0.014. Offensive rebounding
did NOT forecast as a whole (−0.938, 3/12) and its orthogonal part does — the
accounting term was wrong-signed and hiding a real effect.

Also: §6's point-residual turnover channel correlates **−0.003** with the direct
count fit at identical spread. **Fit a mechanism on its own events, then price
it.**

### 5. §8i was WRONG and is overturned (this one matters most for you)

I had claimed the model "prices location well" — valuation correlates +0.989
with raw points/attempt, a long-two→rim move worth **+0.548** — and ranked a
lineup-dependent six-bucket mix as the top next build. **That read the valuation
column in isolation.** The model also carries
`making = 2·2PA·(self_2p − mix @ league_pct)`, which subtracts the league make
rate at the player's own locations and nearly cancels it.

Perturbing real profiles and re-scoring through `asof_point_allocation.predict`
itself: long-mid → rim is **+0.006 per attempt moved, not +0.548**, and mid → rim
is **negative**. The two-point score decomposes exactly (2.2e-14):

```
2-point score = 2·2PA·self_2p  +  Σ_b 2PA_b·(value_b − 2·pct_b)
```

The first term has no mix in it. Location reaches the score only through the
spread of the second (0.079, vs the valuation's 0.548). **`onfloor_location_size`'s
1.354 pts/100 "reliable location gap" uses the same valuation-only arithmetic
and is an upper bound on something the model cannot express.**

### 6. The real defect, and the fix that works

`self_2p` is **one number per player** — the model asserts a rim attempt and a
long two convert at the same personal rate. Nested forward test, 2.66M held-out
attempts, matched to the profile's own 730-day recency:

| predictor | Brier | seasons |
|---|---|---|
| current (player scalar) | 0.241412 | — |
| **league rate at that bucket, no player at all** | 0.234347 | 12/12 |
| league + one player offset | 0.233400 | 12/12 |
| player × bucket | 0.233077 | 12/12 |

**The model's shot predictor is worse than ignoring the player entirely.**

Priced as an exact making-term replacement, nested to 1.4e-14. Best arm
`pbp_offset`: RMSE 10.9120, r² 0.10888, bias −0.495 (vs parent −0.680), novel
8.8812. Slope **+0.635** orthogonal to the parent; placebo +0.004; and
**corr with the shot-quality term −0.030 — it ADDS.**

Ship `offset`, not `bucket`: the player-by-location interaction wins per attempt
(−0.000323, 12/12) and **loses per lineup** (+0.449 vs +0.635).

### 7. Teammates move where you shoot — measured, held back

§10's design, not §11's: one **attempt**, residual against the shooter's own mix,
**only teammates' attempts counted** — no own-rate artifact by construction. All
six buckets forecast 12/12; one sd of teammates moves a player's **rim share by
4.3 percentage points**. A parameterisation error was caught by the corner three
refusing to forecast (−0.077, 0/12): the model normalises `two_mix` and
`three_mix` **separately**, with the 2-vs-3 split owned by `r3pa`.

`flat_mix` demonstrates §8j on the same shift: **0.069 pts/100 on the flat curve,
1.230 on the per-bucket curve.** But the mix prices at slope +0.185 (8/12,
placebo −0.086) — ~5× over-scaled. Prior-only slope scaling helps the metric but
does **not** calibrate it (scaled slope falls to +0.120, prior estimate ranges
−0.277 to +0.580). **Held back.**

### 8. The mixing rule itself

The whole of it is `budget / total_usage`, one scalar, so the model asserts a
player's share is exactly his marginal usage over the five's. Measured
leave-one-unit-out on 6.8M usage events / 3,266 units: asserted 1.000, observed
**1.0574** — shares amplify, the rich get richer (>25% usage players take +0.54pp
more than proportional). **But it is right to within 6%, so this is not the weak
point.** Not a 5-Shaq lever either: five identical players split five ways under
any symmetric rule.

### 9. A shared player factor — real, and it launders shot quality

The influence channels correlate 0.33–0.37 (rim-share ↔ shot quality +0.330,
rim-share ↔ turnover −0.366). Out of sample, the **rim-share coefficient predicts
a player's future turnover influence 92% as well as his own turnover coefficient
does** (−0.0047 ± 0.0007, 12/12, placebo +0.0002 ± 0.0003), and adding the other
channels drops turnover's own weight from 0.0075 to 0.0051. The reverse is not
true — rim share gets nothing from anyone. **The well-measured channel lends to
the badly-measured one.**

Built it (`channel_factor_fit.py`, validated on a synthetic null). It rescues
turnovers — channel r² 471→515, calibration 0.434→~1.0, points MAE 8.1406 with
every metric moving right — and **damages both rebound channels** (ORB r²
771→139). Do not extend it there.

**Then the comparison that matters:** the improved turnover coefficient
correlates **+0.518** with the shot-quality term and prices **−0.239** orthogonal
to parent AND shot quality. Against shot quality alone it adds only novel MAE and
costs pooled MAE. **Most of the rescue is shot quality wearing a turnover hat.**

### 10. Everything assembled

| arm | MAE | RMSE | r² | novel |
|---|---|---|---|---|
| parent | 8.1440 | 10.9214 | 0.10733 | 8.8903 |
| shot quality alone | **8.1321** | 10.9048 | 0.11005 | 8.8745 |
| all four | 8.1517 | 10.9024 | 0.11044 | 8.8678 |
| **best three (no mix)** | 8.1386 | **10.8965** | **0.11140** | **8.8612** |
| corrected additive | **8.0920** | **10.8410** | **0.12043** | 8.9039 |

Location and shot quality are **orthogonal (−0.030)** and add. Turnover overlaps
shot quality at 0.518. Dropping the mix improves everything.

**Honest significance, season-paired over 11 seasons — only one is convincing:**

| comparison | slice | difference | seasons |
|---|---|---|---|
| best three − parent | **novel** | **−0.0298 ± 0.0194** | **9/11** |
| best three − parent | all | −0.0043 ± 0.0247 | 6/11 |
| best three − additive | novel | −0.0445 ± 0.0736 | 6/11 |
| best three − additive | all | +0.0423 ± 0.0334 | 3/11 |

**Nothing here overturns `MATCHED_BENCHMARK.md`.** The additive keeps a pooled
lead. The novel-slice advantage is a point estimate at ±0.074.

---

## Corrections I made to my own claims

Recorded rather than quietly edited, because you may have read the earlier
versions:

1. **§8h overclaim** — "the model is nearly indifferent to shot mix at fixed
   volume" was too broad; corrected in §8i.
2. **§8i overturned by §8j** — see item 5 above. The +0.548 figure, the "location
   is the open lever" ranking, and the 1.354 pts/100 sizing are all superseded.
   This was propagated into CLAUDE.md, BACKLOG, SESSION_HANDOFF, a memory and
   STRUCTURAL_MODEL.md; all corrected.
3. **Asserted residual variances** in `channel_influence` — the docstring claimed
   they were checked against data and they were not (0.75–0.97× truth). Then the
   fix divided by total weight instead of unit count (right for turnovers, 2.3×
   too small for rebounds). Both fixed; variances now measured per origin.
4. **`two_way_demean` drained one key then the other** — sequential
   residualisation, not two-way FE. Caught by a test. Shot quality's forward
   slope went 0.810 → 1.082.
5. **Steals parsed as 0 events** — a `break` after the first match, but "steal
   by" sits inside the turnover segment.
6. **A commit landed on a RED suite** (`d5f6989`) — `unittest | tail && git
   commit` returns tail's exit code. Fixed in `13fdab7`; `set -o pipefail` since.
7. **Bundled the data source with the recency** — the `pbp_scalar` control read
   +0.0252 MAE until matched to the profile's 730-day half-life, then −0.0010.
8. **Wrong EB centre when inverting shrinkage** — `channel_influence.shrink`
   centres on the exposure-weighted mean, not zero. Symptom was a "factor +
   remainder" arm collapsing exactly onto the pure factor; the symptom did not
   name the cause, and three specs gave three orderings before it was fixed.

---

## Four rules this session earned

1. **A coefficient linear in the player's own rate is accounting, not
   influence.** Orthogonalise before believing a 12/12 forward slope.
2. **A channel that forecasts on its own events need not pay in points.**
   Turnover forecast at 0.434 over 3M possessions and priced at −0.028 once what
   the parent already knows is removed.
3. **Borrowed strength must be scored against the lender**, never the parent.
4. **Before building a lever, perturb the model and re-score.** Reading one
   column of a fitted valuation is not the same as asking what the model does —
   that is how §8i survived as the top-ranked build.

---

## Do not re-run

- The channel parse and five-channel forward run (`possession_channels_*_5.npz`,
  `channel_influence_coefficients.pkl`) — complete; the cache key carries the
  channel count.
- Ensembling additive and structural — ρ 0.9856, ceiling 0.15% of RMSE.
- A lineup-dependent shot mix **on a flat conversion curve** — null by
  construction (§8j).
- Fitting a channel on the point residual to recover it (§11b, r = −0.003).
- The shared factor on the rebound channels — it damages them.

## Open, in the order I would take them

1. **Condition the mix on `assisted`.** The arm gives a player pushed to the rim
   by teammates the conversion he earns on his *own* rim attempts; a created shot
   is not a self-created shot. The profile already carries the field.
2. **A contested-rebound expectation.** Both rebound channels forecast (0.908,
   1.031 orthogonal) with inverted face lists. Needs an expectation that knows
   only one of five can collect — not a bigger fit, and the one thing the factor
   cannot fix.
3. **The free-throw garbage-time test** (~10 min, closes an open confound). FT
   rate has the largest spread and an end-of-bench face list; demean by (game,
   score-margin bucket) and re-run `channel_influence_orth`.
4. **Softmax allocator with a learned temperature** — contains proportional
   allocation as the temperature-1 case, worth the measured 6%. For coherence and
   the trade counterfactual, not accuracy.

## New modules

`shot_quality*.py`, `possession_channels.py`, `channel_influence*.py`,
`location_skill*.py`, `location_points.py`, `mix_influence*.py`, `mix_points.py`,
`allocation_rule.py`, `channel_factor*.py`, `factor_test.py`, `assembled.py`,
plus the `onfloor_*` family from the first half of the session. Every scoring
module rebuilds the parent from profiles and gate-checks it to 1e-6 before
scoring anything; observed reproduction is 1e-13 to 1e-14.

---

## Reproduce

Everything below runs from the repo root with the project interpreter, as a
module, always with `-u`. Nothing here writes to Postgres, refits the additive
benchmark, or touches a completed run directory. Times are wall clock as
observed on Adam's machine today.

```bash
cd /Users/adam/Documents/basketball
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
```

**Stage 1 — parses (build the caches everything else reads).** Both are cached;
they only re-parse if the cache file is missing.

| command | time | produces |
|---|---|---|
| `$PY -u -c "from experiments.shot_quality import build; build()"` | ~4 min cold | `shot_events2_<key>.pkl`, 6.85M attempts |
| `$PY -u -c "from experiments.possession_channels import build; build()"` | 57 s | `possession_channels_<key>_5.npz` |

**Stage 2 — channel measurement (all strictly prior, 44 origins).**

| command | time | §  |
|---|---|---|
| `$PY -u -m experiments.shot_quality_sweep` | ~3 min | §10 |
| `$PY -u -m experiments.shot_quality_forward` | ~6 min | §10b |
| `$PY -u -m experiments.channel_influence_run` | **503 s** | §11 |
| `$PY -u -m experiments.channel_influence_orth` | 73 s | §11b |
| `$PY -u -m experiments.location_skill_run` | 35 s | §12 |
| `$PY -u -m experiments.mix_influence_run` | 91 s | §13 |
| `$PY -u -m experiments.allocation_rule` | 8 s | §14 |
| `$PY -u -m experiments.channel_factor` | 5 s | §14b |
| `$PY -u -m experiments.factor_test` | ~40 s | §14c |
| `$PY -u -m experiments.channel_factor_run` | ~30 s | §15 |

**Stage 3 — pricing (each rebuilds the parent and gate-checks it to 1e-6).**

| command | time | § |
|---|---|---|
| `$PY -u -m experiments.shot_quality_points` | ~35 s | §10c |
| `$PY -u -m experiments.turnover_points` | 33 s | §11d, §15 |
| `$PY -u -m experiments.location_points` | 26 s | §12b |
| `$PY -u -m experiments.mix_points` | 26 s | §13b |
| `$PY -u -m experiments.assembled` | 32 s | §16 |

**Order matters.** Stage 3 reads coefficient pickles written by stage 2, and
`assembled` reads four of them. `channel_factor_run` must run before
`turnover_points` if you want its `turnover_factor` arm; without the pickle that
arm silently falls back to the un-improved coefficient (see `FACTOR` in
`turnover_points.py`).

**Tests:** `$PY -u -m unittest discover -s tests` — 606 tests, ~28 s. Use
`set -o pipefail` if you pipe it into `tail` before a commit; a pipeline returns
tail's exit code and that landed a red commit here once (`d5f6989`).

---

## Cache manifest

The repo convention (`.gitignore` lines 6–30) is that **`*.csv` result tables are
tracked and `*.pkl` / `*.npz` caches are not** — 1,113 CSVs under
`experiments/cache/` are in git, and the binaries regenerate. So a fresh
checkout has every number but none of the coefficients.

**Tracked — read these directly, no run needed:**

| file | what |
|---|---|
| `*_metrics.csv` for each module | the headline tables in this digest |
| `location_skill_origins.csv` | per-origin Brier for the four nested predictors |
| `channel_influence_orth_origins.csv` | own-rate slope and variance explained, per channel |
| `assembled_overlap.csv` | the cross-term correlation matrix |
| `channel_factor_correlation.csv` | §14b's cross-channel correlations |
| `channel_factor_run_loadings.csv` | factor loadings and communalities per origin |
| `allocation_rule_metrics.csv`, `_rows.csv.gz` | the 1.0574 mixing-rule result |
| `*_points_cells.csv.gz` (≤900 KB each) | per-cell scores for every arm |
| `shot_quality_forward_shots.csv.gz` (44 MB) | per-shot forward panel |

**Untracked — regenerate before reusing (times in the table above):**

| file | size | regenerate with |
|---|---|---|
| `shot_events2_<key>.pkl` | 229 MB | `shot_quality.build()` |
| `possession_channels_<key>_5.npz` | 32 MB | `possession_channels.build()` |
| `onfloor_influence_coefficients.pkl` | 50 MB | `onfloor_influence_run --fit` |
| `mix_influence_coefficients.pkl` | 10 MB | `mix_influence_run` |
| `channel_influence_orth_coefficients.pkl` | 9.4 MB | `channel_influence_orth` |
| `location_skill_coefficients.pkl` | 7.5 MB | `location_skill_run` |
| `channel_influence_coefficients.pkl` | 7.0 MB | `channel_influence_run` |
| `channel_factor_run_coefficients.pkl` | 6.2 MB | `channel_factor_run` |
| `shot_quality_forward_coefficients.pkl` | 2.8 MB | `shot_quality_forward` |

**Explicitly gitignored, not merely untracked** (`.gitignore` lines 42–43):
`channel_influence_units.csv.gz` and `channel_influence_orth_units.csv.gz`, 96 MB
each. `turnover_points.prior_slopes()` reads the second one, so run
`channel_influence_orth` before `turnover_points` on a fresh checkout.

**Cache keys.** `possession_channels` carries the channel count in its filename
(`..._5.npz`) precisely so that adding a channel cannot be silently satisfied by
a parse made before it existed. If you add one, the file name changes and the
parse re-runs. `shot_events2` and the possession caches key off
`experiments.data._cache_key(DEFAULT)`, which tracks the source database epoch —
do **not** rebuild them to "refresh"; the 2,492-game update is complete and
`CLAUDE.md` forbids repeating it.
