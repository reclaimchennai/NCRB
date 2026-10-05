# ADSI 1999, Table 22: distribution of suicides by causes (State, UT & City-wise), pages 1-14 of the archived file
# (printed pages 141-154). Pages 1-13 carry two causes each, printed as Male / Female / Total / % share
# (Total / row total * 100); page 14 carries the Total (Male / Female / Total). Rows: States 1-25, Total States, UTs 26-32,
# Total UTs, Total All-India, Cities 33-55, Total (Cities). Only the Total columns are recorded here. Read from the page
# images (pages are 1240 px wide scans except page 3, 1688 px). Lakshadweep is printed 0 throughout with "-" shares.
# Checked on the full Male / Female / Total transcription: Male + Female = Total in every cell; Male, Female and Total
# each add across the 26 causes to the row's printed Total for every row (totals rows included); every column of Male,
# Female and Total adds to Total States, Total UTs and Total (Cities); Total States + Total UTs = Total All-India
# (1,10,587). Every place's Total equals its Total in the 1999 means table (data/handread/adsi_1999_means.py).
# All hold as read, with no figure changed. One faded cell, confirmed by the sums and the printed % share: Karnataka
# suspected/illicit relation Total 83 (left half of the 8 faint, could be taken for 33; Male 51 + Female 32 = 83, the
# column adds to Total States 1,689 only with 83, and 0.66% = 83/12,488).
# Carry-over: the rows for Bihar (1795), Goa (256), Lucknow (112) and Patna (43) are identical in all 26 causes to the
# 1998 Table 22 rows (data/handread/adsi_1998_causes.py), as they are in the 1999 means table; the 1998 figures were
# apparently repeated where 1999 returns were not received. Kept as printed, but probably not 1999's own figures.
# Cause names as printed (1999, like 1998, prints "Divorcee", "Illness (Other Prolonged)", "Professional/Career Problem").
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1999, "adsi"
SOURCE = "raw/adsi/1999/archived/table-22_1999.pdf"
PAGES = "1-14"
TITLE = "Table 22: Distribution of Suicides By Causes (State, UT & City-wise), 1999"
CATS = ["Bankruptcy or Sudden Change in Economic Status", "Suspected/illicit Relation", "Cancellation/Non-Settlement of Marriage", "Not having Children (Barrenness/Impotency)", "Illness (Aids/STD)", "Illness (Cancer)", "Illness (Paralysis)", "Illness (Insanity)", "Illness (Other Prolonged)", "Death of Dear Person", "Dowry Dispute", "Divorcee", "Drug Abuse/Addiction", "Failure in Examination", "Fall in Social Reputation", "Family Problems", "Ideological Causes/Hero Worshipping", "Illegitimate Pregnancy", "Love Affairs", "Physical Abuse (Rape, Incest Etc.)", "Poverty", "Professional/Career Problem", "Property Dispute", "Unemployment", "Causes Not known", "Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [149, 104, 50, 64, 258, 40, 55, 665, 2579, 36, 327, 40, 33, 174, 81, 1924, 16, 27, 209, 15, 825, 13, 413, 154, 826, 1309, 10386],
  "Arunachal Pradesh": [0, 3, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 1, 17, 0, 0, 2, 0, 1, 0, 0, 0, 43, 0, 74],
  "Assam": [0, 6, 17, 5, 0, 20, 4, 40, 136, 34, 7, 45, 10, 147, 32, 279, 0, 15, 399, 0, 258, 0, 181, 175, 519, 206, 2535],
  "Bihar": [11, 65, 31, 24, 1, 6, 4, 24, 98, 18, 113, 38, 49, 55, 37, 365, 43, 16, 88, 18, 19, 8, 18, 29, 169, 448, 1795],
  "Goa": [2, 1, 1, 0, 0, 0, 1, 36, 22, 3, 2, 0, 0, 3, 3, 43, 3, 1, 20, 0, 1, 6, 1, 13, 77, 17, 256],
  "Gujarat": [122, 93, 65, 72, 18, 37, 42, 499, 685, 58, 82, 60, 19, 101, 73, 1268, 6, 10, 183, 14, 148, 69, 30, 253, 712, 267, 4986],
  "Haryana": [6, 40, 15, 22, 2, 5, 0, 92, 146, 39, 88, 4, 13, 52, 23, 430, 71, 2, 72, 17, 34, 17, 161, 49, 279, 618, 2297],
  "Himachal Pradesh": [0, 2, 3, 5, 0, 0, 0, 15, 16, 1, 0, 1, 2, 7, 1, 68, 0, 0, 13, 0, 7, 0, 6, 5, 99, 75, 326],
  "Jammu & Kashmir": [1, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 0, 34, 0, 0, 3, 0, 0, 0, 0, 7, 26, 13, 98],
  "Karnataka": [219, 83, 89, 87, 23, 58, 93, 843, 2965, 100, 49, 11, 54, 162, 119, 1591, 20, 4, 206, 1, 479, 91, 126, 200, 3905, 910, 12488],
  "Kerala": [1264, 20, 32, 37, 2, 106, 58, 651, 1252, 63, 20, 24, 109, 57, 139, 2265, 1, 10, 148, 6, 9, 180, 51, 307, 1021, 1946, 9778],
  "Madhya Pradesh": [133, 227, 49, 96, 160, 34, 74, 393, 866, 81, 418, 33, 143, 165, 132, 1630, 13, 41, 315, 121, 106, 91, 194, 94, 4093, 0, 9702],
  "Maharashtra": [288, 63, 95, 65, 52, 209, 97, 743, 1711, 87, 356, 27, 326, 245, 69, 2943, 10, 22, 299, 85, 258, 140, 132, 201, 1275, 3796, 13594],
  "Manipur": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 24, 0, 24],
  "Meghalaya": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 0, 0, 2, 0, 3, 0, 0, 0, 46, 0, 56],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 28],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 15],
  "Orissa": [13, 136, 90, 24, 0, 30, 13, 74, 192, 2, 114, 4, 14, 34, 27, 741, 0, 29, 195, 3, 10, 1, 44, 30, 808, 1024, 3652],
  "Punjab": [1, 10, 4, 3, 0, 2, 4, 37, 132, 8, 27, 6, 35, 8, 14, 112, 1, 3, 20, 0, 33, 2, 11, 11, 238, 264, 986],
  "Rajasthan": [44, 79, 24, 13, 0, 2, 5, 167, 303, 13, 88, 13, 146, 52, 13, 942, 1, 10, 128, 17, 82, 28, 47, 79, 649, 798, 3743],
  "Sikkim": [9, 0, 1, 0, 0, 0, 0, 6, 11, 0, 0, 0, 2, 1, 0, 7, 0, 0, 1, 0, 8, 0, 0, 0, 48, 14, 108],
  "Tamil Nadu": [172, 81, 65, 84, 36, 16, 38, 202, 2268, 34, 117, 26, 53, 184, 49, 3277, 0, 8, 392, 21, 356, 65, 95, 231, 1405, 2173, 11448],
  "Tripura": [0, 6, 10, 4, 0, 3, 5, 48, 31, 4, 0, 0, 3, 48, 341, 116, 0, 2, 119, 0, 40, 2, 2, 0, 92, 62, 938],
  "Uttar Pradesh": [47, 105, 63, 108, 33, 14, 2, 171, 402, 31, 443, 14, 122, 84, 46, 1181, 1, 14, 136, 6, 132, 16, 58, 143, 1217, 887, 5476],
  "West Bengal": [89, 561, 131, 134, 2, 131, 181, 529, 571, 106, 272, 60, 83, 658, 30, 2940, 0, 106, 708, 11, 43, 30, 415, 143, 3685, 2270, 13889],
  "TOTAL (STATES)": [2570, 1689, 838, 849, 587, 713, 676, 5235, 14393, 718, 2523, 408, 1223, 2243, 1230, 22177, 186, 320, 3658, 335, 2852, 759, 1985, 2124, 21290, 17097, 108678],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 0, 0, 0, 13, 20, 1, 0, 0, 0, 2, 0, 29, 0, 0, 7, 0, 1, 0, 0, 2, 42, 15, 132],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 70],
  "D & N Haveli": [0, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 1, 7, 0, 0, 3, 1, 0, 1, 0, 1, 3, 8, 32],
  "Daman & Diu": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 10],
  "Delhi": [10, 9, 9, 5, 0, 2, 1, 27, 86, 2, 42, 3, 34, 26, 15, 322, 0, 1, 36, 3, 65, 9, 3, 69, 227, 25, 1031],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [0, 0, 0, 1, 1, 3, 0, 26, 185, 15, 0, 0, 0, 8, 5, 280, 0, 1, 14, 0, 1, 5, 0, 3, 29, 57, 634],
  "TOTAL (U.TS.)": [10, 9, 9, 6, 1, 5, 1, 70, 308, 18, 49, 3, 34, 36, 21, 640, 0, 2, 60, 4, 67, 15, 3, 75, 306, 157, 1909],
 },
 "Cities": {
  "Ahmedabad": [10, 1, 4, 5, 0, 1, 4, 34, 65, 1, 2, 1, 0, 12, 0, 239, 2, 0, 8, 0, 4, 0, 2, 8, 13, 0, 416],
  "Bangalore": [15, 6, 5, 3, 1, 4, 8, 139, 76, 6, 21, 0, 16, 37, 19, 224, 17, 1, 32, 1, 165, 6, 0, 58, 1078, 0, 1938],
  "Bhopal": [0, 16, 5, 0, 20, 2, 0, 1, 10, 0, 11, 0, 4, 5, 0, 74, 0, 0, 21, 0, 1, 0, 0, 6, 91, 0, 267],
  "Calcutta": [3, 0, 0, 2, 0, 1, 0, 15, 15, 1, 20, 0, 4, 8, 0, 35, 0, 1, 8, 0, 36, 2, 0, 17, 42, 0, 210],
  "Chennai": [0, 7, 7, 0, 0, 8, 12, 38, 152, 0, 0, 0, 15, 30, 0, 274, 0, 0, 32, 0, 106, 15, 11, 11, 300, 124, 1142],
  "Coimbatore": [0, 2, 0, 2, 1, 0, 0, 0, 82, 6, 1, 0, 2, 9, 0, 98, 0, 0, 9, 0, 6, 5, 0, 7, 25, 0, 255],
  "Delhi": [10, 9, 9, 4, 0, 2, 0, 18, 68, 2, 36, 3, 28, 21, 13, 242, 0, 1, 36, 3, 31, 8, 2, 59, 206, 24, 835],
  "Hyderabad": [10, 1, 2, 0, 0, 0, 2, 23, 51, 4, 6, 6, 19, 0, 2, 141, 1, 1, 9, 2, 10, 3, 2, 17, 139, 88, 539],
  "Indore": [2, 11, 7, 7, 2, 4, 8, 12, 0, 20, 0, 0, 21, 7, 9, 156, 0, 0, 18, 0, 0, 13, 21, 17, 148, 10, 493],
  "Jaipur": [1, 3, 1, 1, 0, 0, 0, 3, 3, 0, 5, 0, 1, 0, 0, 21, 0, 0, 4, 0, 8, 3, 1, 10, 207, 3, 275],
  "Kanpur": [0, 6, 3, 5, 17, 0, 0, 0, 2, 0, 35, 0, 2, 0, 0, 297, 0, 0, 5, 0, 21, 1, 0, 8, 32, 35, 469],
  "Kochi": [34, 0, 2, 3, 0, 0, 0, 29, 39, 3, 0, 0, 2, 5, 2, 45, 0, 0, 1, 1, 1, 3, 0, 7, 66, 0, 243],
  "Lucknow": [1, 0, 2, 1, 0, 0, 0, 2, 28, 0, 14, 0, 2, 1, 0, 17, 0, 0, 3, 0, 0, 0, 6, 1, 34, 0, 112],
  "Ludhiana": [0, 0, 4, 0, 0, 0, 0, 3, 2, 0, 1, 0, 1, 1, 1, 4, 0, 0, 3, 0, 3, 2, 0, 1, 4, 0, 30],
  "Madurai": [0, 0, 0, 0, 0, 1, 0, 8, 1, 0, 7, 0, 0, 1, 0, 31, 0, 0, 0, 0, 32, 0, 0, 1, 0, 17, 99],
  "Mumbai": [13, 4, 24, 19, 13, 12, 26, 127, 124, 20, 25, 18, 82, 45, 9, 173, 0, 11, 31, 12, 43, 30, 12, 11, 382, 0, 1266],
  "Nagpur": [2, 3, 5, 0, 1, 1, 2, 30, 45, 1, 14, 2, 8, 17, 6, 154, 0, 0, 7, 0, 15, 9, 1, 25, 37, 0, 385],
  "Patna": [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1, 0, 2, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 4, 20, 43],
  "Pune": [16, 0, 6, 2, 8, 2, 0, 36, 65, 8, 0, 1, 33, 11, 1, 115, 0, 0, 9, 0, 8, 12, 1, 25, 46, 18, 423],
  "Surat": [0, 3, 0, 3, 0, 0, 0, 11, 89, 1, 32, 0, 1, 4, 0, 64, 0, 0, 8, 0, 31, 2, 2, 11, 68, 0, 330],
  "Vadodara": [2, 0, 0, 1, 0, 2, 1, 14, 24, 0, 0, 1, 0, 4, 0, 30, 0, 0, 6, 0, 3, 1, 0, 17, 65, 5, 176],
  "Varanasi": [0, 3, 4, 0, 0, 0, 0, 4, 4, 0, 27, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 30, 76],
  "Vishakhapatnam": [7, 1, 0, 0, 0, 0, 1, 36, 1, 7, 17, 0, 0, 5, 1, 11, 0, 0, 6, 1, 11, 0, 1, 5, 20, 10, 141],
  "TOTAL (CITIES)": [126, 76, 90, 58, 63, 40, 64, 583, 948, 81, 274, 33, 242, 225, 63, 2459, 20, 15, 256, 20, 535, 115, 62, 322, 3009, 384, 10163],
 },
 "Grand": {"GRAND TOTAL": [2580, 1698, 847, 855, 588, 718, 677, 5305, 14701, 736, 2572, 411, 1257, 2279, 1251, 22817, 186, 322, 3718, 339, 2919, 774, 1988, 2199, 21596, 17254, 110587]},
}
