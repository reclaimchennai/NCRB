# ADSI 1998, Table 25: educational status of suicide victims, States / UTs / cities
# (raw/adsi/1998/archived/table-25.pdf, pages 1-5, printed pages 161-165: pages 1-4 each carry two levels of education
# by Male / Female / Total / % share for every place, page 5 the Total). Only the Total column of each level is
# recorded. Read from the page images. In every level Male + Female = Total for every row; the levels' Male, Female
# and Total columns each add to page 5's Male, Female and Total; every column adds to the printed Total States, Total
# UTs and Total (Cities), and Total States + Total UTs = Total All India (entered as GRAND TOTAL). Page 5's figures are
# the same, row for row, as the Total page of Table 23 (profession). Delhi appears as "Delhi (UT)" and "Delhi (City)".
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "education", 1998, "adsi"
SOURCE = "raw/adsi/1998/archived/table-25.pdf"
PAGES = "1-5"
TITLE = "Table 25: Educational Status of Suicide Victims during 1998 (State, UT & City-wise)"
NA = None
CATS = ["No Education", "Primary", "Middle", "Matriculate/Secondary", "Hr. Secondary/Intermediate/Pre-University",
        "Diploma", "Graduate", "Post Graduate and Above", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [3878, 2450, 1809, 769, 338, 33, 128, 28, 9433],
  "Arunachal Pradesh": [11, 11, 19, 7, 2, 1, 0, 0, 51],
  "Assam": [568, 719, 786, 510, 203, 16, 19, 0, 2821],
  "Bihar": [649, 404, 292, 246, 115, 15, 65, 9, 1795],
  "Goa": [52, 71, 58, 49, 18, 2, 5, 1, 256],
  "Gujarat": [1039, 1867, 702, 715, 162, 12, 34, 2, 4533],
  "Haryana": [623, 323, 264, 289, 91, 3, 11, 1, 1605],
  "Himachal Pradesh": [32, 44, 63, 66, 36, 0, 1, 2, 244],
  "Jammu & Kashmir": [33, 11, 13, 23, 10, 6, 7, 4, 107],
  "Karnataka": [3226, 2633, 2273, 1598, 875, 94, 191, 44, 10934],
  "Kerala": [625, 2372, 3188, 1974, 897, 66, 139, 45, 9306],
  "Madhya Pradesh": [2650, 2637, 1686, 1350, 685, 96, 205, 119, 9428],
  "Maharashtra": [3034, 3835, 3184, 2434, 896, 157, 94, 24, 13658],
  "Manipur": [1, 1, 14, 11, 3, 0, 0, 0, 30],
  "Meghalaya": [30, 16, 19, 4, 2, 1, 0, 0, 72],
  "Mizoram": [11, 36, 35, 6, 0, 0, 0, 0, 88],
  "Nagaland": [4, 4, 2, 0, 0, 0, 0, 0, 10],
  "Orissa": [1111, 716, 873, 497, 191, 10, 78, 8, 3484],
  "Punjab": [241, 145, 127, 147, 69, 3, 12, 65, 809],
  "Rajasthan": [995, 790, 514, 697, 249, 7, 31, 9, 3292],
  "Sikkim": [33, 27, 20, 6, 1, 0, 0, 0, 87],
  "Tamil Nadu": [3248, 2616, 2708, 1109, 757, 219, 210, 115, 10982],
  "Tripura": [159, 155, 157, 128, 64, 4, 9, 0, 676],
  "Uttar Pradesh": [1514, 908, 921, 763, 489, 129, 176, 70, 4970],
  "West Bengal": [3226, 4709, 3086, 1793, 872, 185, 326, 56, 14253],
  "TOTAL (STATES)": [26993, 27500, 22813, 15191, 7025, 1059, 1741, 602, 102924],
 },
 "U.Ts.": {
  "A & N Islands": [27, 46, 36, 23, 3, 0, 0, 0, 135],
  "Chandigarh": [15, 8, 15, 41, 5, 0, 2, 0, 86],
  "D & N Haveli": [17, 11, 5, 2, 1, 0, 0, 0, 36],
  "Daman & Diu": [2, 4, 4, 8, 0, 0, 1, 0, 19],
  "Delhi (UT)": [235, 216, 251, 197, 63, 1, 19, 0, 982],
  "Lakshadweep": [0, 1, 0, 0, 0, 0, 0, 0, 1],
  "Pondicherry": [49, 233, 131, 18, 96, 1, 2, 0, 530],
  "TOTAL (U.TS.)": [345, 519, 442, 289, 168, 2, 24, 0, 1789],
 },
 "Cities": {
  "Ahmedabad": [33, 113, 117, 66, 23, 0, 14, 0, 366],
  "Bangalore": [384, 361, 388, 319, 153, 8, 41, 6, 1660],
  "Bhopal": [42, 18, 28, 99, 63, 1, 9, 8, 268],
  "Calcutta": [21, 49, 66, 31, 27, 0, 28, 0, 222],
  "Chennai": [287, 98, 410, 80, 161, 3, 22, 9, 1070],
  "Coimbatore": [48, 76, 86, 38, 14, 3, 7, 2, 274],
  "Delhi (City)": [182, 160, 189, 135, 54, 1, 18, 0, 739],
  "Hyderabad": [145, 82, 100, 84, 58, 5, 24, 2, 500],
  "Indore": [72, 53, 84, 89, 61, 10, 24, 6, 399],
  "Jaipur": [44, 57, 37, 48, 11, 1, 8, 0, 206],
  "Kanpur": [190, 110, 49, 169, 83, 8, 14, 2, 625],
  "Kochi": [0, 50, 84, 52, 12, 2, 9, 2, 211],
  "Lucknow": [20, 13, 32, 32, 12, 0, 3, 0, 112],
  "Ludhiana": [5, 0, 3, 4, 2, 0, 1, 0, 15],
  "Madurai": [112, 12, 20, 20, 14, 1, 1, 0, 180],
  "Mumbai": [180, 331, 359, 320, 138, 14, 24, 0, 1366],
  "Nagpur": [56, 89, 85, 135, 38, 4, 6, 6, 419],
  "Patna": [15, 7, 6, 7, 1, 0, 6, 1, 43],
  "Pune": [50, 99, 129, 94, 25, 4, 0, 0, 401],
  "Surat": [62, 165, 60, 65, 7, 2, 0, 0, 361],
  "Vadodara": [13, 89, 34, 29, 11, 1, 1, 0, 178],
  "Varanasi": [29, 41, 11, 16, 10, 1, 0, 0, 108],
  "Vishakhapatnam": [47, 39, 23, 27, 15, 0, 12, 2, 165],
  "TOTAL (CITIES)": [2037, 2112, 2400, 1959, 993, 69, 272, 46, 9888],
 },
 "Grand": {
  "GRAND TOTAL": [27338, 28019, 23255, 15480, 7193, 1061, 1765, 602, 104713],
 },
}
