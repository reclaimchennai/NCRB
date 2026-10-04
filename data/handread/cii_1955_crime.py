# Crime in India 1955, Appendices I, III, V, VII, IX, XI, XIII, XV, XVII, XIX, XXI (the "-CASES" appendices): cognizable
# crime cases reported during the year, by State, under each head (raw/cii/1955/year_wise/1686382133APPENDIX0.pdf, the
# left-hand pages 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42). The 1955 edition prints no single State x head table: each
# head has its own appendix (I Total cognizable crime, III Murder, V Kidnapping and abduction, VII Dacoity, IX Robbery,
# XI House breaking, XIII Thefts, XV Riots, XVII Criminal breach of trust, XIX Cheating, XXI Counterfeit coins & notes),
# and each column here is that appendix's column 4, "Cases reported during the year". The heads printed do not cover all
# IPC crime, so they do not add up to the total: CHECK = "columns", each head checked against the printed Part 'A' / 'B' /
# 'C' totals (Part A + B + C = Grand Total checked when built). '..' (nil) is 0.
KIND, YEAR, PUB = "crime", 1955, "cii"
SOURCE = "raw/cii/1955/year_wise/1686382133APPENDIX0.pdf"
PAGES = "2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42"
TITLE = "Appendices I-XXI (cases): Total cognizable crime and each head - cases reported during the year, by State, 1955"
CATS = ["Murder", "Kidnapping and abduction", "Dacoity", "Robbery", "House breaking", "Thefts (cattle)", "Thefts (ordinary)", "Riots", "Criminal breach of trust", "Cheating", "Counterfeit coins & notes", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
    ('Punjab', 'Criminal breach of trust'): (None, 346, "printed 34? with the last digit broken; the Part 'A' total (11,897) requires 346, and so does the row's own disposal: 263 pending + 346 reported = 334 not investigated/pending + 76 not detected + 199 trial completed"),
}
ROWS = {
 "Part 'A' States": {
  "Andhra": [569, 121, 36, 94, 3965, 1330, 8729, 1761, 741, 296, 14, 23498],
  "Assam": [341, 322, 244, 152, 4793, 312, 4577, 1418, 271, 217, 52, 17446],
  "Bihar": [841, 424, 1412, 815, 20044, 545, 17709, 4078, 792, 514, 161, 57531],
  "Bombay": [1490, 615, 466, 1803, 12301, 1462, 27600, 1105, 2864, 1667, 24, 69049],
  "Madhya Pradesh": [702, 289, 85, 399, 10793, 1615, 26852, 1223, 1140, 1126, 56, 56133],
  "Madras": [927, 480, 104, 342, 6998, 3171, 21744, 2293, 1873, 782, 34, 54051],
  "Orissa": [255, 97, 81, 196, 4808, 499, 8009, 1031, 510, 391, 29, 19943],
  "Punjab": [477, 338, 16, 151, 3933, 675, 3889, 267, 346, 346, 24, 16005],
  "Uttar Pradesh": [1468, 732, 855, 427, 16282, 2662, 19738, 2795, 2197, 922, 56, 58583],
  "West Bengal": [451, 614, 564, 645, 11456, 526, 23698, 4003, 1163, 1179, 60, 55617],
  "TOTAL (PART 'A' STATES)": [7521, 4032, 3863, 5024, 95373, 12797, 162545, 19974, 11897, 7440, 510, 427856],
 },
 "Part 'B' States": {
  "Hyderabad": [486, 121, 268, 372, 5241, 927, 5285, 808, 492, 478, 11, 20848],
  "Jammu and Kashmir": [58, 80, 55, 91, 912, 229, 515, 231, 107, 44, 2, 3530],
  "Madhya Bharat": [435, 269, 293, 172, 5084, 1386, 5588, 294, 309, 246, 4, 18087],
  "Mysore": [185, 78, 20, 85, 2385, 603, 5429, 289, 403, 193, 13, 12487],
  "Pepsu": [140, 55, 8, 42, 718, 114, 856, 30, 98, 84, 7, 3354],
  "Rajasthan": [387, 465, 96, 406, 4955, 1582, 3153, 992, 327, 295, 9, 17244],
  "Saurashtra": [163, 68, 22, 175, 1644, 170, 1930, 271, 231, 140, 3, 8059],
  "Travancore Cochin": [79, 6, 12, 53, 695, 35, 847, 315, 194, 35, 12, 3983],
  "TOTAL (PART 'B' STATES)": [1933, 1142, 774, 1396, 21634, 5046, 23603, 3230, 2161, 1515, 61, 87592],
 },
 "Part 'C' States": {
  "Ajmer": [14, 11, 2, 9, 323, 35, 348, 11, 9, 17, 0, 916],
  "Bhopal": [32, 34, 8, 28, 797, 50, 635, 45, 37, 46, 1, 2168],
  "Coorg": [6, 2, 1, 1, 103, 26, 194, 3, 34, 6, 0, 480],
  "Delhi": [42, 156, 1, 35, 1191, 50, 4173, 73, 286, 304, 21, 7859],
  "Himachal Pradesh": [15, 41, 3, 35, 274, 23, 286, 29, 54, 18, 1, 1245],
  "Kutch": [22, 8, 0, 46, 226, 48, 529, 47, 46, 16, 0, 1293],
  "Manipur": [7, 40, 4, 6, 112, 44, 159, 45, 46, 50, 1, 757],
  "Tripura": [13, 12, 23, 22, 172, 0, 336, 73, 9, 7, 1, 956],
  "Vindhya Pradesh": [90, 50, 100, 105, 1517, 104, 906, 79, 63, 40, 1, 3929],
  "Andaman and Nicobar Islands": [5, 1, 0, 3, 22, 0, 91, 0, 2, 2, 0, 185],
  "TOTAL (PART 'C' STATES)": [246, 355, 142, 290, 4737, 380, 7657, 405, 586, 506, 26, 19788],
 },
 "Grand": {
  "GRAND TOTAL": [9700, 5529, 4779, 6710, 121744, 18223, 193805, 23609, 14644, 9461, 597, 535236],
 },
}
