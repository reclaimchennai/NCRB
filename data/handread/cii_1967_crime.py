# CII 1967, Table IV: incidence of crime under different heads during 1966 and 1967, States / U.Ts. / cities
# (raw/cii/1967/table_content/table-4-1967.pdf, pages 1-6 = printed pp. 18-23). Read from the page images; the 1967 columns only
# (the 1966 figures and percentage variations are skipped). ".." (nil) is entered as 0. The table prints no "other IPC crimes"
# column, so the heads do not add up to the total and each column is checked against the printed TOTAL (States), TOTAL (U.Ts.),
# GRAND TOTAL and TOTAL (cities) by scripts/check_handread.py. The printed totals rows are all labelled "TOTAL".
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts, Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime cases 1967
KIND, YEAR, PUB = "crime", 1967, "cii"
SOURCE = "raw/cii/1967/table_content/table-4-1967.pdf"
PAGES = "1-6"
TITLE = "Table IV: Incidence of crime under different heads during 1966 and 1967 showing percentage variation (1967 figures)"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Gujarat", "Total cognizable crimes (IPC)"): (32606, 32604, 'printed 32,606; Appendix I of the same edition (appendix1967.pdf page 2, cases reported during the year) prints 32,604, and the States column then adds up to the printed TOTAL 8,52,132'),
    ("Uttar Pradesh", "Ordinary thefts"): (None, 66192, 'last digits smudged (66,19_); the States column adds up to the printed TOTAL 2,99,024 only with 66,192, and 66,192 / 53,932 = +22.7% as printed'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [980, 122, 86, 170, 5981, 1081, 11784, 2277, 734, 284, 114, 38303],
  "Assam": [434, 356, 134, 200, 3851, 541, 6221, 2113, 477, 327, 16, 22273],
  "Bihar": [1367, 482, 1752, 1080, 24725, 823, 27055, 8282, 1592, 818, 95, 86120],
  "Gujarat": [730, 256, 68, 477, 4790, 896, 11348, 495, 1010, 559, 68, 32604],
  "Haryana": [174, 140, 2, 19, 1581, 382, 2236, 66, 256, 290, 11, 8270],
  "Jammu & Kashmir": [85, 165, 31, 19, 925, 158, 938, 627, 118, 61, 1, 6142],
  "Kerala": [306, 79, 20, 93, 3020, 168, 3619, 1839, 410, 148, 80, 22210],
  "Madhya Pradesh": [1616, 772, 432, 1012, 24941, 5014, 36203, 1494, 1542, 1407, 116, 102849],
  "Maharashtra": [1202, 585, 389, 1638, 15339, 1857, 47259, 1427, 3294, 1940, 79, 98338],
  "Mysore": [680, 127, 89, 131, 7168, 954, 10898, 1080, 716, 404, 109, 32525],
  "Nagaland": [7, 12, 12, 28, 94, 10, 264, 4, 22, 9, 0, 514],
  "Orissa": [344, 109, 93, 253, 6920, 925, 11367, 1435, 806, 429, 27, 30709],
  "Punjab": [495, 316, 4, 25, 1855, 238, 3293, 48, 433, 342, 21, 13467],
  "Rajasthan": [575, 994, 128, 786, 7326, 2067, 7778, 2646, 807, 693, 37, 34497],
  "Tamil Nadu": [740, 417, 19, 122, 7869, 1998, 20925, 2461, 1838, 824, 477, 68164],
  "Uttar Pradesh": [2809, 1906, 2066, 3352, 41079, 7411, 66192, 7116, 6742, 2281, 62, 170698],
  "West Bengal": [641, 810, 830, 657, 12739, 1440, 31644, 8514, 2204, 1260, 61, 84449],
  "TOTAL (STATES)": [13185, 7648, 6155, 10062, 170203, 25963, 299024, 41924, 23001, 12076, 1374, 852132],
 },
 "U.Ts.": {
  "A. & N. Islands": [4, 0, 1, 3, 51, 2, 87, 1, 3, 5, 1, 340],
  "Chandigarh": [3, 15, 0, 0, 195, 8, 943, 4, 46, 27, 1, 1538],
  "Dadra & Nagar Haveli": [3, 0, 0, 2, 17, 2, 20, 1, 1, 1, 0, 66],
  "Delhi": [65, 260, 0, 41, 1422, 57, 10330, 95, 544, 377, 33, 17423],
  "Goa, Daman & Diu": [17, 8, 7, 20, 382, 8, 578, 40, 56, 32, 3, 1841],
  "Himachal Pradesh": [37, 70, 1, 18, 522, 28, 521, 9, 151, 50, 0, 2542],
  "Laccadives": [0, 0, 0, 0, 4, 0, 13, 2, 0, 0, 0, 21],
  "Manipur": [55, 165, 72, 43, 225, 99, 597, 170, 83, 95, 0, 2342],
  "Pondicherry": [5, 1, 0, 3, 133, 27, 458, 15, 34, 20, 1, 993],
  "Tripura": [24, 25, 64, 60, 421, 274, 822, 186, 31, 18, 0, 2743],
  "TOTAL (U.TS.)": [213, 544, 145, 190, 3372, 505, 14369, 523, 949, 625, 39, 29849],
 },
 "Cities": {
  "Ahmedabad": [23, 37, 3, 15, 307, 45, 1109, 27, 108, 101, 13, 2865],
  "Bangalore": [19, 13, 3, 19, 1087, 32, 3401, 27, 160, 147, 27, 5945],
  "Bombay": [164, 218, 24, 337, 2230, 91, 16529, 280, 1363, 942, 22, 28891],
  "Calcutta": [57, 127, 8, 30, 752, 56, 5928, 521, 550, 399, 8, 13185],
  "Delhi": [48, 241, 0, 38, 1271, 42, 9949, 88, 518, 361, 33, 16358],
  "Hyderabad": [25, 15, 1, 5, 648, 13, 1565, 46, 65, 79, 0, 2795],
  "Kanpur": [41, 89, 10, 109, 888, 57, 3749, 109, 686, 214, 14, 7093],
  "Madras": [23, 65, 0, 9, 321, 96, 5304, 64, 579, 331, 246, 11746],
  "TOTAL (CITIES)": [400, 805, 49, 562, 7504, 432, 47534, 1162, 4029, 2574, 363, 88878],
 },
 "Grand": {"GRAND TOTAL": [13398, 8192, 6300, 10252, 173575, 26468, 313393, 42447, 23950, 12701, 1413, 881981]},
}
