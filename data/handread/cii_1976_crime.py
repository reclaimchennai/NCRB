# CII 1976, Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads
# of Indian Penal Code, States / UTs / cities (raw/cii/1976/table_content/table-5-1976.pdf, pages 1-2; the running
# head of page 2 misprints the year as 1975, the figures are those of 1976). Read from the page images; only the
# incidence (I) columns are kept, the volume per lakh (V) columns skipped; '..' and '—' are entered as 0. The table
# prints selected heads and the total cognizable crime, with no 'other IPC crimes' column, so each column is checked
# against the printed totals (CHECK = "columns").
KIND, YEAR, PUB = "crime", 1976, "cii"
SOURCE = "raw/cii/1976/table_content/table-5-1976.pdf"
PAGES = "1-2"
TITLE = ("Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads "
         "of Indian Penal Code during the year 1976")
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary",
        "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
    ("Andhra Pradesh", "Murder"): (112, 1129, "printed 112 (2.4 per lakh), a digit lost; the States column adds up to the printed 16,466 only with 1,129, which is 2.4 per lakh on the State's population (61,170 = 128.2 per lakh); Table 6 (1975 and 1976) prints 1,129 (+0.6% on 1,122)"),
    ("West Bengal", "Thefts"): (318699, 31869, "printed 318699 (63.0 per lakh); 31,869 is 63.0 per lakh on the State's population (84,879 = 167.8 per lakh), and the States column then adds up to the printed 349,352"),
    ("D & N Haveli", "Criminal breach of trust"): (None, 2, "figure missing on the page, V printed 2.5; 2 is 2.5 per lakh on the UT's population (146 = 178.9 per lakh), and the UTs column then adds up to the printed 512"),
    ("TOTAL (U.TS.)", "Riots"): (19, 192, "printed 19 (2.3 per lakh), a digit lost; the UT figures add up to 192, Grand Total 63,675 - States 63,483 = 192, and 192 is 2.3 per lakh on the UT population"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1129, 15, 106, 196, 162, 237, 6737, 15208, 2455, 610, 728, 175, 61170],
  "Assam": [413, 28, 224, 547, 308, 394, 5844, 9035, 3713, 541, 525, 9, 32896],
  "Bihar": [1830, 282, 351, 793, 2356, 1433, 16373, 29728, 12630, 1775, 1082, 55, 94782],
  "Gujarat": [840, 10, 99, 451, 98, 735, 6637, 19253, 984, 1495, 990, 15, 55895],
  "Haryana": [171, 95, 52, 107, 20, 19, 1519, 2435, 42, 455, 192, 5, 9146],
  "Himachal Pradesh": [60, 6, 22, 92, 2, 27, 570, 598, 153, 121, 97, 1, 3780],
  "Jammu & Kashmir": [78, 17, 91, 443, 16, 31, 1823, 2370, 1152, 172, 211, 0, 12319],
  "Karnataka": [699, 11, 42, 182, 129, 223, 8138, 14058, 2713, 894, 1188, 100, 50640],
  "Kerala": [326, 5, 52, 80, 22, 104, 3859, 3714, 2730, 474, 477, 67, 31868],
  "Madhya Pradesh": [1975, 121, 698, 860, 349, 1495, 21647, 37440, 2944, 1469, 1740, 34, 122299],
  "Maharashtra": [1406, 24, 315, 671, 424, 2321, 19755, 57951, 1476, 4070, 2736, 42, 133440],
  "Manipur": [42, 2, 11, 183, 24, 33, 313, 819, 163, 79, 118, 1, 2984],
  "Meghalaya": [61, 3, 12, 23, 18, 48, 215, 500, 59, 34, 30, 0, 1604],
  "Nagaland": [17, 3, 7, 8, 10, 30, 262, 372, 38, 44, 32, 1, 824],
  "Orissa": [463, 57, 88, 158, 178, 394, 6833, 11258, 1647, 570, 406, 29, 33400],
  "Punjab": [553, 149, 98, 286, 3, 50, 1453, 2615, 17, 486, 453, 14, 11775],
  "Rajasthan": [648, 49, 200, 1342, 105, 1279, 8116, 11911, 5766, 1100, 1391, 0, 50842],
  "Sikkim": [12, 0, 8, 2, 0, 5, 45, 125, 5, 16, 11, 1, 230],
  "Tamil Nadu": [709, 11, 75, 314, 24, 154, 8154, 25907, 2675, 1369, 1814, 78, 69806],
  "Tripura": [44, 3, 5, 21, 52, 67, 769, 848, 207, 23, 29, 1, 3010],
  "U.P.": [4234, 1194, 745, 3064, 5643, 7790, 39574, 71338, 11175, 5705, 2988, 115, 195633],
  "West Bengal": [756, 372, 491, 986, 953, 858, 7322, 31869, 10739, 1642, 1561, 78, 84879],
  "TOTAL (STATES)": [16466, 2457, 3792, 10809, 10896, 17727, 165958, 349352, 63483, 23144, 18799, 821, 1063222],
 },
 "U.Ts.": {
  "A & N Islands": [7, 0, 3, 3, 0, 7, 57, 114, 23, 11, 14, 0, 517],
  "Arunachal Pradesh": [20, 3, 4, 9, 0, 5, 43, 121, 6, 12, 1, 0, 399],
  "Chandigarh": [2, 4, 3, 15, 0, 7, 89, 709, 11, 45, 44, 0, 1312],
  "D & N Haveli": [7, 0, 0, 1, 1, 3, 30, 33, 17, 2, 0, 0, 146],
  "Delhi": [120, 118, 59, 386, 6, 142, 1702, 13280, 38, 336, 626, 63, 23105],
  "Goa, Daman & Diu": [12, 1, 2, 7, 3, 28, 496, 611, 59, 43, 26, 3, 2150],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 2, 6, 1, 0, 0, 0, 14],
  "Mizoram": [34, 1, 22, 2, 3, 49, 60, 198, 2, 32, 26, 0, 647],
  "Pondicherry": [5, 0, 8, 18, 1, 6, 218, 714, 35, 31, 52, 0, 2385],
  "TOTAL (U.TS.)": [207, 127, 101, 441, 14, 247, 2697, 15786, 192, 512, 789, 66, 30675],
 },
 "Grand": {
  "GRAND TOTAL": [16673, 2584, 3893, 11250, 10910, 17974, 168655, 365138, 63675, 23656, 19588, 887, 1093897],
 },
 "Cities": {
  "Ahmedabad": [49, 2, 8, 86, 2, 24, 524, 2081, 81, 142, 169, 7, 6231],
  "Bangalore": [20, 0, 2, 38, 7, 35, 1704, 4152, 82, 182, 501, 45, 11002],
  "Bombay": [145, 0, 56, 183, 23, 193, 2535, 15941, 114, 1050, 1166, 4, 31376],
  "Calcutta": [57, 8, 21, 139, 11, 46, 480, 5582, 696, 382, 484, 48, 12321],
  "Delhi": [105, 91, 52, 368, 6, 133, 1560, 12534, 32, 328, 599, 62, 21464],
  "Hyderabad": [28, 1, 5, 36, 1, 11, 921, 2830, 23, 52, 187, 36, 5174],
  "Kanpur": [75, 23, 18, 158, 53, 122, 998, 4208, 147, 521, 260, 27, 8399],
  "Madras": [25, 0, 9, 57, 8, 36, 881, 7824, 64, 448, 1061, 10, 14940],
  "TOTAL (CITIES)": [504, 125, 171, 1065, 111, 600, 9603, 55152, 1239, 3105, 4427, 239, 110907],
 },
}
