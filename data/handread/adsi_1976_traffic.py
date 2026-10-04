# ADSI 1976, Appendix II (raw/adsi/1976/table_content/appendix-2_1976.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1976, "adsi"
SOURCE = "raw/adsi/1976/table_content/appendix-2_1976.pdf"
PAGES = "1-2"
TITLE = "Appendix II: Statewise distribution of accidental deaths due to other causes during 1976 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {("Delhi", "Persons killed"): (671, 670, "U.T. Delhi: Female deaths on roads printed 116; 115 makes the U.T. column add to its printed Total (U.Ts.) 128 and the Grand Total 3410, and equals the row's own Motor Vehicle (100) + Other Road (15) female deaths")}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [1051, 174],
  "Assam": [247, 72],
  "Bihar": [446, 69],
  "Gujarat": [134, 33],
  "Haryana": [213, 72],
  "Himachal Pradesh": [100, 4],
  "Jammu & Kashmir": [110, 15],
  "Karnataka": [848, 200],
  "Kerala": [220, 43],
  "Madhya Pradesh": [1709, 1207],
  "Maharashtra": [1291, 295],
  "Manipur": [22, 2],
  "Meghalaya": [30, 3],
  "Nagaland": [26, 0],
  "Orissa": [379, 48],
  "Punjab": [364, 70],
  "Rajasthan": [444, 94],
  "Sikkim": [21, 1],
  "Tamil Nadu": [1311, 253],
  "Tripura": [24, 6],
  "Uttar Pradesh": [1652, 337],
  "West Bengal": [1220, 284],
  "TOTAL (STATES)": [11862, 3282],
 },
 "U.Ts.": {
  "A. & N. Islands": [0, 0],
  "Arunachal Pradesh": [23, 2],
  "Chandigarh": [7, 4],
  "D. & N. Haveli": [0, 0],
  "Delhi": [555, 115],
  "Goa, Daman & Diu": [15, 4],
  "Lakshadweep": [0, 0],
  "Mizoram": [9, 1],
  "Pondicherry": [22, 2],
  "TOTAL (U.TS.)": [631, 128],
 },
 "Grand": {
  "GRAND TOTAL": [12493, 3410],
 },
 "Cities": {
  "Ahmedabad": [13, 6],
  "Bangalore": [73, 15],
  "Bombay": [647, 165],
  "Calcutta": [293, 34],
  "Delhi": [515, 100],
  "Hyderabad": [7, 1],
  "Kanpur": [88, 13],
  "Madras": [157, 51],
  "TOTAL (CITIES)": [1793, 385],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1225],
  "Assam": [None, None, 319],
  "Bihar": [None, None, 515],
  "Gujarat": [None, None, 167],
  "Haryana": [None, None, 285],
  "Himachal Pradesh": [None, None, 104],
  "Jammu & Kashmir": [None, None, 125],
  "Karnataka": [None, None, 1048],
  "Kerala": [None, None, 263],
  "Madhya Pradesh": [None, None, 2916],
  "Maharashtra": [None, None, 1586],
  "Manipur": [None, None, 24],
  "Meghalaya": [None, None, 33],
  "Nagaland": [None, None, 26],
  "Orissa": [None, None, 427],
  "Punjab": [None, None, 434],
  "Rajasthan": [None, None, 538],
  "Sikkim": [None, None, 22],
  "Tamil Nadu": [None, None, 1564],
  "Tripura": [None, None, 30],
  "Uttar Pradesh": [None, None, 1989],
  "West Bengal": [None, None, 1504],
  "TOTAL (STATES)": [None, None, 15144],
 },
 "U.Ts.": {
  "A. & N. Islands": [None, None, 0],
  "Arunachal Pradesh": [None, None, 25],
  "Chandigarh": [None, None, 11],
  "D. & N. Haveli": [None, None, 0],
  "Delhi": [None, None, 670],
  "Goa, Daman & Diu": [None, None, 19],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 10],
  "Pondicherry": [None, None, 24],
  "TOTAL (U.TS.)": [None, None, 759],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 15903],
 },
 "Cities": {
  "Ahmedabad": [None, None, 19],
  "Bangalore": [None, None, 88],
  "Bombay": [None, None, 812],
  "Calcutta": [None, None, 327],
  "Delhi": [None, None, 615],
  "Hyderabad": [None, None, 8],
  "Kanpur": [None, None, 101],
  "Madras": [None, None, 208],
  "TOTAL (CITIES)": [None, None, 2178],
 },
}
