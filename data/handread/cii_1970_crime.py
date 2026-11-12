# CII 1970, Table 5: incidence of crime under different heads during 1969 and 1970 showing percentage variation, States / U.Ts. /
# cities (raw/cii/1970/table_content/table-5-1970.pdf, pages 1-6 = printed pp. 10-15), 1970 columns only (the 1969 and
# percentage-variation columns are skipped). Read from the page images. Table 5 prints no total of cognizable crime, so the last
# column is the 1970 column of Table 4 of the same edition, incidence of total cognizable crime in States, U.Ts. and cities
# (raw/cii/1970/table_content/table-4-1970.pdf page 2, col. 9). "-" (nil) is entered as 0. No "other IPC crimes" column is
# printed, so each column is checked against the printed TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and TOTAL (cities) by
# scripts/check_handread.py. Every printed column added up as read: nothing was corrected.
# Thefts: the table prints "Cattle thefts" (cols 18-20) and "Ordinary thefts" (cols 21-23) separately, but for Madhya Pradesh the
# cattle thefts cell reads "Combined with ordinary thefts" and its ordinary thefts figure (30,209*) is footnoted "inclusive of
# Cattle Thefts"; the printed cattle thefts State total (21,809) leaves Madhya Pradesh out. So the two columns are entered here
# added together as "Thefts" (the head CII 1971 prints), which is exact for every place. The printed 1970 columns, each of which
# adds up to its printed totals, in the row order of ROWS:
#   Cattle thefts:   States 680, 540, 657, 762, 346, 35, 199, 136, - (Madhya Pradesh), 1625, 58, 599, 1, 717, 188, 1830, 1627, 261, 10280, 1268, TOTAL 21809;
#                    U.Ts. 1, 9, 2, 203, 4, 0, 20, TOTAL 239; GRAND TOTAL 22048; Cities 26, 28, 67, 22, 142, 8, 49, 48, TOTAL 390
#   Ordinary thefts: States 10714, 6670, 25597, 9956, 2233, 401, 1038, 5259, 30209, 41053, 408, 10089, 300, 11768, 2696, 7399, 17730, 980, 82394, 28497, TOTAL 295391;
#                    U.Ts. 73, 871, 29, 17804, 367, 10, 618, TOTAL 19772; GRAND TOTAL 315163; Cities 1243, 3591, 13573, 5147, 17026, 1900, 3656, 4550, TOTAL 50686
# West Bengal House-breaking is printed "99,79" (misplaced comma) = 9,979 (-6.99% on 10,729). The Cities block of page 6 (Cheating,
# Counterfeiting) is smudged; each figure there was read at 600 dpi and agrees with its printed percentage variation on 1969.
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Thefts (cattle + ordinary), Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime (Table 4)
KIND, YEAR, PUB = "crime", 1970, "cii"
SOURCE = "raw/cii/1970/table_content/table-5-1970.pdf"
PAGES = "1-6"
TITLE = "Table 5: Incidence of crime under different heads during 1969 and 1970 showing percentage variation (1970 figures; cattle and ordinary thefts added together); total from Table 4 (table-4-1970.pdf p. 2)"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Thefts", "Riots",
        "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [1092, 149, 137, 190, 4919, 11394, 3388, 655, 378, 17, 43942],
  "Assam": [500, 511, 195, 240, 4382, 7210, 3111, 408, 291, 8, 25908],
  "Bihar": [1523, 581, 1626, 1045, 20635, 26254, 10239, 1274, 493, 110, 84091],
  "Gujarat": [734, 246, 56, 354, 4188, 10718, 484, 971, 527, 8, 32225],
  "Haryana": [192, 145, 12, 23, 1715, 2579, 107, 278, 168, 3, 8902],
  "Himachal Pradesh": [42, 57, 1, 28, 366, 436, 49, 85, 60, 0, 2381],
  "Jammu & Kashmir": [59, 190, 12, 12, 840, 1237, 736, 98, 79, 1, 6421],
  "Kerala": [372, 75, 42, 154, 3414, 5395, 4269, 381, 196, 59, 31617],
  "Madhya Pradesh": [1725, 970, 416, 881, 16430, 30209, 2170, 1110, 1011, 19, 83537],
  "Maharashtra": [1356, 543, 391, 1532, 14497, 42678, 2043, 3030, 1644, 57, 96552],
  "Manipur": [51, 166, 10, 33, 175, 466, 311, 52, 67, 0, 2122],
  "Mysore": [694, 125, 81, 136, 6193, 10688, 1953, 768, 530, 33, 35566],
  "Nagaland": [24, 9, 13, 23, 148, 301, 14, 15, 9, 0, 744],
  "Orissa": [389, 117, 104, 227, 6832, 12485, 1992, 589, 282, 3, 31514],
  "Punjab": [574, 301, 0, 28, 1524, 2884, 44, 405, 277, 6, 12478],
  "Rajasthan": [655, 1128, 111, 863, 6827, 9229, 3381, 762, 766, 10, 36230],
  "Tamil Nadu": [890, 297, 94, 107, 6658, 19357, 3057, 1244, 824, 234, 63619],
  "Tripura": [28, 24, 21, 38, 336, 1241, 336, 27, 19, 0, 2704],
  "Uttar Pradesh": [3502, 3051, 5202, 9710, 52006, 92674, 14015, 7796, 2803, 38, 233754],
  "West Bengal": [1140, 863, 1271, 947, 9979, 29765, 16337, 1805, 961, 17, 84528],
  "TOTAL (STATES)": [15542, 9548, 9795, 16571, 162064, 317200, 68036, 21753, 11385, 623, 918835],
 },
 "U.Ts.": {
  "A. & N. Islands": [8, 1, 0, 2, 30, 74, 16, 11, 1, 0, 308],
  "Chandigarh": [12, 16, 1, 2, 133, 880, 9, 46, 45, 0, 1484],
  "Dadra & Nagar Haveli": [5, 0, 3, 5, 26, 31, 0, 4, 0, 0, 106],
  "Delhi": [123, 531, 29, 363, 3601, 18007, 201, 772, 861, 25, 31241],
  "Goa, Daman & Diu": [14, 8, 4, 13, 342, 371, 21, 60, 18, 0, 1195],
  "Laccadives": [0, 1, 0, 0, 6, 10, 0, 0, 1, 0, 28],
  "Pondicherry": [4, 6, 5, 2, 137, 638, 48, 33, 20, 2, 2225],
  "TOTAL (U.TS.)": [166, 563, 42, 387, 4275, 20011, 295, 926, 946, 27, 36587],
 },
 "Cities": {
  "Ahmedabad": [25, 54, 1, 14, 343, 1269, 58, 84, 84, 3, 3269],
  "Bangalore": [20, 20, 1, 26, 1409, 3619, 118, 152, 243, 12, 7778],
  "Bombay": [146, 178, 30, 225, 1903, 13640, 338, 1014, 731, 40, 25763],
  "Calcutta": [157, 131, 18, 72, 819, 5169, 1217, 429, 321, 2, 10588],
  "Delhi": [100, 478, 17, 298, 3074, 17168, 178, 734, 825, 25, 28890],
  "Hyderabad": [21, 16, 2, 36, 662, 1908, 93, 74, 113, 0, 3470],
  "Kanpur": [40, 154, 40, 262, 1370, 3705, 242, 831, 304, 2, 8656],
  "Madras": [26, 35, 0, 1, 162, 4598, 75, 444, 423, 60, 10794],
  "TOTAL (CITIES)": [535, 1066, 109, 934, 9742, 51076, 2319, 3762, 3044, 144, 99208],
 },
 "Grand": {"GRAND TOTAL": [15708, 10111, 9837, 16958, 166339, 337211, 68331, 22679, 12331, 650, 955422]},
}
