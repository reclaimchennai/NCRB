"""Standard names for States, Union Territories and summary rows.

NCRB spells the same place differently across years ("ORISSA" / "Odisha",
"A & N ISLANDS" / "Andaman & Nicobar Islands") and places have been renamed,
split and merged. ``standardise`` maps a printed row label to one canonical
name so tables from different years can be joined. The printed label is always
kept alongside; nothing is merged across real boundary changes (e.g. Andhra
Pradesh before and after Telangana keep the same name but are not the same
territory; see docs/DATA_NOTES.md).
"""

from __future__ import annotations

import re

STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
]
UTS = [
    "Andaman & Nicobar Islands", "Chandigarh", "Dadra & Nagar Haveli", "Daman & Diu",
    "Dadra & Nagar Haveli and Daman & Diu", "Delhi", "Jammu & Kashmir", "Ladakh", "Lakshadweep", "Puducherry",
]

# normalised printed form -> canonical name
ALIASES = {
    "ORISSA": "Odisha",
    "UTTARANCHAL": "Uttarakhand",
    "UTTARAKHAND": "Uttarakhand",
    "PONDICHERRY": "Puducherry",
    "A N ISLANDS": "Andaman & Nicobar Islands",
    "A AND N ISLANDS": "Andaman & Nicobar Islands",
    "AN ISLANDS": "Andaman & Nicobar Islands",
    "ANDAMAN NICOBAR ISLANDS": "Andaman & Nicobar Islands",
    "ANDAMAN AND NICOBAR ISLANDS": "Andaman & Nicobar Islands",
    "ANDAMAN NICOBAR": "Andaman & Nicobar Islands",
    "D N HAVELI": "Dadra & Nagar Haveli",
    "D AND N HAVELI": "Dadra & Nagar Haveli",
    "DN HAVELI": "Dadra & Nagar Haveli",
    "DADRA NAGAR HAVELI": "Dadra & Nagar Haveli",
    "DADRA AND NAGAR HAVELI": "Dadra & Nagar Haveli",
    "DAMAN DIU": "Daman & Diu",
    "DAMAN AND DIU": "Daman & Diu",
    "D N HAVELI AND DAMAN DIU": "Dadra & Nagar Haveli and Daman & Diu",
    "D N HAVELI DAMAN DIU": "Dadra & Nagar Haveli and Daman & Diu",
    "DNH AND DAMAN DIU": "Dadra & Nagar Haveli and Daman & Diu",
    "DADRA AND NAGAR HAVELI AND DAMAN AND DIU": "Dadra & Nagar Haveli and Daman & Diu",
    "DADRA NAGAR HAVELI AND DAMAN DIU": "Dadra & Nagar Haveli and Daman & Diu",
    "DELHI": "Delhi",
    "DELHI UT": "Delhi",
    "NCT OF DELHI": "Delhi",
    "DELHI NCT": "Delhi",
    "J K": "Jammu & Kashmir",
    "JAMMU KASHMIR": "Jammu & Kashmir",
    "JAMMU AND KASHMIR": "Jammu & Kashmir",
    "TAMILNADU": "Tamil Nadu",
    "CHATTISGARH": "Chhattisgarh",
    "CHHATISGARH": "Chhattisgarh",
    "TELENGANA": "Telangana",
    "LAKSHDWEEP": "Lakshadweep",
    "LACCADIVE MINICOY AND AMINDIVI ISLANDS": "Lakshadweep",
    "MYSORE": "Karnataka",
    "MADRAS": "Tamil Nadu",
    # OCR forms of the old scans
    "TAMIL MADU": "Tamil Nadu", "TAMIL NADN": "Tamil Nadu", "TAMIL NEDU": "Tamil Nadu", "TAMILNEDU": "Tamil Nadu", "TAMIL NADU T": "Tamil Nadu",
    "W BENGAL": "West Bengal", "M PRADESH": "Madhya Pradesh", "U PRADESH": "Uttar Pradesh", "H PRADESH": "Himachal Pradesh",
    "A PRADESH": "Andhra Pradesh", "EAST PUNJAB": "Punjab",
    # names of the 1950s-70s that continue as one of today's (same territory, renamed)
    "LACCADIVES": "Lakshadweep", "LACCADIVE MINICOY AMINDIVI ISLANDS": "Lakshadweep", "L M A ISLANDS": "Lakshadweep",
    "L M AND A ISLANDS": "Lakshadweep", "LM AND A ISLANDS": "Lakshadweep", "LMA ISLANDS": "Lakshadweep",
    "NAGA HILLS": "Nagaland", "NAGA HILLS TUENSANG AREA": "Nagaland", "NAGA HILLS TUENSANG": "Nagaland",
    # States that were split or merged away: kept under their own names, never folded into a successor
    "MADHYA BHARAT": "Madhya Bharat", "PEPSU": "PEPSU", "P E P S U": "PEPSU", "PATIALA AND EAST PUNJAB STATES UNION": "PEPSU",
    "PATIALA EAST PUNJAB STATES UNION": "PEPSU", "SAURASHTRA": "Saurashtra", "TRAVANCORE COCHIN": "Travancore-Cochin",
    "TRAVANCORE AND COCHIN": "Travancore-Cochin", "VINDHYA PRADESH": "Vindhya Pradesh", "COORG": "Coorg", "KUTCH": "Kutch",
    "BOMBAY STATE": "Bombay State", "HYDERABAD STATE": "Hyderabad State", "BHOPAL STATE": "Bhopal State", "AJMER STATE": "Ajmer State",
    "BILASPUR STATE": "Bilaspur State", "ANDHRA STATE": "Andhra State", "NEFA": "NEFA", "N E F A": "NEFA",
    "NORTH EAST FRONTIER AGENCY": "NEFA", "NORTH EAST FRONTIER TRACT": "NEFA",
    "GOA DAMAN DIU": "Goa, Daman & Diu", "GOA DAMAN AND DIU": "Goa, Daman & Diu",
}
# States and UTs of the past, with their kind
HISTORIC = {
    "Bombay State": "state", "Hyderabad State": "state", "Madhya Bharat": "state", "PEPSU": "state", "Saurashtra": "state",
    "Travancore-Cochin": "state", "Vindhya Pradesh": "state", "Bhopal State": "state", "Ajmer State": "state", "Coorg": "state",
    "Kutch": "state", "Bilaspur State": "state", "Andhra State": "state", "NEFA": "ut", "Goa, Daman & Diu": "ut",
}
# printed names that were a State until a year and a city (or today's State's name) after it: only the table's year can tell
BY_YEAR = {"BOMBAY": (1959, "Bombay State"), "HYDERABAD": (1956, "Hyderabad State"), "BHOPAL": (1956, "Bhopal State"),
           "AJMER": (1956, "Ajmer State"), "BILASPUR": (1954, "Bilaspur State"), "ANDHRA": (1956, "Andhra State")}
for _n in STATES + UTS:
    ALIASES.setdefault(re.sub(r"[^A-Z0-9]+", " ", _n.upper().replace("&", " ")).strip(), _n)

TOTALS = [
    (re.compile(r"\bALL\s*INDIA\b|^INDIA$|\bGRAND\s+TOTAL\b|^TOTAL\s+ALL\b"), "All India"),
    (re.compile(r"\bTOTAL\b.*\bSTATES?\b|^STATES?\s+TOTAL"), "Total (States)"),
    (re.compile(r"\bTOTAL\b.*\bU\.?\s*T\.?S?\b|\bTOTAL\b.*UNION"), "Total (UTs)"),
    (re.compile(r"\bTOTAL\b.*\bCIT(Y|IES)\b"), "Total (Cities)"),
]


def key(label: str) -> str:
    s = label.upper().replace("&", " ")
    s = re.sub(r"\(.*?\)", " ", s) if not re.search(r"TOTAL", s) else s
    s = re.sub(r"\[LINE \d+\]", " ", s)                    # '[line 2]' left by a wrapped OCR row label
    s = re.sub(r"[@#*$+^]+", " ", s)
    return re.sub(r"[^A-Z0-9]+", " ", s).strip()


def kind_of(name: str) -> str:
    return "state" if name in STATES else HISTORIC.get(name, "ut")


def standardise(label: str, year: int | None = None) -> tuple[str, str]:
    """(standard name, entity type) for a printed row label.

    Entity type is one of ``state``, ``ut``, ``total`` or ``other``. Labels that
    are not a recognised State/UT or total row (cities, crime heads, years...)
    are returned cleaned but otherwise unchanged with type ``other``. ``year``
    (the table's year) settles names that were a State only until then
    (Bombay to 1959, Hyderabad, Bhopal, Ajmer and Andhra to 1956).
    """
    raw = re.sub(r"\s+", " ", label).strip()
    up = raw.upper()
    for rx, name in TOTALS:
        if rx.search(up):
            return name, "total"
    if re.match(r"^\s*(SUB[\s-]*)?TOTAL\b", up):
        return raw, "total"
    k = key(raw)
    if year and k in BY_YEAR and year <= BY_YEAR[k][0]:
        name = BY_YEAR[k][1]
        return name, kind_of(name)
    name = ALIASES.get(k)
    if name:
        return name, kind_of(name)
    return raw, "other"
