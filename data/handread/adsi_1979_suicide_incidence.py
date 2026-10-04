# ADSI 1979, Table II: incidence of suicides, volume of suicides per lakh of population, States / U.Ts. / cities
# (raw/adsi/1979/year_wise/suicides-1979.pdf, pages 4-5; printed pages 21-22). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in (000); converted here to lakh
# (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not transcribed.
# Lakshadweep "-" (nil) is 0. The States' populations as read add to 641730 thousand against the printed Total
# 641729 (every rate agrees with its row; the 1979 errata sheet has no entry for this table).
KIND, YEAR, PUB = "suicide_incidence", 1979, "adsi"
SOURCE = "raw/adsi/1979/year_wise/suicides-1979.pdf"
PAGES = "4-5"
TITLE = 'Table II: Incidence of Suicides, Volume of Suicides per lakh of population during 1979'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3327, 500.73, 6.64],
  "Assam": [1811, 189.74, 9.54],
  "Bihar": [346, 662.15, 0.52],
  "Gujarat": [1488, 319.54, 4.66],
  "Haryana": [450, 120.38, 3.74],
  "Himachal Pradesh": [60, 40.98, 1.46],
  "Jammu & Kashmir": [23, 57.4, 0.4],
  "Karnataka": [4976, 345.26, 14.41],
  "Kerala": [3631, 252.27, 14.39],
  "Madhya Pradesh": [1343, 512.26, 2.62],
  "Maharashtra": [3106, 591.24, 5.25],
  "Manipur": [13, 13.93, 0.93],
  "Meghalaya": [27, 12.66, 2.13],
  "Nagaland": [6, 6.79, 0.88],
  "Orissa": [1982, 262.04, 7.56],
  "Punjab": [327, 156.07, 2.1],
  "Rajasthan": [615, 321.14, 1.92],
  "Sikkim": [17, 2.47, 6.88],
  "Tamil Nadu": [4475, 463.25, 9.66],
  "Tripura": [387, 20.06, 19.29],
  "Uttar Pradesh": [3532, 1026.71, 3.44],
  "West Bengal": [5603, 540.23, 10.37],
  "TOTAL (STATES)": [37545, 6417.29, 5.85],
 },
 "U.Ts.": {
  "A. & N. Islands": [44, 1.75, 25.14],
  "Arunachal Pradesh": [6, 6.06, 0.99],
  "Chandigarh": [13, 4.63, 2.81],
  "D & N. Haveli": [21, 0.86, 24.42],
  "Delhi": [333, 57.8, 5.76],
  "Goa Daman & Diu": [78, 11.07, 7.05],
  "Lakshadweep": [0, 0.35, 0.0],
  "Mizoram": [11, 4.31, 2.55],
  "Pondicherry": [166, 5.72, 29.02],
  "TOTAL (U.TS.)": [672, 92.55, 7.26],
 },
 "Grand": {
  "GRAND TOTAL": [38217, 6509.82, 5.87],
 },
 "Cities": {
  "Ahmedabad": [189, 20.81, 9.08],
  "Bangalore": [455, 19.86, 22.91],
  "Bombay": [201, 81.28, 2.47],
  "Calcutta": [46, 33.45, 1.38],
  "Delhi": [315, 52.89, 5.96],
  "Hyderabad": [82, 21.87, 3.75],
  "Kanpur": [41, 14.5, 2.83],
  "Madras": [277, 33.42, 8.29],
  "TOTAL (CITIES)": [1606, 278.08, 5.78],
 },
}
