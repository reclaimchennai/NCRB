# ADSI 1995, Appendix VIII: suicides by means adopted, States / UTs / cities (raw/adsi/1995/archived/appendix-8.pdf,
# pages 1-9: each page carries two categories by Male / Female / Total / % Share for every place, page 9 the Total).
# Only the Total column of each category is recorded. Read from the page images. Ahmedabad is printed NA (data not
# available) throughout. The cities carry no totals row. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1995, "adsi"
SOURCE = "raw/adsi/1995/archived/appendix-8.pdf"
PAGES = "1-9"
TITLE = "Appendix VIII: Distribution of Suicides By Means adopted (State, UT & City-wise) - 1995"
CATS = ["By Over Alcoholism", "By Drowning", "By Fire/Self Immolation", "By Fire-Arms", "By Hanging",
        "Poison (By Consuming Insecticides)", "By Consuming Other Poison", "By Self Infliction of Injury",
        "By Jumping from (Building)", "By Jumping from (Other Sites)", "By Jumping off Moving Vehicles/Trains",
        "By Machine", "By Overdose of Sleeping pills", "By Touching Electric Wires",
        "By Coming under Running Vehicles/Trains", "By Other Means", "Total"]
NA = None
CORRECTIONS = {
    # p2 prints Madras Fire-Arms 179 + 90 = 269 (25.72%) and p3 Madras Hanging 0, but Tamil Nadu (State) Fire-Arms is
    # printed 1 for the whole State, which the city cannot exceed; Hanging, the commonest means in every other year for
    # Madras, is 0. The 269 is moved to Hanging (row total 1046 unchanged).
    ("Madras", "By Fire-Arms"): (269, 0, "printed 269 (25.72%) but Tamil Nadu prints 1 for the State; NCRB column slip"),
    ("Madras", "By Hanging"): (0, 269, "printed 0; the 269 printed under Fire-Arms, row total 1046 unchanged"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [109, 813, 816, 6, 1212, 1746, 1392, 16, 31, 36, 157, 5, 43, 69, 173, 143, 6767],
  "Arunachal Pradesh": [0, 0, 1, 0, 53, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 57],
  "Assam": [14, 299, 41, 26, 836, 102, 149, 3, 29, 2, 8, 1, 15, 32, 24, 312, 1893],
  "Bihar": [13, 70, 54, 8, 231, 76, 91, 5, 8, 15, 4, 0, 10, 23, 9, 351, 968],
  "Goa": [0, 67, 34, 2, 107, 4, 24, 1, 0, 0, 0, 0, 3, 1, 0, 3, 246],
  "Gujarat": [18, 342, 816, 32, 577, 1073, 687, 11, 26, 40, 144, 1, 33, 7, 45, 189, 4041],
  "Haryana": [45, 144, 156, 15, 223, 149, 478, 0, 12, 4, 0, 0, 6, 49, 10, 587, 1878],
  "Himachal Pradesh": [1, 15, 9, 2, 30, 56, 65, 25, 0, 5, 7, 2, 0, 0, 5, 21, 243],
  "Jammu & Kashmir": [16, 5, 3, 2, 6, 1, 4, 0, 2, 2, 0, 1, 0, 0, 0, 2, 44],
  "Karnataka": [106, 1968, 536, 65, 2837, 2461, 2946, 41, 51, 76, 1, 3, 36, 42, 107, 0, 11276],
  "Kerala": [4, 768, 429, 6, 3092, 1934, 1180, 18, 4, 12, 109, 8, 32, 35, 272, 109, 8012],
  "Madhya Pradesh": [204, 518, 993, 209, 1996, 2068, 431, 35, 29, 0, 150, 5, 63, 45, 97, 0, 6843],
  "Maharashtra": [156, 1692, 2451, 21, 1967, 1789, 2319, 76, 80, 46, 86, 5, 41, 28, 119, 990, 11866],
  "Manipur": [2, 1, 0, 0, 18, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 24],
  "Meghalaya": [6, 8, 2, 0, 31, 0, 2, 2, 0, 0, 1, 0, 0, 0, 0, 5, 57],
  "Mizoram": [0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31],
  "Nagaland": [0, 2, 0, 0, 10, 0, 2, 0, 0, 0, 7, 0, 1, 0, 0, 0, 22],
  "Orissa": [9, 203, 67, 7, 1108, 300, 722, 16, 2, 16, 41, 2, 0, 51, 217, 309, 3070],
  "Punjab": [2, 29, 66, 21, 82, 59, 71, 11, 2, 13, 10, 0, 29, 8, 166, 54, 623],
  "Rajasthan": [97, 43, 130, 0, 66, 13, 0, 773, 21, 32, 103, 0, 69, 91, 903, 878, 3219],
  "Sikkim": [0, 10, 5, 0, 43, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 61],
  "Tamil Nadu": [70, 687, 1308, 1, 1175, 235, 3389, 7, 7, 111, 0, 5, 93, 52, 0, 1614, 8754],
  "Tripura": [0, 10, 0, 0, 275, 154, 146, 0, 0, 0, 0, 0, 0, 10, 0, 0, 595],
  "Uttar Pradesh": [67, 369, 456, 175, 1009, 409, 550, 19, 0, 61, 75, 11, 29, 73, 257, 454, 4014],
  "West Bengal": [2, 896, 1287, 27, 3999, 33, 5705, 1, 62, 6, 0, 15, 111, 30, 418, 232, 12824],
  "TOTAL (STATES)": [941, 8959, 9660, 625, 21014, 12663, 20358, 1061, 366, 477, 903, 64, 614, 647, 2822, 6254, 87428],
 },
 "U.Ts.": {
  "A & N Islands": [0, 2, 7, 1, 86, 0, 29, 0, 0, 0, 0, 0, 0, 0, 0, 0, 125],
  "Chandigarh": [2, 5, 4, 7, 8, 5, 12, 0, 1, 0, 0, 1, 0, 2, 0, 4, 51],
  "D & N Haveli": [0, 2, 1, 0, 21, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25],
  "Daman & Diu": [0, 0, 0, 1, 3, 0, 5, 0, 1, 0, 0, 0, 0, 0, 0, 2, 12],
  "Delhi UT": [1, 19, 173, 30, 353, 12, 178, 8, 14, 5, 1, 3, 2, 5, 0, 130, 934],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [0, 1, 79, 0, 310, 24, 185, 0, 1, 2, 1, 0, 0, 0, 0, 0, 603],
  "TOTAL (U.TS.)": [3, 29, 264, 39, 781, 42, 409, 8, 17, 7, 2, 4, 2, 7, 0, 136, 1750],
 },
 "Cities": {
  "Ahmedabad": [NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA],
  "Bangalore": [4, 163, 119, 12, 314, 37, 247, 44, 21, 57, 1, 0, 4, 0, 59, 0, 1082],
  "Bhopal": [0, 7, 42, 0, 37, 19, 0, 0, 4, 0, 3, 0, 5, 0, 0, 1, 118],
  "Bombay": [9, 31, 494, 5, 309, 235, 32, 0, 47, 0, 13, 0, 26, 3, 0, 0, 1204],
  "Calcutta": [2, 5, 40, 1, 107, 33, 8, 1, 8, 6, 0, 0, 5, 0, 0, 0, 216],
  "Coimbatore": [23, 12, 28, 0, 38, 0, 83, 1, 1, 0, 0, 0, 4, 1, 0, 1, 192],
  "Delhi": [1, 14, 143, 28, 272, 6, 104, 8, 14, 5, 1, 3, 2, 4, 0, 105, 710],
  "Hyderabad": [9, 12, 140, 0, 91, 7, 74, 15, 5, 3, 0, 0, 5, 5, 5, 0, 371],
  "Indore": [0, 30, 110, 1, 38, 114, 0, 0, 0, 3, 0, 1, 1, 2, 7, 97, 404],
  "Jaipur": [0, 32, 58, 0, 27, 24, 5, 0, 9, 0, 4, 1, 4, 4, 4, 56, 228],
  "Kanpur": [4, 21, 18, 9, 52, 29, 40, 0, 7, 0, 0, 3, 2, 7, 4, 92, 288],
  "Kochi": [0, 14, 23, 0, 135, 25, 7, 0, 3, 0, 0, 0, 0, 1, 10, 0, 218],
  "Lucknow": [0, 2, 14, 0, 49, 5, 4, 0, 0, 0, 0, 0, 0, 1, 1, 37, 113],
  "Ludhiana": [0, 0, 28, 1, 5, 0, 4, 0, 0, 0, 0, 0, 11, 0, 0, 0, 49],
  "Madras": [0, 41, 250, 0, 269, 124, 121, 0, 0, 9, 0, 0, 7, 6, 0, 219, 1046],
  "Madurai": [5, 2, 26, 0, 27, 0, 52, 0, 1, 0, 0, 1, 2, 4, 0, 8, 128],
  "Nagpur": [0, 116, 214, 1, 71, 5, 40, 0, 0, 13, 0, 0, 0, 6, 0, 29, 495],
  "Patna": [0, 5, 5, 0, 18, 5, 2, 2, 5, 0, 0, 0, 5, 0, 0, 1, 48],
  "Pune": [7, 32, 125, 2, 115, 12, 67, 0, 3, 2, 0, 0, 1, 0, 3, 0, 369],
  "Surat": [0, 16, 33, 0, 45, 114, 7, 0, 5, 2, 0, 0, 0, 0, 0, 0, 222],
  "Vadodara": [0, 3, 47, 0, 27, 0, 0, 53, 0, 2, 0, 0, 2, 0, 0, 1, 135],
  "Varanasi": [8, 20, 18, 3, 54, 72, 27, 0, 0, 0, 7, 0, 5, 4, 0, 10, 228],
  "Vishakhapatnam": [0, 20, 23, 0, 42, 4, 42, 0, 0, 0, 0, 1, 0, 0, 0, 9, 141],
 },
 "Grand": {
  "GRAND TOTAL": [944, 8988, 9924, 664, 21795, 12705, 20767, 1069, 383, 484, 905, 68, 616, 654, 2822, 6390, 89178],
 },
}
