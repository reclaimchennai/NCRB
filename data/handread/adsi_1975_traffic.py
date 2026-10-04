# ADSI 1975, Appendix II (raw/adsi/1975/table_content/appendix-2_1975.pdf, pages 1). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1975, "adsi"
SOURCE = "raw/adsi/1975/table_content/appendix-2_1975.pdf"
PAGES = "1"
TITLE = "Appendix II: Statewise distribution of accidental deaths due to other causes during 1975 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [964, 149],
  "Assam": [159, 33],
  "Bihar": [317, 51],
  "Gujarat": [528, 127],
  "Haryana": [277, 50],
  "Himachal Pradesh": [98, 6],
  "Jammu & Kashmir": [119, 32],
  "Karnataka": [1058, 228],
  "Kerala": [345, 62],
  "Madhya Pradesh": [1305, 317],
  "Maharashtra": [1332, 276],
  "Manipur": [8, 0],
  "Meghalaya": [16, 0],
  "Nagaland": [8, 0],
  "Orissa": [237, 31],
  "Punjab": [293, 39],
  "Rajasthan": [384, 93],
  "Sikkim": [15, 3],
  "Tamil Nadu": [1547, 325],
  "Tripura": [39, 9],
  "Uttar Pradesh": [1728, 381],
  "West Bengal": [1176, 309],
  "TOTAL (STATES)": [11953, 2521],
 },
 "U.Ts.": {
  "A.&N. Islands": [1, 1],
  "Arunachal Pradesh": [15, 2],
  "Chandigarh": [27, 7],
  "D. & N. Haveli": [1, 0],
  "Delhi": [508, 77],
  "Goa, Daman & Diu": [11, 3],
  "Lakshadweep": [0, 0],
  "Mizoram": [17, 7],
  "Pondicherry": [34, 5],
  "TOTAL (U.TS.)": [614, 102],
 },
 "Grand": {
  "GRAND TOTAL": [12567, 2623],
 },
 "Cities": {
  "Ahmedabad": [26, 6],
  "Bangalore": [169, 61],
  "Bombay": [709, 149],
  "Calcutta": [356, 57],
  "Delhi": [460, 74],
  "Hyderabad": [2, 0],
  "Kanpur": [3, 33],
  "Madras": [209, 52],
  "TOTAL (CITIES)": [1934, 432],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1113],
  "Assam": [None, None, 192],
  "Bihar": [None, None, 368],
  "Gujarat": [None, None, 655],
  "Haryana": [None, None, 327],
  "Himachal Pradesh": [None, None, 104],
  "Jammu & Kashmir": [None, None, 151],
  "Karnataka": [None, None, 1286],
  "Kerala": [None, None, 407],
  "Madhya Pradesh": [None, None, 1622],
  "Maharashtra": [None, None, 1608],
  "Manipur": [None, None, 8],
  "Meghalaya": [None, None, 16],
  "Nagaland": [None, None, 8],
  "Orissa": [None, None, 268],
  "Punjab": [None, None, 332],
  "Rajasthan": [None, None, 477],
  "Sikkim": [None, None, 18],
  "Tamil Nadu": [None, None, 1872],
  "Tripura": [None, None, 48],
  "Uttar Pradesh": [None, None, 2109],
  "West Bengal": [None, None, 1485],
  "TOTAL (STATES)": [None, None, 14474],
 },
 "U.Ts.": {
  "A.&N. Islands": [None, None, 2],
  "Arunachal Pradesh": [None, None, 17],
  "Chandigarh": [None, None, 34],
  "D. & N. Haveli": [None, None, 1],
  "Delhi": [None, None, 585],
  "Goa, Daman & Diu": [None, None, 14],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 24],
  "Pondicherry": [None, None, 39],
  "TOTAL (U.TS.)": [None, None, 716],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 15190],
 },
 "Cities": {
  "Ahmedabad": [None, None, 32],
  "Bangalore": [None, None, 230],
  "Bombay": [None, None, 858],
  "Calcutta": [None, None, 413],
  "Delhi": [None, None, 534],
  "Hyderabad": [None, None, 2],
  "Kanpur": [None, None, 36],
  "Madras": [None, None, 261],
  "TOTAL (CITIES)": [None, None, 2366],
 },
}
