"""The whole site in one process: the JSON API plus the static frontend in web/.

Production runs this behind Caddy (``uvicorn api.site:app``); the frontend is a
few small files, so serving them from the app keeps the deployment to one unit
and one Caddy line.
"""

from pathlib import Path

from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from api.main import app

WEB = Path(__file__).resolve().parents[1] / "web"


class CacheHeaders(BaseHTTPMiddleware):
    """Versioned assets are immutable; HTML and the API decide for themselves."""

    async def dispatch(self, request, call_next):
        resp = await call_next(request)
        p = request.url.path
        if "v=" in request.url.query and p.endswith((".js", ".css")):
            resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        elif p.endswith((".js", ".css", ".html", ".json")) or p.endswith("/"):
            resp.headers.setdefault("Cache-Control", "no-cache")
        elif "/geo/" in p:
            resp.headers["Cache-Control"] = "public, max-age=2592000"
        return resp


app.add_middleware(CacheHeaders)
app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
