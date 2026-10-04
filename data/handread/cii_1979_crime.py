# CII 1979, Table 5: incidence of cognizable IPC crime by crime head, States / UTs / metropolitan cities
# (raw/cii/1979/table_content/table-5-1979.pdf, pages 1-5, printed pages 12-16). Read from the page images; the
# volume-per-lakh (V) columns are skipped. A dash, 'nil' or '..' is 0. Every row adds up to its printed Total cognizable
# crime and every column to the printed section totals (scripts/check_handread.py).
KIND, YEAR, PUB = "crime", 1979, "cii"
SOURCE = "raw/cii/1979/table_content/table-5-1979.pdf"
PAGES = "1-5"
TITLE = "Table 5: Incidence of cognizable crime and volume per one lakh of population under important heads of Indian Penal Code during the year 1979 (States, Union Territories and Cities)"
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary", "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Others", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Punjab", "Cheating"): (294, 394, "printed 294 (volume 1.9, computed from the misprint); with 394 the Punjab row adds up to its printed total 12128 and the States column to its printed 17140, and Table 6 of the same volume (table-6-1979.pdf p3) prints Punjab cheating 1979 = 394, -13.8% on 1978's 457"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1281, 23, 173, 284, 305, 380, 7724, 20120, 5426, 677, 666, 47, 39603, 76709],
  "Assam": [514, 35, 244, 594, 319, 532, 5554, 9872, 5300, 489, 483, 5, 16393, 40334],
  "Bihar": [2146, 281, 418, 1122, 2746, 1574, 14273, 29176, 16354, 1500, 1330, 16, 30210, 101146],
  "Gujarat": [885, 4, 64, 505, 134, 796, 6057, 19618, 1397, 1460, 829, 14, 30745, 62508],
  "Haryana": [318, 105, 78, 208, 24, 70, 2641, 4255, 230, 493, 266, 1, 7608, 16297],
  "Himachal Pradesh": [51, 14, 31, 110, 2, 40, 645, 784, 224, 140, 81, 0, 2679, 4801],
  "Jammu & Kashmir": [96, 13, 116, 438, 63, 31, 1496, 2536, 1677, 113, 133, 3, 7403, 14118],
  "Karnataka": [884, 9, 87, 272, 212, 677, 9723, 22042, 5427, 1000, 1334, 52, 34164, 75883],
  "Kerala": [447, 5, 53, 115, 46, 144, 3812, 3683, 5353, 324, 424, 109, 28897, 43412],
  "Madhya Pradesh": [2348, 50, 790, 970, 563, 2681, 26236, 51408, 5556, 1308, 1400, 37, 67440, 160787],
  "Maharashtra": [1571, 24, 371, 759, 511, 2928, 19418, 61572, 3707, 2987, 2393, 46, 58085, 154372],
  "Manipur": [94, 2, 10, 174, 52, 74, 262, 807, 165, 46, 131, 4, 1421, 3242],
  "Meghalaya": [92, 4, 12, 20, 32, 40, 285, 537, 328, 31, 28, 0, 871, 2280],
  "Nagaland": [18, 8, 4, 16, 6, 29, 277, 385, 22, 32, 37, 0, 0, 834],
  "Orissa": [461, 36, 115, 168, 265, 630, 7571, 12767, 2801, 553, 268, 10, 16950, 42595],
  "Punjab": [590, 156, 83, 306, 1, 28, 1252, 2345, 20, 474, 394, 3, 6476, 12128],
  "Rajasthan": [784, 38, 202, 1472, 111, 1294, 6531, 13646, 8533, 988, 1588, 3, 24687, 59877],
  "Sikkim": [13, 2, 6, 3, 1, 9, 53, 143, 15, 71, 2, 0, 0, 318],
  "Tamil Nadu": [953, 5, 98, 724, 47, 306, 10289, 34545, 8954, 1526, 1471, 28, 45799, 104745],
  "Tripura": [61, 11, 4, 24, 72, 121, 1286, 1540, 522, 40, 39, 0, 2046, 5766],
  "Uttar Pradesh": [5420, 1389, 708, 2924, 6970, 8563, 32837, 72088, 12663, 5522, 2717, 43, 54386, 206230],
  "West Bengal": [1046, 430, 500, 1046, 1466, 1162, 5946, 36585, 13328, 1329, 1126, 65, 28338, 92367],
  "TOTAL (STATES)": [20073, 2644, 4167, 12254, 13948, 22109, 164168, 400454, 98002, 21103, 17140, 486, 504201, 1280749],
 },
 "U.Ts.": {
  "A. & N. Islands": [13, 0, 2, 7, 0, 6, 73, 134, 40, 15, 1, 0, 412, 703],
  "Arunachal Pradesh": [16, 7, 6, 10, 4, 12, 74, 192, 14, 12, 2, 0, 266, 615],
  "Chandigarh": [8, 10, 1, 20, 1, 15, 177, 1484, 21, 42, 61, 1, 589, 2430],
  "D. & N. Haveli": [6, 0, 3, 1, 0, 5, 17, 40, 2, 17, 5, 0, 95, 191],
  "Delhi": [189, 340, 84, 793, 64, 616, 3331, 25755, 395, 674, 1065, 37, 10735, 44078],
  "Goa Daman & Diu": [9, 5, 3, 5, 4, 33, 382, 592, 112, 43, 40, 1, 980, 2209],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 4, 6],
  "Mizoram": [27, 2, 29, 7, 6, 57, 63, 213, 20, 30, 33, 0, 790, 1277],
  "Pondicherry": [8, 0, 5, 28, 1, 7, 288, 1618, 290, 80, 23, 0, 1562, 3910],
  "TOTAL (U.TS.)": [276, 364, 133, 871, 80, 751, 4406, 30029, 894, 913, 1230, 39, 15433, 55419],
 },
 "Cities": {
  "Ahmedabad": [57, 1, 5, 114, 13, 29, 473, 2591, 272, 152, 148, 8, 4154, 8017],
  "Bangalore": [48, 0, 16, 74, 44, 310, 2483, 9383, 447, 315, 661, 42, 8616, 22439],
  "Bombay": [187, 1, 58, 219, 41, 345, 2572, 17773, 273, 958, 1154, 27, 12840, 36448],
  "Calcutta": [93, 6, 23, 130, 48, 181, 620, 6278, 855, 329, 346, 35, 4160, 13104],
  "Delhi": [160, 301, 78, 743, 52, 571, 3060, 25535, 357, 658, 1044, 37, 8956, 41552],
  "Hyderabad": [45, 3, 14, 31, 14, 35, 1242, 4148, 868, 125, 195, 2, 1756, 8478],
  "Kanpur": [188, 48, 23, 68, 266, 302, 1468, 4155, 361, 502, 312, 18, 2835, 10546],
  "Madras": [34, 1, 9, 77, 7, 70, 900, 9762, 231, 416, 504, 0, 5277, 17288],
  "TOTAL (CITIES)": [812, 361, 226, 1456, 485, 1843, 12818, 79625, 3664, 3455, 4364, 169, 48594, 157872],
 },
 "Grand": {"GRAND TOTAL": [20349, 3008, 4300, 13125, 14028, 22860, 168574, 430483, 98896, 22016, 18370, 525, 519634, 1336168]},
}
