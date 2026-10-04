# ADSI 1982, Appendix VI: suicides by means adopted with percentage to total, States / UTs / cities
# (raw/adsi/1982/table_content/1680161585appendix-61982.pdf, pages 1-5, printed sideways: pages 1-3 Railways to Fire
# (States, UTs and Grand Total, cities), pages 4-5 Drowning to Total). Only the counts are recorded; the printed
# percentages were used to confirm readings. '—' is 0; N.A. (not available) is None: Lucknow is printed N.A. across
# the row. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1982, "adsi"
SOURCE = "raw/adsi/1982/table_content/1680161585appendix-61982.pdf"
PAGES = "1-5"
TITLE = "Appendix VI: Distribution of the Suicidal Deaths by Different Means with Percentage to Total Suicidal Deaths in States/U.Ts./Cities during 1982"
CATS = ["By Railways", "By Machine", "By Fire-arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Other Causes", "Total"]
NA = None
CORRECTIONS = {
    ("Gujarat", "By Poison"): (85, 485, "printed '85(27.1)' with the first digit lost; 485/1793 = 27.1% (85 gives 4.7%), the row then adds up to its printed 1,793 and the States' Poison column to the printed 11,348"),
    ("West Bengal", "Total"): (6818, 6881, "printed 6,818 with two digits transposed; the row adds up to 6,881, the States' Total column then adds up to the printed 43,720, and the row's percentages fit 6,881 (2722/6881 = 39.6%, 2263/6881 = 32.9%, 939/6881 = 13.6%; with 6,818 they would be 39.9, 33.2, 13.8)"),
    ("Pondicherry", "By Hanging"): (145, 151, "printed '145(42.9)'; 151/352 = 42.9% (145 gives 41.2%), the row then adds up to its printed 352 and the UTs' Hanging column to the printed 363"),
    ("GRAND TOTAL", "By Weapons"): (385, 185, "printed '385(0.4)'; States 177 + UTs 8 = 185 and 185/44732 = 0.4% (385 gives 0.9%); the Grand Total row then adds up to its printed 44,732"),
    ("Madhya Pradesh", "By Weapons"): (10, 11, "printed '10(0.3)' (clear); the row's categories add up to 3,050 against its printed 3,051 and the States' Weapons column to 176 against the printed 177, both fixed by 11. The printed percentage does not decide it: this row's percentages do not fit its own printed figures (475 printed 15.5% for 15.6, 26 0.8% for 0.9, 282 9.3% for 9.2, 284 9.4% for 9.3, 552 18.2% for 18.1), so they were worked from slightly different figures; 11/3051 = 0.36%"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [285, 0, 3, 4, 750, 164, 766, 468, 69, 481, 2990],
  "Assam": [59, 15, 7, 4, 76, 36, 396, 655, 8, 449, 1705],
  "Bihar": [65, 23, 13, 1, 92, 87, 87, 151, 28, 167, 714],
  "Gujarat": [128, 1, 3, 4, 485, 379, 431, 220, 33, 109, 1793],
  "Haryana": [23, 5, 13, 0, 59, 76, 104, 160, 5, 16, 461],
  "Himachal Pradesh": [0, 0, 2, 0, 20, 4, 9, 10, 6, 39, 90],
  "Jammu & Kashmir": [9, 0, 0, 1, 2, 1, 3, 3, 2, 1, 22],
  "Karnataka": [1, 370, 15, 4, 964, 263, 1483, 1017, 98, 1080, 5295],
  "Kerala": [259, 1, 4, 34, 1649, 70, 571, 1771, 9, 245, 4613],
  "Madhya Pradesh": [475, 8, 26, 11, 342, 282, 284, 983, 88, 552, 3051],
  "Maharashtra": [168, 48, 9, 9, 972, 603, 812, 623, 77, 569, 3890],
  "Manipur": [0, 0, 0, 0, 5, 0, 9, 6, 0, 21, 41],
  "Meghalaya": [0, 0, 0, 1, 2, 3, 1, 24, 0, 5, 36],
  "Nagaland": [0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 5],
  "Orissa": [207, 2, 0, 3, 559, 25, 231, 649, 4, 623, 2303],
  "Punjab": [166, 1, 13, 0, 27, 31, 29, 66, 16, 10, 359],
  "Rajasthan": [54, 3, 11, 4, 96, 98, 288, 185, 24, 174, 937],
  "Sikkim": [0, 0, 0, 0, 0, 1, 1, 14, 1, 0, 17],
  "Tamil Nadu": [63, 13, 1, 3, 2204, 512, 706, 920, 34, 1034, 5490],
  "Tripura": [0, 0, 4, 0, 192, 9, 26, 228, 0, 91, 550],
  "Uttar Pradesh": [312, 45, 214, 85, 130, 223, 141, 266, 30, 1031, 2477],
  "West Bengal": [221, 0, 14, 9, 2722, 353, 285, 2263, 75, 939, 6881],
  "TOTAL (STATES)": [2495, 535, 352, 177, 11348, 3220, 6666, 10683, 608, 7636, 43720],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 1, 0, 21, 5, 3, 42, 0, 0, 72],
  "Arunachal Pradesh": [0, 0, 1, 2, 2, 0, 1, 15, 2, 0, 23],
  "Chandigarh": [0, 0, 0, 3, 0, 5, 2, 11, 0, 0, 21],
  "D & N Haveli": [0, 0, 0, 0, 1, 0, 1, 13, 0, 0, 15],
  "Delhi": [20, 1, 3, 3, 53, 183, 12, 96, 18, 46, 435],
  "Goa, Daman & Diu": [1, 0, 0, 0, 10, 9, 26, 32, 4, 4, 86],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
  "Mizoram": [0, 0, 0, 0, 0, 1, 2, 3, 0, 1, 7],
  "Pondicherry": [1, 0, 0, 0, 123, 15, 21, 151, 0, 41, 352],
  "TOTAL (U.TS.)": [22, 1, 5, 8, 210, 218, 69, 363, 24, 92, 1012],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 0, 17, 63, 76, 9, 9, 11, 185],
  "Bangalore": [0, 0, 1, 0, 113, 168, 96, 97, 86, 157, 718],
  "Bombay": [2, 0, 1, 2, 31, 66, 20, 52, 10, 23, 207],
  "Calcutta": [0, 0, 0, 0, 9, 8, 2, 20, 2, 0, 41],
  "Delhi": [20, 1, 3, 3, 48, 181, 10, 88, 18, 45, 417],
  "Hyderabad": [0, 0, 0, 0, 29, 24, 47, 27, 0, 61, 188],
  "Jaipur": [6, 0, 0, 0, 13, 18, 33, 18, 3, 35, 126],
  "Kanpur": [4, 0, 5, 0, 0, 10, 3, 8, 2, 12, 44],
  "Lucknow": [NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA],
  "Madras": [0, 0, 0, 1, 149, 73, 42, 164, 5, 28, 462],
  "Nagpur": [7, 2, 4, 0, 49, 39, 20, 7, 3, 65, 196],
  "Pune": [0, 1, 0, 3, 16, 54, 27, 30, 3, 6, 140],
  "TOTAL (CITIES)": [39, 4, 14, 9, 474, 704, 376, 520, 141, 443, 2724],
 },
 "Grand": {"GRAND TOTAL": [2517, 536, 357, 185, 11558, 3438, 6735, 11046, 632, 7728, 44732]},
}
