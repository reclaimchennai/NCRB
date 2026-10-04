# ADSI 1967, Table 4: incidence, percentage distribution, population and volume of accidental deaths in States / U.Ts. /
# cities (raw/adsi/1967/year_wise/accidental-deaths-1967.pdf, pages 5-6). Read from the page images; counts are checked
# against the printed Total rows and every printed rate against count / population by scripts/check_handread.py.
# Population is printed "in 00" (hundreds); converted to lakh here (hundreds / 1000), e.g. 4,07,120 -> 407.12.
# The percentage-distribution column is not transcribed. Mysore: printed rate 26.33 against 7202/273.235 = 26.36 (count and population both confirmed by the State totals; left as printed).
KIND, YEAR, PUB = "accidental_incidence", 1967, "adsi"
SOURCE = "raw/adsi/1967/year_wise/accidental-deaths-1967.pdf"
PAGES = "5-6"
TITLE = "Table 4: Incidence, percentage distribution, population and volume of accidental deaths in States/U.Ts/Cities during 1967"
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Delhi", "Rate of accidental deaths per lakh"): (43.94, 44.94, "second digit smudged, reads like 43.94; count 1,637 and population 36,427 hundred are both confirmed by the U.T. column totals, and 1637/36.427 = 44.94"),
    ("GRAND TOTAL", "Number of accidental deaths"): (None, 126762, "last digit obscured (126,76_); the text on page 2 prints 1,26,762 and States 1,23,851 + U.Ts. 2,911 = 126,762"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [7805, 407.120, 19.17],
  "Assam": [1942, 142.861, 13.59],
  "Bihar": [8960, 537.732, 16.66],
  "Gujarat": [6780, 245.000, 27.67],
  "Haryana": [1812, 92.080, 19.67],
  "Jammu and Kashmir": [456, 38.867, 11.73],
  "Kerala": [2952, 197.903, 14.91],
  "Madhya Pradesh": [13970, 378.642, 36.90],
  "Maharashtra": [21122, 464.769, 45.44],
  "Mysore": [7202, 273.235, 26.33],
  "Nagaland": [7, 4.109, 1.70],
  "Orissa": [5589, 202.022, 27.66],
  "Punjab": [4599, 135.066, 34.05],
  "Rajasthan": [2457, 241.594, 10.17],
  "Tamil Nadu": [9133, 375.174, 24.34],
  "Uttar Pradesh": [16916, 849.263, 19.92],
  "West Bengal": [12149, 414.307, 29.32],
  "TOTAL (STATES)": [123851, 4999.744, 24.77],
 },
 "U.Ts.": {
  "A & N Islands": [25, 0.823, 30.38],
  "Chandigarh": [35, 1.453, 24.09],
  "Dadra and Nagar Haveli": [50, 0.675, 74.07],
  "Delhi": [1637, 36.427, 44.94],
  "Goa Daman & Diu": [350, 6.683, 52.37],
  "Himachal Pradesh": [384, 33.393, 11.50],
  "Laccadives": [2, 0.265, 7.55],
  "Manipur": [21, 9.924, 2.12],
  "Pondicherry": [259, 4.209, 61.50],
  "Tripura": [148, 13.807, 10.71],
  "TOTAL (U.TS.)": [2911, 107.659, 27.04],
 },
 "Grand": {
  "GRAND TOTAL": [126762, 5107.403, 24.82],
 },
 "Cities": {
  "Ahmedabad": [703, 14.921, 47.11],
  "Bangalore": [344, 16.158, 21.29],
  "Bombay": [3353, 52.026, 64.45],
  "Calcutta": [415, 30.845, 13.45],
  "Delhi": [1451, 33.183, 43.72],
  "Hyderabad": [283, 13.365, 21.17],
  "Kanpur": [76, 12.027, 6.32],
  "Madras": [680, 19.713, 34.50],
  "TOTAL (CITIES)": [7305, 192.238, 38.00],
 },
}
