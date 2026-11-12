# CII 1992, Table 6: incidence of cognizable IPC crime by crime head, 23 cities
# (raw/cii/1992/table_content/table-6-1992-survey.pdf, pages 2, 4, 6, 8, 10, printed pages 44, 46, 48, 50, 52; the odd
# pages are the States and UTs, in cii_1992_crime.py). Read from the page images; the rate (R) columns are skipped.
# Kidnapping & abduction is the printed total; its two printed sub-columns (of women & girls, of others) are left out so
# the heads add up to the Total. The cities have no printed total row. Every row adds up to its printed Total cognizable
# crimes under IPC (scripts/check_handread.py), with no corrections. Madras kidnapping & abduction is printed 35 (35 of
# women & girls, 0 of others, rate 0.6). Bhopal dacoity is printed 268 (rate 24.4) and its row adds up with it.
KIND, YEAR, PUB = "crime", 1992, "cii"
SOURCE = "raw/cii/1992/table_content/table-6-1992-survey.pdf"
PAGES = "2, 4, 6, 8, 10"
TITLE = "Table 6: Incidence (I) & rate (R) of cognizable crimes (IPC) under different crime heads in States, UTs & cities during 1992"
CATS = ["Murder", "Attempt to commit murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Preparation & assembly for dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Other IPC crimes", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "Cities": {
  "Ahmedabad": [158, 163, 3, 27, 205, 35, 0, 131, 953, 4935, 390, 462, 576, 40, 11797, 19875],
  "Bangalore": [151, 205, 2, 27, 84, 43, 0, 172, 1830, 7793, 618, 262, 716, 2056, 12288, 26247],
  "Bhopal": [116, 135, 20, 44, 24, 268, 3, 77, 493, 1089, 244, 21, 89, 12, 4824, 7459],
  "Bombay": [487, 289, 5, 104, 341, 139, 52, 1219, 2708, 15977, 446, 729, 1181, 96, 17206, 40979],
  "Calcutta": [83, 144, 23, 38, 132, 39, 15, 160, 345, 6536, 624, 346, 638, 31, 4956, 14110],
  "Coimbatore": [27, 33, 0, 1, 10, 2, 0, 15, 285, 1242, 349, 34, 58, 95, 1470, 3621],
  "Delhi": [418, 466, 357, 236, 846, 27, 31, 258, 1400, 13190, 266, 630, 1408, 95, 13427, 33055],
  "Hyderabad": [153, 140, 6, 41, 103, 28, 0, 126, 1344, 3594, 267, 83, 424, 130, 3867, 10306],
  "Indore": [93, 204, 0, 32, 36, 4, 2, 89, 1108, 2881, 81, 40, 65, 0, 6178, 10813],
  "Jaipur": [47, 60, 1, 27, 144, 0, 2, 77, 566, 2339, 1265, 166, 466, 64, 4189, 9413],
  "Kanpur": [286, 263, 27, 38, 207, 51, 67, 225, 707, 2119, 461, 333, 286, 77, 2965, 8112],
  "Kochi": [21, 16, 0, 10, 8, 3, 0, 11, 319, 266, 189, 21, 96, 4, 2356, 3320],
  "Lucknow": [112, 151, 15, 46, 102, 16, 7, 119, 760, 2784, 234, 234, 305, 30, 2769, 7684],
  "Ludhiana": [69, 73, 8, 6, 25, 1, 8, 4, 99, 121, 3, 11, 26, 0, 305, 759],
  "Madras": [106, 169, 7, 17, 35, 4, 0, 116, 667, 5464, 174, 188, 516, 323, 5388, 13174],
  "Madurai": [36, 54, 0, 1, 18, 0, 0, 17, 227, 1092, 84, 17, 61, 103, 1665, 3375],
  "Nagpur": [131, 47, 1, 48, 79, 23, 2, 342, 876, 3645, 182, 124, 195, 45, 4676, 10416],
  "Patna": [192, 301, 26, 21, 111, 24, 9, 218, 400, 2101, 185, 99, 159, 0, 3389, 7235],
  "Pune": [105, 39, 2, 51, 65, 16, 5, 114, 1001, 3190, 171, 84, 175, 30, 6348, 11396],
  "Surat": [162, 58, 1, 17, 52, 138, 0, 58, 387, 1472, 405, 76, 230, 4, 1807, 4867],
  "Vadodara": [52, 31, 2, 4, 50, 9, 0, 38, 445, 1960, 348, 149, 282, 9, 3780, 7159],
  "Varanasi": [72, 103, 26, 8, 45, 14, 4, 75, 324, 876, 147, 91, 72, 0, 1137, 2994],
  "Vishakhapatnam": [31, 31, 1, 16, 5, 4, 0, 42, 458, 1286, 67, 60, 119, 10, 1768, 3898],
 },
}
