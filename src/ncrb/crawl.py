"""Crawl the NCRB listing pages and build a catalog of every published file.

Nothing is downloaded here except the listing HTML itself, which is kept in
``catalog/listing_html/`` as provenance. The output is ``catalog/catalog.csv``
with one row per (listing page, file link).

Usage:
    uv run python -m ncrb.crawl            # crawl everything (cached pages are reused)
    uv run python -m ncrb.crawl --refresh  # re-fetch every listing page
"""

from __future__ import annotations

import argparse
import csv
import re
import time
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from urllib.parse import urlencode, urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.ncrb.gov.in"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
ROOT = Path(__file__).resolve().parents[2]
HTML_DIR = ROOT / "catalog" / "listing_html"
CATALOG = ROOT / "catalog" / "catalog.csv"
DELAY = 1.0  # seconds between requests; this is a small government server

# publication -> {listing kind -> page slug}
LISTINGS: dict[str, dict[str, str]] = {
    "cii": {
        "year_wise": "crime-in-india-year-wise",
        "table_content": "crime-in-india-table-content",
        "additional_table": "crime-in-india-additional-table",
        "table_chapter": "crime-in-india-table-chapter",
    },
    "psi": {
        "year_wise": "prison-statistics-india-year-wise",
        "table_content": "table-contents-of-psi-reports",
    },
    "adsi": {
        "year_wise": "accidental-deaths-suicides-in-india-year-wise",
        "table_content": "accidental-deaths-suicides-in-india-table-content",
        "additional_table": "accidental-death-and-suicides-additional-table",
    },
}

FILE_RE = re.compile(r"\.(pdf|xlsx?|csv|zip|docx?|ods)(\?.*)?$", re.I)


@dataclass
class Entry:
    publication: str
    listing: str
    year: int
    section: str  # nearest heading above the link, e.g. "Chapter - 2 -- SUICIDES IN INDIA"
    serial: str  # S.No. column when the listing is a table, e.g. "2.13"
    title: str
    url: str
    size_text: str
    listing_url: str


class Site:
    def __init__(self, refresh: bool = False):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.refresh = refresh
        self._english = False

    def _get(self, url: str) -> str:
        for attempt in range(5):
            try:
                r = self.s.get(url, timeout=90)
                if r.status_code == 200:
                    time.sleep(DELAY)
                    return r.text
                err = f"HTTP {r.status_code}"
            except requests.RequestException as e:
                err = repr(e)
            time.sleep(5 * (attempt + 1))
        raise RuntimeError(f"failed to fetch {url}: {err}")

    def _ensure_english(self) -> None:
        """The site serves Hindi until the session language is switched."""
        if self._english:
            return
        html = self._get(f"{BASE}/crime-in-india.html")
        token = BeautifulSoup(html, "lxml").find("meta", {"name": "csrf-token"})["content"]
        r = self.s.post(
            f"{BASE}/api/language/set",
            data={"lang": "en", "slug": "crime-in-india", "_csrf": token},
            headers={"X-Requested-With": "XMLHttpRequest", "X-CSRF-Token": token},
            timeout=60,
        )
        r.raise_for_status()
        if str(r.json().get("success")) != "1":
            raise RuntimeError(f"could not switch language: {r.text}")
        self._english = True

    def page(self, slug: str, params: dict | None = None) -> tuple[str, str]:
        """Return (url, html) for a listing page, using the on-disk cache."""
        url = f"{BASE}/{slug}.html" + (f"?{urlencode(params)}" if params else "")
        name = slug + ("".join(f"__{k}-{v}" for k, v in params.items() if v != "") if params else "")
        path = HTML_DIR / f"{name}.html"
        if path.exists() and not self.refresh:
            return url, path.read_text(encoding="utf-8")
        self._ensure_english()
        html = self._get(url)
        if '<html lang="en' not in html[:400]:
            # session expired or was reset; switch again and retry once
            self._english = False
            self._ensure_english()
            html = self._get(url)
            if '<html lang="en' not in html[:400]:
                raise RuntimeError(f"page not served in English: {url}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        return url, html


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def main_content(html: str):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "header", "footer", "nav"]):
        tag.decompose()
    # the listing sits in the same container as the year filter form
    select = soup.find("select", {"name": "year"})
    node = select
    while node is not None and node.name != "form":
        node = node.parent
    container = node.parent if node is not None else soup.body
    return soup, select, container


def year_options(html: str) -> list[int]:
    _, select, _ = main_content(html)
    if select is None:
        return []
    return sorted({int(o["value"]) for o in select.find_all("option") if o.get("value", "").isdigit()})


def parse_listing(html: str, publication: str, listing: str, year: int, listing_url: str) -> list[Entry]:
    _, _, container = main_content(html)
    out: list[Entry] = []
    seen: set[tuple[str, str]] = set()
    section = ""
    for el in container.descendants:
        name = getattr(el, "name", None)
        if name in ("h1", "h2", "h3", "h4", "h5"):
            section = clean(el.get_text(" "))
        elif name == "a" and el.get("href") and FILE_RE.search(el["href"]):
            url = urljoin(BASE, el["href"].strip())
            text = clean(el.get_text(" "))
            row = el.find_parent("tr")
            serial = size = ""
            if row is not None:
                cells = row.find_all("td")
                if len(cells) >= 3:
                    serial = clean(cells[0].get_text(" "))
                    size = clean(cells[-1].get_text(" "))
            if re.fullmatch(r"\[\s*[\d.]+\s*[KMG]?B\s*\]", text):
                # year-wise pages repeat each link with the size as its text
                for e in reversed(out):
                    if e.url == url and not e.size_text:
                        e.size_text = text
                        break
                continue
            if (url, text) in seen:
                continue
            seen.add((url, text))
            out.append(Entry(publication, listing, year, section, serial, text, url, size, listing_url))
    return out


def crawl(refresh: bool = False) -> list[Entry]:
    site = Site(refresh=refresh)
    entries: list[Entry] = []
    for publication, kinds in LISTINGS.items():
        for listing, slug in kinds.items():
            _, html = site.page(slug)
            years = year_options(html)
            print(f"{publication}/{listing}: {len(years)} years ({years[0] if years else '-'}..{years[-1] if years else '-'})")
            for year in years:
                params = {"year": year, "category": "", "keyword": ""}
                url, html = site.page(slug, params)
                found = parse_listing(html, publication, listing, year, url)
                entries.extend(found)
                if re.search(r'href="[^"]*[?&]page=\d+', html):
                    print(f"  WARNING pagination present on {url}")
            n = sum(1 for e in entries if e.publication == publication and e.listing == listing)
            print(f"  -> {n} file links")
    return entries


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--refresh", action="store_true", help="re-fetch listing pages instead of using the cache")
    args = ap.parse_args()
    entries = crawl(refresh=args.refresh)
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    with CATALOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[x.name for x in fields(Entry)])
        w.writeheader()
        for e in entries:
            w.writerow(asdict(e))
    print(f"wrote {len(entries)} rows ({len({e.url for e in entries})} unique files) to {CATALOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
