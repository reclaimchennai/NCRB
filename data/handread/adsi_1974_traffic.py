# ADSI 1974, Appendix II (raw/adsi/1974/table_content/appendix-2_1974.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1974, "adsi"
SOURCE = "raw/adsi/1974/table_content/appendix-2_1974.pdf"
PAGES = "1-2"
TITLE = "Appendix II: State-wise distribution of accidental deaths due to other causes during 1974 (On Road, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [1026, 167],
  "Assam": [143, 43],
  "Bihar": [356, 67],
  "Gujarat": [289, 55],
  "Haryana": [314, 50],
  "Himachal Pradesh": [105, 11],
  "Jammu & Kashmir": [97, 21],
  "Karnataka": [795, 142],
  "Kerala": [359, 73],
  "Madhya Pradesh": [1097, 239],
  "Maharashtra": [1274, 258],
  "Manipur": [0, 0],
  "Meghalaya": [13, 2],
  "Nagaland": [9, 0],
  "Orissa": [136, 20],
  "Punjab": [275, 57],
  "Rajasthan": [592, 79],
  "Tamil Nadu": [1605, 322],
  "Tripura": [21, 2],
  "Uttar Pradesh": [1920, 316],
  "West Bengal": [1013, 284],
  "TOTAL (STATES)": [11439, 2208],
 },
 "U.Ts.": {
  "A & N Islands": [2, 1],
  "Arunachal Pradesh": [20, 0],
  "Chandigarh": [24, 6],
  "D. & N. Haveli": [0, 0],
  "Delhi": [522, 50],
  "Goa, Daman & Diu": [8, 1],
  "Lakshadweep": [0, 0],
  "Mizoram": [6, 2],
  "Pondicherry": [15, 3],
  "TOTAL (U.TS.)": [597, 63],
 },
 "Grand": {
  "GRAND TOTAL": [12036, 2271],
 },
 "Cities": {
  "Ahmedabad": [26, 4],
  "Bangalore": [157, 28],
  "Bombay": [636, 116],
  "Calcutta": [330, 52],
  "Delhi": [456, 46],
  "Hyderabad": [132, 33],
  "Kanpur": [13, 42],
  "Madras": [213, 45],
  "TOTAL (CITIES)": [1963, 366],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1193],
  "Assam": [None, None, 186],
  "Bihar": [None, None, 423],
  "Gujarat": [None, None, 344],
  "Haryana": [None, None, 364],
  "Himachal Pradesh": [None, None, 116],
  "Jammu & Kashmir": [None, None, 118],
  "Karnataka": [None, None, 937],
  "Kerala": [None, None, 432],
  "Madhya Pradesh": [None, None, 1336],
  "Maharashtra": [None, None, 1532],
  "Manipur": [None, None, 0],
  "Meghalaya": [None, None, 15],
  "Nagaland": [None, None, 9],
  "Orissa": [None, None, 156],
  "Punjab": [None, None, 332],
  "Rajasthan": [None, None, 671],
  "Tamil Nadu": [None, None, 1927],
  "Tripura": [None, None, 23],
  "Uttar Pradesh": [None, None, 2236],
  "West Bengal": [None, None, 1297],
  "TOTAL (STATES)": [None, None, 13647],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 3],
  "Arunachal Pradesh": [None, None, 20],
  "Chandigarh": [None, None, 30],
  "D. & N. Haveli": [None, None, 0],
  "Delhi": [None, None, 572],
  "Goa, Daman & Diu": [None, None, 9],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 8],
  "Pondicherry": [None, None, 18],
  "TOTAL (U.TS.)": [None, None, 660],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 14307],
 },
 "Cities": {
  "Ahmedabad": [None, None, 30],
  "Bangalore": [None, None, 185],
  "Bombay": [None, None, 752],
  "Calcutta": [None, None, 382],
  "Delhi": [None, None, 502],
  "Hyderabad": [None, None, 165],
  "Kanpur": [None, None, 55],
  "Madras": [None, None, 258],
  "TOTAL (CITIES)": [None, None, 2329],
 },
}
