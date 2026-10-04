# ADSI 1978, Appendix II (raw/adsi/1978/table_content/appendix-2_1978.pdf, pages 1-3). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1978, "adsi"
SOURCE = "raw/adsi/1978/table_content/appendix-2_1978.pdf"
PAGES = "1-3"
TITLE = "Appendix II: State-wise distribution of accidental deaths due to other causes during 1978 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [1355, 251],
  "Assam": [290, 41],
  "Bihar": [254, 74],
  "Gujarat": [176, 32],
  "Haryana": [297, 87],
  "Himachal Pradesh": [104, 9],
  "Jammu & Kashmir": [54, 12],
  "Karnataka": [1046, 325],
  "Kerala": [388, 75],
  "Madhya Pradesh": [1568, 459],
  "Maharashtra": [1396, 324],
  "Manipur": [36, 10],
  "Meghalaya": [45, 5],
  "Nagaland": [20, 0],
  "Orissa": [310, 44],
  "Punjab": [394, 64],
  "Rajasthan": [427, 106],
  "Sikkim": [16, 3],
  "Tamil Nadu": [1613, 374],
  "Tripura": [24, 3],
  "Uttar Pradesh": [2348, 444],
  "West Bengal": [1468, 381],
  "TOTAL (STATES)": [13629, 3123],
 },
 "U.Ts.": {
  "A. & N. Islands": [3, 0],
  "Arunachal Pradesh": [20, 2],
  "Chandigarh": [12, 1],
  "D. & N. Haveli": [2, 2],
  "Delhi": [594, 112],
  "Goa, Daman & Diu": [87, 25],
  "Lakshadweep": [0, 0],
  "Mizoram": [18, 3],
  "Pondicherry": [24, 3],
  "TOTAL (U.TS.)": [760, 148],
 },
 "Grand": {
  "GRAND TOTAL": [14389, 3271],
 },
 "Cities": {
  "Ahmedabad": [25, 4],
  "Bangalore": [171, 43],
  "Bombay": [716, 152],
  "Calcutta": [318, 55],
  "Delhi": [544, 101],
  "Hyderabad": [2, 0],
  "Kanpur": [62, 11],
  "Madras": [173, 52],
  "TOTAL (CITIES)": [2011, 418],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1606],
  "Assam": [None, None, 331],
  "Bihar": [None, None, 328],
  "Gujarat": [None, None, 208],
  "Haryana": [None, None, 384],
  "Himachal Pradesh": [None, None, 113],
  "Jammu & Kashmir": [None, None, 66],
  "Karnataka": [None, None, 1371],
  "Kerala": [None, None, 463],
  "Madhya Pradesh": [None, None, 2027],
  "Maharashtra": [None, None, 1720],
  "Manipur": [None, None, 46],
  "Meghalaya": [None, None, 50],
  "Nagaland": [None, None, 20],
  "Orissa": [None, None, 354],
  "Punjab": [None, None, 458],
  "Rajasthan": [None, None, 533],
  "Sikkim": [None, None, 19],
  "Tamil Nadu": [None, None, 1987],
  "Tripura": [None, None, 27],
  "Uttar Pradesh": [None, None, 2792],
  "West Bengal": [None, None, 1849],
  "TOTAL (STATES)": [None, None, 16752],
 },
 "U.Ts.": {
  "A. & N. Islands": [None, None, 3],
  "Arunachal Pradesh": [None, None, 22],
  "Chandigarh": [None, None, 13],
  "D. & N. Haveli": [None, None, 4],
  "Delhi": [None, None, 706],
  "Goa, Daman & Diu": [None, None, 112],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 21],
  "Pondicherry": [None, None, 27],
  "TOTAL (U.TS.)": [None, None, 908],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 17660],
 },
 "Cities": {
  "Ahmedabad": [None, None, 29],
  "Bangalore": [None, None, 214],
  "Bombay": [None, None, 868],
  "Calcutta": [None, None, 373],
  "Delhi": [None, None, 645],
  "Hyderabad": [None, None, 2],
  "Kanpur": [None, None, 73],
  "Madras": [None, None, 225],
  "TOTAL (CITIES)": [None, None, 2429],
 },
}
