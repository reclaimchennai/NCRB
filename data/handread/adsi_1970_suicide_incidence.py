# ADSI 1970, Table X: population, incidence of suicidal deaths, volume of suicides and percentage distribution,
# States / Union Territories / cities (raw/adsi/1970/year_wise/suicides-1970.pdf, pages 7-8; printed pages 20-21).
# Read from the page images; checked by scripts/check_handread.py. The table prints the estimated mid-year population
# "in '000"; converted here to lakh (thousands / 100). Rate = volume of suicides per 100,000 of population. The
# percentage column is not transcribed. Himachal Pradesh, Manipur and Tripura are listed among the States this year.
KIND, YEAR, PUB = "suicide_incidence", 1970, "adsi"
SOURCE = "raw/adsi/1970/year_wise/suicides-1970.pdf"
PAGES = "7-8"
TITLE = 'Table X: Population, Incidence of Suicidal Deaths, Volume of Suicides and Percentage Distribution of Suicides in States/Union Territories/Cities During 1970'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [4258, 433.17, 9.83],
  "Assam": [1019, 156.75, 6.5],
  "Bihar": [2267, 578.26, 3.92],
  "Gujarat": [1374, 266.08, 5.16],
  "Haryana": [856, 100.98, 8.48],
  "Himachal Pradesh": [108, 36.25, 2.98],
  "Jammu & Kashmir": [5, 40.5, 0.12],
  "Kerala": [3149, 213.43, 14.75],
  "Madhya Pradesh": [3827, 408.11, 9.38],
  "Maharashtra": [5730, 501.52, 11.43],
  "Manipur": [57, 11.2, 5.09],
  "Mysore": [3149, 293.62, 10.75],
  "Nagaland": [4, 4.33, 0.92],
  "Orissa": [2520, 216.57, 11.64],
  "Punjab": [662, 148.12, 4.47],
  "Rajasthan": [264, 263.24, 1.0],
  "Tamil Nadu": [5199, 395.6, 13.14],
  "Tripura": [124, 15.13, 8.2],
  "Uttar Pradesh": [6338, 909.8, 6.97],
  "West Bengal": [6938, 449.83, 15.42],
  "TOTAL (STATES)": [47848, 5442.49, 8.79],
 },
 "U.Ts.": {
  "A. & N. Islands": [59, 0.93, 63.44],
  "Chandigarh": [6, 1.59, 3.77],
  "Dadra & N. Haveli": [9, 0.73, 12.32],
  "Delhi": [184, 42.41, 4.34],
  "Goa, Daman & Diu": [74, 6.88, 10.76],
  "Laccadive Islands": [1, 0.28, 3.57],
  "Pondicherry": [247, 4.49, 55.01],
  "TOTAL (U.TS.)": [580, 57.31, 10.12],
 },
 "Grand": {
  "GRAND TOTAL": [48428, 5499.8, 8.81],
 },
 "Cities": {
  "Ahmedabad": [72, 16.28, 4.42],
  "Bangalore": [233, 18.09, 12.88],
  "Bombay": [137, 57.0, 2.4],
  "Calcutta": [73, 31.59, 2.31],
  "Delhi": [154, 39.02, 3.95],
  "Hyderabad": [264, 13.77, 19.17],
  "Kanpur": [47, 13.12, 3.58],
  "Madras": [360, 20.86, 17.26],
  "TOTAL (CITIES)": [1340, 209.73, 6.39],
 },
}
