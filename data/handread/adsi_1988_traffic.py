# ADSI 1988, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1988/table_content/appendix-2_1988.pdf, pages 1-2).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'On Roads' (road accident deaths) Male and Female columns; the table prints no Total, so Persons killed = Male + Female and every Male and every Female column was first checked against the printed Total (States), Total (UTs), Grand Total and Total (Cities).
# Road accidents (cases) and Persons injured are None (not printed).
KIND, YEAR, PUB = "traffic", 1988, "adsi"
SOURCE = "raw/adsi/1988/table_content/appendix-2_1988.pdf"
PAGES = "1-2"
TITLE = "Appendix II: State-wise Distribution of Accidental Deaths due to Other Causes during 1988"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 3241],
  "Arunachal Pradesh": [None, None, 78],
  "Assam": [None, None, 359],
  "Bihar": [None, None, 1590],
  "Goa": [None, None, 108],
  "Gujarat": [None, None, 370],
  "Haryana": [None, None, 319],
  "Himachal Pradesh": [None, None, 401],
  "Jammu & Kashmir": [None, None, 584],
  "Karnataka": [None, None, 2578],
  "Kerala": [None, None, 1078],
  "Madhya Pradesh": [None, None, 3200],
  "Maharashtra": [None, None, 2594],
  "Manipur": [None, None, 76],
  "Meghalaya": [None, None, 78],
  "Mizoram": [None, None, 29],
  "Nagaland": [None, None, 36],
  "Orissa": [None, None, 819],
  "Punjab": [None, None, 635],
  "Rajasthan": [None, None, 1578],
  "Sikkim": [None, None, 49],
  "Tamil Nadu": [None, None, 6246],
  "Tripura": [None, None, 18],
  "Uttar Pradesh": [None, None, 5117],
  "West Bengal": [None, None, 3209],
  "TOTAL (STATES)": [None, None, 34390],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 12],
  "Chandigarh": [None, None, 48],
  "D & N Haveli": [None, None, 0],
  "Daman & Diu": [None, None, 6],
  "Delhi": [None, None, 1559],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 104],
  "TOTAL (U.TS.)": [None, None, 1729],
 },
 "Cities": {
  "Ahmedabad": [None, None, 33],
  "Bangalore": [None, None, 497],
  "Bombay": [None, None, 1291],
  "Calcutta": [None, None, 425],
  "Delhi": [None, None, 1243],
  "Hyderabad": [None, None, 251],
  "Jaipur": [None, None, 209],
  "Kanpur": [None, None, 202],
  "Lucknow": [None, None, 106],
  "Madras": [None, None, 399],
  "Nagpur": [None, None, 130],
  "Pune": [None, None, 239],
  "TOTAL (CITIES)": [None, None, 5025],
 },
 "Grand": {"GRAND TOTAL": [None, None, 36119]},
}
