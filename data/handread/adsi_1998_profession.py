# ADSI 1998, Table 23: profile of suicide victims by profession, States / UTs / cities
# (raw/adsi/1998/archived/table-23_1998.pdf, pages 1-7, printed pages 151-157: pages 1-6 each carry two professions by
# Male / Female / Total / % share for every place, page 7 the Total). Only the Total column of each profession is
# recorded. Read from the page images. In every profession Male + Female = Total for every row; the professions' Male,
# Female and Total columns each add to page 7's Male, Female and Total; every column adds to the printed Total States,
# Total UTs and Total (Cities), and Total States + Total UTs = Total All-India (entered as GRAND TOTAL). Delhi appears
# as "Delhi (UT)" and "Delhi (City)". Page 7 is printed askew (the figures drift below their names towards the foot of
# the page); its rows were matched in order and confirmed by the row sums of pages 1-6. Checked by
# scripts/check_handread.py.
KIND, YEAR, PUB = "profession", 1998, "adsi"
SOURCE = "raw/adsi/1998/archived/table-23_1998.pdf"
PAGES = "1-7"
TITLE = "Table 23: Profile of Suicide Victims By Profession During 1998 (State, UT & City-wise)"
NA = None
CATS = ["House Wife", "Service (Government)", "Service (Private)", "Public Sector Undertaking", "Student",
        "Unemployed", "Self-Employed (Business activity)", "Self-Employed (Professional Activity)",
        "Self-Employed (Farming/Agriculture)", "Self-Employed (Others)", "Retired Person", "Others", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [2202, 121, 768, 94, 431, 361, 683, 873, 1813, 1506, 24, 557, 9433],
  "Arunachal Pradesh": [9, 5, 9, 0, 10, 18, 0, 0, 0, 0, 0, 0, 51],
  "Assam": [258, 77, 205, 254, 240, 155, 304, 84, 160, 621, 8, 455, 2821],
  "Bihar": [407, 50, 71, 34, 129, 157, 45, 44, 127, 306, 13, 412, 1795],
  "Goa": [51, 5, 56, 1, 16, 75, 4, 0, 5, 31, 0, 12, 256],
  "Gujarat": [1468, 82, 355, 60, 291, 459, 141, 200, 653, 519, 132, 173, 4533],
  "Haryana": [361, 51, 113, 8, 91, 93, 92, 17, 185, 168, 10, 416, 1605],
  "Himachal Pradesh": [50, 13, 25, 1, 9, 23, 9, 1, 26, 22, 0, 65, 244],
  "Jammu & Kashmir": [26, 2, 3, 3, 8, 14, 0, 0, 2, 41, 0, 8, 107],
  "Karnataka": [1956, 334, 1043, 278, 617, 671, 551, 151, 1883, 3045, 37, 368, 10934],
  "Kerala": [1364, 127, 587, 150, 309, 1614, 569, 209, 1514, 1708, 66, 1089, 9306],
  "Madhya Pradesh": [2329, 348, 623, 191, 415, 621, 302, 397, 2278, 1915, 9, 0, 9428],
  "Maharashtra": [3338, 312, 1002, 183, 759, 742, 390, 154, 2409, 1820, 132, 2417, 13658],
  "Manipur": [3, 5, 0, 0, 5, 9, 0, 2, 0, 6, 0, 0, 30],
  "Meghalaya": [5, 8, 1, 0, 15, 16, 5, 0, 6, 8, 1, 7, 72],
  "Mizoram": [4, 8, 0, 0, 6, 70, 0, 0, 0, 0, 0, 0, 88],
  "Nagaland": [0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 3, 10],
  "Orissa": [851, 74, 96, 46, 210, 323, 229, 8, 418, 766, 14, 449, 3484],
  "Punjab": [174, 34, 37, 13, 30, 53, 38, 14, 108, 180, 15, 113, 809],
  "Rajasthan": [752, 91, 298, 80, 167, 175, 157, 57, 705, 256, 11, 543, 3292],
  "Sikkim": [11, 11, 2, 0, 11, 7, 4, 3, 15, 7, 2, 14, 87],
  "Tamil Nadu": [2271, 209, 941, 324, 421, 1856, 486, 310, 1089, 1394, 89, 1592, 10982],
  "Tripura": [78, 6, 17, 18, 71, 3, 68, 63, 241, 102, 9, 0, 676],
  "Uttar Pradesh": [1413, 149, 311, 108, 283, 376, 134, 51, 727, 436, 61, 921, 4970],
  "West Bengal": [2505, 330, 1379, 523, 1015, 506, 840, 339, 1457, 1883, 161, 3315, 14253],
  "TOTAL (STATES)": [21886, 2452, 7942, 2369, 5563, 8397, 5051, 2977, 15821, 16743, 794, 12929, 102924],
 },
 "U.Ts.": {
  "A & N Islands": [35, 24, 28, 0, 16, 4, 10, 0, 11, 1, 2, 4, 135],
  "Chandigarh": [21, 4, 7, 0, 2, 8, 1, 0, 0, 6, 0, 37, 86],
  "D & N Haveli": [9, 0, 5, 0, 0, 0, 0, 0, 18, 3, 0, 1, 36],
  "Daman & Diu": [4, 3, 5, 0, 5, 0, 1, 0, 0, 0, 0, 1, 19],
  "Delhi (UT)": [314, 30, 141, 12, 101, 215, 28, 5, 37, 71, 4, 24, 982],
  "Lakshadweep": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  "Pondicherry": [122, 1, 2, 1, 48, 79, 33, 93, 128, 23, 0, 0, 530],
  "TOTAL (U.TS.)": [505, 63, 188, 13, 172, 306, 73, 98, 194, 104, 6, 67, 1789],
 },
 "Cities": {
  "Ahmedabad": [119, 0, 44, 1, 35, 41, 8, 14, 0, 88, 16, 0, 366],
  "Bangalore": [367, 47, 210, 15, 92, 150, 72, 13, 46, 645, 3, 0, 1660],
  "Bhopal": [35, 12, 38, 59, 14, 35, 19, 0, 56, 0, 0, 0, 268],
  "Calcutta": [64, 13, 32, 9, 23, 33, 13, 0, 0, 30, 5, 0, 222],
  "Chennai": [209, 21, 306, 4, 17, 98, 105, 10, 0, 78, 4, 218, 1070],
  "Coimbatore": [78, 3, 62, 19, 0, 2, 9, 2, 0, 96, 3, 0, 274],
  "Delhi (City)": [236, 22, 101, 12, 76, 165, 23, 5, 10, 61, 4, 24, 739],
  "Hyderabad": [126, 16, 72, 10, 62, 55, 30, 4, 15, 60, 1, 49, 500],
  "Indore": [53, 21, 94, 4, 17, 31, 24, 2, 84, 59, 0, 10, 399],
  "Jaipur": [47, 3, 88, 1, 30, 8, 6, 0, 7, 3, 1, 12, 206],
  "Kanpur": [209, 30, 114, 0, 75, 154, 14, 1, 24, 4, 0, 0, 625],
  "Kochi": [29, 7, 18, 3, 8, 58, 15, 2, 0, 9, 0, 62, 211],
  "Lucknow": [41, 0, 8, 2, 4, 1, 0, 0, 20, 36, 0, 0, 112],
  "Ludhiana": [5, 1, 1, 0, 1, 1, 0, 0, 0, 2, 0, 4, 15],
  "Madurai": [43, 1, 21, 79, 0, 11, 3, 5, 4, 10, 0, 3, 180],
  "Mumbai": [480, 25, 195, 17, 98, 167, 31, 21, 19, 246, 67, 0, 1366],
  "Nagpur": [132, 13, 93, 7, 39, 47, 26, 2, 7, 44, 9, 0, 419],
  "Patna": [8, 0, 2, 0, 2, 14, 0, 0, 0, 0, 0, 17, 43],
  "Pune": [95, 23, 110, 2, 35, 70, 15, 7, 9, 7, 12, 16, 401],
  "Surat": [128, 3, 83, 4, 12, 31, 14, 40, 4, 26, 16, 0, 361],
  "Vadodara": [49, 6, 14, 2, 20, 6, 2, 4, 0, 35, 2, 38, 178],
  "Varanasi": [35, 2, 6, 0, 3, 14, 1, 0, 3, 3, 0, 41, 108],
  "Vishakhapatnam": [16, 11, 16, 0, 4, 8, 9, 4, 6, 50, 1, 40, 165],
  "TOTAL (CITIES)": [2604, 280, 1728, 250, 667, 1200, 439, 136, 314, 1592, 144, 534, 9888],
 },
 "Grand": {
  "GRAND TOTAL": [22391, 2515, 8130, 2382, 5735, 8703, 5124, 3075, 16015, 16847, 800, 12996, 104713],
 },
}
