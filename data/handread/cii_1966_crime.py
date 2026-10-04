# CII 1966 by crime head, States / U.Ts. / cities, from the 1966 columns of Table IV of the 1967 edition: incidence of crime under
# different heads during 1966 and 1967 (raw/cii/1967/table_content/table-4-1967.pdf, pages 1-6 = printed pp. 18-23). The 1966 edition
# itself prints no State x head table (only one appendix per head), so this two-year table of the next edition is used. Its 1966 Total
# column agrees place by place with the 1966 edition's Table III (raw/cii/1966/table_content/table-3-1966.pdf page 2), which still names
# Tamil Nadu "Madras". ".." (nil) is entered as 0. No "other IPC crimes" column is printed, so each column is checked against the printed
# TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and TOTAL (cities) by scripts/check_handread.py.
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts, Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime cases 1966
KIND, YEAR, PUB = "crime", 1966, "cii"
SOURCE = "raw/cii/1967/table_content/table-4-1967.pdf"
PAGES = "1-6"
TITLE = "Table IV (CII 1967): Incidence of crime under different heads during 1966 and 1967 showing percentage variation (1966 figures)"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("TOTAL (STATES)", "Murder"): (14433, 12433, 'printed 14,433; the States add up to 12,433, 12,433 + U.Ts. 198 = the printed GRAND TOTAL 12,631, and the printed 1967 variation +6.0% = 13,185 / 12,433; Appendix III of the 1966 edition (appendix-1966.pdf p. 10) prints 12,433 and 12,631'),
    ("TOTAL (CITIES)", "Robbery"): (4444, 444, 'printed 4,444; the cities add up to 444 and the printed 1967 variation +26.6% = 562 / 444'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [896, 131, 93, 141, 5530, 1210, 10951, 1777, 863, 303, 60, 35249],
  "Assam": [399, 374, 222, 212, 3404, 501, 5823, 1993, 413, 277, 6, 20708],
  "Bihar": [1072, 640, 1012, 689, 21533, 830, 21692, 6469, 1269, 598, 50, 72699],
  "Gujarat": [755, 267, 65, 504, 4281, 786, 10822, 417, 1027, 543, 17, 31944],
  "Haryana": [183, 134, 6, 19, 1273, 355, 1965, 82, 323, 268, 2, 7398],
  "Jammu & Kashmir": [71, 142, 18, 18, 801, 134, 830, 417, 131, 80, 0, 4971],
  "Kerala": [260, 63, 15, 59, 2241, 129, 3181, 1317, 470, 129, 65, 19257],
  "Madhya Pradesh": [1570, 716, 413, 911, 20439, 4460, 31466, 1414, 1473, 1274, 14, 88476],
  "Maharashtra": [1240, 515, 332, 1452, 14061, 1720, 43396, 1358, 3226, 1775, 51, 92756],
  "Mysore": [753, 120, 99, 137, 6999, 986, 10806, 1024, 762, 377, 83, 31991],
  "Nagaland": [10, 3, 6, 15, 74, 10, 237, 19, 26, 7, 0, 526],
  "Orissa": [385, 89, 60, 216, 6101, 954, 10754, 1224, 771, 426, 16, 28491],
  "Punjab": [473, 268, 1, 24, 1642, 248, 3030, 50, 465, 383, 12, 12667],
  "Rajasthan": [531, 956, 95, 753, 6959, 1917, 7657, 2495, 794, 697, 7, 32962],
  "Tamil Nadu": [758, 473, 39, 130, 8389, 2007, 20605, 2308, 1960, 888, 172, 68019],
  "Uttar Pradesh": [2587, 1636, 1578, 2619, 32554, 6522, 53932, 6540, 5980, 1823, 32, 143179],
  "West Bengal": [490, 768, 651, 526, 10914, 833, 24474, 5233, 1485, 1123, 31, 75933],
  "TOTAL (STATES)": [12433, 7295, 4705, 8425, 147195, 23602, 261621, 34137, 21438, 10971, 618, 767226],
 },
 "U.Ts.": {
  "A. & N. Islands": [8, 3, 0, 3, 46, 2, 67, 5, 9, 4, 2, 301],
  "Chandigarh": [1, 4, 0, 1, 24, 2, 190, 2, 3, 12, 0, 261],
  "Dadra & Nagar Haveli": [4, 0, 6, 1, 19, 2, 20, 0, 1, 1, 0, 89],
  "Delhi": [73, 249, 3, 54, 1502, 45, 10008, 102, 549, 415, 27, 16934],
  "Goa, Daman & Diu": [10, 6, 4, 28, 450, 4, 671, 44, 69, 21, 3, 1962],
  "Himachal Pradesh": [35, 61, 0, 25, 417, 30, 447, 50, 122, 64, 2, 2276],
  "Laccadives": [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],
  "Manipur": [38, 196, 71, 28, 127, 52, 646, 135, 92, 84, 0, 2279],
  "Pondicherry": [4, 15, 0, 1, 139, 20, 479, 31, 42, 24, 2, 1204],
  "Tripura": [25, 45, 28, 19, 261, 344, 445, 190, 28, 10, 1, 2197],
  "TOTAL (U.TS.)": [198, 579, 112, 160, 2985, 501, 12977, 559, 915, 635, 37, 27507],
 },
 "Cities": {
  "Ahmedabad": [33, 37, 0, 14, 384, 47, 1179, 54, 117, 94, 1, 3179],
  "Bangalore": [20, 12, 1, 7, 878, 30, 2775, 23, 132, 109, 29, 4820],
  "Bombay": [133, 180, 23, 297, 2027, 55, 16079, 304, 1321, 884, 31, 28085],
  "Calcutta": [41, 129, 0, 20, 494, 22, 4831, 307, 391, 347, 6, 20759],
  "Delhi": [61, 233, 2, 48, 1366, 30, 9670, 90, 525, 400, 27, 15981],
  "Hyderabad": [11, 21, 1, 3, 479, 20, 1320, 26, 78, 83, 0, 2442],
  "Kanpur": [37, 77, 2, 51, 693, 25, 3273, 124, 556, 164, 2, 6149],
  "Madras": [13, 47, 0, 4, 227, 62, 4966, 24, 585, 362, 64, 10659],
  "TOTAL (CITIES)": [349, 736, 29, 444, 6548, 291, 44093, 952, 3705, 2443, 160, 92074],
 },
 "Grand": {"GRAND TOTAL": [12631, 7874, 4817, 8585, 150180, 24103, 274598, 34696, 22353, 11606, 655, 794733]},
}
