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
from lineups.sources import SOURCE  # noqa: E402

EXPORT = SOURCE["export"]
PLACEHOLDER = "/*LINEUP_MODEL_JS*/"
SIZES = "/*FILE_SIZES*/null"                     # the page's loading progress counts against these
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
    page = page.replace(PLACEHOLDER, model).replace(SIZES, json.dumps(sizes))
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
