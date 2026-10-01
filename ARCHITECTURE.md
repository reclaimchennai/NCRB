# ncrb — NCRB data explorer

Every table the National Crime Records Bureau has published (Crime in India from
1953, Accidental Deaths & Suicides from 1967, Prison Statistics from 1995),
extracted into CSV/JSON/Parquet, plus a dashboard to search, chart and map them.

Data and pipeline: <https://github.com/reclaimchennai/NCRB> (see README.md and docs/).

## Where it runs

| | |
|---|---|
| Live | <https://cpi.reclaimchennai.city/ncrb/> (nested under cpi until DNS exists); <https://ncrb.reclaimchennai.city> once a DNS record is added (Caddy block already in place) |
| Code | laptop repo `~/Desktop/projects/ncrb` (git, pushed to GitHub); on `raw` at `~/projects/ncrb` holds only `api/`, `web/`, `deploy/` and `data/web/ncrb.duckdb` |
| Process | `ncrb.service`, systemd `--user`, `uvicorn api.site:app`, 2 workers, `0.0.0.0:5072`, `MemoryMax=2G` |
| Ingress | Caddy: `handle_path /ncrb/*` inside the `cpi.reclaimchennai.city` block, and a `ncrb.reclaimchennai.city` block, both `reverse_proxy host.docker.internal:5072` |
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
browser -> Caddy -> uvicorn: api/main.py (FastAPI over DuckDB) + web/ (static, served by the same app)
```

The frontend is vanilla ES modules with hand-drawn SVG charts and no external
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
