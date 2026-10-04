# ADSI 1975, Appendix VI: suicides by means with percentage to total, States / UTs / cities
# (raw/adsi/1975/table_content/1680155673appendix-61975.pdf, pages 1-4, upright: page 1 Railway, Machine; page 2
# Fire arms to Fire; page 3 Drowning, Hanging; page 4 Jumping, Other causes, Total). Read from the page images; '—'
# (nil) is 0; percentages left out. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1975, "adsi"
SOURCE = "raw/adsi/1975/table_content/1680155673appendix-61975.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of Suicidal Deaths by Different Means with percentage to total Suicidal Deaths in the States/U.Ts./Cities during the Year 1975"
CATS = ["By Railway", "By Machine", "By Fire arms", "By weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By other causes", "Total"]
CORRECTIONS = {
    ("Madras", "By other causes"): (30, 130, "printed 30 (23·1%), the first digit missing; 130/563 = 23·1%, and both the row (563) and the Cities' other-causes column (292) then add up"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [265, 37, 15, 30, 789, 160, 1019, 534, 21, 521, 3391],
  "Assam": [152, 2, 6, 2, 62, 47, 152, 503, 39, 250, 1215],
  "Bihar": [43, 6, 2, 8, 92, 50, 186, 112, 16, 65, 580],
  "Gujarat": [40, 3, 2, 11, 477, 194, 277, 110, 17, 215, 1346],
  "Haryana": [13, 2, 7, 7, 21, 44, 143, 129, 65, 124, 555],
  "Himachal Pradesh": [1, 0, 1, 1, 22, 5, 10, 24, 4, 23, 91],
  "Jammu & Kashmir": [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
  "Karnataka": [62, 3, 5, 11, 976, 211, 1271, 734, 37, 1419, 4729],
  "Kerala": [158, 0, 13, 6, 1858, 7, 490, 1347, 37, 309, 4225],
  "Madhya Pradesh": [255, 4, 76, 105, 244, 191, 399, 707, 46, 437, 2464],
  "Maharashtra": [153, 4, 6, 20, 1295, 369, 785, 457, 83, 372, 3544],
  "Manipur": [0, 0, 0, 0, 7, 1, 1, 3, 0, 0, 12],
  "Meghalaya": [0, 0, 0, 0, 0, 0, 7, 18, 0, 4, 29],
  "Nagaland": [0, 0, 5, 0, 0, 0, 0, 12, 0, 0, 17],
  "Orissa": [229, 0, 3, 0, 678, 13, 195, 724, 13, 428, 2283],
  "Punjab": [52, 6, 7, 2, 12, 10, 35, 60, 1, 52, 237],
  "Rajasthan": [33, 3, 17, 5, 18, 51, 230, 23, 3, 41, 424],
  "Sikkim": [0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 4],
  "Tamil Nadu": [104, 10, 4, 3, 2188, 313, 566, 646, 75, 931, 4840],
  "Tripura": [0, 0, 1, 1, 262, 4, 0, 121, 1, 19, 409],
  "Uttar Pradesh": [689, 103, 244, 247, 245, 394, 533, 458, 109, 1206, 4228],
  "West Bengal": [229, 14, 3, 26, 3286, 374, 493, 1829, 206, 1151, 7611],
  "TOTAL (STATES)": [2478, 197, 417, 485, 12533, 2438, 6794, 8552, 773, 7569, 42236],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 1, 0, 6, 0, 9, 7, 0, 0, 23],
  "Arunachal Pradesh": [0, 0, 3, 0, 0, 0, 2, 3, 0, 0, 8],
  "Chandigarh": [0, 0, 0, 0, 2, 6, 2, 3, 0, 0, 13],
  "D. & N. Haveli": [0, 0, 0, 0, 1, 0, 0, 11, 0, 0, 12],
  "Delhi": [32, 8, 1, 0, 32, 52, 18, 22, 20, 19, 204],
  "Goa, Daman & Diu": [0, 0, 0, 3, 27, 16, 16, 16, 1, 2, 81],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3],
  "Mizoram": [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2],
  "Pondicherry": [4, 0, 0, 0, 150, 6, 19, 72, 1, 56, 308],
  "TOTAL (U.TS.)": [36, 8, 6, 3, 218, 80, 66, 138, 22, 77, 654],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 1, 0, 15, 33, 27, 3, 6, 6, 91],
  "Bangalore": [0, 1, 0, 0, 92, 53, 98, 16, 7, 105, 372],
  "Bombay": [2, 0, 1, 10, 46, 41, 16, 19, 8, 21, 164],
  "Calcutta": [0, 0, 1, 0, 7, 4, 0, 21, 5, 3, 41],
  "Delhi": [32, 6, 0, 0, 26, 45, 9, 15, 16, 10, 159],
  "Hyderabad": [0, 0, 2, 2, 53, 27, 38, 22, 0, 17, 161],
  "Kanpur": [7, 6, 17, 8, 0, 10, 0, 0, 0, 0, 48],
  "Madras": [1, 0, 0, 0, 181, 82, 52, 117, 0, 130, 563],
  "TOTAL (CITIES)": [42, 13, 22, 20, 420, 295, 240, 213, 42, 292, 1599],
 },
 "Grand": {"GRAND TOTAL": [2514, 205, 423, 488, 12751, 2518, 6860, 8690, 795, 7646, 42890]},
}
