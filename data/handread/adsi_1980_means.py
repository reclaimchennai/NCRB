# ADSI 1980, Appendix VI: suicides by means with percentage to total, States / UTs / cities
# (raw/adsi/1980/table_content/1680160689appendix-61980.pdf, pages 1-4, upright: pages 1-2 Railways to Fire, pages 3-4
# Drowning to Total; each percentage printed before its figure). Read from the page images; '—' (nil) is 0;
# percentages left out. Several figures in the right-hand columns are smudged (the fire column, the Totals of the UTs and
# cities); each was read against its printed percentage and the row it closes
# (Uttar Pradesh fire 400 = 10·1% of 3,957; West Bengal fire 395 = 5·6% of 7,057; Ahmedabad 232, Bangalore 936, Hyderabad 87). Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1980, "adsi"
SOURCE = "raw/adsi/1980/table_content/1680160689appendix-61980.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of the Suicidal Deaths by different Means with Percentage to Total Suicidal Deaths in the States/Union Territories/Cities during 1980"
CATS = ["By Railways", "By Machine", "By Fire-Arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By other causes", "Total"]
CORRECTIONS = {
    ("Assam", "Total"): ("172,", 1721, "printed '172,' with the last digit lost after the comma; the row adds up to 1721, its hanging figure alone is 816 (47·4% of 1721), and the States' Total column then adds up to 40,971 (a reading of the printed digits, not a change)"),
    ("West Bengal", "By other causes"): (1150, 1156, "printed 1,150 (16·4%) clearly; 1156/7057 = 16·4% (1150 would be 16·3%), and both the row (7,057) and the States' other-causes column (7,632) then add up"),
    ("TOTAL (STATES)", "By Fire"): ("2,9?? (blotted)", 2977, "the figure is blotted after '2,9'; the States' fire figures add to 2977, the row then adds up to its printed 40,971, Grand Total 3,095 = 2977 + 118 for the UTs, and its printed (7·3%) = 2977/40971 (a reading of the blotted figure, not a change)"),
    ("TOTAL (U.TS.)", "Total"): (689, 692, "printed 689 (partly blotted, and the UTs' printed percentages were worked out on 689); the UT rows add up to 692, every UT column adds up to its printed total and those totals add to 692, and the Grand Total 41,663 = 40,971 + 692. The printed percentages go with the misprint, so here they do not confirm the change on their own"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [4, 3, 38, 13, 720, 98, 331, 319, 11, 368, 1905],
  "Assam": [73, 14, 9, 4, 80, 38, 311, 816, 15, 361, 1721],
  "Bihar": [53, 0, 7, 14, 56, 51, 94, 125, 14, 10, 424],
  "Gujarat": [258, 3, 19, 2, 301, 276, 363, 149, 32, 201, 1604],
  "Haryana": [23, 0, 3, 2, 27, 64, 77, 109, 0, 35, 340],
  "Himachal Pradesh": [0, 2, 3, 0, 14, 7, 16, 23, 9, 24, 98],
  "Jammu & Kashmir": [7, 0, 0, 1, 4, 4, 4, 8, 1, 4, 33],
  "Karnataka": [51, 124, 11, 7, 1096, 336, 2053, 837, 75, 1169, 5759],
  "Kerala": [207, 1, 0, 9, 1367, 33, 302, 1383, 8, 503, 3813],
  "Madhya Pradesh": [323, 5, 41, 30, 275, 392, 552, 731, 50, 525, 2924],
  "Maharashtra": [153, 0, 14, 9, 629, 330, 781, 449, 54, 487, 2906],
  "Manipur": [0, 0, 2, 0, 0, 0, 0, 10, 0, 0, 12],
  "Meghalaya": [0, 0, 1, 0, 0, 1, 2, 13, 6, 9, 32],
  "Nagaland": [0, 0, 1, 0, 1, 0, 2, 7, 0, 2, 13],
  "Orissa": [279, 3, 1, 2, 529, 3, 219, 629, 5, 668, 2338],
  "Punjab": [77, 4, 7, 3, 25, 29, 26, 60, 4, 32, 267],
  "Rajasthan": [68, 5, 11, 3, 49, 89, 188, 97, 22, 91, 623],
  "Sikkim": [0, 0, 0, 0, 2, 0, 5, 8, 0, 0, 15],
  "Tamil Nadu": [192, 6, 1, 12, 1590, 420, 888, 722, 62, 916, 4809],
  "Tripura": [0, 1, 1, 3, 146, 11, 16, 122, 0, 21, 321],
  "Uttar Pradesh": [528, 38, 312, 200, 320, 400, 406, 602, 101, 1050, 3957],
  "West Bengal": [326, 17, 13, 20, 2412, 395, 478, 2185, 55, 1156, 7057],
  "TOTAL (STATES)": [2622, 226, 495, 334, 9643, 2977, 7114, 9404, 524, 7632, 40971],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [0, 0, 1, 0, 16, 2, 7, 18, 0, 1, 45],
  "Arunachal Pradesh": [0, 2, 0, 0, 0, 0, 3, 9, 0, 4, 18],
  "Chandigarh": [0, 0, 0, 0, 0, 2, 1, 7, 0, 0, 10],
  "Dadra & Nagar Haveli": [0, 0, 0, 0, 0, 0, 1, 8, 0, 0, 9],
  "Delhi": [46, 4, 2, 7, 19, 108, 24, 51, 23, 19, 303],
  "Goa, Daman & Diu": [2, 0, 0, 0, 10, 3, 36, 19, 5, 1, 76],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 6],
  "Pondicherry": [0, 0, 0, 0, 93, 3, 7, 100, 2, 17, 222],
  "TOTAL (U.TS.)": [48, 6, 3, 7, 138, 118, 79, 217, 30, 46, 692],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 1, 0, 23, 64, 72, 7, 0, 65, 232],
  "Bangalore": [0, 0, 0, 0, 161, 178, 200, 122, 25, 250, 936],
  "Bombay": [0, 0, 14, 0, 29, 32, 7, 30, 9, 81, 202],
  "Calcutta": [0, 0, 5, 0, 4, 0, 0, 13, 1, 0, 23],
  "Delhi": [46, 4, 1, 7, 14, 94, 9, 47, 18, 15, 255],
  "Hyderabad": [1, 0, 1, 0, 28, 22, 9, 16, 1, 9, 87],
  "Kanpur": [17, 7, 12, 1, 9, 10, 21, 22, 8, 36, 143],
  "Madras": [0, 0, 0, 0, 58, 50, 41, 42, 7, 65, 263],
  "TOTAL (CITIES)": [64, 11, 34, 8, 326, 450, 359, 299, 69, 521, 2141],
 },
 "Grand": {"GRAND TOTAL": [2670, 232, 498, 341, 9781, 3095, 7193, 9621, 554, 7678, 41663]},
}
