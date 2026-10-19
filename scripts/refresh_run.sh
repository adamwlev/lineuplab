#!/bin/zsh
# The refresh's fits on the clean data, two at a time on this laptop (Adam, 2026-10-16: "refresh all the components
# that produce numbers for the tool"; "Laptop, 2 cores").
#
#   nohup caffeinate -i scripts/refresh_run.sh > /dev/null 2>&1 &
#
# Order (each produces tool numbers; the most consequential first):
# 1. history R, seeds 17, 23, 41, origins 2015q1-2026q4: the forecast's calibration, the band's tau, the
#    benchmark, the network-vs-linear rows (discovery, layer) and the learned module's checks;
# 2. history C, same: the band's alternative arm's calibration;
# 3. era R, seeds 17, 23, 41, origins 2006q1-2013q4: the band's cross-era term and the discovery replication.
# Each fit is scripts/era_run.py; a finished case is skipped, so a rerun resumes.
# Progress: <clean root>/logs/refresh_run.log; one log per fit in <clean root>/logs/refresh/.
set -uo pipefail
REPO=${0:A:h:h}
cd $REPO
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
CLEAN=${LINEUPS_CLEAN:-$REPO/experiments/cache/rebuild_pages_2026_10_14/experiments/cache}
SLOTS=${SLOTS:-2}
LOG=$CLEAN/logs/refresh_run.log
mkdir -p $CLEAN/logs/refresh
export PYTHONPATH=$REPO LINEUPS_CACHE=$CLEAN OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
       VECLIB_MAXIMUM_THREADS=1
say() { echo "$(date '+%F %T') $*" >> $LOG; }

cases() {                                   # campaign tag arm seed, in priority order, unfinished only
  local campaign=$1 arm=$2
  $PY scripts/era_run.py --campaign $campaign --cases | awk -v arm=$arm -v c=$campaign '$2 == arm {print c, $1, $2, $3}'
}
if [[ ${1:-} == --fit ]]; then              # one fit (xargs calls this): campaign tag arm seed
  shift
  log=$CLEAN/logs/refresh/$1_$2_$3_s$4.log
  say "start $*"
  if nice -n 10 $PY -u scripts/era_run.py --campaign $1 --origin $2 --arm $3 --seed $4 >> $log 2>&1; then
    say "done $*"
  else
    say "FAILED $* (see $log)"
  fi
  exit 0
fi
say "start: $SLOTS slots"
{ cases history R; cases history C; cases era R; } > $CLEAN/logs/refresh/queue.txt
say "queue: $(wc -l < $CLEAN/logs/refresh/queue.txt | tr -d ' ') fits"
# xargs holds the slots. (The first launch counted `jobs` inside $(...), a subshell with no jobs, so it started
# every fit at once and the laptop rebooted: logs/refresh_crashed_2026_10_16.)
xargs -P $SLOTS -L 1 ${0:A} --fit < $CLEAN/logs/refresh/queue.txt
say "ALL FITS DONE"
