# ADSI 1983, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1983/table_content/appendix-2_1983.pdf, pages 1-4).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'On Roads' (road accident deaths) Male and Female columns; the table prints no Total, so Persons killed = Male + Female and every Male and every Female column was first checked against the printed Total (States), Total (UTs), Grand Total and Total (Cities).
# Road accidents (cases) and Persons injured are None (not printed).
KIND, YEAR, PUB = "traffic", 1983, "adsi"
SOURCE = "raw/adsi/1983/table_content/appendix-2_1983.pdf"
PAGES = "1-4"
TITLE = "Appendix II: State-wise Distribution of Accidental Deaths due to Other Causes during 1983"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 2276],
  "Assam": [None, None, 234],
  "Bihar": [None, None, 928],
  "Gujarat": [None, None, 340],
  "Haryana": [None, None, 339],
  "Himachal Pradesh": [None, None, 84],
  "Jammu & Kashmir": [None, None, 215],
  "Karnataka": [None, None, 1663],
  "Kerala": [None, None, 526],
  "Madhya Pradesh": [None, None, 2104],
  "Maharashtra": [None, None, 2096],
  "Manipur": [None, None, 41],
  "Meghalaya": [None, None, 50],
  "Nagaland": [None, None, 11],
  "Orissa": [None, None, 545],
  "Punjab": [None, None, 565],
  "Rajasthan": [None, None, 975],
  "Sikkim": [None, None, 25],
  "Tamil Nadu": [None, None, 3524],
  "Tripura": [None, None, 42],
  "Uttar Pradesh": [None, None, 3182],
  "West Bengal": [None, None, 1874],
  "TOTAL (STATES)": [None, None, 21639],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 14],
  "Arunachal Pradesh": [None, None, 21],
  "Chandigarh": [None, None, 23],
  "D & N Haveli": [None, None, 0],
  "Delhi": [None, None, 1481],
  "Goa, Daman & Diu": [None, None, 112],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 49],
  "Pondicherry": [None, None, 36],
  "TOTAL (U.TS.)": [None, None, 1736],
 },
 "Cities": {
  "Ahmedabad": [None, None, 30],
  "Bangalore": [None, None, 263],
  "Bombay": [None, None, 1111],
  "Calcutta": [None, None, 509],
  "Delhi": [None, None, 1332],
  "Hyderabad": [None, None, 241],
  "Jaipur": [None, None, 114],
  "Kanpur": [None, None, 174],
  "Lucknow": [None, None, 90],
  "Madras": [None, None, 366],
  "Nagpur": [None, None, 90],
  "Pune": [None, None, 185],
  "TOTAL (CITIES)": [None, None, 4505],
 },
 "Grand": {"GRAND TOTAL": [None, None, 23375]},
}
