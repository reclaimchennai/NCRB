# ADSI 1967, Appendix V: suicides in States / Union Territories / cities by causes, pages 1-2 (one table across two
# facing pages). Read from the page images; ".." and "—" (nil) are 0. The "Percentage to total" row is not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1967, "adsi"
SOURCE = "raw/adsi/1967/table_content/1679915396appendix-51967.pdf"
PAGES = "1-2"
TITLE = "Appendix V: Suicides in States/Union Territories/Cities—1967, By Causes"
CATS = ["Failure in Examination", "Quarrel with Parents/in laws", "Quarrel with married partner", "Poverty",
        "Frustration", "Love Affairs", "Insanity", "Dispute over property", "Dreadful Disease", "Other Causes", "Total"]
# The U.T. total's Grand Total is printed "12,15" (comma misplaced); read as 1215 (= 38,829 - 37,614).
CORRECTIONS = {
    ("GRAND TOTAL", "Frustration"): (1380, 1390, "printed 1,380 (3.58%); 1390/38829 = 3.58% (1380 would be 3.55%), States 1,370 + U.Ts. 20 = 1,390, and the Grand Total row then adds up to 38,829"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [42, 217, 101, 138, 316, 58, 114, 56, 1319, 1004, 3365],
  "Assam": [66, 67, 49, 106, 44, 60, 15, 11, 65, 207, 690],
  "Bihar": [112, 70, 30, 29, 26, 1, 131, 0, 35, 794, 1228],
  "Gujarat": [58, 165, 141, 61, 26, 33, 128, 11, 209, 652, 1484],
  "Haryana": [63, 28, 40, 11, 6, 2, 5, 0, 96, 342, 593],
  "Jammu & Kashmir": [3, 0, 0, 0, 1, 0, 0, 3, 0, 0, 7],
  "Kerala": [40, 276, 87, 292, 163, 161, 155, 35, 258, 280, 1747],
  "Madhya Pradesh": [43, 182, 210, 54, 106, 28, 41, 42, 396, 1092, 2194],
  "Maharashtra": [50, 197, 206, 109, 82, 71, 205, 17, 741, 1439, 3117],
  "Mysore": [28, 89, 129, 293, 134, 151, 47, 45, 589, 1198, 2703],
  "Nagaland": [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2],
  "Orissa": [41, 292, 427, 9, 48, 154, 21, 27, 238, 640, 1897],
  "Punjab": [87, 118, 96, 26, 18, 21, 21, 7, 55, 352, 801],
  "Rajasthan": [5, 72, 29, 9, 4, 8, 27, 9, 69, 535, 767],
  "Tamilnadu": [132, 561, 412, 492, 98, 173, 89, 60, 1101, 2251, 5369],
  "Uttar Pradesh": [190, 375, 242, 92, 88, 137, 182, 102, 529, 3200, 5137],
  "West Bengal": [514, 770, 529, 351, 208, 249, 174, 21, 866, 2831, 6513],
  "TOTAL (STATES)": [1474, 3479, 2728, 2072, 1370, 1307, 1355, 446, 6566, 16817, 37614],
 },
 "U.Ts.": {
  "A. & N. Islands": [1, 0, 9, 1, 3, 2, 0, 0, 4, 10, 30],
  "Chandigarh": [0, 1, 1, 0, 0, 0, 0, 0, 0, 11, 13],
  "Dadra & Nagar Haveli": [0, 0, 1, 0, 0, 0, 2, 3, 0, 19, 25],
  "Delhi": [6, 7, 17, 6, 8, 3, 8, 0, 55, 428, 538],
  "Goa, Daman & Diu": [1, 3, 0, 0, 2, 0, 3, 1, 8, 100, 118],
  "Himachal Pradesh": [15, 4, 2, 5, 2, 1, 0, 4, 14, 46, 93],
  "Laccadives": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Manipur": [0, 0, 0, 1, 2, 0, 0, 0, 0, 3, 6],
  "Pondicherry": [0, 13, 53, 1, 0, 0, 7, 0, 33, 72, 179],
  "Tripura": [7, 4, 1, 5, 3, 6, 2, 0, 6, 179, 213],
  "TOTAL (U.TS.)": [30, 32, 84, 19, 20, 12, 22, 8, 120, 868, 1215],
 },
 "Cities": {
  "Ahmedabad": [0, 5, 27, 8, 0, 2, 3, 0, 18, 24, 87],
  "Bangalore": [1, 1, 58, 38, 52, 9, 0, 0, 60, 0, 219],
  "Bombay": [4, 9, 12, 6, 4, 10, 8, 3, 16, 52, 124],
  "Calcutta": [2, 1, 5, 9, 4, 3, 7, 0, 24, 34, 89],
  "Delhi": [5, 7, 12, 5, 8, 2, 4, 0, 47, 354, 444],
  "Hyderabad": [1, 19, 5, 6, 1, 2, 0, 0, 24, 69, 127],
  "Kanpur": [0, 0, 0, 0, 0, 0, 0, 1, 2, 6, 9],
  "Madras": [4, 5, 9, 7, 0, 6, 0, 0, 45, 26, 102],
  "TOTAL (CITIES)": [17, 47, 128, 79, 69, 34, 22, 4, 236, 565, 1201],
 },
 "Grand": {"GRAND TOTAL": [1504, 3511, 2812, 2091, 1390, 1319, 1377, 454, 6686, 17685, 38829]},
}
