# Offense-side assumption O (creation conservation): failed — 2026-10-12

Exploratory (docs/CLOSEOUT.md, step 4b).
- Script: `scripts/creation_law_screen.py`.
- Output: `experiments/cache/creation_law_screen_2026_10_12/`.

**Result: O is not used.** The band keeps the reference (R) and capacity (C)
only.

## The assumption

The reference model already has a creation constraint. It sets each player's
assisted-finishing demand against the lineup's passing supply:
- shortage = log(demand / supply), at team level or for the player against
  his four teammates;
- assisted conversion is lowered by k_supply × shortage.

The fitted k_supply is about 0.1. O declared the law at full strength,
k_supply = 1: each assisted make's odds scale by supply / demand. It was meant
as the band's offense-side alternative, so that "no ball handler" would widen
the band.

## Test on real lineups

The 2016–2026 benchmark:
- 44 quarters, 8,345 broad cells, the calibrated network alone, three seeds;
- every saved reference fit rerun with k_supply = 1;
- each seed calibrated by its own prior-only affine;
- the rebuilt reference equals the saved forecasts.

| | R | O | O − R (season SE) | Seasons O > R |
| --- | ---: | ---: | ---: | ---: |
| Raw r² | .1615 | .1450 | −.0164 (.0027) | 0/11 |
| Centered r² | .1012 | .0809 | −.0203 (.0031) | 0/11 |

- O moves 93% of cell possessions by more than 0.1 points. Most real lineups
  have some shortage, usually a finisher whose own assisted demand exceeds
  his four teammates' passing.
- Real lineups with such shortages do not pay what full conservation
  implies. The data contradict the assumption in range.

## Why a hinge does not rescue it

A hinge would apply the law only beyond the largest team shortage among
trained real fives. Five Goberts are not beyond that.
- Across 10,352 fives with at least 25 possessions in 2021–2026, the team
  shortage (mixture mean) has quantiles: median −0.07; 99% 0.45; 99.9% 0.64;
  maximum 0.89.
- Five Goberts are at 0.68 and the legal centers at 0.67.
- A threshold chosen to make the hinge bite would be fitted to the answer,
  which the decisions of record rule out.

## Reading

In this model's terms, the five-center offenses are extreme, beyond 99.9% of
real fives in creation shortage, but not outside what real lineups have
played. Nothing measured says their offense collapses further than the
reference already has it: 108 against a league-average 114.5.

The case that five centers fail therefore rests on:
- the named support reasons: no ball handler, no shooter, five non-spacing
  bigs, and a composition beyond every trained lineup;
- the defense-side assumption C, which carries a small in-range cost;
- a wide band.

That is the "acceptable outcome" in AGENTS.md, not the best one.
