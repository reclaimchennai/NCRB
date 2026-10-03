# ncrb — NCRB data explorer

Every table the National Crime Records Bureau has published (Crime in India from
1953, Accidental Deaths & Suicides from 1967, Prison Statistics from 1995),
extracted into CSV/JSON/Parquet, plus a dashboard to search, chart and map them.

Data and pipeline: <https://github.com/reclaimchennai/NCRB> (see README.md and docs/).

## Where it runs

| | |
|---|---|
| Live | <https://ncrb.reclaimchennai.city> (the old <https://ncrb.reclaimchennai.city/> paths 308-redirect to the same path here) |
| Code | laptop repo `~/Desktop/projects/ncrb` (git, pushed to GitHub); on `raw` at `~/projects/ncrb` holds only `api/`, `web/`, `deploy/` and `data/web/ncrb.duckdb` |
| Process | `ncrb.service`, systemd `--user`, `uvicorn api.site:app`, 2 workers, `0.0.0.0:5072`, `MemoryMax=2G` |
| Ingress | Caddy: the `ncrb.reclaimchennai.city` block, `reverse_proxy host.docker.internal:5072`; `handle_path /ncrb/*` in the `cpi.reclaimchennai.city` block redirects to it |
| Firewall | `ufw allow from 172.16.0.0/12 to any port 5072 proto tcp` (the host.docker.internal double fix) |
| Health | `GET /healthz` counts tables in the database |

```bash
systemctl --user status ncrb
journalctl --user -u ncrb -f
curl -s http://127.0.0.1:5072/healthz
```

## Shape

```
raw/ PDFs + Excel (8 GB, laptop / GitHub release)
  -> python -m ncrb.extract   per-table CSV + JSON, indexes            (laptop)
  -> python -m ncrb.build     data/combined/*.parquet, series          (laptop)
  -> python -m ncrb.webdata   data/web/ncrb.duckdb (~1 GB, read-only)  (laptop)
  -> ./deploy.sh              rsync to raw, restart ncrb.service
     (scripts/ship.sh: the same without rsync, in retried chunks, for flaky links;
      --code / --db for one half)
browser -> Caddy -> uvicorn: api/main.py (FastAPI over DuckDB) + web/ (static, served by the same app)
```

Three pages share the one app:

| Page | Path | What |
|---|---|---|
| Tables | `/` (`web/index.html`, `web/js/`) | search, read, chart and map any extracted table (API-backed) |
| Trends | `/trends/` (`web/trends/`) | dashboard: one dataset, any State, UT or city, every year; play, snapshot, record |
| Chennai | `/chennai/` (`web/chennai/`) | the Chennai and Tamil Nadu story, same charts |
| Explore | `/explore/` (`web/explore/`) | every table printed in 3+ editions, joined across years (`python -m analysis.families` -> `web/data/explore/`, gitignored, rsynced by deploy.sh) |

Trends and Chennai are static: they read `web/data/trends/` (catalog, one
`index.json` per dataset, one JSON per place), written on the laptop by
`python -m analysis.export` from `analysis/engine.py`. They share `web/kit/`:

| File | What |
|---|---|
| `kit.css` | cpi's tokens and controls (pill fields, segmented, switch, timeline, card, capture buttons) plus a red heat ramp and day/night colours |
| `util.js` | DOM, formatting, scales, theme, tooltip (after cpi's util.js) |
| `grapher.js` | hand-rolled SVG charts: lines, bar rows, stacked rows, heatmap (number and % per cell), day/night clocks |
| `cards.js` | controls, the `Timeline` (fractional year position, smooth transitions, play) and the card with camera and video buttons |
| `capture.js` | PNG snapshot and MP4 recording (WebCodecs + vendored mp4-muxer, MediaRecorder fallback), every frame credited `@reclaimchennai` with its source (after cpi's capture.js) |
| `data.js`, `footer.js` | loading the trends JSON; sources and caveats |
| `sprite.svg` | Lucide/Tabler icons, inlined into both pages by `scripts/inline_sprite.py` |

Charts are pure functions of their inputs; animation is done by passing values
interpolated between two years on every frame, so play, scrubbing and video
recording are one code path and every recorded frame is what the screen showed.
`deploy.sh` runs `scripts/inline_sprite.py` and `scripts/stamp_kit.py` (one
content hash written as `?v=` into every kit import and asset link).

The Tables frontend is vanilla ES modules with hand-drawn SVG charts and no external
requests, in cpi's design language (same tokens, same validated palette). State
boundaries in `web/geo/` are cpi's copies of the datameet files (pre-2019 lines:
Jammu & Kashmir undivided, Ladakh not separate).

## Deploying a change

```bash
./deploy.sh          # code + database
./deploy.sh --code   # code only
```

`deploy.sh` stamps content hashes on the JS/CSS URLs bottom-up through the
import graph (util -> charts -> app -> index.html) because Cloudflare overrides
origin cache headers; a new URL is the only reliable cache-buster. The database
is uploaded as `ncrb.duckdb.new` and moved into place, so a half-copied file is
never opened. Paths are relative throughout the frontend (`document.baseURI`),
which is what lets the same build serve at `/ncrb/` and at a domain root.

## Gotchas

- DuckDB connections are not thread-safe: `api/main.py` keeps one read-only
  connection per thread. Two uvicorn workers each open the file read-only, which
  DuckDB allows.
- The Caddyfile was edited in place (`open(..., "r+")`), not replaced, to keep the
  container's bind mount on the same inode; see `caddy/ARCHITECTURE.md`.
- Figures from scanned years (before ~2000) are OCR: the UI marks them (badge,
  shaded years in series charts). Do not remove those marks.
