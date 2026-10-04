# ADSI 1986, Table II: incidence of suicides, percentage of suicides to total, estimated mid-year population and volume
# of suicides per lakh of population, States / UTs / cities (raw/adsi/1986/year_wise/suicides-1986.pdf, pages 5-6;
# printed pages 17-18). Read from the page images; checked by scripts/check_handread.py. The table prints the number of
# suicides, the percentage (not transcribed), the estimated mid-year population in (000) and the volume per lakh;
# population converted here to lakh (thousands / 100). Lakshadweep "-" (nil) is 0. Arunachal Pradesh and Mizoram are
# printed among the States; Goa, Daman & Diu among the UTs.
KIND, YEAR, PUB = "suicide_incidence", 1986, "adsi"
SOURCE = "raw/adsi/1986/year_wise/suicides-1986.pdf"
PAGES = "5-6"
TITLE = 'Table II: Incidence Of Suicides, Volume Of Suicides Per Lakh Of Population During The Year 1986'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3992, 592.16, 6.74],
  "Arunachal Pradesh": [49, 7.34, 6.68],
  "Assam": [2381, 225.02, 10.58],
  "Bihar": [374, 783.08, 0.48],
  "Gujarat": [2180, 379.33, 5.75],
  "Haryana": [884, 149.37, 5.92],
  "Himachal Pradesh": [98, 47.3, 2.07],
  "Jammu & Kashmir": [58, 67.48, 0.86],
  "Karnataka": [4612, 416.04, 11.09],
  "Kerala": [6135, 280.08, 21.9],
  "Madhya Pradesh": [3478, 585.92, 5.94],
  "Maharashtra": [5249, 701.38, 7.48],
  "Manipur": [23, 16.24, 1.42],
  "Meghalaya": [36, 15.49, 2.32],
  "Mizoram": [28, 6.08, 4.61],
  "Nagaland": [21, 9.6, 2.19],
  "Orissa": [2828, 290.32, 9.74],
  "Punjab": [361, 186.22, 1.94],
  "Rajasthan": [1173, 395.4, 2.97],
  "Sikkim": [41, 3.85, 10.65],
  "Tamil Nadu": [8232, 528.49, 15.58],
  "Tripura": [430, 23.43, 18.35],
  "Uttar Pradesh": [2358, 1238.92, 1.9],
  "West Bengal": [8107, 606.25, 13.37],
  "TOTAL (STATES)": [53128, 7554.79, 7.03],
 },
 "U.Ts.": {
  "A & N Islands": [73, 2.43, 30.04],
  "Chandigarh": [29, 6.01, 4.83],
  "D & N Haveli": [35, 1.19, 29.41],
  "Delhi": [638, 77.3, 8.25],
  "Goa, Daman & Diu": [118, 12.36, 9.55],
  "Lakshadweep": [0, 0.44, 0.0],
  "Pondicherry": [336, 6.83, 49.19],
  "TOTAL (U.TS.)": [1229, 106.56, 11.53],
 },
 "Grand": {
  "GRAND TOTAL": [54357, 7661.35, 7.09],
 },
 "Cities": {
  "Ahmedabad": [201, 23.1, 8.7],
  "Bangalore": [590, 31.48, 18.74],
  "Bombay": [481, 97.13, 4.95],
  "Calcutta": [126, 33.56, 3.75],
  "Delhi": [519, 72.72, 7.14],
  "Hyderabad": [284, 23.73, 11.97],
  "Jaipur": [90, 12.43, 7.24],
  "Kanpur": [120, 16.8, 7.14],
  "Lucknow": [118, 9.77, 12.08],
  "Madras": [825, 38.1, 21.65],
  "Nagpur": [192, 14.52, 13.22],
  "Pune": [150, 14.32, 10.47],
  "TOTAL (CITIES)": [3696, 387.66, 9.53],
 },
}
