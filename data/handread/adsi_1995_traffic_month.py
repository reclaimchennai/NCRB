# ADSI 1995, Appendix-III: number of traffic accidents by month of occurrence, ROAD ACCIDENTS column group (cols 3-15),
# States / UTs / cities (raw/adsi/1995/archived/appendix-3.pdf, page 1 = printed page 125). Read from the page images;
# every row is checked against its printed Total and every column against the printed Total (States), Total (UTs) and
# Total (All India) by scripts/check_handread.py. "Total (All India)" is entered as GRAND TOTAL. This edition prints no
# Total (Cities) row, so the city rows are checked only against their own Totals. Delhi is printed as "DELHI UT" and,
# among the cities, "DELHI"; entered as "Delhi (UT)" and "Delhi (City)" to match adsi_1995_traffic_time.py. Cities as
# printed (Bombay, Calcutta, Madras). Rail-road (page 2), other railway (page 3) and Total traffic (page 4, see
# adsi_1995_traffic_month_total.py) are separate column groups.
# Every State, UT and city Total equals its Total in adsi_1995_traffic_time.py (same edition, same order).
KIND, YEAR, PUB = "traffic_month", 1995, "adsi"
SOURCE = "raw/adsi/1995/archived/appendix-3.pdf"
PAGES = "1"
TITLE = "Appendix-III: Number of Traffic Accidents by Month of Occurrence during 1995 (State, UTs & City-wise)"
GROUP = "Road"
CATS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Total"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1071, 1203, 1268, 1245, 1424, 1272, 1117, 1185, 1089, 1139, 1207, 1317, 14537],
  "Arunachal Pradesh": [16, 13, 15, 15, 13, 15, 12, 19, 19, 16, 12, 11, 176],
  "Assam": [105, 106, 129, 97, 127, 97, 96, 88, 87, 103, 93, 106, 1234],
  "Bihar": [397, 467, 449, 427, 527, 507, 546, 412, 426, 466, 485, 469, 5578],
  "Goa": [286, 226, 250, 252, 285, 217, 187, 205, 201, 269, 244, 273, 2895],
  "Gujarat": [1592, 1466, 1666, 1695, 1875, 1744, 1474, 1466, 1466, 1576, 1530, 1805, 19355],
  "Haryana": [535, 486, 494, 461, 519, 583, 530, 457, 487, 401, 402, 581, 5936],
  "Himachal Pradesh": [98, 108, 125, 136, 142, 173, 136, 135, 138, 141, 113, 119, 1564],
  "Jammu & Kashmir": [166, 183, 253, 232, 238, 258, 240, 268, 259, 267, 253, 264, 2881],
  "Karnataka": [2377, 2400, 2520, 2430, 2743, 2534, 2335, 2456, 2328, 2483, 2606, 2703, 29915],
  "Kerala": [2869, 2539, 2881, 2697, 2439, 2258, 2359, 2614, 2447, 2608, 2614, 2713, 31038],
  "Madhya Pradesh": [801, 1282, 1332, 1318, 1488, 1512, 1410, 1236, 1225, 1459, 1398, 1388, 15849],
  "Maharashtra": [2305, 2124, 2357, 2426, 2742, 2436, 2246, 2181, 2212, 2399, 2262, 2644, 28334],
  "Manipur": [17, 27, 39, 29, 36, 38, 18, 24, 24, 36, 22, 42, 352],
  "Meghalaya": [22, 19, 19, 14, 13, 11, 12, 12, 10, 13, 14, 17, 176],
  "Mizoram": [9, 6, 5, 3, 3, 6, 6, 4, 5, 6, 5, 4, 62],
  "Nagaland": [10, 3, 8, 4, 6, 8, 10, 8, 12, 5, 10, 14, 98],
  "Orissa": [424, 433, 377, 449, 504, 422, 458, 391, 388, 420, 441, 456, 5163],
  "Punjab": [65, 67, 83, 71, 77, 76, 66, 60, 62, 86, 84, 71, 868],
  "Rajasthan": [981, 805, 697, 713, 703, 785, 876, 904, 795, 752, 762, 746, 9519],
  "Sikkim": [11, 8, 12, 33, 12, 12, 12, 5, 13, 10, 21, 15, 164],
  "Tamil Nadu": [640, 637, 680, 626, 674, 699, 600, 706, 679, 673, 647, 713, 7974],
  "Tripura": [37, 34, 35, 33, 48, 38, 34, 36, 27, 30, 35, 34, 421],
  "Uttar Pradesh": [869, 949, 992, 858, 958, 922, 936, 830, 794, 868, 842, 917, 10735],
  "West Bengal": [662, 604, 724, 686, 719, 698, 652, 588, 628, 620, 667, 652, 7900],
  "TOTAL (STATES)": [16365, 16195, 17410, 16950, 18315, 17321, 16368, 16290, 15821, 16846, 16769, 18074, 202724],
 },
 "U.Ts.": {
  "A & N Islands": [9, 16, 4, 10, 13, 6, 12, 9, 8, 3, 7, 6, 103],
  "Chandigarh": [25, 34, 26, 16, 27, 25, 27, 38, 39, 31, 22, 36, 346],
  "D & N Haveli": [1, 0, 0, 4, 2, 6, 1, 0, 0, 3, 2, 2, 21],
  "Daman & Diu": [11, 4, 5, 15, 10, 14, 10, 14, 8, 14, 12, 24, 141],
  "Delhi (UT)": [846, 760, 803, 822, 830, 770, 893, 878, 900, 841, 886, 915, 10144],
  "Lakshadweep": [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 3],
  "Pondicherry": [70, 65, 69, 73, 93, 87, 87, 71, 68, 93, 69, 70, 915],
  "TOTAL (U.TS.)": [962, 879, 907, 940, 975, 909, 1030, 1011, 1023, 985, 998, 1054, 11673],
 },
 "Cities": {
  "Ahmedabad": [1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 0, 14],
  "Bangalore": [426, 454, 420, 387, 414, 418, 441, 452, 412, 431, 439, 417, 5111],
  "Bhopal": [134, 156, 141, 169, 121, 161, 139, 131, 167, 147, 152, 168, 1786],
  "Bombay": [226, 194, 195, 194, 196, 211, 193, 219, 235, 231, 192, 224, 2510],
  "Calcutta": [149, 120, 167, 139, 175, 169, 156, 142, 158, 140, 139, 157, 1811],
  "Coimbatore": [99, 79, 88, 87, 90, 68, 72, 99, 86, 100, 99, 89, 1056],
  "Delhi (City)": [734, 667, 701, 713, 714, 656, 779, 758, 782, 728, 759, 782, 8773],
  "Hyderabad": [124, 118, 127, 114, 138, 115, 117, 124, 109, 98, 107, 120, 1411],
  "Indore": [10, 10, 13, 12, 13, 16, 14, 15, 16, 12, 13, 22, 166],
  "Jaipur": [122, 143, 132, 134, 160, 160, 155, 156, 141, 121, 147, 160, 1731],
  "Kanpur": [25, 30, 28, 35, 30, 20, 35, 38, 25, 30, 35, 25, 356],
  "Kochi": [270, 221, 259, 213, 195, 193, 233, 302, 377, 250, 242, 252, 3007],
  "Lucknow": [44, 35, 30, 34, 34, 35, 43, 42, 40, 51, 38, 33, 459],
  "Ludhiana": [5, 4, 4, 4, 5, 4, 5, 4, 3, 4, 3, 3, 48],
  "Madras": [393, 405, 428, 391, 386, 411, 434, 446, 422, 440, 416, 429, 5001],
  "Madurai": [9, 12, 14, 10, 8, 13, 12, 14, 10, 6, 6, 12, 126],
  "Nagpur": [12, 15, 14, 21, 10, 16, 17, 8, 9, 20, 31, 19, 192],
  "Patna": [15, 20, 17, 22, 36, 25, 21, 19, 36, 30, 32, 37, 310],
  "Pune": [34, 26, 20, 24, 25, 25, 30, 26, 22, 26, 32, 23, 313],
  "Surat": [142, 115, 138, 116, 143, 135, 103, 90, 111, 119, 105, 145, 1462],
  "Vadodara": [143, 116, 121, 142, 142, 126, 105, 99, 140, 107, 104, 127, 1472],
  "Varanasi": [34, 24, 33, 25, 24, 29, 27, 30, 31, 30, 34, 27, 348],
  "Vishakhapatnam": [54, 39, 64, 37, 45, 58, 40, 44, 36, 65, 61, 60, 603],
 },
 "Grand": {"GRAND TOTAL": [17327, 17074, 18317, 17890, 19290, 18230, 17398, 17301, 16844, 17831, 17767, 19128, 214397]},
}
