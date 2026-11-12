# CII 1996, incidence of cognizable IPC crime by crime head, States / UTs, from the State and UT rows of Table 8
# (district-wise incidence, raw/cii/1996/table_content/table-8--distric-wise-incidence-of-cognizable-crimes-(ipc)-during-1996-1996.pdf,
# pages 1-24, printed pages 180-203; odd pages carry columns (3)-(14), even pages columns (15)-(26)). The edition's
# State / UT table by crime head (Table 6) is not among the PDFs held (raw/cii/1996/table_content has no table 6 or 7),
# so each State's figures are the 'TOTAL' row printed at the foot of its districts in Table 8, and Chandigarh, D&N
# Haveli, Lakshadweep and Pondicherry their single district row; names are the State / UT headings as printed. Read
# from the page images. Kidnapping & abduction is the printed total; its two printed sub-columns (of women & girls, of
# others) add up to it and are left out so the heads add up to the Total. Table 8 prints no TOTAL (STATES) / TOTAL (UTs)
# rows, only 'ALL-INDIA', kept below as ALL_INDIA (not in ROWS, so that scripts/check_handread.py, which wants the two
# section totals beside a Grand Total, checks the rows). 'NR' (data not received) for arson .. cruelty by husband or
# relatives in Daman & Diu is None; that row still adds up to its printed total. Every row adds up to its printed
# Total (scripts/check_handread.py). Checked besides when built: on every one of the 21 heads and the total the 25
# States and 7 UTs add up to the printed ALL-INDIA row, which is also the 'All-India' column of Table 2.4 of the
# urban-crime chapter; every State / UT total is the one printed in Table 5 (incidence & rate of total cognizable
# crimes, raw/cii/1996/table_content/table-5--...-1996.pdf), whose TOTAL (STATES) 16,44,100 and TOTAL (UTs) 65,476 the
# total column adds up to. The scan is faded at the right edge of page 14: the totals of Maharashtra (18747_), Manipur
# (257_) and Meghalaya (186_) are completed from Table 5 (1,87,471; 2,573; 1,863), with which each row adds up.
KIND, YEAR, PUB = "crime", 1996, "cii"
SOURCE = "raw/cii/1996/table_content/table-8--distric-wise-incidence-of-cognizable-crimes-(ipc)-during-1996-1996.pdf"
PAGES = "1-24"
TITLE = "Table 8: District-wise incidence of cognizable crimes (IPC) during 1996 (State and UT totals)"
CATS = ["Murder", "Attempt to commit murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Preparation & assembly for dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Arson", "Hurt/grievous hurt", "Dowry death", "Molestation", "Sexual harassment", "Cruelty by husband or relatives", "Other IPC crimes", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Madhya Pradesh", "Molestation"): (6833, 6838, "Table 8 prints 6833; the row adds up to its printed total 1,96,779 (also in Table 5) and the States and UTs to the printed ALL-INDIA 28,939 only with 6838, and Table 59 (crimes against women, page 2) prints Madhya Pradesh molestation as 6838"),
    ("Haryana", "Cheating"): (None, 844, "figure lost in a white patch of the scan (8_4 at most); 844 makes the row add up to its printed total 33,516 (also in Table 5) and the States and UTs to the printed ALL-INDIA 33,823"),
    ("Meghalaya", "Other IPC crimes"): (None, 522, "faded in the scan (52_); 522 makes the row add up to 1,863, the total Table 5 prints for Meghalaya, and the States and UTs to the printed ALL-INDIA 7,14,587"),
}
# the 'ALL-INDIA' row as printed at the foot of Table 8 (pages 23-24)
ALL_INDIA = [37671, 29597, 3728, 14846, 20848, 8035, 888, 22705, 115097, 284985, 92831, 15368, 33823, 2796, 12425, 223977, 5513, 28939, 5671, 35246, 714587, 1709576]
ROWS = {
 "States": {
  "Andhra Pradesh": [2609, 1318, 122, 812, 1028, 448, 3, 775, 6177, 14413, 4058, 585, 2671, 113, 1000, 24119, 411, 2559, 994, 3478, 42066, 109759],
  "Arunachal Pradesh": [76, 33, 4, 37, 52, 25, 1, 68, 186, 368, 17, 31, 25, 6, 12, 286, 0, 29, 1, 4, 666, 1927],
  "Assam": [1435, 409, 33, 580, 1190, 843, 24, 1063, 3516, 7521, 3534, 444, 541, 52, 730, 4341, 28, 569, 8, 553, 9076, 36490],
  "Bihar": [5264, 4637, 590, 1453, 2378, 2450, 228, 2955, 6563, 16782, 12449, 1693, 1846, 32, 441, 4805, 478, 533, 107, 675, 50658, 117017],
  "Goa": [30, 11, 9, 10, 13, 4, 0, 71, 532, 737, 184, 31, 54, 5, 19, 222, 1, 17, 7, 13, 828, 2798],
  "Gujarat": [1338, 621, 11, 306, 1055, 371, 3, 1130, 5717, 17608, 2289, 2028, 3197, 138, 541, 15831, 105, 1077, 81, 2666, 61708, 117821],
  "Haryana": [606, 374, 83, 336, 452, 55, 27, 255, 3287, 4997, 739, 356, 844, 28, 221, 6103, 223, 529, 434, 490, 13077, 33516],
  "Himachal Pradesh": [123, 80, 7, 132, 157, 3, 0, 24, 987, 771, 539, 97, 149, 16, 128, 1481, 6, 295, 16, 227, 5538, 10776],
  "Jammu & Kashmir": [1044, 797, 15, 157, 523, 65, 0, 283, 1931, 2357, 710, 71, 150, 3, 709, 385, 0, 376, 166, 33, 7703, 17478],
  "Karnataka": [1604, 1220, 55, 222, 532, 250, 6, 994, 9210, 16832, 8113, 612, 1984, 1208, 696, 24926, 182, 1310, 166, 1382, 42971, 114475],
  "Kerala": [417, 444, 94, 389, 230, 98, 13, 296, 5066, 3727, 6028, 330, 2101, 58, 370, 15653, 25, 1166, 40, 1079, 48517, 86141],
  "Madhya Pradesh": [3302, 3252, 196, 3265, 1084, 198, 112, 1826, 17853, 27160, 3877, 773, 1632, 101, 1267, 28432, 577, 6838, 705, 2493, 91836, 196779],
  "Maharashtra": [2777, 1238, 119, 1444, 1069, 668, 92, 2865, 16713, 47769, 5643, 1789, 3411, 161, 1474, 31357, 443, 3227, 870, 9156, 55186, 187471],
  "Manipur": [194, 136, 4, 14, 79, 18, 0, 36, 97, 269, 73, 12, 38, 4, 120, 255, 0, 19, 0, 2, 1203, 2573],
  "Meghalaya": [139, 19, 4, 33, 24, 94, 0, 105, 190, 432, 44, 18, 33, 2, 25, 153, 1, 24, 1, 0, 522, 1863],
  "Mizoram": [43, 18, 8, 49, 7, 6, 0, 22, 347, 967, 0, 51, 72, 10, 32, 114, 0, 54, 0, 0, 441, 2241],
  "Nagaland": [203, 48, 8, 9, 49, 28, 0, 96, 180, 211, 11, 23, 45, 1, 6, 43, 0, 4, 1, 2, 410, 1378],
  "Orissa": [1008, 1253, 107, 617, 489, 305, 9, 990, 4419, 7638, 1892, 391, 500, 138, 530, 5107, 178, 1690, 175, 861, 22322, 50619],
  "Punjab": [706, 329, 94, 178, 274, 28, 11, 54, 1167, 1664, 6, 208, 805, 32, 57, 2613, 180, 129, 1, 225, 5161, 13922],
  "Rajasthan": [1622, 2248, 87, 1162, 2857, 97, 2, 1183, 8806, 17222, 21413, 953, 5853, 270, 1173, 14203, 349, 2583, 44, 3920, 75574, 161621],
  "Sikkim": [5, 5, 2, 9, 11, 1, 0, 9, 70, 134, 42, 9, 51, 1, 0, 125, 0, 47, 0, 0, 189, 710],
  "Tamil Nadu": [1883, 1668, 16, 327, 976, 171, 1, 600, 6362, 18666, 7195, 474, 1338, 236, 1355, 20689, 112, 1253, 1514, 353, 66308, 131497],
  "Tripura": [228, 34, 1, 90, 183, 115, 4, 120, 301, 488, 266, 27, 30, 5, 106, 566, 19, 94, 1, 66, 886, 3630],
  "Uttar Pradesh": [8500, 8261, 1332, 1854, 3931, 1146, 113, 5395, 11819, 33522, 6980, 3204, 3433, 61, 1157, 14212, 1983, 2526, 118, 3989, 58944, 172480],
  "West Bengal": [1927, 580, 631, 855, 906, 510, 218, 869, 752, 20695, 6285, 447, 1081, 46, 139, 5012, 77, 1254, 22, 3437, 23375, 69118],
 },
 "U.Ts.": {
  "A&N Islands": [11, 8, 1, 7, 2, 0, 0, 0, 42, 38, 8, 3, 6, 0, 4, 69, 0, 9, 2, 5, 161, 376],
  "Chandigarh": [20, 21, 5, 9, 32, 0, 0, 5, 172, 876, 48, 45, 91, 0, 4, 84, 2, 13, 4, 13, 604, 2048],
  "D&N Haveli": [8, 6, 2, 3, 4, 3, 0, 0, 59, 63, 40, 2, 1, 0, 3, 53, 0, 7, 0, 8, 148, 410],
  "Daman & Diu": [4, 2, 0, 1, 4, 1, 0, 3, 42, 37, 26, 7, 3, 1, None, None, None, None, None, None, 127, 258],
  "Delhi": [518, 512, 82, 484, 1250, 32, 21, 609, 2425, 20541, 236, 641, 1813, 66, 87, 2375, 132, 694, 189, 114, 27050, 59871],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 13, 7, 1, 0, 0, 0, 7, 9, 0, 0, 0, 0, 7, 44],
  "Pondicherry": [27, 15, 6, 2, 7, 2, 0, 4, 96, 473, 85, 13, 25, 2, 12, 354, 1, 14, 4, 2, 1325, 2469],
 },
}
