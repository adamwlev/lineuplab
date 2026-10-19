#!/bin/zsh
# The refresh's producers after its fits (reports/refresh_protocol_2026_10_16.md), on the clean root, at most two
# processes at a time, niced, one thread each. Run from a worktree pinned at a commit (as scripts/refresh_run.sh).
#
#   nohup caffeinate -i scripts/refresh_downstream.sh [STEP ...] > /dev/null 2>&1 &
#   nohup caffeinate -i scripts/refresh_downstream.sh --after-fits > /dev/null 2>&1 &    # start when the fits finish
#
# Steps, in order (default: all). Each skips work its producer already saved, so a rerun resumes:
#   modules      learned modules on the history R fits, 2015-2026 x seeds 17, 23, 41: the reference forecast and
#                the frozen_fixed module per origin and seed, into nonlinearity_confirm_2026_10_14 (2015-2021)
#                and nonlinearity_screen_2026_10_13 (2022-2026), then each fit's prior level
#   confirm      the 2026-10-14 confirmation's scoring on 2016-2021 (fixtures, accuracy, product fixtures)
#   rows         network-vs-linear rows, the benchmark (era rows: arm R), synergy rows, era rows (arm R, 17 and 23)
#   discovery    interaction discovery and its post hoc checks
#   summary      the confirmation's summaries per seed (they read discovery's held-up families)
#   layer        the combination layer, on the network alone and on the learned module
#   band         the in-support band (tau)
#   record       the refreshed release record (calibration and league from this root's history)
#   cross_era    the cross-era check with the refreshed release
#   constants    the band's constants for the refresh source
#   release      overall quality, export and page, tests, and the comparison with the clean release
# Progress: <clean root>/logs/refresh_downstream.log; one log per step in <clean root>/logs/refresh/.
set -euo pipefail
SELF=${0:A}                                  # the script (inside a function, zsh sets $0 to its name)
REPO=${SELF:h:h}
cd $REPO
PY=/Users/adam/miniconda3/envs/basketball25/bin/python
CLEAN=${LINEUPS_CLEAN:-$REPO/experiments/cache/rebuild_pages_2026_10_14/experiments/cache}
LOG=$CLEAN/logs/refresh_downstream.log
L=$CLEAN/logs/refresh
mkdir -p $L
export PYTHONPATH=$REPO:$REPO/scripts LINEUPS_CACHE=$CLEAN LINEUPS_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
       OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
say() { echo "$(date '+%F %T') $*" >> $LOG; }
stopped=0 current=setup
stop() { say "STOPPED: $*"; stopped=1; exit 1; }
TRAPZERR() { local code=$?; (( stopped )) || say "STOPPED: $current: a command exited with status $code"; }   # errexit, logged (zsh skips an EXIT trap when errexit fires in a function)
run() { local name=$1; shift; say "$name"; nice -n 10 "$@" >> $L/$name.log 2>&1 || stop "$name failed (see $L/$name.log)"; }
NL=scripts/nonlinearity_screen.py
CONFIRM=nonlinearity_confirm_2026_10_14 SCREEN=nonlinearity_screen_2026_10_13

if [[ ${1:-} == --after-fits ]]; then       # wait for scripts/refresh_run.sh, then run every step if no fit failed
  shift
  FITS=$CLEAN/logs/refresh_run.log
  say "waiting for the fits ($FITS)"
  until grep -q "ALL FITS DONE" $FITS 2>/dev/null; do sleep 600; done
  grep -q FAILED $FITS && stop "a fit failed; see $FITS"
  say "fits done"
fi

if [[ ${1:-} == --module ]]; then           # one module job (xargs calls this): out arm origin seed
  shift
  log=$L/module_$1_$2_$3_s$4.log
  if nice -n 10 $PY -u $NL --out $1 --arm $2 --origin $3 --seed $4 >> $log 2>&1; then say "done module $*"
  else say "FAILED module $* (see $log)"; fi
  exit 0
fi

module_queue() {                             # unfinished reference forecasts first, then the modules
  local arm out tag seed sfx
  for arm in reference frozen_fixed; do
    for seed in 17 23 41; do
      [[ $seed == 17 ]] && sfx="" || sfx="_s$seed"
      $PY -c "from lineups import legacy; s = legacy.schedule(); print(' '.join(s[s.season.between(2015, 2026)].tag))" \
        | tr ' ' '\n' | while read -r tag; do
          [[ ${tag:0:4} -le 2021 ]] && out=$CONFIRM || out=$SCREEN
          [[ -e $CLEAN/$out/${arm}${sfx}_${tag}.json ]] || echo "$out $arm $tag $seed"   # the record is written last
        done
    done
  done
}

step_modules() {
  say "modules: queue"
  module_queue > $L/module_queue.txt
  say "modules: $(wc -l < $L/module_queue.txt | tr -d ' ') jobs"
  local start=$(wc -l < $LOG)                # only this run's failures (a rerun's log holds earlier ones)
  xargs -P 2 -L 1 $SELF --module < $L/module_queue.txt
  [[ $(tail -n +$((start + 1)) $LOG) == *"FAILED module"* ]] && stop "a module job failed"
  for s in 17 23 41; do
    [[ -e $CLEAN/$CONFIRM/prior_level_s$s.csv ]] || \
      run prior_level_confirm_s$s $PY -u $NL --out $CONFIRM --era 2015 2021 --prior-level --seeds $s --name prior_level_s$s
  done
  $PY -c "
import pandas as pd; d = '$CLEAN/$CONFIRM/'
pd.concat([pd.read_csv(d + f'prior_level_s{s}.csv') for s in (17, 23, 41)]).to_csv(d + 'prior_level.csv', index=False)"
  [[ -e $CLEAN/$SCREEN/prior_level.csv ]] || run prior_level_screen $PY -u $NL --out $SCREEN --era 2022 2026 --prior-level
}

step_confirm() {
  run confirm_fixtures $PY -u $NL --out $CONFIRM --era 2016 2021 --confirm --arms frozen_fixed --seeds 17 23 41 --name confirm
  run confirm_accuracy $PY -u $NL --out $CONFIRM --era 2015 2021 --stacked-calibration --name accuracy
  run confirm_product $PY -u $NL --out $CONFIRM --product-fixtures --name confirm
}

step_summary() {                             # the confirmation's summaries read discovery's held-up families
  for s in 17 23 41; do
    run confirm_summary_s$s $PY -u $NL --out $CONFIRM --era 2016 2021 --seed $s --summary --name summary_s$s
  done
}

step_rows() {
  run nn_vs_linear $PY -u scripts/nn_vs_linear.py
  run ensemble_check $PY -u scripts/ensemble_check.py --era-arms R
  run synergy_hypotheses $PY -u scripts/synergy_hypotheses.py
  run era_diagnostics $PY -u scripts/era_diagnostics.py --arms R --seeds 17 23
}

step_discovery() {
  run interaction_discovery $PY -u scripts/interaction_discovery.py
  run interaction_discovery_posthoc $PY -u scripts/interaction_discovery_posthoc.py
}

step_layer() {
  run combination_layer $PY -u scripts/combination_layer.py
  run combination_layer_learned $PY -u scripts/combination_layer.py --learned
}

step_band() { run band_in_support $PY -u scripts/band_in_support.py; }

step_record() {
  run release_record $PY -u scripts/release_record.py --calibration history --name release_record_refresh.json
}

step_cross_era() { ( export LINEUPS_RELEASE=refresh; run cross_era $PY -u scripts/cross_era.py ); }

step_constants() { run refresh_constants $PY -u scripts/refresh_constants.py; }

step_release() {                             # as scripts/release_clean.sh: the release's own environment
  (
    unset LINEUPS_CACHE
    export LINEUPS_CLEAN=$CLEAN LINEUPS_RELEASE=refresh
    [[ -e $CLEAN/player_values_refresh/values.npz ]] || run player_values $PY -u scripts/player_values.py
    run export $PY -u scripts/export_release.py
    run page $PY -u tool/build_lineups.py
    run tests $PY -m unittest tests.test_tool_parity tests.test_release tests.test_players tests.test_learned \
        tests.test_band tests.test_explain
    unset LINEUPS_RELEASE
    run compare $PY -u scripts/compare_releases.py --new-root $CLEAN --old-source clean --new-source refresh \
        --out compare_refresh
  )
}

if (( $# )); then STEPS=("$@"); else STEPS=(modules confirm rows discovery summary layer band record cross_era constants release); fi
for step in $STEPS; do current=$step; step_$step; done
say "ALL DONE: steps $STEPS"
