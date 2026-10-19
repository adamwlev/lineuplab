# Review of joint capability v4, and how the model works end to end

Prepared by Claude Opus 5 on 2026-09-10 at Adam's request, for Sol, Codex and Astra.
Follows `CLAUDE_MODEL_FEEDBACK_2.md` (v2) and `CLAUDE_MODEL_FEEDBACK_3.md` (v3).

**Status: read-only review of saved artifacts. No fit was launched, nothing in any
v4 prefix was touched, and no code was changed.** Derived quantities were
recomputed from the saved per-origin cells and diagnostics; provenance at the end.

Fitted source: `experiments/cache/joint_capability_2026_09_10_v4e/`.
Derived report: `experiments/cache/joint_capability_2026_09_10_v4e_report_r3/`.

---

# Part I — How the model works, soup to nuts

The recommended backbone is **E0M_L2**. The best all-lineup point arm is
**E1P_L2**. They differ in exactly two switches, described at the end. Everything
else below is shared.

## 1. Source data

Read-only from existing caches; no builder is allowed to touch Postgres.

- `context_*.pkl` — 6,059,380 possessions across 32,173 games, 2001-10-30 to
  2026-06-13, with the exact ten players on the floor and the point target.
- `shot_events2_*.pkl` — 6,846,563 shots and free throws with shooter and raw
  distance. 61,369 FGA and 6,965 FTA fail to match a shooter and are **masked,
  not zeroed**.
- `possession_channels_*.npz` — slot-attributed turnovers, rebounds, steals.
- `game_player_stats.pkl` — player-game box lines, including `own_shot_ast`,
  the only place assisted-made share exists.

These collapse to **897,778 rows, one per (game, offensive five)**, carrying
possessions, per-slot FGA/FTA/FTM/turnovers, and per-slot attempts and makes in
six shot-distance buckets: rim ≤3 ft, paint 3–9, mid 9–15, long two >15, corner
three ≤22, above-break three >22. The buckets are distance proxies, not x/y
locations — "corner three" means "a short three."

## 2. Player state, strictly dated

A day-by-day chronological pass produces **667,527 beginning-of-day player
states**. Each day: decay every accumulator, emit states for players appearing
that day, then apply that day's box lines at end of day. A game never sees its
own outcome, and same-day games all read the same state.

Two decay clocks, per the protocol: **180-day half-life** for role quantities
(usage, assists, shot mix) and **730-day** for shooting quantities. Every rate is
empirical-Bayes shrunk toward the contemporaneous league mean using moment
matching with effective exposure `(Σw)²/Σw²`, so a thin player is pulled to the
prior rather than excluded.

That yields an **18-coordinate anchored state** `b_i(t)`, all on unconstrained
scales so the decoder's links are valid by construction:

| coords | content | scale |
|---|---|---|
| 0–2 | FGA, FTA, turnovers per possession | log rate |
| 3–8 | six shot-location shares | centered logits |
| 9–14 | six location-conditional make rates | logits |
| 15 | free-throw make rate | logit |
| 16 | assist rate | log rate |
| 17 | assisted-made share | logit |

Alongside it, a **64-feature vector** `x_i(t)`: the 18 coordinates, their 18
`log1p(effective exposure)` values, 18 missingness flags, offensive-rebound rate,
four recent-role contrasts (180-day minus 730-day usage, 3PA share, turnover
rate, assist rate), four prior-teammate reference features (exposure-weighted
means of past teammates' usage, assist rate, three-point rate and assisted share),
and `log1p(days since last seen)`. Standardization is fitted on training rows only.

**There are no player-ID, pair, team or lineup parameters anywhere.** Identity
joins histories and names outputs; it is never a numeric feature. That is what
makes "same state ⇒ same treatment" true by construction rather than asserted.

## 3. Context: the receiver reads its teammates

Optionally a shared MLP corrects the own state — `h_i = b_i + E(x_i)`, where
`E` is 64 → 32 tanh → 18 with a zero-initialised output layer, so the arm starts
exactly at the anchored state. E0 arms skip this; `h_i = b_i`.

Then one directed message pass. `M` is a shared MLP, 36 → 32 tanh → 18, also
zero-initialised at the output. The three pooling modes are the whole factorial:

```
fixed  (F):  c_i = M(h_i, r)                     r = a constant prefix reference
mean   (M):  c_i = M(h_i, (Σ_j h_j − h_i)/4)     the leave-one-out teammate mean
pair   (P):  c_i = mean_{j≠i} M(h_i, h_j)        each teammate separately
```

`z_i = h_i + c_i`. Coordinate 15 of the message is **masked to zero**: teammates
are not permitted to change free-throw conversion. That is a deliberate
falsifiable restriction and it doubles as the standing negative control.

Permutation equivariance holds in all three modes, and five identical profiles
form a well-defined set because the exclusion is by *slot*, not by player id.

## 4. Decoder: a finite opportunity budget

`decoded = intercept + softplus(raw_slope) · z`, 18 intercepts and 18 positive
slopes — the only decoder parameters, shared by every arm.

The budget is the single piece of accounting that makes the five players
compete:

```
U        = prefix league mean of (FGA + 0.44·FTA + TO) per possession, 365-day
           half-life, strictly before the cutoff.  ≈ 1.12 usage units.
q_i,k    = exp(decoded[0:3])                       unnormalised propensities
Z        = Σ_i (q_i,FGA + 0.44·q_i,FTA + q_i,TO)
λ_i,k    = U · q_i,k / Z                           the five players share one U
```

`U` is identical across arms and does not depend on the lineup, so **no arm can
win by inventing possessions**. Everything else is a link function: softmax over
the six location logits (centered first, since a common shift is meaningless),
sigmoid on the six make logits, on FT make, on assisted share.

## 5. Points

```
points/100 = 100 · Σ_i [ Σ_b value_b · λ_i,FGA · p_i,b · make_i,b  +  λ_i,FTA · ft_i ]
```

with `value_b` = 2 for the four two-point buckets and 3 for the two three-point
buckets. That is the whole scorer. There is no league valuation table, no
shooting surplus, no assist-deficit term and no free residual — all of which
would double count. **`assisted` appears nowhere in this identity**; it is an
auxiliary head only.

Because `make` is per bucket rather than one scalar per player, moving an attempt
from a long two to the rim is worth `2·(make_rim − make_longmid)` and is *not*
cancelled — the §8j defect of the old structural arm is fixed by construction.

## 6. Training

Five loss families, each divided by its own eligible exposure and by its own
training-only baseline, then averaged equally:

1. **Counts** — composite Poisson NLL on FGA/FTA/TO with mean `n · λ_i,k`,
   zero-event players included.
2. **Location** — six-way multinomial cross-entropy on attributed attempts.
3. **Conversion** — binomial on makes/attempts per player and bucket.
4. **Free throws** — binomial on attributed FT attempts.
5. **Assisted share** — binomial at **player-game** level, aggregating predicted
   assisted makes over that player's actual lineup exposures; batches keep whole
   games so the aggregation is exact, and non-reconciling player-games are masked.

Numerators and exposures accumulate globally before division, so the objective is
batching-invariant. **No points loss** — points are an external check.

Optimisation: Adam, lr 1e-3, weight decay 1e-4, gradient clip 5, complete-game
batches targeting 4,096 grouped rows, float32 forward with float64
reconciliation, CPU, seed 17. Every training example carries a **730-day time
weight**, common to all five families and all arms. Penalties: `γ = 0.01` on the
decoder for every arm, and a separate network `λ` on the squared encoder and
message outputs, with the encoder penalty strengthened where exposure is thin
(`1 + 200/(200+n_eff)`).

## 7. The forward protocol

48 quarterly origins, 2015–2026; the four 2015 quarters are warmup and the
**44 primary** origins from 2016 are scored.

For each origin: take the most recent *completed* quarter as an inner validation
window, fit on the five years before it, pick an epoch by the same five-family
objective (max 24, patience 3, min improvement 1e-5), then **refit from the same
seed on all data before the origin cutoff for exactly that many epochs**. The
scored quarter never chooses a coefficient or an epoch.

Player states are frozen at the quarter start for both inner validation and outer
test, matching deployment. Predictions are aggregated to lineup-quarter cells and
joined one-to-one against the frozen benchmark cells, with possessions and actual
points verified to 1e-9.

A prior-only affine calibration is applied last: fit `actual − league = a + b·(P −
league)` with `b ≥ 0` on completed earlier windows, cold-starting at `a=0, b=1`
below 30 cells. Native and calibrated numbers are both saved.

Evaluation population: **5,607 cells / 726,364 possessions**, of which **2,073
cells / 226,256 possessions** are novel — five-man units never previously observed.

## 8. The two switches, and what they cost

| arm | encoder | pooling | parameters | what it is |
|---|---|---|---:|---|
| E0M_L2 | off | mean | **1,814** | recommended backbone |
| E1P_L2 | on | pair | 4,488 | best all-lineup point arm |
| E1M_L2 | on | mean | 4,488 | best novel RMSE and r² |
| E0F_L2 | off | fixed | 1,814 | the no-teammate-information control |

E0M_L2 is 36 decoder parameters plus a 1,778-parameter two-layer MLP that reads
(your state, your teammates' mean state) and returns an 18-coordinate adjustment.
That is the entire learned model. Everything else — the states, the budget, the
links, the point identity — is fixed accounting.

---

# Part II — Review

## 9. What v4 settles

This is the cleanest experiment in the workstream. A 3 × 2 × 2 factorial over
pooling, encoder and λ, nine arms × 48 origins, three of them exact frozen-v3
aliases with **function parity 0.0 across 97 rows each** and the v3 code hashes
verified. 640 tests pass. 600/640 declared optimizer starts, 2.90 hours. The
point-transfer ledger reconciles to 3.9e-14 and creates zero budget.

**Mean pooling is the result, and on novel lineups it is the strongest finding
this project has produced in this workstream.**

| contrast | slice | metric | mean ± sem | 95% interval | seasons |
|---|---|---|---:|---|---:|
| E0M − E0F | novel | RMSE | −0.12239 ± 0.02678 | [−0.18206, −0.06272] | **11/11** |
| E0M − E0F | novel | raw r² | +0.02013 ± 0.00434 | [+0.01046, +0.02980] | **11/11** |
| E1M − E1F | novel | RMSE | −0.10948 ± 0.03931 | [−0.19707, −0.02190] | 9/11 |
| E0M − E0F | all | RMSE | −0.05950 ± 0.02826 | [−0.12247, +0.00346] | 8/11 |
| E1M − E1F | all | RMSE | −0.05622 ± 0.02291 | [−0.10725, −0.00518] | 7/11 |

11/11 seasons with an interval excluding zero, on the slice the northstar says
matters most. For calibration: the opponent adjustment — the one lever in this
repo that unambiguously paid — was 9/11.

**Pair pooling adds nothing, and on novel lineups it subtracts.** This answers the
question I raised in `CLAUDE_MODEL_FEEDBACK_3.md` §P1 directly:

| contrast | all MAE | novel MAE | novel RMSE | novel r² |
|---|---:|---:|---:|---:|
| E0P − E0M | +0.00041 (8/11) | **+0.02364 (3/11)** | **+0.01709 (3/11)** | **−0.00291 (3/11)** |
| E1P − E1M | −0.01269 (9/11)* | +0.00051 (5/11) | +0.00397 (5/11) | −0.00058 (5/11) |

\* interval excludes zero.

So preserving each teammate separately buys a small in-distribution MAE gain with
the encoder on, and is *worse* out of distribution at 3/11 seasons without it.
An effect that appears in-support and reverses out of it is the signature of
overfitting, not chemistry. This is consistent with the whole record —
`novel_lineup_vs_novel_pair.md`, `pair_effects_not_lowrank.md`,
`pair_effects_unpredictable.md` — and it is a genuinely valuable negative: **the
right word for what this architecture learned is "context," not "chemistry."**
The write-up and any eventual tool copy should say so.

**The encoder is dead weight**, as I argued in v3 §G2. At matched pooling and λ,
every encoder contrast is null: E1M − E0M all RMSE −0.01233 (5/11), novel RMSE
−0.01848 (7/11), all MAE −0.00062 (6/11). E1F − E0F and E1P − E0P are likewise
null. 2,674 parameters for nothing measurable.

**λ = .0001 hurts out-of-distribution**, which confirms the mechanism I proposed
in v3 §G7/§P7 for why v3's H3 regressed on novel lineups:

    E1M_L4 − E1M_L2   novel RMSE  +0.03233  [+0.00912, +0.05554]  3/11
    E1P_L4 − E1P_L2   novel RMSE  +0.03578  [+0.00429, +0.06727]  2/11

Both intervals exclude zero. v3's headline arm sat at .0001, and that is exactly
what cost it the novel advantage v2's H3 had. Moving to the factorial design —
treating λ as a declared factor instead of selecting it per arm — also removes
the boundary-control problem I raised in v3 §G1 entirely. That is the right fix.

**My v3 §G6 complaint about the intervals has been properly answered, and the
answer goes against me.** v3 compared composition-isotonic against an
exposure-only baseline on coverage alone; v4 adds a matched `constant_sqrt_n`
control and a proper weighted interval score. On that footing, exposure-only is
clearly worst (weighted coverage .835 at nominal .80, score 38.5), and
composition-isotonic is a hair *worse* than the constant control for every arm
(E0M at 80%: 36.073 vs 36.006). Composition distance adds nothing over a constant
scaled by √n. Better comparator, better scoring rule, negative answer — conceded.

**My §P6 was implemented correctly.** `failure_first_half_selected_second_half.csv`
selects on the first chronological half and tests the second, and the pair-message
disadvantage does not persist. That is the right way to run that audit and it
changed the conclusion.

## 10. Findings and critiques

### C1 — The largest miscalibration in the model is not discussed anywhere

This is my main new finding, and it comes straight out of Sol's own
`reports/event_metrics.csv`, which reports every channel on two cohorts.

| cohort | actual FTA/100 | predicted (E0M) | bias | actual FGA/100 | predicted | bias |
|---|---:|---:|---:|---:|---:|---:|
| full eligible (2,760,546 poss) | 22.504 | 22.612 | **+0.107** | 88.581 | 88.467 | −0.113 |
| **common evaluation cells** (726,364 poss) | **20.321** | **23.232** | **+2.911** | **89.810** | **88.466** | **−1.344** |

The model is nearly unbiased on all eligible possessions and badly biased on the
cells the benchmark actually scores: **it over-predicts free-throw attempts by
2.9 per 100 and under-predicts field-goal attempts by 1.3 and three-point
attempts by 1.1.** Every arm shows it (FTA bias +2.74 to +3.60).

The cause is already documented in this repository. `ASOF_ACCOUNTING_AUDIT.md`:
"22.58 FTA/100 in all possessions versus 20.36 in matched evaluation cells (gap
positive 11/11)." `ASOF_DEPLOYMENT_AUDIT.md`: "Common fives overrepresent Q1/Q3
and have fewer FTs." `DISAGREEMENT_AUDIT.md`: "FTA bias is +4.87/100 (11/11
seasons positive), and 3PA is underpredicted." The evaluation cells are recurring
five-man units, which are deployed in systematically different game situations
than the average possession. The model is trained on all possessions, carries the
unconditional rate, and nothing in the architecture can adapt.

Why it matters:

- **Size.** 2.9 FTA/100 at ~77% is ≈ 2.2 points/100 over-predicted from the free
  throw channel, partly offset through the shared budget by 1.3 fewer FGA
  (≈ −1.4). The residual level is absorbed by the affine calibration, but the
  *composition* error is not — an affine map cannot move FTA down and FGA up. The
  arms are arguing over 0.03–0.06 MAE while carrying a composition error an order
  of magnitude larger.
- **It is a plausible part of the last gap to the additive.** E1P_L2 trails
  corrected additive by 0.018 MAE. The additive is fitted directly on cell-level
  rates and never inherits this.
- **It interacts with the headline result.** The single largest event-channel
  improvement from mean pooling is **FTA NLL, −0.09019** — three times the next
  channel — and on the evaluation cells mean pooling reduces the FTA bias from
  +3.59 to +2.77 (E1) and +3.26 to +2.91 (E0). Some of what the teammate-mean
  signal is buying may be *deployment*: which lineups play in which game
  situations, and therefore how many fouls they draw. That is real predictive
  signal, but it is not teammate influence in the basketball sense, and the
  context shuffle does not rule it out — shuffling four-tuples destroys deployment
  identity along with teammate identity, so a deployment-learning model passes
  that control too.

`ASOF_DEPLOYMENT_AUDIT.md` already showed that coarse clock/score-margin
bucketing cuts the descriptive FTA gap from 2.228 to 1.037/100. That machinery
exists.

### C2 — Conversion moves the score the most and is measured to move the least

The point-transfer ledger and the event metrics tell opposite stories about the
same channel.

Per-channel dispersion of the native point difference (possession-weighted over
48 origins, from `point_transfer_by_origin.csv`):

    E0M − E0F    opportunity  +0.029 (sd 0.686)   location +0.091 (sd 0.678)   conversion +0.112 (sd 0.858)
    E0P − E0M    opportunity  +0.043 (sd 0.072)   location −0.018 (sd 0.055)   conversion +0.058 (sd 0.085)

**Conversion carries the largest lineup-level dispersion of the three channels**
— ±0.86 points/100 for mean-versus-fixed. Meanwhile FG Brier across all nine arms
spans .232642 to .232805, a total range of **0.07%**, and mean-minus-fixed is
0.000076, i.e. **0.03%**.

So the channel that moves the score most is the one where the measured accuracy
gain is smallest. That is not proof the movement is noise — the Brier improvement
is real and consistently signed — but it means the point differences between arms
are dominated by a channel whose predictive improvement is marginal, which is
exactly the configuration in which a point benchmark at this resolution
(~0.04 MAE, per `feedback_significance_bar.md`) will not settle anything.

It is also the fourth consecutive version in which conversion barely moves, while
§10/§10b established that teammate influence on conversion is real and forecasts
(Jokić +1.69 ± 0.36 pp after shooter and game fixed effects, forward slope
1.082 ± 0.084, 12/12 seasons, 2.66M held-out attempts, ~0.9 pts/100 of lineup
spread, FT placebo +0.38). The architecture still does not find it.

### C3 — The fixture magnitudes are unchanged and still out of range

This is v3 §G4, re-measured on v4 and essentially identical.

Native E0M − E0F across all 5,607 real lineup-quarters:
median |Δ| 1.43, p90 3.41, p99 5.16, **max 7.82**.

| fixture | E0F | E0M | Δ | as % of the real maximum |
|---|---:|---:|---:|---:|
| five Goberts | 135.17 | 117.39 | **−17.79** | **228%** |
| five limited centers | 121.17 | 106.08 | **−15.09** | **193%** |
| five small guards | 118.18 | 129.82 | **+11.64** | **149%** |
| five Jokićs | 127.65 | 132.22 | +4.57 | 58% |
| Clippers 2021q4 | 117.41 | 120.93 | +3.52 | 45% |
| highest-exposure real 2026 | 118.07 | 116.88 | −1.19 | 15% |

The review says mean pooling "removes 10–12 points/100 from the fixed-context
center clones" as a feature. It is a feature that the *sign and ordering* are
right — Jokić clones up, Gobert clones down, no position rule, no player-specific
term, and `selection_on_the_outcome.md` says every previously fitted structure
extrapolated the wrong way. But the *magnitude* is twice anything the network
produces anywhere in its fitting range, and `composition_extrapolation.md` is
explicit: never state a composition result without its range.

Two specifics on the strongest fixture: `limited_centers` still has
`min_coordinate_neff = 0.000` — a player with no prior history at all, running on
the generic fallback — and 2,454 days of staleness.

### C4 — The support measure was not repaired, which caps the interval work

v3 §P4 unaddressed, and Sol says so plainly ("the support fields are inherited
from the fixed v3 baseline"). Real cells span composition distance 0.515–3.105;
five Goberts scores 3.191 and five Jokićs 3.231 — **3–4% beyond the real
maximum**. On the older Mahalanobis scale in `composition_extrapolation.md`, real
fives span 4–11.5 and five Shaqs sits at 20.9, roughly 1.8× the maximum.
`max_role_stress > 2` still fires on 0 of 5,607 real cells (max 1.100) and on no
fixture (max 0.765).

So "composition distance adds nothing over a constant" is a sound conclusion about
*this measure*, not about the idea. A distance that cannot separate five copies of
one player from a real NBA lineup by more than 3% has no room to widen an interval
where it should. The uncertainty pillar cannot advance until the measure does.

### C5 — Smaller points

- **No no-context baseline.** Every v4 arm carries the 1,778-parameter message
  network; E0F merely feeds it a constant, so it is still a nonlinear own-state
  transform. There is no v3-H0 equivalent in the v4 table, so the full ladder
  from raw anchored states is not visible in one place.
- **The grid was only explored downward.** λ ∈ {.01, .0001}, and mean pooling is a
  new architecture whose λ was never selected — .01 was chosen in v3 for
  fixed/pair arms. Given that .0001 demonstrably hurts novel lineups, the
  untested direction is *more* penalty. λ = .1 for E0M is one cheap arm.
- **Message inputs are still unstandardized** (v3 §G7). `contextual_state` feeds
  the encoder z-scored `x` and the message raw `h`, whose coordinates run from
  log-rates near −2.5 to centered logits near 0.
- **`assisted` is still a fifth of the gradient** and still has no path into
  `player_points`.
- The report's own `final_status.json` is admirably blunt:
  `defense_implemented: false`, `rebounding_loop_implemented: false`,
  `latent_ood_mean_validated: false`.

## 11. What is genuinely good

- **The factorial design itself.** Declaring λ as a factor rather than selecting
  it per arm removed the entire class of boundary-control problems that
  compromised v2 and v3, and it produced an interpretable 3×2×2 table instead of
  a ladder of confounded pairs. This is the right way to run this experiment.
- **Alias parity of exactly 0.0** across 97 rows per alias with v3 code hashes
  verified, plus two fresh bridge refits — so reusing three v3 fits costs nothing
  in comparability, and 1.5 hours of compute was saved honestly.
- **11/11 seasons on novel lineups** for mean-versus-fixed RMSE and r².
- **A clean, well-powered negative on pair pooling**, which closes the chemistry
  interpretation and saves the project from building on it.
- **The exact point-transfer ledger** — every comparison decomposed into
  opportunity, location and conversion, reconciling to 3.9e-14 with zero budget
  created, and both path orderings printed.
- **Failures reported as failures**: the report r1 OOM, the r2 all-NaN
  placeholder-precedence bug, the superseded v4/v4b/v4c/v4d prefixes all
  preserved and disclosed rather than cleaned up.
- **The Korver/Westbrook result flipped and was kept.** E1M now rates Korver
  +0.765 over Westbrook where the additive rates him −1.084, and v3's contrary
  *increment* finding is not hidden — with Korver's 2,001-day staleness stated.

---

# Part III — Proposed next steps

### P1 — Diagnose the FTA/deployment gap before any new architecture (highest value)

C1 is the largest quantified miscalibration in the model, it sits on exactly the
cells the benchmark scores, it is undiscussed, and it may be doing double duty as
part of the headline result. Three steps, all cheap:

1. Report event bias on the common cells alongside the full cohort in the
   standard table — it is already computed, just not surfaced.
2. Decompose the mean-pooling event gain by whether it survives within coarse
   clock × score-margin strata, reusing the bucketing from
   `ASOF_DEPLOYMENT_AUDIT.md` that cut the descriptive FTA gap from 2.228 to
   1.037/100. If the FTA component of the gain disappears inside strata, part of
   what "context" is learning is deployment.
3. Only then consider a deployment feature. Do not add one before the diagnostic.

### P2 — Make the conversion channel earn its dispersion

C2 says the score is being moved by the least-validated channel. Two options,
both previously proposed and neither yet tried:

- Weight the five families by **points leverage** rather than equally — derivable
  from the decoder, prior-only, not a points loss.
- Feed the measured **shot-quality on/off coefficient** in as a teammate-context
  input. It is the one teammate effect established forward here (12/12 seasons,
  slope 1.082), the strictly-prior refit machinery exists in `shot_quality.py`,
  and the network recovers 0.03% of it from raw states.

Also ablate `assisted` from the objective and keep it as a reported diagnostic.

### P3 — Two cheap arms that close open questions

- **E0M at λ = .1.** The grid has only been explored downward, and downward
  demonstrably hurts novel lineups. One arm, 48 origins.
- **A true no-context arm** (no message network at all) so the ladder from
  anchored states is visible in one table.

### P4 — Rebuild the support measure, then redo the interval work

C4. Put composition distance on a scale where clone lineups are genuinely far —
the Mahalanobis profile space of `composition_extrapolation.md` is the natural
comparator — and re-derive the role-stress threshold from the realized
distribution instead of pinning 2. Then re-run the same pre-registered isotonic
method. Do not retrospectively tune it, and do not record "composition distance
does not help" as settled until it has been given a measure with range.

### P5 — On the recommended opponent experiment

I now agree with Sol's recommendation, which I did not in v3. The reason has
changed: in v3 I argued the mechanism was undetermined so conditioning it was
premature. v4 determined it — mean pooling, not pair matching — so the mechanism
question that was blocking is answered. Opponent conditioning is the right next
build, it advances the two-lineup product directly, and the largest failures
plausibly do mix opponent strength with realized shooting.

One caveat to carry into it: run **P1 first or alongside**. If part of the
context gain is deployment, then opponent strength — which is also a deployment
correlate, since coaches match lineups to opponents — will absorb some of the
same signal, and the two effects will be hard to separate afterwards.

### On the decision itself

I agree with **E0M_L2 as the structural research backbone**. It is the smallest
arm, it holds the entire teammate effect, it has the best novel MAE, and it is
the only recommendation here that gets *simpler*. I would state the headline more
narrowly than the review does: *a lineup's composition changes each player's
predicted event profile, the effect is carried by the teammate average rather
than by specific pairings, and it generalises to unseen fives in 11/11 seasons.*
That is a real result and it does not need the word chemistry.

---

## Provenance

| claim | source |
|---|---|
| arm point metrics, all and novel | `reports/point_metrics.csv` (r3) |
| pre-registered season contrasts and intervals | `reports/season_contrasts.csv` |
| event channels, both cohorts, FTA/FGA bias | `reports/event_metrics.csv` |
| per-channel point decomposition | `diagnostics/point_transfer_by_origin.csv` |
| fixture natives and support fields | `diagnostics/basketball_panel.csv` |
| E0M − E0F range over real cells | recomputed from `native` in v4e `origins/*/{E0F_L2,E0M_L2}/cells.csv.gz` |
| interval methods, scores, coverage | `reports/interval_summary.csv` |
| persistence audit | `diagnostics/failure_first_half_selected_second_half.csv` |
| alias parity and frozen v3 hashes | `audit/alias_parity.json`, `alias_registry.csv` |
| architecture, pooling modes, penalties | `experiments/joint_capability_v4_model.py` |
| protocol, λ grid, stopping rule | `protocol.json` |
| test result | `logs/full_test_suite_20260910.log` — 640 passed |
| historical FTA population gap | `ASOF_ACCOUNTING_AUDIT.md`, `ASOF_DEPLOYMENT_AUDIT.md`, `DISAGREEMENT_AUDIT.md` |

No test suite was run for this review and nothing executable was changed.
