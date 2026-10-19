# Feedback on the contextual/structural direction

*Written 2026-09-04 by a reviewer who worked on the incumbent additive model
and the coverage gate, reading the contextual line cold. Opinions, not
findings; every number quoted is from the repo's own CSVs and is cited.*

---

## 1. The direction is right, and it is right for a specific reason

The move from "fit a residual and adjust the output" to "model the resource
ledger and let the penalty fall out" is the correct architecture, and not just
on aesthetic grounds. This project's own history says so.

Of every composition structure ever measured here, the one that survived
forward without qualification was usage demand — and the note recording it says
why: *"a conservation constraint, not a fitted effect."* Floor geometry
predicted well and had to be thrown away because its sign inverted out of
support. Defensive coverage died against a fresh baseline. The sparse bilinear
was a leak. The profile bilinear is a powered null at every width. The one
survivor was the one that encoded a fact about basketball — there is one ball —
rather than a correlation.

So the contextual line is not merely "a different model." It is a bet that the
*class* of structure that already worked is the class to build in. That bet
looks correct. The usage pool is a conservation constraint. The assist deficit
is a conservation constraint. Both survive forward. That is two for two in a
project where nearly everything else died.

The corollary is the main criticism in this document, and it is a criticism of
scope rather than of approach: **the model currently conserves one resource
properly, one partially, and none of the others.** Every place a five-man
lineup's projection is still a free sum of five independent player rates is a
place the same failure will recur. It already has, on rebounding.

---

## 2. The general principle worth adopting explicitly

> Anything five players compete for must be modeled as a pool that is divided,
> not a rate that is summed.

Right now the codebase has three different treatments of that single idea:

| resource | treatment | status |
|---|---|---|
| usage events | pooled and allocated (alpha 1) | correct |
| assists | free sums, differenced, soft hinge on the gap | partial |
| offensive rebounds | free sum of five individual rates | **broken** |
| shot location | scaled sum of five individual mixes | **broken, and it matters most** |
| defensive attention | not represented | absent |

Unifying these is worth more than any new feature. One allocator, applied per
channel, replaces a growing set of bespoke penalties — and each bespoke penalty
is a place where an asserted number hides.

### The rebound case is the proof

`rebound_shot_value_2026_*` ran to completion and, because of the usage cutoff,
was never read. It is the most informative thing on disk. Named panel, latest
state, points/100:

| lineup | fixed / creation-reg | fixed / shot-exp | rebound / creation-reg | rebound / shot-exp |
|---|---:|---:|---:|---:|
| Jokić + Korver | 122.6 | 122.9 | 122.7 | 121.4 |
| five centers | **103.8** | 112.1 | 105.8 | **125.1** |
| five Goberts | **106.7** | 114.8 | 109.3 | **124.5** |

Two independent defects were cancelling.

1. **The conditional ORB coefficient (−0.365) was supplying about a third of
   the five-center penalty.** They project 19 more ORB/100 than Jokić+Korver,
   so that coefficient alone is ≈ −7 pts/100 before the score slope. The
   perturbation harness shows the same coefficient makes +1 isolated ORB/100
   *hurt* 97–100% of 5,774 real lineup-origins. It is not a rebounding effect.
   It was doing five-center duty in a valuation coefficient's clothing.

2. **Projected ORB is an unconstrained sum.** Five centers project 33.8 ORB/100
   against a 39.9 miss envelope — an **85% offensive rebound rate**, where real
   teams get 22–30%. Under the rebound ledger that grants them 135.5 usage
   events and 97.5 FGA per 100 against a normal 113/88: roughly 22 unearned
   scoring opportunities. Five guards project 4.8 (≈10%), implausibly low. On
   real lineups the sum happens to be calibrated, so the error is invisible
   until you leave support — the same shape as every 5-Shaq failure here.

This is precisely the independence fallacy the project already rejected for
assists ("profiles from different contexts are not a simultaneous ledger"),
committed again one channel over. Worth stating plainly: **the negative ORB
coefficient was silently discounting an over-counted ORB sum.** Make the
valuation literal *and* grant those rebounds real opportunity, and both
protections vanish at once.

The fix follows from the principle: team ORB/100 = predicted misses/100 ×
ORB%(five), with ORB% a bounded function of the five's rebounding profiles fit
against observed team ORB%, then allocated among the five with the existing
alpha-1 machinery so per-player credit survives for the Adams / Robinson / Hart
readouts. Under a *fixed* budget, shot-expectation already ranks five centers
10.8 below Jokić+Korver — only the runaway budget flips it — so bounding ORB%
plausibly lets one arm pass both coherence checks for the first time.

---

## 3. The uncomfortable fact the rebound run establishes

Across the eight arms, five centers spans **21 points/100** while forward MAE
spans 7.453–7.765 and held-out interval coverage is identical to three decimals
(≈ 0.50/0.80/0.95 at nominal 50/80/95).

**On real lineups, forward accuracy is nearly blind to the choice that
determines the counterfactual answer.** A 21-point swing in the flagship case
costs at most 0.3 MAE.

This is not a flaw in the evaluation; it is the honest structure of the
problem, and it deserves to be a stated premise rather than a discovery made
repeatedly. Three consequences:

- **Pillar A cannot arbitrate pillar B.** The three standards are not
  co-equal in the sense of being interchangeable evidence; accuracy is nearly
  uninformative about out-of-support behaviour, by measurement.
- **Coherence checks are therefore load-bearing, and they can conflict.**
  Right now no arm passes both the rebounding mechanism check and the
  pathological-lineup check. That conflict is the real result of the rebound
  experiment and should be the headline of the next checkpoint.
- **Therefore the asserted basketball content should be explicit, principled
  and few.** The failure mode is not "we asserted something." It is that the
  assertion was hiding inside a fitted regression coefficient where nobody
  could audit it. The coverage gate was at least honest about being asserted.

---

## 4. How to put more basketball into the model

Six concrete places, ordered by what I think they are worth. All of them are
conservation or threshold facts — things true of basketball rather than
correlations to be discovered in selected data.

### 4.1 Shot location is a contested resource, not a player attribute

This is the biggest one, and the machinery for it already exists and is already
validated.

The model transports each player's historical shot mix into the lineup. But
shot mix is the most context-dependent thing about a player. Gobert's rim rate
exists *because* Mitchell and Conley created it. Five Goberts keep the all-rim
diet and the model has to claw the points back with an assist-deficit penalty —
a proxy for the real mechanism.

The real mechanism: **the rim is a finite place.** Five rim-finishers cannot all
get rim attempts; somebody takes the 18-footer, and Gobert is dreadful there.

Build it exactly like the usage pool:
- predict the *lineup's* shot-location distribution from the five profiles —
  already done, and these are the strongest channels in the project
  (`channel_totals_validation`: 0.710 rho for 2PA, 0.693 for 3PA, versus 0.322
  for FTA);
- allocate those attempts among the five;
- value each player at *his* efficiency at the location he actually gets.

This makes five centers bad for the reason they are actually bad, with no
hinge, no penalty coefficient, and no extrapolated slope. It also fixes the
duplicate-player bug noted in §5 for free. The fact that team-level location
distribution is far more stable than player-level location distribution *is*
the evidence that location is a team property being mis-attributed to players.

### 4.2 Creation and finishing are different currencies; the excess should be reallocated, not taxed

The hard assist cap failed, and it failed for a good reason — it assumed every
unsupported assisted make becomes a miss, which destroyed calibration (raw r²
−0.156 → −0.621). But the soft hinge that replaced it taxes points without
changing what happens on the floor.

The basketball fact in between: **a player's self-creation capacity is a hard
attribute that should not scale with assigned usage.** Today, scaling usage up
scales assisted demand up — which is how the deficit arises. But giving Gobert
2× usage should generate approximately zero extra self-created shots. The extra
usage should convert into turnovers and bad shots, not into more assisted dunks
that then get taxed.

So: cap each player's *assisted* attempts at what the lineup's assist supply can
actually feed, and convert the excess into *self-created* attempts priced at
that player's self-created efficiency. That is a reallocation inside a closed
ledger, not a destruction of possessions — which is exactly why it should
survive where the hard cap did not. And it is the mechanically correct version
of "five centers have no ball handler."

The profile already carries `assisted` share and self-created 2P/3P rates. The
pieces are there.

### 4.3 Spacing is a count, not a mean

`CONTEXTUAL_MODEL.md` correctly admits the four fewer threes in the Westbrook
lineup are a profile difference, not an estimated spacing interaction.

The basketball fact is that spacing is about **how many defenders can leave the
perimeter** — a count of non-shooters, not an average shooting rate. One
non-shooter is nearly free. Three is catastrophic. That is a threshold, and
this project has already learned the hard way that means do not extrapolate:
floor geometry's uniformity measure helped in range and inverted outside it.

A count of "players a defense will not guard beyond 18 feet" is
basketball-legible, monotone by construction, and has a pre-registerable sign.
It is also the kind of feature whose out-of-support behaviour you can reason
about without data, which is the whole problem.

### 4.4 Defense has two conserved resources with *opposite* curvature

The prototype is entirely offensive — no new module imports `DEF_COLS`. That
means the five-center lineup is currently judged only on the half of the floor
where it is bad, which is not the right basketball answer: it would be a
historically good rim-protection and defensive-rebounding unit with
catastrophic perimeter defense.

Two resources, and the important part is that they curve in opposite
directions:

- **Rim protection is strongly diminishing.** There is one rim. The second
  elite rim protector adds far less than the first, and the fifth adds ~nothing.
- **Perimeter coverage is a threshold failure.** Five offensive players must
  each be accounted for. If two of your five cannot guard anybody, the other
  three are stretched past the point where scheme can hide it.

A single "coverage spread" summary cannot represent both, and I can say that
from having got it wrong: a positional-spread gate I built false-positived on
the 2021 Clippers (−3.06), the Thunder (−3.04) and the Suns (−1.61). Spread
cannot distinguish "all wings" (works) from "all centres" (does not). Two
separate curves, fit per side, is the minimum honest representation.

Also worth carrying over: `channel_ceiling.py` established defence is 8:1 shot
*selection* over shot *making*, and 47% scheme. So defense should be modeled as
"what shots does this five allow" — a location-allocation problem symmetric to
4.1 — rather than as a mirror of the offensive point score. And roughly half of
it is not attributable to players at all, which is a real ceiling on any
player-additive defensive model and should be stated up front rather than
discovered later.

### 4.5 Some jobs must be filled, and competence at them is a threshold

Adam's original framing, still unrepresented. Every possession needs somebody to
advance the ball against pressure and initiate. That is a job with a competence
floor, not a continuous quantity to be averaged.

`selection_on_the_outcome` proves this cannot be fitted from observational
lineup data — coaches field an unusual five only when it works, so in-range
"unusual" correlates with "good" and every fit inherits the sign. So the
initiator requirement has to be asserted. That is fine, provided it is asserted
*once*, in basketball language, in a place a reader can find. The cheapest
honest version: the lineup's best ball-handler must clear a threshold; below it,
turnovers rise and shot quality falls, through the allocator rather than as an
output multiplier.

### 4.6 State should carry a role, not only rates

`usage_load_response.py` is, I think, underrated by the documents that describe
it. It is the identification strategy `ROLE_MODEL.md` was asking for and could
not name: composition-assigned load moves the same player's realized output —
more usage and assists, lower efficiency, more turnovers, less assisted scoring,
with a clean FT% placebo. That is aptitude-versus-assignment, measured, on 5.6M
possessions rather than on a 1e-4 residual.

The two lines should be connected explicitly. The contextual work has
rediscovered the role model's premise from a different direction and is
currently spending it on a single scalar response slope. The Cooper Flagg
question — was he better as a primary or as a secondary creator beside one —
is answerable with the instrument that already exists.

---

## 5. Code and method notes

Mostly small; the discipline here is genuinely good and these are the exceptions.

**Worth fixing:**

- **The named panel is not out-of-sample in its inputs.**
  `structural_counterfactuals.py:293` passes `_prior_environment(blocks, season_max + 1)`,
  which makes the `s < season` filter a no-op, and `panel_profiles` calls
  `select_states` with no `as_of_season` while every validation caller passes
  `season - 1`. The *coefficients* are prior-only, so no validation table is
  affected — but the headline counterfactual numbers use globally-fit profiles,
  channel prices and usage ledger, and they are quoted beside forward-validated
  numbers without that distinction.

- **Duplicate-player lineups scale the making term too.** The usage ledger
  divides the league target by 5× Gobert's native usage, scaling attempts ~2×,
  and `making` is computed from the scaled attempts. His rim finishing is
  credited at twice any volume he has ever played — a second unflagged
  extrapolation, distinct from the assist deficit. §4.1 removes it structurally.

- **`orb_exceeds_miss_envelope` fires only above 100% of misses.** The physical
  bound is ~35%. An 85% offensive rebound rate passes the guard. General
  lesson worth adopting: **impossibility checks are too weak to catch
  implausibility.** Every out-of-support guard should be against the observed
  range, not against physical contradiction.

- **The evaluation rig has diverged from `lineup_scoreboard.py` in five ways**
  — no detrend, no home residualisation, no opposing-side subtraction, min 50
  vs 100 possessions, nan vs floor on unidentifiable splits. The third one
  matters: `lineup_scoreboard.py:143-149` measures the opponent subtraction as
  worth ~0.4 of calibration slope. The structural model's 0.76 slope and its
  pred_sd/truth_sd ratio of 0.68 may therefore be partly a rig artefact rather
  than under-dispersion — which cuts in the model's *favour*, so it is worth
  knowing. This project's rule 13 exists because two rigs disagreeing is
  evidence; reconcile them or measure the gap deliberately.

- **No head-to-head against the incumbent exists.** No new module imports
  `additive_stack`, `tool_model` or `lineup_scoreboard`. The "0.285 versus the
  incumbent's roughly 0.57" citation compares runs on different targets,
  different lineup universes and different rho estimators — the exact
  cross-run comparison the project has a rule against. `CONTEXTUAL_MODEL.md`
  §2A requires that the accuracy trade be "printed, not hidden"; it is
  currently unknown in both directions. `contextual_validation._crossfit_truth`
  takes a `predictor(lineups)` callable, so this is cheap.

- **The assist deficit partly acts as a slope correction.** Adding the deficit
  column raises the fitted score slope in 10/11 expanding origins (2026:
  0.857 → 0.902). Some of what it buys is de-shrinking an over-shrunk score
  rather than pricing a passing shortage. Refitting with the score slope pinned
  to the control's value would separate the two. (The headline `expanding`
  policy is otherwise clean; only `previous` has a degenerate origin — 2021,
  where the control's slope hit its ≥ 0 bound and collapsed to a constant.)

- **The deficit is extrapolated without a cap and is representation-dependent.**
  The maximum ever observed on a real lineup is 18.65; five Goberts is 23.4
  fixed and 28.4 under the rebound ledger, penalised by unbounded linear
  extension. Separately, five centers' deficit is 18.3 under cumulative state
  and 8.0 under latest — outside the real p99 of 12.25 in one case and inside
  it in the other, from a representation choice that accuracy calls a tie
  (MAE 7.474 vs 7.497). Both facts belong next to the panel numbers.

- Minor: `_prior_environment` can return `None` but `channel_points_validation.py:330`
  unpacks it into three names unconditionally.

**Worth keeping and copying:**

- Pre-registration written before results, with the follow-up specified before
  the first arm's outcome was known. This is the reason the rebound experiment
  produced a usable answer instead of a tuned one.
- Tests that assert *known failures*
  (`test_control_exposes_negative_isolated_rebound_value`,
  `test_perfect_shooting_exposes_missing_opportunity_conditioning`). Encoding a
  disclosed limitation as a test is the right way to stop it being quietly
  fixed by accident, and it made the perfect-shooting diagnostic actually fire.
- Six clean self-rejections. Alpha 3 as literal assignment, the hard assist cap,
  the assisted-share interaction, the role-distance interval schedule,
  budget-expansion-alone, the single transported slope. The willingness to kill
  a result that had already been written up is the most valuable habit here.
- The `reliability.py` pooled-moment fix — averaging split-wise ratios produced
  correlations above 1 — is a real bug of this project's historical family.
- Sign-constrained fits via bounded least squares. Cheap, and it removes an
  entire class of "the coefficient came out backwards but we kept it."

---

## 6. What I would do next, in order

1. **Read out and record the interrupted rebound run.** It is a finished
   experiment with an unwritten conclusion, and its conclusion — no arm passes
   both coherence checks — is more important than the arm that was being
   tested.
2. **Conserve offensive rebounds** (§2). Pre-register first; the prediction is
   that bounding ORB% lets shot-expectation + rebound ledger pass both checks.
3. **Conserve shot location** (§4.1). The highest-value structural change, and
   it uses channels already validated at 0.71/0.69 rho.
4. **Reallocate the assist excess instead of taxing it** (§4.2). This is the
   version of the failed hard cap that should work.
5. **Print the accuracy trade against the incumbent** on one rig (§5).
6. **Then defense** (§4.4), with two curves rather than one spread.

Steps 2–4 are the same change three times. If they land, the assist-deficit
hinge, the ORB coefficient and the coverage gate should all become unnecessary
rather than needing to be tuned — which is the test of whether the direction
was right.

---

## 7. One closing thought

The strongest thing about this direction is that it is trying to make graceful
degradation *derived* rather than asserted. The incumbent gate asserts a
number; a closed ledger with conserved resources produces one.

But the rebound run shows how easily an assertion migrates into a fitted
coefficient and stops being visible. −0.365 per offensive rebound was carrying
a third of the five-center answer, and nobody chose that. The way to keep the
direction honest is not fewer assertions — it is fewer *hidden* ones: a short,
explicit list of basketball facts the model is built on (one ball; one rim;
finite misses; every shot has a creator; somebody must bring it up; five
defenders for five attackers), each implemented as a constraint rather than a
coefficient, each auditable by someone who has never read the code.
