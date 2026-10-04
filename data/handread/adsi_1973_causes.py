# ADSI 1973, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-4 (printed sideways; pages 1-2 columns 3-11, pages 3-4 columns 12-16).
# Read from the page images; "—" (nil) is 0; the bracketed percentages are not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1973, "adsi"
SOURCE = "raw/adsi/1973/table_content/1680154890appendix-51973.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Distribution of Suicidal Deaths due to different Causes with Percentage to Total Suicidal Deaths "
         "in the States/U.Ts./Cities during the year 1973")
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear persons", "Fall in Social reputation",
        "Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [21, 264, 145, 130, 93, 57, 49, 1416, 21, 17, 18, 69, 1086, 3386],
  "Assam": [65, 95, 52, 74, 88, 26, 33, 76, 16, 0, 4, 3, 951, 1483],
  "Bihar": [31, 135, 28, 56, 63, 29, 26, 55, 4, 2, 6, 8, 853, 1296],
  "Gujarat": [48, 117, 113, 72, 49, 127, 24, 174, 57, 6, 18, 11, 724, 1540],
  "Haryana": [21, 61, 33, 7, 25, 5, 21, 31, 14, 1, 5, 0, 503, 727],
  "Himachal Pradesh": [0, 8, 2, 1, 2, 1, 0, 10, 1, 1, 2, 2, 57, 87],
  "Jammu & Kashmir": [0, 2, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 29, 40],
  "Karnataka": [14, 121, 23, 219, 80, 32, 317, 759, 107, 67, 14, 109, 1893, 3755],
  "Kerala": [38, 595, 258, 543, 462, 195, 48, 437, 252, 172, 4, 24, 1428, 4456],
  "Madhya Pradesh": [10, 212, 179, 22, 64, 72, 100, 503, 14, 11, 13, 33, 1001, 2234],
  "Maharashtra": [52, 337, 212, 181, 83, 152, 43, 697, 34, 47, 6, 18, 1418, 3280],
  "Manipur": [1, 1, 1, 0, 2, 0, 0, 1, 0, 0, 0, 5, 2, 13],
  "Meghalaya": [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 12, 16],
  "Nagaland": [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 5],
  "Orissa": [14, 201, 181, 92, 56, 5, 38, 281, 0, 1, 0, 10, 1168, 2047],
  "Punjab": [25, 31, 9, 10, 22, 9, 5, 25, 13, 1, 1, 4, 41, 196],
  "Rajasthan": [5, 105, 32, 9, 4, 0, 0, 122, 1, 1, 4, 8, 154, 445],
  "Tamil Nadu": [42, 306, 159, 227, 153, 27, 100, 1081, 72, 82, 14, 190, 1884, 4337],
  "Tripura": [29, 97, 0, 2, 77, 14, 0, 33, 0, 5, 0, 4, 94, 355],
  "Uttar Pradesh": [58, 284, 116, 157, 83, 68, 214, 385, 52, 64, 27, 44, 2414, 3966],
  "West Bengal": [245, 1160, 1106, 239, 665, 258, 32, 657, 23, 28, 12, 28, 2124, 6577],
  "TOTAL (STATES)": [719, 4132, 2649, 2041, 2071, 1088, 1050, 6746, 681, 506, 148, 574, 17836, 40241],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 12, 2, 5, 0, 1, 0, 3, 1, 0, 0, 0, 42, 66],
  "Arunachal Pradesh": [0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 2, 6],
  "Chandigarh": [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5],
  "D & N. Haveli": [0, 0, 4, 1, 1, 1, 0, 0, 0, 0, 0, 1, 21, 29],
  "Delhi": [2, 9, 5, 3, 2, 1, 7, 23, 2, 0, 0, 0, 47, 101],
  "Goa, Daman & Diu": [0, 1, 5, 7, 2, 1, 0, 4, 1, 3, 0, 0, 21, 45],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
  "Pondicherry": [0, 15, 17, 1, 4, 4, 0, 74, 0, 0, 0, 0, 198, 313],
  "TOTAL (U.TS.)": [3, 40, 33, 17, 9, 9, 7, 107, 4, 3, 0, 1, 333, 566],
 },
 "Cities": {
  "Ahmedabad": [0, 2, 19, 4, 3, 7, 0, 23, 0, 0, 0, 2, 24, 84],
  "Bangalore": [3, 5, 0, 28, 11, 4, 2, 55, 1, 0, 11, 0, 320, 440],
  "Bombay": [1, 4, 6, 9, 27, 1, 0, 14, 7, 1, 1, 0, 73, 144],
  "Calcutta": [1, 1, 0, 2, 1, 2, 0, 2, 0, 0, 2, 0, 20, 31],
  "Delhi": [2, 7, 5, 3, 2, 1, 5, 19, 2, 0, 0, 0, 44, 90],
  "Hyderabad": [1, 3, 5, 8, 1, 0, 2, 34, 0, 0, 0, 0, 33, 87],
  "Kanpur": [0, 2, 2, 5, 3, 0, 4, 5, 0, 0, 0, 0, 10, 31],
  "Madras": [7, 42, 5, 10, 14, 7, 0, 124, 10, 19, 2, 4, 63, 307],
  "TOTAL (CITIES)": [15, 66, 42, 69, 62, 22, 13, 276, 20, 20, 16, 6, 587, 1214],
 },
 "Grand": {"GRAND TOTAL": [722, 4172, 2682, 2058, 2080, 1097, 1057, 6853, 685, 509, 148, 575, 18169, 40807]},
}
