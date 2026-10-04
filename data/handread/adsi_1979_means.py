# ADSI 1979, Appendix VI: suicides by means with percentage to total, States / UTs / cities
# (raw/adsi/1979/table_content/1680160310appendix-61979.pdf, pages 1-4, printed sideways: pages 1-2 Railways to Fire,
# pages 3-4 Drowning to Total). Read from the page images; '—' (nil) is 0, as is a bare '(0·0)' with no figure;
# Lakshadweep is printed '—' throughout with no percentages and is kept as 0; percentages left out. Checked by
# scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1979, "adsi"
SOURCE = "raw/adsi/1979/table_content/1680160310appendix-61979.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of the suicidal deaths by different means with percentage to total suicidal deaths in the States/U.Ts./Cities during 1979"
CATS = ["By Railways", "By Machine", "By Fire-Arms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Other Causes", "Total"]
CORRECTIONS = {
    ("Bombay", "By Jumping"): (4, 0, "printed 4 (0·0%); 0·0% means nil, and both the row (201) and the Cities' Jumping column (36) then add up"),
    ("Calcutta", "By Fire"): (8, 4, "printed 8 (8·7%), likely repeated from the poison figure beside it; 4/46 = 8·7%, and both the row (46) and the Cities' Fire column (258) then add up"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [315, 5, 14, 25, 690, 180, 1199, 504, 30, 365, 3327],
  "Assam": [127, 3, 26, 1, 58, 59, 441, 771, 8, 317, 1811],
  "Bihar": [13, 1, 7, 5, 74, 40, 53, 113, 1, 39, 346],
  "Gujarat": [140, 1, 1, 2, 358, 277, 396, 162, 13, 138, 1488],
  "Haryana": [32, 5, 6, 0, 12, 45, 123, 133, 42, 52, 450],
  "Himachal Pradesh": [1, 0, 1, 0, 8, 1, 2, 31, 7, 9, 60],
  "Jammu & Kashmir": [0, 0, 0, 3, 9, 1, 3, 5, 1, 1, 23],
  "Karnataka": [0, 123, 9, 30, 766, 321, 1631, 657, 105, 1334, 4976],
  "Kerala": [221, 0, 5, 35, 1257, 28, 620, 1231, 10, 224, 3631],
  "Madhya Pradesh": [147, 1, 12, 16, 119, 157, 197, 444, 28, 222, 1343],
  "Maharashtra": [144, 0, 2, 10, 713, 294, 880, 499, 107, 457, 3106],
  "Manipur": [0, 0, 0, 0, 4, 1, 0, 8, 0, 0, 13],
  "Meghalaya": [0, 0, 1, 1, 0, 0, 1, 19, 0, 5, 27],
  "Nagaland": [0, 0, 2, 0, 0, 1, 0, 3, 0, 0, 6],
  "Orissa": [189, 21, 1, 7, 457, 9, 298, 593, 3, 404, 1982],
  "Punjab": [69, 0, 12, 1, 25, 35, 67, 89, 4, 25, 327],
  "Rajasthan": [72, 5, 13, 4, 46, 63, 253, 93, 4, 62, 615],
  "Sikkim": [0, 0, 0, 0, 3, 0, 1, 11, 2, 0, 17],
  "Tamil Nadu": [242, 25, 7, 18, 1570, 314, 915, 523, 55, 806, 4475],
  "Tripura": [4, 0, 0, 0, 150, 2, 53, 148, 2, 28, 387],
  "Uttar Pradesh": [608, 72, 231, 128, 216, 441, 423, 534, 90, 789, 3532],
  "West Bengal": [232, 19, 7, 15, 1959, 222, 364, 1614, 18, 1153, 5603],
  "TOTAL (STATES)": [2556, 281, 357, 301, 8494, 2491, 7920, 8185, 530, 6430, 37545],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 0, 0, 15, 1, 5, 17, 0, 6, 44],
  "Arunachal Pradesh": [0, 0, 0, 0, 0, 0, 2, 4, 0, 0, 6],
  "Chandigarh": [0, 0, 1, 0, 1, 5, 1, 5, 0, 0, 13],
  "D. & N. Haveli": [0, 0, 0, 0, 0, 0, 1, 19, 1, 0, 21],
  "Delhi": [32, 3, 8, 3, 25, 55, 35, 43, 12, 117, 333],
  "Goa, Daman & Diu": [5, 0, 0, 1, 12, 6, 26, 20, 3, 5, 78],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 0, 0, 0, 0, 0, 2, 9, 0, 0, 11],
  "Pondicherry": [0, 0, 0, 0, 55, 4, 12, 88, 0, 7, 166],
  "TOTAL (U.TS.)": [37, 3, 9, 4, 108, 71, 84, 205, 16, 135, 672],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 0, 0, 8, 58, 46, 7, 3, 67, 189],
  "Bangalore": [0, 3, 1, 5, 70, 80, 98, 55, 11, 132, 455],
  "Bombay": [0, 0, 0, 6, 17, 27, 12, 9, 0, 130, 201],
  "Calcutta": [0, 0, 2, 1, 8, 4, 2, 26, 3, 0, 46],
  "Delhi": [32, 3, 8, 23, 3, 49, 33, 41, 12, 111, 315],
  "Hyderabad": [0, 0, 0, 2, 23, 15, 21, 9, 0, 12, 82],
  "Kanpur": [2, 0, 5, 4, 10, 0, 3, 12, 2, 3, 41],
  "Madras": [0, 0, 0, 2, 76, 25, 30, 88, 5, 51, 277],
  "TOTAL (CITIES)": [34, 6, 16, 43, 215, 258, 245, 247, 36, 506, 1606],
 },
 "Grand": {"GRAND TOTAL": [2593, 284, 366, 305, 8602, 2562, 8004, 8390, 546, 6565, 38217]},
}
