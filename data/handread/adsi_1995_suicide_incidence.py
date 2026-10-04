# ADSI 1995, Table-2(S): incidence and rate of suicides during 1995 (State, UT & City-wise)
# (raw/adsi/1995/year_wise/suicides-1995.pdf, page 4; printed page 51). Read from the page image; checked by
# scripts/check_handread.py. The table prints the number of suicides, the percentage share (not transcribed), the
# estimated mid-year population already in lakh (one decimal) and the rate of suicides (col.3 / col.5) to two decimals
# (apparently worked from unrounded populations, so a recomputed rate can differ in the second decimal). Lakshadweep 0.
KIND, YEAR, PUB = "suicide_incidence", 1995, "adsi"
SOURCE = "raw/adsi/1995/year_wise/suicides-1995.pdf"
PAGES = "4"
TITLE = 'Table-2(S): Incidence And Rate of Suicides During 1995 (State, UT & City-wise)'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [6767, 717.1, 9.43],
  "Arunachal Pradesh": [57, 9.6, 5.93],
  "Assam": [1893, 246.1, 7.69],
  "Bihar": [968, 949.1, 1.01],
  "Goa": [246, 12.7, 19.37],
  "Gujarat": [4041, 446.1, 9.05],
  "Haryana": [1878, 180.7, 10.39],
  "Himachal Pradesh": [243, 56.1, 4.33],
  "Jammu & Kashmir": [44, 85.1, 0.51],
  "Karnataka": [11276, 480.5, 23.46],
  "Kerala": [8012, 309.1, 25.92],
  "Madhya Pradesh": [6843, 721.4, 9.48],
  "Maharashtra": [11866, 859.1, 13.81],
  "Manipur": [24, 20.3, 1.18],
  "Meghalaya": [57, 19.6, 2.9],
  "Mizoram": [31, 7.9, 3.92],
  "Nagaland": [22, 13.9, 1.58],
  "Orissa": [3070, 342.7, 8.95],
  "Punjab": [623, 216.0, 2.88],
  "Rajasthan": [3219, 482.1, 6.67],
  "Sikkim": [61, 4.7, 12.97],
  "Tamil Nadu": [8754, 582.9, 15.01],
  "Tripura": [595, 30.5, 19.5],
  "Uttar Pradesh": [4014, 1501.2, 2.67],
  "West Bengal": [12824, 732.7, 17.5],
  "TOTAL (STATES)": [87428, 9027.2, 9.68],
 },
 "U.Ts.": {
  "A & N Islands": [125, 3.3, 37.87],
  "Chandigarh": [51, 7.8, 6.53],
  "D & N Haveli": [25, 1.6, 15.62],
  "Daman & Diu": [12, 1.1, 10.9],
  "Delhi": [934, 109.7, 8.51],
  "Lakshadweep": [0, 0.6, 0.0],
  "Pondicherry": [603, 8.8, 68.52],
  "TOTAL (U.TS.)": [1750, 132.9, 13.16],
 },
 "Grand": {
  "GRAND TOTAL": [89178, 9160.1, 9.74],
 },
 "Cities": {
  "Ahmedabad": [399, 37.1, 10.75],
  "Bangalore": [1082, 48.0, 22.54],
  "Bhopal": [118, 13.3, 8.87],
  "Bombay": [1204, 151.4, 7.95],
  "Calcutta": [216, 119.2, 1.81],
  "Coimbatore": [192, 11.9, 16.13],
  "Delhi": [710, 99.5, 7.13],
  "Hyderabad": [371, 54.8, 6.77],
  "Indore": [404, 12.6, 32.06],
  "Jaipur": [228, 18.1, 12.59],
  "Kanpur": [288, 22.3, 12.91],
  "Kochi": [218, 14.2, 15.35],
  "Lucknow": [113, 20.8, 5.43],
  "Ludhiana": [49, 13.2, 3.71],
  "Madras": [1046, 60.0, 17.43],
  "Madurai": [128, 11.7, 10.94],
  "Nagpur": [495, 18.5, 26.75],
  "Patna": [48, 11.9, 4.03],
  "Pune": [369, 29.6, 12.46],
  "Surat": [222, 18.9, 11.74],
  "Vadodara": [135, 13.5, 10.0],
  "Varanasi": [228, 11.5, 19.82],
  "Vishakhapatnam": [141, 13.5, 10.44],
  "TOTAL (CITIES)": [8404, 825.5, 10.18],
 },
}
