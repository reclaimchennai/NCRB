# ADSI 1992, Appendix IV: suicides by means adopted and sex, States / UTs / cities
# (raw/adsi/1992/archived/appendix-4_1992.pdf, pages 1-10; printed pages 94-103). Pages 1-4 (State & UT-wise) and 6-9
# (City-wise) each carry three categories by Male / Female / Total for every place; page 5 the State/UT Grand Total and
# page 10 the City Grand Total, by Male / Female / Total. No percentage share is printed. Only the Total column of each
# category is recorded. Read from the page images. Patna and Varanasi are "NR" (data not received) throughout: rows kept
# with None, so they are left out of the data (their Total cells print "-", except Patna's Electric Wire Total, printed
# "NR", and Varanasi's Other Causes Total, printed "0" beside NR, NR). The cities carry no totals row.
# Checks (Male, Female and Total all transcribed): Male + Female = Total in every cell; every Male, Female and Total
# column adds to the printed Total (States) and Total (UTs), and States + UTs = Total (All-India); every row's twelve
# categories add to its printed Grand Total for Male, Female and Total alike (cities too). Every place's Grand Total
# agrees with Table 7 (adsi_1992_suicide_incidence.py). No figure needed correcting.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1992, "adsi"
SOURCE = "raw/adsi/1992/archived/appendix-4_1992.pdf"
PAGES = "1-10"
TITLE = "Appendix IV: Distribution of Suicide by Means Adopted and Sex during 1992 (State & UT-wise / City-wise)"
CATS = ["By Railways", "By Machine", "By Firearm", "By Weapon", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wire", "By Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [323, 11, 9, 30, 2614, 795, 943, 1055, 46, 57, 102, 540, 6525],
  "Arunachal Pradesh": [0, 0, 0, 0, 4, 4, 13, 60, 1, 0, 0, 0, 82],
  "Assam": [89, 3, 13, 11, 293, 105, 294, 1280, 33, 20, 55, 771, 2967],
  "Bihar": [51, 16, 34, 30, 200, 188, 229, 246, 31, 16, 31, 164, 1236],
  "Goa": [1, 0, 0, 0, 21, 26, 45, 69, 7, 1, 0, 4, 174],
  "Gujarat": [248, 4, 20, 9, 1247, 726, 316, 443, 38, 26, 25, 440, 3542],
  "Haryana": [14, 0, 0, 5, 383, 64, 49, 39, 10, 5, 1, 128, 698],
  "Himachal Pradesh": [4, 2, 3, 0, 70, 9, 8, 15, 13, 1, 1, 10, 136],
  "Jammu & Kashmir": [17, 0, 1, 1, 4, 10, 3, 2, 3, 0, 0, 18, 59],
  "Karnataka": [153, 2, 11, 28, 2866, 564, 1417, 1714, 66, 20, 47, 1248, 8136],
  "Kerala": [330, 0, 3, 17, 3190, 213, 573, 3504, 39, 30, 8, 196, 8103],
  "Madhya Pradesh": [383, 15, 61, 95, 2053, 814, 612, 1854, 56, 122, 48, 1117, 7230],
  "Maharashtra": [229, 17, 10, 23, 3883, 758, 163, 2397, 130, 18, 13, 1417, 9058],
  "Manipur": [0, 0, 2, 0, 0, 0, 0, 17, 0, 0, 0, 15, 34],
  "Meghalaya": [0, 0, 4, 1, 1, 5, 7, 45, 0, 0, 0, 7, 70],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3],
  "Nagaland": [1, 0, 2, 0, 1, 2, 0, 13, 2, 0, 1, 13, 35],
  "Orissa": [210, 1, 3, 0, 1101, 83, 958, 176, 12, 13, 64, 519, 3140],
  "Punjab": [176, 0, 8, 2, 79, 22, 15, 53, 0, 5, 1, 150, 511],
  "Rajasthan": [133, 8, 13, 25, 347, 218, 404, 340, 88, 8, 19, 648, 2251],
  "Sikkim": [0, 0, 1, 1, 2, 4, 0, 36, 3, 0, 0, 0, 47],
  "Tamil Nadu": [99, 10, 13, 5, 3321, 947, 784, 1199, 9, 95, 51, 1448, 7981],
  "Tripura": [0, 0, 2, 0, 145, 4, 0, 174, 1, 0, 0, 96, 422],
  "Uttar Pradesh": [409, 47, 297, 100, 465, 371, 193, 357, 18, 6, 6, 1055, 3324],
  "West Bengal": [950, 33, 36, 57, 5401, 926, 408, 2899, 93, 81, 74, 1839, 12797],
  "TOTAL (STATES)": [3820, 169, 546, 440, 27691, 6858, 7434, 17990, 699, 524, 547, 11843, 78561],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 14, 4, 8, 99, 0, 0, 0, 0, 125],
  "Chandigarh": [0, 0, 2, 0, 16, 7, 2, 10, 0, 0, 0, 0, 37],
  "D & N Haveli": [0, 0, 0, 0, 4, 0, 3, 36, 0, 0, 0, 0, 43],
  "Daman & Diu": [0, 0, 0, 0, 1, 4, 2, 4, 0, 0, 0, 0, 11],
  "Delhi": [2, 0, 13, 14, 149, 189, 8, 223, 21, 4, 1, 163, 787],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [1, 0, 0, 0, 211, 44, 2, 322, 1, 1, 1, 2, 585],
  "TOTAL (U.TS.)": [3, 0, 15, 14, 395, 248, 25, 694, 22, 5, 2, 165, 1588],
 },
 "Cities": {
  "Ahmedabad": [0, 1, 1, 5, 77, 71, 64, 51, 3, 20, 0, 41, 334],
  "Bangalore": [0, 1, 0, 21, 288, 214, 108, 251, 4, 5, 26, 393, 1311],
  "Bhopal": [0, 0, 0, 0, 24, 0, 0, 23, 0, 0, 0, 14, 61],
  "Bombay": [0, 0, 4, 2, 240, 429, 39, 215, 59, 17, 0, 181, 1186],
  "Calcutta": [0, 12, 0, 0, 36, 13, 19, 22, 15, 34, 13, 73, 237],
  "Coimbatore": [0, 0, 0, 0, 118, 20, 14, 66, 0, 1, 1, 0, 220],
  "Delhi": [1, 0, 12, 14, 119, 124, 0, 155, 19, 4, 1, 152, 601],
  "Hyderabad": [1, 4, 0, 0, 83, 173, 101, 55, 6, 8, 11, 76, 518],
  "Indore": [4, 0, 0, 0, 139, 56, 20, 24, 1, 0, 0, 28, 272],
  "Jaipur": [11, 0, 1, 1, 42, 42, 3, 23, 1, 3, 1, 47, 175],
  "Kanpur": [43, 2, 11, 21, 107, 156, 29, 83, 40, 0, 0, 209, 701],
  "Kochi": [12, 0, 0, 0, 56, 22, 9, 118, 4, 0, 0, 4, 225],
  "Lucknow": [5, 0, 15, 0, 18, 1, 46, 1, 0, 4, 7, 61, 158],
  "Ludhiana": [0, 0, 0, 2, 1, 0, 0, 4, 0, 0, 0, 0, 7],
  "Madras": [0, 1, 2, 0, 133, 97, 42, 161, 3, 1, 6, 91, 537],
  "Madurai": [0, 0, 0, 0, 77, 64, 1, 22, 0, 1, 5, 100, 270],
  "Nagpur": [10, 3, 2, 1, 42, 61, 49, 53, 10, 0, 3, 72, 306],
  "Patna": [None, None, None, None, None, None, None, None, None, None, None, None, None],
  "Pune": [4, 0, 1, 2, 88, 94, 41, 93, 7, 0, 0, 15, 345],
  "Surat": [0, 1, 1, 0, 64, 73, 7, 22, 0, 0, 10, 52, 230],
  "Vadodara": [0, 0, 0, 0, 15, 10, 7, 19, 1, 1, 1, 3, 57],
  "Varanasi": [None, None, None, None, None, None, None, None, None, None, None, None, None],
  "Vishakhapatnam": [1, 0, 1, 1, 75, 11, 42, 34, 2, 3, 0, 7, 177],
 },
 "Grand": {
  "GRAND TOTAL": [3823, 169, 561, 454, 28086, 7106, 7459, 18684, 721, 529, 549, 12008, 80149],
 },
}
