# CII 1996, Table 9: city-wise incidence of cognizable IPC crime by crime head
# (raw/cii/1996/table_content/table-9--city-wise-incidence-of-cognizable-crimes-(ipc)-during-1996-1996.pdf, pages 1-4,
# printed pages 204-207; pages 1 and 3 carry columns (3)-(14), pages 2 and 4 columns (15)-(26)). Read from the page
# images. In 1996 the State / UT / city table of the earlier editions (Table 6 with 23 cities) is replaced by this table
# of 63 cities (Trichy without figures) grouped under their States (the State headings are not rows and are left out); it prints incidence only
# and no totals row. Names as printed (Chennai, Bombay Commr., Baroda, Kanpur Nager, Delhi (City), ...). Kidnapping &
# abduction is the printed total; its two printed sub-columns (of women & girls, of others) add up to it on every row and
# are left out so the heads add up to the Total. Trichy is printed 'NA' in every column: None. Every row adds up to its
# printed Total cognizable crimes under IPC (scripts/check_handread.py). Checked besides (not in the checker, as the
# table prints no total): the 23 metropolitan cities of the edition's urban-crime chapter (Ahmedabad, Bangalore, Bhopal,
# Bombay, Calcutta, Coimbatore, Delhi, Hyderabad, Indore, Jaipur, Kanpur, Kochi, Lucknow, Ludhiana, Madras/Chennai,
# Madurai, Nagpur, Patna, Pune, Surat, Vadodara/Baroda, Varanasi, Vishakhapatnam) add up, head by head, to the 'Cities'
# column of Table 2.4 (raw/cii/1996/table_chapter/1679315592CHAPTER-2-URBANCRIMES-1996.pdf, page 7, printed page 53) on
# all 21 heads and the total (2,53,057). No corrections.
KIND, YEAR, PUB = "crime", 1996, "cii"
SOURCE = "raw/cii/1996/table_content/table-9--city-wise-incidence-of-cognizable-crimes-(ipc)-during-1996-1996.pdf"
PAGES = "1-4"
TITLE = "Table 9: City-wise incidence of cognizable crimes (IPC) during 1996"
CATS = ["Murder", "Attempt to commit murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Preparation & assembly for dacoity", "Robbery", "Burglary", "Theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Arson", "Hurt/grievous hurt", "Dowry death", "Molestation", "Sexual harassment", "Cruelty by husband or relatives", "Other IPC crimes", "Total cognizable crimes (IPC)"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "Cities": {
  "Hyderabad": [111, 93, 6, 33, 80, 12, 0, 49, 1026, 2516, 205, 73, 620, 13, 0, 582, 32, 48, 0, 447, 3208, 9154],
  "Vijayawada": [26, 33, 0, 18, 46, 3, 0, 21, 200, 1091, 27, 31, 264, 10, 14, 963, 5, 57, 46, 169, 635, 3659],
  "Vishakhapatnam": [20, 18, 1, 38, 25, 4, 0, 12, 259, 806, 23, 45, 172, 1, 12, 236, 4, 44, 327, 117, 673, 2837],
  "Guwahati": [65, 17, 6, 21, 104, 66, 3, 138, 505, 1382, 103, 62, 71, 26, 7, 233, 2, 19, 1, 21, 2017, 4869],
  "Patna": [228, 344, 20, 18, 95, 54, 16, 223, 306, 1338, 126, 201, 90, 1, 14, 465, 29, 50, 1, 45, 1307, 4971],
  "Ranchi": [92, 73, 13, 15, 29, 13, 5, 127, 201, 490, 59, 23, 97, 2, 1, 93, 6, 37, 0, 26, 608, 2010],
  "Ahmedabad": [95, 58, 2, 13, 122, 24, 0, 225, 705, 3851, 185, 136, 305, 11, 11, 1663, 12, 35, 27, 323, 7441, 15244],
  "Baroda": [44, 23, 0, 8, 49, 20, 0, 31, 423, 1442, 250, 143, 317, 8, 10, 427, 6, 40, 4, 130, 3549, 6924],
  "Bhavnagar": [20, 9, 0, 2, 28, 5, 0, 5, 59, 256, 49, 14, 12, 7, 6, 28, 0, 11, 2, 29, 774, 1316],
  "Rajkot": [32, 19, 0, 3, 25, 4, 0, 27, 270, 608, 67, 30, 45, 7, 10, 293, 5, 20, 9, 107, 1977, 3558],
  "Surat": [100, 28, 0, 17, 49, 29, 0, 67, 475, 1457, 107, 58, 342, 2, 7, 617, 36, 18, 4, 174, 1312, 4899],
  "Bangalore": [201, 283, 0, 34, 105, 42, 2, 513, 2650, 8089, 357, 229, 1069, 1176, 184, 3417, 56, 150, 40, 143, 10135, 28875],
  "Belgaum": [16, 7, 4, 0, 9, 2, 0, 10, 159, 188, 50, 13, 37, 0, 6, 196, 0, 8, 0, 14, 120, 839],
  "Bijapur": [5, 3, 1, 3, 10, 4, 0, 7, 82, 67, 64, 5, 12, 0, 0, 111, 0, 8, 0, 17, 31, 430],
  "Davanagere": [3, 2, 1, 0, 3, 0, 0, 2, 91, 165, 48, 3, 20, 0, 2, 152, 2, 7, 0, 20, 279, 800],
  "Gulbarga": [7, 16, 0, 2, 16, 5, 0, 35, 120, 193, 80, 6, 19, 0, 15, 158, 0, 7, 0, 29, 298, 1006],
  "Hubli Dharwad": [16, 18, 3, 4, 8, 2, 0, 18, 189, 333, 140, 9, 74, 6, 4, 189, 4, 7, 1, 15, 1017, 2057],
  "Mysore": [21, 37, 0, 16, 21, 2, 0, 52, 364, 707, 54, 48, 127, 4, 0, 514, 8, 19, 3, 80, 1098, 3175],
  "Raichur": [7, 5, 0, 2, 2, 1, 0, 1, 25, 40, 55, 2, 3, 0, 0, 65, 0, 6, 0, 3, 105, 322],
  "Kochi": [11, 18, 8, 11, 6, 5, 0, 14, 320, 272, 152, 18, 131, 0, 2, 426, 1, 31, 1, 16, 2833, 4276],
  "Kozhikode": [9, 8, 3, 7, 8, 3, 0, 6, 194, 202, 211, 20, 85, 0, 17, 321, 1, 16, 3, 75, 2029, 3218],
  "Thiruvananthapuram": [17, 41, 3, 13, 16, 17, 10, 56, 361, 348, 322, 20, 163, 1, 1, 756, 3, 49, 1, 31, 2361, 4590],
  "Bhilai (Durg)": [20, 32, 5, 30, 17, 0, 0, 46, 337, 470, 23, 7, 25, 1, 2, 714, 5, 61, 18, 13, 883, 2709],
  "Bhopal": [56, 120, 0, 60, 35, 1, 1, 101, 456, 1170, 82, 12, 153, 7, 12, 941, 5, 115, 21, 54, 4310, 7712],
  "Gwalior": [53, 87, 2, 33, 31, 4, 9, 81, 420, 868, 80, 17, 21, 48, 15, 666, 23, 93, 5, 71, 3758, 6385],
  "Indore": [87, 131, 3, 38, 35, 2, 5, 75, 669, 2253, 86, 40, 109, 0, 21, 71, 20, 69, 21, 123, 5167, 9025],
  "Jabalpur": [47, 115, 33, 54, 7, 0, 1, 57, 457, 890, 38, 14, 99, 0, 0, 131, 14, 212, 39, 82, 3536, 5826],
  "Raipur": [26, 55, 6, 56, 12, 1, 0, 25, 310, 544, 47, 14, 95, 1, 9, 154, 4, 47, 11, 47, 1887, 3351],
  "Aurangabad Commr.": [28, 19, 2, 20, 23, 13, 1, 42, 396, 675, 115, 25, 81, 0, 6, 389, 2, 46, 22, 180, 795, 2880],
  "Bombay Commr.": [327, 187, 5, 153, 169, 83, 43, 628, 2554, 14086, 117, 512, 1364, 46, 6, 3728, 32, 264, 34, 181, 7984, 32503],
  "Nagpur Commr.": [101, 65, 0, 46, 67, 16, 1, 244, 1236, 2619, 144, 72, 172, 13, 25, 1072, 1, 77, 1, 114, 3243, 9329],
  "Nasik Commr.": [21, 16, 0, 13, 15, 5, 1, 19, 280, 495, 37, 21, 70, 0, 4, 269, 3, 20, 5, 78, 876, 2248],
  "New Bombay": [38, 15, 2, 18, 19, 23, 4, 71, 469, 749, 75, 56, 58, 2, 3, 343, 2, 38, 14, 41, 948, 2988],
  "Pune Commr.": [85, 37, 2, 55, 61, 10, 5, 73, 746, 2188, 1415, 80, 194, 8, 15, 1268, 9, 84, 135, 167, 2932, 9569],
  "Solapur Commr.": [19, 15, 0, 24, 12, 0, 0, 30, 145, 320, 21, 13, 37, 5, 2, 286, 3, 19, 4, 39, 774, 1768],
  "Thane Commr.": [131, 57, 4, 51, 69, 27, 10, 145, 1147, 1842, 317, 68, 206, 6, 13, 1747, 0, 120, 45, 171, 818, 6994],
  "Amritsar": [21, 7, 1, 2, 13, 0, 0, 4, 81, 83, 0, 15, 26, 4, 1, 57, 7, 2, 0, 26, 191, 541],
  "Jalandhar": [30, 18, 1, 4, 24, 0, 0, 2, 102, 152, 0, 3, 67, 4, 6, 125, 5, 4, 0, 23, 261, 831],
  "Ludhiana": [61, 25, 16, 14, 30, 3, 4, 5, 118, 250, 0, 14, 82, 8, 0, 91, 18, 2, 0, 31, 422, 1194],
  "Ajmer": [14, 53, 4, 13, 53, 0, 0, 19, 169, 375, 140, 6, 159, 11, 6, 620, 6, 18, 3, 87, 407, 2163],
  "Bharatpur": [6, 1, 0, 5, 23, 0, 0, 8, 85, 232, 147, 12, 62, 4, 8, 18, 4, 9, 0, 34, 696, 1354],
  "Bikaner": [37, 77, 1, 36, 44, 2, 0, 5, 223, 368, 199, 10, 125, 3, 8, 77, 7, 78, 0, 157, 2298, 3755],
  "Jaipur": [61, 168, 3, 25, 201, 4, 0, 68, 1015, 3246, 1635, 196, 644, 70, 28, 168, 17, 134, 0, 212, 5523, 13418],
  "Jodhpur": [27, 33, 0, 7, 49, 1, 0, 25, 246, 457, 236, 40, 225, 4, 9, 657, 12, 28, 0, 207, 1011, 3274],
  "Kota": [36, 203, 2, 44, 118, 8, 0, 62, 410, 837, 361, 44, 226, 4, 25, 202, 9, 61, 10, 209, 2069, 4940],
  "Udaipur": [11, 21, 1, 9, 53, 1, 0, 33, 178, 364, 242, 19, 145, 4, 6, 33, 2, 11, 5, 59, 1281, 2478],
  "Chennai": [64, 283, 1, 11, 27, 3, 0, 80, 567, 2732, 58, 117, 388, 60, 0, 434, 8, 14, 0, 88, 1208, 6143],
  "Coimbatore (Urban)": [19, 17, 0, 2, 9, 1, 0, 20, 128, 964, 129, 30, 64, 20, 0, 65, 3, 1, 1, 6, 1789, 3268],
  "Madurai Urban": [26, 73, 1, 4, 14, 8, 0, 78, 158, 1040, 69, 32, 143, 18, 1, 220, 5, 10, 86, 18, 2012, 4016],
  "Salem": [33, 22, 0, 4, 19, 0, 0, 8, 210, 484, 81, 2, 15, 21, 4, 176, 0, 6, 45, 6, 2219, 3355],
  "Trichy": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
  "Agra": [82, 72, 20, 13, 84, 11, 0, 74, 293, 831, 115, 93, 104, 2, 6, 202, 25, 45, 0, 92, 1044, 3208],
  "Aligarh": [46, 65, 7, 15, 91, 4, 0, 41, 113, 319, 73, 27, 39, 0, 1, 73, 11, 40, 0, 69, 584, 1618],
  "Allahabad": [73, 135, 8, 16, 32, 2, 0, 49, 238, 633, 108, 70, 73, 0, 2, 149, 11, 21, 0, 21, 646, 2287],
  "Bareilly": [100, 71, 12, 16, 73, 3, 1, 54, 195, 617, 59, 51, 90, 0, 6, 70, 19, 17, 0, 64, 760, 2278],
  "Gorakhpur": [41, 66, 11, 8, 12, 1, 1, 128, 25, 220, 96, 90, 69, 0, 7, 132, 13, 10, 0, 37, 980, 1947],
  "Kanpur Nager": [169, 170, 21, 38, 159, 37, 3, 139, 605, 1287, 186, 215, 232, 1, 20, 629, 51, 53, 0, 185, 1504, 5704],
  "Lucknow": [117, 135, 20, 17, 80, 7, 7, 86, 399, 1426, 164, 197, 213, 0, 17, 98, 23, 38, 0, 103, 2367, 5514],
  "Meerut": [79, 113, 12, 18, 70, 3, 2, 93, 261, 754, 80, 61, 140, 6, 7, 138, 10, 63, 0, 179, 852, 2941],
  "Moradabad": [54, 61, 18, 21, 39, 10, 2, 41, 17, 328, 41, 35, 49, 0, 11, 199, 35, 65, 0, 192, 281, 1499],
  "Varanasi": [63, 86, 14, 10, 40, 2, 2, 62, 160, 526, 77, 50, 58, 0, 0, 86, 14, 1, 40, 26, 571, 1888],
  "Calcutta": [89, 176, 16, 29, 106, 35, 31, 171, 158, 5462, 485, 216, 603, 32, 5, 1423, 8, 137, 11, 149, 3053, 12395],
  "Delhi (City)": [426, 432, 62, 419, 1050, 24, 20, 522, 2124, 19206, 180, 580, 1739, 66, 79, 2096, 102, 587, 178, 84, 24223, 54199],
 },
}
