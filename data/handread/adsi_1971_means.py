# ADSI 1971, Appendix VI: suicides by means adopted, by sex, States / UTs / cities
# (raw/adsi/1971/table_content/1680152981appendix-61971.pdf, pages 1-4, printed sideways: pages 1-2 Railway to Fire,
# pages 3-4 Drowning to Other causes, Total Male / Female and Grand Total). The table prints only Male and Female per
# category (no per-category totals), so CATS are the Male and Female columns in printed order and the last is the Grand
# Total (Male & Female); the printed Total Male and Total Female columns are kept in SEX_TOTALS (both add up for every
# row). Read from the page images; '..' (nil) is 0. Jammu & Kashmir's figures were "taken from the old proformae;
# figures on the revised proformae are not available" (footnote): only 2 male suicides by other causes are printed.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1971, "adsi"
SOURCE = "raw/adsi/1971/table_content/1680152981appendix-61971.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Statement of Number of Suicides in States/Union Territories and Cities during 1971 (By means adopted for committing suicide)"
_M = ["By Railway", "By Machine", "By Fire-Arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
      "By Jumping", "By Other causes"]
CATS = [f"{c}, {s}" for c in _M for s in ("Male", "Female")] + ["Grand Total"]
CORRECTIONS = {
    ("TOTAL (STATES)", "By Drowning, Male"): ("37,71", 3771, "printed '37,71' with the comma misplaced; the States add up to 3771 and the Grand Total 3,825 = 3771 + 54 for the UTs (a reading of the printed digits, not a change)"),
    ("GRAND TOTAL", "By Other causes, Female"): (2991, 2981, "printed 2,991 (clear); States 2969 + UTs 12 = 2981, the Grand Total row then adds up to its printed 43,675 and its female columns to the printed Total Female 17,349. Appendix VIII's 20.3% for other causes fits either figure, so the printed totals are the confirmation"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [209, 33, 2, 0, 3, 1, 6, 2, 502, 314, 64, 35, 516, 648, 406, 190, 35, 24, 409, 204, 3603],
  "Assam": [95, 27, 0, 0, 1, 1, 4, 0, 25, 22, 1, 6, 52, 21, 378, 171, 1, 1, 48, 24, 878],
  "Bihar": [58, 25, 0, 0, 34, 0, 0, 0, 54, 39, 23, 49, 96, 80, 126, 72, 8, 4, 77, 54, 799],
  "Gujarat": [60, 19, 2, 2, 2, 1, 0, 0, 224, 139, 109, 278, 265, 283, 116, 62, 34, 20, 347, 206, 2169],
  "Haryana": [18, 4, 26, 0, 2, 0, 1, 2, 3, 1, 46, 55, 99, 121, 151, 137, 23, 13, 307, 183, 1192],
  "Himachal Pradesh": [0, 0, 0, 0, 4, 0, 1, 0, 2, 4, 6, 3, 4, 7, 16, 5, 2, 3, 1, 0, 58],
  "Jammu & Kashmir": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2],
  "Karnataka": [58, 9, 1, 0, 5, 0, 0, 0, 512, 309, 44, 89, 440, 566, 448, 259, 37, 14, 348, 149, 3288],
  "Kerala": [70, 18, 4, 0, 11, 5, 14, 5, 1132, 442, 3, 7, 253, 143, 716, 269, 26, 19, 152, 40, 3329],
  "Madhya Pradesh": [146, 58, 11, 0, 14, 2, 29, 3, 100, 60, 134, 240, 295, 278, 265, 267, 78, 82, 656, 242, 2960],
  "Maharashtra": [126, 11, 6, 2, 1, 2, 14, 4, 811, 417, 136, 213, 500, 648, 368, 131, 58, 26, 455, 290, 4219],
  "Manipur": [0, 0, 0, 0, 8, 0, 0, 0, 7, 0, 0, 0, 8, 0, 1, 2, 0, 0, 13, 1, 40],
  "Nagaland": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2],
  "Orissa": [9, 5, 1, 0, 3, 0, 34, 47, 311, 356, 13, 6, 158, 171, 271, 170, 4, 0, 205, 93, 1857],
  "Punjab": [134, 29, 297, 27, 12, 2, 8, 0, 31, 7, 16, 10, 66, 35, 94, 21, 77, 17, 88, 17, 988],
  "Rajasthan": [27, 13, 0, 0, 4, 3, 3, 0, 11, 6, 5, 20, 63, 107, 25, 14, 0, 2, 10, 9, 322],
  "Tamil Nadu": [119, 32, 5, 3, 2, 1, 13, 10, 1457, 797, 49, 103, 361, 290, 521, 226, 30, 20, 709, 376, 5124],
  "Tripura": [0, 1, 0, 0, 0, 0, 4, 0, 33, 41, 0, 0, 0, 1, 76, 38, 0, 0, 4, 2, 200],
  "Uttar Pradesh": [403, 151, 70, 10, 151, 37, 98, 24, 145, 95, 193, 222, 358, 248, 392, 281, 97, 58, 847, 297, 4177],
  "West Bengal": [239, 90, 12, 9, 53, 6, 18, 5, 1519, 1942, 105, 116, 237, 162, 890, 580, 11, 7, 1176, 782, 7959],
  "TOTAL (STATES)": [1771, 525, 437, 53, 311, 61, 247, 102, 6879, 4991, 947, 1452, 3771, 3810, 5260, 2895, 521, 310, 5854, 2969, 43166],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 0, 0, 1, 0, 1, 0, 7, 13, 1, 1, 6, 0, 11, 3, 0, 0, 18, 2, 64],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 3, 6, 1, 0, 0, 0, 0, 0, 14],
  "Dadra & Nagar Haveli": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 13, 3, 0, 0, 0, 0, 21],
  "Delhi": [28, 7, 0, 0, 0, 0, 0, 0, 9, 4, 7, 15, 6, 5, 11, 9, 1, 3, 4, 0, 109],
  "Goa, Daman & Diu": [2, 0, 0, 0, 1, 2, 1, 0, 8, 11, 1, 2, 18, 11, 16, 3, 2, 0, 1, 2, 81],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
  "Pondicherry": [1, 0, 2, 0, 0, 0, 0, 0, 53, 27, 2, 2, 18, 18, 55, 20, 0, 0, 13, 8, 219],
  "TOTAL (U.TS.)": [31, 7, 2, 0, 2, 2, 3, 0, 78, 57, 11, 20, 54, 42, 108, 38, 3, 3, 36, 12, 509],
 },
 "Cities": {
  "Ahmedabad": [2, 0, 0, 0, 0, 0, 0, 0, 24, 14, 5, 71, 10, 0, 4, 1, 11, 0, 34, 8, 184],
  "Bangalore": [0, 0, 0, 0, 0, 0, 0, 0, 94, 84, 7, 10, 35, 54, 28, 16, 1, 0, 49, 12, 390],
  "Bombay": [0, 0, 0, 0, 0, 0, 3, 1, 24, 17, 12, 19, 8, 3, 16, 5, 13, 1, 6, 1, 129],
  "Calcutta": [0, 0, 0, 0, 0, 0, 0, 0, 8, 4, 1, 5, 3, 1, 14, 5, 1, 0, 0, 0, 42],
  "Delhi": [28, 7, 0, 0, 0, 0, 0, 0, 8, 4, 6, 12, 5, 5, 9, 8, 0, 3, 3, 0, 98],
  "Hyderabad": [0, 0, 0, 0, 2, 0, 0, 0, 42, 30, 4, 15, 13, 22, 4, 0, 1, 2, 6, 7, 148],
  "Kanpur": [5, 4, 3, 0, 0, 0, 1, 0, 6, 4, 0, 3, 4, 3, 1, 0, 0, 0, 0, 0, 34],
  "Madras": [0, 0, 0, 0, 0, 0, 7, 9, 32, 19, 3, 23, 8, 4, 39, 17, 5, 3, 19, 5, 193],
  "TOTAL (CITIES)": [35, 11, 3, 0, 2, 0, 11, 10, 238, 176, 38, 158, 86, 92, 115, 52, 32, 9, 117, 33, 1218],
 },
 "Grand": {"GRAND TOTAL": [1802, 532, 439, 53, 313, 63, 250, 102, 6957, 5048, 958, 1472, 3825, 3852, 5368, 2933, 524, 313, 5890, 2981, 43675]},
}
# printed Total Male, Total Female (columns 23-24), as printed. Two do not match their row: Bihar's Total Female is printed
# 322 and Gujarat's 1013, where the female columns add to 323 and 1010 and the printed Grand Totals (799 = 476 + 323,
# 2169 = 1159 + 1010) and the States' Total Female (17,168) agree with the columns, so those two are misprints.
SEX_TOTALS = {
 "Andhra Pradesh": (2152, 1451), "Assam": (605, 273), "Bihar": (476, 322), "Gujarat": (1159, 1013), "Haryana": (676, 516),
 "Himachal Pradesh": (36, 22), "Jammu & Kashmir": (2, 0), "Karnataka": (1893, 1395), "Kerala": (2381, 948),
 "Madhya Pradesh": (1728, 1232), "Maharashtra": (2475, 1744), "Manipur": (37, 3), "Nagaland": (1, 1), "Orissa": (1009, 848),
 "Punjab": (823, 165), "Rajasthan": (148, 174), "Tamil Nadu": (3266, 1858), "Tripura": (117, 83), "Uttar Pradesh": (2754, 1423),
 "West Bengal": (4260, 3699), "TOTAL (STATES)": (25998, 17168),
 "A. & N. Islands": (45, 19), "Chandigarh": (6, 8), "Dadra & Nagar Haveli": (16, 5), "Delhi": (66, 43), "Goa, Daman & Diu": (50, 31),
 "Lakshadweep": (1, 0), "Pondicherry": (144, 75), "TOTAL (U.TS.)": (328, 181), "GRAND TOTAL": (26326, 17349),
 "Ahmedabad": (90, 94), "Bangalore": (214, 176), "Bombay": (82, 47), "Calcutta": (27, 15), "Delhi (city)": (59, 39),
 "Hyderabad": (72, 76), "Kanpur": (20, 14), "Madras": (113, 80), "TOTAL (CITIES)": (677, 541),
}
