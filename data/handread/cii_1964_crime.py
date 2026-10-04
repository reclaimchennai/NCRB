# CII 1964 by crime head, States / U.Ts. / cities, assembled from the per-head appendices of the 1964 edition
# (raw/cii/1964/table_chapter/appendix-1964.pdf): column 5 "cases reported during the year" of Appendix I (total cognizable crime,
# pages 2 and 4), III murder (10, 12), V kidnapping & abduction (18, 20), VII dacoity (26, 28), IX robbery (34, 36), XI house-breaking
# (42, 44), XIII cattle thefts (50, 52), XV ordinary thefts (58, 60), XVII riots (66, 68), XIX criminal breach of trust (74, 76),
# XXI cheating (82, 84), XXIII counterfeiting (90, 92). The edition prints no single State x head table (Table III, TABLE-31964.pdf,
# gives the total only). ".."/"-" (nil) entered as 0. Kanpur's figures under every head are printed "Not available" (None) and the
# cities' head totals leave it out; its total cognizable crime (6,320) is printed in Appendix I and included in that city total.
# No "other IPC crimes" column, so each column is checked against the printed TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and
# TOTAL (cities) by scripts/check_handread.py.
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts, Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime cases reported
KIND, YEAR, PUB = "crime", 1964, "cii"
SOURCE = "raw/cii/1964/table_chapter/appendix-1964.pdf"
PAGES = "2,4,10,12,18,20,26,28,34,36,42,44,50,52,58,60,66,68,74,76,82,84,90,92"
TITLE = "Appendices I-XXIII (cases): cases reported during the year 1964 under total cognizable crime and each head, States/U.Ts./Cities"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("TOTAL (U.TS.)", "Total cognizable crimes (IPC)"): (25451, 25461, 'printed 25,451; the U.Ts. add up to 25,461 (each as also printed for 1964 in Table III of CII 1965) and TOTAL (States) 7,33,552 + 25,461 = the printed GRAND TOTAL 7,59,013'),
    ("Ahmedabad", "Cattle thefts"): (84, 34, 'first digit damaged (reads 8 or B); the cities add up to the printed TOTAL 275 only with 34, and the printed volume per lakh 2.71 and true cases 34 (page 53) agree'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [859, 118, 95, 173, 6298, 1161, 11042, 2354, 720, 320, 12, 37697],
  "Assam": [375, 446, 196, 172, 3966, 362, 5448, 1619, 480, 338, 34, 20170],
  "Bihar": [1031, 519, 856, 660, 22367, 737, 19435, 5882, 1193, 534, 33, 69061],
  "Gujarat": [660, 305, 97, 479, 4827, 841, 10812, 696, 1002, 564, 10, 32106],
  "Jammu & Kashmir": [85, 99, 23, 15, 795, 111, 667, 445, 133, 46, 2, 4372],
  "Kerala": [231, 49, 24, 49, 2334, 168, 2982, 1187, 382, 171, 16, 18124],
  "Madhya Pradesh": [1386, 829, 536, 978, 17362, 3955, 28098, 1410, 1353, 1366, 21, 80612],
  "Madras": [799, 483, 39, 127, 7192, 2023, 18857, 2007, 1760, 866, 27, 62906],
  "Maharashtra": [1210, 520, 330, 1343, 12477, 1329, 33379, 1336, 2728, 1643, 34, 77566],
  "Mysore": [703, 140, 145, 150, 5750, 849, 8592, 1082, 652, 297, 11, 27703],
  "Nagaland": [13, 7, 6, 10, 55, 0, 86, 0, 13, 4, 0, 484],
  "Orissa": [350, 110, 83, 200, 5295, 662, 8984, 1552, 633, 357, 15, 25899],
  "Punjab": [539, 484, 3, 52, 3174, 609, 4896, 159, 879, 501, 7, 19283],
  "Rajasthan": [469, 957, 93, 609, 7132, 1823, 6502, 1614, 720, 719, 4, 29965],
  "Uttar Pradesh": [2307, 1716, 2142, 2573, 40594, 7566, 54614, 6094, 6304, 2088, 43, 150260],
  "West Bengal": [588, 696, 520, 541, 11057, 791, 24037, 4613, 1298, 1104, 39, 77344],
  "TOTAL (STATES)": [11605, 7478, 5188, 8131, 150675, 22987, 238431, 32050, 20250, 10918, 308, 733552],
 },
 "U.Ts.": {
  "A. & N. Islands": [4, 0, 0, 0, 19, 4, 40, 4, 9, 0, 0, 182],
  "Delhi": [59, 257, 2, 73, 1850, 105, 9227, 89, 501, 575, 9, 16064],
  "Goa, Daman & Diu": [13, 17, 3, 41, 271, 6, 604, 43, 81, 30, 0, 1724],
  "Himachal Pradesh": [20, 45, 1, 26, 245, 17, 321, 68, 139, 19, 0, 1588],
  "Laccadives": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
  "Manipur": [18, 153, 29, 24, 224, 36, 525, 153, 82, 96, 0, 2229],
  "Pondicherry": [3, 5, 0, 2, 195, 23, 475, 33, 59, 15, 0, 1238],
  "Tripura": [26, 95, 64, 39, 383, 326, 549, 253, 59, 17, 0, 2432],
  "TOTAL (U.TS.)": [143, 572, 99, 205, 3187, 517, 11741, 643, 930, 752, 9, 25461],
 },
 "Cities": {
  "Ahmedabad": [31, 51, 2, 27, 448, 34, 1357, 218, 156, 80, 2, 3332],
  "Bangalore": [15, 14, 0, 12, 860, 30, 1881, 39, 119, 93, 3, 3800],
  "Bombay": [152, 162, 23, 273, 1620, 48, 11489, 256, 1034, 875, 20, 21563],
  "Calcutta": [68, 92, 9, 19, 689, 19, 4981, 217, 327, 385, 6, 23598],
  "Delhi": [48, 232, 2, 60, 1637, 62, 8854, 70, 471, 559, 9, 14981],
  "Hyderabad": [11, 14, 0, 5, 536, 18, 1519, 22, 111, 118, 1, 2647],
  "Kanpur": [None, None, None, None, None, None, None, None, None, None, None, 6320],
  "Madras": [15, 53, 0, 4, 212, 64, 3543, 31, 387, 289, 5, 7470],
  "TOTAL (CITIES)": [340, 618, 36, 400, 6002, 275, 33624, 853, 2605, 2399, 46, 83711],
 },
 "Grand": {"GRAND TOTAL": [11748, 8050, 5287, 8336, 153862, 23504, 250172, 32693, 21180, 11670, 317, 759013]},
}
