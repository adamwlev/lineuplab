"""Observed analogues for the five-center defense (exploratory, saved forecasts only).

Question: on real lineups, does the reference forecast err systematically by the
defending lineup's size, and does that error depend on how many shooters the
offense has? A broadcast defense applies one shift to all five attackers, so if
big defenses struggle specifically against spread offenses, the residual
(actual - forecast) should be larger for big defense x spread offense.

Definitions, fixed before looking at residuals (origin-dated information only):
  big       height >= 82 in (nba.players)
  shooter   prior 3PA per 100 on-floor possessions >= 4 (origin-mode state)
  spread    offense with >= 4 shooters

Rows: every game x offense five x defense five row in the 44 primary quarters
(2016-2026), forecasts conditional on the actual defense, possession-weighted,
points per 100. Seed-mean forecasts with strictly prior calibration
(lineups.evaluate.calibrated_rows). Uncertainty: season-level standard errors
over the 11 seasons. Output: experiments/cache/defense_analogues_2026_10_09/.
"""
import numpy as np
import pandas as pd

from lineups import db, legacy, paths
from lineups.evaluate import FIVE, MODELS, calibrated_rows
from lineups.features import Store

OUT = paths.CACHE / "defense_analogues_2026_10_09"
BIG_INCHES = 82
SHOOTER_3PA = 4.


def profiles(store, origin_index, pids):
    off = store.offense(pids, origin_index=origin_index)
    base = off["base"]
    loc = np.exp(base[:, 3:9] - base[:, 3:9].max(1, keepdims=True))
    loc /= loc.sum(1, keepdims=True)
    return 100 * np.exp(np.clip(base[:, 0], -12, 4)) * loc[:, 4:].sum(1)


def stratum_table(rows, by):
    out = []
    for key, g in rows.groupby(by):
        w = g.possessions.to_numpy(float)
        rec = dict(zip(by, key if isinstance(key, tuple) else (key,)), rows=len(g), possessions=int(w.sum()),
                   actual=100 * g.points.sum() / w.sum())
        for m in ("half", "calibrated", "additive_defense"):
            rec[f"resid_{m}"] = float(np.average(g[f"r_{m}"], weights=w))
            per = g.groupby("season")[[f"r_{m}", "possessions"]].apply(
                lambda s: np.average(s[f"r_{m}"], weights=s.possessions))
            rec[f"se_{m}"] = float(per.std(ddof=1) / np.sqrt(len(per))) if len(per) > 1 else np.nan
            rec[f"seasons_pos_{m}"] = f"{int((per > 0).sum())}/{len(per)}"
        out.append(rec)
    return pd.DataFrame(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    store = Store()
    bio = db.heights()
    g = legacy.matchups()
    frames = []
    for o, f in calibrated_rows(legacy.origins(), lambda o: legacy.row_frame(legacy.quarter_rows(o, g), g),
                                lambda o, s: legacy.native(o.tag, "J_POINT_BOTH", s, "checkpoint_average"),
                                lambda o, s: legacy.controls(o.tag, s)[["row", "league", "additive_defense"]],
                                legacy.SEEDS):
        pids = np.unique(f[FIVE + legacy.DEFENSE].to_numpy())
        tpa = pd.Series(profiles(store, int(o.origin_index), pids), index=pids)
        height = bio.reindex(pids)
        off, dfn = f[FIVE].to_numpy(), f[legacy.DEFENSE].to_numpy()
        look = lambda s, a: s.reindex(a.ravel()).to_numpy().reshape(a.shape)
        f["off_shooters"] = (look(tpa, off) >= SHOOTER_3PA).sum(1)
        f["off_bigs"] = (look(height, off) >= BIG_INCHES).sum(1)
        f["def_bigs"] = (look(height, dfn) >= BIG_INCHES).sum(1)
        f["def_nonspacing_bigs"] = ((look(height, dfn) >= BIG_INCHES) & (look(tpa, dfn) < 1)).sum(1)
        f["missing_height"] = np.isnan(look(height, np.c_[off, dfn])).sum(1)
        f["season"], f["origin"] = int(o.season), o.tag
        actual = 100 * f.points / f.possessions
        for m in MODELS:
            f[f"r_{m}"] = actual - f[m]
        frames.append(f.drop(columns=FIVE + legacy.DEFENSE))
        print(o.tag, len(f), flush=True)
    rows = pd.concat(frames, ignore_index=True)
    rows.to_csv(OUT / "rows.csv.gz", index=False)
    rows["def_bigs_bin"] = rows.def_bigs.clip(upper=3)
    rows["spread"] = rows.off_shooters >= 4
    rows["off_bigs_bin"] = rows.off_bigs.clip(upper=3)
    with pd.option_context("display.width", 220, "display.float_format", "{:.3f}".format):
        for by in (["def_bigs_bin"], ["def_nonspacing_bigs"], ["off_bigs_bin"], ["def_bigs_bin", "spread"],
                   ["off_shooters"]):
            t = stratum_table(rows, by)
            t.to_csv(OUT / f"by_{'_'.join(by)}.csv", index=False)
            print("\n== residual (actual - forecast) by", by)
            print(t.to_string(index=False))
        # Interaction: (big D vs spread - big D vs not spread) - (small D vs spread - small D vs not spread), per season.
        def cell(s, big, spread):
            x = s[((s.def_bigs >= 2) == big) & (s.spread == spread)]
            return np.average(x.r_half, weights=x.possessions) if len(x) else np.nan
        gap = lambda s, big: cell(s, big, True) - cell(s, big, False)
        per = rows.groupby("season")[["def_bigs", "spread", "r_half", "possessions"]].apply(
            lambda s: gap(s, True) - gap(s, False))
        print("\n== Interaction, reference half: [2+ big D x spread] residual gap minus [<2 big D] gap, by season")
        print(per.round(3).to_string())
        print(f"mean {per.mean():.3f}  season SE {per.std(ddof=1) / np.sqrt(len(per)):.3f}  positive {int((per > 0).sum())}/{len(per)}")


if __name__ == "__main__":
    main()
