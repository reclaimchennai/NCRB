# CII 1994, Table 6: incidence of cognizable IPC crime by crime head, 23 cities
# (raw/cii/1994/table_content/table6-1994_2.pdf, pages 1-5, printed pages 55-59; the cities are the lower block of each
# page, the States / UTs are in cii_1994_crime.py). Read from the page images; the rate (R) columns are skipped.
# Kidnapping & abduction is the printed total; its two printed sub-columns (of women & girls, of others) add up to it on
# every row and are left out so the heads add up to the Total. The cities have no printed total row. Every row adds up
# to its printed Total cognizable crimes under IPC (scripts/check_handread.py), with no corrections. Two blurred last
# digits (5 or 6) are read as the row totals confirm: Surat Cheating 195, Vadodara Riots 265.
KIND, YEAR, PUB = "crime", 1994, "cii"
SOURCE = "raw/cii/1994/table_content/table6-1994_2.pdf"
PAGES = "1-5"
TITLE = "Table 6: Incidence (I) & rate (R) of cognizable crimes (IPC) under different crime heads in States, UTs & cities during 1994"
CATS = ["Murder", "Attempt to commit murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Preparation & assembly for dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Other IPC crimes", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "Cities": {
  "Ahmedabad": [101, 65, 1, 20, 113, 17, 0, 134, 868, 4554, 143, 110, 160, 19, 4896, 11201],
  "Bangalore": [213, 275, 7, 61, 152, 90, 1, 576, 2547, 8965, 1041, 245, 1013, 367, 14387, 29940],
  "Bhopal": [51, 138, 2, 62, 30, 2, 2, 132, 634, 1402, 58, 16, 79, 7, 5105, 7720],
  "Bombay": [354, 229, 5, 150, 234, 113, 57, 754, 2707, 13484, 233, 565, 1243, 57, 15190, 35375],
  "Calcutta": [77, 124, 22, 36, 90, 35, 33, 154, 174, 4897, 413, 257, 630, 34, 4425, 11401],
  "Coimbatore": [23, 21, 0, 1, 5, 0, 0, 15, 230, 778, 229, 8, 20, 93, 1663, 3086],
  "Delhi": [396, 393, 62, 252, 916, 11, 12, 328, 1442, 12654, 149, 527, 1338, 95, 15903, 34478],
  "Hyderabad": [99, 31, 2, 49, 108, 7, 0, 72, 1327, 3243, 173, 84, 586, 12, 4063, 9856],
  "Indore": [89, 134, 1, 29, 33, 2, 1, 80, 745, 2499, 67, 37, 113, 0, 5139, 8969],
  "Jaipur": [63, 36, 1, 22, 145, 4, 0, 64, 771, 2489, 1216, 164, 810, 118, 4905, 10808],
  "Kanpur": [297, 216, 25, 31, 211, 36, 6, 193, 415, 1593, 203, 300, 254, 109, 2687, 6576],
  "Kochi": [25, 8, 3, 7, 7, 4, 0, 10, 227, 262, 212, 12, 113, 3, 3227, 4120],
  "Lucknow": [177, 194, 16, 33, 142, 32, 12, 222, 994, 3096, 290, 257, 277, 2, 2533, 8277],
  "Ludhiana": [40, 30, 6, 11, 25, 0, 7, 7, 112, 155, 4, 13, 41, 2, 398, 851],
  "Madras": [94, 256, 10, 14, 25, 4, 0, 63, 453, 2829, 68, 267, 364, 68, 1472, 5987],
  "Madurai": [26, 80, 0, 4, 12, 4, 0, 42, 171, 977, 157, 30, 99, 93, 2142, 3837],
  "Nagpur": [87, 60, 3, 46, 61, 8, 0, 276, 864, 2648, 127, 69, 135, 12, 4211, 8607],
  "Patna": [224, 240, 19, 25, 122, 63, 24, 175, 471, 1763, 312, 179, 113, 0, 1555, 5285],
  "Pune": [92, 37, 3, 52, 54, 15, 0, 102, 839, 2035, 78, 63, 172, 18, 5284, 8844],
  "Surat": [93, 54, 0, 10, 39, 17, 0, 66, 456, 1683, 134, 103, 195, 4, 1918, 4772],
  "Vadodara": [35, 13, 1, 13, 41, 7, 0, 26, 364, 1305, 265, 107, 249, 5, 2413, 4844],
  "Varanasi": [70, 112, 8, 9, 43, 6, 3, 73, 184, 593, 119, 62, 41, 6, 870, 2199],
  "Vishakhapatnam": [24, 19, 1, 21, 20, 3, 0, 21, 347, 1094, 13, 49, 177, 11, 1636, 3436],
 },
}
