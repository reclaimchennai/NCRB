# ADSI 1967, Appendix II (raw/adsi/1967/table_content/appendix-2_1967.pdf, pages 1-2). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
# In 1967 Himachal Pradesh, Manipur and Tripura are printed among the Union Territories.
KIND, YEAR, PUB = "traffic", 1967, "adsi"
SOURCE = "raw/adsi/1967/table_content/appendix-2_1967.pdf"
PAGES = "1-2"
TITLE = "Appendix II: Statement of unnatural deaths other than homicide, 1967 (Other causes: Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [323, 51],
  "Assam": [135, 13],
  "Bihar": [178, 48],
  "Gujarat": [124, 34],
  "Haryana": [157, 26],
  "Jammu & Kashmir": [62, 6],
  "Kerala": [85, 9],
  "Madhya Pradesh": [419, 89],
  "Maharashtra": [606, 110],
  "Mysore": [285, 32],
  "Nagaland": [2, 0],
  "Orissa": [59, 6],
  "Punjab": [150, 60],
  "Rajasthan": [329, 76],
  "Tamil Nadu": [579, 170],
  "Uttar Pradesh": [958, 159],
  "West Bengal": [533, 142],
  "TOTAL (STATES)": [4984, 1031],
 },
 "U.Ts.": {
  "A & N Islands": [1, 0],
  "Chandigarh": [3, 1],
  "Dadra & N. H.": [2, 0],
  "Delhi": [86, 9],
  "Goa, Daman & Diu": [11, 4],
  "Himachal Pradesh": [37, 0],
  "Laccadives": [0, 0],
  "Manipur": [2, 0],
  "Pondicherry": [0, 2],
  "Tripura": [0, 0],
  "TOTAL (U.TS.)": [142, 16],
 },
 "Grand": {
  "GRAND TOTAL": [5126, 1047],
 },
 "Cities": {
  "Ahmedabad": [20, 1],
  "Bangalore": [77, 12],
  "Bombay": [371, 63],
  "Calcutta": [225, 48],
  "Delhi": [73, 8],
  "Hyderabad": [11, 3],
  "Kanpur": [7, 0],
  "Madras": [115, 37],
  "TOTAL (CITIES)": [899, 172],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 374],
  "Assam": [None, None, 148],
  "Bihar": [None, None, 226],
  "Gujarat": [None, None, 158],
  "Haryana": [None, None, 183],
  "Jammu & Kashmir": [None, None, 68],
  "Kerala": [None, None, 94],
  "Madhya Pradesh": [None, None, 508],
  "Maharashtra": [None, None, 716],
  "Mysore": [None, None, 317],
  "Nagaland": [None, None, 2],
  "Orissa": [None, None, 65],
  "Punjab": [None, None, 210],
  "Rajasthan": [None, None, 405],
  "Tamil Nadu": [None, None, 749],
  "Uttar Pradesh": [None, None, 1117],
  "West Bengal": [None, None, 675],
  "TOTAL (STATES)": [None, None, 6015],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 1],
  "Chandigarh": [None, None, 4],
  "Dadra & N. H.": [None, None, 2],
  "Delhi": [None, None, 95],
  "Goa, Daman & Diu": [None, None, 15],
  "Himachal Pradesh": [None, None, 37],
  "Laccadives": [None, None, 0],
  "Manipur": [None, None, 2],
  "Pondicherry": [None, None, 2],
  "Tripura": [None, None, 0],
  "TOTAL (U.TS.)": [None, None, 158],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 6173],
 },
 "Cities": {
  "Ahmedabad": [None, None, 21],
  "Bangalore": [None, None, 89],
  "Bombay": [None, None, 434],
  "Calcutta": [None, None, 273],
  "Delhi": [None, None, 81],
  "Hyderabad": [None, None, 14],
  "Kanpur": [None, None, 7],
  "Madras": [None, None, 152],
  "TOTAL (CITIES)": [None, None, 1071],
 },
}
