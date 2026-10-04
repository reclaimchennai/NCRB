# ADSI 1996, Appendix VIII: suicides by means adopted, States / UTs / cities (raw/adsi/1996/archived/appendix-8_1996.pdf,
# pages 1-9, printed pp. 167-175: each page carries two categories by Male / Female / Total / % Share for every place,
# page 9 the Total). Only the Total column of each category is recorded. Read from the page images. No cell is printed
# NA; Lakshadweep is 0 throughout. The cities carry no totals row. Every Male + Female = Total, every Male, Female and
# Total column adds to Total States and Total UTs, States + UTs = Total All-India, every row's categories add to its
# printed Total (Male, Female and Total), and all 630 printed % shares agree with Total / row Total; each place's Total
# agrees with the 1996 suicide counts in the long series. The page prints "By Drowining" and "By Overdose of Sleeping
# Pills"; the 1995 labels are used. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1996, "adsi"
SOURCE = "raw/adsi/1996/archived/appendix-8_1996.pdf"
PAGES = "1-9"
TITLE = "Appendix VIII: Distribution of Suicides By Means adopted (State, UT & City-wise) - 1996"
CATS = ["By Over Alcoholism", "By Drowning", "By Fire/Self Immolation", "By Fire-Arms", "By Hanging",
        "Poison (By Consuming Insecticides)", "By Consuming Other Poison", "By Self Infliction of Injury",
        "By Jumping from (Building)", "By Jumping from (Other Sites)", "By Jumping off Moving Vehicles/Trains",
        "By Machine", "By Overdose of Sleeping pills", "By Touching Electric Wires",
        "By Coming under Running Vehicles/Trains", "By Other Means", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [35, 769, 861, 4, 1287, 1798, 2087, 6, 47, 44, 145, 0, 82, 43, 148, 187, 7543],
  "Arunachal Pradesh": [0, 8, 1, 1, 38, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 51],
  "Assam": [14, 380, 75, 27, 1108, 55, 317, 0, 0, 6, 16, 3, 6, 32, 12, 441, 2492],
  "Bihar": [38, 103, 59, 47, 222, 75, 77, 25, 14, 20, 6, 5, 15, 18, 9, 174, 907],
  "Goa": [7, 95, 81, 0, 130, 31, 67, 0, 6, 6, 4, 0, 0, 7, 18, 97, 549],
  "Gujarat": [15, 388, 964, 24, 659, 982, 718, 4, 31, 24, 16, 9, 40, 12, 167, 129, 4182],
  "Haryana": [5, 70, 87, 3, 212, 236, 300, 0, 5, 27, 5, 1, 4, 23, 15, 161, 1154],
  "Himachal Pradesh": [0, 22, 4, 0, 29, 3, 119, 7, 1, 5, 0, 1, 0, 3, 0, 17, 211],
  "Jammu & Kashmir": [0, 6, 5, 1, 11, 1, 7, 0, 1, 3, 0, 0, 0, 4, 0, 1, 40],
  "Karnataka": [274, 1585, 635, 20, 2045, 2101, 1776, 28, 7, 29, 5, 48, 43, 57, 167, 0, 8820],
  "Kerala": [61, 784, 350, 7, 3259, 1703, 1313, 29, 17, 27, 116, 0, 77, 15, 164, 164, 8086],
  "Madhya Pradesh": [162, 518, 810, 33, 2209, 1615, 777, 36, 33, 27, 19, 17, 43, 212, 259, 0, 6770],
  "Maharashtra": [99, 1463, 2149, 16, 2209, 2498, 1020, 10, 97, 9, 42, 5, 59, 28, 281, 1231, 11216],
  "Manipur": [0, 4, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 18],
  "Meghalaya": [1, 12, 4, 3, 34, 3, 3, 0, 0, 2, 0, 0, 0, 2, 0, 8, 72],
  "Mizoram": [0, 3, 0, 1, 26, 2, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 34],
  "Nagaland": [0, 8, 0, 3, 15, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 34],
  "Orissa": [3, 164, 62, 2, 940, 362, 618, 7, 2, 23, 38, 17, 7, 31, 144, 542, 2962],
  "Punjab": [1, 61, 64, 5, 78, 62, 57, 0, 8, 5, 1, 4, 16, 11, 185, 32, 590],
  "Rajasthan": [55, 547, 350, 8, 533, 398, 212, 1, 14, 14, 24, 11, 20, 15, 133, 284, 2619],
  "Sikkim": [7, 7, 3, 1, 34, 5, 1, 1, 0, 1, 0, 0, 2, 1, 0, 11, 74],
  "Tamil Nadu": [169, 850, 997, 29, 1515, 1239, 1819, 246, 25, 132, 148, 36, 104, 79, 31, 1584, 9003],
  "Tripura": [0, 0, 9, 0, 200, 137, 200, 0, 0, 0, 0, 0, 0, 9, 0, 0, 555],
  "Uttar Pradesh": [47, 341, 761, 111, 1077, 590, 527, 68, 8, 30, 60, 10, 28, 78, 176, 559, 4471],
  "West Bengal": [86, 374, 1285, 50, 4433, 2552, 3465, 36, 41, 95, 264, 51, 101, 94, 204, 951, 14082],
  "TOTAL (STATES)": [1079, 8562, 9616, 396, 22315, 16448, 15487, 504, 357, 530, 909, 218, 648, 774, 2117, 6575, 86535],
 },
 "U.Ts.": {
  "A & N Islands": [0, 4, 11, 0, 98, 0, 35, 0, 0, 0, 0, 0, 0, 0, 0, 1, 149],
  "Chandigarh": [0, 2, 0, 3, 8, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 7, 28],
  "D & N Haveli": [1, 0, 3, 0, 30, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 39],
  "Daman & Diu": [0, 2, 3, 0, 5, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13],
  "Delhi": [13, 19, 222, 12, 400, 73, 145, 6, 20, 21, 1, 0, 10, 5, 2, 9, 958],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [0, 1, 72, 0, 238, 24, 180, 0, 1, 2, 1, 0, 0, 0, 0, 0, 519],
  "TOTAL (U.TS.)": [14, 28, 311, 15, 779, 97, 374, 6, 21, 25, 2, 0, 10, 5, 2, 17, 1706],
 },
 "Cities": {
  "Ahmedabad": [2, 43, 98, 5, 94, 35, 31, 1, 9, 0, 0, 0, 12, 3, 4, 100, 437],
  "Bangalore": [39, 112, 97, 0, 189, 64, 211, 0, 42, 1, 1, 32, 38, 13, 1, 0, 840],
  "Bhopal": [0, 8, 60, 0, 46, 23, 56, 0, 1, 2, 0, 0, 0, 1, 12, 4, 213],
  "Bombay": [20, 28, 410, 4, 305, 180, 74, 0, 47, 0, 0, 0, 13, 3, 2, 0, 1086],
  "Calcutta": [4, 10, 38, 1, 66, 19, 17, 0, 10, 3, 0, 1, 2, 6, 1, 0, 178],
  "Coimbatore": [12, 0, 32, 0, 73, 0, 130, 0, 0, 0, 0, 0, 1, 1, 1, 0, 250],
  "Delhi": [12, 17, 192, 10, 331, 52, 112, 5, 20, 21, 1, 0, 10, 5, 2, 9, 799],
  "Hyderabad": [3, 21, 186, 0, 94, 0, 98, 1, 6, 3, 0, 0, 0, 4, 4, 0, 420],
  "Indore": [10, 28, 39, 1, 36, 47, 38, 3, 0, 2, 2, 1, 2, 6, 3, 19, 237],
  "Jaipur": [0, 34, 34, 0, 14, 23, 0, 0, 10, 0, 0, 0, 0, 0, 23, 29, 167],
  "Kanpur": [7, 13, 93, 6, 91, 76, 35, 19, 5, 7, 3, 3, 0, 4, 30, 96, 488],
  "Kochi": [0, 21, 17, 0, 102, 20, 16, 0, 1, 0, 2, 0, 0, 0, 7, 0, 186],
  "Lucknow": [0, 9, 3, 3, 40, 14, 7, 0, 0, 0, 0, 0, 0, 0, 2, 3, 81],
  "Ludhiana": [0, 0, 2, 1, 3, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 8],
  "Madras": [20, 51, 167, 0, 283, 22, 97, 0, 0, 57, 0, 0, 6, 7, 0, 202, 912],
  "Madurai": [4, 8, 24, 0, 30, 0, 126, 0, 3, 2, 0, 0, 32, 2, 0, 13, 244],
  "Nagpur": [2, 98, 73, 0, 77, 10, 42, 1, 3, 2, 0, 0, 2, 1, 21, 12, 344],
  "Patna": [5, 0, 8, 4, 13, 0, 0, 0, 0, 5, 0, 0, 0, 13, 0, 27, 75],
  "Pune": [4, 28, 135, 0, 150, 38, 29, 2, 14, 0, 0, 0, 4, 0, 3, 0, 407],
  "Surat": [2, 28, 56, 0, 43, 72, 51, 0, 8, 0, 0, 0, 0, 0, 0, 0, 260],
  "Vadodara": [0, 12, 50, 0, 32, 22, 25, 0, 1, 1, 0, 0, 0, 0, 0, 0, 143],
  "Varanasi": [1, 14, 11, 6, 15, 6, 6, 1, 0, 0, 0, 0, 0, 2, 8, 9, 79],
  "Vishakhapatnam": [0, 13, 10, 0, 45, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 113],
 },
 "Grand": {
  "GRAND TOTAL": [1093, 8590, 9927, 411, 23094, 16545, 15861, 510, 378, 555, 911, 218, 658, 779, 2119, 6592, 88241],
 },
}
