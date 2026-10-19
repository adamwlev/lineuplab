# v16 runtime optimization, second candidate — 2026-09-19

Extends the [first protocol](joint_capability_v16_speed_protocol.md), without
changing its files, evidence or tolerances. First candidate proved exact RAW
full-trajectory equivalence and sped warmed RAW 2.49×, BOTH 1.28×, but ALL_BOTH
only 1.04×. The full campaign remains stopped.

The ALL_BOTH profiler attributed 2.16 of 5.97 seconds across eight steps to
variance operations, and 2.70 seconds to the enclosing moments functions.
These include repeated summaries of immutable inputs in allocation/phase
heads, not learned attention projections.

Candidate 2 memoizes exact team moments for these heads and constructs their
shared other-four context once per forward pass. The action allocator still
recomputes every learned or action-dependent quantity for each phase. No
gradient through a learned projection is removed. Static context is not a
predicted outcome and includes no future information.

Memory is deliberately bounded: two additional per-row team summaries (386
float32 coordinates at most), not the full five-player concatenated context.
Combined persistent per-row memo is at most 2448 bytes (~0.75GB for 300k rows).
Allocate only for arms that consume it; RAW/BOTH without allocation/separate
phases retain the first candidate's execution path.

Acceptance: same predeclared point/loss/gradient/state tolerances as candidate1;
44 all-arm early/late full-game-sized six-step comparisons, all 22-arm synthetic
source/schema checks, trained-parameter and reordered-row checks; alternating
original/candidate2 warmed timings for RAW/BOTH/ALL_BOTH. Candidate1's full RAW
pilot is reusable only with explicit RAW path and trainer source-parity tests.
Do not claim a full-stopping ALL_BOTH replay unless actually run. Preserve
original 95 tests, measured RAM plus 1GiB per-worker headroom and 2GiB system
headroom, three workers only if under physical16GiB; storage check unchanged.

New code lives under `v16_fast2_*` and `v16_speed2_*`; candidate1 and originals
remain available. Same scientific protocol and postprocessing. No full relaunch
until acceptance and Adam's authorization; no commits.
