"""Old release vs the release retrained on the clean data (2026-10-15).

Old: the frozen 2026-27 fits on the name-fixed store (what the review copy showed on 2026-10-14).
New: the fits retrained on the clean-data rebuild (paths.CLEAN: possessions from the pages, exact player ids;
scripts/after_download.sh, scripts/prospective_fit.py, scripts/release_record.py).

Both are compared as the tool shows them (arm R, calibrated, each against its own league-average panel):
1. real 2025-26 fives (at least MIN_POSSESSIONS on offense, a fixed sample): offense, points allowed and
   margin, old against new;
2. overall quality (scripts/player_values.py) of the players the fixes touch, and the largest movers.

    PYTHONPATH=. python -u scripts/compare_releases.py [--new-root DIR]
    PYTHONPATH=. python -u scripts/compare_releases.py --old-source clean --new-source refresh --out compare_refresh

Output: <new root>/compare/{fives.csv, values.csv, report.json}. With --old-source and --new-source
(lineups.sources; 2026-10-16, the refresh) both releases come from their sources, and the output goes to
<new root>/<--out>.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from lineups import learned, legacy, paths, players, release
from lineups.sources import SOURCES

MIN_POSSESSIONS, SAMPLE, SEED = 150, 120, 20261015
TOUCHED = ("jalen williams", "jaylin williams", "jalen green", "jeff green", "markieff morris", "marcus morris",
           "taylor hendricks", "nene", "vit krejci", "vasilije micic", "hugo gonzalez", "carlton carrington",
           "draymond green", "danny green")      # folded display names


def releases(new_root):
    old = release.Release(arms=("R",), store=release.STORE, fits=release.FROZEN_FITS, record=release.FROZEN_RECORD,
                          matchups=paths.V16_INPUTS, table=players.TABLE, modules=learned.DIR)
    fits = new_root / "prospective_2027q1"
    new = release.Release(arms=("R",), store=new_root / "lineups_store_2027q1_library", fits=fits,
                          record=fits / "release_record.json",
                          matchups=new_root / "joint_capability_2026_09_18_v16_training_inputs_dev2",
                          table=new_root / "player_seasons", modules=new_root / "release_module_2027q1")
    return old, new


def from_source(name):
    s = SOURCES[name]
    return release.Release(arms=("R",), store=s["store"], fits=s["fits"], record=s["record"], matchups=s["matchups"],
                           table=s["table"], modules=s["modules"])


def real_fives(rel):
    g = rel.matchups
    season = rel.store.schedule().query("season == 2026")
    rows = np.flatnonzero((np.asarray(g["date"]) >= legacy.day(season.start.min()))
                          & (np.asarray(g["date"]) < legacy.day(season.stop.max())))
    fives = np.sort(np.asarray(g["pids"][rows]), 1)
    units, inverse = np.unique(fives, axis=0, return_inverse=True)
    poss = np.bincount(inverse.ravel(), np.asarray(g["possessions"][rows], float), len(units))
    keep = units[poss >= MIN_POSSESSIONS]
    return keep[np.random.default_rng(SEED).choice(len(keep), min(SAMPLE, len(keep)), replace=False)]


def values(table_dir, values_dir, rule="relative"):
    t = players.PlayerSeasons(table_dir)
    with np.load(values_dir / "values.npz") as z:
        v = {k: z[k] for k in z.files}
    return pd.DataFrame(dict(pid=v["pid"], season=v["season"], offense=v[f"{rule}_offense"],
                             defense=v[f"{rule}_defense"], name=[t.names.get(int(p), str(p)) for p in v["pid"]]))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--new-root", type=Path, default=paths.CLEAN)
    p.add_argument("--old-source", choices=sorted(SOURCES))
    p.add_argument("--new-source", choices=sorted(SOURCES))
    p.add_argument("--out", default="compare")
    a = p.parse_args()
    OUT = a.new_root / a.out
    if a.out != "compare" and OUT.exists():
        raise SystemExit(f"{OUT} exists; a comparison is not overwritten")
    OUT.mkdir(parents=True, exist_ok=True)
    by_source = a.old_source is not None and a.new_source is not None
    old, new = (from_source(a.old_source), from_source(a.new_source)) if by_source else releases(a.new_root)
    fives = real_fives(new)
    rows = []
    for five in fives:
        r = {}
        for label, rel in (("old", old), ("new", new)):
            x = rel.season_ratings(rel.seasons.rows(five, np.full(5, 2026)))
            r |= {f"{label}_{k}": v for k, v in x.items()}
        rows.append(dict(five=" ".join(map(str, five)), **r))
    f = pd.DataFrame(rows)
    f.to_csv(OUT / "fives.csv", index=False)
    report = dict(fives=len(f))
    for k in ("offense", "defense", "margin"):
        d = f[f"new_{k}"] - f[f"old_{k}"]
        report[k] = dict(mean_change=round(float(d.mean()), 3), sd_change=round(float(d.std()), 3),
                         max_abs_change=round(float(d.abs().max()), 3),
                         correlation=round(float(np.corrcoef(f[f"old_{k}"], f[f"new_{k}"])[0, 1]), 4))
    if by_source:
        vo = values(SOURCES[a.old_source]["table"], SOURCES[a.old_source]["values"])
        vn = values(SOURCES[a.new_source]["table"], SOURCES[a.new_source]["values"])
    else:
        vo = values(players.TABLE, paths.CACHE / "player_values_2026_10_14")
        vn = values(a.new_root / "player_seasons", a.new_root / "player_values")
    v = vo.merge(vn, on=["pid", "season"], how="outer", suffixes=("_old", "_new"))
    v["net_old"], v["net_new"] = v.offense_old - v.defense_old, v.offense_new - v.defense_new
    v["change"] = v.net_new - v.net_old
    v.to_csv(OUT / "values.csv", index=False)
    from lineups.player_counts import fold
    name = v.name_new.fillna(v.name_old).map(lambda x: fold(str(x)))
    recent = v[(v.season >= 2023) & name.isin(TOUCHED)]
    report["touched"] = (recent
                         .sort_values(["name_old", "season"])[["name_old", "season", "net_old", "net_new", "change"]]
                         .round(2).to_dict("records"))
    big = v[(v.season == 2026)].dropna(subset=["change"]).sort_values("change")
    report["movers_2026"] = dict(down=big.head(8)[["name_new", "net_old", "net_new", "change"]].round(2).to_dict("records"),
                                 up=big.tail(8)[["name_new", "net_old", "net_new", "change"]].round(2).to_dict("records"))
    report["values_2026"] = dict(correlation=round(float(big[["net_old", "net_new"]].corr().iloc[0, 1]), 4),
                                 mean_abs_change=round(float(big.change.abs().mean()), 3))
    (OUT / "report.json").write_text(json.dumps(report, indent=1, default=str))
    print(json.dumps(report, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
