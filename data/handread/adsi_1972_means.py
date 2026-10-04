# ADSI 1972, Appendix VI: suicides by means adopted, by sex, States / UTs / cities
# (raw/adsi/1972/table_content/1680154568appendix-61972.pdf, pages 1-6, printed sideways: pages 1-2 Railway to Weapons,
# pages 3-4 Poison, Fire, Drowning, pages 5-6 Hanging, Jumping, Other causes, Total Male / Female and Grand Total). As in
# 1971 the table prints only Male and Female per category, so CATS are the Male and Female columns in printed order and
# the last is the Grand Total (Male & Female); the printed Total Male and Total Female columns are kept in SEX_TOTALS
# (keyed by section and place) and add up for every row. Read from the page images; '..' (nil) and '—' are 0.
# "Data from Arunachal Pradesh had not been available" (footnote). Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1972, "adsi"
SOURCE = "raw/adsi/1972/table_content/1680154568appendix-61972.pdf"
PAGES = "1-6"
TITLE = "Appendix VI: Statement of Number of Suicides in States/U.Ts./Cities during the Year 1972 (By means adopted for committing suicides)"
_M = ["By Railway", "By Machine", "By Fire-arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
      "By Jumping", "By Other causes"]
CATS = [f"{c}, {s}" for c in _M for s in ("Male", "Female")] + ["Grand Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [214, 33, 4, 1, 0, 0, 5, 0, 587, 334, 46, 71, 462, 662, 351, 109, 70, 10, 197, 130, 3286],
  "Assam": [84, 36, 1, 0, 4, 0, 3, 0, 44, 26, 13, 19, 98, 49, 498, 203, 8, 4, 95, 30, 1215],
  "Bihar": [152, 58, 4, 0, 3, 1, 0, 0, 43, 25, 34, 46, 89, 96, 83, 62, 14, 4, 122, 84, 920],
  "Gujarat": [85, 14, 16, 2, 3, 0, 10, 3, 202, 137, 83, 185, 148, 142, 69, 38, 23, 20, 87, 57, 1324],
  "Haryana": [40, 17, 16, 0, 14, 1, 16, 9, 6, 1, 10, 12, 52, 62, 47, 23, 8, 6, 75, 30, 445],
  "Himachal Pradesh": [0, 0, 0, 0, 3, 0, 1, 0, 3, 5, 2, 0, 5, 10, 7, 5, 1, 0, 3, 4, 49],
  "Jammu & Kashmir": [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 19, 3, 1, 0, 2, 3, 3, 0, 33],
  "Karnataka": [61, 10, 2, 0, 25, 4, 35, 15, 686, 272, 43, 39, 663, 585, 466, 162, 3, 10, 358, 100, 3539],
  "Kerala": [104, 29, 0, 0, 7, 1, 21, 1, 1357, 681, 3, 3, 287, 272, 794, 257, 21, 2, 513, 147, 4500],
  "Madhya Pradesh": [248, 73, 8, 1, 26, 2, 9, 1, 129, 94, 173, 275, 274, 264, 469, 213, 92, 86, 671, 254, 3362],
  "Maharashtra": [146, 27, 8, 2, 3, 0, 13, 1, 791, 393, 135, 226, 535, 597, 402, 69, 67, 63, 538, 262, 4278],
  "Manipur": [0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 1, 0, 0, 0, 4, 2, 0, 0, 5, 1, 20],
  "Meghalaya": [0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 5, 2, 20, 8, 16, 1, 0, 0, 65, 5, 127],
  "Nagaland": [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 8],
  "Orissa": [325, 38, 0, 0, 5, 0, 24, 11, 398, 448, 7, 4, 159, 143, 241, 142, 8, 0, 347, 161, 2461],
  "Punjab": [358, 41, 3, 0, 12, 0, 2, 0, 13, 7, 15, 11, 28, 29, 40, 16, 4, 1, 52, 17, 649],
  "Rajasthan": [23, 13, 3, 1, 12, 4, 2, 0, 9, 6, 14, 39, 139, 136, 38, 9, 3, 0, 45, 17, 513],
  "Tamil Nadu": [77, 20, 13, 1, 3, 2, 4, 4, 1445, 693, 38, 132, 492, 343, 358, 163, 31, 1, 728, 221, 4769],
  "Tripura": [0, 0, 0, 0, 2, 1, 0, 1, 37, 59, 6, 10, 21, 9, 61, 44, 0, 0, 3, 4, 258],
  "Uttar Pradesh": [381, 158, 45, 10, 125, 27, 63, 12, 125, 108, 378, 327, 176, 363, 391, 321, 69, 46, 707, 217, 4049],
  "West Bengal": [214, 59, 23, 10, 17, 6, 15, 11, 1638, 1937, 57, 129, 184, 186, 891, 713, 28, 49, 692, 412, 7271],
  "TOTAL (STATES)": [2513, 626, 149, 28, 269, 49, 223, 69, 7518, 5229, 1063, 1530, 3851, 3959, 5232, 2552, 452, 305, 5306, 2153, 43076],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 3, 0, 0, 0, 0, 0, 11, 6, 0, 0, 8, 1, 8, 3, 0, 0, 18, 4, 62],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1, 2, 6, 5, 3, 0, 1, 0, 0, 0, 23],
  "D. & N. Haveli": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 7, 8, 3, 0, 0, 13, 3, 38],
  "Delhi": [32, 6, 0, 0, 0, 0, 0, 0, 6, 5, 12, 27, 12, 10, 13, 4, 10, 3, 5, 4, 149],
  "Goa, Daman & Diu": [2, 0, 0, 0, 0, 0, 1, 0, 7, 4, 0, 4, 12, 4, 11, 3, 0, 0, 8, 1, 57],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 7, 1, 0, 0, 0, 0, 9],
  "Pondicherry": [1, 0, 0, 0, 0, 0, 0, 0, 47, 26, 4, 1, 18, 12, 36, 18, 0, 0, 14, 10, 187],
  "TOTAL (U.TS.)": [35, 6, 3, 0, 0, 0, 4, 0, 74, 42, 17, 34, 59, 39, 86, 32, 11, 3, 58, 22, 525],
 },
 "Cities": {
  "Ahmedabad": [3, 4, 0, 0, 2, 0, 0, 0, 12, 15, 12, 28, 5, 6, 8, 7, 9, 6, 24, 19, 160],
  "Bangalore": [0, 0, 1, 0, 0, 0, 0, 0, 151, 25, 19, 2, 43, 32, 28, 13, 0, 0, 48, 4, 366],
  "Bombay": [2, 0, 0, 0, 1, 0, 4, 0, 38, 23, 16, 30, 9, 8, 21, 4, 11, 2, 5, 1, 175],
  "Calcutta": [0, 0, 0, 0, 1, 0, 1, 0, 3, 3, 1, 2, 0, 1, 9, 7, 4, 1, 0, 0, 33],
  "Delhi": [32, 6, 0, 0, 0, 0, 0, 0, 5, 4, 11, 20, 10, 8, 10, 4, 9, 3, 5, 4, 131],
  "Hyderabad": [0, 0, 0, 0, 2, 0, 2, 0, 43, 25, 5, 13, 18, 15, 6, 3, 2, 2, 14, 4, 154],
  "Kanpur": [1, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 9, 3, 1, 7, 1, 0, 0, 18, 8, 52],
  "Madras": [0, 0, 0, 0, 0, 0, 0, 0, 53, 40, 9, 10, 14, 16, 31, 23, 1, 0, 22, 2, 221],
  "TOTAL (CITIES)": [38, 11, 3, 0, 6, 0, 7, 0, 306, 135, 73, 114, 102, 87, 120, 62, 36, 14, 136, 42, 1292],
 },
 "Grand": {"GRAND TOTAL": [2548, 632, 152, 28, 269, 49, 227, 69, 7592, 5271, 1080, 1564, 3910, 3998, 5318, 2584, 463, 308, 5364, 2175, 43601]},
}
# printed Total Male, Total Female (columns 23-24), as printed
SEX_TOTALS = {
 ("States", "Andhra Pradesh"): (1936, 1350),
 ("States", "Assam"): (848, 367),
 ("States", "Bihar"): (544, 376),
 ("States", "Gujarat"): (726, 598),
 ("States", "Haryana"): (284, 161),
 ("States", "Himachal Pradesh"): (25, 24),
 ("States", "Jammu & Kashmir"): (27, 6),
 ("States", "Karnataka"): (2342, 1197),
 ("States", "Kerala"): (3107, 1393),
 ("States", "Madhya Pradesh"): (2099, 1263),
 ("States", "Maharashtra"): (2638, 1640),
 ("States", "Manipur"): (14, 6),
 ("States", "Meghalaya"): (111, 16),
 ("States", "Nagaland"): (8, 0),
 ("States", "Orissa"): (1514, 947),
 ("States", "Punjab"): (527, 122),
 ("States", "Rajasthan"): (288, 225),
 ("States", "Tamil Nadu"): (3189, 1580),
 ("States", "Tripura"): (130, 128),
 ("States", "Uttar Pradesh"): (2460, 1589),
 ("States", "West Bengal"): (3759, 3512),
 ("States", "TOTAL (STATES)"): (26576, 16500),
 ("U.Ts.", "A. & N. Islands"): (48, 14),
 ("U.Ts.", "Chandigarh"): (16, 7),
 ("U.Ts.", "D. & N. Haveli"): (24, 14),
 ("U.Ts.", "Delhi"): (90, 59),
 ("U.Ts.", "Goa, Daman & Diu"): (41, 16),
 ("U.Ts.", "Lakshadweep"): (0, 0),
 ("U.Ts.", "Mizoram"): (8, 1),
 ("U.Ts.", "Pondicherry"): (120, 67),
 ("U.Ts.", "TOTAL (U.TS.)"): (347, 178),
 ("Grand", "GRAND TOTAL"): (26923, 16678),
 ("Cities", "Ahmedabad"): (75, 85),
 ("Cities", "Bangalore"): (290, 76),
 ("Cities", "Bombay"): (107, 68),
 ("Cities", "Calcutta"): (19, 14),
 ("Cities", "Delhi"): (82, 49),
 ("Cities", "Hyderabad"): (92, 62),
 ("Cities", "Kanpur"): (32, 20),
 ("Cities", "Madras"): (130, 91),
 ("Cities", "TOTAL (CITIES)"): (827, 465),
}
