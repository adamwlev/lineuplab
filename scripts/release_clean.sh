#!/bin/zsh
# The release on the clean data, after scripts/after_download.sh (2026-10-15): retrain, record, modules,
# overall quality, export, comparison and tests. Each step skips work already done.
#
#   nohup scripts/release_clean.sh > /dev/null 2>&1 &          # paths.CLEAN (the rebuild root)
#   LINEUPS_CLEAN=DIR scripts/release_clean.sh                   # a rehearsal root
#
# 1. fits: scripts/prospective_fit.py, arms R and C, seeds 17/23/41, in parallel, on the root's 2027q1 store
#    and matchups (LINEUPS_CACHE at the root; the frozen record's fits are never touched);
# 2. record: scripts/release_record.py (calibration and league carried from the frozen record);
# 3. modules: scripts/release_module.py, three seeds in parallel (LINEUPS_RELEASE=clean);
# 4. overall quality: scripts/player_values.py;
# 5. export: scripts/export_release.py and the page (tool/build_lineups.py), then the parity and release tests;
# 6. comparison with the release on 2026-10-14's data: scripts/compare_releases.py.
# The tool's default (lineups.sources.DATA) is switched to clean by hand after reading the comparison.
set -euo pipefail
REPO=${0:A:h:h}
cd $REPO
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
CLEAN=${LINEUPS_CLEAN:-$REPO/experiments/cache/rebuild_pages_2026_10_14/experiments/cache}
LOG=${LOG:-$CLEAN/release_clean.log}
mkdir -p $CLEAN/logs
say() { echo "$(date '+%F %T') $*" >> $LOG; }
stop() { say "STOPPED: $*"; exit 1; }
waitall() { local p f=0; for p in $@; do wait $p || f=1; done; (( f == 0 )); }
export PYTHONPATH=$REPO OMP_NUM_THREADS=1

say "fits"
pids=()
for arm in R C; do for seed in 17 23 41; do
  ( LINEUPS_CACHE=$CLEAN $PY -u scripts/prospective_fit.py --arm $arm --seed $seed >> $CLEAN/logs/fit_${arm}_s${seed}.log 2>&1 ) &
  pids+=($!)
done; done
waitall $pids || stop "a fit failed (see $CLEAN/logs/fit_*.log)"
say "record"
LINEUPS_CACHE=$CLEAN $PY -u scripts/release_record.py > $CLEAN/logs/release_record.log 2>&1 || stop "record failed"

export LINEUPS_CLEAN=$CLEAN LINEUPS_RELEASE=clean
say "modules"
pids=()
for seed in 17 23 41; do
  ( $PY -u scripts/release_module.py --seed $seed > $CLEAN/logs/module_s$seed.log 2>&1 ) & pids+=($!)
done
waitall $pids || stop "a module failed (see $CLEAN/logs/module_s*.log)"
say "overall quality"
[[ -e $CLEAN/player_values/values.npz ]] || $PY -u scripts/player_values.py > $CLEAN/logs/player_values.log 2>&1 \
  || stop "player values failed"
say "export"
$PY -u scripts/export_release.py > $CLEAN/logs/export.log 2>&1 || stop "export failed"
$PY -u tool/build_lineups.py >> $CLEAN/logs/export.log 2>&1 || stop "page build failed"
say "tests"
$PY -m unittest tests.test_tool_parity tests.test_release tests.test_players tests.test_learned tests.test_band \
    tests.test_explain > $CLEAN/logs/tests.log 2>&1 || stop "tests failed (see $CLEAN/logs/tests.log)"
say "comparison"
unset LINEUPS_RELEASE
$PY -u scripts/compare_releases.py --new-root $CLEAN > $CLEAN/logs/compare.log 2>&1 || stop "comparison failed"
say "ALL DONE: read $CLEAN/logs/compare.log, then set lineups.sources.DATA = clean and republish"
