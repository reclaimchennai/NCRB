# CII 1961 by crime head, States / U.Ts. / cities, assembled from the per-head appendices of the 1961 edition
# (raw/cii/1961/year_wise/1689771827appendicesall0.pdf): column 5 "cases reported during the year" of Appendix I (total cognizable
# crime, page 1), III murder (5), V kidnapping & abduction (9), VII dacoity (13), IX robbery (17), XI house-breaking (21), XIII cattle
# thefts (25), XV ordinary thefts (29), XVII riots (33), XIX criminal breach of trust (37), XXI cheating (41), XXIII counterfeiting
# (45). The edition prints no single State x head table. ".." (nil) entered as 0. Nagaland is listed under the Union Territories.
# No "other IPC crimes" column, so each column is checked against the printed TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and
# TOTAL (cities) by scripts/check_handread.py.
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts, Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime cases reported
KIND, YEAR, PUB = "crime", 1961, "cii"
SOURCE = "raw/cii/1961/year_wise/1689771827appendicesall0.pdf"
PAGES = "1,5,9,13,17,21,25,29,33,37,41,45"
TITLE = "Appendices I-XXIII (cases): cases reported during the year 1961 under total cognizable crime and each head, States/U.Ts./Cities"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Andhra Pradesh", "Total cognizable crimes (IPC)"): (32215, 33215, "printed 32215; the States add up to the printed TOTAL 609179 only with 33215, the row identity pending 2808 + 5270 + reported - not investigated 14354 = true cases 26939 gives 33215 (it holds for every other State), and the 1963 Survey's table of incidence in States (1689774215SURVEYOFCRIME.pdf p. 6) prints 33,215 for 1961"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [868, 137, 54, 123, 5496, 1296, 11223, 1963, 680, 291, 22, 33215],
  "Assam": [404, 412, 158, 185, 3504, 297, 4722, 1814, 446, 252, 10, 18903],
  "Bihar": [938, 466, 696, 581, 17576, 556, 18047, 4530, 1038, 447, 87, 58876],
  "Gujarat": [762, 245, 75, 598, 5041, 846, 9568, 385, 895, 593, 34, 30650],
  "Jammu & Kashmir": [53, 127, 31, 48, 770, 131, 612, 325, 87, 52, 9, 3926],
  "Kerala": [262, 50, 15, 88, 2285, 150, 3213, 1181, 325, 101, 10, 16897],
  "Madhya Pradesh": [1378, 702, 370, 738, 15096, 3445, 26322, 1468, 1310, 979, 53, 72934],
  "Madras": [762, 517, 35, 196, 6902, 2204, 19919, 2146, 1920, 780, 25, 58794],
  "Maharashtra": [1091, 482, 206, 1085, 9761, 1050, 28701, 838, 2234, 1429, 82, 64078],
  "Mysore": [693, 175, 69, 154, 4705, 771, 8409, 966, 651, 455, 8, 26074],
  "Orissa": [284, 142, 77, 207, 4244, 555, 7619, 980, 660, 363, 8, 21376],
  "Punjab": [542, 359, 4, 59, 3088, 618, 4072, 165, 543, 351, 7, 17230],
  "Rajasthan": [439, 626, 69, 394, 5117, 1843, 4163, 1060, 556, 425, 24, 21274],
  "Uttar Pradesh": [2101, 1150, 1751, 1258, 27078, 5144, 34201, 4856, 3749, 1323, 43, 100756],
  "West Bengal": [468, 703, 508, 597, 9778, 672, 24576, 4152, 1291, 1221, 49, 64196],
  "TOTAL (STATES)": [11045, 6293, 4118, 6311, 120441, 19578, 205367, 26829, 16385, 9062, 471, 609179],
 },
 "U.Ts.": {
  "A. & N. Islands": [3, 1, 0, 3, 27, 2, 86, 2, 5, 3, 0, 241],
  "Delhi": [58, 209, 0, 21, 1125, 72, 5990, 39, 359, 347, 13, 10643],
  "Himachal Pradesh": [20, 32, 2, 28, 175, 13, 253, 45, 45, 29, 1, 1201],
  "L. M. & A. Islands": [0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 9],
  "Manipur": [25, 117, 61, 14, 138, 50, 362, 76, 40, 42, 0, 1361],
  "Nagaland": [15, 8, 5, 7, 58, 5, 64, 6, 12, 4, 0, 252],
  "Tripura": [22, 38, 27, 44, 641, 147, 870, 202, 42, 24, 0, 2765],
  "TOTAL (U.TS.)": [143, 405, 95, 117, 2164, 289, 7634, 370, 503, 449, 14, 16472],
 },
 "Cities": {
  "Ahmedabad": [30, 45, 5, 40, 450, 45, 1494, 34, 172, 114, 6, 3436],
  "Bangalore": [4, 47, 3, 15, 700, 33, 2392, 14, 145, 231, 3, 4317],
  "Bombay": [125, 167, 13, 245, 1547, 48, 10956, 136, 983, 818, 61, 19379],
  "Calcutta": [39, 116, 2, 16, 762, 39, 5642, 226, 378, 428, 12, 14161],
  "Delhi": [50, 186, 0, 18, 1011, 49, 5795, 35, 344, 343, 13, 9983],
  "Hyderabad": [16, 24, 4, 7, 512, 25, 1646, 30, 105, 79, 4, 2971],
  "Kanpur": [23, 74, 2, 11, 621, 12, 1804, 43, 392, 93, 6, 3810],
  "Madras": [13, 31, 0, 8, 122, 35, 3550, 30, 390, 299, 10, 5686],
  "TOTAL (CITIES)": [300, 690, 29, 360, 5725, 286, 33279, 548, 2909, 2405, 115, 63743],
 },
 "Grand": {"GRAND TOTAL": [11188, 6698, 4213, 6428, 122605, 19867, 213001, 27199, 16888, 9511, 485, 625651]},
}
