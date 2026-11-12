# CII 1994, Table 6: incidence of cognizable IPC crime by crime head, States / UTs
# (raw/cii/1994/table_content/table6-1994_2.pdf, pages 1-5, printed pages 55-59; each page carries States, UTs and the
# 23 cities, which are in cii_1994_crime_cities.py). Read from the page images; the rate (R) columns are skipped.
# Kidnapping & abduction is the printed total; its two printed sub-columns (of women & girls, of others) add up to it on
# every row and are left out so the heads add up to the Total. The printed 'TOTAL (ALL-INDIA)' row is GRAND TOTAL here.
# Every row adds up to its printed Total cognizable crimes under IPC and every State / UT column to the printed totals
# (scripts/check_handread.py), with no corrections. 'LAKSHAWDEEP' on printed page 58 is Lakshadweep.
KIND, YEAR, PUB = "crime", 1994, "cii"
SOURCE = "raw/cii/1994/table_content/table6-1994_2.pdf"
PAGES = "1-5"
TITLE = "Table 6: Incidence (I) & rate (R) of cognizable crimes (IPC) under different crime heads in States, UTs & cities during 1994"
CATS = ["Murder", "Attempt to commit murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Preparation & assembly for dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Other IPC crimes", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2419, 1302, 83, 873, 993, 529, 5, 979, 6954, 17396, 3354, 637, 2384, 252, 62629, 100789],
  "Arunachal Pradesh": [64, 32, 3, 28, 41, 45, 0, 52, 165, 317, 11, 31, 22, 6, 1056, 1873],
  "Assam": [1198, 367, 49, 530, 1140, 807, 24, 1054, 3275, 7325, 3876, 456, 509, 95, 14756, 35461],
  "Bihar": [5098, 4542, 630, 1130, 2419, 2677, 248, 3002, 7156, 18399, 13593, 1775, 1362, 74, 53517, 115622],
  "Goa": [38, 8, 2, 8, 16, 5, 0, 19, 488, 875, 163, 46, 57, 18, 1387, 3130],
  "Gujarat": [1340, 714, 6, 356, 1091, 318, 0, 1153, 6238, 20265, 2259, 2394, 3298, 160, 72660, 112252],
  "Haryana": [677, 370, 109, 258, 347, 48, 36, 257, 2749, 4333, 420, 332, 779, 41, 21836, 32592],
  "Himachal Pradesh": [104, 77, 16, 110, 208, 3, 0, 24, 1089, 1019, 696, 109, 196, 11, 7123, 10785],
  "Jammu & Kashmir": [758, 657, 8, 109, 339, 49, 0, 111, 1827, 2348, 647, 93, 172, 3, 7799, 14920],
  "Karnataka": [1552, 1094, 61, 281, 621, 377, 4, 1115, 9980, 19538, 9130, 600, 1905, 425, 66266, 112949],
  "Kerala": [509, 385, 33, 197, 180, 102, 19, 217, 4545, 3706, 7324, 325, 1415, 71, 64832, 83860],
  "Madhya Pradesh": [3331, 3188, 325, 2929, 1264, 265, 112, 2146, 19856, 31934, 3961, 873, 1527, 60, 116254, 188025],
  "Maharashtra": [2787, 1325, 136, 1304, 1171, 693, 84, 3180, 15900, 47668, 4422, 1844, 3179, 239, 97711, 181643],
  "Manipur": [241, 144, 7, 5, 115, 26, 0, 49, 94, 273, 58, 13, 92, 11, 1284, 2412],
  "Meghalaya": [119, 22, 6, 34, 26, 70, 1, 101, 195, 514, 44, 22, 30, 7, 774, 1965],
  "Mizoram": [35, 25, 0, 44, 7, 153, 0, 10, 212, 563, 2, 23, 53, 4, 588, 1719],
  "Nagaland": [137, 57, 4, 12, 40, 35, 0, 117, 221, 274, 9, 38, 50, 6, 499, 1499],
  "Orissa": [821, 1117, 94, 436, 455, 373, 0, 883, 4537, 8640, 1863, 402, 413, 27, 28228, 48289],
  "Punjab": [662, 390, 99, 108, 220, 10, 15, 46, 989, 1275, 7, 147, 532, 11, 6120, 10631],
  "Rajasthan": [1499, 1761, 124, 1002, 2531, 88, 8, 1137, 8327, 15517, 18741, 846, 5549, 287, 75602, 133019],
  "Sikkim": [6, 4, 0, 9, 14, 5, 0, 9, 123, 160, 55, 5, 7, 2, 428, 827],
  "Tamil Nadu": [1742, 1754, 44, 237, 576, 124, 0, 401, 6348, 19986, 7343, 650, 1178, 567, 78121, 119071],
  "Tripura": [284, 61, 1, 61, 114, 154, 0, 177, 408, 607, 283, 13, 19, 11, 1604, 3797],
  "Uttar Pradesh": [10776, 9541, 1371, 2078, 4798, 1740, 238, 6506, 16822, 43143, 9594, 3615, 3722, 284, 90475, 204703],
  "West Bengal": [1817, 560, 646, 743, 1128, 553, 138, 791, 945, 22068, 6147, 610, 1249, 67, 31480, 68942],
  "TOTAL (STATES)": [38014, 29497, 3857, 12882, 19854, 9249, 932, 23536, 119443, 288143, 94002, 15899, 29699, 2739, 903029, 1590775],
 },
 "U.Ts.": {
  "A & N Islands": [14, 4, 0, 4, 4, 0, 0, 1, 68, 61, 21, 8, 6, 0, 356, 547],
  "Chandigarh": [22, 15, 5, 6, 55, 0, 0, 8, 178, 967, 46, 27, 99, 0, 671, 2099],
  "D & N Haveli": [7, 3, 0, 2, 6, 1, 0, 4, 24, 61, 30, 5, 0, 0, 345, 488],
  "Daman & Diu": [3, 2, 0, 1, 1, 2, 0, 3, 37, 33, 24, 4, 4, 2, 107, 223],
  "Delhi": [492, 479, 84, 309, 1055, 19, 14, 377, 1660, 13490, 172, 578, 1383, 99, 18012, 38223],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 3, 20, 8, 1, 0, 0, 20, 52],
  "Pondicherry": [25, 20, 0, 4, 8, 0, 0, 4, 123, 789, 41, 1, 16, 11, 1802, 2844],
  "TOTAL (UTs)": [563, 523, 89, 326, 1129, 22, 14, 397, 2093, 15421, 342, 624, 1508, 112, 21313, 44476],
 },
 "Grand": {"GRAND TOTAL": [38577, 30020, 3946, 13208, 20983, 9271, 946, 23933, 121536, 303564, 94344, 16523, 31207, 2851, 924342, 1635251]},
}
