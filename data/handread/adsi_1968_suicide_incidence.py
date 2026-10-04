# ADSI 1968, Table 10: population, incidence of suicidal deaths, volume of suicides and % distribution, States / UTs /
# cities (raw/adsi/1968/year_wise/suicides-1968.pdf, pages 6 and 8; printed pages 12-13; page 7 is a chart). Read from
# the page images; checked by scripts/check_handread.py. The table prints the estimated mid-year population "in '000";
# converted here to lakh (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column
# is not transcribed. "-" (nil) for Laccadives is 0.
KIND, YEAR, PUB = "suicide_incidence", 1968, "adsi"
SOURCE = "raw/adsi/1968/year_wise/suicides-1968.pdf"
PAGES = "6,8"
TITLE = 'Table 10: Population, incidence of suicidal deaths, volume of suicides and % distribution of suicidal deaths in States/U.Ts. and Cities, 1968'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3349, 415.53, 8.06],
  "Assam": [815, 147.42, 5.53],
  "Bihar": [2237, 550.9, 4.06],
  "Gujarat": [1723, 251.89, 6.84],
  "Haryana": [703, 95.0, 7.4],
  "Jammu & Kashmir": [43, 39.39, 1.09],
  "Kerala": [2921, 202.96, 14.38],
  "Madhya Pradesh": [2234, 388.23, 5.75],
  "Maharashtra": [3432, 476.73, 7.2],
  "Mysore": [3083, 279.85, 11.02],
  "Nagaland": [16, 4.18, 3.83],
  "Orissa": [2349, 206.74, 11.36],
  "Punjab": [301, 139.35, 2.16],
  "Rajasthan": [715, 248.68, 2.88],
  "Tamil Nadu": [5617, 381.74, 14.71],
  "Uttar Pradesh": [4471, 868.89, 5.15],
  "West Bengal": [5744, 425.91, 13.49],
  "TOTAL (STATES)": [39753, 5123.39, 7.76],
 },
 "U.Ts.": {
  "A & N Islands": [27, 0.86, 31.4],
  "Chandigarh": [10, 1.5, 6.67],
  "Dadra & Nagar Haveli": [32, 0.69, 46.38],
  "Delhi": [162, 38.45, 4.21],
  "Goa, Daman & Diu": [54, 6.75, 8.0],
  "Himachal Pradesh": [59, 34.32, 1.72],
  "Laccadives": [0, 0.27, None],
  "Manipur": [45, 10.35, 4.35],
  "Pondicherry": [277, 4.3, 64.42],
  "Tripura": [269, 14.24, 18.89],
  "TOTAL (U.TS.)": [935, 111.73, 8.37],
 },
 "Grand": {
  "GRAND TOTAL": [40688, 5235.12, 7.77],
 },
 "Cities": {
  "Ahmedabad": [158, 15.36, 10.29],
  "Bangalore": [128, 16.8, 7.62],
  "Bombay": [118, 53.68, 2.2],
  "Calcutta": [79, 31.09, 2.54],
  "Delhi": [152, 34.7, 4.38],
  "Hyderabad": [208, 13.5, 15.41],
  "Kanpur": [58, 12.39, 4.68],
  "Madras": [113, 20.09, 5.62],
  "TOTAL (CITIES)": [1014, 197.61, 5.13],
 },
}
