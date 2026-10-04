# ADSI 1989, Table 7: incidence and volume of suicides during 1989 (State, UT & City-wise)
# (raw/adsi/1989/year_wise/suicides-1989.pdf, page 9; printed page 39). Read from the page image; checked by
# scripts/check_handread.py. The table prints the number of suicides, the percentage share (not transcribed), the
# estimated mid-year population already in lakh (one decimal) and the volume of suicides [col.3 / col.5] to one decimal.
# No total is printed for the cities. Pune's population is printed "J5.6" (a broken 1), read 15.6 (219 / 15.6 = 14.0,
# the printed rate).
KIND, YEAR, PUB = "suicide_incidence", 1989, "adsi"
SOURCE = "raw/adsi/1989/year_wise/suicides-1989.pdf"
PAGES = "9"
TITLE = 'Table 7: Incidence And Volume Of Suicides During 1989 (State, UT & City-wise)'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [5467, 624.4, 8.8],
  "Arunachal Pradesh": [54, 7.9, 6.8],
  "Assam": [2618, 240.9, 10.9],
  "Bihar": [991, 835.3, 1.2],
  "Goa": [175, 12.2, 14.3],
  "Gujarat": [2511, 399.5, 6.3],
  "Haryana": [1540, 159.3, 9.7],
  "Himachal Pradesh": [110, 49.7, 2.2],
  "Jammu & Kashmir": [50, 71.9, 0.7],
  "Karnataka": [7548, 440.4, 17.1],
  "Kerala": [7201, 293.7, 24.5],
  "Madhya Pradesh": [5160, 622.4, 8.3],
  "Maharashtra": [6765, 735.0, 9.2],
  "Manipur": [60, 17.4, 3.4],
  "Meghalaya": [86, 16.7, 5.1],
  "Mizoram": [29, 6.7, 4.3],
  "Nagaland": [13, 10.7, 1.2],
  "Orissa": [2737, 305.8, 9.0],
  "Punjab": [271, 194.1, 1.4],
  "Rajasthan": [1372, 427.4, 3.2],
  "Sikkim": [37, 4.3, 8.6],
  "Tamil Nadu": [8286, 551.8, 15.0],
  "Tripura": [594, 25.0, 23.8],
  "Uttar Pradesh": [2133, 1318.5, 1.6],
  "West Bengal": [11473, 640.6, 17.9],
  "TOTAL (STATES)": [67281, 8011.6, 8.4],
 },
 "U.Ts.": {
  "A & N Islands": [106, 2.7, 39.3],
  "Chandigarh": [57, 7.0, 8.1],
  "D & N Haveli": [34, 1.3, 26.2],
  "Daman & Diu": [3, 1.0, 3.0],
  "Delhi": [808, 86.9, 9.3],
  "Lakshadweep": [0, 0.5, 0.0],
  "Pondicherry": [455, 7.2, 63.2],
  "TOTAL (U.TS.)": [1463, 106.6, 13.7],
 },
 "Grand": {
  "GRAND TOTAL": [68744, 8118.2, 8.5],
 },
 "Cities": {
  "Ahmedabad": [354, 24.4, 14.5],
  "Bangalore": [1092, 35.9, 30.4],
  "Bombay": [616, 104.9, 5.9],
  "Calcutta": [73, 34.0, 2.1],
  "Delhi": [678, 82.4, 8.2],
  "Hyderabad": [400, 25.3, 15.8],
  "Jaipur": [126, 14.3, 8.8],
  "Kanpur": [147, 18.2, 8.1],
  "Lucknow": [55, 10.3, 5.3],
  "Madras": [1568, 41.2, 38.1],
  "Nagpur": [135, 15.8, 8.5],
  "Pune": [219, 15.6, 14.0],
 },
}
