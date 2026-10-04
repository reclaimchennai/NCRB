# ADSI 1987, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1987/table_content/appendix-2.pdf, pages 1-2).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'On Roads' (road accident deaths) Male and Female columns; the table prints no Total, so Persons killed = Male + Female and every Male and every Female column was first checked against the printed Total (States), Total (UTs), Grand Total and Total (Cities).
# Road accidents (cases) and Persons injured are None (not printed).
KIND, YEAR, PUB = "traffic", 1987, "adsi"
SOURCE = "raw/adsi/1987/table_content/appendix-2.pdf"
PAGES = "1-2"
TITLE = "Appendix II: State-wise Distribution of Accidental Deaths due to Other Causes during 1987"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 2788],
  "Arunachal Pradesh": [None, None, 117],
  "Assam": [None, None, 757],
  "Bihar": [None, None, 1406],
  "Goa": [None, None, 94],
  "Gujarat": [None, None, 514],
  "Haryana": [None, None, 623],
  "Himachal Pradesh": [None, None, 422],
  "Jammu & Kashmir": [None, None, 483],
  "Karnataka": [None, None, 2242],
  "Kerala": [None, None, 1634],
  "Madhya Pradesh": [None, None, 2997],
  "Maharashtra": [None, None, 2381],
  "Manipur": [None, None, 65],
  "Meghalaya": [None, None, 57],
  "Mizoram": [None, None, 51],
  "Nagaland": [None, None, 25],
  "Orissa": [None, None, 1091],
  "Punjab": [None, None, 521],
  "Rajasthan": [None, None, 1115],
  "Sikkim": [None, None, 30],
  "Tamil Nadu": [None, None, 5260],
  "Tripura": [None, None, 14],
  "Uttar Pradesh": [None, None, 4973],
  "West Bengal": [None, None, 2748],
  "TOTAL (STATES)": [None, None, 32408],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 4],
  "Chandigarh": [None, None, 44],
  "D & N Haveli": [None, None, 0],
  "Daman & Diu": [None, None, 1],
  "Delhi": [None, None, 1353],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 74],
  "TOTAL (U.TS.)": [None, None, 1476],
 },
 "Cities": {
  "Ahmedabad": [None, None, 24],
  "Bangalore": [None, None, 301],
  "Bombay": [None, None, 1178],
  "Calcutta": [None, None, 439],
  "Delhi": [None, None, 909],
  "Hyderabad": [None, None, 148],
  "Jaipur": [None, None, 206],
  "Kanpur": [None, None, 159],
  "Lucknow": [None, None, 160],
  "Madras": [None, None, 433],
  "Nagpur": [None, None, 130],
  "Pune": [None, None, 161],
  "TOTAL (CITIES)": [None, None, 4248],
 },
 "Grand": {"GRAND TOTAL": [None, None, 33884]},
}
