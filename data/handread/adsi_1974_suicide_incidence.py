# ADSI 1974, Table 5: incidence of suicides and volume of suicides per one lakh of population, States / U.Ts. /
# cities (raw/adsi/1974/year_wise/suicides-1974.pdf, pages 8-9; printed pages 24-25). Read from the page images;
# checked by scripts/check_handread.py. The table prints the estimated mid-year population "in 000"; converted here to
# lakh (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not
# transcribed. Lakshadweep "-" (nil) is 0.
KIND, YEAR, PUB = "suicide_incidence", 1974, "adsi"
SOURCE = "raw/adsi/1974/year_wise/suicides-1974.pdf"
PAGES = "8-9"
TITLE = 'Table 5: Incidence of Suicides and Volume of Suicides per one lakh of population during 1974'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Calcutta", "Estimated mid-year population (lakh)"): (33.26, 32.26, "printed 3326 (thousand); the cities' populations add to the printed Total (Cities) 23756 only with 3226, and the printed rate 1.15 = 37 / 32.26 (37 / 33.26 = 1.11); the 1974 errata sheet (raw/adsi/1974/year_wise/errata_2_1974.pdf, item 12: page 25, Table 5, Cities-4th, column 3) corrects 3326 to 3226"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3494, 462.92, 7.55],
  "Assam": [1501, 160.81, 9.33],
  "Bihar": [1081, 597.49, 1.81],
  "Gujarat": [1432, 289.15, 4.95],
  "Haryana": [691, 107.75, 6.41],
  "Himachal Pradesh": [49, 35.86, 1.37],
  "Jammu & Kashmir": [2, 49.27, 0.04],
  "Karnataka": [3453, 312.55, 11.05],
  "Kerala": [4015, 229.8, 17.47],
  "Madhya Pradesh": [4304, 450.63, 9.55],
  "Maharashtra": [3747, 540.94, 6.93],
  "Manipur": [11, 11.49, 0.96],
  "Meghalaya": [76, 10.82, 7.02],
  "Nagaland": [9, 5.41, 1.66],
  "Orissa": [2127, 234.55, 9.07],
  "Punjab": [571, 144.03, 3.96],
  "Rajasthan": [528, 277.79, 1.9],
  "Tamil Nadu": [5407, 438.6, 12.33],
  "Tripura": [426, 16.65, 25.59],
  "Uttar Pradesh": [3610, 932.58, 3.87],
  "West Bengal": [8904, 476.3, 18.69],
  "TOTAL (STATES)": [45438, 5785.39, 7.85],
 },
 "U.Ts.": {
  "A. & N. Islands": [85, 1.23, 69.11],
  "Arunachal Pradesh": [5, 5.01, 1.0],
  "Chandigarh": [5, 2.74, 1.82],
  "D. & N. Haveli": [6, 0.79, 7.59],
  "Delhi": [164, 47.18, 3.48],
  "Goa, Daman & Diu": [43, 9.18, 4.68],
  "Lakshadweep": [0, 0.34, 0.0],
  "Mizoram": [2, 3.65, 0.55],
  "Pondicherry": [260, 5.05, 51.49],
  "TOTAL (U.TS.)": [570, 75.17, 7.58],
 },
 "Grand": {
  "GRAND TOTAL": [46008, 5860.56, 7.85],
 },
 "Cities": {
  "Ahmedabad": [84, 17.8, 4.72],
  "Bangalore": [483, 17.16, 28.15],
  "Bombay": [144, 68.2, 2.11],
  "Calcutta": [37, 32.26, 1.15],
  "Delhi": [106, 42.94, 2.47],
  "Hyderabad": [227, 18.36, 12.36],
  "Kanpur": [89, 12.71, 7.0],
  "Madras": [549, 28.13, 19.52],
  "TOTAL (CITIES)": [1719, 237.56, 7.24],
 },
}
