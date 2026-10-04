# ADSI 1991, Appendix IV: suicides by means adopted and sex, States / UTs / cities
# (raw/adsi/1991/table_content/1680614463appendix-41991.pdf, pages 1-5: each page carries three categories by Male /
# Female / Total for every place, page 5 the Grand Total). Only the Total column of each category is recorded. The
# cities carry no totals row. Read from the page images. Some cells of the Jumping Total column (column 29) on page 3
# are washed out in the scan (Madhya Pradesh, Maharashtra, Manipur to Nagaland, Orissa, Punjab); they are read as the
# printed Male + Female beside them (38 + 42, 72 + 67, 0 + 0, 4 + 2, 0 + 0, 0 + 0, 18 + 13, 0 + 0), which the faint
# traces fit and Appendix VII's percentages confirm (80/5703 = 1.4%, 139/8820 = 1.6%, 6/74 = 8.1%, 31/3105 = 1.0%).
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1991, "adsi"
SOURCE = "raw/adsi/1991/table_content/1680614463appendix-41991.pdf"
PAGES = "1-5"
TITLE = "Appendix IV: Distribution of Suicides by Means Adopted and Sex during 1991 (State, UT & City-wise)"
CATS = ["By Railways", "By Machine", "By Firearms", "By Weapon", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wire", "By Other Means", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [308, 2, 10, 6, 2050, 618, 1086, 1014, 35, 7, 48, 959, 6143],
  "Arunachal Pradesh": [0, 0, 0, 0, 11, 0, 4, 54, 0, 0, 0, 0, 69],
  "Assam": [87, 2, 12, 4, 211, 104, 248, 939, 48, 8, 30, 593, 2286],
  "Bihar": [29, 6, 10, 20, 207, 134, 187, 326, 22, 18, 46, 203, 1208],
  "Goa": [0, 0, 0, 1, 28, 33, 46, 81, 6, 4, 3, 41, 243],
  "Gujarat": [149, 3, 27, 2, 1065, 665, 389, 481, 45, 10, 9, 207, 3052],
  "Haryana": [9, 179, 18, 4, 15, 17, 28, 97, 14, 1, 2, 733, 1117],
  "Himachal Pradesh": [3, 0, 0, 5, 85, 8, 9, 30, 11, 5, 1, 2, 159],
  "Jammu & Kashmir": [6, 0, 1, 0, 9, 15, 2, 5, 0, 0, 1, 10, 49],
  "Karnataka": [142, 6, 10, 4, 3055, 554, 1752, 1430, 10, 28, 36, 1286, 8313],
  "Kerala": [361, 1, 5, 15, 3264, 234, 815, 3398, 6, 5, 15, 290, 8409],
  "Madhya Pradesh": [80, 17, 69, 87, 1518, 800, 602, 1547, 80, 75, 61, 767, 5703],
  "Maharashtra": [235, 8, 8, 8, 2648, 1549, 1592, 1443, 139, 7, 28, 1155, 8820],
  "Manipur": [0, 0, 2, 0, 4, 2, 0, 15, 0, 0, 1, 5, 29],
  "Meghalaya": [0, 0, 0, 2, 3, 2, 19, 28, 6, 0, 0, 14, 74],
  "Mizoram": [0, 0, 0, 1, 2, 0, 2, 27, 0, 0, 0, 2, 34],
  "Nagaland": [1, 0, 1, 0, 0, 1, 2, 5, 0, 3, 0, 5, 18],
  "Orissa": [202, 0, 2, 5, 1229, 52, 125, 1093, 31, 12, 40, 314, 3105],
  "Punjab": [200, 0, 16, 1, 59, 61, 29, 37, 0, 3, 9, 174, 589],
  "Rajasthan": [170, 12, 8, 5, 345, 254, 405, 357, 67, 10, 7, 291, 1931],
  "Sikkim": [0, 0, 1, 0, 2, 0, 0, 35, 0, 0, 0, 0, 38],
  "Tamil Nadu": [174, 6, 10, 7, 3892, 1134, 1019, 1431, 58, 49, 54, 1836, 9670],
  "Tripura": [0, 0, 3, 0, 157, 19, 0, 215, 0, 0, 0, 82, 476],
  "Uttar Pradesh": [335, 35, 245, 83, 424, 337, 162, 320, 14, 4, 0, 883, 2842],
  "West Bengal": [261, 39, 102, 92, 4827, 790, 756, 2770, 47, 73, 38, 2559, 12354],
  "TOTAL (STATES)": [2752, 316, 560, 352, 25110, 7383, 9279, 17178, 639, 322, 429, 12411, 76731],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 28, 4, 2, 92, 0, 0, 0, 0, 126],
  "Chandigarh": [0, 0, 2, 0, 16, 10, 4, 9, 1, 0, 0, 12, 54],
  "D & N Haveli": [0, 0, 0, 0, 1, 0, 2, 17, 0, 0, 0, 0, 20],
  "Daman & Diu": [0, 0, 1, 0, 5, 3, 2, 1, 0, 1, 0, 7, 20],
  "Delhi": [1, 0, 8, 7, 188, 286, 22, 271, 18, 0, 7, 180, 988],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [1, 0, 0, 0, 209, 36, 11, 251, 1, 2, 0, 0, 511],
  "TOTAL (U.TS.)": [2, 0, 11, 7, 447, 339, 43, 641, 20, 3, 7, 199, 1719],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 2, 0, 37, 109, 64, 71, 10, 1, 0, 10, 304],
  "Bangalore": [0, 3, 1, 1, 288, 225, 85, 285, 1, 4, 13, 190, 1096],
  "Bombay": [0, 2, 6, 5, 191, 361, 52, 223, 42, 7, 10, 123, 1022],
  "Calcutta": [0, 0, 0, 0, 34, 28, 19, 31, 12, 39, 8, 43, 214],
  "Delhi": [1, 0, 6, 6, 147, 233, 16, 224, 18, 0, 5, 159, 815],
  "Hyderabad": [0, 0, 3, 0, 46, 124, 41, 53, 2, 5, 6, 100, 380],
  "Jaipur": [4, 0, 0, 0, 30, 25, 1, 26, 2, 4, 1, 70, 163],
  "Kanpur": [4, 0, 1, 1, 17, 0, 6, 27, 0, 0, 0, 72, 128],
  "Lucknow": [6, 0, 3, 8, 33, 13, 8, 23, 3, 1, 0, 21, 119],
  "Madras": [0, 0, 0, 0, 208, 161, 89, 198, 17, 5, 6, 98, 782],
  "Nagpur": [2, 1, 0, 0, 14, 61, 44, 26, 7, 0, 1, 126, 282],
  "Pune": [0, 0, 1, 2, 90, 68, 32, 84, 2, 0, 0, 4, 283],
 },
 "Grand": {
  "GRAND TOTAL": [2754, 316, 571, 359, 25557, 7722, 9322, 17819, 659, 325, 436, 12610, 78450],
 },
}
