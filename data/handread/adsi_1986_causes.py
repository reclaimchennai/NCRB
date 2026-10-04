# ADSI 1986, Appendix V: statewise distribution of suicidal deaths under different causes with percentage to total
# deaths, pages 1-4 (printed sideways; pages 1-2 columns 3-11, pages 3-4 columns 12-19). Read from the page images;
# "—" (nil) is 0; the bracketed percentages are not recorded. Arunachal Pradesh and Mizoram are listed among the
# States this year. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1986, "adsi"
SOURCE = "raw/adsi/1986/table_content/1680163530appendix-51986.pdf"
PAGES = "1-4"
TITLE = ("Appendix V: Statewise Distribution of Sucidal Deaths Under Different Causes With Percentage to Total Deaths "
         "During 1986")
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear person", "Fall in social reputation",
        "Dowry disputes", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
# The States' totals row prints 4036 under Quarrel with parents-in-law and 20683 under Other causes (the row adds up
# either way, and the percentages 7.6 and 38.9 fit both); the States add up to 4039 and 20680, and Appendix III of the
# same report (suicides by causes and sex) prints 1,711 + 2,328 = 4039 and 12,545 + 8,135 = 20680 for the States and
# 1,718 + 2,353 = 4071 and 12,689 + 8,242 = 20931 for the Grand Total, so the 3 is misplaced in both totals rows.
CORRECTIONS = {
    ("TOTAL (STATES)", "Quarrel with parents-in-law"): (4036, 4039, "the States add up to 4039; Appendix III prints 1,711 male + 2,328 female = 4039; 7.6% fits both"),
    ("TOTAL (STATES)", "Other causes"): (20683, 20680, "the States add up to 20680; Appendix III prints 12,545 + 8,135 = 20680; 38.9% fits both; the totals row still adds up to 53,128"),
    ("GRAND TOTAL", "Quarrel with parents-in-law"): (4068, 4071, "States 4039 + UTs 32 = 4071; Appendix III prints 1,718 + 2,353 = 4071; 7.5% fits both"),
    ("GRAND TOTAL", "Other causes"): (20934, 20931, "States 20680 + UTs 251 = 20931; Appendix III prints 12,689 + 8,242 = 20931; 38.5% fits both"),
    ("TOTAL (U.TS.)", "Fall in social reputation"): (9, 19, "printed '9(1.5)'; 19/1229 = 1.5% (9 would be 0.7%); the UTs add up to 19 (2 + 9 + 3 + 5), the row then adds up to the printed 1,229 and States 345 + 19 = the printed Grand Total 364"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [44, 150, 164, 231, 105, 147, 66, 1046, 36, 30, 0, 11, 150, 0, 127, 1685, 3992],
  "Arunachal Pradesh": [0, 3, 2, 0, 3, 0, 1, 7, 0, 2, 0, 0, 0, 0, 15, 16, 49],
  "Assam": [55, 40, 29, 72, 140, 48, 50, 171, 47, 0, 14, 16, 2, 12, 1016, 669, 2381],
  "Bihar": [14, 40, 15, 11, 40, 18, 18, 24, 14, 2, 2, 3, 23, 3, 55, 92, 374],
  "Gujarat": [19, 100, 258, 83, 91, 173, 10, 291, 75, 33, 50, 40, 10, 11, 203, 733, 2180],
  "Haryana": [20, 43, 101, 35, 28, 39, 27, 140, 21, 15, 12, 18, 60, 2, 183, 140, 884],
  "Himachal Pradesh": [3, 5, 15, 4, 9, 8, 4, 8, 3, 3, 0, 0, 3, 0, 3, 30, 98],
  "Jammu & Kashmir": [1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 1, 0, 38, 13, 58],
  "Karnataka": [81, 140, 108, 281, 142, 176, 132, 551, 72, 94, 49, 16, 37, 2, 721, 2010, 4612],
  "Kerala": [34, 517, 153, 6, 177, 282, 91, 676, 43, 259, 25, 7, 15, 16, 446, 3388, 6135],
  "Madhya Pradesh": [105, 563, 195, 46, 89, 125, 80, 608, 33, 14, 18, 66, 44, 3, 610, 879, 3478],
  "Maharashtra": [90, 395, 362, 105, 149, 229, 121, 622, 73, 62, 16, 16, 71, 8, 392, 2538, 5249],
  "Manipur": [0, 0, 3, 1, 3, 1, 3, 7, 1, 0, 0, 0, 0, 0, 4, 0, 23],
  "Meghalaya": [0, 0, 4, 4, 2, 3, 0, 10, 0, 1, 0, 0, 0, 0, 10, 2, 36],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 0, 28],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 15, 4, 21],
  "Orissa": [105, 213, 197, 53, 185, 66, 35, 308, 42, 12, 32, 34, 22, 8, 467, 1049, 2828],
  "Punjab": [20, 17, 19, 11, 19, 16, 11, 35, 5, 2, 0, 5, 17, 2, 84, 98, 361],
  "Rajasthan": [33, 101, 138, 23, 42, 117, 31, 118, 7, 17, 16, 24, 20, 3, 55, 428, 1173],
  "Sikkim": [1, 1, 4, 4, 0, 6, 0, 11, 0, 1, 0, 0, 0, 0, 13, 0, 41],
  "Tamil Nadu": [102, 475, 340, 174, 465, 89, 162, 1522, 112, 37, 37, 15, 34, 12, 505, 4151, 8232],
  "Tripura": [27, 32, 32, 0, 56, 6, 21, 134, 0, 0, 2, 12, 0, 0, 0, 108, 430],
  "Uttar Pradesh": [27, 259, 64, 48, 82, 70, 133, 257, 14, 11, 7, 16, 58, 4, 384, 924, 2358],
  "West Bengal": [235, 945, 652, 143, 761, 264, 161, 576, 170, 70, 90, 46, 100, 57, 2114, 1723, 8107],
  "TOTAL (STATES)": [1016, 4039, 2856, 1336, 2590, 1884, 1157, 7123, 768, 666, 370, 345, 667, 143, 7488, 20680, 53128],
 },
 "U.Ts.": {
  "A & N Islands": [2, 2, 10, 0, 2, 0, 0, 14, 0, 0, 1, 2, 0, 0, 10, 30, 73],
  "Chandigarh": [0, 0, 1, 0, 4, 2, 0, 11, 0, 0, 0, 0, 0, 0, 8, 3, 29],
  "D & N Haveli": [0, 1, 13, 1, 0, 7, 0, 0, 0, 2, 1, 0, 0, 0, 1, 9, 35],
  "Delhi": [12, 22, 23, 14, 31, 6, 5, 75, 15, 6, 6, 9, 32, 0, 266, 116, 638],
  "Goa, Daman & Diu": [2, 1, 5, 4, 11, 5, 0, 10, 2, 0, 0, 3, 0, 0, 58, 17, 118],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [1, 6, 65, 25, 8, 69, 3, 28, 4, 0, 1, 5, 1, 0, 44, 76, 336],
  "TOTAL (U.TS.)": [17, 32, 117, 44, 56, 89, 8, 138, 21, 8, 9, 19, 33, 0, 387, 251, 1229],
 },
 "Cities": {
  "Ahmedabad": [4, 3, 18, 1, 10, 7, 0, 28, 2, 1, 6, 2, 0, 1, 6, 112, 201],
  "Bangalore": [20, 2, 5, 36, 16, 1, 0, 29, 13, 1, 1, 3, 12, 0, 97, 354, 590],
  "Bombay": [7, 15, 30, 8, 22, 23, 0, 48, 27, 7, 6, 0, 28, 0, 209, 51, 481],
  "Calcutta": [3, 9, 2, 9, 11, 6, 0, 20, 5, 1, 3, 0, 6, 0, 38, 13, 126],
  "Delhi": [11, 14, 11, 14, 29, 6, 3, 69, 11, 4, 6, 7, 29, 0, 242, 63, 519],
  "Hyderabad": [2, 4, 11, 11, 6, 4, 0, 25, 8, 3, 1, 0, 16, 0, 67, 126, 284],
  "Jaipur": [13, 6, 19, 1, 4, 7, 0, 8, 4, 0, 1, 4, 11, 0, 12, 0, 90],
  "Kanpur": [1, 8, 6, 0, 4, 0, 2, 21, 1, 0, 2, 1, 0, 0, 0, 74, 120],
  "Lucknow": [1, 0, 0, 1, 21, 5, 3, 44, 0, 0, 0, 0, 0, 0, 0, 43, 118],
  "Madras": [11, 25, 42, 37, 40, 6, 14, 144, 26, 5, 6, 0, 1, 0, 74, 394, 825],
  "Nagpur": [15, 12, 17, 0, 15, 3, 0, 11, 0, 0, 0, 0, 1, 2, 35, 81, 192],
  "Pune": [4, 12, 8, 1, 7, 1, 0, 18, 5, 1, 2, 1, 0, 0, 0, 90, 150],
  "TOTAL (CITIES)": [92, 110, 169, 119, 185, 69, 22, 465, 102, 23, 34, 18, 104, 3, 780, 1401, 3696],
 },
 "Grand": {"GRAND TOTAL": [1033, 4071, 2973, 1380, 2646, 1973, 1165, 7261, 789, 674, 379, 364, 700, 143, 7875, 20931, 54357]},
}
