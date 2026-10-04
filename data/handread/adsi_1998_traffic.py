# ADSI 1998: road accidents and persons killed, States / UTs / cities. Read from the page images.
# Road accidents (cases) = Total column (col 15) of Table-12 'Number of Traffic Accidents by Month of Occurrence during
# 1998', Road Accidents block (raw/adsi/1998/table_content/table-12_1998.pdf, page 1, printed page 98).
# Persons killed = Total column (col 33) of Table-8 (Concluded) 'Incidence of Road Accidental Deaths in type of Vehicles
# during 1998' (raw/adsi/1998/table_content/table-8_1998.pdf, page 3, printed page 43).
# Both columns are printed again, figure for figure, in Table 1.11 'Incidence and Rate of Deaths due to Road Accidents
# during 1998' (raw/adsi/1998/year_wise/accidental-deaths-1998.pdf, PDF page 12, printed page 25), whose printed
# deaths-per-100-cases column (col 7) agrees with every row. But Table 1.11 prints the city NAMES in the old order
# (Bombay, Calcutta ... Madras, Madurai) against FIGURES in the new order (Calcutta, Chennai ... Madurai, Mumbai): its
# 'Bombay' row carries Calcutta's figures, 'Calcutta' Chennai's, 'Madras' Madurai's and 'Madurai' Mumbai's. The city
# names here are those of Table-12 and Table-8, which agree with each other.
# Persons injured is None: no State/UT/City-wise count of persons injured in road accidents is printed in the 1998
# files we hold (Table-6 gives injured by cause for All India only).
# Every column adds to the printed Total (States), Total (UTs), Total (All-India) and Total (Cities).
KIND, YEAR, PUB = "traffic", 1998, "adsi"
SOURCE = "raw/adsi/1998/table_content/table-12_1998.pdf"
PAGES = "1 (table-12); 3 (table-8_1998.pdf); 12 (accidental-deaths-1998.pdf, Table 1.11)"
TITLE = "Table-12: Number of Traffic Accidents by Month of Occurrence during 1998 (Road Accidents, Total) and Table-8: Incidence of Road Accidental Deaths in type of Vehicles during 1998 (Total)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [21424, None, 8053],
  "Arunachal Pradesh": [205, None, 160],
  "Assam": [1246, None, 724],
  "Bihar": [7167, None, 3139],
  "Goa": [1313, None, 219],
  "Gujarat": [25361, None, 4885],
  "Haryana": [4413, None, 1914],
  "Himachal Pradesh": [1639, None, 581],
  "Jammu & Kashmir": [4242, None, 786],
  "Karnataka": [30177, None, 5650],
  "Kerala": [32836, None, 2524],
  "Madhya Pradesh": [22608, None, 5757],
  "Maharashtra": [33875, None, 8241],
  "Manipur": [411, None, 93],
  "Meghalaya": [95, None, 72],
  "Mizoram": [44, None, 37],
  "Nagaland": [47, None, 27],
  "Orissa": [6777, None, 1855],
  "Punjab": [1083, None, 954],
  "Rajasthan": [20798, None, 5622],
  "Sikkim": [85, None, 34],
  "Tamil Nadu": [46723, None, 9801],
  "Tripura": [297, None, 142],
  "Uttar Pradesh": [16118, None, 9286],
  "West Bengal": [9195, None, 3691],
  "TOTAL (STATES)": [288179, None, 74247],
 },
 "U.Ts.": {
  "A & N Islands": [120, None, 24],
  "Chandigarh": [348, None, 133],
  "D & N Haveli": [83, None, 38],
  "Daman & Diu": [64, None, 17],
  "Delhi": [10217, None, 2132],
  "Lakshadweep": [3, None, 0],
  "Pondicherry": [990, None, 141],
  "TOTAL (U.TS.)": [11825, None, 2485],
 },
 "Grand": {
  "GRAND TOTAL": [300004, None, 76732],
 },
 "Cities": {
  "Ahmedabad": [9, None, 9],
  "Bangalore": [8408, None, 718],
  "Bhopal": [2264, None, 168],
  "Calcutta": [1885, None, 454],
  "Chennai": [5121, None, 692],
  "Coimbatore": [1301, None, 151],
  "Delhi": [8634, None, 1746],
  "Hyderabad": [1688, None, 338],
  "Indore": [2854, None, 273],
  "Jaipur": [2382, None, 376],
  "Kanpur": [500, None, 386],
  "Kochi": [2418, None, 144],
  "Lucknow": [528, None, 227],
  "Ludhiana": [22, None, 22],
  "Madurai": [860, None, 126],
  "Mumbai": [3878, None, 1013],
  "Nagpur": [1508, None, 213],
  "Patna": [174, None, 75],
  "Pune": [367, None, 395],
  "Surat": [1440, None, 148],
  "Vadodara": [1897, None, 147],
  "Varanasi": [221, None, 190],
  "Vishakhapatnam": [843, None, 200],
  "TOTAL (CITIES)": [49202, None, 8211],
 },
}
