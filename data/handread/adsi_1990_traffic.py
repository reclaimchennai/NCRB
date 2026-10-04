# ADSI 1990, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1990/table_content/appendix-2_1990.pdf, pages 2).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'Total Road Accidents' Male / Female / Total columns (cols 12-14): Persons killed = the printed Total; every row's Male + Female = Total and every column adds to the printed Total (States), Total (UTs) and Total (All-India).
# Road accidents (cases) and Persons injured are None (not printed).
# No Total (Cities) is printed.
KIND, YEAR, PUB = "traffic", 1990, "adsi"
SOURCE = "raw/adsi/1990/table_content/appendix-2_1990.pdf"
PAGES = "2"
TITLE = "Appendix II: Distribution of Accidental Deaths by Other Causes and Sex during 1990 (State, UT & City-wise)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 4210],
  "Arunachal Pradesh": [None, None, 43],
  "Assam": [None, None, 215],
  "Bihar": [None, None, 1989],
  "Goa": [None, None, 121],
  "Gujarat": [None, None, 625],
  "Haryana": [None, None, 522],
  "Himachal Pradesh": [None, None, 478],
  "Jammu & Kashmir": [None, None, 471],
  "Karnataka": [None, None, 3198],
  "Kerala": [None, None, 1558],
  "Madhya Pradesh": [None, None, 3931],
  "Maharashtra": [None, None, 2683],
  "Manipur": [None, None, 50],
  "Meghalaya": [None, None, 68],
  "Mizoram": [None, None, 26],
  "Nagaland": [None, None, 13],
  "Orissa": [None, None, 827],
  "Punjab": [None, None, 549],
  "Rajasthan": [None, None, 1644],
  "Sikkim": [None, None, 36],
  "Tamil Nadu": [None, None, 7551],
  "Tripura": [None, None, 19],
  "Uttar Pradesh": [None, None, 6953],
  "West Bengal": [None, None, 3286],
  "TOTAL (STATES)": [None, None, 41066],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 17],
  "Chandigarh": [None, None, 45],
  "D & N Haveli": [None, None, 1],
  "Daman & Diu": [None, None, 16],
  "Delhi": [None, None, 1743],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 117],
  "TOTAL (U.TS.)": [None, None, 1939],
 },
 "Cities": {
  "Ahmedabad": [None, None, 26],
  "Bangalore": [None, None, 491],
  "Bombay": [None, None, 1239],
  "Calcutta": [None, None, 463],
  "Delhi": [None, None, 1468],
  "Hyderabad": [None, None, 246],
  "Jaipur": [None, None, 237],
  "Kanpur": [None, None, 233],
  "Lucknow": [None, None, 99],
  "Madras": [None, None, 506],
  "Nagpur": [None, None, 166],
  "Pune": [None, None, 223],
 },
 "Grand": {"GRAND TOTAL": [None, None, 43005]},
}
