# ADSI 1983, Appendix VI: suicides by means adopted with percentage to total, States / UTs / cities
# (raw/adsi/1983/table_content/1680161900appendix-61983.pdf, pages 1-6, printed sideways: pages 1-3 Railways to Fire
# (States 1-17; States 18-22, UTs and Grand Total; cities), pages 4-6 Drowning to Total). Only the counts are
# recorded; the printed percentages were used to confirm readings. '—' is 0; N.A. (not available) is None: Lucknow is
# printed "not available" across the row. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1983, "adsi"
SOURCE = "raw/adsi/1983/table_content/1680161900appendix-61983.pdf"
PAGES = "1-6"
TITLE = "Appendix VI: Distribution of the Suicidal Deaths by Different Means with Percentage to Total Suicidal Deaths in States/U.Ts./Cities during 1983"
CATS = ["By Railways", "By Machine", "By Fire-Arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Other Causes", "Total"]
NA = None
CORRECTIONS = {
    ("West Bengal", "By Drowning"): ("2,79", 279, "printed '2,79(3.8)' with a stray comma; 279/7316 = 3.8% and the row adds up to its printed 7,316 (a reading of the printed digits, not a change)"),
    ("Orissa", "By Weapons"): ("(2.01)", 2, "printed '(2.01)', the bracket misplaced in '2(0.1)'; 2/2405 = 0.1% (a reading, not a change)"),
    ("TOTAL (U.TS.)", "By Fire"): ("23", 232, "printed '23(23.2)' with the last digit lost; the UTs add up to 232 (23.1% of 1,003), and the Grand Total 4,334 = 4,102 for the States + 232"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [343, 2, 3, 4, 828, 261, 760, 556, 63, 563, 3383],
  "Assam": [113, 35, 45, 32, 89, 85, 608, 857, 24, 548, 2436],
  "Bihar": [52, 17, 25, 12, 134, 100, 119, 151, 9, 135, 754],
  "Gujarat": [108, 4, 6, 3, 524, 435, 412, 184, 34, 65, 1775],
  "Haryana": [41, 0, 8, 1, 61, 128, 123, 164, 31, 37, 594],
  "Himachal Pradesh": [0, 0, 2, 2, 29, 13, 21, 17, 26, 56, 166],
  "Jammu & Kashmir": [6, 0, 1, 0, 5, 7, 8, 8, 4, 2, 41],
  "Karnataka": [63, 3, 10, 10, 1119, 538, 1250, 1059, 105, 573, 4730],
  "Kerala": [296, 0, 7, 15, 1822, 68, 555, 2065, 11, 402, 5241],
  "Madhya Pradesh": [364, 2, 16, 12, 506, 450, 300, 1000, 53, 454, 3157],
  "Maharashtra": [180, 3, 5, 11, 1001, 622, 849, 642, 85, 346, 3744],
  "Manipur": [0, 0, 2, 0, 2, 2, 11, 15, 0, 21, 53],
  "Meghalaya": [0, 0, 0, 0, 0, 3, 4, 17, 0, 0, 24],
  "Nagaland": [0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 4],
  "Orissa": [144, 2, 0, 2, 930, 17, 174, 808, 2, 326, 2405],
  "Punjab": [140, 0, 5, 2, 36, 24, 18, 68, 5, 13, 311],
  "Rajasthan": [95, 8, 17, 4, 106, 117, 324, 169, 5, 199, 1044],
  "Sikkim": [0, 0, 0, 0, 1, 2, 0, 11, 10, 10, 34],
  "Tamil Nadu": [330, 2, 3, 2, 1812, 622, 652, 1015, 23, 901, 5362],
  "Tripura": [1, 0, 2, 4, 204, 8, 52, 154, 0, 74, 499],
  "Uttar Pradesh": [292, 46, 212, 79, 135, 214, 114, 245, 29, 1137, 2503],
  "West Bengal": [226, 5, 12, 13, 3149, 386, 279, 2115, 64, 1067, 7316],
  "TOTAL (STATES)": [2794, 129, 381, 208, 12493, 4102, 6634, 11323, 583, 6929, 45576],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 15, 0, 3, 31, 0, 0, 49],
  "Arunachal Pradesh": [0, 0, 3, 0, 2, 0, 1, 21, 0, 6, 33],
  "Chandigarh": [0, 0, 0, 2, 0, 2, 8, 6, 0, 0, 18],
  "D & N Haveli": [0, 0, 0, 0, 0, 0, 4, 27, 0, 0, 31],
  "Delhi": [40, 0, 8, 0, 42, 208, 23, 79, 15, 17, 432],
  "Goa, Daman & Diu": [4, 0, 1, 0, 12, 12, 30, 33, 5, 2, 99],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
  "Mizoram": [0, 0, 4, 0, 1, 0, 3, 8, 0, 1, 17],
  "Pondicherry": [2, 0, 0, 0, 140, 10, 16, 155, 0, 0, 323],
  "TOTAL (U.TS.)": [46, 0, 16, 2, 212, 232, 88, 361, 20, 26, 1003],
 },
 "Cities": {
  "Ahmedabad": [0, 4, 0, 0, 16, 102, 54, 11, 11, 15, 213],
  "Bangalore": [0, 0, 1, 0, 135, 202, 110, 157, 3, 146, 754],
  "Bombay": [0, 0, 1, 6, 43, 115, 22, 60, 16, 34, 297],
  "Calcutta": [0, 0, 0, 0, 8, 9, 1, 37, 2, 0, 57],
  "Delhi": [40, 0, 8, 0, 30, 187, 21, 64, 15, 17, 382],
  "Hyderabad": [0, 0, 1, 2, 48, 47, 41, 26, 0, 88, 253],
  "Jaipur": [8, 0, 1, 0, 13, 10, 13, 6, 0, 3, 54],
  "Kanpur": [0, 0, 0, 0, 28, 30, 0, 31, 1, 1, 91],
  "Lucknow": [NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA],
  "Madras": [0, 0, 1, 0, 184, 145, 87, 325, 13, 143, 898],
  "Nagpur": [16, 2, 1, 0, 52, 44, 48, 12, 7, 64, 246],
  "Pune": [0, 0, 0, 0, 29, 37, 31, 24, 10, 8, 139],
  "TOTAL (CITIES)": [64, 6, 14, 8, 586, 928, 428, 753, 78, 519, 3384],
 },
 "Grand": {"GRAND TOTAL": [2840, 129, 397, 210, 12705, 4334, 6722, 11684, 603, 6955, 46579]},
}
