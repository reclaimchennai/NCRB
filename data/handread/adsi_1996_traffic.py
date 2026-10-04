# ADSI 1996, Appendix-II: road accidents, persons injured and persons killed, States / UTs / cities
# (raw/adsi/1996/table_content/appendix-2_1996.pdf, PDF page 33, printed page 126: 'Traffic Accidents (Road Accidents)').
# Read from the page image. Road accidents (cases) = col 3 'No. of Cases'; Persons injured = col 230 (Total injured);
# Persons killed = col 233 (Total killed). Every row's printed Male + Female equals its Total for both injured and killed,
# and every column adds to the printed Total (States), Total (UTs) and Total (All-India). No Total (Cities) is printed.
# Delhi (UT) is entered under U.Ts. as "Delhi", Delhi (City) under Cities as "Delhi".
KIND, YEAR, PUB = "traffic", 1996, "adsi"
SOURCE = "raw/adsi/1996/table_content/appendix-2_1996.pdf"
PAGES = "33"
TITLE = "Appendix-II: Number of Persons Injured & Killed by Un-Natural Causes during 1996 (State, UT & City-wise) - Traffic Accidents (Road Accidents)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [18836, 21866, 7194],
  "Arunachal Pradesh": [230, 429, 101],
  "Assam": [1146, 1231, 714],
  "Bihar": [5255, 3860, 2596],
  "Goa": [1021, 1087, 220],
  "Gujarat": [21479, 22388, 4607],
  "Haryana": [4067, 4019, 1563],
  "Himachal Pradesh": [1704, 3353, 709],
  "Jammu & Kashmir": [3335, 3777, 593],
  "Karnataka": [20930, 35043, 4865],
  "Kerala": [35731, 51780, 2780],
  "Madhya Pradesh": [23260, 22020, 4938],
  "Maharashtra": [34426, 28940, 8712],
  "Manipur": [399, 578, 99],
  "Meghalaya": [107, 187, 89],
  "Mizoram": [71, 107, 82],
  "Nagaland": [132, 240, 99],
  "Orissa": [5429, 6550, 1693],
  "Punjab": [1286, 513, 1041],
  "Rajasthan": [16434, 16702, 4260],
  "Sikkim": [83, 128, 30],
  "Tamil Nadu": [42197, 26854, 9028],
  "Tripura": [562, 927, 136],
  "Uttar Pradesh": [12737, 9336, 7881],
  "West Bengal": [8504, 8350, 3144],
  "TOTAL (STATES)": [259361, 270265, 67174],
 },
 "U.Ts.": {
  "A & N Islands": [94, 122, 13],
  "Chandigarh": [382, 375, 128],
  "D & N Haveli": [34, 43, 34],
  "Daman & Diu": [64, 94, 15],
  "Delhi": [11314, 10334, 2328],
  "Lakshadweep": [0, 0, 0],
  "Pondicherry": [833, 929, 108],
  "TOTAL (U.TS.)": [12721, 11897, 2626],
 },
 "Grand": {
  "GRAND TOTAL": [272082, 282162, 69800],
 },
 "Cities": {
  "Ahmedabad": [255, 181, 90],
  "Bangalore": [8646, 6572, 723],
  "Bhopal": [1926, 1953, 178],
  "Bombay": [4949, 3967, 1361],
  "Calcutta": [1942, 1493, 474],
  "Coimbatore": [1150, 1090, 184],
  "Delhi": [9952, 9046, 1888],
  "Hyderabad": [1923, 1788, 372],
  "Indore": [3150, 2137, 289],
  "Jaipur": [2311, 1788, 338],
  "Kanpur": [468, 216, 252],
  "Kochi": [2379, 2649, 144],
  "Lucknow": [525, 279, 246],
  "Ludhiana": [25, 0, 25],
  "Madras": [5458, 3783, 615],
  "Madurai": [101, 0, 107],
  "Nagpur": [1368, 1234, 217],
  "Patna": [125, 126, 111],
  "Pune": [315, 73, 339],
  "Surat": [1379, 1260, 133],
  "Vadodara": [1669, 1178, 145],
  "Varanasi": [188, 74, 169],
  "Vishakhapatnam": [683, 739, 161],
 },
}
