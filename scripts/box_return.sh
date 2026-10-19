#!/bin/zsh
# Bring the capability library back from the rented box and finish the clean release here (2026-10-15).
#
#   nohup scripts/box_return.sh HOST KEYFILE > /dev/null 2>&1 &
#
# 1. wait until the box's run (scripts/box_run.sh) logs ALL DONE (stop if it logs STOPPED);
# 2. copy back the library chains and the era and 2027q1 extensions into the clean rebuild root;
# 3. check that every chain has its receipt;
# 4. stores and player seasons (scripts/after_download.sh - stores), then the release (scripts/release_clean.sh).
# The key is used by path only. Progress: experiments/cache/rescrape_2026_10_14/box_return.log
set -euo pipefail
HOST=$1; KEY=$2; WATCH=${3:-finish.log}   # the box log that reports ALL DONE (run.log or finish.log)
REPO=${0:A:h:h}
cd $REPO
LOG=$REPO/experiments/cache/rescrape_2026_10_14/box_return.log
C=$REPO/experiments/cache/rebuild_pages_2026_10_14/experiments/cache
REMOTE=/home/ubuntu/box_2026_10_15
SSH=(ssh -i $KEY -o BatchMode=yes -o ServerAliveInterval=60)
say() { echo "$(date '+%F %T') $*" >> $LOG; }
stop() { say "STOPPED: $*"; exit 1; }

say "waiting for the box ($HOST)"
while true; do
  state=$($SSH ubuntu@$HOST "grep -o -e 'ALL DONE' -e 'STOPPED.*' $REMOTE/logs/$WATCH | tail -1" 2>/dev/null || echo unreachable)
  [[ $state == "ALL DONE" ]] && break
  [[ $state == STOPPED* ]] && stop "box: $state"
  sleep 600
done
say "box done; copying back"
LIB=joint_capability_2026_09_18_v16_library_full1
rsync -a -e "${SSH[*]}" ubuntu@$HOST:$REMOTE/experiments/cache/$LIB/chains/ $C/$LIB/chains/ || stop "copy of the chains failed"
for d in capability_library_era_extension capability_library_2027q1_extension; do
  rsync -a -e "${SSH[*]}" ubuntu@$HOST:$REMOTE/experiments/cache/$d/ $C/$d/ || stop "copy of $d failed"
done
rsync -a -e "${SSH[*]}" ubuntu@$HOST:$REMOTE/logs/ $REPO/experiments/cache/rescrape_2026_10_14/box_logs/ || true
for bank in offense defense; do for fam in counts location conversion recovery; do
  [[ -f $C/$LIB/chains/$bank/$fam/complete.json ]] || stop "chain $bank/$fam has no receipt"
done; done
say "copied; stores"
scripts/after_download.sh - stores || stop "stores failed (see after_download.log)"
say "release"
scripts/release_clean.sh || stop "release failed (see $C/release_clean.log)"
say "ALL DONE: read $C/logs/compare.log, then set lineups.sources.DATA = clean and republish"
