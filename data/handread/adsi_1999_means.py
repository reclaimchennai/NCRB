# ADSI 1999, Table 26: suicides by means adopted, States / UTs / cities (raw/adsi/1999/archived/table-26_1999.pdf,
# pages 1-9: pages 1-8 each carry two categories by Male / Female / Total / % Share for every place, page 9 the Total
# by Male / Female / Total / % Share). The running page header wrongly reads "Accidental Deaths & Suicides in India -
# 1998"; the figures are 1999's (Total All-India 1,10,587, the 1999 count). Only the Total column of each category is
# recorded. Read from the page images. Nothing is printed N.A.; Lakshadweep is printed 0 throughout with "-" for its
# shares. Totals rows are printed for States, UTs, All-India and Cities. Checks run on the full Male / Female / Total
# transcription: Male + Female = Total in every cell; the Male, Female and Total columns each add to Total (States),
# Total (UTs) and Total (Cities), and States + UTs = Total All-India; every row's 16 categories add to its printed Total
# for Male, Female and Total; every printed % share equals the category's share of the row Total (to 0.01). All pass
# as printed, so no figure is changed. No suicide_incidence hand-read file exists for 1999 to cross-check against.
# Carry-over: the rows for Bihar (1795), Goa (256), Lucknow (112) and Patna (43) are identical, figure for figure in all
# 16 categories and by sex (Bihar 960 + 835), to the 1998 Table 26 rows (data/handread/adsi_1998_means.py), checked
# on both page images. NCRB's 1999 incidence table prints the same totals as 1998 for these four places, so the 1998
# figures were apparently repeated where 1999 returns were not received. They are kept as printed but are probably
# not 1999's own figures.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1999, "adsi"
SOURCE = "raw/adsi/1999/archived/table-26_1999.pdf"
PAGES = "1-9"
TITLE = "Table 26: Distribution of Suicides By Means adopted (State, UT & City-wise) - 1999"
CATS = ["By Over Alcoholism", "By Drowning", "By Fire/Self Immolation", "By Fire-Arms", "By Hanging",
        "Poison (By Consuming Insecticides)", "By Consuming Other Poison", "By Self Infliction of Injury",
        "By Jumping from (Building)", "By Jumping from (Other Sites)", "By Jumping off Moving Vehicles/Trains",
        "By Machine", "By Overdose of Sleeping pills", "By Touching Electric Wires",
        "By Coming under Running Vehicles/Trains", "By Other Means", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [238, 1026, 1209, 63, 1926, 3151, 1471, 19, 110, 57, 1, 41, 70, 118, 408, 478, 10386],
  "Arunachal Pradesh": [0, 2, 6, 0, 61, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 74],
  "Assam": [6, 408, 2, 21, 1300, 9, 353, 27, 1, 3, 56, 2, 0, 55, 22, 270, 2535],
  "Bihar": [53, 157, 182, 34, 402, 185, 268, 28, 35, 24, 1, 4, 48, 18, 19, 337, 1795],
  "Goa": [6, 57, 26, 1, 103, 5, 37, 1, 2, 4, 8, 0, 1, 2, 2, 1, 256],
  "Gujarat": [11, 356, 1040, 60, 786, 1041, 1268, 47, 22, 39, 6, 3, 25, 33, 197, 52, 4986],
  "Haryana": [18, 145, 313, 20, 283, 467, 422, 75, 7, 2, 8, 0, 29, 54, 124, 330, 2297],
  "Himachal Pradesh": [6, 15, 10, 9, 62, 58, 158, 0, 0, 0, 1, 0, 0, 0, 0, 7, 326],
  "Jammu & Kashmir": [0, 6, 1, 3, 11, 21, 19, 0, 2, 26, 0, 0, 0, 3, 4, 2, 98],
  "Karnataka": [238, 1426, 1269, 29, 2974, 1334, 3695, 33, 91, 237, 1, 0, 131, 68, 297, 665, 12488],
  "Kerala": [19, 874, 546, 1, 3915, 2123, 1782, 41, 30, 47, 44, 0, 52, 37, 192, 75, 9778],
  "Madhya Pradesh": [193, 790, 1146, 50, 2525, 2396, 1573, 183, 52, 89, 33, 22, 252, 122, 276, 0, 9702],
  "Maharashtra": [124, 1778, 2432, 14, 3221, 3222, 1433, 32, 48, 70, 67, 12, 39, 36, 229, 837, 13594],
  "Manipur": [0, 0, 0, 1, 15, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 24],
  "Meghalaya": [0, 6, 3, 2, 43, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56],
  "Mizoram": [0, 0, 0, 3, 20, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 28],
  "Nagaland": [0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 15],
  "Orissa": [3, 193, 68, 9, 1072, 234, 1200, 2, 12, 36, 4, 0, 2, 30, 126, 661, 3652],
  "Punjab": [10, 53, 54, 16, 94, 50, 205, 1, 1, 0, 0, 0, 25, 8, 282, 187, 986],
  "Rajasthan": [100, 434, 327, 18, 719, 722, 449, 0, 18, 45, 61, 24, 73, 64, 199, 490, 3743],
  "Sikkim": [6, 14, 6, 0, 44, 3, 1, 0, 1, 0, 0, 0, 0, 3, 0, 30, 108],
  "Tamil Nadu": [90, 941, 1710, 5, 1627, 1045, 3575, 140, 127, 50, 13, 61, 107, 90, 466, 1401, 11448],
  "Tripura": [5, 0, 6, 0, 367, 297, 121, 0, 0, 0, 0, 0, 23, 18, 0, 101, 938],
  "Uttar Pradesh": [71, 391, 1113, 175, 1335, 1204, 243, 46, 17, 35, 52, 10, 55, 119, 200, 410, 5476],
  "West Bengal": [120, 484, 515, 12, 4075, 2356, 2461, 54, 65, 75, 69, 34, 161, 110, 791, 2507, 13889],
  "TOTAL (STATES)": [1317, 9563, 11984, 546, 26987, 19924, 20745, 729, 641, 839, 425, 213, 1097, 988, 3834, 8846, 108678],
 },
 "U.Ts.": {
  "A & N Islands": [0, 3, 7, 0, 106, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 132],
  "Chandigarh": [0, 2, 7, 1, 11, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 36, 70],
  "D & N Haveli": [0, 3, 1, 0, 23, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32],
  "Daman & Diu": [0, 3, 3, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
  "Delhi": [6, 4, 233, 3, 413, 148, 117, 8, 15, 11, 4, 0, 11, 5, 12, 41, 1031],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [0, 7, 86, 0, 336, 177, 21, 0, 1, 0, 1, 0, 4, 1, 0, 0, 634],
  "TOTAL (U.TS.)": [6, 22, 337, 4, 891, 327, 172, 8, 16, 11, 5, 0, 15, 6, 12, 77, 1909],
 },
 "Cities": {
  "Ahmedabad": [1, 35, 145, 0, 64, 59, 99, 0, 6, 0, 0, 0, 3, 3, 1, 0, 416],
  "Bangalore": [47, 101, 311, 1, 554, 217, 575, 12, 28, 67, 1, 0, 10, 13, 1, 0, 1938],
  "Bhopal": [1, 22, 52, 0, 54, 97, 20, 0, 2, 1, 0, 0, 12, 0, 6, 0, 267],
  "Calcutta": [6, 26, 35, 0, 104, 0, 26, 0, 0, 5, 5, 0, 3, 0, 0, 0, 210],
  "Chennai": [28, 39, 163, 0, 382, 26, 142, 0, 18, 0, 0, 0, 9, 4, 0, 331, 1142],
  "Coimbatore": [4, 5, 60, 1, 59, 0, 116, 1, 5, 0, 0, 0, 2, 2, 0, 0, 255],
  "Delhi": [6, 3, 197, 3, 353, 98, 70, 8, 14, 11, 4, 0, 11, 5, 12, 40, 835],
  "Hyderabad": [10, 51, 182, 3, 99, 0, 139, 11, 3, 0, 0, 0, 1, 0, 0, 40, 539],
  "Indore": [43, 54, 116, 0, 67, 96, 43, 17, 15, 7, 0, 16, 12, 7, 0, 0, 493],
  "Jaipur": [0, 8, 39, 0, 67, 41, 90, 0, 5, 0, 0, 0, 15, 0, 4, 6, 275],
  "Kanpur": [0, 1, 134, 6, 113, 136, 0, 0, 0, 0, 1, 0, 0, 7, 2, 69, 469],
  "Kochi": [0, 21, 23, 0, 127, 0, 54, 0, 2, 0, 4, 0, 1, 2, 9, 0, 243],
  "Lucknow": [0, 2, 3, 3, 45, 36, 5, 0, 6, 0, 0, 0, 5, 0, 7, 0, 112],
  "Ludhiana": [0, 0, 4, 2, 13, 9, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 30],
  "Madurai": [0, 0, 55, 0, 18, 0, 22, 0, 0, 0, 0, 0, 4, 0, 0, 0, 99],
  "Mumbai": [12, 62, 321, 7, 655, 21, 40, 3, 19, 57, 0, 3, 27, 5, 34, 0, 1266],
  "Nagpur": [2, 86, 125, 1, 104, 24, 27, 5, 0, 0, 0, 0, 1, 0, 9, 1, 385],
  "Patna": [12, 0, 0, 0, 9, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 13, 43],
  "Pune": [0, 34, 107, 0, 194, 27, 53, 1, 2, 0, 0, 0, 0, 0, 4, 1, 423],
  "Surat": [1, 21, 76, 1, 64, 44, 115, 1, 7, 0, 0, 0, 0, 0, 0, 0, 330],
  "Vadodara": [0, 10, 56, 0, 33, 0, 68, 0, 3, 1, 0, 0, 5, 0, 0, 0, 176],
  "Varanasi": [1, 10, 7, 4, 12, 5, 0, 0, 2, 0, 3, 0, 0, 1, 5, 26, 76],
  "Vishakhapatnam": [7, 11, 25, 0, 44, 51, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 141],
  "TOTAL (CITIES)": [181, 602, 2236, 32, 3234, 987, 1715, 59, 139, 149, 18, 19, 122, 49, 94, 527, 10163],
 },
 "Grand": {
  "GRAND TOTAL": [1323, 9585, 12321, 550, 27878, 20251, 20917, 737, 657, 850, 430, 213, 1112, 994, 3846, 8923, 110587],
 },
}
