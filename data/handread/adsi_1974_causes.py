# ADSI 1974, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in States / U.Ts. / cities, pages 1-4 (printed sideways; pages 1-2 columns 3-8, pages 3-4 columns 9-16).
# Read from the page images; ".." (nil) is 0; the bracketed percentages are not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1974, "adsi"
SOURCE = "raw/adsi/1974/table_content/1680155296appendix-51974.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Distribution of Suicidal Deaths due to different Causes with Percentage to Total Suicidal Deaths "
         "in States/U.Ts. and Cities during 1974")
CATS = ["Failure in examination", "Quarrel with parents in law", "Quarrel with spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear persons", "Fall in social reputation",
        "Other causes", "Total"]
CORRECTIONS = {
    ("Himachal Pradesh", "Fall in social reputation"): (0, 2, "printed '.. (4 1)' with the figure 2 set one line low, on the Jammu & Kashmir line; 2/49 = 4.1% and the row then adds up to 49"),
    ("Jammu & Kashmir", "Fall in social reputation"): (2, 0, "printed '2 (0.0)', the 2 belonging to Himachal Pradesh above; the percentage is 0.0 and the row then adds up to 2"),
    ("Tamil Nadu", "Dispute over property"): (1, 63, "printed '1 (1.2)'; 63/5407 = 1.2%, the row then adds up to 5407 and the States' column to the printed 940"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [43, 288, 104, 117, 78, 43, 28, 1250, 16, 16, 0, 15, 1496, 3494],
  "Assam": [96, 51, 21, 95, 98, 45, 26, 104, 21, 80, 6, 9, 849, 1501],
  "Bihar": [43, 90, 13, 30, 65, 37, 29, 48, 4, 4, 1, 24, 693, 1081],
  "Gujarat": [5, 121, 156, 114, 53, 126, 14, 199, 77, 30, 4, 56, 477, 1432],
  "Haryana": [14, 96, 19, 7, 13, 9, 36, 59, 15, 1, 3, 0, 419, 691],
  "Himachal Pradesh": [1, 11, 5, 2, 2, 3, 2, 5, 0, 0, 3, 2, 13, 49],
  "Jammu & Kashmir": [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2],
  "Karnataka": [27, 99, 30, 278, 100, 65, 89, 420, 55, 35, 8, 95, 2152, 3453],
  "Kerala": [34, 413, 66, 266, 241, 148, 36, 490, 64, 56, 4, 25, 2172, 4015],
  "Madhya Pradesh": [17, 181, 162, 73, 57, 105, 91, 542, 53, 18, 18, 27, 2960, 4304],
  "Maharashtra": [60, 471, 225, 137, 96, 136, 50, 667, 37, 57, 2, 10, 1799, 3747],
  "Manipur": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 11],
  "Meghalaya": [1, 3, 0, 5, 6, 5, 0, 7, 0, 0, 0, 0, 49, 76],
  "Nagaland": [0, 0, 0, 1, 0, 4, 2, 0, 0, 0, 1, 1, 0, 9],
  "Orissa": [8, 261, 101, 4, 80, 23, 23, 359, 0, 1, 2, 2, 1263, 2127],
  "Punjab": [7, 50, 22, 34, 27, 33, 21, 42, 16, 5, 3, 3, 308, 571],
  "Rajasthan": [6, 97, 26, 8, 14, 27, 16, 93, 8, 3, 2, 23, 205, 528],
  "Tamil Nadu": [74, 276, 107, 302, 195, 21, 63, 1364, 75, 21, 56, 4, 2849, 5407],
  "Tripura": [14, 54, 50, 13, 68, 25, 1, 56, 17, 19, 0, 0, 109, 426],
  "Uttar Pradesh": [68, 240, 136, 138, 102, 75, 158, 474, 31, 69, 17, 64, 2038, 3610],
  "West Bengal": [333, 1113, 1123, 64, 1232, 247, 255, 1134, 0, 0, 0, 0, 3403, 8904],
  "TOTAL (STATES)": [852, 3916, 2366, 1688, 2528, 1177, 940, 7313, 489, 415, 130, 360, 23264, 45438],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 2, 0, 7, 0, 2, 0, 1, 1, 0, 0, 16, 56, 85],
  "Arunachal Pradesh": [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1, 5],
  "Chandigarh": [0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 5],
  "D. & N. Haveli": [0, 0, 3, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 6],
  "Delhi": [1, 17, 9, 1, 7, 1, 0, 29, 3, 6, 0, 0, 90, 164],
  "Goa, Daman & Diu": [1, 2, 4, 4, 7, 3, 2, 3, 0, 1, 2, 0, 14, 43],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2],
  "Pondicherry": [0, 11, 17, 0, 4, 2, 0, 57, 0, 0, 0, 0, 169, 260],
  "TOTAL (U.TS.)": [2, 32, 37, 12, 19, 10, 2, 94, 4, 7, 2, 18, 331, 570],
 },
 "Cities": {
  "Ahmedabad": [1, 6, 24, 7, 2, 7, 0, 14, 3, 2, 0, 3, 15, 84],
  "Bangalore": [5, 1, 1, 30, 2, 1, 0, 78, 3, 5, 0, 0, 357, 483],
  "Bombay": [0, 6, 2, 5, 15, 1, 0, 21, 8, 2, 1, 0, 83, 144],
  "Calcutta": [0, 0, 0, 3, 1, 0, 0, 6, 0, 0, 0, 0, 27, 37],
  "Delhi": [1, 4, 5, 0, 7, 1, 0, 22, 2, 6, 0, 0, 58, 106],
  "Hyderabad": [26, 6, 14, 14, 2, 1, 0, 57, 2, 0, 0, 0, 105, 227],
  "Kanpur": [1, 3, 11, 3, 4, 0, 9, 18, 4, 1, 2, 0, 33, 89],
  "Madras": [2, 26, 11, 15, 22, 4, 1, 206, 11, 3, 0, 0, 248, 549],
  "TOTAL (CITIES)": [36, 52, 68, 77, 55, 15, 10, 422, 33, 19, 3, 3, 926, 1719],
 },
 "Grand": {"GRAND TOTAL": [854, 3948, 2403, 1700, 2547, 1187, 942, 7407, 493, 422, 132, 378, 23595, 46008]},
}
