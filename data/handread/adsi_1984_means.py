# ADSI 1984, Appendix VI: suicides by means adopted, States / UTs / cities, pages 1-6 (pages 2-6 printed sideways).
# Read from the page images; N.A. (not available) is None. Checked by scripts/check_handread.py (N.A. counts as 0).
KIND, YEAR, PUB = "means", 1984, "adsi"
SOURCE = "raw/adsi/1984/table_content/1680162408appendix-61984.pdf"
PAGES = "1-6"
TITLE = "Appendix VI: Statewise Distribution of the Suicidal Deaths by Means Adopted, 1984"
CATS = ["By Railways", "By Machine", "By Fire Arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By taking sleeping pills", "By touching electric wires", "other causes", "Total"]
NA = None
CORRECTIONS = {
    ("TOTAL (STATES)", "By Weapons"): (235, 255, "the States add up to 255; Grand Total 263 = 255 + 8 for the UTs; the States total row then adds up to 49567"),
    ("TOTAL (STATES)", "By Fire Arms"): (3851, 385, "printed '3851 (0.8)' with a stray digit; 385/49567 = 0.8% and the States add up to 385"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [236, 3, 2, 5, 896, 309, 1029, 695, 77, NA, NA, 406, 3658],
  "Assam": [63, 1, 3, 8, 102, 60, 203, 744, 8, 10, 11, 373, 1586],
  "Bihar": [50, 17, 14, 0, 113, 73, 98, 123, 9, NA, NA, 118, 615],
  "Gujarat": [149, 0, 3, 5, 604, 407, 378, 272, 6, 3, 6, 60, 1893],
  "Haryana": [26, 11, 1, 3, 105, 105, 107, 142, 10, 2, 4, 14, 530],
  "Himachal Pradesh": [0, 1, 1, 1, 19, 0, 3, 18, 7, 3, 0, 24, 77],
  "Jammu & Kashmir": [7, 0, 1, 1, 4, 9, 3, 5, 0, 0, 0, 4, 34],
  "Karnataka": [153, 20, 23, 4, 1393, 313, 1279, 977, 66, 34, 48, 552, 4862],
  "Kerala": [258, 0, 4, 8, 2186, 86, 639, 2153, 20, 0, 8, 255, 5617],
  "Madhya Pradesh": [321, 5, 59, 12, 411, 382, 501, 770, 38, NA, NA, 588, 3087],
  "Maharashtra": [158, 8, 5, 8, 1071, 735, 933, 666, 138, 17, 2, 380, 4121],
  "Manipur": [0, 0, 1, 1, 3, 1, 12, 21, 0, 0, 1, 24, 64],
  "Meghalaya": [0, 0, 1, 0, 2, 2, 8, 22, 0, 0, 0, 0, 35],
  "Nagaland": [0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 31, 36],
  "Orissa": [200, 1, 0, 1, 496, 57, 122, 688, 5, 0, 4, 179, 1753],
  "Punjab": [47, 1, 7, 0, 27, 60, 42, 48, 2, 0, 0, 19, 253],
  "Rajasthan": [89, 5, 10, 35, 74, 128, 253, 140, 17, 8, 13, 113, 885],
  "Sikkim": [0, 0, 1, 0, 2, 1, 3, 6, 5, 0, 0, 0, 18],
  "Tamil Nadu": [349, 0, 7, 36, 3071, 753, 1007, 1234, 34, 23, 33, 924, 7471],
  "Tripura": [0, 0, 3, 0, 196, 0, 13, 188, 0, 0, 0, 39, 439],
  "Uttar Pradesh": [296, 79, 222, 61, 151, 377, 323, 241, 60, 16, 5, 790, 2621],
  "West Bengal": [311, 13, 17, 66, 4743, 676, 486, 2565, 53, 5, 5, 972, 9912],
  "TOTAL (STATES)": [2713, 165, 385, 255, 15669, 4534, 7444, 11721, 555, 121, 140, 5865, 49567],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 14, 3, 8, 44, 1, 0, 0, 10, 80],
  "Arunachal Pradesh": [0, 0, 0, 1, 1, 5, 0, 15, 1, 0, 0, 2, 25],
  "Chandigarh": [0, 0, 0, 0, 4, 2, 9, 1, 0, 0, 0, 1, 17],
  "Dadra & Nagar Haveli": [0, 0, 0, 0, 0, 0, 5, 21, 0, 0, 0, 2, 28],
  "Delhi": [31, 1, 5, 1, 76, 189, 16, 88, 14, NA, 3, 9, 433],
  "Goa, Daman & Diu": [2, 0, 0, 6, 11, 10, 52, 28, 4, 0, 0, 8, 121],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
  "Mizoram": [0, 0, 1, 0, 1, 0, 0, 10, 0, 0, 0, 0, 12],
  "Pondicherry": [0, 0, 0, 0, 115, 16, 10, 146, 0, 0, 0, 0, 287],
  "TOTAL (U.TS.)": [33, 1, 6, 8, 222, 225, 100, 354, 20, 0, 3, 32, 1004],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 0, 12, 88, 57, 18, 4, 0, 0, 32, 211],
  "Bangalore": [1, 0, 1, 1, 120, 141, 163, 97, 16, 5, 23, 186, 754],
  "Bombay": [2, 1, 0, 2, 66, 172, 33, 81, 25, 9, 0, 12, 403],
  "Calcutta": [0, 0, 1, 0, 3, 4, 1, 25, 4, 0, 0, 0, 38],
  "Delhi": [31, 1, 5, 0, 63, 174, 10, 77, 13, NA, 1, 9, 384],
  "Hyderabad": [0, 0, 0, 1, 27, 42, 79, 32, 1, NA, NA, 81, 263],
  "Jaipur": [2, 0, 0, 0, 13, 9, 9, 12, 0, 1, 0, 0, 46],
  "Kanpur": [12, 0, 0, 3, 12, 4, 7, 12, 0, 0, 0, 0, 50],
  "Lucknow": [15, 1, 8, 0, 12, 26, 42, 31, 5, 3, 0, 61, 204],
  "Madras": [1, 0, 0, 1, 147, 95, 47, 223, 4, 8, 9, 131, 666],
  "Nagpur": [17, 6, 0, 0, 27, 60, 55, 2, 2, 0, 2, 68, 239],
  "Pune": [1, 0, 2, 0, 18, 52, 27, 23, 10, 0, 0, 19, 152],
  "TOTAL (CITIES)": [82, 9, 17, 8, 520, 867, 530, 633, 84, 26, 35, 599, 3410],
 },
 "Grand": {"GRAND TOTAL": [2746, 166, 391, 263, 15891, 4759, 7544, 12075, 575, 121, 143, 5897, 50571]},
}
