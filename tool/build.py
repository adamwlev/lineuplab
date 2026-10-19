"""Rebuild tool/five.html by injecting a fresh ratings export into the page.

The page carries its data inline as a `const DATA = {...}` literal, so a
refit is a two-step:

    python -u experiments/export_ratings.py --out experiments/cache/ratings.json
    python -u tool/build.py

then republish tool/five.html to the SAME artifact URL (see tool/README.md).

Kept deliberately dumb -- a textual splice between two known anchors -- so the
page stays hand-editable. It validates the result rather than trusting it: the
JSON must parse, the anchors must be unique, and the required keys must be
present, because a silently truncated DATA literal produces a page that loads
and then shows every rating as NaN.
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "tool", "five.html")
RATINGS = os.path.join(ROOT, "experiments", "cache", "ratings.json")
HEAD, TAIL = "const DATA = ", ";\nconst P = DATA.players"
REQUIRED = ("players", "dims", "synergy", "calib", "exp_off", "exp_def", "meta")


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else RATINGS
    data = json.load(open(src))
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        sys.exit(f"ratings.json is missing {missing}")
    page = open(PAGE).read()
    if page.count(HEAD) != 1 or page.count(TAIL) != 1:
        sys.exit("anchors are not unique -- did the page's script header change?")
    i = page.index(HEAD)
    j = page.index(TAIL)
    out = page[:i] + HEAD + json.dumps(data, separators=(",", ":")) + page[j:]

    check = re.search(r"const DATA = (\{.*?\});\nconst P = DATA", out, re.S)
    if not check:
        sys.exit("post-splice DATA literal did not match -- refusing to write")
    json.loads(check.group(1))          # raises if truncated
    open(PAGE, "w").write(out)
    print(f"{PAGE}  {os.path.getsize(PAGE)/1e6:.2f} MB  "
          f"{len(data['players'])} players from {src}")


if __name__ == "__main__":
    main()
