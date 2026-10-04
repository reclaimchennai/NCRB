# ADSI 1980, Table II: incidence of suicides, volume of suicides per lakh of population, States / U.Ts. / cities
# (raw/adsi/1980/year_wise/suicides-1980.pdf, pages 5-6; printed pages 22-23). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in 1,000; converted here to lakh
# (thousands / 100). Rate = volume of suicides per 1,00,000 of population. The percentage column is not transcribed.
# Goa, Daman & Diu's population is printed "1.139" and the Grand Total count "41.663" (separator misprinted as a
# decimal point), read as 1139 and 41663.
KIND, YEAR, PUB = "suicide_incidence", 1980, "adsi"
SOURCE = "raw/adsi/1980/year_wise/suicides-1980.pdf"
PAGES = "5-6"
TITLE = 'Table II: Incidence of Suicides, Volume of Suicides per Lakh of Population during 1980'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [1905, 508.72, 3.74],
  "Assam": [1721, 195.49, 8.8],
  "Bihar": [424, 674.34, 0.63],
  "Gujarat": [1604, 326.15, 4.92],
  "Haryana": [340, 123.05, 2.76],
  "Himachal Pradesh": [98, 41.76, 2.35],
  "Jammu & Kashmir": [33, 58.84, 0.56],
  "Karnataka": [5759, 351.73, 16.37],
  "Kerala": [3813, 256.66, 14.86],
  "Madhya Pradesh": [2924, 523.1, 5.59],
  "Maharashtra": [2906, 601.45, 4.83],
  "Manipur": [12, 14.35, 0.84],
  "Meghalaya": [32, 12.99, 2.46],
  "Nagaland": [13, 7.0, 1.86],
  "Orissa": [2338, 267.23, 8.75],
  "Punjab": [267, 158.76, 1.68],
  "Rajasthan": [623, 329.16, 1.89],
  "Sikkim": [15, 2.51, 5.98],
  "Tamil Nadu": [4809, 469.18, 10.25],
  "Tripura": [321, 20.64, 15.55],
  "Uttar Pradesh": [3957, 1045.09, 3.79],
  "West Bengal": [7057, 551.63, 12.79],
  "TOTAL (STATES)": [40971, 6539.83, 6.26],
 },
 "U.Ts.": {
  "Andaman and Nicobar Islands": [45, 1.83, 24.59],
  "Arunachal Pradesh": [18, 6.23, 2.88],
  "Chandigarh": [10, 4.95, 2.02],
  "Dadra and Nagar Haveli": [9, 0.87, 10.34],
  "Delhi": [303, 60.21, 5.03],
  "Goa, Daman & Diu": [76, 11.39, 6.67],
  "Lakshadweep": [3, 0.36, 8.33],
  "Mizoram": [6, 4.44, 1.35],
  "Pondicherry": [222, 5.85, 37.95],
  "TOTAL (U.TS.)": [692, 96.13, 7.2],
 },
 "Grand": {
  "GRAND TOTAL": [41663, 6635.96, 6.28],
 },
 "Cities": {
  "Ahmedabad": [232, 21.41, 10.84],
  "Bangalore": [936, 20.4, 45.88],
  "Bombay": [202, 83.9, 2.41],
  "Calcutta": [23, 33.69, 0.68],
  "Delhi": [255, 54.88, 4.65],
  "Hyderabad": [87, 22.57, 3.85],
  "Kanpur": [143, 14.86, 9.62],
  "Madras": [263, 34.47, 7.63],
  "TOTAL (CITIES)": [2141, 286.18, 7.48],
 },
}
