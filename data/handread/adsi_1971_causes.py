# ADSI 1971, Appendix V: statement of number of suicides in States / U.Ts. / cities by causes of suicides, by sex
# (pages 1-6, printed sideways: pages 1-2 Failure in examination to Love affairs, pages 3-4 Insanity to Bankruptcy,
# pages 5-6 Death of dear persons to Other causes, Total Male / Female and Grand Total; odd pages the States, even
# pages the U.Ts. and cities). The table prints only Male and Female per cause (no per-cause totals), so CATS are the
# Male and Female columns in printed order and the last is the Grand Total (M & F); the printed Total Male and Total
# Female columns are kept in SEX_TOTALS. Read from the page images; ".." and "—" (nil) are 0. This table prints no
# percentages. Jammu & Kashmir's figures were "taken from the old proformae; figures on the revised proformae are not
# available" (footnote): only 2 male suicides by other causes are printed. Each section's totals row is printed just
# "Total"; it is named TOTAL (STATES) / TOTAL (U.TS.) / TOTAL (CITIES) here. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1971, "adsi"
SOURCE = "raw/adsi/1971/table_content/1680153025appendix-51971.pdf"
PAGES = "1-6"
TITLE = "Appendix V: Statement of Number of Suicides in States/U.Ts./Cities during 1971 (By Causes of Suicides)"
_C = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
      "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
      "Bankruptcy or sudden change in economic position", "Death of dear persons", "Fall in social reputation",
      "Other causes"]
CATS = [f"{c}, {s}" for c in _C for s in ("Male", "Female")] + ["Grand Total"]
CORRECTIONS = {
    ("Andhra Pradesh", "Total, Female"): ("14,51", 1451, "printed '14,51' with the comma misplaced; the female columns add up to 1451 and 2152 + 1451 = the printed Grand Total 3,603 (a reading of the printed digits, not a change)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [40, 14, 171, 199, 88, 102, 73, 24, 26, 14, 19, 19, 34, 8, 741, 599, 24, 8, 16, 4, 0, 2, 8, 2, 912, 456, 3603],
  "Assam": [26, 10, 30, 30, 30, 27, 37, 16, 80, 44, 22, 13, 18, 5, 170, 47, 5, 0, 2, 0, 2, 2, 7, 3, 176, 76, 878],
  "Bihar": [11, 4, 15, 22, 6, 15, 5, 4, 16, 20, 17, 7, 8, 3, 44, 12, 15, 0, 4, 0, 0, 0, 3, 3, 332, 233, 799],
  "Gujarat": [9, 6, 14, 87, 21, 111, 94, 26, 20, 16, 103, 70, 25, 13, 107, 114, 13, 4, 4, 3, 10, 8, 7, 14, 732, 538, 2169],
  "Haryana": [54, 29, 89, 78, 22, 20, 8, 4, 17, 3, 3, 5, 2, 2, 46, 50, 0, 0, 0, 0, 0, 0, 2, 0, 433, 325, 1192],
  "Himachal Pradesh": [1, 0, 4, 5, 1, 4, 0, 2, 6, 2, 2, 0, 8, 0, 5, 6, 0, 0, 0, 0, 2, 0, 2, 0, 5, 3, 58],
  "Jammu & Kashmir": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2],
  "Karnataka": [26, 7, 45, 108, 35, 128, 135, 95, 68, 79, 77, 43, 60, 13, 508, 388, 11, 0, 15, 1, 6, 2, 11, 9, 896, 522, 3288],
  "Kerala": [31, 8, 254, 165, 101, 108, 289, 73, 116, 101, 79, 37, 8, 0, 247, 102, 0, 0, 200, 104, 0, 0, 302, 125, 754, 125, 3329],
  "Madhya Pradesh": [15, 14, 113, 86, 78, 117, 30, 14, 24, 23, 73, 33, 32, 7, 283, 243, 3, 0, 1, 0, 2, 2, 2, 1, 1072, 692, 2960],
  "Maharashtra": [49, 9, 168, 201, 82, 191, 124, 31, 52, 65, 74, 54, 55, 9, 444, 255, 29, 4, 25, 2, 32, 13, 8, 4, 1333, 906, 4219],
  "Manipur": [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 3, 0, 1, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 29, 1, 40],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
  "Orissa": [15, 1, 48, 133, 49, 66, 39, 8, 54, 78, 27, 19, 30, 4, 190, 158, 2, 0, 9, 5, 1, 14, 23, 16, 522, 346, 1857],
  "Punjab": [31, 12, 42, 15, 8, 7, 105, 30, 8, 5, 18, 10, 45, 1, 49, 27, 0, 0, 0, 0, 0, 0, 0, 0, 517, 58, 988],
  "Rajasthan": [9, 3, 21, 50, 8, 31, 14, 8, 2, 4, 6, 1, 0, 2, 49, 51, 2, 1, 3, 0, 0, 2, 4, 3, 30, 18, 322],
  "Tamil Nadu": [48, 17, 333, 192, 61, 82, 140, 55, 165, 107, 52, 25, 139, 60, 771, 437, 91, 31, 40, 14, 13, 3, 64, 28, 1349, 807, 5124],
  "Tripura": [8, 5, 3, 14, 6, 13, 14, 5, 14, 24, 14, 5, 6, 0, 31, 9, 0, 0, 0, 0, 4, 3, 0, 0, 17, 5, 200],
  "Uttar Pradesh": [45, 18, 159, 230, 92, 93, 114, 53, 81, 68, 104, 72, 139, 55, 361, 235, 22, 12, 31, 9, 4, 2, 26, 23, 1576, 553, 4177],
  "West Bengal": [163, 176, 605, 672, 573, 819, 30, 59, 359, 313, 128, 57, 18, 1, 652, 438, 46, 14, 8, 1, 5, 20, 24, 19, 1649, 1110, 7959],
  "TOTAL (STATES)": [581, 333, 2114, 2287, 1261, 1934, 1252, 508, 1108, 966, 821, 471, 629, 183, 4701, 3172, 263, 74, 358, 143, 81, 73, 493, 250, 12336, 6774, 43166],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 2, 1, 0, 5, 3, 2, 0, 2, 1, 1, 0, 0, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 34, 6, 64],
  "Chandigarh": [1, 1, 1, 3, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 14],
  "Dadra & N. Haveli": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 3, 21],
  "Delhi": [2, 3, 4, 7, 6, 11, 4, 0, 4, 1, 1, 0, 1, 0, 16, 9, 0, 0, 0, 0, 0, 0, 0, 0, 28, 12, 109],
  "Goa, Daman & Diu": [2, 1, 2, 2, 2, 2, 3, 0, 4, 5, 8, 2, 0, 0, 3, 3, 2, 0, 2, 0, 0, 0, 2, 0, 20, 16, 81],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  "Pondicherry": [0, 0, 19, 9, 8, 13, 3, 1, 1, 1, 4, 2, 0, 0, 46, 22, 11, 2, 0, 0, 0, 0, 0, 0, 52, 25, 219],
  "TOTAL (U.TS.)": [5, 5, 28, 22, 17, 32, 14, 4, 9, 9, 17, 7, 1, 0, 76, 36, 13, 2, 2, 0, 0, 1, 2, 0, 144, 63, 509],
 },
 "Cities": {
  "Ahmedabad": [3, 2, 0, 4, 2, 21, 6, 4, 3, 2, 5, 3, 0, 0, 9, 8, 0, 0, 0, 0, 0, 1, 1, 3, 61, 46, 184],
  "Bangalore": [2, 1, 4, 10, 0, 0, 10, 7, 1, 1, 0, 0, 0, 0, 59, 65, 2, 0, 1, 0, 0, 1, 0, 0, 135, 91, 390],
  "Bombay": [2, 0, 0, 2, 1, 2, 10, 1, 9, 7, 0, 1, 0, 1, 15, 4, 6, 1, 2, 0, 1, 1, 0, 0, 36, 27, 129],
  "Calcutta": [0, 0, 2, 0, 2, 1, 2, 3, 3, 2, 1, 1, 0, 0, 2, 1, 1, 0, 0, 0, 0, 1, 0, 0, 14, 6, 42],
  "Delhi": [2, 3, 3, 7, 6, 8, 2, 0, 4, 1, 1, 0, 1, 0, 15, 9, 0, 0, 0, 0, 0, 0, 0, 0, 25, 11, 98],
  "Hyderabad": [4, 0, 2, 12, 1, 1, 5, 4, 4, 0, 1, 0, 1, 0, 28, 30, 1, 0, 1, 0, 0, 2, 0, 1, 24, 26, 148],
  "Kanpur": [3, 1, 3, 3, 1, 3, 0, 1, 1, 3, 5, 2, 3, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34],
  "Madras": [1, 1, 10, 14, 5, 3, 0, 0, 2, 2, 1, 1, 7, 4, 32, 17, 1, 0, 2, 0, 4, 0, 0, 0, 48, 38, 193],
  "TOTAL (CITIES)": [17, 8, 24, 52, 18, 39, 35, 20, 27, 18, 14, 8, 12, 5, 164, 135, 11, 1, 6, 0, 5, 6, 1, 4, 343, 245, 1218],
 },
 "Grand": {"GRAND TOTAL": [586, 338, 2142, 2309, 1278, 1966, 1266, 512, 1117, 975, 838, 478, 630, 183, 4777, 3208, 276, 76, 360, 143, 81, 74, 495, 250, 12480, 6837, 43675]},
}
# the printed Total Male and Total Female columns (both add up for every row)
SEX_TOTALS = {
 "Andhra Pradesh": (2152, 1451),
 "Assam": (605, 273),
 "Bihar": (476, 323),
 "Gujarat": (1159, 1010),
 "Haryana": (676, 516),
 "Himachal Pradesh": (36, 22),
 "Jammu & Kashmir": (2, 0),
 "Karnataka": (1893, 1395),
 "Kerala": (2381, 948),
 "Madhya Pradesh": (1728, 1232),
 "Maharashtra": (2475, 1744),
 "Manipur": (37, 3),
 "Nagaland": (1, 1),
 "Orissa": (1009, 848),
 "Punjab": (823, 165),
 "Rajasthan": (148, 174),
 "Tamil Nadu": (3266, 1858),
 "Tripura": (117, 83),
 "Uttar Pradesh": (2754, 1423),
 "West Bengal": (4260, 3699),
 "TOTAL (STATES)": (25998, 17168),
 "A. & N. Islands": (45, 19),
 "Chandigarh": (6, 8),
 "Dadra & N. Haveli": (16, 5),
 "Delhi": (66, 43),
 "Goa, Daman & Diu": (50, 31),
 "Lakshadweep": (1, 0),
 "Pondicherry": (144, 75),
 "TOTAL (U.TS.)": (328, 181),
 "GRAND TOTAL": (26326, 17349),
 "Ahmedabad": (90, 94),
 "Bangalore": (214, 176),
 "Bombay": (82, 47),
 "Calcutta": (27, 15),
 "Delhi": (59, 39),
 "Hyderabad": (72, 76),
 "Kanpur": (20, 14),
 "Madras": (113, 80),
 "TOTAL (CITIES)": (677, 541),
}
