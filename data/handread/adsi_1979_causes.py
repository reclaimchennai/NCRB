# ADSI 1979, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-4 (printed sideways; page 1 the States, columns 3-9, page 2 the U.Ts.
# and cities, columns 3-9, page 3 the States, columns 10-16, page 4 the U.Ts. and cities, columns 10-16).
# Read from the page images; "—" (nil) is 0; the bracketed percentages are not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1979, "adsi"
SOURCE = "raw/adsi/1979/table_content/1680160347appendix-51979.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Distribution of suicidal deaths due to different causes with percentage to total suicidal deaths "
         "in the States/U.Ts./Cities during the year 1979")
CATS = ["Failure in Examination", "Quarrel with Parents-in-law", "Quarrel with Spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful Diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Deaths of dear persons", "Fall in social reputation",
        "Other causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [26, 138, 73, 201, 72, 37, 169, 955, 40, 27, 10, 8, 1571, 3327],
  "Assam": [18, 49, 27, 120, 135, 16, 39, 144, 10, 13, 3, 18, 1219, 1811],
  "Bihar": [9, 18, 16, 17, 41, 11, 16, 33, 3, 4, 5, 3, 170, 346],
  "Gujarat": [13, 79, 179, 34, 69, 108, 16, 232, 90, 14, 27, 17, 610, 1488],
  "Haryana": [8, 98, 33, 10, 17, 15, 11, 55, 25, 0, 3, 29, 146, 450],
  "Himachal Pradesh": [2, 1, 2, 2, 3, 0, 2, 7, 1, 1, 0, 1, 38, 60],
  "Jammu & Kashmir": [0, 2, 3, 0, 1, 1, 0, 1, 0, 0, 0, 0, 15, 23],
  "Karnataka": [17, 186, 78, 221, 155, 91, 163, 774, 15, 23, 11, 108, 3134, 4976],
  "Kerala": [38, 250, 59, 78, 384, 149, 97, 465, 92, 37, 16, 74, 1892, 3631],
  "Madhya Pradesh": [19, 212, 106, 27, 65, 42, 38, 256, 4, 10, 3, 11, 550, 1343],
  "Maharashtra": [31, 257, 315, 91, 141, 122, 72, 703, 36, 33, 10, 27, 1268, 3106],
  "Manipur": [0, 1, 0, 0, 1, 6, 0, 5, 0, 0, 0, 0, 0, 13],
  "Meghalaya": [1, 0, 0, 2, 3, 1, 0, 2, 0, 0, 2, 0, 16, 27],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
  "Orissa": [52, 232, 125, 21, 108, 22, 32, 219, 2, 9, 4, 15, 1141, 1982],
  "Punjab": [25, 43, 23, 16, 52, 13, 10, 50, 14, 5, 3, 6, 67, 327],
  "Rajasthan": [4, 149, 71, 6, 7, 48, 23, 64, 1, 5, 4, 17, 216, 615],
  "Sikkim": [0, 3, 2, 5, 3, 0, 2, 2, 0, 0, 0, 0, 0, 17],
  "Tamil Nadu": [83, 360, 113, 138, 169, 30, 203, 806, 60, 18, 16, 28, 2451, 4475],
  "Tripura": [16, 50, 62, 5, 96, 20, 5, 40, 1, 2, 8, 2, 80, 387],
  "Uttar Pradesh": [67, 287, 149, 147, 140, 90, 196, 335, 33, 74, 38, 237, 1739, 3532],
  "West Bengal": [190, 662, 729, 84, 489, 147, 81, 674, 20, 14, 10, 25, 2478, 5603],
  "TOTAL (STATES)": [619, 3077, 2165, 1225, 2151, 969, 1175, 5822, 447, 289, 173, 626, 18807, 37545],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 7, 6, 3, 4, 2, 0, 7, 0, 1, 0, 0, 14, 44],
  "Arunachal Pradesh": [0, 0, 3, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 6],
  "Chandigarh": [0, 2, 4, 0, 0, 0, 0, 2, 1, 0, 1, 0, 3, 13],
  "D. & N. Haveli": [0, 0, 4, 0, 0, 0, 0, 5, 0, 0, 0, 7, 5, 21],
  "Delhi": [5, 25, 25, 5, 25, 17, 15, 34, 5, 1, 4, 2, 170, 333],
  "Goa, Daman & Diu": [0, 2, 5, 3, 6, 21, 0, 4, 1, 1, 0, 0, 35, 78],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 5, 11],
  "Pondicherry": [2, 50, 27, 4, 1, 0, 0, 26, 4, 0, 0, 0, 52, 166],
  "TOTAL (U.TS.)": [7, 86, 74, 16, 37, 43, 15, 79, 11, 6, 5, 9, 284, 672],
 },
 "Cities": {
  "Ahmedabad": [3, 0, 33, 2, 8, 5, 1, 19, 0, 2, 0, 4, 112, 189],
  "Bangalore": [1, 0, 0, 11, 22, 0, 0, 3, 0, 2, 0, 0, 416, 455],
  "Bombay": [0, 2, 5, 6, 16, 5, 2, 33, 6, 2, 1, 0, 123, 201],
  "Calcutta": [1, 2, 3, 1, 0, 7, 0, 8, 0, 0, 0, 0, 24, 46],
  "Delhi": [5, 22, 18, 5, 24, 17, 14, 31, 5, 1, 4, 2, 167, 315],
  "Hyderabad": [4, 4, 5, 6, 11, 0, 0, 27, 4, 2, 0, 1, 18, 82],
  "Kanpur": [2, 1, 4, 2, 1, 0, 12, 0, 0, 5, 0, 0, 14, 41],
  "Madras": [3, 8, 3, 15, 4, 1, 0, 82, 3, 2, 0, 0, 156, 277],
  "TOTAL (CITIES)": [19, 39, 71, 48, 86, 35, 29, 203, 18, 16, 5, 7, 1030, 1606],
 },
 "Grand": {"GRAND TOTAL": [626, 3163, 2239, 1241, 2188, 1012, 1190, 5901, 458, 295, 178, 635, 19091, 38217]},
}
