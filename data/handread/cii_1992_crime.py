# CII 1992, Table 6: incidence of cognizable IPC crime by crime head, States / UTs
# (raw/cii/1992/table_content/table-6-1992-survey.pdf, pages 1, 3, 5, 7, 9, printed pages 43, 45, 47, 49, 51; the even
# pages are the cities, in cii_1992_crime_cities.py). Read from the page images; the rate (R) columns are skipped.
# Kidnapping & abduction is the printed total; its two printed sub-columns (of women & girls, of others) are left out so
# the heads add up to the Total. The printed 'TOTAL (ALL-INDIA)' row is GRAND TOTAL here. Every row adds up to its
# printed Total cognizable crimes under IPC and every State / UT column to the printed totals
# (scripts/check_handread.py), with no corrections; digits broken in the print (theft, Meghalaya to Uttar Pradesh;
# counterfeiting, Tamil Nadu 999 and Uttar Pradesh 246) were confirmed by the row and column totals.
KIND, YEAR, PUB = "crime", 1992, "cii"
SOURCE = "raw/cii/1992/table_content/table-6-1992-survey.pdf"
PAGES = "1, 3, 5, 7, 9"
TITLE = "Table 6: Incidence (I) & rate (R) of cognizable crimes (IPC) under different crime heads in States, UTs & cities during 1992"
CATS = ["Murder", "Attempt to commit murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Preparation & assembly for dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Other IPC crimes", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2780, 1512, 74, 773, 955, 846, 4, 1219, 7248, 19769, 3902, 692, 1976, 443, 57139, 99332],
  "Arunachal Pradesh": [55, 39, 3, 25, 54, 27, 0, 54, 224, 283, 19, 36, 18, 2, 983, 1822],
  "Assam": [1111, 281, 60, 533, 1201, 670, 13, 1041, 4025, 8736, 6763, 488, 535, 35, 15320, 40812],
  "Bihar": [5112, 4907, 631, 1120, 2734, 3287, 283, 3508, 7694, 23443, 15067, 1485, 1580, 14, 60142, 131007],
  "Goa": [34, 10, 7, 12, 18, 6, 0, 25, 523, 1072, 257, 61, 47, 11, 1885, 3968],
  "Gujarat": [1622, 923, 11, 346, 1138, 478, 0, 1148, 6902, 23623, 3280, 2960, 3881, 181, 81662, 128155],
  "Haryana": [587, 339, 90, 219, 336, 55, 25, 246, 2640, 4016, 530, 350, 487, 20, 20306, 30246],
  "Himachal Pradesh": [131, 57, 24, 83, 166, 7, 0, 34, 958, 1026, 570, 122, 140, 9, 5537, 8864],
  "Jammu & Kashmir": [689, 573, 18, 119, 348, 53, 0, 77, 1820, 2589, 728, 99, 168, 0, 8224, 15505],
  "Karnataka": [1465, 535, 76, 175, 431, 499, 3, 585, 8847, 16696, 10191, 618, 1485, 2200, 55873, 99679],
  "Kerala": [544, 360, 37, 227, 120, 125, 0, 211, 4140, 3876, 6564, 263, 1120, 133, 54199, 71919],
  "Madhya Pradesh": [3545, 3345, 208, 2733, 1081, 557, 137, 2328, 20525, 37024, 4732, 831, 1662, 47, 122626, 201381],
  "Maharashtra": [3206, 1533, 132, 991, 1243, 974, 98, 3924, 17177, 58510, 5582, 2326, 3129, 321, 97224, 196370],
  "Manipur": [141, 89, 0, 18, 156, 12, 0, 60, 100, 352, 128, 24, 113, 22, 1172, 2387],
  "Meghalaya": [112, 42, 3, 33, 23, 66, 1, 86, 255, 693, 102, 16, 38, 2, 949, 2421],
  "Mizoram": [29, 12, 7, 35, 1, 9, 0, 35, 270, 582, 0, 37, 59, 5, 621, 1702],
  "Nagaland": [70, 26, 6, 10, 25, 37, 0, 130, 298, 328, 21, 58, 39, 10, 547, 1605],
  "Orissa": [760, 866, 114, 326, 397, 335, 0, 914, 4764, 10412, 2569, 425, 376, 33, 28147, 50438],
  "Punjab": [1875, 1800, 112, 66, 257, 38, 24, 159, 1219, 1546, 35, 120, 338, 12, 4779, 12380],
  "Rajasthan": [1473, 1445, 80, 848, 2435, 104, 17, 1228, 7955, 15645, 18424, 1060, 4377, 179, 68156, 123426],
  "Sikkim": [17, 3, 1, 11, 6, 1, 0, 5, 72, 138, 9, 7, 16, 0, 271, 557],
  "Tamil Nadu": [1569, 1413, 23, 256, 859, 167, 0, 502, 7442, 25990, 6587, 650, 1330, 999, 80878, 128665],
  "Tripura": [267, 88, 1, 76, 90, 148, 10, 241, 518, 1058, 344, 14, 22, 3, 2205, 5085],
  "Uttar Pradesh": [10559, 9804, 1728, 1757, 4352, 2210, 496, 7591, 18400, 49956, 10604, 3799, 3894, 246, 90943, 216339],
  "West Bengal": [1770, 606, 779, 615, 1104, 555, 151, 778, 1243, 26913, 7256, 663, 994, 57, 28687, 72171],
  "TOTAL (STATES)": [39523, 30608, 4225, 11407, 19530, 11266, 1262, 26129, 125259, 334276, 104264, 17204, 27824, 4984, 888475, 1646236],
 },
 "U.Ts.": {
  "A & N Islands": [6, 4, 0, 4, 3, 0, 0, 1, 96, 110, 11, 7, 2, 7, 374, 625],
  "Chandigarh": [14, 23, 5, 15, 20, 0, 0, 3, 107, 523, 15, 14, 82, 2, 554, 1377],
  "D & N Haveli": [5, 1, 1, 1, 2, 1, 0, 3, 18, 54, 14, 3, 1, 0, 223, 327],
  "Daman & Diu": [7, 0, 0, 1, 5, 3, 0, 3, 23, 34, 22, 10, 4, 5, 88, 205],
  "Delhi": [521, 535, 389, 276, 948, 35, 35, 294, 1559, 13872, 325, 669, 1459, 96, 15289, 36302],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 9, 18, 2, 1, 0, 0, 16, 46],
  "Pondicherry": [29, 31, 1, 4, 10, 3, 0, 11, 210, 1695, 96, 17, 25, 39, 2052, 4223],
  "TOTAL (UTs)": [582, 594, 396, 301, 988, 42, 35, 315, 2022, 16306, 485, 721, 1573, 149, 18596, 43105],
 },
 "Grand": {"GRAND TOTAL": [40105, 31202, 4621, 11708, 20518, 11308, 1297, 26444, 127281, 350582, 104749, 17925, 29397, 5133, 907071, 1689341]},
}
