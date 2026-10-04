# ADSI 1977, Appendix II (raw/adsi/1977/table_content/appendix-2_1977.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1977, "adsi"
SOURCE = "raw/adsi/1977/table_content/appendix-2_1977.pdf"
PAGES = "1-2"
TITLE = "Appendix II: State-wise distribution of accidental deaths due to other causes during 1977 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [1016, 199],
  "Assam": [113, 30],
  "Bihar": [273, 54],
  "Gujarat": [207, 42],
  "Haryana": [339, 74],
  "Himachal Pradesh": [99, 3],
  "Jammu & Kashmir": [117, 18],
  "Karnataka": [930, 258],
  "Kerala": [373, 93],
  "Madhya Pradesh": [906, 271],
  "Maharashtra": [1306, 368],
  "Manipur": [26, 10],
  "Meghalaya": [21, 1],
  "Nagaland": [21, 0],
  "Orissa": [384, 45],
  "Punjab": [369, 83],
  "Rajasthan": [558, 85],
  "Sikkim": [44, 5],
  "Tamil Nadu": [1185, 279],
  "Tripura": [11, 1],
  "Uttar Pradesh": [2054, 334],
  "West Bengal": [1362, 275],
  "TOTAL (STATES)": [11714, 2528],
 },
 "U.Ts.": {
  "A. & N. Islands": [3, 0],
  "Arunachal Pradesh": [10, 0],
  "Chandigarh": [8, 5],
  "D. & N. Haveli": [2, 0],
  "Delhi": [554, 115],
  "Goa, Daman, Diu": [71, 14],
  "Lakshadweep": [0, 0],
  "Mizoram": [36, 4],
  "Pondicherry": [25, 1],
  "TOTAL (U.TS.)": [709, 139],
 },
 "Grand": {
  "GRAND TOTAL": [12423, 2667],
 },
 "Cities": {
  "Ahmedabad": [43, 8],
  "Bangalore": [158, 99],
  "Bombay": [609, 213],
  "Calcutta": [307, 51],
  "Delhi": [470, 101],
  "Hyderabad": [2, 2],
  "Kanpur": [89, 7],
  "Madras": [167, 43],
  "TOTAL (CITIES)": [1845, 524],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1215],
  "Assam": [None, None, 143],
  "Bihar": [None, None, 327],
  "Gujarat": [None, None, 249],
  "Haryana": [None, None, 413],
  "Himachal Pradesh": [None, None, 102],
  "Jammu & Kashmir": [None, None, 135],
  "Karnataka": [None, None, 1188],
  "Kerala": [None, None, 466],
  "Madhya Pradesh": [None, None, 1177],
  "Maharashtra": [None, None, 1674],
  "Manipur": [None, None, 36],
  "Meghalaya": [None, None, 22],
  "Nagaland": [None, None, 21],
  "Orissa": [None, None, 429],
  "Punjab": [None, None, 452],
  "Rajasthan": [None, None, 643],
  "Sikkim": [None, None, 49],
  "Tamil Nadu": [None, None, 1464],
  "Tripura": [None, None, 12],
  "Uttar Pradesh": [None, None, 2388],
  "West Bengal": [None, None, 1637],
  "TOTAL (STATES)": [None, None, 14242],
 },
 "U.Ts.": {
  "A. & N. Islands": [None, None, 3],
  "Arunachal Pradesh": [None, None, 10],
  "Chandigarh": [None, None, 13],
  "D. & N. Haveli": [None, None, 2],
  "Delhi": [None, None, 669],
  "Goa, Daman, Diu": [None, None, 85],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 40],
  "Pondicherry": [None, None, 26],
  "TOTAL (U.TS.)": [None, None, 848],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 15090],
 },
 "Cities": {
  "Ahmedabad": [None, None, 51],
  "Bangalore": [None, None, 257],
  "Bombay": [None, None, 822],
  "Calcutta": [None, None, 358],
  "Delhi": [None, None, 571],
  "Hyderabad": [None, None, 4],
  "Kanpur": [None, None, 96],
  "Madras": [None, None, 210],
  "TOTAL (CITIES)": [None, None, 2369],
 },
}
