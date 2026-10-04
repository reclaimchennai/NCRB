# ADSI 1982, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / UTs / cities, pages 1-6 (printed sideways; pages 1-3 columns 3-9 for States 1-15, States
# 16-22 and UTs, and cities; pages 4-6 columns 10-16 likewise). Read from the page images; "—" (nil) is 0; the
# bracketed percentages are not recorded. Lucknow is printed "N.A." across the row. Checked by
# scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1982, "adsi"
SOURCE = "raw/adsi/1982/table_content/1680161612appendix-51982.pdf"
PAGES = "1-6"
TITLE = ("Appendix V: Distribution of Suicidal Deaths due to Different Causes with Percentage to Total Suicidal Deaths "
         "in the States/UTs/Cities during the year 1982")
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear person", "Fall in social reputation",
        "Other causes", "Total"]
CORRECTIONS = {
    ("Tamil Nadu", "Dreadful diseases"): (400, 1400, "printed '400(25.5)' with the thousands digit lost; 1400/5490 = 25.5% (400 would be 7.3%), the row then adds up to the printed 5,490 and the States' column to the printed 6,409"),
    ("TOTAL (CITIES)", "Other causes"): (690, 1690, "printed '690(62.1)' with the thousands digit lost; the cities add up to 1690 = 62.0% of 2,724 (690 would be 25.3%), and the totals row then adds up to the printed 2,724"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [115, 101, 154, 165, 142, 39, 64, 910, 19, 11, 7, 23, 1240, 2990],
  "Assam": [6, 16, 14, 84, 83, 21, 19, 94, 12, 7, 3, 18, 1328, 1705],
  "Bihar": [31, 93, 22, 31, 51, 22, 42, 71, 7, 5, 3, 3, 333, 714],
  "Gujarat": [25, 127, 215, 41, 91, 144, 11, 210, 55, 27, 36, 34, 777, 1793],
  "Haryana": [24, 52, 68, 16, 17, 44, 15, 80, 6, 4, 2, 15, 118, 461],
  "Himachal Pradesh": [0, 2, 1, 0, 7, 3, 0, 12, 0, 6, 2, 0, 57, 90],
  "Jammu & Kashmir": [1, 2, 0, 3, 1, 0, 0, 0, 1, 0, 0, 0, 14, 22],
  "Karnataka": [33, 69, 52, 85, 46, 110, 65, 423, 17, 5, 10, 13, 4367, 5295],
  "Kerala": [28, 448, 122, 60, 260, 185, 40, 411, 83, 109, 94, 164, 2609, 4613],
  "Madhya Pradesh": [58, 604, 163, 82, 94, 79, 89, 677, 21, 19, 20, 17, 1128, 3051],
  "Maharashtra": [44, 361, 244, 78, 110, 168, 70, 566, 50, 62, 14, 38, 2085, 3890],
  "Manipur": [0, 0, 0, 2, 4, 5, 1, 4, 1, 0, 0, 0, 24, 41],
  "Meghalaya": [1, 2, 3, 1, 6, 1, 0, 6, 0, 0, 2, 0, 14, 36],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5],
  "Orissa": [15, 140, 183, 29, 81, 64, 10, 178, 13, 8, 2, 15, 1565, 2303],
  "Punjab": [12, 62, 31, 23, 16, 5, 4, 82, 10, 2, 4, 3, 105, 359],
  "Rajasthan": [8, 117, 107, 11, 18, 76, 27, 118, 7, 12, 8, 24, 404, 937],
  "Sikkim": [0, 0, 0, 5, 0, 8, 0, 4, 0, 0, 0, 0, 0, 17],
  "Tamil Nadu": [65, 442, 214, 134, 275, 43, 41, 1400, 63, 38, 23, 25, 2727, 5490],
  "Tripura": [13, 78, 75, 46, 39, 15, 0, 31, 3, 0, 0, 1, 249, 550],
  "Uttar Pradesh": [63, 191, 138, 64, 95, 68, 160, 286, 32, 20, 112, 50, 1198, 2477],
  "West Bengal": [210, 774, 876, 228, 713, 273, 164, 846, 105, 31, 28, 36, 2597, 6881],
  "TOTAL (STATES)": [752, 3681, 2682, 1188, 2149, 1373, 822, 6409, 505, 366, 370, 479, 22944, 43720],
 },
 "U.Ts.": {
  "A & N Islands": [2, 17, 17, 0, 4, 2, 0, 5, 0, 0, 1, 0, 24, 72],
  "Arunachal Pradesh": [0, 0, 0, 1, 1, 4, 0, 3, 0, 0, 0, 0, 14, 23],
  "Chandigarh": [0, 0, 1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 15, 21],
  "D & N Haveli": [0, 3, 4, 0, 1, 3, 0, 2, 0, 1, 1, 0, 0, 15],
  "Delhi": [16, 44, 48, 6, 17, 14, 2, 44, 11, 5, 4, 1, 223, 435],
  "Goa, Daman & Diu": [0, 0, 5, 2, 4, 20, 0, 9, 1, 2, 0, 0, 43, 86],
  "Lakshadweep": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
  "Mizoram": [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 7],
  "Pondicherry": [1, 58, 100, 5, 9, 9, 0, 155, 1, 0, 4, 0, 10, 352],
  "TOTAL (U.TS.)": [19, 122, 175, 14, 36, 55, 2, 223, 13, 8, 10, 1, 334, 1012],
 },
 "Cities": {
  "Ahmedabad": [4, 38, 4, 2, 12, 9, 0, 19, 6, 3, 7, 4, 77, 185],
  "Bangalore": [0, 1, 9, 6, 7, 3, 4, 15, 0, 0, 0, 0, 673, 718],
  "Bombay": [2, 6, 12, 9, 17, 7, 2, 17, 12, 7, 2, 15, 99, 207],
  "Calcutta": [0, 0, 7, 2, 3, 8, 0, 3, 0, 0, 0, 0, 18, 41],
  "Delhi": [15, 43, 48, 3, 17, 12, 2, 40, 8, 5, 4, 1, 219, 417],
  "Hyderabad": [4, 11, 15, 5, 17, 4, 1, 14, 6, 4, 1, 16, 90, 188],
  "Jaipur": [2, 15, 4, 0, 8, 0, 17, 11, 2, 0, 5, 3, 59, 126],
  "Kanpur": [0, 4, 2, 2, 7, 0, 0, 0, 5, 1, 6, 0, 17, 44],
  "Lucknow": [None] * 14,
  "Madras": [8, 25, 25, 25, 25, 6, 0, 103, 1, 20, 0, 4, 220, 462],
  "Nagpur": [8, 6, 4, 0, 0, 3, 0, 26, 0, 0, 1, 0, 148, 196],
  "Pune": [1, 17, 4, 1, 5, 10, 1, 14, 3, 8, 1, 5, 70, 140],
  "TOTAL (CITIES)": [44, 166, 134, 55, 118, 62, 27, 262, 43, 48, 27, 48, 1690, 2724],
 },
 "Grand": {"GRAND TOTAL": [771, 3803, 2857, 1202, 2185, 1428, 824, 6632, 518, 374, 380, 480, 23278, 44732]},
}
