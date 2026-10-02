"""One stable list of topics for the Explore page.

NCRB's own chapter names drift ("Cyber Crime", "Cyber Crimes", "Cyber Crimes
(States/UTs)", "Cyber Crimes (34 Metropolitan Cities)"...), and many tables
sit under catch-alls ("ADSI Additional Tables 2014", "States/UTs", "Mega
City", "Annexures"). Each table is classified by its chapter and its title
together, first matching rule wins; geography (States/UTs, cities, all India)
becomes a separate property of the table instead of part of the topic.
"""

from __future__ import annotations

import re

RULES = {
    "cii": [
        (r"cyber", "Cyber crime"),
        (r"missing", "Missing persons & children"),
        (r"juvenile", "Juveniles in conflict with law"),
        (r"senior citizen", "Crime against senior citizens"),
        (r"scheduled tribe|\bsts?\b(?!ate)", "Crime against Scheduled Tribes"),
        (r"scheduled caste|\bscs?\b|dalit|untouchab|protection of civil rights|pcr act", "Crime against Scheduled Castes"),
        (r"against children|child|pocso|infanticide|foeticide|minor girls", "Crime against children"),
        (r"against women|women|dowry|rape|modesty|cruelty by husband|sati|immoral traffic", "Crime against women"),
        (r"trafficking", "Human trafficking"),
        (r"kidnap|abduct", "Kidnapping & abduction"),
        (r"foreigner", "Crime by and against foreigners"),
        (r"railway", "Crime in railways"),
        (r"custod|complaints against police|human rights violation", "Custodial crime & complaints against police"),
        (r"police firing|casualt|lathi|police personnel killed|injuries", "Police firing & casualties"),
        (r"police strength|expenditure|infrastructure|vehicles|police station|training", "Police strength & infrastructure"),
        (r"economic offence|counterfeit|forgery|cheating|criminal breach|fraud", "Economic offences"),
        (r"corruption|prevention of corruption", "Corruption"),
        (r"property stolen|recovered|value of property", "Property stolen & recovered"),
        (r"seizure|narcotic|ndps|arms|explosive", "Seizures, arms & narcotics"),
        (r"environment|forest|wild ?life|pollution", "Offences against the environment"),
        (r"against the state|anti.?national|extremist|insurgent|terror|naxal|left wing|sedition|unlawful activities", "Offences against the State"),
        (r"recidivism", "Recidivism"),
        (r"disposal of cases by police|police disposal|chargesheet|charge.?sheet|investigation", "Police disposal of cases"),
        (r"disposal of cases by courts|court disposal|trials|conviction|acquittal", "Court disposal & convictions"),
        (r"persons arrested|arrest", "Persons arrested"),
        (r"special (and|&) local laws|\bsll\b", "Special & local laws"),
        (r"murder|homicide|culpable", "Murder & violent crime"),
        (r"riot|hurt|assault|violent", "Murder & violent crime"),
        (r"theft|burglary|robbery|dacoity|snatching", "Property crime"),
        (r"motive", "Motives behind crime"),
        (r"\bipc\b|indian penal code|cognizable|crime rate|incidence|total crime", "Crime overall (IPC)"),
    ],
    "adsi": [
        (r"farmer|agricultur|cultivator", "Farm suicides"),
        (r"armed police|capf", "Deaths in the armed police forces"),
        (r"suicid", "Suicides"),
        (r"railway crossing|railway accident|railway", "Railway crashes"),
        (r"time of occurrence|months? of occurrence|quarter", "Traffic crashes: when"),
        (r"traffic|road|vehicle|mode of transport|motor", "Road crashes"),
        (r"fire", "Fire"),
        (r"un.?natural", "Accidental deaths: unnatural causes"),
        (r"forces of nature|natural cause|lightning|flood|heat|cold", "Accidental deaths: forces of nature"),
        (r"drown|electrocut|poison|fall|other causes|un.?natural", "Other accidental deaths"),
        (r"accident", "Accidental deaths overall"),
    ],
    "psi": [
        (r"death|illness|suicide", "Deaths in prison"),
        (r"break|escape|clash|firing|riot", "Jail breaks, escapes & clashes"),
        (r"foreign", "Foreign prisoners"),
        (r"undertrial|period of detention|detention", "Undertrial prisoners"),
        (r"convict|sentence|capital punishment|death sentence", "Convicts & sentences"),
        (r"release|parole|transfer|movement|furlough|escort", "Releases, transfers & parole"),
        (r"capacity|occupancy|overcrowd|population|jails? \(|type of jail|central jail|district jail|sub jail|open jail|special jail|borstal", "Prisons & overcrowding"),
        (r"demograph|age|caste|religion|education|domicile|sex|gender|women|children", "Who is in prison"),
        (r"offence|ipc|sll|crime head", "Prisoners by offence"),
        (r"staff|strength|official|officer|training|vacanc", "Prison staff"),
        (r"budget|expenditure|infrastructure|vehicle|electronic|quarter|construction", "Budget & infrastructure"),
        (r"vocational|welfare|rehabilitat|education|wages|product|legal aid|literacy", "Work, education & welfare"),
        (r"inspection|visit|grievance", "Inspections & visits"),
        (r"recidiv|habitual", "Repeat offenders"),
        (r"inmate|prisoner|jail|prison", "Prisoners overall"),
    ],
}
_COMPILED = {p: [(re.compile(rx, re.I), name) for rx, name in rules] for p, rules in RULES.items()}


def topic_of(pub: str, chapter: str | None, title: str | None) -> str:
    """The title decides first (it is specific); the chapter only where the title says nothing classifiable."""
    for text in (title or "", f"{chapter or ''} {title or ''}"):
        for rx, name in _COMPILED.get(pub, []):
            if rx.search(text):
                return name
    return "Other tables"


GEO = [
    (re.compile(r"metropolitan|mega city|city.?wise|cities|\bcity\b", re.I), "city"),
    (re.compile(r"\bstates?\b|\buts?\b|union territor", re.I), "state"),
    (re.compile(r"all.?india|crime.?head.?wise|cause.?wise\b(?!.*state)", re.I), "india"),
]


def geo_of(chapter: str | None, title: str | None) -> str:
    t = f"{title or ''}"
    if GEO[1][0].search(t):          # 'State/UT & City-wise': States first, the cities come along as rows
        return "state"
    for rx, tag in GEO:
        if rx.search(t):
            return tag
    for rx, tag in GEO[:2]:
        if rx.search(chapter or ""):
            return tag
    return ""


GEO_WORDS = re.compile(
    r"\s*[\(\[]?\s*(state\s*[/&,-]?\s*(ut|uts)?\s*[&,]?\s*(and\s+)?(city)?\s*[-–]?\s*wise|states?\s*(&|and)\s*uts?(\s*-\s*wise)?|"
    r"state\s*[/-]\s*ut\s*-?\s*wise|city\s*[-–]?\s*wise|all[\s-]*india|in\s+(34\s+)?metropolitan\s+cities|metropolitan\s+cities|"
    r"\d+\s+metropolitan\s+cities|crime\s*head\s*[-–]?\s*wise|states?\s*,\s*uts?\s*(&|and)\s*city[\s-]*wise|states?\s*/\s*uts?)\s*[\)\]]?", re.I)


PROSE = re.compile(r"\b(has|have|was|were|accounting|followed|showing|compared|respectively|however|whereas|a total of|more than the|presented in|shown in|the following)\b", re.I)
MARK = re.compile(r"\s*\b(?:FIGURE|Figure|LIST|List|CHART|Chart|Table)\s*[—–-]*\s*\d+[A-Z]?(?:\.\d+)*(?:\s*\([A-Z]\))?\s*[:.\-–]?\s*")


def prose(t: str) -> bool:
    """A title captured with the report's running text around it."""
    t = str(t or "")
    hits = len(PROSE.findall(t))
    numbers = bool(re.search(r"\d,\d{2,3}|\d\.\d+\s*%|\(\d[\d,]{3,}", t))
    return len(t) > 160 or bool(re.match(r"^[^\w(]", t)) or hits >= 2 or numbers or (hits >= 1 and len(t) > 80)


def running_text(t: str) -> bool:
    """Sentences of the report, not a table title: dropped rather than shown as one."""
    t = str(t or "")
    return len(re.findall(r"[A-Za-z]", t)) < 6 or len(PROSE.findall(t)) >= 1 or bool(re.search(r"\d,\d{2,3}|\d\.\d+\s*%|\(\d[\d,]{3,}", t))


def clean_title(title: str) -> str:
    """NCRB's title without numbering, years, continuation marks, Roman-numeral part labels or geography."""
    t = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", str(title or ""))
    t = re.sub(r"\s+", " ", t).strip()
    # text around 'FIGURE 1.2' / 'LIST-2.4' / 'Table - 2 (M)' markers: the first stretch that reads like a title
    segs = [x.strip(" .,;:-–") for x in MARK.split(t)]
    segs = [x for x in segs if len(x.split()) >= 2]
    if len(segs) > 1:
        t = next((x for x in segs if not prose(x)), segs[-1])
    t = re.sub(r"^[\]\)\s.]*\(?[A-Z]\)\s+", "", t)                 # '] P) ', '(J) ', 'M) ' part labels
    t = re.sub(r"\((?:contd|concld|concluded|continued)[^)]*\)", "", t, flags=re.I)
    t = re.sub(r"^\W*(?:(?:table|list|figure|statement|appendix)\W*)?[0-9]+[A-Z]?(?:[.\-][0-9]+[A-Z]?)*\s*[-–—_:.]*\s*", "", t, flags=re.I)
    t = re.sub(r"^\s*(?:[IVX]{1,4}|[a-h])[.)]\s+", "", t)            # 'II. Economic Status', 'a) ...'
    t = re.sub(r"^\s*table[_\s]*[ivx\d]+\b\s*[,.:-]*\s*", "", t, flags=re.I)  # 'Table_VII ...'
    t = re.sub(r"\s*[-–,]?\s*\b(during|in|for)?\s*(the\s+year\s+)?(19|20)\d\d(\s*(to|-|–|&|and)\s*(19|20)\d\d)?\b", "", t, flags=re.I)
    t = re.sub(r"\bduring\b\s*$", "", t, flags=re.I)
    # '(Crime Head-wise & States/UT-wise)', '(State/UT & City-wise)': brackets that only name the geography
    t = re.sub(r"\((?:\s*(?:crime|head|cause|wise|states?|uts?|union|territor(?:y|ies)|city|cities|metropolitan|mega|all|india|and|\d+|[&/,\-–]))+\s*\)", " ", t, flags=re.I)
    t = GEO_WORDS.sub(" ", t)
    t = re.sub(r"\(\s*[,&/-]*\s*\)", "", t)
    t = re.sub(r"\s*[-–]+\s*wise\b", "-wise", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip(" -–—,:.;")
    t = re.sub(r"\s+(during|in|for)$", "", t, flags=re.I).strip(" -–—,:.;")
    t = re.sub(r"^[&,/\s]+", "", t)
    t = re.sub(r"^[\W_]*wise\b\s*[&,]?\s*", "", t, flags=re.I)              # '‐wise & Purpose‐wise ...' left by a stripped 'State/UT'
    t = re.sub(r"[\u2010\u2011]", "-", t)
    if t.isupper():
        t = t.capitalize()
        t = re.sub(r"\b(ipc|sll|it|ndps|pocso|sc|st|scs|sts|ut|uts|capf|rpf|grp)\b", lambda m: m.group(0).upper(), t, flags=re.I)
        t = re.sub(r"\bi\.? ?t\.?(?= act)", "IT", t, flags=re.I)
    return t[:1].upper() + t[1:] if t else t
