#!/bin/bash
# Finish the capability library and its extensions on a rented box (scripts/box_bundle.sh; 2026-10-15).
#
#   tar -xf box_2026_10_15.tar && cd box_2026_10_15
#   python3.13 -m venv .venv && .venv/bin/pip install -r requirements.txt
#   nohup ./box_run.sh > run.log 2>&1 &
#   ./box_run.sh finish     # when blocks were (re)started by hand: wait for every block, then steps 1b and 2;
#                           # logs to logs/finish.log
#
# 1. every library chain in season-aligned blocks (scripts/library_blocks.py), finished snapshots skipped,
#    as many processes as CORES allows; then the legacy chain command verifies each chain and writes its receipt;
# 2. the era and 2027q1 extensions (scripts/library_extend.py), era chains in segments.
# Bring back: experiments/cache/joint_capability_2026_09_18_v16_library_full1/chains,
#             experiments/cache/capability_library_{era,2027q1}_extension.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-.venv/bin/python}
CORES=${CORES:-$(nproc)}
export PYTHONPATH=$PWD:$PWD/scripts OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
       VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 PYTHONHASHSEED=160918
LIB=experiments/cache/joint_capability_2026_09_18_v16_library_full1
mkdir -p logs
RUNLOG=logs/run.log; [[ ${1:-} == finish ]] && RUNLOG=logs/finish.log
say() { echo "$(date '+%F %T') $*" | tee -a $RUNLOG; }
waitall() { local f=0; for p in "$@"; do wait "$p" || f=1; done; return $f; }
# Blocks per family: location carries most of the work (about 4 CPU-minutes a snapshot), counts and
# conversion about a fifth of it, recovery little. A chain has at most one block per season (18).
if [[ ${1:-} == finish ]]; then
  say "waiting for the running blocks"
  while pgrep -f "[l]ibrary_blocks.py" > /dev/null; do sleep 60; done
  grep -l Traceback logs/block_*.log > /dev/null 2>&1 && { say "STOPPED: a block failed (logs/block_*)"; exit 1; }
else
LOC=${LOC:-$(( CORES * 6 / 10 / 2 ))}; OTHER=${OTHER:-$(( CORES * 4 / 10 / 4 ))}   # LOC, OTHER: blocks per chain
(( LOC < 1 )) && LOC=1; (( LOC > 18 )) && LOC=18; (( OTHER < 1 )) && OTHER=1; (( OTHER > 18 )) && OTHER=18
declare -A N=([location]=$LOC [counts]=$OTHER [conversion]=$OTHER [recovery]=1)
say "library blocks on $CORES cores: location $LOC, counts and conversion $OTHER, recovery 1 per bank"
pids=()
for bank in offense defense; do for fam in counts location conversion recovery; do
  for (( k = 1; k <= N[$fam]; k++ )); do
    $PY -u scripts/library_blocks.py --out $LIB --bank $bank --family $fam --block $k/${N[$fam]} \
        > logs/block_${bank}_${fam}_$k.log 2>&1 & pids+=($!)
  done
done; done
waitall "${pids[@]}" || { say "STOPPED: a block failed (logs/block_*)"; exit 1; }
fi
say "blocks done; verifying chains"
for bank in offense defense; do for fam in counts location conversion recovery; do
  $PY -u -c "
from experiments.joint_capability_repro import no_database
from experiments.joint_capability_v16_library import chain
with no_database(): chain('$LIB', '$bank', '$fam')" > logs/chain_${bank}_${fam}.log 2>&1 \
    || { say "STOPPED: chain $bank/$fam"; exit 1; }
done; done
say "chains complete; extensions"
pids=()
SEG=${SEG:-$(( CORES / 8 ))}; (( SEG < 1 )) && SEG=1; (( SEG > 6 )) && SEG=6   # era location segments
for bank in offense defense; do
  for fam in location counts conversion recovery; do
    n=$([ $fam = location ] && echo $SEG || ([ $fam = counts ] && echo 2) || echo 1)
    for (( k = 1; k <= n; k++ )); do
      $PY -u scripts/library_extend.py --era --bank $bank --family $fam --segment $k/$n \
          > logs/era_${bank}_${fam}_$k.log 2>&1 & pids+=($!)
    done
    $PY -u scripts/library_extend.py --bank $bank --family $fam > logs/ext2027_${bank}_${fam}.log 2>&1 & pids+=($!)
  done
done
waitall "${pids[@]}" || { say "STOPPED: an extension failed (logs/era_*, logs/ext2027_*)"; exit 1; }
say "ALL DONE"
