# CII 1968, Table IV: incidence of crime under different heads during 1967 and 1968, States / U.Ts. / cities
# (raw/cii/1968/table_content/table-IV-1968.pdf, pages 1-6 = printed pp. 22-27; page 7 is Table IV(a), disposal), 1968 columns only
# (the 1967 figures and percentage variations are skipped). Table IV prints no total of cognizable crime, so the last column is the
# 1968 column of Table III of the same edition, incidence of total cognizable crime in States, U.Ts. and cities
# (raw/cii/1968/table_content/table-III-1968.pdf page 2, col. 9). Table III prints no totals rows; the totals of that column are
# from the Appendix of the same edition, total cognizable crime, "cases reported during the year"
# (raw/cii/1968/table_chapter/1679313928APPENDIX-1968.pdf page 2 = printed p. 54, col. 5), where every State, U.T. and city figure
# is the same as in Table III. "-" (nil) is entered as 0. No "other IPC crimes" column is printed, so each column is checked
# against the printed TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and TOTAL (cities) by scripts/check_handread.py. The printed
# totals rows are all labelled "TOTAL". Every column adds up as printed; nothing was corrected.
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts, Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime (Table III)
KIND, YEAR, PUB = "crime", 1968, "cii"
SOURCE = "raw/cii/1968/table_content/table-IV-1968.pdf"
PAGES = "1-6"
TITLE = "Table IV: Incidence of crime under different heads during 1967 and 1968 showing percentage variation (1968 figures); total from Table III (table-III-1968.pdf p. 2)"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [974, 120, 151, 175, 5621, 1020, 11440, 2492, 649, 341, 67, 39778],
  "Assam": [433, 420, 440, 230, 3935, 592, 6456, 3126, 394, 301, 52, 24462],
  "Bihar": [1282, 571, 1580, 978, 21210, 642, 24580, 8048, 1409, 603, 127, 79899],
  "Gujarat": [697, 256, 63, 484, 4465, 762, 10298, 573, 1039, 566, 38, 32088],
  "Haryana": [207, 137, 1, 17, 1731, 426, 2355, 94, 292, 219, 4, 9108],
  "Jammu & Kashmir": [71, 166, 13, 19, 930, 192, 1019, 604, 127, 95, 3, 5992],
  "Kerala": [320, 72, 30, 144, 3733, 175, 4429, 2321, 443, 170, 193, 27411],
  "Madhya Pradesh": [1677, 857, 363, 991, 19331, 4806, 30700, 1801, 1463, 1259, 63, 93488],
  "Maharashtra": [1270, 593, 296, 1612, 15609, 1861, 44654, 1534, 3474, 1967, 78, 99105],
  "Mysore": [739, 113, 107, 170, 6884, 842, 11143, 1802, 882, 494, 75, 35441],
  "Nagaland": [8, 10, 10, 41, 124, 6, 228, 17, 45, 8, 2, 682],
  "Orissa": [431, 134, 111, 261, 7433, 1023, 12375, 1944, 782, 480, 36, 33537],
  "Punjab": [522, 319, 2, 24, 1728, 258, 2889, 47, 450, 291, 24, 13003],
  "Rajasthan": [621, 1326, 132, 893, 7680, 2144, 7855, 3132, 782, 795, 16, 37001],
  "Tamil Nadu": [793, 402, 35, 126, 7524, 1754, 20415, 3253, 1509, 779, 475, 70487],
  "Uttar Pradesh": [2928, 1979, 2023, 3209, 34138, 7428, 56914, 7114, 6101, 2060, 102, 154666],
  "West Bengal": [631, 832, 854, 658, 11029, 1148, 28553, 7220, 1739, 1430, 51, 76193],
  "TOTAL (STATES)": [13604, 8307, 6211, 10032, 153105, 25079, 276303, 45122, 21580, 11858, 1406, 832341],
 },
 "U.Ts.": {
  "A. & N. Islands": [7, 3, 0, 2, 44, 3, 79, 10, 6, 0, 0, 309],
  "Chandigarh": [4, 13, 0, 0, 159, 6, 822, 7, 60, 39, 0, 1390],
  "Dadra & Nagar Haveli": [2, 0, 2, 1, 22, 2, 15, 0, 3, 1, 0, 73],
  "Delhi": [86, 265, 6, 35, 1336, 60, 9644, 78, 444, 420, 11, 16937],
  "Goa, Daman & Diu": [16, 5, 3, 19, 330, 4, 411, 27, 65, 15, 3, 1320],
  "Himachal Pradesh": [36, 46, 1, 27, 376, 26, 432, 30, 120, 50, 0, 2305],
  "Laccadives": [0, 0, 0, 0, 5, 0, 24, 2, 2, 1, 0, 48],
  "Manipur": [55, 165, 72, 43, 225, 99, 597, 170, 83, 95, 0, 2342],
  "Pondicherry": [9, 4, 1, 0, 140, 34, 406, 29, 33, 37, 2, 1478],
  "Tripura": [30, 22, 88, 35, 464, 266, 1234, 326, 12, 8, 3, 3419],
  "TOTAL (U.TS.)": [245, 523, 173, 162, 3101, 500, 13664, 679, 828, 666, 19, 29621],
 },
 "Cities": {
  "Ahmedabad": [24, 36, 2, 9, 295, 20, 956, 39, 107, 84, 6, 2832],
  "Bangalore": [16, 16, 1, 23, 1202, 44, 4078, 100, 269, 204, 8, 7266],
  "Bombay": [148, 203, 20, 295, 2021, 67, 15022, 260, 1280, 968, 10, 27569],
  "Calcutta": [56, 134, 7, 41, 797, 31, 5787, 543, 508, 406, 7, 11864],
  "Delhi": [70, 237, 1, 27, 1210, 41, 9216, 69, 413, 406, 11, 15763],
  "Hyderabad": [27, 14, 1, 20, 745, 9, 1662, 116, 55, 75, 0, 3072],
  "Kanpur": [31, 115, 11, 102, 761, 49, 3301, 95, 632, 235, 4, 6638],
  "Madras": [29, 70, 2, 2, 265, 77, 5199, 94, 399, 281, 192, 11297],
  "TOTAL (CITIES)": [401, 825, 45, 519, 7296, 338, 45221, 1316, 3663, 2659, 238, 86301],
 },
 "Grand": {"GRAND TOTAL": [13849, 8830, 6384, 10194, 156206, 25579, 289967, 45801, 22408, 12524, 1425, 861962]},
}
