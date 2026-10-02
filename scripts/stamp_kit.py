"""Version every module and stylesheet URL of the trends and Chennai pages.

Cloudflare overrides the origin's cache headers, so a changed file only
reaches visitors under a new URL. One hash over all the kit and page files is
written as ?v= into every import and every asset link (one version for all,
so no module is ever loaded twice under two URLs). Run by deploy.sh.
"""

import hashlib
import re
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "web"
JS = sorted((WEB / "kit").glob("*.js")) + [WEB / "trends" / "trends.js", WEB / "chennai" / "chennai.js", WEB / "explore" / "explore.js"]
CSS = [WEB / "kit" / "kit.css"]
HTML = [WEB / "trends" / "index.html", WEB / "chennai" / "index.html", WEB / "explore" / "index.html"]
V = re.compile(r"\?v=[0-9a-f]+")

h = hashlib.sha256()
for f in JS + CSS:
    h.update(V.sub("", f.read_text(encoding="utf-8")).encode())
ver = h.hexdigest()[:10]
imp = re.compile(r"""(from\s+['"])(\.{1,2}/[^'"?]+\.js)(\?v=[0-9a-f]+)?(['"])""")
for f in JS:
    s = f.read_text(encoding="utf-8")
    f.write_text(imp.sub(lambda m: f"{m.group(1)}{m.group(2)}?v={ver}{m.group(4)}", s), encoding="utf-8")
asset = re.compile(r"""((?:href|src)=")([^"?]+\.(?:js|css))(\?v=[0-9a-f]+)?(")""")
for f in HTML:
    s = f.read_text(encoding="utf-8")
    f.write_text(asset.sub(lambda m: f"{m.group(1)}{m.group(2)}?v={ver}{m.group(4)}" if not m.group(2).startswith("http") else m.group(0), s), encoding="utf-8")
print(f"kit stamped v={ver}")
