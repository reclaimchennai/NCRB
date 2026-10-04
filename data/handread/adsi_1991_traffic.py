# ADSI 1991, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1991/table_content/appendix-2_1991.pdf, pages 2).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'Total Road Accidents' Male / Female / Total columns (cols 12-14): Persons killed = the printed Total; every row's Male + Female = Total and every column adds to the printed Total (States), Total (UTs) and Total (All-India).
# Road accidents (cases) and Persons injured are None (not printed).
# Madras city is printed as 5 road accident deaths (5 male, 0 female) -- as printed, implausibly low.
# No Total (Cities) is printed.
KIND, YEAR, PUB = "traffic", 1991, "adsi"
SOURCE = "raw/adsi/1991/table_content/appendix-2_1991.pdf"
PAGES = "2"
TITLE = "Appendix II: Distribution of Accidental Deaths by Other Causes during 1991 (State, UT & City-wise)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 4983],
  "Arunachal Pradesh": [None, None, 83],
  "Assam": [None, None, 242],
  "Bihar": [None, None, 2127],
  "Goa": [None, None, 177],
  "Gujarat": [None, None, 965],
  "Haryana": [None, None, 506],
  "Himachal Pradesh": [None, None, 523],
  "Jammu & Kashmir": [None, None, 550],
  "Karnataka": [None, None, 2845],
  "Kerala": [None, None, 1813],
  "Madhya Pradesh": [None, None, 4067],
  "Maharashtra": [None, None, 3043],
  "Manipur": [None, None, 81],
  "Meghalaya": [None, None, 118],
  "Mizoram": [None, None, 39],
  "Nagaland": [None, None, 19],
  "Orissa": [None, None, 866],
  "Punjab": [None, None, 499],
  "Rajasthan": [None, None, 1953],
  "Sikkim": [None, None, 40],
  "Tamil Nadu": [None, None, 6581],
  "Tripura": [None, None, 33],
  "Uttar Pradesh": [None, None, 7130],
  "West Bengal": [None, None, 3542],
  "TOTAL (STATES)": [None, None, 42825],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 5],
  "Chandigarh": [None, None, 36],
  "D & N Haveli": [None, None, 0],
  "Daman & Diu": [None, None, 8],
  "Delhi": [None, None, 1949],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 107],
  "TOTAL (U.TS.)": [None, None, 2105],
 },
 "Cities": {
  "Ahmedabad": [None, None, 49],
  "Bangalore": [None, None, 311],
  "Bombay": [None, None, 1137],
  "Calcutta": [None, None, 452],
  "Delhi": [None, None, 1480],
  "Hyderabad": [None, None, 291],
  "Jaipur": [None, None, 269],
  "Kanpur": [None, None, 243],
  "Lucknow": [None, None, 179],
  "Madras": [None, None, 5],
  "Nagpur": [None, None, 173],
  "Pune": [None, None, 223],
 },
 "Grand": {"GRAND TOTAL": [None, None, 44930]},
}
