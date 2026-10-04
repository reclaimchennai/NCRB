# ADSI 1990, Table 7: incidence and volume of suicides during 1990 (State, UT & City-wise)
# (raw/adsi/1990/year_wise/suicides-1990.pdf, page 10; printed page 27). Read from the page image; checked by
# scripts/check_handread.py. The table prints the number of suicides, the percentage share (not transcribed), the
# estimated mid-year population already in lakh (one decimal) and the volume of suicides (col.3 / col.5) to one decimal.
# No total is printed for the cities. The Total (States) rate is printed 9.0 though 72398 / 8159.9 = 8.87; left as
# printed (the States' counts add to 72398 and the All India rate 8.9 is consistent).
# The States' populations as printed add to 8160.0 lakh against the printed Total (States) 8159.9 (rounding of
# the one-decimal figures); left as printed.
KIND, YEAR, PUB = "suicide_incidence", 1990, "adsi"
SOURCE = "raw/adsi/1990/year_wise/suicides-1990.pdf"
PAGES = "10"
TITLE = 'Table 7: Incidence And Volume Of Suicides During 1990 (State, UT & City-wise)'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [5666, 635.1, 8.9],
  "Arunachal Pradesh": [40, 8.1, 4.9],
  "Assam": [2323, 246.4, 9.4],
  "Bihar": [1428, 853.4, 1.7],
  "Goa": [221, 12.4, 17.8],
  "Gujarat": [2688, 405.8, 6.6],
  "Haryana": [1375, 162.4, 8.5],
  "Himachal Pradesh": [134, 50.5, 2.7],
  "Jammu & Kashmir": [63, 73.4, 0.9],
  "Karnataka": [8040, 448.3, 17.9],
  "Kerala": [7845, 298.1, 26.3],
  "Madhya Pradesh": [5609, 634.5, 8.8],
  "Maharashtra": [7773, 745.6, 10.4],
  "Manipur": [59, 17.7, 3.3],
  "Meghalaya": [30, 17.1, 1.8],
  "Mizoram": [22, 7.0, 3.1],
  "Nagaland": [35, 11.1, 3.2],
  "Orissa": [2911, 311.0, 9.4],
  "Punjab": [387, 196.5, 2.0],
  "Rajasthan": [1611, 438.5, 3.7],
  "Sikkim": [38, 4.4, 8.6],
  "Tamil Nadu": [8632, 559.2, 15.4],
  "Tripura": [616, 25.5, 24.2],
  "Uttar Pradesh": [3127, 1346.1, 2.3],
  "West Bengal": [11725, 651.9, 18.0],
  "TOTAL (STATES)": [72398, 8159.9, 9.0],
 },
 "U.Ts.": {
  "A & N Islands": [114, 2.9, 39.3],
  "Chandigarh": [47, 7.3, 6.4],
  "D & N Haveli": [32, 1.3, 24.6],
  "Daman & Diu": [10, 1.0, 10.0],
  "Delhi": [832, 90.2, 9.2],
  "Lakshadweep": [1, 0.5, 2.0],
  "Pondicherry": [477, 7.4, 64.5],
  "TOTAL (U.TS.)": [1513, 110.6, 13.7],
 },
 "Grand": {
  "GRAND TOTAL": [73911, 8270.5, 8.9],
 },
 "Cities": {
  "Ahmedabad": [345, 24.9, 13.9],
  "Bangalore": [1184, 37.5, 31.6],
  "Bombay": [743, 107.5, 6.9],
  "Calcutta": [121, 34.7, 3.5],
  "Delhi": [728, 85.8, 8.5],
  "Hyderabad": [392, 25.9, 15.1],
  "Jaipur": [144, 14.9, 9.7],
  "Kanpur": [347, 18.6, 18.7],
  "Lucknow": [237, 10.5, 22.6],
  "Madras": [729, 42.3, 17.2],
  "Nagpur": [395, 16.2, 24.4],
  "Pune": [245, 16.0, 15.3],
 },
}
