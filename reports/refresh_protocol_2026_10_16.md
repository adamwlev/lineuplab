# Refreshing the tool's numbers on the clean data: protocol (2026-10-16)

Adam (2026-10-16): "go ahead and refresh all the components that produce
numbers for the tool"; compute: "Laptop, 2 cores". Committed before any
refreshed result exists.

## Why

The clean release (reports/clean_release_2026_10_16.md) retrained the
2027q1 fits on the rebuilt data but carried everything that comes from the
2015–2026 history: the calibration, the band's width, the combination
layer, the learned module's check and the scorecard. Those still rest on
fits trained on the old data. This refresh reruns each of them on the clean
data with its registered method.

## What the tool prints, and where it comes from

| Tool number | Producer | Needs |
| --- | --- | --- |
| Calibration, arms R and C, per seed | prior-only affine on 2015–2026 history cells (as `scripts/prospective_freeze.py`) | history R and C |
| Band τ (offense, defense, margin) | `scripts/band_in_support.py` | benchmark rows (`scripts/ensemble_check.py`) |
| Band cross-era variance and correlation | `scripts/cross_era.py` | release fits, era R fits, history R |
| The 14 measured combination effects and their evidence | `scripts/interaction_discovery.py` (+ `_posthoc`), `scripts/combination_layer.py` | network-vs-linear rows (`scripts/nn_vs_linear.py`), era rows (`scripts/era_diagnostics.py`), module rows |
| Learned module at half strength, and its check | `scripts/nonlinearity_screen.py` (`frozen_fixed`), the 2026-10-14 confirmation protocol | history R fits |
| Overall quality | `scripts/player_values.py` | the recalibrated release |
| Scorecard and model-page accuracy lines | the benchmark, the module check, the layer's forward check | all of the above |

The league level in every calibration is the dated league average of the
matchups (`era_score.league_at`); on the old data it equals the saved
controls' league to six decimals at every origin checked. The additive
ridge control (legacy code) only feeds the printed "additive half" trade.
It is refitted last, if time allows, and that line is labeled until then.

## Fits

All on the clean root (`LINEUPS_CACHE = paths.CLEAN`); nothing in the main
cache is written. Two at a time, niced, one thread each
(`scripts/refresh_run.sh`), run from a worktree pinned at commit eb9c97ae (each fit also saves its loss references, for the modules) so
that later code edits cannot reach the fits.

1. **History R:** origins 2015q1–2026q4, seeds 17, 23 and 41
   (`scripts/era_run.py --campaign history`). This is two-phase from scratch,
   exactly the 2027q1 release protocol, on the clean `lineups_store_v16`
   with the five-year lookback. It replaces the saved v16 reference, which was
   warm-started from v14 parents trained on the old data.
2. **History C:** the same for capacity v2.
3. **Era R:** origins 2006q1–2013q4, seeds 17, 23 and 41, on the clean
   `lineups_store_era`. Era C is fitted only if a producer above needs it.
4. **Learned modules:** the confirmed `frozen_fixed` design on each history
   R fit (3 seeds). Each must reproduce its base fit's saved forecast before
   the module trains.

## Fixed in advance

- **Code changes are ports, not redesigns.** One module serves the history
  for the active cache root: the saved v16 reference under the main cache,
  the refresh under the clean root. Under the main cache, each ported
  producer must reproduce its saved output exactly before it runs on the
  clean root.
- **Calibration:** replaces the carried constants in the release record.
- **τ and cross-era terms:** computed by the same scripts. The input rule
  stays era-relative (Adam, 2026-10-12); only the constants change.
- **Discovery:** the registered protocol unchanged: discover on 2016–2021
  (BH, q = .10), confirm the top five per family on 2022–2026 (one-sided,
  Holm), replicate on 2007–2013. The layer holds whatever survives on the
  clean data, which may differ from the 14.
- **Learned module:** the 2026-10-14 confirmation protocol unchanged
  (24 scored quarters 2016–2021, three seeds, the same bars). If it passes,
  half strength stays. If it fails, I report to Adam before the release
  changes; the review copy keeps the current release until he decides.
- **Layer:** the combination-layer protocol, re-measured on top of the
  refreshed module.
- **Release:** a new record with the refreshed calibration, then modules,
  overall quality, export, tests and an old-vs-new comparison, as
  `scripts/release_clean.sh`. The tool's default switches only after that
  comparison is read.
- **Reported, not gated:** each refreshed constant next to its old value.

## Order and time

The first fits took about 14 s an epoch, roughly 15–20 minutes a fit. On two
slots, history R takes about 20 h, history C another 20 h and era R about
12 h. Ports and their main-cache reproductions are written while the fits
run. Producers that need only history R run as soon as it finishes.

## Incident before this protocol

The first launch of the fit queue (09:57) started all 384 fits at once: the
slot limiter counted shell jobs inside a subshell. The laptop rebooted at
10:27 and no fit completed. The queue now uses `xargs -P 2`, tested with
dummy jobs and checked live. Logs of that attempt are kept in
`logs/refresh_crashed_2026_10_16/` under the clean root.
