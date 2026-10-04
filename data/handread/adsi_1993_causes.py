# ADSI 1993, Appendix IV: distribution of suicides by causes and sex (State, UT & City-wise), 12 pages, all upright.
# Pages 1-6 State & UT-wise, three causes per page each printed as Male / Female / Total (page 6 Other causes and the
# Grand Total); pages 7-12 the same columns for cities 33-55, which have no printed totals row. The 16 causes are the
# same as in 1991 and in the same order (the heading prints "Econimic"). Only the Total columns are recorded here;
# while reading, Male, Female and Total were all transcribed and checked: every Male + Female = Total in every cell;
# every row's 16 causes add to its printed Grand Total separately for Male, Female and Total; every Male, Female and
# Total column of the States adds to the printed Total (States), of the UTs to Total (UTs), and Total (States) +
# Total (UTs) = the printed "Total (All - India)" (kept here as GRAND TOTAL). Every check passed with the figures as
# printed, so no figure is changed. The shaded totals rows are faint on pages 4-6 (e.g. bankruptcy totals 1259 and
# 1269, Grand Total male 48798 for the States); each reading is the only one that satisfies both the Male + Female
# sum and the States + UTs = All-India sum. Read from the page images. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1993, "adsi"
SOURCE = "raw/adsi/1993/archived/appendix-4_1993.pdf"
PAGES = "1-12"
TITLE = "Appendix IV: Distribution of Suicides by Causes and Sex during 1993 (State, UT & City-wise)"
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic status", "Death of dear person", "Fall in social reputation",
        "Dowry dispute", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [86, 345, 229, 360, 164, 142, 182, 2063, 37, 148, 27, 26, 238, 15, 1198, 2590, 7850],
  "Arunachal Pradesh": [0, 0, 2, 0, 3, 1, 0, 5, 0, 1, 0, 0, 0, 0, 44, 0, 56],
  "Assam": [41, 68, 33, 50, 75, 74, 24, 52, 21, 20, 15, 87, 15, 15, 1369, 598, 2557],
  "Bihar": [23, 50, 28, 61, 46, 34, 51, 64, 24, 15, 33, 4, 45, 6, 742, 417, 1643],
  "Goa": [1, 4, 8, 9, 19, 22, 2, 11, 3, 1, 1, 0, 0, 0, 93, 29, 203],
  "Gujarat": [51, 146, 281, 71, 140, 277, 18, 456, 137, 96, 47, 48, 34, 5, 480, 1144, 3431],
  "Haryana": [29, 48, 75, 21, 25, 7, 38, 202, 20, 4, 9, 26, 41, 4, 248, 457, 1254],
  "Himachal Pradesh": [7, 19, 12, 6, 12, 5, 2, 23, 10, 0, 4, 0, 0, 0, 34, 36, 170],
  "Jammu & Kashmir": [4, 0, 5, 0, 3, 1, 1, 0, 2, 1, 0, 1, 7, 0, 27, 18, 70],
  "Karnataka": [102, 137, 174, 272, 168, 215, 35, 1693, 74, 109, 41, 23, 78, 5, 2034, 2895, 8055],
  "Kerala": [83, 573, 460, 3, 186, 441, 287, 1081, 180, 385, 77, 68, 11, 17, 477, 3795, 8124],
  "Madhya Pradesh": [103, 731, 733, 89, 347, 324, 109, 829, 33, 33, 63, 100, 161, 11, 903, 1682, 6251],
  "Maharashtra": [130, 785, 973, 266, 261, 395, 141, 1028, 133, 136, 58, 66, 112, 7, 936, 4911, 10338],
  "Manipur": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 19],
  "Meghalaya": [0, 3, 1, 1, 5, 6, 0, 10, 0, 0, 0, 0, 0, 1, 20, 24, 71],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 25],
  "Nagaland": [0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0, 8, 8, 20],
  "Orissa": [76, 170, 211, 20, 212, 65, 30, 167, 26, 6, 16, 25, 98, 18, 914, 1291, 3345],
  "Punjab": [0, 8, 22, 8, 14, 33, 7, 44, 4, 3, 3, 2, 18, 0, 185, 142, 493],
  "Rajasthan": [137, 144, 160, 44, 66, 127, 60, 189, 41, 28, 14, 57, 82, 3, 537, 1040, 2729],
  "Sikkim": [2, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 42, 0, 48],
  "Tamil Nadu": [154, 530, 533, 307, 414, 140, 107, 1729, 135, 146, 41, 33, 87, 14, 940, 2585, 7895],
  "Tripura": [37, 68, 34, 0, 50, 36, 0, 24, 0, 0, 2, 2, 0, 0, 43, 247, 543],
  "Uttar Pradesh": [21, 99, 154, 39, 138, 37, 127, 277, 10, 13, 65, 35, 394, 29, 699, 3810, 5947],
  "West Bengal": [944, 509, 611, 161, 3110, 960, 942, 1753, 179, 114, 821, 449, 74, 119, 584, 51, 11381],
  "TOTAL (STATES)": [2031, 4437, 4740, 1788, 5458, 3346, 2163, 11701, 1070, 1259, 1337, 1054, 1495, 269, 12600, 27770, 82518],
 },
 "U.Ts.": {
  "A & N Islands": [1, 14, 6, 1, 6, 6, 0, 11, 0, 0, 2, 0, 0, 0, 59, 4, 110],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 4, 0, 21, 10, 58],
  "D & N Haveli": [0, 1, 9, 0, 0, 9, 0, 7, 0, 0, 1, 0, 0, 0, 0, 12, 39],
  "Daman & Diu": [0, 0, 2, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4, 12, 20],
  "Delhi": [4, 12, 24, 31, 30, 14, 1, 41, 30, 5, 2, 5, 51, 1, 380, 252, 883],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [4, 89, 170, 9, 7, 19, 0, 214, 2, 4, 5, 12, 1, 0, 46, 34, 616],
  "TOTAL (U.TS.)": [9, 116, 211, 41, 44, 48, 1, 296, 32, 10, 10, 17, 56, 1, 510, 324, 1726],
 },
 "Cities": {
  "Ahmedabad": [9, 33, 1, 9, 8, 13, 2, 46, 13, 12, 4, 3, 3, 0, 23, 184, 363],
  "Bangalore": [15, 11, 14, 23, 14, 18, 0, 162, 6, 3, 1, 0, 11, 0, 293, 227, 798],
  "Bhopal": [0, 5, 70, 0, 4, 20, 0, 40, 2, 0, 0, 0, 0, 0, 0, 25, 166],
  "Bombay": [14, 53, 113, 43, 38, 14, 3, 94, 43, 10, 9, 2, 40, 1, 378, 250, 1105],
  "Calcutta": [9, 12, 9, 30, 21, 16, 10, 8, 18, 6, 23, 10, 3, 6, 35, 23, 239],
  "Coimbatore": [1, 2, 6, 4, 7, 0, 0, 79, 5, 0, 0, 0, 0, 0, 99, 0, 203],
  "Delhi": [1, 7, 21, 29, 26, 14, 0, 30, 21, 3, 0, 3, 41, 1, 320, 206, 723],
  "Hyderabad": [3, 27, 7, 14, 13, 4, 3, 37, 4, 5, 0, 5, 26, 0, 77, 315, 540],
  "Indore": [3, 11, 26, 3, 4, 6, 0, 6, 0, 0, 0, 0, 0, 0, 0, 202, 261],
  "Jaipur": [2, 6, 1, 0, 8, 1, 0, 19, 10, 0, 0, 3, 7, 0, 44, 103, 204],
  "Kanpur": [3, 0, 2, 1, 2, 4, 2, 71, 1, 1, 0, 0, 4, 0, 6, 524, 621],
  "Kochi": [3, 1, 0, 0, 0, 14, 0, 9, 3, 4, 0, 0, 0, 0, 0, 184, 218],
  "Lucknow": [1, 2, 0, 3, 5, 4, 3, 8, 2, 0, 0, 1, 14, 0, 67, 50, 160],
  "Ludhiana": [0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 4, 7, 15],
  "Madras": [26, 63, 25, 118, 38, 21, 3, 230, 27, 38, 2, 1, 9, 1, 188, 366, 1156],
  "Madurai": [0, 0, 0, 5, 2, 0, 1, 5, 0, 0, 0, 0, 0, 0, 34, 243, 290],
  "Nagpur": [0, 0, 0, 0, 0, 1, 0, 15, 0, 0, 0, 0, 12, 0, 46, 203, 277],
  "Patna": [0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 20, 1, 30],
  "Pune": [1, 2, 1, 8, 11, 2, 0, 16, 8, 0, 0, 0, 0, 0, 0, 303, 352],
  "Surat": [2, 1, 9, 1, 5, 5, 1, 13, 2, 4, 1, 2, 3, 0, 14, 48, 111],
  "Vadodara": [1, 0, 10, 0, 5, 5, 0, 11, 2, 0, 0, 1, 0, 0, 57, 32, 124],
  "Varanasi": [4, 16, 0, 12, 31, 0, 24, 17, 0, 0, 1, 4, 24, 0, 52, 57, 242],
  "Vishakhapatnam": [10, 0, 12, 24, 13, 9, 0, 48, 11, 0, 1, 1, 1, 0, 9, 36, 175],
 },
 "Grand": {"GRAND TOTAL": [2040, 4553, 4951, 1829, 5502, 3394, 2164, 11997, 1102, 1269, 1347, 1071, 1551, 270, 13110, 28094, 84244]},
}
