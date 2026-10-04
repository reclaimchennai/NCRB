# ADSI 1985, Table II: incidence of suicides, volume of suicides per lakh of population, States / UTs / cities
# (raw/adsi/1985/year_wise/suicides-1985.pdf, pages 6-7; printed pages 27-28). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in (000); converted here to lakh
# (thousands / 100). Rate = volume of suicides per lakh of population. The percentage column is not transcribed.
# Lakshadweep "-" (nil) is 0. Two figures have one faint digit: Orissa's population "28,_16", read 28516 (the States
# add to the printed Total 7,39,292 with it, and 2342 / 285.16 = 8.21, the printed rate), and the Total (States) count
# "51,_62", read 51762 (the States add to it, and 51762 + 1049 = the printed Grand Total 52,811).
KIND, YEAR, PUB = "suicide_incidence", 1985, "adsi"
SOURCE = "raw/adsi/1985/year_wise/suicides-1985.pdf"
PAGES = "6-7"
TITLE = 'Table II: Incidence Of Suicides, Volume Of Suicides per Lakh Of Population During 1985'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [4021, 581.48, 6.92],
  "Assam": [1845, 220.08, 8.38],
  "Bihar": [788, 766.59, 1.03],
  "Gujarat": [1899, 372.36, 5.1],
  "Haryana": [860, 145.68, 5.9],
  "Himachal Pradesh": [90, 46.48, 1.94],
  "Jammu & Kashmir": [32, 65.99, 0.49],
  "Karnataka": [4776, 407.78, 11.71],
  "Kerala": [6075, 275.27, 22.07],
  "Madhya Pradesh": [3448, 573.66, 6.01],
  "Maharashtra": [4758, 688.54, 6.91],
  "Manipur": [27, 15.86, 1.7],
  "Meghalaya": [36, 15.09, 2.39],
  "Nagaland": [17, 9.24, 1.84],
  "Orissa": [2342, 285.16, 8.21],
  "Punjab": [350, 183.13, 1.91],
  "Rajasthan": [913, 385.18, 2.37],
  "Sikkim": [25, 3.72, 6.72],
  "Tamil Nadu": [7798, 520.16, 15.0],
  "Tripura": [461, 22.91, 20.12],
  "Uttar Pradesh": [2690, 1213.79, 2.22],
  "West Bengal": [8511, 594.77, 14.31],
  "TOTAL (STATES)": [51762, 7392.92, 7.0],
 },
 "U.Ts.": {
  "A & N Islands": [65, 2.32, 28.02],
  "Arunachal Pradesh": [41, 7.15, 5.74],
  "Chandigarh": [26, 5.71, 4.55],
  "D & N Haveli": [13, 1.16, 11.21],
  "Delhi": [442, 74.28, 5.95],
  "Goa, Daman & Diu": [111, 12.07, 9.2],
  "Lakshadweep": [0, 0.43, 0.0],
  "Mizoram": [17, 5.87, 2.9],
  "Pondicherry": [334, 6.68, 50.0],
  "TOTAL (U.TS.)": [1049, 115.67, 9.07],
 },
 "Grand": {
  "GRAND TOTAL": [52811, 7508.59, 7.03],
 },
 "Cities": {
  "Ahmedabad": [171, 22.64, 7.55],
  "Bangalore": [461, 30.12, 15.31],
  "Bombay": [423, 94.4, 4.48],
  "Calcutta": [128, 33.48, 3.82],
  "Delhi": [410, 56.88, 7.21],
  "Hyderabad": [184, 23.2, 7.93],
  "Jaipur": [45, 11.88, 3.79],
  "Kanpur": [255, 16.39, 15.56],
  "Lucknow": [72, 9.61, 7.49],
  "Madras": [718, 37.06, 19.37],
  "Nagpur": [194, 14.08, 13.78],
  "Pune": [165, 13.89, 11.88],
  "TOTAL (CITIES)": [3226, 363.63, 8.87],
 },
}
