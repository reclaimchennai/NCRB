# ADSI 1992, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1992/table_content/appendix-2_1992.pdf, pages 2, 13).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'Total Road Accidents' Male / Female / Total columns (cols 12-14): Persons killed = the printed Total; every row's Male + Female = Total and every column adds to the printed Total (States), Total (UTs) and Total (All-India).
# Road accidents (cases) and Persons injured are None (not printed).
# Patna and Varanasi are printed NR (data not received). No Total (Cities) is printed.
KIND, YEAR, PUB = "traffic", 1992, "adsi"
SOURCE = "raw/adsi/1992/table_content/appendix-2_1992.pdf"
PAGES = "2, 13"
TITLE = "Appendix II: Distribution of Accidental Deaths by Un-natural Causes during 1992 (State, UT & City-wise)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 5126],
  "Arunachal Pradesh": [None, None, 175],
  "Assam": [None, None, 215],
  "Bihar": [None, None, 2106],
  "Goa": [None, None, 198],
  "Gujarat": [None, None, 2473],
  "Haryana": [None, None, 538],
  "Himachal Pradesh": [None, None, 348],
  "Jammu & Kashmir": [None, None, 448],
  "Karnataka": [None, None, 4052],
  "Kerala": [None, None, 2137],
  "Madhya Pradesh": [None, None, 4512],
  "Maharashtra": [None, None, 3109],
  "Manipur": [None, None, 110],
  "Meghalaya": [None, None, 87],
  "Mizoram": [None, None, 30],
  "Nagaland": [None, None, 5],
  "Orissa": [None, None, 1024],
  "Punjab": [None, None, 499],
  "Rajasthan": [None, None, 1573],
  "Sikkim": [None, None, 61],
  "Tamil Nadu": [None, None, 7192],
  "Tripura": [None, None, 120],
  "Uttar Pradesh": [None, None, 7622],
  "West Bengal": [None, None, 3243],
  "TOTAL (STATES)": [None, None, 47003],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 14],
  "Chandigarh": [None, None, 22],
  "D & N Haveli": [None, None, 0],
  "Daman & Diu": [None, None, 11],
  "Delhi": [None, None, 1973],
  "Lakshadweep": [None, None, 1],
  "Pondicherry": [None, None, 132],
  "TOTAL (U.TS.)": [None, None, 2153],
 },
 "Cities": {
  "Ahmedabad": [None, None, 30],
  "Bangalore": [None, None, 383],
  "Bhopal": [None, None, 72],
  "Bombay": [None, None, 1327],
  "Calcutta": [None, None, 472],
  "Coimbatore": [None, None, 142],
  "Delhi": [None, None, 1460],
  "Hyderabad": [None, None, 303],
  "Indore": [None, None, 233],
  "Jaipur": [None, None, 241],
  "Kanpur": [None, None, 271],
  "Kochi": [None, None, 101],
  "Lucknow": [None, None, 226],
  "Ludhiana": [None, None, 12],
  "Madras": [None, None, 471],
  "Madurai": [None, None, 103],
  "Nagpur": [None, None, 180],
  "Patna": [None, None, None],
  "Pune": [None, None, 222],
  "Surat": [None, None, 22],
  "Vadodara": [None, None, 41],
  "Varanasi": [None, None, None],
  "Vishakhapatnam": [None, None, 95],
 },
 "Grand": {"GRAND TOTAL": [None, None, 49156]},
}
