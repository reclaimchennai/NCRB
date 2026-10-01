#!/usr/bin/env bash
# Ship the dashboard to raw: stamp asset versions, sync code and the DuckDB file, restart.
#
#   ./deploy.sh            code + data
#   ./deploy.sh --code     code only (the 1 GB database is left alone)
#
# Asset versions are content hashes taken bottom-up through the import graph
# (util.js -> charts.js -> app.js -> index.html): rewriting a module's imports
# changes its own bytes, so hashing app.js before its imports are restamped
# would publish a stale version. Cloudflare overrides origin cache headers, so
# a new URL is the only reliable cache-buster.
set -euo pipefail
cd "$(dirname "$0")"
HOST=parag@raw
DEST=projects/ncrb
SSH='ssh -o ServerAliveInterval=15 -o ServerAliveCountMax=4'

hash_of() { shasum -a 256 "$1" | cut -c1-10; }
stamp_import() { perl -0pi -e "s{(['\"]\\./$2\\.js)(\\?v=[0-9a-f]+)?(['\"])}{\$1?v=$3\$3}g" "$1"; }
stamp_html() { perl -0pi -e "s{(\"$1)(\\?v=[0-9a-f]+)?\"}{\$1?v=$2\"}g" web/index.html; }

H_UTIL=$(hash_of web/js/util.js)
stamp_import web/js/charts.js util "$H_UTIL"; stamp_import web/js/app.js util "$H_UTIL"
H_CHARTS=$(hash_of web/js/charts.js)
stamp_import web/js/app.js charts "$H_CHARTS"
stamp_html js/app.js "$(hash_of web/js/app.js)"
stamp_html css/app.css "$(hash_of web/css/app.css)"
echo "assets stamped"

$SSH $HOST "mkdir -p $DEST/data/web"
rsync -az --delete --timeout=60 -e "$SSH" --exclude __pycache__ api web deploy "$HOST:$DEST/"
if [[ "${1:-}" != "--code" ]]; then
  rsync -az --timeout=120 --partial -e "$SSH" data/web/ncrb.duckdb "$HOST:$DEST/data/web/ncrb.duckdb.new"
  $SSH $HOST "mv $DEST/data/web/ncrb.duckdb.new $DEST/data/web/ncrb.duckdb"
fi
$SSH $HOST "cd $DEST && { [ -x .venv/bin/uvicorn ] || python3 -m venv .venv; } \
  && .venv/bin/pip install -q -r deploy/requirements.txt \
  && install -m 644 deploy/ncrb.service ~/.config/systemd/user/ncrb.service \
  && systemctl --user daemon-reload && systemctl --user enable -q ncrb && systemctl --user restart ncrb \
  && sleep 3 && curl -sf http://127.0.0.1:5072/healthz"
echo; echo "deployed"
