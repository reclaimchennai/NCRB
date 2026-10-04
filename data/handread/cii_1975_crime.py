# CII 1975, Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads
# of Indian Penal Code during the year 1975, States / UTs / cities (raw/cii/1975/table_content/table-5-1975.pdf,
# pages 1-4). Read from the page images; only the incidence (I) columns are kept, the volume per lakh (V) columns
# skipped; '—' is entered as 0 (for Nagaland, Tripura, Mizoram and Kanpur the 'Others' column is '—' and the printed
# heads add up exactly to the printed total). This table prints an 'Others' column, so every row is checked against
# its printed total as well as every column against the printed section totals.
KIND, YEAR, PUB = "crime", 1975, "cii"
SOURCE = "raw/cii/1975/table_content/table-5-1975.pdf"
PAGES = "1-4"
TITLE = ("Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads "
         "of Indian Penal Code during the year 1975")
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary",
        "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Others",
        "Total cognizable crimes (IPC)"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [1122, 13, 101, 182, 156, 227, 6570, 16553, 2345, 679, 601, 205, 28351, 57105],
  "Assam": [465, 26, 172, 567, 286, 441, 7076, 10372, 3784, 534, 569, 7, 11778, 36077],
  "Bihar": [1886, 289, 304, 805, 2913, 1887, 19900, 31884, 12413, 1633, 949, 91, 24181, 99135],
  "Gujarat": [819, 14, 55, 392, 165, 711, 6680, 20591, 1149, 1280, 943, 8, 22065, 54872],
  "Haryana": [182, 100, 43, 122, 15, 27, 1626, 2619, 55, 462, 299, 1, 4045, 9596],
  "Himachal Pradesh": [54, 9, 17, 71, 3, 26, 610, 560, 140, 108, 80, 1, 1771, 3450],
  "Jammu & Kashmir": [95, 10, 70, 341, 13, 34, 1558, 2082, 873, 272, 185, 2, 4884, 10419],
  "Karnataka": [753, 5, 48, 181, 151, 261, 8983, 15183, 2794, 789, 938, 34, 19371, 49491],
  "Kerala": [398, 6, 59, 89, 31, 140, 4705, 5222, 3587, 501, 427, 100, 20757, 36022],
  "Madhya Pradesh": [1879, 22, 565, 973, 569, 1824, 26605, 44709, 3364, 1333, 1612, 57, 43699, 127211],
  "Maharashtra": [1576, 19, 283, 657, 487, 2721, 22409, 65936, 2197, 4066, 2503, 74, 39052, 141980],
  "Manipur": [45, 1, 7, 196, 30, 40, 330, 898, 193, 78, 136, 0, 1148, 3102],
  "Meghalaya": [46, 0, 9, 30, 16, 38, 246, 604, 80, 29, 41, 1, 479, 1619],
  "Nagaland": [37, 5, 1, 13, 15, 29, 227, 477, 40, 32, 34, 0, 0, 910],
  "Orissa": [444, 42, 58, 100, 235, 466, 7728, 13270, 1571, 551, 437, 28, 9581, 34511],
  "Punjab": [638, 169, 105, 296, 3, 48, 1553, 2807, 32, 485, 378, 2, 5844, 12360],
  "Rajasthan": [710, 35, 164, 1303, 141, 1237, 8852, 12897, 5841, 893, 1220, 2, 17689, 50984],
  "Sikkim": [8, 0, 1, 1, 1, 5, 39, 151, 4, 2, 9, 0, 115, 336],
  "Tamil Nadu": [907, 25, 50, 272, 21, 170, 7709, 27660, 3018, 935, 1155, 100, 32887, 74909],
  "Tripura": [36, 7, 3, 23, 76, 35, 655, 968, 159, 27, 36, 1, 0, 2026],
  "Uttar Pradesh": [4499, 1133, 760, 3242, 6117, 9868, 47315, 92088, 12360, 6495, 3139, 124, 43761, 230901],
  "West Bengal": [715, 422, 408, 745, 1032, 1086, 8001, 34642, 10925, 1465, 1255, 64, 25754, 86514],
  "TOTAL (STATES)": [17314, 2352, 3283, 10601, 12476, 21321, 189377, 402173, 66924, 22649, 16946, 902, 357212, 1123530],
 },
 "U.Ts.": {
  "A. & N. Islands": [10, 0, 2, 5, 0, 8, 74, 129, 15, 14, 9, 0, 275, 541],
  "Arunachal Pradesh": [10, 2, 7, 5, 2, 2, 37, 93, 5, 12, 4, 0, 139, 318],
  "Chandigarh": [7, 4, 3, 12, 0, 0, 86, 634, 8, 30, 47, 1, 370, 1202],
  "D. & N. Haveli": [7, 0, 0, 2, 0, 1, 29, 31, 5, 2, 2, 0, 74, 153],
  "Delhi": [165, 139, 55, 481, 18, 256, 2388, 16980, 147, 435, 656, 47, 6804, 28571],
  "Goa": [11, 3, 4, 11, 3, 38, 545, 739, 73, 51, 32, 1, 933, 2444],
  "Lakshadweep": [0, 0, 0, 0, 1, 0, 1, 10, 0, 1, 0, 0, 14, 27],
  "Mizoram": [28, 2, 19, 5, 6, 24, 49, 167, 0, 52, 10, 0, 0, 362],
  "Pondicherry": [11, 0, 3, 17, 0, 6, 268, 935, 64, 41, 66, 0, 1961, 3372],
  "TOTAL (U.TS.)": [249, 150, 93, 538, 30, 335, 3477, 19718, 317, 638, 826, 49, 10570, 36990],
 },
 "Grand": {
  "GRAND TOTAL": [17563, 2502, 3376, 11139, 12506, 21656, 192854, 421891, 67241, 23287, 17772, 951, 367782, 1160520],
 },
 "Cities": {
  "Ahmedabad": [50, 3, 9, 74, 2, 18, 523, 2145, 129, 109, 164, 6, 2393, 5625],
  "Bangalore": [34, 1, 4, 27, 2, 37, 1448, 5164, 33, 156, 379, 19, 2878, 10182],
  "Bombay": [165, 3, 41, 177, 27, 316, 2772, 18252, 228, 1097, 1024, 17, 9255, 33374],
  "Calcutta": [57, 7, 18, 131, 11, 66, 592, 5958, 694, 407, 374, 39, 3475, 11829],
  "Delhi": [149, 122, 50, 460, 15, 239, 2276, 16191, 124, 418, 648, 46, 6458, 27196],
  "Hyderabad": [25, 4, 6, 30, 0, 29, 922, 2850, 30, 110, 150, 31, 838, 5025],
  "Kanpur": [85, 15, 15, 140, 30, 260, 1784, 5232, 305, 506, 295, 2, 0, 8669],
  "Madras": [35, 1, 2, 36, 0, 49, 642, 9074, 130, 267, 617, 8, 6769, 17630],
  "TOTAL (CITIES)": [600, 156, 145, 1075, 87, 1014, 10959, 64866, 1673, 3070, 3651, 168, 32066, 119530],
 },
}
