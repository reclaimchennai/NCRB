# ADSI 1988, Appendix V: statewise distribution of suicidal deaths under different causes with percentage to total
# deaths, pages 1-4 (printed sideways; pages 1-2 columns 3-11, pages 3-4 columns 12-19). Read from the page images;
# "—" (nil) and a bare "(0.0)" are 0; the bracketed percentages are not recorded. The All India row is printed
# "TOTAL (ALL INDIA)" (kept here as GRAND TOTAL).
# Union Territories: on page 2 Daman & Diu is printed with long dashes (no figures) in columns 3-11; on page 4 the
# A & N Islands line is blank and the figures for A & N Islands, Chandigarh and D & N Haveli are each printed one line
# low, against Chandigarh, D & N Haveli and Daman & Diu. They are read here against the place their percentages and
# totals belong to: A & N Islands 4(4.1), 21(21.7), 13(13.4) are of 97 (columns 3-11 add to 63, the page-4 line
# 1 + 1 + 1 + 27 + 4 to 34); Chandigarh 10(21.3) is of 47 (10 + 2 + 21 + 14); D & N Haveli 12(34.3), 7(20.0) are of
# 35 (23 + 2 + 10). Daman & Diu therefore has no figures and is None. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1988, "adsi"
SOURCE = "raw/adsi/1988/table_content/1680163840appendix-51988.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Statewise Distribution of Suicidal Deaths Under Different Causes With Percentage To Total Deaths "
         "During 1988")
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear person", "Fall in social reputation",
        "Dowry disputes", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
CORRECTIONS = {
    ("Jammu & Kashmir", "Dreadful diseases"): ("(2.9)", 1, "the figure is not printed, only its percentage '(2.9)'; 1/35 = 2.9%, and the row adds up to the printed 35 only with 1 (a reading from the printed percentage and Total, not a change)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [64, 227, 180, 235, 93, 130, 131, 1124, 47, 47, 26, 14, 111, 5, 567, 1769, 4770],
  "Arunachal Pradesh": [6, 0, 2, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 12, 15, 41],
  "Assam": [33, 106, 30, 34, 187, 33, 75, 91, 12, 0, 7, 34, 0, 2, 978, 745, 2367],
  "Bihar": [16, 43, 46, 16, 14, 28, 14, 25, 13, 3, 20, 6, 47, 11, 215, 217, 734],
  "Goa": [1, 0, 6, 4, 9, 27, 2, 7, 3, 1, 5, 0, 1, 0, 63, 18, 147],
  "Gujarat": [32, 105, 277, 51, 92, 164, 19, 331, 127, 37, 37, 18, 17, 4, 230, 686, 2227],
  "Haryana": [19, 255, 40, 12, 13, 16, 34, 48, 15, 25, 7, 17, 34, 0, 95, 279, 909],
  "Himachal Pradesh": [7, 4, 7, 1, 6, 5, 0, 10, 0, 0, 0, 4, 0, 0, 30, 46, 120],
  "Jammu & Kashmir": [0, 6, 2, 0, 1, 1, 0, 1, 0, 0, 0, 0, 3, 0, 11, 10, 35],
  "Karnataka": [76, 76, 99, 227, 175, 162, 95, 1016, 69, 76, 69, 17, 115, 5, 1057, 3427, 6761],
  "Kerala": [60, 385, 360, 15, 210, 309, 199, 1400, 155, 180, 16, 12, 9, 3, 243, 3589, 7145],
  "Madhya Pradesh": [70, 607, 382, 42, 119, 125, 104, 721, 17, 14, 140, 47, 125, 13, 390, 1657, 4573],
  "Maharashtra": [103, 477, 411, 159, 180, 334, 89, 692, 82, 94, 29, 21, 35, 6, 338, 2955, 6005],
  "Manipur": [0, 2, 0, 1, 1, 2, 0, 1, 1, 0, 0, 0, 0, 0, 51, 0, 59],
  "Meghalaya": [0, 0, 0, 0, 1, 8, 0, 6, 0, 0, 0, 1, 0, 0, 20, 2, 38],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25],
  "Nagaland": [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 6],
  "Orissa": [47, 310, 238, 19, 127, 45, 22, 311, 12, 10, 18, 6, 40, 7, 624, 707, 2543],
  "Punjab": [16, 18, 26, 30, 14, 25, 6, 101, 5, 6, 3, 5, 18, 1, 240, 143, 657],
  "Rajasthan": [30, 147, 125, 30, 25, 97, 47, 131, 15, 5, 9, 23, 19, 10, 109, 629, 1451],
  "Sikkim": [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 27, 0, 31],
  "Tamil Nadu": [94, 582, 543, 448, 410, 194, 103, 2044, 217, 107, 69, 29, 99, 21, 1093, 3667, 9720],
  "Tripura": [11, 35, 21, 0, 74, 17, 5, 22, 1, 0, 0, 0, 0, 0, 86, 245, 517],
  "Uttar Pradesh": [25, 81, 58, 99, 86, 82, 132, 374, 15, 7, 3, 55, 76, 22, 320, 874, 2309],
  "West Bengal": [168, 852, 982, 191, 754, 354, 109, 588, 203, 19, 69, 24, 236, 51, 2097, 3171, 9868],
  "TOTAL (STATES)": [878, 4318, 3835, 1614, 2595, 2166, 1188, 9044, 1009, 631, 527, 333, 985, 161, 8897, 24877, 63058],
 },
 "U.Ts.": {
  "A & N Islands": [4, 6, 21, 1, 6, 9, 0, 13, 3, 1, 1, 1, 0, 0, 27, 4, 97],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 2, 0, 21, 14, 47],
  "D & N Haveli": [1, 0, 12, 0, 0, 7, 0, 3, 0, 0, 2, 0, 0, 0, 0, 10, 35],
  "Daman & Diu": [None] * 17,
  "Delhi": [12, 22, 20, 10, 24, 13, 4, 63, 9, 2, 3, 10, 38, 0, 211, 189, 630],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 3],
  "Pondicherry": [1, 43, 94, 13, 6, 3, 35, 70, 3, 7, 0, 0, 0, 0, 0, 125, 400],
  "TOTAL (U.TS.)": [18, 71, 147, 24, 36, 32, 39, 159, 15, 10, 7, 11, 40, 1, 259, 343, 1212],
 },
 "Cities": {
  "Ahmedabad": [2, 6, 13, 2, 7, 9, 4, 28, 6, 5, 7, 2, 3, 0, 68, 56, 218],
  "Bangalore": [5, 4, 1, 7, 13, 0, 0, 49, 16, 1, 1, 0, 20, 1, 78, 685, 881],
  "Bombay": [10, 23, 49, 18, 32, 32, 3, 25, 21, 6, 9, 1, 25, 5, 214, 136, 609],
  "Calcutta": [6, 10, 0, 1, 9, 1, 0, 10, 5, 0, 1, 1, 3, 0, 59, 0, 106],
  "Delhi": [11, 12, 14, 7, 15, 13, 7, 54, 7, 1, 2, 9, 37, 0, 170, 146, 505],
  "Hyderabad": [6, 7, 3, 12, 0, 3, 0, 19, 5, 2, 0, 1, 18, 0, 174, 73, 323],
  "Jaipur": [3, 0, 22, 0, 2, 0, 0, 2, 0, 0, 0, 1, 0, 0, 1, 29, 60],
  "Kanpur": [1, 6, 0, 2, 3, 1, 1, 8, 0, 0, 0, 1, 12, 0, 33, 35, 103],
  "Lucknow": [0, 14, 0, 0, 15, 2, 2, 17, 1, 0, 0, 0, 0, 0, 0, 28, 79],
  "Madras": [4, 40, 56, 44, 44, 38, 2, 155, 33, 59, 2, 4, 2, 0, 32, 370, 885],
  "Nagpur": [2, 1, 6, 0, 1, 5, 0, 9, 0, 0, 0, 0, 1, 0, 18, 128, 171],
  "Pune": [1, 0, 3, 7, 4, 2, 0, 9, 2, 1, 5, 1, 0, 0, 0, 192, 227],
  "TOTAL (CITIES)": [51, 123, 167, 100, 145, 106, 19, 385, 96, 75, 27, 21, 121, 6, 847, 1878, 4167],
 },
 "Grand": {"GRAND TOTAL": [896, 4389, 3982, 1638, 2631, 2198, 1227, 9203, 1024, 641, 534, 344, 1025, 162, 9156, 25220, 64270]},
}
