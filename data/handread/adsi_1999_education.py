# ADSI 1999, Table 25: educational status of suicide victims, States / UTs / cities
# (raw/adsi/1999/archived/table-25_1999.pdf, pages 1-5, printed pages 165-169: pages 1-4 each carry two levels of
# education by Male / Female / Total / % Share for every place, page 5 the Total by Male / Female / Total). Only the
# Total column of each level is recorded. Read from the page images (scanned at 150 dpi, rendered at zoom 3): every
# Male, Female and Total cell was transcribed and checked: Male + Female = Total in every cell; each row's eight levels
# add to page 5's Total for Male, Female and Total alike; every Male, Female and Total column adds to the printed Total
# States, Total UTs and Total (Cities), and Total States + Total UTs = Total All India (entered as GRAND TOTAL,
# 1,10,587). All of these held as printed, so nothing was corrected. Every row's Total equals that place's Total in the
# 1999 Table 26 (means, data/handread/adsi_1999_means.py). Nothing is printed N.A.; Lakshadweep is printed 0 throughout
# with "-" for its shares. Delhi appears as "Delhi (UT)" and "Delhi (City)".
# Carry-over: the rows for Bihar (1795), Goa (256), Lucknow (112) and Patna (43) are identical, level for level, to the
# 1998 Table 25 rows (data/handread/adsi_1998_education.py), as they are in the 1999 means table; no other row repeats
# 1998. Kept as printed: NCRB appears to have carried the 1998 figures for these two States and two cities into 1999.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "education", 1999, "adsi"
SOURCE = "raw/adsi/1999/archived/table-25_1999.pdf"
PAGES = "1-5"
TITLE = "Table 25: Educational Status of Suicide Victims during 1999 (State, UT & City-wise)"
NA = None
CATS = ["No Education", "Primary", "Middle", "Matriculate/Secondary", "Hr. Secondary/Intermediate/Pre-University",
        "Diploma", "Graduate", "Post Graduate and Above", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [4409, 2523, 1924, 949, 375, 60, 119, 27, 10386],
  "Arunachal Pradesh": [24, 11, 26, 7, 5, 0, 1, 0, 74],
  "Assam": [528, 551, 638, 518, 228, 32, 36, 4, 2535],
  "Bihar": [649, 404, 292, 246, 115, 15, 65, 9, 1795],
  "Goa": [52, 71, 58, 49, 18, 2, 5, 1, 256],
  "Gujarat": [1231, 1916, 844, 768, 168, 15, 39, 5, 4986],
  "Haryana": [808, 381, 376, 579, 121, 14, 15, 3, 2297],
  "Himachal Pradesh": [66, 47, 72, 93, 41, 3, 4, 0, 326],
  "Jammu & Kashmir": [24, 14, 22, 19, 8, 4, 3, 4, 98],
  "Karnataka": [4367, 3014, 2596, 1465, 780, 59, 141, 66, 12488],
  "Kerala": [616, 2382, 3328, 2350, 857, 66, 144, 35, 9778],
  "Madhya Pradesh": [2837, 2303, 2006, 1533, 684, 91, 157, 91, 9702],
  "Maharashtra": [2720, 3789, 3230, 2905, 686, 122, 117, 25, 13594],
  "Manipur": [3, 0, 7, 12, 0, 0, 2, 0, 24],
  "Meghalaya": [23, 9, 16, 6, 1, 1, 0, 0, 56],
  "Mizoram": [0, 6, 16, 4, 2, 0, 0, 0, 28],
  "Nagaland": [13, 1, 1, 0, 0, 0, 0, 0, 15],
  "Orissa": [1051, 830, 930, 540, 210, 25, 55, 11, 3652],
  "Punjab": [345, 180, 186, 183, 71, 6, 15, 0, 986],
  "Rajasthan": [1160, 782, 690, 693, 250, 20, 95, 53, 3743],
  "Sikkim": [49, 31, 21, 6, 0, 0, 1, 0, 108],
  "Tamil Nadu": [3875, 2128, 2558, 1431, 887, 245, 223, 101, 11448],
  "Tripura": [212, 381, 223, 85, 29, 0, 8, 0, 938],
  "Uttar Pradesh": [1796, 1202, 973, 677, 443, 131, 146, 108, 5476],
  "West Bengal": [3241, 4164, 2775, 1933, 1067, 220, 432, 57, 13889],
  "TOTAL (STATES)": [30099, 27120, 23808, 17051, 7046, 1131, 1823, 600, 108678],
 },
 "U.Ts.": {
  "A & N Islands": [22, 44, 40, 25, 0, 0, 1, 0, 132],
  "Chandigarh": [20, 11, 17, 18, 4, 0, 0, 0, 70],
  "D & N Haveli": [17, 6, 0, 9, 0, 0, 0, 0, 32],
  "Daman & Diu": [0, 3, 4, 3, 0, 0, 0, 0, 10],
  "Delhi (UT)": [216, 209, 220, 244, 114, 9, 16, 3, 1031],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [26, 110, 184, 225, 81, 3, 5, 0, 634],
  "TOTAL (U.TS.)": [301, 383, 465, 524, 199, 12, 22, 3, 1909],
 },
 "Cities": {
  "Ahmedabad": [42, 118, 93, 107, 46, 1, 9, 0, 416],
  "Bangalore": [625, 417, 374, 300, 169, 15, 34, 4, 1938],
  "Bhopal": [50, 17, 24, 111, 50, 7, 8, 0, 267],
  "Calcutta": [8, 39, 43, 52, 37, 0, 31, 0, 210],
  "Chennai": [307, 99, 437, 87, 175, 3, 24, 10, 1142],
  "Coimbatore": [44, 68, 78, 40, 18, 1, 5, 1, 255],
  "Delhi (City)": [171, 160, 182, 203, 91, 9, 16, 3, 835],
  "Hyderabad": [178, 120, 132, 62, 26, 2, 16, 3, 539],
  "Indore": [109, 97, 178, 65, 29, 9, 6, 0, 493],
  "Jaipur": [31, 105, 52, 54, 19, 0, 13, 1, 275],
  "Kanpur": [184, 131, 92, 49, 11, 2, 0, 0, 469],
  "Kochi": [16, 60, 87, 52, 22, 0, 6, 0, 243],
  "Lucknow": [20, 13, 32, 32, 12, 0, 3, 0, 112],
  "Ludhiana": [8, 2, 3, 8, 2, 1, 3, 3, 30],
  "Madurai": [18, 17, 62, 2, 0, 0, 0, 0, 99],
  "Mumbai": [168, 293, 345, 317, 100, 16, 27, 0, 1266],
  "Nagpur": [35, 75, 97, 128, 37, 5, 7, 1, 385],
  "Patna": [15, 7, 6, 7, 1, 0, 6, 1, 43],
  "Pune": [52, 116, 107, 108, 32, 7, 1, 0, 423],
  "Surat": [77, 133, 74, 42, 4, 0, 0, 0, 330],
  "Vadodara": [21, 66, 44, 37, 8, 0, 0, 0, 176],
  "Varanasi": [10, 18, 12, 17, 6, 5, 3, 5, 76],
  "Vishakhapatnam": [20, 22, 40, 33, 17, 3, 6, 0, 141],
  "TOTAL (CITIES)": [2209, 2193, 2594, 1913, 912, 86, 224, 32, 10163],
 },
 "Grand": {
  "GRAND TOTAL": [30400, 27503, 24273, 17575, 7245, 1143, 1845, 603, 110587],
 },
}
