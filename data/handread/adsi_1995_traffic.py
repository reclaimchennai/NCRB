# ADSI 1995, Table-9(A): road accident deaths, States / UTs / cities (raw/adsi/1995/year_wise/accidental-deaths-1995.pdf, pages 19-21).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the Total column (col 33) of Table-9(A) (Concluded), road accident deaths by type of vehicle; it adds to the printed Total States, Total UTs, Total All India and Total Cities. Appendix II (un-natural causes) for 1995 is not among the files we hold.
# Road accidents (cases) and Persons injured are None (not printed).
KIND, YEAR, PUB = "traffic", 1995, "adsi"
SOURCE = "raw/adsi/1995/year_wise/accidental-deaths-1995.pdf"
PAGES = "19-21"
TITLE = "Table-9(A): Incidence of Road Accident Deaths by type of vehicle during 1995 (State, UT & City-wise)"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 5814],
  "Arunachal Pradesh": [None, None, 85],
  "Assam": [None, None, 674],
  "Bihar": [None, None, 2539],
  "Goa": [None, None, 237],
  "Gujarat": [None, None, 4097],
  "Haryana": [None, None, 2000],
  "Himachal Pradesh": [None, None, 673],
  "Jammu & Kashmir": [None, None, 430],
  "Karnataka": [None, None, 5557],
  "Kerala": [None, None, 2720],
  "Madhya Pradesh": [None, None, 5556],
  "Maharashtra": [None, None, 8721],
  "Manipur": [None, None, 111],
  "Meghalaya": [None, None, 116],
  "Mizoram": [None, None, 66],
  "Nagaland": [None, None, 51],
  "Orissa": [None, None, 1675],
  "Punjab": [None, None, 852],
  "Rajasthan": [None, None, 3933],
  "Sikkim": [None, None, 56],
  "Tamil Nadu": [None, None, 8773],
  "Tripura": [None, None, 135],
  "Uttar Pradesh": [None, None, 8079],
  "West Bengal": [None, None, 2802],
  "TOTAL (STATES)": [None, None, 65752],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 22],
  "Chandigarh": [None, None, 103],
  "D & N Haveli": [None, None, 21],
  "Daman & Diu": [None, None, 25],
  "Delhi": [None, None, 2288],
  "Lakshadweep": [None, None, 0],
  "Pondicherry": [None, None, 140],
  "TOTAL (U.TS.)": [None, None, 2599],
 },
 "Cities": {
  "Ahmedabad": [None, None, 14],
  "Bangalore": [None, None, 649],
  "Bhopal": [None, None, 137],
  "Bombay": [None, None, 1594],
  "Calcutta": [None, None, 480],
  "Coimbatore": [None, None, 179],
  "Delhi": [None, None, 1873],
  "Hyderabad": [None, None, 316],
  "Indore": [None, None, 166],
  "Jaipur": [None, None, 269],
  "Kanpur": [None, None, 340],
  "Kochi": [None, None, 153],
  "Lucknow": [None, None, 160],
  "Ludhiana": [None, None, 52],
  "Madras": [None, None, 557],
  "Madurai": [None, None, 126],
  "Nagpur": [None, None, 201],
  "Patna": [None, None, 91],
  "Pune": [None, None, 332],
  "Surat": [None, None, 141],
  "Vadodara": [None, None, 161],
  "Varanasi": [None, None, 394],
  "Vishakhapatnam": [None, None, 128],
  "TOTAL (CITIES)": [None, None, 8513],
 },
 "Grand": {"GRAND TOTAL": [None, None, 68351]},
}
