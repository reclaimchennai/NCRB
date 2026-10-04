# ADSI 1984, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1984/table_content/appendix-2_1984.pdf, pages 1-3).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'On Roads' (road accident deaths) Male and Female columns; the table prints no Total, so Persons killed = Male + Female and every Male and every Female column was first checked against the printed Total (States), Total (UTs), Grand Total and Total (Cities).
# Road accidents (cases) and Persons injured are None (not printed).
KIND, YEAR, PUB = "traffic", 1984, "adsi"
SOURCE = "raw/adsi/1984/table_content/appendix-2_1984.pdf"
PAGES = "1-3"
TITLE = "Appendix II: State-wise Distribution of Accidental Deaths due to Other Causes during 1984"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 2876],
  "Assam": [None, None, 176],
  "Bihar": [None, None, 1005],
  "Gujarat": [None, None, 465],
  "Haryana": [None, None, 321],
  "Himachal Pradesh": [None, None, 146],
  "Jammu & Kashmir": [None, None, 388],
  "Karnataka": [None, None, 2238],
  "Kerala": [None, None, 799],
  "Madhya Pradesh": [None, None, 2403],
  "Maharashtra": [None, None, 2171],
  "Manipur": [None, None, 48],
  "Meghalaya": [None, None, 92],
  "Nagaland": [None, None, 37],
  "Orissa": [None, None, 488],
  "Punjab": [None, None, 615],
  "Rajasthan": [None, None, 870],
  "Sikkim": [None, None, 46],
  "Tamil Nadu": [None, None, 4481],
  "Tripura": [None, None, 51],
  "Uttar Pradesh": [None, None, 5558],
  "West Bengal": [None, None, 2363],
  "TOTAL (STATES)": [None, None, 27637],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 8],
  "Arunachal Pradesh": [None, None, 57],
  "Chandigarh": [None, None, 31],
  "D & N Haveli": [None, None, 0],
  "Delhi": [None, None, 1423],
  "Goa, Daman & Diu": [None, None, 140],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 35],
  "Pondicherry": [None, None, 44],
  "TOTAL (U.TS.)": [None, None, 1738],
 },
 "Cities": {
  "Ahmedabad": [None, None, 32],
  "Bangalore": [None, None, 338],
  "Bombay": [None, None, 1178],
  "Calcutta": [None, None, 423],
  "Delhi": [None, None, 1281],
  "Hyderabad": [None, None, 213],
  "Jaipur": [None, None, 160],
  "Kanpur": [None, None, 825],
  "Lucknow": [None, None, 124],
  "Madras": [None, None, 386],
  "Nagpur": [None, None, 131],
  "Pune": [None, None, 166],
  "TOTAL (CITIES)": [None, None, 5257],
 },
 "Grand": {"GRAND TOTAL": [None, None, 29375]},
}
