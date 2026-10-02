"""Inline web/kit/sprite.svg into every page between <!--sprite--> markers.

Safari has never supported cross-file <use href="sprite.svg#id">, so the
icons are carried inside each page (as cpi.reclaimchennai.city does).
"""

import re
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web"
sprite = (WEB / "kit" / "sprite.svg").read_text(encoding="utf-8").strip()
for page in [WEB / "trends" / "index.html", WEB / "chennai" / "index.html", WEB / "explore" / "index.html"]:
    if not page.exists():
        continue
    html = page.read_text(encoding="utf-8")
    new = re.sub(r"<!--sprite-->.*?<!--/sprite-->", lambda m: f"<!--sprite-->{sprite}<!--/sprite-->", html, flags=re.S)
    if new != html:
        page.write_text(new, encoding="utf-8")
        print(f"sprite inlined: {page.relative_to(WEB.parent)}")
