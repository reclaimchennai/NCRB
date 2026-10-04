# ADSI 1986, Appendix VI: suicides by means adopted with percentage to total, States / UTs / cities
# (raw/adsi/1986/table_content/1680163506appendix-61986.pdf, pages 1-4, printed sideways: pages 1-2 Railways to
# Drowning (States; UTs, Grand Total and cities), pages 3-4 Hanging to Total). Only the counts are recorded; the
# printed percentages were used to confirm readings. '-(0.0)' is 0. Arunachal Pradesh and Mizoram are listed among
# the States from this year. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1986, "adsi"
SOURCE = "raw/adsi/1986/table_content/1680163506appendix-61986.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of Suicidal Deaths by Means Adopted with Percentage to Total, States/U.Ts./Cities, 1986"
CATS = ["By Railways", "By Machine", "By Firearms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wires", "Other Causes", "Total"]
NA = None
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [303, 2, 40, 64, 983, 423, 647, 726, 37, 26, 25, 716, 3992],
  "Arunachal Pradesh": [0, 1, 0, 1, 5, 4, 3, 18, 9, 0, 0, 8, 49],
  "Assam": [75, 9, 22, 12, 207, 156, 520, 895, 9, 23, 15, 438, 2381],
  "Bihar": [75, 2, 8, 2, 59, 58, 52, 52, 7, 11, 27, 21, 374],
  "Gujarat": [170, 3, 6, 5, 682, 530, 335, 330, 31, 3, 8, 77, 2180],
  "Haryana": [142, 0, 2, 0, 163, 112, 186, 130, 15, 2, 8, 124, 884],
  "Himachal Pradesh": [1, 0, 0, 0, 36, 8, 23, 24, 3, 1, 0, 2, 98],
  "Jammu & Kashmir": [2, 0, 0, 0, 19, 28, 7, 0, 0, 1, 1, 0, 58],
  "Karnataka": [77, 23, 18, 4, 1627, 284, 1042, 990, 99, 19, 20, 409, 4612],
  "Kerala": [255, 0, 15, 24, 2236, 172, 649, 2565, 7, 8, 3, 201, 6135],
  "Madhya Pradesh": [292, 15, 116, 37, 760, 409, 510, 720, 284, 41, 16, 278, 3478],
  "Maharashtra": [138, 6, 15, 8, 1381, 1052, 994, 847, 93, 23, 10, 682, 5249],
  "Manipur": [0, 0, 2, 0, 4, 1, 3, 12, 1, 0, 0, 0, 23],
  "Meghalaya": [0, 0, 0, 0, 1, 2, 8, 24, 0, 1, 0, 0, 36],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 27, 1, 0, 0, 0, 28],
  "Nagaland": [1, 0, 2, 0, 1, 1, 4, 7, 0, 0, 0, 5, 21],
  "Orissa": [462, 2, 5, 6, 830, 28, 218, 949, 4, 1, 22, 301, 2828],
  "Punjab": [146, 0, 5, 3, 40, 29, 44, 57, 5, 10, 2, 20, 361],
  "Rajasthan": [105, 3, 13, 2, 170, 161, 331, 215, 54, 4, 6, 109, 1173],
  "Sikkim": [0, 0, 0, 0, 5, 5, 2, 29, 0, 0, 0, 0, 41],
  "Tamil Nadu": [241, 12, 11, 9, 3062, 926, 983, 1163, 65, 59, 59, 1642, 8232],
  "Tripura": [0, 3, 0, 0, 184, 20, 6, 170, 0, 0, 0, 47, 430],
  "Uttar Pradesh": [259, 35, 131, 144, 112, 188, 137, 384, 15, 7, 5, 941, 2358],
  "West Bengal": [227, 9, 13, 25, 3682, 619, 331, 2320, 52, 27, 35, 767, 8107],
  "TOTAL (STATES)": [2971, 125, 424, 346, 16249, 5216, 7035, 12654, 791, 267, 262, 6788, 53128],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 21, 1, 1, 48, 1, 0, 0, 1, 73],
  "Chandigarh": [0, 0, 1, 0, 2, 8, 2, 2, 0, 0, 3, 11, 29],
  "D & N Haveli": [0, 0, 0, 0, 4, 0, 1, 27, 0, 0, 1, 2, 35],
  "Delhi": [17, 0, 5, 1, 112, 250, 20, 162, 13, 0, 6, 52, 638],
  "Goa, Daman & Diu": [0, 0, 1, 0, 20, 11, 33, 37, 7, 0, 0, 9, 118],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [1, 0, 0, 0, 130, 20, 8, 156, 0, 3, 0, 18, 336],
  "TOTAL (U.TS.)": [18, 0, 7, 1, 289, 290, 65, 432, 21, 3, 10, 93, 1229],
 },
 "Cities": {
  "Ahmedabad": [0, 1, 1, 0, 20, 91, 58, 19, 7, 0, 0, 4, 201],
  "Bangalore": [1, 1, 3, 0, 170, 103, 78, 155, 0, 12, 7, 60, 590],
  "Bombay": [0, 0, 3, 3, 61, 207, 33, 115, 42, 8, 2, 7, 481],
  "Calcutta": [0, 0, 1, 0, 12, 32, 4, 49, 13, 7, 0, 8, 126],
  "Delhi": [16, 0, 5, 1, 76, 213, 10, 139, 12, 0, 1, 46, 519],
  "Hyderabad": [0, 0, 3, 1, 32, 102, 34, 30, 5, 2, 4, 71, 284],
  "Jaipur": [4, 0, 0, 0, 23, 24, 20, 18, 0, 0, 1, 0, 90],
  "Kanpur": [14, 4, 2, 2, 5, 40, 8, 42, 3, 0, 0, 0, 120],
  "Lucknow": [0, 0, 7, 4, 5, 17, 3, 19, 8, 0, 3, 52, 118],
  "Madras": [0, 1, 0, 2, 188, 145, 65, 262, 1, 12, 3, 146, 825],
  "Nagpur": [8, 0, 0, 0, 30, 32, 37, 16, 22, 12, 0, 35, 192],
  "Pune": [1, 0, 8, 1, 33, 51, 3, 35, 3, 0, 0, 15, 150],
  "TOTAL (CITIES)": [44, 7, 33, 14, 655, 1057, 353, 899, 116, 53, 21, 444, 3696],
 },
 "Grand": {"GRAND TOTAL": [2989, 125, 431, 347, 16538, 5506, 7100, 13086, 812, 270, 272, 6881, 54357]},
}
