# CII 1981, Chapter 1, Table 5: incidence of cognizable IPC crime by crime head, States / UTs / 12 cities
# (raw/cii/1981/table_chapter/chapter-1-1981.pdf, pages 7, 9, 13, 17, 21, printed pages 10, 12, 16, 20, 24 -- three
# heads per page, the pages between are charts). Read from the page images; the volume-per-lakh (V) columns are skipped.
# '..' / '...' (nil) is 0. Cities in printed order; city 9 is printed "Nagpur" on the burglary / thefts / riots page
# (a misprint for Pune: Nagpur is city 12 on the same page). Every row adds up to its printed Total cognizable crime
# and every column to the printed section totals (scripts/check_handread.py). Digits broken in the scan and settled by
# the row total, the column total and the printed volume: Gujarat murder 1,0?5 = 1025 (V 3.0), Madhya Pradesh dacoity
# 6?9 = 629 (V 1.2), Manipur others 1,?59 = 1559 (V 110.5), A & N Islands others 37? = 372.
KIND, YEAR, PUB = "crime", 1981, "cii"
SOURCE = "raw/cii/1981/table_chapter/chapter-1-1981.pdf"
PAGES = "7, 9, 13, 17, 21"
TITLE = "Table 5: Incidence of cognizable crime and volume per one lakh of population under important heads of Indian Penal Code during the year 1981 (States, Union Territories and Cities)"
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary", "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Others", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("West Bengal", "Others"): (28938, 28038, "printed 28,938 with volume 51.4 per lakh; 28038 fits the rate (pop. about 545 lakh; 28938 would be 53.1), the West Bengal row then adds up to its printed total 89207 and the States column to its printed 559872"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1342, 41, 192, 310, 392, 519, 7162, 18423, 4801, 581, 775, 23, 40733, 75294],
  "Assam": [608, 18, 281, 775, 394, 664, 5652, 11037, 5807, 501, 570, 4, 17486, 43797],
  "Bihar": [2461, 356, 516, 1205, 3448, 1933, 12587, 29705, 16868, 1491, 1232, 9, 35195, 107006],
  "Gujarat": [1025, 5, 92, 571, 282, 942, 6406, 20927, 3138, 1335, 694, 7, 43215, 78639],
  "Haryana": [371, 96, 80, 200, 38, 87, 2656, 4094, 243, 353, 343, 2, 8136, 16699],
  "Himachal Pradesh": [48, 14, 17, 79, 1, 22, 533, 614, 202, 78, 90, 1, 2498, 4197],
  "Jammu & Kashmir": [90, 7, 141, 475, 10, 22, 1347, 3184, 1822, 135, 160, 3, 8577, 15973],
  "Karnataka": [942, 28, 106, 323, 231, 723, 9559, 21514, 5686, 976, 1422, 167, 37928, 79605],
  "Kerala": [539, 13, 75, 144, 54, 172, 4568, 3953, 5657, 316, 498, 109, 31966, 48064],
  "Madhya Pradesh": [2417, 57, 1066, 975, 629, 2939, 25433, 52415, 6224, 1302, 1418, 26, 74218, 169119],
  "Maharashtra": [1811, 27, 516, 865, 676, 3660, 19803, 68377, 9120, 2851, 2419, 27, 62824, 172976],
  "Manipur": [123, 4, 14, 184, 53, 149, 218, 661, 168, 51, 85, 9, 1559, 3278],
  "Meghalaya": [82, 1, 13, 25, 29, 57, 249, 613, 160, 21, 44, 0, 828, 2122],
  "Nagaland": [28, 7, 7, 17, 9, 54, 286, 486, 37, 29, 32, 1, 0, 993],
  "Orissa": [541, 42, 124, 210, 416, 1091, 7691, 14611, 3313, 558, 342, 13, 18828, 47780],
  "Punjab": [555, 133, 88, 279, 1, 21, 1212, 2315, 119, 681, 335, 1, 7848, 13588],
  "Rajasthan": [882, 43, 298, 1674, 152, 1247, 6891, 14016, 10138, 1151, 1691, 0, 28869, 67052],
  "Sikkim": [8, 2, 7, 3, 0, 9, 33, 99, 3, 9, 7, 2, 113, 295],
  "Tamil Nadu": [1391, 10, 180, 711, 46, 294, 9959, 33135, 12406, 1252, 1169, 211, 57707, 118471],
  "Tripura": [93, 2, 19, 51, 160, 126, 853, 2393, 416, 24, 38, 3, 0, 4178],
  "Uttar Pradesh": [5693, 1606, 942, 2978, 6129, 6606, 26718, 63761, 10136, 4700, 2599, 311, 53306, 185485],
  "West Bengal": [1393, 508, 504, 954, 1411, 1337, 4763, 34587, 13190, 1439, 1041, 42, 28038, 89207],
  "TOTAL (STATES)": [22443, 3020, 5278, 13008, 14561, 22674, 154579, 400920, 109654, 19834, 17004, 971, 559872, 1343818],
 },
 "U.Ts.": {
  "A & N Islands": [6, 1, 1, 9, 0, 5, 79, 210, 43, 10, 1, 0, 372, 737],
  "Arunachal Pradesh": [17, 3, 9, 20, 5, 24, 94, 215, 17, 14, 11, 0, 412, 841],
  "Chandigarh": [9, 4, 3, 30, 0, 5, 87, 843, 21, 50, 70, 0, 561, 1683],
  "D & N Haveli": [2, 0, 0, 3, 1, 3, 25, 44, 4, 12, 5, 0, 93, 192],
  "Delhi": [199, 230, 79, 726, 47, 187, 1734, 17253, 165, 537, 589, 16, 8874, 30636],
  "Goa, Daman & Diu": [21, 7, 5, 19, 7, 59, 655, 1044, 243, 53, 43, 12, 1250, 3418],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 4, 3, 2, 1, 0, 0, 2, 12],
  "Mizoram": [19, 7, 29, 5, 4, 33, 46, 254, 5, 26, 20, 5, 1053, 1506],
  "Pondicherry": [11, 0, 5, 13, 1, 6, 237, 1273, 207, 42, 24, 0, 1095, 2914],
  "TOTAL (U.TS.)": [284, 252, 131, 825, 65, 322, 2961, 21139, 707, 745, 763, 33, 13712, 41939],
 },
 "Cities": {
  "Ahmedabad": [57, 1, 5, 115, 45, 46, 529, 2672, 891, 95, 88, 0, 5958, 10502],
  "Bangalore": [38, 2, 19, 63, 11, 344, 1710, 8021, 384, 256, 592, 93, 5589, 17122],
  "Bombay": [228, 3, 74, 190, 48, 443, 1872, 17073, 296, 843, 930, 9, 13254, 35263],
  "Calcutta": [100, 11, 24, 138, 63, 374, 908, 6513, 886, 347, 414, 28, 4145, 13951],
  "Delhi": [176, 207, 78, 690, 44, 174, 1645, 16787, 140, 521, 474, 16, 8389, 29341],
  "Hyderabad": [29, 13, 8, 51, 17, 50, 1164, 3272, 344, 57, 233, 5, 1627, 6870],
  "Kanpur": [204, 50, 45, 172, 250, 186, 812, 3309, 265, 312, 240, 37, 0, 5882],
  "Madras": [49, 5, 10, 82, 3, 50, 690, 7413, 359, 322, 395, 39, 6276, 15693],
  "Pune": [59, 3, 12, 45, 9, 83, 754, 2707, 184, 92, 135, 0, 3948, 8031],
  "Jaipur": [24, 7, 10, 116, 5, 87, 574, 2231, 632, 89, 171, 3, 1628, 5577],
  "Lucknow": [71, 25, 18, 110, 34, 121, 1137, 4936, 251, 307, 271, 0, 3010, 10291],
  "Nagpur": [56, 0, 26, 41, 12, 197, 616, 2505, 120, 88, 179, 6, 1904, 5750],
  "TOTAL (CITIES)": [1091, 327, 329, 1813, 541, 2155, 12411, 77439, 4752, 3329, 4122, 236, 55728, 164273],
 },
 "Grand": {"GRAND TOTAL": [22727, 3272, 5409, 13833, 14626, 22996, 157540, 422059, 110361, 20579, 17767, 1004, 573584, 1385757]},
}
