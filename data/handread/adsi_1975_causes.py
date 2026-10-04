# ADSI 1975, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-6 (upright; page 1 the States, columns 3-6, page 2 the States,
# columns 7-11, pages 3-4 the U.Ts. and cities, columns 3-6 and 7-11, page 5 all sections, columns 12-13, page 6 all
# sections, columns 14-16). Read from the page images; "—" (nil) is 0; the bracketed percentages are not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1975, "adsi"
SOURCE = "raw/adsi/1975/table_content/1680155697appendix-51975.pdf"
PAGES = "1-6"
TITLE = ("Appendix V: Distribution of Suicidal Deaths due to different Causes with Percentage to total Suicidal Deaths "
         "in the States/U.Ts./Cities during the year 1975")
CATS = ["Failure in Examination", "Quarrel with Parents-in-law", "Quarrel with spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Deaths of dear persons", "Fall in social reputation",
        "Other causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [40, 292, 190, 167, 61, 18, 23, 1116, 9, 8, 56, 12, 1399, 3391],
  "Assam": [89, 65, 29, 64, 182, 10, 14, 36, 9, 12, 0, 14, 691, 1215],
  "Bihar": [29, 33, 64, 21, 28, 22, 15, 32, 11, 2, 1, 6, 316, 580],
  "Gujarat": [15, 122, 149, 88, 49, 71, 24, 160, 73, 12, 10, 18, 555, 1346],
  "Haryana": [10, 76, 31, 4, 7, 18, 17, 88, 3, 7, 13, 23, 258, 555],
  "Himachal Pradesh": [4, 5, 4, 3, 6, 7, 3, 17, 0, 0, 1, 0, 41, 91],
  "Jammu & Kashmir": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
  "Karnataka": [59, 126, 68, 251, 120, 66, 129, 538, 62, 61, 5, 28, 3216, 4729],
  "Kerala": [25, 423, 71, 170, 438, 189, 93, 373, 39, 74, 44, 28, 2258, 4225],
  "Madhya Pradesh": [25, 274, 163, 47, 48, 68, 62, 463, 31, 17, 17, 18, 1231, 2464],
  "Maharashtra": [39, 418, 247, 189, 96, 114, 31, 708, 55, 41, 9, 30, 1567, 3544],
  "Manipur": [0, 1, 0, 4, 1, 0, 3, 2, 0, 0, 0, 0, 1, 12],
  "Meghalaya": [0, 0, 0, 3, 0, 1, 0, 3, 0, 0, 0, 0, 22, 29],
  "Nagaland": [0, 0, 0, 8, 2, 5, 0, 0, 0, 2, 0, 0, 0, 17],
  "Orissa": [37, 505, 130, 119, 166, 40, 23, 333, 4, 44, 14, 42, 826, 2283],
  "Punjab": [6, 12, 11, 5, 7, 51, 33, 14, 5, 1, 1, 1, 90, 237],
  "Rajasthan": [7, 87, 38, 8, 4, 20, 2, 77, 4, 2, 4, 9, 162, 424],
  "Sikkim": [0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 0, 0, 4],
  "Tamil Nadu": [47, 222, 117, 223, 243, 47, 115, 1517, 82, 69, 41, 22, 2095, 4840],
  "Tripura": [10, 94, 37, 0, 71, 11, 2, 55, 1, 1, 0, 0, 127, 409],
  "Uttar Pradesh": [81, 262, 172, 139, 134, 122, 174, 509, 37, 38, 76, 21, 2463, 4228],
  "West Bengal": [474, 1009, 948, 28, 925, 199, 110, 836, 12, 34, 26, 10, 3000, 7611],
  "TOTAL (STATES)": [997, 4026, 2469, 1541, 2589, 1081, 873, 6878, 437, 425, 318, 282, 20320, 42236],
 },
 "U.Ts.": {
  "A. & N. Islands": [3, 1, 0, 1, 0, 0, 1, 2, 1, 8, 0, 0, 6, 23],
  "Arunachal Pradesh": [0, 0, 3, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 8],
  "Chandigarh": [2, 0, 2, 0, 0, 0, 0, 6, 0, 0, 0, 1, 2, 13],
  "D. & N. Haveli": [0, 0, 5, 0, 0, 1, 0, 1, 0, 0, 0, 0, 5, 12],
  "Delhi": [3, 18, 28, 8, 21, 11, 5, 20, 6, 1, 5, 1, 77, 204],
  "Goa, Daman & Diu": [1, 1, 9, 1, 7, 8, 2, 8, 0, 1, 0, 1, 42, 81],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 3],
  "Mizoram": [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2],
  "Pondicherry": [1, 40, 9, 12, 7, 3, 0, 138, 2, 1, 0, 0, 95, 308],
  "TOTAL (U.TS.)": [10, 60, 56, 24, 39, 24, 8, 176, 9, 11, 5, 3, 229, 654],
 },
 "Cities": {
  "Ahmedabad": [3, 5, 14, 3, 6, 3, 0, 14, 3, 3, 1, 2, 34, 91],
  "Bangalore": [5, 0, 0, 13, 3, 0, 0, 56, 3, 0, 0, 0, 292, 372],
  "Bombay": [4, 13, 3, 10, 16, 3, 0, 12, 8, 3, 0, 2, 90, 164],
  "Calcutta": [1, 0, 2, 0, 1, 3, 0, 3, 0, 0, 1, 0, 30, 41],
  "Delhi": [3, 16, 15, 8, 21, 9, 5, 17, 6, 1, 3, 1, 54, 159],
  "Hyderabad": [3, 4, 4, 14, 6, 3, 0, 0, 36, 1, 0, 0, 90, 161],
  "Kanpur": [2, 7, 3, 4, 4, 0, 0, 10, 3, 0, 0, 0, 15, 48],
  "Madras": [0, 0, 6, 19, 34, 9, 4, 178, 7, 31, 0, 1, 274, 563],
  "TOTAL (CITIES)": [21, 45, 47, 71, 91, 30, 9, 290, 66, 39, 5, 6, 879, 1599],
 },
 "Grand": {"GRAND TOTAL": [1007, 4086, 2525, 1565, 2628, 1105, 881, 7054, 446, 436, 323, 285, 20549, 42890]},
}
