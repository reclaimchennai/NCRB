"""Bring readings back: any mix of zips and folders (a Drive folder download, split into several zips or not),
into a local cache with the layout <cache>/<model slug>/<file id>/<page>.txt.

    ocrkit fetch ~/Downloads/myproject-*.zip --cache data/ocr_cache
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

PAGE = re.compile(r"(?:^|/)(?P<model>[A-Za-z0-9.\-]+)/(?P<id>[0-9a-f]{16})/(?P<page>\d{4})\.txt$")


def fetch(sources: list[str], cache: str, overwrite: bool = False) -> dict[str, int]:
    cache_p = Path(cache)
    added: dict[str, int] = {}

    def put(rel: str, read):
        m = PAGE.search(rel.replace("\\", "/"))
        if not m:
            return
        dst = cache_p / m["model"] / m["id"] / f"{m['page']}.txt"
        if dst.exists() and not overwrite:
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(read())
        added[m["model"]] = added.get(m["model"], 0) + 1

    for src in sources:
        p = Path(src).expanduser()
        if p.is_dir():
            for f in p.rglob("*.txt"):
                put(f.relative_to(p).as_posix(), f.read_bytes)
        elif zipfile.is_zipfile(p):
            with zipfile.ZipFile(p) as z:
                for name in z.namelist():
                    if name.endswith(".txt"):
                        put(name, lambda n=name: z.read(n))
    return added
