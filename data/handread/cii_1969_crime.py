# CII 1969, Table 5: incidence of crime under different heads during 1968 and 1969, States / U.Ts. / cities
# (raw/cii/1969/table_content/table-5-1969.pdf, pages 1-8 = printed pp. 10-17), 1969 columns only. Table 5 prints no total of
# cognizable crime, so the last column is the 1969 column of Table 4 of the same edition, incidence of total cognizable crime in
# States, U.Ts. and cities (raw/cii/1969/table_content/table-41969.pdf page 2, col. 9). "-" (nil) is entered as 0. No "other IPC
# crimes" column is printed, so each column is checked against the printed TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and TOTAL
# (cities) by scripts/check_handread.py. The figures corrected below were each confirmed in the head's appendix of the same edition
# (raw/cii/1969/table_chapter/appendix-1969.pdf: kidnapping cases page 6, ordinary thefts cases page 16, "cases reported during the year").
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts, Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime (Table 4)
KIND, YEAR, PUB = "crime", 1969, "cii"
SOURCE = "raw/cii/1969/table_content/table-5-1969.pdf"
PAGES = "1-8"
TITLE = "Table 5: Incidence of crime under different heads during 1968 and 1969 showing percentage variation (1969 figures); total from Table 4 (table-41969.pdf p. 2)"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Punjab", "Kidnapping & abduction"): (113, 313, 'printed 113 (-1.9% on 319 in 1968); 313 / 319 = -1.9%, Appendix (kidnapping cases, page 6) prints 313, and the States column then adds up to 7,847'),
    ("Tamil Nadu", "Kidnapping & abduction"): (1935, 335, 'printed 1,935 (-16.7% on 402 in 1968); 335 / 402 = -16.7%, Appendix (kidnapping cases, page 6) prints 335, and the States column then adds up to 7,847'),
    ("TOTAL (STATES)", "Kidnapping & abduction"): (7846, 7847, 'printed 7,846; the States add up to 7,847, 7,847 + U.Ts. 617 = the printed GRAND TOTAL 8,464, and the Appendix (page 6) prints 7847'),
    ("Maharashtra", "Ordinary thefts"): (44089, 40089, 'printed 44,089 (-10.2% on 44,654 in 1968); 40,089 / 44,654 = -10.2%, Appendix (ordinary thefts cases, page 16) prints 40,089, and the States column then adds up to the printed TOTAL 2,63,636'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1060, 99, 249, 189, 5455, 796, 10654, 3218, 606, 275, 37, 40153],
  "Assam": [472, 368, 199, 232, 3772, 570, 5752, 4192, 343, 240, 11, 24925],
  "Bihar": [1299, 498, 1333, 923, 18886, 637, 22669, 8384, 1317, 584, 80, 75333],
  "Gujarat": [862, 239, 106, 389, 4194, 683, 9948, 1356, 1150, 521, 12, 33129],
  "Haryana": [192, 154, 10, 12, 1666, 401, 2246, 101, 278, 209, 6, 8858],
  "Jammu & Kashmir": [80, 186, 24, 22, 1020, 163, 937, 725, 107, 99, 2, 6131],
  "Kerala": [403, 97, 26, 118, 3283, 170, 4270, 3089, 543, 155, 86, 28492],
  "Madhya Pradesh": [1739, 834, 347, 954, 18238, 4602, 28031, 2081, 1219, 1217, 41, 86946],
  "Maharashtra": [1319, 515, 305, 1411, 13711, 1552, 40089, 1767, 3317, 1824, 79, 92135],
  "Mysore": [731, 144, 78, 131, 6220, 745, 10466, 1563, 826, 731, 31, 35566],
  "Nagaland": [15, 16, 9, 25, 149, 4, 210, 13, 24, 13, 3, 685],
  "Orissa": [415, 136, 122, 264, 6503, 803, 11627, 2021, 631, 401, 16, 31395],
  "Punjab": [576, 313, 3, 18, 1699, 260, 2804, 29, 411, 256, 19, 12926],
  "Rajasthan": [669, 1105, 130, 859, 6997, 1910, 7287, 3050, 756, 702, 16, 34995],
  "Tamil Nadu": [814, 335, 58, 141, 7968, 1688, 20918, 2817, 1329, 1046, 217, 69114],
  "Uttar Pradesh": [3147, 1945, 2101, 3406, 31865, 6123, 55385, 7337, 5704, 1777, 34, 150712],
  "West Bengal": [709, 863, 876, 673, 10729, 857, 30343, 13137, 1713, 1203, 33, 82662],
  "TOTAL (STATES)": [14502, 7847, 5976, 9767, 142355, 21964, 263636, 54880, 20274, 11253, 723, 814157],
 },
 "U.Ts.": {
  "A. & N. Islands": [3, 4, 1, 3, 35, 0, 76, 12, 8, 0, 0, 338],
  "Chandigarh": [7, 23, 0, 1, 120, 10, 993, 3, 65, 36, 0, 1510],
  "Dadra & Nagar Haveli": [2, 1, 0, 4, 26, 1, 23, 0, 4, 3, 0, 106],
  "Delhi": [94, 305, 2, 44, 1353, 94, 9903, 93, 431, 487, 13, 17606],
  "Goa, Daman & Diu": [14, 9, 4, 19, 366, 1, 394, 17, 67, 19, 3, 1336],
  "Himachal Pradesh": [26, 63, 2, 22, 388, 25, 445, 47, 121, 56, 0, 2278],
  "Laccadives": [0, 0, 0, 0, 1, 0, 14, 1, 2, 0, 0, 38],
  "Manipur": [53, 181, 23, 43, 204, 35, 573, 240, 74, 100, 0, 2351],
  "Pondicherry": [4, 8, 0, 4, 132, 16, 513, 75, 45, 27, 0, 2008],
  "Tripura": [27, 23, 41, 15, 449, 208, 1216, 428, 27, 20, 0, 3439],
  "TOTAL (U.TS.)": [230, 617, 73, 155, 3074, 390, 14150, 916, 844, 748, 16, 31010],
 },
 "Cities": {
  "Ahmedabad": [150, 32, 36, 15, 239, 13, 867, 709, 95, 85, 3, 3578],
  "Bangalore": [20, 14, 5, 30, 1280, 54, 3887, 60, 261, 352, 6, 8051],
  "Bombay": [168, 170, 29, 206, 1898, 64, 13523, 577, 1093, 862, 32, 25289],
  "Calcutta": [68, 139, 14, 52, 746, 22, 5438, 799, 488, 429, 4, 10801],
  "Delhi": [75, 270, 1, 33, 1149, 73, 9467, 86, 408, 455, 13, 16254],
  "Hyderabad": [21, 11, 9, 22, 789, 5, 1886, 217, 40, 52, 0, 3593],
  "Kanpur": [42, 111, 14, 99, 753, 41, 3404, 116, 637, 211, 3, 6703],
  "Madras": [14, 60, 0, 4, 211, 52, 5271, 49, 423, 575, 84, 11707],
  "TOTAL (CITIES)": [558, 807, 108, 461, 7065, 324, 43743, 2613, 3445, 3021, 145, 85976],
 },
 "Grand": {"GRAND TOTAL": [14732, 8464, 6049, 9922, 145429, 22354, 277786, 55796, 21118, 12001, 739, 845167]},
}
