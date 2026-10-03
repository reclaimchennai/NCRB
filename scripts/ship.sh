#!/usr/bin/env bash
# Upload the dashboard to raw without rsync: for links where macOS's openrsync stalls on thousands of
# files or a 1 GB file. Code goes as one tar stream; the database in 50 MB chunks, each retried on its
# own and checked by SHA-256 when reassembled. Then the same restart as deploy.sh.
#
#   scripts/ship.sh          code + database
#   scripts/ship.sh --code   code only
#   scripts/ship.sh --db     database only
set -euo pipefail
cd "$(dirname "$0")/.."
HOST=parag@raw
DEST=projects/ncrb
SSH="ssh -o ConnectTimeout=20 -o ServerAliveInterval=10 -o ServerAliveCountMax=6"
retry() { local n=0; until "$@"; do n=$((n + 1)); [ $n -ge 12 ] && return 1; echo "  retry $n"; sleep 8; done; }

# send a local file in chunks (each resent until it arrives whole; chunks already there are skipped), then
# reassemble it on the server as $2 and check its SHA-256
put() {
  local src=$1 dst=$2 chunk=${3:-10m} sum tmp
  sum=$(shasum -a 256 "$src" | cut -d' ' -f1)
  tmp=$(mktemp -d)
  split -b "$chunk" "$src" "$tmp/part."
  $SSH $HOST "mkdir -p $DEST/.upload"
  for p in "$tmp"/part.*; do
    local name size have
    name=$(basename "$p"); size=$(stat -f %z "$p")
    have=$($SSH $HOST "stat -c %s $DEST/.upload/$name 2>/dev/null || echo 0" || echo 0)
    [ "$have" = "$size" ] && continue
    retry timeout 180 scp -q -o ConnectTimeout=20 -o ServerAliveInterval=5 -o ServerAliveCountMax=3 "$p" "$HOST:$DEST/.upload/$name"
  done
  rm -rf "$tmp"
  retry $SSH $HOST "cd $DEST && cat .upload/part.* > '$dst' && echo '$sum  $dst' | sha256sum -c --quiet && rm -rf .upload"
}

python3 scripts/inline_sprite.py >/dev/null
python3 scripts/stamp_kit.py

if [[ "${1:-}" != "--db" ]]; then
  echo "code"
  TAR=$(mktemp -t ncrb-web).tgz
  COPYFILE_DISABLE=1 tar --exclude __pycache__ -czf "$TAR" api web deploy ARCHITECTURE.md
  put "$TAR" ncrb-web.tgz 10m
  # safe to repeat: a dropped connection after a good unpack must not fail the retry
  retry $SSH $HOST "cd $DEST && { [ ! -f ncrb-web.tgz ] || { tar -xzf ncrb-web.tgz && rm ncrb-web.tgz; }; }"
  rm -f "$TAR"
fi

if [[ "${1:-}" != "--code" ]]; then
  echo "database"
  put data/web/ncrb.duckdb data/web/ncrb.duckdb.new 25m
  retry $SSH $HOST "cd $DEST/data/web && { [ ! -f ncrb.duckdb.new ] || mv ncrb.duckdb.new ncrb.duckdb; } && echo 'database replaced'"
fi

$SSH $HOST "cd $DEST && { [ -x .venv/bin/uvicorn ] || python3 -m venv .venv; } \
  && .venv/bin/pip install -q -r deploy/requirements.txt \
  && install -m 644 deploy/ncrb.service ~/.config/systemd/user/ncrb.service \
  && systemctl --user daemon-reload && systemctl --user enable -q ncrb && systemctl --user restart ncrb \
  && sleep 3 && curl -sf http://127.0.0.1:5072/healthz"
echo; echo "shipped"
