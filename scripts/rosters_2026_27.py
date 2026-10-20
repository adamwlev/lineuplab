"""2026-27 opening-night rosters for the tool's team picker, with each team's projected starting five.

Rosters: Wikipedia's NBA roster templates ("Template:<Team> roster", CC BY-SA 4.0), through the MediaWiki API.
Not Sports Reference: our permission request to them is pending (reports/v1_launch_2026_10_19.md).

Projected starters: the latest published reporting, checked 2026-10-19 (STARTERS, with SOURCES). The base is
Sports Illustrated's projections for all 30 teams (17 October). Three teams use newer team reporting:
- the Warriors: Steve Kerr's leaning five;
- the Kings: Bleacher Report's five, without Ben Simmons;
- the Jazz: Jaxson Hayes for the injured Jusuf Nurkic.
Every projected starter must be on his team's roster. A rookie projected to start has no NBA data, so a
teammate stands in. The stand-in is the rostered player who played in 2025-26, not two-way or listed as injured,
who shares the rookie's position and started the largest share of his games, starts / max(games, 20), if
that share is at least a quarter; otherwise the teammate with the largest share at any position. A start is
being in the game's first possession (nba_pages.possessions). The page
says so in that slot. Each player enters at his latest season, and the five run guard to centre.

    PYTHONPATH=. python -u scripts/rosters_2026_27.py --fetch   # download the 30 templates (kept), then build
    PYTHONPATH=. python -u scripts/rosters_2026_27.py           # rebuild from the kept templates

Writes tool/rosters_2026_27.json (tool/build_lineups.py puts the fives in the page) and prints every rostered
name it could not match.
"""
import argparse
import datetime as dt
import json
import re
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

import psycopg2
import requests

from lineups import paths
from lineups.db import dsn
from lineups.sources import SOURCE

TEAMS = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers",
         "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets",
         "Indiana Pacers", "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
         "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
         "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
         "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"]
RAW = paths.CACHE / "rosters_2026_10_19"
SOURCES = {
    "si": ("Sports Illustrated, Ranking All 30 Projected NBA Starting Lineups in 2026-27 (17 October 2026)",
           "https://www.si.com/nba/ranking-all-30-projected-nba-starting-lineups-from-worst-to-best"),
    "gsw": ("Golden State of Mind: the five Steve Kerr is leaning towards (October 2026)",
            "https://www.goldenstateofmind.com/warriors-news/112634/warriors-coach-steve-kerr-starting-lineup"),
    "sac": ("Bleacher Report, Ranking Every NBA Team's Starting Lineup Ahead of Preseason (1 October 2026); "
            "Sabonis, LaVine and Murray played the preseason finale",
            "https://bleacherreport.com/articles/25504515-ranking-every-nba-teams-starting-lineup-ahead-preseason"),
    "uta": ("Jake Weinbach and the Jazz's preseason starters: Jaxson Hayes for the injured Jusuf Nurkic (October 2026)",
            "https://x.com/JWeinbachNBA/status/2111297997032329379"),
}
STARTERS = {    # checked 2026-10-19; SI and Bleacher Report agree on 23 teams
    "Atlanta Hawks": ("si", ["Jalen Johnson", "Nickeil Alexander-Walker", "CJ McCollum", "Onyeka Okongwu", "Dyson Daniels"]),
    "Boston Celtics": ("si", ["Jayson Tatum", "Derrick White", "Paul George", "Neemias Queta", "Payton Pritchard"]),
    "Brooklyn Nets": ("si", ["Michael Porter Jr.", "Julius Randle", "Day'Ron Sharpe", "Egor Dëmin", "Mikel Brown Jr."]),
    "Charlotte Hornets": ("si", ["Brandon Miller", "Kon Knueppel", "Coby White", "Naz Reid", "Moussa Diabaté"]),
    "Chicago Bulls": ("si", ["Josh Giddey", "Matas Buzelis", "Caleb Wilson", "Norman Powell", "Nic Claxton"]),
    "Cleveland Cavaliers": ("si", ["Donovan Mitchell", "James Harden", "Evan Mobley", "Jarrett Allen", "Peyton Watson"]),
    "Dallas Mavericks": ("si", ["Cooper Flagg", "Kyrie Irving", "Max Christie", "P.J. Washington", "Daniel Gafford"]),
    "Denver Nuggets": ("si", ["Nikola Jokić", "Jamal Murray", "Aaron Gordon", "Cameron Johnson", "Christian Braun"]),
    "Detroit Pistons": ("si", ["Cade Cunningham", "Jalen Duren", "Ausar Thompson", "John Collins", "Duncan Robinson"]),
    "Golden State Warriors": ("gsw", ["Stephen Curry", "Brandin Podziemski", "Gui Santos", "Yaxel Lendeborg", "Draymond Green"]),
    "Houston Rockets": ("si", ["Kevin Durant", "Amen Thompson", "Alperen Şengün", "Fred VanVleet", "Jabari Smith Jr."]),
    "Indiana Pacers": ("si", ["Tyrese Haliburton", "Pascal Siakam", "Ivica Zubac", "Andrew Nembhard", "Aaron Nesmith"]),
    "Los Angeles Clippers": ("si", ["Darius Garland", "Rui Hachimura", "Derrick Jones Jr.", "Brook Lopez", "Keaton Wagler"]),
    "Los Angeles Lakers": ("si", ["Luka Dončić", "Austin Reaves", "Walker Kessler", "Quentin Grimes", "Jake LaRavia"]),
    "Memphis Grizzlies": ("si", ["Cameron Boozer", "Zach Edey", "Cedric Coward", "Jaylen Wells", "Ty Jerome"]),
    "Miami Heat": ("si", ["Giannis Antetokounmpo", "Bam Adebayo", "Andrew Wiggins", "Davion Mitchell", "Klay Thompson"]),
    "Milwaukee Bucks": ("si", ["Tyler Herro", "Myles Turner", "Jaime Jaquez Jr.", "Ryan Rollins", "Kyle Kuzma"]),
    "Minnesota Timberwolves": ("si", ["Anthony Edwards", "LaMelo Ball", "Rudy Gobert", "Jaden McDaniels", "Jonathan Kuminga"]),
    "New Orleans Pelicans": ("si", ["Zion Williamson", "Trey Murphy III", "Herbert Jones", "Dejounte Murray", "Yves Missi"]),
    "New York Knicks": ("si", ["Jalen Brunson", "Karl-Anthony Towns", "OG Anunoby", "Josh Hart", "Mikal Bridges"]),
    "Oklahoma City Thunder": ("si", ["Shai Gilgeous-Alexander", "Jalen Williams", "Chet Holmgren", "Cason Wallace", "Isaiah Hartenstein"]),
    "Orlando Magic": ("si", ["Paolo Banchero", "Franz Wagner", "Desmond Bane", "Wendell Carter Jr.", "Jalen Suggs"]),
    "Philadelphia 76ers": ("si", ["Tyrese Maxey", "Jaylen Brown", "LeBron James", "Joel Embiid", "V.J. Edgecombe"]),
    "Phoenix Suns": ("si", ["Devin Booker", "Dillon Brooks", "Jalen Green", "Miles Bridges", "Oso Ighodaro"]),
    "Portland Trail Blazers": ("si", ["Deni Avdija", "Ja Morant", "Damian Lillard", "Donovan Clingan", "Toumani Camara"]),
    "Sacramento Kings": ("sac", ["Darius Acuff Jr.", "Zach LaVine", "De'Andre Hunter", "Keegan Murray", "Domantas Sabonis"]),
    "San Antonio Spurs": ("si", ["Victor Wembanyama", "Stephon Castle", "De'Aaron Fox", "Devin Vassell", "Julian Champagnie"]),
    "Toronto Raptors": ("si", ["Kawhi Leonard", "Scottie Barnes", "RJ Barrett", "Immanuel Quickley", "Jakob Poeltl"]),
    "Utah Jazz": ("uta", ["Keyonte George", "Darryn Peterson", "Lauri Markkanen", "Jaren Jackson Jr.", "Jaxson Hayes"]),
    "Washington Wizards": ("si", ["Trae Young", "Anthony Davis", "AJ Dybantsa", "Alex Sarr", "Kyshawn George"]),
}
POSITION_ORDER = {"G": 0, "PG": 0, "SG": 0, "GF": 1, "F": 2, "SF": 2, "PF": 2, "FC": 3, "C": 4}
OUT = Path(__file__).resolve().parent.parent / "tool" / "rosters_2026_27.json"
API = "https://en.wikipedia.org/w/api.php"
AGENT = "LineupLab/1.0 (https://lineuplab.dev; https://github.com/adamwlev/lineuplab)"
MIN_GAMES = 20                                       # the stand-ins' start share
SUFFIX = {"jr", "sr", "ii", "iii", "iv", "v"}
ALIASES = {"Jakob Pöltl": "Jakob Poeltl", "Sviatoslav Mykhailiuk": "Svi Mykhailiuk",   # Wikipedia -> nba.players,
           "Bub Carrington": "Carlton Carrington", "Hansen Yang": "Yang Hansen"}        # checked 2026-10-19


def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    words = re.sub(r"[^a-z0-9]+", " ", s).split()
    while len(words) > 2 and words[-1] in SUFFIX:       # only a trailing suffix: "V. J. Edgecombe" keeps his V
        words.pop()
    return " ".join(words)


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = AGENT
    for team in TEAMS:
        r = session.get(API, params=dict(action="parse", page=f"Template:{team} roster", prop="wikitext|revid",
                                         format="json", formatversion=2), timeout=30)
        r.raise_for_status()
        body = r.json()
        if "parse" not in body:
            raise SystemExit(f"{team}: {body.get('error')}")
        body["fetched"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        (RAW / f"{team.replace(' ', '_')}.json").write_text(json.dumps(body))
        print("fetched", team, body["parse"]["revid"], flush=True)
        time.sleep(1.0)


def roster(team):
    body = json.loads((RAW / f"{team.replace(' ', '_')}.json").read_text())
    players = []
    for block in re.findall(r"\{\{\s*player2\s*\|(.*?)\}\}", body["parse"]["wikitext"], flags=re.S):
        fields = {}
        for part in block.split("|"):
            if "=" in part:
                k, v = part.split("=", 1)
                fields[k.strip()] = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", v).strip()
        name = f"{fields.get('first', '')} {fields.get('last', '')}".strip()
        players.append(dict(name=name, pos=fields.get("pos", ""), two_way=fields.get("note", "").upper() == "TW",
                            injured=fields.get("inj", "").lower() == "yes"))
    return dict(team=team, revid=body["parse"]["revid"], fetched=body["fetched"], players=players)


def season_of(day):
    return day.year + 1 if day.month >= 8 else day.year


def starts():
    """{(pid, season): games started}, a start being a place in the game's first possession, 2023-24 to 2025-26."""
    counts = defaultdict(int)
    with psycopg2.connect(dsn()) as conn, conn.cursor() as cur:
        cur.execute("""select distinct on (p.game_id) g.game_date, p.away_player_1_id, p.away_player_2_id,
                              p.away_player_3_id, p.away_player_4_id, p.away_player_5_id, p.home_player_1_id,
                              p.home_player_2_id, p.home_player_3_id, p.home_player_4_id, p.home_player_5_id
                       from nba_pages.possessions p join nba.games g on g.id = p.game_id
                       where g.game_date >= '2023-08-01'
                       order by p.game_id, p.quarter, p.time_left_start desc, p.id""")
        for day, *ten in cur.fetchall():
            for pid in ten:
                counts[pid, season_of(day)] += 1
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="download the 30 roster templates first")
    if ap.parse_args().fetch:
        fetch()
    meta = json.loads((SOURCE["export"] / "meta.json").read_text())
    P = meta["players"]
    seasons = defaultdict(dict)             # pid -> season -> (games, possessions)
    for pid, season, off, de, games in zip(P["pid"], P["season"], P["offense_possessions"],
                                          P["defense_possessions"], P["games"]):
        seasons[pid][season] = (games, (off + de) / 2)
    with psycopg2.connect(dsn()) as conn, conn.cursor() as cur:
        cur.execute("select id, first_name, last_name from nba.players")
        people = cur.fetchall()
    index = defaultdict(list)
    for pid, first, last in people:
        if pid in seasons:                  # the tool can only use players it has a season for
            index[norm(f"{first} {last}")].append(pid)
            index[norm(f"{first} {last}").replace(" ", "")].append(pid)   # "V. J." is "VJ"
    started = starts()
    out, unmatched = [], []
    for team in TEAMS:
        r = roster(team)
        rows = []
        for p in r["players"]:
            key = norm(ALIASES.get(p["name"], p["name"]))
            hits = index.get(key) or index.get(key.replace(" ", ""), [])
            pid = max(hits, key=lambda q: max(seasons[q])) if hits else None
            if len(hits) > 1:
                print(f"  {team}: {p['name']} matches {hits}; took {pid} (latest season)")
            if pid is None:
                unmatched.append((team, p["name"]))
                rows.append(dict(p, pid=None))
                continue
            latest = max(seasons[pid])
            games, poss = seasons[pid][latest]
            share = started[pid, latest] / max(games, MIN_GAMES)
            rows.append(dict(p, pid=pid, season=latest, starts=started[pid, latest], games=games,
                             share=round(share, 3), per_game=round(poss / max(games, 1), 1)))
        source, names = STARTERS[team]
        five = []
        for name in names:                  # each projected starter must be on the opening-night roster
            key = norm(ALIASES.get(name, name))
            hits = [x for x in rows if norm(ALIASES.get(x["name"], x["name"])).replace(" ", "") == key.replace(" ", "")]
            if len(hits) != 1:
                raise SystemExit(f"{team}: projected starter {name} is not on the roster once ({len(hits)})")
            five.append(hits[0])
        five.sort(key=lambda x: POSITION_ORDER.get(x["pos"], 2))
        letters = lambda x: set(x["pos"].replace("P", "").replace("S", ""))
        spare = sorted((x for x in rows if x["pid"] is not None and x not in five and not x["two_way"] and not x["injured"]
                        and x["season"] == meta["latest_season"]),
                       key=lambda x: (-x["share"], -x["per_game"]))
        picks = []
        for x in five:
            if x["pid"] is not None:
                picks.append(dict(pid=x["pid"], season=x["season"], name=x["name"]))
                continue
            near = [y for y in spare if letters(y) & letters(x) and y["share"] >= 0.25]
            sub = near[0] if near else spare[0]
            spare.remove(sub)
            picks.append(dict(pid=sub["pid"], season=sub["season"], name=sub["name"], stands_in_for=x["name"]))
        short = team.split()[-1] if team != "Portland Trail Blazers" else "Trail Blazers"
        out.append(dict(team=team, short=short, revid=r["revid"], fetched=r["fetched"], source=source,
                        five=picks, roster=rows))
        shown = " · ".join(x["name"] + (f" (for {x['stands_in_for']})" if "stands_in_for" in x else "") for x in picks)
        print(f"{short:14s} {shown}")
    doc = dict(rosters="Wikipedia NBA roster templates (CC BY-SA 4.0), fetched through the MediaWiki API",
               fetched=min(t["fetched"] for t in out), starters={k: dict(text=v[0], url=v[1]) for k, v in SOURCES.items()},
               rule=__doc__.split("\n\n")[2].replace("\n", " "), teams=out)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"\n{len(unmatched)} rostered names not in the tool (rookies have no NBA data yet):")
    for team, name in unmatched:
        print(f"  {team}: {name}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
