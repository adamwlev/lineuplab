"""Which data the tool shows (2026-10-15): one switch for the release, the player seasons and the modules.

lineups.release, lineups.players and lineups.learned read their default directories from SOURCE, so a
release and its inputs always come from one source.
"""
import os

from lineups import paths

FROZEN_FITS = paths.CACHE / "prospective_2027q1"                 # the frozen 2026-27 prospective record
MAIN = paths.ROOT / "experiments" / "cache"                       # the main cache, whatever LINEUPS_CACHE says
LAYER_2026_10_14 = MAIN / "combination_layer_2026_10_14_learned" / "layer.json"   # on the old data

# What the tool shows. DATA picks one source; LINEUPS_RELEASE (environment) overrides it.
# - names (2026-10-14): the frozen fits on the frozen store with origin states rebuilt on the fixed name
#   matching (scripts/rebuild_player_states.py).
# - clean (2026-10-15): every artifact rebuilt from the possession table rebuilt from the pages with exact
#   player ids (paths.CLEAN; scripts/after_download.sh), the fits retrained (scripts/prospective_fit.py,
#   scripts/release_record.py: calibration and league carried from the frozen record).
# - refresh (2026-10-16, reports/refresh_protocol_2026_10_16.md): the clean release with every number that
#   came from the 2015-2026 history refitted on the clean data: calibration and league
#   (release_record_refresh.json), the band's constants (band_constants_refresh.json), the combination layer
#   and its evidence, and overall quality.
# names and clean keep the 2026-10-14 layer (on the old data) and the band's constants in lineups.band.
SOURCES = dict(
    names=dict(fits=FROZEN_FITS, record=FROZEN_FITS / "freeze" / "record.json",
               store=paths.CACHE / "lineups_store_2027q1_library_names_2026_10_14", matchups=paths.V16_INPUTS,
               table=paths.CACHE / "player_seasons_2026_10_14", modules=paths.CACHE / "release_module_2027q1",
               values=paths.CACHE / "player_values_2026_10_14",
               era_store=paths.CACHE / "lineups_store_era_names_2026_10_14",
               export=paths.CACHE / "release_export_2026_10_12", layer=LAYER_2026_10_14, band=None),
    clean=dict(fits=paths.CLEAN / "prospective_2027q1", record=paths.CLEAN / "prospective_2027q1" / "release_record.json",
               store=paths.CLEAN / "lineups_store_2027q1_library",
               matchups=paths.CLEAN / "joint_capability_2026_09_18_v16_training_inputs_dev2",
               table=paths.CLEAN / "player_seasons", modules=paths.CLEAN / "release_module_2027q1",
               values=paths.CLEAN / "player_values", era_store=paths.CLEAN / "lineups_store_era",
               export=paths.CLEAN / "release_export", layer=LAYER_2026_10_14, band=None))
SOURCES["refresh"] = SOURCES["clean"] | dict(
    record=paths.CLEAN / "prospective_2027q1" / "release_record_refresh.json",
    values=paths.CLEAN / "player_values_refresh", export=paths.CLEAN / "release_export_refresh",
    layer=paths.CLEAN / "combination_layer_2026_10_14_learned" / "layer.json",
    band=paths.CLEAN / "band_constants_refresh.json")
DATA = os.environ.get("LINEUPS_RELEASE", "refresh")    # the refresh since 2026-10-19; "clean" 2026-10-16 to 18 (scripts/compare_releases.py)
SOURCE = SOURCES[DATA]
