# ADSI 1985, Appendix VI: suicides by means adopted and percentage to total, States / UTs / cities
# (raw/adsi/1985/table_content/1680163181appendix-61985.pdf, pages 1-6, printed sideways: pages 1-3 Railways to
# Drowning (States 1-18; States 19-22, UTs and Grand Total; cities), pages 4-6 Hanging to Total). Only the counts are
# recorded; the printed percentages were used to confirm readings. '—(0.0)' is 0. The cities carry a totals row.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1985, "adsi"
SOURCE = "raw/adsi/1985/table_content/1680163181appendix-61985.pdf"
PAGES = "1-6"
TITLE = "Appendix VI: Statewise Distribution of the Suicidal Deaths by Means Adopted and Percentage to Total Deaths of Respective States During 1985"
CATS = ["By railways", "By machine", "By fire arms", "By weapons", "By poison", "By fire", "By drowning", "By hanging",
        "By jumping", "By taking sleeping pills", "By touching electric wire", "Other causes", "Total"]
NA = None
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [334, 5, 7, 7, 1263, 340, 854, 801, 9, 0, 0, 401, 4021],
  "Assam": [55, 12, 5, 9, 125, 131, 230, 834, 87, 3, 27, 327, 1845],
  "Bihar": [59, 12, 15, 21, 107, 80, 131, 141, 19, 28, 6, 169, 788],
  "Gujarat": [122, 0, 12, 5, 599, 482, 342, 239, 24, 4, 6, 64, 1899],
  "Haryana": [18, 2, 4, 0, 239, 145, 178, 218, 8, 4, 12, 32, 860],
  "Himachal Pradesh": [1, 0, 1, 2, 19, 2, 6, 19, 15, 0, 1, 24, 90],
  "Jammu & Kashmir": [6, 0, 3, 1, 7, 6, 4, 5, 0, 0, 0, 0, 32],
  "Karnataka": [107, 11, 16, 5, 1533, 171, 1266, 1084, 13, 10, 21, 539, 4776],
  "Kerala": [283, 2, 7, 11, 2229, 122, 618, 2450, 5, 4, 0, 344, 6075],
  "Madhya Pradesh": [298, 18, 76, 112, 591, 562, 539, 724, 68, 14, 4, 442, 3448],
  "Maharashtra": [149, 1, 19, 12, 1343, 900, 798, 744, 296, 15, 17, 464, 4758],
  "Manipur": [0, 0, 1, 0, 8, 0, 0, 18, 0, 0, 0, 0, 27],
  "Meghalaya": [0, 0, 0, 1, 1, 3, 6, 22, 1, 0, 0, 2, 36],
  "Nagaland": [0, 0, 0, 0, 0, 0, 6, 7, 0, 0, 0, 4, 17],
  "Orissa": [222, 0, 3, 0, 588, 44, 206, 758, 36, 2, 33, 450, 2342],
  "Punjab": [103, 1, 4, 0, 37, 44, 44, 63, 9, 5, 9, 31, 350],
  "Rajasthan": [114, 3, 17, 2, 87, 124, 290, 164, 32, 8, 5, 67, 913],
  "Sikkim": [0, 0, 1, 0, 2, 1, 1, 17, 3, 0, 0, 0, 25],
  "Tamil Nadu": [440, 6, 9, 31, 2934, 835, 957, 1096, 18, 24, 57, 1391, 7798],
  "Tripura": [0, 2, 13, 2, 141, 3, 45, 146, 0, 0, 0, 109, 461],
  "Uttar Pradesh": [503, 73, 232, 68, 94, 168, 79, 113, 26, 3, 1, 1330, 2690],
  "West Bengal": [247, 7, 23, 12, 3945, 544, 418, 2513, 65, 21, 31, 685, 8511],
  "TOTAL (STATES)": [3061, 155, 468, 301, 15892, 4707, 7018, 12176, 734, 145, 230, 6875, 51762],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 16, 3, 9, 34, 0, 0, 0, 3, 65],
  "Arunachal Pradesh": [0, 0, 3, 1, 3, 7, 2, 21, 3, 0, 0, 1, 41],
  "Chandigarh": [0, 0, 1, 0, 4, 10, 5, 6, 0, 0, 0, 0, 26],
  "D & N Haveli": [0, 0, 0, 0, 0, 1, 1, 11, 0, 0, 0, 0, 13],
  "Delhi": [25, 0, 2, 3, 78, 188, 11, 103, 20, 0, 2, 10, 442],
  "Goa, Daman & Diu": [0, 0, 0, 0, 16, 13, 35, 41, 3, 0, 3, 0, 111],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 1, 0, 2, 0, 0, 14, 0, 0, 0, 0, 17],
  "Pondicherry": [3, 0, 0, 0, 123, 15, 13, 177, 0, 3, 0, 0, 334],
  "TOTAL (U.TS.)": [28, 0, 7, 4, 242, 237, 76, 407, 26, 3, 5, 14, 1049],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 2, 0, 20, 63, 45, 21, 9, 0, 0, 11, 171],
  "Bangalore": [0, 0, 6, 0, 101, 69, 100, 112, 3, 0, 0, 70, 461],
  "Bombay": [0, 0, 3, 3, 54, 208, 18, 85, 27, 7, 4, 14, 423],
  "Calcutta": [0, 0, 0, 0, 16, 49, 5, 50, 2, 4, 0, 2, 128],
  "Delhi": [25, 0, 2, 3, 72, 179, 9, 89, 20, 0, 2, 9, 410],
  "Hyderabad": [0, 1, 0, 1, 24, 47, 20, 23, 2, 3, 11, 52, 184],
  "Jaipur": [8, 0, 2, 0, 8, 11, 8, 8, 0, 0, 0, 0, 45],
  "Kanpur": [12, 2, 5, 2, 15, 79, 7, 30, 11, 0, 0, 92, 255],
  "Lucknow": [3, 0, 4, 7, 12, 5, 3, 14, 2, 0, 0, 22, 72],
  "Madras": [0, 0, 0, 0, 166, 128, 89, 165, 6, 5, 15, 144, 718],
  "Nagpur": [8, 0, 0, 2, 32, 36, 38, 16, 4, 5, 6, 47, 194],
  "Pune": [2, 0, 10, 1, 30, 53, 15, 45, 6, 0, 0, 3, 165],
  "TOTAL (CITIES)": [58, 3, 34, 19, 550, 927, 357, 658, 92, 24, 38, 466, 3226],
 },
 "Grand": {"GRAND TOTAL": [3089, 155, 475, 305, 16134, 4944, 7094, 12583, 760, 148, 235, 6889, 52811]},
}
