# The refresh of every tool number on the clean data: results (2026-10-19)

Protocol, committed before any result:
[refresh_protocol_2026_10_16.md](refresh_protocol_2026_10_16.md). Adam
(2026-10-16): "go ahead and refresh all the components that produce numbers
for the tool"; compute: "Laptop, 2 cores".

## What ran

- **Fits:** 384, two at a time, from 2026-10-16 14:27 to 2026-10-18 17:35, about 17
  minutes each, none failed. They were history R and history C (2015q1–2026q4 × seeds 17,
  23, 41, two-phase from scratch on the clean store) and era R (2006q1–2013q4 × 3 seeds).
- **Downstream** (`scripts/refresh_downstream.sh`), from 2026-10-18 17:39 to 2026-10-19
  00:11: the learned modules and their confirmation, the benchmark and discovery rows,
  discovery, the layer, the band, the release record, cross-era, the band's constants, and
  the release as the source `refresh`.
- **Stops:** it stopped seven times. Each cause was fixed, committed and relaunched from the
  step that stopped, with partial outputs moved to `logs/refresh_failed_2026_10_18/`:

  | # | Cause |
  | ---: | --- |
  | 1 | zsh sets `$0` to a function's name, so the module queue's self-call failed silently |
  | 2 | the fixture registry was read under the clean root |
  | 3 | the confirmation's summaries were scheduled before discovery |
  | 4 | the benchmark expected arm C in the era rows, which hold arm R alone |
  | 5 | the layer's fixed effect list didn't match the clean discovery (a real result, below) |
  | 6 | the layer's forward check couldn't handle an event family with no effect |
  | 7 | a band test hard-coded the old τ |

  Stops 1–4 and 6 were paths the main-cache reproductions never ran
  (memory: run every step once on the smallest input first).

## Results, clean data against the earlier fits

| Component | Refresh (clean data) | Before (earlier data) |
| --- | --- | --- |
| Calibration, arm R, seeds 17 / 23 / 41 | intercept 0.82 / 1.04 / 0.80, slope 0.81 / 0.76 / 0.81 | 0.88 / 0.83 / 0.91, 0.80 / 0.79 / 0.78 |
| League level (2027q1) | 115.844 | 115.831 |
| Benchmark, calibrated network R, 44 quarters 2016–26 | r² 0.1594 raw, 0.0988 centered | 0.1615, 0.1012 |
| Era rows 2007–13, R | r² 0.1482 raw, 0.1368 centered | (not comparable) |
| Learned module, half strength, previous-centered, 24 quarters 2016–21 | **+0.0006 (SE 0.0010)**, 12/24 positive | +0.0010 |
| Learned module, full strength | −0.0007 (SE 0.0020) | +0.0001 |
| Module fixture bars (five Goberts, legal centers, Jokić/Westbrook) | all pass at s = 0.5 and 1 | all pass |
| Measured combinations held up | **12** | 14 |
| Layer forward check (2016–21 fit, 2022–26 rows) | +0.00001 raw | +0.00003 |
| τ² offense / defense / net | 10.43 / 10.04 / 19.80 | 10.25 / 10.45 / 19.83 |
| Cross-era variance (relative / as played) | 4.51 / 5.24 | 4.0 / 5.3 |
| Cross-era correlation (relative / as played) | 0.857 / 0.855 | 0.878 / 0.844 |

- **The benchmark is about 0.002 lower.** It isn't like for like: the outcome data changed
  (the rebuilt possession table) and so did the training protocol (from scratch rather than
  warm-started from v14 parents).
- **The learned module passes** the 2026-10-14 confirmation protocol. On the bar of −0.003,
  full strength would pass too; the protocol keeps half strength, Adam's decision of 2026-10-14.
- **Measured combinations.** Discovery under the registered protocol, unchanged, kept 12:
  - **dropped:** the three turnover effects. Shooters beside self-creators and slashers beside
    high-usage players miss the Holm bar at 0.063 (4/5 and 3/5 seasons); non-shooters beside
    offensive rebounders no longer passes discovery;
  - **added:** bigs beside defensive rebounders (rim share): confirmation +0.41 (0.10),
    Holm < 0.001, 4/5 seasons, the same sign in 2007–13;
  - **the joint fit:** the new effect is carried by its neighbours (−0.11, SE 0.13), like
    bigs beside shot-blockers and small players beside self-creators. Offensive rebounders
    together fits at about zero (−0.02, SE 0.24; before +0.18, SE 0.25).

  The protocol keeps whatever survives, so `lineups.combinations.EFFECTS` is the clean list
  for the refresh.

## The comparison and the switch

`scripts/compare_releases.py --old-source clean --new-source refresh` on 120 real 2025–26
fives (calibrated network, each against its league-average panel):

| | Mean change | SD of change | Largest | Correlation |
| --- | ---: | ---: | ---: | ---: |
| Offense | +0.007 | 0.021 | 0.05 | 1.00 |
| Points allowed | +0.013 | 0.022 | 0.06 | 1.00 |
| Net | −0.006 | 0.037 | 0.09 | 1.00 |

The calibration's refit moves real lineups by hundredths of a point. The measured layer, with
12 effects instead of 14, moves its pairings by up to about half a point. The release tests
(31) and the full suite (124) pass.

**The tool's default is the refresh** (`lineups.sources.DATA`, commit f0daea7f). The review
copy is version 11. The model page now carries the refreshed numbers; nothing in it is
"carried" or "not re-scored" any more.

## Not refreshed

- The additive ridge control. It feeds only the printed "straight-line half" trade
  (−0.0015), which stays labelled as earlier data.
- The release fits' learned module, which keeps its 2026-10-16 training on the clean
  release fits.

## Addendum, 2026-10-19 (evening): the ports, moved here from STATUS

Before the refresh ran on the clean data, each producer was ported to read the active cache
root. `lineups/history.py` serves the 2015–2026 history of that root: the v16 reference under
the main cache, and the refits under the clean root. `paths.CLEAN_ROOT` picks the possession
table. Each ported producer first reproduced its saved output under the main cache:

- calibration to 2e-13;
- the benchmark to 3e-13;
- the network-vs-linear rows and the learned module exactly;
- the band's constants to their rounding.

The launch incident of 2026-10-16 (all 384 fits started at once, and the laptop rebooted) is in
the [protocol](refresh_protocol_2026_10_16.md).
