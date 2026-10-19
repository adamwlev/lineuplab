> **Historical neural notebook — 2026-09-18 notice:** This records learning
> through v10, not the current v14/v15 architecture or v16 priorities. Broad
> “closed” claims apply to the specific tested settings; see the
> [independent v5–v9 review](../../reports/joint_capability_v5_v9_codex_review.md) and
> [current backlog](../../MODEL_RESEARCH_ROADMAP.md) for qualifications. Current
> implementation is described in [NEURAL_MODEL.md](../../NEURAL_MODEL.md).
> Original notebook body follows unchanged.

# Joint capability: learnings by version

One section per version, appended and never rewritten. Each carries the same five
headings so the arc is readable end to end: what changed, what was established,
what was killed, what it cost, what stayed open.

Negatives are the expensive half of this record. A killed mechanism is worth as
much as an established one, and more than a result nobody trusts.

Source reviews, in order: `reports/joint_capability_v3_review.md`,
`reports/joint_capability_v3_codex_review.md`,
`reports/joint_capability_v4_review.md`, and the external critiques
`CLAUDE_MODEL_FEEDBACK_2.md` (v2), `_3.md` (v3), `_4.md` (v4).

---

## v2 — 2026-09-09 — `joint_capability_2026_09_09_v2`

### What changed
First implementation of `JOINT_CAPABILITY_MODEL_PLAN.md`. Four arms over the
encoder × message factorial: H0 (anchored states only), H1 (learned own-state
encoder), H2 (teammate messages), H3 (both). 48 origins each.

### What was established
The native, pre-calibration correlation with actual rose monotonically across the
four arms — .3192 / .3271 / .3305 / .3340 — and correlation is invariant to any
affine map, so that ordering is discrimination rather than level. H3 posted the
best novel-lineup r² on record at the time (.10770) and degraded least from `all`
to `novel` (−0.009 against the corrected additive's −0.033).

### What was killed
Nothing. The factorial was not identified — see below — so no arm contrast could
be believed.

### What was established, found late

- **The message is a learned duplication penalty.** It leaves real lineups alone
  (+0.196 mean swing) and pulls repeated-player lineups down in proportion to
  composition distance (−3.004 ± 0.432 at matched score, 8/8 origins). That is
  what `tool/five.html` asserts and what four fitted attempts failed to produce —
  `distance_shrink.py`, floor geometry, index curvature, defensive coverage.
  **It escapes selection-on-the-outcome by construction:** the message is fitted
  on five event-level families per player, never on lineup points, so the bias
  that made every previous fit extrapolate the wrong way pushes AGAINST this
  result rather than producing it. Direction established; **magnitude
  uncalibrated** and that is the v8 question.

### What it cost
192 arm-origins, 384 fits, 3,077 s. Roughly one wall-clock hour.

### Still open — the defects that defined v3
- **The control never trained.** One λ multiplied `own + context + decoder`, and
  the decoder is shared by every arm. H0's λ was selected at 1.0 by a tie-break
  over a grid whose entire response spanned 2.9e-5 against a 1e-4 tolerance, so
  H0 was penalised 100× harder than H3 on identical shared parameters and
  **selected epoch 1 in 48 of 48 origins**. CLAUDE.md rule 10 in a new costume.
- **The 730-day training weight the protocol required was never implemented.**
- **The model sat ~2% off its initialisation** — RMS state corrections of
  0.04–0.08 against base coordinates of 1–4, from roughly 250–400 Adam steps.
- **No placebo existed.** `joint_capability_diagnostics.py` was never written;
  10 of ~20 required tests were present.
- Most of the headline MAE ordering was level: debiased, it read
  8.1584 / 8.1596 / 8.1607 / 8.1516 — flat.

---

## v3 — 2026-09-09 — `joint_capability_2026_09_09_v3`

### What changed
Every v2 defect above was repaired. The decoder penalty was separated from the
network penalty (common γ = .01); the 730-day training weight was implemented;
stopping went from 12 epochs / patience 2 / min-delta 1e-4 to 24 / 3 / 1e-5;
losses accumulated global numerator and exposure before dividing; masks began
preserving unknown actors instead of zeroing them; origin states stopped being
selected by the future roster. A fifth arm, **H3F**, gave H3's exact capacity a
fixed reference sender — the first real control for teammate information.

### What was established
- H3 beat H3F on outer event loss in **44/44** primary quarters.
- The date/role-bin context shuffle favoured H3 **4/4** at the diagnostic origins.
- The free-throw negative control was a clean null: real minus fixed sender
  +4e-6 NLL, mixed 2/4 — teammates do not move FT conversion, as designed.
- Seed sensitivity was tight at the event level, max |Δ| 3.2e-4.
- Points: H0 8.1754, H1 8.1586, H2 8.1228, H3 8.1229, H3F 8.1604, against
  corrected additive 8.0920.

### What was killed
Nothing definitively, but the encoder began to look null: H3 − H2 read
−0.006 RMSE at 6/11 seasons, with H2 carrying 2.5× fewer parameters.

### What it cost
240 arm-origins, 480 fits, 631 tests.

### Still open
- **λ mismatch, mirrored.** H3 selected .0001 on the extended low boundary while
  its same-capacity control H3F sat at .01. The grid-extension rule gave the
  candidate a search the control never got. The effect size survived a matched-λ
  substitute (H2 − H3F, −0.046 against H3 − H3F's −0.052); the *interval that
  excluded zero* did not.
- **Conversion did not move** — FG Brier spread 0.22% across every arm.
- **Fixture magnitudes were 226% and 192%** of the largest context effect the
  model produces on any real lineup.
- **"Exceptional lineups are shrunk too hard" was a selection artifact** — every
  arm, additive included, has a dispersion slope of ~0.88, i.e. over-dispersed.
- The support measure had no dynamic range, capping the interval work.

---

## v4 — 2026-09-10 — `joint_capability_2026_09_10_v4e` (+ report `_r3`)

### What changed
A 3 × 2 × 2 factorial: pooling {fixed, mean, pair} × encoder {off, on} × λ
{.01, .0001}, nine arms × 48 origins. **Mean pooling** — the receiver reads the
leave-one-out mean of the other four states — was the new mode. Three arms were
exact frozen-v3 aliases (E0P_L2 = H2, E1F_L2 = H3F, E1P_L4 = H3) with **function
parity 0.0** across 97 rows each and v3 source hashes verified.

The single best design decision: **λ became a declared factor rather than a
per-arm selection**, which removed the entire class of boundary-control problems
that compromised v2 and v3.

### What was established
**Mean pooling, and on novel lineups it is the strongest result of the workstream.**

| contrast | slice | metric | mean ± sem | 95% interval | seasons |
|---|---|---|---:|---|---:|
| E0M − E0F | novel | RMSE | −0.12239 ± 0.02678 | [−0.18206, −0.06272] | **11/11** |
| E0M − E0F | novel | raw r² | +0.02013 ± 0.00434 | [+0.01046, +0.02980] | **11/11** |
| E1M − E1F | novel | RMSE | −0.10948 ± 0.03931 | [−0.19707, −0.02190] | 9/11 |

For calibration: the opponent adjustment, the one lever in this repo that
unambiguously paid, was 9/11. Mean beat fixed on every reported event loss in
both encoder settings.

Points: corrected additive 8.09195 / 10.84099 / .12043; best neural E1P_L2
8.10963 / 10.85914 / .11749; E0M_L2 8.12239 / 10.87968 / .11414 with the best
novel MAE 8.85744; E1M_L2 best novel RMSE 11.77732 and novel r² .11181.

### What was killed
- **Pair pooling.** E0P − E0M is +0.02364 novel MAE and +0.01709 novel RMSE, both
  3/11 seasons. It buys a small in-distribution MAE gain with the encoder on
  (−0.01269, interval excluding zero) and is *worse* out of sample without it —
  the signature of overfitting, not chemistry. **The right word for what this
  architecture learned is "context," not "chemistry."**
- **The learned own-state encoder.** Every matched-pooling contrast is null:
  E1M − E0M all RMSE −0.01233 (5/11), novel RMSE −0.01848 (7/11), all MAE
  −0.00062 (6/11). 2,674 parameters for nothing measurable.
- **λ = .0001.** E1M_L4 − E1M_L2 novel RMSE +0.03233 [+0.00912, +0.05554] at
  3/11; E1P +0.03578 [+0.00429, +0.06727] at 2/11. Both exclude zero. This also
  explains v3's novel regression: its headline arm sat at .0001.

### What it cost
600/640 declared optimizer starts, 10,423.68 s of fitting (2.895 h), 640 tests.
Three aliases saved ~1.5 h honestly. Not run: any architecture change, defence,
rebound feedback.

### Still open — and these set v5
- **The FTA/deployment gap.** On the evaluation cells the model over-predicts FTA
  by **+2.9/100** against +0.1 on the full eligible cohort — the documented
  common-fives artifact (`ASOF_ACCOUNTING_AUDIT.md`, `ASOF_DEPLOYMENT_AUDIT.md`)
  reproduced almost exactly. An affine calibration absorbs the level but not the
  composition. It is an order of magnitude larger than the differences the arms
  argue over, and the largest single event gain from mean pooling is FTA NLL,
  which raises the question of how much of "context" is deployment.
- **Conversion still does not move** — FG Brier spans 0.07% across all nine arms,
  fourth version running — while carrying the *largest* lineup point dispersion
  of the three channels (sd 0.858 for mean vs fixed). The score is moved most by
  the channel measured to move least.
- **The opponent asymmetry.** `asof_additive.identity_design` returns `(n, 2P)`,
  offence *and* defence blocks, so the additive's θ_off is estimated controlling
  for who was defending. The neural model's 18 coordinates are raw historical
  rates. The two families are not on equal footing on their inputs.
- **Input poverty.** E0M_L2 reads 18 of its 64 features — E0 arms have no encoder,
  so exposure, missingness, recency contrasts, teammate reference, staleness and
  ORB are unused. Effective free dimensions per player: **13**, against
  `box_score_explains_rating.md`'s measured 32 for 78% of offensive rating.
  Offensive rebounding is absent from the budget entirely.
- **Fixture magnitudes remain 228% and 193%** of the in-range maximum, and the
  support measure was inherited unchanged, so the interval conclusion is a
  statement about the measure rather than the idea.

### Decision carried forward
Corrected additive stays the predictive baseline. **E0M_L2** is the structural
research backbone — 1,814 parameters, the smallest arm, holding the entire
teammate effect. E1P_L2 is retained as the strongest neural point reference.
No scorer promoted.

---

## v5 — 2026-09-11 — `joint_capability_2026_09_10_v5`

### What changed
v4 settled the architecture, so v5 froze it at the E0M backbone (leave-one-out
mean pooling, no encoder, γ = .01) and varied **only the inputs and the
objective**. Eight arms × 48 origins, each one factor: BASE (v4's E0M_L2
reproduced), OPP (opponent-deconfounded states), BIO (height/position), ORB
(rebounds per team miss as a 19th coordinate and sixth loss family), RICH (the
46 otherwise-unused features routed into the message), ALL, plus L1 (λ = .1) and
LEV (points-leverage family weights). 2026 held out as a confirmation slice.

Preceded by a Phase 0 that sized four levers without fitting anything, recorded
in `V5_PHASE0_FINDINGS.md`.

### What was established
**λ = .01 is an interior optimum**, from two independent runs. v4: λ = .0001
costs novel RMSE +0.03233 [+0.00912, +0.05554], 3/11. v5: λ = .1 costs +0.02636
[+0.00084, +0.05187], 1/10, with novel r² −0.00453 [−0.00886, −0.00019]. Both
directions established worse out of sample.

**V5_BASE reproduces v4's E0M_L2 to 3.8e-5 points/100**, so every v5 contrast is
one factor off a verified baseline rather than off a new implementation.

**The opponent asymmetry is real and Phase 0's measurement replicates.** Phase 0
put the v4 ancestor's paired residual loading on state-window schedule at +2.39;
V5_BASE lands at +2.34 from a fresh run and a different code path.

### What was killed
- **Every input intervention.** Every arm-minus-BASE MAE point estimate is
  positive on both slices. BASE has the best novel MAE, RMSE and r² of the eight.
- **Points-leverage family weighting** — established *worse* on novel lineups
  (MAE +0.05244 [+0.00327, +0.10161], 1/10). Pointing the objective at conversion
  did not move conversion. This closes a proposal made in three consecutive
  reviews, mine.
- **Opponent-deconfounded inputs as an accuracy lever.** The mechanism works —
  the loading collapses 36%, predictions move a mean 0.34 pts/100, the sign is
  right — and it buys nothing in points, exactly as Phase 0 sized it (0.0024
  RMSE). Correct and worthless are not contradictory.
- **Stacking.** ALL is the sum of its parts: interaction −0.00126 MAE, −0.00617
  RMSE. Four independent, independently mildly harmful changes.
- From Phase 0: the backlog's "free" over-dispersion shrink (unavailable, and its
  deployable form makes every arm worse), the FTA composition gap as a points
  lever (absorbed by calibration, t = 0.35), and the fixed opportunity budget
  (0.18% of offensive-rating variance — which also sizes ORB budget feedback).

### What it cost
384 arm-origins, 768 fits, ~3,080 s primary plus ~3,080 s secondary. 654 tests.
A concurrent-launch race killed one process; all completed work verified intact,
and a run lock plus atomic checkpoint writes closed the gap.

### Still open
- **Conversion has not moved in five consecutive versions.** Largest change
  across all seven v5 interventions: 5.0e-5 of FG Brier. §10's shot-quality
  effect remains the one established teammate mechanism the architecture cannot
  find.
- **Channels improve, points do not** — now reproduced on the input side. RICH
  and ALL genuinely improve raw counts, location and assisted-share loss and are
  *worse* in points.
- **The holdout was too small.** 428 cells cannot resolve 0.03 MAE; r² collapses
  to ~0.02 and the rankings scramble. Right discipline, wrong size.
- **The two unmet product standards are untouched and well powered**: fixture
  magnitudes are ~2× anything the model produces in range, and the support
  measure cannot separate five Gobert clones from a real five by more than 3%.

### Measurement traps earned
- **A baseline-scaled loss is not comparable across arms that change the
  baseline.** `event_loss` is scaled by each arm's own untrained model; OPP's
  adjusted base state changes that baseline, so OPP appears to have the best
  scaled event loss while being worse on raw location. Compare raw families.
- **An opponent adjustment fitted across players gets the sign backwards.** A man
  on a strong defence meets a league that excludes it, so his schedule-faced runs
  high for reasons unrelated to inflated statistics. Player fixed effects are
  load-bearing; pooled, the make-logit slopes come out negative.
- **A concurrent second launch is a silent data hazard**, not just wasted compute:
  both processes write the same `.tmp` paths and one `os.replace` consumes the
  other's file.

---

## v6 — 2026-09-11 — `joint_capability_2026_09_11_v6`

### What changed
Architecture frozen at v5's `E0M`; **the training population became the factor.**
Five arms × 48 origins: FULL, HOLD75 (trains only below the prefix p75 of
composition distance), RAND75 (a matched random 75%), HOLD50, RAND50. Preceded
by a no-fit Phase 0 that rebuilt the support measure as Mahalanobis on an
identity-free 31-dim composition vector and measured the clone ladder
(`V6_PHASE0_FINDINGS.md`).

The question: does this model price a composition region it has never seen, or
interpolate from neighbours? It matters because `selection_on_the_outcome.md` —
why the tool's coverage gate is asserted rather than fitted — was established
against models carrying lineup, pair or identity parameters. `E0M` has none.

### What was established
**Withholding the unusual quartile is free.** `HOLD75` has the best
withheld-region MAE of the five arms (8.3164) — better than the model trained on
everything (8.3342) — and is within 0.001 MAE of FULL on all cells while
training on a quarter less data. `HOLD75 − RAND75` in the withheld region is
**−0.0050 ± 0.0288**, 5/11.

**The clone response is invariant to the holdout.** Five-clone ratings correlate
**r = 0.9966** donor-by-donor between HOLD75 and FULL, with the 1→5 move,
its spread and its sign distribution all unchanged.

**No gradient with distance.** `HOLD75 − RAND75` by decile of cell composition
distance shows no trend. Interpolation from neighbours would grow a penalty as
cells move away from the training region; it does not.

Nothing is statistically established — every interval crosses zero — but six
point estimates, a clean dose–response and the clone correlation all agree.

### What was killed
- **The assumption that this architecture needs to have seen unusual lineups.**
  It does not, across the observed range.
- **My mid-run sanity check.** I claimed `HOLD − RAND` inside the support should
  be ≈ 0 if the control is fair. Wrong: HOLD75 trains *exclusively* inside the
  support, so it should be better there, and is (−0.0241). That is
  specialisation, not a broken control. The clean statistic is the
  difference-in-differences, which nets it out.

### What it cost
240 arm-origins, 480 fits, 7,070 s. 680 tests. Three attempts to get the random
control right, and two defects caught in the smoke rather than in the results.

### Still open
- **The range.** 99.5% of withheld cells sit at or below the clean real maximum
  composition distance of 10.31. The fixtures that matter are at **1.81×** (five
  copies of a p99 player) and 3.02×. v6 validates extrapolation *across* the
  observed range, not beyond it, and `composition_extrapolation.md` is explicit
  that a composition result without its range is not a result.
- **The one number leaning the other way.** The difference-in-differences is
  +0.0191 ± 0.0138 at 7/11 — a 1.4-sem hint that HOLD pays something out there
  net of its specialisation.
- `V6_SHOT` was built and smoked but not run; conversion remains unmoved.

### Measurement traps earned
- **A specialist control is not a broken control.** An arm trained only on a
  region will beat its partner in that region by construction; compare the
  difference of differences, not either region alone.
- **Matching a control on exposure alone can still hand it an advantage.**
  Matching possessions left the random arm 4% more *distinct* lineups — more
  composition diversity, pointing toward the expected conclusion. Stratify on
  the row-size distribution and assert both.
- **A launcher that writes its own lock file locks out the process it starts.**
  The `pgrep -f` self-match in a new costume, sixth occurrence in this repo.
- **A support measure calibrated against a contaminated tail understates the
  distance.** 9.5% of rows contain a zero-exposure player and carried the entire
  upper tail; the real maximum is 10.31, not 15.50.

## v7 — 2026-09-11 — `joint_capability_2026_09_11_v7`

Full record in `reports/joint_capability_v7_review.md` and `V7_PHASE0_FINDINGS.md`.
288/288 arm-origins, 48 origins, 12 seasons, 6,179 cells, 803,447 possessions.

### What changed

Architecture frozen at the v5/v6 backbone. The factor is **who is in the
training population**, pushed from v6's lineup-quantile axis to **donor
extremity** — a player's five-clone Mahalanobis distance on the v6 composition
measure, prefix-ranked and refit per origin.

| arm | one change |
|---|---|
| `V7_FULL` | none; the frozen backbone |
| `V7_HOLDX5` / `V7_RANDX5` | withhold the top 5% of donors (52 players, ~29% of rows) / a footprint-matched random 52 |
| `V7_HOLDX2` / `V7_RANDX2` | withhold the top 2% (21 players, ~13% of rows) / matched random 21 |
| `V7_LOAD` | §8.1 overload response, three non-negative coefficients, zero exactly attainable |

Two holdout pairs because volume and extremity move **oppositely** across them:
`HOLDX2` keeps more data and is more extreme per player removed.

### What was established

- **`k_make_over` fits non-zero in 48/48 origins** (mean 0.0709, range
  0.0402–0.1108) while `k_to_over` is **exactly zero in 47/48** and
  `k_make_under` in 42/48. Two of three coefficients found the boundary and one
  did not, under negligible weight decay. Overloading a player costs his
  *shooting* and not his *turnovers* — the first mechanism here fitted rather
  than asserted.
- **Removing the top 5% of donors is established harm**, and worst where those
  donors play: `HOLDX5 − FULL` is +0.0596 ± 0.0216 (2/12) on donor5 and
  +0.0889 ± 0.0355 (2/12) on donor2.
- **The epoch cap is not binding.** Raised 24 → 48 after v6; across 288
  arm-origins the median selected epoch is 12, the maximum 30, **none at the
  cap**. Adam's v6 observation is discharged; leave the cap alone.
- **The five-clone level is sane.** 1,068 clone lineups span 90.85–132.43
  pts/100 and the maximum is 106.6% of the model's own in-range prediction
  maximum. The neural model does not have the raw additive's 5-Shaq behaviour.

### What was killed

- **v6's "no composition-distance gradient."** Pushed past the observed range the
  gradient appears: mean |diff| against `V7_FULL` on the clone ladder rises
  0.434 → 0.457 → 0.454 → 0.757 → **1.643** across distance quartiles then the
  top 5% (`HOLDX5`, slope +0.0616/unit), and a model disagrees about donors it
  never saw by **3.2x** what it disagrees about donors it did. Correlation stayed
  at 0.9958 throughout — **correlation was the wrong statistic**, blind to
  exactly the level shift a tool that prints a number cares about. v6's finding
  was true of v6's holdout, not of the model.
- **This version's own partial result.** At 39 origins `HOLDX2 − FULL` read
  −0.0311 on donor5 and looked like "prices donors better having never seen
  them." At 48 it is −0.0139 ± 0.0218 and the difference-in-differences is
  +0.0011 ± 0.0178. **Dead.** What survives is a *uniform* `HOLDX2 − RANDX2`
  advantage of −0.0164 ± 0.0077 (7/12, ALL) that is the same size in every
  region — outlier trimming on a shared fit, not better extrapolation.
- **Assertion gates as run control.** `assert_matched` destroyed a 2-hour sweep
  at origin 39/48 over one pair-origin at 3.22% against a 3% threshold. Replaced
  by `match_quality`. Dropping the one flagged origin moves the headline from
  −0.0164 ± 0.0077 to −0.0164 ± 0.0076.
- **"The fixture magnitude is a defect."** Corrected same day. The five-clone
  context swing is 255% of the in-range maximum for `V7_FULL` against v3's 226%
  and v4's 192% — and three versions reported that magnitude without ever
  checking its SIGN. It is negative, and it is a composition penalty rather than
  score shrinkage: at MATCHED no-message score, clones in the far half by
  composition distance are pulled down 3.004 ± 0.432 pts/100 more than the near
  half, **negative in 8/8 origins spanning 2016–2026**, partial r on distance
  −0.447 in 8/8, while the control — mean swing on real lineups — is **+0.196**.
  The model learned a duplication penalty from data. See below.

### What it cost

288 arm-origins, 1,585 s of core compute after the resume, plus the aborted first
launch. Three Phase-0 audits (H0.1 hyperparameters, H0.2 the 5-Shaq check, H0.3
the one-sided overload test). `V7_SHOT` is built and smoked and **still unrun** —
seventh version, conversion still unmeasured by a dedicated arm. Tracking data
deferred again.

### Still open

1. **The message penalty's units** (`BACKLOG` §0ag Part A). λ_network penalises
   the message in raw coordinate units, so one sd of effect costs `sd_j²` — a 93x
   spread — and the fit follows the price list: make logits achieve 0.440 sd of
   message, location logits 0.125, backwards against §8g–8h. Two nested arms.
2. **Recency** (`BACKLOG` §0ag Part B). The neural arm decays training rows at a
   730-day half-life and the additive does not decay at all, so the two have
   never been on equal footing on time. 730 is a pinned default no run has walked
   off. `FLAT` / 365 / 180 against 730 settles both at once.
3. **Uncertainty, now with evidence.** The distance gradient above is a measured
   quantity with dynamic range, which is what `distance_shrink.py` could not fit
   and what the coverage gate asserts. Carried since v5; now the item with the
   best support.
4. **Conversion.** The §10 route is closed harm; the role route (`k_make_over`,
   48/48) is open and worth ~0 in points. v8 P0.3 asks whether `V7_SHOT` lost
   by double-counting what the message already derives.

### Measurement traps earned

- **A level-blind statistic will call an extrapolation failure a success.**
  v6 read r = 0.9966 and concluded no gradient; v7 finds a 3.2x level shift at
  r = 0.9958. Report mean |difference| in the units the product prints, beside
  any correlation.
- **Read a dose curve before naming a mechanism.** `HOLDX2` helping and `HOLDX5`
  hurting is one coherent curve; either alone invites the wrong story.
- **Check whether a benefit is uniform or localised before claiming the
  localisation.** The difference-in-differences is what separated "prices donors
  better" from "is a better model everywhere," and only the second survived.
- **A quality threshold is not a run gate.** Measure it, record the sign, and
  report the contrast with and without.

## v8 — 2026-09-12 — `joint_capability_2026_09_11_v8`

Full record in `reports/joint_capability_v8_review.md` and `V8_PHASE0_FINDINGS.md`.
336/336 arm-origins, 48 origins, 12 seasons, 9,828 s, zero errors.

### What changed

Architecture frozen at the v5 backbone for the fourth version. The factor is the
**objective's conditioning**, and — following Adam's steer that only model
improvement matters at this stage — the **measurement** was rebuilt first.

| arm | one change |
|---|---|
| `V8_BASE` | none; bit-identical to `V7_FULL` |
| `V8_TRIM2` / `V8_TRIM5` | training rows down-weighted by donor extremity, footprints matched to v7's `HOLDX2`/`HOLDX5` (13.20% / 28.60% of weight) |
| `V8_SCALE` | message penalty weighted per coordinate by `1/sd_j²`, weights normalised to mean one |
| `V8_STD` | message INPUTS standardised; skip path, decoder, budget and point identity untouched |
| `V8_HL365` / `V8_FLAT` | training-row half-life 365 / none |

**The measurement change.** v7 normalised each event family by the untrained
model on **that arm's own** training rows, so any arm that reweights moved its own
denominator — at 2024q3 the artifact was 3.5x the effect and `HOLDX2 − FULL` read
a spurious 21.4 sem. v8 computes one baseline per origin for every arm; verified
identical to **0.00e+00** across all 336 arm-origins.

### What was established

- **Standardising the message inputs improves the training objective, and it is
  the most consistent result this workstream has produced.** `V8_STD`:
  event loss **−4.12e-04 ± 4e-05**, negative in **47 of 48 origins** and **12 of
  12 seasons**, with every family moving the same way — location −7.35e-04,
  counts −2.06e-04, conversion −1.39e-04, all 12/12. The 18 coordinates had means
  from −3.663 to +1.307 and a 9.7x sd range and went into `Linear(36, 32)` raw.
- **Conversion moved.** Seven versions of "conversion has not moved", and
  `V7_SHOT` made it worse. It moves in 12/12 seasons here, because the network
  could finally read its inputs.
- **`lambda_network`'s units were mis-set, and correcting them is free.**
  `V8_SCALE` moved the budget exactly as §0ag predicted — location 0.1052 →
  0.1251, make 0.4809 → 0.4046 — and the families follow: location −6.13e-05
  (10/12), conversion +3.40e-05 (0/12), net +1.21e-05 (ns). Diagnosis confirmed,
  fix worth nothing.
- **Shortening the training-row half-life is harm.** 365 costs +1.064e-04 on
  event loss (1/12). The pinned 730 survives its first audit.
- **The additive/neural time asymmetry was costing nothing.** `V8_FLAT` adopts
  the additive's own no-decay convention and is worse in points (+0.0143 ±
  0.0207) and a wash on events.

### What was killed

- **v7's `HOLDX2` lead.** −0.0164 ± 0.0077 at 7/12 was the one v7 contrast that
  cleared two sem. With footprints matched by construction, the continuous trim
  is **worse than base on both readouts** (`TRIM2` event +8.17e-05 at 1/12,
  points +0.0117 ± 0.0082). Either the mechanism was hard removal specifically —
  not a shippable model, since a tool must price Gobert and Capela — or it was
  the coin flip it looked like. With a dead difference-in-differences, the second
  reading is now the likelier one. **Do not re-open the extremity-trim route.**
- **The idea that the message penalty's mis-pricing was costing accuracy.** It
  was real and it was free.
- **`V8_STD` as a points lever.** +0.0125 ± 0.0233 at 5/12, with RMSE and r²
  indistinguishable from base. The largest objective gain on record converts to
  nothing.

### What it cost

336 arm-origins, 9,828 s, one launch, no resume. Phase 0 ran and was parked after
Adam's steer: `V8_PHASE0_FINDINGS.md` records a measured null for the ensemble
interval and a product-side comparison of the two duplication rules that is not
being pursued. Three parameterisations of the trim, the first two caught by
sizing before any fit.

### Still open

1. **Answered inside v8, and it is the benign answer.** The six-arm inverse
   ranking (Spearman −0.886) does not survive a powered test: pooling all 288
   (arm, origin) paired deltas, the MAE gain regressed on the event gain has
   **slope −3.68 ± 21.39, r = −0.0102**, and `V8_STD` alone reads r = +0.038 over
   48 origins. **Resolution, not misalignment** — the benchmark cannot see gains
   this size, which is `BACKLOG` §0's standing calibration. So v9 must NOT change
   the objective; its choice is between accepting event-level improvement as the
   deliverable and finding a point evaluation with more power.
2. **Tracking** — `BACKLOG` §0ai, deferred by decision. Refit the pair block on
   the tracking era first.
3. The distance-aware interval is a measured null on this population
   (`V8_PHASE0_FINDINGS.md` P0.1) and the question is only answerable out of
   support, where no forward error exists to fit against.

### Measurement traps earned

- **A normalised loss is only comparable if the normaliser is shared.** v7's
  per-arm baseline moved 1.7–3.0% while the effects were 0.1%, and it read
  21.4 sem out of nothing. `feedback_matched_flags` in a new costume: check what
  the denominator is made of before comparing two arms on a ratio.
- **Size a reweighting before running it.** The trim's first parameterisation
  removed 34.5% of the training weight at a p90/p10 discrimination of 1.61x — a
  uniform down-weight, which a weight-normalised objective ignores. The second
  was 10x too weak. Both were visible from the weight distribution alone.
- **A max-over-five statistic does not live where its per-player quantile
  says.** Row extremity sits at p10 = 12.3 / p90 = 23.3 while the player-level
  p98 is 22.29; setting a row threshold from a player quantile is a category
  error.
- **Six arms ranked against each other is not a test.** The cross-arm event/MAE
  Spearman of −0.886 looked like a structural finding and evaporated at n = 288
  paired deltas (r = −0.0102). `feedback_fold_count` and `feedback_screener_calibration`
  restated: rank on the population with power, never on the handful of arms you
  happen to have run.

## v9 — 2026-09-12 — `joint_capability_2026_09_12_v9`

Full record in `reports/joint_capability_v9_review.md` and `V9_PHASE0_FINDINGS.md`.
288/288 arm-origins, 48 origins, 12 seasons, 9,145 s, zero errors.

### What changed

The **architecture**, for the first time along axes that were never varied. v2–v8
searched encoder on/off, message on/off, pooling ∈ {mean, pair, fixed}, width and
λ. The aggregation moment, the depth, the decoder's structure and the sender
weighting were untouched.

`V9_BASE` adopts v8's `V8_STD` and reproduces it bit-identically. Every arm
reproduces `V9_BASE` to **0.000e+00 at initialisation** — new blocks enter through
separately-constructed zero-initialised parameters while the shared blocks are
drawn in the same order from the same seed — so an arm starts *at* the base and a
null means the data declined the block.

| arm | change | params |
|---|---|---|
| `V9_SPREAD` | sender = [mean, **leave-one-out sd**] | 2,390 |
| `V9_MINMAX` | sender = [mean, min, max] | 2,966 |
| `V9_DEPTH` | two message rounds | 3,592 |
| `V9_DECODER` | rank-3 additive correction to the diagonal | 1,922 |
| `V9_ALL` | SPREAD + DEPTH + DECODER | 4,276 |

### What was established

- **Teammate VARIETY matters, and the model was blind to it.** `V9_SPREAD`:
  event loss **−2.46e-04 ± 2e-05, 12/12 seasons, 45/48 origins**, with location
  −2.56e-04 (11/12) and counts −1.68e-04 (12/12). Conversion does not move
  (7/12, ns), which is coherent — variety changes where and how often you shoot,
  not how well.
- **It compounds with v8.** `V9_SPREAD − V8_BASE` = **−6.58e-04 ± 3e-05, 12/12**.
  Two representational fixes for 576 extra parameters, and the most consistent
  improvement in eight versions.
- **Phase 0 predicted it before any fit**: teammate sd is 98.1% orthogonal to
  teammate mean (median over 18 coordinates, 17 of 18 above 80%).
- **It is the second moment, not capacity.** `V9_MINMAX` reaches −2.35e-04 (11/12)
  while its block grows *larger* (0.443 vs 0.352 of the base first-layer norm) —
  so sd is the more efficient encoding of the same idea.
- **A second message round is HARM**: +4.05e-05 ± 2e-05, 3/12, worse on every
  family, better in only 17/48 origins — and the block grew to **45% of round
  one**. The data used it and it generalised worse. One round is the right depth,
  now measured.
- **The diagonal decoder is not costing anything.** `V9_DECODER` is null
  (−1.76e-05, 8/12) with `U` at 4.7% of the slope. Its interpretability is safe.
- **`V9_ALL` is roughly additive** — predicted −2.23e-04 from the parts, observed
  −2.57e-04. The factors barely interact and `V9_SPREAD` carries the version.

### What was killed

- **My claim that the architecture was a dead end.** It was based on three
  capacity axes (width, encoder, pair pooling) and generalised to "the
  architecture". Adam pushed back, and the single best-supported change in the
  workstream came out of the axis I had not tested. **"We tried X, Y, Z and they
  failed" is not "that class of change fails."**
- **`V9_USAGE`, in Phase 0**: within-lineup usage sd is 0.050 around a mechanical
  mean of 0.197, so a usage-weighted sender sits 0.026–0.255 coordinate sds from
  the uniform mean against the sd sender's 3.805. "Which teammate is loudest" is
  not answerable from usage share here.
- **Depth as a route.** Established harm; do not revisit two-round message passing
  on this data.
- **The hope that objective gains would eventually show in points.** −6.6e-04 at
  12/12 seasons converts to `V9_ALL − V8_BASE` = **−0.0008 ± 0.0254**. v8 said the
  benchmark cannot resolve gains this size; v9 tested that with an effect 1.6x
  larger and the answer held.

### What it cost

288 arm-origins, 9,145 s, one launch. Phase 0 was minutes, killed one arm and
retracted one claim from the plan.

### Still open

1. **A point evaluation with power** is now the binding constraint on everything.
   Two versions have produced real, unanimous objective improvement and the
   benchmark has moved 0.0008. An ~84-possession cell is mostly finite-batch
   noise; more cells, a lower-variance target, or a paired design that removes it.
   Until this exists, no architecture or objective work can be graded.
2. **Tracking** — `BACKLOG` §0ai, still deferred; refit the pair block on the
   tracking era first.
3. Is there a **third moment**, or a better set summary than mean+sd? v9 shows the
   second moment pays and min/max pays about the same; nobody has looked further.

### Measurement traps earned

- **Check whether the block GREW before reading a null.** `V9_DEPTH`'s round two
  reached 45% of round one and still hurt; `V9_DECODER`'s `U` reached 4.7% and did
  nothing. Those are different findings and the growth log is what separates them.
- **Exact nesting at initialisation is worth the engineering.** Every arm at
  0.000e+00 from base means a flat contrast is about the data, not the seed.
- **A test that guards what you want to be true deserves a second look.** The
  "a live block changes the prediction" assertion passed vacuously — the message
  head is zero-initialised, so nothing upstream can move the prediction at init,
  and it would have kept passing had the block never been wired in.

## v10 — 2026-09-13 — `joint_capability_2026_09_12_v10`

Full record in `reports/joint_capability_v10_review.md`. 96/96 new arm-origins,
192 fits, 48 origins, 2,572.4 s, zero errors or epoch-cap hits.

### What changed

Day4 did three bounded things. It exactly decomposed the old event-to-points
transfer, evaluated fixed-half and prior-only GLOBAL additive/`V9_SPREAD`
blends, and trained two exactly nested `V9_SPREAD` trajectories with a normalized
team-point auxiliary loss: `TEAM_01` at alpha .1 and `TEAM_1` at alpha 1. The
five event families, architecture, row weights and outer protocol stayed fixed.

### What was established

- **Blending helps.** Fixed half scores 8.07274 MAE / 10.80812 RMSE / .12576
  raw r2 versus additive 8.09195 / 10.84099 / .12043 and BASE 8.14017 /
  10.86667 / .11626. Novel MAE improves to 8.83865. GLOBAL is effectively tied,
  so fitting the weight earns nothing material.
- **The event gains are not being destroyed by one bad channel.** In the exact
  `V9_SPREAD - V8_BASE` accounting, volume, location and conversion each help
  squared loss; calibration and component cancellation return much of the gain.
- **The team objective can move its target, but barely.** Alpha 1 reduces native
  team MSE 0.547 from a 2025.088 baseline (0.027%). That is a successful wiring
  test and not a useful new target.
- The basketball signs survive: limited centers remain below a real lineup,
  duplication remains penalized, and the contextual correction favors Korver
  beside Jokic relative to additive even though total rankings are not forced.

### What was killed

- **Direct team-point supervision as the next backbone.** `TEAM_1` reaches
  8.11221 MAE but trails additive; its mean season improvement over BASE is
  -0.02619 with 95% CI [-0.07605,+0.02367]. It worsens outer event loss in 11/11
  seasons and attenuates contextual behavior. `TEAM_01` is worse. Do not tune
  another alpha grid on this formulation.
- **More tiny cells as free statistical power.** The expanded population grows
  to 220,381 cells, but 190,937 have 1–19 possessions and are dominated by
  finite-batch noise. Regrouping the same outcomes does not create independent
  seasons.
- **The old v9 no-message helper.** It left round two active and can differ from
  corrected replay by 3.45 pts/100. This invalidates that ablation only, not the
  historical ordinary predictions. Rank-positive FT isolation also fails as
  diagnosed; the rank-zero backbone remains clean.

### What it cost

96 new arm-origins / 192 fits in 42m52s. Saved-control analyses and reports ran
automatically afterward. The expensive 2,000-game-cluster bootstrap was recorded
as not run; no IID possession substitute was used.

### Still open

1. **Separate individual value from context.** The blend is the version's real
   clue. Test a prior-only cross-fitted shrunk mean arm plus a zero-centred
   `V9_SPREAD` context residual, without player-pair effects.
2. **Latent-mean OOD uncertainty.** Observed finite-outcome intervals are near
   nominal, but no arbitrary-lineup mean coverage statement is justified.
3. Tracking, actual-opponent interaction, adaptive role states, and physical
   rebound/defense mechanisms remain distinct future workstreams.

### Measurement traps earned

- **Improving the supervised target is not sufficient.** Report the scale of the
  gain and what was traded away. Here 0.027% native MSE cost event fidelity in
  every season.
- **Post-hoc best is a lead, not a winner.** Half additive/`TEAM_1` reaches the
  best pooled MAE on this population (8.05677), but its season CI crosses zero
  and it gives back some novel-lineup performance. Preserve it as evidence for
  factor separation, not promotion.
- **A blend can diagnose missing representation.** Two highly correlated models
  can still split individual-value and context errors. The useful response is to
  identify those sources explicitly, not to add unconstrained capacity.

### Independent continuation qualifications, 2026-09-13

See `reports/joint_capability_v10_codex_review.md`. The fixed blend's RMSE
advantage over additive has nominal season-paired 95% intervals below zero,
overall and on novel fives; overall MAE remains uncertain. The source Shapley
results are valid, but the first prose table mislabeled its control and is now
corrected. The native team-MSE percentage uses a noise-dominated denominator
and does not measure learnable signal. A smaller context increment is not
intrinsically less coherent; five-Gobert final offense remains too respectable
despite its negative message adjustment. The message-on/off Korver-Westbrook
contrast is distinct from the NN-minus-additive contrast. No-message retains
budget interactions, so the proposed value/context separation requires a prior
reference projection. These findings support a next experiment, not a closed
class of models or causal identification of the blend's complementary errors.
