# v18 engineering runtime refinement — 2026-09-28

This replaces planning multipliers with measurements, as §9 of the frozen plan
requires. No scientific arm, loss, stopping rule, seed, population or comparison
changes. Completed micro/pilot/benchmark/engineering producers are preserved.

Seven full inner/final pilots completed with three workers in17.17 wall minutes.
Selected final lengths were7 epochs except A_SELECT/A_ACCOUNT at9. None hit cap.
Fourteen12-batch input/routing micros passed in53.52seconds. A separately
versioned fast gate computes the same equations with bank-wise matrix reductions;
selective defensive moments reuse fixed masked summaries. Same parameters and
state_dict. The fourteen paired12-step optimizer checks passed, with maximum
forecast difference0.00003483pts/100. Slower early/late measured gate ratios are
.8702/.8679 and A_SELECT.8351. All other measured ratios, including slowdowns,
remain in projections rather than assuming free speedups.

The end-to-end single-origin analysis pilot took84.66seconds, including tests,
48 exactly reproduced archived control views, scoring, three concurrent derived
workers and summary. Worker wall durations: average62.42s, role15.55s, U0/U1
7.18s; summary5.55s. It exported all required native player predictions directly
from saved NPZs; no control player inference was necessary. J_ACTION_BOTH average
opponent integration remains budgeted because compatible exports do not exist.

The first readiness estimate retained the initial **4-hour analysis allowance**
even after measuring analysis. The measured refinement is:

- Average:62.42s ×48 origins ×(3 seeds ×8 newly integrated arms /11 pilot arms)
  /3 workers ×1.5 late-size/overhead allowance ≈.908h.
- Roles:15.55s ×48 /3 ×1.5 ≈.104h.
- Add1.5h for chronological scoring, full-history U1, fixtures, summaries,
  independent integrity/metric review and handoff. The cold U1 pilot is NOT
  extrapolated as the cost of a fitted full-history U1.
- Total downstream reference ≈2.512h. The extra1.5h is informed by v17's full
  uncertainty366.70s, summary123.95s, basketball32.62s, handoff.67s, plus scoring
  and integrity allowance. v18 has24 uncertainty models versus16 in v17.

Keep the old4-hour allowance scenario in the final budget output, not hide it.
With measured kernels, reference training is about42.18h; 20% longer training
plus the measured downstream estimate remains under54h. The original4-hour
analysis allowance plus20% longer training exceeds54h slightly. Neither scenario
is a confidence bound or guarantee; report slippage, do not truncate fits.

The ready adapter performs these measured estimates without modifying the
already fingerprinted v18_run/preflight producers. It preserves the same full
runner/workers and adds itself and this note to production hashes. Production
still requires explicit user launch. Physical storage is checked independently
against actual archived full-schedule sizes, pilot size ratios and10GiB reserve.
