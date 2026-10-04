# ADSI 1973, Appendix VI: suicides by means with percentage to total, States / UTs / cities
# (raw/adsi/1973/table_content/1680154864appendix-61973.pdf, pages 1-4, printed sideways: pages 1-2 Railway to Fire,
# pages 3-4 Drowning to Total). Read from the page images; '—' (nil) is 0; percentages left out. Checked by
# scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1973, "adsi"
SOURCE = "raw/adsi/1973/table_content/1680154864appendix-61973.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of Suicidal Deaths by Different Means with Percentage to Total Suicidal Deaths in the States/U.Ts./Cities during 1973"
CATS = ["By Railway", "By Machine", "By Fire-arms", "By Weapons", "By poison", "By fire", "By Drowning", "By Hanging",
        "By Jumping", "By other causes", "Total"]
CORRECTIONS = {
    ("Jammu & Kashmir", "By Weapons"): ("— (0.0)", 1, "printed '— (0.0)', with a bare '—' (no percentage) in the Fire-arms column beside it; the row's other figures add to 39 against its printed Total 40 and their printed percentages to 97.5%, leaving 2.5% = 1/40, the States' Weapons column adds to 283 against its printed 284 (Grand Total 287 = 284 + 3 for the UTs), and Appendix IV prints Jammu & Kashmir's weapons suicides as 1 female. The printed (0.0) goes with the dropped figure, so here the percentage does not confirm the change on its own"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [252, 0, 2, 6, 896, 118, 1214, 509, 86, 303, 3386],
  "Assam": [140, 1, 4, 7, 61, 53, 455, 486, 56, 220, 1483],
  "Bihar": [82, 0, 29, 19, 126, 90, 332, 184, 83, 351, 1296],
  "Gujarat": [89, 7, 8, 2, 425, 294, 267, 122, 40, 286, 1540],
  "Haryana": [74, 11, 19, 0, 19, 63, 218, 98, 15, 210, 727],
  "Himachal Pradesh": [0, 0, 8, 1, 15, 6, 18, 21, 3, 15, 87],
  "Jammu & Kashmir": [2, 1, 0, 1, 1, 6, 16, 3, 0, 10, 40],
  "Karnataka": [49, 4, 13, 13, 847, 150, 1001, 564, 41, 1073, 3755],
  "Kerala": [153, 0, 1, 41, 1841, 6, 326, 1052, 28, 1008, 4456],
  "Madhya Pradesh": [256, 2, 25, 23, 191, 246, 427, 576, 54, 434, 2234],
  "Maharashtra": [157, 9, 19, 10, 1132, 309, 815, 380, 136, 313, 3280],
  "Manipur": [0, 0, 1, 0, 3, 0, 4, 3, 0, 2, 13],
  "Meghalaya": [0, 0, 1, 0, 0, 0, 0, 14, 0, 1, 16],
  "Nagaland": [0, 0, 1, 0, 0, 0, 0, 4, 0, 0, 5],
  "Orissa": [250, 0, 3, 15, 787, 33, 263, 272, 18, 406, 2047],
  "Punjab": [40, 7, 13, 2, 21, 12, 24, 45, 3, 29, 196],
  "Rajasthan": [38, 3, 1, 6, 5, 56, 169, 15, 23, 129, 445],
  "Tamil Nadu": [86, 25, 12, 9, 1920, 302, 734, 552, 32, 665, 4337],
  "Tripura": [0, 0, 2, 0, 235, 8, 8, 82, 16, 4, 355],
  "Uttar Pradesh": [403, 84, 125, 114, 176, 356, 720, 487, 74, 1427, 3966],
  "West Bengal": [214, 1, 12, 15, 3111, 136, 207, 1633, 17, 1231, 6577],
  "TOTAL (STATES)": [2285, 155, 299, 284, 11812, 2244, 7218, 7102, 725, 8117, 40241],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 0, 0, 12, 1, 5, 8, 0, 40, 66],
  "Arunachal Pradesh": [0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 6],
  "Chandigarh": [0, 0, 0, 0, 0, 1, 3, 0, 0, 1, 5],
  "D. & N. Haveli": [0, 0, 0, 0, 2, 0, 5, 6, 0, 16, 29],
  "Delhi": [32, 0, 4, 3, 14, 12, 16, 9, 5, 6, 101],
  "Goa, Daman & Diu": [0, 0, 2, 0, 15, 5, 10, 11, 0, 2, 45],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
  "Pondicherry": [0, 0, 0, 0, 62, 22, 63, 59, 1, 106, 313],
  "TOTAL (U.TS.)": [32, 0, 6, 3, 105, 42, 102, 99, 6, 171, 566],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 0, 18, 45, 5, 8, 3, 5, 84],
  "Bangalore": [0, 1, 2, 8, 127, 31, 106, 38, 3, 124, 440],
  "Bombay": [0, 2, 2, 1, 50, 26, 16, 18, 16, 13, 144],
  "Calcutta": [0, 0, 1, 0, 7, 3, 2, 16, 1, 1, 31],
  "Delhi": [32, 0, 4, 3, 12, 12, 11, 7, 4, 5, 90],
  "Hyderabad": [0, 0, 0, 1, 35, 9, 34, 0, 3, 5, 87],
  "Kanpur": [2, 0, 0, 0, 4, 9, 9, 7, 0, 0, 31],
  "Madras": [1, 0, 0, 0, 109, 59, 34, 79, 3, 22, 307],
  "TOTAL (CITIES)": [35, 3, 9, 13, 362, 194, 217, 173, 33, 175, 1214],
 },
 "Grand": {"GRAND TOTAL": [2317, 155, 305, 287, 11917, 2286, 7320, 7201, 731, 8288, 40807]},
}
