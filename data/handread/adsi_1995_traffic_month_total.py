# ADSI 1995, Appendix-III (Concluded): number of traffic accidents by month of occurrence, TOTAL TRAFFIC ACCIDENTS
# column group (cols 42-54 = Road + Rail-road + Other railway), States / UTs / cities
# (raw/adsi/1995/archived/appendix-3.pdf, page 4 = printed page 128). Read from the page images; every row is checked
# against its printed Total and every column against the printed Total (States), Total (UTs) and Total (All India) by
# scripts/check_handread.py. "Total (All India)" is entered as GRAND TOTAL. This edition prints no Total (Cities) row,
# so the city rows are checked only against their own Totals. Delhi is printed as "DELHI UT" and, among the cities,
# "DELHI"; entered as "Delhi (UT)" and "Delhi (City)" to match adsi_1995_traffic_time.py. Cities as printed (Bombay,
# Calcutta, Madras). The Road group is in adsi_1995_traffic_month.py; every figure here is >= its Road figure.
KIND, YEAR, PUB = "traffic_month", 1995, "adsi"
SOURCE = "raw/adsi/1995/archived/appendix-3.pdf"
PAGES = "4"
TITLE = "Appendix-III: Number of Traffic Accidents by Month of Occurrence during 1995 (State, UTs & City-wise)"
GROUP = "Total traffic"
CATS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Total"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("TOTAL (STATES)", "Jun"): (18867, 18857, "printed 18,867 (clear at zoom 8); the 25 State June figures add to 18,857, the Total (States) row adds to its printed 219,418 only with 18,857, and Total (All India) June 19,831 = 18,857 + Total (UTs) 974, so the printed figure is a misprint"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1130, 1274, 1331, 1312, 1502, 1342, 1184, 1255, 1155, 1208, 1282, 1385, 15360],
  "Arunachal Pradesh": [16, 13, 15, 15, 13, 15, 12, 19, 19, 16, 12, 11, 176],
  "Assam": [110, 108, 132, 101, 131, 100, 106, 94, 94, 105, 96, 111, 1288],
  "Bihar": [462, 522, 544, 528, 578, 615, 617, 519, 531, 570, 572, 574, 6632],
  "Goa": [287, 227, 251, 253, 286, 218, 188, 206, 202, 270, 245, 274, 2907],
  "Gujarat": [1683, 1534, 1756, 1791, 1971, 1854, 1568, 1573, 1572, 1672, 1615, 1873, 20462],
  "Haryana": [535, 486, 494, 461, 519, 583, 530, 457, 487, 401, 402, 581, 5936],
  "Himachal Pradesh": [100, 108, 125, 136, 145, 174, 137, 135, 139, 141, 113, 119, 1572],
  "Jammu & Kashmir": [166, 183, 253, 232, 238, 258, 240, 268, 259, 267, 253, 264, 2881],
  "Karnataka": [2388, 2406, 2526, 2438, 2747, 2539, 2339, 2471, 2333, 2490, 2611, 2709, 29997],
  "Kerala": [2892, 2559, 2906, 2714, 2460, 2278, 2386, 2642, 2464, 2636, 2635, 2737, 31309],
  "Madhya Pradesh": [865, 1366, 1413, 1403, 1589, 1605, 1494, 1315, 1308, 1549, 1469, 1476, 16852],
  "Maharashtra": [2878, 2637, 2931, 3010, 3355, 3040, 2865, 2732, 2815, 2968, 2870, 3268, 35369],
  "Manipur": [17, 27, 39, 29, 36, 38, 18, 24, 24, 36, 22, 42, 352],
  "Meghalaya": [22, 19, 19, 14, 13, 11, 12, 12, 10, 13, 14, 17, 176],
  "Mizoram": [9, 6, 5, 3, 3, 6, 6, 4, 5, 6, 5, 4, 62],
  "Nagaland": [10, 3, 8, 4, 6, 8, 10, 8, 12, 5, 10, 14, 98],
  "Orissa": [444, 453, 407, 468, 529, 453, 490, 413, 402, 441, 456, 469, 5425],
  "Punjab": [113, 118, 138, 114, 129, 133, 109, 110, 110, 138, 134, 128, 1474],
  "Rajasthan": [997, 816, 707, 722, 718, 800, 889, 916, 807, 760, 780, 762, 9674],
  "Sikkim": [11, 8, 12, 33, 12, 12, 12, 5, 13, 10, 21, 15, 164],
  "Tamil Nadu": [741, 735, 787, 725, 779, 809, 694, 817, 786, 778, 748, 825, 9224],
  "Tripura": [37, 34, 35, 33, 48, 38, 34, 36, 27, 30, 35, 34, 421],
  "Uttar Pradesh": [943, 1016, 1059, 922, 1036, 995, 1016, 907, 872, 929, 919, 980, 11594],
  "West Bengal": [855, 756, 900, 887, 945, 933, 791, 763, 770, 796, 815, 802, 10013],
  "TOTAL (STATES)": [17711, 17414, 18793, 18348, 19788, 18857, 17747, 17701, 17216, 18235, 18134, 19474, 219418],
 },
 "U.Ts.": {
  "A & N Islands": [9, 16, 4, 10, 13, 6, 12, 9, 8, 3, 7, 6, 103],
  "Chandigarh": [25, 34, 26, 16, 27, 25, 27, 38, 39, 31, 22, 36, 346],
  "D & N Haveli": [1, 0, 0, 4, 2, 6, 1, 0, 0, 3, 2, 2, 21],
  "Daman & Diu": [11, 4, 5, 15, 10, 14, 10, 14, 8, 14, 12, 24, 141],
  "Delhi (UT)": [924, 821, 870, 894, 891, 835, 953, 948, 954, 903, 942, 969, 10904],
  "Lakshadweep": [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 3],
  "Pondicherry": [70, 65, 69, 73, 93, 87, 87, 71, 68, 93, 69, 70, 915],
  "TOTAL (U.TS.)": [1040, 940, 974, 1012, 1036, 974, 1090, 1081, 1077, 1047, 1054, 1108, 12433],
 },
 "Cities": {
  "Ahmedabad": [1, 1, 2, 1, 3, 3, 2, 3, 2, 2, 2, 1, 23],
  "Bangalore": [426, 454, 420, 387, 414, 418, 441, 452, 412, 431, 439, 417, 5111],
  "Bhopal": [134, 156, 141, 169, 121, 161, 139, 131, 167, 147, 152, 168, 1786],
  "Bombay": [235, 201, 205, 198, 205, 218, 202, 223, 242, 241, 197, 228, 2595],
  "Calcutta": [149, 120, 167, 139, 175, 169, 156, 142, 158, 140, 139, 157, 1811],
  "Coimbatore": [99, 79, 88, 87, 90, 68, 72, 99, 86, 100, 99, 89, 1056],
  "Delhi (City)": [812, 728, 768, 785, 775, 721, 839, 828, 836, 790, 815, 836, 9533],
  "Hyderabad": [124, 118, 127, 114, 138, 115, 117, 124, 109, 98, 107, 120, 1411],
  "Indore": [11, 10, 15, 12, 16, 18, 14, 16, 18, 13, 14, 22, 179],
  "Jaipur": [122, 143, 134, 135, 162, 162, 155, 156, 141, 121, 147, 160, 1738],
  "Kanpur": [45, 45, 39, 42, 35, 20, 48, 54, 39, 48, 44, 32, 491],
  "Kochi": [270, 221, 259, 213, 195, 193, 233, 302, 377, 250, 242, 252, 3007],
  "Lucknow": [47, 35, 31, 36, 34, 36, 43, 44, 42, 53, 40, 34, 475],
  "Ludhiana": [5, 4, 4, 4, 5, 4, 5, 4, 3, 4, 3, 3, 48],
  "Madras": [393, 405, 428, 391, 386, 411, 434, 446, 422, 440, 416, 429, 5001],
  "Madurai": [9, 12, 14, 10, 8, 13, 12, 14, 10, 6, 6, 12, 126],
  "Nagpur": [12, 15, 14, 21, 10, 16, 17, 8, 9, 20, 31, 19, 192],
  "Patna": [15, 20, 17, 22, 36, 25, 21, 19, 36, 30, 32, 37, 310],
  "Pune": [34, 26, 20, 24, 25, 25, 30, 26, 22, 26, 32, 23, 313],
  "Surat": [142, 115, 138, 116, 143, 135, 103, 90, 111, 119, 105, 145, 1462],
  "Vadodara": [143, 116, 121, 142, 142, 126, 106, 99, 140, 107, 104, 127, 1473],
  "Varanasi": [35, 31, 35, 28, 26, 32, 30, 32, 32, 32, 36, 28, 377],
  "Vishakhapatnam": [54, 39, 64, 37, 45, 58, 40, 44, 36, 65, 61, 60, 603],
 },
 "Grand": {"GRAND TOTAL": [18751, 18354, 19767, 19360, 20824, 19831, 18837, 18782, 18293, 19282, 19188, 20582, 231851]},
}
