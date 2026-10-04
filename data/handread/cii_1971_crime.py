# CII 1971, Table 5: Incidence of crime under different heads during 1970 & 1971 showing percentage variation,
# States / UTs / cities (raw/cii/1971/table_content/table-5-1971.pdf, pages 1-4). Read from the page images; only the
# 1971 columns are kept (the 1970 and percentage-variation columns are skipped). The table prints selected heads and
# the total cognizable crime, with no 'other IPC crimes' column, so the heads do not add up to the total and each
# column is checked against the printed State, UT, Grand and City totals (CHECK = "columns").
KIND, YEAR, PUB = "crime", 1971, "cii"
SOURCE = "raw/cii/1971/table_content/table-5-1971.pdf"
PAGES = "1-4"
TITLE = "Table 5: Incidence of crime under different heads during 1970 & 1971 showing percentage variation"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Thefts", "Riots",
        "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
    ("TOTAL (CITIES)", "Kidnapping & abduction"): (977, 917, "NCRB's CII 1972 errata corrects the 1971 Cities total to 917; Kanpur stays as printed (117), as CII 1972 Table 6 also prints it (the printed +14.9% on 154 would give 177)"),
}
# Andhra Pradesh Murder 1971: the figure is partly blotted on the scan and reads 1,020; it agrees with the printed
# -6.6% and the Murder column then adds up to the printed State total 16,018.
ROWS = {
 "States": {
  "Andhra Pradesh": [1020, 160, 147, 205, 5377, 12062, 2953, 602, 406, 19, 46390],
  "Assam": [494, 424, 189, 239, 5040, 7964, 3154, 417, 299, 13, 28199],
  "Bihar": [1423, 559, 2015, 1387, 19419, 26000, 10054, 1095, 476, 94, 83270],
  "Gujarat": [702, 254, 56, 404, 3843, 10412, 548, 958, 458, 8, 32747],
  "Haryana": [194, 109, 2, 21, 1472, 2448, 72, 206, 137, 1, 8237],
  "Himachal Pradesh": [43, 76, 1, 25, 386, 418, 67, 92, 55, 0, 2494],
  "Jammu & Kashmir": [70, 187, 5, 10, 789, 999, 563, 64, 78, 0, 5518],
  "Kerala": [431, 60, 40, 134, 3334, 4184, 3840, 339, 173, 82, 29712],
  "Madhya Pradesh": [1727, 928, 443, 1066, 16986, 30776, 2390, 973, 1028, 16, 88548],
  "Maharashtra": [1311, 526, 358, 1718, 15102, 44500, 1729, 3036, 1710, 55, 99125],
  "Manipur": [25, 149, 15, 43, 163, 430, 152, 73, 74, 1, 1931],
  "Mysore": [759, 115, 78, 152, 6472, 11235, 1797, 738, 599, 75, 36557],
  "Nagaland": [24, 11, 14, 42, 127, 495, 28, 54, 44, 0, 1004],
  "Orissa": [383, 80, 142, 286, 6462, 12495, 1650, 487, 294, 13, 30502],
  "Punjab": [604, 289, 6, 29, 1387, 2472, 31, 367, 234, 6, 11433],
  "Rajasthan": [555, 1164, 100, 956, 6319, 8924, 4045, 720, 715, 9, 36743],
  "Tamil Nadu": [785, 211, 22, 124, 6996, 18959, 4023, 1078, 527, 152, 59616],
  "Tripura": [45, 12, 43, 30, 307, 995, 286, 28, 29, 0, 1785],
  "Uttar Pradesh": [3572, 3063, 6004, 10049, 52773, 93407, 14561, 7071, 2637, 41, 236328],
  "West Bengal": [1851, 792, 1496, 1131, 9521, 27498, 11799, 1129, 763, 21, 78546],
  "TOTAL (STATES)": [16018, 9169, 11176, 18051, 162275, 316673, 63742, 19527, 10736, 606, 918685],
 },
 "U.Ts.": {
  "A. & N. Islands": [12, 1, 0, 2, 50, 99, 16, 7, 1, 0, 370],
  "Chandigarh": [7, 11, 0, 1, 116, 748, 5, 51, 36, 0, 1251],
  "Dadra & Nagar Haveli": [3, 0, 0, 0, 33, 27, 1, 3, 0, 0, 84],
  "Delhi": [113, 453, 14, 329, 2833, 16735, 240, 587, 595, 30, 29236],
  "Goa, Daman & Diu": [18, 6, 2, 17, 349, 379, 16, 42, 28, 1, 1219],
  "Laccadives": [0, 0, 0, 0, 6, 5, 0, 0, 2, 0, 19],
  "Pondicherry": [9, 7, 1, 2, 145, 538, 94, 53, 14, 4, 1717],
  "TOTAL (U.TS.)": [162, 478, 17, 351, 3532, 18531, 372, 743, 676, 35, 33896],
 },
 "Grand": {
  "GRAND TOTAL": [16180, 9647, 11193, 18402, 165807, 335204, 64114, 20270, 11412, 641, 952581],
 },
 "Cities": {
  "Ahmedabad": [31, 39, 5, 11, 284, 1145, 51, 72, 112, 3, 3060],
  "Bangalore": [22, 12, 0, 20, 1714, 4307, 59, 196, 292, 47, 8961],
  "Bombay": [131, 180, 30, 203, 1866, 12758, 290, 1003, 729, 39, 25066],
  "Calcutta": [285, 118, 40, 112, 761, 4225, 1143, 354, 225, 5, 10911],
  "Delhi": [94, 407, 9, 293, 2346, 16051, 203, 553, 544, 28, 26933],
  "Hyderabad": [16, 26, 3, 28, 743, 2041, 54, 95, 140, 0, 3794],
  "Kanpur": [54, 117, 28, 200, 1771, 4479, 235, 782, 294, 5, 9659],
  "Madras": [20, 18, 0, 17, 125, 3700, 210, 400, 235, 38, 7205],
  "TOTAL (CITIES)": [653, 917, 115, 884, 9610, 48706, 2245, 3455, 2571, 165, 95589],
 },
}
