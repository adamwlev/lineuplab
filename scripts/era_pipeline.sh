#!/usr/bin/env bash
# Era backtest 2006-2013, every stage in order (protocol: reports/era_backtest_protocol_2026_10_12.md).
#
# Run from a worktree pinned at the protocol commit, with experiments/cache linked to the main tree's cache
# and the legacy worktree at ../basketball-legacy:
#   nohup bash scripts/era_pipeline.sh >> experiments/cache/era_backtest_2026_10_12/pipeline.log 2>&1 &
# Every stage resumes: rerunning the script skips finished work.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LEGACY="$(dirname "$ROOT")/basketball-legacy"
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
CACHE="$ROOT/experiments/cache"
ERA="$CACHE/capability_library_era_extension"
RUN="$CACHE/era_backtest_2026_10_12"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p "$RUN" "$ERA/logs"
cd "$ROOT"
say() { echo "[$(date '+%F %T')] $*"; }
complete_snapshots() { find "$ERA/chains" -path '*/snapshots/*/complete.json' 2>/dev/null | wc -l | tr -d ' '; }

# 1. Library: 8 chains x 87 monthly snapshots (2001-12 .. 2009-02).
say "library: $(complete_snapshots)/696 snapshots"
while [ "$(complete_snapshots)" -lt 696 ]; do
  if pgrep -f "library_extend.py --era" > /dev/null; then
    sleep 120
  else
    say "library incomplete with no chain running: (re)launching the 14 tasks"
    (cd "$LEGACY" && PYTHONPATH=. xargs -P 10 -L 1 sh -c \
      "$PY -u $ROOT/scripts/library_extend.py --era --bank \$0 --family \$1 --segment \$2 >> $ERA/logs/\$0_\$1_\$(echo \$2 | tr / -).log 2>&1" \
      < "$ERA/tasks.txt")
    if [ "$(complete_snapshots)" -lt 696 ]; then say "library still incomplete after a relaunch; stopping"; exit 1; fi
  fi
done
say "library complete"

# 2. Store.
if [ ! -f "$CACHE/lineups_store_era/manifest.json" ]; then
  say "building lineups_store_era"
  PYTHONPATH=".:$LEGACY" $PY -u scripts/build_era_store.py >> "$RUN/build_store.log" 2>&1 || { say "store build failed"; exit 1; }
fi
say "store ready"

# 3-4. Fits seed by seed (9 at a time), scoring after each seed.
for SEED in 17 23 41; do
  say "fits for seed $SEED"
  PYTHONPATH=. $PY scripts/era_run.py --cases | awk -v s=$SEED '$3 == s' | \
    PYTHONPATH=. xargs -P 9 -L 1 sh -c "$PY -u scripts/era_run.py --origin \$0 --arm \$1 --seed \$2 >> $RUN/fit_\$0_\$1_s\$2.log 2>&1"
  missing=$(PYTHONPATH=. $PY scripts/era_run.py --cases | awk -v s=$SEED '$3 == s' | wc -l | tr -d ' ')
  say "seed $SEED done; $missing cases missing"
  if [ "$missing" = "0" ]; then
    PYTHONPATH=. $PY -u scripts/era_score.py > "$RUN/score_through_s$SEED.log" 2>&1 \
      && cp "$RUN/score/result.json" "$RUN/score/result_through_s$SEED.json" \
      && say "scored through seed $SEED" || say "scoring failed through seed $SEED"
  fi
done
say "pipeline finished"
