# Crime in India 1953, Appendices I-VIII: cognizable crime cases reported in the year, by State, under each head
# (raw/cii/1953/year_wise/1686379941APPENDIX-ALL-TOTALCONGNIZABLECRIME.pdf, pages 1-6, 8, 10). The 1953 edition prints no
# single State x head table: each head has its own appendix (Appendix I Total cognizable crime, II Murder, III Kidnapping &
# abduction, IV Dacoity, V Robbery, VI House-breaking, VII Theft, VIII Rioting), and each column here is that appendix's
# "Number reported in the year". The heads printed are only these, so they do not add up to the total: CHECK = "columns",
# each head checked against the printed Part 'A' / 'B' / 'C' totals (Part A + B + C = Grand Total checked when built).
# '..' (nil) is 0. Jammu & Kashmir figures are not for the calendar year (footnote).
KIND, YEAR, PUB = "crime", 1953, "cii"
SOURCE = "raw/cii/1953/year_wise/1686379941APPENDIX-ALL-TOTALCONGNIZABLECRIME.pdf"
PAGES = "1-6, 8, 10"
TITLE = "Appendices I-VIII: Total cognizable crime, Murder, Kidnapping & abduction, Dacoity, Robbery, House-breaking, Theft, Rioting - number reported in the year, by State, 1953"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House-breaking", "Theft (cattle)", "Theft (ordinary)", "Rioting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
# Theft: Kutch (598), Tripura (616) and Andaman & Nicobar Islands (70) are printed as one figure across the Cattle and
# Ordinary columns; the printed Part 'C' Ordinary total (7,839) includes them, so the figure is kept under Theft (ordinary)
# and Theft (cattle) is None for those three.
CORRECTIONS = {
}
ROWS = {
 "Part 'A' States": {
  "Andhra": [642, 113, 99, 169, 6051, 2229, 12182, 1169, 29240],
  "Assam": [267, 255, 334, 174, 5462, 276, 5012, 984, 17885],
  "Bihar": [788, 421, 1395, 841, 21955, 631, 18480, 3588, 59943],
  "Bombay": [1343, 627, 683, 2120, 15016, 1930, 33511, 1161, 78614],
  "Madhya Pradesh": [629, 231, 68, 409, 12433, 2019, 29002, 1026, 58923],
  "Madras": [1048, 300, 270, 569, 12865, 7168, 34529, 1732, 75591],
  "Orissa": [230, 125, 74, 223, 4839, 484, 8810, 1111, 20895],
  "Punjab": [526, 388, 40, 261, 5263, 1171, 4607, 236, 18889],
  "Uttar Pradesh": [1527, 787, 871, 522, 18284, 2938, 22208, 2975, 63864],
  "West Bengal": [447, 386, 709, 998, 13605, 633, 24743, 3159, 55887],
  "TOTAL (PART 'A' STATES)": [7447, 3633, 4543, 6286, 115773, 19479, 193084, 17141, 479731],
 },
 "Part 'B' States": {
  "Hyderabad": [541, 162, 312, 524, 5709, 1521, 5769, 710, 22337],
  "Jammu & Kashmir": [46, 68, 59, 55, 892, 130, 490, 208, 3044],
  "Madhya Bharat": [424, 274, 230, 255, 6008, 1581, 7274, 255, 21013],
  "Mysore": [179, 76, 16, 86, 3025, 576, 6221, 178, 13150],
  "Pepsu": [217, 91, 16, 136, 1122, 238, 999, 41, 4762],
  "Rajasthan": [373, 472, 162, 502, 6461, 2472, 3977, 1082, 21299],
  "Saurashtra": [161, 100, 28, 207, 2353, 303, 2656, 231, 10338],
  "Travancore-Cochin": [152, 5, 21, 97, 975, 64, 1399, 380, 6403],
  "TOTAL (PART 'B' STATES)": [2093, 1248, 844, 1862, 26545, 6885, 28785, 3085, 102346],
 },
 "Part 'C' States": {
  "Ajmer": [18, 14, 4, 8, 345, 53, 370, 14, 1691],
  "Bhopal": [24, 44, 19, 11, 782, 51, 634, 32, 1229],
  "Coorg": [2, 0, 1, 2, 70, 17, 111, 0, 325],
  "Delhi": [60, 171, 0, 38, 1200, 85, 3927, 69, 7625],
  "Himachal Pradesh": [14, 33, 5, 31, 270, 28, 288, 18, 1200],
  "Kutch": [19, 10, 11, 36, 349, None, 598, 49, 1434],
  "Manipur": [10, 38, 8, 3, 168, 109, 247, 20, 952],
  "Tripura": [16, 11, 66, 31, 26, None, 616, 41, 1084],
  "Vindhya Pradesh": [95, 56, 78, 97, 1827, 152, 978, 59, 4193],
  "Andaman & Nicobar Islands": [4, 3, 0, 2, 24, None, 70, 1, 154],
  "TOTAL (PART 'C' STATES)": [262, 380, 192, 259, 5061, 495, 7839, 303, 19887],
 },
 "Grand": {
  "GRAND TOTAL": [9802, 5261, 5579, 8407, 147379, 26859, 229708, 20529, 601964],
 },
}
