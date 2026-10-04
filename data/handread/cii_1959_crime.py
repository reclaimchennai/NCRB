# Crime in India 1959: cognizable crime cases reported during the year, by State, Union Territory and city, under each head.
# Heads: Appendices III, V, ... XXIII (the "-CASES" appendices; raw/cii/1959/year_wise/1689773004appendicesall2.pdf, the
# left-hand pages 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44), each printing States, Union Territories (with a Grand Total)
# and Cities (with their own Total); each column is that appendix's column 5, "Cases reported during the year". The 1959
# edition prints no single State x head table. The left-hand page of Appendix I (Total cognizable crime, cases) is not in
# the PDF we hold (the file opens with its right-hand half, columns 8-16), so the Total column is read from the survey
# chapter's State / UT / city table of total cognizable crime 1959 vs 1958 (raw/cii/1959/year_wise/1689773778SURVEYOFCRIME1.pdf,
# pages 2-3), which prints no section totals: TOTAL (STATES), TOTAL (U.TS.) and TOTAL (CITIES) are None in that column,
# and GRAND TOTAL is the 5,82,008 printed for 1959 in the chapter's "Crime under different heads" table (page 1). The
# States (566,942) and UTs (15,066) read add up to that Grand Total exactly. CHECK = "columns": the heads printed do not
# cover all IPC crime; every head is checked against the printed appendix totals. '..' (nil) is 0. Delhi is printed both
# as a Union Territory and as a city with the same figures.
KIND, YEAR, PUB = "crime", 1959, "cii"
SOURCE = "raw/cii/1959/year_wise/1689773004appendicesall2.pdf"
PAGES = "4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44 (Total: SURVEYOFCRIME1.pdf pages 1-3)"
TITLE = "Appendices III-XXIII (cases), with total cognizable crime from the survey chapter - cases reported during the year, by State / Union Territory / city, 1959"
CATS = ["Murder", "Kidnapping and abduction", "Dacoity", "Robbery", "House breaking", "Cattle theft", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
    ('TOTAL (CITIES)', 'Kidnapping and abduction'): (752, 757, "printed 752; the seven cities, each read clearly, add up to 757, and the Total row's own disposal needs 757: 163 pending investigation + 102 pending in court + 757 reported - 541 not investigated = 481 true cases, as printed (every city row satisfies the same identity)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [812, 184, 68, 165, 6263, 1539, 12451, 2217, 931, 471, 15, 34296],
  "Assam": [331, 329, 198, 183, 4638, 423, 5278, 1349, 406, 290, 27, 18853],
  "Bihar": [867, 446, 867, 651, 18285, 752, 17570, 4206, 913, 499, 77, 55777],
  "Bombay": [1925, 735, 468, 1876, 16776, 2502, 39743, 2237, 3383, 2097, 53, 99402],
  "Jammu & Kashmir": [62, 124, 59, 89, 912, 182, 568, 272, 104, 50, 7, 3757],
  "Kerala": [301, 49, 26, 104, 2437, 192, 3251, 1893, 226, 98, 9, 16599],
  "Madhya Pradesh": [1326, 740, 388, 845, 15585, 3336, 28077, 1612, 1346, 1102, 48, 71591],
  "Madras": [803, 542, 58, 326, 7362, 3112, 22519, 2205, 2064, 734, 38, 56032],
  "Mysore": [646, 236, 109, 190, 4588, 907, 8494, 862, 695, 336, 14, 24100],
  "Orissa": [302, 108, 90, 226, 4472, 611, 8110, 1121, 747, 346, 13, 20830],
  "Punjab": [595, 415, 6, 103, 3929, 625, 4698, 201, 445, 485, 17, 18881],
  "Rajasthan": [454, 568, 81, 383, 4594, 2027, 4228, 1134, 428, 364, 16, 19586],
  "Uttar Pradesh": [1694, 859, 849, 504, 15570, 3351, 22862, 2900, 2281, 1005, 43, 64272],
  "West Bengal": [448, 766, 412, 621, 10348, 687, 27709, 4412, 1511, 1362, 54, 62966],
  "TOTAL (STATES)": [10566, 6101, 3679, 6266, 115759, 20246, 205558, 26621, 15480, 9239, 431, None],
 },
 "U.Ts.": {
  "A. & N. Islands": [3, 4, 0, 1, 26, 1, 52, 4, 2, 2, 0, 168],
  "Delhi": [76, 207, 0, 36, 1209, 46, 5558, 81, 300, 338, 12, 9899],
  "Himachal Pradesh": [20, 36, 3, 22, 241, 28, 224, 41, 43, 25, 0, 1068],
  "Manipur": [15, 77, 46, 5, 148, 56, 357, 52, 21, 49, 0, 1122],
  "Tripura": [25, 30, 39, 34, 783, 195, 661, 181, 21, 11, 0, 2611],
  "Naga Hills & Tuensang Area": [7, 4, 7, 3, 39, 5, 65, 7, 11, 13, 0, 198],
  "TOTAL (U.TS.)": [146, 358, 95, 101, 2446, 331, 6917, 366, 398, 438, 12, None],
 },
 "Grand": {
  "GRAND TOTAL": [10712, 6459, 3774, 6367, 118205, 20577, 212475, 26987, 15878, 9677, 443, 582008],
 },
 "Cities": {
  "Bangalore": [12, 86, 0, 11, 612, 48, 2082, 12, 158, 127, 7, 3907],
  "Bombay": [130, 163, 13, 127, 1438, 38, 9126, 99, 1086, 829, 5, 16177],
  "Calcutta": [34, 177, 2, 30, 1109, 51, 7234, 383, 534, 439, 13, 11893],
  "Delhi": [76, 207, 0, 36, 1209, 46, 5558, 81, 300, 338, 12, 9899],
  "Hyderabad": [12, 44, 1, 13, 610, 39, 2029, 49, 203, 163, 3, 3817],
  "Kanpur": [21, 43, 4, 12, 278, 9, 1127, 38, 178, 85, 5, 2110],
  "Madras": [18, 37, 0, 15, 154, 45, 4045, 26, 411, 221, 2, 6010],
  "TOTAL (CITIES)": [303, 757, 20, 244, 5410, 276, 31201, 688, 2870, 2202, 47, None],
 },
}
