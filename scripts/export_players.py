"""Export static player attributes (listed height and position) into the input store.

Reads nba.players (read-only) and writes ``paths.STORE / "players.npz"``:
pid, height (inches), position (1 = point guard ... 5 = center, quarter steps)
and flags for imputed values. A missing position is imputed from height by
least squares on players with both; a missing height from position the same way;
a player with neither gets the population means. These are listings, not
outcomes, and they do not vary over time.

    PYTHONPATH=. python -u scripts/export_players.py
"""
import json
from contextlib import closing

import numpy as np

from lineups import db, paths


def main():
    with closing(db.connect()) as conn, conn.cursor() as cur:
        cur.execute("select id, height_inches, position from nba.players order by id")
        rows = np.array([(i, np.nan if h is None else h, np.nan if p is None else p) for i, h, p in cur.fetchall()],
                        float)
    pid, height, position = rows[:, 0].astype(np.int64), rows[:, 1], rows[:, 2]
    both = np.isfinite(height) & np.isfinite(position)
    slope, intercept = np.polyfit(height[both], position[both], 1)
    back, back_intercept = np.polyfit(position[both], height[both], 1)
    imputed_position = ~np.isfinite(position) & np.isfinite(height)
    imputed_height = ~np.isfinite(height) & np.isfinite(position)
    position = np.where(imputed_position, np.clip(intercept + slope * height, 1, 5), position)
    height = np.where(imputed_height, back_intercept + back * position, height)
    neither = ~np.isfinite(height) | ~np.isfinite(position)
    height = np.where(neither, np.nanmean(height), height)
    position = np.where(neither, np.nanmean(position), position)
    np.savez(paths.STORE / "players.npz", pid=pid, height=height.astype(np.float32),
             position=position.astype(np.float32), imputed_height=imputed_height | neither,
             imputed_position=imputed_position | neither)
    note = dict(source="nba.players (height_inches, position)", players=int(len(pid)),
                imputed_position=int(imputed_position.sum()), imputed_height=int(imputed_height.sum()),
                neither=int(neither.sum()), position_on_height=[float(slope), float(intercept)],
                correlation=float(np.corrcoef(height[both], position[both])[0, 1]))
    (paths.STORE / "players.json").write_text(json.dumps(note, indent=1))
    print(json.dumps(note))


if __name__ == "__main__":
    main()
