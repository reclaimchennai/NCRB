# ADSI 1989, Appendix IV: suicides by means adopted and sex, States / UTs / cities
# (raw/adsi/1989/table_content/1680164107appendix-41989.pdf, pages 1-5: each page carries three categories by Male /
# Female / Total for every place, page 5 the Grand Total). Only the Total column of each category is recorded; every
# printed Male + Female equals its Total, and the Male and Female columns add up across categories and down the
# sections as well. The All-India row is printed "Total (All - India)". The cities carry no totals row. Read from the
# page images. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1989, "adsi"
SOURCE = "raw/adsi/1989/table_content/1680164107appendix-41989.pdf"
PAGES = "1-5"
TITLE = "Appendix IV: Distribution of Suicides by Means Adopted and Sex during 1989 (State, UT & City-wise)"
CATS = ["By Railways", "By Machine", "By Firearm", "By Weapon", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wire", "By Other Means", "Total"]
NA = None
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [286, 1, 5, 6, 1991, 573, 998, 890, 26, 21, 22, 648, 5467],
  "Arunachal Pradesh": [0, 0, 1, 2, 6, 2, 3, 38, 0, 0, 0, 2, 54],
  "Assam": [64, 19, 16, 10, 256, 32, 185, 1232, 22, 2, 30, 750, 2618],
  "Bihar": [16, 4, 9, 6, 248, 158, 74, 267, 22, 5, 38, 144, 991],
  "Goa": [2, 0, 0, 0, 25, 13, 33, 73, 9, 0, 1, 19, 175],
  "Gujarat": [136, 0, 2, 17, 784, 582, 367, 434, 47, 13, 5, 124, 2511],
  "Haryana": [447, 7, 4, 5, 383, 121, 148, 186, 13, 1, 19, 206, 1540],
  "Himachal Pradesh": [0, 0, 1, 2, 49, 5, 16, 21, 10, 1, 0, 5, 110],
  "Jammu & Kashmir": [12, 0, 2, 0, 11, 10, 5, 6, 1, 2, 0, 1, 50],
  "Karnataka": [133, 29, 16, 24, 2337, 444, 1511, 1842, 28, 33, 28, 1123, 7548],
  "Kerala": [267, 3, 3, 13, 2561, 242, 695, 3066, 12, 8, 37, 294, 7201],
  "Madhya Pradesh": [273, 8, 35, 34, 1254, 537, 599, 1582, 75, 83, 8, 672, 5160],
  "Maharashtra": [130, 19, 31, 4, 1908, 1071, 1294, 1199, 68, 14, 1, 1026, 6765],
  "Manipur": [0, 0, 1, 2, 4, 2, 7, 42, 0, 0, 1, 1, 60],
  "Meghalaya": [0, 6, 1, 0, 0, 12, 15, 49, 0, 1, 0, 2, 86],
  "Mizoram": [0, 0, 0, 0, 0, 0, 1, 22, 0, 0, 0, 6, 29],
  "Nagaland": [0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 7, 13],
  "Orissa": [182, 0, 6, 4, 932, 56, 174, 1020, 6, 17, 37, 303, 2737],
  "Punjab": [72, 0, 9, 4, 55, 38, 22, 51, 12, 7, 1, 0, 271],
  "Rajasthan": [142, 17, 11, 2, 211, 149, 256, 262, 30, 25, 5, 262, 1372],
  "Sikkim": [0, 0, 0, 2, 0, 4, 1, 30, 0, 0, 0, 0, 37],
  "Tamil Nadu": [157, 45, 49, 43, 3206, 1055, 842, 1290, 72, 106, 160, 1261, 8286],
  "Tripura": [0, 0, 0, 1, 201, 18, 0, 237, 0, 0, 0, 137, 594],
  "Uttar Pradesh": [250, 29, 306, 142, 201, 111, 54, 131, 13, 5, 1, 890, 2133],
  "West Bengal": [136, 13, 42, 50, 5348, 831, 462, 2697, 182, 11, 35, 1666, 11473],
  "TOTAL (STATES)": [2705, 200, 553, 373, 21971, 6066, 7762, 16670, 648, 355, 429, 9549, 67281],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 20, 2, 3, 81, 0, 0, 0, 0, 106],
  "Chandigarh": [0, 0, 0, 0, 11, 9, 2, 3, 1, 9, 5, 17, 57],
  "D & N Haveli": [0, 0, 0, 0, 5, 3, 0, 25, 1, 0, 0, 0, 34],
  "Daman & Diu": [0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 3],
  "Delhi": [1, 1, 9, 5, 139, 286, 22, 284, 16, 0, 1, 44, 808],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [3, 0, 0, 0, 204, 22, 3, 220, 0, 2, 1, 0, 455],
  "TOTAL (U.TS.)": [4, 1, 9, 5, 379, 322, 32, 614, 18, 11, 7, 61, 1463],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 1, 49, 113, 50, 71, 4, 3, 1, 62, 354],
  "Bangalore": [3, 0, 9, 0, 284, 140, 130, 272, 0, 2, 2, 250, 1092],
  "Bombay": [0, 0, 4, 1, 136, 226, 32, 158, 31, 14, 1, 13, 616],
  "Calcutta": [0, 0, 0, 0, 13, 19, 9, 14, 2, 10, 1, 5, 73],
  "Delhi": [1, 1, 8, 3, 99, 257, 17, 252, 14, 0, 1, 25, 678],
  "Hyderabad": [0, 0, 2, 1, 54, 154, 31, 31, 12, 4, 7, 104, 400],
  "Jaipur": [13, 0, 0, 0, 15, 8, 4, 22, 0, 2, 1, 61, 126],
  "Kanpur": [8, 1, 5, 1, 24, 16, 1, 53, 9, 0, 1, 28, 147],
  "Lucknow": [0, 0, 3, 4, 4, 0, 3, 11, 0, 0, 0, 30, 55],
  "Madras": [13, 0, 3, 0, 343, 333, 111, 503, 21, 50, 19, 172, 1568],
  "Nagpur": [2, 0, 1, 0, 14, 31, 42, 29, 1, 0, 0, 15, 135],
  "Pune": [0, 0, 0, 0, 60, 61, 20, 39, 1, 0, 0, 38, 219],
 },
 "Grand": {
  "GRAND TOTAL": [2709, 201, 562, 378, 22350, 6388, 7794, 17284, 666, 366, 436, 9610, 68744],
 },
}
