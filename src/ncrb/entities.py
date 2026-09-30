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
}
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
    s = re.sub(r"[@#*$+^]+", " ", s)
    return re.sub(r"[^A-Z0-9]+", " ", s).strip()


def standardise(label: str) -> tuple[str, str]:
    """(standard name, entity type) for a printed row label.

    Entity type is one of ``state``, ``ut``, ``total`` or ``other``. Labels that
    are not a recognised State/UT or total row (cities, crime heads, years...)
    are returned cleaned but otherwise unchanged with type ``other``.
    """
    raw = re.sub(r"\s+", " ", label).strip()
    up = raw.upper()
    for rx, name in TOTALS:
        if rx.search(up):
            return name, "total"
    if re.match(r"^\s*(SUB[\s-]*)?TOTAL\b", up):
        return raw, "total"
    k = key(raw)
    name = ALIASES.get(k)
    if name:
        return name, "state" if name in STATES else "ut"
    return raw, "other"
