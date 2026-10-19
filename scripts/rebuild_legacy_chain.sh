#!/bin/zsh
# The legacy data chain behind the release store, rebuilt through scripts/legacy_names.py (2026-10-14).
#
#   scripts/rebuild_legacy_chain.sh MODE ROOT [STEP ...]
#
# MODE  off    nothing transformed (parity: every artifact must equal the original)
#       names  the name fix (folded names, learned aliases)
#       ids    exact ids from the pages (lineups.pbp_ids; needs OUT/anchors.npz, and
#              `python -m lineups.player_counts --ids` for the per-player counts).
#              ANCHORS=DIR and COUNTS=FILE override the anchors directory and the counts.
# ROOT  a new directory; the legacy relative paths (experiments/cache/...) land in ROOT.
# STEP  any of: setup context text v3 v14 v15 v16 library (default: all, in order); library runs each chain
#       in parallel season blocks (scripts/library_blocks.py; LOCATION_BLOCKS, default 5), then the chain command;
#       text runs shots, channels and extract in parallel, and each can be run alone.
# TABLE=nba_pages.possessions reads the possession table rebuilt from the pages
#       (lineups.page_possessions) instead of nba.possessions.
#
# The commands are the ones run step by step for the names rebuild
# (reports/name_matching_rebuild_progress_2026_10_14.md). Run detached:
#   nohup scripts/rebuild_legacy_chain.sh ids experiments/cache/names_fix_2026_10_14/ids > /dev/null 2>&1 &
# Each step logs to ROOT/logs/<step>.log; a failing step stops the chain.
set -euo pipefail
MODE=$1; ROOT=${2:a}; shift 2
if (( $# )); then STEPS=($@); else STEPS=(setup context text v3 v14 v15 v16 library); fi
REPO=${0:A:h:h}
LEGACY=${REPO:h}/basketball-legacy
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
C=$REPO/experiments/cache
R=$ROOT/experiments/cache
LOG=$ROOT/logs
export PYTHONPATH=$REPO:$REPO/scripts:$LEGACY
case $MODE in
  off) FLAG=(--off); COUNTS=$C/game_player_stats.pkl ;;
  names) FLAG=(); COUNTS=$C/game_player_stats_2026_10_14.pkl ;;
  ids) FLAG=(--ids); COUNTS=${COUNTS:-$C/game_player_stats_ids_2026_10_14.pkl}
       [[ -n ${ANCHORS:-} ]] && FLAG+=(--anchors ${ANCHORS:a}) ;;
  *) echo "MODE must be off, names or ids" >&2; exit 2 ;;
esac
[[ -n ${TABLE:-} ]] && FLAG+=(--table $TABLE)
cd $REPO

run() {  # run LOGNAME MODULE FUNCTION [ARGS...]
  local name=$1; shift
  echo "$(date '+%F %T') start $name" >> $LOG/chain.log
  $PY -u scripts/legacy_names.py --root $ROOT $FLAG "$@" > $LOG/$name.log 2>&1
  echo "$(date '+%F %T') done $name" >> $LOG/chain.log
}

waitall() {  # wait for every background job; fail if any failed
  local pid failed=0
  for pid in $@; do wait $pid || failed=1; done
  (( failed == 0 )) || { echo "$(date '+%F %T') a parallel step failed" >> $LOG/chain.log; exit 1; }
}

threads() {
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
         NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 PYTHONHASHSEED=160918
}

for step in $STEPS; do
  case $step in
    setup)
      [[ -e $ROOT/experiments ]] && { echo "$ROOT exists; use a new root" >&2; exit 2; }
      mkdir -p $R $LOG
      for f in $LEGACY/experiments/*.py; do ln -s $f $ROOT/experiments/${f:t}; done   # library code hashing
      for f in data_epoch.txt asof_points_2026 asof_points_centered_2026 influence_repair_2026_09_09_v2; do
        ln -s $C/$f $R/$f; done                       # date-keyed or unread by the chain: unchanged
      [[ -e $COUNTS ]] || { echo "missing per-player counts $COUNTS" >&2; exit 2; }
      ln -s $COUNTS $R/game_player_stats.pkl
      cp $C/game_player_stats.pkl.epoch $R/game_player_stats.pkl.epoch
      ln -s $ROOT/v14_extract $R/joint_capability_2026_09_15_v14_extract
      ;;
    context)                       # the possession context (clock, ids) and the plain possession cache, from the table
      run context experiments.context load_context
      run possessions experiments.data load_possessions        # lineups.schedule (era windows) reads it
      ;;
    shots) run shots experiments.shot_quality build ;;
    channels) run channels experiments.possession_channels build ;;
    extract) run v14_extract experiments.joint_capability_v14_data main -- extract --output-dir $ROOT/v14_extract ;;
    text)                                                   # the three readers of the text, in parallel
      pids=()
      run shots experiments.shot_quality build & pids+=($!)
      run channels experiments.possession_channels build & pids+=($!)
      run v14_extract experiments.joint_capability_v14_data main -- extract --output-dir $ROOT/v14_extract & pids+=($!)
      waitall $pids
      ;;
    v3)
      run v3_grouped experiments.joint_capability_data build_grouped experiments/cache/joint_capability_2026_09_09_v3
      run v3_augment experiments.joint_capability_v3_data build_grouped experiments/cache/joint_capability_2026_09_09_v3
      run v3_states experiments.joint_capability_v3_data build_states experiments/cache/joint_capability_2026_09_09_v3
      ;;
    v14)
      run v14_labels experiments.joint_capability_v14_data main -- labels --source-dir $ROOT/v14_extract \
          --output-dir $R/joint_capability_2026_09_15_v14_labels
      run v14_states experiments.joint_capability_v14_data main -- states \
          --source-dir $R/joint_capability_2026_09_15_v14_labels --output-dir $R/joint_capability_2026_09_15_v14_states
      ;;
    v15)
      run v15 experiments.joint_capability_v15_data main -- build --output $R/joint_capability_2026_09_17_v15_inputs
      ;;
    v16)
      run v16_phase experiments.joint_capability_v16_phase main -- --out $R/joint_capability_2026_09_18_v16_phase_dev2
      threads
      run v16_training_inputs experiments.joint_capability_v16_training_data prepare \
          $R/joint_capability_2026_09_18_v16_training_inputs_dev2
      run v16_library_prepare experiments.joint_capability_v16_library main -- prepare \
          --out $R/joint_capability_2026_09_18_v16_library_full1
      ;;
    library)  # each chain in season-aligned blocks, cold-started, in parallel (scripts/library_blocks.py);
              # then the ordinary chain command finds every snapshot complete and writes the chain receipt
      threads
      LIB=$R/joint_capability_2026_09_18_v16_library_full1
      typeset -A NBLOCKS; NBLOCKS=(location ${LOCATION_BLOCKS:-5} counts 2 conversion 2 recovery 1)
      pids=()
      for bank in offense defense; do for fam in counts location conversion recovery; do
        for (( k = 1; k <= NBLOCKS[$fam]; k++ )); do
          ( cd $ROOT && $PY -u $REPO/scripts/library_blocks.py --out $LIB --bank $bank --family $fam \
              --block $k/$NBLOCKS[$fam] > $LOG/library_${bank}_${fam}_block$k.log 2>&1 ) & pids+=($!)
        done
      done; done
      echo "$(date '+%F %T') start library blocks (${#pids} processes)" >> $LOG/chain.log
      waitall $pids
      echo "$(date '+%F %T') done library blocks" >> $LOG/chain.log
      pids=()
      for bank in offense defense; do for fam in counts location conversion recovery; do
        run library_${bank}_${fam} experiments.joint_capability_v16_library main -- chain --out $LIB \
            --bank $bank --family $fam & pids+=($!)
      done; done
      waitall $pids
      ;;
    *) echo "unknown step $step" >&2; exit 2 ;;
  esac
done
echo "$(date '+%F %T') chain finished: $STEPS" >> $LOG/chain.log
