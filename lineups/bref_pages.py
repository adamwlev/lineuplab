"""Basketball Reference pages, parsed: schedules, box scores, player bios and play-by-play into possessions.

Shared by the database updater (lineups.ingest, which downloads the pages and is not in the public
repository) and the rebuild from saved pages (lineups.page_possessions, lineups.pbp_ids). Split out of
lineups.ingest on 2026-10-19, unchanged.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from bs4 import BeautifulSoup

PLAYER_HREF = re.compile(r"/players/./([a-z0-9]+)\.html")
PERIOD_Q = re.compile(r"^(\d+)(?:st|nd|rd|th) Q$")
PERIOD_OT = re.compile(r"^(\d+)(?:st|nd|rd|th) OT$")
CLOCK = re.compile(r"^(\d+):(\d+(?:\.\d+)?)$")
FT_NUMBER = re.compile(r"(\d+) of (\d+)")
HEIGHT = re.compile(r"\b(\d+)-(\d+)\b")


@dataclass(frozen=True)
class GameListing:
    game_id: str
    game_date: dt.date
    away_team: str
    home_team: str
    away_points: int
    home_points: int
    playoffs: bool


@dataclass(frozen=True)
class PlayerRef:
    bref_id: str
    name: str
    starter: bool
    minutes: float = 0.0


@dataclass(frozen=True)
class PlayerBio:
    bref_id: str
    first_name: str
    last_name: str
    position: float
    height_inches: int | None


@dataclass(frozen=True)
class ParsedPossession:
    quarter: int
    time_left_start: float
    time_left_end: float
    away_team_ball: bool
    turnover: bool
    points_scored: int
    scorer_bref_id: str | None
    away_players: tuple[str, ...]
    home_players: tuple[str, ...]
    texts: str
    cell_texts: str = ""      # each event cell's text as the original scraper stored it (stripped, lowercased)


@dataclass(frozen=True)
class ParsedGame:
    away_roster: Mapping[str, PlayerRef]
    home_roster: Mapping[str, PlayerRef]
    possessions: tuple[ParsedPossession, ...]
    technical_points: tuple[int, int] | None = None
    repairs: tuple[str, ...] = ()


class ParseError(RuntimeError):
    """A whole game is rejected rather than leaving a partial database row."""


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def parse_schedule_index(html: str) -> list[str]:
    soup = _soup(html)
    paths = []
    for a in soup.select("div.filter a[href]"):
        href = a.get("href", "")
        if re.search(r"/leagues/NBA_\d{4}_games-[a-z]+\.html$", href):
            paths.append(href)
    return list(dict.fromkeys(paths))


def parse_schedule_month(html: str) -> list[GameListing]:
    soup = _soup(html)
    table = soup.select_one("table#schedule")
    if table is None:
        raise ParseError("schedule table not found")
    games: list[GameListing] = []
    playoffs = False
    for tr in table.select("tr"):
        header = tr.find("th", attrs={"data-stat": "date_game"})
        date_text = header.get_text(" ", strip=True) if header else ""
        if date_text == "Playoffs":
            playoffs = True
            continue
        link = tr.select_one("td[data-stat=box_score_text] a[href]")
        if link is None or not date_text or date_text == "Date":
            continue
        away = tr.select_one("td[data-stat=visitor_team_name]")
        home = tr.select_one("td[data-stat=home_team_name]")
        away_pts = tr.select_one("td[data-stat=visitor_pts]")
        home_pts = tr.select_one("td[data-stat=home_pts]")
        if any(x is None for x in (away, home, away_pts, home_pts)):
            continue
        try:
            game_date = dt.datetime.strptime(date_text, "%a, %b %d, %Y").date()
            ap, hp = int(away_pts.get_text(strip=True)), int(home_pts.get_text(strip=True))
        except ValueError:
            continue
        game_id = Path(link.get("href", "")).stem
        if not re.fullmatch(r"\d{9}[A-Z]{3}", game_id):
            raise ParseError(f"unexpected Basketball Reference game id: {game_id!r}")
        games.append(GameListing(
            game_id, game_date, away.get_text(" ", strip=True),
            home.get_text(" ", strip=True), ap, hp, playoffs))
    return games


def _player_id(tag) -> str | None:
    if tag is None:
        return None
    match = PLAYER_HREF.search(tag.get("href", ""))
    return match.group(1) if match else None


def _parse_box_table(table) -> dict[str, PlayerRef]:
    players: dict[str, PlayerRef] = {}
    starter = True
    for tr in table.select("tbody tr"):
        if "thead" in (tr.get("class") or []):
            starter = False
            continue
        a = tr.select_one("th[data-stat=player] a[href]")
        bref_id = _player_id(a)
        if bref_id:
            mp = tr.select_one("td[data-stat=mp]")
            minute_text = mp.get_text(strip=True) if mp else ""
            minute_match = CLOCK.match(minute_text)
            minutes = (_clock(minute_text) / 60.0 if minute_match else 0.0)
            players[bref_id] = PlayerRef(
                bref_id, a.get_text(" ", strip=True), starter, minutes)
    if len(players) < 5 or sum(p.starter for p in players.values()) != 5:
        raise ParseError("box score did not yield exactly five starters")
    return players


def parse_boxscore(html: str) -> tuple[dict[str, PlayerRef], dict[str, PlayerRef]]:
    soup = _soup(html)
    tables = [t for t in soup.find_all("table")
              if t.get("id", "").endswith("game-basic")]
    if len(tables) != 2:
        raise ParseError(f"expected two basic box-score tables, found {len(tables)}")
    return _parse_box_table(tables[0]), _parse_box_table(tables[1])


POSITION = {
    "point guard": 1.0, "shooting guard": 2.0, "small forward": 3.0,
    "power forward": 4.0, "center": 5.0, "guard": 1.5,
    "guard-forward": 2.5, "forward": 3.5, "forward-center": 4.5,
}


def parse_position(text: str) -> float:
    value = text.lower().replace("position:", "").split("▪", 1)[0].strip()
    value = value.replace(", and ", " and ").replace(",", " and ")
    parts = [p.strip() for p in re.split(r"\s+and\s+", value) if p.strip()]
    vals = [POSITION[p] for p in parts[:2] if p in POSITION]
    if not vals:
        return 3.0
    return vals[0] if len(vals) == 1 else 0.75 * vals[0] + 0.25 * vals[1]


def parse_player_bio(bref_id: str, html: str) -> PlayerBio:
    soup = _soup(html)
    h1 = soup.select_one("h1 span")
    meta = soup.select_one("div#meta")
    if h1 is None or meta is None:
        raise ParseError(f"player metadata missing for {bref_id}")
    name = h1.get_text(" ", strip=True).split()
    if len(name) < 2:
        raise ParseError(f"player name malformed for {bref_id}")
    text = meta.get_text(" ", strip=True)
    position_match = re.search(r"Position:\s*(.*?)\s*(?:▪|Shoots:)", text)
    position = parse_position(position_match.group(1)) if position_match else 3.0
    height_match = HEIGHT.search(text)
    height = (int(height_match.group(1)) * 12 + int(height_match.group(2))
              if height_match else None)
    return PlayerBio(bref_id, name[0], " ".join(name[1:]), position, height)


def _period_number(text: str, overtime_count: int) -> tuple[int | None, int]:
    q = PERIOD_Q.match(text)
    if q:
        return int(q.group(1)), overtime_count
    ot = PERIOD_OT.match(text)
    if ot:
        number = int(ot.group(1))
        return 4 + number, max(overtime_count, number)
    return None, overtime_count


def _period_rows(soup: BeautifulSoup) -> list[tuple[int, list]]:
    table = soup.select_one("table#pbp")
    if table is None:
        raise ParseError("play-by-play table not found")
    periods: list[tuple[int, list]] = []
    current: list | None = None
    overtime_count = 0
    for tr in table.select("tr"):
        heads = tr.find_all("th")
        cells = tr.find_all("td")
        if len(heads) == 1 and not cells:
            period, overtime_count = _period_number(
                heads[0].get_text(" ", strip=True), overtime_count)
            if period is not None:
                current = []
                periods.append((period, current))
            continue
        if current is not None and cells:
            current.append(tr)
    if len(periods) < 4:
        raise ParseError(f"expected at least four periods, found {len(periods)}")
    return periods


def _event_side_and_text(tr) -> tuple[str | None, str]:
    cells = tr.find_all("td")
    if len(cells) == 2:
        return None, cells[1].get_text(" ", strip=True)
    if len(cells) != 6:
        return None, ""
    away = cells[1].get_text(" ", strip=True)
    home = cells[5].get_text(" ", strip=True)
    if away:
        return "away", away
    if home:
        return "home", home
    return None, ""


def _linked_player_ids(tr) -> list[str]:
    return [pid for pid in (_player_id(a) for a in tr.select("a[href]")) if pid]


def determine_period_starters(rows: Sequence, away_roster: Mapping[str, PlayerRef],
                              home_roster: Mapping[str, PlayerRef]) -> tuple[set[str], set[str]]:
    """Infer a period's opening five from first appearances and substitutions."""
    seen = {"away": set(), "home": set()}
    first_sub: dict[str, bool] = {}
    away_ids, home_ids = set(away_roster), set(home_roster)
    for tr in rows:
        _, text = _event_side_and_text(tr)
        # Bench players and coaches can receive technical fouls; appearing in
        # that row is not evidence that the linked person is on the floor.
        if "technical" in text.lower() or "ejected from game" in text.lower():
            continue
        ids = _linked_player_ids(tr)
        for pid in ids:
            if pid in away_ids:
                seen["away"].add(pid)
            elif pid in home_ids:
                seen["home"].add(pid)
        if " enters the game for " in text.lower() and len(ids) >= 2:
            new_player, old_player = ids[0], ids[1]
            first_sub.setdefault(old_player, True)
            first_sub.setdefault(new_player, False)

    def starters(side: str) -> set[str]:
        ids = seen[side]
        result = (ids - set(first_sub)) | {
            pid for pid, was_outgoing in first_sub.items()
            if was_outgoing and pid in ids
        }
        # Rarely, a player stays on court for the whole period without a
        # recorded event (most often in overtime). PBP cannot identify him.
        # Exclude players whose first substitution role proves they began on
        # the bench, then fill the missing slot with the highest-minute
        # remaining player from the box score. This is deterministic and is
        # used only when the event evidence yields fewer than five players.
        if len(result) < 5:
            roster = away_roster if side == "away" else home_roster
            explicit_bench = {pid for pid, outgoing in first_sub.items()
                              if not outgoing}
            candidates = set(roster) - result - explicit_bench
            ranked = sorted(
                candidates,
                key=lambda pid: (-roster[pid].minutes, pid))
            result.update(ranked[:5 - len(result)])
        if len(result) != 5:
            raise ParseError(
                f"could not infer {side} period starters: {len(result)} {sorted(result)}")
        return result
    return starters("away"), starters("home")


def _clock(text: str) -> float:
    match = CLOCK.match(text)
    if not match:
        raise ParseError(f"unrecognized game clock: {text!r}")
    return int(match.group(1)) * 60 + float(match.group(2))


def _continuation_after_make(rows: Sequence, index: int, clock_text: str) -> bool:
    """Whether a made field goal is followed by an and-one at the same clock."""
    shooter = _linked_player_ids(rows[index])[:1]
    side, _ = _event_side_and_text(rows[index])
    for later in rows[index + 1:]:
        cells = later.find_all("td")
        if len(cells) != 6 or cells[0].get_text(strip=True) != clock_text:
            break
        later_side, original = _event_side_and_text(later)
        text = original.lower()
        # Rounded timestamps can contain the opponent's next scoring play.
        # Require the actual shooter's one-and-one attempt, not just a foul.
        if (later_side == side and _linked_player_ids(later)[:1] == shooter
                and "free throw 1 of 1" in text and "technical" not in text):
            return True
        if "turnover" in text or ("-pt" in text and "shot" in text):
            break
    return False


def _normalize_free_throw_order(rows: Sequence) -> list:
    """Normalize same-clock FT trips, including their bookkeeping rebounds.

    Group each attempt with an immediately following team rebound so an
    out-of-order final miss cannot terminate the trip early. Substitution slots
    retain their order. Opponent inbound turnovers inserted between attempts
    move after the trip. Technical and nonfinal-FT team rebounds are dead-ball
    bookkeeping and are removed from possession/outcome accounting.
    """
    rows = list(rows)
    out = []
    i = 0
    while i < len(rows):
        cells = rows[i].find_all("td")
        clock_text = cells[0].get_text(strip=True) if cells else ""
        j = i + 1
        while j < len(rows) and rows[j].find_all("td")[0].get_text(strip=True) == clock_text:
            j += 1
        group = rows[i:j]
        nodes = []
        k = 0
        while k < len(group):
            side, original = _event_side_and_text(group[k])
            text = original.lower()
            ft = FT_NUMBER.search(text) if "free throw" in text else None
            node = [group[k]]
            if "free throw" in text and k + 1 < len(group):
                _, nxt = _event_side_and_text(group[k + 1])
                if "rebound by team" in nxt.lower():
                    if ("technical" not in text
                            and (ft is None or ft.group(1) == ft.group(2))):
                        node.append(group[k + 1])
                    k += 1
            nodes.append(node)
            k += 1
        trips = {}
        for k, node in enumerate(nodes):
            side, text = _event_side_and_text(node[0])
            ft = FT_NUMBER.search(text) if "free throw" in text.lower() else None
            if ft:
                key = (side, tuple(_linked_player_ids(node[0])[:1]), ft.group(2),
                       "flagrant" in text.lower())
                trips.setdefault(key, []).append((k, int(ft.group(1))))
        for slots in trips.values():
            numbers = [n for _, n in slots]
            if len(numbers) != len(set(numbers)):
                continue  # two separate trips cannot be safely merged
            sorted_nodes = [nodes[k] for k, _ in sorted(slots, key=lambda x: x[1])]
            for (k, _), node in zip(slots, sorted_nodes):
                nodes[k] = node
        for (side, _, _, _), slots in trips.items():
            if len(slots) < 2:
                continue
            first, last = slots[0][0], slots[-1][0]
            deferred = []
            for k in range(first + 1, last):
                other_side, text = _event_side_and_text(nodes[k][0]) if nodes[k] else (None, "")
                if other_side not in (None, side) and "turnover" in text.lower():
                    deferred.extend(nodes[k])
                    nodes[k] = []
            nodes[last].extend(deferred)
        out.extend(row for node in nodes for row in node)
        i = j
    return out


def parse_play_by_play(html: str, away_roster: Mapping[str, PlayerRef],
                       home_roster: Mapping[str, PlayerRef],
                       repairs: list | None = None) -> tuple[ParsedPossession, ...]:
    """Possessions of one game. With repairs (a list), two page defects that otherwise reject the game are
    repaired and listed there:

    - a missing row that changes possession (usually a rebound after a missed free throw): an event of the
      other offense arrives while points are pending, so the pending possession ends there;
    - a repeated substitution row: the outgoing player is already off and the incoming one already on.
    """
    soup = _soup(html)
    periods = _period_rows(soup)
    possessions: list[ParsedPossession] = []

    for quarter, rows in periods:
        rows = _normalize_free_throw_order(rows)
        if quarter == 1:
            away_floor = {p.bref_id for p in away_roster.values() if p.starter}
            home_floor = {p.bref_id for p in home_roster.values() if p.starter}
        else:
            away_floor, home_floor = determine_period_starters(
                rows, away_roster, home_roster)
        period_length = 720.0 if quarter <= 4 else 300.0
        time_left_start = period_length
        point_counter = 0
        scorer = None
        scoring_side = None
        scoring_floor = None
        texts: list[str] = []
        turnover = False

        def append_possession(offense_side, time_left):
            if scoring_side is not None and offense_side != scoring_side:
                raise ParseError(f"possession mixes both offenses in period {quarter} at {time_left}")
            away, home = away_floor, home_floor
            if scorer is not None:
                expected = away if offense_side == "away" else home
                if scorer not in expected:
                    # A made FT followed by an offensive rebound can precede
                    # a dead-ball substitution. The schema permits one five
                    # per possession: use the observed scoring lineup when
                    # the scorer has since left, never invent a replacement.
                    away, home = scoring_floor
                expected = away if offense_side == "away" else home
                if scorer not in expected:
                    raise ParseError(f"scorer {scorer} absent at his scoring event")
            if len(away) != 5 or len(home) != 5:
                raise ParseError("possession ended without two five-player lineups")
            possessions.append(ParsedPossession(
                quarter, time_left_start, time_left,
                offense_side == "away", turnover, point_counter, scorer,
                tuple(sorted(away)), tuple(sorted(home)), "/n".join(t for t, _ in texts),
                "/n".join(c for _, c in texts)))

        def close_pending(time_left):
            """Repair: end the pending scored possession before the current event (already in texts)."""
            nonlocal time_left_start, point_counter, scorer, texts, turnover, scoring_side, scoring_floor
            current, event_turnover, turnover = texts.pop(), turnover, turnover_before
            append_possession(scoring_side, time_left)
            time_left_start = time_left
            point_counter, scorer, texts, turnover = 0, None, [current], event_turnover
            scoring_side, scoring_floor = None, None

        for index, tr in enumerate(rows):
            cells = tr.find_all("td")
            if len(cells) == 2:
                # Held-ball jumps and period markers must not erase points
                # already accumulated in an unfinished possession.
                jump_text = cells[1].get_text(" ", strip=True).lower()
                jump_ids = _linked_player_ids(tr)
                if scoring_side and "gains possession" in jump_text and jump_ids:
                    winner = jump_ids[-1]
                    winner_side = "away" if winner in away_roster else "home"
                    if winner_side != scoring_side:
                        append_possession(scoring_side, _clock(cells[0].get_text(strip=True)))
                        time_left_start = _clock(cells[0].get_text(strip=True))
                        point_counter, scorer, texts, turnover = 0, None, [], False
                        scoring_side, scoring_floor = None, None
                continue
            if len(cells) != 6:
                continue
            clock_text = cells[0].get_text(strip=True)
            time_left = _clock(clock_text)
            side, original_text = _event_side_and_text(tr)
            if side is None or not original_text:
                continue
            text = original_text.lower()
            texts.append((text, cells[1 if side == "away" else 5].get_text().strip().lower()))
            ids = _linked_player_ids(tr)

            if " enters the game for " in text:
                if len(ids) < 2:
                    raise ParseError(f"substitution without two player ids: {original_text}")
                new_player, old_player = ids[0], ids[1]
                floor = away_floor if side == "away" else home_floor
                if old_player not in floor and new_player in floor and repairs is not None:
                    repairs.append(f"repeated substitution, period {quarter} at {clock_text}: {original_text}")
                    continue
                if old_player not in floor:
                    raise ParseError(
                        f"substitution removes absent player {old_player}: {original_text}")
                floor.remove(old_player)
                floor.add(new_player)
                if len(floor) != 5:
                    raise ParseError(f"substitution produced {len(floor)} players")
                continue

            if "technical" in text:
                # Ignore the technical event/FT itself, but preserve any
                # ordinary and-one sequence it interrupts at the same clock.
                # Clearing the accumulator here loses the made basket.
                texts.pop()
                continue

            complete, turnover_before = False, turnover
            offense_side = side
            if any(token in text for token in
                   ("traveling", "steals", "turnover", "stolen")):
                complete, turnover = True, True
            elif "violation by" in text and "(jump ball)" in text:
                complete = True
            elif "defensive rebound" in text:
                complete = True
                offense_side = "home" if side == "away" else "away"
            elif " makes " in text:
                if scoring_side is not None and scoring_side != side:
                    if repairs is None:
                        raise ParseError(f"scoring side changed mid-possession at {clock_text}")
                    repairs.append(f"possession change without a row, period {quarter} at {clock_text}")
                    close_pending(time_left)
                scorer = ids[0] if ids else None
                scoring_side = side
                scoring_floor = (set(away_floor), set(home_floor))
                diff_cell = cells[2] if side == "away" else cells[4]
                diff = diff_cell.get_text(strip=True).replace("+", "")
                if diff:
                    try:
                        point_counter += int(diff)
                    except ValueError as exc:
                        raise ParseError(f"bad score change {diff!r}") from exc
                if "free throw" in text:
                    ft = FT_NUMBER.search(text)
                    complete = bool(ft and ft.group(1) == ft.group(2)
                                    and "flagrant" not in text)
                else:
                    complete = not _continuation_after_make(rows, index, clock_text)

            if complete and repairs is not None and scoring_side is not None and offense_side != scoring_side:
                repairs.append(f"possession change without a row, period {quarter} at {clock_text}")
                close_pending(time_left)
            if complete:
                append_possession(offense_side, time_left)
                time_left_start = time_left
                point_counter, scorer, texts, turnover = 0, None, [], False
                scoring_side, scoring_floor = None, None

        # A missed final FT with only a team rebound at 0:00 still owns any
        # earlier made FTs. Preserve that scored possession at the horn.
        if point_counter:
            append_possession(scoring_side, 0.0)

    if len(possessions) < 100:
        raise ParseError(f"implausibly few possessions parsed: {len(possessions)}")
    return tuple(possessions)


def parse_game(box_html: str, pbp_html: str, repair: bool = False) -> ParsedGame:
    """repair: repair the page defects parse_play_by_play lists, instead of rejecting the game."""
    away, home = parse_boxscore(box_html)
    repairs = [] if repair else None
    possessions = parse_play_by_play(pbp_html, away, home, repairs)
    technical = [0, 0]
    for _, rows in _period_rows(_soup(pbp_html)):
        for row in rows:
            side, text = _event_side_and_text(row)
            if side and "makes technical free throw" in text.lower():
                cell = row.find_all("td")[2 if side == "away" else 4]
                technical[side == "home"] += int(cell.get_text(strip=True).replace("+", "") or 0)
    return ParsedGame(away, home, possessions, tuple(technical), tuple(repairs or ()))


def ordinary_score(parsed: ParsedGame) -> tuple[int, int]:
    return (
        sum(p.points_scored for p in parsed.possessions if p.away_team_ball),
        sum(p.points_scored for p in parsed.possessions if not p.away_team_ball),
    )


def validate_score(listing: GameListing, parsed: ParsedGame,
                   max_technical_gap: int = 5) -> tuple[int, int]:
    """Require parsed points to match after allowing unassigned technical FTs."""
    away, home = ordinary_score(parsed)
    gap = listing.away_points - away, listing.home_points - home
    valid = (gap == parsed.technical_points if parsed.technical_points is not None
             else all(0 <= value <= max_technical_gap for value in gap))
    if not valid:
        raise ParseError(
            f"ordinary-possession score {away}-{home} is not compatible with "
            f"official {listing.away_points}-{listing.home_points}; gap={gap}; "
            f"recorded technical points={parsed.technical_points}")
    return gap


def _ordered_player_ids(ids: Iterable[str], db_players: Mapping[str, tuple]) -> tuple[int, ...]:
    remaining = {pid: db_players[pid] for pid in ids}
    result: list[int] = []
    if len(remaining) != 5:
        raise ParseError(f"expected five unique players, got {len(remaining)}")
    for target_position in range(1, 6):
        def key(pid: str):
            internal_id, position, height = remaining[pid]
            position = 3.0 if position is None else float(position)
            height = 100 if height is None else int(height)
            return abs(target_position - position), height, internal_id
        chosen = min(remaining, key=key)
        result.append(int(remaining.pop(chosen)[0]))
    return tuple(result)
