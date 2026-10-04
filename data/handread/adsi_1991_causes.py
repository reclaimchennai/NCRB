# ADSI 1991, Appendix III: distribution of suicides by causes and sex (State, UT & City-wise), pages 1-6 (upright;
# three causes per page, each printed as Male / Female / Total; page 6 Other causes and the Grand Total). Only the
# Total columns are recorded here; while reading, every Male + Female = Total and every row's Male and Female columns
# were checked against the printed Grand Total Male and Female. The All India row is printed "Total (All - India)"
# (kept here as GRAND TOTAL); the cities have no printed totals row. Read from the page images. Some cells on pages 4
# and 5 are faint: Tamil Nadu bankruptcy female "?2" (32 = 139 - 107; the female column then adds up to the printed
# 172), Rajasthan bankruptcy male 18, Kerala / Madhya Pradesh / Maharashtra causes-not-known totals 611, 666, 629
# (= male + female, and the column adds up to the printed 12695).
# Pondicherry, Other causes: printed Male 16, Female 2, Total 28; the female figure should be 12 (the UTs' female
# column adds up to the printed 245 only with 12, and Pondicherry's female columns to its printed 172), so the
# printed Total 28 is right and is recorded as printed.
# Karnataka prints 1344 (807 male, 537 female) under Death of dear person; the States' column adds up to the printed
# 1770 with it and the row to the printed 8313, so it is kept as printed although far out of line with other years.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1991, "adsi"
SOURCE = "raw/adsi/1991/table_content/1680614497appendix-31991.pdf"
PAGES = "1-6"
TITLE = "Appendix III: Distribution of Suicides by Causes and Sex during 1991 (State, UT & City-wise)"
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic status", "Death of dear person", "Fall in social reputation",
        "Dowry dispute", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
CORRECTIONS = {
    ("Calcutta", "Insanity"): (91, 19, "printed Male 10, Female 9, Total 91 (digits transposed); 10 + 9 = 19, and the row then adds up to the printed Grand Total 214"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [84, 233, 198, 290, 142, 161, 73, 1410, 55, 80, 18, 21, 175, 11, 740, 2452, 6143],
  "Arunachal Pradesh": [10, 0, 0, 0, 7, 0, 0, 0, 6, 0, 0, 0, 0, 0, 46, 0, 69],
  "Assam": [64, 77, 32, 40, 105, 23, 36, 69, 15, 13, 10, 21, 8, 3, 1163, 607, 2286],
  "Bihar": [57, 31, 57, 21, 39, 86, 35, 45, 31, 22, 16, 7, 46, 0, 478, 237, 1208],
  "Goa": [2, 1, 7, 1, 14, 11, 0, 19, 3, 1, 2, 1, 2, 0, 64, 115, 243],
  "Gujarat": [52, 151, 274, 62, 115, 223, 34, 417, 153, 37, 61, 64, 32, 3, 362, 1012, 3052],
  "Haryana": [9, 179, 18, 4, 15, 17, 28, 97, 14, 1, 2, 3, 26, 2, 223, 479, 1117],
  "Himachal Pradesh": [2, 17, 8, 0, 10, 8, 2, 25, 4, 1, 0, 0, 3, 0, 31, 48, 159],
  "Jammu & Kashmir": [0, 4, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 10, 0, 11, 20, 49],
  "Karnataka": [84, 165, 232, 249, 148, 194, 94, 97, 88, 34, 1344, 21, 66, 51, 1274, 4172, 8313],
  "Kerala": [49, 777, 414, 10, 175, 323, 213, 973, 171, 306, 31, 19, 15, 13, 611, 4309, 8409],
  "Madhya Pradesh": [150, 682, 561, 56, 273, 301, 143, 803, 30, 13, 41, 68, 91, 16, 666, 1809, 5703],
  "Maharashtra": [136, 543, 846, 208, 245, 300, 168, 1119, 95, 122, 23, 61, 82, 7, 629, 4236, 8820],
  "Manipur": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 29],
  "Meghalaya": [1, 0, 0, 1, 3, 1, 0, 2, 0, 1, 0, 0, 0, 16, 21, 28, 74],
  "Mizoram": [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 21, 10, 34],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 5, 18],
  "Orissa": [84, 381, 197, 46, 317, 60, 25, 287, 25, 7, 9, 22, 82, 29, 983, 551, 3105],
  "Punjab": [3, 20, 11, 9, 3, 46, 4, 9, 0, 1, 2, 3, 14, 0, 278, 186, 589],
  "Rajasthan": [25, 168, 103, 34, 38, 119, 61, 220, 22, 20, 5, 15, 20, 1, 321, 759, 1931],
  "Sikkim": [1, 8, 0, 1, 11, 3, 0, 1, 1, 0, 0, 0, 0, 0, 11, 1, 38],
  "Tamil Nadu": [226, 664, 727, 387, 508, 152, 200, 1878, 268, 139, 92, 8, 123, 9, 1292, 2997, 9670],
  "Tripura": [26, 47, 35, 0, 61, 24, 0, 19, 0, 0, 10, 3, 0, 0, 58, 193, 476],
  "Uttar Pradesh": [30, 101, 123, 53, 126, 118, 169, 287, 57, 38, 34, 12, 295, 16, 512, 871, 2842],
  "West Bengal": [261, 977, 576, 429, 848, 418, 187, 692, 229, 61, 70, 58, 245, 52, 2887, 4364, 12354],
  "TOTAL (STATES)": [1356, 5226, 4419, 1902, 3206, 2589, 1472, 8470, 1267, 897, 1770, 408, 1335, 229, 12695, 29490, 76731],
 },
 "U.Ts.": {
  "A & N Islands": [3, 4, 12, 0, 0, 7, 0, 15, 0, 0, 0, 0, 0, 0, 0, 85, 126],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 2, 0, 22, 13, 54],
  "D & N Haveli": [0, 2, 2, 0, 0, 1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 12, 20],
  "Daman & Diu": [0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 5, 11, 20],
  "Delhi": [18, 14, 17, 27, 25, 37, 2, 52, 25, 4, 6, 9, 23, 0, 343, 386, 988],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [3, 145, 68, 18, 10, 32, 0, 148, 6, 6, 6, 2, 0, 0, 39, 28, 511],
  "TOTAL (U.TS.)": [24, 165, 99, 45, 36, 80, 2, 232, 32, 10, 14, 11, 25, 0, 409, 535, 1719],
 },
 "Cities": {
  "Ahmedabad": [8, 7, 21, 2, 6, 19, 3, 42, 9, 6, 12, 2, 6, 0, 96, 65, 304],
  "Bangalore": [9, 3, 7, 13, 5, 29, 0, 63, 3, 3, 0, 1, 15, 0, 93, 852, 1096],
  "Bombay": [18, 45, 83, 30, 27, 15, 1, 84, 29, 5, 5, 8, 31, 1, 283, 357, 1022],
  "Calcutta": [11, 7, 1, 25, 25, 19, 7, 11, 8, 4, 19, 10, 7, 12, 25, 23, 214],
  "Delhi": [16, 4, 13, 21, 21, 35, 2, 42, 21, 4, 5, 8, 19, 0, 269, 335, 815],
  "Hyderabad": [6, 17, 5, 3, 10, 1, 3, 27, 5, 3, 1, 5, 26, 0, 181, 87, 380],
  "Jaipur": [6, 1, 3, 1, 5, 0, 1, 7, 0, 0, 0, 0, 1, 0, 71, 67, 163],
  "Kanpur": [0, 14, 5, 0, 7, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 96, 128],
  "Lucknow": [2, 1, 1, 2, 1, 5, 0, 23, 1, 0, 2, 0, 4, 0, 30, 47, 119],
  "Madras": [13, 33, 57, 43, 39, 3, 10, 111, 26, 2, 4, 3, 3, 0, 61, 374, 782],
  "Nagpur": [0, 0, 0, 0, 2, 2, 1, 13, 1, 0, 0, 5, 1, 0, 8, 249, 282],
  "Pune": [9, 2, 2, 4, 8, 2, 2, 15, 6, 12, 2, 0, 5, 0, 0, 214, 283],
 },
 "Grand": {"GRAND TOTAL": [1380, 5391, 4518, 1947, 3242, 2669, 1474, 8702, 1299, 907, 1784, 419, 1360, 229, 13104, 30025, 78450]},
}
