# CII 1974, Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads
# of Indian Penal Code during the year 1974, States / UTs / cities (raw/cii/1974/table_content/table-5-1974_0.pdf,
# pages 1-2). Read from the page images; only the incidence (I) columns are kept, the volume per lakh (V) columns
# skipped; '—' is entered as 0. The table prints selected heads and the total cognizable crime, with no 'other IPC
# crimes' column, so each column is checked against the printed totals (CHECK = "columns").
KIND, YEAR, PUB = "crime", 1974, "cii"
SOURCE = "raw/cii/1974/table_content/table-5-1974_0.pdf"
PAGES = "1-2"
TITLE = ("Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads "
         "of Indian Penal Code during the year 1974")
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary",
        "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [1163, 36, 73, 185, 176, 246, 6408, 16724, 2737, 534, 602, 130, 55601],
  "Assam": [498, 32, 106, 468, 374, 437, 7112, 11168, 3971, 555, 477, 3, 36238],
  "Bihar": [1946, 260, 252, 737, 2994, 1921, 21121, 31752, 14474, 1235, 760, 56, 101100],
  "Gujarat": [927, 5, 60, 387, 435, 692, 6577, 19439, 3572, 1109, 681, 16, 55829],
  "Haryana": [222, 98, 54, 126, 10, 32, 1797, 2862, 74, 321, 252, 1, 10194],
  "Himachal Pradesh": [60, 15, 16, 84, 10, 39, 567, 683, 177, 86, 90, 0, 3783],
  "Jammu & Kashmir": [86, 11, 48, 284, 9, 17, 1245, 1685, 879, 109, 108, 2, 8693],
  "Karnataka": [785, 4, 23, 177, 168, 222, 8621, 16156, 2842, 804, 1008, 73, 49023],
  "Kerala": [552, 2, 55, 79, 51, 162, 4417, 5724, 5216, 339, 336, 31, 43124],
  "Madhya Pradesh": [2002, 26, 515, 743, 487, 1644, 25485, 46999, 3758, 1282, 1475, 49, 127302],
  "Maharashtra": [1695, 34, 280, 590, 683, 2991, 23425, 69073, 3015, 3680, 2061, 59, 144432],
  "Manipur": [32, 1, 11, 187, 27, 39, 389, 879, 180, 82, 118, 1, 2820],
  "Meghalaya": [48, 0, 6, 15, 15, 32, 161, 713, 66, 41, 33, 0, 1566],
  "Nagaland": [54, 8, 13, 19, 21, 39, 276, 549, 52, 32, 25, 0, 1088],
  "Orissa": [453, 33, 40, 99, 277, 389, 6519, 11702, 2156, 598, 244, 20, 32207],
  "Punjab": [659, 159, 86, 272, 8, 51, 1685, 2903, 52, 350, 355, 2, 12878],
  "Rajasthan": [730, 43, 182, 1285, 164, 1301, 8920, 12597, 6748, 847, 990, 2, 51102],
  "Tamil Nadu": [1030, 13, 65, 275, 30, 141, 8212, 28304, 4464, 1147, 1000, 39, 79862],
  "Tripura": [44, 3, 7, 19, 49, 37, 678, 1233, 250, 31, 21, 1, 2373],
  "Uttar Pradesh": [4586, 1210, 682, 3164, 6392, 10207, 52509, 97079, 14528, 7000, 2827, 111, 244284],
  "West Bengal": [816, 395, 288, 729, 1270, 1204, 9761, 35422, 10790, 1367, 1067, 62, 86600],
  "TOTAL (STATES)": [18388, 2388, 2862, 9924, 13650, 21843, 195885, 413646, 80001, 21549, 14530, 658, 1150099],
 },
 "U.Ts.": {
  "A. & N. Islands": [4, 1, 6, 7, 0, 4, 58, 157, 26, 7, 13, 0, 538],
  "Arunachal Pradesh": [8, 1, 2, 4, 0, 1, 31, 62, 1, 5, 3, 0, 188],
  "Chandigarh": [10, 2, 6, 17, 0, 0, 115, 794, 15, 38, 57, 0, 1411],
  "D. & N. Haveli": [2, 0, 0, 1, 0, 5, 40, 31, 44, 5, 3, 0, 131],
  "Delhi": [174, 119, 64, 555, 32, 343, 2998, 20398, 280, 522, 697, 56, 33824],
  "Goa, Daman & Diu": [20, 1, 0, 4, 7, 28, 423, 629, 71, 56, 37, 2, 2112],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 10],
  "Mizoram": [35, 1, 13, 13, 7, 54, 60, 262, 3, 41, 12, 0, 501],
  "Pondicherry": [8, 1, 9, 18, 1, 8, 264, 935, 106, 51, 28, 1, 3463],
  "TOTAL (U.TS.)": [261, 126, 100, 619, 47, 443, 3993, 23272, 546, 725, 850, 60, 42178],
 },
 "Grand": {
  "GRAND TOTAL": [18649, 2514, 2962, 10543, 13697, 22286, 199878, 436918, 80547, 22274, 15380, 718, 1192277],
 },
 "Cities": {
  "Ahmedabad": [41, 1, 8, 80, 113, 35, 520, 2282, 1129, 83, 137, 11, 6588],
  "Bangalore": [26, 0, 3, 35, 2, 19, 1529, 5845, 61, 183, 448, 49, 10688],
  "Bombay": [184, 8, 50, 183, 32, 409, 2824, 18550, 512, 1191, 781, 33, 33992],
  "Calcutta": [69, 4, 18, 121, 12, 63, 671, 6087, 801, 406, 316, 30, 11874],
  "Delhi": [150, 102, 61, 538, 27, 329, 2846, 19638, 260, 504, 681, 55, 32307],
  "Hyderabad": [30, 3, 8, 41, 1, 29, 932, 2769, 69, 83, 136, 2, 4999],
  "Kanpur": [71, 29, 26, 83, 44, 256, 1533, 543, 311, 639, 265, 4, 9003],
  "Madras": [36, 0, 5, 27, 1, 25, 622, 8083, 316, 316, 531, 2, 17257],
  "TOTAL (CITIES)": [607, 147, 179, 1108, 232, 1165, 11477, 63797, 3459, 3405, 3295, 186, 126708],
 },
}
