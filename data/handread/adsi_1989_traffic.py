# ADSI 1989, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1989/table_content/appendix-2_1989.pdf, pages 2).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'Total Road Accidents' Male / Female / Total columns (cols 12-14): Persons killed = the printed Total; every row's Male + Female = Total and every column adds to the printed Total (States), Total (UTs) and Total (All-India).
# Road accidents (cases) and Persons injured are None (not printed).
# No Total (Cities) is printed.
KIND, YEAR, PUB = "traffic", 1989, "adsi"
SOURCE = "raw/adsi/1989/table_content/appendix-2_1989.pdf"
PAGES = "2"
TITLE = "Appendix II: Distribution of Accidental Deaths by Other Causes and Sex during 1989 (State, UT & City-wise)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 3742],
  "Arunachal Pradesh": [None, None, 41],
  "Assam": [None, None, 388],
  "Bihar": [None, None, 2028],
  "Goa": [None, None, 126],
  "Gujarat": [None, None, 511],
  "Haryana": [None, None, 488],
  "Himachal Pradesh": [None, None, 434],
  "Jammu & Kashmir": [None, None, 780],
  "Karnataka": [None, None, 2798],
  "Kerala": [None, None, 1779],
  "Madhya Pradesh": [None, None, 4192],
  "Maharashtra": [None, None, 2910],
  "Manipur": [None, None, 130],
  "Meghalaya": [None, None, 96],
  "Mizoram": [None, None, 21],
  "Nagaland": [None, None, 15],
  "Orissa": [None, None, 667],
  "Punjab": [None, None, 614],
  "Rajasthan": [None, None, 1452],
  "Sikkim": [None, None, 8],
  "Tamil Nadu": [None, None, 6020],
  "Tripura": [None, None, 33],
  "Uttar Pradesh": [None, None, 7303],
  "West Bengal": [None, None, 3549],
  "TOTAL (STATES)": [None, None, 40125],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 15],
  "Chandigarh": [None, None, 41],
  "D & N Haveli": [None, None, 3],
  "Daman & Diu": [None, None, 8],
  "Delhi": [None, None, 1792],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 91],
  "TOTAL (U.TS.)": [None, None, 1950],
 },
 "Cities": {
  "Ahmedabad": [None, None, 36],
  "Bangalore": [None, None, 542],
  "Bombay": [None, None, 1236],
  "Calcutta": [None, None, 467],
  "Delhi": [None, None, 1442],
  "Hyderabad": [None, None, 263],
  "Jaipur": [None, None, 215],
  "Kanpur": [None, None, 232],
  "Lucknow": [None, None, 96],
  "Madras": [None, None, 413],
  "Nagpur": [None, None, 173],
  "Pune": [None, None, 261],
 },
 "Grand": {"GRAND TOTAL": [None, None, 42075]},
}
