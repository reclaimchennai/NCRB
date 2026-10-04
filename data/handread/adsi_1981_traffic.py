# ADSI 1981, Appendix II (raw/adsi/1981/table_content/appendix-2_1881.pdf, pages 1-4). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
KIND, YEAR, PUB = "traffic", 1981, "adsi"
SOURCE = "raw/adsi/1981/table_content/appendix-2_1881.pdf"
PAGES = "1-4"
TITLE = "Appendix II: Statewise distribution of accidental deaths due to other causes during 1981 (On Roads, by sex)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {("Delhi", "Persons killed"): (760, 770, "U.T. Delhi: Male deaths on roads printed 650; 660 makes the U.T. column add to its printed Total (U.Ts.) 818 and the Grand Total 16851, and equals the row's own Motor Vehicle (644) + Other Road (16) male deaths")}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "States": {
  "Andhra Pradesh": [1258, 244],
  "Assam": [155, 47],
  "Bihar": [458, 97],
  "Gujarat": [488, 106],
  "Haryana": [273, 69],
  "Himachal Pradesh": [184, 29],
  "Jammu & Kashmir": [138, 9],
  "Karnataka": [1158, 222],
  "Kerala": [452, 94],
  "Madhya Pradesh": [1578, 528],
  "Maharashtra": [2128, 323],
  "Manipur": [33, 6],
  "Meghalaya": [37, 1],
  "Nagaland": [52, 8],
  "Orissa": [418, 74],
  "Punjab": [531, 89],
  "Rajasthan": [812, 168],
  "Sikkim": [58, 19],
  "Tamil Nadu": [2241, 595],
  "Tripura": [45, 8],
  "Uttar Pradesh": [2432, 517],
  "West Bengal": [1104, 316],
  "TOTAL (STATES)": [16033, 3569],
 },
 "U.Ts.": {
  "A & N Islands": [7, 1],
  "Arunachal Pradesh": [19, 5],
  "Chandigarh": [16, 2],
  "D & N Haveli": [1, 0],
  "Delhi": [660, 110],
  "Goa, Daman & Diu": [59, 14],
  "Lakshadweep": [0, 0],
  "Mizoram": [24, 23],
  "Pondicherry": [32, 3],
  "TOTAL (U.TS.)": [818, 158],
 },
 "Grand": {
  "GRAND TOTAL": [16851, 3727],
 },
 "Cities": {
  "Ahmedabad": [19, 6],
  "Bangalore": [181, 40],
  "Bombay": [1409, 168],
  "Calcutta": [368, 70],
  "Delhi": [536, 92],
  "Hyderabad": [94, 9],
  "Jaipur": [60, 5],
  "Kanpur": [22, 23],
  "Lucknow": [95, 12],
  "Madras": [307, 57],
  "Nagpur": [45, 10],
  "Pune": [115, 16],
  "TOTAL (CITIES)": [3251, 508],
 },
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 1502],
  "Assam": [None, None, 202],
  "Bihar": [None, None, 555],
  "Gujarat": [None, None, 594],
  "Haryana": [None, None, 342],
  "Himachal Pradesh": [None, None, 213],
  "Jammu & Kashmir": [None, None, 147],
  "Karnataka": [None, None, 1380],
  "Kerala": [None, None, 546],
  "Madhya Pradesh": [None, None, 2106],
  "Maharashtra": [None, None, 2451],
  "Manipur": [None, None, 39],
  "Meghalaya": [None, None, 38],
  "Nagaland": [None, None, 60],
  "Orissa": [None, None, 492],
  "Punjab": [None, None, 620],
  "Rajasthan": [None, None, 980],
  "Sikkim": [None, None, 77],
  "Tamil Nadu": [None, None, 2836],
  "Tripura": [None, None, 53],
  "Uttar Pradesh": [None, None, 2949],
  "West Bengal": [None, None, 1420],
  "TOTAL (STATES)": [None, None, 19602],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 8],
  "Arunachal Pradesh": [None, None, 24],
  "Chandigarh": [None, None, 18],
  "D & N Haveli": [None, None, 1],
  "Delhi": [None, None, 770],
  "Goa, Daman & Diu": [None, None, 73],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 47],
  "Pondicherry": [None, None, 35],
  "TOTAL (U.TS.)": [None, None, 976],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 20578],
 },
 "Cities": {
  "Ahmedabad": [None, None, 25],
  "Bangalore": [None, None, 221],
  "Bombay": [None, None, 1577],
  "Calcutta": [None, None, 438],
  "Delhi": [None, None, 628],
  "Hyderabad": [None, None, 103],
  "Jaipur": [None, None, 65],
  "Kanpur": [None, None, 45],
  "Lucknow": [None, None, 107],
  "Madras": [None, None, 364],
  "Nagpur": [None, None, 55],
  "Pune": [None, None, 131],
  "TOTAL (CITIES)": [None, None, 3759],
 },
}
