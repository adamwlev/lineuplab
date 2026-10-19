# The role-assignment model — design with stage-3 evidence

*Written 2026-09-03 at the end of a session that closed six composition ideas;
updated 2026-09-04 after the first assigned-load tests. Read `CLAUDE.md` for
the rules of evidence, `CONTEXTUAL_MODEL.md` for the active product contract,
and `CURRENT_MODEL.md` for what the incumbent model is today.*

---

## 1. The problem this exists to solve

The tool prices any five in points per 100. It is broken by lineups that cannot
**function** — five centres with nobody to bring the ball up, five guards with
nobody to protect the rim. Today that is handled by an asserted **coverage
gate** (`tool/README.md`): a multiplier keyed on whether the five have a player
at position ≤ 3 and one at ≥ 3. It works, its in-range cost is measured at
0.0009 pts/100, and it is honest about being a guardrail.

It is also a patch applied after the model has spoken. The right thing is a
model that produces the penalty itself.

**Every attempt to get there by adding a FEATURE has failed, and the failures
rhyme:**

| structure | result |
|---|---|
| profile bilinear, sparse bilinear, RFF, quadratic prior | powered forward nulls (§13.3, §18.4, §18.5) |
| floor geometry (shot-map diversity) | predicts, **sign inverted** (§18.3) |
| index curvature | all defensive, **sign inverted** (§20.3) |
| defensive coverage (height/position spread) | dies on a fresh baseline (§19.2) |
| multiplicative usage conservation `I·(D̄/D−1)` | powered null (§22.1) |
| order statistics of the profile (`ORD` − `LIN`) | **+0.0000026** — nothing |
| role stretch (usage rank vs habitual rank) | null, and does not beat its placebo (§31.1) |
| defensive assignment cost | t=+0.85, but **4/4 pre-registered signs** (§31) |

The reason is always the same and it is not the functional form. **99.99% of
real possessions have a ball handler** (§30.2). A model fitted on the residual
of real lineups has no information about the case the requirement is about, and
worse, what variation there is has the wrong sign because lineups are
*selected on the outcome* — a coach fields an unusual five only when it works
(§20.5).

## 2. The idea

Basketball has roles that **must** be filled. Somebody brings the ball up on
every possession. If five centres ever shared a floor, one of them would have
to, and he would be bad at it.

So a player's observed profile confounds two things:

1. what he is **capable of** at each role — his aptitude;
2. what he was **asked to do**, which depends on who else was on the floor.

Cooper Flagg played point guard for much of last season because Irving was
hurt. Build a profile from his box score and he looks like a lead ball handler.
That is a team filling a hole, not a statement about him. The question worth
answering — *was he better as a primary, or did he over-perform as a secondary
creator beside a real point guard?* — is exactly the question the model needs
to answer to price a hypothetical five.

**The confound is already measured in this repo.** `context_bias_is_real`:
teammate context bends the box score, placebo-clean, and it keys on **role**
(`assisted`) rather than on shooting skill. What nobody has done is *invert*
it. The same variation that contaminates the profile identifies aptitude,
because we see the same player at different assigned roles depending on who is
beside him.

## 3. The model

Three stages. The prediction for a five is formed differently, not corrected
afterwards.

```
  1. APTITUDE      a_p    a vector over roles, per player, latent
  2. ASSIGNMENT    who takes which role in THIS five,  given {a_p}
  3. VALUE         each player priced at the role he is ACTUALLY given
```

**Stage 1 — aptitude.** Latent, but its consequence is observed: the
within-lineup distribution of role load. For each (player, lineup) we observe
his usage share, his assist share, his rebound share, his shot-location mix.
Model that as a choice: the ball goes to the man best suited to having it,
softly. A conditional-logit / softmax over the five, with `a_p` as the utility.

**Stage 2 — assignment.** Falls out of stage 1: for a hypothetical five,
predict the role loads from `{a_p}`. Five centres → one of them is handed 30%
usage because somebody must be.

**Stage 3 — value.** A player's contribution is a function of the role he is
given, not of his career average: `θ_p(load)`. Five centres is penalised
because the model prices a centre **at 30% usage**, which it can estimate —
centres do end up there, in garbage time, in injury stretches, on bad teams.

**Why this escapes the trap in §1.** Stage 1 is not a 10⁻⁴ residual-fitting
problem. The assignment is *directly observed* on 5.6M possessions, so it is a
well-determined estimation problem with an enormous sample. The model factors
into a **well-identified part** (who takes the ball) and a **hard part**
(what it is worth), and the well-identified part carries the structure that
makes five centres bad.

## 4. Why Bayesian, specifically

Three things, and the second is the reason to do it at all.

**(a) The parameter count.** `θ_p(load)` is several parameters per player where
there was one. With ~1,200 players and a corpus that supports r² ≈ 0.002, a
free fit is hopeless. Partial pooling toward a **role-specific prior mean
predicted from the box score** is the fix — and it is exactly what
`prior_ridge` already does for `θ`, which is the single most robust lever in
the project (+0.000244 forward). Ridge *is* a Gaussian prior and the repo
already picks its scale by empirical Bayes; this is an extension of machinery
that works, not a new machine.

**(b) Graceful degradation stops being asserted and becomes derived.** This is
the point. For a lineup that forces a centre into a 30%-usage role, there is
almost no data at that (player type, load) combination, so the **posterior
reverts toward the prior with a wide interval**. That is precisely the
behaviour the coverage gate currently asserts, and precisely what
`distance_shrink.py` could not fit as a schedule. A correctly specified
hierarchical model produces it as arithmetic rather than as a product decision.
**If this works, the 5-Shaq rule is met by the model instead of by a guardrail,
and CLAUDE.md's northstar item can be rewritten.**

**(c) Honest per-lineup uncertainty, which the additive model cannot give.**
`lineup_uncertainty.py` measured the additive posterior sd across real lineups
and it varies only **1.3×** and does not order calibration quality — which is
why per-lineup error bars were measured and deliberately not shipped. The
reason it is flat is that the additive model has no notion of being outside its
support: every five is just a sum. A role model does have one, so its posterior
should widen exactly where the five is unlike anything observed. That is a
testable prediction and it is the same test `lineup_uncertainty` already
implements.

**First distance test, 2026-09-04: null.** Before building the hierarchy,
`role_support_validation.py` measured how far each held-out assignment lies
from that player's prior common/relative load history. After prior-origin point
calibration and game-disjoint noise correction, centered persistent-error SD
is 3.95, 3.94, 3.50 and 3.87 pts/100 across increasing distance quartiles;
Q4−Q1 error variance is −0.58 ± 3.76 (t=−0.15). The empirical distance is not
an interval schedule. This does not test the proposed posterior—observed roles
occupy a selected, narrow range—but it raises the bar: the hierarchy must show
calibration that this shortcut could not.

## 5. Do these cheap things FIRST

CLAUDE.md rule 8: measure the ceiling before building the model. Each of these
can kill the build in under an hour, and they are ordered so the cheapest
decisive one comes first.

**5.1 Does a player's value actually vary with his assigned load?** If
`θ_p(load)` is flat, stage 3 is empty and the model cannot penalise five
centres however well stages 1–2 work. Bin (player, lineup) cells by the
player's *predicted* share (career usage rationed by the five's total — a
function of composition, not an outcome) and read his marginal contribution
within player. **Watch the endogeneity**: realised share is an outcome, so use
the predicted one. This is the single most important number in the design.

**Result, 2026-09-04: yes at the population level.**
`usage_load_response.py` builds profiles strictly before each held-out season,
assigns load from lineup composition alone, and joins that assignment to
held-out player-game output. Across 2015–2024, more assigned load predicts more
realized usage and assists, but lower points per usage (player FE
−0.0785 ± 0.0109, t=−7.23), more turnovers, lower eFG and less assisted
scoring. FT% is null. The signs survive player + team-game fixed effects.

The transport test is more discriminating. One scalar slope worsens lineup
points, while separately measured common-lineup and player-relative slopes
improve alpha 3 true-quality rho 0.4636 → 0.4813 and MAE 8.299 → 8.155 using
only earlier-origin slopes. Thus stage 3 is not empty, but it is not solved.
Five Goberts still retain implausible finishing efficiency. A pre-registered
interaction with prior assisted share is correctly signed but null (t=−0.83
common, −0.92 relative), so that particular type-specific shortcut is closed.

**Direct allocator result, 2026-09-04: use alpha 1 for assignment.** When the
realized held-out team total is conditioned out, alpha 1 beats alpha 3 badly on
who actually consumes usage (NLL 1.816 vs 1.873; share correlation 0.931 vs
0.882) and is selected at every rolling origin. Usage, FGA, assists and
assisted makes all agree. Self-created makes mildly favor alpha 1.5 by MAE only.
The alpha-3 point-ranking gain was not a direct role-allocation result.

**First structural point result, 2026-09-04: the factorization works.** A
training-only alpha-1 ledger predicts future shot mix, turnovers, offensive
rebounds and self-created makes. Training-only channel valuation plus separate
shot-making skill is tied with the current box-score point construction. A
sign-constrained assist-deficit residual then improves true-quality rho
0.413 → 0.482 across nine future origins and lowers five Goberts to 106.75
offensive points/100 without a gate. This is a simpler empirical realization
of stages 1–3 than the full Bayesian build. The remaining Bayesian burden is
uncertainty: the pathological deficits exceed observed support, so a coherent
mean alone does not satisfy the product contract.

**5.2 How much within-player variation in assigned load actually exists?**
Distribution of a player's usage-rank across the lineups he played in, weighted
by possessions. If most players sit at one rank almost always, stage 1 is
identified only for the minority who moved around, and the model's reach is
that minority.

**5.3 Re-screen `ORD` on a de-contaminated profile.** `ORD` − `LIN` is
+0.0000026 on the *raw* profile. If aptitude ≠ profile, the order statistics of
**aptitude** may carry what the order statistics of the raw profile do not.
`context_deconfound.py` has an exact resolvent for the static version. This is
the cheapest direct test of the whole premise, and it re-uses two existing
modules.

**5.4 Reconcile with `context_deconfound_null`.** Subtracting context was null
forward (+0.000001) and adding it was null too (+0.000011 ± 0.000015). That is
the static version of stage 1 and it did not help. Understand whether it was
null because aptitude ≈ profile, or because the correction was tiny, **before**
building the dynamic version. If the former, the whole design is in trouble.

## 6. What is already in the repo

| piece | module |
|---|---|
| context bends the profile, and keys on role | `context_profile.py` — `context_bias_is_real` |
| exact resolvent for removing context | `context_deconfound.py` |
| per-(player, game) box score, leak-free by fit window | `game_player_stats.py` |
| the prior that maps profile → value | `prior_ridge.py` (now `box+posn`) |
| lineup cells, pair keys, forward rig with nested arms | `forward_pairs.py` |
| the conservation template that WORKED | `demand_block` — usage demand, +0.0000103 (t=+4.99) |
| the sign-check template | `match_block` — 4/4 pre-registered signs |
| per-lineup posterior machinery | `lineup_uncertainty.py` |
| end-to-end product check | `page_calibration.py` |

## 7. Risks, stated plainly

- **`context_deconfound` was null.** The static stage 1 did not help
  forecasting. §5.4 exists because of this and it should be settled first.
- **Endogeneity in stage 3.** A lineup where a player shot a lot may be one
  where he was hot. Use predicted load, never realised, and expect to have to
  defend that choice.
- **Selection has not gone away.** Coaches assign roles well, so the observed
  (player, load) pairs are the good ones — the same bias as §20.5 one level
  down. The Bayesian answer is that the posterior is honest about regions with
  no data, but that is an argument for the *uncertainty*, not for the *mean*.
- **This is the eighth composition idea.** Seven are closed. The prior that it
  works should not be high, and the kill-tests in §5 are there to spend an hour
  rather than a week finding out.

## 8. What success looks like

Not an r² number. Three things, in order of what they would change:

1. **`θ_p(load)` is measurably non-flat** (§5.1) — the mechanism exists.
2. **The model prices five centres badly without being told to**, and prices
   the 2021 Clippers correctly, with no gate applied.
3. **Its per-lineup posterior widens out of support** where the additive one
   does not (§4c) — at which point the coverage gate can be deleted rather than
   disclosed, and the northstar's 5-Shaq item is met by measurement.
