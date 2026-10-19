"""Player-season inputs equal the stores' origin-mode inputs (needs local caches)."""
import unittest

import numpy as np

from lineups import paths, players, release


@unittest.skipUnless((players.TABLE / "player_seasons.npz").exists() and release.STORE.exists(), "local caches absent")
class PlayerSeasonInputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from lineups.features import Store
        cls.seasons = players.PlayerSeasons()
        cls.store = Store(release.STORE)
        cls.normalizer = cls.store.normalizer(release.ORIGIN, "final")
        index = int(cls.store.schedule().query("tag == @release.ORIGIN").iloc[0].origin_index)
        cls.league = float(cls.store.offense_origins["league"][index])
        cls.index = index

    def fives(self, season, count=40, seed=0):
        t = self.seasons.table
        rows = np.flatnonzero(t["season"] == season)
        rng = np.random.default_rng(seed)
        return np.stack([rng.choice(rows, 5, replace=False) for _ in range(count)])

    def check(self, store, origin_index, query_day, season):
        off, de = self.fives(season), self.fives(season, seed=1)
        pid = self.seasons.table["pid"].astype(np.int64)
        new = self.seasons.batch(off, de, self.normalizer, self.league, self.store)
        old = store.batch(pid[off], pid[de], None, self.normalizer, origin_index=origin_index, query_day=query_day)
        old["league_capture"] = old["league_capture"] * 0 + np.float32(self.league)
        self.assertEqual(set(new), set(old))
        for key in new:
            with self.subTest(season=season, key=key):
                np.testing.assert_array_equal(new[key].numpy(), old[key].numpy())

    def test_latest_season_is_the_release_origin(self):
        self.check(self.store, self.index, None, 2026)

    def test_era_season_is_the_next_opening_night_in_the_era_store(self):
        from lineups.features import Store
        era = Store(release.SOURCE["era_store"])                              # the table's era source
        origin = era.schedule().query("tag == '2011q1'").iloc[0]
        self.check(era, int(origin.origin_index), int(np.datetime64(origin.start.date(), "D").astype(np.int64)), 2010)

    def test_relative_rule_is_the_identity_for_the_latest_season(self):
        off, de = self.fives(2026), self.fives(2026, seed=1)
        a = self.seasons.batch(off, de, self.normalizer, self.league, self.store, "as_was")
        b = self.seasons.batch(off, de, self.normalizer, self.league, self.store, "relative")
        for key in a:
            np.testing.assert_allclose(a[key].numpy(), b[key].numpy(), atol=1e-4, err_msg=key)

    def test_relative_rule_moves_an_older_season(self):
        off = self.fives(2008)
        a = self.seasons.batch(off, off, self.normalizer, self.league, self.store, "as_was")
        b = self.seasons.batch(off, off, self.normalizer, self.league, self.store, "relative")
        self.assertGreater(float((a["msg"] - b["msg"]).abs().max()), .1)

    def test_defaults(self):
        t = self.seasons.table
        active = int(t["pid"][np.flatnonzero(t["season"] == 2026)[0]])
        self.assertEqual(self.seasons.defaults[active], 2026)
        retired = set(t["pid"][t["season"] <= 2008].tolist()) - set(t["pid"][t["season"] >= 2009].tolist())
        pid = sorted(retired)[0]
        mine = np.flatnonzero(t["pid"] == pid)
        busiest = mine[np.argmax(t["offense_possessions"][mine] + t["defense_possessions"][mine])]
        self.assertEqual(self.seasons.defaults[pid], int(t["season"][busiest]))


if __name__ == "__main__":
    unittest.main()
