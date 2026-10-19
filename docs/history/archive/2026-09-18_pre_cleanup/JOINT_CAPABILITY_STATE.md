# The joint-capability model: where it stands after v10

## v10 addendum — 2026-09-13

Final independent qualifications are in
`reports/joint_capability_v10_codex_review.md`. The blend improves season-paired
RMSE against additive overall and on novel fives. Five-Gobert final offense
remains unresolved, and smaller contextual increments alone do not establish
worse coherence. Define the individual/context split before a new model build.

Day4 is complete and independently reviewed in
`reports/joint_capability_v10_review.md`. On the fixed 2016–2026 primary
population, corrected additive / `V9_SPREAD` / their fixed-half blend scores
8.09195 / 8.14017 / **8.07274 MAE**; the blend reaches **.12576 raw r2** and
improves novel MAE to **8.83865**. A prior-only fitted blend is tied. This is the
clearest evidence that individual-value and contextual forecasts contain small,
useful complementary information.

Adding team-point supervision did not solve the backbone. Alpha 1 reaches
8.11221 MAE and improves BASE by -0.02619 mean season MAE, but the 95% interval
[-0.07605,+0.02367] crosses zero; it trails additive, improves its directly
supervised native team MSE only 0.027%, worsens outer event loss in 11/11
seasons, and attenuates contextual fixtures. Alpha .1 is worse. Neither is
adopted. A post-run half additive/alpha-1 blend reaches 8.05677 MAE but is
exploratory and slightly worse than half-BASE on novel lineups.

Exact event-to-point accounting shows useful volume/location/conversion changes
partly canceled by calibration and one another. The next experiment is therefore
an explicit cross-fitted, shrunk individual-value mean arm plus a zero-centred
`V9_SPREAD` context residual—no known-pair chemistry. Corrected additive remains
the standalone predictive baseline, `V9_SPREAD` the structural backbone, and
fixed half the best pre-registered combined forecast. Latent-mean OOD uncertainty
remains unfinished; no scorer was promoted.

**Historical v2–v9 synthesis follows.** Its broad ceiling and mandatory
evaluation-power claims are qualified by the v10 review and
`reports/joint_capability_v5_v9_codex_review.md`. The following private artifact
still contains the v9 version; it has not been republished with this addendum.

**Published as a private artifact:**
https://claude.ai/code/artifact/d42ff3c4-21b7-4072-8af1-1d6eb2fdab60
(same content, easier to hand to another agent or read on a phone; republish from
this file's content, never edit the page independently of this file).

2026-09-12 (Opus + Adam). A synthesis across v2–v9, written to answer one
question Adam asked directly and which had only ever been answered in
conversation:

> **Is there any hope for a non-additive model to exceed the additive one?**

Per-version detail lives in `reports/joint_capability_v*_review.md` and
`JOINT_CAPABILITY_LEARNINGS.md`; the do-not-re-run lists are `BACKLOG.md`
§0ae–§0ak. This file is the standing summary and the case for what to do next.

---

## The short answer

**On pooled MAE: no, not with this data, and it is the wrong target.**
**On novel lineups — the slice the northstar actually cares about — it already
does, and has in every version since v5.** The pooled gap is a *mixture* of a
novel-slice win and a recurring-slice loss, and neither is established because
**the benchmark cannot resolve effects of this size.** That last fact is now the
binding constraint on the entire workstream, ahead of any model work.

---

## What the model is

**1,814 parameters in the incumbent backbone, 2,390 with v9's addition.** Nothing
about it is a generic network; almost all of it is hand-designed structure.

- **Input:** 18 anchored coordinates per player, from his own prefix history —
  3 log rates (FGA/FTA/TO), 6 centred location logits, 6 location-conditional make
  logits, an FT logit, a log assist rate, an assisted-made logit. 13 effective
  free dimensions. **Standardised** since v8; raw for the first seven versions.
- **Context:** one round of message passing over the five-man complete graph,
  `msg_i = M(x_i, summary_{j≠i})`, permutation-invariant. The summary is the
  leave-one-out **mean and standard deviation** since v9; mean only before that.
  `Linear(54,32) → Tanh → Linear(32,18)`, output zero-initialised.
- **Decoder:** diagonal affine, `intercept + slope · z`, 36 parameters. No
  cross-coordinate mixing, and v9 established that this costs nothing.
- **Accounting:** fixed, not learned — softmax over six locations, sigmoid
  conversion, a **shared finite opportunity budget** `U = FGA + 0.44·FTA + TO`
  renormalised across the five, and the exact point identity. Free-throw
  conversion is masked from the message: teammates cannot change it.
- **Objective:** five event families (Poisson counts, multinomial location,
  binomial conversion, binomial FT, binomial assisted share), each normalised by
  the untrained model on a **shared** reference set. Not points.
- **Protocol:** 48 quarterly origins; an inner quarter selects the epoch, then a
  refit on the full prefix for exactly that many epochs; the outer window is never
  inspected. Prior-only affine point calibration on top.

---

## The scoreboard, 48 origins, 12 seasons, 6,179 cells, 803,447 possessions

| | pooled | **novel fives** | recurring |
|---|---:|---:|---:|
| corrected additive | **8.0343** | 8.9217 | **7.6455** |
| `V9_ALL` | 8.0680 | 8.8871 | 7.7090 |
| `V9_SPREAD` | 8.0730 | **8.8784** | 7.7201 |
| `V8_BASE` | 8.0663 | 8.8758 | 7.7116 |
| 50/50 blend | **8.0066** | — | — |

Season-paired, `V9_ALL` − additive:

| slice | effect | seasons favouring neural |
|---|---|---|
| pooled | +0.0302 ± 0.0393 | 6/12 |
| **novel fives** | **−0.0362 ± 0.0527** | **9/12** |
| recurring | +0.0570 ± 0.0438 | 4/12 |

On novel lineups the neural arms also win **RMSE** (11.7482 vs 11.8193) and
**r²** (0.1341 vs 0.1235), and v9 improved both materially over v8 (r² 0.1287 →
0.1341). On recurring fives the additive wins on every metric.

**The sign flip between slices is the structure**, and it is what the pooled
number hides. The additive's overall lead comes entirely from lineups that recur —
where its per-player coefficients have been fitted on those very lineups'
history — and it loses where the model has to price a five it has never seen.
`CLAUDE.md` is explicit that `novel_off5` is the slice that counts.

---

## What is established

Only a short list, and two of the three are from the last two versions.

1. **Mean pooling carries the whole teammate effect** (v4): novel RMSE −0.122,
   11/11 seasons. Pair pooling and a learned encoder add nothing.
2. **Standardising the message inputs** (v8): event loss **−4.12e-04 ± 4e-05,
   12/12 seasons, 47/48 origins**, every family. The 18 coordinates had means from
   −3.663 to +1.307 and a 9.7x sd range and were fed raw for seven versions.
3. **Teammate VARIETY** (v9): the leave-one-out sd, **−2.46e-04 ± 2e-05, 12/12
   seasons, 45/48 origins**; **−6.58e-04 stacked with (2) against `V8_BASE`**, for
   576 extra parameters. Phase 0 predicted it with no fits — teammate sd is 98.1%
   orthogonal to teammate mean.
4. **λ = .01 is an interior optimum** (v4 + v5, two independent runs); lr, width
   and γ are audited interior (v7 H0.1); the epoch cap is not binding.
5. **`k_make_over` fits non-zero in 48/48 origins** (v7): overloading a player
   costs his shooting and not his turnovers. Mechanism, not accuracy.

---

## What is closed — the expensive half

- **Inputs** (v5, six arms): opponent-deconfounded states, height/position,
  offensive rebounding as a 19th coordinate, the 46 unused features routed into
  the message, all four together, points-leverage family weights. **Every one null
  or harmful**, and `ALL` was the exact sum of its parts.
- **Training population** (v6, v7): withholding the unusual lineup quartile is
  free; withholding the top 2% of donors beat its matched control by
  −0.0164 ± 0.0077 (7/12) and **did not reproduce** as a continuous trim at a
  matched footprint (v8); withholding the top 5% is established harm.
- **Objective conditioning** (v8): the message penalty's units were genuinely
  mis-set (one sd of effect cost `sd_j²`, a 93x spread) and correcting them
  reallocates the budget exactly as diagnosed and **buys nothing**. The 730-day
  row half-life survives its audit; 365 is harm; the additive/neural time
  asymmetry was costing nothing.
- **Architecture beyond the second moment** (v9): a **second message round is
  established harm** (+4.05e-05, 3/12) even though the block grew to 45% of round
  one; a non-diagonal decoder is null; min/max matches sd with a 26% larger block.
  Usage-weighted senders died in Phase 0.
- **Conversion via teammate identity** (v7 `V7_SHOT`): the §10 shot-quality
  coefficient in the message is **established harm on conversion**
  (+0.000033 ± 0.000008, better in 1/12 seasons). The live conversion route is
  role, not identity.
- **Distance-aware intervals** (v8 P0.1): a third independent method, a third
  null. The ensemble spread *is* a composition measure (r = +0.1526 with distance)
  and composition does not order forward error in range (+0.0093).

---

## Why pooled MAE will not move

Three reasons, in order of weight:

1. **The two models are reading the same information.** Their forward errors
   correlate **0.9826** (§8b–8c measured 0.9856 independently). A 50/50 blend
   reaches 8.0066, better than either, and §8c established the whole prize from
   optimal combination is 0.15% of RMSE — so that is banked and closed too.
2. **The non-additive budget is small.** The forecastable non-additive ceiling is
   **+0.00017 r²** against the additive stack's **+0.0018** forward — roughly 9%.
3. **The benchmark cannot see the gains we are making.** v8 regressed the
   per-arm-per-origin MAE gain on the event-loss gain across 288 paired deltas:
   **slope −3.68 ± 21.39, r = −0.0102.** v9 retested with an effect 1.6x larger and
   the answer held — the objective improved −6.6e-04 at 12/12 seasons while
   `V9_ALL − V8_BASE` in points was **−0.0008 ± 0.0254**.

Point 3 is not evidence the improvements are fake. It is evidence about the ruler.

---

## The binding constraint, and the recommendation

**Build a point evaluation with power, before any further model work.**

Two consecutive versions have produced real, unanimous improvement to the model's
own objective, and the point benchmark has moved 0.0008 ± 0.0254. An ~84-possession
evaluation cell is mostly finite-batch noise, which is why the population resolves
a lever worth ~0.04 MAE and cannot establish one worth ~0.01. Until this is fixed:

- No architecture or objective arm can be graded.
- The additive comparison (+0.0302 ± 0.0393, unchanged since v7) stays permanently
  unresolvable.
- The novel-slice result (−0.0362 ± 0.0527, **9/12**) — the most promising number
  in the project — cannot be established even though its sign has been stable
  across five versions.

Three routes, cheapest first:

1. **A paired design.** Score every arm on the same possessions and difference the
   batch noise out *before* aggregating, rather than comparing two noisy cell
   means. Costs nothing but code.
2. **More cells.** Relax the exposure floor and weight correctly. The current
   population is 6,179 cells from 803,447 possessions out of 6.06M.
3. **A lower-variance target.** Score the centred/detrended score rather than raw
   points per 100, which is what the rest of the repository already does
   (`CLAUDE.md` conventions).

Then, and only then: **tracking** (`BACKLOG` §0ai — pair-level passing is the one
genuinely new input available, and the pair block must be refitted on the tracking
era first), and **a richer set summary** than mean+sd, since the second moment paid
and nobody has looked further.

---

## Two corrections worth carrying forward

**"We tried X, Y and Z and they failed" is not "that class of change fails."**
After v8 I told Adam the architecture was a dead end. That generalised from three
*capacity* axes — width, the encoder, pair pooling — to the architecture as a
whole. He pushed back; the best-supported single change in the workstream came out
of the axis I had never tested.

**A normalised loss is only comparable if the normaliser is shared.** Through v7
each arm's event loss was divided by the untrained model on *that arm's own*
training rows, so any arm that reweighted moved its own denominator — an artifact
3.5x the effect, reading 21.4 sem out of nothing. v8 fixed it and verified the
baseline identical to 0.00e+00 across 288 arm-origins. Every event-loss number in
this file is post-fix.

---

## Decisions of record

Everything here is a decision, not a measurement — the measurements are above and
in the per-version reviews. Adam's calls are marked; the rest were taken in the
work and are open to revision with a reason.

### Scope and priority

1. **A point evaluation with power comes before any further model work.**
   Tracking, richer set summaries and further architecture all queue behind it.
   (§0ak item 1. This is the live decision and everything else defers to it.)
2. **Gates, coverage rules and anything the page prints are product decisions,
   deferred.** *(Adam, explicitly, twice.)* v8's P0.2 comparison of the learned
   duplication penalty against the asserted gate is recorded in
   `V8_PHASE0_FINDINGS.md` and **parked**, not pursued. Model improvement only.
3. **Do not change the objective.** v8 established the objective/target gap is
   **resolution, not misalignment** (slope −3.68 ± 21.39, r = −0.0102 over 288
   paired deltas; retested in v9 at 1.6× the effect). The five event families
   stay.
4. **The additive comparator is frozen.** It is called with no profile-recency
   `halflife`; switching that on retroactively invalidates every gap quoted since
   v2. If it is ever tested it must be a separately named comparator reported
   beside the frozen one.
5. **Tracking is deferred by decision, not drift** (§0ai). When it resumes, refit
   the pair block on the tracking era first so target and features share a period.

### Measurement

6. **Event loss on a SHARED baseline is the primary readout; points are
   secondary and a null is expected.** One baseline per origin, handed to every
   arm, verified identical to `0.00e+00`. Any future version must keep this.
7. **Quality thresholds are measured and recorded, never asserted as run gates.**
   *(Adam: "i don't like assertion gates so let's get away from that idea.")* An
   assertion destroyed a 2-hour v7 sweep at origin 39/48 over one pair-origin at
   3.22% against a 3% threshold; dropping that origin moved the headline by
   0.0001. Correctness invariants that can only fire on a bug — `assert_unseen` —
   are a different animal and stay.
8. **Report mean |difference| in the units the product prints, beside any
   correlation.** v6 read r = 0.9966 and called an extrapolation failure a
   success; v7 found a 3.2× level shift at r = 0.9958.
9. **Difference-in-differences before claiming a benefit is localised.** It is
   what separated "prices donors better" from "is a better model everywhere" in
   v7, and only the second survived.

### Process

10. **No secondary arm blocks.** `V6_SHOT` and `V7_SHOT` each sat in one for a
    version and were never launched; it cost 30 minutes to run and closed a
    question open since v2. An arm is either in the run or not in the plan.
11. **Every arm must be exactly nested and zero-initialised**, reproducing the
    base arm at initialisation, so a null reads "the data did not pay" rather
    than "it started elsewhere". Verified at `0.000e+00` for all six v9 arms.
12. **Log how far each new block grew.** `V9_DEPTH` reached 45% of round one and
    still hurt; `V9_DECODER` reached 4.7% and did nothing. Different findings,
    and only the growth log separates them.
13. **Size a reweighting before running it.** v9's trim was reparameterised twice
    on the weight distribution alone, before any fit.
14. **Build the plan and run it rather than over-sizing first.** *(Adam: "I'm not
    sure how exact we can know these ablations before we try them.")* Phase 0
    exists to kill arms that cannot work, not to predict effect sizes.
15. **Each version ends in a written record and a commit** *(Adam)*: the five
    headings in `JOINT_CAPABILITY_LEARNINGS.md`, `MODEL_SCORECARD.md`,
    `BACKLOG.md` open and do-not-re-run entries, `CLAUDE.md`'s header,
    `SESSION_HANDOFF.md`.

### Adopted into the backbone

16. **Standardised message inputs** (v8 `V8_STD`) and **the leave-one-out
    teammate standard deviation** (v9 `V9_SPREAD`). Both are free, both moved the
    objective in 12/12 seasons, and neither pays in points. Any future backbone
    starts from them.
