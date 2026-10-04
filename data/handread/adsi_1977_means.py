# ADSI 1977, Appendix VI: suicides by means with percentage to total, States / UTs / cities
# (raw/adsi/1977/table_content/1680159790appendix-61977.pdf, pages 1-4, printed sideways: pages 1-2 Railway to Fire,
# pages 3-4 Drowning to Total). Read from the page images (old-style numerals); '—' (nil) is 0; percentages left out.
# Stray marks before the cities' poison figures (Bangalore '[43', Delhi '[20', Hyderabad '[59') are not digits: the
# printed percentages (14·9% of 289, 9·2% of 218, 40·1% of 147) and the column total 262 fit 43, 20, 59. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1977, "adsi"
SOURCE = "raw/adsi/1977/table_content/1680159790appendix-61977.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of the Suicidal Deaths by Different Means with Percentage to Total Suicidal Deaths in the States/Union Territories/Cities during 1977"
CATS = ["By Railway", "By Machine", "By Firearms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Other causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [319, 8, 6, 6, 793, 214, 1014, 439, 59, 291, 3149],
  "Assam": [126, 9, 12, 70, 122, 39, 374, 594, 5, 404, 1755],
  "Bihar": [128, 1, 1, 13, 77, 45, 161, 79, 29, 118, 652],
  "Gujarat": [104, 2, 10, 11, 346, 238, 310, 106, 38, 101, 1266],
  "Haryana": [42, 3, 2, 0, 11, 39, 156, 122, 7, 95, 477],
  "Himachal Pradesh": [0, 0, 6, 1, 7, 4, 22, 23, 7, 69, 139],
  "Jammu & Kashmir": [0, 0, 0, 0, 0, 1, 3, 0, 1, 7, 12],
  "Karnataka": [0, 90, 6, 1, 975, 195, 1356, 819, 76, 940, 4458],
  "Kerala": [182, 0, 3, 35, 1391, 31, 536, 1183, 17, 319, 3697],
  "Madhya Pradesh": [280, 7, 22, 68, 221, 217, 419, 651, 71, 163, 2119],
  "Maharashtra": [219, 1, 5, 6, 994, 464, 810, 396, 69, 408, 3372],
  "Manipur": [0, 0, 0, 0, 1, 0, 0, 4, 0, 0, 5],
  "Meghalaya": [0, 0, 0, 0, 2, 0, 10, 16, 1, 11, 40],
  "Nagaland": [0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 4],
  "Orissa": [99, 1, 0, 0, 582, 53, 308, 525, 5, 390, 1963],
  "Punjab": [88, 1, 5, 3, 32, 15, 43, 45, 5, 23, 260],
  "Rajasthan": [78, 7, 18, 3, 38, 49, 180, 62, 5, 54, 494],
  "Sikkim": [0, 0, 0, 1, 1, 1, 1, 2, 0, 0, 6],
  "Tamil Nadu": [112, 8, 2, 11, 1526, 228, 864, 593, 33, 764, 4141],
  "Tripura": [2, 0, 1, 0, 219, 0, 11, 129, 0, 21, 383],
  "Uttar Pradesh": [323, 36, 113, 57, 115, 259, 362, 409, 38, 541, 2253],
  "West Bengal": [336, 8, 27, 28, 3806, 431, 446, 1825, 34, 1387, 8328],
  "TOTAL (STATES)": [2438, 182, 239, 314, 11259, 2523, 7387, 8025, 500, 6106, 38973],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 0, 0, 9, 0, 3, 13, 0, 7, 32],
  "Arunachal Pradesh": [0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 5],
  "Chandigarh": [0, 0, 0, 1, 5, 9, 3, 1, 1, 0, 20],
  "D. & N. Haveli": [0, 0, 0, 0, 2, 0, 0, 23, 0, 0, 25],
  "Delhi": [56, 0, 6, 0, 22, 64, 32, 23, 12, 30, 245],
  "Goa, Daman & Diu": [1, 0, 0, 1, 14, 7, 21, 16, 12, 1, 73],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 4, 0, 1, 0, 0, 1, 0, 5, 11],
  "Pondicherry": [0, 0, 0, 0, 171, 0, 47, 66, 0, 50, 334],
  "TOTAL (U.TS.)": [57, 0, 11, 2, 224, 80, 108, 145, 25, 93, 745],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 4, 15, 51, 54, 1, 9, 8, 142],
  "Bangalore": [0, 1, 0, 0, 43, 47, 57, 54, 15, 72, 289],
  "Bombay": [0, 1, 3, 2, 33, 90, 19, 28, 10, 6, 192],
  "Calcutta": [0, 1, 0, 1, 6, 4, 0, 23, 5, 0, 40],
  "Delhi": [56, 0, 4, 0, 20, 53, 24, 22, 9, 30, 218],
  "Hyderabad": [0, 0, 3, 2, 59, 21, 43, 14, 0, 5, 147],
  "Kanpur": [3, 0, 0, 1, 2, 17, 1, 12, 0, 0, 36],
  "Madras": [0, 0, 0, 1, 84, 32, 28, 89, 4, 13, 251],
  "TOTAL (CITIES)": [59, 3, 10, 11, 262, 315, 226, 243, 52, 134, 1315],
 },
 "Grand": {"GRAND TOTAL": [2495, 182, 250, 316, 11483, 2603, 7495, 8170, 525, 6199, 39718]},
}
