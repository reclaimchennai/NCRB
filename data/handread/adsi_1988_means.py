# ADSI 1988, Appendix VI: suicides by means adopted and percentage to total, States / UTs / cities
# (raw/adsi/1988/table_content/1680163818appendix-61988.pdf, pages 1-4, printed sideways: pages 1-2 Railways to
# Drowning (States; UTs, All India total and cities), pages 3-4 Hanging to Total). Only the counts are recorded; the
# printed percentages were used to confirm readings. '-(0.0)' or a bare '(0.0)' is 0. The All-India row is printed
# "TOTAL (ALL INDIA)" and recorded as the GRAND TOTAL. Appendix IV of the same report gives the same table by sex.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1988, "adsi"
SOURCE = "raw/adsi/1988/table_content/1680163818appendix-61988.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Statewise Distribution of the Suicidal Deaths by Means Adopted and Percentage to Total During 1988"
CATS = ["By Railways", "By Machine", "By Firearms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wires", "Other Causes", "Total"]
NA = None
CORRECTIONS = {
    ("Nagpur", "By Touching Electric Wires"): ("(0.6)", 0, "no count printed, only '(0.6)' (the sleeping-pills percentage repeated); with 0 the row adds up to its printed 171 and the cities' column to the printed 22, so the cell is nil"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [277, 1, 10, 8, 1566, 425, 897, 816, 33, 31, 28, 678, 4770],
  "Arunachal Pradesh": [0, 0, 0, 2, 2, 3, 8, 16, 1, 0, 1, 8, 41],
  "Assam": [73, 13, 11, 23, 266, 94, 245, 948, 3, 3, 38, 650, 2367],
  "Bihar": [56, 10, 3, 5, 71, 92, 78, 220, 21, 31, 22, 125, 734],
  "Goa": [0, 0, 1, 1, 11, 17, 24, 63, 9, 0, 1, 20, 147],
  "Gujarat": [105, 0, 3, 3, 668, 542, 359, 382, 39, 4, 13, 109, 2227],
  "Haryana": [32, 8, 3, 7, 296, 132, 74, 120, 18, 11, 30, 178, 909],
  "Himachal Pradesh": [0, 0, 1, 3, 48, 5, 19, 15, 4, 0, 3, 22, 120],
  "Jammu & Kashmir": [4, 0, 1, 0, 2, 9, 7, 5, 1, 0, 0, 6, 35],
  "Karnataka": [140, 105, 29, 7, 2206, 386, 1392, 1604, 22, 55, 14, 801, 6761],
  "Kerala": [258, 1, 6, 8, 2529, 198, 812, 3193, 10, 3, 11, 116, 7145],
  "Madhya Pradesh": [271, 12, 197, 41, 963, 442, 459, 1187, 53, 49, 29, 870, 4573],
  "Maharashtra": [169, 0, 12, 9, 1689, 1167, 1267, 1134, 76, 5, 16, 461, 6005],
  "Manipur": [0, 0, 2, 0, 7, 1, 5, 32, 2, 1, 2, 7, 59],
  "Meghalaya": [0, 0, 0, 0, 3, 2, 9, 24, 0, 0, 0, 0, 38],
  "Mizoram": [0, 0, 3, 0, 3, 0, 0, 16, 0, 0, 0, 3, 25],
  "Nagaland": [0, 0, 1, 0, 0, 2, 0, 3, 0, 0, 0, 0, 6],
  "Orissa": [207, 3, 2, 2, 857, 37, 241, 792, 10, 1, 34, 357, 2543],
  "Punjab": [398, 1, 9, 0, 87, 36, 33, 83, 0, 2, 4, 4, 657],
  "Rajasthan": [167, 4, 27, 7, 180, 153, 299, 310, 75, 13, 6, 210, 1451],
  "Sikkim": [0, 0, 0, 0, 0, 3, 2, 26, 0, 0, 0, 0, 31],
  "Tamil Nadu": [213, 28, 6, 33, 3673, 1024, 1045, 1615, 38, 43, 95, 1907, 9720],
  "Tripura": [1, 0, 1, 0, 174, 35, 0, 177, 0, 0, 0, 129, 517],
  "Uttar Pradesh": [204, 14, 173, 127, 146, 188, 92, 339, 23, 3, 0, 1000, 2309],
  "West Bengal": [212, 15, 21, 32, 4535, 673, 396, 2512, 12, 6, 27, 1427, 9868],
  "TOTAL (STATES)": [2787, 215, 522, 318, 19982, 5666, 7763, 15632, 450, 261, 374, 9088, 63058],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 15, 4, 10, 63, 0, 0, 3, 2, 97],
  "Chandigarh": [0, 1, 0, 0, 11, 11, 7, 8, 0, 0, 3, 6, 47],
  "D & N Haveli": [0, 0, 0, 0, 4, 0, 0, 30, 1, 0, 0, 0, 35],
  "Daman & Diu": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Delhi": [6, 0, 4, 4, 111, 264, 11, 186, 17, 0, 3, 24, 630],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3],
  "Pondicherry": [0, 0, 0, 15, 163, 20, 39, 129, 6, 0, 0, 28, 400],
  "TOTAL (U.TS.)": [6, 1, 4, 19, 304, 299, 67, 419, 24, 0, 9, 60, 1212],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 1, 1, 33, 87, 32, 38, 8, 3, 0, 15, 218],
  "Bangalore": [0, 1, 22, 2, 230, 160, 116, 187, 8, 5, 4, 146, 881],
  "Bombay": [1, 0, 2, 5, 102, 262, 32, 150, 34, 4, 1, 16, 609],
  "Calcutta": [0, 3, 0, 0, 23, 38, 15, 21, 0, 3, 1, 2, 106],
  "Delhi": [6, 0, 4, 4, 77, 238, 6, 137, 12, 0, 3, 18, 505],
  "Hyderabad": [0, 1, 0, 2, 59, 115, 32, 38, 8, 5, 1, 62, 323],
  "Jaipur": [9, 0, 0, 1, 16, 16, 7, 3, 0, 0, 0, 8, 60],
  "Kanpur": [4, 0, 3, 0, 16, 10, 2, 35, 5, 0, 0, 28, 103],
  "Lucknow": [8, 8, 3, 3, 15, 9, 16, 7, 5, 0, 0, 5, 79],
  "Madras": [0, 2, 1, 1, 262, 165, 49, 314, 2, 5, 12, 72, 885],
  "Nagpur": [13, 0, 0, 0, 7, 42, 52, 35, 6, 1, 0, 15, 171],
  "Pune": [0, 0, 1, 1, 52, 56, 28, 37, 4, 0, 0, 48, 227],
  "TOTAL (CITIES)": [41, 15, 37, 20, 892, 1198, 387, 1002, 92, 26, 22, 435, 4167],
 },
 "Grand": {"GRAND TOTAL": [2793, 216, 526, 337, 20286, 5965, 7830, 16051, 474, 261, 383, 9148, 64270]},
}
