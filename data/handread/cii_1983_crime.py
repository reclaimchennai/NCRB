# CII 1983, Chapter 1, Table 5: incidence of cognizable IPC crime by crime head, States / UTs / 12 cities
# (raw/cii/1983/table_chapter/chapter-1-1983.pdf, pages 9, 13, 17, 21, 23, printed pages 12, 16, 20, 24, 26 -- three
# heads per page, the pages between are charts). Read from the page images; the volume-per-lakh (V) columns are skipped.
# '..' (nil) is 0. Every figure was read a second time in Table 6 (raw/cii/1983/table_content/table-6-1983.pdf, pages
# 1-7, printed pages 28-34: incidence under each head in 1982 and 1983 with the percentage variation), which prints the
# same 1983 counts for every head except 'Others' (the two printings differ in one figure, Lucknow robbery; Rajasthan
# cheating, under an ink blot in Table 5, is 2,056 in Table 6). Every row adds up to its printed Total cognizable crime
# and every column to the printed section totals (scripts/check_handread.py) after the two corrections below.
KIND, YEAR, PUB = "crime", 1983, "cii"
SOURCE = "raw/cii/1983/table_chapter/chapter-1-1983.pdf"
PAGES = "9, 13, 17, 21, 23"
TITLE = "Table 5: Incidence of cognizable crime and volume of crime per lakh of population under important heads of Indian Penal Code during 1983 (States, Union Territories and Cities)"
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary", "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Others", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Madras", "Others"): (6021, 6121, "printed 6,021; the Madras row then adds up to its printed total 13816 and the Cities column to its printed 59343, and the printed rate 174.9 on Madras's population (13816 / 394.7 = 35.0 lakh) is 6121, not 6021 (172.0)"),
    ("Lucknow", "Robbery"): (49, 79, "Table 5 prints 49, Table 6 prints 79; with 79 the Lucknow row adds up to its printed total 6659 and the Cities column to its printed 2249, and the printed rate 8.5 on Lucknow's population (6659 / 716.0 = 9.3 lakh) is 79, not 49 (5.3)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1401, 32, 349, 452, 374, 532, 6529, 17251, 3813, 613, 1012, 84, 52331, 84773],
  "Assam": [1911, 24, 265, 761, 519, 698, 4392, 9735, 9917, 413, 492, 0, 19852, 48979],
  "Bihar": [3107, 628, 643, 1653, 3607, 2156, 10446, 27955, 17567, 1408, 1314, 14, 38164, 108662],
  "Gujarat": [958, 5, 92, 561, 186, 827, 5620, 18882, 1974, 1236, 899, 13, 48306, 79559],
  "Haryana": [366, 103, 85, 202, 26, 86, 2300, 3261, 215, 254, 354, 11, 9511, 16774],
  "Himachal Pradesh": [64, 17, 32, 66, 2, 23, 462, 561, 217, 100, 84, 2, 2800, 4430],
  "Jammu & Kashmir": [103, 8, 146, 461, 33, 46, 1366, 2573, 2022, 141, 205, 0, 10035, 17139],
  "Karnataka": [947, 15, 119, 301, 166, 589, 9069, 17462, 5735, 802, 1259, 131, 40709, 77304],
  "Kerala": [514, 24, 116, 108, 33, 138, 4119, 3468, 5440, 408, 850, 97, 31994, 47309],
  "Madhya Pradesh": [2593, 45, 1271, 1019, 497, 2660, 21613, 42081, 6602, 1289, 1628, 18, 85039, 166355],
  "Maharashtra": [1973, 26, 565, 813, 595, 3334, 16890, 53641, 9037, 2477, 2246, 73, 65579, 157249],
  "Manipur": [71, 4, 5, 205, 31, 66, 265, 548, 226, 86, 128, 12, 1422, 3069],
  "Meghalaya": [61, 3, 8, 11, 31, 37, 258, 460, 59, 14, 36, 0, 668, 1646],
  "Nagaland": [27, 2, 10, 19, 6, 49, 319, 470, 39, 64, 41, 0, 894, 1940],
  "Orissa": [566, 52, 174, 248, 377, 836, 6522, 12285, 2761, 462, 313, 12, 20054, 44662],
  "Punjab": [591, 169, 57, 204, 9, 64, 1018, 1703, 89, 356, 354, 9, 9337, 13960],
  "Rajasthan": [979, 35, 378, 1465, 147, 1217, 6431, 12202, 11874, 1030, 2056, 13, 33540, 71367],
  "Sikkim": [7, 0, 4, 1, 3, 5, 28, 85, 7, 8, 4, 0, 105, 257],
  "Tamil Nadu": [1310, 31, 202, 640, 63, 373, 11446, 29566, 9575, 1244, 1451, 166, 58349, 114416],
  "Tripura": [111, 1, 26, 39, 228, 200, 1175, 1471, 374, 42, 30, 0, 2203, 5900],
  "Uttar Pradesh": [5752, 1702, 856, 2834, 4210, 5710, 22494, 49804, 9016, 4256, 2966, 62, 55264, 164926],
  "West Bengal": [1327, 616, 464, 936, 1193, 1339, 3667, 32031, 10952, 1221, 1089, 53, 26351, 81239],
  "TOTAL (STATES)": [24739, 3542, 5867, 12999, 12336, 20985, 136429, 337495, 107511, 17924, 18811, 770, 612507, 1311915],
 },
 "U.Ts.": {
  "A. & N. Islands": [12, 1, 4, 3, 0, 6, 50, 164, 42, 10, 13, 0, 450, 755],
  "Arunachal Pradesh": [34, 5, 8, 17, 7, 17, 131, 237, 19, 17, 9, 1, 569, 1071],
  "Chandigarh": [19, 7, 3, 23, 0, 11, 140, 735, 19, 43, 64, 2, 546, 1612],
  "D. & N. Haveli": [7, 0, 1, 2, 2, 4, 36, 25, 5, 6, 5, 0, 112, 205],
  "Delhi": [245, 226, 79, 759, 29, 211, 1503, 13028, 173, 384, 752, 26, 9945, 27360],
  "Goa, Daman & Diu": [20, 5, 11, 16, 3, 44, 536, 805, 234, 43, 52, 5, 1162, 2936],
  "Lakshadweep": [0, 0, 1, 0, 0, 0, 1, 6, 1, 0, 0, 0, 9, 18],
  "Mizoram": [22, 7, 38, 11, 3, 23, 81, 262, 1, 53, 34, 5, 1156, 1696],
  "Pondicherry": [14, 0, 7, 12, 2, 9, 196, 779, 96, 34, 27, 0, 1122, 2298],
  "TOTAL (U.TS.)": [373, 251, 152, 843, 46, 325, 2674, 16041, 590, 590, 956, 39, 15071, 37951],
 },
 "Cities": {
  "Ahmedabad": [60, 0, 8, 115, 10, 31, 540, 2508, 298, 88, 148, 5, 6689, 10500],
  "Bangalore": [56, 2, 21, 46, 7, 270, 1467, 6275, 242, 195, 540, 74, 4954, 14149],
  "Bombay": [261, 2, 107, 201, 47, 567, 2059, 13973, 222, 709, 917, 42, 12615, 31722],
  "Calcutta": [95, 11, 21, 114, 45, 360, 916, 6943, 830, 351, 426, 27, 3923, 14062],
  "Delhi": [214, 190, 74, 722, 28, 200, 1443, 12600, 159, 372, 732, 26, 9310, 26070],
  "Hyderabad": [99, 0, 22, 63, 20, 75, 1066, 2565, 312, 90, 339, 22, 1976, 6649],
  "Jaipur": [21, 0, 13, 80, 2, 67, 496, 1323, 537, 77, 200, 5, 1670, 4491],
  "Kanpur": [119, 165, 39, 169, 30, 166, 545, 1259, 189, 409, 110, 31, 3407, 6638],
  "Lucknow": [65, 16, 10, 98, 20, 79, 725, 2760, 168, 217, 218, 28, 2255, 6659],
  "Madras": [33, 14, 22, 42, 3, 76, 645, 6141, 104, 86, 505, 24, 6121, 13816],
  "Nagpur": [68, 0, 35, 50, 18, 252, 746, 2270, 133, 62, 136, 2, 2376, 6148],
  "Pune": [52, 5, 16, 56, 15, 106, 687, 2101, 167, 112, 146, 7, 4047, 7517],
  "TOTAL (CITIES)": [1143, 405, 388, 1756, 245, 2249, 11335, 60718, 3361, 2768, 4417, 293, 59343, 148421],
 },
 "Grand": {"GRAND TOTAL": [25112, 3793, 6019, 13842, 12382, 21310, 139103, 353536, 108101, 18514, 19767, 809, 627578, 1349866]},
}
