# ADSI 1985, Appendix V: statewise distribution of suicidal deaths by different causes with percentage to total deaths
# of respective States / U.Ts. / cities, pages 1-9 (printed sideways; pages 1-3 columns 3-8, pages 4-6 columns 9-14,
# pages 7-9 columns 15-19). Read from the page images; "—" (nil) is 0; the bracketed percentages are not recorded.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1985, "adsi"
SOURCE = "raw/adsi/1985/table_content/1680163057appendix-51985.pdf"
PAGES = "1-9"
TITLE = ("Appendix V: Statewise Distribution Of Suicidal Deaths By Different Causes With Percentage To Total Deaths Of "
         "Respective States During 1985")
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear person", "Fall in social reputation",
        "Dowry disputes", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
# Assam, Death of dear person: the first digit is clear, the second blurred; read 15 (15/1845 = 0.8%, as printed;
# 13 would be 0.7%), which the row and column sums confirm. The Grand Total under Failure in examination prints with
# its first digit lost (".032"); read 1032 = 1013 (States) + 19 (U.Ts.).
CORRECTIONS = {
    ("Punjab", "Causes not known"): (57, 51, "printed '57(14.6)'; 51/350 = 14.6% (57 would be 16.3%), the row then adds up to 350 and the States' column to the printed 5303"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [50, 113, 149, 124, 120, 50, 166, 935, 26, 28, 8, 292, 0, 0, 0, 1960, 4021],
  "Assam": [81, 32, 40, 50, 153, 77, 77, 133, 39, 32, 15, 5, 0, 3, 725, 383, 1845],
  "Bihar": [23, 40, 16, 68, 32, 31, 54, 88, 20, 7, 16, 2, 31, 2, 249, 109, 788],
  "Gujarat": [24, 83, 250, 37, 111, 154, 10, 299, 53, 38, 38, 46, 11, 3, 83, 659, 1899],
  "Haryana": [13, 53, 69, 44, 13, 31, 28, 150, 32, 8, 15, 21, 38, 0, 144, 201, 860],
  "Himachal Pradesh": [1, 5, 8, 6, 6, 7, 0, 6, 3, 0, 2, 7, 2, 0, 9, 28, 90],
  "Jammu & Kashmir": [2, 2, 1, 1, 3, 1, 0, 0, 3, 0, 0, 1, 0, 0, 5, 13, 32],
  "Karnataka": [70, 213, 99, 256, 107, 192, 133, 771, 83, 95, 56, 24, 41, 19, 662, 1955, 4776],
  "Kerala": [56, 484, 123, 30, 219, 244, 44, 721, 64, 207, 25, 138, 7, 0, 186, 3527, 6075],
  "Madhya Pradesh": [77, 643, 216, 38, 95, 167, 99, 493, 31, 19, 33, 38, 24, 3, 0, 1472, 3448],
  "Maharashtra": [65, 344, 394, 137, 164, 221, 136, 683, 85, 55, 30, 25, 49, 10, 342, 2018, 4758],
  "Manipur": [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 0, 0, 0, 21, 27],
  "Meghalaya": [1, 0, 0, 0, 3, 3, 1, 11, 0, 0, 0, 0, 0, 0, 17, 0, 36],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 4, 17],
  "Orissa": [85, 184, 119, 50, 217, 66, 34, 291, 33, 19, 8, 13, 9, 6, 438, 770, 2342],
  "Punjab": [5, 36, 24, 15, 22, 27, 8, 55, 13, 7, 4, 6, 9, 1, 51, 67, 350],
  "Rajasthan": [30, 146, 140, 20, 34, 75, 28, 142, 8, 10, 10, 66, 11, 6, 28, 159, 913],
  "Sikkim": [0, 0, 0, 4, 0, 6, 0, 3, 0, 0, 0, 3, 0, 0, 9, 0, 25],
  "Tamil Nadu": [81, 557, 431, 323, 401, 72, 155, 1505, 122, 28, 133, 33, 14, 6, 525, 3412, 7798],
  "Tripura": [54, 41, 13, 6, 51, 28, 17, 93, 0, 0, 2, 8, 0, 0, 0, 148, 461],
  "Uttar Pradesh": [25, 117, 128, 89, 87, 59, 167, 295, 27, 14, 4, 15, 31, 2, 433, 1197, 2690],
  "West Bengal": [270, 962, 1137, 0, 966, 406, 214, 809, 0, 32, 44, 40, 85, 51, 1384, 2111, 8511],
  "TOTAL (STATES)": [1013, 4056, 3357, 1298, 2804, 1917, 1371, 7484, 642, 600, 444, 785, 362, 112, 5303, 20214, 51762],
 },
 "U.Ts.": {
  "A & N Islands": [0, 1, 22, 2, 6, 2, 0, 10, 1, 1, 0, 0, 0, 0, 0, 20, 65],
  "Arunachal Pradesh": [0, 0, 3, 0, 5, 2, 0, 3, 0, 1, 1, 1, 0, 0, 19, 6, 41],
  "Chandigarh": [0, 0, 1, 0, 2, 0, 0, 13, 0, 0, 0, 0, 0, 0, 9, 1, 26],
  "D & N Haveli": [0, 1, 2, 0, 0, 3, 0, 2, 0, 0, 2, 0, 0, 0, 1, 2, 13],
  "Delhi": [12, 25, 22, 10, 10, 7, 0, 58, 7, 1, 5, 6, 14, 0, 166, 99, 442],
  "Goa, Daman & Diu": [2, 2, 10, 2, 9, 13, 0, 14, 7, 2, 0, 2, 0, 0, 36, 12, 111],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Mizoram": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 17],
  "Pondicherry": [5, 87, 53, 25, 10, 0, 0, 117, 3, 0, 1, 0, 0, 0, 33, 0, 334],
  "TOTAL (U.TS.)": [19, 117, 113, 39, 42, 27, 0, 217, 18, 5, 9, 9, 14, 0, 280, 140, 1049],
 },
 "Cities": {
  "Ahmedabad": [3, 5, 7, 0, 5, 16, 0, 25, 3, 6, 6, 1, 0, 0, 0, 94, 171],
  "Bangalore": [1, 1, 1, 23, 5, 2, 0, 35, 8, 14, 0, 4, 0, 0, 0, 367, 461],
  "Bombay": [10, 19, 20, 9, 19, 22, 3, 56, 13, 5, 10, 5, 7, 9, 173, 43, 423],
  "Calcutta": [5, 6, 7, 0, 16, 5, 1, 31, 1, 0, 1, 3, 2, 0, 41, 9, 128],
  "Delhi": [10, 14, 19, 10, 8, 7, 0, 57, 7, 1, 4, 6, 11, 0, 160, 96, 410],
  "Hyderabad": [8, 2, 8, 4, 4, 6, 0, 20, 0, 0, 0, 3, 9, 0, 45, 75, 184],
  "Jaipur": [8, 14, 9, 0, 5, 0, 1, 5, 0, 0, 0, 3, 0, 0, 0, 0, 45],
  "Kanpur": [0, 29, 24, 7, 0, 4, 0, 13, 0, 0, 0, 0, 0, 0, 0, 178, 255],
  "Lucknow": [0, 0, 0, 1, 4, 0, 0, 38, 0, 0, 0, 0, 0, 0, 17, 12, 72],
  "Madras": [13, 4, 32, 57, 44, 11, 19, 120, 34, 1, 13, 14, 3, 0, 71, 282, 718],
  "Nagpur": [18, 7, 3, 0, 15, 0, 0, 7, 4, 0, 0, 0, 0, 0, 19, 121, 194],
  "Pune": [1, 7, 9, 2, 13, 9, 1, 17, 5, 1, 1, 1, 0, 0, 0, 98, 165],
  "TOTAL (CITIES)": [77, 108, 139, 113, 138, 82, 25, 424, 75, 28, 35, 40, 32, 9, 526, 1375, 3226],
 },
 "Grand": {"GRAND TOTAL": [1032, 4173, 3470, 1337, 2846, 1944, 1371, 7701, 660, 605, 453, 794, 376, 112, 5583, 20354, 52811]},
}

