#!/bin/zsh
# A self-contained bundle to finish the capability library on a rented CPU box (2026-10-15).
#
#   scripts/box_bundle.sh [ROOT]        # default: the clean rebuild root (paths.CLEAN's parent)
#
# Adam (2026-10-15): "please stop for now. i will rent you a box for the restart." The library and its era
# and 2027q1 extensions need no database and no data beyond the prepared library directory, so they run
# elsewhere and come back as files. The bundle holds:
#   experiments/             the 21 legacy modules the library imports (tag pre-refactor-2026-10-09); the two
#                            that open database connections (data.py, game_player_stats.py) have that line
#                            replaced by an error, so no credentials leave this machine (checked below)
#   experiments/cache/       the prepared library with every finished snapshot, the schedule, the data epoch
#   scripts/                 library_blocks.py, library_extend.py
#   box_run.sh, requirements.txt
# Output: experiments/cache/box_2026_10_15/ (links to the big data) and box_2026_10_15.tar (links followed).
set -euo pipefail
REPO=${0:A:h:h}
LEGACY=${REPO:h}/basketball-legacy
ROOT=${1:-$REPO/experiments/cache/rebuild_pages_2026_10_14}
B=$REPO/experiments/cache/box_2026_10_15
[[ -e $B ]] && { echo "$B exists; use a new name" >&2; exit 2; }
mkdir -p $B/experiments/cache/asof_points_2026 $B/scripts
MODULES=(__init__ config data data_version game_player_stats joint_capability_data joint_capability_repro
         joint_capability_v16_curvature joint_capability_v16_direct_curvature joint_capability_v16_draws
         joint_capability_v16_features joint_capability_v16_inputs joint_capability_v16_library
         joint_capability_v16_location_operator joint_capability_v16_location_preconditioner
         joint_capability_v16_profiles joint_capability_v16_protocol joint_capability_v16_runtime
         joint_capability_v16_solver joint_capability_v16_storage possession_outcomes)
for m in $MODULES; do cp $LEGACY/experiments/$m.py $B/experiments/$m.py; done
for m in data game_player_stats; do      # the connection string is the only credential in these modules
  sed -E -i '' 's/return psycopg2\.connect\("[^"]*"\)/raise RuntimeError("no database on the compute box")/' $B/experiments/$m.py
done
if grep -l -i -E 'psycopg2\.connect\("|password|passwd|user=|host=' $B/experiments/*.py | grep -v joint_capability_repro; then
  echo "credential-like text left in the bundle; not packing" >&2; exit 1
fi
C=$ROOT/experiments/cache
ln -s $C/joint_capability_2026_09_18_v16_library_full1 $B/experiments/cache/joint_capability_2026_09_18_v16_library_full1
cp $C/asof_points_2026/schedule.csv $B/experiments/cache/asof_points_2026/schedule.csv
cp $C/data_epoch.txt $B/experiments/cache/data_epoch.txt
cp $REPO/scripts/library_blocks.py $REPO/scripts/library_extend.py $B/scripts/
cp $REPO/scripts/box_run.sh $B/box_run.sh
printf 'numpy==2.3.4\nscipy==1.16.3\npandas==2.3.3\npsycopg2-binary\n' > $B/requirements.txt
( cd $B/.. && tar -chf box_2026_10_15.tar box_2026_10_15 )
echo "bundle: $B.tar ($(du -h $B.tar | cut -f1))"
