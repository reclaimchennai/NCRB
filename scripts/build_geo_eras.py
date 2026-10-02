"""Year-accurate State/UT boundary maps of India, 1951-2024, as static GeoJSON.

Every era's States and UTs are built as unions of the Census 2011 districts
(datameet/maps), so all eras share the same lines and only the grouping
changes. Writes:

    web/geo/states-<first year>.geojson   one file per era
    web/geo/eras.json                     year range -> file
    web/geo/README.md                     sources, era table, approximations, name map

Run from the repo root:

    uv run --with shapely --with pyproj python scripts/build_geo_eras.py

Needs ogr2ogr (GDAL) and npx (for mapshaper). Raw downloads are cached in
data/geo_src/; delete them to fetch again.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from copy import deepcopy
from pathlib import Path

from pyproj import Geod
from shapely.geometry import mapping, shape
from shapely.ops import unary_union
from shapely.validation import make_valid

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "geo_src"
BUILD = SRC / "build"
OUT = ROOT / "web" / "geo"
sys.path.insert(0, str(ROOT / "src"))
from ncrb.entities import HISTORIC, STATES, UTS, standardise  # noqa: E402

OGR2OGR = shutil.which("ogr2ogr") or "/opt/homebrew/bin/ogr2ogr"
SIMPLIFY = "15%"  # share of removable vertices mapshaper keeps (weighted Visvalingam)
PRECISION = "0.001"  # ~100 m, as in the old india-states.geojson

RAW = "https://raw.githubusercontent.com/datameet/maps/master/"
SOURCES = {
    "2011_Dist": {
        "files": [f"Districts/Census_2011/2011_Dist.{e}" for e in ("shp", "shx", "dbf", "prj")],
        "page": "https://github.com/datameet/maps/tree/master/Districts/Census_2011",
        "licence": "CC BY 2.5 India (https://creativecommons.org/licenses/by/2.5/in/), per Districts/README.md",
        "credit": "Census 2011 district boundaries by the DataMeet India community",
    },
    "Admin2": {
        "files": [f"States/Admin2.{e}" for e in ("shp", "shx", "dbf", "prj", "cpg")],
        "page": "https://github.com/datameet/maps/tree/master/States",
        "licence": "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), the repository default",
        "credit": "Present-day State/UT boundaries (2020-) by the DataMeet India community; used only for the J&K / Ladakh line inside the area the 2011 district file marks 'Data Not Available'",
    },
}

geod = Geod(ellps="WGS84")


def km2(g) -> float:
    return abs(geod.geometry_area_perimeter(g)[0]) / 1e6


# ---------------------------------------------------------------------------
# 1. download and convert
# ---------------------------------------------------------------------------

def download() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    for src in SOURCES.values():
        for f in src["files"]:
            dest = SRC / Path(f).name
            if dest.exists() and dest.stat().st_size > 0:
                continue
            print("download", RAW + f)
            with urllib.request.urlopen(RAW + f) as r, open(dest, "wb") as out:
                shutil.copyfileobj(r, out)
    lines = ["Raw boundary downloads for scripts/build_geo_eras.py", ""]
    for name, src in SOURCES.items():
        lines += [f"{name}: {src['credit']}", f"  page:    {src['page']}", f"  licence: {src['licence']}"]
        lines += [f"  file:    {RAW}{f}" for f in src["files"]] + [""]
    (SRC / "SOURCES.txt").write_text("\n".join(lines))


def to_geojson(shp: str) -> dict:
    BUILD.mkdir(parents=True, exist_ok=True)
    out = BUILD / f"{shp}.geojson"
    if not out.exists():
        subprocess.run([OGR2OGR, "-f", "GeoJSON", "-t_srs", "EPSG:4326", str(out), str(SRC / f"{shp}.shp")], check=True)
    return json.loads(out.read_text())


# ---------------------------------------------------------------------------
# 2. units: 2011 districts, tagged with the present-day State/UT they lie in
# ---------------------------------------------------------------------------

ST_FIX = {
    "Andaman & Nicobar Island": "Andaman & Nicobar Islands", "Arunanchal Pradesh": "Arunachal Pradesh",
    "Dadara & Nagar Havelli": "Dadra & Nagar Haveli", "NCT of Delhi": "Delhi",
}
TELANGANA = {"Adilabad", "Nizamabad", "Karimnagar", "Medak", "Hyderabad", "Rangareddy", "Mahbubnagar", "Nalgonda", "Warangal", "Khammam"}
LADAKH = {"Leh (ladakh)", "Kargil"}
DNA = "Data Not Available"
DNA_JK, DNA_LA = "Data Not Available (Pakistan-administered J&K)", "Data Not Available (Gilgit-Baltistan)"
# the 2011 States/UTs are kept apart here (Dadra & Nagar Haveli, Daman & Diu); `covers` uses today's names
TODAY = {"Dadra & Nagar Haveli": "Dadra & Nagar Haveli and Daman & Diu", "Daman & Diu": "Dadra & Nagar Haveli and Daman & Diu"}


def build_units() -> tuple[dict, dict]:
    """{uid: geometry}, {uid: base State/UT}. uid = 'State/District'."""
    dist = to_geojson("2011_Dist")
    adm = to_geojson("Admin2")
    geoms, base = {}, {}
    for f in dist["features"]:
        p = f["properties"]
        st, d = ST_FIX.get(p["ST_NM"], p["ST_NM"]), p["DISTRICT"]
        if st == "Andhra Pradesh" and d in TELANGANA:
            st = "Telangana"
        if st == "Jammu & Kashmir" and d in LADAKH:
            st = "Ladakh"
        g = make_valid(shape(f["geometry"])).buffer(0)
        if d == DNA:
            # Pakistan- and China-administered J&K carry no district in the census file. Split it on the
            # J&K UT / Ladakh UT line of datameet's present-day state file: what lies in its J&K is
            # PoK (Muzaffarabad, Mirpur), the rest (Gilgit-Baltistan, Shaksgam) goes with Ladakh.
            jk = unary_union([make_valid(shape(a["geometry"])) for a in adm["features"] if a["properties"]["ST_NM"] == "Jammu & Kashmir"])
            rest = g.difference(jk)
            parts = getattr(rest, "geoms", [rest])
            la = unary_union([q for q in parts if q.geom_type == "Polygon" and q.area > 0.05])  # drop edge slivers
            geoms[f"Jammu & Kashmir/{DNA_JK}"], base[f"Jammu & Kashmir/{DNA_JK}"] = g.difference(la).buffer(0), "Jammu & Kashmir"
            geoms[f"Ladakh/{DNA_LA}"], base[f"Ladakh/{DNA_LA}"] = la.buffer(0), "Ladakh"
            continue
        uid = f"{st}/{d}"
        assert uid not in geoms, uid
        geoms[uid], base[uid] = g, st
    return geoms, base


# ---------------------------------------------------------------------------
# 3. eras
# ---------------------------------------------------------------------------

class Groups:
    def __init__(self, base: dict):
        self.base = base

    def S(self, *states) -> frozenset:
        out = frozenset(u for u, b in self.base.items() if b in states)
        assert out, states
        return out

    def D(self, state, *districts) -> frozenset:
        out = frozenset(f"{state}/{d}" for d in districts)
        missing = [u for u in out if u not in self.base]
        assert not missing, missing
        return out


def eras(base: dict) -> list[dict]:
    g = Groups(base)
    S, D = g.S, g.D
    # building blocks (2011 districts)
    malabar = D("Kerala", "Kasaragod", "Kannur", "Wayanad", "Kozhikode", "Malappuram", "Palakkad")
    kanyakumari = D("Tamil Nadu", "Kanniyakumari")
    south_canara = D("Karnataka", "Dakshina Kannada", "Udupi")
    bellary = D("Karnataka", "Bellary")
    old_mysore = D("Karnataka", "Bangalore", "Bangalore Rural", "Ramanagara", "Chikkaballapura", "Kolar", "Tumkur", "Chitradurga",
                   "Davanagere", "Shimoga", "Chikmagalur", "Hassan", "Mandya", "Mysore", "Chamrajnagar")
    bombay_ka = D("Karnataka", "Belgaum", "Bijapur", "Bagalkot", "Dharwad", "Gadag", "Haveri", "Uttara Kannada")
    hyderabad_ka = D("Karnataka", "Gulbarga", "Yadgir", "Raichur", "Koppal", "Bidar")
    kodagu = D("Karnataka", "Kodagu")
    marathwada = D("Maharashtra", "Aurangabad", "Jalna", "Bid", "Parbhani", "Hingoli", "Nanded", "Osmanabad", "Latur")
    vidarbha = D("Maharashtra", "Buldana", "Akola", "Washim", "Amravati", "Yavatmal", "Wardha", "Nagpur", "Bhandara", "Gondiya",
                 "Chandrapur", "Garhchiroli")
    saurashtra = D("Gujarat", "Jamnagar", "Rajkot", "Porbandar", "Junagadh", "Amreli", "Bhavnagar", "Surendranagar")
    kutch = D("Gujarat", "Kachchh")
    madhya_bharat = D("Madhya Pradesh", "Morena", "Sheopur", "Bhind", "Gwalior", "Shivpuri", "Guna", "Ashoknagar", "Vidisha", "Rajgarh",
                      "Shajapur", "Ujjain", "Dewas", "Indore", "Dhar", "Jhabua", "Alirajpur", "Ratlam", "Mandsaur", "Neemuch",
                      "West Nimar", "Barwani")
    vindhya = D("Madhya Pradesh", "Rewa", "Satna", "Sidhi", "Singrauli", "Shahdol", "Anuppur", "Umaria", "Panna", "Chhatarpur",
                "Tikamgarh", "Datia")
    bhopal = D("Madhya Pradesh", "Bhopal", "Sehore", "Raisen")
    mahakoshal = S("Madhya Pradesh") - madhya_bharat - vindhya - bhopal
    assert len(mahakoshal) == 15, sorted(mahakoshal)
    pepsu = D("Punjab", "Patiala", "Fatehgarh Sahib", "Sangrur", "Barnala", "Bathinda", "Mansa", "Faridkot", "Kapurthala") | D("Haryana", "Jind", "Mahendragarh")
    punjab_hills = D("Himachal Pradesh", "Kangra", "Kullu", "Lahul & Spiti", "Hamirpur", "Una")
    bilaspur = D("Himachal Pradesh", "Bilaspur")
    naga_hills = D("Nagaland", "Kohima", "Dimapur", "Peren", "Phek", "Wokha", "Zunheboto", "Mokokchung")
    tuensang = S("Nagaland") - naga_hills
    purulia = D("West Bengal", "Puruliya")
    ajmer = D("Rajasthan", "Ajmer")

    def st(units, kind="state", part=None, note=None):
        return {"units": frozenset(units), "kind": kind, "part": part, "note": note}

    NEFA_NOTE = ("Constitutionally part of Assam but administered by the Centre through the Governor of Assam; "
                 "no NCRB row for it was found in the extracted tables.")
    out: list[dict] = []

    def add(start, frm, note, m):
        out.append({"start": start, "from": frm, "note": note, "features": deepcopy(m)})

    m = {
        # Part A
        "Assam": st(S("Assam", "Meghalaya", "Mizoram") | naga_hills, part="A"),
        "Bihar": st(S("Bihar", "Jharkhand") | purulia, part="A"),
        "Bombay": st(S("Gujarat", "Maharashtra") - saurashtra - kutch - marathwada - vidarbha | bombay_ka, part="A"),
        "Madhya Pradesh": st(S("Chhattisgarh") | vidarbha | mahakoshal, part="A"),
        "Madras": st(S("Tamil Nadu", "Andhra Pradesh", "Lakshadweep") - kanyakumari | malabar | south_canara | bellary, part="A"),
        "Orissa": st(S("Odisha"), part="A"),
        "Punjab": st(S("Punjab", "Haryana", "Chandigarh") - pepsu | punjab_hills, part="A"),
        "Uttar Pradesh": st(S("Uttar Pradesh", "Uttarakhand"), part="A"),
        "West Bengal": st(S("West Bengal") - purulia, part="A"),
        # Part B
        "Hyderabad": st(S("Telangana") | marathwada | hyderabad_ka, part="B"),
        "Jammu and Kashmir": st(S("Jammu & Kashmir", "Ladakh"), part="B"),
        "Madhya Bharat": st(madhya_bharat, part="B"),
        "Mysore": st(old_mysore, part="B"),
        "PEPSU": st(pepsu, part="B", note="Patiala and East Punjab States Union."),
        "Rajasthan": st(S("Rajasthan") - ajmer, part="B"),
        "Saurashtra": st(saurashtra, part="B"),
        "Travancore-Cochin": st(S("Kerala") - malabar | kanyakumari, part="B"),
        # Part C
        "Ajmer": st(ajmer, part="C"),
        "Bhopal": st(bhopal, part="C"),
        "Bilaspur": st(bilaspur, part="C"),
        "Coorg": st(kodagu, part="C"),
        "Delhi": st(S("Delhi"), part="C"),
        "Himachal Pradesh": st(S("Himachal Pradesh") - punjab_hills - bilaspur, part="C"),
        "Kutch": st(kutch, part="C"),
        "Manipur": st(S("Manipur"), part="C"),
        "Tripura": st(S("Tripura"), part="C"),
        "Vindhya Pradesh": st(vindhya, part="C"),
        # Part D and the agency
        "Andaman and Nicobar Islands": st(S("Andaman & Nicobar Islands"), "ut", part="D"),
        "North-East Frontier Agency": st(S("Arunachal Pradesh") | tuensang, "ut", note=NEFA_NOTE),
    }
    add("1950-01-26", 1951, "Part A, B and C States of the 1950 Constitution. Madras still includes the Andhra districts and Bellary. "
        "Goa, Daman, Diu, Dadra & Nagar Haveli (Portuguese), Pondicherry (French) and Sikkim (protectorate) are not part of India and have no feature.", m)

    m["Madras"]["units"] -= S("Andhra Pradesh") | bellary
    m["Andhra"] = st(S("Andhra Pradesh"), part="A")
    m["Mysore"]["units"] |= bellary
    add("1953-10-01", 1953, "Andhra State carved out of Madras (1 Oct 1953); Bellary district (less Adoni, Alur, Rayadurg) to Mysore.", m)

    m["Himachal Pradesh"]["units"] |= bilaspur
    del m["Bilaspur"]
    m["Pondicherry"] = st(S("Puducherry"), "ut", note="French establishments transferred de facto on 1 Nov 1954 and run by the Centre; de jure Union Territory from 16 Aug 1962.")
    add("1954-07-01", 1954, "Bilaspur merged into Himachal Pradesh (1 Jul 1954); Pondicherry, Karaikal, Mahe and Yanam transferred from France de facto (1 Nov 1954).", m)

    m = {
        "Andhra Pradesh": st(S("Andhra Pradesh", "Telangana")),
        "Assam": m["Assam"] | {"part": None},
        "Bihar": st(S("Bihar", "Jharkhand")),
        "Bombay": st(S("Gujarat", "Maharashtra")),
        "Jammu and Kashmir": st(S("Jammu & Kashmir", "Ladakh")),
        "Kerala": st(S("Kerala")),
        "Madhya Pradesh": st(S("Madhya Pradesh", "Chhattisgarh")),
        "Madras": st(S("Tamil Nadu")),
        "Mysore": st(S("Karnataka")),
        "Orissa": st(S("Odisha")),
        "Punjab": st(S("Punjab", "Haryana", "Chandigarh") | punjab_hills),
        "Rajasthan": st(S("Rajasthan")),
        "Uttar Pradesh": st(S("Uttar Pradesh", "Uttarakhand")),
        "West Bengal": st(S("West Bengal")),
        "Andaman and Nicobar Islands": st(S("Andaman & Nicobar Islands"), "ut"),
        "Delhi": st(S("Delhi"), "ut"),
        "Himachal Pradesh": st(S("Himachal Pradesh") - punjab_hills, "ut"),
        "Laccadive, Minicoy and Amindivi Islands": st(S("Lakshadweep"), "ut"),
        "Manipur": st(S("Manipur"), "ut"),
        "Tripura": st(S("Tripura"), "ut"),
        "Pondicherry": m["Pondicherry"],
        "North-East Frontier Agency": m["North-East Frontier Agency"],
    }
    add("1956-11-01", 1956, "States Reorganisation Act (1 Nov 1956): 14 States and 6 Union Territories. Andhra + Telangana = Andhra Pradesh; "
        "Bombay gains Saurashtra, Kutch, Marathwada and Vidarbha, loses its Kannada districts; Kerala formed; Madhya Pradesh absorbs "
        "Madhya Bharat, Vindhya Pradesh and Bhopal; Mysore enlarged; PEPSU into Punjab; Ajmer into Rajasthan; Purulia from Bihar to West Bengal.", m)

    m["Assam"]["units"] -= naga_hills
    m["North-East Frontier Agency"]["units"] -= tuensang
    m["Naga Hills-Tuensang Area"] = st(S("Nagaland"), "ut", note="Naga Hills district of Assam and the Tuensang Frontier Division of NEFA, run by the Centre from 1 Dec 1957 (constitutionally still in Assam); NCRB printed it among the Union Territories ('Naga Hills', later 'Nagaland').")
    add("1957-12-01", 1957, "Naga Hills-Tuensang Area formed (1 Dec 1957) from Assam's Naga Hills district and NEFA's Tuensang division.", m)

    del m["Bombay"]
    m["Maharashtra"], m["Gujarat"] = st(S("Maharashtra")), st(S("Gujarat"))
    add("1960-05-01", 1960, "Bombay Reorganisation Act (1 May 1960): Bombay split into Maharashtra and Gujarat.", m)

    m["Nagaland"] = m.pop("Naga Hills-Tuensang Area") | {"note": "Naga Hills-Tuensang Area renamed Nagaland in Feb 1961; run by the Centre until statehood on 1 Dec 1963."}
    m["Dadra and Nagar Haveli"] = st(S("Dadra & Nagar Haveli"), "ut")
    m["Goa, Daman and Diu"] = st(S("Goa", "Daman & Diu"), "ut")
    add("1961-08-11", 1961, "Dadra and Nagar Haveli a Union Territory (11 Aug 1961); Goa, Daman and Diu annexed and made a Union Territory (20 Dec 1961); "
        "Naga Hills-Tuensang Area renamed Nagaland (Feb 1961). Pondicherry becomes a Union Territory de jure on 16 Aug 1962 (no line change).", m)

    m["Nagaland"] = st(S("Nagaland"))
    add("1963-12-01", 1963, "Nagaland a State (1 Dec 1963).", m)

    m["Punjab"] = st(S("Punjab"))
    m["Haryana"] = st(S("Haryana"))
    m["Chandigarh"] = st(S("Chandigarh"), "ut")
    m["Himachal Pradesh"]["units"] |= punjab_hills
    add("1966-11-01", 1966, "Punjab Reorganisation Act (1 Nov 1966): Haryana formed; Chandigarh a Union Territory; Kangra, Kullu, Lahaul & Spiti, Simla and Una areas of Punjab to Himachal Pradesh.", m)

    m["Tamil Nadu"] = m.pop("Madras")
    add("1969-01-14", 1969, "Madras renamed Tamil Nadu (14 Jan 1969). Meghalaya becomes an autonomous State within Assam on 2 Apr 1970 (still drawn in Assam; NCRB printed it from 1972).", m)

    m["Himachal Pradesh"]["kind"] = "state"
    add("1971-01-25", 1971, "Himachal Pradesh a State (25 Jan 1971); no line change.", m)

    m["Assam"]["units"] = S("Assam")
    m["Meghalaya"] = st(S("Meghalaya"))
    m["Mizoram"] = st(S("Mizoram"), "ut")
    del m["North-East Frontier Agency"]
    m["Arunachal Pradesh"] = st(S("Arunachal Pradesh"), "ut")
    m["Manipur"]["kind"] = m["Tripura"]["kind"] = "state"
    add("1972-01-21", 1972, "North-Eastern Areas (Reorganisation) Act (21 Jan 1972): Meghalaya, Manipur and Tripura States; Mizoram and Arunachal Pradesh (ex-NEFA) Union Territories.", m)

    m["Karnataka"] = m.pop("Mysore")
    m["Lakshadweep"] = m.pop("Laccadive, Minicoy and Amindivi Islands")
    add("1973-11-01", 1973, "Mysore renamed Karnataka and the Laccadive, Minicoy and Amindivi Islands renamed Lakshadweep (1 Nov 1973).", m)

    m["Sikkim"] = st(S("Sikkim"))
    add("1975-05-16", 1975, "Sikkim a State (16 May 1975).", m)

    m["Mizoram"]["kind"] = m["Arunachal Pradesh"]["kind"] = "state"
    del m["Goa, Daman and Diu"]
    m["Goa"] = st(S("Goa"))
    m["Daman and Diu"] = st(S("Daman & Diu"), "ut")
    add("1987-02-20", 1987, "Mizoram and Arunachal Pradesh States (20 Feb 1987); Goa a State and Daman and Diu a separate Union Territory (30 May 1987). "
        "Delhi became the National Capital Territory in 1992 (no line change).", m)

    m["Madhya Pradesh"]["units"] = S("Madhya Pradesh")
    m["Chhattisgarh"] = st(S("Chhattisgarh"))
    m["Uttar Pradesh"]["units"] = S("Uttar Pradesh")
    m["Uttaranchal"] = st(S("Uttarakhand"))
    m["Bihar"]["units"] = S("Bihar")
    m["Jharkhand"] = st(S("Jharkhand"))
    add("2000-11-01", 2000, "Chhattisgarh (1 Nov 2000), Uttaranchal (9 Nov 2000) and Jharkhand (15 Nov 2000) formed.", m)

    m["Puducherry"] = m.pop("Pondicherry") | {"note": None}
    add("2006-10-01", 2006, "Pondicherry renamed Puducherry (1 Oct 2006).", m)

    m["Uttarakhand"] = m.pop("Uttaranchal")
    add("2007-01-01", 2007, "Uttaranchal renamed Uttarakhand (1 Jan 2007).", m)

    m["Odisha"] = m.pop("Orissa")
    add("2011-11-01", 2011, "Orissa renamed Odisha (1 Nov 2011).", m)

    m["Andhra Pradesh"]["units"] = S("Andhra Pradesh")
    m["Telangana"] = st(S("Telangana"))
    add("2014-06-02", 2014, "Telangana formed (2 Jun 2014).", m)

    m["Jammu and Kashmir"] = st(S("Jammu & Kashmir"), "ut")
    m["Ladakh"] = st(S("Ladakh"), "ut")
    add("2019-10-31", 2019, "Jammu and Kashmir Reorganisation Act (31 Oct 2019): Union Territories of Jammu and Kashmir and of Ladakh.", m)

    del m["Dadra and Nagar Haveli"], m["Daman and Diu"]
    m["Dadra and Nagar Haveli and Daman and Diu"] = st(S("Dadra & Nagar Haveli", "Daman & Diu"), "ut")
    add("2020-01-26", 2020, "Dadra and Nagar Haveli and Daman and Diu merged (26 Jan 2020).", m)

    for i, e in enumerate(out):
        e["to"] = out[i + 1]["from"] - 1 if i + 1 < len(out) else 2024
        e["file"] = f"states-{e['from']}.geojson"
        e["key"] = f"e{i:02d}"
    return out


# printed names standardise() has no answer for -> the State NCRB's series continues as
SUCCESSOR = {
    "Andhra": "Andhra Pradesh", "Hyderabad": "Andhra Pradesh", "Bombay": "Maharashtra", "Madhya Bharat": "Madhya Pradesh",
    "Vindhya Pradesh": "Madhya Pradesh", "Bhopal": "Madhya Pradesh", "PEPSU": "Punjab", "Saurashtra": "Gujarat", "Kutch": "Gujarat",
    "Travancore-Cochin": "Kerala", "Coorg": "Karnataka", "Ajmer": "Rajasthan", "Bilaspur": "Himachal Pradesh",
    "North-East Frontier Agency": "Arunachal Pradesh", "Naga Hills-Tuensang Area": "Nagaland", "Goa, Daman and Diu": "Goa",
}
SUCCESSOR_NOTE = {
    "Bombay": "its territory also continues as Gujarat from 1960 and as north Karnataka from 1956",
    "Hyderabad": "in 1956 Telangana went to Andhra Pradesh, Marathwada to Bombay and the Kannada districts to Mysore",
    "Goa, Daman and Diu": "Daman and Diu became a separate UT in 1987",
}


# era feature names whose data rows carry a name of their own (src/ncrb/entities.py HISTORIC / BY_YEAR)
HIST_STD = {"Bombay": "Bombay State", "Hyderabad": "Hyderabad State", "Bhopal": "Bhopal State", "Ajmer": "Ajmer State",
            "Bilaspur": "Bilaspur State", "Andhra": "Andhra State", "North-East Frontier Agency": "NEFA",
            "Naga Hills-Tuensang Area": "Nagaland", "Goa, Daman and Diu": "Goa, Daman & Diu"}


def std_of(name: str) -> tuple[str, str]:
    if name in HIST_STD:
        return HIST_STD[name], "standardise"
    s, kind = standardise(name)
    if kind in ("state", "ut"):
        return s, "standardise"
    return SUCCESSOR[name], "successor"


# ---------------------------------------------------------------------------
# 4. geometry: clean + simplify the districts once, dissolve per era
# ---------------------------------------------------------------------------

def write_units(geoms: dict, base: dict, era_list: list[dict]) -> Path:
    owner = {e["key"]: {u: n for n, f in e["features"].items() for u in f["units"]} for e in era_list}
    feats = []
    for uid, g in geoms.items():
        props = {"uid": uid, "base": base[uid]}
        for e in era_list:
            props[e["key"]] = owner[e["key"]].get(uid)
        feats.append({"type": "Feature", "properties": props, "geometry": mapping(g)})
    path = BUILD / "units.geojson"
    path.write_text(json.dumps({"type": "FeatureCollection", "features": feats}))
    return path


def mapshaper(units: Path, era_list: list[dict]) -> None:
    cmd = ["npx", "-y", "mapshaper", "-i", str(units), "snap", "name=units", "-clean", "-simplify", "weighted", "keep-shapes", SIMPLIFY,
           "-o", str(BUILD / "units-simplified.json"), "format=geojson", f"precision={PRECISION}"]
    for e in era_list:
        cmd += ["-dissolve2", e["key"], "+", f"name={e['key']}", "target=units"]
    cmd += ["-o", str(BUILD) + "/", "format=geojson", f"precision={PRECISION}", "target=" + ",".join(e["key"] for e in era_list)]
    subprocess.run(cmd, check=True)


def today_names(units: frozenset, base: dict) -> list[str]:
    return sorted({TODAY.get(base[u], base[u]) for u in units})


def write_eras(era_list: list[dict], base: dict) -> None:
    for e in era_list:
        raw = json.loads((BUILD / f"{e['key']}.json").read_text())
        geo = {f["properties"][e["key"]]: f["geometry"] for f in raw["features"] if f["properties"].get(e["key"])}
        lines = []
        for name in sorted(e["features"]):
            f = e["features"][name]
            std, how = std_of(name)
            props = {"name": name, "std": std, "kind": f["kind"], "covers": today_names(f["units"], base)}
            if how == "successor":
                props["std_from"] = "successor"
                props["std_note"] = "standardise() has no mapping for this name; std is the State NCRB's series continues as" + (
                    f" ({SUCCESSOR_NOTE[name]})" if name in SUCCESSOR_NOTE else "")
            if f["part"]:
                props["part"] = f["part"]
            if f["note"]:
                props["note"] = f["note"]
            lines.append(json.dumps({"type": "Feature", "properties": props, "geometry": geo[name]}, ensure_ascii=False, separators=(",", ":")))
        (OUT / e["file"]).write_text('{"type":"FeatureCollection","features":[\n' + ",\n".join(lines) + "\n]}\n")
    index = [{"from": e["from"], "to": e["to"], "file": e["file"], "start": e["start"], "note": e["note"]} for e in era_list]
    (OUT / "eras.json").write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 5. validation
# ---------------------------------------------------------------------------

def validate(era_list: list[dict], base: dict) -> list[dict]:
    outline = make_valid(shape(json.loads((OUT / "india-outline.geojson").read_text())["features"][0]["geometry"]))
    a_out = km2(outline)
    years = []
    report = []
    for e in era_list:
        years += range(e["from"], e["to"] + 1)
        assigned = [u for f in e["features"].values() for u in f["units"]]
        assert len(assigned) == len(set(assigned)), f"{e['file']}: a district is in two features"
        missing = sorted(set(base) - set(assigned))
        d = json.loads((OUT / e["file"]).read_text())
        names = [f["properties"]["name"] for f in d["features"]]
        assert sorted(names) == sorted(e["features"]), e["file"]
        geoms = []
        for f in d["features"]:
            g = make_valid(shape(f["geometry"]))
            assert not g.is_empty and g.area > 0, f"{e['file']}: empty {f['properties']['name']}"
            assert f["properties"]["std"] in STATES + UTS + list(HISTORIC), f["properties"]
            geoms.append(g)
        u = unary_union(geoms)
        omitted = sorted({base[m] for m in missing})
        report.append({
            "file": e["file"], "years": f"{e['from']}-{e['to']}", "features": len(names),
            "kb": round((OUT / e["file"]).stat().st_size / 1024), "omitted": omitted,
            "outline_minus_union_pct": round(100 * km2(outline.difference(u)) / a_out, 2),
            "union_minus_outline_pct": round(100 * km2(u.difference(outline)) / a_out, 2),
        })
    assert years == list(range(1951, 2025)), "eras must cover 1951-2024 without gaps"
    return report


def compare_current(era_list: list[dict]) -> list[tuple[str, float]]:
    """Per-feature agreement of the 2014-2018 file with the old india-states.geojson (intersection over union)."""
    old = json.loads((OUT / "india-states.geojson").read_text())
    rename = {"Andaman and Nicobar": "Andaman and Nicobar Islands", "Uttaranchal": "Uttarakhand", "Orissa": "Odisha"}
    oldg = {rename.get(f["properties"]["NAME_1"], f["properties"]["NAME_1"]): make_valid(shape(f["geometry"])) for f in old["features"]}
    e = next(x for x in era_list if x["from"] == 2014)
    new = {f["properties"]["name"]: make_valid(shape(f["geometry"])) for f in json.loads((OUT / e["file"]).read_text())["features"]}
    out = []
    for n, g in sorted(new.items()):
        if n in oldg:
            out.append((n, round(km2(g.intersection(oldg[n])) / km2(g.union(oldg[n])), 3)))
        else:
            out.append((n, float("nan")))
    return out


# ---------------------------------------------------------------------------
# 6. README
# ---------------------------------------------------------------------------

APPROXIMATIONS = [
    ("Kollegal taluk", "Madras until 1956, then Mysore; it is part of today's Chamarajanagar district, drawn in Mysore throughout."),
    ("Shenkottai taluk", "Travancore-Cochin until 1956, then Madras; part of today's Tirunelveli (Tenkasi), drawn in Madras throughout."),
    ("Chittur taluk (Palakkad)", "Cochin, i.e. Travancore-Cochin, until 1956; Palakkad is drawn whole in Madras (Malabar) before 1956."),
    ("Chavakkad / Ponnani area (Thrissur)", "Malabar (Madras) until 1956; Thrissur is drawn whole in Travancore-Cochin before 1956."),
    ("Kasaragod", "Kasaragod taluk of South Canara (Madras) to Kerala in 1956; today's Kasaragod district is used for it (good match)."),
    ("Amreli", "Baroda's Amreli prant was in Bombay State 1949-56, but today's district also holds former Saurashtra states; drawn in Saurashtra before 1956. Okhamandal (Dwarka, Baroda -> Bombay) is likewise drawn in Saurashtra with Jamnagar."),
    ("Abu Road taluk", "Bombay until 1956, then Rajasthan; part of Sirohi, drawn in Rajasthan throughout."),
    ("Sironj", "Rajasthan (Tonk) until 1956, then Madhya Pradesh; part of Vidisha, drawn in Madhya Bharat before 1956."),
    ("Sunel tappa", "Madhya Bharat until 1956, then Rajasthan; part of Jhalawar, drawn in Rajasthan throughout."),
    ("Ajmer State", "Ajmer-Merwara is drawn as today's Ajmer district; the old State's limits differ somewhat."),
    ("Bhadrachalam / Nuguru Venkatapuram taluks", "East Godavari (Madras, then Andhra) until 1959, then Khammam; Khammam is drawn whole in Hyderabad (to 1956), Andhra Pradesh (1956-2014) and Telangana (2014-)."),
    ("Polavaram mandals", "Seven mandals of Khammam moved to Andhra Pradesh in 2014; Khammam is drawn whole in Telangana."),
    ("Tiruttani / Pallipattu", "Andhra Pradesh to Madras on 1 Apr 1960 (and small areas the other way); not shown."),
    ("Bidar, Gulbarga, Raichur edges", "Hyderabad's 1956 split followed taluk lines that differ slightly from today's district lines (e.g. taluks of Bidar to Andhra Pradesh and Bombay); today's lines used."),
    ("Islampur area of Purnea", "Bihar to West Bengal in 1956; it is in Uttar Dinajpur, drawn in West Bengal throughout. Purulia is today's Puruliya district (good match)."),
    ("Solan", "Kandaghat and Nalagarh tehsils were PEPSU (to 1956) and Punjab (to 1966); Solan district is drawn whole in Himachal Pradesh throughout."),
    ("Shimla", "Simla town and some nearby areas were in Punjab until 1966; Shimla district is drawn in Himachal Pradesh throughout."),
    ("Dalhousie / Bakloh", "Gurdaspur (Punjab) to Himachal in 1966; part of Chamba, drawn in Himachal throughout."),
    ("Una", "Una town and 290 villages of Hoshiarpur's Una tahsil to Himachal in 1966; today's Una district is used (good match)."),
    ("PEPSU pieces", "PEPSU is drawn as today's Patiala, Fatehgarh Sahib, Sangrur, Barnala, Bathinda, Mansa, Faridkot, Kapurthala, Jind and Mahendragarh. Scattered pieces (Charkhi Dadri in Bhiwani, Bawal in Rewari, Kalsia in Yamunanagar, Dera Bassi in SAS Nagar) are drawn in Punjab, and Punjab enclaves inside those districts in PEPSU."),
    ("Kalka / Pinjore", "Panchkula is drawn in Punjab until 1966, then Haryana (Kalka went to Haryana in 1966)."),
    ("Chandernagore", "French until 1950-52, merged into West Bengal on 2 Oct 1954; inside Hugli district, not shown separately."),
    ("Tuensang", "Tuensang, Mon, Longleng and Kiphire districts stand for NEFA's Tuensang Frontier Division (to Naga Hills-Tuensang Area, 1957)."),
    ("Meghalaya 1970-71", "An autonomous State within Assam from 2 Apr 1970; drawn in Assam until full statehood on 21 Jan 1972."),
    ("Pakistan- and China-administered J&K", "Drawn as part of Jammu and Kashmir (to Oct 2019), following India's official boundary. The census file has no districts there; for 2019- the area is split on datameet's J&K UT / Ladakh UT line (PoK with J&K, Gilgit-Baltistan and Shaksgam with Ladakh; Aksai Chin is in Leh district)."),
]

UNMAPPED_NOTE = """`std` comes from `ncrb.entities.standardise(name)`. Where it returns no State/UT, `std` is the
State whose series NCRB continues and the feature carries `"std_from": "successor"` plus a `std_note`."""


def write_readme(era_list: list[dict], report: list[dict], cmp: list) -> None:
    rows = {r["file"]: r for r in report}
    L = ["# State/UT boundaries by year", "",
         "Generated by `scripts/build_geo_eras.py` (do not edit by hand; edit the script and rerun:",
         "`uv run --with shapely --with pyproj python scripts/build_geo_eras.py`).", "",
         "One GeoJSON per boundary era, so a choropleth for data year *Y* can draw the States and Union",
         "Territories that existed then. `eras.json` maps years to files:", "",
         "```json", '[{"from": 1951, "to": 1952, "file": "states-1951.geojson", "start": "1950-01-26", "note": "..."}, ...]', "```", "",
         "## Sources and licences", ""]
    for name, s in SOURCES.items():
        L.append(f"- **{s['credit']}**. {s['page']} (files: " + ", ".join(f"`{Path(f).name}`" for f in s["files"]) + f"). Licence: {s['licence']}.")
    L += ["- `india-outline.geojson` (unchanged) is the official external boundary drawn beneath the States.",
          "",
          "Attribution: *State/UT boundaries derived from Census 2011 district boundaries by the [DataMeet India community](http://datameet.org/) ([CC BY 2.5 India](https://creativecommons.org/licenses/by/2.5/in/)).*",
          "", "Raw downloads are cached in `data/geo_src/` (git-ignored); `data/geo_src/SOURCES.txt` lists the exact URLs.", "",
          "## Method", "",
          "Each era's States/UTs are unions of the 640 Census 2011 districts (plus the census file's undistricted",
          "Pakistan/China-administered part of J&K, split in two for 2019-). The districts are cleaned, snapped and",
          f"simplified once with mapshaper (weighted Visvalingam, {SIMPLIFY} of vertices, shapes kept, {PRECISION}° coordinates),",
          "then dissolved per era, so every era shares exactly the same lines and neighbouring features meet without gaps.",
          "Territory that was not part of India at the time (Portuguese Goa, Daman, Diu and Dadra & Nagar Haveli to 1961, French",
          "Pondicherry to 1954, Sikkim to 1975) has no feature in those eras; the outline drawn beneath shows it as blank.", "",
          "## Year rule", "",
          "NCRB tables report a calendar year. Each year uses the map in force on **31 December** of that year. So 1956 uses",
          "the post-reorganisation map (States Reorganisation Act, 1 Nov 1956), although most of 1956 ran under the old map;",
          "likewise 1953 shows Andhra State (from 1 Oct), 1960 shows Maharashtra and Gujarat (from 1 May), 2000 shows",
          "Chhattisgarh, Uttaranchal and Jharkhand (from November) and 2019 shows the two new UTs (from 31 Oct).", "",
          "## Eras", "",
          "| Years | File | In force from | Features | KB | What changed |", "|---|---|---|---|---|---|"]
    for e in era_list:
        r = rows[e["file"]]
        L.append(f"| {e['from']}–{e['to']} | `{e['file']}` | {e['start']} | {r['features']} | {r['kb']} | {e['note']} |")
    L += ["", "### States and UTs in each era", ""]
    for e in era_list:
        st = sorted(n for n, f in e["features"].items() if f["kind"] == "state")
        ut = sorted(n for n, f in e["features"].items() if f["kind"] == "ut")
        L.append(f"- **{e['from']}–{e['to']}** ({len(st)} States, {len(ut)} UTs/other). States: {', '.join(st)}. UTs: {', '.join(ut)}.")
    L += ["", "## Feature properties", "",
          "- `name`: the State/UT as named then (\"Bombay\", \"Madras\", \"Mysore\", \"Uttaranchal\", \"Orissa\" ...).",
          "- `std`: the modern standard name NCRB's pipeline gives that printed name (see the name map below).",
          "- `kind`: `state` or `ut`. Part C States (1950-56) are `state`; the Part D Andaman and Nicobar Islands, the North-East",
          "  Frontier Agency (constitutionally in Assam, run by the Centre) and the Naga Hills-Tuensang Area / Nagaland of 1957-63 are `ut`.",
          "- `covers`: present-day States/UTs (today's names) whose territory the feature includes, at district level.",
          "- `part`: `A`/`B`/`C`/`D` for 1951-1956 features (the 1950 Constitution's classes); `note`: special status, where any.",
          "- `std_from` / `std_note`: present when `std` is a successor because `standardise()` has no mapping.", "",
          "## Name map (name -> std)", "", UNMAPPED_NOTE, "", "| name | std | from | years |", "|---|---|---|---|"]
    seen: dict[str, list] = {}
    for e in era_list:
        for n in e["features"]:
            seen.setdefault(n, []).append((e["from"], e["to"]))
    for n in sorted(seen):
        std, how = std_of(n)
        yrs = f"{min(a for a, _ in seen[n])}–{max(b for _, b in seen[n])}"
        L.append(f"| {n} | {std} | {'standardise()' if how == 'standardise' else '**successor** (not mapped)'} | {yrs} |")
    L += ["", "## Approximations", "",
          "Lines are Census 2011 district lines. Where a historical transfer split a modern district, the whole district goes",
          "to the side holding most of it:", ""]
    L += [f"- **{a}**: {b}" for a, b in APPROXIMATIONS]
    L += ["", "## Validation", "",
          "Every file parses, has no empty geometry, and has exactly the features listed above. Area of the outline not covered",
          "by the era's features, and area of features outside the outline, as % of the outline (3.27 million km²):", "",
          "| File | outline not covered | outside outline | territory with no feature |", "|---|---|---|---|"]
    for r in report:
        L.append(f"| `{r['file']}` | {r['outline_minus_union_pct']}% | {r['union_minus_outline_pct']}% | {', '.join(r['omitted']) or '-'} |")
    L += ["", "The ~0.3% left either way when nothing is omitted is coastline, Sundarbans and island detail where the census",
          "district file and the outline were digitised differently.", "",
          "### Against the old `india-states.geojson` (2014-2018 file)", "",
          "Intersection over union per feature. The old file leaves Pakistan- and China-administered J&K out of Jammu and Kashmir",
          "(the outline shows it), which is why J&K differs; the rest differ only by digitising detail.", "",
          "| Feature | IoU |", "|---|---|"]
    L += [f"| {n} | {v} |" for n, v in cmp]
    (OUT / "README.md").write_text("\n".join(L) + "\n")


def main() -> None:
    download()
    geoms, base = build_units()
    era_list = eras(base)
    units = write_units(geoms, base, era_list)
    mapshaper(units, era_list)
    write_eras(era_list, base)
    report = validate(era_list, base)
    cmp = compare_current(era_list)
    write_readme(era_list, report, cmp)
    for r in report:
        print(f"{r['file']:24} {r['years']:10} {r['features']:3} features {r['kb']:4} KB  outline-not-covered {r['outline_minus_union_pct']:5}%  "
              f"outside {r['union_minus_outline_pct']:4}%  omitted: {', '.join(r['omitted']) or '-'}")
    print("IoU vs old india-states.geojson (2014 file):", ", ".join(f"{n} {v}" for n, v in cmp))


if __name__ == "__main__":
    main()
