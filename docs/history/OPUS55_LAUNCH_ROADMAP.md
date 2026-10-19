> **Advisory proposal — Opus 5.5, 2026-09-23.** Written at Adam's request as a
> high-level design and roadmap to launch. It is not current guidance and
> authorizes no training, export or publishing. Current state, scores and the
> backlog remain in [JOINT_CAPABILITY_STATE.md](JOINT_CAPABILITY_STATE.md),
> [MODEL_SCORECARD.md](../../MODEL_SCORECARD.md) and
> [MODEL_RESEARCH_ROADMAP.md](../../MODEL_RESEARCH_ROADMAP.md).

# Roadmap to launch — from v16 to opening night

## Context

Adam wants the lineup tool live shortly before 2026-27 opening night, about one
month from today (Wed 2026-09-23; opening night **assumed ~Tue Oct 20** — confirm).
v16 is running (27/48 origins; forecast to finish ~Sep 26–27 plus its automatic
analyses). This document is the high-level design and roadmap from here to
launch. It proposes work; it authorizes no training, export or publishing.

**Launch goals (Adam, 2026-09-23):**

1. **Demonstrably better than additive models such as RAPM** — registered
   historical intervals with multiplicity handled, holding on novel lineups, and
   beating plain RAPM as well as the repo's prior-informed additive. No
   prospective test required; selection has already used all seasons.
2. **Calibrated uncertainty** shown alongside every point prediction.
3. **Reasonable point predictions and distributions for any lineup**, including
   five centers. The tool shows the model's output and uncertainty for every
   lineup; no coverage rule. Unsatisfactory lineups are improved in later
   versions, not patched.

**Headline rule (Adam):** ship the most accurate forecast that can still be
explained clearly. Today that looks like a 50/50 blend of the neural model and
the additive. More training versions before launch are allowed.

---

## Design

### 1. Architecture: research → export contract → static page

The page stays a self-contained static artifact, like today's `tool/five.html`:
all data inlined, no server. The Artifact CSP blocks runtime fetches, including
WebAssembly runtimes, so **the neural forward pass is hand-written JavaScript**,
not ONNX. That is feasible because every model is small and uses only matmul,
tanh, softmax, sigmoid, exp, clamps and the accounting identities.

The key decision is a **versioned export contract** between research and the
page, so a later version can replace the model without rewriting the tool:

- `schema_version`, model id, data cutoff, provenance hashes
- player-season table: states, role descriptors, adjusted-capability banks,
  support features (default = latest season; earlier seasons selectable)
- per-seed network weights for the headline neural model
- additive ratings and calibrations for the blend's other half
- calibration parameters (the registered prior-only affine fits)
- uncertainty-model coefficients (see §4)
- a prior-defensive-five reference set for "vs league average"

Reuse the existing pattern: `tool/build.py` splices a data literal between
anchors; `experiments/tool_model.py` is a pure-Python mirror of the page's
arithmetic that `experiments/tool_audit.py` scores against real units. Do the
same for the neural page — a NumPy reference scorer of the *exported* artifact —
so parity is tested at two joints: torch ↔ export, export ↔ JavaScript.

**Budgets:** artifact hard limit 16 MB → target ≤ 10 MB using quantized
base64 arrays rather than JSON decimals. Rating against league average needs
many forward passes (v16 §8 integration) → run in a web worker and choose the
reference count from v16's convergence study, displaying integration error
when it exceeds 0.10 pts/100.

### 2. What the page shows

Per the product contract §1: two five-man teams (Team B defaults to league
average), player-seasons, offense / defense / margin in pts/100, the mechanism
ledger, who is pushed out of role, and uncertainty with its reason in
basketball language.

- **Headline:** blended offense, defense and margin, with an interval.
- **Two views, shown side by side:** *sum of players* (additive, per-player
  contributions) and *lineup-aware* (neural). The blend is their calibrated
  average; the gap between them is the lineup effect.
- **Why:** the neural event ledger — FGA/FTA/TO per 100, shot location,
  conversion, rebound capture and renewal — against each player's usual role,
  flagging role displacement (predicted share vs historical share).
- **Support indicator:** how far this lineup sits from observed lineups, in
  plain language, driving the interval width.

**The explanation criterion**, used in the candidate rule: every component of
the headline must have a faithful, displayable breakdown. The additive half
explains by player contributions; the neural half by its ledger. Attention
weights are routing, not explanation — the ledger remains the source.

### 3. Uncertainty

Build on v16 §9 rather than inventing a second method. v16's U2 fits a
persistent-discrepancy variance whose log is linear in support features
(minimum player support, role/composition/opponent distance, coefficient-
variance projection, seed disagreement), fit strictly on prior windows.

- **Gap to close:** v16 fits U1/U2 only for a fixed set (old HALF+D, J_BOTH half,
  J_ALL_BOTH half). The launch forecast must get its own U2 fit after selection.
- **The interval on the page** combines finite-game noise (U0) and persistent
  discrepancy (U2) through the working model, **not** by adding separately
  estimated variances in quadrature — v16 §9 forbids that double count.
- **Out of support:** five centers sit outside U2's fitting range, so their
  width is an extrapolation of the log-linear support model. The page labels it
  as extrapolation. A wide band does not repair a poor mean (v16 §10); the
  limitations text says so.
- **Fallback:** if U2 is `NOT_IDENTIFIED` for the candidate, ship U0 bands plus
  the support indicator, and say why the larger quantity is unavailable.

### 4. Evaluation: "demonstrably better"

A registered launch-evaluation plan, written **before v16's final report is
read**. Adam declined a split-sample holdout, so the discipline comes from a
declared rule and from accounting for selection:

- **Candidate rule:** the most accurate forecast passing the explanation
  criterion, by broad-population all-cell RMSE (MAE as secondary); order
  invariance and margin antisymmetry must pass exactly.
- **Comparators:** corrected additive, **plain RAPM** (new), old HALF+D.
- **Plain RAPM:** career-only ridge for both sides from
  `experiments/asof_additive.py` (`solve(career, prior, experience, delta)` with
  the last three blocks switched off), tuned by the same prior-only protocol,
  scored on the same origins, cells and calibration. Verify the nesting rather
  than assume it.
- **Contrasts:** all / novel / recurring; legacy 5,607-cell and broad ≥50
  populations; 10,000 season-block resamples; Holm within the launch family.
  Reuse the machinery in `experiments/v15_postrun_review.py`
  (`contrasts.csv` format).
- **Selection-aware intervals:** bootstrap the *whole selection* — in each
  resample, re-apply the candidate rule over all eligible forecasts and record
  the winner's margin. That prices in best-of-22 optimism honestly.
- **The headline question gets its own row:** neural − additive and blend −
  additive, never yet computed in a registered analysis.

---

## Roadmap

Four workstreams: **Evaluation**, **Uncertainty**, **Tool**, **Model**. They can
run in sequence under one editing agent or in parallel if `AGENTS.md` is amended;
roles are undecided. **The tool is the critical path and starts this week.**

### Week 1 — Sep 23–29: v16 finishes; build what doesn't depend on it

- **Evaluation:** write and commit the registered launch-evaluation plan;
  implement plain RAPM with a nesting test; run its full fit after v16 finishes
  (it loads the possession caches — avoid competing with three workers).
- **Tool:** define export schema v1; hand-port the shared v14/v15 backbone
  forward pass to JavaScript; NumPy reference scorer; parity test against saved
  v15 predictions; page layout and content design.
- **Hygiene:** scope `NEURAL_MODEL.md` §2's free-throw-isolation claim to the
  rank-zero backbone (v9 decoder defect); commit the uncommitted v16 case-preview
  viewer and tests with the next authorized checkpoint.

### Week 2 — Sep 30–Oct 6: results, candidate, uncertainty

- **Evaluation:** read the v16 review; apply the candidate rule; run the
  registered evaluation; three-pillar matrix; read the action-allocation arms on
  the five-center fixtures, not only the leaderboard.
- **Uncertainty:** fit U2 for the candidate; coverage by support bin on held-out
  real lineups; five-center monotonicity check.
- **Tool:** choose the integration reference count from v16 §8; begin exporting
  real player tables.
- **Checkpoint 1 (Adam):** does the candidate meet "demonstrably better"? If not,
  choose: launch with the claim worded to the evidence, use another eligible
  forecast, or rely on a further version.
- **Model:** optional v17, scoped from the v16 reading, with fixtures read first.

### Week 3 — Oct 7–13: build and freeze the model

- **Tool:** port the candidate's heads; full export; parity ≤ 1e-3 pts/100 on a
  fixed panel (case library, random real lineups, low-support and debut players);
  UI for two teams, ledger, band and support indicator.
- **Model freeze ~Oct 13:** only versions whose registered analysis is complete by
  then are eligible for launch; later versions ship afterwards.

### Week 4 — Oct 14–19: harden, document, launch

- **Acceptance suite** (below) run against the exported page, not the notebook.
- **Documentation:** model card — what the number means, the population it was
  scored on, what the interval does and does not cover, known limitations
  including five centers; methodology page; changelog.
- **Launch (authorized by Adam):** publish; preserve the additive page source in
  the repo.

### After launch

Improve out-of-distribution coherence (the five-center allocation failure),
tracking data (roadmap R12), and — optionally, since it becomes free — score the
launched model on 2026-27 games as they arrive.

---

## Launch acceptance (go/no-go)

| Pillar | Check |
|---|---|
| Prediction | Selection-aware 95% intervals exclude zero for the headline vs corrected additive **and** vs plain RAPM, all-cell RMSE, legacy and broad; same direction on novel lineups |
| Coherence | Frozen v16 case library runs in the exported page; order invariance and margin antisymmetry exact; five-center ledgers reported as the model gives them, no forced ranking |
| Uncertainty | Held-out real-lineup coverage within ±5 points of nominal in each support bin; five centers measurably wider than a conventional real five; displayed integration error < 0.10 pts/100 |
| Engineering | JS ↔ Python parity ≤ 1e-3 pts/100; page ≤ 10 MB; no runtime fetches; works at 400 px in both themes; league-average rating under ~1 s |

---

## Risks

1. **Tool port is unstarted and on the critical path.** Mitigation: start Week 1
   on the shared backbone, independent of which arm wins.
2. **The candidate may not clear "demonstrably better"**, especially vs the
   corrected additive once selection is priced in. Mitigation: plain-RAPM and
   blend rows are likelier to clear; Checkpoint 1 decides the wording.
3. **U2 may be unidentified or extrapolate badly for five centers.** Mitigation:
   U0 + support indicator fallback, labelled honestly.
4. **Browser performance** of league-average integration. Mitigation: web worker,
   reference count from v16 §8, integration error displayed.
5. **Page size.** Mitigation: quantized arrays; earlier player-seasons optional.
6. **Late model swap.** Mitigation: the export contract; a hard freeze date.
7. **Roles.** One editing agent means workstreams serialize; the plan fits one
   agent only if the tool starts now.

## Open decisions for Adam

- Confirm the opening-night date and the launch day.
- Publish venue: replace the page at the existing tool URL (the repo convention)
  or publish alongside it.
- Roles: who takes which workstream, and whether `AGENTS.md` changes to allow
  parallel work.
- Scope of any pre-launch v17 after reading v16.

## Assumptions

- Latest player states come from 2025-26 (data through 2026-06-13); 2026 rookies
  and players without NBA minutes use pooled prior states with wide bands. No
  data refresh is needed for launch.
- The v16 campaign completes without intervention; nothing here touches it.
