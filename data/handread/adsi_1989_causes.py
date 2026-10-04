# ADSI 1989, Appendix III: distribution of suicides by causes and sex (State, UT & City-wise), pages 1-6 (upright;
# three causes per page, each printed as Male / Female / Total; page 6 Other causes and the Grand Total). Only the
# Total columns are recorded here; every Male + Female = Total and every row's Male and Female columns add up to the
# printed Grand Total Male and Female (checked while reading, with the readings noted in CORRECTIONS). The All India
# row is printed "Total (All - India)" (kept here as GRAND TOTAL); the cities have no printed totals row. Read from the
# page images. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1989, "adsi"
SOURCE = "raw/adsi/1989/table_content/1680164134appendix-31989.pdf"
PAGES = "1-6"
TITLE = "Appendix III: Distribution of Suicides By Causes And Sex During 1989 (State, UT & City-wise)"
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic status", "Death of dear person", "Fall in social reputation",
        "Dowry dispute", "Illegitimate pregnancy", "Cause not known", "Other causes", "Total"]
# Page 5's Cause not known columns are washed out for Assam, Bihar and Goa. The figures below are read from the
# visible parts of the digits and are the only values that make the arithmetic work: Assam male "13?1" (1371) and
# total "188?" (1889 = 1371 + 518 female); Bihar total "4??" (423 = 244 + 179); Goa male "4?" (47) and total "6?"
# (61 = 47 + 14). Each row then adds up to its printed Grand Total (male, female and total), and the States' male
# column to the printed 6743 (1371 + 47 = the 1418 the other States leave) and total column to the printed 10759.
CORRECTIONS = {
    ("Assam", "Cause not known"): ("188?", 1889, "last digit washed out; 1371 male + 518 female = 1889, the row then adds up to the printed 2618 and the States' column to the printed 10759"),
    ("Bihar", "Cause not known"): ("4??", 423, "last two digits washed out; 244 male + 179 female = 423, the row then adds up to the printed 991"),
    ("Goa", "Cause not known"): ("6?", 61, "second digit washed out; 47 male + 14 female = 61, the row then adds up to the printed 175"),
    ("Pune", "Unemployment"): (0, 7, "printed Male 7, Female 0, Total 0; the Total is 7 = 7 + 0, the male column then adds up to the printed 129 and the Total row to the printed 219"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [57, 229, 164, 210, 132, 70, 197, 1525, 39, 55, 13, 29, 129, 5, 651, 1962, 5467],
  "Arunachal Pradesh": [0, 0, 1, 1, 3, 0, 0, 6, 0, 0, 0, 0, 0, 0, 26, 17, 54],
  "Assam": [39, 35, 58, 10, 118, 48, 39, 53, 43, 1, 7, 9, 4, 24, 1889, 241, 2618],
  "Bihar": [17, 45, 50, 31, 32, 27, 9, 33, 18, 5, 9, 16, 45, 4, 423, 227, 991],
  "Goa": [1, 0, 7, 0, 18, 22, 2, 7, 3, 3, 0, 0, 3, 0, 61, 48, 175],
  "Gujarat": [52, 113, 239, 46, 140, 171, 38, 334, 159, 47, 48, 26, 19, 3, 227, 849, 2511],
  "Haryana": [14, 182, 135, 17, 18, 13, 28, 125, 27, 8, 0, 4, 20, 15, 82, 852, 1540],
  "Himachal Pradesh": [1, 6, 4, 2, 14, 6, 3, 7, 3, 0, 0, 2, 3, 1, 34, 24, 110],
  "Jammu & Kashmir": [1, 10, 3, 1, 5, 3, 0, 0, 1, 0, 2, 0, 3, 0, 15, 6, 50],
  "Karnataka": [78, 126, 116, 355, 203, 170, 203, 1156, 102, 82, 47, 11, 54, 4, 985, 3856, 7548],
  "Kerala": [48, 621, 209, 20, 226, 235, 217, 743, 198, 300, 22, 91, 3, 2, 751, 3515, 7201],
  "Madhya Pradesh": [80, 634, 265, 67, 194, 181, 46, 640, 17, 31, 51, 62, 178, 9, 372, 2333, 5160],
  "Maharashtra": [105, 431, 462, 142, 220, 236, 141, 731, 90, 89, 19, 18, 146, 4, 348, 3583, 6765],
  "Manipur": [0, 0, 14, 0, 3, 0, 0, 6, 0, 1, 0, 0, 0, 0, 29, 7, 60],
  "Meghalaya": [0, 0, 3, 2, 6, 2, 0, 8, 0, 0, 1, 0, 0, 1, 57, 6, 86],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 0, 29],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 13],
  "Orissa": [68, 273, 165, 26, 116, 64, 33, 326, 16, 8, 11, 31, 29, 9, 575, 987, 2737],
  "Punjab": [7, 25, 11, 23, 9, 22, 6, 31, 8, 2, 5, 2, 14, 1, 74, 31, 271],
  "Rajasthan": [23, 101, 109, 40, 39, 141, 36, 124, 13, 4, 15, 25, 13, 4, 235, 450, 1372],
  "Sikkim": [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 33, 0, 37],
  "Tamil Nadu": [172, 570, 525, 436, 414, 202, 151, 1278, 197, 98, 85, 73, 212, 62, 829, 2982, 8286],
  "Tripura": [30, 94, 30, 0, 65, 24, 5, 26, 12, 0, 2, 0, 0, 0, 26, 280, 594],
  "Uttar Pradesh": [12, 72, 130, 42, 54, 48, 96, 288, 11, 15, 6, 15, 63, 3, 297, 981, 2133],
  "West Bengal": [256, 741, 666, 378, 917, 436, 136, 570, 124, 32, 88, 94, 132, 76, 2698, 4129, 11473],
  "TOTAL (STATES)": [1061, 4308, 3366, 1852, 2946, 2121, 1386, 8017, 1081, 781, 431, 508, 1071, 227, 10759, 27366, 67281],
 },
 "U.Ts.": {
  "A & N Islands": [1, 0, 4, 2, 4, 4, 0, 5, 0, 0, 0, 0, 0, 0, 86, 0, 106],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 25, 15, 57],
  "D & N Haveli": [0, 0, 19, 0, 0, 8, 0, 1, 0, 1, 0, 0, 0, 0, 0, 5, 34],
  "Daman & Diu": [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
  "Delhi": [15, 5, 33, 5, 21, 15, 3, 57, 15, 5, 5, 4, 46, 0, 201, 378, 808],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [0, 249, 11, 8, 3, 21, 8, 120, 4, 4, 1, 0, 0, 0, 26, 0, 455],
  "TOTAL (U.TS.)": [16, 254, 67, 16, 29, 49, 11, 200, 19, 10, 6, 4, 46, 0, 338, 398, 1463],
 },
 "Cities": {
  "Ahmedabad": [12, 15, 34, 5, 14, 17, 0, 77, 36, 18, 6, 2, 4, 0, 32, 82, 354],
  "Bangalore": [6, 3, 0, 10, 4, 1, 0, 61, 13, 1, 1, 0, 19, 0, 44, 929, 1092],
  "Bombay": [19, 26, 63, 29, 33, 26, 16, 62, 34, 4, 8, 9, 32, 2, 176, 77, 616],
  "Calcutta": [2, 12, 9, 0, 2, 1, 2, 12, 0, 3, 0, 1, 8, 1, 0, 20, 73],
  "Delhi": [13, 3, 27, 5, 19, 15, 2, 56, 13, 5, 4, 4, 40, 0, 175, 297, 678],
  "Hyderabad": [3, 14, 5, 4, 9, 5, 2, 28, 5, 2, 2, 8, 22, 0, 158, 133, 400],
  "Jaipur": [1, 1, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 62, 54, 126],
  "Kanpur": [1, 0, 1, 2, 2, 3, 0, 16, 0, 2, 1, 2, 14, 2, 42, 59, 147],
  "Lucknow": [0, 3, 0, 2, 0, 0, 2, 33, 0, 0, 0, 0, 0, 0, 0, 15, 55],
  "Madras": [40, 110, 112, 110, 80, 66, 19, 279, 80, 15, 3, 0, 5, 21, 159, 469, 1568],
  "Nagpur": [0, 0, 1, 0, 1, 3, 0, 7, 0, 0, 0, 0, 0, 0, 6, 117, 135],
  "Pune": [0, 4, 0, 9, 5, 0, 1, 4, 7, 5, 0, 0, 13, 0, 0, 171, 219],
 },
 "Grand": {"GRAND TOTAL": [1077, 4562, 3433, 1868, 2975, 2170, 1397, 8217, 1100, 791, 437, 512, 1117, 227, 11097, 27764, 68744]},
}
