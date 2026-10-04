# ADSI 1994, Appendix IV: distribution of suicides by causes and sex (State, UT & City-wise), 12 pages (upright):
# pages 1-6 State & UT-wise, pages 7-12 City-wise (cities 33-55, no printed cities totals row); three causes per page,
# each printed as Male / Female / Total, page 6 and page 12 Other causes and the Grand Total. Only the Total columns
# are recorded here; while reading, every Male, Female and Total figure was transcribed and checked: every Male +
# Female = Total; every row's Male, Female and Total columns add up to its printed Grand Total Male, Female and Total;
# every column (Male, Female, Total) of the States adds up to the printed Total (States), of the UTs to the printed
# Total (UTs), and States + UTs = the printed Total (All - India) (kept here as GRAND TOTAL). Read from the page
# images. City pages 8 and 12 are faintly printed (read with the contrast raised); every city row adds up exactly.
# Tamil Nadu, Dispute over property: Total printed "09" (the leading 1 not printed); Male 85 + Female 24 = 109, the
# row adds up to the printed 9248 and the States' column to the printed 1987 only with 109, and App. VI prints 1.2 %
# (109 / 9248), so it is recorded as 109 (see CORRECTIONS).
# Assam, Causes not known: printed Male 812, Female 42, Total 1234; the female figure should be 422 (812 + 422 = 1234,
# Assam's female columns add up to the printed 850 and the States' female column to the printed 5322 only with 422),
# so the printed Total 1234 is right and is recorded as printed.
# Gujarat, Unemployment: Male printed ".49" (149: 149 + 15 = the printed Total 164); the Total is as printed.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1994, "adsi"
SOURCE = "raw/adsi/1994/archived/appendix-4_1994.pdf"
PAGES = "1-12"
TITLE = "Appendix IV: Distribution of Suicides by Causes and Sex during 1994 (State, UT & City-wise)"
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful disease", "Unemployment",
        "Bankruptcy or sudden change in economic status", "Death of dear person", "Fall in social reputation",
        "Dowry dispute", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
CORRECTIONS = {
    ("Tamil Nadu", "Dispute over property"): (9, 109, "printed Male 85, Female 24, Total 09 (leading 1 not printed); 85 + 24 = 109, the row then adds up to the printed Grand Total 9248 and the States' column to the printed 1987, and App. VI prints 1.2 %"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [93, 255, 247, 321, 132, 138, 170, 2146, 75, 156, 13, 45, 228, 24, 891, 2297, 7231],
  "Arunachal Pradesh": [0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 46, 0, 51],
  "Assam": [45, 37, 17, 43, 79, 41, 22, 77, 18, 4, 5, 23, 11, 17, 1234, 891, 2564],
  "Bihar": [19, 55, 39, 81, 82, 44, 36, 81, 12, 7, 6, 17, 39, 8, 298, 612, 1436],
  "Goa": [3, 5, 12, 4, 19, 33, 0, 17, 5, 4, 2, 0, 0, 0, 99, 34, 237],
  "Gujarat": [51, 238, 245, 82, 143, 256, 25, 476, 164, 79, 60, 48, 35, 10, 574, 1307, 3793],
  "Haryana": [33, 34, 72, 22, 31, 74, 39, 134, 22, 7, 9, 26, 7, 0, 157, 271, 938],
  "Himachal Pradesh": [18, 5, 2, 1, 14, 2, 4, 21, 6, 0, 0, 0, 0, 0, 47, 152, 272],
  "Jammu & Kashmir": [9, 1, 2, 2, 0, 0, 0, 1, 0, 0, 0, 0, 3, 0, 7, 19, 44],
  "Karnataka": [126, 174, 131, 294, 226, 219, 60, 1630, 134, 148, 59, 31, 116, 45, 1345, 4312, 9050],
  "Kerala": [62, 334, 353, 55, 147, 369, 216, 1006, 181, 385, 58, 55, 13, 20, 944, 4335, 8533],
  "Madhya Pradesh": [142, 390, 628, 146, 282, 242, 105, 649, 38, 56, 40, 109, 185, 11, 1598, 2403, 7024],
  "Maharashtra": [154, 911, 1017, 286, 350, 381, 49, 1298, 119, 155, 52, 27, 133, 21, 1177, 4652, 10782],
  "Manipur": [1, 0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 17, 12, 34],
  "Meghalaya": [0, 0, 5, 0, 4, 7, 0, 2, 0, 0, 0, 1, 0, 0, 30, 1, 50],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 42],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 23, 37],
  "Orissa": [71, 167, 243, 24, 287, 58, 17, 205, 20, 2, 2, 26, 113, 5, 760, 1013, 3013],
  "Punjab": [10, 25, 23, 27, 23, 54, 14, 28, 9, 2, 1, 4, 27, 0, 175, 123, 545],
  "Rajasthan": [96, 109, 140, 53, 102, 102, 63, 161, 26, 49, 24, 27, 90, 5, 830, 814, 2691],
  "Sikkim": [0, 0, 0, 11, 3, 7, 0, 4, 2, 0, 2, 0, 0, 2, 18, 8, 57],
  "Tamil Nadu": [249, 700, 648, 282, 382, 75, 109, 1514, 270, 89, 157, 41, 101, 9, 1196, 3426, 9248],
  "Tripura": [35, 61, 53, 0, 56, 27, 0, 22, 0, 0, 0, 0, 0, 2, 54, 208, 518],
  "Uttar Pradesh": [85, 160, 358, 66, 177, 158, 106, 431, 28, 15, 65, 40, 474, 15, 1186, 3574, 6938],
  "West Bengal": [568, 587, 746, 127, 2634, 743, 952, 1856, 168, 395, 834, 727, 79, 191, 1782, 0, 12389],
  "TOTAL (STATES)": [1870, 4248, 4983, 1927, 5177, 3031, 1987, 11761, 1297, 1553, 1389, 1247, 1654, 385, 14479, 30529, 87517],
 },
 "U.Ts.": {
  "A & N Islands": [2, 6, 17, 0, 2, 11, 0, 21, 1, 0, 1, 0, 0, 0, 41, 20, 122],
  "Chandigarh": [1, 5, 7, 2, 3, 3, 1, 12, 4, 0, 0, 0, 1, 0, 34, 46, 119],
  "D & N Haveli": [0, 0, 0, 0, 1, 12, 1, 1, 0, 0, 0, 0, 0, 0, 7, 15, 37],
  "Daman & Diu": [0, 0, 3, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 7],
  "Delhi": [13, 8, 32, 8, 27, 32, 11, 50, 28, 4, 9, 7, 28, 0, 315, 231, 803],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
  "Pondicherry": [9, 88, 172, 16, 6, 27, 0, 178, 2, 3, 6, 5, 4, 0, 33, 40, 589],
  "TOTAL (U.TS.)": [25, 107, 231, 26, 39, 86, 13, 262, 36, 7, 16, 12, 33, 0, 431, 354, 1678],
 },
 "Cities": {
  "Ahmedabad": [6, 28, 3, 4, 5, 15, 3, 47, 22, 8, 8, 1, 1, 0, 155, 78, 384],
  "Bangalore": [10, 7, 6, 27, 17, 1, 3, 83, 18, 5, 7, 0, 29, 0, 125, 778, 1116],
  "Bhopal": [1, 26, 68, 0, 0, 1, 2, 54, 0, 1, 0, 3, 0, 0, 0, 79, 235],
  "Bombay": [16, 67, 108, 56, 45, 28, 2, 141, 39, 11, 4, 6, 31, 8, 608, 164, 1334],
  "Calcutta": [8, 19, 9, 29, 18, 12, 11, 14, 19, 8, 12, 12, 8, 7, 49, 0, 235],
  "Coimbatore": [3, 4, 7, 5, 2, 10, 0, 65, 6, 1, 1, 0, 0, 0, 0, 146, 250],
  "Delhi": [6, 3, 32, 8, 22, 30, 11, 43, 19, 3, 9, 0, 11, 0, 216, 175, 588],
  "Hyderabad": [8, 12, 18, 10, 15, 9, 6, 39, 12, 7, 3, 6, 35, 0, 138, 246, 564],
  "Indore": [3, 6, 4, 7, 1, 2, 0, 9, 0, 0, 2, 0, 16, 0, 0, 220, 270],
  "Jaipur": [9, 4, 5, 0, 7, 1, 0, 5, 0, 0, 0, 3, 13, 0, 73, 128, 248],
  "Kanpur": [4, 0, 4, 3, 5, 7, 4, 90, 3, 2, 0, 0, 6, 0, 14, 521, 663],
  "Kochi": [4, 1, 1, 26, 4, 10, 0, 4, 5, 2, 0, 0, 0, 10, 12, 163, 242],
  "Lucknow": [0, 0, 0, 0, 4, 6, 3, 21, 1, 0, 0, 0, 9, 0, 13, 6, 63],
  "Ludhiana": [0, 3, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 2, 3, 12],
  "Madras": [27, 23, 74, 53, 26, 2, 0, 185, 29, 0, 4, 1, 7, 0, 125, 451, 1007],
  "Madurai": [2, 0, 0, 4, 2, 0, 3, 2, 0, 0, 0, 0, 5, 0, 18, 178, 214],
  "Nagpur": [2, 4, 0, 1, 2, 0, 1, 3, 0, 0, 3, 0, 4, 0, 50, 82, 152],
  "Patna": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 125, 125],
  "Pune": [9, 8, 1, 2, 15, 9, 0, 17, 14, 4, 4, 0, 1, 0, 22, 247, 353],
  "Surat": [1, 8, 14, 6, 3, 3, 0, 16, 8, 2, 1, 0, 2, 0, 0, 118, 182],
  "Vadodara": [6, 3, 19, 1, 6, 5, 0, 7, 7, 0, 0, 1, 2, 0, 46, 47, 150],
  "Varanasi": [0, 8, 3, 3, 2, 4, 3, 2, 0, 0, 0, 0, 7, 0, 78, 218, 328],
  "Vishakhapatnam": [10, 3, 5, 21, 10, 3, 1, 51, 5, 6, 2, 1, 3, 0, 27, 15, 163],
 },
 "Grand": {"GRAND TOTAL": [1895, 4355, 5214, 1953, 5216, 3117, 2000, 12023, 1333, 1560, 1405, 1259, 1687, 385, 14910, 30883, 89195]},
}
