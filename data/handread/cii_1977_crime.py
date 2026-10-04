# CII 1977, Table 5: incidence of cognizable IPC crime by crime head, States / UTs / metropolitan cities
# (raw/cii/1977/table_content/table-5-1977.pdf, pages 1-5, printed pages 23-27). Read from the page images; the
# volume-per-lakh (V) columns are skipped. A dash is 0. Every row adds up to its printed Total cognizable crime and every
# column to the printed section totals (scripts/check_handread.py). Three Robbery figures on page 2 are circled and
# overwritten by hand in the scanned copy; the handwritten figures are the ones that add up (see CORRECTIONS).
KIND, YEAR, PUB = "crime", 1977, "cii"
SOURCE = "raw/cii/1977/table_content/table-5-1977.pdf"
PAGES = "1-5"
TITLE = "Table 5: Incidence of cognizable crime and volume per one lakh of population under important heads of Indian Penal Code during the year 1977 (States, Union Territories and Cities)"
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary", "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Others", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Karnataka", "Robbery"): (None, 565, "printed figure circled and overwritten by hand with 565 in the scan (printed digits not legible, looks like 665); 565 fits the volume 1.7 per lakh, the row then adds up to its printed total 69315 and the States column to its printed 22297"),
    ("Meghalaya", "Robbery"): (None, 55, "printed figure circled and overwritten by hand with 55 in the scan (printed digits not legible); 55 fits the volume 4.6 per lakh, the row then adds up to its printed total 1705 and the States column to 22297"),
    ("Arunachal Pradesh", "Robbery"): (None, 5, "printed figure circled and overwritten by hand with 5 in the scan (printed digit not legible); 5 fits the volume 0.9 per lakh, the row then adds up to its printed total 476 and the U.Ts. column to its printed 428"),
    ("TOTAL (U.TS.)", "Cheating"): (10.42, 1042, "printed '10.42'; the CII 1977 errata (raw/cii/1977/year_wise/1654002114_ERRATA1.pdf, page 26 Table 5 col. 23) corrects it to 1042, which the U.Ts. figures add up to"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1268, 16, 115, 230, 245, 373, 7569, 16991, 3960, 625, 701, 112, 34647, 66852],
  "Assam": [414, 28, 209, 598, 260, 397, 7079, 9867, 3783, 467, 428, 2, 12518, 36050],
  "Bihar": [1963, 279, 345, 887, 2675, 1439, 17670, 29939, 12349, 1425, 1033, 10, 26883, 96897],
  "Gujarat": [847, 22, 82, 500, 115, 837, 6822, 20613, 1249, 1326, 936, 5, 26561, 59915],
  "Haryana": [231, 94, 70, 194, 21, 48, 2453, 3954, 112, 431, 251, 1, 5179, 13039],
  "Himachal Pradesh": [63, 13, 29, 91, 6, 44, 621, 790, 207, 89, 158, 2, 2440, 4553],
  "Jammu & Kashmir": [99, 5, 73, 377, 12, 32, 2393, 2532, 1792, 128, 176, 0, 6910, 14529],
  "Karnataka": [816, 14, 62, 260, 164, 565, 11162, 21497, 3806, 1045, 1528, 120, 28276, 69315],
  "Kerala": [461, 2, 50, 94, 20, 125, 4354, 4093, 5006, 443, 407, 59, 26148, 41262],
  "Madhya Pradesh": [1923, 25, 766, 960, 401, 2019, 28414, 48921, 4093, 1406, 1849, 32, 57316, 148125],
  "Maharashtra": [1526, 25, 358, 607, 518, 2656, 20109, 61890, 2734, 3421, 2660, 141, 48441, 145086],
  "Manipur": [47, 6, 6, 184, 14, 56, 298, 840, 181, 89, 164, 1, 1372, 3258],
  "Meghalaya": [57, 3, 7, 18, 16, 55, 206, 567, 98, 23, 32, 0, 623, 1705],
  "Nagaland": [17, 3, 6, 9, 6, 42, 308, 374, 38, 27, 14, 0, 0, 844],
  "Orissa": [401, 57, 68, 133, 189, 434, 7265, 12356, 1688, 460, 360, 26, 11979, 35416],
  "Punjab": [624, 143, 94, 320, 6, 61, 1937, 3007, 37, 428, 470, 2, 6865, 13994],
  "Rajasthan": [683, 55, 219, 1491, 141, 1638, 8292, 14877, 7930, 1065, 1583, 0, 24270, 62244],
  "Sikkim": [4, 0, 2, 5, 1, 1, 40, 125, 1, 9, 5, 0, 0, 193],
  "Tamil Nadu": [835, 14, 101, 493, 35, 162, 10975, 33214, 6509, 1617, 1596, 96, 34749, 90396],
  "Tripura": [44, 12, 14, 27, 46, 122, 929, 936, 309, 29, 41, 0, 1311, 3820],
  "Uttar Pradesh": [4962, 1258, 736, 3127, 6518, 10006, 42701, 82699, 12497, 6075, 2766, 66, 49210, 222621],
  "West Bengal": [818, 355, 531, 969, 1153, 1185, 8147, 36011, 11702, 1482, 1423, 68, 27606, 91450],
  "TOTAL (STATES)": [18103, 2429, 3943, 11574, 12562, 22297, 189744, 406093, 80081, 22110, 18581, 743, 433304, 1221564],
 },
 "U.Ts.": {
  "A. & N. Islands": [8, 1, 0, 4, 1, 5, 86, 131, 33, 9, 9, 0, 305, 592],
  "Arunachal Pradesh": [13, 1, 3, 3, 4, 5, 51, 139, 7, 10, 7, 0, 233, 476],
  "Chandigarh": [12, 2, 3, 16, 1, 6, 185, 1712, 8, 46, 59, 0, 445, 2495],
  "D. & N. Haveli": [5, 1, 0, 3, 3, 6, 16, 31, 19, 9, 9, 0, 7, 109],
  "Delhi": [185, 173, 71, 610, 20, 357, 2894, 21699, 148, 548, 867, 38, 8246, 35856],
  "Goa, Daman & Diu": [16, 2, 1, 3, 1, 18, 361, 534, 76, 30, 34, 1, 813, 1890],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 5, 7, 2, 1, 0, 0, 0, 15],
  "Mizoram": [22, 6, 31, 6, 5, 28, 46, 265, 7, 49, 16, 0, 256, 737],
  "Pondicherry": [12, 0, 6, 21, 2, 3, 234, 1435, 68, 56, 41, 2, 1390, 3270],
  "TOTAL (U.TS.)": [273, 186, 115, 666, 37, 428, 3878, 25953, 368, 758, 1042, 41, 11695, 45440],
 },
 "Cities": {
  "Ahmedabad": [43, 15, 9, 98, 2, 28, 547, 2577, 127, 146, 153, 0, 3578, 7323],
  "Bangalore": [37, 1, 12, 73, 15, 277, 2607, 9639, 451, 345, 861, 36, 6397, 20751],
  "Bombay": [194, 1, 63, 189, 30, 343, 2461, 18967, 253, 1175, 1234, 101, 11855, 36866],
  "Calcutta": [64, 10, 19, 126, 31, 104, 710, 6278, 731, 360, 421, 47, 3676, 12577],
  "Delhi": [151, 148, 63, 565, 15, 338, 2711, 20525, 119, 536, 826, 37, 7831, 33865],
  "Hyderabad": [43, 3, 2, 27, 6, 20, 990, 3272, 21, 77, 172, 17, 1305, 5955],
  "Kanpur": [73, 15, 16, 148, 26, 178, 1162, 4649, 224, 523, 353, 16, 369, 7752],
  "Madras": [22, 5, 11, 100, 0, 32, 1021, 9774, 381, 493, 696, 17, 5695, 18247],
  "TOTAL (CITIES)": [627, 198, 195, 1326, 125, 1320, 12209, 75681, 2307, 3655, 4716, 271, 40706, 143336],
 },
 "Grand": {"GRAND TOTAL": [18376, 2615, 4058, 12240, 12599, 22725, 193622, 432046, 80449, 22868, 19623, 784, 444999, 1267004]},
}
