# ADSI 1981, Appendix VI: suicides by means adopted with percentage to total, States / UTs / cities
# (raw/adsi/1981/table_content/1680161137appendix-61881.pdf, pages 1-4, printed sideways: pages 1-2 Railways to Fire,
# pages 3-4 Drowning to Total). Only the counts are recorded; the printed percentages were used to confirm readings.
# '—' (0.0) is 0; N.A. (not available) is None. Lucknow is printed "Not Available" across the row,
# and Tamil Nadu's suicides by weapons are printed N.A. (the row adds up to its printed 4,836 without them).
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1981, "adsi"
SOURCE = "raw/adsi/1981/table_content/1680161137appendix-61881.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of the Suicidal Deaths by Different Means with Percentage to Total Suicidal Deaths in States/U.Ts./Cities during 1981"
CATS = ["By Railways", "By Machine", "By Fire-Arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Other causes", "Total"]
NA = None
CORRECTIONS = {
    ("Nagaland", "By Hanging"): (6, 8, "printed '6(66.7)'; 8/12 = 66.7% (6/12 = 50%), the row then adds up to its printed 12 and the States' Hanging column to the printed 9,225"),
    ("Tamil Nadu", "By Fire-Arms"): (45, 46, "printed '45(1.0)'; 46/4836 = 1.0% (45 gives 0.9%), the row then adds up to its printed 4,836 and the States' Fire-Arms column to the printed 518"),
    ("Pondicherry", "By Poison"): (6, 76, "printed '6(33.8)' with a digit lost; 76/225 = 33.8%, the row then adds up to its printed 225 and the UTs' Poison column to the printed 146"),
    ("Uttar Pradesh", "By Fire"): ("295", 296, "last digit smudged (5 or 6); 296 makes the row add up to its printed 3,077 and the States' Fire column to the printed 3,403 (296/3077 = 9.6%, as printed; a reading, not a change)"),
    ("West Bengal", "By Poison"): ("2,285", 2286, "last digit smudged (5 or 6); 2,286 makes the row add up to its printed 6,544 and the States' Poison column to the printed 8731 (2286/6544 = 34.9%, as printed; a reading, not a change)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [297, 6, 5, 10, 587, 274, 811, 400, 2, 523, 2915],
  "Assam": [92, 5, 3, 4, 65, 33, 339, 729, 22, 649, 1941],
  "Bihar": [48, 28, 11, 5, 48, 44, 42, 72, 11, 131, 440],
  "Gujarat": [107, 1, 8, 2, 424, 356, 407, 159, 32, 129, 1625],
  "Haryana": [75, 3, 8, 2, 31, 107, 96, 159, 13, 106, 600],
  "Himachal Pradesh": [0, 1, 3, 0, 17, 3, 14, 9, 6, 32, 85],
  "Jammu & Kashmir": [0, 0, 4, 0, 0, 6, 2, 2, 0, 5, 19],
  "Karnataka": [47, 7, 14, 93, 772, 203, 1289, 797, 121, 599, 3942],
  "Kerala": [259, 1, 3, 6, 1510, 38, 501, 1530, 16, 232, 4096],
  "Madhya Pradesh": [164, 29, 34, 23, 365, 283, 326, 905, 39, 376, 2544],
  "Maharashtra": [116, 2, 11, 8, 658, 507, 860, 502, 62, 534, 3260],
  "Manipur": [0, 0, 1, 0, 3, 0, 0, 2, 0, 0, 6],
  "Meghalaya": [0, 0, 0, 0, 0, 0, 4, 17, 0, 10, 31],
  "Nagaland": [0, 0, 0, 2, 0, 1, 0, 8, 0, 1, 12],
  "Orissa": [213, 0, 2, 0, 453, 38, 291, 534, 1, 348, 1880],
  "Punjab": [91, 0, 16, 3, 23, 50, 31, 60, 3, 4, 281],
  "Rajasthan": [47, 1, 12, 4, 74, 120, 249, 151, 6, 175, 839],
  "Sikkim": [0, 0, 0, 0, 1, 0, 0, 18, 2, 0, 21],
  "Tamil Nadu": [151, 44, 46, NA, 866, 661, 912, 823, 45, 1288, 4836],
  "Tripura": [0, 0, 1, 0, 196, 5, 22, 182, 5, 25, 436],
  "Uttar Pradesh": [508, 36, 323, 218, 352, 296, 301, 330, 96, 617, 3077],
  "West Bengal": [383, 10, 13, 5, 2286, 378, 375, 1836, 16, 1242, 6544],
  "TOTAL (STATES)": [2598, 174, 518, 385, 8731, 3403, 6872, 9225, 498, 7026, 39430],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 13, 1, 7, 18, 0, 0, 39],
  "Arunachal Pradesh": [0, 0, 1, 0, 1, 1, 0, 15, 0, 2, 20],
  "Chandigarh": [0, 0, 0, 0, 1, 9, 1, 4, 2, 0, 17],
  "D & N Haveli": [0, 0, 0, 0, 0, 0, 2, 14, 0, 0, 16],
  "Delhi": [28, 0, 3, 1, 42, 140, 19, 111, 22, 31, 397],
  "Goa, Daman & Diu": [1, 0, 0, 1, 13, 6, 30, 33, 2, 0, 86],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
  "Mizoram": [0, 0, 2, 0, 0, 0, 1, 9, 1, 1, 14],
  "Pondicherry": [5, 0, 0, 0, 76, 8, 7, 129, 0, 0, 225],
  "TOTAL (U.TS.)": [34, 0, 6, 2, 146, 165, 67, 333, 27, 35, 815],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 1, 0, 24, 50, 78, 10, 3, 12, 178],
  "Bangalore": [2, 0, 0, 1, 140, 109, 107, 109, 92, 130, 690],
  "Bombay": [0, 0, 2, 3, 24, 62, 19, 48, 12, 31, 201],
  "Calcutta": [0, 0, 0, 0, 1, 4, 0, 17, 3, 0, 25],
  "Delhi": [28, 0, 3, 0, 37, 128, 11, 100, 18, 21, 346],
  "Hyderabad": [0, 1, 0, 2, 45, 39, 19, 9, 0, 26, 141],
  "Jaipur": [7, 0, 0, 0, 11, 11, 15, 3, 0, 40, 87],
  "Kanpur": [11, 3, 4, 0, 0, 8, 6, 13, 2, 3, 50],
  "Lucknow": [NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA],
  "Madras": [0, 0, 0, 0, 228, 145, 67, 249, 7, 0, 696],
  "Nagpur": [2, 1, 1, 0, 4, 37, 79, 13, 9, 7, 153],
  "Pune": [0, 0, 1, 2, 23, 27, 22, 30, 4, 2, 111],
  "TOTAL (CITIES)": [50, 5, 12, 8, 537, 620, 423, 601, 150, 272, 2678],
 },
 "Grand": {"GRAND TOTAL": [2632, 174, 524, 387, 8877, 3568, 6939, 9558, 525, 7061, 40245]},
}
