# ADSI 1995, Appendix-IV: number of traffic accidents by time of occurrence, ROAD ACCIDENTS column group (cols 3-11),
# States / UTs / cities (raw/adsi/1995/table_content/appendix-4_1995.pdf, page 1 = printed page 129). Read from the
# page images; every row is checked against its printed Total and every column against the printed Total (States),
# Total (UTs) and Total (All-India) by scripts/check_handread.py. "Total (All-India)" is entered as GRAND TOTAL; the
# "% Share" row is not transcribed. This edition prints no Total (Cities) row, so the city rows are checked only
# against their own Totals. Delhi appears as "Delhi (UT)" and "Delhi (City)"; cities as printed (Bombay, Calcutta,
# Madras).
# Every State, UT and city Total (and Total (States) 202724, Total (UTs) 11673, Total (All-India) 214397) equals the
# printed Road Total of the same place in the 1995 month table (raw/adsi/1995/archived/appendix-3.pdf, page 1), in
# the same order, so no rows are shifted in this edition. (The month figures for 1995 in web/data/trends/traffic_month
# are the Total traffic figures -- Road + Rail-road + Other railway -- not Road: e.g. Delhi city 9533 = 8773 + 0 + 760.)
KIND, YEAR, PUB = "traffic_time", 1995, "adsi"
SOURCE = "raw/adsi/1995/table_content/appendix-4_1995.pdf"
PAGES = "1"
TITLE = "Appendix-IV: Number of Traffic Accidents by Time of Occurrence during 1995 (State, UT & City-wise)"
GROUP = "Road"
CATS = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24", "Total"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1274, 2468, 1669, 2272, 917, 1085, 1989, 2863, 14537],
  "Arunachal Pradesh": [9, 12, 23, 27, 22, 28, 33, 22, 176],
  "Assam": [29, 49, 180, 257, 207, 223, 195, 94, 1234],
  "Bihar": [407, 569, 831, 887, 818, 752, 775, 539, 5578],
  "Goa": [60, 61, 313, 511, 576, 612, 509, 253, 2895],
  "Gujarat": [1351, 1422, 2576, 3344, 2993, 3226, 2597, 1846, 19355],
  "Haryana": [589, 721, 602, 739, 764, 878, 902, 741, 5936],
  "Himachal Pradesh": [57, 91, 248, 230, 245, 371, 203, 119, 1564],
  "Jammu & Kashmir": [228, 270, 370, 403, 446, 410, 415, 339, 2881],
  "Karnataka": [3220, 3746, 3603, 3857, 3337, 3993, 4201, 3958, 29915],
  "Kerala": [939, 1269, 4665, 6859, 4917, 6304, 4379, 1706, 31038],
  "Madhya Pradesh": [2424, 2390, 2207, 1647, 1792, 1723, 1956, 1710, 15849],
  "Maharashtra": [2836, 3041, 3576, 4241, 4051, 4073, 3460, 3056, 28334],
  "Manipur": [3, 15, 52, 77, 69, 112, 20, 4, 352],
  "Meghalaya": [8, 9, 22, 22, 29, 41, 28, 17, 176],
  "Mizoram": [2, 4, 5, 13, 10, 11, 12, 5, 62],
  "Nagaland": [15, 20, 10, 12, 17, 10, 10, 4, 98],
  "Orissa": [347, 804, 857, 806, 617, 718, 573, 441, 5163],
  "Punjab": [92, 94, 114, 112, 110, 130, 106, 110, 868],
  "Rajasthan": [1021, 1006, 1192, 1141, 1303, 1285, 1276, 1295, 9519],
  "Sikkim": [5, 6, 26, 30, 30, 35, 20, 12, 164],
  "Tamil Nadu": [798, 873, 1137, 1112, 974, 1116, 1028, 936, 7974],
  "Tripura": [20, 31, 25, 120, 90, 85, 40, 10, 421],
  "Uttar Pradesh": [900, 1180, 1644, 1815, 1563, 1620, 1160, 853, 10735],
  "West Bengal": [534, 785, 1454, 1213, 1133, 1299, 963, 519, 7900],
  "TOTAL (STATES)": [17168, 20936, 27401, 31747, 27030, 30140, 26850, 21452, 202724],
 },
 "U.Ts.": {
  "A & N Islands": [0, 2, 16, 21, 24, 22, 15, 3, 103],
  "Chandigarh": [4, 7, 35, 62, 60, 72, 68, 38, 346],
  "D & N Haveli": [0, 1, 3, 0, 3, 2, 8, 4, 21],
  "Daman & Diu": [3, 1, 6, 19, 26, 29, 35, 22, 141],
  "Delhi (UT)": [816, 655, 1251, 1622, 1368, 1561, 1646, 1225, 10144],
  "Lakshadweep": [0, 0, 0, 1, 1, 1, 0, 0, 3],
  "Pondicherry": [27, 31, 126, 141, 158, 200, 161, 71, 915],
  "TOTAL (U.TS.)": [850, 697, 1437, 1866, 1640, 1887, 1933, 1363, 11673],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 1, 3, 5, 4, 1, 0, 14],
  "Bangalore": [235, 395, 650, 901, 631, 891, 840, 568, 5111],
  "Bhopal": [22, 9, 165, 444, 419, 365, 264, 98, 1786],
  "Bombay": [211, 213, 298, 375, 382, 391, 363, 277, 2510],
  "Calcutta": [32, 142, 297, 326, 305, 287, 284, 138, 1811],
  "Coimbatore": [84, 30, 250, 250, 161, 145, 105, 31, 1056],
  "Delhi (City)": [710, 501, 1075, 1414, 1201, 1339, 1434, 1099, 8773],
  "Hyderabad": [103, 121, 176, 202, 231, 227, 195, 156, 1411],
  "Indore": [8, 15, 22, 28, 22, 24, 22, 25, 166],
  "Jaipur": [182, 280, 70, 380, 478, 241, 75, 25, 1731],
  "Kanpur": [40, 35, 45, 51, 45, 58, 52, 30, 356],
  "Kochi": [30, 39, 385, 628, 482, 683, 518, 242, 3007],
  "Lucknow": [13, 27, 109, 103, 54, 78, 36, 39, 459],
  "Ludhiana": [7, 6, 6, 6, 5, 7, 4, 7, 48],
  "Madras": [172, 188, 614, 990, 938, 765, 847, 487, 5001],
  "Madurai": [3, 13, 15, 14, 20, 26, 19, 16, 126],
  "Nagpur": [12, 10, 29, 34, 28, 26, 31, 22, 192],
  "Patna": [20, 45, 59, 37, 32, 36, 31, 50, 310],
  "Pune": [25, 11, 34, 35, 48, 62, 54, 44, 313],
  "Surat": [70, 68, 189, 217, 234, 243, 264, 177, 1462],
  "Vadodara": [89, 52, 175, 281, 251, 247, 210, 167, 1472],
  "Varanasi": [3, 14, 38, 44, 75, 74, 52, 48, 348],
  "Vishakhapatnam": [24, 54, 116, 102, 123, 70, 78, 36, 603],
 },
 "Grand": {"GRAND TOTAL": [18018, 21633, 28838, 33613, 28670, 32027, 28783, 22815, 214397]},
}
