"""Post-hoc checks on the interactions that held up (not in the protocol; labeled post hoc).

1. Late-game fouling. Rows containing any possession in the last two minutes of
   the 4th quarter or in overtime are dropped (nba.possessions, read-only), and
   the confirmation and replication tests are rerun. The model has no game-state
   input, so a free-throw "synergy" among closing lineups could be fouling.
2. Does the network already capture it? The same tests use the residual against
   the network's own forecast instead of its additive approximation. If the
   coefficient shrinks toward zero, the network models that interaction.

    PYTHONPATH=.:scripts python -u scripts/interaction_discovery_posthoc.py
"""
import json
from contextlib import closing

import numpy as np
import pandas as pd
from scipy import stats

import interaction_discovery as d
from lineups import db, paths
from lineups.evaluate import FIVE
from lineups.legacy import DEFENSE

OUT = d.OUT


def late_rows():
    """(game_id, sorted offense five, sorted defense five) -> possessions in the last 2:00 of Q4 or in OT."""
    path = OUT / "late_possessions.pkl"
    if path.exists():
        return pd.read_pickle(path)
    ids = [f"{s}_player_{i}_id" for s in ("away", "home") for i in range(1, 6)]
    query = f"""select game_id, away_team_ball, {", ".join(ids)} from {paths.POSSESSIONS_TABLE}
                where quarter >= 5 or (quarter = 4 and time_left_start <= 120)"""
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute(query)
        f = pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])
    away = np.sort(f[[f"away_player_{i}_id" for i in range(1, 6)]].to_numpy(), 1)
    home = np.sort(f[[f"home_player_{i}_id" for i in range(1, 6)]].to_numpy(), 1)
    a = f.away_team_ball.to_numpy()[:, None]
    off, de = np.where(a, away, home), np.where(a, home, away)
    keys = pd.DataFrame(np.c_[f.game_id.to_numpy(), off, de], columns=["game_id", *FIVE, *DEFENSE])
    late = keys.groupby(list(keys.columns)).size().rename("late").reset_index()
    late.to_pickle(path)
    return late


def network_residuals(frame, era):
    """Residual against the network's own forecast (points: R; events: the forecast rate)."""
    rows = pd.read_pickle(d.SYNERGY / f"rows_{'era' if era else 'benchmark'}.pkl")[["origin", "row", "actual", "R"]]
    ev = d.event_columns(era)
    m = frame[["origin", "row"]].merge(rows, on=["origin", "row"], how="left").merge(ev, on=["origin", "row"], how="left")
    out = {"points": (m.actual - m.R).to_numpy()}
    for k in d.EVENTS:
        exp = m[f"{k}_exp"].fillna(0).to_numpy(float)
        rate = np.divide(m[f"{k}_num"].fillna(0).to_numpy(float), exp, out=np.zeros(len(m)), where=exp > 0)
        out[k] = 100 * (rate - m[f"{k}_fc"].to_numpy(float))
    return out


def run(frame, feats, family, years, c, sign, y=None, keep=None):
    f = frame if keep is None else frame[keep]
    ft = feats if keep is None else feats[keep]
    if y is not None:
        f = f.copy()
        f[f"y_{family}"] = y if keep is None else y[keep]
    data = d.window_data(f, ft, family, years)
    r = d.test(data, c)
    r["p_one"] = float(stats.norm.sf(sign * r["coef"] / r["se"])) if r["se"] and np.isfinite(r["se"]) else np.nan
    return r


def main():
    result = json.loads((OUT / "result.json").read_text())
    held = [(fam, c) for fam, v in result["families"].items() for c in v["confirmed"] if c["label"].startswith("held up")]
    bench, era = d.residuals(False), d.residuals(True)
    fb, _ = d.features(bench, False)
    fe, _ = d.features(era, True)
    late = late_rows()
    keys = ["game_id", *FIVE, *DEFENSE]
    no_late = {}
    for name, frame in (("bench", bench), ("era", era)):
        m = frame[keys].merge(late, on=keys, how="left")
        no_late[name] = (m.late.fillna(0).to_numpy() == 0)
        print(name, "rows without late possessions:", round(no_late[name].mean(), 3), flush=True)
    net = {"bench": network_residuals(bench, False), "era": network_residuals(era, True)}
    lines, out = ["Post hoc checks on the interactions that held up (residual units as in the main report).",
                  "columns: confirmation 2022-2026 | replication 2007-2013, each as coef (SE)"], []
    for fam, c in held:
        cand = next(x for x in d.CANDIDATES if d.name(x) == c["candidate"])
        sign = np.sign(c["discovery"]["coef"])
        rec = dict(family=fam, candidate=c["candidate"], label=c["label"])
        for tag, kw in (("main", {}), ("no_late", "late"), ("vs_network", "net")):
            for window, frame, feats, key in (("confirmation", bench, fb, "bench"), ("replication", era, fe, "era")):
                args = {}
                if kw == "late":
                    args["keep"] = no_late[key]
                elif kw == "net":
                    args["y"] = net[key][fam]
                r = run(frame, feats, fam, d.WINDOWS[window], cand, sign, **args)
                rec[f"{tag}_{window}"] = r["coef"]
                rec[f"{tag}_{window}_se"] = r["se"]
        out.append(rec)
        fmt = lambda t: f"{rec[f'{t}_confirmation']:+.2f} ({rec[f'{t}_confirmation_se']:.2f}) | {rec[f'{t}_replication']:+.2f} ({rec[f'{t}_replication_se']:.2f})"
        lines.append(f"{fam:<12} {c['candidate']:<24} main {fmt('main')}   no late-game rows {fmt('no_late')}   vs network forecast {fmt('vs_network')}")
    text = "\n".join(lines)
    (OUT / "posthoc.txt").write_text(text)
    pd.DataFrame(out).to_csv(OUT / "posthoc.csv", index=False)
    print(text)


if __name__ == "__main__":
    main()
