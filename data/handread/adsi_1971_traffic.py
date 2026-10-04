# ADSI 1971, Appendix II (raw/adsi/1971/table_content/appendix-2_1971.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1971, "adsi"
SOURCE = "raw/adsi/1971/table_content/appendix-2_1971.pdf"
PAGES = "1-2"
TITLE = "Appendix II: Statement of number of accidental deaths in States/Union Territories/Cities during 1971 (other causes, Part II: On Roads, Total road accidents, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [709, 217],
  "Assam": [89, 18],
  "Bihar": [348, 107],
  "Gujarat": [250, 43],
  "Haryana": [167, 27],
  "Himachal Pradesh": [115, 14],
  "Jammu & Kashmir": [25, 5],
  "Karnataka": [769, 149],
  "Kerala": [566, 70],
  "Madhya Pradesh": [785, 202],
  "Maharashtra": [1142, 208],
  "Manipur": [4, 1],
  "Nagaland": [4, 0],
  "Orissa": [130, 18],
  "Punjab": [230, 29],
  "Rajasthan": [431, 53],
  "Tamil Nadu": [981, 268],
  "Tripura": [18, 3],
  "Uttar Pradesh": [1743, 310],
  "West Bengal": [1084, 217],
  "TOTAL (STATES)": [9590, 1959],
 },
 "U.Ts.": {
  "A. & N. Islands": [8, 1],
  "Chandigarh": [6, 2],
  "Dadra & Nagar Haveli": [0, 0],
  "Delhi": [112, 16],
  "Goa, Daman & Diu": [24, 6],
  "Lakshadweep": [0, 0],
  "Pondicherry": [14, 2],
  "TOTAL (U.TS.)": [164, 27],
 },
 "Grand": {
  "GRAND TOTAL": [9754, 1986],
 },
 "Cities": {
  "Ahmedabad": [20, 2],
  "Bangalore": [124, 21],
  "Bombay": [548, 99],
  "Calcutta": [373, 61],
  "Delhi": [94, 15],
  "Hyderabad": [81, 12],
  "Kanpur": [67, 9],
  "Madras": [142, 42],
  "TOTAL (CITIES)": [1449, 261],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 926],
  "Assam": [None, None, 107],
  "Bihar": [None, None, 455],
  "Gujarat": [None, None, 293],
  "Haryana": [None, None, 194],
  "Himachal Pradesh": [None, None, 129],
  "Jammu & Kashmir": [None, None, 30],
  "Karnataka": [None, None, 918],
  "Kerala": [None, None, 636],
  "Madhya Pradesh": [None, None, 987],
  "Maharashtra": [None, None, 1350],
  "Manipur": [None, None, 5],
  "Nagaland": [None, None, 4],
  "Orissa": [None, None, 148],
  "Punjab": [None, None, 259],
  "Rajasthan": [None, None, 484],
  "Tamil Nadu": [None, None, 1249],
  "Tripura": [None, None, 21],
  "Uttar Pradesh": [None, None, 2053],
  "West Bengal": [None, None, 1301],
  "TOTAL (STATES)": [None, None, 11549],
 },
 "U.Ts.": {
  "A. & N. Islands": [None, None, 9],
  "Chandigarh": [None, None, 8],
  "Dadra & Nagar Haveli": [None, None, 0],
  "Delhi": [None, None, 128],
  "Goa, Daman & Diu": [None, None, 30],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 16],
  "TOTAL (U.TS.)": [None, None, 191],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 11740],
 },
 "Cities": {
  "Ahmedabad": [None, None, 22],
  "Bangalore": [None, None, 145],
  "Bombay": [None, None, 647],
  "Calcutta": [None, None, 434],
  "Delhi": [None, None, 109],
  "Hyderabad": [None, None, 93],
  "Kanpur": [None, None, 76],
  "Madras": [None, None, 184],
  "TOTAL (CITIES)": [None, None, 1710],
 },
}
