# ADSI 1970, Appendix V: statement of number of suicides in States / U.Ts. / cities by causes of suicides, pages 1-2
# (printed sideways). Read from the page images; ".." (nil) is 0. This table prints no percentages.
# Each section's totals row is printed just "Total"; it is named TOTAL (STATES) / TOTAL (U.TS.) / TOTAL (CITIES) here.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1970, "adsi"
SOURCE = "raw/adsi/1970/table_content/1680152236appendix-51970.pdf"
PAGES = "1-2"
TITLE = "Appendix V: Statement of Number of Suicides in States/U.Ts./Cities during 1970 (By Causes of Suicides)"
CATS = ["Failure in Examination", "Quarrel with parents-in-law", "Quarrel with married partners", "Poverty",
        "Frustration", "Love Affairs", "Insanity", "Dispute over property", "Dreadful disease", "Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [30, 229, 119, 130, 15, 79, 38, 71, 1418, 2129, 4258],
  "Assam": [25, 28, 37, 45, 102, 48, 56, 10, 205, 463, 1019],
  "Bihar": [74, 55, 51, 12, 4, 8, 5, 9, 29, 2020, 2267],
  "Gujarat": [11, 132, 130, 124, 74, 20, 136, 11, 206, 530, 1374],
  "Haryana": [39, 146, 12, 2, 1, 24, 4, 30, 32, 566, 856],
  "Himachal Pradesh": [2, 7, 10, 4, 4, 1, 3, 0, 1, 76, 108],
  "Jammu & Kashmir": [1, 0, 1, 2, 0, 1, 0, 0, 0, 0, 5],
  "Kerala": [31, 331, 139, 337, 132, 255, 126, 75, 126, 1597, 3149],
  "Madhya Pradesh": [173, 311, 366, 95, 23, 55, 101, 83, 464, 2156, 3827],
  "Maharashtra": [50, 384, 287, 185, 114, 66, 228, 39, 702, 3675, 5730],
  "Manipur": [0, 2, 0, 4, 0, 2, 0, 0, 0, 49, 57],
  "Mysore": [31, 134, 189, 322, 143, 130, 74, 17, 573, 1536, 3149],
  "Nagaland": [0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 4],
  "Orissa": [31, 298, 267, 5, 17, 72, 17, 12, 294, 1507, 2520],
  "Punjab": [59, 53, 25, 47, 10, 21, 24, 11, 102, 310, 662],
  "Rajasthan": [1, 69, 38, 11, 7, 16, 9, 8, 47, 58, 264],
  "Tamil Nadu": [130, 591, 233, 178, 137, 169, 25, 128, 1259, 2349, 5199],
  "Tripura": [42, 5, 0, 12, 0, 30, 0, 0, 21, 14, 124],
  "Uttar Pradesh": [265, 378, 289, 178, 110, 127, 264, 210, 436, 4081, 6338],
  "West Bengal": [734, 971, 834, 313, 166, 415, 139, 69, 848, 2449, 6938],
  "TOTAL (STATES)": [1729, 4124, 3027, 2006, 1059, 1539, 1250, 784, 6765, 25565, 47848],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [8, 5, 5, 7, 3, 4, 1, 0, 0, 26, 59],
  "Chandigarh": [0, 1, 1, 0, 0, 0, 0, 0, 1, 3, 6],
  "Dadra & Nagar Haveli": [0, 4, 0, 1, 1, 0, 1, 0, 1, 1, 9],
  "Delhi": [4, 10, 14, 8, 3, 6, 0, 1, 19, 119, 184],
  "Goa, Daman & Diu": [2, 0, 5, 5, 0, 3, 7, 0, 5, 47, 74],
  "Laccadives": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
  "Pondicherry": [2, 23, 23, 12, 24, 0, 4, 0, 39, 120, 247],
  "TOTAL (U.TS.)": [16, 43, 48, 33, 32, 13, 13, 1, 65, 316, 580],
 },
 "Cities": {
  "Ahmedabad": [2, 8, 12, 4, 1, 6, 4, 0, 5, 30, 72],
  "Bangalore": [5, 11, 10, 29, 20, 4, 0, 0, 83, 71, 233],
  "Bombay": [2, 5, 6, 23, 6, 15, 4, 0, 24, 52, 137],
  "Calcutta": [3, 0, 5, 11, 8, 3, 3, 0, 8, 32, 73],
  "Delhi": [4, 7, 13, 6, 3, 5, 0, 1, 16, 99, 154],
  "Hyderabad": [13, 3, 3, 13, 6, 3, 2, 0, 29, 192, 264],
  "Kanpur": [3, 10, 8, 4, 6, 4, 0, 0, 4, 8, 47],
  "Madras": [43, 20, 2, 14, 8, 14, 9, 1, 89, 160, 360],
  "TOTAL (CITIES)": [75, 64, 59, 104, 58, 54, 22, 2, 258, 644, 1340],
 },
 "Grand": {"GRAND TOTAL": [1745, 4167, 3075, 2039, 1091, 1552, 1263, 785, 6830, 25881, 48428]},
}
