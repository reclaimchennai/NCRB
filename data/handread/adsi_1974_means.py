# ADSI 1974, Appendix VI: suicides by means with percentage to total, States / UTs / cities
# (raw/adsi/1974/table_content/1680155263appendix-61974.pdf, pages 1-4, printed sideways: pages 1-2 Railways to Fire,
# pages 3-4 Drowning to Total). Read from the page images; '..' (nil) is 0; percentages left out. The same figures
# by sex are in Appendix IV (raw/adsi/1974/table_content/1680155320appendix-41974.pdf). Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1974, "adsi"
SOURCE = "raw/adsi/1974/table_content/1680155263appendix-61974.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of Suicidal Deaths by different Means with Percentage to Total Suicidal Deaths in States, Union Territories and Cities during 1974"
CATS = ["By Railways", "By Machine", "By Fire Arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Other causes", "Total"]
CORRECTIONS = {
    ("Delhi", "By Poison"): ("..", 9, "printed '..' with (5.5%); 9/164 = 5.5%, the row then adds up to 164 and the UTs' Poison column to 92; Appendix IV prints Delhi's poison as 6 male + 3 female"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [264, 1, 1, 10, 996, 135, 1131, 573, 22, 361, 3494],
  "Assam": [136, 10, 4, 2, 102, 38, 327, 634, 84, 164, 1501],
  "Bihar": [91, 12, 8, 53, 83, 163, 295, 99, 12, 265, 1081],
  "Gujarat": [56, 1, 15, 3, 436, 276, 259, 116, 14, 256, 1432],
  "Haryana": [34, 14, 17, 11, 29, 61, 208, 124, 5, 188, 691],
  "Himachal Pradesh": [1, 0, 2, 1, 13, 11, 9, 8, 4, 0, 49],
  "Jammu & Kashmir": [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2],
  "Karnataka": [55, 1, 5, 20, 716, 268, 840, 601, 35, 912, 3453],
  "Kerala": [2, 0, 2, 52, 1917, 12, 532, 1272, 11, 215, 4015],
  "Madhya Pradesh": [285, 10, 37, 136, 190, 367, 798, 807, 121, 1553, 4304],
  "Maharashtra": [136, 5, 15, 34, 1239, 332, 935, 473, 194, 384, 3747],
  "Manipur": [0, 0, 0, 0, 5, 1, 0, 5, 0, 0, 11],
  "Meghalaya": [0, 0, 0, 0, 11, 2, 8, 12, 1, 42, 76],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 6, 0, 3, 9],
  "Orissa": [294, 20, 2, 5, 497, 10, 247, 354, 9, 689, 2127],
  "Punjab": [250, 8, 15, 7, 20, 12, 54, 48, 5, 152, 571],
  "Rajasthan": [55, 4, 8, 7, 17, 33, 226, 49, 7, 122, 528],
  "Tamil Nadu": [61, 5, 4, 139, 1942, 424, 855, 749, 44, 1184, 5407],
  "Tripura": [0, 0, 0, 1, 275, 10, 0, 94, 0, 46, 426],
  "Uttar Pradesh": [378, 57, 220, 71, 206, 357, 647, 473, 89, 1112, 3610],
  "West Bengal": [446, 8, 10, 20, 4024, 221, 457, 1891, 34, 1793, 8904],
  "TOTAL (STATES)": [2544, 156, 365, 572, 12718, 2733, 7829, 8389, 691, 9441, 45438],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 1, 1, 0, 8, 3, 22, 23, 1, 26, 85],
  "Arunachal Pradesh": [0, 0, 0, 0, 0, 0, 1, 4, 0, 0, 5],
  "Chandigarh": [0, 0, 0, 1, 1, 0, 2, 1, 0, 0, 5],
  "D. & N. Haveli": [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 6],
  "Delhi": [30, 0, 4, 5, 9, 21, 29, 19, 11, 36, 164],
  "Goa, Daman & Diu": [0, 0, 0, 0, 11, 3, 24, 4, 0, 1, 43],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2],
  "Pondicherry": [0, 0, 0, 0, 63, 4, 45, 36, 0, 112, 260],
  "TOTAL (U.TS.)": [30, 1, 5, 6, 92, 31, 123, 95, 12, 175, 570],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 1, 0, 16, 46, 14, 5, 1, 1, 84],
  "Bangalore": [0, 1, 0, 0, 206, 33, 88, 29, 4, 122, 483],
  "Bombay": [1, 0, 11, 7, 40, 27, 13, 21, 2, 22, 144],
  "Calcutta": [0, 0, 0, 0, 5, 3, 9, 17, 3, 0, 37],
  "Delhi": [30, 0, 4, 3, 9, 13, 12, 15, 6, 14, 106],
  "Hyderabad": [0, 1, 0, 2, 64, 37, 67, 11, 7, 38, 227],
  "Kanpur": [16, 0, 0, 0, 9, 7, 30, 15, 0, 12, 89],
  "Madras": [3, 0, 0, 0, 185, 70, 106, 102, 1, 82, 549],
  "TOTAL (CITIES)": [50, 2, 16, 12, 534, 236, 339, 215, 24, 291, 1719],
 },
 "Grand": {"GRAND TOTAL": [2574, 157, 370, 578, 12810, 2764, 7952, 8484, 703, 9616, 46008]},
}
