# ADSI 1973, Table 5: incidence of suicides and volume of suicides per one lakh of population, States / UTs / cities
# (raw/adsi/1973/year_wise/suicides-1973.pdf, pages 8-9). Read from the page images; checked by scripts/check_handread.py.
# The table prints the estimated mid-year population in (000) first, then the number of suicides; converted here to lakh
# (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not transcribed.
# Lakshadweep "-" (nil) is 0. Only 8 cities are printed.
KIND, YEAR, PUB = "suicide_incidence", 1973, "adsi"
SOURCE = "raw/adsi/1973/year_wise/suicides-1973.pdf"
PAGES = "8-9"
TITLE = 'Table 5: Incidence of Suicides and Volume of Suicides per one lakh of population during 1973'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3386, 454.28, 7.45],
  "Assam": [1483, 156.29, 9.49],
  "Bihar": [1296, 586.96, 2.21],
  "Gujarat": [1540, 282.27, 5.46],
  "Haryana": [727, 105.46, 6.89],
  "Himachal Pradesh": [87, 35.47, 2.45],
  "Jammu & Kashmir": [40, 48.31, 0.83],
  "Karnataka": [3755, 306.46, 12.25],
  "Kerala": [4456, 224.74, 19.83],
  "Madhya Pradesh": [2234, 440.1, 5.07],
  "Maharashtra": [3280, 529.5, 6.19],
  "Manipur": [13, 11.26, 1.15],
  "Meghalaya": [16, 10.59, 1.51],
  "Nagaland": [5, 5.33, 0.94],
  "Orissa": [2047, 229.89, 8.9],
  "Punjab": [196, 141.36, 1.39],
  "Rajasthan": [445, 271.54, 1.64],
  "Tamil Nadu": [4337, 430.35, 10.08],
  "Tripura": [355, 16.31, 21.77],
  "Uttar Pradesh": [3966, 917.32, 4.32],
  "West Bengal": [6577, 465.84, 14.12],
  "TOTAL (STATES)": [40241, 5669.63, 7.1],
 },
 "U.Ts.": {
  "A. & N. Islands": [66, 1.2, 55.0],
  "Arunachal Pradesh": [6, 4.9, 1.22],
  "Chandigarh": [5, 2.68, 1.87],
  "Dadra & Nagar Haveli": [29, 0.78, 37.18],
  "Delhi": [101, 45.15, 2.24],
  "Goa, Daman & Diu": [45, 8.99, 5.01],
  "Lakshadweep": [0, 0.34, 0.0],
  "Mizoram": [1, 3.55, 0.28],
  "Pondicherry": [313, 4.94, 63.36],
  "TOTAL (U.TS.)": [566, 72.53, 7.8],
 },
 "Grand": {
  "GRAND TOTAL": [40807, 5742.16, 7.11],
 },
 "Cities": {
  "Ahmedabad": [84, 17.21, 4.88],
  "Bangalore": [440, 16.62, 26.47],
  "Bombay": [144, 65.59, 2.2],
  "Calcutta": [31, 32.02, 0.97],
  "Delhi": [90, 40.95, 2.2],
  "Hyderabad": [87, 17.65, 4.93],
  "Kanpur": [31, 12.35, 2.51],
  "Madras": [307, 27.07, 11.34],
  "TOTAL (CITIES)": [1214, 229.46, 5.29],
 },
}
