# Proposal: a big-lineup era backtest (2006–2013) — 2026-10-09

**Status: proposal.** It needs Adam's approval, because it runs longer than
six hours.

## Why

The weird-lineup failure sits where 2016–2026 has no data. Lineups with three
or more bigs (6'10"+) on defense were 3–6% of possessions in 2002–2014 and
0.1–1.4% in 2017–2025:

| Seasons | Three-big defensive possessions per season | Share |
| --- | ---: | ---: |
| 2002–2004 | 14–15k | 6.2% |
| 2005–2013 | 6–11k | 2.6–4.7% |
| 2017–2025 | 0.1–3.6k | 0.1–1.4% |

A forward backtest in that era gives real outcomes for the lineup shapes
where the reference and the capacity-law model disagree. It is the closest
thing to validating pillar 2 with data. It also tests cross-era use, which
the tool promises.

## Design

- **Origins.** 2006q1–2013q4, 32 quarters. 2006 is warmup for calibration.
  Every input is built for these origins with the ported pipeline:
  - schedule;
  - the three state sweeps;
  - normalizers and environment.
- **Capability library.** Monthly snapshots from 2001-11 to 2009-02, from the
  legacy chain code (`scripts/library_extend.py`, generalized). The existing
  library starts 2009-03.
- **Arms.** R (broadcast defense) and C (CapacityDefense version 2), both
  trained two-phase with self-references. These are the training and arms of
  the prospective test.
- **Control.** additive_defense per origin (`scripts/additive_origin_fit.py`
  plus `lineups.additive`). Its calibration cohort rules would need porting,
  or the cohort redefined.
- **Primary contrasts, frozen before the run:**
  1. **Residual bias on real big lineups.** Actual minus forecast on rows
     whose defense has three or more bigs, C vs R, paired, with season-level
     SEs.
     - About 60k such possessions fall in the 2007–2013 outer quarters, so
       each model's bias has an SE of about 0.45 points per 100. The paired
       difference should be tighter.
     - The question: does the capacity law forecast real big defenses better
       or worse than broadcast pooling?
  2. **Non-inferiority on all lineups.** Half r², C vs R, margin −0.003, as
     in the 2016–2026 confirmatory run.
- **Secondary:**
  - the property suite and fixtures at era origins;
  - the five-center margin with era-trained models.

## Cost (CPU only, this machine has 10 cores)

| Step | CPU-hours | Wall time at 8 workers |
| --- | ---: | ---: |
| Library, 2001-11 → 2009-02 (about 88 dates × 8 chains, plus 8 annual tunings) | about 35 | about 4.5 h |
| Fits, 2 arms × 32 origins × 1 seed (about 20 min each) | about 21 | about 2.7 h |
| Fits, 3 seeds instead | about 64 | about 8 h |
| Additive fits (32 × 8 min) | about 4 | about 0.5 h |

- **One seed:** about 8 hours of wall time.
- **Three seeds:** about 13 hours.
- **Rented 64-core CPU box:** about 2 hours for either, but it costs money,
  which also needs approval.

## Risks

- **Era drift in the inputs** (checked 2026-10-12, player-game table).
  - Every field the state sweeps read is present from 2002:
    - made and missed shots by type, free throws, turnovers, assists and
      rebounds;
    - assisted makes;
    - steals, blocks and fouls committed.
  - Their rates drift smoothly with known era trends. Shot locations are
    recorded for 100% of attempts in every season.
  - Two gaps fall in fields no input reads: fouls drawn are missing before
    2006, and shot distance covers 75% of attempts before 2011 (96% after).
- **Early origins have shorter histories.** Data start 2001-10-30, so the
  2006 origins see 4.3 years instead of 5.
- **One seed.** That bounds the model-to-model comparison, not era-level
  uncertainty. Season-level SEs come from 7 scored seasons.
