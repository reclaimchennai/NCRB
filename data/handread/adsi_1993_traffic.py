# ADSI 1993, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1993/table_content/appendix-2_1993.pdf, pages 2, 13).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'Total Road Accidents' Male / Female / Total columns (cols 12-14): Persons killed = the printed Total; every row's Male + Female = Total and every column adds to the printed Total (States), Total (UTs) and Total (All-India).
# Road accidents (cases) and Persons injured are None (not printed).
# Madras city is printed as 5 road accident deaths (5 male, 0 female) -- as printed, implausibly low.
# No Total (Cities) is printed.
KIND, YEAR, PUB = "traffic", 1993, "adsi"
SOURCE = "raw/adsi/1993/table_content/appendix-2_1993.pdf"
PAGES = "2, 13"
TITLE = "Appendix II: Distribution of Accidental Deaths by Un-natural Causes during 1993 (State, UT & City-wise)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 4821],
  "Arunachal Pradesh": [None, None, 3],
  "Assam": [None, None, 270],
  "Bihar": [None, None, 1913],
  "Goa": [None, None, 178],
  "Gujarat": [None, None, 2605],
  "Haryana": [None, None, 398],
  "Himachal Pradesh": [None, None, 383],
  "Jammu & Kashmir": [None, None, 295],
  "Karnataka": [None, None, 2852],
  "Kerala": [None, None, 2081],
  "Madhya Pradesh": [None, None, 4063],
  "Maharashtra": [None, None, 2954],
  "Manipur": [None, None, 151],
  "Meghalaya": [None, None, 212],
  "Mizoram": [None, None, 37],
  "Nagaland": [None, None, 26],
  "Orissa": [None, None, 1040],
  "Punjab": [None, None, 630],
  "Rajasthan": [None, None, 1777],
  "Sikkim": [None, None, 35],
  "Tamil Nadu": [None, None, 7412],
  "Tripura": [None, None, 84],
  "Uttar Pradesh": [None, None, 6278],
  "West Bengal": [None, None, 3040],
  "TOTAL (STATES)": [None, None, 43538],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 9],
  "Chandigarh": [None, None, 44],
  "D & N Haveli": [None, None, 0],
  "Daman & Diu": [None, None, 8],
  "Delhi": [None, None, 2030],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 140],
  "TOTAL (U.TS.)": [None, None, 2231],
 },
 "Cities": {
  "Ahmedabad": [None, None, 26],
  "Bangalore": [None, None, 367],
  "Bhopal": [None, None, 157],
  "Bombay": [None, None, 1209],
  "Calcutta": [None, None, 494],
  "Coimbatore": [None, None, 155],
  "Delhi": [None, None, 1629],
  "Hyderabad": [None, None, 452],
  "Indore": [None, None, 149],
  "Jaipur": [None, None, 265],
  "Kanpur": [None, None, 269],
  "Kochi": [None, None, 112],
  "Lucknow": [None, None, 237],
  "Ludhiana": [None, None, 24],
  "Madras": [None, None, 5],
  "Madurai": [None, None, 86],
  "Nagpur": [None, None, 167],
  "Patna": [None, None, 17],
  "Pune": [None, None, 295],
  "Surat": [None, None, 13],
  "Vadodara": [None, None, 7],
  "Varanasi": [None, None, 337],
  "Vishakhapatnam": [None, None, 103],
 },
 "Grand": {"GRAND TOTAL": [None, None, 45769]},
}
