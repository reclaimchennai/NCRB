# ADSI 1992, Appendix III: distribution of suicides by causes and sex during 1992, pages 1-6 State & UT-wise and pages
# 7-12 City-wise (upright; three causes per page, each printed as Male / Female / Total; pages 6 and 12 Other causes
# and the Grand Total). Only the Total columns are recorded here; while reading, Male and Female were transcribed too
# and every Male + Female = Total, every Male, Female and Total column adds up to the printed Total (States),
# Total (UTs) and Total (All-India), and every row's sixteen causes add up to its Grand Total in each of the Male,
# Female and Total columns. The All India row is printed "Total (All-India)" (kept here as GRAND TOTAL); the cities
# have no printed totals row. Patna and Varanasi are printed "NR" (Male, Female) and "-" (Total) in every column, so
# they are None. Cause names as in the 1991 file (the printed headings are the same sixteen causes in the same order).
# Read from the page images; no figure changed. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1992, "adsi"
SOURCE = "raw/adsi/1992/archived/appendix-3_1992.pdf"
PAGES = "1-12"
TITLE = "Appendix III: Distribution of Suicides by Causes and Sex during 1992 (State & UT-wise; City-wise)"
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic status", "Death of dear person", "Fall in social reputation",
        "Dowry dispute", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [76, 326, 234, 405, 176, 145, 207, 1855, 49, 73, 25, 23, 173, 2, 655, 2101, 6525],
  "Arunachal Pradesh": [9, 0, 0, 0, 19, 0, 0, 0, 6, 0, 0, 0, 0, 0, 48, 0, 82],
  "Assam": [61, 46, 10, 102, 168, 65, 29, 111, 30, 42, 15, 126, 15, 3, 1483, 661, 2967],
  "Bihar": [21, 51, 39, 34, 28, 33, 31, 67, 15, 14, 18, 6, 50, 9, 516, 304, 1236],
  "Goa": [2, 6, 6, 4, 11, 12, 0, 12, 3, 1, 0, 3, 0, 0, 98, 16, 174],
  "Gujarat": [45, 189, 262, 112, 132, 255, 28, 423, 133, 67, 41, 41, 28, 9, 411, 1366, 3542],
  "Haryana": [18, 14, 51, 32, 19, 20, 18, 92, 17, 2, 5, 11, 2, 1, 167, 229, 698],
  "Himachal Pradesh": [9, 9, 8, 2, 17, 2, 5, 9, 4, 1, 2, 0, 7, 2, 18, 41, 136],
  "Jammu & Kashmir": [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 11, 0, 1, 45, 59],
  "Karnataka": [140, 218, 223, 288, 253, 226, 182, 1282, 96, 101, 46, 12, 101, 8, 646, 4314, 8136],
  "Kerala": [58, 469, 469, 11, 230, 379, 394, 1057, 143, 317, 27, 23, 55, 35, 817, 3619, 8103],
  "Madhya Pradesh": [374, 513, 561, 86, 349, 347, 110, 853, 42, 43, 45, 86, 177, 7, 969, 2668, 7230],
  "Maharashtra": [120, 674, 940, 229, 238, 352, 89, 894, 120, 130, 34, 77, 88, 9, 742, 4322, 9058],
  "Manipur": [0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 19, 11, 34],
  "Meghalaya": [0, 3, 2, 5, 8, 1, 1, 5, 0, 1, 0, 0, 0, 0, 37, 7, 70],
  "Mizoram": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 3],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 16, 18, 35],
  "Orissa": [84, 222, 242, 26, 266, 67, 22, 185, 8, 4, 23, 4, 91, 9, 909, 978, 3140],
  "Punjab": [4, 13, 16, 4, 13, 14, 11, 26, 4, 6, 1, 4, 11, 0, 194, 190, 511],
  "Rajasthan": [50, 192, 159, 33, 61, 141, 59, 169, 19, 14, 27, 28, 36, 0, 457, 806, 2251],
  "Sikkim": [0, 0, 13, 0, 17, 7, 1, 1, 0, 1, 0, 0, 0, 0, 6, 1, 47],
  "Tamil Nadu": [159, 551, 695, 306, 500, 147, 168, 1595, 183, 155, 70, 17, 60, 20, 961, 2394, 7981],
  "Tripura": [23, 56, 28, 0, 48, 40, 0, 21, 0, 0, 2, 1, 0, 0, 61, 142, 422],
  "Uttar Pradesh": [37, 121, 151, 62, 155, 144, 198, 346, 69, 42, 40, 19, 326, 17, 582, 1015, 3324],
  "West Bengal": [263, 659, 776, 332, 863, 382, 129, 521, 163, 67, 97, 62, 149, 49, 3104, 5181, 12797],
  "TOTAL (STATES)": [1553, 4334, 4885, 2073, 3574, 2780, 1683, 9524, 1105, 1081, 518, 543, 1380, 180, 12919, 30429, 78561],
 },
 "U.Ts.": {
  "A & N Islands": [3, 12, 27, 9, 6, 6, 0, 21, 1, 3, 0, 1, 0, 0, 11, 25, 125],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 0, 26, 4, 37],
  "D & N Haveli": [0, 4, 6, 2, 1, 10, 0, 8, 0, 0, 0, 0, 0, 0, 1, 11, 43],
  "Daman & Diu": [0, 0, 3, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 11],
  "Delhi": [17, 2, 16, 13, 14, 9, 3, 31, 13, 4, 0, 4, 54, 0, 312, 295, 787],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [2, 120, 119, 21, 6, 30, 0, 170, 5, 0, 4, 14, 6, 0, 34, 54, 585],
  "TOTAL (U.TS.)": [22, 138, 171, 45, 28, 57, 3, 236, 19, 7, 4, 19, 61, 0, 389, 389, 1588],
 },
 "Cities": {
  "Ahmedabad": [4, 25, 16, 11, 5, 6, 4, 65, 26, 18, 2, 3, 2, 1, 10, 136, 334],
  "Bangalore": [13, 1, 4, 26, 11, 2, 15, 49, 5, 8, 7, 3, 29, 0, 119, 1019, 1311],
  "Bhopal": [14, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 37, 61],
  "Bombay": [13, 45, 92, 9, 23, 13, 9, 90, 27, 9, 4, 3, 31, 1, 292, 525, 1186],
  "Calcutta": [11, 16, 7, 30, 27, 19, 8, 9, 12, 8, 19, 12, 5, 4, 26, 24, 237],
  "Coimbatore": [1, 9, 4, 5, 7, 0, 0, 72, 3, 4, 4, 0, 0, 0, 111, 0, 220],
  "Delhi": [11, 1, 9, 4, 12, 5, 1, 22, 8, 2, 0, 0, 38, 0, 254, 234, 601],
  "Hyderabad": [5, 4, 5, 8, 4, 12, 2, 42, 0, 1, 0, 2, 32, 0, 112, 289, 518],
  "Indore": [6, 43, 55, 8, 11, 11, 5, 36, 0, 4, 2, 1, 0, 0, 0, 90, 272],
  "Jaipur": [5, 6, 1, 2, 0, 0, 0, 12, 2, 0, 0, 3, 3, 0, 66, 75, 175],
  "Kanpur": [2, 0, 3, 0, 5, 9, 2, 81, 0, 2, 0, 0, 4, 0, 0, 593, 701],
  "Kochi": [2, 0, 2, 3, 1, 13, 0, 13, 5, 2, 1, 0, 0, 0, 58, 125, 225],
  "Lucknow": [1, 1, 0, 0, 2, 5, 2, 18, 4, 0, 0, 0, 5, 0, 41, 79, 158],
  "Ludhiana": [0, 0, 0, 0, 2, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 1, 7],
  "Madras": [15, 18, 11, 52, 20, 8, 0, 81, 26, 0, 1, 0, 0, 1, 91, 213, 537],
  "Madurai": [2, 4, 6, 2, 2, 0, 0, 73, 3, 7, 0, 0, 0, 0, 29, 142, 270],
  "Nagpur": [0, 0, 0, 0, 0, 1, 0, 21, 1, 0, 0, 2, 3, 0, 49, 229, 306],
  "Patna": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
  "Pune": [3, 21, 4, 4, 7, 0, 0, 22, 9, 3, 1, 0, 0, 0, 0, 271, 345],
  "Surat": [1, 0, 7, 2, 8, 12, 0, 10, 3, 4, 0, 0, 0, 0, 38, 145, 230],
  "Vadodara": [1, 0, 5, 2, 3, 5, 2, 4, 0, 0, 1, 0, 1, 0, 6, 27, 57],
  "Varanasi": [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
  "Vishakhapatnam": [5, 8, 1, 31, 9, 8, 0, 41, 4, 1, 0, 6, 6, 0, 15, 42, 177],
 },
 "Grand": {"GRAND TOTAL": [1575, 4472, 5056, 2118, 3602, 2837, 1686, 9760, 1124, 1088, 522, 562, 1441, 180, 13308, 30818, 80149]},
}
