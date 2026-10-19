"""Run the directional property suite (lineups.properties) on the reference model.

Base lineups at each origin: real offense fives and defense fives with at least
50 possessions in that origin's quarter. Panel: the 40 offense fives with the
most possessions. Model: J_POINT_BOTH checkpoint mixture across seeds, native.

Usage: PYTHONPATH=. python -u scripts/property_suite.py [origin ...]
Output: experiments/cache/property_suite_2026_10_09/<origin>.csv and summary.csv
"""
import sys
from functools import partial

import numpy as np
import pandas as pd

from lineups import legacy, paths, properties
from lineups.coherence import checkpoint_models, ledgers
from lineups.evaluate import FIVE
from lineups.features import Store

OUT = paths.CACHE / "property_suite_2026_10_09"


def real_fives(origin_tag, g, keys, minimum=50):
    f = legacy.row_frame(legacy.quarter_rows(legacy.schedule().query("tag == @origin_tag").iloc[0], g), g)
    units = f.groupby(keys).possessions.sum().sort_values(ascending=False)
    units = units[units >= minimum]
    return np.array(units.index.tolist(), np.int64)


def main(origins):
    OUT.mkdir(parents=True, exist_ok=True)
    store, g = Store(), legacy.matchups()
    summaries = []
    for tag in origins:
        offense = real_fives(tag, g, FIVE)
        defense = real_fives(tag, g, legacy.DEFENSE)
        predict = partial(ledgers, checkpoint_models(tag), store, origin_tag=tag)
        frame = properties.run(lambda o, d: predict(o, d), store, tag, offense, defense, offense[:40])
        frame.to_csv(OUT / f"{tag}.csv", index=False)
        s = properties.summarize(frame).assign(origin=tag)
        summaries.append(s)
        print(f"\n== {tag}: {len(offense)} offense fives, {len(defense)} defense fives")
        with pd.option_context("display.width", 200, "display.float_format", "{:.4f}".format):
            print(s.to_string())
    pd.concat(summaries).to_csv(OUT / "summary.csv")


if __name__ == "__main__":
    main(sys.argv[1:] or ["2026q4"])
