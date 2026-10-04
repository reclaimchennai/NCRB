# ADSI 1973, Appendix II (raw/adsi/1973/table_content/appendix-2_1973.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1973, "adsi"
SOURCE = "raw/adsi/1973/table_content/appendix-2_1973.pdf"
PAGES = "1-2"
TITLE = "Appendix II: Statewise distribution of accidental deaths due to other causes during 1973 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [851, 182],
  "Assam": [143, 19],
  "Bihar": [298, 41],
  "Gujarat": [156, 44],
  "Haryana": [234, 55],
  "Himachal Pradesh": [93, 4],
  "Jammu & Kashmir": [159, 40],
  "Karnataka": [670, 156],
  "Kerala": [234, 33],
  "Madhya Pradesh": [984, 325],
  "Maharashtra": [1278, 248],
  "Manipur": [10, 2],
  "Meghalaya": [23, 4],
  "Nagaland": [1, 0],
  "Orissa": [160, 32],
  "Punjab": [294, 54],
  "Rajasthan": [490, 92],
  "Tamil Nadu": [1269, 263],
  "Tripura": [19, 3],
  "Uttar Pradesh": [1870, 186],
  "West Bengal": [1166, 255],
  "TOTAL (STATES)": [10402, 2038],
 },
 "U.Ts.": {
  "A.&N. Islands": [5, 0],
  "Arunachal Pradesh": [9, 1],
  "Chandigarh": [13, 1],
  "Dadra & Nagar Haveli": [0, 0],
  "Delhi": [524, 42],
  "Goa, Daman & Diu": [15, 3],
  "Lakshadweep": [0, 0],
  "Mizoram": [2, 0],
  "Pondicherry": [26, 9],
  "TOTAL (U.TS.)": [594, 56],
 },
 "Grand": {
  "GRAND TOTAL": [10996, 2094],
 },
 "Cities": {
  "Ahmedabad": [29, 5],
  "Bangalore": [113, 23],
  "Bombay": [683, 116],
  "Calcutta": [443, 44],
  "Delhi": [483, 37],
  "Hyderabad": [0, 0],
  "Kanpur": [1, 10],
  "Madras": [188, 42],
  "TOTAL (CITIES)": [1940, 277],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1033],
  "Assam": [None, None, 162],
  "Bihar": [None, None, 339],
  "Gujarat": [None, None, 200],
  "Haryana": [None, None, 289],
  "Himachal Pradesh": [None, None, 97],
  "Jammu & Kashmir": [None, None, 199],
  "Karnataka": [None, None, 826],
  "Kerala": [None, None, 267],
  "Madhya Pradesh": [None, None, 1309],
  "Maharashtra": [None, None, 1526],
  "Manipur": [None, None, 12],
  "Meghalaya": [None, None, 27],
  "Nagaland": [None, None, 1],
  "Orissa": [None, None, 192],
  "Punjab": [None, None, 348],
  "Rajasthan": [None, None, 582],
  "Tamil Nadu": [None, None, 1532],
  "Tripura": [None, None, 22],
  "Uttar Pradesh": [None, None, 2056],
  "West Bengal": [None, None, 1421],
  "TOTAL (STATES)": [None, None, 12440],
 },
 "U.Ts.": {
  "A.&N. Islands": [None, None, 5],
  "Arunachal Pradesh": [None, None, 10],
  "Chandigarh": [None, None, 14],
  "Dadra & Nagar Haveli": [None, None, 0],
  "Delhi": [None, None, 566],
  "Goa, Daman & Diu": [None, None, 18],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 2],
  "Pondicherry": [None, None, 35],
  "TOTAL (U.TS.)": [None, None, 650],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 13090],
 },
 "Cities": {
  "Ahmedabad": [None, None, 34],
  "Bangalore": [None, None, 136],
  "Bombay": [None, None, 799],
  "Calcutta": [None, None, 487],
  "Delhi": [None, None, 520],
  "Hyderabad": [None, None, 0],
  "Kanpur": [None, None, 11],
  "Madras": [None, None, 230],
  "TOTAL (CITIES)": [None, None, 2217],
 },
}
