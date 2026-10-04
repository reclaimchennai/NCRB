# ADSI 1983, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / UTs / cities, pages 1-6 (printed sideways; pages 1-3 columns 3-8 for States 1-18, States
# 19-22 and UTs, and cities; pages 4-6 columns 9-16 for States 1-17, States 18-22 and UTs, and cities). Read from the
# page images; "—" (nil) is 0; the bracketed percentages are not recorded. Lucknow is printed "not available" across
# the row. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1983, "adsi"
SOURCE = "raw/adsi/1983/table_content/1680161935appendix-51983.pdf"
PAGES = "1-6"
TITLE = ("Appendix V: Distribution of Suicidal Deaths due to Different Causes with Percentage to Total Suicidal Deaths "
         "in the States/U.Ts./Cities during the Year 1983")
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear person", "Fall in social reputation",
        "Other causes", "Total"]
# TOTAL (U.TS.), Fall in social reputation prints as "(7·07)", the figure run into its percentage; read 7 (0.7% of
# 1003), which the UTs' column (1 + 1 + 5) and the Grand Total 554 = 547 + 7 confirm.
CORRECTIONS = {
    ("Jammu & Kashmir", "Death of dear person"): (11, 1, "printed '11(2.5)'; 1/41 = 2.4% (11 would be 26.8%), the row then adds up to the printed 41 and the States' column to the printed 432"),
    ("Tripura", "Total"): (449, 499, "printed 449; the causes add up to 499 and every printed percentage in the row is of 499 (69 = 13.8%, 78 = 15.6%, 104 = 20.8%; of 449 they would be 15.4%, 17.4%, 23.2%), and the States' Total column then adds up to the printed 45,576"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [58, 284, 108, 91, 143, 40, 115, 926, 98, 25, 2, 5, 1488, 3383],
  "Assam": [51, 59, 38, 215, 277, 92, 62, 183, 40, 26, 75, 101, 1217, 2436],
  "Bihar": [37, 50, 33, 12, 65, 32, 149, 101, 36, 6, 5, 4, 224, 754],
  "Gujarat": [26, 132, 297, 46, 73, 161, 13, 278, 34, 33, 24, 32, 626, 1775],
  "Haryana": [8, 33, 46, 21, 10, 32, 15, 127, 5, 17, 12, 15, 253, 594],
  "Himachal Pradesh": [4, 4, 4, 15, 15, 4, 19, 32, 3, 1, 0, 4, 61, 166],
  "Jammu & Kashmir": [3, 3, 3, 11, 4, 0, 0, 6, 2, 0, 1, 0, 8, 41],
  "Karnataka": [104, 198, 239, 356, 240, 164, 135, 850, 64, 49, 73, 63, 2195, 4730],
  "Kerala": [71, 429, 190, 188, 266, 228, 56, 551, 70, 69, 15, 109, 2999, 5241],
  "Madhya Pradesh": [64, 579, 121, 28, 81, 101, 69, 663, 17, 20, 9, 20, 1385, 3157],
  "Maharashtra": [38, 312, 337, 84, 117, 178, 47, 664, 50, 72, 19, 64, 1762, 3744],
  "Manipur": [2, 0, 0, 4, 7, 5, 2, 3, 0, 0, 0, 0, 30, 53],
  "Meghalaya": [1, 0, 2, 1, 3, 1, 4, 2, 0, 0, 1, 0, 9, 24],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4],
  "Orissa": [45, 233, 226, 27, 165, 84, 10, 233, 4, 4, 25, 25, 1324, 2405],
  "Punjab": [10, 23, 33, 16, 4, 13, 11, 41, 1, 3, 1, 0, 155, 311],
  "Rajasthan": [15, 114, 163, 19, 33, 76, 25, 137, 10, 25, 18, 29, 380, 1044],
  "Sikkim": [0, 0, 0, 5, 2, 7, 1, 10, 0, 0, 0, 0, 9, 34],
  "Tamil Nadu": [122, 357, 360, 121, 355, 45, 118, 1199, 117, 75, 34, 35, 2424, 5362],
  "Tripura": [20, 78, 76, 21, 104, 42, 9, 58, 2, 4, 16, 0, 69, 499],
  "Uttar Pradesh": [50, 199, 153, 78, 98, 75, 119, 382, 34, 3, 45, 29, 1238, 2503],
  "West Bengal": [252, 1155, 849, 59, 868, 302, 157, 696, 59, 6, 57, 12, 2844, 7316],
  "TOTAL (STATES)": [981, 4242, 3278, 1418, 2930, 1682, 1136, 7142, 646, 438, 432, 547, 20704, 45576],
 },
 "U.Ts.": {
  "A & N Islands": [1, 6, 7, 1, 2, 1, 3, 12, 1, 1, 2, 0, 12, 49],
  "Arunachal Pradesh": [1, 0, 2, 3, 4, 1, 0, 0, 0, 0, 1, 1, 20, 33],
  "Chandigarh": [0, 0, 1, 0, 1, 0, 0, 3, 0, 0, 0, 0, 13, 18],
  "D & N Haveli": [1, 5, 2, 1, 2, 10, 0, 6, 1, 1, 0, 1, 1, 31],
  "Delhi": [19, 36, 71, 6, 10, 11, 6, 85, 12, 3, 9, 5, 159, 432],
  "Goa, Daman & Diu": [1, 3, 4, 4, 6, 10, 0, 11, 5, 2, 0, 0, 53, 99],
  "Lakshadweep": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
  "Mizoram": [0, 0, 0, 2, 0, 2, 0, 3, 0, 2, 0, 0, 8, 17],
  "Pondicherry": [0, 64, 87, 13, 15, 1, 0, 131, 2, 6, 0, 0, 4, 323],
  "TOTAL (U.TS.)": [23, 114, 174, 30, 40, 37, 9, 251, 21, 15, 12, 7, 270, 1003],
 },
 "Cities": {
  "Ahmedabad": [6, 4, 31, 5, 5, 17, 0, 33, 5, 1, 2, 1, 103, 213],
  "Bangalore": [4, 2, 0, 17, 13, 4, 0, 46, 19, 1, 0, 0, 648, 754],
  "Bombay": [2, 13, 37, 7, 24, 16, 5, 37, 17, 2, 3, 5, 129, 297],
  "Calcutta": [2, 4, 14, 2, 6, 10, 0, 10, 0, 0, 2, 0, 7, 57],
  "Delhi": [16, 29, 49, 4, 8, 11, 3, 81, 10, 3, 8, 5, 155, 382],
  "Hyderabad": [4, 5, 10, 13, 11, 1, 0, 21, 8, 1, 0, 0, 179, 253],
  "Jaipur": [6, 10, 9, 0, 5, 0, 0, 10, 1, 0, 0, 1, 12, 54],
  "Kanpur": [1, 26, 13, 10, 8, 0, 2, 15, 4, 0, 8, 0, 4, 91],
  "Lucknow": [None] * 14,
  "Madras": [66, 18, 110, 15, 122, 12, 5, 188, 15, 28, 11, 28, 280, 898],
  "Nagpur": [6, 5, 6, 3, 5, 0, 0, 17, 2, 0, 0, 30, 172, 246],
  "Pune": [6, 13, 13, 0, 6, 2, 2, 16, 3, 2, 5, 5, 66, 139],
  "TOTAL (CITIES)": [119, 129, 292, 76, 213, 73, 17, 474, 84, 38, 39, 75, 1755, 3384],
 },
 "Grand": {"GRAND TOTAL": [1004, 4356, 3452, 1448, 2970, 1719, 1145, 7393, 667, 453, 444, 554, 20974, 46579]},
}
