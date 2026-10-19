# Era backtest 2006–2013: results — 2026-10-12

These are the results of the run registered in
[the protocol](era_backtest_protocol_2026_10_12.md).

- **Run.** 192 fits: 32 origins × arms R and C × seeds 17, 23, 41. They are in
  `experiments/cache/era_backtest_2026_10_12/`, made from the worktree pinned
  at fa08a160.
- **Scorer.** The frozen `scripts/era_score.py`, unchanged. Its output is
  `.../score/result_through_s41.json`.
- **Population.** 28 scored quarters, 2007q1–2013q4 (7 seasons). There are
  5,476 broad offense-five cells with at least 50 possessions each. Each
  forecast is the calibrated neural model alone, averaged over three seeds.

Anything the protocol does not name is marked **post hoc**.

## Verdict

| Contrast | Result | Reading |
| --- | --- | --- |
| 1. Big-defense gradient, C − R | −0.25 ± 0.22 points per 100 (season SE) | No difference. Capacity is not closer to zero; its point estimate is further away. |
| 2a. Raw r², C − R | −0.0018 ± 0.0018; lower bound −0.0053 | **Not non-inferior** |
| 2b. Centered r², C − R | −0.0027 ± 0.0014; lower bound −0.0054; 1 of 7 seasons positive | **Not non-inferior** |

In the era where big defenses have outcomes, the capacity-law defense does
not track them better than the reference does. It also ranks lineups worse.
This agrees with the 2016–2026 post-hoc finding: centered −0.0024 ± 0.0008,
neural model alone.

The result was stable across seeds:

| Seeds | C − R gradient | Δ centered r² |
| --- | ---: | ---: |
| 17 | −0.25 ± 0.28 | −0.0031 |
| 17, 23 | −0.26 ± 0.24 | −0.0029 |
| 17, 23, 41 | −0.25 ± 0.22 | −0.0027 |

## 1. Big-defense gradient

Residual is actual minus forecast, in points per 100. The gradient is the
residual on defenses with three or more bigs (82 in or taller) minus the
residual on defenses with at most one.

| | Estimate | Season SE |
| --- | ---: | ---: |
| R | −1.06 | 0.59 |
| C | −1.31 | 0.60 |
| C − R | −0.25 | 0.22 |

Both models give big defenses too little credit. Real offenses score about a
point per 100 less against three-big defenses than either model forecasts.
The protocol says neither model's own gradient is free of deployment
selection, so this is not a clean causal estimate. The paired C − R
difference is free of selection that affects both models equally.

**Per season:**

| | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R | −0.18 | −3.21 | −2.87 | +0.70 | +0.05 | −0.11 | +0.09 |
| C | +0.51 | −3.68 | −2.72 | +0.29 | −0.02 | −0.69 | −1.08 |
| C − R | +0.69 | −0.47 | +0.15 | −0.41 | −0.07 | −0.58 | −1.17 |

**Secondary: residual by number of defensive bigs.**

| Defensive bigs | Possessions | R | C |
| --- | ---: | ---: | ---: |
| 0 | 239,529 | +0.29 ± 0.25 | +0.27 ± 0.31 |
| 1 | 868,631 | −0.52 ± 0.21 | −0.50 ± 0.19 |
| 2 | 470,829 | −0.84 ± 0.25 | −0.62 ± 0.17 |
| 3+ | 60,134 | −1.40 ± 0.56 | −1.64 ± 0.52 |

The residual falls steadily with size under both models. Each added big is
worth about half a point per 100 more than either model credits.

## 2. Accuracy

| | R | C | C − R | Season SE | Lower bound | Seasons C > R |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Raw r² | .1464 | .1446 | −.0018 | .0018 | −.0053 | 2 of 7 |
| Centered r² | .1357 | .1330 | −.0027 | .0014 | −.0054 | 1 of 7 |

Per-season Δ centered r²: 2007 +.0026, 2008 −.0010, 2009 −.0013,
2010 −.0048, 2011 −.0022, 2012 −.0089, 2013 −.0046.

## 3. Post hoc: why capacity did not help (seeds 17 and 23)

This section comes from `scripts/era_diagnostics.py`. Its tables are in
`experiments/cache/era_diagnostics_2026_10_12/tables_s17_23/`.

- **The third big still matters.**
  - Real steps per added defensive big are about −1.8, −1.4 and −0.7 points
    per 100.
  - The reference's forecast flattens at the third big.
  - Capacity reads only the top two inside defenders, so it gives the third
    big the wrong sign.
- **The channel is conversion.** Against 3+ bigs, the miss is mostly made
  shots, everywhere on the floor:
  - conversion −2.4 (R) and −2.8 (C);
  - rim FG% 1.2–1.8 points below forecast.

  It is not shot volume or location.
- **The miss is largest against small offenses.** With at most one offensive
  big, the residual against 3+ defensive bigs is −2.0 (R) and −2.3 (C).
- **It is not only keep-what-works selection.** The gradient holds in a
  defensive five's first game: R −1.9 ± 1.0, C −2.0 ± 1.0. It also holds for
  fives with no prior possessions together: R −1.3, C −1.6.
- **Familiar defenses are about 2 points better than forecast at every
  size.** Defensive fives with 200 or more prior possessions together beat
  the forecast by 1.8–3.5 points. This replicates on 2016–2026
  (`scripts/familiarity_check.py`).

## What this changes

- **The confirmatory recommendation gets stronger.** Keep the reference.
  Capacity stays only as the band's named alternative assumption, labeled as
  an assumption with no in-range support.
- **The data contradict the capacity assumption in range.** In 2007–2013, big
  defenses do better than forecast, not worse. The assumption that rim
  protection saturates at two inside defenders is wrong for the three-big
  lineups that were actually played. Nothing here measures four or five bigs.
- **For five centers, the defensive side needs care.** The data do not show
  big defenses collapsing, so "five centers fail" cannot rest on defense
  alone. It can rest on the offense: no handler and no spacing.
