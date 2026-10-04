# CII 1993, Table 6: incidence of cognizable IPC crime by crime head, States / UTs / 23 cities
# (raw/cii/1993/table_content/table-6-1993-crime.pdf, pages 1-10, printed pages 49-58; odd pages States/UTs, even pages
# cities). Read from the page images; the rate (R) columns are skipped. Kidnapping & abduction is the printed total; its
# two printed sub-columns (of women & girls, of others) add up to it on every row and are left out so the heads add up to
# the Total. The printed 'TOTAL (ALL-INDIA)' row is GRAND TOTAL here. The cities have no printed total row. Every row
# adds up to its printed Total cognizable crimes under IPC and every State / UT column to the printed totals
# (scripts/check_handread.py). The totals rows are printed on a dark screen; where a leading digit is lost in the screen
# the reading that every check confirms is used (see CORRECTIONS).
KIND, YEAR, PUB = "crime", 1993, "cii"
SOURCE = "raw/cii/1993/table_content/table-6-1993-crime.pdf"
PAGES = "1-10"
TITLE = "Table 6: Incidence (I) & rate (R) of cognizable crimes (IPC) under different crime heads in States, UTs & cities during 1993"
CATS = ["Murder", "Attempt to commit murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Preparation & assembly for dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Other IPC crimes", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("TOTAL (STATES)", "Attempt to commit murder"): (28213, 29213, "on the dark screen the first digits read 28213; the States add up to 29213, States + UTs (512) = 29725 = the All-India total, and the printed rate 3.4 fits 29213 (not 28213 = 3.2)"),
    ("GRAND TOTAL", "Attempt to commit murder"): (28725, 29725, "on the dark screen the first digits read 28725; 29213 + 512 = 29725, and the rate 3.4 fits 29725"),
    ("TOTAL (STATES)", "Dacoity"): (8324, 9324, "on the dark screen the first digit reads 8; the States add up to 9324, the rate 1.1 fits 9324 (8324 would be 1.0), and 9324 + 33 = 9357"),
    ("GRAND TOTAL", "Dacoity"): (8357, 9357, "on the dark screen the first digit reads 8; 9324 + 33 = 9357 and the rate 1.1 fits"),
    ("Karnataka", "Kidnapping & abduction"): (499, 498, "last digit blurred (reads 499 or 498); 498 = its printed sub-columns 306 + 192, the Karnataka row then adds up to its printed total 105863 and the States column to its printed 18965"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2514, 1385, 79, 840, 796, 680, 6, 1136, 6816, 19032, 3255, 621, 2207, 236, 59022, 98625],
  "Arunachal Pradesh": [55, 35, 5, 29, 19, 18, 1, 61, 157, 278, 19, 32, 20, 7, 824, 1560],
  "Assam": [1105, 336, 48, 560, 1158, 725, 23, 1010, 3599, 7859, 4462, 487, 554, 102, 15327, 37355],
  "Bihar": [4983, 4902, 624, 1118, 2635, 2754, 242, 3030, 7914, 20098, 13819, 1523, 1595, 30, 60375, 125642],
  "Goa": [36, 14, 9, 14, 26, 13, 0, 30, 579, 1083, 241, 49, 65, 16, 1936, 4111],
  "Gujarat": [1514, 854, 13, 355, 1071, 338, 0, 1053, 6361, 20728, 2682, 2742, 3619, 178, 78301, 119809],
  "Haryana": [611, 310, 98, 235, 313, 78, 22, 202, 2558, 4218, 435, 287, 679, 37, 21671, 31754],
  "Himachal Pradesh": [126, 72, 10, 100, 193, 12, 0, 34, 1084, 1148, 678, 138, 185, 7, 7077, 10864],
  "Jammu & Kashmir": [691, 585, 15, 115, 354, 45, 0, 96, 1601, 2264, 681, 100, 141, 0, 8043, 14731],
  "Karnataka": [1494, 951, 47, 232, 498, 306, 2, 985, 10141, 18680, 7856, 724, 1936, 1055, 60956, 105863],
  "Kerala": [506, 362, 28, 211, 135, 53, 18, 221, 4592, 3795, 6126, 324, 1372, 67, 59042, 76852],
  "Madhya Pradesh": [3250, 3091, 192, 2658, 1092, 260, 135, 2198, 18834, 32184, 3772, 669, 1407, 61, 109955, 179758],
  "Maharashtra": [3133, 1586, 150, 1145, 1158, 794, 89, 3388, 16791, 52247, 4892, 1974, 3145, 367, 93730, 184589],
  "Manipur": [319, 144, 3, 8, 123, 48, 0, 50, 97, 267, 112, 10, 83, 24, 1336, 2624],
  "Meghalaya": [106, 25, 2, 19, 27, 77, 0, 70, 219, 521, 56, 7, 31, 13, 690, 1863],
  "Mizoram": [39, 11, 2, 40, 7, 4, 0, 11, 239, 544, 3, 21, 61, 6, 477, 1465],
  "Nagaland": [104, 30, 0, 8, 43, 49, 0, 162, 223, 327, 25, 30, 29, 28, 488, 1546],
  "Orissa": [821, 963, 101, 405, 432, 307, 0, 957, 4699, 10172, 1941, 470, 444, 12, 29885, 51609],
  "Punjab": [702, 867, 112, 90, 189, 13, 18, 44, 939, 1069, 12, 135, 328, 18, 4909, 9445],
  "Rajasthan": [1406, 1515, 102, 893, 2372, 90, 16, 1038, 7551, 14262, 17668, 951, 4552, 274, 68410, 121100],
  "Sikkim": [12, 3, 3, 7, 4, 3, 0, 9, 97, 124, 42, 6, 10, 0, 342, 662],
  "Tamil Nadu": [1630, 1571, 28, 244, 774, 155, 0, 416, 6945, 22975, 8339, 621, 1107, 554, 80295, 125654],
  "Tripura": [255, 94, 0, 69, 101, 206, 4, 292, 520, 913, 440, 20, 14, 1, 2246, 5175],
  "Uttar Pradesh": [10589, 9054, 1543, 1787, 4423, 1778, 362, 6683, 17541, 45491, 9273, 3792, 3886, 403, 86883, 203488],
  "West Bengal": [1685, 453, 584, 712, 1022, 518, 142, 830, 1038, 24847, 6642, 623, 1162, 116, 30344, 70718],
  "TOTAL (STATES)": [37686, 29213, 3798, 11894, 18965, 9324, 1080, 24006, 121135, 305126, 93471, 16356, 28632, 3612, 882564, 1586862],
 },
 "U.Ts.": {
  "A & N Islands": [10, 10, 0, 4, 3, 0, 0, 5, 88, 84, 15, 6, 7, 2, 430, 664],
  "Chandigarh": [14, 15, 7, 6, 31, 0, 0, 9, 177, 906, 31, 22, 95, 1, 629, 1943],
  "D & N Haveli": [4, 1, 0, 0, 4, 1, 0, 1, 20, 27, 14, 3, 0, 0, 246, 321],
  "Daman & Diu": [4, 1, 0, 1, 2, 5, 0, 0, 22, 33, 28, 5, 4, 1, 116, 222],
  "Delhi": [487, 472, 83, 306, 817, 27, 22, 326, 1465, 13161, 219, 634, 1318, 99, 17161, 36597],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 8, 17, 1, 0, 0, 0, 22, 48],
  "Pondicherry": [35, 13, 2, 7, 8, 0, 0, 7, 105, 1080, 59, 13, 23, 13, 1914, 3279],
  "TOTAL (UTs)": [554, 512, 92, 324, 865, 33, 22, 348, 1885, 15308, 367, 683, 1447, 116, 20518, 43074],
 },
 "Cities": {
  "Ahmedabad": [154, 119, 3, 20, 174, 29, 0, 118, 879, 4353, 279, 488, 536, 25, 10322, 17499],
  "Bangalore": [163, 310, 3, 48, 111, 27, 2, 486, 2510, 7239, 342, 294, 936, 1010, 12998, 26479],
  "Bhopal": [55, 132, 9, 39, 42, 8, 0, 120, 495, 1211, 65, 10, 59, 7, 3532, 5784],
  "Bombay": [687, 354, 7, 131, 220, 117, 39, 824, 2855, 13470, 772, 559, 1054, 152, 14446, 35687],
  "Calcutta": [70, 118, 12, 33, 123, 38, 29, 163, 228, 5405, 467, 294, 650, 104, 4472, 12206],
  "Coimbatore": [16, 24, 0, 0, 10, 3, 0, 21, 263, 1163, 235, 18, 50, 73, 1370, 3246],
  "Delhi": [396, 401, 57, 270, 727, 24, 18, 277, 1292, 12560, 186, 577, 1274, 98, 15642, 33799],
  "Hyderabad": [103, 107, 7, 43, 76, 14, 0, 114, 1180, 3374, 170, 65, 448, 12, 3452, 9165],
  "Indore": [67, 155, 0, 21, 28, 2, 0, 99, 801, 2336, 73, 24, 80, 0, 4708, 8394],
  "Jaipur": [49, 35, 3, 28, 169, 0, 0, 76, 618, 2179, 1244, 139, 479, 71, 4345, 9435],
  "Kanpur": [271, 259, 21, 31, 185, 34, 14, 240, 641, 1909, 319, 299, 276, 149, 2489, 7137],
  "Kochi": [9, 11, 1, 5, 5, 0, 0, 11, 281, 302, 178, 19, 98, 3, 2477, 3400],
  "Lucknow": [103, 155, 18, 40, 85, 24, 8, 158, 821, 2584, 230, 204, 333, 11, 2172, 6946],
  "Ludhiana": [26, 31, 3, 3, 11, 1, 6, 4, 97, 125, 1, 11, 9, 4, 314, 646],
  "Madras": [100, 265, 3, 17, 12, 1, 0, 71, 530, 4393, 118, 263, 368, 107, 2688, 8936],
  "Madurai": [26, 20, 0, 4, 21, 0, 0, 24, 181, 871, 109, 13, 44, 106, 1516, 2935],
  "Nagpur": [110, 55, 3, 53, 71, 6, 3, 348, 915, 3452, 124, 121, 225, 8, 4545, 10039],
  "Patna": [161, 251, 21, 15, 96, 16, 8, 156, 401, 1922, 260, 141, 101, 2, 2195, 5746],
  "Pune": [71, 68, 3, 47, 58, 6, 2, 124, 898, 2692, 85, 70, 246, 17, 5438, 9825],
  "Surat": [89, 49, 1, 14, 49, 29, 0, 60, 411, 1421, 167, 61, 162, 1, 2022, 4536],
  "Vadodara": [41, 13, 2, 11, 36, 3, 0, 21, 348, 1368, 318, 112, 215, 11, 2672, 5171],
  "Varanasi": [62, 131, 8, 12, 54, 10, 8, 60, 245, 727, 101, 76, 77, 27, 976, 2574],
  "Vishakhapatnam": [25, 17, 3, 12, 20, 1, 0, 30, 384, 1130, 18, 50, 146, 19, 1934, 3789],
 },
 "Grand": {"GRAND TOTAL": [38240, 29725, 3890, 12218, 19830, 9357, 1102, 24354, 123020, 320434, 93838, 17039, 30079, 3728, 903082, 1629936]},
}
