# CII 1978, Table 5: incidence of cognizable IPC crime by crime head, States / UTs / metropolitan cities
# (raw/cii/1978/table_content/table-5-1978.pdf, pages 1-5, printed pages 8-12). Read from the page images; the
# volume-per-lakh (V) columns are skipped. A dash is 0. Every row adds up to its printed Total cognizable crime and every
# column to the printed section totals (scripts/check_handread.py) once one figure is corrected (see CORRECTIONS). Names
# are as printed, in their usual spelling where a page misprints them ("Hyderbad" on printed page 8, "Goa, Dama & Diu"
# on pages 9 and 11). Tamil Nadu's printed volume of total crime, 263.2, is a transposition of 236.2 (its head volumes
# all use a population of about 457 lakh); the incidence figures are unaffected.
KIND, YEAR, PUB = "crime", 1978, "cii"
SOURCE = "raw/cii/1978/table_content/table-5-1978.pdf"
PAGES = "1-5"
TITLE = "Table 5: Incidence of cognizable crime and volume per one lakh of population under important heads of Indian Penal Code during the year 1978 (States, Union Territories and Cities)"
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary", "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Others", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Pondicherry", "Thefts"): (1899, 1889, "printed 189 with the last digit inked over by hand as 9 in the scanned copy; with 1889 the Pondicherry row adds up to its printed total 4345 and the U.Ts. column to its printed 29989 (and States + U.Ts. to the Grand Total 437187); the printed volume 373.3 is a transposition of 337.3 = 1889 / 5.60 lakh (1899 would give 339.1)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1138, 17, 157, 313, 283, 393, 7471, 18554, 4461, 639, 734, 34, 33898, 68092],
  "Assam": [495, 48, 223, 573, 252, 390, 6180, 9134, 4653, 451, 546, 2, 14193, 37140],
  "Bihar": [2002, 269, 422, 964, 2684, 1559, 15396, 30385, 15747, 1422, 983, 56, 28232, 100121],
  "Gujarat": [896, 6, 94, 542, 144, 813, 6472, 18887, 1317, 1485, 904, 8, 30168, 61736],
  "Haryana": [288, 82, 64, 192, 37, 71, 2782, 4477, 187, 378, 250, 1, 6696, 15505],
  "Himachal Pradesh": [48, 18, 23, 111, 1, 35, 630, 798, 219, 106, 81, 0, 2511, 4581],
  "Jammu & Kashmir": [83, 11, 117, 411, 20, 33, 1746, 2083, 1444, 150, 147, 0, 6198, 12443],
  "Karnataka": [784, 12, 73, 292, 227, 872, 10797, 23233, 5147, 1144, 1542, 67, 35946, 80136],
  "Kerala": [481, 2, 74, 97, 32, 128, 4200, 4204, 5926, 328, 493, 62, 32591, 48618],
  "Madhya Pradesh": [2193, 28, 858, 1100, 523, 2279, 27707, 52707, 5754, 1467, 1691, 37, 68125, 164469],
  "Maharashtra": [1536, 23, 358, 821, 564, 2850, 19168, 58700, 4576, 3143, 2466, 28, 56393, 150626],
  "Manipur": [48, 3, 5, 199, 28, 49, 299, 813, 186, 135, 128, 3, 1467, 3363],
  "Meghalaya": [62, 4, 9, 4, 14, 53, 232, 600, 141, 26, 37, 0, 712, 1894],
  "Nagaland": [32, 6, 6, 10, 12, 30, 314, 429, 43, 31, 44, 0, 0, 957],
  "Orissa": [458, 35, 94, 170, 277, 556, 7679, 12516, 2195, 539, 369, 13, 14688, 39589],
  "Punjab": [560, 145, 81, 299, 2, 25, 1552, 2672, 21, 518, 457, 7, 6492, 12831],
  "Rajasthan": [772, 47, 318, 1649, 127, 1521, 8384, 14275, 9031, 1105, 1643, 6, 24874, 63752],
  "Sikkim": [8, 5, 10, 3, 0, 6, 36, 129, 2, 15, 2, 1, 0, 217],
  "Tamil Nadu": [908, 25, 118, 683, 44, 243, 11073, 36897, 8852, 1873, 1899, 131, 45227, 107973],
  "Tripura": [34, 6, 13, 47, 72, 143, 569, 1791, 458, 35, 42, 0, 2145, 5355],
  "Uttar Pradesh": [5325, 1277, 812, 3223, 6431, 8881, 39147, 76248, 13101, 5897, 2818, 63, 54054, 217277],
  "West Bengal": [909, 378, 495, 1015, 1332, 1218, 7229, 37666, 12402, 1412, 1255, 92, 28193, 93596],
  "TOTAL (STATES)": [19060, 2447, 4424, 12718, 13106, 22148, 179063, 407198, 95863, 22299, 18531, 611, 492803, 1290271],
 },
 "U.Ts.": {
  "A. & N. Islands": [8, 2, 1, 8, 0, 12, 85, 167, 29, 17, 9, 0, 363, 701],
  "Arunachal Pradesh": [10, 4, 3, 6, 3, 12, 59, 146, 13, 11, 4, 0, 172, 443],
  "Chandigarh": [6, 6, 3, 24, 2, 7, 187, 1663, 6, 57, 62, 0, 586, 2609],
  "D. & N. Haveli": [6, 4, 0, 1, 0, 7, 28, 35, 11, 10, 2, 0, 116, 220],
  "Delhi": [182, 256, 79, 821, 69, 667, 3738, 25286, 305, 679, 1114, 22, 10189, 43407],
  "Goa, Daman & Diu": [10, 4, 4, 7, 4, 29, 441, 566, 119, 24, 31, 0, 942, 2181],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 8, 8, 4, 0, 0, 0, 0, 20],
  "Mizoram": [21, 4, 29, 7, 8, 39, 71, 229, 2, 62, 26, 0, 273, 771],
  "Pondicherry": [11, 1, 15, 24, 3, 2, 311, 1889, 136, 96, 42, 3, 1812, 4345],
  "TOTAL (U.TS.)": [254, 281, 134, 898, 89, 775, 4928, 29989, 625, 956, 1290, 25, 14453, 54697],
 },
 "Cities": {
  "Ahmedabad": [36, 2, 11, 137, 2, 32, 475, 2655, 193, 146, 209, 1, 4136, 8035],
  "Bangalore": [38, 1, 19, 94, 46, 474, 2764, 10554, 548, 451, 949, 52, 10073, 26063],
  "Bombay": [191, 0, 63, 240, 22, 314, 2525, 17638, 334, 1045, 1130, 11, 12647, 36160],
  "Calcutta": [97, 5, 22, 130, 52, 170, 671, 6400, 818, 323, 370, 58, 3923, 13039],
  "Delhi": [156, 224, 69, 768, 52, 629, 3450, 24295, 267, 663, 1092, 22, 9374, 41061],
  "Hyderabad": [42, 2, 11, 43, 7, 43, 1268, 4136, 179, 85, 175, 6, 1775, 7772],
  "Kanpur": [200, 39, 37, 230, 227, 390, 1674, 4488, 412, 530, 315, 23, 2830, 11395],
  "Madras": [40, 1, 9, 78, 1, 28, 839, 10597, 356, 548, 886, 61, 5645, 19089],
  "TOTAL (CITIES)": [800, 274, 241, 1720, 409, 2080, 13666, 80763, 3107, 3791, 5126, 234, 50403, 162614],
 },
 "Grand": {"GRAND TOTAL": [19314, 2728, 4558, 13616, 13195, 22923, 183991, 437187, 96488, 23255, 19821, 636, 507256, 1344968]},
}
