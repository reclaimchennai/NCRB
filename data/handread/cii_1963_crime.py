# CII 1963 by crime head, States / U.Ts. / cities, assembled from the per-head appendices of the 1963 edition
# (raw/cii/1963/year_wise/1689771154APPENDIX.pdf): column 5 "cases reported during the year" of Appendix I (total cognizable crime,
# pages 1 and 3), III murder (9, 11), V kidnapping & abduction (17, 19), VII dacoity (25, 27), IX robbery (33, 35), XI house-breaking
# (41, 43), XIII cattle thefts (49, 51), XV ordinary thefts (57, 59), XIX criminal breach of trust (71, 73), XXI cheating (79, 81),
# XXIII counterfeiting (87, 89). The edition prints no single State x head table. ".." (nil) entered as 0.
# RIOTS (Appendix XVII) is left out: the page with the State figures (printed p. 96) is missing from the PDF (page 63 = printed 94 is
# followed by page 64 = printed 97). The rest of Appendix XVII (page 65, printed 98) gives cases reported: U.Ts. A. & N. Islands 0,
# Delhi 86, Himachal Pradesh 59, L.M. & A. Islands 0, Manipur 166, Tripura 286, TOTAL 597, GRAND TOTAL 28,114; cities Ahmedabad 35,
# Bangalore 20, Bombay 144, Calcutta 211, Delhi 81, Hyderabad 20, Kanpur 81, Madras 15, TOTAL 607. The Survey text (survey p. 19)
# gives riots for a few States only (Bihar 4,883, Nagaland 12, Maharashtra 697).
# No "other IPC crimes" column, so each column is checked against the printed TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and
# TOTAL (cities) by scripts/check_handread.py.
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime cases reported
KIND, YEAR, PUB = "crime", 1963, "cii"
SOURCE = "raw/cii/1963/year_wise/1689771154APPENDIX.pdf"
PAGES = "1,3,9,11,17,19,25,27,33,35,41,43,49,51,57,59,71,73,79,81,87,89"
TITLE = "Appendices I-XXIII (cases): cases reported during the year 1963 under total cognizable crime and each head (riots missing), States/U.Ts./Cities"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("TOTAL (U.TS.)", "Kidnapping & abduction"): (104, None, 'printed 104, but Manipur alone has 101 and the U.Ts. as printed add up to 374 (each U.T. figure agrees with its printed volume of crime per lakh, page 20); the GRAND TOTAL 6,924 (also in the Survey text, p. 13) = States 6,820 + the misprinted 104, so 374 cannot be confirmed either; set to None'),
    ("GRAND TOTAL", "Kidnapping & abduction"): (6924, 6924, 'kept as printed (also the Survey text figure), but it is TOTAL (States) 6,820 + the misprinted U.T. total 104; the U.T. figures add up to 374, which would make it 7,194'),
    ("GRAND TOTAL", "Counterfeiting"): (None, 289, 'print damaged (28_, last digit broken); TOTAL (States) 270 + TOTAL (U.Ts.) 19 = 289'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [861, 141, 78, 135, 5950, 1259, 11219, 703, 316, 13, 34460],
  "Assam": [377, 468, 180, 169, 3908, 392, 5372, 415, 288, 13, 19268],
  "Bihar": [867, 461, 680, 617, 19990, 611, 18835, 1250, 582, 44, 63785],
  "Gujarat": [691, 280, 92, 596, 5072, 936, 10531, 991, 538, 24, 32526],
  "Jammu & Kashmir": [61, 111, 17, 12, 708, 134, 638, 68, 47, 0, 3822],
  "Kerala": [206, 53, 5, 58, 2080, 133, 2812, 300, 114, 5, 16105],
  "Madhya Pradesh": [1350, 846, 870, 1014, 16300, 4087, 28956, 1573, 1129, 30, 79547],
  "Madras": [681, 500, 20, 131, 6442, 1807, 17815, 1563, 730, 16, 56477],
  "Maharashtra": [924, 330, 209, 939, 8983, 1188, 19993, 1548, 665, 12, 49493],
  "Mysore": [665, 147, 75, 139, 4830, 749, 7994, 638, 349, 6, 25824],
  "Nagaland": [6, 3, 11, 9, 47, 5, 102, 17, 1, 0, 283],
  "Orissa": [320, 113, 93, 221, 5188, 657, 8465, 653, 354, 10, 23723],
  "Punjab": [533, 382, 6, 54, 3114, 729, 4531, 823, 427, 11, 18452],
  "Rajasthan": [448, 886, 100, 626, 6132, 1937, 5507, 739, 539, 9, 27040],
  "Uttar Pradesh": [2192, 1531, 1835, 2194, 34663, 7586, 46406, 5454, 1566, 45, 132220],
  "West Bengal": [446, 568, 664, 618, 11067, 930, 19644, 1056, 652, 32, 55085],
  "TOTAL (STATES)": [10628, 6820, 4935, 7532, 134474, 23140, 208820, 17791, 8297, 270, 638110],
 },
 "U.Ts.": {
  "A. & N. Islands": [5, 4, 0, 0, 24, 3, 74, 2, 0, 0, 211],
  "Delhi": [69, 203, 0, 52, 1556, 94, 8412, 452, 460, 16, 14373],
  "Himachal Pradesh": [16, 20, 5, 46, 236, 14, 286, 84, 22, 3, 1442],
  "L. M. & A. Islands": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2],
  "Manipur": [15, 101, 21, 27, 228, 32, 407, 57, 58, 0, 1702],
  "Tripura": [21, 46, 36, 37, 507, 274, 930, 52, 17, 0, 2990],
  "TOTAL (U.TS.)": [126, None, 62, 162, 2551, 417, 10110, 647, 557, 19, 20720],
 },
 "Cities": {
  "Ahmedabad": [32, 49, 3, 29, 409, 39, 1400, 157, 88, 8, 3333],
  "Bangalore": [17, 6, 0, 16, 553, 30, 1935, 114, 101, 3, 3499],
  "Bombay": [125, 158, 12, 162, 1354, 34, 9647, 964, 724, 33, 17926],
  "Calcutta": [31, 94, 1, 6, 490, 32, 4874, 363, 394, 8, 20492],
  "Delhi": [57, 187, 0, 46, 1370, 66, 8066, 434, 450, 16, 13479],
  "Hyderabad": [8, 21, 3, 6, 450, 19, 1371, 82, 98, 5, 2424],
  "Kanpur": [32, 75, 5, 27, 885, 27, 2905, 620, 147, 3, 5809],
  "Madras": [12, 55, 0, 7, 213, 33, 3570, 306, 265, 5, 6036],
  "TOTAL (CITIES)": [314, 645, 24, 299, 5724, 280, 33768, 3040, 2267, 81, 72998],
 },
 "Grand": {"GRAND TOTAL": [10754, 6924, 4997, 7694, 137025, 23557, 218930, 18438, 8854, 289, 658830]},
}
