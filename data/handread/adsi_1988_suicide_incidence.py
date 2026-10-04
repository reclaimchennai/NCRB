# ADSI 1988, Table II: incidence of suicides, population and volume of suicides per lakh of population, States / UTs /
# cities (raw/adsi/1988/year_wise/suicides-1988.pdf, pages 4-5; printed pages 21-22). Read from the page images; checked
# by scripts/check_handread.py. The table prints the number of suicides, the percentage (not transcribed), the estimated
# mid-year population in (000) and the volume per lakh (to one decimal); population converted here to lakh
# (thousands / 100). Uttar Pradesh's population is printed "12,9,137" (commas misplaced), read 129137 thousand (the
# States add to within 3 of the printed Total with it). Daman & Diu "-" (nil) is 0. The States' populations as read
# (clear at zoom 7) add to 786338 thousand against the printed Total (States) 7,86,335, which with the UTs' 10,261 gives
# the printed All India 7,96,596; the 3 thousand difference is left as printed (the rates, to one decimal, cannot locate
# it).
KIND, YEAR, PUB = "suicide_incidence", 1988, "adsi"
SOURCE = "raw/adsi/1988/year_wise/suicides-1988.pdf"
PAGES = "4-5"
TITLE = 'Table-II: Incidence Of Suicides, Population And Volume Of Suicides Per Lakh Of Population During The Year-1988'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [4770, 613.61, 7.8],
  "Arunachal Pradesh": [41, 7.74, 5.3],
  "Assam": [2367, 235.42, 10.1],
  "Bihar": [734, 817.42, 0.9],
  "Goa": [147, 11.96, 12.3],
  "Gujarat": [2227, 392.9, 5.7],
  "Haryana": [909, 156.19, 5.8],
  "Himachal Pradesh": [120, 48.93, 2.5],
  "Jammu & Kashmir": [35, 70.44, 0.5],
  "Karnataka": [6761, 432.36, 15.6],
  "Kerala": [7145, 289.3, 24.7],
  "Madhya Pradesh": [4573, 610.27, 7.5],
  "Maharashtra": [6005, 724.42, 8.3],
  "Manipur": [59, 17.0, 3.5],
  "Meghalaya": [38, 16.27, 2.3],
  "Mizoram": [25, 6.51, 3.8],
  "Nagaland": [6, 10.34, 0.6],
  "Orissa": [2543, 300.63, 8.5],
  "Punjab": [657, 191.69, 3.4],
  "Rajasthan": [1451, 416.51, 3.5],
  "Sikkim": [31, 4.12, 7.5],
  "Tamil Nadu": [9720, 544.29, 17.9],
  "Tripura": [517, 24.49, 21.1],
  "Uttar Pradesh": [2309, 1291.37, 1.8],
  "West Bengal": [9868, 629.2, 15.7],
  "TOTAL (STATES)": [63058, 7863.35, 8.0],
 },
 "U.Ts.": {
  "A & N Islands": [97, 2.64, 36.7],
  "Chandigarh": [47, 6.65, 7.1],
  "D & N Haveli": [35, 1.25, 28.0],
  "Daman & Diu": [0, 0.94, 0.0],
  "Delhi": [630, 83.57, 7.5],
  "Lakshadweep": [3, 0.45, 6.7],
  "Pondicherry": [400, 7.11, 56.3],
  "TOTAL (U.TS.)": [1212, 102.61, 11.8],
 },
 "Grand": {
  "GRAND TOTAL": [64270, 7965.96, 8.1],
 },
 "Cities": {
  "Ahmedabad": [218, 24.0, 9.1],
  "Bangalore": [881, 34.38, 25.6],
  "Bombay": [609, 102.37, 6.0],
  "Calcutta": [106, 33.7, 3.2],
  "Delhi": [505, 79.04, 6.4],
  "Hyderabad": [323, 24.79, 13.0],
  "Jaipur": [60, 13.61, 4.4],
  "Kanpur": [103, 17.68, 5.8],
  "Lucknow": [79, 10.14, 7.8],
  "Madras": [885, 40.17, 22.0],
  "Nagpur": [171, 15.36, 11.1],
  "Pune": [227, 15.14, 15.0],
  "TOTAL (CITIES)": [4167, 410.38, 10.2],
 },
}
