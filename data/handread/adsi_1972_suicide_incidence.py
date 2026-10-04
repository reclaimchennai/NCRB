# ADSI 1972, Table X: population, incidence of suicidal deaths, volume of suicides and percentage distribution,
# States / U.Ts. / cities (raw/adsi/1972/year_wise/suicides-1972.pdf, pages 7-8; printed pages 18-19). Read from the
# page images; checked by scripts/check_handread.py. The table prints the estimated mid-year population "in '000";
# converted here to lakh (thousands / 100). Rate = volume of suicides per 1,00,000 of population. The percentage
# column is not transcribed. Lakshadweep "-" (nil) is 0. Note on the page: data from Arunachal Pradesh not available.
KIND, YEAR, PUB = "suicide_incidence", 1972, "adsi"
SOURCE = "raw/adsi/1972/year_wise/suicides-1972.pdf"
PAGES = "7-8"
TITLE = 'Table X: Population, Incidence of Suicidal Deaths, Volume of Suicides and Percentage distribution of suicides in States/U.Ts./Cities during the year 1972'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3286, 445.71, 7.37],
  "Assam": [1215, 151.92, 8.0],
  "Bihar": [920, 576.49, 1.6],
  "Gujarat": [1324, 275.44, 4.81],
  "Haryana": [445, 103.17, 4.31],
  "Himachal Pradesh": [49, 35.06, 1.4],
  "Jammu & Kashmir": [33, 47.35, 0.7],
  "Karnataka": [3539, 300.42, 11.78],
  "Kerala": [4500, 219.71, 20.48],
  "Madhya Pradesh": [3362, 429.59, 7.83],
  "Maharashtra": [4278, 518.15, 8.26],
  "Manipur": [20, 11.02, 1.81],
  "Meghalaya": [127, 10.38, 12.23],
  "Nagaland": [8, 5.26, 1.52],
  "Orissa": [2461, 225.22, 10.93],
  "Punjab": [649, 138.74, 4.68],
  "Rajasthan": [513, 265.33, 1.93],
  "Tamil Nadu": [4769, 422.16, 11.3],
  "Tripura": [258, 15.98, 16.15],
  "Uttar Pradesh": [4049, 902.16, 4.49],
  "West Bengal": [7271, 455.6, 15.96],
  "TOTAL (STATES)": [43076, 5554.86, 7.75],
 },
 "U.Ts.": {
  "A. & N. Islands": [62, 1.18, 52.54],
  "Chandigarh": [23, 2.63, 8.75],
  "D. & N. Haveli": [38, 0.76, 50.0],
  "Delhi": [149, 43.13, 3.45],
  "Goa, Daman & Diu": [57, 8.8, 6.48],
  "Lakshadweep": [0, 0.33, 0.0],
  "Mizoram": [9, 3.34, 2.69],
  "Pondicherry": [187, 4.84, 38.64],
  "TOTAL (U.TS.)": [525, 65.01, 8.08],
 },
 "Grand": {
  "GRAND TOTAL": [43601, 5619.87, 7.76],
 },
 "Cities": {
  "Ahmedabad": [160, 16.66, 9.6],
  "Bangalore": [366, 16.13, 22.69],
  "Bombay": [175, 63.19, 2.77],
  "Calcutta": [33, 31.81, 1.04],
  "Delhi": [131, 39.12, 3.35],
  "Hyderabad": [154, 17.01, 9.05],
  "Kanpur": [52, 12.02, 4.33],
  "Madras": [221, 26.1, 8.47],
  "TOTAL (CITIES)": [1292, 222.04, 5.82],
 },
}
