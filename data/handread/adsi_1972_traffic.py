# ADSI 1972, Appendix II (raw/adsi/1972/table_content/appendix-2_1972.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1972, "adsi"
SOURCE = "raw/adsi/1972/table_content/appendix-2_1972.pdf"
PAGES = "1-2"
TITLE = "Appendix II: Statement of number of accidental deaths in States/U.Ts./Cities during 1972 (by other causes, Part II: On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [641, 147],
  "Assam": [103, 21],
  "Bihar": [174, 45],
  "Gujarat": [268, 64],
  "Haryana": [269, 54],
  "Himachal Pradesh": [110, 7],
  "Jammu & Kashmir": [411, 84],
  "Karnataka": [752, 146],
  "Kerala": [364, 74],
  "Madhya Pradesh": [1057, 266],
  "Maharashtra": [1254, 252],
  "Manipur": [6, 6],
  "Meghalaya": [29, 2],
  "Nagaland": [8, 1],
  "Orissa": [154, 32],
  "Punjab": [330, 57],
  "Rajasthan": [478, 92],
  "Tamil Nadu": [1176, 243],
  "Tripura": [49, 13],
  "Uttar Pradesh": [1628, 257],
  "West Bengal": [1143, 238],
  "TOTAL (STATES)": [10404, 2101],
 },
 "U.Ts.": {
  "A. & N. Islands": [1, 0],
  "Chandigarh": [5, 2],
  "D. & N. Haveli": [1, 1],
  "Delhi": [290, 39],
  "Goa, Daman & Diu": [18, 2],
  "Lakshadweep": [0, 0],
  "Mizoram": [13, 0],
  "Pondicherry": [11, 3],
  "TOTAL (U.TS.)": [339, 47],
 },
 "Grand": {
  "GRAND TOTAL": [10743, 2148],
 },
 "Cities": {
  "Ahmedabad": [26, 4],
  "Bangalore": [121, 22],
  "Bombay": [700, 138],
  "Calcutta": [401, 76],
  "Delhi": [214, 34],
  "Hyderabad": [0, 0],
  "Kanpur": [47, 10],
  "Madras": [180, 40],
  "TOTAL (CITIES)": [1689, 324],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 788],
  "Assam": [None, None, 124],
  "Bihar": [None, None, 219],
  "Gujarat": [None, None, 332],
  "Haryana": [None, None, 323],
  "Himachal Pradesh": [None, None, 117],
  "Jammu & Kashmir": [None, None, 495],
  "Karnataka": [None, None, 898],
  "Kerala": [None, None, 438],
  "Madhya Pradesh": [None, None, 1323],
  "Maharashtra": [None, None, 1506],
  "Manipur": [None, None, 12],
  "Meghalaya": [None, None, 31],
  "Nagaland": [None, None, 9],
  "Orissa": [None, None, 186],
  "Punjab": [None, None, 387],
  "Rajasthan": [None, None, 570],
  "Tamil Nadu": [None, None, 1419],
  "Tripura": [None, None, 62],
  "Uttar Pradesh": [None, None, 1885],
  "West Bengal": [None, None, 1381],
  "TOTAL (STATES)": [None, None, 12505],
 },
 "U.Ts.": {
  "A. & N. Islands": [None, None, 1],
  "Chandigarh": [None, None, 7],
  "D. & N. Haveli": [None, None, 2],
  "Delhi": [None, None, 329],
  "Goa, Daman & Diu": [None, None, 20],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 13],
  "Pondicherry": [None, None, 14],
  "TOTAL (U.TS.)": [None, None, 386],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 12891],
 },
 "Cities": {
  "Ahmedabad": [None, None, 30],
  "Bangalore": [None, None, 143],
  "Bombay": [None, None, 838],
  "Calcutta": [None, None, 477],
  "Delhi": [None, None, 248],
  "Hyderabad": [None, None, 0],
  "Kanpur": [None, None, 57],
  "Madras": [None, None, 220],
  "TOTAL (CITIES)": [None, None, 2013],
 },
}
