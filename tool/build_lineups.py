"""Build the Lineup Lab page: inline tool/lineup_model.js into tool/lineups.html.

The built page goes beside the release export (scripts/export_release.py). It
fetches meta.json, and weights.txt and players.txt (the .bin files base64-encoded,
because artifacts serve text and media but not raw binary), by relative path:

    PYTHONPATH=. python -u tool/build_lineups.py [--out DIR] [--site]

Output: the selected release's export directory (lineups.sources: release_export_2026_10_12, or the clean
rebuild's release_export): lineups.html, and model.html (the model details page) copied beside it. With --out,
a new directory instead, with the export's meta.json copied in, so a page change leaves the export untouched.

The page is a fragment for the artifact host, which wraps it in its own frame. --site (with --out) builds the
public site instead (lineuplab.dev, tool/wrangler.jsonc): index.html as a whole document, with the frame's base
styles, a description and link preview, and the icon; model.html links back to it.
"""
import argparse
import base64
import json
from pathlib import Path

import shutil
import sys

TOOL = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOL.parent))
from lineups import paths  # noqa: E402
from lineups.sources import SOURCE  # noqa: E402

EXPORT = SOURCE["export"]
TEAM_SEASONS = paths.CLEAN / "team_seasons_2026_10_20" / "team_seasons.json"   # scripts/team_seasons.py
PLACEHOLDER = "/*LINEUP_MODEL_JS*/"
SIZES = "/*FILE_SIZES*/null"                     # the page's loading progress counts against these
ROSTERS = "/*ROSTERS*/null"                      # the 2026–27 teams' projected fives (scripts/rosters_2026_27.py)
TEAMS = "/*TEAM_SEASONS*/null"                   # the best five's rosters, past (scripts/team_seasons.py) and 2026–27
SITE = "https://lineuplab.dev/"
DESCRIPTION = ("Pick any five NBA players, each as of one season since 2001-02, and see how they would do together: "
               "offense, defense and net per 100 possessions, the basketball reasons, and an honest range.")
SITE_HEAD = f"""<meta name="description" content="{DESCRIPTION}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="Lineup Lab">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:image" content="{SITE}preview.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>body {{ margin: 0; }} [hidden] {{ display: none !important; }} img {{ max-width: 100%; }}</style>
"""                                              # the last line: what the artifact host's frame supplied


def team_seasons(rosters, meta, known):
    """The best five's rosters by season: past team-seasons, then 2026-27's opening-night rosters (two-way players
    left out, and rookies, who have no data), the 13 who played the most in their latest season."""
    doc = json.loads(TEAM_SEASONS.read_text())
    size, thin = doc["roster_size"], meta["band"]["thin_possessions"]
    offense = dict(zip(zip(meta["players"]["pid"], meta["players"]["season"]), meta["players"]["offense_possessions"]))
    out = {}
    for t in doc["team_seasons"]:
        y = t["season"]
        out.setdefault(str(y), []).append(dict(team=t["team"], roster=[[p, y] for p, _ in t["roster"]], thin=t["thin"],
                                               ref=[[p, y] for p in t["most_used"]["five"]],
                                               label=f"most used, {t['most_used']['possessions']:,} possessions"))
    upcoming = []
    for t in rosters["teams"]:
        cands = sorted(((x["pid"], x["season"]) for x in t["roster"] if x["pid"] is not None and not x["two_way"]
                        and offense.get((x["pid"], x["season"]), 0) >= thin), key=lambda q: -offense[q])
        subs = [f'{x["name"].split()[-1]} in place of the rookie {x["stands_in_for"]}' for x in t["five"] if "stands_in_for" in x]
        upcoming.append(dict(team=t["team"], roster=[list(q) for q in cands[:size]], thin=0,
                             ref=[[x["pid"], x["season"]] for x in t["five"]],
                             label="projected starters" + (f" ({'; '.join(subs)})" if subs else "")))
    out[str(max(map(int, out)) + 1)] = upcoming
    bad = [(y, t["team"]) for y, ts in out.items() for t in ts
           if len(t["roster"]) < 5 or any(tuple(x) not in known for x in t["roster"] + t["ref"])]
    if bad:
        raise SystemExit(f"team-seasons with fewer than five players or player-seasons the release lacks: {bad[:5]}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, help="a new directory to build into (default: the export directory)")
    ap.add_argument("--site", action="store_true", help="the public site: index.html as a whole document (needs --out)")
    args = ap.parse_args()
    out_dir = args.out or EXPORT
    if args.site and out_dir == EXPORT:
        raise SystemExit("--site needs --out")
    if out_dir != EXPORT:
        out_dir.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(EXPORT / "meta.json", out_dir / "meta.json")
    page = (TOOL / "lineups.html").read_text()
    model = (TOOL / "lineup_model.js").read_text()
    if page.count(PLACEHOLDER) != 1:
        raise SystemExit("the page must hold exactly one model placeholder")
    if "</script" in model.lower():
        raise SystemExit("the model source contains a closing script tag")
    for name in ("meta.json", "weights.bin", "players.bin"):
        if not (EXPORT / name).exists():
            raise SystemExit(f"{name} missing: run scripts/export_release.py first")
    for name in ("weights", "players"):
        (out_dir / f"{name}.txt").write_bytes(base64.b64encode((EXPORT / f"{name}.bin").read_bytes()))
    if page.count(SIZES) != 1:
        raise SystemExit("the page must hold exactly one file-size placeholder")
    sizes = {name: (out_dir / name if name != "meta.json" else EXPORT / name).stat().st_size
             for name in ("meta.json", "weights.txt", "players.txt")}
    if page.count(ROSTERS) != 1:
        raise SystemExit("the page must hold exactly one rosters placeholder")
    rosters = json.loads((TOOL / "rosters_2026_27.json").read_text())
    meta = json.loads((EXPORT / "meta.json").read_text())
    known = set(zip(meta["players"]["pid"], meta["players"]["season"]))
    teams = [dict(team=t["team"], five=[[x["pid"], x["season"]] + ([x["stands_in_for"]] if "stands_in_for" in x else [])
                                        for x in t["five"]]) for t in rosters["teams"]]
    missing = [(t["team"], x) for t in teams for x in t["five"] if tuple(x[:2]) not in known]
    if missing or any(len(t["five"]) != 5 for t in teams):
        raise SystemExit(f"rosters: player-seasons the release lacks, or a short five: {missing}")
    page = page.replace(PLACEHOLDER, model).replace(SIZES, json.dumps(sizes))
    page = page.replace(ROSTERS, json.dumps(dict(fetched=rosters["fetched"], teams=teams), ensure_ascii=False))
    if page.count(TEAMS) != 1:
        raise SystemExit("the page must hold exactly one team-seasons placeholder")
    page = page.replace(TEAMS, json.dumps(team_seasons(rosters, meta, known), ensure_ascii=False, separators=(",", ":")))
    details = (TOOL / "model.html").read_text()
    if args.site:
        if page.count("</title>\n") != 1 or details.count("</title>\n") != 1:
            raise SystemExit("each page must hold exactly one title")
        page = '<!doctype html>\n<html lang="en">\n' + page.replace("</title>\n", "</title>\n" + SITE_HEAD) + "</html>\n"
        details = details.replace("</title>\n", '</title>\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n')
        for name in ("favicon.svg", "preview.png"):
            shutil.copyfile(TOOL / name, out_dir / name)
    out = out_dir / ("index.html" if args.site else "lineups.html")
    out.write_text(page)
    (out_dir / "model.html").write_text(details)
    print(out, round(out.stat().st_size / 1e3), "kB")


if __name__ == "__main__":
    main()
