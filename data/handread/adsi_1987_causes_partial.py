# ADSI 1987, Appendix III: distribution of suicides by causes, by sex, States / UTs / cities
# (raw/adsi/1987/table_content/appendix-3.pdf, pages 1-4, printed sideways: pages 1-2 columns 3-12, Failure in
# examination to Love affairs; pages 3-4 columns 13-20, Insanity to Unemployment; Male and Female only). The file we
# hold STOPS AT COLUMN 20: the pages with the remaining causes (Bankruptcy, Death of dear person, Fall in social
# reputation, Dowry dispute, Illegitimate pregnancy, Causes not known, Other causes) and the Total are not in it. With
# no Total a row cannot be checked against anything, so this is KIND "causes_partial" with CHECK = "columns" (each
# column adds to the printed section totals; States + UTs = the printed Total (All India)); analysis code does not
# read this kind (a "causes" table's last column is taken as the place's number of suicides, which this has not).
# Read from the page images; "—" (nil) is 0.
#
# Three columns of page 1 are washed out in the scan and are NOT in CATS: they are kept in UNCHECKED_ROWS with None
# for the cells that cannot be read (their UT and city cells, on page 2, are clear):
#  - Failure in examination, Female (col. 4): the States add to 423 as read against the printed 430 (430 + UTs 15 =
#    All India 445, so 430 is right); the faint cells (Andhra Pradesh "18?", Gujarat "13/17/11", Kerala "23?",
#    Tripura "27?", West Bengal "130/139") admit several ways to make up the 7, so they are None.
#  - Quarrel with spouse, Female (col. 8): Arunachal Pradesh, Assam and Bihar cannot be read (together 27 = the
#    printed 1859 less the other States; 1859 + UTs 64 = All India 1923).
#  - Poverty, Male (col. 9): rows 1-13 are blank or a few specks; Tamil Nadu reads "186" or "156". Printed total 885.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes_partial", 1987, "adsi"
CHECK = "columns"
SOURCE = "raw/adsi/1987/table_content/appendix-3.pdf"
PAGES = "1-4"
TITLE = "Appendix III: Distribution of Suicides by Causes during 1987 (State, UT & City-wise; columns 3-20 only)"
CATS = ["Failure in examination, Male",
        "Quarrel with parents-in-law, Male", "Quarrel with parents-in-law, Female",
        "Quarrel with spouse, Male", "Poverty, Female", "Love affairs, Male", "Love affairs, Female",
        "Insanity, Male", "Insanity, Female", "Dispute over property, Male", "Dispute over property, Female",
        "Dreadful diseases, Male", "Dreadful diseases, Female", "Unemployment, Male", "Unemployment, Female"]
UNCHECKED_CATS = ["Failure in examination, Female", "Quarrel with spouse, Female", "Poverty, Male"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [46, 176, 139, 69, 39, 71, 58, 43, 28, 60, 26, 655, 479, 94, 39],
  "Arunachal Pradesh": [5, 0, 0, 2, 0, 1, 0, 2, 0, 2, 0, 2, 1, 0, 0],
  "Assam": [14, 38, 18, 14, 9, 80, 51, 31, 8, 45, 12, 56, 31, 9, 5],
  "Bihar": [15, 17, 43, 28, 9, 19, 19, 20, 9, 12, 4, 23, 12, 5, 1],
  "Goa": [0, 0, 1, 3, 1, 3, 8, 8, 10, 1, 0, 11, 4, 6, 1],
  "Gujarat": [28, 14, 115, 91, 16, 37, 30, 100, 96, 14, 3, 156, 138, 75, 1],
  "Haryana": [10, 5, 20, 55, 9, 8, 7, 11, 7, 24, 14, 83, 39, 18, 3],
  "Himachal Pradesh": [2, 1, 2, 2, 1, 1, 0, 4, 1, 2, 0, 11, 2, 1, 0],
  "Jammu & Kashmir": [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 4, 2, 0, 0],
  "Karnataka": [44, 73, 40, 33, 51, 76, 86, 120, 75, 21, 12, 551, 428, 61, 9],
  "Kerala": [16, 307, 130, 62, 2, 119, 84, 170, 85, 143, 29, 621, 229, 65, 4],
  "Madhya Pradesh": [48, 350, 455, 106, 14, 58, 63, 71, 41, 71, 21, 417, 218, 44, 7],
  "Maharashtra": [53, 168, 381, 199, 46, 83, 89, 139, 103, 85, 58, 391, 277, 59, 4],
  "Manipur": [0, 2, 0, 0, 4, 5, 2, 2, 0, 8, 0, 1, 0, 1, 0],
  "Meghalaya": [0, 0, 0, 2, 0, 1, 0, 6, 2, 0, 0, 6, 1, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Nagaland": [0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Orissa": [46, 158, 180, 112, 5, 79, 107, 44, 25, 9, 3, 142, 125, 14, 0],
  "Punjab": [2, 14, 7, 9, 3, 2, 4, 16, 6, 2, 0, 30, 14, 6, 0],
  "Rajasthan": [19, 53, 72, 64, 8, 11, 17, 69, 38, 19, 1, 123, 55, 5, 0],
  "Sikkim": [1, 0, 0, 2, 0, 0, 2, 1, 1, 0, 0, 2, 2, 0, 0],
  "Tamil Nadu": [69, 328, 236, 204, 79, 220, 191, 47, 27, 114, 35, 1059, 723, 131, 11],
  "Tripura": [14, 46, 30, 7, 0, 38, 53, 4, 10, 5, 2, 14, 17, 0, 0],
  "Uttar Pradesh": [13, 37, 77, 53, 12, 42, 26, 30, 18, 107, 25, 168, 71, 7, 3],
  "West Bengal": [115, 354, 586, 339, 81, 266, 423, 229, 167, 36, 22, 335, 224, 134, 30],
  "TOTAL (STATES)": [560, 2144, 2533, 1457, 389, 1222, 1320, 1167, 758, 780, 267, 4861, 3092, 735, 118],
 },
 "U.Ts.": {
  "A & N Islands": [0, 2, 6, 3, 0, 5, 2, 1, 0, 0, 0, 5, 1, 0, 0],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2, 0, 0],
  "D & N Haveli": [0, 0, 0, 9, 0, 0, 3, 7, 1, 0, 0, 3, 0, 0, 0],
  "Daman & Diu": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Delhi": [7, 8, 13, 11, 1, 10, 3, 7, 3, 0, 1, 25, 26, 10, 0],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [5, 6, 7, 51, 5, 5, 7, 5, 0, 1, 0, 58, 33, 11, 0],
  "TOTAL (U.TS.)": [12, 16, 26, 74, 6, 20, 15, 20, 4, 1, 1, 96, 62, 21, 0],
 },
 "Cities": {
  "Ahmedabad": [2, 2, 10, 2, 0, 1, 1, 9, 12, 1, 1, 16, 14, 3, 0],
  "Bangalore": [5, 0, 1, 3, 8, 7, 7, 9, 8, 0, 0, 24, 25, 18, 0],
  "Bombay": [3, 0, 20, 10, 9, 6, 19, 6, 7, 1, 0, 25, 19, 15, 1],
  "Calcutta": [0, 0, 34, 0, 1, 1, 4, 1, 0, 0, 0, 9, 10, 2, 0],
  "Delhi": [5, 7, 9, 5, 0, 9, 3, 4, 3, 0, 0, 24, 24, 5, 0],
  "Hyderabad": [2, 2, 5, 1, 0, 1, 2, 1, 2, 0, 0, 13, 5, 1, 2],
  "Jaipur": [5, 0, 9, 12, 0, 1, 6, 5, 0, 0, 0, 5, 2, 3, 0],
  "Kanpur": [1, 1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 4, 2, 0, 0],
  "Lucknow": [2, 5, 5, 2, 0, 3, 4, 1, 0, 1, 1, 2, 0, 0, 0],
  "Madras": [4, 33, 23, 8, 22, 30, 31, 8, 4, 2, 0, 77, 77, 20, 12],
  "Nagpur": [11, 0, 21, 9, 0, 7, 9, 5, 2, 3, 0, 2, 1, 0, 0],
  "Pune": [0, 2, 3, 4, 3, 1, 1, 0, 1, 1, 0, 8, 3, 4, 1],
  "TOTAL (CITIES)": [40, 52, 140, 56, 43, 67, 89, 49, 39, 10, 2, 209, 182, 71, 16],
 },
 "Grand": {"GRAND TOTAL": [572, 2160, 2559, 1531, 395, 1242, 1335, 1187, 762, 781, 268, 4957, 3154, 756, 118]},
}

UNCHECKED_ROWS = {
 "States": {
  "Andhra Pradesh": [None, 95, None],
  "Arunachal Pradesh": [0, None, None],
  "Assam": [13, None, None],
  "Bihar": [16, None, None],
  "Goa": [0, 11, None],
  "Gujarat": [None, 172, None],
  "Haryana": [4, 24, None],
  "Himachal Pradesh": [4, 8, None],
  "Jammu & Kashmir": [0, 0, None],
  "Karnataka": [22, 67, None],
  "Kerala": [None, 41, None],
  "Madhya Pradesh": [36, 154, None],
  "Maharashtra": [28, 346, None],
  "Manipur": [0, 1, 4],
  "Meghalaya": [0, 0, 0],
  "Mizoram": [0, 0, 0],
  "Nagaland": [0, 0, 0],
  "Orissa": [23, 150, 26],
  "Punjab": [0, 6, 17],
  "Rajasthan": [9, 63, 13],
  "Sikkim": [0, 2, 0],
  "Tamil Nadu": [51, 210, None],
  "Tripura": [None, 2, 0],
  "Uttar Pradesh": [6, 38, 88],
  "West Bengal": [None, 442, 73],
  "TOTAL (STATES)": [430, 1859, 885],
 },
 "U.Ts.": {
  "A & N Islands": [2, 6, 0],
  "Chandigarh": [0, 0, 0],
  "D & N Haveli": [0, 0, 0],
  "Daman & Diu": [0, 0, 0],
  "Delhi": [10, 18, 5],
  "Lakshadweep": [0, 0, 0],
  "Pondicherry": [3, 40, 13],
  "TOTAL (U.TS.)": [15, 64, 18],
 },
 "Cities": {
  "Ahmedabad": [1, 17, 0],
  "Bangalore": [2, 1, 7],
  "Bombay": [5, 36, 2],
  "Calcutta": [3, 0, 0],
  "Delhi": [10, 11, 3],
  "Hyderabad": [2, 1, 2],
  "Jaipur": [2, 2, 3],
  "Kanpur": [0, 0, 2],
  "Lucknow": [0, 2, 0],
  "Madras": [3, 23, 28],
  "Nagpur": [5, 19, 0],
  "Pune": [2, 5, 3],
  "TOTAL (CITIES)": [35, 117, 50],
 },
 "Grand": {"GRAND TOTAL": [445, 1923, 903]},
}
