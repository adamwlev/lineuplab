# Review of joint capability v3

Prepared by Claude Opus 5 on 2026-09-09 at Adam's request, for Sol, Codex and Astra.
Follows `CLAUDE_MODEL_FEEDBACK_2.md` (review of v2).

**Status: read-only review of saved artifacts. No fit was launched, no file in
`experiments/cache/joint_capability_2026_09_09_v3/` was touched, and no code was
changed.** Derived quantities below (season-paired contrasts, dispersion slopes,
fixture-vs-range comparisons) were recomputed from the saved per-origin cells;
the arithmetic is stated so it can be reproduced. Provenance table at the end.

---

## 0. Summary

v3 is a large, honest improvement. Every structural defect I raised against v2
was fixed, the placebo suite that did not exist now exists and is clean, and the
run is complete, budgeted and reproducible. The headline claim — that real
teammate identity carries information — now has genuine support.

Four things I would change in how the result is read:

1. **The best arm is H2, not H3.** H3−H2 is a clean zero on every metric
   (RMSE −0.006 ± 0.046, 6/11) while H2 has 1,814 parameters against H3's 4,488,
   sits at matched λ with its own control, has better bias on all four count
   channels, and has the higher novel r². The learned own-state encoder is dead
   weight. H2 was omitted from the fixture panel, which is the one thing
   standing between that observation and a decision.
2. **The remaining control gap is "mean teammate quality" versus "who
   specifically."** Neither H3F nor the shuffle separates them, and on this
   project's own record the mean is the likely explanation. That is the next
   experiment, and it is cheaper than the opponent diagnostic.
3. **The fixture magnitudes are extrapolation, not measurement.** Five Goberts
   moves −21.3 points/100 and five limited centers −18.1, against a maximum
   |H3−H1| of **9.44** across all 5,607 real lineup-quarters. The signs and the
   ordering are a real achievement; the levels are unevidenced.
4. **The uncertainty section is under-sold and mis-diagnosed.** The
   composition-distance intervals are narrower at every level *and* closer to
   nominal on possession-weighted coverage. The real defect is that the support
   measure has almost no dynamic range — five Goberts scores 3.19 against a real
   maximum of 3.11 — and that the role-stress gate at >2 never fires on any cell,
   real or synthetic.

The conversion channel still does not move (F5 from the v2 review, unchanged).

---

## 1. What v3 fixed

Credit where it is due — this is a thorough response, and several fixes go
beyond what I flagged.

| v2 finding | v3 status |
|---|---|
| F1 shared decoder penalty tied to the per-arm λ, control froze at epoch 1 | **Fixed.** `gamma_decoder` 0.01 common to all arms; network λ selected separately. H0 now trains (dev traces show epoch 11–21 selections). |
| F3 the protocol's 730-day training weight was never implemented | **Fixed.** Now weights every family, its baseline scale, standardization and output penalties; outer evaluation left unweighted, correctly. |
| F4 ~250–400 optimizer steps, stopping bar 6% of available signal | **Mostly fixed.** max_epochs 12→24, patience 2→3, min improvement 1e-4→1e-5. Selected epochs now run to 24. |
| F4c message MLP reads unstandardized state | **Not addressed** — see G7. |
| F5 conversion barely moves; `assisted` takes a fifth of the gradient and cannot score | **Not addressed** — see G3. |
| F6 no diagnostics module, no placebo, 10 of ~20 required tests | **Fixed.** Shuffle, FT, seed, fixtures, failure review, intervals all present; 631 tests pass. |
| v2 origin states selected by who appears in the future window | **Fixed.** Origin exports now cover every player with pre-cutoff history plus a generic fallback. |

Also fixed without prompting: global numerator/exposure accumulation so
validation is batching-invariant; masks that preserve unknown actors and
locations instead of zeroing them; pooled moment-EB 2P/3P conversion
initialization; inner training on its own five-year prefix; and an early-stop
that distinguishes the best finite checkpoint from the patience reference.

**H3F is the right control and is well built.** `M(h_i, reference)` with a fixed
training-prefix sender, same parameter count as H3. Because `M` is nonlinear,
`mean_j M(h_i,h_j) ≠ M(h_i, mean_j h_j)`, so H3−H3F correctly isolates teammate
*dispersion* as well as level. It is a better control than the H3−H1 contrast it
replaced.

---

## 2. Findings

### G1 — H3 vs H3F is at mismatched λ, but the effect survives a matched contrast

`selection.json`: network λ is H1 .01, H2 .01, **H3 .0001 (`boundary: true`)**,
H3F .01. The v2 defect has flipped sides: the candidate now has 100× *less*
network penalty than its same-capacity control.

The mechanism is the grid-extension rule doing exactly what it says. From
`development/grid.csv` (mean over dev origins):

    λ_network        0.0001     0.0010     0.0100     0.1000
    H1                  —    .99850220  .99851020  .99865328
    H2                  —    .99809528  .99806485  .99829045
    H3            .99721689  .99722998  .99728428  .99782857
    H3F                 —    .99845869  .99843861  .99859800

H3's best landed at the 0.001 edge, so it earned the one permitted downward
extension; H3F's best was 0.01, interior, so it did not. **The candidate got a
search the control did not**, and ended on the extended boundary. H3's margin at
0.0001 over 0.001 is 1.3e-5, barely above the 1e-5 tie tolerance.

**But the effect is not an artifact of this.** The matched-λ architecture pair —
H2 (.01) versus H3F (.01) — reproduces the effect size almost exactly:

| contrast | λ | RMSE | seasons | r² |
|---|---|---:|---:|---:|
| H3 − H3F | .0001 vs .01 | **−0.05232 ± 0.02033** | 9/11 | +0.00936 ± 0.00361 |
| H2 − H3F | .01 vs .01 | −0.04648 ± 0.04648 | 7/11 | +0.00835 ± 0.00811 |
| H2 − H1 | .01 vs .01 | −0.04288 ± 0.04571 | 7/11 | +0.00771 ± 0.00796 |

The point estimates agree to within 12%. What the mismatch buys is *precision*,
not effect size: H3 and H3F are the same architecture from the same seed, so
their seasonal errors are tightly paired and the SEM is 2.3× smaller. So the
honest statement is that **the magnitude replicates at matched λ; the interval
that excludes zero does not.** Sol's disclosure is appropriate but the
qualification deserves that sharper form.

### G2 — The encoder is dead weight; H2 is the better backbone

| contrast | RMSE | seasons | MAE | novel RMSE |
|---|---:|---:|---:|---:|
| H3 − H2 | −0.00584 ± 0.04596 | 6/11 | −0.00334 ± 0.04712 | **+0.00417 ± 0.06376** |
| H2 − H0 | −0.06816 ± 0.03274 | 9/11 | −0.05053 ± 0.03394 | −0.09472 ± 0.03264 |
| H3 − H0 | −0.07399 ± 0.03364 | 8/11 | −0.05386 ± 0.03193 | −0.09055 ± 0.07283 |

H2 captures essentially the entire gain. It also has:

- **2.5× fewer parameters** — 1,814 against 4,488, and no encoder at all;
- **matched λ (.01) with H3F**, so its control contrast needs no qualification;
- **the higher novel r²** — .10591 against H3's .10582;
- **better bias on every count channel** (`reports/outer_event_metrics.csv`):
  FGA −0.070 vs −0.355, FTA +0.109 vs +0.240, TO −0.037 vs +0.198, 3PA −0.164
  vs −0.218;
- **the best FT Brier** (.080510, identical to H0) — every arm carrying the
  encoder is worse on free throws, which have no message path. Small, but it is
  the encoder adding noise rather than signal, in the one channel where it can
  only add noise.

The clean way to see it: anything that is a function of own state alone lands at
~8.159 MAE (H1 8.1586, H3F 8.1604), and anything that reads real teammates lands
at ~8.123 (H2 8.1228, H3 8.1229). The dichotomy is sharp and the encoder is on
the wrong side of it.

**The blocker:** `diagnostics/basketball_panel.csv` contains only H1, H3 and H3F.
H2's basketball coherence is untested, so if H3's encoder earns its keep it can
only be on the fixtures. That is a one-command gap.

### G3 — Conversion still does not move (v2 F5, unchanged)

From `reports/outer_event_metrics.csv`, FG Brier across all five arms:

    H0 .1704955   H1 .1701721   H2 .1701693   H3 .1701158   H3F .1701708

The **entire spread across every arm is 0.22%**, and H3−H3F is 0.000055, i.e.
**0.03%** — confirmed by Sol's own family table: conversion −.00012 at 33/44
quarters, the only family below 40/44 and the only one near coin-flip. Location
(44/44), assisted share (44/44) and allocation all move; conversion does not.

This matters for the same reason as in v2. §10/§10b established that teammate
influence on conversion is real and forecasts — Jokić +1.69 ± 0.36 pp on the
same shooters from the same distance after shooter and game fixed effects,
forward slope 1.082 ± 0.084 in 12/12 seasons over 2.66M held-out attempts, ~0.9
pts/100 of lineup spread, free-throw placebo +0.38. **The one teammate effect
this project has independently established is still the one the message pass
does not find.** Reallocating who shoots is close to zero-sum in points, and the
location mix is partly cancelled by construction, so the flat conversion channel
is a sufficient explanation for why H3 improves events but not points against
the additive.

`assisted` also remains a fifth of the training objective while having no path
into `player_points` — check `forward()`: the point identity uses `fga`,
`location`, `make`, `fta`, `ft_make` only.

### G4 — The fixture magnitudes are outside anything the network ever produced

Native H3 − H1 across all 5,607 real 2016-2026 lineup-quarters:

    median |gap| 1.48   p90 3.80   p99 6.08   max 9.44   (sd 2.22)

Against that range:

| fixture | H1 | H3 | H3 − H1 | as % of the real maximum |
|---|---:|---:|---:|---:|
| five_goberts | 135.27 | 113.98 | **−21.29** | **226%** |
| limited_centers | 119.51 | 101.40 | **−18.11** | **192%** |
| small_guards | 117.75 | 127.44 | +9.69 | 103% |
| five_jokics | 126.35 | 132.37 | +6.02 | 64% |
| jokic_westbrook | 117.93 | 123.95 | +6.02 | 64% |
| clippers_2021q4 | 116.81 | 122.24 | +5.43 | 58% |
| jokic_korver | 122.45 | 125.40 | +2.94 | 31% |
| haliburton | 120.06 | 121.50 | +1.44 | 15% |
| highest_exposure_real_2026 | 119.30 | 119.33 | +0.04 | 0.4% |

The two headline coherence results are 1.9× and 2.3× beyond the largest context
correction the model produces anywhere in its fitting range. `composition_distance`
agrees the fixtures are outside support and `support_reasons` labels them — but
the report still quotes "H3 **101.40**" and "five Goberts **113.98**" as if the
level were a finding. `composition_extrapolation.md` is explicit: never state a
composition result without its range.

Two further caveats on the strongest fixture specifically: `limited_centers` has
`min_neff = 0.000000` and `max_staleness = 2454` days, so at least one of the
five players has **no prior history at all** and is running on the generic
fallback prior, and the fixture is 6.7 years stale.

To be clear about what *is* evidence here: five Jokić clones move **up** (+6.0)
while five Gobert clones move **down** (−21.3), from the same network, with no
position rule and no player-specific term. That is a genuine internal control
against "unusual composition is penalised," and it is the most encouraging
result in the run. The ordering is the finding. The number is not.

### G5 — "Exceptional lineups are shrunk too hard" is a selection artifact

`failure_pattern_summary.csv` records H3 mean absolute error 13.77 against the
additive's 8.92 on the ten worst H3-versus-additive cases, and the review reads
this as H3 over-shrinking exceptional lineups (2023q1 Golden State: actual
137.19, H3 114.64, additive 117.42).

Every arm does this, in the same amount. Top and bottom deciles of *actual*
across the primary cohort:

    bottom 10% of actual:  actual  91.44   H3 111.72   H2 112.10   additive 111.16
    top 10% of actual:     actual 139.09   H3 116.50   H2 116.78   additive 116.35

The additive is 0.15 points *below* H3 on the top decile. Selecting cells on a
noisy realized outcome produces this pattern mechanically at these exposures, and
the ten cases were selected on H3's squared-error loss, so the comparison is
conditioned on H3 being wrong.

Worse, the direction is backwards. Regression slope of actual on prediction
(1.0 = correctly dispersed) on the calibrated forecasts:

    H0 .861   H1 .877   H2 .888   H3 .882   H3F .881   additive .885

All arms are **over-dispersed by ~12%**, not shrunk. H3's *native* slope is
0.715 with native sd 5.403 — the most over-dispersed of the five arms, which is
what a boundary-selected λ of .0001 predicts (G1), and is consistent with H3's
novel r² regressing from v2's .10770 to .10582 while H2 at λ .01 improved from
.10260 to .10591.

The persistence check (19/20 same residual sign in both halves) is suggestive
but not clean: both halves lie inside the window the cases were selected on.
Selecting on the first half and testing on the second would settle it.

### G6 — The uncertainty result is under-sold, and the real defect is elsewhere

The review concludes "the new composition-distance intervals do not improve
calibration." `diagnostics/rolling_interval_identical_summary.csv` does not
support that. On the identical 5,607 H3 cells (distance from nominal in
brackets):

| nominal | exposure cell | composition cell | exposure poss-wtd | composition poss-wtd | width |
|---|---|---|---|---|---|
| 50% | .5176 [1.76] | .4963 [**0.37**] | .5741 [7.41] | .4884 [**1.16**] | 17.41 → **17.14** |
| 80% | .8022 [**0.22**] | .7967 [0.33] | .8404 [4.04] | .7896 [**1.04**] | 33.13 → **32.38** |
| 95% | .9527 [0.27] | .9506 [**0.06**] | .9641 [1.41] | .9488 [**0.12**] | 52.08 → **50.53** |

Composition is **narrower at every level**, closer to nominal on both weightings
at 50% and 95%, and closer possession-weighted at 80% (the one cell-weighted
loss is 0.11pp). Reporting the possession-weighted 80% move 84.04% → 78.96% as a
drop reads a move *toward* nominal as a degradation.

The genuine negative is the one the review states second: coverage does not
order by distance quartile (77.42% Q1 to 79.91% Q4). **The cause is that the
support measure has almost no dynamic range at the extremes.** Real cells span
composition distance 0.52 to 3.11 (p95 1.41); five Goberts scores 3.19 and five
Jokićs 3.23 — clone lineups sit **3% beyond the real maximum**. On the older
Mahalanobis scale (`composition_extrapolation.md`) real fives span 4–11.5 and
five Shaqs is 20.9, roughly 1.8× the real maximum. A distance that cannot
separate five copies of one player from a real NBA lineup cannot be expected to
order error or to widen an interval where it should.

The same defect appears in the role-stress gate: `max_role_stress > 2` fires on
**0 of 5,607 real cells**, the real maximum is 1.007, and even the five-limited-
centers fixture only reaches 1.010. The threshold cannot fire on anything, real
or synthetic. Reporting it as a zero-count slice is honest; leaving it at 2 makes
it decoration rather than a guardrail.

### G7 — Message inputs are still unstandardized

`contextual_state` feeds the encoder the z-scored `x` (standardization fitted on
training rows) but feeds `self.message` the raw `pair = cat([h_i, h_j])`, whose
coordinates run from log-rates near −2.5 through centered location logits near 0
to conversion logits near −0.5, into a default `nn.Linear` init. The encoder got
a conditioned problem and the message net did not. This is a defect, not a
design choice, and it is consistent with the message arms needing more epochs
than the encoder arms to reach their selection.

---

## 3. What is genuinely good

- **Real teammate information passes two independent controls.** H3 beats H3F on
  outer event loss in 44/44 primary quarters, and beats the date/role-bin
  context shuffle in 4/4 diagnostic origins (mean +.001738, larger than the
  H3−H3F mean of −.001546). Both controls hold parameter count fixed.
- **The FT negative control is a clean null.** Real-minus-fixed outer FT NLL is
  +4e-6 at 2016q1 and mixed 2/4 overall, mean −.00005. The mechanism restriction
  holds where basketball says it should.
- **Seed stability at the event level.** Max |Δ| .000321 in event loss across
  seeds 29/43 on four origins — and the review correctly notes the *decomposed
  point ledger* is not that stable (max 1.171 points/100), which is the right
  caution to attach to a mechanism story.
- **The clone dichotomy** (G4): five Jokićs up, five Goberts down, no position
  rule, no player-specific term. This is the 5-Shaq requirement being approached
  by mechanism rather than by assertion, and `selection_on_the_outcome.md` says
  every previously fitted structure extrapolated the *wrong* way. This one does
  not. That is the single most important qualitative result here.
- **The Korver/Westbrook falsification was kept.** The learned context increment
  favours Westbrook (+6.02) over Korver (+2.94) against both H1 and H3F, which
  contradicts the pre-registered qualitative expectation, and it was reported
  rather than tuned away. Both decomposition orderings are printed with the
  order-sensitivity shown and all path residuals exactly zero.
- **Operational discipline.** 240/240 arm-origins, 646/700 fits, 2.89 h against
  an 8 h bound, 631 tests, hashes for plan/protocol/selection, max scoring
  discrepancy 3.2e-5 points/100, and the `_x/_y` duplicate-column defect
  disclosed rather than quietly repaired.

---

## 4. Proposed improvements

Ordered by information per fit-hour. Items 1–3 are together about the cost of
one core re-run.

### P1 — The mean-teammate control (the one control still missing)

Add **H3M**: `c_i = M(h_i, mean_{j≠i} h_j)` — the message network reads the
*average* of the four actual teammates rather than each one.

Neither existing control separates the two hypotheses that matter:

- H3F supplies a **constant** reference, so H3−H3F says only "actual teammates
  beat no teammate information."
- The shuffle supplies a **random real four-tuple**, so H3−shuffle says "my
  actual teammates beat someone else's" — which a mean-quality effect also
  passes, since a random four-tuple has a different mean.

H3−H3M is the discriminator: it separates *mean teammate quality* from *who
specifically*. The distinction is the whole product argument. Mean teammate
quality is close to what the additive model already encodes, and this project's
record predicts that is most of it — `novel_lineup_vs_novel_pair.md` (chemistry
does not generalise to unseen pairs), `pair_effects_not_lowrank.md` (rank 256
needed, explains every embedding null), `the_ball_is_the_interaction.md` (usage
conflict is the only named mechanism with signal). If H3 ≈ H3M, the honest word
for what the message pass learned is "context," not "chemistry," and the write-up
and the eventual tool copy should both say so.

Run it at H3's λ on all 44 primary origins; it is one arm, ~10 minutes of fitting
at the measured rate.

### P2 — Close the λ mismatch

Either refit H3 at .001 (costs 1.3e-5 of development loss) or extend the grid
down to .0001 for H3F and H2 as well, and report H3−H3F at matched λ. The
extension rule as written gives the arm that wants less penalty an extra grid
point its control never sees; consider extending the grid for *all* arms whenever
*any* arm hits an edge. Given G1, expect the effect size to survive and the
interval to widen.

### P3 — Add H2 to the fixture panel and the failure review

`basketball_panel.csv` covers H1/H3/H3F only. If H2 reproduces the limited-centers
and clone results, the encoder is dead weight on coherence as well as on points
and the backbone should be H2 at 40% of the parameters. If it does not, that is
the first evidence the encoder does anything, and it belongs in the write-up.

### P4 — Fix the support measure before touching intervals again

The interval work is not failing because empirical support adjustment cannot
work; it is failing because `composition_distance` puts five Gobert clones 3%
beyond the real maximum. Rebuild it in units where degenerate lineups are
actually far — Mahalanobis in the profile space used by
`composition_extrapolation.md` is the obvious comparator, and it put five Shaqs
at 1.8× the real max. Then re-derive the role-stress threshold from the realized
distribution instead of pinning 2, which fires on nothing. Re-run the same
pre-registered isotonic-scale method afterwards; do not retrospectively tune it,
and do not conclude the method failed until it has been given a measure with
range.

### P5 — Point the capacity at the channel that pays

G3 is unchanged from v2 and is the best explanation for why H3 wins on events and
loses on points.

- Weight the five families by **points leverage** rather than equally. Leverage
  is derivable from the decoder and is prior-only, so this is not a points loss
  in training and does not violate §2.7.
- Ablate `assisted` from the objective (keep it as a reported diagnostic): a
  fifth of the gradient that cannot reach `player_points`.
- Feed the measured **shot-quality on/off coefficient** in as a teammate-context
  input. It is the one teammate effect established forward here, the
  refit-strictly-before-each-origin machinery exists in `shot_quality.py`, and
  the message pass currently recovers 0.03% of the conversion channel. If the
  network cannot find a 1.7pp effect from raw states, hand it the coordinate.

### P6 — Two cheap methodological repairs

- **Standardize the message inputs** with the same fitted mean/scale path the
  encoder uses (G7).
- **Test failure persistence on disjoint halves**: select the high-exposure cases
  on the first chronological half's residual and test the sign on the second.
  The current 19/20 uses both halves of the selection window.

### P7 — Select λ against the property that matters

Development selection minimises **in-support inner-validation event loss**.
Nothing in the criterion sees novel-lineup generalisation, which is this
architecture's main advantage and the northstar's binding constraint. H3's
boundary λ improved in-support fit and coincided with a novel r² regression from
v2 (.10770 → .10582) while H2 at λ .01 improved (.10260 → .10591). At minimum,
print the novel-slice metric for every candidate λ so the trade is visible; a
pre-registered novel-weighted tiebreak would be better.

### On Sol's recommended next decision

The prior-only opponent diagnostic is a reasonable next step and I would keep it
on the list — the failure review cannot separate offensive context from defences
faced, and the two-lineup product needs it eventually. But I would run **P1
before it**. The opponent diagnostic conditions a mechanism whose nature is still
undetermined; if H3 ≈ H3M, what is being conditioned is mean teammate quality,
and the interpretation of every downstream result changes. P1 is also perhaps a
tenth of the cost.

---

## 5. Provenance

| claim | source |
|---|---|
| pooled and novel metrics, per-arm | `reports/metrics.csv` |
| season-paired contrasts incl. H2−H3F, H3−H2 | recomputed from `origins/*/*/cells.csv.gz`, 2016+ |
| λ selection, boundary flag, grid response | `selection.json`, `development/grid.csv` |
| event-channel metrics, FG/FT Brier, count biases | `reports/outer_event_metrics.csv` |
| fixture natives and support labels | `diagnostics/basketball_panel.csv` |
| H3−H1 range over real cells | recomputed from `native` in `origins/*/{H1,H3}/cells.csv.gz` |
| dispersion slopes, actual deciles | recomputed from `prediction`/`native` vs `actual` |
| interval coverage and widths | `diagnostics/rolling_interval_identical_summary.csv` |
| support-measure ranges, role-stress counts | recomputed from `*_y` columns in H3 cells |
| shuffle, FT, seed controls | `diagnostics/controls/*.csv` |
| failure patterns | `diagnostics/failure_pattern_summary.csv` |
| run state, fits, budget | `completion_status.json`, `manifest.json` |
| test result | `logs/full_test_suite_final_20260909.log` (631 passed) |

No test suite was run for this review and nothing executable was changed.
