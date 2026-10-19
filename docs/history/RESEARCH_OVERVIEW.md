> **Historical research journal — 2026-09-18 notice:** Preserve these dated
> investigations, corrections and failed approaches as evidence. Their “next,”
> “closed” and shipped-product claims are not present operating instructions.
> Start with [current state](JOINT_CAPABILITY_STATE.md), the
> [canonical backlog](../../MODEL_RESEARCH_ROADMAP.md) and
> [documentation index](README.md). Original journal body follows unchanged.

# Basketball Possession Prediction — Research Overview

A structured memo on what this repository is trying to do, what has been tried,
what the data appears to allow, and where the research can productively go next.

**How to read this.** It is written in order of discovery, so later sections
supersede earlier ones. If you have time for two sections, read **§8** (how much
non-additive lineup signal exists at all) and **§9** (how much *linear* signal
exists, and the current model). §1–7 are the historical record of how the
project got there, including several conclusions later shown to be artifacts of
the target or the baseline — each is flagged where it occurs. Where §1–7
conflict with §8–9, §8–9 is current.

**Current contextual work:** read `CONTEXTUAL_MODEL.md` for the three-pillar
contract and §39 below for the verified 2025-26 refresh. Historical contextual
point-model rho headlines used unstable averages of reliability ratios; §39
supersedes those levels with pooled-moment estimates and ordinary metrics.

---

## 1. Problem statement

**The northstar: a tool that prices any theoretical five-man lineup** —
including one that has never played — in points per 100 possessions, from the
10 players on the court and what their play-style profiles say about how they
fit together. Both sides of the ball ship, even where the best defensive model
is one coefficient per player. Output must be broadly understandable and backed
by real, well-founded data, with the model's uncertainty shown rather than
hidden. Built: `tool/five.html`.

The unit of fitting is still a single possession: predict `points_scored` from
the 5 offensive and 5 defensive players.

- **Inputs**: an unordered set of 5 offensive player IDs and an unordered set of 5 defensive player IDs.
- **Target**: `points_scored`, a small integer per possession (typically 0, 1, 2, 3; occasionally 4+ with and-ones / technicals).
- **Player profiles**: play-style vectors built from box-score aggregates
  (shot locations, assist/turnover/rebound rates, self-creation) are a first-class
  input. They carry the synergy term (§8.4) and, used as a ridge *prior mean*,
  are the single largest improvement ever measured on this problem
  (+0.000181, §9.3). Profiles are always built from training games only.
- **Context**: score margin and game clock are loaded by `context.py` and used
  as controls — for checking that an effect is not garbage-time deployment
  (§9.4) — rather than as features.
- **The one constraint that still binds**: the model must be able to price a
  **lineup that has never played**. That is the whole point, and it is what
  rules out trees (§1.1) — not any restriction on what a player's profile may
  contain.
- **Evaluation**: MSE on held-out possessions from future time periods (forward-in-time splits).
- **Framing**: research *and*, since Phase 9, a deliverable. Relative
  improvement over a strong linear baseline is what matters for the science;
  absolute variance reduction is small because possession-level outcomes are
  extremely noisy. For the tool, the metric that matters is not r² at all but
  ρ with true lineup quality and the calibration slope — see §9.6.

The research question underneath the prediction task: **Is there an identifiable non-linear player-interaction signal in this data, and if so, what kind of model architecture teaches us about it?** The user's prior (as an experienced basketball player) is that interactions and skill-profile synergies *must* be present; the data-side difficulty is proving it statistically.

### 1.1 Why this is interesting — the dream model

A purely additive model — "each player has a scalar offensive and defensive skill; lineup value is the sum" — can rank players, but it cannot tell a coach anything about *combinations*. The interesting model is one that captures **synergy**: the fact that Player A plus Player B together produces more (or less) than the sum of their individual parts, that a specific offensive five-man group can exploit specific weaknesses in a specific defensive five-man group, and that the optimal offensive lineup against one defense is not the optimal offensive lineup against another.

If such a model exists and is predictive, it unlocks research use cases that a linear model cannot:

- **Lineup search**: given a fixed defensive five, rank every possible offensive five by expected PPP — and the ranking is *not* just the top five offensive-skill players summed, because it depends on the specific defense.
- **Matchup analysis**: identify which archetype combinations a given defense struggles against, without pre-defining archetypes.
- **Counterfactual reasoning**: evaluate lineups that have never co-occurred in training — the whole point of extrapolation.

**Architectural consequence — this rules out tree-based models.** Random forests and gradient-boosted trees (XGBoost, LightGBM) predict by partitioning the input space and returning leaf averages. For a 10-player-ID input with ~500 candidate players, the "cells" of interest are specific lineup combinations; a tree that has never seen a particular lineup returns a generic average over similar leaves, which collapses back toward the linear additive prediction. Trees **cannot extrapolate across the combinatorial space of lineups** in the way needed for lineup search — they can interpolate within seen partitions, but they cannot synthesize new combinations from learned player-level representations. This is why XGBoost showed up in the approaches below and never helped: it was the wrong tool for the research goal, not just an underperforming one.

The models that *can* support the dream use case are ones that learn **per-player vector representations** and combine them through a learned non-linear function:

- Factorization machines and their neural extensions (NFM, deep FMs).
- Set-attention / deep-set architectures over the 10-player set.
- Transformer-style interaction via multi-head attention across player embeddings.
- Any explicitly factorized interaction model where lineup value = f(aggregation of learned player vectors).

All of these produce predictions for novel lineups by composing player vectors that *are* in training, even when the specific combination is not. That composition is what enables extrapolation. The research goal is therefore narrower than "beat ridge on MSE" — it is **"beat ridge on MSE with an architecture that can evaluate unseen lineups."**

---

## 2. Data & feature layer

### Schema (see `tables.sql`)

- `nba.games`: `game_id`, `game_date`, teams, points, `playoffs` flag.
- `nba.possessions`: `game_id`, `quarter`, `time_left_start/end`, `away_team_ball`, `turnover`, `points_scored`, `scorer`, and the 10 player-ID columns. Also a `texts` column with play-by-play text.
- `nba.players`: `player_id`, name, `position` (float), `height_inches`.
- `nba.player_game_stats` + `nba.player_historical_features`: box-score features and rolling 10-game stats, computed by `calculate_historical_features.py`. **Not used in the player-IDs-only framing.**

### Data provenance

- `scrape_br.ipynb` scrapes Basketball-Reference box scores / play-by-play.
- `collect_player_stats.py` pulls ESPN for supplementary game-level stats.
- CSVs like `jokic.csv`, `lebron.csv`, `ant.csv`, `mj.csv` appear to be single-player exploratory data; not load-bearing for the modeling work.

### Data scale

- **~20 NBA seasons of possession-level play-by-play is available in the database** (roughly 2003–2024, depending on the scrape coverage). This is the full corpus.
- **Prior experiments have mostly used a 2-season window** (`2022-08-01 → 2024-08-01`), which is a choice, not a constraint. Within that window: ~500–600 unique players, 25th-percentile player ~100 possessions, many players < 500. Possession-level variance ≈ 1.39 points².
- **Using the full corpus changes the small-data picture substantially**. A ~20-year window gives ≈ 10× more possessions and introduces a much larger cast of players (turnover + aging + expansion), but it also increases pair co-occurrence counts for long-tenured and frequently-teammates players by 10–20×, which is precisely the quantity that governs whether pair-interaction effects are identifiable. Pair sparsity, not total-n, is what limits non-additive signal detection, and pair sparsity improves non-linearly with seasons of coverage.
- **Caveats of long-window training for this problem**: (a) the game has changed substantially across 20 years (pace, 3-point rate, defensive rules) — seasonal/era detrending becomes essential; (b) player-identity is stable (the same `player_id` means the same person) but a player's *skill* evolves with age; (c) rule changes (hand-checking in 2004, take-foul in 2022, etc.) create regime shifts; (d) not every season may have equal play-by-play quality in the scrape. All of these are addressable inside the pipeline and should not gate using the larger corpus.

---

## 3. Approaches tried — at-a-glance

Organized by family. MSE values are at the possession level where reported.

| Family | Representative file(s) | Idea | Result vs mean baseline |
|---|---|---|---|
| **Ridge baselines** | `predict_possessions_baselines.ipynb`, `ridge_*_optimization.py` | One coefficient per player; variants: offense-only, overall-quality, offense+defense | Ridge + detrend + shrinkage best ≈ **+0.11%** (lineup-level grid, MSE 1.38547) |
| **Ridge w/ pair interactions** | `interaction_threshold_experiment.py`, `possession_level_grid_search.csv` | Add interaction columns for teammate pairs with ≥ T co-occurrences, heavily regularized | Best **+0.095%** at α=10000, min_pair_count=1000, detrend=True (MSE 1.38571) |
| **Lasso** | `lasso_experiment.py` | L1-regularized linear model over one-hot lineups | Comparable to ridge; no measurable advantage |
| **NFM (Neural FM)** | `nfm_experiment.py`, `nfm_optimization.py`, `nfm_multisplit.py` | Factorization machines with embedding-based pairwise interactions | Best MSE 1.38629 (emb=16, dropout=0.3, wd=1e-4) — **ties ridge, does not beat** |
| **Bayesian / Hierarchical NFM** | `bayesian_nfm.py`, `bayesian_nfm_multisplit.py`, `hierarchical_nfm.py` | Prior-regularized NFM variants | No reliable improvement reported |
| **FFN** | `predict_possessions-ffn.ipynb` | Feed-forward net over lineup embeddings | Matches ridge at best, typically worse |
| **Transformer (v1–v3)** | `predict_possessions-transformer.ipynb` (52MB), `-transformer2.ipynb`, `-transformer2-2.ipynb` | Attention over the 10-player sequence with positional encodings, multi-head attention, regression head; O/D embeddings | Matches ridge at best |
| **Ridge-Transformer hybrid** | `predict_possessions-ridgetransformer.ipynb` | Linear ridge terms + transformer residual | No improvement |
| **Residual learning** | `residual_learning.py`, `residual_team_aware*.py`, `residual_bayesian_ensemble.py`, `residual_xgboost_experiment.py`, etc. (7+ files) | Second-stage model learns ridge residuals | Second stage fits noise; no gain |
| **XGBoost** | `xgboost_optimization.py`, `residual_xgboost_experiment.py` | Tree ensemble over one-hot features | No gain — **and architecturally inappropriate for the extrapolation goal** (see §1.1) |
| **Text-joint model** | `text_model.py`, `text_*embedding_*.py` | Joint prediction of `points_scored` and play-by-play text | No gain on the points target |
| **O/D decomposition** | `offense_defense_models.py` | Train separate 5-man offense and defense models, combine at prediction | **Worse** than joint |
| **Lineup-level denoising** | `lineup_level_experiments.py`, `possession_vs_lineup_comparison.py`, `multisplit_grid_search.py`, `predict_possessions_smoothing.ipynb` | Aggregate possessions to unique 10-man lineups, model the mean, evaluate on raw | Best single improvement: **+0.11%** with detrend+shrinkage (k=5) |
| **Seasonal detrending** | `explore_seasonal.py` | Remove league-wide cyclical PPP trend before modeling | Detrend alone ≈ 0.02% of variance; **essential** for lineup-level to not degrade |
| **Most recent iteration** | `predict_possessions_smoothing.ipynb` (Feb 2025), `NNPredictor` class | Transformer + multiple embedding-divergence regularizers + label smoothing + temporal weighting + lineup aggregation | Still ties ridge |

**Supporting CSVs**: `possession_level_grid_search.csv`, `lineup_level_grid_search.csv`, `nfm_optimization_results.csv`, `multisplit_grid_search.py` output.

---

## 4. Key findings so far

1. **Every family plateaus at MSE ≈ 1.385–1.395** on the 2-season window. Ridge, NFM, transformer, residual ensembles, XGBoost — they converge on the same number. **Whether this plateau persists with the full ~20-year corpus is an open question** and is the single most important empirical uncertainty in the repository right now.
2. **Ridge explains ~0.1% of possession-level variance** over a simple mean predictor (league PPP), on the 2-season window. This sets an apparent ceiling on "lineup-identity attributable variance" at per-possession granularity — but the estimate itself is sample-size limited, and the ceiling may rise with more seasons of data because player effects and pair effects are estimated more precisely.
3. **Lineup-level aggregation** (averaging PPP for each unique 10-man lineup) plus seasonal detrending plus empirical-Bayes shrinkage of lineup means is the single biggest improvement found so far: **+0.11%** vs **+0.095%** for possession-level pair interactions. Both marginal in absolute terms.
4. **Seasonal detrending** is trivially tiny on its own (0.02%) but **essential** in the lineup-level setup — without it, shrinkage on the lineup target degrades test performance by 17–47% because lineup sample composition is confounded with date.
5. **Splitting offense and defense into separate models hurts.** The joint representation carries information that the decomposition throws away, or the shared signal regularization is what matters.
6. **Pair-interaction ridge at very high α showed a whisker of improvement** over additive ridge — the only direct positive evidence in the repository that non-additive player signal is detectable in this dataset. The magnitude is on the edge of noise.

---

## 5. Critique

### 5.1 The apparent ceiling may be sample-size limited, not intrinsic

Per-possession `points_scored` is a small integer with total variance ≈ 1.39. Within the 2-season window used for most prior experiments, lineup identity contributes ~0.0014 to MSE-reduction, so ~0.1% of total variance. Any model — ridge, NFM, transformer — has had to pull that tiny signal out of a much larger noise floor using only hundreds of possessions per player and far fewer per pair.

The important nuance: **much of this ceiling is likely sample-size artifact, not a true information-theoretic limit.** The within-possession shot/ref/bounce noise is irreducible; but the apparent 0.1% is an estimate of signal *attributable to what the model could stably learn from the available data*, not of the true underlying signal. With 10× more data (the full 20-year corpus), two things change: (a) per-player coefficients are estimated with ~√10 ≈ 3× less variance, so the additive baseline itself gets tighter; (b) pair co-occurrences with ≥ T possessions multiply by roughly 10–20×, meaning the *identifiable* non-additive signal — the quantity that all non-linear modeling work has been trying to estimate — should rise substantially.

This reframing is important: complex models in the existing work have not "failed to learn synergy"; they have **hit a sample-size-limited signal ceiling**. The right next question is not "which architecture wins on the 2-season data?" but "how does the recoverable non-additive signal scale with seasons of data, and what architecture best exploits it at the largest data setting we can construct?"

### 5.2 Evaluation protocol inconsistency is the single biggest methodological problem

Across ~50 scripts and ~10 notebooks:

- Some use a single split; some use 5; some use K-fold.
- Different date windows and different inclusion/exclusion filters (playoffs? garbage time? turnover-only possessions?).
- Different α ranges, different weighting schemes, different temporal decay constants.
- Different "improvement" baselines (mean vs ridge vs additive NFM).

This makes cross-script numerical comparisons unreliable — and the research trajectory has relied on them. A single canonical evaluation harness is a prerequisite for anything else.

### 5.3 The residual-learning framework is learning mostly noise

Ridge residuals at possession level have variance ≈ total variance (ridge removes only 0.1%). Training a second-stage tree / NFM / NN on those residuals is asking it to find signal in a dataset that is 99.9% noise. The extensive `residual_*.py` family cannot plausibly yield stable gains; the setup is mis-targeted. A residual approach would only make sense if the first stage explained a non-trivial fraction of variance (which at this granularity it cannot).

### 5.4 Non-linear models are overparameterized for the data window they've been trained on

A transformer with embeddings for ~500 players, multi-head attention, FFN head, and positional encoding for the 10-player sequence easily has 10⁶ parameters. Against ~200k training possessions from a 2-season window where identifiable non-additive signal is ≲ 0.1% of variance, the implicit regularization burden is enormous. Regularization schedules have been tuned empirically but never *derived* from a noise-ceiling estimate. The architecture class is not wrong — in fact it is exactly the right class for the extrapolation goal (§1.1) — but its capacity has not been matched to the signal floor, **and it has not been given the full available data**. Retraining the same architectures on the full 20-year corpus is a cheap and informative test before concluding anything about the architecture itself.

### 5.5 The "is there synergy at all?" question has never been answered cleanly — and was asked against the wrong data size

Before asking *which* non-linear model teaches us about synergy, the identifiability question should be settled: can stable pair-level or lineup-level non-additive effects be detected in the data at all? That is a statistical-identifiability question, not a modeling question, and it has a concrete answer obtainable without training any deep model (see Phase 1 below). The whisker of improvement from the pair-interaction ridge suggests "maybe" — but crucially, that test was run on 2 seasons. Running the same identifiability probe on the full 20-year corpus is where this question should actually be answered.

### 5.6 Denoising-the-target and modeling strands were pursued in parallel rather than composed

Lineup-level aggregation is the most promising finding but was explored alongside, not inside, the modeling family experiments. There is no clean head-to-head of "best possession-level model" vs "same model trained on lineup-aggregated target and evaluated on raw possessions" with the same hyperparameter grid and the same eval protocol.

### 5.7 Repository sprawl

- 7+ `residual_*.py` variants, 4+ NFM variants, 3 transformer notebooks, several ridge-optimization scripts, multiple grid-search scripts with subtly different protocols.
- No canonical "here's the best model, here's how to reproduce it" entry point.
- `Basketball Model Research.md` is a raw chat transcript — useful history, not a research summary.
- Model checkpoint files (`best.pt`, `player_embeddings.pt`) sit at repo root with no linkage back to the script that produced them.

This makes it hard to *extend* the research — a future session either re-derives what's been tried or duplicates it.

---

## 6. Proposed path forward

Ordered so that each phase's result determines whether the next is worth pursuing. The overarching goal of the plan is a **non-linear model, predictive above a strong additive baseline, that extrapolates to unseen offensive-vs-defensive lineup combinations** (§1.1). The prior 2-season window is abandoned in favor of **using as much of the ~20-year corpus as stable evaluation allows** (§2).

### Phase 0 — Lock the evaluation protocol and choose the training window (prerequisite, ~1–2 days)

Build a single evaluation harness all future experiments share:

- **Training window**: default to the largest stable window — probably the full ~20 years of available possessions, optionally with era-boundary handling for large rule changes (2004 hand-check, 2017-ish three-point-revolution, 2022 take-foul). The harness should make this a parameter so the "2 seasons vs 20 seasons" contrast is itself measurable.
- **Held-out test set**: last K weeks of the most recent season (forward-in-time only). This is fixed regardless of training window.
- **Extra validation set dedicated to extrapolation**: construct a "novel-lineup" evaluation split — possessions where the specific 10-man lineup (or even the offensive 5 / defensive 5) has not appeared in training. This directly measures the property the dream model needs. Every model reports MSE both on the standard test set and on this extrapolation set.
- Fixed filters (regular season only, explicit rules on garbage time / injury-early-quarter).
- Fixed reporting: standard-MSE, novel-lineup-MSE, R²-over-mean, R²-over-additive-ridge, across ≥ 5 rolling-origin validation splits (not random ones, since training window size matters), mean ± std.
- Seasonal / era detrending applied inside the harness, not per-script. This becomes more important when the window extends 20 years.

All current `ridge_*.py`, `nfm_*.py`, `residual_*.py`, grid-search scripts are retired or rewritten against this harness. Number one rule: no cross-script comparison unless both went through the same harness.

### Phase 1 — Identifiability probe (~2–3 days, model-free, run on the full corpus)

Before any more architecture work, answer: *can non-additive lineup and pair signal be detected in the data, and how does detectability scale with data size?*

1. **Additive baseline**: for each player, estimate an offensive-impact scalar `oᵢ` and defensive-impact scalar `dᵢ` via ridge. Predicted lineup PPP = league_mean + Σ oᵢ (off) − Σ dⱼ (def).
2. **Observed lineup residual**: for each 10-man lineup with ≥ N possessions, compute `r_L = observed_PPP(L) − additive_prediction(L)`.
3. **Resampling null**: for each such lineup, bootstrap-resample its possessions and recompute `r_L`; the spread across resamples is the per-lineup noise scale.
4. **Stability test**: partition games into two halves (earlier / later, or odd / even); compute `r_L` on each half; check correlation. Non-zero correlation beyond the resampling null = identifiable non-additive signal.
5. **Pair-level version**: same idea for 2-player co-occurrence residuals (both within-team "teammate pair" and cross-team "matchup pair"). Matchup pairs are the ones most directly relevant to the extrapolation/lineup-search goal.
6. **Scaling curve**: re-run the probe at 2, 5, 10, 20 seasons of data. The output is a curve showing how the fraction of variance attributable to stable non-additive effects grows with sample size. This curve alone is a publishable empirical result for the NBA-analytics community, and it directly informs whether the architectural work in Phases 2–5 can succeed at current data volumes or whether the research frames as "more data needed".

If the stability correlation is already positive at 2 seasons, the existing "every model ties ridge" result is strong evidence that architectures have been the bottleneck. If it only becomes positive at 10+ seasons, the bottleneck was data all along and prior null results are explained.

### Phase 2 — Empirical-Bayes / partial-pooling player embeddings

The principled version of "ridge with tuned α". Instead of each player getting an independent coefficient penalized by a single global α:

- Estimate a global prior `(μ, σ²)` for player effects from the training data.
- Shrink each player's effect toward μ with strength proportional to `1 / n_possessions`.
- Equivalent to a hierarchical Bayesian model with player effects drawn from a shared Gaussian; solvable in closed form or with a couple of EM iterations.

This should dominate any method that doesn't explicitly pool, and provides a baseline that already encodes the main small-data insight.

Extension (subject to the "players only" constraint): **hierarchical pooling by empirical cluster** — cluster players by their observed usage patterns *derived from the training data only* (no exogenous position labels), then pool within cluster. This is borderline with the "inputs = players only" rule; document the decision explicitly.

#### Phase 2 — results (full corpus, 20 seasons, 5.5M possessions, 2300+ players)

Implemented in `experiments/eb.py` as MacKay's fixed-point update on the marginal likelihood — no free hyperparameter, (α_off, α_def, σ²) learned from training data. Two variants:

- `eb_ridge_shared`: single τ² across both blocks (ties α_off = α_def).
- `eb_ridge_offdef`: separate τ²_off and τ²_def, both fitted.

Canonical harness, 5 rolling-origin folds from season 2024:

| Model | α_off | α_def | possession MSE (all) | r²_over_ridge (all) | r²_over_ridge (novel_off5) |
|---|---|---|---|---|---|
| `ridge_ref_α10000` (baseline) | 10000 | 10000 | 1.410103 | 0.000000 | 0.002497 |
| `eb_ridge_shared` | 3178 | 3178 | 1.409994 | +0.000077 | +0.000215 |
| `eb_ridge_offdef` | 3062 | 3302 | 1.409990 | +0.000080 | +0.000218 |

**Key findings:**

1. The baseline α=10000 is **~3× over-regularized**. EB picks α ≈ 3180 on the full corpus. Correcting this gives a tiny, consistent gain across all folds and all slices — positive in every cell, largest in novel-lineup extrapolation slices.
2. **The off/def prior split adds essentially nothing on top of shared-α EB.** Δ r²_over_ridge from splitting = +0.000003 — noise. The α_off / α_def ratio at 20 seasons is 0.93 (nearly 1:1). An earlier smoke test on 5 seasons showed a ratio of 0.69, which appears to have been finite-sample drift — the asymmetry washes out at scale.
3. The absolute improvement over ridge α=10000 is ~8×10⁻⁵ in r²_over_mean. The per-(season,week) baseline already explains ~8.5% of raw variance; the additive-player layer on top explains a further ~0.18%; the EB-tuned α adds another ~0.008% on top of that. The additive ceiling is very close, regardless of how α is chosen.
4. The hierarchical-empirical-clusters extension is **unlikely to pay off**: if partitioning into {off, def} — a partition where one side has plausibly higher prior variance than the other — contributes nothing, finer data-driven partitions are unlikely to either. (This is conditional on the cluster structure being about *prior variance*. If clusters captured a genuinely different prior *mean*, that would be a different lever; worth noting but not the first place to look.)

**Phase 2 conclusion:** pooling is not the lever. Ridge at any reasonable α is essentially at the additive-model ceiling for this problem. The remaining signal is in **interactions**, not in better additive shrinkage. The minimum-viable Phase 2 deliverable — a no-hyperparameter EB additive baseline — is in place and should be used as the reference for Phase 3 going forward, alongside (or in place of) the ridge α=10000 baseline.

### Phase 3 — Interaction modeling

Phase 1 established that *teammate-pair* synergy is identifiable at 20 seasons (split-half r ≈ 0.10); *matchup-pair* synergy is not. Phase 3 asks two questions, in order: (a) does the identifiable pair signal improve prediction above the additive ceiling at all, and (b) — the one that matters for the dream use case (§1.1) — does that signal have the **low-rank / embedding structure** required to predict synergy between players who *never co-occurred* in training? Per-pair coefficients alone cannot answer (b): if players (i,j) never played together, their pair coefficient is mechanically zero regardless of what we know about i and j individually. Only a factorized representation can extrapolate across the combinatorial space of pairs. Phase 3 is therefore staged.

#### Phase 3A — Explicit teammate-pair ridge

One scalar per teammate pair (off-off and def-def separately; off×def excluded per Phase 1), only for pairs with ≥ T training co-occurrences, with per-pair L2 penalty `λ_{ij} = α · c_ref / n_cooccur(i,j)` so rare pairs shrink harder. Staged fit: Phase 2 EB additive, then occurrence-weighted ridge on pair indicators against the residual. This is the cleanest "is there identified pair signal above additive?" test; it is *interpolation-only* by construction and cannot serve the dream use case.

#### Phase 3B — Low-rank / embedding identifiability probe

Before fitting any end-to-end embedding model: is the pair-synergy matrix `Ŝ` (n_players × n_players, symmetric, one per side) low-rank enough that a rank-k factorization fit on one subset of the data predicts held-out pair entries elsewhere?

- Compute per-pair additive-residual synergy estimates on independent halves A and B of the corpus → `Ŝ_A`, `Ŝ_B`.
- Truncated rank-k SVD of `Ŝ_A` for k ∈ {1, 2, 4, 8, 16, 32, 64}.
- Critical subset: pairs observed in B but **not in A**. Does the rank-k reconstruction of `Ŝ_A` predict `Ŝ_B[i,j]` on this subset above chance?

If positive at any k, embeddings extrapolate — Phase 3C is motivated. If flat across all k, the FM / transformer class is closed for this data regardless of architecture sophistication, and the research frames as "the additive ceiling is architectural, not just empirical."

#### Phase 3C — Factorization machine / bilinear under the harness

Conditional on Phase 3B ≥ 0. Fit `y = additive + Σ_{off pairs} <v_i, v_j> + Σ_{def pairs} <v_i, v_j>` with shared player embeddings and co-occurrence-aware embedding-magnitude regularization. Evaluate on the full harness including `novel_off5` / `novel_def5` / `novel_10` — the novel-lineup slices are decisive: they measure whether the learned embeddings compose into useful predictions for lineups not in training, which is the dream use case in its most direct form. A positive result here is the first real architectural claim in this research.

#### Phase 3A — results (full corpus, 20 seasons, 5.5M possessions)

Implemented in `experiments/pairs.py` (`PairMap`, `encode_pairs`, `weighted_ridge_solve` via preconditioned CG) and `experiments/models.py::PairRidge`. Staged fit against Phase 2 `eb_ridge_shared`. Grid: `min_cooccur ∈ {200, 500}`, `α_pair ∈ {3000, 7000, 15000}`, 5 rolling-origin folds from season 2024. Best configuration: `min_cooccur=500, α_pair=15000` (~23k offensive pairs + ~23k defensive pairs retained).

Paired-fold Δr²_over_ridge vs `eb_ridge_shared`:

| Slice | PairRidge | EBRidge | paired Δ | SEM | t |
|---|---|---|---|---|---|
| all | +0.000182 | +0.000077 | +0.000104 | 0.000128 | 0.82 |
| novel_10 | +0.000158 | +0.000084 | +0.000074 | 0.000122 | 0.60 |
| novel_off5 | +0.000183 | +0.000215 | −0.000032 | 0.000241 | −0.13 |
| novel_def5 | +0.000391 | +0.000159 | **+0.000232** | 0.000303 | 0.76 |

**Key findings:**

1. **Direction is consistently positive** at α=15000 on three of four slices, with the largest effect on `novel_def5`. No slice clears |t| > 2 at 5 folds — signal is directionally present but within paired-difference noise.
2. α=15000 sits at the edge of the grid and may not be the optimum. Under-regularized configs (α=3000) overfit on `novel_off5` / `novel_10`.
3. **Asymmetry**: pair ridge lifts `novel_def5` but is flat on `novel_off5`. Phase-1-consistent — defensive coverage rotations appear more pair-structured than offensive scheme.
4. **Phase 3A cannot serve the dream use case** (§1.1). Even where it works, explicit per-pair coefficients predict synergy for pairs with zero training co-occurrences as exactly zero. Extrapolation to unseen lineup composition requires a factorized representation, which Phase 3B tests for and Phase 3C builds.

**Phase 3A verdict:** weak positive direction, hyperparameter-bounded, and — crucially — architecturally incapable of answering the question the research actually cares about. The productive next step is not further α tuning; it is Phase 3B.

#### Phase 3B — results (full corpus, 23 seasons, 5.5M possessions)

Implemented in `experiments/embedding_probe.py` and `experiments/run_embedding_probe.py`. Common EB additive on full corpus (α≈3190, σ²≈1.28) → per-possession detrended residuals → game-level random half-split → per-side mean-residual pair synergy estimates (`Ŝ_A`, `Ŝ_B`, dense symmetric, min_cooccur_half=100) → truncated rank-k SVD of `Ŝ_A` → weighted Pearson correlation against `Ŝ_B` on *pairs observed in B but not in A* (`w_pearson_novel`), against a player-permutation null (`w_pearson_novel_null`), averaged across 3 seeds.

Methodology sanity check — `w_pearson_both` at near-full rank (intersection pairs, the analogue of Phase 1's split-half r):

| side | rank=1024 w_pearson_both | Phase 1 weighted_r at 23 seasons |
|---|---|---|
| off | +0.057 | +0.089 |
| def | +0.015 | +0.059 |

My numbers are 25–65% of Phase 1's — expected. Phase 1 used Ridge(α=10000), whose heavily-shrunk β leaves residual individual-player bias that inflates split-half correlations. EB residuals (α≈3190) have cleaner additive/interaction separation and give a more conservative estimate.

**Main result — generalization to unseen pairs:**

| side | rank | w_pearson_novel | null | Δ | std (3 seeds) |
|---|---|---|---|---|---|
| off | 32 | +0.014 | +0.000 | +0.013 | 0.013 |
| off | 64 | +0.021 | −0.002 | +0.023 | 0.007 |
| **off** | **128** | **+0.029** | **−0.002** | **+0.031** | **0.002** |
| off | 256 | +0.017 | +0.004 | +0.013 | 0.017 |
| off | 1024 | −0.024 | +0.006 | −0.030 | 0.030 |
| def | any | ≲ 0.01 | ≈ 0 | noise | — |

**Key findings:**

1. **Offense: clear positive result at rank ≈ 64–128.** Rank-128 SVD of `Ŝ_A` predicts held-out-in-A pair entries in `Ŝ_B` at weighted r = +0.029 (null = −0.002, 3-seed std = 0.002; ~15σ above null). The signal rises with rank to a peak near 128 then falls as noise dominates. **This is direct evidence that offensive pair synergy has low-rank embedding structure that generalizes to truly unseen pairs** — the property the dream use case requires.
2. **Defense: null at every rank.** `w_pearson_novel` oscillates around 0 across k ∈ {1, 2, 4, ..., 1024}; no meaningful separation from the null. Defensive coverage appears scheme/system driven, not player-chemistry driven — different structural regime than offense.
3. **Asymmetry is interesting and opposite to Phase 3A.** Phase 3A found the pair-ridge prediction improvement on `novel_def5`; Phase 3B finds the embedding extrapolation on offense. Not contradictory — Phase 3A measures "do per-pair coefficients improve possession-level prediction"; Phase 3B measures "do embeddings generalize to unseen pair *synergies*". Different levers in different places.
4. **Rank 128 is surprisingly high.** Only ~37% of Frobenius energy is captured at rank 128; the signal is spread across many components, not concentrated in a handful. A naively-sized FM with embedding dim ∈ {8, 16} — typical of prior NFM work — would underfit. The Phase 3C FM should start at dim ≈ 32–64 and sweep upward.

**Phase 3B verdict:** offensive pair synergy has extrapolable low-rank embedding structure — the dream-use-case property, in principle, exists. Defensive pair synergy does not. **Phase 3C (FM / bilinear under the harness) is motivated, offense-only.** An asymmetric architecture (offense = factorized embedding, defense = additive-only) may outperform a symmetric FM.

#### Phase 3C — results (full corpus, 23 seasons, 5.5M possessions)

Implemented in `experiments/fm.py` (shared-embedding FM using the `0.5·(‖Σe_i‖² − Σ‖e_i‖²)` identity for within-side pair sums) and `experiments/models.py::FactorizationMachine`. Staged on the same EB shared-α baseline used in Phase 3A and 3B. Offense-only per Phase 3B finding. Training: Adam, lr=3e-3, batch=16384, 30 epochs, OOV row pinned to zero. Grid: `dim ∈ {32, 64}`, `weight_decay ∈ {3e-4, 1e-3, 3e-3}`. 5 rolling-origin folds.

Paired-fold Δr²_over_ridge vs `eb_ridge_shared`:

| Config | slice `all` | slice `novel_off5` | slice `novel_def5` |
|---|---|---|---|
| fm_d32_wd3e-4 | −0.000018 (t=−1.19) | −0.000043 (t=−0.50) | +0.000029 (t=+0.36) |
| **fm_d32_wd1e-3** | **+0.000001 (t=+0.08)** | **+0.000003 (t=+0.30)** | **+0.000018 (t=+1.50)** |
| fm_d32_wd3e-3 | −0.000001 (t=−1.38) | −0.000001 (t=−1.11) | −0.000000 (t=−0.28) |
| fm_d64_wd3e-4 | −0.000103 (t=−1.02) | −0.000133 (t=−1.66) | +0.000046 (t=+0.35) |
| fm_d64_wd1e-3 | −0.000037 (t=−1.32) | −0.000018 (t=−1.29) | +0.000014 (t=+0.71) |
| fm_d64_wd3e-3 | −0.000001 (t=−0.78) | −0.000001 (t=−0.56) | +0.000001 (t=+0.65) |

**Headline: null result. No configuration beats EB additive on any slice at |t| > 2.**

Training-dynamics diagnostic is the more interesting output. Across every (dim, wd) × fold combination:

- `emb_off_rms` stayed in the band **0.0005 – 0.008** (initialization: 0.01). Embeddings never escape the vicinity of zero.
- `init_train_loss` ≈ `final_train_loss` to the 4th–5th decimal. The FM contributes essentially nothing to the training fit either.
- Per-possession MSE on test differs from EB additive by O(10⁻⁵).

**Interpretation — why per-possession SGD does not recover the Phase 3B signal.**
Possession-level residuals have variance σ² ≈ 1.27; a pair's contribution to any single possession is O(0.01–0.05). Per-possession gradient SNR on any individual embedding is ~1:100 at best. Adam's mini-batch estimate averages that noise down but not to the level where the pair-level signal (which Phase 3B does see, at ~15σ) dominates the per-step gradient. Phase 3B's SVD works because it **first averages** possession residuals onto pairs (SNR gain ≈ √n_cooccur ≈ 30–50 on well-observed pairs) and **then** does linear algebra on the pair-level matrix. The FM as formulated here trains on the unaggregated possession residuals, where the SNR lift from aggregation is lost.

**Key findings:**

1. **The FM architecture is capable of representing the Phase 3B structure, but possession-level SGD does not find it.** This is a training-objective problem, not an architectural one. The same embedding space that succeeds under SVD of the pair-mean-residual matrix fails under mini-batch Adam on raw residuals.
2. **Weight decay sweep is one-sided:** low wd (3e-4) mildly hurts `novel_off5`, high wd (3e-3) ties EB (because embeddings are crushed to zero), middle wd (1e-3) is a perfect tie — precisely because the embeddings stay near init.
3. **Larger dim makes things worse at fixed wd.** fm_d64 wd=3e-4 is the worst config (t=−1.66 on novel_off5). More parameters fit more noise without finding more signal.
4. **Phase 3A and Phase 3C are nearly indistinguishable null results** against the dream use case. Phase 3A cannot extrapolate by construction; Phase 3C can in principle, but doesn't in practice under this training recipe.

**Phase 3C verdict:** the per-possession-MSE + SGD + generic-weight-decay formulation of the FM is not the right implementation of the Phase 3B signal. The productive next step is **not** hyperparameter tuning or larger dim — it is changing the training objective to match the signal, either by (a) fitting the FM directly on pair-level mean residuals (`min_{E} ‖Ŝ − E Eᵀ‖²` with occurrence weights), (b) warm-starting E from the Phase 3B SVD factors and evaluating as-is under the harness to see whether the pair-level signal even *translates* to possession-level prediction, or (c) both. Proposed as Phase 3C-v2 in §7.

#### Phase 3C-v2 — results (full corpus, 23 seasons, 5.5M possessions)

Design: `experiments/svd_plug.py`, `experiments/run_svd_plug.py`, `experiments/models.py::SVDPairPredictor`. Fit EB additive, compute training residuals, build the offensive pair-mean-residual matrix Ŝ (pairs with ≥ 40 co-occurrences), take the truncated rank-k SVD of Ŝ, then score each possession as

```
pred_n = EB_additive(x_n) + α · Σ_{(i,j) in 10 offensive pairs of n} Ŝ_k[i, j]
```

with α fit by OLS through the origin on training residuals. Rank sweep k ∈ {16, 32, 64, 128}, 5 rolling folds, offense-only per Phase 3B.

**Paired Δr²_over_ridge vs EBRidge** (5 folds; t-stat in parens):

| k | all | novel_off5 | novel_def5 | novel_10 |
|---|---|---|---|---|
| 16  | −0.000041 (t=−0.25) | +0.000045 (t=+0.23) | +0.000030 (t=+0.13) | −0.000031 (t=−0.18) |
| 32  | −0.000147 (t=−0.47) | −0.000141 (t=−0.51) | +0.000031 (t=+0.07) | −0.000131 (t=−0.41) |
| 64  | −0.000447 (t=−1.11) | −0.000553 (t=−1.52) | −0.000221 (t=−0.35) | −0.000441 (t=−1.05) |
| 128 | −0.001125 (t=−2.11) | **−0.001654 (t=−3.50)** | −0.000945 (t=−1.07) | −0.001124 (t=−2.01) |

**Headline: null-to-negative.** No rank beats EBRidge at |t|>2 in the positive direction; k=128 — the rank Phase 3B identified as optimal for pair-level novel-generalization — *hurts* `novel_off5` at t=−3.50.

Diagnostic pattern (consistent across all 5 folds):
- Training RSS monotonically improves with k (k=16: Δ≈−2.5k; k=128: Δ≈−12k out of ~7.0M, ≈0.18% fit).
- OLS α ≈ 0.52–0.60 at k=16, ≈0.49 at k=128. OLS consistently shrinks the plug-in below unit scale — the per-possession prediction carries more variance than signal and wants to be dampened.
- `frac_energy_off` is 5.8% at k=16 and 32.6% at k=128. Ŝ's effective rank across the 23-season player universe (~1200 players clearing T=40) is much higher than Phase 3B's per-half 600-player rank, so the same k captures less energy here.
- Train improves, test degrades, monotonically with k. Classic overfit in the denoising step.

**Key findings:**

1. **Phase 3B's pair-level signal does not translate to per-possession MSE.** Rank-128 predicts held-out pair entries at r=+0.029 on `Ŝ_B`, but summing 10 such estimates per possession injects more variance than signal — `novel_off5` is actively hurt at k=128 (Δ=−0.0017, t=−3.50).
2. **The pencil estimate is saturated.** Per-pair correlation of 0.029 implies per-possession r² gain ≲ 10⁻⁴ under optimistic independence of pair synergies. Empirically the best-case observation (k=16) is Δ=+0.000045 on `novel_off5` — matching the order of magnitude, and well below 5-fold noise.
3. **Low rank is where "no harm" lives, not "signal".** k=16 captures ~6% of Frobenius energy, yields near-zero training fit *and* near-zero test delta. The plug-in effectively becomes EB.
4. **Consistent with Phase 3C (SGD), via a different route.** Two independent implementations — possession-level SGD (3C) and pair-level SVD + plug-in (3C-v2) — both fail to convert Phase 3B's structure into harness gains. The bottleneck is the pair-to-possession translation ceiling, not the optimizer.

**Phase 3C-v2 verdict:** the unweighted-SVD plug-in cannot translate Phase 3B's identified structure into per-possession harness gains. This is a sharp negative result about the dream-use-case implication of Phase 3B: the rank-k low-rank structure in Ŝ is real, but its magnitude is too small to move possession-level MSE at this corpus size. Phase 3B's 15σ is a structural claim, not a predictive one.

One related direction within the same class: **weighted low-rank approximation of Ŝ** (occurrence-weighted `‖Ŝ − EEᵀ‖²` via ALS). Weights rare-pair estimates by their precision, which unweighted SVD does not. Expected ceiling is similar — still bounded by the Phase 3B-scale pair-level signal — but it could shift the ceiling from not-reachable to marginally-reachable. Listed as Phase 3C-v3 in §7.

### Phase 4 — Denoised-target curriculum (null by construction for linear models)

Design (`experiments/denoise.py`, `experiments/run_denoise.py`, `experiments/models.py::DenoisedTargetWrapper`): for each training possession, group by unique 10-man lineup `g`; replace `points_scored_n` with `b_n + r_hat_g` where `b_n` is the detrender baseline, `r_hat_g = r_bar_g · n_g/(n_g + α_d)`, and `r_bar_g` is the within-group mean of detrended residuals. Evaluate on raw test possessions.

**Phase 4 — results (5-season smoke, AdditiveRidge(α=10000) inner)**

| α_denoise | Δ vs raw ridge (novel_off5) | t |
|---|---|---|
| 0 | −0.000000 | −0.14 |
| 0.1 | −0.000030 | −2.72 |
| 1 | −0.000262 | −2.82 |
| 5 | −0.000869 | −3.17 |
| 11.8 (EB-optimal) | −0.001332 | −3.41 |
| 20 | −0.001604 | −3.55 |

α_denoise = 0 reproduces raw ridge to within evaluation noise (Δ=−0.0000, t=−0.14), and every α_denoise > 0 hurts monotonically. The match at α_d=0 is *approximate, not exact*: `DenoisedTargetWrapper` rewrites `train_df["points_scored"]` with `b + r_bar_g[groups]` and the inner `AdditiveRidge` then fits its own detrender on this modified target, which produces a per-(season,week) baseline subtly different from the original `b`. Because `mean(r_bar_g[groups] | (s,w)) ≈ 0` for lineup10 grouping (most 10-mans appear in a single (s,w) bucket), the discrepancy is below the t-test resolution at α_d=0 — but it explains why Δ is "essentially zero" rather than literally zero.

**Why Phase 4 with a linear inner is null by construction.** At fixed ridge α and a *fixed* baseline, the ridge minimizer depends on the target only through `X'(target − baseline)`. With the lineup10 grouping, `X_n` is identical for all possessions in a lineup, so

```
X'(y_raw − b)        = Σ_g X_g · n_g · r_bar_g
X'(y_denoised − b)   = Σ_g X_g · n_g · s_g · r_bar_g  where  s_g = n_g/(n_g + α_d)
```

At α_d = 0, `s_g ≡ 1` and the two right-hand sides are identical (modulo the small detrender-refit drift noted above) → essentially identical ridge fit. At any α_d > 0, every per-lineup contribution is multiplied by `s_g < 1`, biasing every ridge coefficient toward 0 in proportion to lineup rarity. The bias monotonically grows with α_d, and the test MSE reflects that bias directly. There is no regime in which lineup-level target shrinkage helps a linear inner; the EB-optimal α_d is a noise-minimization criterion that does not align with the ridge β minimizer.

The `EBRidge` inner produced an additional independent failure mode in earlier smoke runs: MacKay's α auto-tune saw the ~3× lower target variance of the smoothed target and *reduced* its own regularization, overfitting further. Decoupling that path with `AdditiveRidge(α=10000)` isolates the structural bias, which is what the table above shows.

**Phase 4 + FM (gradient-SNR test) was not run.** Pencil estimate: lineup10 grouping reduces target variance by ≈3.6× → gradient SNR improves ≈1.9×. Phase 3C found the SNR gap to be ≈30–50×, so even with denoised target the FM SGD is unlikely to clear the gap. Documenting the linear result and skipping FM keeps Phase 4 compact.

**Phase 4 verdict:** the denoised-target curriculum, in the linear-inner formulation that was tractable to implement, is **null by construction** — the framework collapses to raw ridge at α_d=0 and biases against it for any positive α_d. The lever does not exist for additive models. A non-linear inner *might* benefit from the SNR reduction, but the size of the SNR gap makes it implausible at this corpus size.

### Phase 5 — Set-attention over offensive players, on EB additive (v1: null)

**Design** (`experiments/attn.py`, `experiments/run_attn.py`, `experiments/models.py::SetAttentionPredictor`).

Architecture:
- `emb_off`: (n_players, d), warm-started per fold from rank-d SVD of the training-fold offensive pair-mean-residual matrix Ŝ_off (Phase 3B's matrix; embedding row for player i is `U[i, :d] · √diag(Σ[:d])`).
- For each possession with offensive 5 indices `off_idx`: 1-layer multi-head self-attention (4 heads, optional dropout) over the 5 offensive embeddings, mean-pool to scalar-per-possession, MLP head (`d → 4d → 1`), output added as a residual on top of EB additive.
- Defense participates only via the EB additive baseline (per-player defensive coefficient). No defense embedding table in v1, since Phase 3B found defensive pair structure null.

Training:
- Stage 1 (`freeze_epochs`): emb_off frozen; train attention + head only via Adam on possession-level MSE of EB residuals. Protects the SVD warm-start from being destroyed by SGD instability — the gradient-SNR problem that killed Phase 3C.
- Stage 2 (`finetune_epochs`): unfreeze emb_off at `lr_stage2 = lr_stage1 / 10`.
- 5-season smoke found stage-2 finetune (i) hurts vs frozen-only on most configs and (ii) crushes embedding magnitude (RMS 0.025 → 0.001 in 5 epochs at full corpus). Frozen-only chosen for the canonical run.

**Methodology — multi-seed required.** Initial single-seed result (d=64, svd, seed=0, frozen, wd=2e-3) measured Δr²_over_ridge=+0.000070 on `novel_off5` with 5-fold paired t=+4.19 — apparently publishable. Re-running with seeds {0, 1, 2} aggregated to t=+0.52 (basically zero). Single-seed t-stats are unreliable at this signal scale — fold-pairing cancels data variance but not initialization variance, and expected effect (Phase 3B pencil ≈ 10⁻⁴ r²) is on the order of init-induced noise in attention parameters that barely move during training. All Phase 5+ comparisons must use 3+ seeds.

#### Phase 5 v1 — results (full corpus, 23 seasons, 5.5M possessions, frozen-only)

5-season smoke grid swept wd ∈ {1e-4, 3e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2}, dropout ∈ {0, 0.1, 0.2}, freeze ∈ {5+3, 8+0}, dim ∈ {32, 64, 128}, init ∈ {svd, random}, seeds ∈ {0, 1, 2}. Frozen-only at wd=2e-3, dp=0 was the seed-aggregated optimum on the smoke. Full corpus run: dim=64, depth=1, heads=4, frozen-only 8 epochs, wd=2e-3, dp=0, init ∈ {svd, random} × seed ∈ {0, 1, 2} = 6 configs.

**Paired-fold Δr²_over_ridge vs eb_ridge_shared, seed-aggregated (3 seeds × 5 folds = 15 paired observations per cell):**

| init  | all                         | novel_off5                   | novel_def5                   |
|-------|-----------------------------|------------------------------|------------------------------|
| svd   | +0.000005 (t=+1.08, sem=5e-6) | −0.000002 (t=−0.15, sem=2e-5) | +0.000015 (t=+1.27, sem=1e-5) |
| rand  | +0.000005 (t=+1.08, sem=5e-6) | −0.000002 (t=−0.15, sem=2e-5) | +0.000015 (t=+1.28, sem=1e-5) |

**Headline: definitive null.** No slice crosses |t|>2 in the positive direction. Critically, **svd-init and random-init produce statistically identical results to 6 decimal places** — the per-cell means match exactly, sems match exactly. This means the attention head learns to produce essentially the same correction over EB regardless of which embeddings it attends to. The SVD warm-start is not the lever; the architecture itself is not finding signal.

The full-corpus per-fold sem (~10⁻⁵) is ~5× tighter than 5-season (~5×10⁻⁵), so the null is much more decisive — the model and the data are well-trained, there's just no signal to find at the harness scale.

**Key findings:**

1. **Set-attention over Phase-3B-warm-started offensive embeddings adds nothing measurable to EB additive.** The Phase 3 ceiling holds: pair-level offensive structure that's identifiable on the pair-mean-residual matrix does not translate to per-possession MSE gains via attention any more than via SGD-FM (3C) or SVD-plug (3C-v2).
2. **SVD warm-start is not informative at this corpus scale.** Random and SVD init are indistinguishable at the harness output. The attention head, trained for 8 epochs at lr=1e-3 with wd=2e-3, converges to essentially the same function regardless of input embedding structure.
3. **Single-seed results at this signal scale are unreliable.** Phase 5 v2 single-seed produced t=+4.19 that vanished to t=+0.52 across 3 seeds. Memory `feedback_seeds_for_sgd.md` records this as a project-wide methodological constraint.
4. **Frozen-only beats finetune at this scale.** Stage-2 finetuning crushes embedding magnitude under Adam+wd at the realistic regularization levels and adds no test-set value over frozen-only. (Frozen-only also matches "linear probe of SVD-init", which is precisely Phase 3C-v2 dressed in attention — and 3C-v2 was already null.)

**Phase 5 v1 verdict:** the canonical single-side, single-layer set-attention model with SVD warm-start, on top of EB additive, produces a clean null at full corpus scale. The pair-to-possession translation ceiling identified in Phase 3 holds across this architecture too. **Three independent attempts** — possession-level SGD on FM (3C), pair-level SVD plug-in (3C-v2), and now set-attention with SVD-initialized embeddings (5 v1) — all fail to convert Phase 3B's identified rank-k offensive pair structure into harness gains on `novel_off5`.

#### Phase 5 v2 — three architectural variants (all null/marginal)

If non-pairwise structure (3-way, 4-way interactions, or matchup-specific contributions) exists at this corpus size, v1's single-layer offense-only self-attention is too narrow to exploit it. Three v2 architectures were specified, three were run.

**v2c1 — deeper attention (L=2):** offense-only self-attention, two stacked layers, otherwise identical to v1. **Null.** Doubling depth produced no measurable improvement on `novel_off5`; the second attention layer didn't pull additional structure out of the warm-started embeddings beyond what v1's single layer already failed to find.

**v2c3 — joint fine-tune with very low LR, zero wd on emb_off:** designed to preserve the SVD warm-start through stage-2 fine-tuning (v1 fine-tune crushed embedding RMS under Adam + wd=2e-3). **Marginal.** Embedding magnitude was preserved as intended, but the harness-level Δ vs EB stayed within fold-paired noise on `novel_off5`. Fine-tuning is not the lever; the warm-start itself was already non-informative (v1 svd vs random matched to 6 decimals).

**v2c2 — cross-attention from offense to defense:** Q = E_off, K=V = E_def. emb_off SVD-warmed (rank-d of training Ŝ_off), emb_def random init. dim=64, depth=1, heads=4, mp=0.2, dp=0.3. Best-val checkpointing on chronological 10% val (`train_attn` wired in Task 53). LR sweep (lr_stage2 ∈ {3e-5, 1e-5}, freeze=20, finetune=50, wd=0, 3 seeds × 5 folds × 2 LRs = 30 fits, 5-season smoke).

| | all | novel_off5 |
|---|---|---|
| eb_ridge_shared | +0.000173 | +0.000339 |
| attn mean (3 seeds) | +0.000001 | −0.000013 |
| **Δ vs EB** | **−0.000172** | **−0.000352** |

**Null — and the LR sweep was a no-op.** lr_stage2 ∈ {3e-5, 1e-5} produced *identical* aggregate r²_over_ridge to 5+ decimals. Reason: across all 30 fits, the best-val epoch landed in stage 1 (freeze, ep ≤ 9), so lr_stage2 never got to matter. Best-val epoch values for lr=1e-5: s0 [3,3,4,4,5], s1 [4,4,8,4,5], s2 [9,9,6,4,4]. Stage 1 trains head + attention only at the default lr_stage1=1e-3 regardless of the lr_stage2 setting — so the chosen checkpoint is identical across the two runs.

**Per-fold val/test instability — the val-noise diagnostic.** Per-fold `best_val_test_loss` from the lr=1e-5 trace ranges 1.400 to 1.432 — a 0.03 spread, **300× the actual signal scale (~10⁻⁴)**. Some folds (s0 fold 2) picked best-val checkpoints that test catastrophically; others picked sane ones. Same architecture, same data scale — the val sem is dominating the selection.

**Why val-noise dominates** (now codified in `feedback_val_noise_floor.md` memory). val_n ≈ 25k (10% of ~250k 5-season train), σ² ≈ 1.4 → val_sem ≈ √(2·1.96/25000) ≈ 0.0125. Epoch-to-epoch val MSE differences are ~10⁻⁴. So sem is ~125× signal — best-val selection is picking noise. At full-corpus scale (val_n ≈ 300k) sem drops to ~0.0036 — still ~30× signal. Best-val checkpointing is a structurally bad selection mechanism at this signal regime regardless of LR/wd/architecture choices.

**Phase 5 v2 verdict.** Three independent v2 architectures (deeper, careful fine-tune, cross-attention) all null or marginal. Combined with v1's decisive null and the val-noise diagnostic, this closes the architectural-search line of the project: **set-attention over Phase-3B-warm-started embeddings cannot translate the offensive pair signal into per-possession harness gains, regardless of layer depth, fine-tune protocol, or whether defense participates as a query target.**

Several follow-up runs at lr=7e-5 with no freeze epochs and various weight-decay schedules were attempted but killed early before completion; given the val-noise floor analysis above, completing them would not have changed the conclusion.

### Phase 5 v3 — two-stream asymmetric attention with bilinear interaction head

**Architecture (`experiments/models.py::TwoStreamAttention`).** Two independent self-attention stacks (depth_off, depth_def) over offensive and defensive 5-player sets, each pooled by PMA, fed through a bilinear interaction head:
```
o_vec = PMA(self_attn_off(emb_off[off_idx]))
d_vec = PMA(self_attn_def(emb_def[def_idx]))
pred  = head([o_vec, d_vec, o_vec ⊙ d_vec])
```
The elementwise product `o_vec ⊙ d_vec` is the bilinear lever — if any off-def alignment is identifiable in a coordinate system shared by both streams, the head can route it. v1/v2 had emb_def random; v3 added `--init-def svd` to give defense a Phase-3B-style warm-start from rank-d SVD of Ŝ_def, so the bilinear term wouldn't start at zero.

**Cross-matrix identifiability probe (`experiments/run_cross_probe.py`).** Before chasing v3 nulls, the data-side question was settled: does the off-def cross matrix R[i,j] = E[r | i ∈ offense ∧ j ∈ defense] have a rank-k SVD that generalizes across game-disjoint halves? **Null.** At 5-season corpus (1.26M poss, 1030 players, min_cooccur=20, 3 seeds), pearson_novel ≈ +0.002 at rank 1 vs null −0.002 (~4×10⁻³ edge, within seed noise); ranks ≥ 16 go negative. Compare Phase 3B offense within-side at rank 128: weighted r ≈ +0.029 (~15σ). **Defensive identity is not low-rank-identifiable at this n in any matrix we know how to construct** — within-side def (Phase 3B), cross (this probe), or any combination thereof. Codified in `phase5_cross_init_null.md`.

**5-season runs (3 seeds × 5 folds, EB ridge baseline = +0.000151 r²_over_ridge on `all` slice):**

| Run | Schedule | def init | freeze sym | Mean Δ vs EB ridge (`all`) |
|---|---|---|---|---|
| v3 wd=1e-3 highreg noval | 15+0 | random | def free | def_rms collapsed to 0 by ep5 → bilinear term zeroed; null |
| v3 wd=1e-4 dsvd | 15+0 | svd (Ŝ_def) | def free | **+0.000011** (within seed std ±0.000017) |
| v3 wd=1e-4 dsvd freezedef | 15+0 | svd | def frozen | tracks dsvd-free run; emb_def constant 0.0338 |
| v3 d=4 wd=1e-4 dsvd | 20+5 finetune | svd | def frozen | partial; fold 0 mean +0.000133, larger seed variance |
| v3 d=2 ebshr | 15+0 | svd-EBshr | def frozen | tracks unshrunk d=2 to ±5×10⁻⁵ |
| v3 d=2 ebshr long | 60+0 | svd-EBshr | def frozen | partial folds 0–2 mean +0.000093 vs short-freeze same folds +0.000051 (Δ ≈ +0.000042 from longer training, within seed std) |
| v3 d=4 ebshr long | 60+0 | svd-EBshr | def frozen | partial fold 0 only (+0.000180 across 2 seeds) |

**EB shrinkage of pair-mean residuals before SVD** (`svd_plug.py::_eb_shrink_synergy_inplace_copy`, default-on). Rationale: unweighted SVD of Ŝ treats a pair at n=20 (SE σ/√20 ≈ 0.26) the same as a pair at n=5000, so noisy rare-pair entries can pollute top singular directions. Shrink each entry by `n / (n + λ)` with λ = median(n_cooccur). For 5-season offense: median ≈ 311 → shrink @ n=20 = 0.060 (heavy damp), @ median = 0.500, @ n=1000 = 0.762 (mostly pass-through). Embedding rms post-shrinkage drops 0.034 → 0.019 but per-fold harness scores match unshrunk d=2 to within 5×10⁻⁵ — the SVD's top singular directions were robust to the noise the shrinkage targets, at least at these ranks.

A first attempt used data-estimated τ² via moment-matching (Var(s) − E[σ²/n] for τ²); for our regime the estimator returns τ² ≈ 0 because per-pair signal-to-noise is far below 1 (Phase 3B's rank-128 r=0.029 means signal at the entry level is ~50× smaller than noise — only recoverable via low-rank averaging). Mathematically correct but collapses the matrix to zero, destroying the cross-pair signal SVD pools to recover. The `λ = median(n)` heuristic preserves SVD's pooling capacity while damping the noisiest entries.

**Long-freeze diagnostic.** Per-epoch test_mse averaged across all 15 fits of d=2 unshrunk (centered within fit to remove fold offset):

| epoch | centered test_mse | sem |
|---|---|---|
| 1 | +0.000139 | 0.000096 |
| 5 | −0.000020 | 0.000047 |
| 10 | −0.000001 | 0.000037 |
| 13 | −0.000075 | 0.000024 |
| 15 | −0.000080 | 0.000022 |

Test MSE was still drifting down at the original 15-epoch stopping point — the late-freeze drop from ep10 → ep15 (Δ = −0.000079) is comparable to the entire effect we chase. Extending to 60 freeze epochs picked up ≈ +0.000042 r² on folds 0–2 (within seed std). Real but small: the architecture asymptote is about 4× the previous stopping point, still nowhere near the level needed to break out of EB-ridge-equivalent.

**Phase 5 v3 verdict.** Two-stream + bilinear + every defensive lever we can construct (random, SVD, EB-shrunk SVD, frozen, free, depth 2, depth 4, freeze 15, freeze 60, finetune 0/5) hits the same ceiling as v1 and v2: Δ ≈ 10⁻⁴ r²_over_ridge, within fold/seed noise. The cross-matrix identifiability null provides the *data-side* explanation: defensive identity is not low-rank-identifiable at 5-season n, so no architecture above EB-additive can extract it.

### Phase 6 — Final null synthesis (the trigger has fired)

The "if v2 also lands null, the writeup is the negative empirical claim" trigger from `phase5_v1_null.md` has fired. The project's main contribution is now the empirical claim:

> *With 23 NBA seasons (≈5.5M possessions) restricted to the 10-player-only input, the identifiable non-additive lineup signal remains below the level at which the architectures we tested (FM, weighted SVD plug-in, set-attention v1 with SVD warm-start, deeper self-attention, cross-attention to defense, two-stream attention v3 with bilinear interaction head and SVD def warm-start) can exploit for per-possession prediction. Phase 3B identifies generalizable rank-k offensive pair structure on the pair-mean residual matrix, but the per-pair correlation r ≈ 0.029 implies a per-possession ceiling of ≲ 10⁻⁴ r²_over_ridge — within fold-paired noise of the EB additive baseline. Six independent estimators all hit this ceiling. Defensive identity is additionally null at all matrix probes (Phase 3B within-side def, Phase 5 v3 off×def cross), explaining why no architecture lift is possible on the def stream specifically.*

That claim is publishable as a negative result with: the scaling curve from Phase 1, the rank-k structure from 3B, the per-possession ceilings from 3C / 3C-v2 / 5 v1, and the v2 architectural-extension nulls. A val-noise-floor analysis (see `feedback_val_noise_floor.md`) is part of the methodological contribution: it shows that best-val checkpointing is structurally invalid at this signal regime, independent of architecture.

### Phase 6 — Repository consolidation

After the research question has a clean answer:

- Canonical pipeline lives in `experiments/` with: `data.py` (loader), `eval.py` (harness), `models/` (a small, curated registry), `run.py` (entry point).
- All superseded scripts move to `archive/` with a short `README.md` explaining what each was for.
- `RESEARCH_OVERVIEW.md` (this file) is kept current as the top-of-repo map.

---

## 7. Status and next action

**Completed:**

- **Phase 0** — harness in `experiments/` (data loader, splits, novel-lineup slicing, detrender, metrics, reference-model orchestration). All models now report the same six numbers on the same five slices.
- **Phase 1** — identifiability scaling curve (`experiments/identifiability.py`, `run_identifiability.py`). At 20-season scale: teammate-pair synergy is identifiable (weighted split-half r ≈ 0.10, rising with data); matchup-pair synergy is **not** identifiable at any tested scale (r ≤ 0.02). This reframes Phase 5: raw-ID matchup learning is closed; embedding-space matchup learning remains open.
- **Phase 2** — empirical-Bayes ridge with shared and with off/def-split priors (`experiments/eb.py`, `experiments/run_eb.py`). Result: pooling is not the lever. Full corpus gain over ridge α=10000 is r²_over_ridge ≈ +0.00008 and all of it comes from α-tuning, not from the off/def split. See §Phase 2 — results above.
- **Phase 3A** — explicit teammate-pair ridge (`experiments/pairs.py`, `experiments/run_pairs.py`, `experiments/models.py::PairRidge`). Result: weak positive direction at the grid boundary (α=15000), largest on `novel_def5`, all within 5-fold paired-difference noise. Interpolation-only architecture; does not serve the dream use case. See §Phase 3A — results above.
- **Phase 3B** — low-rank / embedding identifiability probe (`experiments/embedding_probe.py`, `experiments/run_embedding_probe.py`). **Offense: positive result.** Rank-128 SVD of `Ŝ_A` predicts held-out-in-A pair entries in `Ŝ_B` at weighted r = +0.029, ~15σ above the null permutation baseline. Defense: flat at every rank. Offensive pair synergy has extrapolable low-rank embedding structure; defensive pair synergy does not. See §Phase 3B — results above.
- **Phase 3C** — factorization machine with offense-only embeddings, staged on EB additive (`experiments/fm.py`, `experiments/run_fm.py`, `experiments/models.py::FactorizationMachine`). Grid: `dim ∈ {32, 64} × wd ∈ {3e-4, 1e-3, 3e-3}`, 30 epochs, Adam, possession-level MSE on EB residuals. **Null result.** No config beats EB additive on any slice at |t| > 2. Training diagnostic explains why: embeddings barely leave initialization (RMS 0.0005–0.008), train loss is flat. Per-possession gradient SNR is too low for SGD to recover the pair-level signal that Phase 3B's SVD finds after averaging residuals onto pairs. See §Phase 3C — results above.
- **Phase 3C-v2** — SVD-plug-in predictor under the harness (`experiments/svd_plug.py`, `experiments/run_svd_plug.py`, `experiments/models.py::SVDPairPredictor`). Rank sweep k ∈ {16, 32, 64, 128}, min_cooccur=40, offense-only, OLS-fit α. **Null-to-negative result.** k=16 is within noise on all slices; k=128 — the Phase 3B-optimal rank — is Δ=−0.0017 on `novel_off5` at t=−3.50. Training RSS monotonically improves with k while test MSE monotonically degrades: classic overfit in the denoising step. Phase 3B's pair-level structure is real but too small to translate to per-possession MSE at this corpus size. See §Phase 3C-v2 — results above.
- **Phase 4** — denoised-target curriculum, linear inner (`experiments/denoise.py`, `experiments/run_denoise.py`, `experiments/models.py::DenoisedTargetWrapper`). 5-season smoke with `AdditiveRidge(α=10000)` inner. **Null by construction.** At α_d=0 the wrapper reproduces raw ridge exactly (Δ=−0.0000); every positive α_d biases ridge β toward 0 monotonically. Mathematical reason: at fixed ridge α, X'(target − baseline) is a per-lineup-weighted sum of `s_g · r_bar_g` with `s_g = n_g/(n_g+α_d)`, and shrinking `s_g < 1` shrinks every coefficient. Phase 4+FM not run; pencil estimate is that the ≈3.6× target-variance reduction yields ≈1.9× SGD gradient SNR improvement, against a 30–50× SNR gap from Phase 3C — implausible to clear. See §Phase 4 — results above.
- **Phase 5 v1** — set-attention over offensive players, on EB additive (`experiments/attn.py`, `experiments/run_attn.py`, `experiments/models.py::SetAttentionPredictor`). Single self-attention layer (4 heads, d=64), mean-pool, MLP head; offensive embedding warm-started per fold from rank-d SVD of Ŝ_off. Frozen-only training (8 epochs, Adam, wd=2e-3). Full corpus, init ∈ {svd, random} × seed ∈ {0, 1, 2} × 5 folds = 30 paired observations per init. **Definitive null.** novel_off5 Δ = −0.000002, t = −0.15 (svd init); novel_off5 Δ = −0.000002, t = −0.15 (random init). The two cells match to 6+ decimal places — the attention head produces essentially identical outputs regardless of input embedding structure. SVD warm-start is not the lever; the architecture itself doesn't find signal at this corpus scale. See §Phase 5 — results above.
- **Phase 5 v2** — three architectural variants (`experiments/attn.py` with `--depth`, `--use-defense`, plus stage-2 fine-tune knobs; `phase5_v2c2_null.md` memory). v2c1 (deeper self-attention, L=2): null. v2c3 (joint fine-tune with very low LR, zero wd on emb_off, preserves SVD warm-start magnitude): marginal. v2c2 (cross-attention Q=E_off, K=V=E_def with emb_def random init, best-val checkpointing wired in via Task 53): **null at 5-season smoke** — mean attn worse than EB by ~10⁻⁴ on `novel_off5`; the LR sweep (lr_stage2 ∈ {3e-5, 1e-5}) produced identical aggregate r² to 5+ decimals because best-val locked into stage-1 freeze (ep ≤ 9) for all 30 fits, making lr_stage2 a no-op. Per-fold `best_val_test_loss` ranges 1.400 to 1.432 — a 0.03 spread, ~300× the signal scale, exposing val-noise dominance of best-val selection at this regime. See §Phase 5 v2 — results above.
- **Phase 5 v3** — two-stream asymmetric attention + bilinear interaction head, with `--init-def svd` for defensive warm-start (`experiments/models.py::TwoStreamAttention`, `attn.py` v3 branch, `phase5_cross_init_null.md` memory). Combined with the **off-def cross-matrix identifiability probe** (`run_cross_probe.py`): rank-k SVD of R[i,j]=E[r|i_off ∧ j_def] is **null** at 5-season n (pearson_novel ≈ +0.002 vs null −0.002, within seed noise). v3 harness runs across all defensive levers — random/svd/EB-shrunk-svd init, free/frozen def in stage-1, depth 2/4, freeze 15/20/60, finetune 0/5 — all hit Δ ≈ 10⁻⁴ r²_over_ridge. The freeze-symmetry fix (freeze emb_def whenever it has a warm-start, not just when arch ≠ v3) was applied. EB shrinkage of pair-mean residuals before SVD (`svd_plug.py::build_svd_embedding_init` default `eb_shrink=True`) damps rare-pair noise but doesn't change the harness ceiling. Long-freeze diagnostic: test_mse was still drifting at the original 15-epoch stopping point (centered Δ −0.000079 between ep10 and ep15, ~3σ); extending to 60 freeze epochs picked up ≈ +0.000042 r² on folds 0–2 (within seed std). See §Phase 5 v3 — results above.

**Phases 3, 4, and 5 (v1 + v2 + v3) are closed.** Six independent implementations (FM under per-possession SGD; pair-level SVD plug-in; denoised-target curriculum with linear inner; v1 single-layer set-attention with SVD-init; v2c1 deeper self-attention; v2c2 cross-attention to defense; v3 two-stream + bilinear with def warm-start variants) fail to convert Phase 3B's identified rank-k offensive pair structure into harness gains on `novel_off5`. The pair-to-possession translation ceiling is ≲ 10⁻⁴ r² across all of them — of the same order as EB-over-ridge. Defensive identity is additionally null at every matrix-level probe (Phase 3B within-side def, Phase 5 cross-matrix off×def), so the def stream of any architecture is fundamentally constrained by data, not capacity.

**Two methodological constraints codified during Phase 5:**
1. *Multi-seed required for SGD-trained models at this signal scale.* Single-seed Phase 5 v2 produced t=+4.19 on novel_off5 that vanished to t=+0.52 across 3 seeds — fold-pairing cancels data variance but not initialization variance. Recorded in `feedback_seeds_for_sgd.md`.
2. *Best-val checkpointing is structurally invalid at this signal regime.* val sem (≈0.0125 at val_n=25k, ≈0.0036 at full-corpus val_n=300k) is 30–125× the effect size we chase (~10⁻⁴), so best-val epoch selection is noise-dominated. Per-fold best_val_test_loss spread of 0.03 in Phase 5 v2c2 is direct evidence. Recorded in `feedback_val_noise_floor.md`.

**Phase 6 — final null writeup is the next move.** The trigger from `phase5_v1_null.md` has fired (two of three v2 variants null, one marginal). The project deliverable is the negative empirical claim in §Phase 6 above, supported by Phase 1's scaling curve, Phase 3B's rank-128 structural result, and the per-possession ceilings from 3C / 3C-v2 / 5 v1 / 5 v2.

Phase 2B hierarchical pooling, raw-ID matchup terms, and Phase 3C-v3 (weighted ALS) remain de-prioritized — none of them attack the pair-to-possession translation ceiling that all five Phase 3+/5 estimators have hit.

---

## Appendix — key files for orientation

- `tables.sql` — schema.
- `predict_possessions_baselines.ipynb` — canonical ridge baseline.
- `predict_possessions_smoothing.ipynb` — most recent work (Feb 2025): `NNPredictor` with multiple embedding regularizers + lineup aggregation.
- `possession_vs_lineup_comparison.py` + `multisplit_grid_search.py` — prior attempts at the head-to-head that Phase 4 finishes.
- `possession_level_grid_search.csv`, `lineup_level_grid_search.csv`, `nfm_optimization_results.csv` — results of the last serious grid searches.
- `explore_seasonal.py` — seasonal detrend derivation.
- `Basketball Model Research.md` — raw chat-log history; useful as provenance, not as summary.

---

## 8. Phase 8 — measuring the ceiling (2026-08-28/29)

Every phase above ends at the same number: Δr² ≈ 10⁻⁴ over EB additive, on every
basis, from six independent estimators. Phase 8 asked the question none of them
asked — **how much non-additive lineup signal exists at all** — and the answer
reframes the whole record: 10⁻⁴ is not where the models fail, it is roughly
where the signal ends.

### 8.1 The measurement (`experiments/lineup_variance.py`)

Partition **games** four ways: F1, F2 to fit, E1, E2 to evaluate. Fit the
additive model separately on F1 and F2; score E1 with β₁ and E2 with β₂. Then
every term in the two lineup mean-residuals except the true lineup effect is a
function of a disjoint set of games, so `cov(m₁, m₂) = τ²_lineup`.

Two designs that look right and are not, both measured before settling on this
one: scoring both halves with one β biases the covariance **up** (shared
prediction error); scoring each half with the other's β biases it **down**
(β_B absorbed half B's noise, which returns in m_A with a minus sign —
measured ρ = −0.12). Split by game, not by possession, or the halves share the
opponent's game plan.

| grouping | ceiling Δr² | t over 5 seeds |
|---|---|---|
| offensive five | **+0.000256** | +4.3 |
| defensive five | **+0.000180** | +3.8 |
| team-season, offense | +0.000063 | +6.4 |
| team-season, defense | +0.000085 | +9.2 |

Controls that came back clean: **shrinkage** — τ² is 0.000328 / 0.000336 /
0.000400 at α = 10 / 300 / 3224, i.e. it *rises* ~22% with α, exactly as a
residual shrinkage bias would; the headline uses α=10 where that bias is
negligible — **deployment context** (residualising on season ×
score-margin × game-phase removes 7%), **lineup recurrence** (pairs appearing in
*more* distinct lineups replicate better, not worse).

Controls that bite, and shrink the number:

- **team scheme** — 25% of the offensive ceiling, **47%** of the defensive one,
  is at the (team, season) level, which no player-profile model can represent;
- **player-season main effects** — the additive baseline gives each player one
  coefficient for 25 seasons, and his season-specific form is shared by every
  lineup he appears in. Removing it cross-fit drops τ² by ~⅓;
- **persistence** — splitting the evaluation first-half-of-season → second-half
  instead of at random gives τ² = +0.000215 vs +0.000328, so ~65% survives
  three months.

**Net: the genuinely non-additive, forecastable lineup ceiling is ≈ +0.0001 r²,
against an additive model that explains ~0.002 over the mean.** Maximum
available improvement from all lineup structure is ~5% relative.

### 8.2 What reaches it (`experiments/basis_screen.py`, `pair_ceiling.py`)

`basis_screen.py` fits a basis at possession level *through* lineup sufficient
statistics — exact, not approximate — and reports Δr² in harness units in ~10
seconds. (It replaces `screen.py`, whose bootstrap understated uncertainty 13×.)

| basis | Δr² | % of ceiling | on NOVEL five-man sets |
|---|---|---|---|
| free PLAYER (2,370) | +0.000000 | 0% | — |
| free PAIR (66,737) | +0.000038 | 15% | +0.000026 |
| free TRIPLE (269,636) | +0.000026 | 10% | +0.000011 |
| PAIR + TRIPLE | +0.000052 | 20% | +0.000035 |
| free PLAYER-SEASON (11,523) | +0.000024 | 9% | +0.000023 |
| PLAYER-SEASON + PAIR | +0.000053 | 21% | **+0.000046** |
| free TEAM-SEASON (717) | +0.000024 | 10% | +0.000029 |
| free LINEUP (194,092) | +0.000001 | **0%** | 0 |
| profile bilinear, 10 dim | +0.000004 | 1% | — |

Four things follow.

1. **The effect is pairwise-plus and it extrapolates.** Free pairs beat the
   additive model on five-man sets never seen in training. Triples add ~5 more
   points, so it does not stop at pairs.
2. **The profile compression, not the pair basis, was the bottleneck.** Free
   pairs 15%, the 10-dim bilinear form 1%. This reverses the standing argument
   that "the pair basis is the wrong unit."
3. **Free lineup identity reaches 0%, and that is not evidence of absence.** A
   lineup averages ~23 possessions, so with σ²/τ² ≈ 3900 its reliability is
   ~0.6%. A saturated random effect is arithmetically incapable of reaching a
   ceiling that demonstrably exists. Had `run_lineup_identity.py` been used as
   the planned "decision gate", it would have returned ~0 and closed the project
   on a measurement error.
4. **Defense is a different animal.** The same decomposition on the defensive
   five: player-season +0.000020 (11%), **free PAIR +0.000000 (0%)**. Offensive
   pairs are worth 15% of their ceiling; defensive pairs are worth nothing.
   Together with the 47% team-scheme share, that is the cleanest available
   explanation of why every defensive interaction model in Phases 1/3B/5 died.

### 8.3 Why the embedding architectures failed (`experiments/pair_spectrum.py`)

Assemble the fitted free-pair effects into Θ and truncate to rank k. Top-10
eigenvalues hold 9.6% of ‖Θ‖²_F, top-50 32%, top-256 75%. Out-of-sample, rank 8
recovers 4% of the ceiling and **zero** on novel lineups; rank 256 is needed to
approach the untruncated free-pair model.

**Pair effects do not factor through a low-dimensional player embedding.** Every
architecture in Phases 3C and 5 — factorization machines, SVD warm-starts,
self- and cross-attention over d=64–128 embeddings — was compressing a matrix
that needs rank ~256, against the worst-SNR target of the eleven available.
Phase 3B's "rank-128 signal at 15σ" is consistent: real, and worth ~12% of the
ceiling, which is exactly the size of thing that vanishes in the harness.

Caveat: Θ is ridge-fitted and structurally zero for the 97.6% of player pairs
that never shared a floor, so its spectrum is biased toward high rank by
construction. The out-of-sample column is honest; "not low-rank" is a statement
about this estimate of Θ, not a theorem.

### 8.4 Synergy, finally isolated (`experiments/synergy_decomp.py`)

The mu_O block is `½(SS' − Σₖ zₖzₖ')`, whose second term is **additive in
players** — so a gain there is consistent with un-shrinking rather than synergy,
and the earlier `MAIN` control only removed the *linear* profile sum. Splitting
into separately-parameterised blocks — LIN (`S`), SELF (`Σₖ zₖzₖ'`, additive),
CROSS (`Σ_{i<j} z_i z_j'`, the only non-additive one) — makes `ALL − SELF` the
synergy estimate with un-shrinking removed. **Pooled over 30 folds across three
disjoint windows** (full corpus, ≤ 2023, ≤ 2022):

| contrast | `all` | novel_off5 | novel_10 |
|---|---|---|---|
| ALL over EB ridge | **+0.000106 (t=+4.47)** | +0.000143 (t=+3.08) | +0.000104 (t=+4.41) |
| **ALL over SELF — synergy** | **+0.000068 (t=+3.34)** | +0.000107 (t=+2.45) | +0.000066 (t=+3.27) |

Positive in all three windows: +0.000038 (t=+0.93) full corpus, +0.000067
(t=+2.02) ≤2022, +0.000098 (t=+3.10) ≤2023 — weakest on the full corpus, which
is the era pattern again. `basis_screen` on a random
split over the whole corpus puts CROSS-on-top at ~+0.000001, but restricted to
2013+ or 2018+ it gives +0.000027 to +0.000032 — the harness tests only the
final weeks of a modern season, so the full-corpus screen was diluting a
modern-era effect across 25 years. **The era-dependence itself is unexplained:**
neither era-z-scored profiles nor per-(player, season) profiles reproduce it on
the full corpus.

Separately, the replication settled the older question: **mu_D is dead** (pooled
t=+0.41 across two disjoint windows, against +2.47 on the single window that
produced it), so the interpretable `M_def` story — rorb×rorb redundancy,
Gobert+Mutombo as the worst pair — was told about noise.

### 8.5 The clock channel (`experiments/context.py`)

`data.py` never loaded `quarter` / `time_left_*`. Possession duration runs PPP
1.37 (0–4s) to 0.78 (24–30s), worth r² ≈ 0.018 — ten times the additive player
model. The honest between-lineup slope (cross-half, so the noises are
independent) is −0.0206 PPP/sec, barely attenuated from naive. Replacing each
possession's points by the league mean for its duration puts the clock-mediated
share of the non-additive lineup effect at **15%**, measured at t=+16.9 versus
+4.3 for the points channel — five times more reliable per lineup, but only a
sixth of the effect.

### 8.6 The combined model

Two gains, measured independently and shown not to subsume each other:

- **time-varying player coefficients** — free (player, season, side) effects on
  top of EB ridge, penalty pinned. Positive at every penalty tried, strongest
  where the *defensive* five is novel (t = +3.6 to +3.8), i.e. it pays most when
  the offensive lineup is familiar and what you need is this season's form;
- **the profile CROSS block** — synergy, which survives the time-varying
  baseline *unchanged* (+0.000038 on a static base, +0.000038 on a
  time-varying one, on the full-corpus window). It is not temporal
  misspecification wearing a profile.

Pooled over 30 folds and three disjoint windows:

| contrast | `all` | novel_off5 | novel_def5 |
|---|---|---|---|
| **combined over EB ridge** | **+0.000145 (t=+5.35)** | +0.000158 (t=+3.41) | +0.000183 (t=+3.65) |
| additive part (time-varying + LIN/SELF) | +0.000079 (t=+4.13) | +0.000057 | +0.000116 |
| **synergy part (CROSS on top)** | **+0.000066 (t=+3.40)** | +0.000101 (t=+2.43) | +0.000067 |

Positive in all three windows (+0.000082 full corpus, +0.000161 ≤2022,
+0.000191 ≤2023). Roughly half additive, half synergy. Against the additive
model's own r² over the mean (~0.002) that is a ~7% relative improvement;
against the non-additive ceiling the synergy half is ~26–39% depending on which
adjustment you apply.

**A caveat on the penalties.** The pair and player-season blocks had their ridge
penalties *pinned*, not tuned, because selecting on the tail of the training
window collapsed them to zero (the free-pair block returned +0.000002 with sem
0.000002 — a point estimate and a standard error both at zero is over-shrinkage,
not a weak signal). Pinning makes the numbers above honest as a demonstration
that the signal is there, but a deployable model needs a real penalty-selection
scheme.

### 8.6b What the synergy matrix says

`M_cross` read out on the corpus ≤ 2023 (×1000, points per possession per unit
z_i z_j). Descriptive — one fit, no standard errors; the predictive claim is the
+0.000066 above.

*Diagonal, the same trait twice:* **usage × usage −1.961** (the most negative
entry in the matrix), rtov × rtov −1.399, **rast × rast −1.370**; and on the
other side rorb × rorb +1.584, r3pa × r3pa +1.149, shot_rim × shot_rim +0.678.

*Strongest complementary off-diagonals:* **rast × assisted +1.378**,
rast × shot_rim +0.651, r3pa × shot_rim +0.650, rast × self_3p +0.561.

*Strongest redundant:* r3pa × rtov −0.929, shot_rim × rorb −0.893,
assisted × r3pa −0.873.

This is the founding hypothesis of the whole profile program, recovered from
data on both halves: **two high-usage players is the single most redundant
combination in the matrix**, two high-assist players is third, and **a
playmaker paired with a player who gets assisted is the largest positive
off-diagonal**. Unhypothesised bonus: spacing is self-complementary and pairs
with rim pressure, while offensive rebounding is the most self-complementary
trait of all yet conflicts with rim scoring — crashing the glass and finishing
at the rim compete for the same floor position.

At the level of named players the free-pair model tells the same story:
Nowitzki+Terry +0.40 per 100, Iguodala+Curry +0.34, Nash+Marion +0.33,
Curry+Draymond +0.29; and on the other side Duncan+Kawhi −0.25, Wade+Bosh −0.23,
**Curry+Monta Ellis −0.20** — the pairing the Warriors broke up for exactly
this reason.

### 8.7 Status

The northstar as stated — "extrapolate to unseen lineups significantly better
than any linear model" — is bounded by measurement, not by architecture: there
is ~+0.0001 r² of forecastable non-additive signal to win, against a linear
baseline at ~0.002. What replaces it is a scoreboard. Best measured basis:
player-season + free pairs, +0.000046 on novel five-man sets. Best harness
result: **+0.000145 (t=+5.35)** over 30 folds and three disjoint windows, from
time-varying player coefficients plus the profile CROSS block — about half
additive and half synergy, with the synergy half the first in this project to
survive an un-shrinking control.

The cheapest real improvement available is not an interaction model at all —
it is giving the additive baseline **time-varying player coefficients**, which
is standard RAPM practice and which this codebase has never had. That is a
linear change; it raises the bar rather than clearing it.

---

## 9. Phase 9 — the linear model was the bigger half all along

Phase 8 ended with a reframe: the non-additive ceiling is ~+0.00026 raw and
~+0.00017 forecastable, so the recurring 10⁻⁴ was roughly where the signal
ends. Phase 9 asked the corresponding question about the additive model that
carries the other 95% of the prediction, and the answer reframes the project a
second time.

### 9.1 The linear ceiling (`additive_ceiling.py`)

Four-way game-disjoint split; fit β on two disjoint halves A and B, score a
third set E with both. `noisefree = [E(y(p_A+p_B)) − E(p_A p_B)]/var(y)` cancels
estimation variance and leaves the noise-free score of the *shrunken*
predictor; as α→0 the shrinkage goes with it, so the limit is
var(Xβ_true)/var(y). Full corpus, 3 seeds:

| | Δr² | pts/100 |
|---|---|---|
| additive (static linear) ceiling | **+0.002759 ± 0.000034** | 5.94 |
| best a full-corpus player ridge reaches | +0.002259 | 5.38 |
| **linear headroom** | **+0.000499** | 2.53 |
| non-additive forecastable ceiling, for contrast | +0.00017 | 1.51 |

Flat across α = 1 → 300, which is the signature that shrinkage bias is gone.
Not extrapolated: because `G_{A∪B} = G_A + G_B` the double-data fit is free to
compute, and predicted vs observed agree within 3% at the operating α.

**There is ~3× more recoverable signal in the linear model than in the entire
non-additive budget the project spent eight phases on.**

The gap is an upper bound, not a prize. It is ridge's estimation error, and if
β were iid Gaussian ridge would be Bayes-optimal and the gap irreducible. It is
attackable only where that prior is wrong.

### 9.2 The time-varying ceiling (`timevarying_ceiling.py`)

A player-season column is nonzero only inside its season, so `X'X` is **exactly
block diagonal by season** and the free per-season model is just independent
per-season ridges — no CG, no approximation.

| model class | ceiling | best achieved |
|---|---|---|
| one coefficient per player | +0.002759 | +0.002259 |
| one per player-season | **+0.003400 ± 0.000103** | +0.001823 (free fit) |

Letting players change over time is worth **+0.00064 of pure additive signal**,
four times the whole non-additive ceiling — but a free per-season fit collects
*less* than the static model, because a season is a tenth of the data. The
prize sits entirely behind estimation noise.

### 9.3 Three levers that work, and stack (`additive_stack.py`)

θ_{p,s} = Z_p γ + β_p + δ_{p,s}, plus a shared career-stage curve η. One
solver, all corners off one split; the Schur complement collapses via
`G − G D⁻¹ G = α_d G D⁻¹` to a 4,886² assembly instead of 30,000².

| lever | Δr² vs plain ridge |
|---|---|
| box-score prior | +0.000181 ± 0.000014 |
| time-varying δ | +0.000099 ± 0.000005 |
| experience curve | +0.000097 ± 0.000013 |
| **all three** | **+0.000385 ± 0.000021** |

Overlap **+0.000009** — slightly super-additive. This closes **51% of the
linear gap** and is **5.5× everything the synergy program delivered**.

**The prior only works after dropping columns.** With all 80 profile dims it is
null (+0.000003); with box-score dims only it is +0.000181; with the on/off
`lift` dims only it is exactly zero (−0.000000, t=−0.25). Unadjusted plus-minus
is noisy and collinear with what ridge already estimates, so it adds variance
without information *and* dilutes the box-score signal. Two traps hit and fixed:
profile dims are badly collinear and must be orthonormalised (unrotated, the
prior lost 0.0009 r² on the *validation* split — diagnostic that it was
conditioning, not selection); and aggregate r² was the wrong first test, since
it is dominated by possessions where everyone has 20k possessions of history.

### 9.4 The experience curve, and why it matters more than its size

Measured within player (deviation from his own career mean, pts/100):

| experience | 0 | 1 | 2–3 | 4–5 | 8 | 10–12 | 14 |
|---|---|---|---|---|---|---|---|
| offense | −0.160 | −0.046 | +0.035 | +0.100 | **+0.144** | −0.030 | −0.167 |
| defense | −0.032 | +0.015 | +0.052 | +0.082 | +0.106 | +0.138 | −0.013 |

Rookies below their own average, peak four to nine seasons in, decline after
ten; **defence ages considerably better than offence**. Eighteen shared
parameters.

`delta_persistence.py` explains why this is the important half of time
variation. Cross-fitting δ against itself one season on gives reliability
+0.248 and persistence +0.078, so **ρ_AR = 0.31**: a free season deviation
barely forecasts, and for a season the model has not seen it falls back to the
career value and is worth nothing. An experience curve *extrapolates* — nobody
knows a player's 2026 deviation, everybody knows it will be his ninth season.

Garbage-time control (`exp_curve_control.py`): restricting to competitive
possessions (|margin| ≤ 12, 77% of the corpus) the gain **rises** from
+0.000077 to +0.000101, and the rookie penalty steepens. Blowout minutes were
diluting the effect, not causing it. Remaining caveat is survivorship — the
surviving 14th-season players are the good ones, so read the right tail as a
lower bound on decline.

### 9.5 What did not work

**Per-channel shrinkage is null** (`channel_ridge.py`). Possession outcomes were
parsed from the play-by-play into channels (`possession_outcomes.py`) giving an
exact orthogonal split of scoring: **22.5% of possession variance is shot
selection, 77.5% is shot-making plus luck**. Since ridge is linear in y and the
channels sum to y, fitting every channel at the same α reproduces the single
ridge exactly — so the comparison is airtight, and the answer is
**−0.000103 ± 0.000036**. Every channel wants α ≈ 3000, the same as points:
optimal shrinkage is σ²/τ², and a lower-noise channel carries proportionally
less player signal. This kills per-channel α; it does *not* touch the separate
claim that defensive *interaction* structure is visible on rim attempts.

**Transformer, final verdict** (10 folds, corpus ≤2023). Bilinear CROSS over
LIN+SELF +0.000121 (t=+4.11); transformer over the same base +0.000094
(t=+3.29); **transformer over bilinear −0.000027 (t=−0.96), not significant**.
This corrects a 6-fold interim reading of −0.000039 (t=−2.78) that said capacity
hurts — 76,353 parameters are *indistinguishable* from 55, not worse.

**Regularization is not the issue.** Sweep: bilinear (55 params) +0.000130;
transformer at dropout 0.1 / wd 1e-4 +0.000075; dropout 0.3 / wd 1e-3 +0.000047;
wd 1e-1 +0.000025; and a *small* transformer, d16 with 3,041 params, +0.000047.
Neither more regularization nor less capacity closes the gap. The bilinear form
encodes the factorization-machine identity exactly; that inductive bias is the
whole difference.

### 9.6 A product scoreboard (`lineup_scoreboard.py`)

r2_over_ridge is right for research and wrong for a product. The question a
lineup tool answers is whether a ranking of candidate fives is correct, and a
lineup's *realized* rating over a few hundred possessions is mostly noise. So
cross-fit the truth: split evaluation games into E1/E2, `var_true = cov(m1,m2)`
cancels the noise, and ρ = cov(p, m̄)/√(var_true·var_p) is the correlation with
true lineup quality.

| | ρ | slope | sd_true | top-3 lift |
|---|---|---|---|---|
| offense | +0.586 | 0.61 | 4.19 /100 | +1.06 /100 |
| defense | +0.658 | 0.66 | 3.11 /100 | +0.66 /100 |

Defense is **more** predictable than offense, which is the opposite of this
project's usual framing. **slope = 0.61 means 38% of the variance in a raw
lineup rating is estimation noise** — the same gap as §9.1 seen from the
product side. Staleness: one season past the cutoff ρ=+0.593 / slope 0.62 /
top-3 +2.13; two seasons out ρ=+0.561 / slope 0.47 / top-3 +0.82. The ranking
survives; the magnitude decays fast.

### 9.7 Synergy is untouched by all of it

The worry was specific: the box-score prior makes a coefficient a linear
function of profile, which summed over a lineup is exactly the LIN block synergy
is measured against. Modern window, 3 seeds, CROSS over LIN+SELF: **+0.000022 ±
0.000015 over plain ridge, +0.000020 ± 0.000011 over the improved model.**
Unchanged. (On the full 25-season corpus the same rig fails to reproduce synergy
at all on *either* baseline — §8's era finding, exactly. Use this rig for the
comparison, not the level.)

### 9.8 Status

The northstar became a tool: build any five, get a projected rating in points
per 100 with the model's own uncertainty attached. Ratings pass the eye test at
both ends — Curry +8.4 and Gobert +7.0, Lou Williams and Trae Young at the
bottom of defense — and the prior moves exactly the thin samples (Wembanyama
+6.5 on defense off 4,818 possessions).

Where the whole problem now stands, in one place:

| | Δr² |
|---|---|
| linear ceiling, static | +0.002759 |
| linear ceiling, per-season | +0.003400 |
| plain ridge | +0.001949 |
| **best model now** | **+0.002334** |
| non-additive ceiling on top, forecastable | +0.00017 |
| synergy actually captured | ~+0.00007 |

Untested levers on the remaining gap: heavy-tailed priors (stars are genuine
outliers and Gaussian shrinkage over-pulls them), position and height as prior
dimensions, an explicit aging curve rather than a step function, and defensive
interaction structure on channel targets rather than points.

### 9.9 Closing out the prior-misspecification list

§9.1 argued the linear gap is attackable only where the iid-Gaussian ridge prior
is wrong, and named four ways it might be. All are now tested. Three work
(§9.3); the rest are null.

**Heavy tails are null.** Student-t of ν df via EM adaptive ridge,
α_j = α_0(ν+1)/(ν + E[δ_j²]/τ²); ν→∞ recovers plain ridge exactly, so it is a
strict generalisation. Full corpus, 3 seeds: best Student-t − Gaussian =
**+0.000006 ± 0.000004**, flat optimum near ν=8. Stars are not outliers relative
to the ridge scale.

*One trap, which flipped the sign.* Using the point estimate δ̂² in the EM update
gives −0.000032, because δ̂ is small both when a player really is average and
when there is no data on him — it punishes a thin record for being thin. The
correct EM uses the posterior second moment E[δ²] = δ̂² + Var(δ), approximated as
σ²/(n_j + α_j). With that fix the effect goes to zero.

**Position and height are null.** box alone +0.000139, box+pos +0.000132 on the
same window. The box-score profile already encodes position through shot
locations and block/rebound rates.

**A season-specific profile prior is null**, and monotonically so: career
+0.002334, blend 0.25 +0.002316, blend 0.5 +0.002231, pure season +0.001977;
best − career = −0.000018 ± 0.000005. A single season's box score is too noisy
to be a prior mean. This kills the appealing story that a season prior could
make time-variation forecastable where a free δ cannot.

*Trap here too, and a general one.* `profile_matrix` orthonormalises by SVD per
call, so each season's Z landed in its own rotated basis while γ is shared
across seasons — γ meant a different thing every season, costing −0.000197 on
its own. Fixed by returning the rotation from the career call and pushing every
season through it. Any future prior built from several matrices sharing one γ
must do the same.

**So the remaining ~+0.0004 has survived every prior-shape attack available.**
It looks close to irreducible for a linear-in-players model on this data. Moving
it needs new information, not a better estimator.

### 9.10 Where the non-additive signal actually lives (`channel_ceiling.py`)

Phase 8 measured the non-additive lineup ceiling on points. Points split exactly
and orthogonally into what the shots were and whether they went in, so run the
same four-way cross-fit on each channel. Full corpus, 3 seeds, τ² in points²:

| side | α | points | shots | making | shots share |
|---|---|---|---|---|---|
| **defense** | 10 | +0.000553 | **+0.000393** | +0.000047 | **71%** |
| defense | 3224 | +0.000653 | +0.000474 | +0.000109 | 73% |
| offense | 10 | +0.000833 | +0.000299 | +0.000247 | 36% |
| offense | 3224 | +0.001047 | +0.000506 | +0.000306 | 48% |

**Defence is ~8:1 shot selection over shot-making; offence is roughly even
(1.2:1).** Defences control where you shoot far more than whether it drops.

This confirms §8's `target_channel_finding` at the ceiling level rather than by
a correlation between fitted pair effects. The defensive interaction nulls of
Phases 1, 3B and 5 were hunting on a target where only ~9% of the defensive
non-additive effect lives, against 76% of the variance being shot-making noise.
The shot-selection channel has variance 0.309 against points' 1.281 — **4×
better signal-to-noise** — and carries 71% of the effect. Any future defensive
interaction work should target it.

Note this does *not* contradict §9.5: per-channel **shrinkage** of the additive
model is null, because optimal α is σ²/τ² and both scale together. Whether
**interactions** are identifiable on a channel is a different question, and the
answer is yes.

Two cautions. τ²(points) here is larger than §8's numbers because this rig uses
min_n=10 and no team-scheme or deployment controls — trust the ratio within the
table, not the level across experiments. And τ²(points) ≠ τ²(shots) + τ²(making):
the lineup-level channel effects have a cross-covariance (positive for offence,
slightly negative for defence), so never infer one channel by subtracting.

---

# 10. Teammate context: the profile is measured in a context (Phase 10)

**The hypothesis (user, 2026-09-01).** A player's box-score profile is not a
property of the player. Luka is a great passer, but if he never plays with
finishers we never see it — his assist rate is a fact about *him in his observed
context*. If so, `Z` in `theta = Z gamma + beta + delta` carries a bias that is
correlated across teammates, `gamma` is attenuated, and the prior is worth less
than it should be. The proposed cure was the strength-of-schedule algebra of
Park & Newman (arXiv:physics/0505169): a circular dependency resolved by a
matrix inverse.

The algebra is exactly right. Writing the observed profile as
`Z = S + lam A S B'` — `A` the row-normalised shared-possession matrix, `B` a
small (d x d) context-sensitivity matrix, `S` the latent context-neutral
profile — the solution is a resolvent, `(I + lam B (x) A) vec(S) = vec(Z)`,
whose Neumann series

    S = Z - lam(A Z B') + lam^2 (A (A Z B') B') - ...

is the same direct-plus-indirect expansion Park & Newman use, with the same
convergence condition (`rho(A)=1`, so damping is mandatory).

## 10.1 The bias is real, and the placebo proves the design

`context_profile.py` regresses each player-season's profile on the
co-occurrence-weighted profile of his teammates, with **player fixed effects**,
so `B` is identified off trades and roster turnover — changes in who a man plays
with, holding who he is fixed. 9,107 player-seasons, 2002–2024.

`ft_pct` is a **placebo**: nothing a teammate does can change your free throws.
It reads **0.008** of within-player variance explained by context, against
**0.183** between players. That 23x gap is roster selection — like players
cluster on like teams — and only the within design removes it.

| effect (sd per sd) | beta | t |
|---|---|---|
| usage <- teammate usage | -0.060 | -4.21 |
| def reb <- teammate def reb | -0.051 | -5.67 |
| assisted <- teammate assist rate | +0.058 | +5.01 |
| **assist rate <- teammate `assisted`** | **+0.040** | **+3.60** |
| blocks <- teammate blocks | -0.024 | -3.95 |
| eFG% <- teammate eFG% | +0.026 | +2.99 |
| `ft_pct` (placebo) | -0.014 | -1.49 |

Two families, opposite signs. **Crowding out** on the diagonal — one ball, one
rebound, one shot to take. **Role complementarity** off it.

**The Luka effect is confirmed, on a different variable than proposed.** Assist
rate does not respond to how well teammates *shoot* (`self_efg` beta = -0.002,
t = -0.30). It responds to whether they are finishers **by role** — `assisted`,
the share of their makes set up by someone else. Not how well they convert;
whether they catch-and-finish rather than create. It runs both ways
(`assisted <- rast` is +0.058, t = +5.01).

Two corrections were needed to get here, both material:

* **The loop.** Player fixed effects plus leave-one-season-out teammate profiles
  are *not* enough. A teammate's career `assisted` rate is high partly because
  he played with the focal player in other seasons; LOO removes the focal
  season, not the focal player. `--mode strictnew` (a teammate counts only if
  the pair had never played together before, and his profile uses only prior
  seasons) cut `rast <- assisted` from **+0.154 (t=10.71)** to **+0.040
  (t=3.60)** and killed `self_efg <- self_efg` outright.
* **The conditioning.** The six shot-location shares sum to 1, so their context
  coefficients are identified only up to a constant shift and OLS picks a wild
  member of the family — it projected Gobert to **-2.0 three-point attempts per
  100**. Fitting in an SVD-truncated basis (condition 266 -> 19.5) is the same
  treatment `profile_matrix` already applies to `gamma`, for the same reason.

## 10.2 Removing the bias does nothing. Adding the context does a little.

Full corpus, 3 seeds, penalties and `lam` selected on a disjoint validation set,
scored on a third:

| | delta r2 vs the current model |
|---|---|
| **SUBTRACT** — deconfound to a context-neutral profile | **+0.000001 +/- 0.000001** |
| **ADD** — teammate context as extra prior columns | **+0.000020 +/- 0.000003** |

**The null is real, not a no-op.** Deconfounding moves `Z` by **34% of its
norm**, and only **6.7%** of the correction lies in `Z`'s own span, so `gamma`
cannot quietly absorb it. The model sees a substantially different profile and
predicts the same thing. *The part of the profile that context distorts is not
the part that predicts value.*

**And the two are nested.** `S gamma = Z gamma - lam (AZ)(B' gamma)` is exactly
`[Z, AZ]` with coefficients `[gamma, -lam B' gamma]`, so the augmented model
contains first-order deconfounding — and beats it. The +0.000020 therefore is
**not** coming from the bias-correction direction. It is context as
*information* (who he played with tells you what he is worth), not context as
bias. That is partly selection, and legitimate for prediction.

Per the fold/seed rule, 3 seeds share the corpus: read sem 0.000003 as a lower
bound on the uncertainty.

## 10.3 What it buys the tool

`B` supports something the rating cannot: projecting a player's **rates** inside
a hypothetical five, `z_p = S_p + B * mean(S_q)`, in box-score units. The delta
must be `B(c_new - c_old)`, not `B c_new` — an observed profile already contains
its own history.

    Luka's assists per 100
      beside finishers (Klay, Covington, Capela, Robinson)   11.53 -> 11.67
      beside creators  (Westbrook, Harden, Trae, Kyrie)      11.53 -> 11.03
                                                     usage  39.99 -> 38.98

The second is flagged **[EXTRAPOLATION: 3.5 sd]**. `B` is a local linear
approximation fitted on within-player context shifts almost all under 1 sd; a
lineup of five creators asks it about a 3.5 sd shift. `context_projection.py`
prints "out of range" rather than a number whenever a projected rate leaves the
physically possible interval.

**Modules:** `context_profile.py` (measure `B`; `--mode strictnew`, `--svd-tol`),
`context_deconfound.py` (the resolvent; verified exact to 1e-14 on a synthetic
ground truth), `context_prior.py` (the harness verdict; `--mode deconf|augment`,
`lam=0` is exactly the current model and is a regression test on the whole rig),
`context_projection.py` (the tool readout).

---

# 11. We were grading ourselves on the wrong exam (Phase 11)

Every model comparison in Phases 8–9 used a **random 40/40/20 split over game
ids** spanning the whole corpus. For a test possession in week 20 of 2019, the
training set contained other 2019 games — including later ones. That is
interpolation within a season, not forecasting, and the tool's job is
forecasting.

`harness.py` has always implemented rolling-origin forward-in-time folds. The
Phase 9 modules were written standalone for the fast Gram path and each copied
the same random-split boilerplate. **Correct machinery existing elsewhere in the
repo is not protection.**

## 11.1 The corrected ranking

`forward_eval.py`: for each test season T, fit on seasons ≤ T−2 and select
penalties on T−1, then refit on ≤ T−1 and score T. The profile `Z` is rebuilt
from fitting games at each origin, so a player who debuts in T has a zero
profile and falls back to the league-average prior — the actual rookie case.
16 test seasons, 2010–2025.

| lever | random split | **forward** | sem | t |
|---|---|---|---|---|
| base | +0.001949 | **+0.001322** | | |
| box-score prior | +0.000181 | **+0.000175** | 0.000036 | 4.87 |
| time-varying δ | +0.000099 | **−0.000001** | 0.000016 | −0.05 |
| δ **carried forward** (ρ=0.6) | — | **+0.000115** | 0.000012 | **9.31** |
| experience curve | +0.000097 | **+0.000155** | 0.000034 | 4.61 |
| all (naive δ) | +0.000385 | +0.000271 | 0.000068 | 3.97 |
| **all + carried δ** | — | **+0.000371** | 0.000060 | 6.21 |

**The base model is 1.47× weaker at forecasting than we believed.** Every "we
reach X% of the linear ceiling" claim in §9 is an in-period claim.

**The prior is the robust lever** — +0.000181 → +0.000175, essentially
unchanged. It exists to help players you have little data on, which is precisely
the forecasting problem.

**Time-varying δ is worthless as fitted and valuable as carried.** Naive, it is
exactly zero: at forecast time `δ_{p,T}` does not exist, and the random split
had been handing it over. Carrying the previous season's δ forward at ρ=0.6
— chosen on validation in *every one* of the 16 seasons — yields +0.000115 at
the tightest sem of any lever. δ is a **recency** signal, not a season-specific
fit. This finally reconciles `delta_persistence.py` (31% persistent, "worth 10×
less for forecasting") with the old +0.000099.

The stack totals about the same (+0.000371 vs +0.000385), but its **composition
is completely different** — so the old ranking was not merely optimistic, it
pointed at the wrong things to build.

**The law this suggests:** forecasting rewards structure *shared across players*
and punishes anything fitted *per-player-per-season*. Synergy is shared
structure, so it ought to survive the forward test — untested as of writing, and
the obvious next thing to check.

Two cautions. Test seasons share training history, so the sems are lower bounds.
And beware single seasons: 2022 alone said the experience curve was 3.4× bigger
forward; over 16 seasons it is 1.6×.

## 11.2 The experience variable was wrong for a quarter of the corpus

Chasing the now-larger experience lever exposed a bug. Experience was
`season − first season the player appears in this corpus`, and the corpus starts
in 2002, so everyone already in the league read as a rookie:

```
season 2002  100.00% of possessions credited to "rookies"
season 2003   90.84%
season 2007   49.69%
season 2013   12.28%
```

440 players — **26.9% of all possessions** — carry a wrong number for their
entire career. Possession-weighted, experience is understated by **1.00 season**;
for the 21% actually affected the median error is **5 seasons**.

`player_bio.py` fixes it from the basketball-reference player index (26 pages,
3s apart, cached): `year_min` for the true debut and `birth_date` for age.
**98.8% matched.** Our `season` uses the same end-year convention as BBR.

Two validation traps, both hit and both worth remembering: folding away the
generational suffix merged **Gary Payton II into Gary Payton** (a 34-season
error), and requiring the BBR career span to overlap the observed span was what
caught it. The 30 remaining "implausible" matches were all *correct* — Michael
Jordan, debut 1985, observed 2002–03, is the Wizards comeback.

This also supplies **age**, which the database lacks entirely and which
experience cannot substitute for. `aging_curve.py` builds the career-stage block
on observed / true-debut / age, with either the incumbent 9-step bins or a
natural cubic spline (linear beyond the boundary knots, so a 20-year veteran is
not extrapolated off a cubic). `obs`+`bins` reproduces the old block exactly.

**Modules:** `forward_eval.py` (the rig; `--exp-mode`, `--exp-basis`,
`--context`), `player_bio.py`, `aging_curve.py`.

---

## 12. Phase 12 — synergy is real, and it is idiosyncratic (2026-09-01, overnight)

Phase 11 established that every lever must be ranked forward in time. Phase 12
points that discipline at the one question the project had never settled: **is
there any non-additive structure that actually forecasts?**

The answer is yes, and it is not the one we had been modelling for four phases.

### 12.1 Free teammate pairs forecast (`experiments/forward_pairs.py`)

A free indicator per unordered teammate pair, fitted on the additive model's
residual, under the `forward_eval` protocol: fit ≤ T−1, penalties chosen on
T−1, scored on season T, sixteen rolling origins 2010–2025.

The basis is constant within a five-man set, so the sufficient statistics are
the per-(five, season, team) possession count and mean residual — 295k cells
instead of 5.6M possessions, an identical fit. Cell codes, rosters and pair keys
are built once; each origin is a mask.

| arm | test r² | vs previous | sem | t | seasons + |
|---|---|---|---|---|---|
| additive (prior + career + true-debut stage) | +0.001701 | | | | |
| + free player indicator | +0.001699 | −0.000002 | 0.000001 | −1.52 | 3/16 |
| **+ free pair indicator** | **+0.001727** | **+0.000028** | 0.000008 | **+3.66** | **13/16** |
| novel five-man sets only | +0.001647 | +0.000015 | 0.000004 | +3.42 | 13/16 |

**The `player` arm is the whole design.** A free indicator per player refit on
the additive residual adds no structure — it can only undo shrinkage, the trap
`pair_ceiling`'s docstring names. It reads −0.000002, with its penalty driven to
the *top* of the grid, because there is nothing left for it to recover. Both
arms select the same penalty, so the pair increment is a matched contrast.

+0.000028 is **16% of the +0.00017 forecastable non-additive ceiling**. The
random-split `ceiling_decomposition` put free pairs at 15%. Unlike time-varying
δ, this survives the change of protocol essentially unchanged.

**Defence is null**: +0.000003 (t=+0.81, 8/16), reproducing
`ceiling_decomposition`'s "defensive free pairs are 0% of their ceiling"
forward. Offense yes, defence no.

### 12.2 The profile bilinear does not (`forward_synergy.py`, both targets)

| contrast | Δr² | sem | t | seasons + |
|---|---|---|---|---|
| CROSS net of LIN+SELF, points | +0.000005 | 0.000012 | +0.43 | 10/16 |
| CROSS net of LIN+SELF, shots | +0.000005 | 0.000007 | +0.72 | 12/16 |

Null on both targets. This closes the channel escape hatch: the bilinear fails
even where the non-additive signal demonstrably lives.

**Synergy is real and it is idiosyncratic.** It lives in particular pairs of
people, not in interactions of play-style summaries. Free pairs beat the 10×10
quadratic by six times forward.

### 12.3 What a pair effect is made of (`experiments/pair_readout.py`)

Three readouts from one full-corpus fit:

- **Not a team in disguise.** Adding a team-season indicator that absorbs every
  team's level leaves the pair coefficients correlated **r = +0.960** with the
  originals; their spread moves 0.173 → 0.171 points per 100. This was the main
  alternative explanation and it is dead.
- **Not predictable from profiles.** Regressing the fitted pair coefficients on
  the bilinear basis `vech(z_i z_j' + z_j z_i')` — the exact 55-parameter form
  the tool's chemistry matrix uses — gives a weighted **R² of 1.5%**. That is an
  upper bound on what any rank-10 profile quadratic can recover, and it is a
  third independent confirmation of `pair_effects_not_lowrank`.
- **Face validity, unprompted.** Best: Curry + Green +0.83, Iguodala + Curry
  +0.81, Nowitzki + Terry +0.73, Booker + Bridges +0.72. Worst: Wade + Bosh
  −0.84, Smart + Rozier −0.81, Monta Ellis + Curry −0.76, Paul + Ayton −0.76,
  Turner + Sabonis −0.57. The famous fit successes and the famous fit failures.

### 12.4 The un-shrinking trap, caught and priced

Over an additive baseline fitted on the **shots** channel, the same pair block
first read +0.000142 (t=+5.74) — five times the points-target number. But the
`player` control also jumped to +0.000223 and its penalty sat on the grid
boundary: a shots-fit additive model leaves the entire shot-*making* half of
player value in the residual, and an under-fit player block lets the pair block
claim it.

Re-running with the player grid opened two decades downward cut the pair gain to
**+0.000060** — 58% of the apparent effect was un-shrinking. A third run,
opened two decades further, is byte-identical, so the optimum is interior and
+0.000060 (t=+6.53, 16/16) is the honest shots-channel number.

**Rule: a control arm whose penalty sits on a grid boundary is not a control.**

### 12.5 Per-lineup error bars: measured, and deliberately not shipped

`experiments/lineup_uncertainty.py` propagates the ratings' posterior covariance
— σ²M⁻¹ through the Schur-collapsed system, so a five's variance is the sum over
all 25 entries of Cov(θ), not the 5 diagonal ones. The off-diagonal is the
interesting part: two men who only ever shared a floor have individually vague
ratings and a sharp *sum*, because their estimation errors cancel.

It compresses to rank-32 + diagonal at **0.2% median error**, so shipping it
would have been cheap. It is not shipped, because it failed its own test:

- the posterior sd ranges only **1.80 → 2.37** points per 100 across real
  lineups, so a per-lineup shrink would move 0.38–0.52 against a shared 0.45;
- sorting lineups by their own posterior variance does **not** order how well
  they calibrate (offense, by quartile: 0.250, 0.558, 0.592, 0.620 — backwards),
  and the bin-level true spread is noisier than the effect being tested.

Two things did validate, by independent routes: ρ = +0.52 / +0.51 against the
published scoreboard's 0.586 / 0.658, and a calibrated offensive posterior sd of
3.5 points per 100 against the tool's independently measured residual spread of
3.46.

### 12.6 What shipped

`tool/five.html`, same URL. Chemistry is now **measured, not modelled**: 28,446
teammate pairs with ≥200 shared possessions, each carrying its own coefficient.
A pair with no shared history contributes **zero**, and the page says how many of
the ten pairs that applies to — replacing a quadratic that used to extrapolate to
22× the real lineup spread and be capped.

The shrink is re-measured forward **on this model**, per side (0.447 offense,
0.591 defence). Re-using the 2019-era 0.60 would have been a real error: the
true-debut career-stage fix alone moved the sum of five ratings ~15%, and the
old slope would have paid that improvement straight back out as a bigger
projection. With the honest slope the Warriors' death lineup lands at +9.5,
where it always did.

### 12.7 Does the low-noise channel give better PAIR estimates? No.

`forward_pairs` showed the pair gain roughly doubling when the additive baseline
is fitted on the shot-selection channel (+0.000060 vs +0.000028 offense), and on
defence that configuration was the difference between null (+0.000003) and
apparently real (+0.000032). The natural reading — the channel thesis extending
from additive value to pair value — is wrong.

`experiments/pair_channel.py` separates the two stages, holding the additive
baseline fixed at the good POINTS model and changing only the channel the pair
coefficients are estimated from. The pair block is always fitted alongside a
free player block with its own swept penalty, and only the PAIR component enters
the prediction, so it cannot smuggle additive shot-making value into a model
that already contains it.

| | offense | defence |
|---|---|---|
| additive (points) | +0.001701 | +0.001701 |
| + pairs estimated from points | **+0.001731** (+0.000030, t=+3.64, 15/16) | +0.001702 (+0.000001, t=+0.16) |
| + pairs estimated from shots | +0.001718 (+0.000017, t=+2.30, 10/16) | +0.001702 (+0.000001, t=+0.14) |
| shots over points, paired by season | **−0.000013** (t=−1.73, 3/16) | −0.000000 (t=−0.02) |

The shots channel is **worse**, not better, for estimating pairs. What the
`forward_pairs` shots row was measuring is that a shots-fit additive model is a
much weaker additive model (+0.000705 against +0.001701), so its residual leaves
more for any block to find — the totals never come near the points row. And
defensive chemistry is null on both channels, so the tool is right to claim
none.

`--chan points` reproduces the `forward_pairs` off/points result season by
season, which is the rig's built-in calibration.

**The deployable model is the simple one**, and it is what shipped: points
additive + pairs estimated from points, +0.001731.

### 12.8 Can anything predict a pair effect? No — and that closes the loop

Free pairs forecast, but only for pairs that have shared a floor; 97.6% have
not, and the northstar is pricing lineups that never played. The fix everyone
reaches for is the prior-mean ridge one level up,

    pair_effect(i,j) = f(z_i, z_j) + deviation,   penalty on the deviation

so `experiments/pair_predictability.py` asks what `f` could possibly be.

**The rig.** Split games in half, fit the pair block independently on each, so a
pair has two estimates with independent noise. `corr(β_A, β_B)` is the
reliability r — the ceiling on what any f could correlate with, and the number
saying how much of the target is even real. Score each candidate **out of fold
over pairs** against the two-half mean, then un-attenuate by
`r_mean = 2r/(1+r)` to get the fraction of a pair effect's REAL variance the
feature set reaches.

Reliability is **0.18–0.20** over 14,894 pairs with ≥400 possessions per half.
Mean r² of truth across three game-split seeds:

| f | params | r² of truth |
|---|---|---|
| sum + \|difference\| | 20 | 1.1% |
| \|difference\| only (complementarity) | 10 | 0.83% |
| **sum only — additive control, should be 0** | 10 | **0.47%** |
| gradient boosting on symmetrised features | — | 0.7% |
| profile bilinear (what the tool used to ship) | 55 | **0.1%** |
| archetype × archetype, K = 6…24 | 21–297 | 0.07% |
| placebos (permuted features) | — | ~0.05% |

Three things follow. The bilinear is **zero out of fold** — §12.3's 1.5% was
in-sample optimism against a noisy target. It is **not a functional-form
problem**: boosting bounds any smooth function of these ten dimensions at ~1%,
no better than a ten-parameter linear form, and archetype × archetype (backlog
§3.5) is dead at 0.07%. And **half of the little that is there is additive** —
the `sum only` control is additive in the players by construction and scores
0.47%, so the genuinely pairwise predictable component is well under 1%.

**Consequence.** Measured pairs work because they are direct observations of
high-possession duos. Predicted pairs cannot work on box-score features. The
hierarchical model is bounded at ~1% of an effect that is itself +0.000030 —
negligible. The route is richer features (§4.1 tracking aggregates), not a
better `f`. This also deepens the explanation for the Phase 5 architecture
search: those models failed not merely because pair effects are not low-rank,
but because pair effects are not a function of the players' observable profiles
at all.

**The trap it caught.** The first version of this file trained on β_A and scored
against β_B on the *same* pairs, arguing that independent noise across halves
makes overfitting harmless. That is false for a model that can memorise:
boosting drives its prediction to β_A, so corr(pred, β_B) → r and the
un-attenuated score → √r = 0.28 out of nothing at all. The permutation placebo
scored **7.2%** against the real features' 9.6% and killed the entire first
reading. Out-of-fold over pairs fixed it, and the placebos then read ~0.

### 12.9 The other regime: mid-season, δ comes back (`intraseason_eval.py`)

Season-ahead is the right protocol for ranking levers, and §11 rewrote the
ranking on it. But it is not the only question a lineup tool is asked. In
January a coach choosing between two fives *has* this season's games, and
δ_{p,T} is estimable from them. Backlog §2.2 asked for that regime; this is it.

Per test season T: fit all seasons < T **plus the first half of T by week**,
score T's second half. Nothing from the scored half is ever seen. The Gram is
still block diagonal by season, so the fit is the sum of full blocks for seasons
< T and a *half* block for T — two block sets built once, every origin a subset
sum. 15 origins, 2010–2024, ~60s each.

| lever | test r² | vs base | sem | t | seasons + |
|---|---|---|---|---|---|
| base | +0.001700 | | | | |
| prior | +0.001858 | +0.000158 | 0.000031 | 5.08 | 13/15 |
| exp | +0.001863 | +0.000164 | 0.000023 | 7.09 | 15/15 |
| all_nodelta | +0.002024 | +0.000324 | 0.000039 | 8.25 | 15/15 |
| **all_delta** | **+0.002114** | **+0.000414** | 0.000038 | **10.94** | **15/15** |
| all_cf | +0.002024 | +0.000324 | 0.000040 | 8.11 | 15/15 |

**This season's δ, estimated from the first half: +0.000090 ± 0.000015,
t = +5.97, 13/15 seasons** (sign test p = 0.004).

**The mechanism flips between the two regimes, and that is the whole finding:**

| | δ as fitted | δ carried forward at ρ=0.6 |
|---|---|---|
| season-ahead (§11.1) | **+0.000000** | **+0.000115** |
| intra-season (here) | **+0.000090** | **+0.000000** |

Season-ahead, δ_{p,T} does not exist, so the only way to use a per-season
deviation is to carry the last one forward. Mid-season it does exist, and once
it is in the fit, last season's deviation adds exactly nothing — the current
partial season supersedes it. The δ lever is worth about the same either way;
what changes is which version of it is usable. Neither regime substitutes for
the other and both belong in the record.

+0.002114 is the best number this project has for a deployable model in any
regime. The tool ships career ratings; a mid-season mode would use this-season
δ, not carry-forward.

### 12.10 Pair chemistry drifts: 31% persistent across a decade

The tool ships one static coefficient per pair, averaged over up to 24 seasons.
`pair_predictability.py --split time` asks whether that is right, by splitting
the corpus at its median date instead of at random and correlating a pair's
older-decade estimate with its newer-decade one.

Matched on the **678 pairs that qualify in both designs** (≥400 shared
possessions in each half):

| | correlation |
|---|---|
| same-period (random game halves) | **+0.409** |
| across time (older vs newer decade) | **+0.129** |
| **persistence** | **0.31** |

sem ≈ 0.038 at n = 678, so the gap is roughly 7 sem. The matching matters:
unmatched, the random split reads 0.250 over 14,894 pairs against the time
split's 0.129 over 680, which confounds drift with *which pairs qualify* —
tenure decides who straddles a date.

**0.31 is the same number `delta_persistence` measured for player-season
deviations.** Whatever makes a player's season deviate from his career appears
to move a pair's chemistry away from its career average by the same fraction.

For the tool this says a career-average pair number understates recent chemistry
and overstates old. Recency weighting should be better — but the static version
is the one validated forward at +0.000030, so that is a testable improvement,
not a change to make on this measurement alone.

### 12.11 The upstream model must be refit inside the split

Getting §12.10 required fixing the rig twice, and the fix is general enough to
be a rule. Split-half reliability of a free pair effect, same pairs, same
everything except how the additive model whose residual the pairs are fitted on
was estimated:

| additive model | corr(β_A, β_B) |
|---|---|
| one global fit, static coefficients | **+0.080** |
| one global fit, per-season δ on | **−0.140** |
| **refit separately on each half** | **+0.250** |

An additive model fitted on all the data has already seen both halves. It
absorbs part of each half's noise, and that absorbed noise returns in the
residual with the opposite sign — the same mechanism as the ρ = −0.12 artifact
§8 documents for lineup means, one level up. δ_{p,s} makes it far worse, because
a per-(player, season) parameter has enough freedom to absorb lineup-level
structure directly.

For a time split there is a second, independent reason: with static player
coefficients a player's career trajectory makes his single coefficient too low
early and too high late, so his pairs anti-correlate with themselves across eras
(−0.068 before the fix, +0.129 after).

**Rule: when two estimates of the same quantity are compared across a split,
everything upstream of them must be fitted inside the split too.** Refitting
costs ~10s per half here and changed a headline by 3× and a sign. It also means
§12.8's ~1% predictability ceiling is an *overstatement*: it un-attenuated by a
reliability that was biased down.

### 12.12 The drift is real and unexploitable

§12.10 says pair chemistry is 31% persistent across a decade, so a career
average should be a compromise and down-weighting old shared possessions should
help. `forward_pairs.py --halflife 0 8 4 2` sweeps the half-life on validation
like any other hyperparameter, 16 origins:

| | pair gain over the player control | t | seasons + |
|---|---|---|---|
| half-life swept (0 / 2 / 4 / 8 seasons) | +0.000028 | +3.48 | 13/16 |
| incumbent (no decay) | +0.000028 | +3.66 | 13/16 |
| **paired difference** | **−0.000000** (sem 0.000003) | | **7/16** |

Exactly nothing. The pair *set* is chosen on undecayed counts in both arms so
the comparison is matched, and with `--halflife 0` the run is bit-for-bit
identical to the committed incumbent — the regression check that makes the
paired difference meaningful.

**Why the drift cannot be exploited.** Down-weighting old possessions buys a
more current estimate and pays in sample size, and a pair coefficient is already
mostly noise (reliability 0.25 on the full sample). The pairs whose chemistry
drifted most are exactly the ones without enough recent possessions to
re-measure. The two effects cancel to three decimal places.

It is also a textbook case of the validation noise floor: validation chose a
decay in 10 of 16 seasons — half-life 2 in nine of them — and the test says the
choice was worth nothing at all. At 10⁻⁵ effect sizes the validation set simply
cannot tell.

The tool's static career pair number stands, not by default but by measurement.

### 12.13 Off × def matchups are at the noise floor (`matchup_reliability.py`)

"We attack the rim, they have no rim protector" is the most natural
non-additive effect in basketball and backlog §3.1 had it as the last untested
one. Rather than fit another cross-side model, this applies rule 8 and measures
whether there is anything to fit: split the games in half, estimate every
(offensive i, defensive j) pair's effect twice on independent data, correlate.

| min possessions per half | pairs | corr, raw | corr, team-controlled |
|---|---|---|---|
| 100 | 141,190 | +0.0119 | **+0.0094** |
| 200 | 54,820 | +0.0197 | **+0.0154** |
| 400 | 12,213 | +0.0406 | **+0.0207** |

**Same-side teammate pairs measured the identical way come out at +0.250.**
Matchups are 12–25× less reliable.

**About half the raw signal was the two teams, not the two players.** Division
rivals meet four times a season, so a player-matchup mean carries its teams'
matchup, and team structure persists across halves exactly as a real player
effect would. Removing each (off team, def team, season) cell's mean *within*
each half halves the correlation at the strictest threshold; what survives is
about 2 sem, and the control is conservative because players are nested in
teams. The estimated true sd falls as the threshold rises (0.55 → 0.47), which
is the signature of a quantity that is mostly estimation noise rather than a
real effect being measured better.

Phase 1 called matchup pairs non-identifiable and Phase 5 found every cross-side
model null. This says why, and closes §3.1 without another null model being
written. It is also consistent with §12.2: the non-additive structure that does
exist is same-side and idiosyncratic.

### 12.14 Why the carry-forward is 0.6 when persistence is 0.31

Backlog §5.2, open since Phase 11. `forward_eval` sweeps ρ for carrying last
season's deviation forward and picks **0.6 in all 16 seasons**;
`delta_persistence` measured season-to-season persistence at **0.31**. The naive
reading makes the gap worse rather than better: a fitted δ is measured with
error, so a regression on it is attenuated and the optimal weight should sit
*below* the true persistence, not at twice it.

`delta_decompose.py` reads it off the fitted δ panel — 9,122 player-seasons,
1,690 players, offense, ≥500 possessions:

| quantity | value |
|---|---|
| AR(1) slope of δ on last season's δ | **+0.049** |
| between-player ("standing") share of var(δ) | **6.2%** |
| optimal carry weight, θ fit on the full corpus | **+0.157** |
| optimal carry weight, **θ fit on seasons < T** | **+0.500** |
| what `forward_eval` picks | 0.6 |

**Carrying δ forward does two jobs.** When θ has seen every season it absorbs
the standing part of a player's deviation and there is little left for ρ to
carry. When θ is fitted only on the past — which is what a forecast must do —
θ is stale, and δ_{T-1} carries both the transient recency signal *and* a
correction to an out-of-date career coefficient. That is the factor of three.

It also explains the 6.2%: the standing share looks tiny only because it is
measured after a full-corpus θ has already eaten it. So 0.31 and 0.6 were never
the same quantity, and §5.2's comparison was not valid.

Per-origin slopes are 2014 +0.644, 2018 +0.374, 2022 +0.278, 2024 +0.703 —
noisy at four origins, but far from 0.157 and consistent with 0.6.

**Untested implication.** If most of what ρ buys is a correction to a stale θ,
recency-weighting θ *itself* should capture it more directly. Recency-weighting
the pair block gained exactly nothing (§12.12), but that block is 25% reliable
and this signal is far larger, so the result does not transfer. One forward run
would settle it.

### 12.15 Recency-weighting θ: suggestive, and left there

§12.14 says most of what the carry-forward ρ buys in a forecast is a patch on a
stale θ. The direct fix is to let θ forget — weight each season's Gram block by
0.5^(age/halflife), which is exactly weighted least squares and costs nothing,
because X'X is already block diagonal by season.

`theta_recency.py`, forward protocol, half-life and ρ and the penalties all
chosen on season T-1, 16 origins:

| arm | test r² | vs incumbent | sem | t | seasons + |
|---|---|---|---|---|---|
| incumbent (no decay) | +0.001769 | | | | |
| recency-weighted θ | **+0.001788** | **+0.000019** | 0.000010 | **1.89** | **11/16** |
| let validation choose per season | +0.001782 | +0.000013 | 0.000010 | 1.32 | 8/16 |

The incumbent reproduces the published deployable +0.001769 exactly, which is
the regression check on the rig.

**The mechanism test passes directionally.** If weighting θ is doing the
stale-θ job, ρ has less left to do and its chosen value should fall. It does:
{0.6 in 13 seasons, 0.31 in 3} becomes {0.6 in 9, 0.31 in 7}. Chosen half-life
is 2 seasons in eight origins, 4 in four, 8 in four.

**It does not clear the bar.** t = 1.89 over origins that share training history,
11/16 seasons, sign-test p ≈ 0.11. By rules 3 and 6 that is screening, not a
result, so it is not shipped and not added to the deployable model. Recording it
as suggestive is the honest disposition — the alternative is to quote +0.000019
as a gain, which is exactly the move this project's rules exist to prevent.

The third row is worth its own note: letting validation pick between decay and
no-decay *per season* does worse than always decaying. At 10⁻⁵ effect sizes the
validation season cannot make the call — the same lesson as §12.12.

---

# §13 Does chemistry generalize to lineups that never played? (2026-09-02)

Two accounts of this project were in circulation and they contradicted each
other. One said the tool carried a valuable generalizing chemistry component
worth a few points per 100. The other said no non-additive component
generalizes at all. Both were made about the same repository within days.
**Both were half-right, and the ambiguity that hid the contradiction is a
distinction nobody had drawn: an unseen LINEUP is not an unseen PAIR.**

## 13.1 The distinction that resolves it

`forward_pairs` reports a `novel5` slice — five-man sets that never appear in
training. Free pairs win it: **+0.000017, t=+4.00, 13/15 seasons**, on 88% of
test possessions, a *higher* t than their overall +0.000030. So free pairs do
generalize to unseen lineups, and the claim that nothing does is wrong.

But a novel five in a real season is almost always the same team's players in a
new combination, so its PAIRS are observed even when the FIVE is not:

| unseen pairs | share of novel-five possessions | pair gain |
|---|---|---|
| 0–4 | 61.2% | +0.000011, t=+2.27 |
| 5–8 | 34.6% | +0.000023, t=+1.90 |
| 9–10 | 4.1% | +0.000041, t=+0.97 |

The tool's headline use case is the opposite regime. Only **4.1%** of possible
pairs among its 1,183 players have ever shared a floor, and for five players
drawn at random:

| pool | mean pairs with history | zero history |
|---|---|---|
| all 1,183 | **0.43 / 10** | **65.5%** |
| top 100 by possessions | 1.64 / 10 | 17.1% |

So a cross-team, cross-era superteam gets a chemistry number of exactly zero
about two thirds of the time. That is honest, and §13.3 says it is also
unavoidable.

## 13.2 How big is chemistry, and how big did the old tool say it was

Anchor everything on the one quantity measured forward: free pairs are
+0.000030 r², and var(y)=1.2807, so a calibrated chemistry term carries
`100·√(Δr²·var_y)` = **0.62 pts/100** of spread across lineups. The whole
forecastable non-additive ceiling (+0.00017) is 1.48 pts/100.

Same 40,000 sampled five-man cliques, every pair over 400 shared possessions:

| | sd | p1 / p99 |
|---|---|---|
| OLD bilinear chemistry (10-dim quadratic) | 0.720 | −2.04 / +1.73 |
| NEW measured pair chemistry | 0.483 | −1.06 / +1.23 |
| **correlation between them** | **+0.12** | |

The old term displayed more spread than the entire measured phenomenon, from a
function explaining 0.06% of a pair effect's true variance — about **47×**
over-dispersed. That is how one agent could truthfully report "a few points per
100" and another could truthfully report "nothing generalizes".

(The √10 per-lineup scaling is not an assumption: measured pairs have per-pair
sd 0.153 and per-lineup sd 0.483, and 0.153·√10 = 0.484.)

## 13.3 Width was the last live hypothesis, and it is dead

The incumbent bilinear used ten box-score dims. On a RANDOM game split, the
same functional form on twenty-six dims looked alive and survived every control
that had ever been applied here:

| arm (random split) | Δ over LIN+SELF | t |
|---|---|---|
| p10 + cross | +0.000008 | +1.00 |
| **ind26 + cross** | **+0.000028** | **+2.40** |
| ind26 + cross, base penalties pinned | +0.000022 | +3.08 |
| ind26 + cross, pinned + (team, season) block in the base | +0.000020 | +2.98 |

Forward it is nothing. `forward_pairs --cross --cross-dims ind26`, arms
additive → +free player indicator → +CROSS, both sweeping an identical interior
penalty grid, 15 origins:

| | |
|---|---|
| CROSS over the control, all | **−0.000001 ± 0.000005, t=−0.25**, 10/15 |
| CROSS over the control, novel fives | −0.000010 ± 0.000008, t=−1.31, 5/15 |
| free PAIRS over the same control (re-check) | +0.000030, t=+3.73 |

This is a **powered** null: sem 0.000005 against `forward_synergy`'s 0.000012,
so the 95% interval [−0.000011, +0.000009] *excludes* the +0.000030 that
measured pairs earn. Eval and fit share seasons on a random split, and a smooth
function of five profiles can read roster structure shared between them. Add
this to the list of things a random split invents.

Confirmed independently at the pair level. `pair_predictability`, 3 seeds,
identical flags, out of fold over pairs, un-attenuated:

| f | 10 dims | 26 dims | 26 + height/position |
|---|---|---|---|
| min/max on ball-and-role dims | 2.49% | 2.49% | 2.49% |
| \|difference\| only | 1.91% | 1.68% | 1.59% |
| gradient boosting (bounds smooth f) | 1.19% | 1.13% | 1.07% |
| **sum only — ADDITIVE control** | **1.09%** | **1.23%** | **1.13%** |
| profile bilinear | 0.02% | 0.16% | 0.11% |
| placebos | −0.11% … −0.02% | −0.17% … −0.11% | −0.16% … −0.06% |

Width buys nothing; height and position buy nothing. What ranks is FORM —
complementarity beats products every time, and the bilinear equals its placebo.
Net of its own additive control the honest pairwise content is ~1.3% of a pair
effect's true variance, i.e. **0.07 pts/100** of lineup chemistry. The route to
pricing a novel pair is new FEATURES, and tracking data is still the only
candidate (BACKLOG §1.1).

**The min/max result does not transfer upward.** Summed over five players,
Σ min(z_i,z_j) = Σ(5−k)·z_(k) and Σ max = Σ(k−1)·z_(k) — both linear in the
order statistics, a subspace of ORD, which is null at the possession level
(+0.000003, t=+1.04). Its pair-level score is largely additive leakage.

## 13.4 Value adds up: no diminishing returns to stacking scorers

`index_curvature.py`. The most widely believed non-additive claim in basketball
is not here at any level that predicts.

| arm (offense) | random split | forward split |
|---|---|---|
| free hinges in the lineup total | −0.000004, t=−0.63 | +0.000027, t=+6.05 |
| quadratic only, I², J² | −0.000002, t=−0.49 | +0.000027, t=+9.73 |
| **WHO: the five order statistics of θ** | −0.000004, t=−0.70 | −0.000073, t=−7.29 |
| **WHO: concentration** (sd, max, min, star gap, top-two product) | −0.000015, t=−2.05 | −0.000152, t=−13.7 |
| offense × defence, I·J | +0.000007, t=+1.96 | −0.000016, t=−6.23 |
| PLACEBO, hinges on a shuffled index | −0.000000 | −0.000034 |

The forward-only curvature is not a finding: the binned curve is *concave* on
the random split (−0.752, a −1.48 pts/100 bend across the range) and *convex*
forward (+0.315). A real phenomenon does not flip sign between splits; a
recalibration of a stale additive model does, and half of it dies under a
control for the lineup's information content. The cleanest single number is
that the top decile of lineup strength — where stacking would bite — sits on
the line: +0.006 ± 0.282 pts/100 forward, −0.291 ± 0.276 random.

Concentration is the sharpest version and the deadest. The five order
statistics sum to the total, so that arm is purely "does it matter WHO the
total comes from", and it is null. Two stars and three minimum-salary players
price the same as five solid starters. **The tool's linear extrapolation to a
superteam — the first thing anyone types in — is correct.**

## 13.5 Composition: order statistics, dispersion, counts, size

Nested paired contrasts over LIN+SELF on the same features, random split, so
the number is composition and never the wider additive profile.

| extra over LIN+SELF | p10 | p10+size | ind26 |
|---|---|---|---|
| ord (five order statistics per dim) | +0.000005, t=0.84 | +0.000008, t=1.54 | +0.000003, t=1.04 |
| disp (std, range, max, min) | +0.000008, t=1.38 | +0.000011, t=1.53 | +0.000005, t=0.73 |
| cnt (how many clear each threshold) | +0.000005, t=1.72 | +0.000003, t=1.21 | +0.000005, t=1.16 |
| ord+disp+cnt | +0.000009, t=1.50 | +0.000011, t=1.95 | +0.000007, t=1.05 |

Nothing reaches t=2. Height and a fractional 1–5 position — 100% covered in
`nba.players`, never used in an interaction basis before — add +0.000003
(t=0.91) over their own additive control.

**A control that had been missing for months.** `basis_screen_off.csv`
reported ORD_ind26 at +0.000038, the largest number in the file, and never
screened LIN_ind26. LIN_ind26 is **+0.000036**. The biggest interaction number
in the repo was the wider *additive* profile.

## 13.6 The chemistry term is UNDER-shown by the tool

Regressing each test season's residual on the fitted chemistry term, 15
origins, pooled by sd²·n:

| | slope |
|---|---|
| all possessions | **+1.111** |
| novel five-man sets only | **+1.040** |

A slope of 1 means no further shrinkage is owed — the ridge already did it at
its validation-chosen penalty. But `five.html` computes `oRaw = oAdd +
chemistry` and multiplies the **sum** by `SL_O = 0.447`, the slope measured for
the *additive* rating. Displayed chemistry is therefore about **2.2× smaller
than it earns** (0.450 × 0.447 = 0.20 pts/100 shown against ~0.45 earned).

A second, free improvement: the tool exports pairs at ≥200 shared possessions
while the forward-validated model uses ≥50. Matching it moves coverage from
0.43 to 0.54 of ten pairs known, and zero-history lineups from 65.5% to 58.4%.

## 13.7 Two rig failures worth keeping

**Recalibration must be fitted out of sample.** The first `index_curvature`
fitted the curve on the same games as the additive model. A placebo on a
SHUFFLED player index read **+0.000009, t=+6.25**. A ridge residual correlates
positively with the fitted index in sample and negatively out of sample, so the
coefficient arrives with the wrong sign, the base scores −0.000383, and every
richer arm scores for undoing it. Three splits, not two: fit the model on 50%,
the recalibration on the next 20%, score the last 30%. The placebo then reads
−0.000000. The same defect is why `basis_screen`'s forward split returns a
negative base r² and cannot be used forward at all.

**Compare only runs made with identical flags.** The 26-dim pair-prediction
result was first read against the previous night's 10-dim CSVs and reported as
a 30× gain. Re-running 10 dims with matched flags: no gain at all. The tell was
visible and ignored — the two runs reported different split-half reliabilities
(0.19 vs 0.25) for a quantity computed upstream of the change. A quantity that
should be identical and is not is proof the configurations differ.

## 13.8 Why the bilinear worked on a random split — the mechanism

§13.3 showed the 26-dim bilinear is +0.000022 (t=+3.08) random and −0.000001
forward. Four follow-ups say what the random-split number actually was, and it
is not an artifact in the usual sense.

| test | result | rules out |
|---|---|---|
| gain on SEEN vs NOVEL five-man sets (random split) | novel **larger**: +0.000045 (t=2.51) vs +0.000017 (t=2.26) | lineup memorisation |
| strictly additive spline, same features, 130 cols | +0.000003 (t=1.92) vs +0.000022 | "just extra capacity" |
| cross on top of that spline | +0.000018, t=+2.55 | — |
| spline on top of cross | +0.000001, t=+0.32 | cross subsumes the additive expansion |
| LAG the profile by one season | +0.000022 → **+0.000007** | needs a contemporaneous PROFILE |
| forward split | +0.000022 → **−0.000001** | needs a contemporaneous MATRIX |

The bilinear is a genuinely non-additive function of the five profiles that
requires **both** the profile and the interaction matrix to come from the same
period as the scored possessions. That is within-season form and scheme — real,
and season-local. It is not a transferable law about how player types interact,
which is the only kind of thing a tool pricing a future lineup can use. It also
explains the long-noted instability of CROSS across seasons (+0.000080 in 2010,
−0.000088 in 2012).

**This corrects a stated belief.** `feedback_random_split` holds that a random
split makes *shared* structure look redundant — understated. For a shared
351-parameter basis on contemporaneous features it does the opposite. The
direction of the bias depends on whether the basis's FEATURES are
contemporaneous with the scored data, not only on whether its parameters are
per-(player, season).

## 13.9 Defence closes the same way

The defensive screen was the strongest interaction number this project has
produced — ind26+height/position, +0.000017 (t=+2.57) over a pinned LIN+SELF
base on a random split, against offense's +0.000022. Forward, over the free
per-player un-shrinking control, 15 origins:

| | |
|---|---|
| DEF cross, all possessions | **−0.000005 ± 0.000008, t=−0.62**, 4/15 |
| DEF cross, novel five-man sets | −0.000005 ± 0.000009, t=−0.56, 5/15 |

Both sides of the ball, every width tried, null forward. The bilinear is
finished as a route to pricing an unseen pair.

## 13.10 The range every composition null is conditional on

Asked by the user: five Shaquille O'Neals — is that the best lineup of all
time? The additive model says roughly five times a great player. The honest
answer exposed a qualifier missing from every non-additive statement above.

**Inside the observed range, additivity is not measurably wrong.**
`composition_support.py` bins eval lineups by Mahalanobis distance from the
centre of composition space (28 features: min/max/mean/sd over the five of 3PA
rate, rim finishing, assists, usage, blocks, rebounding, height) and reads the
out-of-sample residual:

| Mahalanobis | mean residual, pts/100 |
|---|---|
| 4.0 | −0.156 ± 0.244 |
| 5.0 | +0.173 ± 0.245 |
| 5.9 | +0.223 ± 0.249 |
| 7.0 | −0.146 ± 0.252 |
| trend | +0.046 per unit, i.e. +0.14 over the whole range |

**But that range is 4 to 11.5, and it is narrow because coaches made it
narrow.** A null measured on pre-filtered lineups is not evidence about a
lineup no coach would select:

| lineup | distance |
|---|---|
| real lineups | median 5.2, p99 8.2, max ever **11.5** |
| five Currys | 13.7 |
| five LeBrons | 14.6 |
| five Draymond Greens | 16.5 |
| **five Shaqs** | **20.9** |
| five Chris Pauls | 21.8 |
| five Goberts | 25.0 |

So the three-part answer: interactions are real (+0.00026 r² of non-additive
budget, of which measured pairs forecast +0.000030); additivity holds where the
data lives; and outside it the model is extrapolating 1.8× past the most
extreme five ever played and should say so. The tool flags missing PAIR
history and is silent on composition — the larger failure mode for exactly the
lineup a user types first.

---

# §14 Ratings go stale: the shrink is drift, not estimation noise (2026-09-02)

## 14.1 The measurement

`slope_by_horizon.py` — fit an EB ridge on seasons ≤ S, read the calibration
slope of the additive index on season S+k, nothing refitted per horizon so the
only thing that varies is the gap. 10 origins, ~2.4M possessions per cell:

| seasons between fit and test | offense | defence |
|---|---|---|
| **k=0 (the fitted seasons)** | **+1.143 ± 0.018** | **+1.248 ± 0.016** |
| k=1 | +0.780 ± 0.038 | +0.803 ± 0.032 |
| k=2 | +0.686 ± 0.032 | +0.708 ± 0.035 |
| k=3 | +0.646 ± 0.033 | +0.648 ± 0.032 |
| k=4 | +0.590 ± 0.039 | +0.615 ± 0.022 |
| k=5 | +0.516 ± 0.037 | +0.547 ± 0.039 |

A slope of ~1.2 in period is not luck. An EB ridge picks its penalty by
empirical Bayes, so `E[y | θ̂] = θ̂` by construction: **estimation noise is
already absorbed by the shrinkage.** Everything lost at k ≥ 1 is drift, and
half the slope is gone within five seasons.

**Offense and defence drift at the same rate.** They are statistically
indistinguishable at every horizon. An earlier version of this section claimed
defence drifts three times faster; that was a missing intercept — see §14.4.

## 14.2 What it unifies

Four results filed separately are one phenomenon — ratings go stale and
freshness is the lever:

| result | what it is |
|---|---|
| `intraseason_regime` | this season's δ is +0.000090 mid-season, exactly 0.000000 season-ahead |
| `carry_forward_resolved` | last season's δ carried at ρ=0.6 is worth +0.000115 |
| `theta_recency` | down-weighting old seasons: +0.000019, t=1.89 |
| `fractional_eval` (§15) | this season's δ is **+0.000164, t=+7.97** at quarter resolution |

`lineup_scoreboard`'s framing — "38% of the tool's rating spread is estimation
noise" — should be read as staleness. That changes which levers are worth
pulling: fresher data, not more of it or better pooling.

## 14.3 The slope does NOT vary with data volume, and the tool's numbers are right

Errors-in-variables predicts the optimal shrink should rise as a lineup's data
grows. Bucketed forward, it does not — the trend is −0.014 per e-fold on
offense and non-monotone on defence. That is the empirical counterpart of
`lineup_uncertainty`'s model-based null (posterior sd varies only 1.3× and
orders calibration backwards). Two routes, one answer: **one global slope per
side.** It is also consistent with §14.1 — a staleness correction should not
depend on sample size.

`slope_reconcile.py` then settled whether the tool's shipped slopes are right,
by running several estimators on the **same** predictions from the **same**
model and split:

| estimator (plain EB ridge, forward split) | offense | defence |
|---|---|---|
| univariate, mean-centred, every cell | 0.541 | 0.731 |
| univariate, cells ≥100 poss (the tool's filter) | **0.402** | **0.685** |
| univariate, cells ≥500 poss | 0.348 | 0.574 |
| **what the tool ships** | **0.447** | **0.591** |

The tool's numbers sit inside that range with the right ordering. **The shipped
slopes are fine.**

## 14.4 A specification error of mine, and what it cost

`slope_by_horizon` and `calibration_by_information` were first written as
`lstsq(column_stack([I, J]), y − icept)` with **no intercept column**, on the
reasoning that the target is already centred. It is only approximately centred
— detrending is done over the whole corpus, not within each evaluation slice —
and the omitted constant is absorbed unequally by the two regressors.

It produced a clean, monotone, entirely plausible finding that **defence drifts
three times faster than offense** (0.743 → 0.352 across five seasons against
offense's 0.864 → 0.735). That was written up before it was checked. With an
intercept the two sides are indistinguishable. The same omission flipped the
offense/defence ordering, which is what made the tool's shipped slopes look
wrong when they were not.

The tell was that two estimators of one quantity disagreed in **order**, not
just level. That is a specification difference, not a discovery, and it should
be chased before either number is believed.

## 14.5 What the box score can and cannot say about a player

`profile_mining.py`: build the profile on half the games, predict θ fitted on
the **other** half so the noise is independent, both directions averaged, every
number un-attenuated by θ's own split-half reliability (0.712 off, 0.693 def).
1,119 players over 2,000 possessions per half.

| prior feature set | offense | defence |
|---|---|---|
| 10 dims (`DEFAULT_DIMS` — the *bilinear's* set) | 63.1% | 42.0% |
| **32 dims = `profile_matrix(which="box")`, what the model ships** | **78.3%** | **52.4%** |
| 32 + height + position | 80.3% | 53.8% |
| PLACEBO, shuffled profiles | −12.7% | −7.4% |

Mind the widths: `profiles_for_games` returns 82 columns — 32 own box-score
dims, 48 on/off (`tm_*`, `d_*`, dropped because they carry teammates), and 2
possession counts. The prior is the 32. `DEFAULT_DIMS` is 10 and belongs to the
matchup work; conflating them understates the prior by 15 points.

**The asymmetry is the finding.** 48% of a player's true *defensive* value is
invisible to his own box score against 22% on offense. That is the strongest
quantitative case yet for tracking data, and it names which: opponent FG% at
the rim while defending, not the offensive columns.

Most useful offensive dims by leave-one-out (what each adds that no other dim
has): usage +3.5%, rorb +1.7%, own_ftr +1.7%, rtov +1.1%, avg_dist +1.1%. Solo,
the strongest are usage 33%, rast 28%, rfoul 27%, ft_pct 24%, r3pa 21% — and
three of those five are **not** in the 10-dim set. Within the 10-dim set,
`rblk` (−0.07%) and `assisted` (−0.31%) contribute nothing once the others are
present.

---

# §15 The user's three ideas (2026-09-02)

Proposed by the user after §13: weight play profiles toward recent play, mine
which stats produce accurate player profiles, and add folds that test on
fractions of seasons so the model and profiles have current data. All three
attack the additive model, which §14 says is where the leverage is.

## 15.1 Fractional-season origins — the best model number in the project

`fractional_eval.py`. Cut each season into K slices; for each slice j, fit on
seasons < T plus slices 0..j−1, select on slice j−1, score slice j. K=4 gives 3
origins per season instead of 1, and the profile is rebuilt from the fit mask,
so at slice j it contains this season's first j quarters — the honest way to
give a model current data, as opposed to the way that made the profile bilinear
look alive (§13.8). 37 origins from 13 seasons:

| lever | vs base | t | seasons |
|---|---|---|---|
| box-score prior | +0.000162 | +6.37 | 31/37 |
| experience curve | +0.000168 | +8.38 | 36/37 |
| prior + exp | +0.000297 | +9.46 | **37/37** |
| **+ this season's δ** | **+0.000437** | **+13.25** | **37/37** |
| + last season's δ at ρ=0.6 | +0.000307 | +8.97 | 35/37 |

**This season's δ alone is +0.000140 (t=+7.63, 34/37)** where season-ahead it is
exactly 0.000000, and carry-forward collapses to +0.000010 (t=+0.71) once
current data exists. Best deployable r²: **+0.002221**, against +0.002114
half-season and ~+0.0017 season-ahead.

δ does *not* grow with more current data — by slice it is +0.000158, +0.000132,
+0.000127. The gain is from having **any** current-season data.

**This answers BACKLOG §1.3.** Variance of the lever within a season across
slices is 1.19e−8 against 4.81e−9 between season means — **2.5:1**. Test
sampling noise dominates genuine season heterogeneity, so extra origins are
real information rather than correlated looks, and every marginal 2–4 sem
result here can be re-tested at 3× the origins.

## 15.2 Which stats make an accurate profile

See §14.5. Headline: a player's own box score explains **78.3%** of his true
offensive rating variance and **52.4%** of his defensive one; height and
position add ~2pp and are currently unused. The 48% defensive gap is the
strongest quantitative case for tracking data in this repo.

## 15.3 Recency-weighted profiles — queued

`profile_matrix` now takes `halflife` and `era`, routing through
`profiles_era_adjusted` (per-season profiles, z-scored within season, distant
seasons down-weighted). `forward_eval --profile-halflife` sweeps it. Note the
baseline is re-run under identical flags rather than compared to the existing
`forward_eval.csv` — §13.7's lesson.

A related result is already in: recency weighting the *fit* (not the profile),
split by side, is significantly **worse** than pooling — −0.000033, t=−2.20,
1/14 against a pooled control. That experiment existed to exploit the drift
asymmetry that turned out to be a missing intercept, and it refutes it from a
second direction. Pooled recency stays suggestive: +0.000022, t=+1.11.

---

# §16 The 5-Shaq rule, and the one interaction that is real (2026-09-02)

The user added a hard requirement to the northstar: a user must not be able to
break the tool with five Shaquille O'Neals and be told it is the best lineup of
all time; the tool must extrapolate gracefully to *all* unseen lineups.
Refusing to answer is explicitly not gracefulness.

## 16.1 Why it is hard

Every composition effect measured here is null, and every one of those nulls is
measured over Mahalanobis 4–11.5 in composition space (§13.10). Five Shaqs is
20.9. So the rule cannot be met by fitting composition effects from the
observed spread — there is no signal there, and extrapolating a null four times
past its support is not a model. It points instead at structure that holds **by
construction**.

## 16.2 Usage conservation — the first composition structure to survive forward

A possession has one ball, so the five usage shares must sum to 100% whoever is
on the floor; the additive model is fitted on each player at *his own usual
usage* and then adds five of them as if all five could keep it. Give the model
hinges in the unserved part of demand, `D = Σ career usage rates`:

| | |
|---|---|
| forward, all possessions, 15 origins | **+0.0000100 ± 0.0000021, t=+4.84, 14/15** |
| forward, novel five-man sets | +0.0000094, t=+4.30, 13/15 |
| random split, over a 26-dim profile LIN+SELF control | +0.000021, t=+2.88 |
| placebo, hinges on shuffled usage | −0.000000, t=−0.79 |
| in points per 100 of lineup spread | **0.358** |

**The fitted shape is face-valid and nobody put it there by hand.**
Coefficients on standardised columns: `max(D−1.0,0)` +0.155, `max(D−1.1,0)`
−0.286, `max(0.9−D,0)` −0.225. The two upper hinges share a variable at
adjacent knots, so their individual signs are not interpretable — the composite
slope above D = 1.1 is **−0.131**, negative exactly as the conservation
argument predicts an over-subscribed lineup should be. The third hinge says
*under*-subscribed lineups are penalised too. So the shape is a U: a lineup
wants enough shot creation to fill its possessions and not so much that its
players fight over the ball, with the optimum around D ∈ [1.0, 1.1] — which is
where real lineups actually sit (median 1.119). That is basketball read out of
sample from a basis whose only input was "one ball, five shares, they sum to
one".

It is the **only** structure in Phase 13 positive and significant on *both*
splits with a clean placebo. That also disposes of the obvious confound: a
staleness proxy would vanish on a random split, where fit and eval interleave
in time. 0.36 pts/100 against 0.62 for measured chemistry — but unlike
chemistry it applies to every lineup, including one whose ten pairs have never
met.

## 16.3 Named interactions: the ball, and nothing else

Five interactions named from basketball theory **before looking**, one column
each, with signs pre-registered. Solo gains over a 26-dim profile control:

| term | dims | delta | t | joint coef | predicted sign |
|---|---|---|---|---|---|
| spacing | shot_rim × r3pa | −0.000001 | −0.44 | +0.040 | + ✓ |
| creation | rast × assisted | −0.000003 | −0.60 | +0.077 | + ✓ |
| **usage conflict** | **usage × usage** | **+0.000012** | **+1.79** | **−0.113** | **− ✓** |
| handler+scorer | rast × usage | +0.000005 | +1.03 | −0.073 | + ✗ |
| floor spacing | r3pa × r3pa | −0.000000 | −0.92 | +0.004 | + ✓ |

All five together, forward, 15 origins: **+0.0000068, t=+1.73, 12/15** —
suggestive, not a result, and faded from t=+3.65 at 7 origins. Five named
interactions clearly beat 351 fitted ones (§13.3 is −0.000001) but not
decisively.

**The convergence is the finding.** §16.2 reaches the same mechanism from a
conservation argument and §16.3 from theory, and both isolate competition for
the ball. Nothing else survives. That makes sense: the ball is the only
conserved resource on a possession. Spacing and defensive attention are not
conserved, and within the range coaches occupy every lineup already carries
enough shooting for the effect to be unmeasurable.

## 16.4 Where that leaves the rule

Five Shaqs' problem is **spacing**, and spacing is null. The one mechanism that
is measurable does not separate the case: D = 1.590 for five Shaqs against a
real-lineup maximum of 1.631, and 1.605 for five Currys. So the rule cannot
currently be met by any measured effect.

The remaining route is **distance-aware shrinkage** — degrade gracefully toward
the league mean as a lineup leaves the support, the way a Gaussian process
does — with the usage term underneath it. That satisfies the letter of the rule
and is honest about why: not "five Shaqs is bad because of spacing", which the
data cannot support, but "this lineup is 1.8× outside anything ever played and
the model reverts to what it knows."

**Caveat on all of §16 and §13.** Every interaction result is measured against a
deliberately stale season-ahead baseline. §14 says drift dominates. Running
these blocks in the intra-season regime (§15.1) is the outstanding check.

---

# §17 The staleness caveat, discharged for the two results that matter (2026-09-02, night)

§16.4 closed with a caveat covering every interaction number in §13 and §16:
they are all measured against a season-ahead baseline that is stale by
construction, and §14 says drift dominates. The user put it more sharply —
*"maybe we should stop judging based on full season evals?"* — and it was made
the top backlog item, because it does not merely add a result, it re-grades
every interaction in Phase 13.

## 17.1 A cheaper and sharper test than re-fitting

The planned fix was to re-fit at intra-season origins so the baseline is at
most a quarter-season stale. That is the right *deployable* number but it is
the wrong *diagnostic*, because it changes the fit and the evaluation at the
same time and the contrast then confounds them.

`slice_horizon.py` holds the fit completely constant instead. Fit once per
season exactly as `forward_pairs` does — additive model on <= T-1, penalties
chosen on T-1, interaction block fitted on that model's residual — and then
score season T in four calendar quarters. The model, the penalties, the pair
set and the residual the block was fitted on are bit-for-bit identical across
the four looks. The only thing that varies is how stale the baseline has
become by the time it is scored, so:

> a COMPOSITION effect is flat in the slice index; a STALENESS effect rises,
> because there is more drift to absorb in April than in November.

It also costs one extra scoring pass over a fit that had to happen anyway.

## 17.2 The result: both survive

| block | overall gain | slope per slice | sem | pure-staleness slope | sem away |
|---|---|---|---|---|---|
| free pairs | +0.0000279 | +0.0000015 | 0.0000035 | +0.0000186 | **5.0** |
| usage demand | +0.0000075 | −0.0000000 | 0.0000006 | +0.0000050 | **8.3** |
| player (control) | −0.0000021 | +0.0000001 | 0.0000005 | — | — |

"Pure-staleness slope" is the arithmetic benchmark: what the slope would have
to be if the entire gain were drift-absorption — zero at the start of the
season, twice the mean by the end. Both blocks sit 5–8 sem below it. These are
powered nulls, not absences of evidence.

The null is meaningful because **there was real drift to absorb**: the additive
r² falls 15% across the test season, +0.001830 at slice 0 to +0.001558 at slice
3. The baseline does go stale. The interaction blocks simply are not paid for
it.

**What does NOT calibrate the test.** The free per-player `player` arm is flat
too, but it cannot track drift either — fitted on <= T-1 it has no season-T
data and can only undo shrinkage. The discriminating comparison is the observed
slope against the arithmetic benchmark, not against the player arm.

**Still open.** The sparse bilinear (`--cross --cross-topk 10`) is the block
whose per-season series actually decays (2010 +29 … 2019 −29, in 1e-6) and the
one that prompted the concern. Its slice-horizon run is the outstanding check,
and it is the expensive one because the 351-column cross block has to be built
twice per origin.

---

# §18 Floor geometry, and the difference between predicting and extrapolating (2026-09-02, night)

## 18.1 The second conservation constraint

CLAUDE.md's northstar says the 5-Shaq rule "points at constraints that hold by
construction (**a possession has one ball and one shot**)". §16.2 built the
ball — usage demand, +0.000010 forward. The shot half had never been built.

A player's six shot-location shares sum to one, so a lineup's implied shot map
is a usage-weighted average of five points on the same simplex, and five copies
of one player put every shot in one man's distribution **by construction**.
`geometry_block` carries the mean and minimum pairwise total-variation distance
between the five maps, the Herfindahl and largest share of the implied mix, and
height spread.

Measured before fitting anything, over cells with ≥50 possessions:

| feature | real p1 | p50 | p99 | max | five of one player |
|---|---|---|---|---|---|
| div_mean | 0.156 | 0.307 | 0.449 | 0.532 | **0.000, all of them** |
| div_min | 0.032 | 0.104 | 0.222 | 0.305 | **0.000, all of them** |
| herf | 0.209 | 0.237 | 0.306 | 0.409 | 0.254 Shaq, 0.730 Gobert |
| maxshare | 0.256 | 0.331 | 0.454 | 0.584 | 0.292 Shaq, 0.845 Gobert |

It flags **every** degenerate five where usage flagged only five Currys and
concentration only five Goberts — Shaq's own shot map is not concentrated; he
shot from the rim, the paint *and* the mid-range. And five Shaqs lands 0.156
below a range 0.376 wide, so pricing it is a ~40%-of-range extrapolation rather
than the 1.8× that Mahalanobis distance implies (§13.10).

## 18.2 It predicts, and the two constraints are independent

Forward, 16 origins, offense, over the free per-player un-shrinking control:

| arm | gain | t | seasons |
|---|---|---|---|
| floor geometry | **+0.000010** | **+3.37** | 15/16 |
| … on novel five-man sets | +0.000009 | +2.91 | 14/16 |
| **geometry + usage demand jointly** | **+0.000020** | **+5.13** | 15/16 |

**Exactly additive.** One ball and one shot are independent information, not
one effect measured twice. Together ~12% of the forecastable ceiling, next to
free pairs at 16%.

Four checks passed: a shuffled-profile **placebo** (−0.000002, t=−1.22),
**interiority** (grid widened twice, ending with λ=0 in it — same answer,
+0.000009 t=+3.40, λ=0 chosen at 10/16), **staleness** (§17: slope per slice
3.7 sem below the pure-drift benchmark), and defence, where it is correctly
null (−0.000001, t=−0.88) because a defender's own shot map says little about
whom he can guard.

## 18.3 And the sign is backwards, which kills the northstar claim

The signs were written down before the fit: div_mean +, div_min +, herf −,
maxshare −, height_sd +. **Two of five came back right**, and the two largest
terms came back inverted — div_mean −0.071 pts/100 per sd, height_sd −0.179.
Fitting each column alone gives the same signs, and the columns are nearly
orthogonal, so this is the marginal relationship and not a collinearity
artefact.

The reading is not mysterious. **Uniform lineups score better** — five
interchangeable 6'6"–6'9" players who can all shoot is the modern positionless
five, and high height spread is a 7-footer next to a 6'1" guard, the
traditional and less efficient shape. The additive model prices each player
alone and misses the lineup-level shape, so the block finds real signal.

Extrapolated, that slope hands five copies of anyone a **positive** adjustment
at the 100th percentile of real lineups:

    real lineups (>=50 poss)   p1 -0.51   p50 +0.00   p99 +0.42 pts/100
    five Jermaine O'Neals      +0.98      five Chris Pauls   +0.91
    five Rudy Goberts          +0.89      five LeBrons       +0.74
    five Stephen Currys        +0.59

**So the feature that separates degenerate lineups by construction separates
them in the wrong direction.** The model learned "uniform height means
small-ball means good" from lineups that were uniform *and* perimeter-oriented,
then applied it to a lineup that is uniform and enormous.

**The lesson generalises past this block.** Being extreme out of range is not
enough; the *sign* has to survive the trip, and a feature that measures how
much uniformity there is cannot know what kind. The two columns that encode
*direction* rather than spread — herf and maxshare, where the implied mix piles
up — do carry the predicted negative sign marginally. That is the thread to
pull. Predictive value and the 5-Shaq rule are separate claims, and this block
earns the first while failing the second.

## 18.4 The joint neural question, answered without SGD

Asked by the user: was a net ever learned **jointly** with the player
coefficients, with the profile as the embedding start? The strongest form of
that question needs no SGD. Expand the 32-dim prior with all pairwise products,
orthonormalise that block separately so it carries its own penalty, and the
existing Schur collapse fits γ and β jointly — exact, no seeds, no val-noise
floor, nested (α_quad → BIG is bit-for-bit the linear prior).

**−0.0000022 ± 0.0000047, t=−0.46, 16 origins.** The 95% CI upper bound
(+0.0000071) is below the effects that do work in the same rig, so it is a
powered null. The penalty was interior at both ends (0/16 at BIG, 0/16 at the
floor). Twelve of sixteen origins are positive but small, with the mean dragged
negative by three large losses — added variance, not added signal.

This is the **SELF** basis; **CROSS** was already a powered forward null. Both
halves of the profile quadratic are now closed. If a second-order expansion of
the 32 box dims adds nothing when fitted jointly and exactly, a deeper network
on the same inputs is unlikely to; the remaining route for a learned
representation is new **inputs**, not a richer function of these.

## 18.5 The sparse bilinear was a test-set leak

`code` maps possessions to cells: its values are cell indices, its length is
n_possessions. `forward_pairs` fed `np.isin(season, sel_fit)[code]` — a
per-possession mask indexed by cell ids — into the top-k cell selection. That
reads the mask at positions 0..294,754, all from 2002-03, all inside every fit
window, so it came back **100% True** and the selection saw 1.5M test-era
possessions.

Leaked: +0.0000153, t=+2.70. Clean, in `slice_horizon`: **+0.0000028.** ~82% of
the effect, on what was the project's live lead. The fit and the scoring were
both clean; only the *basis selection* was contaminated, which is why "is this
forward?" passed. It was caught because two rigs disagreed on the same protocol
with the same grid — a gap between two implementations of one quantity is
evidence, not noise.

---

# §19 The fresh-baseline re-grade, and a cheap screen that predicted it (2026-09-03)

## 19.1 The test

§17 answered the *diagnostic* question by holding one fit constant and scoring
the test season in quarters. §19 is the *deployable* version.
`fractional_pairs.py`, for each season T and slice j:

    fit    seasons < T, PLUS slices 0..j-1 of season T
    select slice j-1 of T
    score  slice j of T

45 origins at K=4, ~20s each, because the Gram is block diagonal by season so a
prefix of T is just a narrower block. **The fresh baseline is a much better
model** — additive +0.002026 against +0.001701 season-ahead — so there is less
room for anything on top of it. That is what makes it the honest test rather
than an easier one.

## 19.2 Three survive, one dies

| block | stale baseline | fresh baseline | §17 slice verdict |
|---|---|---|---|
| free pairs (off) | +0.000028, t=+3.6 | **+0.000034, t=+3.98**, 36/45 | composition, 5.0 sem |
| floor geometry (off) | +0.000010, t=+3.37 | **+0.000008, t=+3.50**, 33/45 | composition, 3.7 sem |
| usage demand (off) | +0.000010, t=+4.85 | **+0.000007, t=+4.03**, 33/45 | composition, 8.3 sem |
| defensive coverage | +0.000005, t=+1.93 | **+0.000002, t=+0.80**, 28/45 | **staleness, 0.0 sem** |

**The cheap screen predicted all four.** `slice_horizon` costs one extra
scoring pass over a fit that had to happen anyway; `fractional_pairs` costs a
full re-fit at every origin. Blocks whose gain was flat across the test season
survived a current baseline; the one whose gain rose at exactly the pure-drift
rate did not. Run the screen first on anything new.

**Free pairs get bigger on a fresh baseline**, which is the opposite of what a
drift-absorber does, and agrees with `pair_drift`: chemistry is only 31%
persistent across a decade, so a fresher fit measures it better.

## 19.3 What this costs the defensive result

`defensive_coverage` was the most northstar-relevant finding of the night — the
first defensive composition structure with any signal, six of six marginal
signs matching a pre-registration, a clean placebo, and the only structure
pointing the RIGHT way for the 5-Shaq rule (five copies of anyone: +1.16
pts/100 allowed, at the 100th percentile of real lineups). It does not survive
a baseline that is current. The sign result stands as a description; the r² does
not.

That is the second time in one session that the most attractive-looking result
turned out to be an artefact of how it was measured — the first being the
sparse bilinear's selection leak (§18.5). Both were caught by a check that cost
less than the result did.

## 19.4 On the baseline a deployable model would actually use

The fresh baseline above is still static (α_delta = BIG). The best fractional
model carries **this season's δ**, fitted on the slices already seen — the
biggest lever in this regime (§15.1). Validation switches it on at 30 of 45
origins and it lifts the additive baseline to +0.002104.

| block | fresh baseline | fresh + this season's δ |
|---|---|---|
| usage demand | +0.000007, t=+4.03 | **+0.000006, t=+2.48**, 31/45 |
| floor geometry | +0.000008, t=+3.50 | +0.000003, t=+1.24, 28/45 |
| free pairs | +0.000034, t=+3.98 | +0.000005, t=+0.60, 29/45 |

**Only usage demand clearly survives**, and the reason is mechanical rather
than statistical. δ is a per-(player, season) deviation, so "these two are
playing well together this year" shows up as both players' δ, and measured pair
chemistry is largely the same information seen from the other side. Usage
demand is not: it is a constraint on how five usage rates fit around one ball,
and it does not depend on how anyone is playing this season. That is the
argument for the conservation class, made by measurement rather than by taste.

**Caveat, biasing all three the same way.** With δ on, the block is fitted on a
partly in-sample residual — δ over-fits the fit window and is then applied out
of sample — which is exactly what `forward_pairs` avoids by pinning α_delta to
BIG. These are lower bounds. The ordering is informative because all three
carry the same bias; the levels are not. A clean version fits δ on slices
< j−1 and the block on slice j−1, at the cost of a slice of data.

## 19.5 What the tool should print

Four arms deep — additive → player → usage demand → demand + free pairs — which
is the question the product actually has to answer:

| baseline | demand over player | pairs over demand |
|---|---|---|
| static fresh | +0.000007, t=+4.03 | **+0.000025, t=+2.48**, 32/45 |
| fresh + this season's δ | +0.000006, t=+2.48 | **−0.000004, t=−0.49**, 28/45 |

**Measured chemistry is worth printing only when the model does not already
know how the players are performing this season.** Give the model this season's
δ and free pairs add nothing over the conservation term; take δ away and
chemistry is the larger of the two. Usage demand survives both, because it
constrains how five usage rates fit around one ball rather than describing form.

For the tool as it stands — which prices hypothetical lineups from career
ratings, with no current-season δ for a five that has never played — the
static-fresh row is the relevant one, and chemistry belongs on the page. For a
tool asked about a real lineup in a live season, it does not.

---

# §20 What the tool actually prints, and a fourth wrong-signed structure (2026-09-03)

## 20.1 The 5-Shaq rule has been argued about in the wrong units

Every number on the record for this rule — real lineups p1 −8.8 / p50 +7.1 /
max +30.2, five LeBrons +49.6 — comes from `five_shaq_audit.py`, which prices
lineups with the **raw additive model**. The tool does not print that. It
prints `(oAdd + chemistry) × 0.447` and `dAdd × 0.591`. So the requirement is a
statement about numbers nobody had computed.

`tool_audit.py` reads the shipped `DATA` blob out of `tool/five.html`,
reimplements the page's arithmetic exactly, and prices every real five-man unit
in the corpus the same way. Real units with ≥50 possessions, **as the tool
prints them**:

| | p1 | p50 | p99 | max |
|---|---|---|---|---|
| offense (×0.447) | −2.15 | +2.60 | +7.67 | **+10.90** |
| defence (×0.591) | −4.51 | +0.56 | +5.76 | **+8.84** |
| **net** | −4.64 | +3.21 | +11.22 | **+15.64** |

Face validity first: the Warriors' death lineup prints **+13.64**, the 99.95th
percentile of real units, and the 2014 Spurs **+12.68**. Those are right.

## 20.2 The tool is broken by REPETITION, not by excellence

| lineup nobody fielded | oProj | dProj | net | percentile of real |
|---|---|---|---|---|
| five Nikola Jokićs | +14.13 | +11.63 | **+25.76** | 100.00% |
| five LeBron Jameses | +18.02 | +5.62 | **+23.64** | 100.00% |
| five Kevin Garnetts | +4.81 | +18.41 | +23.22 | 100.00% |
| five Rudy Goberts | +1.27 | **+21.09** | +22.37 | 100.00% |
| five Chris Pauls | +16.48 | +4.86 | +21.34 | 100.00% |
| five Draymond Greens | +3.74 | +17.13 | +20.87 | 100.00% |
| five Stephen Currys | +18.19 | −0.59 | +17.60 | 100.00% |
| five Shaquille O'Neals | +2.49 | +6.93 | +9.42 | 95.93% |
| **the 5 best DISTINCT offensive players** | +17.59 | −1.85 | **+15.74** | 100.00% |
| the 5 best DISTINCT defensive players | +1.13 | +18.59 | +19.72 | 100.00% |

**Five different superstars price sanely.** Curry + LeBron + Nash + Harden +
Lillard comes to +15.74 against a real maximum of +15.64 — a superteam that
edges the best unit ever measured is not an absurd answer. It is five *copies*
of one player that breaks the page, by 35% to 65%.

That is a sharper statement of the requirement than "extrapolate gracefully",
and it says what the safety device has to be a function of. Two consequences:

- **The rule is not primarily an offensive problem.** The write-up frames it
  around the ball — one possession, five usage shares — but four of the seven
  worst cases are driven by the DEFENSIVE sum, where no conservation law
  applies at all: five Goberts allow 21.09 fewer points per 100 on their own.
- **The duplication curve is exactly linear.** k copies of one player plus
  (5−k) league-average fillers gives k × (one player's contribution), to
  machine precision, for every k. The model contains no duplication penalty of
  any kind, which is what makes the failure mode reachable in one click.

## 20.3 Index curvature is entirely DEFENSIVE, and it points the wrong way

`index_curvature.py`'s recorded verdict is "value adds up: curvature flips sign
between splits". That verdict came from a **pooled** arm and a binned readout
of the offensive index only. Splitting the arm by side, forward, over the same
three-way split:

| arm (nested on base = I, J linear) | Δr² | t |
|---|---|---|
| + quadratic, both sides: I², J² | +0.000027 | +9.73 |
| **+ quadratic, OFFENSE only: I²** | **+0.000000** | **+0.59** |
| **+ quadratic, DEFENCE only: J²** | **+0.000026** | **+9.79** |

All of it is defensive; offense is exactly flat. Over the information control
(`I, J, logN, logN·I, logN·J`, which absorbs "a lineup of stars is shrunk
less"):

| | Δr² | t |
|---|---|---|
| control + quadratic, DEFENCE only | **+0.000006** | **+3.63** |
| control + quadratic, OFFENSE only | −0.000006 | −2.55 |
| control + PLACEBO, quadratic on a shuffled index | −0.000024 | −3.66 |

So ~77% of the raw curvature is the shrinkage confound and the rest survives it
with a clean placebo. The binned defensive curve is concave (−10.4 on the
binned quadratic, −3.88 pts/100 of bend across the observed range), and the
best-defence decile beats its own linear fit by 1.03 ± 0.28 pts/100.

**And that is the wrong sign.** J is signed so a good defender is negative, so
concavity means *the best defences beat their linear prediction*. Extrapolated,
the fitted curve takes five Goberts from saving 35.7 points per 100 to saving
**50.6**. It is a real forward effect that makes the northstar failure worse.

It is also absent on a random split (−0.000002, t=−0.49), which points at
staleness or selection rather than a structural nonlinearity — the same
signature as every other block whose gain lives only in the forward regime.

## 20.4 The multiplicative conservation constraint, and why the screen was wrong twice

`demand_block` is the **additive** form of "a possession has one ball": hinges
in D = Σ of the five career usage rates, the same penalty whatever the lineup
is worth. The **multiplicative** form is what the argument actually implies. A
player's rating is estimated at his own usual usage share; in a lineup of
demand D the five shares ration to u_p/D, so if a fraction φ of his value is
exercised per possession *used*,

    I(lineup)  ->  I * (1 - phi + phi * Dbar / D)

which is one column, `C = I * (Dbar/D - 1)`, with coefficient φ. It is the only
structure in this project whose extrapolation is bounded **by construction**:
as D grows the correction tends to −I, so it zeroes the index and can never
flip its sign. Pre-registered φ > 0.

On a single 50/50 forward split it reads φ = **+0.943** — the pre-registered
sign, near the theoretical magnitude — with an r² contrast of −0.000003
(t=−1.44), and an imposed sweep that falls monotonically (φ=1 costs −0.000007,
t=−5.06). Rerun with usage built from the whole corpus (`--usage-all`, a leak
on purpose) it reads φ = **+1.176** and the imposed sweep turns positive with
an interior optimum near φ ≈ 0.5–0.75.

**The two disagree because a 50/50 forward split measures usage on 2002–2013
only**, so every player who debuted later falls back to the median and D is
attenuated for exactly the lineups being scored. Neither number is usable: one
has a mismeasured feature, the other a leak. `forward_pairs --scale` rebuilds
usage from seasons ≤ T−1 at every origin and is nested over the demand hinges,
so it has neither defect; that is the reading to believe.

## 20.5 Four structures, one pattern: selection on the outcome

| structure | in-range signal | sign for the 5-Shaq rule |
|---|---|---|
| floor geometry (shot-map diversity) | +0.000008, t=+3.50 fresh | **inverted** — five copies get a bonus |
| defensive index curvature (§20.3) | +0.000006, t=+3.63 controlled | **inverted** — five Goberts get better |
| defensive coverage (height/position) | dies on a fresh baseline | correct, but not established |
| usage scaling (§20.4) | not yet clean | correct by construction |

The first two are the ones with real, controlled, placebo-clean forward signal,
and both extrapolate the wrong way. That is not bad luck. **Lineups are
selected on the outcome**: a coach fields an unusual five only when it works,
so within the observed range "unusual" and "extreme" are correlated with
"good", and any effect fitted from observed lineups inherits that sign.
Extrapolating such a fit past the support is therefore not merely unsupported —
its bias has a known direction, and it is the wrong one.

This upgrades the standing conclusion. `distance_shrink.py` showed the
graceful-degradation schedule cannot be *fitted*; §20.5 says it cannot be
fitted **in principle** from observational lineup data, because the only
lineups that exist are the ones someone chose. The safety device must be
asserted, and asserting it is the correct thing to do rather than a compromise.

---

# §21 Height and position in the prior: the largest additive lever since the debut-year fix (2026-09-03)

## 21.1 It was measured overnight and never read

`run_idea1.sh` ran `forward_eval --prior-bio` at the end of the 2026-09-02/03
session and wrote `fwd_prior_bio.csv`. Nobody opened it. Paired against
`fwd_prof_flat.csv`, which was produced by the same script with the same
arguments and no other difference — `base`, `exp` and `timevar` agree to
**1e-15**, so the comparison is matched in the sense
[[feedback-matched-flags]] demands:

| arm | flat | + height/position | Δ | sem | t | seasons |
|---|---|---|---|---|---|---|
| **the prior lever** (prior − base) | +0.000175 | **+0.000246** | +0.000071 | 0.000024 | **+2.96** | 14/16 |
| prior | +0.001497 | +0.001568 | +0.000071 | 0.000024 | +2.96 | 14/16 |
| all | +0.001593 | +0.001636 | +0.000044 | 0.000012 | +3.69 | 13/16 |
| **all_cf (the full stack)** | **+0.001693** | **+0.001736** | **+0.000043** | 0.000011 | **+3.88** | **13/16** |

**+0.000043 on the full stack is 0.74 points per 100 of lineup spread** — more
than measured chemistry (+0.000034, 0.66), floor geometry and usage demand
combined, and the largest single lever since the true-debut-year data fix.

`profile_mining` already had the player-level version of this: the box score
explains 78.3% of a player's true offensive rating and 52.4% of his defensive
one, and adding height and position takes those to 80.3% and 53.8%. That was
recorded as "~2pp and currently unused". It is worth 0.74 pts/100 in the
harness.

`prior_shape_nulls` records position as null. That measurement predates forward
evaluation and is superseded.

## 21.2 It survives a fresh baseline

The check that killed defensive coverage: fit through slice j−1 of the test
season and score slice j, so the baseline is at most a half-season stale.
`fractional_eval --slices 2`, 16 matched origins against `frac_k2_flat.csv`
(`base` and `exp` identical to 6e-16):

| arm | flat | + height/position | Δ | sem | t | seasons |
|---|---|---|---|---|---|---|
| prior lever | +0.000175 | +0.000200 | +0.000025 | 0.000025 | +1.00 | 10/16 |
| all_nodelta | +0.002036 | +0.002058 | +0.000023 | 0.000012 | +1.98 | 11/16 |
| all_delta | +0.002134 | +0.002157 | +0.000023 | 0.000010 | **+2.34** | 13/16 |
| **all_cf** | +0.002048 | **+0.002077** | **+0.000028** | 0.000011 | **+2.56** | **13/16** |

Smaller, as everything is against a baseline that is already a better model
(+0.002048 against +0.001693), and it holds on both deployable arms at 13/16
seasons — a sign test at p = 0.021. The isolated prior lever weakens to t=+1.00,
so what survives freshening is the gain *in the stack*, not the lever measured
alone.

Two things that make this conservative rather than optimistic:

- **Height and position owe nothing to what happened on the floor.** They come
  from `nba.players`, are known before a player takes a possession, and carry
  no outcome information, so there is no leak to look for.
- **The penalty grid cannot express what the wider prior wants.** Both rigs
  sweep `a_gamma ∈ {1e6, BIG}` — on or off — and 1e6 was chosen when the prior
  was 32 dims a side. `roster_dims` adds height, height² and 17 position
  dummies, so the bio arm is fitted at a penalty tuned for a narrower block.
  That biases the measurement **down**.

There is an obvious improvement left on the table: `position` in `nba.players`
is a **number** on the 1 = point guard to 5 = centre scale with quarter steps,
and `roster_dims` one-hots it into 17 dummies. A linear and quadratic term
would spend 2 columns instead of 17 and would order the scale correctly.

## 21.3 Why this is the right kind of lever for the northstar

The tool prices lineups that never played, and its weakest numbers are the
players with the thinnest records — exactly where the prior does the work, and
exactly where a fact known before a player debuts is worth most. It is also the
first material progress on the gap `profile_mining` named: 48% of a player's
true *defensive* value is invisible to his own box score, and height is the
cheapest available piece of it.

## 21.4 Multi-lag carry-forward: null

The stack carries **one** season's deviation forward, `θ + 0.6·δ_{T−1}`, and
discards every earlier season. If δ is a noisy read on slowly-moving form then
a player whose last three deviations all point the same way is a better bet
than one whose last one does, and `carry_forward_resolved` gives a reason to
expect structure there: with the prefix-fit θ a forecast must use, the optimal
one-lag weight is 0.500, well above the +0.31 persistence of δ itself.

`forward_eval --multilag` adds geometric schedules `w·λ^(k−1)` over lags 1–4,
normalised so the TOTAL carried weight matches a one-lag ρ — so the contrast is
"spread the same carry over several seasons", not "carry more". The schedules
join the same validation sweep the one-lag ρ values are already in, so the arm
is nested and validation can still choose lag-1-only. 16 origins, matched to
`fwd_prof_flat.csv` (`base`, `prior`, `exp`, `all`, `timevar` all identical):

| arm | lag 1 only | multi-lag | Δ | t | |
|---|---|---|---|---|---|
| timevar_cf | +0.001437 | +0.001442 | +0.000005 | +1.83 | 5/16 better, 10 identical |
| **all_cf** | +0.001693 | +0.001691 | **−0.000002** | **−0.42** | 3/16 better, 10 identical |

Validation chose a multi-lag schedule at 6 of 16 origins and was wrong at
almost all of them — the same signature as the pair-recency sweep, which picked
a decay in 10/16 seasons and lost every time. At 1e−5 effect sizes the
validation season cannot tell these schedules apart.

So the one-lag carry-forward is not throwing information away. δ's usable
content really is concentrated in the most recent season, which is what
[[ratings-go-stale]] says it should be: the signal is recency, and the season
before last is already stale.

---

# §22 The multiplicative conservation column is null, and the default penalty grid was a trap (2026-09-03)

## 22.1 The clean reading

§20.4 left the multiplicative form of the one-ball constraint undecided,
because the two screens available disagreed for a reason that was a property of
the screen and not of the world. `forward_pairs --scale` settles it: 16 rolling
origins, usage rebuilt from seasons ≤ T−1 at every origin, the column nested
directly over its own additive form so the contrast is the interaction and not
a main effect of demand, and the penalty grid reaching λ = 0.

| arm | test r² | vs prev | sem | t | seasons |
|---|---|---|---|---|---|
| additive | +0.001701 | | | | |
| player (un-shrinking control) | +0.001699 | −0.000002 | 0.000001 | −1.46 | 3/16 |
| **player_demand** (hinges in D) | +0.001709 | **+0.0000103** | 0.0000021 | **+4.99** | 15/16 |
| **player_demand_scale** (+ I·(D̄/D−1)) | +0.001709 | **−0.0000001** | 0.0000034 | **−0.02** | 10/16 |

A **powered null**: the 95% interval is ±0.0000067, which excludes an effect
the size of free pairs (+0.000034) or of usage demand itself. So the ball
constraint is real in its ADDITIVE form and adds nothing in its MULTIPLICATIVE
one — a level shift when demand cannot be served, not a rescaling of what the
lineup is worth. That agrees with the imposed-φ sweep in `index_curvature`,
where every φ > 0 lost monotonically.

For the 5-Shaq rule this closes the last route that looked like it might be
*measured* rather than asserted. The multiplicative correction remains the only
correction whose extrapolation is bounded by construction, but imposing it is a
choice the data does not support and mildly contradicts.

## 22.2 The default `--lam-cr` grid floor was three decades too high

`player_demand` first came back at **+0.0000000 (t=+2.09)** against the
published **+0.0000103 (t=+4.85)**, with `additive` and `player` identical to
the published run to the last digit. Two implementations of one quantity
disagreeing is evidence, so the control was run: `--demand` alone, current
code, no other flag. It reproduced the *failure*, which ruled out the new
`--scale` wiring and pointed at the environment.

The cause is in the log of the published run: it chose a `cr` penalty of
**100** at every origin. `--lam-cr` defaulted to `[1e5 … 1e10]`, so the block
was being fitted at a penalty **a thousand times stronger than it wants**, and
with the grid floor at 1e5 the selection sat on the boundary at 10 of 16
origins. Every published block run passed an explicit widened grid — the
geometry runs used `0 1 100 1e4 1e6 1e8 1e10 1e12`. The DEFAULT was the trap,
and it was only ever exercised by a run made today.

Rerun with `--lam-cr 0 1 100 1e4 … 1e10`, validation picks λ = 0 at 10 origins
and λ = 100 at 3, and the published +0.0000103 (t=+4.99, 15/16) comes back
exactly.

The default is now `[0, 1, 100, 1e4 … 1e10]`. This is the fourth appearance of
CLAUDE.md rule 10 in three sessions, and the first where the boundary was in a
DEFAULT rather than in a hand-passed grid — which is worse, because a default
is invisible in the command line and in the write-up. **Print the selected
penalty against both ends of its grid on every run, and treat a default grid as
un-audited until a run has walked off it.**

---

# §23 One ridge penalty for every player: usage is not the missing axis (2026-09-03)

The additive model shrinks every player's career coefficient by the same
`a_career`. The optimal ridge penalty is σ²/τ², so one penalty is right only if
τ² — the variance of a player's true rating around what his box-score prior
predicts — is the same for a 30%-usage star and a 12%-usage specialist. Nobody
had checked, and a role-dependent penalty is free to implement, since
`M[i,i] += a_career` broadcasts a vector.

`shrink_by_role.py` measures τ² before fitting anything (CLAUDE.md rule 8).
Split games in half, fit the whole stack separately on each, and take
`cov(r_A, r_B)` within a role bin, where `r = θ̂ − Zγ`. Estimation noise is
independent across halves and cancels.

**The estimator has one bias and it decides how to read the table.** Splitting
by game cancels estimation noise but *not* shrinkage: both halves shrink a
thin-record player by the same `k_i = n_i/(n_i+α)`, so what comes back is
`k_i²·τ²`. The possession axis is therefore uninterpretable — the 3.2× (offense)
and 3.9× (defence) gradients across possession bins are exactly what pure
attenuation predicts. **Usage read within a possession tercile is clean**,
because `k_i` is roughly constant inside one.

| offense, τ in pts/100 | low usage | mid | high |
|---|---|---|---|
| low-possession tercile | 0.278 | 0.157 | 0.184 |
| mid | 0.328 | 0.323 | 0.285 |
| high | 0.555 | 0.492 | 0.605 |

No ordering in usage at any data volume, and the spread within a tercile is
smaller than between terciles. Defence reads the same
(0.248/0.233/0.288 · 0.508/0.497/0.467 · 0.746/0.579/0.760).

**A player's role does not predict how far his true rating sits from his box
score.** So the single `a_career` is not wrong in the direction anyone would
guess first, and the remaining additive headroom is not a heteroscedastic-prior
problem. Worth five minutes to know, and it is the third shape the Gaussian
career prior has now survived, after heavy tails and position-as-a-mean.

---

# §24 The duplication gate's cost, measured forward rather than described (2026-09-03)

The gate is asserted, so the one thing that must not be asserted is its price.
It had been reported descriptively — of 18,071 real units 1.0% move at all and
the mean absolute change is 0.0012 pts/100 — which is the right shape of
statement but is computed on the same units that calibrated `d_floor`.

`forward_pairs --gate` makes it an r² number in the rig everything else in this
project is measured in. Profiles, `d_floor` and the calibration all come from
the fit window; the additive prediction is multiplied by the per-cell gate and
scored on a season the model has never seen. 16 rolling origins:

| | Δr² vs ungated | sem | t | origins |
|---|---|---|---|---|
| all possessions | **+0.0000024** | 0.0000023 | +1.05 | 12/16 |
| novel five-man sets | +0.0000026 | 0.0000026 | +1.03 | 12/16 |

**Not significant, and the sign is the point.** Applying the device costs
nothing measurable and if anything gains a little, at 12 of 16 origins, against
a scale where free pairs gain +0.000034 and usage demand +0.0000103. `d_floor`
comes out at 3.47 from the fit window against 3.33 from the full corpus, and
1.00% of fit cells move in both — so the calibration is stable out of sample
too.

That is the honest completion of the claim. The gate is asserted because
§20.5 says the schedule cannot be fitted from observational lineup data at all;
what can be measured is that asserting it does not damage the numbers that were
measured, and it does not.

## 24.1 Selecting the prior's own penalty gains nothing

`a_gamma` is pinned at 1e6 in every rig — the sweep is `{1e6, BIG}`, on or
off — so it had never actually been selected, and CLAUDE.md says nothing with a
pinned penalty is deployable. It matters more now that the prior is 36 dims a
side rather than 32.

`forward_eval --a-gamma 3e4 1e5 3e5 1e6 3e6 1e7`, on the shipped
numeric-position prior, 16 matched origins against the pinned run (`base` and
`exp` bit-identical):

| arm | pinned at 1e6 | selected | Δ | t | origins |
|---|---|---|---|---|---|
| prior | +0.001565 | +0.001560 | −0.000006 | −0.39 | 7/16 |
| all | +0.001628 | +0.001626 | −0.000003 | −0.13 | 8/16 |
| all_cf | +0.001730 | +0.001742 | +0.000012 | +0.70 | 10/16 |

Null on every arm, and negative on two. Either the objective is flat in
`a_gamma` around 1e6 or the validation season cannot tell the values apart at
this effect size — the same noise floor that defeated the pair-recency sweep
and the multi-lag schedules. Both readings say the same practical thing: **1e6
is fine, and widening the grid is not where the remaining additive headroom
is.** The flag stays, because the next person to widen the prior should re-ask.

---

# §25 Do guards and centres age differently? Yes, and modelling it costs you (2026-09-03)

BACKLOG §3.6 had this open: "bigs and guards almost certainly age differently".
It became worth running once position was shown to carry real information
(§21), and `aging_is_shotmaking` sharpens the prior — the decline is
shot-MAKING rather than creation, which is the more guard-relevant half.

`curve_block` gained a group split laid out as **[SHARED | deviations for
groups 0..G−2]** rather than as G independent curves, so the two halves carry
different penalties. `additive_stack` does `M[i,i] += a_exp`, which broadcasts,
so a vector penalty needs no change to the solver, and sending the deviation
penalty to BIG recovers the shared curve bit-for-bit. That makes the arm
properly nested and lets validation switch the split off. Groups from
`nba.players.position` read as the number it is: guards 1,026, wings 537, bigs
807.

16 matched origins, true-debut binned curve and the shipped numeric-position
prior on both sides, `base`/`prior`/`timevar` identical to 4e−16:

| arm | shared | by position | Δ | sem | t | origins |
|---|---|---|---|---|---|---|
| exp (the curve alone) | +0.001560 | +0.001587 | +0.000027 | 0.000016 | +1.66 | 10/16 |
| all | +0.001711 | +0.001687 | **−0.000023** | 0.000010 | **−2.20** | 2/16 |
| **all_cf (the deployable stack)** | **+0.001799** | +0.001782 | **−0.000017** | 0.000008 | **−2.11** | **3/16** |

**It helps alone and hurts in the stack, significantly.** Validation switched
the split off at 8 of 16 origins for `all_cf` and the arm still lost, which is
the signature of the validation noise floor rather than of a real effect with
the wrong sign: 36 extra parameters buy variance the validation season cannot
price. Do not split the curve.

The wider lesson is worth keeping separate from the result: **a lever measured
alone can reverse in the stack.** The curve alone gains +0.000027 at 10/16;
inside the full model the same block loses at 3/16. Nine bins shared across
everybody remain the right answer, as they were against a spline and against
age.

## 25.1 A bug the identity check caught, and why the check exists

The first version of this run had `base`, `prior` and `timevar` differing by
4e−4 between the two arms, where they must be bit-identical — those arms have
`a_exp = BIG`, which switches the career-stage block off entirely. The penalty
vector was setting the shared columns to BIG and leaving the DEVIATION columns
at their own penalty, so the arms tagged `base`, `prior` and `timevar` quietly
carried position deviations and stopped being comparable to the control.

The measured conclusion did not change once fixed, which is luck rather than
vindication. **Print the arms that must be identical, every paired run.** It
costs one line and it is the only reason this was caught at all.

---

# §26 Half the "linear headroom" is an artefact of the random split (2026-09-03)

§9.1 is the result that reframed the project: the additive ceiling is
+0.002759, ridge reaches +0.002259, so there is **+0.000499 of linear
headroom** — three times the entire non-additive budget. Every phase since has
been steered by it. It was measured with a **random** evaluation split, and
`additive_ceiling.py` has carried an unused `--esplit forward` flag the whole
time.

Same code, same data, 3 seeds, only E moved from a random 20% to the
chronological tail:

| α | FORWARD noisefree | sd over seeds | RANDOM noisefree | sd |
|---|---|---|---|---|
| 0 | +0.001289 | **0.002585** | +0.002717 | 0.000064 |
| 1 | +0.001321 | 0.001783 | +0.002722 | 0.000069 |
| 10 | +0.000966 | 0.000493 | +0.002752 | 0.000065 |
| 100 | +0.000865 | 0.000152 | +0.002759 | 0.000059 |
| **1000** | **+0.000959** | **0.000050** | +0.002635 | 0.000050 |
| 3000 | +0.000891 | 0.000017 | +0.002421 | 0.000037 |

**The two behave differently in kind.** On a random split `noisefree` is flat
from α=0 to α=300, which is what makes "the ceiling" well defined: as α→0 the
shrinkage bias goes with it and the limit is `var(Xβ_true)/var(y)`. Forward it
peaks at an **interior** α ≈ 1000 and the low-α estimates are unstable — sd
0.0026 at α=0, fifty times the random split's. Removing shrinkage forward
removes shrinkage bias *and* increases drift exposure, so **there is no
infinite-data limit to extrapolate to.** The additive ceiling, as defined, does
not transfer to the deployable regime.

What does transfer is the gap between the best noise-free score and the best
full-data fit, on the same rig:

| | best stable noisefree | best achieved (full data) | **gap** |
|---|---|---|---|
| random split | +0.002763 (α=30) | +0.002259 (α=3000) | **+0.000504** |
| **forward tail** | **+0.000959** (α=1000) | **+0.000697** (α=10000) | **+0.000262** |

The random arm reproduces the published +0.000499 to within 1%, so the rig is
the same one; only the question changed. **About half the linear headroom the
project has been chasing is an artefact of scoring on a random split.**

**The levels are not comparable to the rolling-origin numbers** and should not
be quoted as if they were: E here is a fixed chronological tail 0 to 5 years
past the fit window, where `forward_eval` refits at every origin. That is why
`achieved` is *negative* for α < 3000 — a lightly-shrunk plain ridge fitted on
2002–2019 and applied to 2020–2025 is worse than predicting zero. Only the
internal gap is a like-for-like comparison.

Two things follow for what to work on.

- **Better estimation of β is worth about half what the record says.** The
  levers that fight drift — this season's δ, the fractional regime, freshness —
  keep their standing, and §14 already said drift dominates. This says the
  alternative was smaller than advertised.
- **The optimal forward α is ~10⁴, not ~10³** — in this rig. The EB α on the
  full corpus is 3,224, chosen by a criterion that assumes the test data comes
  from the same distribution as the training data, and forward `achieved` is
  still rising at α=10,000. Shrinking harder than empirical Bayes recommends is
  the right response to drift.

## 26.1 …but that does NOT transfer to the stack's `a_career`, and I checked

The obvious inference from the paragraph above is that the model's own career
penalty is too small. It reads like a grid-boundary case: `a_career` sweeps
`[3e3, 1e4, 3e4]`, and in `forward_pairs` validation picks the TOP at 6 of 16
origins and the bottom never. So the grid was widened to 1e6 and run against a
matched control:

| arm | incumbent grid | widened to 1e6 | Δ | t | origins |
|---|---|---|---|---|---|
| prior | +0.001565 | +0.001563 | −0.000003 | −1.00 | 0/16 |
| all | +0.001711 | +0.001704 | −0.000006 | −1.00 | 0/16 |
| all_cf | +0.001799 | +0.001790 | −0.000009 | −1.46 | 0/16 |

**Null, negative, and 0 of 16 origins better.** Validation reaches the new
values at only 2 of 16 origins and loses when it does — more choices, more
selection noise, the same floor that defeated the pair-recency sweep and the
multi-lag schedules.

**The reconciliation is that the two α are not the same parameter.**
`additive_ceiling` fits a plain ridge, so its α penalises θ itself, shrinking
toward zero. The stack's `a_career` penalises **β = θ − Zγ**, the deviation
from the box-score prior, shrinking toward what the player's stat line implies.
Those have different natural scales and different optima, and the prior already
supplies most of the extra shrinkage the plain-ridge result asks for. In
`forward_eval` the top of the grid is chosen at 4 of 16 origins, not 6, which
is not a boundary.

Recorded because the inference was mine and it was wrong: **a boundary in one
rig's penalty is not a boundary in another rig's differently-defined penalty.**
Checking cost twenty minutes.

---

# §27 Is a +5 in 2003 the same as a +5 in 2024? Near enough (2026-09-03)

The tool's headline use is a **cross-era** five — Jordan next to Curry, Shaq
next to Jokić — and it prints one number per player pooled over his whole
career. The target is detrended by (season, week), so a rating is always
relative to that season's league average. The tool then compares those ratings
across seasons, which is only valid if the **spread** of true player quality is
the same in every season. If the league got deeper, a +5 in 2003 was easier to
earn than a +5 in 2024 and every cross-era lineup is tilted. Nobody had checked.

`era_comparability.py`. Per season, split that season's GAMES in half, fit a
plain ridge on each half at a **fixed** α (letting empirical Bayes pick per
season would absorb exactly the thing being measured), and take
`cov(β_A, β_B)` across players. Estimation noise is independent across halves
and cancels, so τ is the true sd of player quality in that season. 3 seeds.

| | 2002 | 2010 | 2016 | 2021 | 2024 | trend across the corpus |
|---|---|---|---|---|---|---|
| offense, τ pts/100 | 0.599 | 0.575 | 0.591 | 0.659 | 0.580 | **−0.06 (−10%)** |
| offense, players ≥800 poss that season | 0.674 | 0.639 | 0.663 | 0.762 | 0.680 | −0.04 (−6%) |
| defence, τ pts/100 | 0.475 | 0.474 | 0.537 | 0.392 | 0.494 | −0.09 (−17%) |
| defence, ≥800 poss | 0.544 | 0.528 | 0.595 | 0.462 | 0.603 | −0.07 (−12%) |

**Flat, to within season-to-season noise.** The trend over 22 seasons is 6–17%
of the mean, and the season-to-season swing is larger than the trend — offense
runs 0.478 in 2020 and 0.659 in 2021. Restricting to players above a
possession bar, which holds the population roughly fixed against roster
expansion (440 players in 2002 against 571 in 2024), halves the trend on both
sides.

So **cross-era comparison is sound to within about 10%**, and the tool's
central use case is not tilted. Two footnotes worth keeping:

- The direction of the small trend is *compression* — the league is very
  slightly flatter now — so if anything the tool marginally over-rates modern
  players relative to old ones, by well under a tenth of a point per 100.
- This measures the spread of **single-season** ratings at a fixed α, which is
  the right first-order check on the scale but not the same object as the
  career ratings the tool prints. A player whose career straddles eras is
  unaffected either way.

---

# §28 θ-recency is real, and it is the same lever as δ seen from a third side (2026-09-03)

`theta_recency` down-weights old seasons when fitting θ — free, because `X'X`
is block diagonal by season, so it is just scaling each block. Season-ahead it
read **+0.000019 (t=+1.89, 11/16)** and was filed as screening, with a note
that settling it needed a better design rather than more origins. §26 raises
its prior (drift is most of what is left) and §15.1 contradicts the note
(fractional origins buy real power). So it was ported into `fractional_eval`,
nested — half-life 0 is in the grid and reproduces the incumbent bit-for-bit.

16 fractional origins (K=2), matched against `frac_k2_bionum.csv`:

| arm | flat | with recency | Δ | t | origins |
|---|---|---|---|---|---|
| **base** (plain ridge, nothing else) | +0.001681 | +0.001851 | **+0.000169** | **+7.30** | **16/16** |
| all_nodelta (prior + curve, no δ) | +0.002053 | +0.002145 | **+0.000092** | +4.30 | 14/16 |
| all_cf (+ last season's δ carried) | +0.002075 | +0.002121 | +0.000046 | +2.74 | 11/16 |
| **all_delta** (+ THIS season's δ) | +0.002160 | +0.002138 | **−0.000022** | −1.55 | 6/16 |

**A perfectly monotone substitution.** The more current-season information the
model already has, the less θ-recency adds — and once this season's δ is in, it
is worth nothing. That is the third route to the same place: **carry-forward,
this-season δ and θ-recency are three ways of buying freshness, and they
substitute almost exactly.** It also explains why the season-ahead reading was
weak: it was measured on the arm that already had carry-forward, which is the
row where 60% of the effect has already been spent.

(Note the identity check does *not* apply here and its absence is not a bug:
θ-recency touches every arm including `base`, so `base` moving by +0.000169 is
the effect. Contrast §25.1, where `base` had no experience block and therefore
*had* to be identical — the same 4e−4 discrepancy meant a bug there and means
the effect here. Know which invariant you are checking.)

## 28.1 Why it must NOT go into the tool, measured rather than asserted

The tool's configuration is the `all_nodelta` row — career ratings, no δ of any
kind — where recency is worth **+0.000092**, larger than anything else shipped
today. It is still the wrong thing to ship, and the reason is specific to what
the tool is for.

The tool fits θ on the whole corpus, so weighting by `0.5^((T_last − s)/hl)`
puts a player who retired in 2010 at weight 0.0002 and collapses his θ toward
his box-score prior. Fitting the full stack twice, flat against a 2-season
half-life, and grouping players by the last season they appear in:

| last season | players | sd of career offensive rating, flat | with recency | ratio |
|---|---|---|---|---|
| 2002–2007 | 145 | 1.921 | 0.848 | **0.441** |
| 2008–2012 | 188 | 1.986 | 0.901 | 0.454 |
| 2013–2017 | 235 | 2.181 | 1.008 | 0.462 |
| 2018–2021 | 169 | 1.705 | 0.946 | 0.555 |
| 2022–2025 | 513 | 1.789 | 1.266 | **0.708** |

**Historical players are shrunk 1.6× harder than current ones.** §27 measured
that the true spread of player quality is flat across eras to within 10%, so
that 1.6× is pure artefact — exactly the era distortion a cross-era tool must
not have. θ-recency is right for forecasting next season and wrong for pricing
Jordan beside Curry, and the tool does the second.

This is worth stating as a general rule for this project, because the northstar
makes it recur: **a lever that improves forecast r² is not automatically a
lever the tool should ship.** The tool answers a different question, and the
mechanism that makes recency pay — forget the past — is the mechanism that
makes it wrong here.

---

# §29 Is what the page prints calibrated? End to end, and mostly yes (2026-09-03)

Every piece of the tool's number was validated separately and on a *different*
residual — the additive index earns 0.447 against estimated true lineup
quality, chemistry earns ~1.0 on the residual after the additive-plus-free-player
arm, usage demand on the residual after that, and the duplication gate
multiplies the lot. Nothing had checked that the **sum** is calibrated, and
three of the four changed today.

`page_calibration.py` fits all of them on games before 2022-08-01, builds the
printed number per lineup, and hands it to `lineup_scoreboard.evaluate`, which
cross-fits the truth on the evaluation games so measurement noise in the truth
cancels. `slope` = 1.0 means the number is what it claims to be. 5 truth-splits.

| offense | slope | ρ | sd_pred | sd_true | top-3 lift |
|---|---|---|---|---|---|
| raw sum of five ratings | **0.526** | 0.581 | 4.67 | 4.25 | +1.36 |
| × 0.447 calibration | 1.189 | 0.571 | 2.09 | 4.37 | +1.19 |
| + chemistry × 1.0 | 1.077 | 0.551 | 2.22 | 4.34 | +1.44 |
| + usage demand | 1.130 | 0.541 | 2.08 | 4.39 | +1.58 |
| **+ duplication gate = what the page prints** | **1.160** | 0.577 | 2.09 | 4.21 | **+1.62** |

| defence (the page claims no defensive chemistry and no demand term) | slope | ρ | top-3 |
|---|---|---|---|
| raw sum of five ratings | **0.530** | 0.602 | +0.99 |
| × 0.591 calibration | 0.892 | 0.776 | +0.49 |
| **+ duplication gate = what the page prints** | **0.879** | 0.671 | +0.73 |

Three things worth having.

**1. The page is calibrated to within about 15%, in opposite directions per
side.** Offense **under**-claims (slope 1.16 ± 0.04 — true quality is 1.16× the
printed number), defence **over**-claims (0.88 ± 0.03). Under-claiming is the
safe direction for a tool whose headline risk is over-claiming, and neither
error is large enough to act on from one split; but it is now a measured
statement rather than an assumption.

**2. The decision metric improves at every step of today's work.** Top-3 lift —
the realized quality of the three units the model ranks best within a
team-season, which is the decision the tool exists to support — runs
+1.19 → +1.44 (chemistry) → +1.58 (usage demand) → **+1.62** (gate) on offense,
and +0.49 → +0.73 on defence. Every change shipped today moves it up, including
the asserted one.

**3. The per-side slope asymmetry is not visible here, and that is a
discrepancy.** The tool shrinks defence by 0.591 and offense by 0.447 — a 32%
difference — but the raw slopes in this rig are **0.526 and 0.530**, all but
identical. §14.4 records that an earlier per-side asymmetry was a specification
error (a missing intercept) and §14.3's reconcile put the shipped pair "inside
the range with the right ordering"; this rig sees no ordering at all. Two
estimators of one quantity disagreeing in ORDER rather than level is exactly
the tell §14.4 describes, so **this is logged as open rather than acted on** —
changing the constants is a product decision and the evidence is one split.

## 29.1 The per-side shrink, across three split dates

§29 saw no per-side asymmetry where the tool ships a 32% one, so the check was
repeated at three split dates. Raw slope of the sum of five ratings, cross-fit
truth, ± the sd over 5 truth-splits:

| split | offense | defence | def/off |
|---|---|---|---|
| 2018-08-01 | 0.373 ± 0.014 | 0.520 ± 0.013 | 1.40 |
| 2020-08-01 | 0.530 ± 0.016 | 0.488 ± 0.012 | **0.92** |
| 2022-08-01 | 0.526 ± 0.024 | 0.530 ± 0.029 | 1.01 |
| **mean** | **0.476** | **0.513** | **1.08** |

The tool ships 0.447 / 0.591, a ratio of **1.32**. The measured ratio is 1.08
and it changes sign across splits — 1.40, 0.92, 1.01 — while the seed sd within
a split is only 0.01–0.03. **So the asymmetry is not a stable feature of the
data; the split-to-split variation swamps it.** The level does move a lot with
the evaluation window (offense 0.373 at the 2018 split against 0.530 at 2020),
which is §14.1's horizon effect showing up as expected.

What the page actually prints, by split:

| | 2018 | 2020 | 2022 | mean |
|---|---|---|---|---|
| offense slope | 0.793 | 1.137 | 1.160 | **1.03** |
| defence slope | 0.881 | 0.769 | 0.879 | **0.84** |

**Averaged over splits the offensive side is essentially perfectly calibrated
(1.03) and the defensive side over-claims by about 16%, at all three splits.**
That is consistent enough to act on and it points the same way the 5-Shaq rule
does — five Goberts is a defensive-sum problem.

**It is logged as the top open tool item rather than changed here**, for two
reasons. The shipped 0.591 comes from `lineup_uncertainty.py`, a different
estimator on a six-season horizon, and §14.1 says the slope FALLS with the
fit–test gap — so that estimator giving the *higher* number is backwards from
what the horizon effect predicts, and the disagreement should be understood
before either is trusted. And changing a constant that multiplies every
defensive number the tool prints is a product decision, not a research one.

## 29.2 The slope is a function of HORIZON, and the shipped pair matches no horizon

Asked by the user: *why would we have different slopes for different years at
all, and how would this work for the first possession of a new season?* The
first half has a clean answer and the second exposes a design error.

**They are not different slopes for different years.** Each split date
evaluates on everything after it, so a 2018 split averages over seven seasons
of drift and a 2022 split over two and a half. The slope falls as ratings go
stale (§14.1), so the pooled number is a possession-weighted average over
whatever horizon mix the window happens to contain — which is not a quantity
anyone asked for.

Measuring it *by* horizon instead, same rig, cross-fit truth:

| raw slope of the sum of five ratings | offense | defence | def/off |
|---|---|---|---|
| **horizon 0** — train on a random half of GAMES, evaluate in the same seasons | **0.563** | **0.677** | 1.20 |
| **horizon 1** — first season after the fit (mean of 3 split dates) | **0.605** | **0.615** | 1.02 |
| pooled over 1–7 seasons (mean of 3 split dates) | 0.476 | 0.509 | 1.07 |
| **what the tool ships** | **0.447** | **0.591** | **1.32** |

Three things follow.

**1. The shrink is not mostly drift, and it is not arbitrary.** At horizon 0
there is no drift at all — the evaluation games sit in the same seasons as the
fit — and the raw sum still over-claims at 0.563 / 0.677. So the correction is
genuinely about estimation error in five summed coefficients. (§14.1's k=0
slope of +1.14 was measured *in sample* on the fitted seasons and is optimism;
this is the held-out version of the same quantity.)

**2. For the first possession of a new season the right number is ≈0.61, on
both sides** — not 0.447. With the shipped constants the page reads slope
**1.30** on offense at horizon 1, i.e. it *under*-claims by about 30% for the
near-term question, and 1.03 on defence.

**3. The per-side asymmetry the tool ships is an artefact of horizon, not a
property of offense versus defence.** The measured def/off ratio is 1.20, 1.02
and 1.07 at the three horizons — mean 1.10 — against a shipped 1.32. The
shipped pair is a long-horizon offensive number (0.447) beside a short-horizon
defensive one (0.591), which is why §29.1 found the asymmetry unstable: it was
never one.

**And the tool has no horizon at all.** It prices Jordan beside Curry; there is
no "when". So the defensible constant is the **horizon-0** one — estimation
noise, with no drift correction, because the question is "how good is this
five" and not "how good will it be in four years". That is ~0.56 offense and
~0.68 defence, and adopting it would raise the page's offensive numbers by
about 26% and its defensive ones by about 15%.

**Not changed here.** It moves every number on the page and it is a product
decision. But the current pair is now known to correspond to no horizon, which
is a stronger statement than §29.1's "the asymmetry is unstable", and it
supersedes that item.

---

# §30 The 5-Shaq rule was read too literally: coverage, not duplication (2026-09-03)

The user's test case: **Andrew Bogut, Rudy Gobert, Kevon Looney, Mitchell
Robinson, DeAndre Jordan.** Five centres, no ball handler, no perimeter
defender. The duplication gate of §20 passed them at 0.94 — five different
people with five different play-style profiles — and the page printed **+11.10
net with +12.36 on defence**, better than any real unit ever measured, for a
lineup with nobody who can guard a guard.

Five copies of one man is the easiest case to state. It is not the meaningful
one, and building the guardrail around it was too literal a reading of the
requirement.

## 30.1 Positional SPREAD is the wrong summary, and trying it shows why

The obvious repair is mean pairwise distance on the 1 = point guard to
5 = centre scale. It does flag five centres — 0.15 against a real minimum of
0.25 — but it also flags real lineups, by up to **3.1 pts/100**:

| real unit the spread gate penalised | positions | poss | change |
|---|---|---|---|
| Harden, George, Leonard, Powell, Mann (2021 Clippers) | 1.75–3.00 | 63 | **−3.06** |
| Gilgeous-Alexander, Dort, Giddey, Williams, Joe | 1.75–2.25 | 81 | −3.04 |
| Durant, Gordon, Beal, Booker, Allen (Suns) | 2.00–3.25 | 113 | −1.61 |

Positionless basketball is a shape coaches field on purpose. Spread cannot tell
"all wings", which works, from "all centres", which does not.

## 30.2 Coverage of the ENDS can, and it is a hard fact rather than a model

Over 17,315 real units and 2.7M possessions:

| | p50 | p99 | weighted p99.99 | raw extreme |
|---|---|---|---|---|
| most guard-like slot | 1.00 | 2.00 | **3.00** | 3.50 |
| most centre-like slot | 4.75 | 3.75 (p1) | **3.00** | 2.25 |

**Outside 0.012% of possessions, no lineup in twenty-three seasons has taken
the floor without a player at 3.0 or lower AND one at 3.0 or higher.** Somebody
has to bring the ball up and somebody has to defend the rim. That is not fitted;
it is what the corpus contains.

| | guard slot | big slot | |
|---|---|---|---|
| five centres | **4.75** | 5.00 | no handler |
| five point guards | 1.00 | **1.00** | no big |
| five best distinct defenders | **3.75** | 5.00 | no handler |
| 2021 Clippers small-ball | 1.75 | 3.00 | both covered — untouched |
| Suns small-ball | 2.00 | 3.25 | both covered — untouched |
| Warriors death lineup | 1.00 | 3.75 | both covered — untouched |

**The bounds are the possession-weighted 99.99th percentile, not the raw
extreme**, and that detail matters: exactly ONE unit of 18,071 has a guard slot
above 3.00, and it played 98 possessions of 2.7 million. Using the raw maximum
puts the bound at 3.50 and lets the five best defenders (3.75) through almost
untouched.

## 30.3 What it does

Both axes ship and the binding one wins. Ends-coverage catches five who cannot
cover a floor; profile diversity still catches five copies of one *wing*, whom
the ends test barely touches (five LeBrons sit at 3.25, only 0.25 past a bound).

| | before | after |
|---|---|---|
| **five centres** | +11.10 (defence +12.36) | **+6.04 (defence +6.73)** |
| five point guards | — | +3.94 (offense +4.61, defence −0.67) |
| five best distinct defenders | +19.79 | +15.56 |
| five Jokićs / five Goberts | +11.03 / +9.75 | unchanged |
| **2021 Clippers, Suns, death lineup, Spurs** | | **all untouched, gate 1.000** |

Cost in range **falls**: 0.57% of real units move against 1.00% for the gate it
replaces, mean absolute change 0.0009 against 0.0012 pts/100. Forward, in
`forward_pairs --gate` over 16 rolling origins with everything built from the
fit window, **+0.0000026 ± 0.0000023 (t=+1.12, 12/16)** — indistinguishable
from zero, like its predecessor.

## 30.4 The lesson

A guardrail aimed at the example rather than at the mechanism catches the
example and nothing else. "Five Shaqs" was shorthand for *a lineup that cannot
function*, and identity duplication is one narrow instance of that. The
generalisation had to come from asking what a lineup structurally needs — a
handler and a rim protector — and then checking that against what every real
lineup has, rather than from making the stated example harder to type.

## 29.3 The horizon-0 slope, measured carefully

§29.2 argued the tool should use the horizon-0 constant, from one split. Done
properly — four independent random game splits per side, six truth-splits each,
train on half the GAMES and evaluate in the same seasons so there is no drift:

| split | 0 | 1 | 2 | 3 | mean | sd |
|---|---|---|---|---|---|---|
| offense | 0.562 | 0.637 | 0.644 | 0.619 | **0.615** | 0.037 |
| defence | 0.677 | 0.690 | 0.659 | 0.745 | **0.693** | 0.037 |

**And it does not depend on how much data the ratings were fitted from**, which
is the objection that had to be cleared: the tool fits on the whole corpus,
while these fit on half, and errors-in-variables says less estimation noise
should mean a higher deserved slope. Holding the evaluation set fixed at a
quarter of the games and varying only the training fraction:

| train on | 18.8% | 37.5% | 56.2% | 75.0% | extrapolated to 100% |
|---|---|---|---|---|---|
| offense | 0.653 | 0.636 | 0.633 | 0.600 | **0.612** |
| defence | 0.730 | 0.749 | 0.746 | 0.684 | **0.717** |

Flat, or very slightly falling. So the half-corpus reading transfers and no
extrapolation is required. This is a **third independent confirmation** of
`calibration_slope_is_flat`, which found the same bucket by bucket, and of
`lineup_uncertainty`'s model-based null.

**Horizon-0 constants: offense ≈ 0.61, defence ≈ 0.70**, against a shipped
0.447 / 0.591 — the page under-claims by about 37% on offense and 18% on
defence for the timeless question it actually asks.

---

# §31 The defensive assignment cost: the first structure to pass its sign check (2026-09-03)

Prompted by the user's objection that the coverage gate is a post-hoc heuristic
and that the penalty should come out of a MODEL. `demand_block` is "a
possession has one ball". This is the constraint nobody had built: **five
offensive players must be guarded by five defenders, one each.** A lineup of
five centres cannot cover a 1-2-3-4-5 offense however good each of them is
alone, and the additive model cannot know it — each defender is priced against
a background of average teammates, where somebody else was always taking the
guard.

Sort the five defenders' positions and match them in order to the canonical
offensive shape (1,2,3,4,5). In one dimension the sorted assignment IS the
minimum-cost matching, so this is exact rather than a heuristic for it. Four
columns: total cost, worst single assignment, and the two signed halves (too
small for the slot, too big for it). Signs pre-registered before fitting: all
four **positive** on defence, since the target is points allowed and a worse
matching cannot help.

| arm, 16 forward origins | Δr² | sem | t | seasons |
|---|---|---|---|---|
| **defence** | **+0.0000055** | 0.0000064 | +0.85 | **12/16** |
| PLACEBO, positions shuffled across players | +0.0000006 | 0.0000007 | +0.87 | 10/16 |
| offense (control — no assignment constraint on that side) | −0.0000018 | 0.0000019 | −0.95 | 5/16 |

**Not significant.** The same magnitude as `defensive_coverage` and everything
else in this family. But three things separate it from the four structures in
§20.5:

- **4/4 signs as pre-registered.** total cost +0.226, worst assignment +0.062,
  too-small +0.143, too-big +0.120 pts/100 per sd. Floor geometry managed 2/5
  and its predictive content sat entirely in the inverted columns; index
  curvature came back inverted outright. This is the first block in the project
  whose every coefficient points where theory said it would.
- **Its magnitude is 9× the placebo's**, and the offensive side — where the
  constraint does not exist — is correctly null.
- **It extrapolates the right way, and by construction.** Real units run
  −0.74 / −0.19 / +0.80 (p1/p50/p99). Five centres score **+3.49**, five
  Goberts +3.73, five point guards +3.37, the five best defenders +2.34, and
  the Warriors death lineup +0.13. A worse matching cost cannot be good, so
  unlike spread-based features the sign is not something the fit could get
  backwards.

**Why it is anchored where `--coverage` was not.** Height/position SPREAD
cannot tell "all wings", which works, from "all centres", which does not — both
have low spread. An assignment cost is measured against a fixed offensive
shape, so it distinguishes them: the 2021 Clippers cover 1-2-3-4-5 acceptably
and five centres do not.

At t=+0.85 this is screening, not a result. It is recorded as the best-shaped
candidate the project has produced for the northstar, and as the template the
next structure should follow: **anchor the feature, pre-register the sign, and
put the constraint in the model rather than in a multiplier afterwards.**

## 31.1 Role stretch is null, and does not beat its own placebo

The first attempt at the user's role framing. The exogenous handle on "assigned
role" is a player's RANK in career usage among the five — composition only, not
an outcome — against his own habitual rank over the fit window. 16 forward
origins, offense:

| arm | Δr² | sem | t | seasons |
|---|---|---|---|---|
| role stretch | −0.0000033 | 0.0000029 | −1.13 | 8/16 |
| **PLACEBO, career usage shuffled across players** | −0.0000045 | 0.0000038 | −1.18 | 3/16 |
| stretch on novel five-man sets | −0.0000054 | 0.0000033 | −1.64 | 6/16 |

**The real block is indistinguishable from the shuffled one.** Usage rank
against habitual rank does not carry forecastable signal.

What this closes and what it does not. It closes the direct observable
implication — a lineup does not measurably underperform when one of its players
is playing above his usual role, at least not detectably at this scale. It does
**not** close the model the framing actually describes: estimate each player's
latent aptitude PER ROLE from how his output changes across lineup contexts,
then predict who takes which role in a new five and price him at that role.
That is a different object — a model of role assignment, not a feature of the
composition — and the pieces for it exist (`context_profile.py` measures that
context bends the profile and that it keys on role; `context_deconfound.py` has
the exact resolvent for the static version, which was null forward).

The honest reading of §20.5, §31 and §31.1 together: **every handle on
composition that can be written as a feature of the five and fitted on the
residual has now come back null or wrong-signed.** The assignment cost is the
only one whose signs all point the right way, and it is t=+0.85. If a role
model is going to work it has to change what the model IS — how a lineup's
prediction is formed — rather than add a term to what it already computes.

---

# §32 Composition-assigned load changes role and efficiency (2026-09-04)

`ROLE_MODEL.md` §5.1 asked the decisive cheap question: does a player's output
change when lineup composition forces him away from his usual workload? The
old `role_stretch` residual feature could not answer it; it asked whether an
observed lineup underperformed, not whether the same player's held-out box
score changed at a role assigned without looking at the outcome.

## 32.1 Protocol

`usage_load_response.py` runs one origin per season, 2015–2024. For test season
T it:

1. builds player usage profiles and the team usage pool from seasons < T;
2. assigns every real offensive five that fixed pool in proportion to prior
   `usage ** alpha`, with alpha 3 from the earlier allocation screen;
3. aggregates the possession-level assignment to player-game;
4. joins only then to the held-out game's realized box score; and
5. estimates weighted within-player slopes, with a second specification also
   absorbing a team-game fixed effect.

The predictor is always composition-assigned load. Realized usage is an
outcome, never an input. Coverage must be at least 90%, the player must have at
least ten offensive possessions in the game and eight games in the season.

## 32.2 The population response is unambiguous

Mean season slopes and season-level standard errors:

| outcome | player FE | player + team-game FE | expected |
|---|---:|---:|---:|
| realized usage | +0.4098 ± 0.0171 | +0.3308 ± 0.0231 | + |
| assist rate | +0.02149 ± 0.00141 | +0.01036 ± 0.00301 | + |
| points per usage | **−0.07854 ± 0.01086** | **−0.18445 ± 0.01560** | − |
| turnover share | +0.01825 ± 0.00291 | +0.02757 ± 0.00494 | + |
| eFG | −0.04048 ± 0.00579 | −0.09874 ± 0.00906 | − |
| assisted share | −0.11847 ± 0.00963 | −0.12078 ± 0.01316 | − |
| FT% placebo | +0.01029 ± 0.00927 | −0.01197 ± 0.01971 | 0 |

All six mechanism signs reproduce across controls. More predicted workload
becomes more actual workload and creation, but it costs efficiency, turnovers
and assisted finishing. This is the first direct evidence in the repository
that the stage-3 value function is non-flat.

The whole five can be overloaded at once, while one player can also be loaded
relative to his four teammates. Writing every player-lineup log load exactly as
its lineup mean plus a zero-sum player deviation and fitting both jointly gives:

| outcome | common-load slope | relative-load slope |
|---|---:|---:|
| points per usage | **−0.10138 ± 0.01986** | **−0.06540 ± 0.00720** |
| turnover share | +0.02702 ± 0.00384 | +0.01330 ± 0.00358 |
| eFG | −0.04523 ± 0.01327 | −0.03734 ± 0.00390 |
| assisted share | −0.11023 ± 0.01814 | −0.12678 ± 0.01447 |
| FT% placebo | +0.01407 ± 0.01607 | +0.00459 ± 0.01604 |

## 32.3 The response must be transported on the channel it measured

For each scored season, `contextual_validation.py` averages response slopes
only from earlier diagnostic origins. A first scalar implementation used the
player + team-game slope as if it priced the entire player load. It fails at
alpha 3: cross-fit true-quality rho falls 0.4636 → 0.4386, raw r² falls
−0.1558 → −0.2629 and MAE rises 8.299 → 8.696. The within-team slope is not a
whole-lineup slope.

Using common and relative coefficients on the matching components succeeds:

| 2016–2024 | alpha 3 | + decomposed prior response | paired delta ± sem |
|---|---:|---:|---:|
| true-quality rho | 0.4636 | **0.4813** | +0.0212 ± 0.0109 (7/9) |
| calibration r² | 0.0397 | **0.0421** | +0.0027 ± 0.0014 (7/9) |
| raw r² | −0.1558 | **−0.1354** | +0.0217 ± 0.0162 (4/9) |
| MAE | 8.299 | **8.155** | −0.150 ± 0.082 (5/9) |
| ordinary corr. | 0.1795 | **0.1874** | +0.0088 ± 0.0036 (8/9) |

The cross-fit rho losses are 2016 and 2017, when only one or two response
origins exist. Every 2018–2024 origin improves. This is promising, modest
forward evidence rather than a production selection: the alpha and mechanism
were developed on this same era and the standalone points model remains behind
the incumbent scorer.

## 32.4 Counterfactual pass and remaining failure

On career profiles, uniform allocation prices the Jokić/Korver and
Jokić/Westbrook offenses at 118.60 and 113.91. Alpha 3 changes them to 118.68
and 111.91; adding the decomposed response gives 119.87 and 114.57. Thus the
combined allocation/response adjustment changes the Westbrook-minus-Korver gap
by **−0.61 pts/100 relative to the uniform model**, the pre-registered direction,
without asserting which complete lineup must win. The named all-center offense
(Bogut, Gobert, Looney, Robinson, Jordan) moves 120.86 → 115.31. A five-guard
offense moves upward to 119.51, appropriately leaving its size cost to defense.

The model is not yet OOD-coherent. Five copies of Gobert still score 126.97:
his observed finishing percentage is being priced as if it survives a creation
role. The pre-registered cheap remedy—interact common and relative load with a
strictly prior assisted-share profile—has the expected average signs but no
support: −0.01235 ± 0.01482 (t=−0.83) common and −0.01399 ± 0.01521 (t=−0.92)
relative. It must not be tuned or shipped.

The next model needs separate assisted-finishing and self-creation allocation,
plus a hierarchical prior that widens when a player is assigned a role his data
do not cover. The population load response earns a place as a candidate mean
component; the player-type extrapolation remains an explicit open problem.

## 32.5 A literal assist-supply constraint is too hard

Every assisted make has one matching assist, suggesting another exact resource:
sum the five profiles' assist supply, compare it with their assisted-make
demand, and turn unsupported assisted makes into misses. There is no fitted
coefficient. The identity is true for a realized lineup, but the proposed use
is not: five career profiles were learned in five different teammate contexts
and are not a simultaneous ledger.

Forward scoring confirms the distinction. Against alpha 3 on 2016–2024:

| metric | alpha 3 | hard assist constraint |
|---|---:|---:|
| true-quality rho | 0.4636 | 0.4423 |
| calibration r² | 0.0397 | 0.0338 |
| raw r² | −0.1558 | **−0.6207** |
| MAE | 8.299 | **9.922** |
| predicted SD | 3.12 | **5.73** |

It penalizes ordinary lineups by 2.84 pts/100 on average; raw r² and MAE worsen
in all 9/9 origins. Adding the decomposed load response does not rescue it.
The constraint is closed in this form. Do not fit a soft multiplier merely to
make the failed hard cap smaller; assisted and self-created opportunities need
to be modeled jointly from simultaneous lineup data.

---

# §33 Assigned-load distance does not calibrate OOD error (2026-09-04)

The third product pillar requires data-driven intervals that widen outside
role support. `role_support_validation.py` tests the cheapest candidate before
a hierarchical role model is built.

At each 2016–2024 origin it builds, strictly from seasons < T, each player's
possession-weighted history of common lineup log-load and player-relative
log-load under the alpha-3 allocator. A held-out five's distance is the largest
two-channel standardized deviation among its players. Point predictions use
only earlier response origins; their affine calibration uses only earlier
scored seasons.

Held-out lineup outcomes are split by game. If `r1` and `r2` are prediction
residuals on independent halves, `r1*r2` estimates persistent squared model
error without counting shot noise. Centering each half within season removes
common era drift before asking whether error variance grows with role distance.

| within-season role-distance quartile | mean distance | tail beyond prior range | persistent error SD | centered error SD |
|---|---:|---:|---:|---:|
| Q1 | 0.54 | 0.00 | 4.34 | **3.95** |
| Q2 | 0.83 | 0.01 | 4.24 | **3.94** |
| Q3 | 1.15 | 0.03 | 4.01 | **3.50** |
| Q4 | 2.28 | 0.26 | 4.53 | **3.87** |

The centered Q4−Q1 error-variance difference is **−0.58 ± 3.76 (t=−0.15,
4/9 positive)**. Excluding the first no-history calibration origin does not
change the conclusion (+0.98 ± 3.88, t=0.25). Assigned-load distance therefore
does not order forecast error among real lineups and must not drive the product
interval.

This is not evidence that synthetic extremes are safe. It repeats the central
support problem: coaches select real roles, so the observed range contains few
bad assignments. A five-center synthetic can be far outside the range, but
distance alone cannot say how much wider its interval should be. The proposed
hierarchical allocator now has a specific burden: derive role uncertainty from
the fitted posterior and show held-out calibration beyond what this empirical
distance failed to show.

---

# §34 Direct role allocation says alpha 1, not alpha 3 (2026-09-04)

The earlier point screen preferred concentrating a fixed usage pool with
historical usage cubed. That was a prediction about lineup point ranking, not
proof that players literally divide the ball that way.

`role_allocation_validation.py` separates the questions. At each 2015–2024
origin it builds profiles from seasons < T, predicts each player's share from
the five-man composition, and scores the held-out player-game shares after
conditioning out the realized team total. Alpha 1 has event-weighted NLL
**1.81635** versus 1.87346 for alpha 3, share correlation **0.931 vs 0.882**,
and is selected from prior history at every 2016–2024 origin.

`role_channel_validation.py` repeats the design for FGA, 3PA, turnovers,
assists, assisted makes, and self-created makes. Alpha 1 is the robust default
for usage, FGA, assists and assisted makes. Three-point and turnover selections
move across origins without consistent forward metric gains. Self-created
makes mildly prefer alpha 1.5: share MAE improves −0.00193 ± 0.00052 (t=−3.73,
7/9), but NLL and correlation do not. Do not over-read it.

The model distinction is now explicit: **alpha 1 is assignment; alpha 3 was a
predictive value/strategy effect.** A structural model must not label the
latter as observed role allocation.

---

# §35 Opportunity creation and shot making form a competitive point score (2026-09-04)

`channel_totals_validation.py` asks how much a held-out lineup generates after
the direct allocator has answered who. With strictly prior profiles and the
alpha-1 usage ledger, split-half corrected true-quality rho is:

| channel | rho |
|---|---:|
| two-point attempts | **0.710** |
| three-point attempts | **0.693** |
| turnovers | **0.541** |
| free throws | 0.322 |
| offensive rebounds | **0.620** |
| self-created makes | **0.558** |

Total usage is constant by construction and has no ranking signal. Total FGA
is much weaker than its two/three split because composition mainly predicts
*where* a fixed set of opportunities goes. Passing supply by itself is weak
(rho 0.282); assisted-finishing demand is better (0.452 before the ledger,
0.418 after it).

`channel_points_validation.py` then predicts rim, paint, midrange, long
midrange, corner-three, above-break-three, FTA, ORB and turnover rates. Their
point values are fit only on seasons before T. Player shot making is a separate
term: broad 2P, 3P and FT ability above the league expectation for that
player's prior shot mix.

The making term is necessary. Versus creation alone, it raises true-quality
rho in all 10 origins by **+0.2559 ± 0.0484 (t=5.29)** and descriptive
calibration r² in all 10. After prior-only point calibration, the full
structural score is tied with the alpha-1 box-score identity over 2016–2024:

| model | MAE | raw r² | true-quality rho |
|---|---:|---:|---:|
| creation + making | **7.561** | **−0.0132** | 0.413 |
| box-score identity | 7.576 | −0.0141 | **0.430** |

This is not a predictive victory. It is enough under the three-pillar contract:
the structural model gives up little ranking accuracy, slightly improves point
error, and exposes interpretable mechanisms the identity cannot.

---

# §36 Assisted-finishing demand beyond passing supply predicts future point loss (2026-09-04)

The hard identity in §32.5 failed because it assumed every unsupported assisted
make becomes a miss. `assist_residual_validation.py` tests a narrower question:
does the composition-predicted mismatch explain future point residuals at all?

For each held-out lineup define

`assist deficit = max(assisted-finish demand - assist supply, 0)`.

The point calibration is fit on completed validation origins only. Its score
slope is constrained nonnegative and the deficit coefficient nonpositive, so
noise cannot reverse either basketball meaning. Against calibration alone:

| metric | calibration | + assist deficit | paired change |
|---|---:|---:|---:|
| true-quality rho | 0.413 | **0.482** | +0.0739 ± 0.0175, t=4.22, 9/9 |
| raw r² | −0.0123 | **−0.0002** | +0.01284, t=3.11, 8/9 |
| MAE | 7.576 | **7.496** | −0.0855, t=−2.78 |
| ordinary correlation | 0.158 | **0.184** | +0.0274, t=4.25, 8/9 |

The latest honest expanding fit is

`points = 30.454 + 0.7154 × structural score − 0.4168 × assist deficit`.

It converts the career-profile stress panel to 100.69 for the distinct
five-center offense, 122.97 for five guards, 106.75 for five Goberts and 116.17
for five Jokićs. Jokić/Korver scores 119.92 and Jokić/Westbrook 115.62. Within
the uncalibrated structural score, the finite usage ledger changes Westbrook's
+9.92 freely additive advantage to −6.62, a −16.54 complementarity residual;
the final calibrated gap is −4.30.

Those are coherent means, not completed OOD claims. Real 2024 lineups have an
assist-deficit p99 of **12.25**, while the distinct centers reach 19.04 and five
Goberts 23.82. The next experiment must propagate profile, valuation,
calibration and deficit-slope uncertainty and test interval coverage on real
lineups. Synthetic extremes can verify widening but cannot validate their own
coverage.

---

# §37 The first uncertainty floor is dominated by persistent model error, not player sampling (2026-09-04)

`assist_support_validation.py` splits every reliable held-out lineup by whole
games and multiplies its two centered residuals. This estimates persistent
forecast-error variance without treating possession-level shot noise as a
property of the lineup. The result does not support a smooth in-range distance
schedule:

| assist-deficit band | persistent SD (pts/100) |
|---|---:|
| zero | 3.88 |
| positive-low | 3.69 |
| positive-mid | 3.19 |
| positive-high | 5.15 |

High-minus-zero variance is +12.62 ± 13.84 (t=0.91; only 4/9 seasons
positive), and the continuous variance/deficit slope is +0.163 ± 0.856
(t=0.19). Beyond the origin-specific prior p99, estimated persistent variance
is 52.2 (SD 7.23), versus a smaller in-support value, but support averages only
4.4 reliable lineups per split-season. The season-level variance contrast is
+73.0 ± 58.7 (t=1.24, 5/9 positive). Directionally wider tail uncertainty is
reasonable; claiming calibrated tail coverage is not.

`profile_bootstrap_uncertainty.py` resamples each player's games, recomputes
the EB profile, and holds the same draw fixed across repeated copies. Across
500 draws, profile-only structural-score SD is 0.428 for Jokić/Korver, 0.420
for Jokić/Westbrook, 0.512 for the distinct centers, 0.337 for the five guards,
0.831 for five Goberts and 0.790 for five Jokićs. Player sampling is therefore
not the main source of OOD uncertainty. `structural_counterfactuals.py` now
combines it with prior-origin model disagreement and the empirical persistent
error floor, while explicitly labeling the resulting 95% ranges diagnostic.
Shot valuation, point-calibration and assist-coefficient uncertainty plus an
honest coverage test are still required.

---

# §38 Current-data audit, safe updater and the Haliburton test (2026-09-04)

The database source is Basketball Reference. Before this update it contained
29,698 games and 5,569,624 possessions from 2001-10-30 through 2024-11-10.
The 2025 and 2026 ending-year schedules contain **2,492 completed games after
that date**—almost all of 2024-25 and the full 2025-26 season.

The original `scrape_br.ipynb` cannot safely be resumed: it inserts a game
before parsing, commits possessions one at a time, and then skips every
existing game forever. The database has 17 zero-possession and 15 sub-50-row
games consistent with this failure mode. It also sleeps only about 0.6 seconds
on success, above Sports Reference's published 20-request/minute ceiling.

`experiments/bref_ingest.py` replaces it with a 3.1-second minimum delay,
atomic gzip page cache, complete in-memory parse, bulk per-game transaction,
inventory-only default and explicit `--write`. It exactly reproduced an
existing stored game, including possession count, points and turnovers, and
then passed ten evenly spaced 2024-25/2025-26 regular-season and playoff games.
Two real edge cases are handled explicitly: an overtime player with no event
is filled from non-bench candidates by total minutes, and a bench technical
foul is not treated as on-court evidence. Official-versus-ordinary score gaps
are checked before insertion. The job is resumable by design.

The cache system was also unsafe for updates: its keys depended only on date
bounds. `experiments/data_version.py` now bumps a database epoch before a write;
possession/context/outcome cache keys include it, and fixed game-player and
game-season artifacts verify it. New rows can no longer be silently hidden by
old multi-gigabyte pickles.

The new named case is Tyrese Haliburton. Indiana was 50-32 and reached the 2025
Finals, then went 19-63 while he missed 2025-26 following an Achilles tear.
That before/after is confounded and is not training evidence by itself. It is a
valuable model audit with three predeclared views: same-four Haliburton versus
replacement-guard lineups; mechanism changes in assist supply, teammate
assisted finishing, rim/threes, turnovers and pace; and a strictly preseason
posterior check on actual 2025-26 Indiana lineups. Teammate on/off effects are
an evaluation target only, not known-pair input to the primary mean.

`experiments/player_season_profiles.py` supplies the needed state semantics:
exact season overrides and otherwise the latest sufficiently observed season.
An injured Haliburton therefore retains his 2024-25 state in a 2025-26
counterfactual. That representation still needs rolling-origin predictive
validation before replacing cumulative prior profiles.

---

# §39 Verified 2025-26 refresh, corrected reliability and current-state cases (2026-09-04)

## Data accounting

The update is complete: **32,190 games and 6,059,380 possessions through
2026-06-13**. Offline `bref_audit.py` reparsed all 2,492 targeted games and
compared every stored possession's canonical signature. Of 2,465 existing
games, 2,455 changed and ten were unchanged; 27 missing games were inserted.
Original replaced rows are backed up under the ignored raw-cache
`database_repairs/1788577025507373000-37f71aa800a1/` directory.

The full pass exposed same-clock and-one mismatches, out-of-order free throws
with interleaved rebounds/turnovers, dead-ball rebound artifacts, bench
ejections mistaken for starter evidence, and scoring lost across period ends
or substitutions. All games now reconcile ordinary plus explicitly recorded
technical points to official scores exactly. Possessions crossing a substitution
still use one scoring-lineup snapshot: an explicit schema approximation, not
full event-level attribution. This update does not repair the 32 older empty
or very short games identified in §38.

Outcome targets and player profiles now agree on credited player ORBs and
nontechnical special FTs. Derived caches were rebuilt under the new data epoch.
An index on `nba.possessions(game_id)` makes audits and per-game repairs
practical; its reproducible DDL is in `experiments/sql/`.

## Reliability reporting correction

The contextual point scorer previously averaged split-wise disattenuated
correlations while dropping nonpositive estimated true variances. Near-zero
denominators produced impossible values (including an old 2018 value above
one), and could dominate an average. `reliability.py` now pools covariance and
variance moments before division, retaining negative split estimates in the
average. Impossible pooled ratios are flagged as unidentifiable, not clipped.
Season summaries pool moments too. **Old rho headlines are superseded.**
Raw r², ordinary correlation, MAE and fitted means do not change from this
reporting fix. Individual low-information origins remain unidentifiable.

## Forward prediction and latest-state trade

On 2016–2026 expanding-history origins, assist deficit versus calibration only:

| metric | calibration only | + assist deficit | season-paired change ± SE |
|---|---:|---:|---:|
| MAE, points/100 | 7.600 | 7.497 | −0.10685 ± 0.03309 |
| raw r² | −0.0075 | +0.0100 | +0.01784 ± 0.00526 |
| ordinary correlation | 0.164 | 0.199 | +0.03639 ± 0.00668 |
| pooled-moment reliability rho | 0.410 | 0.499 | not an average of season ratios |

Latest observed player-season state versus cumulative state is approximately
tied: MAE 7.474 versus 7.497, paired difference −0.01879 ± 0.05154; raw r²
0.0139 versus 0.0100. Latest state loses in 2025 and 2026, so this is a
product-representation trade, not a uniform recency victory. Each case now
uses calibration fitted for its own representation and an explicit history
cutoff. Shared usage ledgers also match validation.

## Intervals and named counterfactuals

For 2019–2026 held-out future half-game-sample lineup outcomes, latest-state
coverage is **50.2%, 79.8%, 95.1%** at nominal 50/80/95%. The conservative
tail arm covers 97.5% at nominal 95% across 64 distinct season-lineup cells.
For cumulative state, constant tail coverage is 91.2%; the conservative tail
arm reaches 95.1% across 60 cells. Repeated split rows are not independent
lineups. This validates finite-batch coverage in observed data, not impossible
lineups' latent means.

The diagnostic panel now prevents a sparse tail's noisy near-zero variance
from granting extra certainty. Latest-state five Goberts scores 106.69 with
diagnostic 95% range 91.75–121.62, compared with Jokić/Korver 122.60 and
114.82–130.38. Jokić/Westbrook scores 119.48; its relative-to-additive residual
is −3.27 points/100 before calibration. The latest-season choices are printed,
including Korver 2020 and injured players' most recent observed seasons.
Valuation, defense and actual-opponent uncertainty remain incomplete.

The exact-2025 Haliburton-for-McConnell swap beside
Nembhard/Nesmith/Siakam/Turner adds **2.75 points/100**. Its freely additive
gap is +2.62 and finite-ledger gap +3.41, giving +0.80 contextual residual
before calibration. Assist supply rises 1.48/100, 3PA rises 9.51 and turnovers
fall 1.15. No known-pair feature is involved.

On supported actual 2026 Indiana fours using preseason states, healthy-2025
Haliburton for Nembhard adds 5.05 points/100 and lowers assist deficit 5.58/100;
for McConnell it adds 3.24. The supported observed-rotation forecast is 114.93
versus actual 116.34, but covers only **44.9% of all Pacers possessions**.
Full-team ordinary offense is 111.80. Thin player histories and low-minute
lineup exclusions make this a conditional audit, not a whole-season forecast
or causal explanation of the 19–63 record.

## What this checkpoint does not settle

Next test offensive rebounding in isolation. Its fitted valuation coefficient
is negative conditional on attempts, while the fixed usage ledger gives no
extra shot opportunity when rebounds rise. A rebound-dependent opportunity
budget is a proposed experiment, not an established fix. Add partially pooled
rookie/thin-history states, real small-ball checks and remaining latent/OOD
uncertainty before building direct defensive/opponent interactions. The HTML
tool is unchanged. All 84 database-free unit tests pass.

Persistent evidence: `experiments/cache/*_2026.csv`,
`haliburton_case_2025.csv`, and `bref_audit.csv`. Exact commands and backup
location are in `SESSION_HANDOFF.md`.
