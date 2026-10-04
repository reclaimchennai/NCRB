# ADSI 1994, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1994/table_content/appendix-2_1994.pdf, pages 2, 13).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'Total Road Accidents' Male / Female / Total columns (cols 12-14): Persons killed = the printed Total; every row's Male + Female = Total and every column adds to the printed Total (States), Total (UTs) and Total (All-India).
# Road accidents (cases) and Persons injured are None (not printed).
# No Total (Cities) is printed.
KIND, YEAR, PUB = "traffic", 1994, "adsi"
SOURCE = "raw/adsi/1994/table_content/appendix-2_1994.pdf"
PAGES = "2, 13"
TITLE = "Appendix II: Distribution of Accidental Deaths by Un-natural Causes during 1994 (State, UT & City-wise)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 5175],
  "Arunachal Pradesh": [None, None, 3],
  "Assam": [None, None, 235],
  "Bihar": [None, None, 2360],
  "Goa": [None, None, 207],
  "Gujarat": [None, None, 2653],
  "Haryana": [None, None, 513],
  "Himachal Pradesh": [None, None, 436],
  "Jammu & Kashmir": [None, None, 341],
  "Karnataka": [None, None, 4194],
  "Kerala": [None, None, 2202],
  "Madhya Pradesh": [None, None, 4557],
  "Maharashtra": [None, None, 3228],
  "Manipur": [None, None, 97],
  "Meghalaya": [None, None, 114],
  "Mizoram": [None, None, 37],
  "Nagaland": [None, None, 37],
  "Orissa": [None, None, 1120],
  "Punjab": [None, None, 873],
  "Rajasthan": [None, None, 2571],
  "Sikkim": [None, None, 22],
  "Tamil Nadu": [None, None, 7798],
  "Tripura": [None, None, 129],
  "Uttar Pradesh": [None, None, 7649],
  "West Bengal": [None, None, 2800],
  "TOTAL (STATES)": [None, None, 49351],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 9],
  "Chandigarh": [None, None, 124],
  "D & N Haveli": [None, None, 3],
  "Daman & Diu": [None, None, 19],
  "Delhi": [None, None, 2210],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 139],
  "TOTAL (U.TS.)": [None, None, 2504],
 },
 "Cities": {
  "Ahmedabad": [None, None, 46],
  "Bangalore": [None, None, 607],
  "Bhopal": [None, None, 168],
  "Bombay": [None, None, 1423],
  "Calcutta": [None, None, 513],
  "Coimbatore": [None, None, 140],
  "Delhi": [None, None, 1741],
  "Hyderabad": [None, None, 397],
  "Indore": [None, None, 169],
  "Jaipur": [None, None, 254],
  "Kanpur": [None, None, 289],
  "Kochi": [None, None, 131],
  "Lucknow": [None, None, 145],
  "Ludhiana": [None, None, 19],
  "Madras": [None, None, 479],
  "Madurai": [None, None, 113],
  "Nagpur": [None, None, 128],
  "Patna": [None, None, 65],
  "Pune": [None, None, 255],
  "Surat": [None, None, 2],
  "Vadodara": [None, None, 21],
  "Varanasi": [None, None, 280],
  "Vishakhapatnam": [None, None, 155],
 },
 "Grand": {"GRAND TOTAL": [None, None, 51855]},
}
