# ADSI 1972, Appendix V: statement of number of suicides in States / U.Ts. / cities by causes of suicides, by sex
# (pages 1-8, printed sideways: pages 1-2 Failure in examination to Poverty, pages 3-4 Love affairs to Dreadful
# diseases, pages 5-6 Unemployment to Fall in social reputation, pages 7-8 Other causes, Total Male / Female and Grand
# Total; odd pages the States, even pages the U.Ts. and cities). The table prints only Male and Female per cause (no
# per-cause totals), so CATS are the Male and Female columns in printed order and the last is the Grand Total
# (Male & Female); the printed Total Male and Total Female columns are kept in SEX_TOTALS. Read from the page images;
# ".." (nil) is 0. This table prints no percentages. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1972, "adsi"
SOURCE = "raw/adsi/1972/table_content/1680154594appendix-51972.pdf"
PAGES = "1-8"
TITLE = "Appendix V: Statement of Number of Suicides in States/U.Ts./Cities during 1972 (By Causes of Suicides)"
_C = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
      "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
      "Bankruptcy or sudden change in economic position", "Deaths of dear persons", "Fall in social reputation",
      "Other causes"]
CATS = [f"{c}, {s}" for c in _C for s in ("Male", "Female")] + ["Grand Total"]
CORRECTIONS = {
    ("Calcutta", "Dispute over property, Female"): (3, 0, "printed '3' (clear); Calcutta's female columns then add up to 17 against the printed Total Female 14 and the cities' column to 11 against the printed TOTAL (CITIES) 8; with 0 both add up exactly (the male columns already add up to the printed 19), and Appendix VII (raw/adsi/1972/table_content/1680154544appendix-71972.pdf, page 4) prints Calcutta's dispute over property as '.. (0.0)' and the cities' total as 25 = 17 male + 8 female"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [17, 2, 111, 111, 33, 54, 112, 72, 27, 25, 23, 19, 56, 39, 813, 573, 15, 5, 17, 5, 4, 5, 1, 0, 707, 440, 3286],
  "Assam": [45, 18, 83, 36, 34, 23, 41, 17, 55, 63, 31, 11, 24, 2, 146, 44, 12, 3, 6, 4, 0, 0, 4, 0, 367, 146, 1215],
  "Bihar": [4, 0, 6, 13, 5, 10, 2, 1, 17, 5, 10, 5, 7, 4, 28, 8, 0, 0, 4, 0, 0, 0, 0, 0, 461, 330, 920],
  "Gujarat": [12, 3, 6, 89, 38, 87, 47, 16, 18, 14, 90, 54, 14, 9, 119, 70, 21, 3, 11, 2, 5, 9, 8, 13, 337, 229, 1324],
  "Haryana": [30, 14, 33, 40, 29, 25, 9, 3, 14, 11, 4, 5, 15, 1, 31, 22, 5, 1, 2, 0, 5, 3, 0, 0, 107, 36, 445],
  "Himachal Pradesh": [0, 1, 2, 4, 2, 5, 1, 0, 4, 0, 3, 3, 0, 0, 2, 4, 0, 0, 1, 0, 2, 0, 0, 0, 8, 7, 49],
  "Jammu & Kashmir": [0, 0, 3, 0, 0, 0, 3, 0, 1, 0, 0, 0, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 4, 33],
  "Karnataka": [25, 4, 37, 70, 37, 56, 131, 63, 56, 41, 56, 40, 36, 13, 465, 320, 36, 7, 44, 3, 7, 6, 26, 10, 1386, 564, 3539],
  "Kerala": [65, 32, 227, 171, 70, 69, 343, 211, 131, 137, 153, 69, 128, 30, 420, 149, 152, 27, 215, 91, 11, 0, 6, 3, 1186, 404, 4500],
  "Madhya Pradesh": [13, 7, 158, 92, 85, 138, 42, 8, 25, 18, 59, 47, 28, 10, 350, 289, 3, 0, 6, 0, 2, 5, 11, 9, 1317, 640, 3362],
  "Maharashtra": [37, 8, 183, 176, 88, 143, 123, 41, 37, 36, 91, 65, 49, 9, 413, 245, 41, 5, 25, 1, 6, 6, 11, 2, 1534, 903, 4278],
  "Manipur": [0, 0, 1, 0, 0, 0, 1, 1, 3, 2, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 7, 1, 20],
  "Meghalaya": [0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 104, 13, 127],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8],
  "Orissa": [4, 0, 101, 179, 84, 110, 3, 2, 33, 28, 6, 3, 30, 49, 170, 140, 1, 0, 4, 0, 0, 0, 16, 4, 1062, 432, 2461],
  "Punjab": [21, 9, 31, 24, 22, 9, 15, 9, 13, 13, 14, 1, 11, 5, 25, 3, 10, 2, 3, 0, 1, 1, 6, 2, 355, 44, 649],
  "Rajasthan": [2, 0, 37, 55, 26, 36, 12, 0, 9, 11, 3, 2, 14, 4, 113, 76, 2, 0, 1, 0, 5, 3, 6, 4, 58, 34, 513],
  "Tamil Nadu": [53, 10, 226, 125, 67, 78, 163, 62, 115, 81, 38, 29, 72, 30, 786, 364, 69, 17, 38, 7, 20, 14, 63, 15, 1479, 748, 4769],
  "Tripura": [8, 3, 16, 21, 6, 15, 1, 0, 8, 18, 12, 6, 1, 0, 33, 9, 1, 4, 1, 0, 0, 0, 0, 0, 43, 52, 258],
  "Uttar Pradesh": [36, 34, 108, 212, 92, 144, 100, 22, 60, 53, 54, 25, 89, 33, 488, 261, 28, 24, 26, 10, 15, 15, 38, 25, 1326, 731, 4049],
  "West Bengal": [301, 225, 618, 783, 357, 637, 123, 143, 304, 239, 122, 70, 50, 16, 494, 312, 26, 5, 37, 14, 5, 10, 15, 27, 1307, 1031, 7271],
  "TOTAL (STATES)": [673, 370, 1987, 2201, 1075, 1639, 1272, 671, 933, 796, 769, 455, 629, 256, 4901, 2891, 422, 104, 441, 137, 89, 77, 219, 114, 13166, 6789, 43076],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 3, 2, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 43, 9, 62],
  "Chandigarh": [3, 0, 0, 0, 5, 4, 0, 0, 0, 0, 2, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 23],
  "D. & N. Haveli": [0, 0, 6, 3, 3, 7, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 11, 3, 38],
  "Delhi": [3, 2, 25, 12, 11, 23, 2, 0, 2, 3, 1, 0, 1, 1, 4, 5, 4, 0, 2, 0, 0, 1, 0, 1, 35, 11, 149],
  "Goa, Daman & Diu": [0, 1, 0, 0, 1, 6, 1, 1, 2, 1, 8, 3, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 24, 4, 57],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 9],
  "Pondicherry": [0, 0, 10, 6, 8, 13, 1, 1, 5, 0, 2, 1, 0, 0, 40, 20, 0, 0, 4, 0, 1, 0, 0, 0, 49, 26, 187],
  "TOTAL (U.TS.)": [6, 3, 44, 23, 28, 54, 9, 3, 9, 5, 16, 5, 2, 1, 50, 28, 5, 0, 7, 0, 2, 1, 1, 1, 168, 54, 525],
 },
 "Cities": {
  "Ahmedabad": [0, 1, 0, 3, 3, 18, 2, 4, 2, 2, 1, 6, 0, 0, 18, 12, 0, 0, 5, 1, 0, 2, 2, 5, 42, 31, 160],
  "Bangalore": [0, 1, 6, 5, 2, 4, 2, 2, 3, 2, 1, 1, 1, 0, 35, 30, 6, 1, 1, 0, 1, 4, 3, 2, 229, 24, 366],
  "Bombay": [1, 1, 0, 6, 1, 4, 6, 2, 9, 10, 1, 2, 3, 1, 16, 8, 6, 0, 5, 0, 0, 1, 1, 0, 58, 33, 175],
  "Calcutta": [0, 0, 0, 0, 0, 1, 2, 0, 0, 1, 1, 1, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 12, 10, 33],
  "Delhi": [3, 2, 24, 4, 9, 23, 2, 0, 0, 3, 1, 0, 0, 0, 4, 5, 4, 0, 2, 0, 0, 1, 0, 1, 33, 10, 131],
  "Hyderabad": [8, 5, 5, 4, 2, 3, 7, 4, 1, 1, 0, 1, 0, 0, 19, 17, 0, 0, 0, 0, 0, 0, 0, 0, 50, 27, 154],
  "Kanpur": [0, 0, 0, 5, 2, 2, 3, 0, 0, 1, 0, 0, 12, 1, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 7, 9, 52],
  "Madras": [2, 1, 4, 9, 1, 6, 1, 1, 4, 5, 1, 0, 1, 6, 68, 53, 11, 0, 1, 0, 0, 0, 0, 1, 36, 9, 221],
  "TOTAL (CITIES)": [14, 11, 39, 36, 20, 61, 25, 13, 19, 25, 6, 11, 17, 8, 172, 128, 27, 1, 14, 1, 1, 8, 6, 9, 467, 153, 1292],
 },
 "Grand": {"GRAND TOTAL": [679, 373, 2031, 2224, 1103, 1693, 1281, 674, 942, 801, 785, 460, 631, 257, 4951, 2919, 427, 104, 448, 137, 91, 78, 220, 115, 13334, 6843, 43601]},
}
# the printed Total Male and Total Female columns (both add up for every row)
SEX_TOTALS = {
 "Andhra Pradesh": (1936, 1350),
 "Assam": (848, 367),
 "Bihar": (544, 376),
 "Gujarat": (726, 598),
 "Haryana": (284, 161),
 "Himachal Pradesh": (25, 24),
 "Jammu & Kashmir": (27, 6),
 "Karnataka": (2342, 1197),
 "Kerala": (3107, 1393),
 "Madhya Pradesh": (2099, 1263),
 "Maharashtra": (2638, 1640),
 "Manipur": (14, 6),
 "Meghalaya": (111, 16),
 "Nagaland": (8, 0),
 "Orissa": (1514, 947),
 "Punjab": (527, 122),
 "Rajasthan": (288, 225),
 "Tamil Nadu": (3189, 1580),
 "Tripura": (130, 128),
 "Uttar Pradesh": (2460, 1589),
 "West Bengal": (3759, 3512),
 "TOTAL (STATES)": (26576, 16500),
 "A. & N. Islands": (48, 14),
 "Chandigarh": (16, 7),
 "D. & N. Haveli": (24, 14),
 "Delhi": (90, 59),
 "Goa, Daman & Diu": (41, 16),
 "Lakshadweep": (0, 0),
 "Mizoram": (8, 1),
 "Pondicherry": (120, 67),
 "TOTAL (U.TS.)": (347, 178),
 "GRAND TOTAL": (26923, 16678),
 "Ahmedabad": (75, 85),
 "Bangalore": (290, 76),
 "Bombay": (107, 68),
 "Calcutta": (19, 14),
 "Delhi": (82, 49),
 "Hyderabad": (92, 62),
 "Kanpur": (32, 20),
 "Madras": (130, 91),
 "TOTAL (CITIES)": (827, 465),
}
