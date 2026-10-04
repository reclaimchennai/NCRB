# ADSI 1999, Table-13: number of traffic accidents by time of occurrence, ROAD ACCIDENTS column group (cols 3-11),
# States / UTs / cities (raw/adsi/1999/table_content/table-13_1999.pdf, page 1 = printed page 105). Read from the page
# images; every row is checked against its printed Total and every column against the printed Total (States),
# Total (UTs), Total (All-India) and Total (Cities) by scripts/check_handread.py. "Total (All-India)" is entered as
# GRAND TOTAL. Delhi appears as "Delhi (UT)" and "Delhi (City)". Blurred digits read with the row and column totals:
# Andhra Pradesh 18-21 3420 (could be 3470), Delhi (UT) 18-21 1747, Bangalore 18-21 1372 (could be 1172).
# Every State, UT and city Total equals the printed Total of the same place in the 1999 month table
# (raw/adsi/1999/table_content/table-12_1999.pdf), so no rows are shifted in this edition.
KIND, YEAR, PUB = "traffic_time", 1999, "adsi"
SOURCE = "raw/adsi/1999/table_content/table-13_1999.pdf"
PAGES = "1"
TITLE = "Table-13: Number of Traffic Accidents by Time of Occurrence during 1999 (State, UT & City-wise)"
GROUP = "Road"
CATS = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24", "Total"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("Chandigarh", "12-15"): (50, 60, "printed 50; the row then adds to its printed Total 454 and the 12-15 column to the printed Total UTs 1680"),
    ("Goa", "21-24"): (126, 128, "printed 126 (clear); the row then adds to its printed Total 1313 and the 21-24 column to the printed Total States 28505 (= Total All-India 30190 - Total UTs 1685). NB the month table's Goa months add to 1311"),
    ("TOTAL (STATES)", "15-18"): (44605, 44606, "the last digit is blurred and reads as 5; the States add to 44606, the row then adds to its printed Total 294716, and Total All-India 46566 - Total UTs 1960 = 44606"),
    ("Calcutta", "Total"): (1382, 1882, "the second digit is blurred (1382 or 1882); the row adds to 1882, Total (Cities) 48735 needs 1882, and the month table's Kolkata total is 1882"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2576, 3800, 2737, 3237, 3235, 2808, 3420, 2496, 24309],
  "Arunachal Pradesh": [15, 17, 29, 27, 24, 27, 25, 24, 188],
  "Assam": [65, 114, 147, 226, 188, 224, 141, 53, 1158],
  "Bihar": [738, 837, 1014, 1201, 1052, 968, 786, 571, 7167],
  "Goa": [37, 34, 165, 258, 279, 238, 174, 128, 1313],
  "Gujarat": [1536, 1518, 2716, 3500, 3413, 3500, 3415, 2306, 21904],
  "Haryana": [425, 599, 932, 847, 640, 850, 842, 525, 5660],
  "Himachal Pradesh": [82, 131, 191, 375, 306, 380, 369, 174, 2008],
  "Jammu & Kashmir": [198, 391, 756, 905, 679, 788, 381, 237, 4335],
  "Karnataka": [1998, 2771, 3317, 4791, 4760, 5023, 4780, 3395, 30835],
  "Kerala": [948, 1660, 4400, 6221, 5471, 6515, 4833, 2336, 32384],
  "Madhya Pradesh": [1509, 2188, 3169, 3558, 3696, 3182, 3111, 1998, 22411],
  "Maharashtra": [3745, 3849, 4744, 5204, 4798, 4627, 4600, 3936, 35503],
  "Manipur": [1, 9, 100, 172, 86, 76, 41, 10, 495],
  "Meghalaya": [7, 18, 29, 44, 30, 43, 31, 14, 216],
  "Mizoram": [0, 0, 4, 9, 9, 12, 7, 5, 46],
  "Nagaland": [1, 2, 9, 19, 14, 15, 3, 1, 64],
  "Orissa": [724, 916, 912, 981, 694, 905, 856, 589, 6577],
  "Punjab": [128, 155, 182, 221, 215, 194, 218, 185, 1498],
  "Rajasthan": [1890, 2460, 2848, 2932, 3226, 3121, 2764, 1891, 21132],
  "Sikkim": [2, 1, 10, 22, 25, 24, 19, 10, 113],
  "Tamil Nadu": [5253, 4662, 6229, 6595, 6786, 7049, 6396, 5116, 48086],
  "Tripura": [22, 10, 73, 110, 122, 48, 51, 12, 448],
  "Uttar Pradesh": [1346, 1874, 2417, 2507, 2380, 2510, 2360, 1561, 16955],
  "West Bengal": [718, 992, 1316, 1715, 1394, 1479, 1365, 932, 9911],
  "TOTAL (STATES)": [23964, 29008, 38446, 45677, 43522, 44606, 40988, 28505, 294716],
 },
 "U.Ts.": {
  "A & N Islands": [0, 5, 27, 24, 24, 26, 19, 13, 138],
  "Chandigarh": [16, 8, 60, 57, 60, 72, 102, 79, 454],
  "D & N Haveli": [2, 3, 4, 11, 12, 19, 20, 10, 81],
  "Daman & Diu": [1, 0, 7, 4, 11, 7, 12, 4, 46],
  "Delhi (UT)": [697, 659, 1046, 1250, 1391, 1630, 1747, 1489, 9909],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [28, 27, 141, 180, 182, 206, 178, 90, 1032],
  "TOTAL (U.TS.)": [744, 702, 1285, 1526, 1680, 1960, 2078, 1685, 11660],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Bangalore": [0, 452, 871, 1484, 1357, 1360, 1372, 1010, 7906],
  "Bhopal": [24, 51, 389, 491, 364, 493, 298, 119, 2229],
  "Calcutta": [126, 191, 189, 351, 258, 201, 395, 171, 1882],
  "Chennai": [173, 159, 371, 946, 858, 864, 596, 626, 4593],
  "Coimbatore": [53, 41, 162, 267, 212, 268, 263, 159, 1425],
  "Delhi (City)": [584, 576, 916, 1116, 1256, 1466, 1541, 1303, 8758],
  "Hyderabad": [84, 74, 182, 257, 199, 288, 251, 180, 1515],
  "Indore": [58, 117, 523, 481, 551, 436, 496, 128, 2790],
  "Jaipur": [101, 107, 226, 376, 442, 370, 322, 233, 2177],
  "Kanpur": [65, 90, 95, 105, 89, 109, 75, 98, 726],
  "Kochi": [42, 118, 364, 428, 352, 464, 472, 261, 2501],
  "Lucknow": [41, 48, 58, 96, 74, 67, 87, 57, 528],
  "Ludhiana": [1, 3, 14, 10, 5, 8, 4, 4, 49],
  "Madurai": [35, 61, 79, 145, 171, 213, 68, 37, 809],
  "Mumbai": [698, 612, 769, 749, 442, 369, 269, 213, 4121],
  "Nagpur": [119, 60, 128, 290, 283, 297, 315, 266, 1758],
  "Patna": [19, 26, 22, 24, 20, 22, 23, 18, 174],
  "Pune": [30, 25, 23, 38, 51, 40, 51, 65, 323],
  "Surat": [82, 46, 165, 212, 262, 226, 276, 168, 1437],
  "Vadodara": [94, 102, 243, 342, 337, 290, 290, 242, 1940],
  "Varanasi": [12, 22, 21, 24, 14, 20, 17, 14, 144],
  "Vishakhapatnam": [44, 53, 109, 153, 152, 165, 164, 110, 950],
  "TOTAL (CITIES)": [2485, 3034, 5919, 8385, 7749, 8036, 7645, 5482, 48735],
 },
 "Grand": {"GRAND TOTAL": [24708, 29710, 39731, 47203, 45202, 46566, 43066, 30190, 306376]},
}
