# v7 Phase 0

2026-09-11, Claude Opus 5 with Adam. No core fits; H0.1 fits only on the two
development origins. Everything under `no_database()`.

---

## H0.2 — the 5-Shaq problem is in the NEURAL model too. My claim was half wrong.

**What I have been saying since v4**, in three reviews and two handoffs: `E0M`'s
sane behaviour on degenerate lineups comes from the shared finite budget, which
bounds what five copies of one player can score. **That is only half true, and
the half it misses is the half that matters.**

Method: 2,500 real fives at 2026q1, replace slots 1..k with copies of slot 0,
score through each model's own scorer — the neural arm on states, the corrected
additive on identities via `additive_offense_score` with its own prior-only
calibration (a = 1.807, b = 0.693) — and stratify by the **donor's own additive
per-player value**, because duplicating an ordinary player was never the failure
mode. Median individual value 1.13 pts/100, max 6.36.

1 → 5 copies, and how often the five-clone rating exceeds the 99th percentile of
real single-copy ratings (123.71):

| donor stratum | neural | additive | 50/50 blend |
|---|---|---|---|
| median (n=120) | **−6.00**, 0% | −3.43, 0% | −4.72, 0% |
| top quartile (n=200) | **+10.45**, 71% | +14.41, 100% | +12.43, 100% |
| top decile (n=80) | +16.05, **89%** | +15.25, 100% | +15.65, 100% |
| top 5% (n=40) | **+18.92**, 90% | +15.70, 100% | +17.31, 100% |

**Three things follow.**

1. **The neural model has the 5-Shaq problem.** At the top decile it moves
   **+16 points** from one copy to five and exceeds the real ceiling **89%** of
   the time. The shared budget bounds *volume* — the five compete for one `U` —
   but not *efficiency*: five copies of an elite converter each shoot at his own
   rate, so points rise with attempts held fixed.
2. **There is a crossover.** The neural arm bounds duplication better than the
   additive for good-but-not-elite donors (+10.45 against +14.41 at the top
   quartile) and **worse for elite ones** (+18.92 against +15.70 at the top 5%).
   The additive is damped by its calibration slope of 0.693, a global shrink the
   neural arm does not have; above some value the neural arm's per-player
   conversion wins out.
3. **The blend is not uniquely guilty.** It sits between its parents everywhere.
   The premise of the v7 Phase 2 product idea — *blend inside the support, neural
   outside it, because the blend reimports the additive's linear duplication* —
   **is wrong.** Outside the support the neural arm is not the safe choice.

**The coverage gate stays**, and it is now needed for every arm rather than only
for the additive. v6 showed the model extrapolates across the observed range;
that is not the same as being safe on degenerate lineups, and I conflated them.

The v5/v6 fixture story — five Goberts *down* — is consistent with this and was
never general: Gobert is efficient but his state is not an elite scorer's, and a
single fixture was doing more rhetorical work than it could carry.

### Consequence for v7

The Phase 2 product question is reframed, not deleted. The handoff is not
blend-inside/neural-outside; it is **model inside the support, asserted gate
outside it**, and what v6 bought is a *validated distance* on which to place that
boundary rather than a pinned constant. Worth measuring where the crossover sits,
because that is where the gate has to bind.

---

## H0.1 — the defaults nobody had varied in six versions are correct.

`lr = 0.001` is hardcoded in every joint-capability module from v2 to v6 and had
**never been changed**. Neither had hidden width 32, weight decay 1e-4 or batch
target 4096. γ was selected in v3 on **3.5e-5** of validation loss against a 1e-5
tie tolerance, on one arm — the tie-break-on-noise pattern that gave v2's control
λ = 1.0 and froze it at epoch 1. CLAUDE.md rule 12 has been pointing at this
since my v3 review, and it was never closed.

I expected to find the model undertrained, because v6's Phase 0 showed the
learned corrections sit at ~2% of state scale after a few hundred Adam steps.
**That suspicion is wrong.**

Two development origins (2014q3, 2014q4), epoch cap 48, mean validation loss:

| lr | width 16 | width 32 | width 64 |
|---|---|---|---|
| 0.0003 | 0.99795629 | 0.99790081 | — |
| **0.001** | 0.99787989 | **0.99779274** | 0.99782320 |
| 0.003 | — | 0.99783340 | 0.99789279 |
| 0.01 | — | 0.99815977 | 0.99818227 |

γ at the incumbent: .003 → 0.99779290, **.01 → 0.99779274**, .03 → 0.99779195.

**Both grids were widened after the first pass selected a low edge, and both are
now INTERIOR.** `lr = 0.001` beats 3e-4 below it and 3e-3 above it; width 32
beats 16 below and 64 above. Higher learning rates are monotonically worse, and
at 3e-4 the fit needs 34–36 epochs to reach a worse place than 1e-3 reaches in
17–18.

γ spans **9.5e-7** across a 10× range — it does nothing. Its v3 selection was
noise, but harmlessly so, because the parameter has no purchase. It remains at
.01 rather than moving to the .03 edge on a 7.9e-7 difference.

**Three consequences.** The rule-12 hole is closed, and the honest finding is
that the defaults were right all along. **`V7_TUNE` is not needed** — that arm is
free for something else. And the epoch cap still goes 24 → 48, not because it
binds (only 3 of v6's 240 arm-origins selected epoch 24) but because removing a
boundary costs nothing and leaves nothing un-audited.

Width 64 losing to 32 at every learning rate is the third time extra
expressiveness has gone the wrong way in this workstream, after pair pooling
(v4) and the learned encoder (v4/v5).

---

## H0.3 — §8.1's overload term cannot bind on the case H0.2 found.

Discovered while building `V7_LOAD`, and measured before a line of it was fitted.

§8.1's excess is **one-sided**: `max(0, assigned − reference) / max(prior_sd,
0.05)`. It fires only when a player is asked to do *more* than his history.

Measured on real clone ladders at 2026q1, 1,500 donors, five copies:

| donor stratum | assigned share | his historical share | mean excess | slots firing |
|---|---:|---:|---:|---:|
| median | 0.200 | 0.203 | 0.153 | 49% |
| **top decile** | **0.200** | **0.294** | **0.006** | **2%** |

Each copy of an elite player is assigned **less** than his usual share, because
the budget splits five ways. So one-sided overload addresses **five limited
creators** — which the model already handles, and which the v5 fixtures showed
going the right way — and is **silent on five stars**, which is precisely what
H0.2 showed it fails. Building §8.1 as written would have produced a null on the
case it was assigned, for a structural reason available in advance.

**The minimum widening that reaches it** is to treat displacement in either
direction as unmodelled territory. Over-use overextends a role player; under-use
wastes a creator, who no longer takes the shots his conversion rate was earned
on. Three non-negative coefficients, zero attainable, fitted on real events:

    over  = max(0, assigned − reference) / max(prior_sd, 0.05)
    under = max(0, reference − assigned) / max(prior_sd, 0.05)
      + k_to_over    · over    on the turnover-versus-FGA log odds
      − k_make_over  · over    on the FG make logits
      − k_make_under · under   on the FG make logits

No `k_to_under`: an under-used player has no mechanism story for turning the ball
over more, and a free parameter without one invites noise.

On the same star-clone case the under-use excess is **0.627** where the one-sided
term read 0.006, so the mechanism can now reach the failure. **Whether it should
is for the data to say.** This is a widening of the hypothesis, not a tuning of
it: all three coefficients are fitted on real events with zero attainable, and if
they fit zero the duplication problem is unsolved and that is the finding. §8.1's
own instruction stands — never tune k to make a fixture cross a chosen number.
