# ADSI 1998, Table 26: suicides by means adopted, States / UTs / cities (raw/adsi/1998/archived/table-26_1998.pdf,
# pages 1-9, printed pages 166-174: pages 1-8 each carry two categories by Male / Female / Total / % Share for every
# place, page 9 the Total). Only the Total column of each category is recorded. Read from the page images. No figure is
# N.A. Checks done on the full Male / Female / Total transcription: Male + Female = Total in every cell; the Male,
# Female and Total columns each add to the printed Total (States), Total (UTs) and Total (Cities), and States + UTs =
# Total (All-India); every row's categories add to its printed Total (by sex as well); every printed % share agrees
# with Total / row Total except Total (Cities) "By Consuming Other Poison", printed 14.79% where 1468 / 9888 = 14.85%
# (the counts 885 + 583 = 1468 add up down the column, so the percentage is the slip; nothing changed). The page 8
# city rows are skewed in the scan; each was matched to its place by its % share. No suicide-incidence hand-read file
# exists for 1998 to cross-check against. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1998, "adsi"
SOURCE = "raw/adsi/1998/archived/table-26_1998.pdf"
PAGES = "1-9"
TITLE = "Table 26: Distribution of Suicides By Means adopted (State, UT & City-wise) - 1998"
CATS = ["By Over Alcoholism", "By Drowning", "By Fire/Self Immolation", "By Fire-Arms", "By Hanging",
        "Poison (By Consuming Insecticides)", "By Consuming Other Poison", "By Self Infliction of Injury",
        "By Jumping from (Building)", "By Jumping from (Other Sites)", "By Jumping off Moving Vehicles/Trains",
        "By Machine", "By Overdose of Sleeping pills", "By Touching Electric Wires",
        "By Coming under Running Vehicles/Trains", "By Other Means", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [100, 911, 1071, 315, 1994, 2576, 1628, 61, 19, 53, 3, 20, 47, 60, 194, 381, 9433],
  "Arunachal Pradesh": [0, 0, 3, 0, 44, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 51],
  "Assam": [15, 338, 131, 35, 1258, 144, 423, 5, 13, 10, 31, 1, 28, 34, 57, 298, 2821],
  "Bihar": [53, 157, 182, 34, 402, 185, 268, 28, 35, 24, 1, 4, 48, 18, 19, 337, 1795],
  "Goa": [6, 57, 26, 1, 103, 5, 37, 1, 2, 4, 8, 0, 1, 2, 2, 1, 256],
  "Gujarat": [3, 383, 875, 11, 718, 1017, 1030, 45, 26, 29, 14, 1, 110, 23, 136, 112, 4533],
  "Haryana": [12, 83, 200, 20, 192, 221, 311, 46, 3, 17, 19, 4, 0, 33, 146, 298, 1605],
  "Himachal Pradesh": [4, 18, 0, 11, 42, 53, 79, 0, 0, 8, 0, 0, 0, 4, 0, 25, 244],
  "Jammu & Kashmir": [1, 6, 7, 2, 16, 21, 18, 0, 1, 11, 8, 0, 1, 4, 1, 10, 107],
  "Karnataka": [223, 1703, 1059, 94, 2618, 1201, 3252, 110, 29, 131, 4, 2, 146, 37, 245, 80, 10934],
  "Kerala": [15, 950, 425, 3, 3573, 2264, 1508, 40, 29, 13, 70, 3, 50, 84, 175, 104, 9306],
  "Madhya Pradesh": [145, 663, 1187, 34, 2687, 2789, 1130, 71, 52, 35, 44, 26, 182, 78, 305, 0, 9428],
  "Maharashtra": [73, 1695, 2351, 12, 2897, 3617, 1549, 12, 59, 39, 110, 4, 39, 30, 94, 1077, 13658],
  "Manipur": [0, 0, 0, 4, 17, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 2, 30],
  "Meghalaya": [1, 4, 3, 6, 23, 0, 7, 3, 1, 0, 0, 0, 0, 2, 2, 20, 72],
  "Mizoram": [5, 16, 0, 5, 48, 0, 5, 0, 0, 0, 0, 1, 7, 1, 0, 0, 88],
  "Nagaland": [0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 10],
  "Orissa": [4, 110, 54, 60, 1125, 400, 1028, 4, 1, 48, 8, 0, 2, 8, 23, 609, 3484],
  "Punjab": [3, 43, 46, 12, 113, 96, 125, 1, 4, 5, 0, 0, 17, 13, 262, 69, 809],
  "Rajasthan": [70, 462, 385, 11, 630, 620, 256, 2, 8, 10, 38, 20, 24, 38, 101, 617, 3292],
  "Sikkim": [1, 13, 1, 0, 58, 1, 6, 0, 0, 0, 1, 0, 0, 2, 0, 4, 87],
  "Tamil Nadu": [414, 758, 1284, 18, 1816, 1300, 3505, 85, 59, 77, 77, 19, 165, 61, 286, 1058, 10982],
  "Tripura": [0, 0, 0, 13, 253, 183, 217, 0, 0, 0, 0, 0, 0, 10, 0, 0, 676],
  "Uttar Pradesh": [70, 326, 977, 153, 1257, 859, 301, 32, 58, 13, 122, 12, 31, 143, 198, 418, 4970],
  "West Bengal": [115, 736, 662, 17, 4112, 1222, 3081, 84, 60, 138, 13, 69, 193, 144, 800, 2807, 14253],
  "TOTAL (STATES)": [1333, 9432, 10929, 871, 26002, 18774, 19774, 631, 459, 665, 571, 186, 1095, 829, 3046, 8327, 102924],
 },
 "U.Ts.": {
  "A & N Islands": [0, 4, 7, 0, 100, 16, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 135],
  "Chandigarh": [0, 2, 0, 0, 15, 0, 34, 0, 4, 0, 0, 0, 0, 0, 0, 31, 86],
  "D & N Haveli": [0, 0, 2, 0, 24, 1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 1, 36],
  "Daman & Diu": [0, 2, 5, 0, 6, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 19],
  "Delhi": [8, 27, 206, 8, 408, 150, 130, 4, 17, 0, 0, 0, 6, 7, 3, 8, 982],
  "Lakshadweep": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  "Pondicherry": [0, 8, 73, 0, 263, 133, 49, 1, 0, 0, 0, 0, 2, 0, 1, 0, 530],
  "TOTAL (U.TS.)": [8, 43, 293, 8, 817, 301, 228, 11, 21, 0, 0, 0, 8, 7, 4, 40, 1789],
 },
 "Cities": {
  "Ahmedabad": [0, 8, 81, 0, 76, 56, 119, 2, 2, 1, 0, 0, 7, 10, 4, 0, 366],
  "Bangalore": [87, 101, 422, 4, 321, 115, 383, 82, 25, 36, 4, 2, 63, 10, 5, 0, 1660],
  "Bhopal": [2, 17, 61, 0, 57, 79, 28, 0, 4, 3, 4, 0, 5, 0, 4, 4, 268],
  "Calcutta": [0, 13, 49, 1, 117, 3, 19, 1, 10, 4, 0, 1, 2, 1, 1, 0, 222],
  "Chennai": [29, 38, 138, 0, 364, 24, 132, 0, 17, 0, 0, 0, 9, 4, 0, 315, 1070],
  "Coimbatore": [5, 2, 31, 0, 106, 0, 128, 0, 0, 0, 0, 0, 2, 0, 0, 0, 274],
  "Delhi": [5, 23, 155, 7, 322, 78, 112, 4, 16, 0, 0, 0, 5, 1, 3, 8, 739],
  "Hyderabad": [5, 48, 193, 3, 100, 127, 9, 1, 0, 0, 0, 0, 3, 3, 1, 7, 500],
  "Indore": [26, 44, 97, 2, 48, 79, 26, 15, 10, 4, 0, 8, 5, 33, 0, 2, 399],
  "Jaipur": [0, 5, 19, 2, 57, 69, 20, 0, 3, 0, 2, 0, 1, 4, 1, 23, 206],
  "Kanpur": [7, 20, 214, 47, 7, 122, 0, 0, 29, 0, 0, 3, 0, 40, 0, 136, 625],
  "Kochi": [0, 8, 20, 0, 124, 1, 46, 0, 0, 0, 5, 0, 0, 0, 7, 0, 211],
  "Lucknow": [0, 2, 3, 3, 45, 36, 5, 0, 6, 0, 0, 0, 5, 0, 7, 0, 112],
  "Ludhiana": [0, 0, 0, 0, 10, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 15],
  "Madurai": [0, 0, 17, 0, 67, 0, 84, 0, 0, 0, 0, 0, 4, 0, 0, 8, 180],
  "Mumbai": [11, 40, 485, 2, 444, 207, 85, 5, 53, 26, 4, 0, 2, 2, 0, 0, 1366],
  "Nagpur": [0, 104, 113, 0, 105, 31, 39, 0, 0, 0, 11, 2, 2, 1, 11, 0, 419],
  "Patna": [12, 0, 0, 0, 9, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 13, 43],
  "Pune": [0, 25, 113, 0, 176, 58, 20, 0, 0, 6, 0, 0, 1, 2, 0, 0, 401],
  "Surat": [2, 39, 52, 0, 67, 42, 140, 2, 5, 0, 0, 1, 11, 0, 0, 0, 361],
  "Vadodara": [1, 21, 47, 0, 28, 16, 55, 0, 1, 0, 0, 0, 0, 0, 0, 9, 178],
  "Varanasi": [2, 13, 26, 8, 14, 19, 0, 0, 2, 0, 1, 0, 1, 7, 1, 14, 108],
  "Vishakhapatnam": [2, 21, 15, 18, 68, 29, 7, 0, 2, 0, 0, 3, 0, 0, 0, 0, 165],
  "TOTAL (CITIES)": [196, 592, 2351, 97, 2732, 1191, 1468, 112, 185, 80, 31, 20, 131, 118, 45, 539, 9888],
 },
 "Grand": {
  "GRAND TOTAL": [1341, 9475, 11222, 879, 26819, 19075, 20002, 642, 480, 665, 571, 186, 1103, 836, 3050, 8367, 104713],
 },
}
