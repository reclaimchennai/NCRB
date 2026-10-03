#!/usr/bin/env bash
# Convert every .doc under raw/ to .docx with LibreOffice (in a throwaway Debian container), cached in
# data/docx_cache/<first 16 hex of the source SHA-256>.docx. macOS textutil flattens Word tables into
# running text; LibreOffice keeps each cell. extract.py uses the cached .docx when there is one.
set -euo pipefail
cd "$(dirname "$0")/.."
IN=$(mktemp -d); OUT=$(mktemp -d)
find raw -iname "*.doc" | while read -r f; do
  sha=$(shasum -a 256 "$f" | cut -c1-16)
  [ -f "data/docx_cache/$sha.docx" ] || cp "$f" "$IN/$sha.doc"
done
if [ -n "$(ls -A "$IN")" ]; then
  docker run --rm -v "$IN":/in:ro -v "$OUT":/out debian:stable-slim bash -c \
    "apt-get update -qq >/dev/null && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends libreoffice-writer-nogui >/dev/null 2>&1 \
     && cd /in && for f in *.doc; do soffice --headless --convert-to docx --outdir /out \"\$f\" >/dev/null 2>&1; done"
  mkdir -p data/docx_cache && cp "$OUT"/*.docx data/docx_cache/
fi
echo "$(ls data/docx_cache | wc -l) converted files in data/docx_cache"
