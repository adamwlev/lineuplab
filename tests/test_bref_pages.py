import datetime as dt
import unittest

from bs4 import BeautifulSoup

from lineups.bref_pages import (
    ParseError,
    GameListing,
    ParsedGame,
    ParsedPossession,
    PlayerRef,
    _ordered_player_ids,
    _normalize_free_throw_order,
    _continuation_after_make,
    determine_period_starters,
    parse_boxscore,
    parse_player_bio,
    parse_play_by_play,
    parse_position,
    parse_schedule_index,
    parse_schedule_month,
    validate_score,
)


class BrefIngestTests(unittest.TestCase):
    @staticmethod
    def row(side, text, clock="1:00.0", points=0):
        cells = [clock, "", "", "0-0", "", ""]
        cells[1 if side == "away" else 5] = text
        if points:
            cells[2 if side == "away" else 4] = f"+{points}"
        return BeautifulSoup("<tr>" + "".join(f"<td>{x}</td>" for x in cells)
                             + "</tr>", "html.parser").tr

    @staticmethod
    def player(pid):
        return f'<a href="/players/a/{pid}.html">{pid}</a>'

    def parse_events(self, events, repairs=None):
        away = {f"away{i}": PlayerRef(f"away{i}", f"A{i}", i < 5, 40-i)
                for i in range(6)}
        home = {f"home{i}": PlayerRef(f"home{i}", f"H{i}", i < 5, 40-i)
                for i in range(6)}
        html = '<table id="pbp">'
        for q, suffix in [(1, "st"), (2, "nd"), (3, "rd"), (4, "th")]:
            html += f'<tr><th>{q}{suffix} Q</th></tr>'
            for i in range(26):
                side = "away" if i % 2 == 0 else "home"
                html += str(self.row(side, self.player(side+"0") + " makes 2-pt jump shot",
                                     clock=f"{11-i//3}:{50-i%3*10:02d}.0", points=2))
            if q == 1:
                html += "".join(str(r) for r in events)
            html += '<tr><td>0:00.0</td><td>End of quarter</td></tr>'
        return parse_play_by_play(html + '</table>', away, home, repairs)

    def test_missing_rebound_after_free_throw_is_repaired_and_listed(self):
        a, h = self.player("away0"), self.player("home0")
        events = [self.row("away", a + " makes free throw 1 of 2", points=1),
                  self.row("away", a + " misses free throw 2 of 2"),
                  self.row("home", "Turnover by " + h + " (bad pass)")]   # the home rebound row is missing
        with self.assertRaises(ParseError):
            self.parse_events(events)
        repairs = []
        pp = self.parse_events(events, repairs)[26:28]
        self.assertEqual([(p.away_team_ball, p.points_scored, p.turnover) for p in pp],
                         [(True, 1, False), (False, 0, True)])
        self.assertEqual(pp[1].texts, "turnover by home0 (bad pass)")
        self.assertEqual(len(repairs), 1)

    def test_repeated_substitution_is_ignored_and_listed(self):
        sub = self.row("home", self.player("home5") + " enters the game for " + self.player("home0"))
        with self.assertRaises(ParseError):
            self.parse_events([sub, sub])
        repairs = []
        self.parse_events([sub, sub], repairs)
        self.assertEqual(len(repairs), 1)
        self.assertIn("repeated substitution", repairs[0])

    def test_cell_texts_keep_the_original_scraper_form(self):
        a, b = self.player("away0"), self.player("away1")
        events = [self.row("away", a + " makes 2-pt jump shot (assist by " + b + ")", points=2)]
        p = self.parse_events(events)[26]
        self.assertEqual(p.texts, "away0 makes 2-pt jump shot (assist by away1 )")
        self.assertEqual(p.cell_texts, "away0 makes 2-pt jump shot (assist by away1)")

    def test_technical_miss_rebound_does_not_interrupt_and_one(self):
        a, h = self.player("away0"), self.player("home0")
        events = [self.row("away", a + " makes 2-pt dunk", points=2),
                  self.row("home", h + " shooting foul"),
                  self.row("home", h + " misses technical free throw"),
                  self.row("away", "Defensive rebound by Team"),
                  self.row("away", a + " makes free throw 1 of 1", points=1)]
        p = self.parse_events(events)[26]
        self.assertEqual((p.points_scored, p.away_team_ball), (3, True))
        self.assertNotIn("rebound by team", p.texts)

    def test_opponent_turnover_between_free_throws_is_deferred(self):
        a, h = self.player("away0"), self.player("home0")
        events = [self.row("away", a + " makes free throw 1 of 2", points=1),
                  self.row("home", "Turnover by " + h + " (bad pass)"),
                  self.row("away", a + " makes free throw 2 of 2", points=1)]
        pp = self.parse_events(events)[26:28]
        self.assertEqual([(p.away_team_ball, p.points_scored, p.turnover) for p in pp],
                         [(True, 2, False), (False, 0, True)])

    def test_scored_possession_survives_substitution_after_offensive_rebound(self):
        a, h = self.player("away0"), self.player("home0")
        events = [self.row("away", a + " makes free throw 1 of 2", points=1),
                  self.row("away", a + " misses free throw 2 of 2"),
                  self.row("away", "Offensive rebound by Team"),
                  self.row("away", self.player("away5") + " enters the game for " + a),
                  self.row("away", self.player("away1") + " misses 2-pt shot", "0:45.0"),
                  self.row("home", "Defensive rebound by " + h, "0:44.0")]
        p = self.parse_events(events)[26]
        self.assertEqual(p.points_scored, 1)
        self.assertIn("away0", p.away_players)
        self.assertNotIn("away5", p.away_players)

    def test_scored_free_throws_are_preserved_at_period_end(self):
        a = self.player("away0")
        events = [self.row("away", a + " makes free throw 1 of 2", "0:00.0", 1),
                  self.row("away", a + " misses free throw 2 of 2", "0:00.0"),
                  self.row("away", "Offensive rebound by Team", "0:00.0")]
        p = self.parse_events(events)[26]
        self.assertEqual((p.quarter, p.time_left_end, p.points_scored), (1, 0, 1))

    def test_and_one_is_matched_to_shooter_even_when_clocks_repeat(self):
        a, h = self.player("away0"), self.player("home0")
        events = [self.row("home", h + " makes 2-pt layup", points=2),
                  self.row("away", a + " makes 2-pt layup", points=2),
                  self.row("home", h + " shooting foul"),
                  self.row("away", a + " makes free throw 1 of 1", points=1)]
        pp = self.parse_events(events)[26:28]
        self.assertEqual([(p.away_team_ball, p.points_scored) for p in pp],
                         [(False, 2), (True, 3)])

    def test_out_of_order_final_miss_carries_its_rebound(self):
        a, h = self.player("away0"), self.player("home0")
        events = [self.row("away", a + " misses free throw 1 of 3"),
                  self.row("away", "Offensive rebound by Team"),
                  self.row("away", a + " misses free throw 3 of 3"),
                  self.row("home", "Defensive rebound by Team"),
                  self.row("away", a + " makes free throw 2 of 3", points=1)]
        p = self.parse_events(events)[26]
        self.assertEqual((p.points_scored, p.away_team_ball), (1, True))
        self.assertNotIn("offensive rebound by team", p.texts)

    def test_recorded_technical_total_replaces_arbitrary_score_tolerance(self):
        listing = GameListing("202510210OKC", dt.date(2025,10,21), "A", "H", 0, 6, False)
        self.assertEqual(validate_score(listing, ParsedGame({}, {}, (), (0, 6))), (0, 6))
        with self.assertRaises(ParseError):
            validate_score(listing, ParsedGame({}, {}, (), (0, 5)))

    def test_schedule_discovery_and_completed_game(self):
        index = """
        <div class="filter"><div><a href="/leagues/NBA_2026_games-october.html">Oct</a></div></div>
        """
        self.assertEqual(parse_schedule_index(index),
                         ["/leagues/NBA_2026_games-october.html"])
        month = """
        <table id="schedule"><tbody>
          <tr><th data-stat="date_game">Tue, Oct 21, 2025</th>
            <td data-stat="visitor_team_name">Houston Rockets</td>
            <td data-stat="visitor_pts">124</td>
            <td data-stat="home_team_name">Oklahoma City Thunder</td>
            <td data-stat="home_pts">125</td>
            <td data-stat="box_score_text"><a href="/boxscores/202510210OKC.html">Box Score</a></td></tr>
          <tr><th data-stat="date_game">Wed, Oct 22, 2025</th>
            <td data-stat="visitor_team_name">A</td><td data-stat="visitor_pts"></td>
            <td data-stat="home_team_name">B</td><td data-stat="home_pts"></td>
            <td data-stat="box_score_text"></td></tr>
        </tbody></table>
        """
        games = parse_schedule_month(month)
        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].game_id, "202510210OKC")
        self.assertEqual(games[0].game_date, dt.date(2025, 10, 21))
        self.assertEqual((games[0].away_points, games[0].home_points), (124, 125))

    def test_boxscore_starters_and_reserves(self):
        def table(team):
            starters = "".join(
                f'<tr><th data-stat="player"><a href="/players/a/{team}s{i}.html">S{i}</a></th></tr>'
                for i in range(5))
            return (f'<table id="box-{team}-game-basic"><tbody>{starters}'
                    '<tr class="thead"><th>Reserves</th></tr>'
                    f'<tr><th data-stat="player"><a href="/players/a/{team}b0.html">B0</a></th></tr>'
                    '</tbody></table>')
        away, home = parse_boxscore(table("aaa") + table("bbb"))
        self.assertEqual(sum(p.starter for p in away.values()), 5)
        self.assertFalse(away["aaab0"].starter)
        self.assertEqual(len(home), 6)

    def test_player_bio_and_position(self):
        html = """
        <h1><span>Cooper Flagg</span></h1>
        <div id="meta">Position: Small Forward and Power Forward ▪ Shoots: Right
          6-9, 205lb</div>
        """
        bio = parse_player_bio("flaggco01", html)
        self.assertEqual((bio.first_name, bio.last_name), ("Cooper", "Flagg"))
        self.assertEqual(bio.height_inches, 81)
        self.assertEqual(bio.position, 3.25)
        self.assertEqual(parse_position("Guard and Forward"), 2.0)

    def test_period_starters_from_first_substitution_direction(self):
        away_ids = [f"away{i}" for i in range(6)]
        home_ids = [f"home{i}" for i in range(6)]
        away = {p: PlayerRef(p, p, i < 5) for i, p in enumerate(away_ids)}
        home = {p: PlayerRef(p, p, i < 5) for i, p in enumerate(home_ids)}
        rows = []
        for side, ids in (("away", away_ids), ("home", home_ids)):
            for p in ids[:4]:
                cells = ["1:00", "", "", "0-0", "", ""]
                cells[1 if side == "away" else 5] = (
                    f'<a href="/players/a/{p}.html">{p}</a> misses 2-pt shot')
                rows.append(BeautifulSoup(
                    "<tr>" + "".join(f"<td>{x}</td>" for x in cells) + "</tr>",
                    "html.parser").tr)
            cells = ["0:30", "", "", "0-0", "", ""]
            cells[1 if side == "away" else 5] = (
                f'<a href="/players/a/{ids[5]}.html">bench</a> enters the game for '
                f'<a href="/players/a/{ids[4]}.html">starter</a>')
            rows.append(BeautifulSoup(
                "<tr>" + "".join(f"<td>{x}</td>" for x in cells) + "</tr>",
                "html.parser").tr)
        a, h = determine_period_starters(rows, away, home)
        self.assertEqual(a, set(away_ids[:5]))
        self.assertEqual(h, set(home_ids[:5]))

    def test_period_starter_fallback_uses_minutes_for_silent_player(self):
        away = {
            f"away{i}": PlayerRef(f"away{i}", f"A{i}", i < 5, 40 - i)
            for i in range(6)
        }
        home = {
            f"home{i}": PlayerRef(f"home{i}", f"H{i}", i < 5, 40 - i)
            for i in range(5)
        }
        rows = []
        for side, ids in (("away", list(away)[:4]), ("home", list(home))):
            for p in ids:
                cells = ["1:00", "", "", "0-0", "", ""]
                cells[1 if side == "away" else 5] = (
                    f'<a href="/players/a/{p}.html">{p}</a> misses 2-pt shot')
                rows.append(BeautifulSoup(
                    "<tr>" + "".join(f"<td>{x}</td>" for x in cells) + "</tr>",
                    "html.parser").tr)
        a, _ = determine_period_starters(rows, away, home)
        self.assertEqual(a, set(list(away)[:5]))

    def test_bench_technical_is_not_starter_evidence(self):
        away = {
            f"away{i}": PlayerRef(f"away{i}", f"A{i}", i < 5, 40 - i)
            for i in range(6)
        }
        home = {
            f"home{i}": PlayerRef(f"home{i}", f"H{i}", i < 5, 40 - i)
            for i in range(5)
        }
        rows = []
        for side, ids in (("away", list(away)[:5]), ("home", list(home))):
            for p in ids:
                cells = ["1:00", "", "", "0-0", "", ""]
                cells[1 if side == "away" else 5] = (
                    f'<a href="/players/a/{p}.html">{p}</a> misses 2-pt shot')
                rows.append(BeautifulSoup(
                    "<tr>" + "".join(f"<td>{x}</td>" for x in cells) + "</tr>",
                    "html.parser").tr)
        cells = ["0:30", '<a href="/players/a/away5.html">A5</a> technical foul',
                 "", "0-0", "", ""]
        rows.append(BeautifulSoup(
            "<tr>" + "".join(f"<td>{x}</td>" for x in cells) + "</tr>",
            "html.parser").tr)
        a, _ = determine_period_starters(rows, away, home)
        self.assertEqual(a, set(list(away)[:5]))

    def test_position_order_is_deterministic(self):
        players = {
            "a": (10, 5.0, 84), "b": (11, 1.0, 72), "c": (12, 3.0, 78),
            "d": (13, 2.0, 76), "e": (14, 4.0, 81),
        }
        self.assertEqual(_ordered_player_ids(players, players), (11, 13, 12, 14, 10))

    def test_score_validation_allows_only_unassigned_technical_points(self):
        possession = ParsedPossession(
            1, 720, 700, True, False, 2, None,
            ("a", "b", "c", "d", "e"),
            ("f", "g", "h", "i", "j"), "shot")
        parsed = ParsedGame({}, {}, (possession,))
        listing = GameListing(
            "202510210OKC", dt.date(2025, 10, 21), "A", "H", 3, 0, False)
        self.assertEqual(validate_score(listing, parsed), (1, 0))
        bad = GameListing(
            "202510210OKC", dt.date(2025, 10, 21), "A", "H", 1, 0, False)
        with self.assertRaises(ParseError):
            validate_score(bad, parsed)

    def test_out_of_order_free_throws_are_repaired_narrowly(self):
        rows = []
        for number in (1, 3, 2):
            html = (f'<tr><td>10:50.0</td><td><a href="/players/a/p1.html">P</a> '
                    f'makes free throw {number} of 3</td>'
                    '<td>+1</td><td>0-0</td><td></td><td></td></tr>')
            rows.append(BeautifulSoup(html, "html.parser").tr)
        fixed = _normalize_free_throw_order(rows)
        self.assertEqual(
            [int(row.find_all("td")[1].get_text().split()[-3]) for row in fixed],
            [1, 2, 3])

    def test_same_clock_technical_ft_is_not_an_and_one(self):
        make = BeautifulSoup(
            '<tr><td>1:00.0</td><td>P makes 2-pt shot</td><td>+2</td>'
            '<td>2-0</td><td></td><td></td></tr>', "html.parser").tr
        tech = BeautifulSoup(
            '<tr><td>1:00.0</td><td>Q makes technical free throw</td><td>+1</td>'
            '<td>3-0</td><td></td><td></td></tr>', "html.parser").tr
        self.assertFalse(_continuation_after_make([make, tech], 0, "1:00.0"))


if __name__ == "__main__":
    unittest.main()
