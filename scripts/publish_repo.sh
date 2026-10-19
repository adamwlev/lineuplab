#!/bin/zsh
# The public repository (github.com/adamwlev/lineuplab): this tree's committed HEAD, minus what stays private.
#
#   scripts/publish_repo.sh DEST "commit message"
#
# DEST is a clone of the public repository (a new directory becomes one). Its files are replaced by HEAD's,
# minus EXCLUDE, and the change is committed there under Adam's GitHub noreply address. Nothing is pushed:
# read `git -C DEST show --stat`, then `git -C DEST push`.
#
# Left out (Adam, 2026-10-19: MIT licence, no scrape scripts; and nothing derived from the data, as the
# request to Sports Reference says):
#   - the downloader: lineups/ingest.py, tests/test_ingest.py, scripts/rescrape_pages.py,
#     scripts/rescrape_pilot.py, scripts/after_download.sh;
#   - data: the golden test fixtures (rows from five 2020 games) and tool/five.html (the retired page,
#     which embeds its player data).
set -euo pipefail
DEST=${1:?usage: publish_repo.sh DEST "message"}; MSG=${2:?usage: publish_repo.sh DEST "message"}
REPO=${0:A:h:h}
EXCLUDE=(lineups/ingest.py tests/test_ingest.py scripts/rescrape_pages.py scripts/rescrape_pilot.py
         scripts/after_download.sh tool/five.html tests/fixtures/reference_2020q1_s17.npz
         tests/fixtures/reference_2020q1_s17.pt tests/fixtures/history_2020q1_final.npz)
NAME="Adam Levin"; EMAIL="6889910+adamwlev@users.noreply.github.com"
[[ -z $(git -C $REPO status --porcelain --untracked-files=no) ]] || { echo "commit first: HEAD is what is published" >&2; exit 1; }
for f in $EXCLUDE; do
  git -C $REPO cat-file -e HEAD:$f 2>/dev/null || { echo "not in HEAD: $f (update EXCLUDE)" >&2; exit 1; }
done
STAGE=$(mktemp -d)
git -C $REPO archive HEAD | tar -x -C $STAGE
for f in $EXCLUDE; do rm $STAGE/$f; done
# A private value must never leave: a password assignment (other than "<redacted>"), keys, tokens.
if grep -r -I -l -E "password\s*=\s*['\"]?[^<'\" ]|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|gh[ps]_[A-Za-z0-9]{30,}" $STAGE; then
  echo "secret-like text in the files above; nothing published" >&2; rm -rf $STAGE; exit 1
fi
mkdir -p $DEST
[[ -d $DEST/.git ]] || git -C $DEST init -q -b main
rsync -a --delete --exclude .git $STAGE/ $DEST/
rm -rf $STAGE
git -C $DEST add -A
git -C $DEST -c user.name="$NAME" -c user.email="$EMAIL" commit -q -m "$MSG"
git -C $DEST show --stat --format='%h %an <%ae>%n%s' HEAD | tail -4
