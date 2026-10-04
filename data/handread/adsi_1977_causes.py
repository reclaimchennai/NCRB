# ADSI 1977, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-4 (printed sideways; pages 1-2 columns 3-9, pages 3-4 columns 10-16).
# Read from the page images; ".." and "—" (nil) are 0; the bracketed percentages are not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1977, "adsi"
SOURCE = "raw/adsi/1977/table_content/1680159812appendix-51977.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Distribution of suicidal Deaths due to different causes with percentage to total suicidal deaths "
         "in the States/U.Ts./Cities during the year 1977")
CATS = ["Failure in Examination", "Quarrel with parents/in-law", "Quarrel with spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in Economic position", "Deaths of dear persons", "Fall in social reputation",
        "Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [37, 204, 207, 118, 65, 41, 124, 1084, 33, 17, 9, 25, 1185, 3149],
  "Assam": [56, 66, 4, 85, 109, 35, 12, 178, 13, 11, 1, 10, 1175, 1755],
  "Bihar": [19, 31, 16, 15, 84, 12, 9, 20, 3, 1, 18, 18, 406, 652],
  "Gujarat": [15, 110, 169, 59, 47, 73, 19, 192, 41, 17, 17, 18, 489, 1266],
  "Haryana": [7, 52, 27, 19, 24, 19, 22, 51, 4, 4, 7, 2, 239, 477],
  "Himachal Pradesh": [0, 8, 12, 10, 4, 9, 0, 21, 0, 0, 3, 0, 72, 139],
  "Jammu and Kashmir": [0, 2, 1, 0, 0, 0, 3, 2, 0, 0, 0, 0, 4, 12],
  "Karnataka": [16, 155, 68, 305, 173, 45, 170, 627, 58, 94, 43, 66, 2638, 4458],
  "Kerala": [32, 416, 94, 133, 289, 182, 38, 564, 104, 34, 122, 21, 1668, 3697],
  "Madhya Pradesh": [27, 323, 152, 22, 59, 80, 71, 381, 9, 21, 11, 28, 935, 2119],
  "Maharashtra": [43, 343, 386, 116, 110, 124, 36, 679, 58, 34, 8, 47, 1388, 3372],
  "Manipur": [0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 0, 0, 0, 5],
  "Meghalaya": [0, 4, 0, 1, 4, 1, 0, 1, 1, 1, 0, 0, 27, 40],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 4],
  "Orissa": [23, 387, 194, 38, 103, 30, 30, 296, 31, 21, 28, 23, 759, 1963],
  "Punjab": [21, 33, 5, 14, 28, 32, 23, 28, 16, 4, 8, 2, 46, 260],
  "Rajasthan": [34, 114, 49, 2, 19, 39, 22, 45, 1, 6, 1, 42, 120, 494],
  "Sikkim": [0, 1, 3, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 6],
  "Tamil Nadu": [49, 313, 144, 137, 213, 15, 60, 1055, 88, 7, 3, 4, 2053, 4141],
  "Tripura": [3, 88, 64, 7, 82, 19, 0, 46, 0, 0, 0, 0, 74, 383],
  "Uttar Pradesh": [28, 223, 74, 77, 120, 96, 177, 324, 34, 17, 21, 30, 1032, 2253],
  "West Bengal": [299, 1032, 854, 26, 752, 241, 364, 846, 42, 6, 60, 12, 3794, 8328],
  "TOTAL (STATES)": [709, 3905, 2523, 1184, 2288, 1096, 1180, 6440, 536, 296, 360, 350, 18106, 38973],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 3, 2, 0, 0, 0, 1, 0, 0, 0, 0, 26, 32],
  "Arunachal Pradesh": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4, 5],
  "Chandigarh": [0, 2, 2, 1, 0, 3, 0, 7, 0, 3, 1, 0, 1, 20],
  "D. & N. Haveli": [0, 3, 3, 1, 0, 0, 0, 4, 0, 0, 0, 4, 10, 25],
  "Delhi": [3, 11, 18, 4, 15, 17, 9, 37, 2, 3, 2, 2, 122, 245],
  "Goa, Daman & Diu": [2, 2, 12, 2, 7, 12, 0, 10, 0, 0, 3, 4, 19, 73],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 1, 1, 0, 4, 0, 0, 0, 0, 5, 11],
  "Pondicherry": [1, 74, 6, 14, 8, 6, 0, 118, 3, 0, 0, 0, 104, 334],
  "TOTAL (U.TS.)": [6, 92, 44, 24, 31, 39, 9, 182, 5, 6, 6, 10, 291, 745],
 },
 "Cities": {
  "Ahmedabad": [1, 7, 24, 3, 5, 8, 3, 24, 4, 0, 2, 2, 59, 142],
  "Bangalore": [1, 3, 2, 9, 12, 0, 0, 74, 1, 1, 0, 0, 186, 289],
  "Bombay": [5, 15, 21, 15, 16, 5, 2, 12, 6, 5, 2, 3, 85, 192],
  "Calcutta": [2, 3, 4, 4, 1, 5, 0, 5, 0, 0, 0, 0, 16, 40],
  "Delhi": [3, 11, 13, 4, 12, 16, 8, 26, 2, 3, 2, 3, 115, 218],
  "Hyderabad": [3, 5, 8, 9, 8, 1, 2, 22, 4, 10, 0, 2, 73, 147],
  "Kanpur": [1, 11, 8, 4, 2, 1, 0, 4, 1, 0, 0, 0, 4, 36],
  "Madras": [1, 22, 12, 8, 14, 13, 0, 93, 9, 5, 0, 0, 74, 251],
  "TOTAL (CITIES)": [17, 77, 92, 56, 70, 49, 15, 260, 27, 24, 6, 10, 612, 1315],
 },
 "Grand": {"GRAND TOTAL": [715, 3997, 2567, 1208, 2319, 1135, 1189, 6622, 541, 302, 366, 360, 18397, 39718]},
}
