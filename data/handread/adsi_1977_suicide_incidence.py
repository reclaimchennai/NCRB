# ADSI 1977, Table 2: incidence of suicides, volume of suicides per lakh of population, States / U.Ts. / cities
# (raw/adsi/1977/year_wise/suicides-1977.pdf, pages 5-6; printed pages 23-24). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in '000; converted here to lakh
# (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not transcribed.
# Lakshadweep ".." (nil) is 0. A. & N. Islands' rate prints "20.0" with a faint last digit, read 20.00 (32 / 1.60).
KIND, YEAR, PUB = "suicide_incidence", 1977, "adsi"
SOURCE = "raw/adsi/1977/year_wise/suicides-1977.pdf"
PAGES = "5-6"
TITLE = 'Table 2: Incidence of suicides, volume of suicides per lakh of population during 1977'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3149, 484.93, 6.49],
  "Assam": [1755, 178.59, 9.83],
  "Bihar": [652, 637.78, 1.02],
  "Gujarat": [1266, 306.3, 4.13],
  "Haryana": [477, 115.11, 4.14],
  "Himachal Pradesh": [139, 39.42, 3.53],
  "Jammu & Kashmir": [12, 54.56, 0.22],
  "Karnataka": [4458, 332.28, 13.42],
  "Kerala": [3697, 243.41, 15.19],
  "Madhya Pradesh": [2119, 490.83, 4.32],
  "Maharashtra": [3372, 570.57, 5.91],
  "Manipur": [5, 13.11, 0.38],
  "Meghalaya": [40, 12.0, 3.33],
  "Nagaland": [4, 6.37, 0.63],
  "Orissa": [1963, 251.5, 7.81],
  "Punjab": [260, 150.67, 1.73],
  "Rajasthan": [494, 305.31, 1.62],
  "Sikkim": [6, 2.39, 2.51],
  "Tamil Nadu": [4141, 450.98, 9.18],
  "Tripura": [383, 18.91, 20.25],
  "Uttar Pradesh": [2253, 990.1, 2.28],
  "West Bengal": [8328, 517.39, 16.1],
  "TOTAL (STATES)": [38973, 6172.51, 6.31],
 },
 "U.Ts.": {
  "A. & N. Islands": [32, 1.6, 20.0],
  "Arunachal Pradesh": [5, 5.71, 0.88],
  "Chandigarh": [20, 4.05, 4.94],
  "D. N. Haveli": [25, 0.83, 30.12],
  "Delhi": [245, 53.21, 4.6],
  "Goa, Daman & Diu": [73, 10.43, 7.0],
  "Lakshadweep": [0, 0.34, 0.0],
  "Mizoram": [11, 4.06, 2.71],
  "Pondicherry": [334, 5.48, 60.95],
  "TOTAL (U.TS.)": [745, 85.71, 8.69],
 },
 "Grand": {
  "GRAND TOTAL": [39718, 6258.22, 6.35],
 },
 "Cities": {
  "Ahmedabad": [142, 19.61, 7.24],
  "Bangalore": [289, 18.78, 15.39],
  "Bombay": [192, 76.05, 2.52],
  "Calcutta": [40, 32.97, 1.21],
  "Delhi": [218, 48.91, 4.46],
  "Hyderabad": [147, 20.46, 7.18],
  "Kanpur": [36, 13.78, 2.61],
  "Madras": [251, 31.3, 8.02],
  "TOTAL (CITIES)": [1315, 261.86, 5.02],
 },
}
