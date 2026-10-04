# ADSI 1978, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-4 (printed sideways; pages 1-2 columns 3-9, pages 3-4 columns 10-16).
# Read from the page images; "—" (nil) is 0; the bracketed percentages are not recorded. Each section's totals row is
# printed just "Total"; it is named TOTAL (STATES) / TOTAL (U.TS.) / TOTAL (CITIES) here.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1978, "adsi"
SOURCE = "raw/adsi/1978/table_content/1680159999appendix-51978.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Distribution of suicidal Deaths due to different causes with percentage to total suicidal deaths "
         "in the States/U.Ts./Cities during the year 1978")
CATS = ["Failure in Examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Deaths of dear persons", "Fall in social reputation",
        "Other causes", "Total"]
# Andhra Pradesh, Fall in social reputation is printed "11 (6.4)": 11/2881 = 0.4%, but 11 is what makes the row and
# the column add up, so the percentage is the misprint and 11 is kept.
CORRECTIONS = {
    ("Rajasthan", "Love Affairs"): (67, 57, "printed '67 (6.5)'; 57/876 = 6.5% (67 would be 7.6%), the row then adds up to 876 and the States' column to the printed 2294"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [36, 172, 60, 113, 94, 38, 107, 1050, 30, 19, 5, 11, 1146, 2881],
  "Assam": [55, 71, 29, 102, 273, 50, 103, 231, 6, 23, 22, 13, 1001, 1979],
  "Bihar": [11, 9, 6, 26, 17, 8, 22, 39, 22, 0, 3, 8, 1028, 1199],
  "Gujarat": [24, 110, 138, 46, 75, 94, 15, 193, 73, 39, 12, 36, 1119, 1974],
  "Haryana": [11, 115, 45, 14, 6, 24, 14, 67, 7, 3, 8, 51, 127, 492],
  "Himachal Pradesh": [0, 3, 16, 5, 7, 4, 0, 11, 1, 0, 0, 2, 8, 57],
  "Jammu & Kashmir": [2, 3, 7, 0, 1, 6, 2, 0, 0, 0, 0, 0, 19, 40],
  "Karnataka": [25, 145, 85, 304, 118, 52, 163, 504, 47, 32, 9, 12, 3396, 4892],
  "Kerala": [19, 355, 128, 91, 447, 132, 45, 613, 76, 98, 4, 101, 1481, 3590],
  "Madhya Pradesh": [22, 419, 203, 9, 60, 63, 65, 569, 4, 18, 6, 29, 914, 2381],
  "Maharashtra": [39, 436, 296, 80, 93, 156, 33, 671, 29, 34, 33, 12, 1250, 3162],
  "Manipur": [0, 1, 0, 0, 4, 3, 0, 1, 0, 0, 0, 0, 0, 9],
  "Meghalaya": [0, 0, 2, 0, 0, 1, 2, 1, 1, 3, 1, 0, 42, 53],
  "Nagaland": [0, 0, 0, 2, 0, 2, 1, 0, 0, 0, 0, 2, 1, 8],
  "Orissa": [13, 247, 86, 30, 89, 18, 19, 231, 18, 7, 20, 7, 672, 1457],
  "Punjab": [8, 44, 24, 15, 14, 34, 7, 49, 8, 3, 5, 8, 47, 266],
  "Rajasthan": [12, 187, 86, 15, 57, 82, 29, 98, 22, 3, 2, 66, 217, 876],
  "Sikkim": [0, 0, 0, 3, 3, 0, 2, 4, 0, 0, 0, 0, 0, 12],
  "Tamil Nadu": [77, 287, 118, 118, 179, 13, 44, 1033, 23, 18, 12, 24, 1959, 3905],
  "Tripura": [20, 51, 33, 7, 69, 7, 0, 33, 1, 7, 0, 13, 39, 280],
  "Uttar Pradesh": [49, 221, 114, 85, 144, 78, 93, 445, 17, 27, 28, 61, 1900, 3262],
  "West Bengal": [177, 759, 778, 45, 544, 225, 79, 747, 41, 17, 17, 8, 3306, 6743],
  "TOTAL (STATES)": [600, 3635, 2254, 1110, 2294, 1090, 845, 6590, 426, 351, 187, 464, 19672, 39518],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 2, 4, 0, 0, 0, 0, 1, 0, 0, 0, 3, 28, 38],
  "Arunachal Pradesh": [0, 0, 0, 1, 1, 3, 1, 1, 0, 0, 0, 0, 4, 11],
  "Chandigarh": [1, 7, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 7, 19],
  "D. & N. Haveli": [0, 1, 1, 0, 0, 8, 0, 0, 0, 0, 0, 0, 4, 14],
  "Delhi": [9, 28, 7, 3, 9, 8, 0, 20, 4, 0, 5, 25, 87, 205],
  "Goa, Daman & Diu": [0, 4, 5, 1, 9, 11, 2, 8, 2, 0, 0, 0, 28, 70],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
  "Mizoram": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 4],
  "Pondicherry": [4, 79, 28, 8, 2, 1, 2, 54, 3, 0, 0, 0, 146, 327],
  "TOTAL (U.TS.)": [14, 121, 45, 13, 22, 32, 5, 88, 9, 0, 5, 28, 307, 689],
 },
 "Cities": {
  "Ahmedabad": [5, 4, 35, 7, 4, 9, 1, 32, 8, 3, 3, 3, 52, 166],
  "Bangalore": [4, 2, 2, 9, 7, 0, 0, 34, 11, 0, 0, 0, 876, 945],
  "Bombay": [3, 15, 5, 11, 25, 1, 0, 6, 13, 9, 7, 0, 91, 186],
  "Calcutta": [0, 0, 4, 4, 0, 7, 2, 0, 0, 0, 0, 1, 11, 29],
  "Delhi": [9, 25, 7, 3, 4, 5, 0, 20, 4, 0, 5, 25, 82, 189],
  "Hyderabad": [3, 2, 3, 9, 9, 0, 6, 6, 0, 0, 0, 0, 58, 96],
  "Kanpur": [2, 5, 4, 3, 1, 0, 0, 29, 0, 0, 0, 0, 28, 72],
  "Madras": [1, 6, 2, 6, 2, 3, 2, 42, 3, 2, 0, 0, 79, 148],
  "TOTAL (CITIES)": [27, 59, 62, 52, 52, 25, 11, 169, 39, 14, 15, 29, 1277, 1831],
 },
 "Grand": {"GRAND TOTAL": [614, 3756, 2299, 1123, 2316, 1122, 850, 6678, 435, 351, 192, 492, 19979, 40207]},
}
