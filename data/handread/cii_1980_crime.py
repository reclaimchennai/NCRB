# CII 1980, Chapter 1, Table 5: incidence of cognizable IPC crime by crime head, States / UTs / metropolitan cities
# (raw/cii/1980/table_chapter/chapter-1-1980.pdf, pages 9, 13, 17, 21, 23 -- three heads per page, the pages between are
# charts). Read from the page images; the volume-per-lakh (V) columns are skipped. A dash is 0. Every row adds up to its
# printed Total cognizable crime and every column to the printed section totals (scripts/check_handread.py).
KIND, YEAR, PUB = "crime", 1980, "cii"
SOURCE = 'raw/cii/1980/table_chapter/chapter-1-1980.pdf'
PAGES = '9, 13, 17, 21, 23'
TITLE = 'Table 5: Incidence of cognizable crime and volume per one lakh of population under important heads of Indian Penal Code during the year 1980 (States, Union Territories and Metropolitan Cities)'
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary", "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Others", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Punjab", "C.H. not amounting to murder"): (137, 147, "printed 137; the Punjab row then adds up to its printed total 11679 and the States column to its printed 2739 (rate 0.9 fits both)"),
    ("Arunachal Pradesh", "Robbery"): (1, 13, "printed 1 with volume 2.1 per lakh; 13 fits the rate (pop. about 6.2 lakh), the row then adds up to its printed total 852 and the U.Ts. column to its printed 402"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1393, 30, 225, 335, 349, 459, 7150, 18467, 3868, 722, 837, 33, 35452, 69320],
  "Assam": [642, 57, 235, 565, 363, 522, 5467, 10895, 7124, 517, 492, 4, 16890, 43773],
  "Bihar": [2267, 272, 441, 1240, 2864, 1571, 12544, 29571, 16795, 1539, 1127, 23, 33971, 104225],
  "Gujarat": [993, 3, 109, 580, 165, 972, 6664, 21232, 1782, 1464, 808, 4, 26937, 61713],
  "Haryana": [363, 91, 99, 197, 35, 64, 2823, 4513, 229, 448, 322, 1, 7415, 16600],
  "Himachal Pradesh": [71, 15, 35, 100, 6, 38, 649, 752, 272, 84, 88, 0, 2754, 4864],
  "Jammu & Kashmir": [100, 7, 135, 473, 13, 22, 1684, 2875, 1709, 134, 136, 0, 7787, 15075],
  "Karnataka": [870, 19, 103, 286, 259, 655, 9868, 22051, 5692, 967, 1324, 330, 35019, 77443],
  "Kerala": [500, 0, 64, 134, 41, 174, 4540, 3925, 5676, 288, 475, 78, 31746, 47641],
  "Madhya Pradesh": [2392, 51, 899, 1188, 687, 3001, 27514, 55401, 5471, 1209, 1443, 19, 70476, 169751],
  "Maharashtra": [1643, 27, 418, 853, 689, 3222, 20126, 57462, 8202, 2905, 2251, 28, 69521, 167347],
  "Manipur": [86, 2, 17, 179, 89, 151, 274, 851, 213, 63, 83, 7, 1490, 3505],
  "Meghalaya": [87, 3, 21, 32, 24, 54, 179, 678, 165, 22, 34, 0, 904, 2203],
  "Nagaland": [21, 15, 7, 12, 14, 34, 291, 440, 27, 23, 35, 0, 0, 919],
  "Orissa": [502, 38, 132, 201, 391, 784, 8092, 15402, 3339, 582, 325, 9, 18284, 48081],
  "Punjab": [620, 147, 78, 256, 1, 21, 1207, 2299, 129, 466, 338, 3, 6114, 11679],
  "Rajasthan": [830, 37, 313, 1532, 116, 1216, 6736, 13807, 8510, 1053, 1462, 6, 25228, 60846],
  "Sikkim": [6, 0, 3, 2, 0, 1, 49, 92, 1, 11, 4, 0, 112, 281],
  "Tamil Nadu": [1289, 13, 151, 750, 82, 336, 10206, 34376, 10606, 1313, 1213, 97, 55678, 116110],
  "Tripura": [201, 1, 21, 52, 157, 143, 955, 1709, 499, 36, 44, 1, 2279, 6098],
  "Uttar Pradesh": [5680, 1385, 811, 2746, 7309, 8301, 30492, 71007, 11339, 4592, 2427, 101, 51941, 198131],
  "West Bengal": [1300, 526, 577, 1014, 1446, 1350, 5298, 36859, 14611, 1389, 1107, 61, 28080, 93618],
  "TOTAL (STATES)": [21856, 2739, 4894, 12727, 15100, 23091, 162808, 404664, 106259, 19827, 16375, 805, 528078, 1319223],
 },
 "U.Ts.": {
  "A & N Islands": [14, 0, 3, 7, 0, 7, 83, 176, 55, 13, 6, 0, 441, 805],
  "Arunachal Pradesh": [11, 4, 8, 12, 8, 13, 111, 222, 18, 13, 7, 0, 425, 852],
  "Chandigarh": [14, 7, 3, 21, 0, 14, 138, 1160, 17, 46, 63, 0, 635, 2118],
  "D. & N. Haveli": [7, 0, 1, 1, 1, 3, 39, 46, 6, 4, 3, 0, 66, 177],
  "Delhi": [182, 262, 56, 775, 75, 296, 2682, 22276, 201, 667, 872, 23, 9221, 37588],
  "Goa, Daman & Diu": [20, 7, 7, 10, 1, 35, 499, 888, 176, 55, 40, 1, 1188, 2927],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 5, 8, 1, 1, 0, 0, 0, 15],
  "Mizoram": [32, 13, 41, 8, 5, 28, 64, 181, 0, 20, 26, 0, 637, 1055],
  "Pondicherry": [13, 0, 10, 34, 4, 6, 266, 1415, 224, 38, 24, 1, 1734, 3769],
  "TOTAL (U.TS.)": [293, 293, 129, 868, 94, 402, 3887, 26372, 698, 857, 1041, 25, 14347, 49306],
 },
 "Cities": {
  "Ahmedabad": [62, 1, 13, 98, 26, 59, 475, 2585, 438, 124, 117, 4, 4676, 8678],
  "Bangalore": [58, 0, 19, 36, 13, 269, 1883, 8527, 290, 306, 540, 145, 6221, 18307],
  "Bombay": [217, 2, 49, 219, 56, 382, 2344, 17616, 233, 926, 1041, 20, 12590, 35695],
  "Calcutta": [117, 11, 17, 146, 62, 330, 829, 6659, 984, 332, 450, 41, 4003, 13981],
  "Delhi": [163, 224, 42, 730, 67, 274, 2528, 21339, 180, 646, 861, 23, 8571, 35648],
  "Hyderabad": [45, 2, 12, 34, 12, 68, 1214, 4127, 243, 95, 241, 4, 1315, 7412],
  "Kanpur": [197, 157, 34, 145, 299, 252, 1028, 3301, 248, 320, 269, 50, 0, 6300],
  "Madras": [52, 3, 16, 84, 2, 85, 859, 9018, 463, 353, 386, 1, 5957, 17279],
  "TOTAL (CITIES)": [911, 400, 202, 1492, 537, 1719, 11160, 73172, 3079, 3102, 3905, 288, 43333, 143300],
 },
 "Grand": {"GRAND TOTAL": [22149, 3032, 5023, 13595, 15194, 23493, 166695, 431036, 106957, 20684, 17416, 830, 542425, 1368529]},
}
