# ADSI 1970, Appendix VI: suicides by means adopted, States / UTs / cities
# (raw/adsi/1970/table_content/1680152202appendix-61970.pdf, pages 1-2, printed sideways: page 1 the States, page 2 the
# UTs, Grand Total and cities). This year's table has an "On Roads" column (col. 8) between poison and fire. Read from
# the page images; '..' (nil) is 0. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1970, "adsi"
SOURCE = "raw/adsi/1970/table_content/1680152202appendix-61970.pdf"
PAGES = "1-2"
TITLE = "Appendix VI: Statement of Suicides in States/U.Ts./and Cities during 1970 (By Means Adopted for Committing Suicides)"
CATS = ["By Railways", "By Machines", "By Fire Arms", "By Weapons", "By taking poison", "On Roads", "By Fire",
        "By Drowning", "By Hanging", "By Jumping", "By other ways", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [413, 93, 60, 7, 739, 111, 161, 1580, 455, 91, 548, 4258],
  "Assam": [89, 0, 3, 5, 19, 0, 18, 130, 717, 11, 27, 1019],
  "Bihar": [1106, 14, 15, 8, 63, 27, 77, 273, 186, 66, 432, 2267],
  "Gujarat": [97, 0, 4, 82, 331, 5, 241, 271, 114, 38, 191, 1374],
  "Haryana": [16, 18, 2, 0, 1, 4, 110, 72, 261, 60, 312, 856],
  "Himachal Pradesh": [0, 1, 3, 0, 9, 9, 4, 12, 23, 3, 44, 108],
  "Jammu & Kashmir": [0, 0, 0, 0, 0, 1, 0, 1, 2, 1, 0, 5],
  "Kerala": [67, 1, 1, 5, 1463, 14, 28, 427, 901, 53, 189, 3149],
  "Madhya Pradesh": [354, 21, 29, 92, 183, 157, 464, 1241, 637, 89, 560, 3827],
  "Maharashtra": [185, 5, 4, 13, 1282, 107, 617, 1287, 504, 314, 1412, 5730],
  "Manipur": [0, 0, 0, 0, 15, 0, 0, 14, 4, 0, 24, 57],
  "Mysore": [48, 5, 17, 23, 652, 18, 69, 1219, 515, 66, 517, 3149],
  "Nagaland": [0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 4],
  "Orissa": [206, 3, 5, 14, 810, 30, 44, 433, 485, 0, 490, 2520],
  "Punjab": [381, 8, 7, 4, 32, 21, 11, 77, 40, 10, 71, 662],
  "Rajasthan": [8, 1, 2, 0, 3, 3, 31, 139, 18, 3, 56, 264],
  "Tamil Nadu": [56, 1, 18, 16, 2505, 130, 124, 780, 739, 150, 680, 5199],
  "Tripura": [0, 0, 2, 0, 71, 0, 0, 0, 51, 0, 0, 124],
  "Uttar Pradesh": [792, 67, 307, 176, 305, 523, 577, 1146, 658, 222, 1565, 6338],
  "West Bengal": [196, 29, 25, 9, 3259, 175, 193, 498, 1498, 54, 1002, 6938],
  "TOTAL (STATES)": [4014, 267, 507, 455, 11742, 1335, 2769, 9600, 7808, 1231, 8120, 47848],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [0, 0, 0, 0, 8, 2, 1, 8, 18, 1, 21, 59],
  "Chandigarh": [0, 0, 1, 0, 0, 0, 2, 2, 0, 1, 0, 6],
  "Dadra & Nagar Haveli": [0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9],
  "Delhi": [35, 0, 2, 1, 7, 10, 18, 18, 25, 5, 63, 184],
  "Goa, Daman & Diu": [5, 0, 1, 1, 4, 6, 7, 24, 14, 4, 8, 74],
  "Laccadives": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  "Pondicherry": [1, 0, 0, 0, 76, 3, 2, 40, 67, 0, 58, 247],
  "TOTAL (U.TS.)": [41, 0, 5, 2, 95, 21, 30, 92, 133, 11, 150, 580],
 },
 "Cities": {
  "Ahmedabad": [2, 0, 0, 0, 20, 0, 35, 6, 5, 1, 3, 72],
  "Bangalore": [0, 0, 1, 1, 0, 44, 13, 38, 19, 36, 81, 233],
  "Bombay": [1, 0, 0, 3, 47, 0, 33, 8, 16, 14, 15, 137],
  "Calcutta": [1, 2, 2, 0, 16, 0, 3, 2, 44, 3, 0, 73],
  "Delhi": [35, 0, 2, 1, 7, 10, 14, 5, 14, 3, 63, 154],
  "Hyderabad": [0, 2, 2, 0, 68, 12, 66, 46, 11, 8, 49, 264],
  "Kanpur": [3, 1, 2, 0, 8, 1, 10, 0, 10, 2, 10, 47],
  "Madras": [0, 0, 4, 0, 149, 1, 37, 42, 69, 5, 53, 360],
  "TOTAL (CITIES)": [42, 5, 13, 5, 315, 68, 211, 147, 188, 72, 274, 1340],
 },
 "Grand": {"GRAND TOTAL": [4055, 267, 512, 457, 11837, 1356, 2799, 9692, 7941, 1242, 8270, 48428]},
}
