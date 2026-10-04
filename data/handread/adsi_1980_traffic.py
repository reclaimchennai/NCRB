# ADSI 1980, Appendix II (raw/adsi/1980/table_content/appendix-2_1980.pdf, pages 1-3). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1980, "adsi"
SOURCE = "raw/adsi/1980/table_content/appendix-2_1980.pdf"
PAGES = "1-3"
TITLE = "Appendix II: State-wise distribution of accidental deaths due to other causes during 1980 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [1181, 254],
  "Assam": [118, 29],
  "Bihar": [297, 90],
  "Gujarat": [290, 68],
  "Haryana": [291, 61],
  "Himachal Pradesh": [109, 8],
  "Jammu & Kashmir": [149, 19],
  "Karnataka": [1047, 291],
  "Kerala": [554, 104],
  "Madhya Pradesh": [1151, 399],
  "Maharashtra": [1437, 333],
  "Manipur": [31, 3],
  "Meghalaya": [38, 4],
  "Nagaland": [12, 0],
  "Orissa": [397, 58],
  "Punjab": [419, 83],
  "Rajasthan": [694, 90],
  "Sikkim": [19, 4],
  "Tamil Nadu": [1663, 388],
  "Tripura": [51, 3],
  "Uttar Pradesh": [2262, 443],
  "West Bengal": [1559, 374],
  "TOTAL (STATES)": [13769, 3106],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [10, 1],
  "Arunachal Pradesh": [6, 1],
  "Chandigarh": [16, 1],
  "Dadra & Nagar Haveli": [1, 3],
  "Delhi": [352, 62],
  "Goa, Daman & Diu": [73, 18],
  "Lakshadweep": [0, 0],
  "Mizoram": [13, 0],
  "Pondicherry": [44, 5],
  "TOTAL (U.TS.)": [515, 91],
 },
 "Grand": {
  "GRAND TOTAL": [14284, 3197],
 },
 "Cities": {
  "Ahmedabad": [20, 6],
  "Bangalore": [170, 35],
  "Bombay": [772, 164],
  "Calcutta": [322, 51],
  "Delhi": [292, 57],
  "Hyderabad": [169, 34],
  "Kanpur": [44, 6],
  "Madras": [11, 31],
  "TOTAL (CITIES)": [1800, 384],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1435],
  "Assam": [None, None, 147],
  "Bihar": [None, None, 387],
  "Gujarat": [None, None, 358],
  "Haryana": [None, None, 352],
  "Himachal Pradesh": [None, None, 117],
  "Jammu & Kashmir": [None, None, 168],
  "Karnataka": [None, None, 1338],
  "Kerala": [None, None, 658],
  "Madhya Pradesh": [None, None, 1550],
  "Maharashtra": [None, None, 1770],
  "Manipur": [None, None, 34],
  "Meghalaya": [None, None, 42],
  "Nagaland": [None, None, 12],
  "Orissa": [None, None, 455],
  "Punjab": [None, None, 502],
  "Rajasthan": [None, None, 784],
  "Sikkim": [None, None, 23],
  "Tamil Nadu": [None, None, 2051],
  "Tripura": [None, None, 54],
  "Uttar Pradesh": [None, None, 2705],
  "West Bengal": [None, None, 1933],
  "TOTAL (STATES)": [None, None, 16875],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [None, None, 11],
  "Arunachal Pradesh": [None, None, 7],
  "Chandigarh": [None, None, 17],
  "Dadra & Nagar Haveli": [None, None, 4],
  "Delhi": [None, None, 414],
  "Goa, Daman & Diu": [None, None, 91],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 13],
  "Pondicherry": [None, None, 49],
  "TOTAL (U.TS.)": [None, None, 606],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 17481],
 },
 "Cities": {
  "Ahmedabad": [None, None, 26],
  "Bangalore": [None, None, 205],
  "Bombay": [None, None, 936],
  "Calcutta": [None, None, 373],
  "Delhi": [None, None, 349],
  "Hyderabad": [None, None, 203],
  "Kanpur": [None, None, 50],
  "Madras": [None, None, 42],
  "TOTAL (CITIES)": [None, None, 2184],
 },
}
