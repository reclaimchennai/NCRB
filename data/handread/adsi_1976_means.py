# ADSI 1976, Appendix VI: suicides by means, States / UTs / cities (raw/adsi/1976/table_content/1680155995appendix-61976.pdf,
# pages 1-4). Read from the page images; every row is checked against its printed Total and every column against the
# printed Total (States), Total (U.Ts.), Grand Total and Total (Cities) by scripts/check_handread.py.
# Columns: Railway, Machine, Firearms, Weapons, Poison, Fire, Drowning, Hanging, Jumping, Other causes, Total
KIND, YEAR, PUB = "means", 1976, "adsi"
SOURCE = "raw/adsi/1976/table_content/1680155995appendix-61976.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of Suicidal Deaths by different means, States/U.T.s/Cities, 1976"
CATS = ["By Railway", "By Machine", "By Firearms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Other causes", "Total"]
# corrections: (place, category): (printed, corrected, why) -- only where the row total AND the printed percentage agree
CORRECTIONS = {
    ("Meghalaya", "By Fire"): (11, 1, "printed 11 (2.4%); 1/42 = 2.4% and the row then adds up to 42"),
    ("Meghalaya", "By Other causes"): (271, 27, "printed 271 (64.3%); 27/42 = 64.3% and the row then adds up to 42"),
    ("Rajasthan", "By Drowning"): (53, 253, "printed 53 (42.7%), the first digit faint; 253/593 = 42.7% and the row then adds up to 593"),
    ("Maharashtra", "By Jumping"): (37, 137, "printed 37 (3.5%); 137/3903 = 3.5%, and both the row (3903) and the Jumping column (585) then add up"),
    ("Calcutta", "By Drowning"): (1, 1, "printed 1 (12.3%); 1/44 = 2.3%, the percentage is the misprint"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [273, 2, 9, 10, 1184, 223, 1413, 562, 17, 526, 4219],
  "Assam": [70, 4, 0, 6, 80, 36, 232, 458, 11, 316, 1213],
  "Bihar": [49, 5, 2, 5, 82, 32, 249, 66, 9, 114, 613],
  "Gujarat": [83, 8, 7, 6, 315, 275, 382, 150, 22, 228, 1476],
  "Haryana": [36, 6, 8, 0, 13, 95, 211, 109, 37, 132, 647],
  "Himachal Pradesh": [0, 0, 2, 1, 9, 0, 16, 29, 1, 16, 74],
  "Jammu & Kashmir": [2, 0, 1, 0, 5, 0, 20, 5, 0, 16, 49],
  "Karnataka": [116, 4, 8, 77, 867, 231, 1452, 848, 96, 579, 4278],
  "Kerala": [180, 0, 2, 8, 1454, 11, 446, 1139, 35, 282, 3557],
  "Madhya Pradesh": [315, 114, 248, 104, 393, 340, 228, 134, 49, 376, 2301],
  "Maharashtra": [203, 0, 6, 9, 1287, 452, 774, 451, 137, 584, 3903],
  "Manipur": [0, 2, 1, 0, 4, 0, 0, 0, 0, 4, 11],
  "Meghalaya": [0, 0, 0, 0, 0, 1, 6, 4, 4, 27, 42],
  "Nagaland": [0, 0, 0, 0, 0, 0, 1, 2, 0, 2, 5],
  "Orissa": [257, 0, 4, 0, 575, 9, 190, 537, 2, 373, 1947],
  "Punjab": [94, 5, 16, 15, 23, 23, 39, 51, 4, 11, 281],
  "Rajasthan": [66, 5, 11, 4, 24, 70, 253, 78, 8, 74, 593],
  "Sikkim": [0, 0, 0, 0, 4, 1, 2, 4, 1, 0, 12],
  "Tamil Nadu": [97, 3, 1, 8, 1836, 324, 919, 799, 22, 813, 4822],
  "Tripura": [0, 0, 3, 0, 288, 7, 6, 112, 0, 9, 425],
  "Uttar Pradesh": [512, 48, 239, 107, 197, 288, 341, 328, 72, 481, 2613],
  "West Bengal": [171, 21, 9, 15, 3642, 310, 439, 1682, 58, 1318, 7665],
  "TOTAL (STATES)": [2524, 227, 577, 375, 12282, 2728, 7619, 7548, 585, 6281, 40746],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 1, 0, 25, 0, 10, 27, 0, 8, 71],
  "Arunachal Pradesh": [0, 0, 0, 0, 1, 0, 2, 4, 0, 1, 8],
  "Chandigarh": [0, 0, 0, 0, 0, 7, 5, 5, 2, 2, 21],
  "D & N Haveli": [0, 0, 0, 0, 3, 0, 1, 13, 0, 0, 17],
  "Delhi": [42, 0, 0, 1, 34, 62, 37, 24, 12, 28, 240],
  "Goa, Daman & Diu": [4, 0, 0, 0, 21, 6, 24, 13, 8, 0, 76],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
  "Mizoram": [0, 0, 0, 0, 0, 0, 2, 5, 0, 0, 7],
  "Pondicherry": [0, 0, 0, 0, 107, 0, 20, 61, 3, 37, 228],
  "TOTAL (U.TS.)": [46, 0, 1, 1, 191, 75, 101, 153, 25, 76, 669],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 1, 18, 42, 8, 5, 4, 37, 115],
  "Bangalore": [1, 0, 0, 2, 61, 46, 59, 40, 0, 114, 323],
  "Bombay": [0, 0, 1, 3, 45, 65, 25, 36, 11, 23, 209],
  "Calcutta": [0, 0, 0, 1, 8, 6, 1, 26, 2, 0, 44],
  "Delhi": [42, 0, 0, 0, 27, 56, 21, 16, 8, 10, 180],
  "Hyderabad": [0, 0, 4, 0, 27, 11, 15, 0, 0, 46, 103],
  "Kanpur": [2, 0, 1, 0, 9, 8, 1, 18, 0, 0, 39],
  "Madras": [0, 2, 0, 0, 95, 62, 56, 57, 2, 61, 335],
  "TOTAL (CITIES)": [45, 2, 6, 7, 290, 296, 186, 198, 27, 291, 1348],
 },
 "Grand": {"GRAND TOTAL": [2570, 227, 578, 376, 12473, 2803, 7720, 7701, 610, 6357, 41415]},
}
