# ADSI 1968, Appendix II (raw/adsi/1968/table_content/appendix-2_1968.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1968, "adsi"
SOURCE = "raw/adsi/1968/table_content/appendix-2_1968.pdf"
PAGES = "1-2"
TITLE = "Appendix II: Statement of number of accidental deaths in States/U.Ts./Cities during 1968 (Other causes, Part II: On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [353, 82],
  "Assam": [88, 14],
  "Bihar": [138, 30],
  "Gujarat": [121, 25],
  "Haryana": [81, 32],
  "Jammu & Kashmir": [98, 14],
  "Kerala": [104, 27],
  "Madhya Pradesh": [416, 119],
  "Maharashtra": [612, 122],
  "Mysore": [215, 86],
  "Nagaland": [2, 0],
  "Orissa": [35, 10],
  "Punjab": [165, 16],
  "Rajasthan": [228, 50],
  "Tamil Nadu": [482, 175],
  "Uttar Pradesh": [1114, 201],
  "West Bengal": [463, 105],
  "TOTAL (STATES)": [4715, 1108],
 },
 "U.Ts.": {
  "A & N Islands": [1, 0],
  "Chandigarh": [7, 1],
  "Dadra & Nagar Haveli": [0, 0],
  "Delhi": [197, 30],
  "Goa, Daman & Diu": [19, 4],
  "Himachal Pradesh": [55, 3],
  "Laccadives": [0, 0],
  "Manipur": [8, 0],
  "Pondicherry": [3, 0],
  "Tripura": [0, 1],
  "TOTAL (U.TS.)": [290, 39],
 },
 "Grand": {
  "GRAND TOTAL": [5005, 1147],
 },
 "Cities": {
  "Ahmedabad": [9, 1],
  "Bangalore": [38, 9],
  "Bombay": [364, 77],
  "Calcutta": [67, 14],
  "Delhi": [162, 27],
  "Hyderabad": [5, 0],
  "Kanpur": [49, 4],
  "Madras": [120, 41],
  "TOTAL (CITIES)": [814, 173],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 435],
  "Assam": [None, None, 102],
  "Bihar": [None, None, 168],
  "Gujarat": [None, None, 146],
  "Haryana": [None, None, 113],
  "Jammu & Kashmir": [None, None, 112],
  "Kerala": [None, None, 131],
  "Madhya Pradesh": [None, None, 535],
  "Maharashtra": [None, None, 734],
  "Mysore": [None, None, 301],
  "Nagaland": [None, None, 2],
  "Orissa": [None, None, 45],
  "Punjab": [None, None, 181],
  "Rajasthan": [None, None, 278],
  "Tamil Nadu": [None, None, 657],
  "Uttar Pradesh": [None, None, 1315],
  "West Bengal": [None, None, 568],
  "TOTAL (STATES)": [None, None, 5823],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 1],
  "Chandigarh": [None, None, 8],
  "Dadra & Nagar Haveli": [None, None, 0],
  "Delhi": [None, None, 227],
  "Goa, Daman & Diu": [None, None, 23],
  "Himachal Pradesh": [None, None, 58],
  "Laccadives": [None, None, 0],
  "Manipur": [None, None, 8],
  "Pondicherry": [None, None, 3],
  "Tripura": [None, None, 1],
  "TOTAL (U.TS.)": [None, None, 329],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 6152],
 },
 "Cities": {
  "Ahmedabad": [None, None, 10],
  "Bangalore": [None, None, 47],
  "Bombay": [None, None, 441],
  "Calcutta": [None, None, 81],
  "Delhi": [None, None, 189],
  "Hyderabad": [None, None, 5],
  "Kanpur": [None, None, 53],
  "Madras": [None, None, 161],
  "TOTAL (CITIES)": [None, None, 987],
 },
}
