# ADSI 1990, Appendix IV: suicides by means adopted and sex, States / UTs / cities
# (raw/adsi/1990/table_content/1680164328appendix-41990.pdf, pages 1-5: each page carries three categories by Male /
# Female / Total for every place, page 5 the Grand Total). Only the Total column of each category is recorded; every
# printed Male + Female equals its Total, and the Male and Female columns add up across categories and down the
# sections as well. The All-India row is printed "Total (All - India)". The cities carry no totals row. Read from the
# page images. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1990, "adsi"
SOURCE = "raw/adsi/1990/table_content/1680164328appendix-41990.pdf"
PAGES = "1-5"
TITLE = "Appendix IV: Distribution of Suicides by Means Adopted and Sex during 1990 (State, UT & City-wise)"
CATS = ["By Railways", "By Machine", "By Firearm", "By Weapon", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wire", "By Other Means", "Total"]
NA = None
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [327, 19, 14, 26, 2114, 596, 1003, 829, 78, 12, 25, 623, 5666],
  "Arunachal Pradesh": [0, 0, 0, 0, 2, 0, 6, 26, 1, 0, 2, 3, 40],
  "Assam": [67, 0, 14, 2, 245, 140, 65, 1140, 10, 1, 26, 613, 2323],
  "Bihar": [25, 5, 17, 21, 241, 250, 210, 366, 13, 9, 72, 199, 1428],
  "Goa": [0, 0, 1, 0, 27, 33, 50, 52, 10, 1, 0, 47, 221],
  "Gujarat": [97, 3, 4, 5, 869, 583, 338, 486, 49, 12, 10, 232, 2688],
  "Haryana": [269, 12, 8, 7, 369, 158, 125, 155, 14, 6, 31, 221, 1375],
  "Himachal Pradesh": [3, 1, 2, 0, 48, 9, 19, 25, 2, 0, 3, 22, 134],
  "Jammu & Kashmir": [7, 0, 4, 1, 11, 26, 5, 5, 4, 0, 0, 0, 63],
  "Karnataka": [155, 44, 10, 33, 2735, 458, 1722, 1966, 145, 28, 73, 671, 8040],
  "Kerala": [351, 0, 8, 18, 3144, 198, 733, 3220, 25, 10, 8, 130, 7845],
  "Madhya Pradesh": [313, 25, 58, 57, 1485, 588, 543, 1393, 64, 60, 54, 969, 5609],
  "Maharashtra": [196, 39, 7, 20, 2236, 1456, 1336, 1222, 131, 6, 12, 1112, 7773],
  "Manipur": [0, 0, 2, 0, 1, 1, 13, 22, 1, 2, 1, 16, 59],
  "Meghalaya": [0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 30],
  "Mizoram": [0, 0, 0, 0, 0, 10, 3, 0, 0, 0, 0, 9, 22],
  "Nagaland": [1, 1, 2, 0, 0, 1, 6, 13, 0, 0, 1, 10, 35],
  "Orissa": [191, 1, 1, 5, 984, 29, 195, 979, 8, 1, 45, 472, 2911],
  "Punjab": [214, 0, 7, 1, 37, 32, 18, 68, 2, 1, 2, 5, 387],
  "Rajasthan": [133, 8, 15, 9, 252, 224, 430, 294, 11, 8, 5, 222, 1611],
  "Sikkim": [0, 0, 0, 0, 2, 1, 0, 35, 0, 0, 0, 0, 38],
  "Tamil Nadu": [208, 1, 11, 2, 3658, 959, 828, 1343, 73, 38, 37, 1474, 8632],
  "Tripura": [0, 1, 2, 0, 195, 30, 0, 271, 0, 0, 0, 117, 616],
  "Uttar Pradesh": [303, 58, 223, 151, 482, 215, 138, 474, 53, 12, 47, 971, 3127],
  "West Bengal": [256, 32, 117, 73, 5140, 673, 489, 2941, 17, 43, 40, 1904, 11725],
  "TOTAL (STATES)": [3116, 250, 527, 431, 24277, 6670, 8275, 17355, 711, 250, 494, 10042, 72398],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 34, 0, 4, 76, 0, 0, 0, 0, 114],
  "Chandigarh": [0, 0, 0, 0, 14, 4, 2, 12, 0, 2, 0, 13, 47],
  "D & N Haveli": [0, 0, 0, 0, 1, 2, 4, 25, 0, 0, 0, 0, 32],
  "Daman & Diu": [0, 0, 0, 0, 3, 2, 2, 3, 0, 0, 0, 0, 10],
  "Delhi": [2, 0, 8, 6, 128, 247, 17, 225, 19, 2, 10, 168, 832],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
  "Pondicherry": [3, 0, 0, 0, 184, 28, 10, 240, 7, 5, 0, 0, 477],
  "TOTAL (U.TS.)": [5, 0, 8, 6, 364, 283, 39, 582, 26, 9, 10, 181, 1513],
 },
 "Cities": {
  "Ahmedabad": [1, 0, 1, 0, 55, 99, 58, 74, 6, 4, 1, 46, 345],
  "Bangalore": [0, 2, 0, 1, 293, 137, 271, 235, 42, 6, 33, 164, 1184],
  "Bombay": [2, 0, 1, 4, 126, 358, 22, 196, 22, 6, 0, 6, 743],
  "Calcutta": [0, 0, 0, 0, 27, 19, 15, 14, 3, 25, 3, 15, 121],
  "Delhi": [2, 0, 7, 6, 101, 223, 15, 200, 19, 2, 10, 143, 728],
  "Hyderabad": [0, 0, 1, 1, 57, 122, 101, 44, 5, 3, 6, 52, 392],
  "Jaipur": [13, 0, 0, 1, 19, 39, 16, 22, 1, 1, 0, 32, 144],
  "Kanpur": [52, 18, 20, 3, 39, 35, 11, 65, 5, 0, 15, 84, 347],
  "Lucknow": [20, 0, 20, 4, 19, 12, 42, 10, 2, 0, 25, 83, 237],
  "Madras": [0, 0, 0, 0, 299, 57, 20, 276, 0, 0, 0, 77, 729],
  "Nagpur": [14, 0, 0, 0, 20, 133, 86, 25, 1, 0, 0, 116, 395],
  "Pune": [1, 0, 3, 1, 53, 68, 35, 61, 4, 0, 0, 19, 245],
 },
 "Grand": {
  "GRAND TOTAL": [3121, 250, 535, 437, 24641, 6953, 8314, 17937, 737, 259, 504, 10223, 73911],
 },
}
