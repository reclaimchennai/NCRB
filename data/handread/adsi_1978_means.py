# ADSI 1978, Appendix VI: suicides by means with percentage to total, States / UTs / cities
# (raw/adsi/1978/table_content/1680159963appendix-61978.pdf, pages 1-4, printed sideways: pages 1-2 Railways to Fire,
# pages 3-4 Drowning to Total). Read from the page images; '—' (nil) is 0; percentages left out. The same figures by
# sex are in Appendix IV (raw/adsi/1978/table_content/1680160020appendix-41978.pdf). Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1978, "adsi"
SOURCE = "raw/adsi/1978/table_content/1680159963appendix-61978.pdf"
PAGES = "1-4"
TITLE = "Appendix VI: Distribution of the Suicidal Deaths by Different Means with Percentage to Total Suicidal Deaths in the States/U.Ts./Cities during 1978"
CATS = ["By Railways", "By Machine", "By Firearms", "By Weapons", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By other Causes", "Total"]
CORRECTIONS = {
    ("Nagaland", "Total"): ("81 (00·0)", 8, "printed '81 (00·0)', the '1' of '(100·0)' slipped left; the row adds up to 8 and its percentages (2 = 25·0%, 3 = 37·5%) are of 8"),
    ("Goa, Daman & Diu", "By Firearms"): ("—", 4, "printed '— (0·0)'; the row's other figures add to 66 against its printed Total 70, their printed percentages add to 94·3% leaving 5·7% = 4/70, the UTs' Firearms column adds to 3 against its printed 7 (Grand Total 385 = 378 + 7), and Appendix IV prints Goa's firearms suicides as 4 male. The printed (0·0) goes with the dropped figure, so here the percentage does not confirm the change on its own"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [278, 1, 15, 2, 779, 127, 1001, 350, 45, 283, 2881],
  "Assam": [172, 8, 8, 9, 116, 56, 407, 678, 25, 500, 1979],
  "Bihar": [46, 6, 12, 8, 77, 141, 362, 218, 79, 250, 1199],
  "Gujarat": [68, 5, 2, 2, 345, 259, 365, 141, 9, 778, 1974],
  "Haryana": [56, 0, 7, 7, 16, 48, 134, 137, 25, 62, 492],
  "Himachal Pradesh": [0, 0, 1, 3, 4, 2, 11, 22, 6, 8, 57],
  "Jammu & Kashmir": [0, 0, 2, 0, 2, 5, 4, 8, 0, 19, 40],
  "Karnataka": [302, 99, 14, 4, 1013, 223, 1629, 733, 77, 798, 4892],
  "Kerala": [166, 1, 6, 20, 1510, 12, 438, 1269, 35, 133, 3590],
  "Madhya Pradesh": [259, 3, 13, 70, 213, 202, 411, 712, 89, 409, 2381],
  "Maharashtra": [185, 3, 3, 7, 872, 381, 875, 454, 48, 334, 3162],
  "Manipur": [0, 0, 0, 0, 2, 0, 3, 3, 0, 1, 9],
  "Meghalaya": [0, 0, 2, 0, 0, 2, 9, 16, 12, 12, 53],
  "Nagaland": [0, 0, 2, 0, 1, 0, 2, 3, 0, 0, 8],
  "Orissa": [85, 9, 5, 5, 442, 27, 172, 413, 11, 288, 1457],
  "Punjab": [91, 2, 6, 5, 22, 14, 44, 55, 2, 25, 266],
  "Rajasthan": [89, 3, 14, 0, 47, 64, 389, 121, 22, 127, 876],
  "Sikkim": [0, 0, 0, 0, 2, 0, 1, 9, 0, 0, 12],
  "Tamil Nadu": [582, 14, 8, 1, 1163, 216, 583, 528, 41, 769, 3905],
  "Tripura": [0, 0, 0, 0, 140, 1, 21, 91, 0, 27, 280],
  "Uttar Pradesh": [559, 63, 232, 133, 151, 308, 482, 577, 79, 678, 3262],
  "West Bengal": [340, 4, 26, 19, 2719, 275, 372, 1802, 10, 1176, 6743],
  "TOTAL (STATES)": [3278, 221, 378, 295, 9636, 2363, 7715, 8340, 615, 6677, 39518],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0, 0, 0, 12, 3, 11, 12, 0, 0, 38],
  "Arunachal Pradesh": [0, 0, 1, 0, 1, 1, 0, 5, 1, 2, 11],
  "Chandigarh": [0, 0, 1, 0, 4, 4, 7, 3, 0, 0, 19],
  "D. & N. Haveli": [0, 0, 0, 0, 1, 0, 3, 10, 0, 0, 14],
  "Delhi": [25, 1, 1, 1, 39, 51, 22, 24, 20, 21, 205],
  "Goa, Daman & Diu": [0, 0, 4, 0, 12, 4, 23, 22, 5, 0, 70],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4],
  "Pondicherry": [0, 0, 0, 0, 138, 5, 42, 55, 0, 87, 327],
  "TOTAL (U.TS.)": [25, 1, 7, 1, 207, 68, 108, 136, 26, 110, 689],
 },
 "Cities": {
  "Ahmedabad": [3, 0, 0, 0, 26, 49, 67, 3, 3, 15, 166],
  "Bangalore": [0, 0, 2, 1, 279, 113, 156, 100, 23, 271, 945],
  "Bombay": [0, 1, 5, 0, 39, 67, 22, 23, 11, 18, 186],
  "Calcutta": [0, 1, 0, 2, 1, 3, 0, 16, 2, 4, 29],
  "Delhi": [25, 1, 1, 1, 39, 44, 19, 24, 20, 15, 189],
  "Hyderabad": [0, 0, 0, 0, 29, 10, 23, 20, 5, 9, 96],
  "Kanpur": [2, 0, 3, 0, 13, 1, 0, 26, 3, 24, 72],
  "Madras": [0, 1, 0, 1, 43, 27, 23, 34, 2, 17, 148],
  "TOTAL (CITIES)": [30, 4, 11, 5, 469, 314, 310, 246, 69, 373, 1831],
 },
 "Grand": {"GRAND TOTAL": [3303, 222, 385, 296, 9843, 2431, 7823, 8476, 641, 6787, 40207]},
}
