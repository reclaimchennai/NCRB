# ADSI 1980, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-6 (upright; pages 1-3 columns 3-9: States 1-12, States 13-22 and
# U.Ts. 23-28, U.Ts. 29-31 and cities; pages 4-6 columns 10-16: States 1-17, States 18-22 and U.Ts., cities).
# Each figure is printed after its bracketed percentage. Read from the page images; "—" (nil) is 0; the bracketed
# percentages are not recorded (Lakshadweep's bankruptcy, deaths of dear persons and fall in social reputation print
# "—" with no percentage). Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1980, "adsi"
SOURCE = "raw/adsi/1980/table_content/1680160740appendix-51980.pdf"
PAGES = "1-6"
TITLE = ("Appendix V: Distribution of suicidal Deaths due to different causes with Percentage to total suicidal "
         "Deaths in the States/U.Ts./Cities during the Year 1980")
CATS = ["Failure in examination", "Quarrel with Parents-in-laws", "Quarrel with Spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of Dear persons", "Fall in Social reputation",
        "Other causes", "Total"]
# Uttar Pradesh, Unemployment is printed "(0.8) (32)", the figure itself in brackets; 32/3957 = 0.8%, read as 32.
CORRECTIONS = {
    ("Sikkim", "Insanity"): (18, 8, "printed '(53.4) 18' (clear); 8/15 = 53.3% (18 would be 120%), Sikkim's row then adds up to its printed Total 15 and the States' column to the printed 1,290 (Grand Total 1,317 = 1,290 + 27 for the U.Ts.)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [17, 179, 78, 100, 57, 73, 150, 401, 11, 13, 24, 7, 795, 1905],
  "Assam": [36, 41, 24, 82, 86, 47, 44, 75, 35, 17, 25, 105, 1104, 1721],
  "Bihar": [19, 27, 6, 47, 34, 28, 25, 62, 10, 2, 3, 6, 155, 424],
  "Gujarat": [13, 109, 209, 59, 72, 106, 28, 213, 49, 24, 10, 36, 676, 1604],
  "Haryana": [6, 37, 43, 9, 7, 18, 5, 88, 5, 2, 5, 6, 109, 340],
  "Himachal Pradesh": [2, 6, 3, 4, 7, 1, 2, 12, 0, 8, 1, 3, 49, 98],
  "Jammu & Kashmir": [0, 1, 1, 0, 10, 0, 0, 1, 0, 0, 0, 5, 15, 33],
  "Karnataka": [53, 138, 97, 329, 211, 118, 228, 683, 48, 11, 73, 58, 3712, 5759],
  "Kerala": [27, 359, 82, 30, 241, 136, 48, 450, 98, 117, 21, 57, 2147, 3813],
  "Madhya Pradesh": [28, 240, 149, 17, 55, 82, 46, 466, 0, 20, 26, 26, 1769, 2924],
  "Maharashtra": [22, 276, 225, 95, 134, 120, 48, 585, 40, 34, 13, 11, 1303, 2906],
  "Manipur": [1, 0, 0, 0, 1, 1, 0, 3, 0, 0, 0, 0, 6, 12],
  "Meghalaya": [0, 0, 3, 2, 2, 3, 0, 1, 4, 0, 0, 0, 17, 32],
  "Nagaland": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 12, 13],
  "Orissa": [20, 163, 121, 20, 102, 18, 23, 130, 3, 1, 4, 14, 1719, 2338],
  "Punjab": [14, 27, 22, 30, 25, 16, 2, 33, 7, 1, 2, 4, 84, 267],
  "Rajasthan": [4, 157, 49, 8, 18, 28, 4, 63, 6, 8, 4, 31, 243, 623],
  "Sikkim": [0, 0, 0, 2, 0, 8, 0, 5, 0, 0, 0, 0, 0, 15],
  "Tamil Nadu": [94, 350, 152, 96, 263, 47, 90, 1179, 89, 26, 9, 22, 2392, 4809],
  "Tripura": [25, 59, 25, 7, 45, 18, 4, 26, 0, 0, 0, 2, 110, 321],
  "Uttar Pradesh": [84, 228, 184, 144, 125, 128, 209, 279, 32, 48, 45, 56, 2395, 3957],
  "West Bengal": [227, 716, 516, 98, 728, 294, 150, 580, 41, 7, 64, 54, 3582, 7057],
  "TOTAL (STATES)": [692, 3113, 1989, 1179, 2224, 1290, 1106, 5335, 478, 339, 329, 503, 22394, 40971],
 },
 "U.Ts.": {
  "A. & N. Islands": [1, 7, 6, 0, 2, 3, 0, 6, 0, 1, 0, 0, 19, 45],
  "Arunachal Pradesh": [0, 0, 1, 0, 1, 3, 0, 0, 0, 0, 0, 0, 13, 18],
  "Chandigarh": [0, 0, 2, 0, 0, 0, 0, 4, 0, 0, 1, 0, 3, 10],
  "D. & N. Haveli": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 8, 9],
  "Delhi": [9, 26, 26, 10, 18, 9, 7, 31, 4, 0, 7, 2, 154, 303],
  "Goa, Daman & Diu": [1, 3, 2, 5, 6, 8, 0, 6, 0, 2, 0, 0, 43, 76],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
  "Pondicherry": [0, 17, 47, 9, 2, 3, 0, 19, 3, 0, 1, 0, 121, 222],
  "TOTAL (U.TS.)": [11, 53, 84, 24, 29, 27, 7, 66, 7, 3, 9, 2, 370, 692],
 },
 "Cities": {
  "Ahmedabad": [2, 2, 41, 4, 10, 7, 0, 44, 3, 3, 1, 3, 112, 232],
  "Bangalore": [2, 5, 0, 12, 5, 0, 4, 17, 11, 2, 1, 2, 875, 936],
  "Bombay": [2, 8, 4, 11, 11, 12, 0, 0, 9, 0, 0, 0, 145, 202],
  "Calcutta": [1, 4, 2, 2, 1, 2, 0, 4, 0, 0, 0, 0, 7, 23],
  "Delhi": [7, 22, 25, 9, 18, 9, 7, 29, 2, 0, 6, 2, 119, 255],
  "Hyderabad": [2, 11, 8, 8, 5, 2, 1, 12, 2, 6, 1, 2, 27, 87],
  "Kanpur": [29, 28, 26, 10, 14, 0, 6, 1, 5, 7, 0, 6, 11, 143],
  "Madras": [0, 6, 0, 20, 6, 0, 0, 80, 0, 2, 0, 0, 149, 263],
  "TOTAL (CITIES)": [45, 86, 106, 76, 70, 32, 18, 187, 32, 20, 9, 15, 1445, 2141],
 },
 "Grand": {"GRAND TOTAL": [703, 3166, 2073, 1203, 2253, 1317, 1113, 5401, 485, 342, 338, 505, 22764, 41663]},
}
