"""Map the categories NCRB printed in different years onto one stable list.

Wording and grouping change between editions ("Poison (Consuming insecticides)"
in 2004, "By Poison (By Consuming Insecticides)" in 2014). Each mapping is an
ordered list of (pattern, standard name); the first match wins. ``None`` means
the column is a subtotal of others in the same table and is dropped so nothing
is counted twice. The printed label is always kept next to the standard one.
"""

from __future__ import annotations

import re

MEANS = [
    (r"^\W*(grand\s+)?total\W*$|^total\b(?!.*poison)|^\W*grand\b", None),
    (r"\(total\)|\btotal\)", None),  # parent rows such as 'By Poison (Total)'
    (r"insecticid", "Poison: insecticides"),
    (r"poison", "Poison: other"),
    (r"hang", "Hanging"),
    (r"drown", "Drowning"),
    (r"fire.?arm", "Firearms"),
    (r"fire|immolat", "Fire / self-immolation"),
    (r"sleeping|overdose|drugs?\b", "Sleeping pills / drug overdose"),
    (r"running vehicle|moving vehicle|under.*train|train|vehicle", "Under or off vehicles & trains"),
    (r"jump", "Jumping from height"),
    (r"electrocut", "Electrocution"),
    (r"self.?inflict", "Self-inflicted injury"),
    (r"alcohol", "Over-drinking alcohol"),
    (r"machine", "Machine"),
    (r"other|not known|unknown", "Other / not known"),
]

PROFESSION = [
    (r"^\W*(grand\s+)?total\W*$|^\W*grand\b", None),
    (r"\(total\)|\btotal\)|\btotal\]", None),
    (r"house\s*wife", "House wife"),
    (r"student", "Student"),
    (r"unemploy", "Unemployed"),
    (r"retire", "Retired"),
    (r"daily wage", "Daily wage earner"),
    (r"agricultur\w* labou?r", "Agricultural labourer"),
    (r"farm|cultivat", "Farmer / cultivator"),
    (r"public sector|\bpsu\b|undertaking", "Public sector undertaking"),
    (r"govern|govt", "Government servant"),
    (r"private", "Private sector"),
    (r"business", "Self-employed: business"),
    (r"professional activit|self.?employ|other self", "Self-employed: other"),
    (r"salaried|service", "Salaried (other)"),
    (r"other|not known|unknown", "Other / not known"),
]


def standard(label: str, table: list[tuple[str, str | None]]) -> str | None:
    t = re.sub(r"\s+", " ", re.sub(r"[–—]", "-", label or "")).strip().lower()
    for rx, name in table:
        if re.search(rx, t):
            return name
    return "Other / not known"


# Age groups as printed, named by the ages they cover. 2004-2013 used up to 14,
# 15-29, 30-44, 45-59, 60+; from 2014 'below 14, 14-18, 18-30, 30-45, 45-60, 60+'
# where '18-30' means 18 and above, below 30. So 30-44, 45-59 and 60+ run
# unbroken from 2004; the younger groups were re-cut in 2014 (see YOUNG).
AGE = [
    # headings cut short or run into the next line in some PDFs ('45 Yr and above – below 30 years 45 years'): the lower bound identifies the group
    (r"^14\D*above", "14-17"),
    (r"^18\D*above", "18-29"),
    (r"^30\D*above", "30-44"),
    (r"^45\D*above", "45-59"),
    (r"(up\s*to|upto|below|under|less than)\s*14|0\s*-\s*14|^\D*14\D*$(?<!above)", "0-14"),
    (r"14.*18|15\s*-\s*18", "14-17"),
    (r"(below|under)\s*18|0\s*-\s*17", "0-17"),
    (r"15\s*-\s*29|15.*30", "15-29"),
    (r"18.*30", "18-29"),
    (r"30\s*-\s*44|30.*45", "30-44"),
    (r"45\s*-\s*59|45.*60", "45-59"),
    (r"60|above\s*59", "60+"),
    (r"total", "all ages"),
]
AGE_ORDER = ["0-14", "0-17", "14-17", "15-29", "18-29", "30-44", "45-59", "60+", "all ages"]
YOUNG = {"0-14", "0-17", "14-17", "15-29", "18-29"}  # together: 'under 30' in every edition


def age_band(label: str) -> str:
    t = re.sub(r"\s+", " ", re.sub(r"[–—]", "-", label or "")).strip().lower()
    for rx, name in AGE:
        if re.search(rx, t):
            return name
    return t or "all ages"
