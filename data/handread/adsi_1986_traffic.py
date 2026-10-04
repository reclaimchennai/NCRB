# ADSI 1986, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1986/table_content/appendix-2_1986.pdf, pages 1-2).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'On Roads' (road accident deaths) Male and Female columns; the table prints no Total, so Persons killed = Male + Female and every Male and every Female column was first checked against the printed Total (States), Total (UTs), Grand Total and Total (Cities).
# Road accidents (cases) and Persons injured are None (not printed).
KIND, YEAR, PUB = "traffic", 1986, "adsi"
SOURCE = "raw/adsi/1986/table_content/appendix-2_1986.pdf"
PAGES = "1-2"
TITLE = "Appendix II: State-wise Distribution of Accidental Deaths due to Other Causes during 1986"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ('Kanpur', 'Persons killed'): (319, 317, "Total road accident deaths, males, printed 289; the row's own (a) motor vehicle 176 + (b) other road 111 = 287, and with 287 the Cities male column adds to the printed Total (Cities) 3,967 (no percentage is printed in this table); Persons killed = males + females = 287 + 30"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 3062],
  "Arunachal Pradesh": [None, None, 83],
  "Assam": [None, None, 241],
  "Bihar": [None, None, 932],
  "Gujarat": [None, None, 403],
  "Haryana": [None, None, 403],
  "Himachal Pradesh": [None, None, 262],
  "Jammu & Kashmir": [None, None, 307],
  "Karnataka": [None, None, 2449],
  "Kerala": [None, None, 1044],
  "Madhya Pradesh": [None, None, 2563],
  "Maharashtra": [None, None, 2242],
  "Manipur": [None, None, 70],
  "Meghalaya": [None, None, 73],
  "Mizoram": [None, None, 40],
  "Nagaland": [None, None, 21],
  "Orissa": [None, None, 990],
  "Punjab": [None, None, 537],
  "Rajasthan": [None, None, 877],
  "Sikkim": [None, None, 50],
  "Tamil Nadu": [None, None, 6412],
  "Tripura": [None, None, 23],
  "Uttar Pradesh": [None, None, 5354],
  "West Bengal": [None, None, 2555],
  "TOTAL (STATES)": [None, None, 30993],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 18],
  "Chandigarh": [None, None, 44],
  "D & N Haveli": [None, None, 1],
  "Delhi": [None, None, 1345],
  "Goa, Daman & Diu": [None, None, 131],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 55],
  "TOTAL (U.TS.)": [None, None, 1594],
 },
 "Cities": {
  "Ahmedabad": [None, None, 25],
  "Bangalore": [None, None, 397],
  "Bombay": [None, None, 1094],
  "Calcutta": [None, None, 410],
  "Delhi": [None, None, 1158],
  "Hyderabad": [None, None, 274],
  "Jaipur": [None, None, 175],
  "Kanpur": [None, None, 317],
  "Lucknow": [None, None, 99],
  "Madras": [None, None, 454],
  "Nagpur": [None, None, 120],
  "Pune": [None, None, 191],
  "TOTAL (CITIES)": [None, None, 4714],
 },
 "Grand": {"GRAND TOTAL": [None, None, 32587]},
}
