# CII 1965 by crime head, States / U.Ts. / cities, assembled from the per-head appendices of the 1965 edition
# (raw/cii/1965/table_chapter/appendix-1965.pdf): column 5 "cases reported during the year" of Appendix I (total cognizable crime,
# pages 2 and 4), III murder (10, 12), V kidnapping & abduction (18, 20), VII dacoity (26, 28), IX robbery (34, 36), XI house-breaking
# (42, 44), XIII cattle thefts (50, 52), XV ordinary thefts (58, 60), XVII riots (66, 68), XIX criminal breach of trust (74, 76),
# XXI cheating (82, 84), XXIII counterfeiting (90, 92). The 1965 edition prints no single State x head table (Table III gives the
# total only). ".."/"-"/blank (nil) entered as 0; Haryana did not yet exist (Punjab undivided). No "other IPC crimes" column, so each
# column is checked against the printed TOTAL (States), TOTAL (U.Ts.), GRAND TOTAL and TOTAL (cities) by scripts/check_handread.py.
# Two printed State totals do not equal their States and are set to None (see CORRECTIONS); the State figures are kept as printed.
# Columns: Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Cattle thefts, Ordinary thefts, Riots,
# Criminal breach of trust, Cheating, Counterfeiting, Total cognizable crime cases reported
KIND, YEAR, PUB = "crime", 1965, "cii"
SOURCE = "raw/cii/1965/table_chapter/appendix-1965.pdf"
PAGES = "2,4,10,12,18,20,26,28,34,36,42,44,50,52,58,60,66,68,74,76,82,84,90,92"
TITLE = "Appendices I-XXIII (cases): cases reported during the year 1965 under total cognizable crime and each head, States/U.Ts./Cities"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Orissa", "Total cognizable crimes (IPC)"): (27288, 27228, 'printed 27,288 in Appendix I; Table III of the same edition (1680078432TABLE-3-1965.pdf p. 2) prints 27,228 = Q.A. 23,142 + increase 4,086, Table 4 of CII 1969 prints 27228 for 1965, and the States column then adds up to the printed TOTAL 7,25,420'),
    ("TOTAL (U.TS.)", "Criminal breach of trust"): (867, 876, 'printed 867; the U.Ts. add up to 876 (each U.T. figure agrees with its printed volume of crime per lakh on page 75) and 20,478 + 876 = the printed GRAND TOTAL 21,354'),
    ("TOTAL (STATES)", "Murder"): (12130, None, "printed 12,130 (and 12,130 + U.Ts. 171 = GRAND TOTAL 12,310, also in the Survey text); the States as printed add up to 12,139. The excess, 9, is exactly Nagaland's figure (whose other columns are all nil) -- the total may leave Nagaland out -- but which figure is wrong cannot be confirmed (the CII 1966 Survey says Nagaland had 14 murders in 1965). Every other murder column adds up; State figures kept as printed, of which Kerala, J&K, Gujarat, Orissa, Punjab, Rajasthan, West Bengal and Madras are confirmed by the Survey text (p. 4 of survey-of-crime-1965.pdf)"),
    ("TOTAL (STATES)", "Cattle thefts"): (21880, None, 'printed 21,880 (and 21,880 + U.Ts. 363 = the printed GRAND TOTAL 22,243 = the Survey text figure); the States as printed (re-read at zoom 6) add up to 21,882. Every other cattle-theft column adds up and every State figure agrees with its printed volume per lakh within rounding, so the misprinted figure cannot be identified; State figures kept as printed'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [924, 114, 74, 139, 5468, 1120, 10305, 1874, 833, 314, 24, 36250],
  "Assam": [373, 495, 199, 180, 3656, 478, 5538, 1612, 465, 289, 9, 20201],
  "Bihar": [1058, 436, 892, 664, 20691, 577, 19867, 6093, 1267, 639, 24, 67905],
  "Gujarat": [754, 285, 72, 457, 4235, 775, 10069, 330, 1049, 595, 11, 30700],
  "Jammu & Kashmir": [101, 108, 24, 14, 734, 112, 625, 359, 75, 50, 4, 4083],
  "Kerala": [276, 53, 18, 53, 2412, 133, 3247, 1053, 376, 155, 24, 19720],
  "Madhya Pradesh": [1482, 734, 452, 870, 16649, 3734, 26920, 1397, 1403, 1290, 11, 77768],
  "Madras": [723, 448, 38, 150, 7066, 1881, 18126, 3270, 1572, 743, 74, 60490],
  "Maharashtra": [1261, 564, 389, 1492, 13209, 1546, 37980, 1493, 3039, 1752, 49, 86160],
  "Mysore": [757, 116, 121, 147, 5770, 825, 9379, 1080, 678, 357, 35, 28877],
  "Nagaland": [9, 2, 4, 6, 21, 0, 135, 5, 28, 4, 0, 328],
  "Orissa": [399, 114, 92, 216, 4993, 694, 9223, 1085, 708, 770, 15, 27228],
  "Punjab": [603, 447, 4, 29, 2653, 519, 4548, 135, 837, 502, 26, 19377],
  "Rajasthan": [520, 1004, 82, 624, 6659, 1805, 6322, 2040, 779, 687, 6, 30176],
  "Uttar Pradesh": [2441, 1808, 1832, 2372, 34740, 6960, 52418, 6057, 6019, 1979, 39, 141985],
  "West Bengal": [458, 705, 547, 462, 9911, 723, 24068, 4454, 1350, 1129, 26, 74172],
  "TOTAL (STATES)": [None, 7433, 4840, 7875, 138867, None, 238770, 32337, 20478, 11255, 377, 725420],
 },
 "U.Ts.": {
  "A. & N. Islands": [4, 1, 0, 0, 41, 3, 66, 2, 5, 1, 0, 285],
  "Dadra & Nagar Haveli": [2, 0, 2, 1, 18, 2, 20, 0, 5, 4, 0, 81],
  "Delhi": [76, 283, 10, 50, 1702, 60, 10334, 72, 544, 477, 55, 17209],
  "Goa, Daman & Diu": [15, 14, 5, 45, 423, 3, 657, 44, 67, 33, 3, 1988],
  "Himachal Pradesh": [19, 37, 1, 35, 254, 18, 303, 67, 100, 29, 1, 1538],
  "Laccadives": [0, 0, 0, 0, 1, 0, 4, 1, 1, 1, 0, 8],
  "Manipur": [26, 131, 63, 43, 154, 43, 401, 124, 68, 98, 0, 1817],
  "Pondicherry": [3, 3, 0, 0, 165, 15, 350, 63, 43, 17, 0, 1132],
  "Tripura": [26, 25, 34, 18, 390, 219, 554, 230, 43, 20, 0, 2137],
  "TOTAL (U.TS.)": [171, 494, 115, 192, 3148, 363, 12689, 603, 876, 680, 59, 26195],
 },
 "Cities": {
  "Ahmedabad": [27, 47, 3, 17, 424, 30, 1432, 32, 121, 93, 3, 3363],
  "Bangalore": [16, 11, 3, 16, 729, 23, 2213, 27, 132, 115, 12, 4176],
  "Bombay": [152, 203, 12, 359, 2092, 70, 14407, 273, 1276, 920, 41, 26791],
  "Calcutta": [26, 100, 4, 10, 473, 19, 4809, 184, 350, 383, 6, 21030],
  "Delhi": [65, 271, 5, 44, 1495, 50, 9973, 61, 521, 459, 55, 16216],
  "Hyderabad": [16, 15, 2, 6, 488, 11, 1631, 25, 105, 110, 1, 2805],
  "Kanpur": [31, 98, 0, 73, 807, 24, 3302, 90, 742, 247, 6, 6689],
  "Madras": [11, 34, 0, 5, 214, 76, 3765, 35, 348, 244, 29, 7010],
  "TOTAL (CITIES)": [344, 779, 29, 530, 6722, 303, 41532, 727, 3595, 2571, 153, 88080],
 },
 "Grand": {"GRAND TOTAL": [12310, 7927, 4955, 8067, 142015, 22243, 251459, 32940, 21354, 11935, 436, 751615]},
}
