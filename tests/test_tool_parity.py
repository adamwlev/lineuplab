"""The browser model (tool/lineup_model.js) reproduces the Python release (needs node and the export).

Cases: 1,200 matchups of random player-seasons (2003-2026; both input rules, both
arms, per-seed native points), fixtures, average-opponent ratings, bands with
their reasons, explanations, the combination layer with the band it moves, and
the learned combinations (per row, against the average opponent, in a matchup,
and in the band with the layer), and the missing-piece search's exact forecast.
Run scripts/export_release.py first.
"""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from lineups import paths, players, release

EXPORT = release.SOURCE["export"]          # the release's export (lineups.sources)
TOOL = Path(__file__).resolve().parents[1] / "tool"


@unittest.skipUnless(shutil.which("node") and (EXPORT / "meta.json").exists()
                     and (players.TABLE / "player_seasons.npz").exists(), "node or the export absent")
class BrowserParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.band import Band
        from lineups.coherence import fixtures
        from lineups.combinations import Combinations
        from lineups.explain import Explainer
        rng = np.random.default_rng(7)
        cls.rel = {rule: release.Release(rule=rule) for rule in players.RULES}
        t = cls.rel["relative"].seasons.table
        fx = fixtures()
        fixture = lambda n: cls.rel["relative"].seasons.rows(fx[n]["pids"], np.full(5, 2026)).tolist()

        def five(season=None):
            pool = np.flatnonzero(t["season"] == (season or int(rng.integers(2003, 2027))))
            return rng.choice(pool, 5, replace=False).tolist()

        native = []
        for k in range(1200):
            rule, arm = players.RULES[k % 2], list(release.ARMS)[(k // 2) % 2]
            if k < 1000:
                off, de = five(), five()
            else:
                names = ["five_goberts", "legal_pure_centers", "five_jokics", "jokic_westbrook", "highest_exposure_real_2026"]
                off, de = fixture(names[k % 5]), fixture(names[(k + 2) % 5])
            native.append(dict(rule=rule, arm=arm, offense=off, defense=de))
        celtics, warriors = five(2008), five(2017)
        cases = dict(
            native=native,
            ratings=[dict(rule=r, arm=a, rows=x) for r in players.RULES for a in release.ARMS
                     for x in (fixture("highest_exposure_real_2026"), five(2011))],
            band_lineup=[dict(rule=r, rows=x) for r in players.RULES for x in (fixture("five_goberts"), five(2005))],
            band_matchup=[dict(rule="relative", a=celtics, b=warriors), dict(rule="as_was", a=warriors, b=celtics)],
            explain_lineup=[dict(rule="relative", rows=fixture("five_goberts")), dict(rule="as_was", rows=five(2009))],
            explain_against=[dict(rule="relative", rows=fixture("jokic_westbrook"), opponent=fixture("legal_pure_centers"))],
            combinations_lineup=[dict(rule="relative", rows=fixture("five_goberts")),
                                 dict(rule="as_was", rows=fixture("legal_pure_centers")),
                                 dict(rule="relative", rows=fixture("highest_exposure_real_2026")),
                                 dict(rule="as_was", rows=five(2005))],
            combinations_matchup=[dict(rule="relative", a=fixture("five_jokics"), b=fixture("legal_pure_centers")),
                                  dict(rule="as_was", a=celtics, b=warriors)],
            learned_points=[dict(rule=players.RULES[k % 2], offense=five(), defense=five()) for k in range(40)]
            + [dict(rule="relative", offense=fixture("five_goberts"), defense=fixture("jokic_westbrook"))],
            learned_lineup=[dict(rule="relative", rows=fixture("five_goberts")),
                            dict(rule="relative", rows=fixture("highest_exposure_real_2026")),
                            dict(rule="as_was", rows=five(2005))],
            learned_matchup=[dict(rule="relative", a=fixture("five_jokics"), b=fixture("legal_pure_centers")),
                             dict(rule="as_was", a=celtics, b=warriors)],
            profile=[int(r) for r in rng.choice(len(t["pid"]), 25, replace=False)])
        expected = dict(native=[], ratings=[], band_lineup=[], band_matchup=[], explain_lineup=[], explain_against=[],
                        combinations_lineup=[], combinations_matchup=[], learned_points=[], learned_lineup=[],
                        learned_matchup=[])
        for c in native:
            r = cls.rel[c["rule"]]
            preds = r.season_ledgers(c["arm"], r.inputs([c["offense"]], [c["defense"]]))
            expected["native"].append([float(p.points100[0]) for p in preds])
        for c in cases["ratings"]:
            expected["ratings"].append(cls.rel[c["rule"]].season_ratings(c["rows"], c["arm"]))
        bands = {rule: Band(cls.rel[rule]) for rule in players.RULES}
        expected["band_lineup"] = [bands[c["rule"]].lineup(c["rows"]) for c in cases["band_lineup"]]
        expected["band_matchup"] = [bands[c["rule"]].matchup(c["a"], c["b"]) for c in cases["band_matchup"]]
        explainers = {rule: Explainer(cls.rel[rule]) for rule in players.RULES}
        expected["explain_lineup"] = [explainers[c["rule"]].lineup(c["rows"]) for c in cases["explain_lineup"]]
        expected["explain_against"] = [explainers[c["rule"]].against(c["rows"], c["opponent"])
                                       for c in cases["explain_against"]]
        combos = {rule: Combinations(cls.rel[rule]) for rule in players.RULES}
        for c in cases["combinations_lineup"]:
            ex = explainers[c["rule"]]
            layer = combos[c["rule"]].lineup(c["rows"], ex.lineup(c["rows"])["rates"], ex.league)
            expected["combinations_lineup"].append(dict(layer=layer, band=bands[c["rule"]].lineup(c["rows"], layer)))
        for c in cases["combinations_matchup"]:
            ex = explainers[c["rule"]]
            layer = combos[c["rule"]].matchup(c["a"], c["b"], ex.against(c["a"], c["b"])["rates"],
                                              ex.against(c["b"], c["a"])["rates"])
            expected["combinations_matchup"].append(dict(layer=layer, band=bands[c["rule"]].matchup(c["a"], c["b"], layer)))
        for c in cases["learned_points"]:
            got = cls.rel[c["rule"]].season_learned([c["offense"]], [c["defense"]])
            expected["learned_points"].append({k: float(v[0]) for k, v in got.items()})
        for c in cases["learned_lineup"]:
            ex, r = explainers[c["rule"]], cls.rel[c["rule"]]
            layer = combos[c["rule"]].lineup(c["rows"], ex.lineup(c["rows"])["rates"], ex.league)
            learned = r.season_learned_ratings(c["rows"])
            expected["learned_lineup"].append(dict(learned=learned, band=bands[c["rule"]].lineup(c["rows"], layer, learned)))
        for c in cases["learned_matchup"]:
            ex, r = explainers[c["rule"]], cls.rel[c["rule"]]
            layer = combos[c["rule"]].matchup(c["a"], c["b"], ex.against(c["a"], c["b"])["rates"],
                                              ex.against(c["b"], c["a"])["rates"])
            learned = r.season_learned_matchup(c["a"], c["b"])
            expected["learned_matchup"].append(dict(learned=learned,
                                                    band=bands[c["rule"]].matchup(c["a"], c["b"], layer, learned)))
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "cases.json").write_text(json.dumps(cases))
            subprocess.run(["node", str(TOOL / "parity.js"), str(EXPORT), str(Path(tmp) / "cases.json"),
                            str(Path(tmp) / "out.json")], check=True)
            cls.got = json.loads((Path(tmp) / "out.json").read_text())
        cls.expected, cls.cases = expected, cases

    def close(self, a, b, tol, label):
        self.assertLess(abs(float(a) - float(b)), tol, f"{label}: python {a} vs js {b}")

    def test_native_points_for_1200_matchups(self):
        print(f"\nnode: {self.got['seconds']:.1f}s for every case", flush=True)
        worst = max(abs(e - g) for exp, got in zip(self.expected["native"], self.got["native"]) for e, g in zip(exp, got))
        self.assertLess(worst, 1e-3, f"worst per-seed native difference {worst}")

    def test_average_opponent_ratings(self):
        for exp, got in zip(self.expected["ratings"], self.got["ratings"]):
            for k in ("offense", "defense", "margin"):
                self.close(exp[k], got[k], 1e-3, k)

    def test_bands_and_reasons(self):
        for kind, keys in (("band_lineup", ("offense", "defense", "margin")),
                           ("band_matchup", ("a_offense", "b_offense", "margin"))):
            for exp, got in zip(self.expected[kind], self.got[kind]):
                for k in keys:
                    for part in ("point", "low", "high", "sd"):
                        self.close(exp[k][part], got[k][part], 1e-3, f"{kind} {k} {part}")
                self.assertEqual(exp["reasons"], got["reasons"])

    def test_explanations(self):
        for kind in ("explain_lineup", "explain_against"):
            for exp, got in zip(self.expected[kind], self.got[kind]):
                for k, v in exp["channels"].items():
                    self.close(v, got["channels"][k], 1e-3, f"{kind} channel {k}")
                for k, v in exp["team"].items():     # per-100 counts like points; shares and rates tighter
                    tol = 1e-5 if k.endswith(("share", "_fg")) else 1e-3
                    self.close(v, got["team"][k], tol, f"{kind} team {k}")
                for pe, pg in zip(exp["players"], got["players"]):
                    self.assertEqual(pe["player"], pg["player"])
                    for k in ("usage_share", "usual_share", "points", "threes", "rim_attempts"):
                        self.close(pe[k], pg[k], 1e-3, f"{kind} player {k}")
                if "creation" in exp:
                    for k in ("demand", "supply"):
                        self.close(exp["creation"][k], got["creation"][k], 1e-3, f"creation {k}")

    def test_combination_layer(self):
        for kind, keys in (("combinations_lineup", ("offense", "defense", "margin")),
                           ("combinations_matchup", ("a_offense", "b_offense", "margin"))):
            for exp, got in zip(self.expected[kind], self.got[kind]):
                le, lg = exp["layer"], got["layer"]
                for part in ("layer", "continued"):
                    for k in keys:
                        self.close(le[part][k], lg[part][k], 1e-4, f"{kind} {part} {k}")
                for group, effects in le["effects"].items():
                    self.assertEqual([e["id"] for e in effects], [e["id"] for e in lg["effects"][group]], f"{kind} {group}")
                    for e, g in zip(effects, lg["effects"][group]):
                        self.assertEqual(e["title"], g["title"])
                        for k in ("pairs", "expected", "change"):
                            self.close(e[k], g[k], 1e-6, f"{kind} {e['id']} {k}")
                        self.close(e["points"], g["points"], 1e-4, f"{kind} {e['id']} points")
                self.assertEqual(le["beyond"], lg["beyond"])
                self.assertEqual(le["notes"], lg["notes"])
                for k in keys:
                    for part in ("point", "low", "high", "assumption_low", "assumption_high"):
                        self.close(exp["band"][k][part], got["band"][k][part], 1e-3, f"{kind} band {k} {part}")
                self.assertEqual(exp["band"]["reasons"], got["band"]["reasons"])

    def test_player_profiles(self):
        """The details sheet's estimates are the player-season table's capability banks, block by block."""
        t = self.rel["relative"].seasons.table
        for row, got in zip(self.cases["profile"], self.got["profile"]):
            off, de = t["adjusted_offense"][row], t["adjusted_defense"][row]
            for block, coef, sd in (("own", off[0:16], off[64:80]), ("teammates", off[16:32], off[80:96]),
                                    ("defense", de[0:16], de[32:48])):
                np.testing.assert_allclose([e["coef"] for e in got["blocks"][block]], coef, rtol=0, atol=1e-6)
                np.testing.assert_allclose([e["sd"] for e in got["blocks"][block]], np.exp(sd), rtol=1e-5)
            self.assertEqual(got["season"], int(t["season"][row]))

    def test_learned_combinations(self):
        for exp, got in zip(self.expected["learned_points"], self.got["learned_points"]):
            self.close(exp["points"], got["points"], 1e-4, "learned points")
            for k in ("rim_share", "three_share", "tov", "fta"):
                self.close(exp[k], got[k], 1e-6, f"learned {k}")
        for kind, keys in (("learned_lineup", ("offense", "defense", "margin")),
                           ("learned_matchup", ("a_offense", "b_offense", "margin"))):
            for exp, got in zip(self.expected[kind], self.got[kind]):
                for k in keys:
                    self.close(exp["learned"][k], got["learned"][k], 1e-4, f"{kind} {k}")
                    for part in ("point", "low", "high", "assumption_low", "assumption_high"):
                        self.close(exp["band"][k][part], got["band"][k][part], 1e-3, f"{kind} band {k} {part}")
                for side, ev in exp["learned"]["events"].items():
                    for k, v in ev.items():
                        self.close(v, got["learned"]["events"][side][k], 1e-6, f"{kind} {side} {k}")
                self.assertEqual(exp["band"]["reasons"], got["band"]["reasons"])

    def test_missing_piece_forecast(self):
        # the search's exact forecast is the band's point (the printed number), in Python and in the page
        for exp, got in zip(self.expected["learned_lineup"], self.got["learned_lineup"]):
            for k in ("offense", "defense", "margin"):
                self.close(got["search"][k], got["band"][k]["point"], 1e-9, f"search {k} vs the page's band")
                self.close(got["search"][k], exp["band"][k]["point"], 1e-3, f"search {k} vs python")
            self.close(got["search"]["network"] + got["search"]["learned"] + got["search"]["combinations"],
                       got["search"]["margin"], 1e-9, "search parts")
        for exp, got in zip(self.expected["learned_matchup"], self.got["learned_matchup"]):   # against Team B
            for k in ("a_offense", "b_offense", "margin"):
                self.close(got["search"][k], got["band"][k]["point"], 1e-9, f"search {k} vs the page's band")
                self.close(got["search"][k], exp["band"][k]["point"], 1e-3, f"search {k} vs python")
            for part in ("point", "low", "high"):
                self.close(got["searchBand"][part], got["band"]["margin"][part], 1e-9, f"search range {part}")


if __name__ == "__main__":
    unittest.main()
