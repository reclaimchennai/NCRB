# CII 1972, Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads
# of the Indian Penal Code during the year 1972, States / UTs / cities (raw/cii/1972/table_content/table-5-1972..pdf,
# pages 1-4). Read from the page images; only the 'cases reported' columns are kept (the volume per lakh columns are
# skipped). '..' in the table is entered as 0 (nil): the UTs and cities shown '..' under a head report other crime, and
# the columns add up to the printed totals with it as nil. The table prints selected heads and the total cognizable
# crime, with no 'other IPC crimes' column, so each column is checked against the printed totals (CHECK = "columns").
KIND, YEAR, PUB = "crime", 1972, "cii"
SOURCE = "raw/cii/1972/table_content/table-5-1972..pdf"
PAGES = "1-4"
TITLE = ("Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads "
         "of Indian Penal Code during the year 1972")
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping and abduction", "Dacoity", "Robbery", "Burglary",
        "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
    ("Madhya Pradesh", "Kidnapping and abduction"): (147, 741, "printed 147 (1.72 per lakh); 741 gives 1.72 on the State's population (murder 1,686 = 3.92 per lakh), and the States column then adds up to the printed 8,855"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1031, 15, 59, 147, 165, 225, 5746, 13671, 3054, 678, 401, 13, 49914],
  "Assam": [488, 45, 117, 451, 229, 254, 5038, 7947, 4390, 431, 276, 9, 30320],
  "Bihar": [1401, 236, 240, 580, 2142, 1447, 19082, 25539, 10053, 1321, 526, 52, 82744],
  "Gujarat": [705, 6, 57, 242, 77, 442, 4056, 11464, 624, 905, 515, 44, 36157],
  "Haryana": [175, 90, 59, 129, 9, 15, 1616, 2808, 93, 281, 149, 2, 9104],
  "Himachal Pradesh": [46, 15, 17, 58, 2, 27, 451, 587, 115, 118, 88, 0, 3073],
  "Jammu & Kashmir": [74, 6, 26, 195, 9, 11, 880, 1086, 586, 74, 50, 2, 6021],
  "Karnataka": [684, 6, 36, 119, 106, 144, 6660, 11196, 2576, 680, 714, 50, 37786],
  "Kerala": [448, 6, 38, 87, 34, 157, 4313, 4832, 5107, 371, 246, 93, 35442],
  "Madhya Pradesh": [1686, 26, 443, 741, 387, 1152, 18180, 34010, 2474, 989, 1212, 23, 95556],
  "Maharashtra": [1358, 33, 238, 556, 446, 1941, 15450, 46448, 2099, 3262, 1828, 108, 104782],
  "Manipur": [20, 2, 8, 164, 22, 20, 180, 415, 176, 56, 94, 0, 1920],
  "Meghalaya": [52, 0, 4, 22, 5, 13, 117, 342, 33, 13, 11, 1, 1105],
  "Nagaland": [26, 12, 10, 13, 17, 44, 130, 505, 31, 57, 54, 0, 1117],
  "Orissa": [442, 55, 52, 73, 113, 313, 6517, 13297, 1746, 602, 365, 8, 31983],
  "Punjab": [597, 161, 85, 288, 4, 34, 1590, 2700, 52, 433, 243, 6, 12111],
  "Rajasthan": [590, 46, 153, 1221, 160, 973, 6878, 9678, 4627, 707, 738, 8, 39204],
  "Tamil Nadu": [952, 21, 58, 224, 40, 111, 7266, 20285, 5183, 1016, 601, 102, 71050],
  "Tripura": [46, 2, 1, 24, 41, 56, 526, 1286, 250, 26, 125, 0, 2383],
  "Uttar Pradesh": [3701, 929, 577, 2752, 4909, 8148, 48459, 87061, 12398, 6587, 2533, 49, 217731],
  "West Bengal": [781, 387, 285, 769, 1461, 1127, 9897, 30900, 9488, 1619, 1065, 23, 77855],
  "TOTAL (STATES)": [15303, 2099, 2562, 8855, 10378, 16654, 163032, 326057, 65155, 20226, 11834, 593, 947358],
 },
 "U.Ts.": {
  "A. & N. Islands": [5, 0, 0, 1, 0, 2, 43, 59, 11, 14, 0, 0, 322],
  "Chandigarh": [7, 3, 4, 8, 0, 2, 113, 676, 4, 26, 29, 0, 1156],
  "D. & N. Haveli": [6, 0, 0, 4, 1, 2, 37, 42, 3, 4, 2, 0, 101],
  "Delhi": [132, 90, 33, 523, 27, 378, 3329, 18720, 447, 658, 737, 70, 32589],
  "Goa": [15, 3, 1, 6, 5, 14, 333, 364, 37, 38, 19, 5, 1321],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 18],
  "Pondicherry": [7, 1, 5, 5, 0, 2, 171, 460, 124, 38, 25, 2, 1908],
  "TOTAL (U.TS.)": [172, 97, 43, 547, 33, 400, 4030, 20325, 626, 778, 812, 77, 37415],
 },
 "Grand": {
  "GRAND TOTAL": [15475, 2196, 2605, 9402, 10411, 17054, 167062, 346382, 65781, 21004, 12646, 670, 984773],
 },
 "Cities": {
  "Ahmedabad": [35, 0, 7, 42, 3, 12, 315, 1000, 78, 76, 122, 22, 3212],
  "Bangalore": [26, 0, 4, 11, 0, 11, 1285, 4041, 70, 148, 297, 6, 7555],
  "Bombay": [160, 3, 29, 167, 23, 249, 1882, 13215, 214, 1052, 626, 86, 25970],
  "Calcutta": [51, 10, 15, 113, 20, 61, 853, 4726, 661, 459, 330, 3, 9793],
  "Delhi": [99, 71, 30, 467, 16, 341, 2807, 17812, 388, 631, 701, 70, 30054],
  "Hyderabad": [22, 2, 2, 30, 4, 23, 785, 2271, 43, 98, 133, 0, 4089],
  "Kanpur": [55, 15, 14, 149, 35, 210, 1387, 4487, 214, 719, 283, 2, 10104],
  "Madras": [29, 4, 9, 13, 3, 14, 472, 5019, 205, 380, 244, 24, 13015],
  "TOTAL (CITIES)": [477, 105, 110, 992, 104, 921, 9786, 52571, 1873, 3563, 2736, 213, 103792],
 },
}
