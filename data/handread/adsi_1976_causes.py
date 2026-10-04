# ADSI 1976, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-4 (printed sideways; pages 1-2 columns 3-9, pages 3-4 columns 10-16).
# Read from the page images; ".." (nil) is 0; the bracketed percentages are not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1976, "adsi"
SOURCE = "raw/adsi/1976/table_content/1680156021appendix-51976.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Distribution of Suicidal Deaths due to different Causes with Percentage to Total Suicidal Deaths "
         "in the States/U.Ts/Cities During the Year 1976")
CATS = ["Failure in Examination", "Quarrel with parents in-law", "Quarrel with spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in Economic position", "Deaths of dear persons", "Fall in social reputation",
        "Other causes", "Total"]
CORRECTIONS = {
    ("Himachal Pradesh", "Fall in social reputation"): (11, 1, "printed '11 (1.3)'; 1/74 = 1.35%, printed 1.3 (11 would be 14.9%), the row then adds up to 74 and the States' column to the printed 294"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [43, 270, 150, 130, 67, 17, 170, 1385, 19, 18, 22, 28, 1900, 4219],
  "Assam": [45, 21, 13, 142, 126, 36, 49, 241, 19, 8, 11, 0, 502, 1213],
  "Bihar": [31, 27, 12, 25, 39, 16, 12, 16, 11, 10, 7, 12, 395, 613],
  "Gujarat": [33, 127, 177, 98, 58, 110, 28, 190, 52, 41, 12, 34, 516, 1476],
  "Haryana": [58, 104, 34, 20, 26, 13, 44, 105, 16, 5, 31, 33, 158, 647],
  "Himachal Pradesh": [2, 8, 3, 0, 8, 3, 4, 5, 0, 4, 3, 1, 33, 74],
  "Jammu & Kashmir": [0, 5, 0, 0, 5, 2, 1, 0, 7, 1, 1, 4, 23, 49],
  "Karnataka": [25, 153, 81, 278, 151, 107, 221, 715, 100, 169, 13, 35, 2230, 4278],
  "Kerala": [55, 293, 155, 97, 243, 84, 6, 451, 72, 45, 5, 14, 2037, 3557],
  "Madhya Pradesh": [13, 155, 157, 35, 0, 0, 452, 555, 15, 0, 0, 0, 919, 2301],
  "Maharashtra": [49, 390, 329, 170, 120, 164, 75, 798, 46, 53, 6, 20, 1683, 3903],
  "Manipur": [0, 0, 0, 2, 7, 0, 1, 0, 0, 0, 0, 0, 1, 11],
  "Meghalaya": [0, 0, 0, 1, 2, 27, 0, 1, 0, 1, 0, 0, 10, 42],
  "Nagaland": [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 5],
  "Orissa": [45, 370, 139, 18, 141, 32, 26, 265, 22, 10, 8, 21, 850, 1947],
  "Punjab": [5, 34, 26, 9, 9, 46, 10, 29, 5, 1, 5, 2, 100, 281],
  "Rajasthan": [27, 104, 30, 8, 20, 24, 15, 62, 4, 3, 14, 26, 256, 593],
  "Sikkim": [0, 1, 3, 0, 1, 2, 0, 4, 0, 0, 1, 0, 0, 12],
  "Tamil Nadu": [66, 363, 157, 290, 247, 42, 36, 1576, 102, 14, 9, 2, 1918, 4822],
  "Tripura": [9, 50, 100, 2, 63, 24, 0, 67, 0, 4, 0, 4, 102, 425],
  "Uttar Pradesh": [45, 182, 144, 135, 113, 106, 174, 567, 51, 26, 34, 30, 1006, 2613],
  "West Bengal": [305, 1053, 826, 28, 750, 255, 232, 905, 24, 9, 10, 27, 3241, 7665],
  "TOTAL (STATES)": [856, 3710, 2537, 1489, 2196, 1110, 1556, 7937, 565, 423, 193, 294, 17880, 40746],
 },
 "U.Ts.": {
  "A. & N. Islands": [1, 4, 12, 9, 6, 0, 1, 2, 2, 0, 0, 3, 31, 71],
  "Arunachal Pradesh": [0, 0, 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 4, 8],
  "Chandigarh": [3, 1, 1, 0, 1, 0, 0, 8, 1, 0, 1, 0, 5, 21],
  "D. & N. Haveli": [0, 0, 11, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 17],
  "Delhi": [5, 16, 17, 2, 10, 3, 2, 47, 6, 7, 2, 1, 122, 240],
  "Goa, Daman & Diu": [2, 2, 6, 4, 3, 10, 1, 3, 2, 3, 2, 0, 38, 76],
  "Lakshadweep": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7],
  "Pondicherry": [0, 33, 4, 23, 9, 0, 0, 90, 4, 0, 0, 0, 65, 228],
  "TOTAL (U.TS.)": [11, 56, 51, 39, 33, 13, 4, 152, 15, 10, 5, 5, 275, 669],
 },
 "Cities": {
  "Ahmedabad": [5, 16, 10, 0, 12, 11, 3, 9, 1, 0, 1, 1, 46, 115],
  "Bangalore": [2, 1, 0, 1, 4, 3, 0, 26, 8, 2, 1, 0, 275, 323],
  "Bombay": [3, 23, 14, 10, 24, 7, 1, 23, 12, 10, 0, 0, 82, 209],
  "Calcutta": [0, 2, 4, 5, 1, 3, 0, 8, 0, 0, 0, 0, 21, 44],
  "Delhi": [5, 10, 15, 0, 9, 2, 1, 35, 6, 7, 2, 1, 87, 180],
  "Hyderabad": [2, 5, 9, 14, 1, 0, 0, 23, 1, 6, 0, 0, 42, 103],
  "Kanpur": [0, 7, 6, 5, 3, 3, 1, 13, 0, 0, 0, 1, 0, 39],
  "Madras": [6, 36, 17, 31, 10, 15, 7, 59, 7, 0, 0, 2, 145, 335],
  "TOTAL (CITIES)": [23, 100, 75, 66, 64, 44, 13, 196, 35, 25, 4, 5, 698, 1348],
 },
 "Grand": {"GRAND TOTAL": [867, 3766, 2588, 1528, 2229, 1123, 1560, 8089, 580, 433, 198, 299, 18155, 41415]},
}
