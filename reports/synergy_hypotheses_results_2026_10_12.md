# Synergy hypotheses: results — 2026-10-12

Results of the [protocol](synergy_hypotheses_protocol_2026_10_12.md), which
was committed (2320349f) before any outcome was looked at.

- Script: `scripts/synergy_hypotheses.py`.
- Output: `experiments/cache/synergy_hypotheses_2026_10_12/` (`report.txt`,
  `result.json`).

These tests are exploratory.

**Residual.** Actual points per 100 minus the best additive approximation of
the forward forecast, centered within quarter and possession-weighted, on all
game × five × five rows.
- Primary: 2016–2026, 11 seasons.
- Replication: 2007–2013, 7 seasons.

## Verdicts

| | Hypothesis | Primary interaction (points per 100) | Seasons in predicted direction | Holm p | Replication | Verdict |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| H1 | Small guards need an anchor | −0.66 ± 0.19 per small defender | 9/11 | .028 | +0.24 ± 0.21 (2/7) | **Suggestive.** Strong in the modern era; does not replicate |
| H2 | Shooters need a playmaker | +0.05 ± 0.18 | 5/11 | 1 | +0.20 ± 0.45 | No evidence |
| H3 | Transition finishers need steal pressure | −0.00 ± 0.10 | 8/11 | 1 | −0.06 ± 0.11 | No evidence |
| H4 | Two ball-dominant creators clash | +0.27 ± 0.25 (wrong sign) | 4/11 | 1 | −0.34 ± 0.28 (6/7) | No evidence |
| H5 | A rim runner needs shooters | +0.07 ± 0.15 | 4/11 | 1 | +0.28 ± 0.24 | No evidence |

Estimates are season means ± season SE.

## H1 in detail: points allowed compared with the additive baseline

| Small defenders (6'3" or shorter) | 2016–2026, no anchor | 2016–2026, with anchor | 2007–2013, no anchor | 2007–2013, with anchor |
| --- | ---: | ---: | ---: | ---: |
| 0 | −0.04 | −0.06 | +0.63 | −0.54 |
| 1 | +0.12 | −0.30 | −0.06 | −0.48 |
| 2 or more | **+0.82** | **−0.33** | **+1.22** | **+0.80** |

- **2016–2026.** Two small guards without a rim anchor allow 0.8 more points
  per 100 than their individual values imply. With an anchor they allow 0.3
  fewer: a swing of about 1.1. This is Adam's pattern, and it holds in 9 of 11
  seasons.
- **2007–2013.**
  - Two small guards are costly with or without an anchor (+1.2 and +0.8).
  - An anchor helps at every guard count. That matches the era backtest:
    big defenses beat their forecast in that era.
- The interaction is therefore strong in the modern, switch-heavy league and
  absent in the earlier one. It may be an era effect: rim anchors protect
  small guards when the floor is spread.

## What the other tests show

- **H2.** Lineups with a top-10% passer beat the additive baseline by about
  0.4–0.7 points per 100, whatever the number of shooters. Playmakers help
  everyone about equally, which is an additive undervaluation of passers, not
  a synergy with shooters.
- **H3.**
  - Possessions right after a steal yield 0.18 more points than others.
  - The data-defined transition finishers include Mikal Bridges and Tyrese
    Maxey (top 15 in 2024).
  - Finishers convert those possessions slightly better: +0.008 points per
    post-steal possession per finisher, under 0.1 points per 100 overall.
  - Steal pressure does not raise the lineup's offense more when finishers
    are present.

  | Finishers in the five | Post-steal possessions | Post-steal points per possession | Other | Lift |
  | ---: | ---: | ---: | ---: | ---: |
  | 0 | 113,433 | 1.286 | 1.108 | 0.178 |
  | 1 | 79,929 | 1.301 | 1.115 | 0.186 |
  | 2+ | 18,574 | 1.322 | 1.128 | 0.194 |

- **H4.** No clash. In 2016–2026, two ball-dominant creators slightly beat the
  baseline. In 2007–2013 they slightly trail it.
- **H5.** Shooters help with or without a rim runner, again an additive
  effect. Each extra shooter beats the baseline by about 0.4 points per 100,
  which says the forecast slightly undervalues shooting.

## Reading

- **One of five hypotheses shows an interaction of a size that matters.**
  Small guards with a rim anchor are worth about 1 point per 100 in
  2016–2026, against an outcome noise of about 10 per lineup-quarter. It does
  not replicate in 2007–2013, so it is not a law of basketball. It is a
  candidate modern-era effect.
- **The other effects are additive.** Passers, shooters and anchors are worth
  a little more than the forecast credits, on their own and not through
  combinations.
- **The limits declared in the protocol still apply.**
  - Profiles are measured in each player's actual context, which biases the
    tests toward finding no synergy.
  - Deployment selection can mix with any interaction.
- **For the model.** H1 is a concrete candidate for a named, labeled
  defensive interaction: small defenders' cost depending on rim protection.
  Under the rules of evidence, it should first be pre-registered as a
  forward test on 2026–27 games, or on held-out seasons, before it enters the
  forecast.
