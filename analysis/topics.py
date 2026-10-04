"""The questions this analysis answers, as table-finding rules.

Each topic names the publication, a title pattern (with exclusions), a header
pattern the right table must contain, and the place whose rows are wanted.
``tables_for(topic)`` returns one table per year, oldest first.
"""

from __future__ import annotations

from .lib import find_tables, pick_per_year

TOPICS = {
    # Number of traffic accidents by time of day, Chennai (Madras before 1996)
    "traffic_time_chennai": dict(
        pub="adsi", title=r"time of occurrence", exclude=r"persons injured|all.?india", require=r"hrs|hours", place="chennai",
    ),
    # Number of traffic accidents by month, Chennai (city-wise tables stop in 2020)
    "traffic_month_chennai": dict(
        pub="adsi", title=r"month", exclude=r"persons injured|all.?india", require=r"jan|feb|mar", place="chennai",
    ),
    # Persons died in traffic accidents by time of day / month, Tamil Nadu (state-level, 2021 onwards)
    "traffic_time_deaths_tn": dict(
        pub="adsi", title=r"time of occurrence.*persons injured|persons injured.*time of occurrence", place="tamil_nadu",
    ),
    "traffic_month_deaths_tn": dict(
        pub="adsi", title=r"month of occurrence.*persons injured|persons injured.*month", place="tamil_nadu",
    ),
    # Suicides by means adopted, Tamil Nadu
    "suicide_means_tn": dict(
        pub="adsi", title=r"means", exclude=r"all.?india|percentage share of suicide committed|city wise|age wise details|percentage distribution|prominent means|percentage share", place="tamil_nadu",
    ),
    "suicide_means_age_tn": dict(  # 2021 onwards: means x sex x age, state-wise
        pub="adsi", title=r"age wise details of suicide victims according to means", place="tamil_nadu",
    ),
    # Suicides by profession and sex, Tamil Nadu
    "suicide_profession_tn": dict(
        pub="adsi", title=r"profession", exclude=r"all.?india|age wise details|city wise", place="tamil_nadu",
    ),
    "suicide_profession_age_tn": dict(  # 2021 onwards: profession x sex x age, state-wise
        pub="adsi", title=r"age wise details of suicide victims according to their profession", place="tamil_nadu",
    ),
    # Suicides by sex and age group: Tamil Nadu and the cities
    "suicide_sex_age_tn": dict(
        pub="adsi", title=r"suicid.*(sex|gender).*age|suicid.*age.*(sex|gender)|(sex|gender).*age.*suicid|age.*(sex|gender).*suicid|suicid.*age.?groups?|age.?groups?.*suicid",
        exclude=r"all.?india|profession|means|cause|education|marital|social|economic|farmer|cultivator|mass|family|accident", place="tamil_nadu",
    ),
    "suicide_sex_age_chennai": dict(
        pub="adsi", title=r"suicid.*(sex|gender).*age|suicid.*age.*(sex|gender)|(sex|gender).*age.*suicid|age.*(sex|gender).*suicid|suicid.*age.?groups?|age.?groups?.*suicid",
        exclude=r"all.?india|profession|means|cause|education|marital|social|economic|farmer|cultivator|mass|family|accident", place="chennai",
    ),
    # The same tables for the cities, where NCRB printed them separately (2014-2015 'City wise')
    "suicide_means_city": dict(
        pub="adsi", title=r"suicid.*means|means.*suicid", exclude=r"all.?india|percentage share|age wise details|age.?group", place="chennai",
    ),
    "suicide_profession_city": dict(
        pub="adsi", title=r"profession", exclude=r"all.?india|age wise details", place="chennai",
    ),
    # Suicides by causes, and by educational status
    "suicide_causes_tn": dict(
        pub="adsi", title=r"suicid.*cause|cause.*suicid", exclude=r"all.?india|age|farm|cultivat|labour|share|student|female|cities and", place="tamil_nadu",
    ),
    "suicide_causes_city": dict(
        pub="adsi", title=r"suicid.*cause|cause.*suicid", exclude=r"all.?india|age|farm|cultivat|labour|share|student|female|cities and", place="chennai",
    ),
    "suicide_education_tn": dict(
        pub="adsi", title=r"education", exclude=r"all.?india|percentage|social, economic", place="tamil_nadu",
    ),
    "suicide_education_city": dict(
        pub="adsi", title=r"education", exclude=r"all.?india|percentage|social, economic", place="chennai",
    ),
    # Incidence and rate of suicides (the State/UT & city table), every State, UT and city
    "suicide_rate": dict(
        pub="adsi", title=r"(incidence|volume).*(suicid)|suicid.*(rate|volume)",
        exclude=r"all.?india|decade|during \d{4} to \d{4}|growth of population|clock|countries|prone|proportion|causes|means|sex|age|figure|accidental|inopportune",
        require=r"rate|volume|per (one )?lakh", place="tamil_nadu",
    ),
}


def tables_for(name: str):
    t = TOPICS[name]
    c = find_tables(t["pub"], t["title"], exclude=t.get("exclude"))
    return pick_per_year(c, t.get("place"), require=t.get("require"))
