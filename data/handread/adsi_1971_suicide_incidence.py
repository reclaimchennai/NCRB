# ADSI 1971, Table X: population, incidence of suicidal deaths, volume of suicides and percentage distribution,
# States / Union Territories / cities (raw/adsi/1971/year_wise/suicides-1971.pdf, pages 7-8; printed pages 20-21).
# Read from the page images; checked by scripts/check_handread.py. The table prints the estimated mid-year population
# "in '000" (cities: actual population on 1 April 1971); converted here to lakh (thousands / 100). Rate = volume of
# suicides per 100,000 of population. The percentage column is not transcribed. Jammu & Kashmir's rate is printed
# 0.00 (2 / 46.37 lakh = 0.04).
KIND, YEAR, PUB = "suicide_incidence", 1971, "adsi"
SOURCE = "raw/adsi/1971/year_wise/suicides-1971.pdf"
PAGES = "7-8"
TITLE = 'Table X: Population, Incidence of Suicidal Deaths, Volume of Suicides and Percentage Distribution of Suicides in States/Union Territories and Cities During 1971'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3603, 436.11, 8.26],
  "Assam": [878, 160.55, 5.47],
  "Bihar": [799, 565.89, 1.41],
  "Gujarat": [2169, 268.55, 8.08],
  "Haryana": [1192, 100.24, 11.89],
  "Himachal Pradesh": [58, 34.31, 1.69],
  "Jammu & Kashmir": [2, 46.37, 0.0],
  "Karnataka": [3288, 294.09, 11.18],
  "Kerala": [3329, 214.05, 15.55],
  "Madhya Pradesh": [2960, 419.12, 7.06],
  "Maharashtra": [4219, 506.1, 8.34],
  "Manipur": [40, 10.75, 3.72],
  "Nagaland": [2, 5.17, 0.39],
  "Orissa": [1857, 220.49, 8.42],
  "Punjab": [988, 135.37, 7.3],
  "Rajasthan": [322, 258.75, 1.24],
  "Tamil Nadu": [5124, 413.06, 12.4],
  "Tripura": [200, 15.65, 12.78],
  "Uttar Pradesh": [4177, 887.36, 4.71],
  "West Bengal": [7959, 446.86, 17.81],
  "TOTAL (STATES)": [43166, 5438.84, 7.94],
 },
 "U.Ts.": {
  "A. & N. Islands": [64, 1.16, 55.17],
  "Chandigarh": [14, 2.57, 5.45],
  "Dadra & Nagar Haveli": [21, 0.74, 28.38],
  "Delhi": [109, 40.93, 2.66],
  "Goa, Daman & Diu": [81, 8.61, 9.41],
  "Lakshadweep": [1, 0.32, 3.13],
  "Pondicherry": [219, 4.74, 46.2],
  "TOTAL (U.TS.)": [509, 59.07, 8.62],
 },
 "Grand": {
  "GRAND TOTAL": [43675, 5497.91, 7.94],
 },
 "Cities": {
  "Ahmedabad": [184, 17.42, 10.56],
  "Bangalore": [390, 16.54, 23.58],
  "Bombay": [129, 59.71, 2.16],
  "Calcutta": [42, 31.49, 1.33],
  "Delhi": [98, 36.47, 2.69],
  "Hyderabad": [148, 17.96, 8.24],
  "Kanpur": [34, 12.75, 2.67],
  "Madras": [193, 31.7, 6.09],
  "TOTAL (CITIES)": [1218, 224.04, 5.44],
 },
}
