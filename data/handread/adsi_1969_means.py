# ADSI 1969, Appendix VI: suicides by means adopted, States / UTs / cities (raw/adsi/1969/table_content/1680151963appendix-61969.pdf,
# pages 1-2, both printed sideways: page 1 the States, page 2 the UTs, Grand Total and cities). Read from the page
# images; '..' (nil) is 0. Uttar Pradesh's last three figures are printed shifted one column left (126, 1,473, 5,699
# under Jumping / Other ways / Total); they are read in their column order. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1969, "adsi"
SOURCE = "raw/adsi/1969/table_content/1680151963appendix-61969.pdf"
PAGES = "1-2"
TITLE = "Appendix VI: Suicides in States/Union Territories/Cities during 1969 (By Means Adopted)"
CATS = ["By Railways", "By Machines", "By Fire-arms", "By Weapons", "By taking poison", "On Road", "By Fire",
        "By Drowning", "By Hanging", "By Jumping", "By Other-ways", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [131, 5, 19, 11, 629, 89, 125, 1471, 495, 57, 574, 3606],
  "Assam": [50, 0, 5, 2, 8, 37, 11, 103, 537, 3, 176, 932],
  "Bihar": [776, 1, 2, 2, 97, 46, 152, 282, 104, 76, 262, 1800],
  "Gujarat": [102, 6, 16, 8, 301, 27, 370, 479, 157, 80, 571, 2117],
  "Haryana": [36, 17, 1, 1, 18, 25, 11, 348, 138, 11, 196, 802],
  "Jammu & Kashmir": [0, 0, 0, 0, 1, 12, 0, 0, 1, 0, 0, 14],
  "Kerala": [81, 1, 5, 7, 1303, 25, 14, 475, 963, 36, 295, 3205],
  "Madhya Pradesh": [284, 3, 17, 61, 167, 86, 267, 679, 698, 68, 561, 2891],
  "Maharashtra": [197, 3, 1, 32, 991, 142, 541, 922, 436, 277, 692, 4234],
  "Mysore": [58, 1, 3, 42, 574, 68, 157, 1097, 466, 200, 522, 3188],
  "Nagaland": [0, 0, 1, 0, 3, 3, 1, 0, 3, 0, 10, 21],
  "Orissa": [294, 4, 2, 0, 626, 107, 39, 388, 518, 18, 513, 2509],
  "Punjab": [304, 5, 9, 3, 36, 50, 23, 69, 46, 21, 96, 662],
  "Rajasthan": [24, 3, 3, 2, 13, 4, 16, 125, 29, 18, 92, 329],
  "Tamil Nadu": [135, 11, 5, 7, 2029, 221, 98, 952, 686, 95, 728, 4967],
  "Uttar Pradesh": [633, 81, 219, 184, 195, 519, 490, 1184, 595, 126, 1473, 5699],
  "West Bengal": [216, 9, 37, 13, 2096, 29, 183, 459, 1657, 15, 899, 5613],
  "TOTAL (STATES)": [3321, 150, 345, 375, 9087, 1490, 2498, 9033, 7529, 1101, 7660, 42589],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [0, 0, 0, 0, 9, 0, 0, 5, 8, 0, 0, 22],
  "Chandigarh": [0, 0, 0, 0, 3, 0, 1, 2, 4, 1, 0, 11],
  "Dadra & Nagar Haveli": [0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 11],
  "Delhi": [35, 0, 2, 1, 15, 0, 18, 22, 13, 6, 6, 118],
  "Goa, Daman & Diu": [1, 0, 3, 0, 4, 1, 7, 15, 8, 3, 1, 43],
  "Himachal Pradesh": [0, 0, 2, 0, 0, 4, 9, 0, 17, 5, 61, 98],
  "Laccadives": [0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 4],
  "Manipur": [0, 0, 3, 0, 5, 4, 0, 9, 5, 0, 12, 38],
  "Pondicherry": [2, 0, 0, 0, 106, 7, 1, 37, 47, 0, 77, 277],
  "Tripura": [5, 1, 1, 1, 60, 6, 4, 162, 108, 0, 74, 422],
  "TOTAL (U.TS.)": [43, 1, 12, 2, 202, 22, 40, 252, 224, 15, 231, 1044],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 2, 0, 32, 0, 34, 9, 8, 0, 2, 87],
  "Bangalore": [1, 1, 1, 0, 110, 52, 82, 74, 16, 0, 358, 695],
  "Bombay": [0, 0, 1, 2, 32, 0, 19, 10, 14, 15, 5, 98],
  "Calcutta": [0, 0, 0, 2, 13, 0, 10, 0, 39, 4, 0, 68],
  "Delhi": [35, 0, 2, 1, 15, 0, 15, 13, 7, 5, 6, 99],
  "Hyderabad": [0, 0, 13, 0, 34, 8, 51, 42, 5, 1, 69, 223],
  "Kanpur": [1, 7, 0, 0, 2, 48, 40, 4, 21, 0, 129, 252],
  "Madras": [0, 0, 0, 0, 93, 0, 0, 21, 20, 0, 9, 143],
  "TOTAL (CITIES)": [37, 8, 19, 5, 331, 108, 251, 173, 130, 25, 578, 1665],
 },
 "Grand": {"GRAND TOTAL": [3364, 151, 357, 377, 9289, 1512, 2538, 9285, 7753, 1116, 7891, 43633]},
}
