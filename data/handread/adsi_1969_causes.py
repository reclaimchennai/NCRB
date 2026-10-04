# ADSI 1969, Appendix V: suicides in States / Union Territories / cities by causes, pages 1-2 (printed sideways).
# Read from the page images; ".." (nil) is 0. This table prints no percentages. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1969, "adsi"
SOURCE = "raw/adsi/1969/table_content/1680151989appendix-51969.pdf"
PAGES = "1-2"
TITLE = "Appendix V: Suicides in States/Union Territories/Cities during 1969 (By Causes)"
CATS = ["Failure in Examination", "Quarrel With parents in law", "Quarrel With Married partner", "Poverty",
        "Frustration", "Love Affairs", "Insanity", "Dispute over property", "Dreadful disease", "Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [27, 216, 250, 123, 49, 62, 21, 110, 1011, 1737, 3606],
  "Assam": [41, 109, 35, 47, 37, 72, 33, 9, 130, 419, 932],
  "Bihar": [152, 152, 59, 7, 5, 3, 27, 12, 34, 1349, 1800],
  "Gujarat": [18, 142, 150, 71, 37, 25, 116, 25, 290, 1243, 2117],
  "Haryana": [54, 49, 42, 22, 23, 13, 5, 4, 110, 480, 802],
  "Jammu & Kashmir": [12, 1, 0, 0, 1, 0, 0, 0, 0, 0, 14],
  "Kerala": [41, 267, 177, 333, 121, 196, 101, 87, 425, 1457, 3205],
  "Madhya Pradesh": [19, 207, 303, 46, 44, 73, 72, 62, 754, 1311, 2891],
  "Maharashtra": [49, 312, 255, 132, 133, 74, 202, 33, 565, 2479, 4234],
  "Mysore": [26, 105, 201, 221, 69, 72, 47, 48, 562, 1837, 3188],
  "Nagaland": [15, 0, 1, 1, 0, 0, 0, 0, 0, 4, 21],
  "Orissa": [24, 212, 298, 3, 1, 134, 14, 206, 285, 1332, 2509],
  "Punjab": [92, 65, 26, 76, 38, 11, 15, 17, 95, 227, 662],
  "Rajasthan": [8, 51, 19, 29, 9, 10, 14, 17, 31, 141, 329],
  "Tamil Nadu": [71, 372, 301, 333, 69, 172, 17, 74, 967, 2591, 4967],
  "Uttar Pradesh": [431, 355, 262, 153, 108, 141, 152, 174, 382, 3541, 5699],
  "West Bengal": [512, 644, 907, 228, 216, 360, 129, 70, 528, 2019, 5613],
  "TOTAL (STATES)": [1592, 3259, 3286, 1825, 960, 1418, 965, 948, 6169, 22167, 42589],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [0, 2, 6, 2, 1, 1, 0, 0, 0, 10, 22],
  "Chandigarh": [0, 4, 0, 0, 2, 0, 1, 0, 3, 1, 11],
  "Dadra & Nagar Haveli": [0, 0, 1, 2, 2, 1, 0, 0, 3, 2, 11],
  "Delhi": [2, 19, 5, 5, 8, 4, 5, 3, 21, 46, 118],
  "Goa, Daman and Diu": [1, 1, 0, 3, 0, 5, 7, 4, 6, 16, 43],
  "Himachal Pradesh": [1, 1, 0, 2, 2, 0, 10, 0, 4, 78, 98],
  "Laccadives": [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4],
  "Manipur": [0, 0, 0, 4, 0, 2, 1, 0, 7, 24, 38],
  "Pondicherry": [12, 17, 34, 10, 33, 6, 0, 0, 57, 108, 277],
  "Tripura": [90, 22, 11, 6, 0, 2, 5, 0, 25, 261, 422],
  "TOTAL (U.TS.)": [106, 66, 57, 34, 48, 21, 29, 7, 126, 550, 1044],
 },
 "Cities": {
  "Ahmedabad": [2, 10, 19, 9, 0, 5, 7, 1, 9, 25, 87],
  "Bangalore": [1, 4, 3, 36, 0, 0, 0, 8, 123, 520, 695],
  "Bombay": [2, 1, 7, 25, 5, 8, 5, 0, 11, 34, 98],
  "Calcutta": [1, 2, 4, 9, 8, 4, 4, 0, 13, 23, 68],
  "Delhi": [1, 17, 3, 4, 6, 4, 5, 3, 16, 40, 99],
  "Hyderabad": [1, 2, 9, 11, 0, 0, 1, 2, 13, 184, 223],
  "Kanpur": [0, 43, 4, 0, 0, 1, 0, 0, 20, 184, 252],
  "Madras": [17, 13, 6, 12, 0, 4, 0, 0, 60, 31, 143],
  "TOTAL (CITIES)": [25, 92, 55, 106, 19, 26, 22, 14, 265, 1041, 1665],
 },
 "Grand": {"GRAND TOTAL": [1698, 3325, 3343, 1859, 1008, 1439, 994, 955, 6295, 22717, 43633]},
}
