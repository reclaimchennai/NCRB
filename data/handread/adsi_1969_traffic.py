# ADSI 1969, Appendix II (raw/adsi/1969/table_content/appendix-2_1969.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1969, "adsi"
SOURCE = "raw/adsi/1969/table_content/appendix-2_1969.pdf"
PAGES = "1-2"
TITLE = "Appendix II: Statement of number of accidental deaths in different States/U.Ts./Cities during the year 1969 (by other causes: On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [379, 74],
  "Assam": [157, 20],
  "Bihar": [238, 75],
  "Gujarat": [101, 32],
  "Haryana": [119, 35],
  "Jammu & Kashmir": [36, 8],
  "Kerala": [115, 24],
  "Madhya Pradesh": [455, 85],
  "Maharashtra": [615, 132],
  "Mysore": [320, 72],
  "Nagaland": [18, 0],
  "Orissa": [28, 9],
  "Punjab": [145, 31],
  "Rajasthan": [466, 102],
  "Tamil Nadu": [565, 171],
  "Uttar Pradesh": [1289, 190],
  "West Bengal": [592, 154],
  "TOTAL (STATES)": [5638, 1214],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [3, 0],
  "Chandigarh": [4, 0],
  "Dadra & Nagar Haveli": [1, 0],
  "Delhi": [112, 9],
  "Goa, Daman & Diu": [11, 1],
  "Himachal Pradesh": [54, 5],
  "Laccadives": [0, 0],
  "Manipur": [3, 1],
  "Pondicherry": [5, 1],
  "Tripura": [6, 3],
  "TOTAL (U.TS.)": [199, 20],
 },
 "Grand": {
  "GRAND TOTAL": [5837, 1234],
 },
 "Cities": {
  "Ahmedabad": [9, 0],
  "Bangalore": [41, 11],
  "Bombay": [343, 70],
  "Calcutta": [296, 71],
  "Delhi": [91, 9],
  "Hyderabad": [5, 1],
  "Kanpur": [65, 10],
  "Madras": [123, 45],
  "TOTAL (CITIES)": [973, 217],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 453],
  "Assam": [None, None, 177],
  "Bihar": [None, None, 313],
  "Gujarat": [None, None, 133],
  "Haryana": [None, None, 154],
  "Jammu & Kashmir": [None, None, 44],
  "Kerala": [None, None, 139],
  "Madhya Pradesh": [None, None, 540],
  "Maharashtra": [None, None, 747],
  "Mysore": [None, None, 392],
  "Nagaland": [None, None, 18],
  "Orissa": [None, None, 37],
  "Punjab": [None, None, 176],
  "Rajasthan": [None, None, 568],
  "Tamil Nadu": [None, None, 736],
  "Uttar Pradesh": [None, None, 1479],
  "West Bengal": [None, None, 746],
  "TOTAL (STATES)": [None, None, 6852],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [None, None, 3],
  "Chandigarh": [None, None, 4],
  "Dadra & Nagar Haveli": [None, None, 1],
  "Delhi": [None, None, 121],
  "Goa, Daman & Diu": [None, None, 12],
  "Himachal Pradesh": [None, None, 59],
  "Laccadives": [None, None, 0],
  "Manipur": [None, None, 4],
  "Pondicherry": [None, None, 6],
  "Tripura": [None, None, 9],
  "TOTAL (U.TS.)": [None, None, 219],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 7071],
 },
 "Cities": {
  "Ahmedabad": [None, None, 9],
  "Bangalore": [None, None, 52],
  "Bombay": [None, None, 413],
  "Calcutta": [None, None, 367],
  "Delhi": [None, None, 100],
  "Hyderabad": [None, None, 6],
  "Kanpur": [None, None, 75],
  "Madras": [None, None, 168],
  "TOTAL (CITIES)": [None, None, 1190],
 },
}
