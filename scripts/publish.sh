#!/usr/bin/env bash
# Package the large outputs and upload them as GitHub release assets.
#
#   scripts/publish.sh raw     source PDFs/Excel  -> release "raw-files"   (once; they do not change)
#   scripts/publish.sh data    long CSVs, Parquet, series, dashboard DB, OCR cache -> release "data-<date>"
#
# GitHub limits a release asset to 2 GB, so the 8 GB of source files go up as
# year-range tars of at most ~1.9 GB each (PDFs do not compress; plain tar).
# Everything else is zstd-compressed. Needs `gh` logged in with push access
# to reclaimchennai/NCRB.
set -euo pipefail
cd "$(dirname "$0")/.."
REPO=reclaimchennai/NCRB
DIST=dist
mkdir -p "$DIST"

release() {  # tag title notes
  gh release view "$1" -R "$REPO" >/dev/null 2>&1 || gh release create "$1" -R "$REPO" --title "$2" --notes "$3"
}

case "${1:-}" in
raw)
  # year ranges chosen so each tar stays under the asset limit (see catalog/files.csv for sizes)
  ranges="cii:1953:1998 cii:1999:2022 cii:2023:2024 adsi:1967:2024 psi:1995:2010 psi:2011:2024"
  release raw-files "Source files from ncrb.gov.in" \
"Every PDF, Excel and Word file listed on the NCRB publication pages, as downloaded on 30 Sep–1 Oct 2026.
Unpack into the repository root to get raw/<publication>/<year>/<listing>/<file>.
catalog/files.csv in the repository lists every file with its source URL and SHA-256."
  for r in $ranges; do
    IFS=: read -r pub y0 y1 <<<"$r"
    name="ncrb-raw-$pub-$y0-$y1.tar"
    if [[ ! -f $DIST/$name ]]; then
      dirs=$(for y in $(seq "$y0" "$y1"); do [[ -d raw/$pub/$y ]] && echo "raw/$pub/$y"; done)
      tar -cf "$DIST/$name" $dirs
    fi
    gh release upload raw-files "$DIST/$name" -R "$REPO" --clobber
    echo "uploaded $name"
  done
  ;;
data)
  tag="data-$(date +%Y.%m.%d)"
  release "$tag" "Extracted data $(date +%Y-%m-%d)" \
"Tables extracted from the source files. The wide CSV and JSON of every table are in the repository under data/tables/; these assets hold the rest:

- ncrb-tables-long-<pub>.tar.zst: the tidy long CSV of every table (one row per cell)
- ncrb-cells-<pub>.parquet: all cells of a publication in one file
- ncrb-series-<pub>.tar.zst: tables stacked across years
- ncrb-dashboard.duckdb.zst: the database behind the dashboard
- ncrb-ocr-cache.tar.zst: raw output of the OCR model for each scanned page read so far

Quality per year: docs/COVERAGE.md."
  for pub in cii adsi psi; do
    find data/tables/$pub -name '*.long.csv' -print0 | tar --null -cf - -T - | zstd -q -T0 -19 --long=27 -f -o "$DIST/ncrb-tables-long-$pub.tar.zst"
    cp data/combined/${pub}_cells.parquet "$DIST/ncrb-cells-$pub.parquet"
    tar -cf - data/series/$pub | zstd -q -T0 -19 --long=27 -f -o "$DIST/ncrb-series-$pub.tar.zst"
  done
  zstd -q -T0 -10 -f data/web/ncrb.duckdb -o "$DIST/ncrb-dashboard.duckdb.zst"
  [[ -d data/ocr_cache ]] && tar -cf - data/ocr_cache | zstd -q -T0 -19 -f -o "$DIST/ncrb-ocr-cache.tar.zst"
  gh release upload "$tag" -R "$REPO" --clobber \
    "$DIST"/ncrb-tables-long-*.tar.zst "$DIST"/ncrb-cells-*.parquet "$DIST"/ncrb-series-*.tar.zst \
    "$DIST"/ncrb-dashboard.duckdb.zst $( [[ -f $DIST/ncrb-ocr-cache.tar.zst ]] && echo "$DIST/ncrb-ocr-cache.tar.zst" )
  echo "uploaded $tag"
  ;;
*)
  echo "usage: $0 raw|data" >&2; exit 2 ;;
esac
