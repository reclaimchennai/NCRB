# CII 1986, Table 5: incidence of cognizable IPC crime by crime head, States / UTs / 12 cities
# (raw/cii/1986/table_content/tabl5-1986.pdf, pages 1-4, printed pages 8-11). Read from the page images; the
# volume-per-lakh (V) columns are skipped. A dash is 0. This year's table prints an 'Other IPC offences' column, so
# every row adds to its Total, every column to the printed TOTAL (STATES), TOTAL (U.Ts.), TOTAL (CITIES), and States +
# UTs to the GRAND TOTAL (scripts/check_handread.py). Arunachal Pradesh and Mizoram are printed among the States.
# In the Thefts column the scan has lost part of one digit in many rows (a leading or middle digit of 14 States from
# Bihar to Punjab, of the TOTAL (STATES) and GRAND TOTAL and of most cities); each is read from what remains of the
# digit and is the figure that makes the row add to its printed Total and the column to its printed totals.
# No corrections.
KIND, YEAR, PUB = "crime", 1986, "cii"
SOURCE = "raw/cii/1986/table_content/tabl5-1986.pdf"
PAGES = "1-4"
TITLE = "Table 5: Incidence of cognizable crime and volume of crime per lakh of population under important heads of IPC during 1986 (States, U.Ts, Cities)"
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Other IPC offences", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1599, 21, 428, 558, 330, 575, 6676, 11838, 3157, 619, 1161, 109, 54251, 81322],
  "Arunachal Pradesh": [48, 2, 9, 11, 13, 29, 143, 253, 13, 19, 6, 0, 734, 1280],
  "Assam": [720, 37, 398, 898, 446, 575, 4236, 9150, 4531, 504, 584, 1, 16028, 38108],
  "Bihar": [3470, 613, 794, 1650, 2961, 2226, 9339, 18623, 16816, 1375, 1437, 49, 46548, 105901],
  "Gujarat": [1179, 17, 149, 557, 236, 826, 5646, 17913, 2277, 1458, 796, 63, 51884, 83001],
  "Haryana": [417, 110, 142, 182, 36, 70, 2133, 3524, 245, 283, 423, 10, 14222, 21797],
  "Himachal Pradesh": [59, 18, 52, 90, 2, 23, 719, 617, 302, 98, 99, 4, 3872, 5955],
  "Jammu & Kashmir": [87, 9, 187, 509, 15, 29, 1532, 3326, 1805, 231, 267, 0, 11858, 19855],
  "Karnataka": [1071, 23, 133, 329, 239, 475, 7206, 16857, 6019, 797, 1538, 302, 46551, 81540],
  "Kerala": [535, 36, 138, 149, 32, 149, 3856, 3054, 5131, 362, 1220, 224, 39025, 53911],
  "Madhya Pradesh": [2650, 40, 1506, 995, 294, 1781, 18249, 37178, 4540, 1485, 1657, 37, 100261, 170673],
  "Maharashtra": [2222, 109, 804, 1081, 606, 3425, 16575, 55558, 5189, 2693, 2710, 272, 90782, 182026],
  "Manipur": [70, 4, 10, 158, 38, 51, 212, 742, 118, 61, 103, 8, 1029, 2604],
  "Meghalaya": [98, 4, 19, 24, 23, 36, 125, 389, 79, 23, 29, 0, 745, 1594],
  "Mizoram": [37, 4, 46, 5, 2, 18, 112, 205, 2, 32, 22, 7, 514, 1006],
  "Nagaland": [50, 3, 10, 15, 25, 94, 277, 388, 36, 35, 49, 3, 574, 1559],
  "Orissa": [639, 59, 172, 269, 248, 684, 5213, 10191, 2223, 476, 297, 6, 24626, 45103],
  "Punjab": [1101, 159, 49, 172, 51, 361, 1363, 1939, 91, 252, 299, 1, 7386, 13224],
  "Rajasthan": [1112, 51, 598, 1738, 62, 1106, 6438, 12263, 13234, 1007, 2708, 36, 40765, 81118],
  "Sikkim": [4, 2, 5, 5, 1, 8, 44, 77, 9, 22, 14, 0, 182, 373],
  "Tamil Nadu": [1422, 22, 252, 686, 79, 444, 8899, 25205, 8810, 962, 1353, 296, 67846, 116276],
  "Tripura": [127, 1, 38, 57, 119, 135, 748, 896, 369, 31, 19, 0, 2174, 4714],
  "Uttar Pradesh": [6836, 2051, 1292, 3664, 3660, 8142, 24310, 50347, 10315, 4548, 3603, 80, 65970, 184818],
  "West Bengal": [1372, 585, 612, 965, 867, 848, 2013, 27702, 8059, 1010, 1017, 140, 23336, 68526],
  "TOTAL (STATES)": [26925, 3980, 7843, 14767, 10385, 22110, 126064, 308235, 93370, 18383, 21411, 1648, 711163, 1366284],
 },
 "U.Ts.": {
  "A & N Islands": [12, 2, 2, 3, 0, 1, 65, 117, 28, 12, 16, 0, 461, 719],
  "Chandigarh": [9, 0, 5, 18, 0, 8, 108, 725, 9, 28, 85, 2, 513, 1510],
  "D & N Haveli": [6, 0, 0, 4, 1, 6, 22, 54, 22, 8, 2, 0, 339, 464],
  "Delhi": [276, 204, 89, 857, 40, 203, 1884, 12543, 179, 521, 985, 22, 12025, 29828],
  "Goa, Daman & Diu": [27, 9, 8, 14, 16, 59, 645, 1217, 470, 49, 53, 11, 2072, 4650],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 3, 6, 2, 2, 0, 0, 7, 20],
  "Pondicherry": [14, 0, 5, 4, 2, 8, 155, 636, 117, 18, 27, 4, 1370, 2360],
  "TOTAL (U.TS.)": [344, 215, 109, 900, 59, 285, 2882, 15298, 827, 638, 1168, 39, 16787, 39551],
 },
 "Cities": {
  "Ahmedabad": [111, 4, 4, 103, 8, 69, 677, 2989, 390, 155, 175, 14, 5806, 10505],
  "Bangalore": [69, 3, 25, 84, 9, 211, 1120, 6467, 292, 209, 655, 185, 7263, 16592],
  "Bombay": [297, 0, 102, 230, 70, 741, 2444, 15821, 223, 892, 1131, 119, 14573, 36643],
  "Calcutta": [69, 14, 31, 141, 26, 242, 557, 7065, 582, 363, 474, 30, 4419, 14013],
  "Delhi": [227, 165, 72, 799, 30, 177, 1769, 11996, 154, 491, 966, 22, 10945, 27813],
  "Hyderabad": [50, 0, 23, 53, 12, 78, 1294, 3133, 310, 74, 289, 44, 2121, 7481],
  "Jaipur": [34, 3, 4, 88, 1, 21, 362, 1115, 732, 105, 229, 28, 2266, 4988],
  "Kanpur": [133, 37, 27, 187, 46, 204, 834, 2488, 279, 428, 325, 21, 2623, 7632],
  "Lucknow": [78, 22, 19, 111, 17, 96, 596, 2739, 199, 249, 319, 2, 367, 4814],
  "Madras": [64, 2, 16, 26, 3, 54, 438, 4462, 134, 213, 421, 125, 7508, 13466],
  "Nagpur": [76, 7, 63, 81, 13, 271, 737, 2868, 232, 95, 161, 18, 4210, 8832],
  "Pune": [65, 2, 27, 75, 12, 135, 887, 2534, 236, 124, 145, 14, 5166, 9422],
  "TOTAL (CITIES)": [1273, 259, 413, 1978, 247, 2299, 11715, 63677, 3763, 3398, 5290, 622, 67267, 162201],
 },
 "Grand": {"GRAND TOTAL": [27269, 4195, 7952, 15667, 10444, 22395, 128946, 323533, 94197, 19021, 22579, 1687, 727950, 1405835]},
}
