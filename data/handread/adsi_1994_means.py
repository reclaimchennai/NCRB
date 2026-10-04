# ADSI 1994, Appendix V: suicides by means adopted and sex, States / UTs / cities
# (raw/adsi/1994/archived/appendix-5_1994.pdf, pages 1-10; printed pages N.C.R.B.-131 to 140). Pages 1-4 carry three
# categories each by Male / Female / Total for every State and UT with Total (States), Total (UTs) and Total
# (All-India); page 5 the Grand Total (Male / Female / Total) for them; pages 6-10 the same for 23 cities, with no
# cities' total row. No % share is printed. Only the Total column of each category is recorded. Read from the page
# images (zoom 3 bands, doubtful cells at zoom 6). Nothing is NA. Checks done on the full Male / Female / Total
# transcription: Male + Female = Total for every category and row; every row's categories add to its Grand Total in
# all three sexes; every column adds to Total (States) and Total (UTs), and States + UTs = Total (All-India); each
# place's Grand Total equals the number of suicides in Table 7 (adsi_1994_suicide_incidence.py) for all 58 rows.
# The one failing check: Ahmedabad's Grand Total Female is printed 183 (clear at zoom 6), but its female figures add
# to 193 and 191 + 193 = 384, the printed Total; only the Total column is recorded here, so nothing is changed.
# Calcutta is printed "Caleutta" on page 6. Category labels as printed (as in the 1992 and 1993
# files). Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1994, "adsi"
SOURCE = "raw/adsi/1994/archived/appendix-5_1994.pdf"
PAGES = "1-10"
TITLE = "Appendix V: Distribution of Suicide by Means Adopted and Sex during 1994 (State & UT-wise / City-wise)"
CATS = ["By Railways", "By Machine", "By Firearm", "By Weapon", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wire", "By Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [341, 7, 24, 5, 3137, 823, 721, 1287, 65, 23, 45, 753, 7231],
  "Arunachal Pradesh": [0, 0, 0, 0, 2, 6, 1, 42, 0, 0, 0, 0, 51],
  "Assam": [66, 12, 12, 13, 335, 130, 203, 1070, 90, 5, 32, 596, 2564],
  "Bihar": [32, 10, 34, 58, 348, 210, 215, 284, 38, 16, 56, 135, 1436],
  "Goa": [4, 0, 0, 2, 44, 24, 40, 106, 14, 1, 0, 2, 237],
  "Gujarat": [175, 19, 6, 6, 1337, 917, 370, 465, 65, 47, 9, 377, 3793],
  "Haryana": [15, 0, 6, 135, 320, 95, 59, 180, 3, 3, 1, 121, 938],
  "Himachal Pradesh": [2, 0, 8, 0, 136, 15, 18, 32, 5, 3, 2, 51, 272],
  "Jammu & Kashmir": [0, 0, 4, 0, 5, 7, 0, 7, 0, 0, 0, 21, 44],
  "Karnataka": [113, 9, 7, 17, 3510, 794, 1399, 1887, 32, 15, 49, 1218, 9050],
  "Kerala": [349, 2, 5, 12, 3298, 318, 871, 3480, 20, 17, 24, 137, 8533],
  "Madhya Pradesh": [300, 9, 15, 93, 1714, 762, 449, 1470, 250, 89, 74, 1799, 7024],
  "Maharashtra": [159, 2, 14, 37, 3736, 1987, 1439, 2155, 114, 17, 31, 1091, 10782],
  "Manipur": [0, 0, 6, 0, 6, 0, 1, 12, 0, 0, 1, 8, 34],
  "Meghalaya": [0, 0, 0, 0, 0, 6, 14, 24, 0, 0, 0, 6, 50],
  "Mizoram": [0, 0, 0, 0, 4, 0, 0, 38, 0, 0, 0, 0, 42],
  "Nagaland": [4, 0, 2, 0, 0, 0, 1, 15, 3, 1, 0, 11, 37],
  "Orissa": [162, 1, 1, 4, 1065, 30, 154, 927, 9, 31, 36, 593, 3013],
  "Punjab": [191, 0, 8, 2, 100, 30, 18, 94, 6, 11, 7, 78, 545],
  "Rajasthan": [167, 8, 24, 4, 629, 313, 423, 451, 48, 36, 29, 559, 2691],
  "Sikkim": [0, 0, 0, 0, 6, 5, 9, 35, 0, 0, 2, 0, 57],
  "Tamil Nadu": [260, 11, 1, 0, 3885, 1336, 751, 1408, 29, 25, 83, 1459, 9248],
  "Tripura": [3, 2, 0, 1, 203, 0, 0, 173, 3, 1, 9, 123, 518],
  "Uttar Pradesh": [575, 37, 369, 298, 1023, 909, 510, 1101, 79, 56, 161, 1820, 6938],
  "West Bengal": [578, 24, 19, 32, 5747, 1244, 714, 3451, 122, 249, 95, 114, 12389],
  "TOTAL (STATES)": [3496, 153, 565, 719, 30590, 9961, 8380, 20194, 995, 646, 746, 11072, 87517],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 27, 7, 4, 82, 0, 0, 0, 2, 122],
  "Chandigarh": [0, 0, 1, 0, 11, 42, 1, 17, 1, 2, 5, 39, 119],
  "D & N Haveli": [0, 0, 0, 0, 11, 4, 2, 20, 0, 0, 0, 0, 37],
  "Daman & Diu": [0, 0, 0, 0, 0, 2, 0, 4, 1, 0, 0, 0, 7],
  "Delhi": [10, 1, 20, 3, 164, 229, 28, 237, 40, 1, 15, 55, 803],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
  "Pondicherry": [0, 0, 0, 0, 215, 54, 3, 311, 2, 3, 0, 1, 589],
  "TOTAL (U.TS.)": [10, 1, 21, 3, 428, 338, 38, 672, 44, 6, 20, 97, 1678],
 },
 "Cities": {
  "Ahmedabad": [6, 0, 0, 2, 68, 101, 65, 64, 6, 19, 0, 53, 384],
  "Bangalore": [0, 0, 0, 0, 278, 255, 71, 342, 3, 3, 11, 153, 1116],
  "Bhopal": [7, 0, 0, 0, 57, 72, 27, 31, 11, 0, 0, 30, 235],
  "Bombay": [1, 0, 7, 16, 363, 530, 52, 298, 45, 13, 9, 0, 1334],
  "Calcutta": [2, 3, 0, 0, 32, 34, 22, 50, 15, 25, 7, 45, 235],
  "Coimbatore": [0, 0, 0, 0, 107, 40, 6, 39, 1, 1, 0, 56, 250],
  "Delhi": [10, 1, 18, 2, 104, 178, 23, 177, 35, 1, 15, 24, 588],
  "Hyderabad": [0, 5, 0, 0, 111, 162, 64, 72, 3, 3, 8, 136, 564],
  "Indore": [2, 0, 0, 0, 136, 66, 14, 51, 1, 0, 0, 0, 270],
  "Jaipur": [17, 0, 2, 0, 55, 41, 7, 29, 0, 1, 2, 94, 248],
  "Kanpur": [48, 4, 12, 26, 106, 146, 33, 70, 22, 0, 3, 193, 663],
  "Kochi": [14, 0, 1, 0, 52, 21, 8, 142, 3, 0, 1, 0, 242],
  "Lucknow": [1, 2, 0, 0, 10, 6, 11, 3, 4, 1, 0, 25, 63],
  "Ludhiana": [0, 0, 0, 0, 6, 2, 0, 2, 0, 0, 1, 1, 12],
  "Madras": [0, 0, 0, 0, 220, 242, 21, 330, 6, 0, 22, 166, 1007],
  "Madurai": [0, 0, 0, 0, 120, 21, 2, 35, 0, 1, 1, 34, 214],
  "Nagpur": [3, 0, 2, 0, 20, 32, 34, 31, 3, 1, 3, 23, 152],
  "Patna": [0, 0, 1, 0, 28, 32, 16, 13, 0, 0, 13, 22, 125],
  "Pune": [4, 0, 2, 0, 79, 101, 23, 132, 5, 0, 0, 7, 353],
  "Surat": [0, 1, 0, 0, 67, 47, 8, 19, 2, 3, 3, 32, 182],
  "Vadodara": [0, 0, 1, 0, 42, 41, 13, 35, 1, 6, 0, 11, 150],
  "Varanasi": [36, 0, 22, 19, 49, 24, 23, 35, 1, 2, 10, 107, 328],
  "Vishakhapatnam": [1, 0, 0, 0, 67, 25, 15, 51, 2, 0, 0, 2, 163],
 },
 "Grand": {
  "GRAND TOTAL": [3506, 154, 586, 722, 31018, 10299, 8418, 20866, 1039, 652, 766, 11169, 89195],
 },
}
