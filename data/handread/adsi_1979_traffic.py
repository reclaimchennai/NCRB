# ADSI 1979, Appendix II (raw/adsi/1979/table_content/appendix-2_1979.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1979, "adsi"
SOURCE = "raw/adsi/1979/table_content/appendix-2_1979.pdf"
PAGES = "1-2"
TITLE = "Appendix II: State-wise distribution of accidental deaths due to other causes during 1979 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [1681, 274],
  "Assam": [92, 5],
  "Bihar": [312, 106],
  "Gujarat": [255, 68],
  "Haryana": [341, 112],
  "Himachal Pradesh": [86, 13],
  "Jammu & Kashmir": [106, 16],
  "Karnataka": [1168, 233],
  "Kerala": [443, 125],
  "Madhya Pradesh": [1048, 388],
  "Maharashtra": [1643, 320],
  "Manipur": [51, 3],
  "Meghalaya": [22, 4],
  "Nagaland": [16, 4],
  "Orissa": [444, 41],
  "Punjab": [471, 94],
  "Rajasthan": [547, 103],
  "Sikkim": [18, 6],
  "Tamil Nadu": [1726, 477],
  "Tripura": [29, 1],
  "Uttar Pradesh": [2232, 423],
  "West Bengal": [1498, 361],
  "TOTAL (STATES)": [14229, 3177],
 },
 "U.Ts.": {
  "A. & N. Islands": [6, 0],
  "Arunachal Pradesh": [10, 0],
  "Chandigarh": [11, 0],
  "D. & N. Haveli": [0, 0],
  "Delhi": [596, 69],
  "Goa, Daman & Diu": [89, 22],
  "Lakshadweep": [0, 0],
  "Mizoram": [27, 5],
  "Pondicherry": [30, 2],
  "TOTAL (U.TS.)": [769, 98],
 },
 "Grand": {
  "GRAND TOTAL": [14998, 3275],
 },
 "Cities": {
  "Ahmedabad": [21, 2],
  "Bangalore": [122, 35],
  "Bombay": [942, 161],
  "Calcutta": [314, 81],
  "Delhi": [532, 53],
  "Hyderabad": [193, 37],
  "Kanpur": [25, 31],
  "Madras": [171, 46],
  "TOTAL (CITIES)": [2320, 446],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1955],
  "Assam": [None, None, 97],
  "Bihar": [None, None, 418],
  "Gujarat": [None, None, 323],
  "Haryana": [None, None, 453],
  "Himachal Pradesh": [None, None, 99],
  "Jammu & Kashmir": [None, None, 122],
  "Karnataka": [None, None, 1401],
  "Kerala": [None, None, 568],
  "Madhya Pradesh": [None, None, 1436],
  "Maharashtra": [None, None, 1963],
  "Manipur": [None, None, 54],
  "Meghalaya": [None, None, 26],
  "Nagaland": [None, None, 20],
  "Orissa": [None, None, 485],
  "Punjab": [None, None, 565],
  "Rajasthan": [None, None, 650],
  "Sikkim": [None, None, 24],
  "Tamil Nadu": [None, None, 2203],
  "Tripura": [None, None, 30],
  "Uttar Pradesh": [None, None, 2655],
  "West Bengal": [None, None, 1859],
  "TOTAL (STATES)": [None, None, 17406],
 },
 "U.Ts.": {
  "A. & N. Islands": [None, None, 6],
  "Arunachal Pradesh": [None, None, 10],
  "Chandigarh": [None, None, 11],
  "D. & N. Haveli": [None, None, 0],
  "Delhi": [None, None, 665],
  "Goa, Daman & Diu": [None, None, 111],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 32],
  "Pondicherry": [None, None, 32],
  "TOTAL (U.TS.)": [None, None, 867],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 18273],
 },
 "Cities": {
  "Ahmedabad": [None, None, 23],
  "Bangalore": [None, None, 157],
  "Bombay": [None, None, 1103],
  "Calcutta": [None, None, 395],
  "Delhi": [None, None, 585],
  "Hyderabad": [None, None, 230],
  "Kanpur": [None, None, 56],
  "Madras": [None, None, 217],
  "TOTAL (CITIES)": [None, None, 2766],
 },
}
