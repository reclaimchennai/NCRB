# ADSI 1967, Appendix VI: suicides by means adopted, States / UTs / cities (raw/adsi/1967/table_content/1679915364appendix-61967.pdf,
# pages 1-2, a two-page spread: page 1 carries Railway to Weapons, page 2 Taking poison to Total). Read from the page
# images; '..' (nil) is 0. The printed "Percentage to total" row is left out. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1967, "adsi"
SOURCE = "raw/adsi/1967/table_content/1679915364appendix-61967.pdf"
PAGES = "1-2"
TITLE = "Appendix VI: Suicides in States/Union Territories/Cities—1967 (By means adopted)"
CATS = ["Railway", "Machine", "Fire-arms", "Weapons", "Taking poison", "On road", "By fire", "By drowning",
        "By hanging", "By jumping", "By other means", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [309, 3, 9, 5, 471, 73, 117, 1441, 446, 156, 335, 3365],
  "Assam": [45, 1, 0, 2, 10, 10, 6, 90, 390, 17, 119, 690],
  "Bihar": [45, 0, 3, 1, 79, 32, 100, 292, 194, 48, 434, 1228],
  "Gujarat": [64, 4, 6, 6, 179, 40, 291, 386, 163, 35, 310, 1484],
  "Haryana": [40, 25, 3, 0, 4, 30, 24, 248, 90, 13, 116, 593],
  "Jammu & Kashmir": [0, 0, 1, 3, 0, 0, 0, 3, 0, 0, 0, 7],
  "Kerala": [69, 0, 1, 7, 463, 22, 25, 238, 750, 59, 113, 1747],
  "Madhya Pradesh": [106, 1, 16, 25, 80, 60, 182, 586, 591, 55, 492, 2194],
  "Maharashtra": [121, 2, 14, 8, 462, 12, 261, 1165, 422, 136, 514, 3117],
  "Mysore": [12, 0, 7, 4, 422, 148, 162, 907, 363, 266, 412, 2703],
  "Nagaland": [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
  "Orissa": [298, 11, 0, 1, 554, 2, 20, 382, 539, 14, 76, 1897],
  "Punjab": [193, 13, 8, 1, 33, 8, 61, 194, 147, 57, 86, 801],
  "Rajasthan": [99, 7, 6, 2, 15, 23, 91, 344, 44, 8, 128, 767],
  "Tamil Nadu": [100, 15, 3, 7, 2018, 170, 162, 1378, 816, 62, 638, 5369],
  "Uttar Pradesh": [886, 78, 162, 92, 116, 304, 470, 1037, 522, 224, 1246, 5137],
  "West Bengal": [508, 52, 152, 19, 1542, 275, 159, 853, 1604, 117, 1232, 6513],
  "TOTAL (STATES)": [2895, 212, 393, 183, 6448, 1209, 2131, 9544, 7081, 1267, 6251, 37614],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [0, 0, 0, 0, 9, 0, 1, 4, 9, 2, 5, 30],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 4, 8, 1, 0, 0, 13],
  "Dadra Nagar Haveli": [0, 0, 0, 0, 0, 2, 1, 6, 6, 0, 10, 25],
  "Delhi": [57, 6, 3, 0, 21, 42, 81, 61, 16, 25, 226, 538],
  "Goa, Daman & Diu": [4, 0, 1, 0, 5, 3, 4, 28, 18, 8, 47, 118],
  "Himachal Pradesh": [0, 0, 0, 1, 1, 2, 1, 7, 23, 5, 53, 93],
  "Laccadives": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Manipur": [0, 0, 1, 0, 2, 0, 0, 1, 2, 0, 0, 6],
  "Pondicherry": [2, 0, 0, 0, 52, 0, 5, 47, 57, 0, 16, 179],
  "Tripura": [0, 0, 1, 0, 23, 0, 4, 97, 66, 0, 22, 213],
  "TOTAL (U.TS.)": [63, 6, 6, 1, 113, 49, 101, 259, 198, 40, 379, 1215],
 },
 "Cities": {
  "Ahmedabad": [0, 1, 0, 0, 15, 0, 50, 8, 4, 4, 5, 87],
  "Bangalore": [0, 0, 2, 0, 137, 0, 3, 43, 34, 0, 0, 219],
  "Bombay": [3, 0, 2, 0, 11, 4, 34, 16, 10, 14, 30, 124],
  "Calcutta": [0, 0, 0, 3, 13, 0, 5, 2, 58, 8, 0, 89],
  "Delhi": [57, 6, 2, 0, 20, 27, 73, 33, 9, 24, 193, 444],
  "Hyderabad": [0, 0, 0, 3, 29, 6, 25, 26, 4, 0, 34, 127],
  "Kanpur": [0, 0, 0, 0, 2, 2, 5, 0, 0, 0, 0, 9],
  "Madras": [0, 0, 0, 0, 49, 0, 3, 31, 19, 0, 0, 102],
  "TOTAL (CITIES)": [60, 7, 6, 6, 276, 39, 198, 159, 138, 50, 262, 1201],
 },
 "Grand": {"GRAND TOTAL": [2958, 218, 399, 184, 6561, 1258, 2232, 9803, 7279, 1307, 6630, 38829]},
}
