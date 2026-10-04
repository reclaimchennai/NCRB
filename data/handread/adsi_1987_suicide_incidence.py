# ADSI 1987, Table II: incidence of suicides, population and volume of suicides per lakh of population, States / UTs /
# cities (raw/adsi/1987/year_wise/suicides-87.pdf, pages 4 and 6, page 5 being a chart; printed pages 18-19). Read from
# the page images; checked by scripts/check_handread.py. The table prints the number of suicides, the percentage (not
# transcribed), the population in (000) and the volume per lakh; population converted here to lakh (thousands / 100).
# The All India population is printed "78,1374" (comma misplaced), read 781374 thousand (the States and UTs add to it).
# Pune's rate is printed "11.0" (162 / 14.73 = 11.00). Goa is printed among the States, Daman & Diu among the UTs.
KIND, YEAR, PUB = "suicide_incidence", 1987, "adsi"
SOURCE = "raw/adsi/1987/year_wise/suicides-87.pdf"
PAGES = "4-6"
TITLE = 'Table-II: Incidence Of Suicides, Population and Volume Of Suicides Per Lakh Of Population During The Year-1987'
CHECK = "incidence"
CATS = ["Number of suicides", "Population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [4371, 602.88, 7.25],
  "Arunachal Pradesh": [44, 7.54, 5.84],
  "Assam": [2214, 230.12, 9.62],
  "Bihar": [769, 800.02, 0.96],
  "Goa": [130, 11.75, 11.06],
  "Gujarat": [2104, 386.17, 5.45],
  "Haryana": [852, 152.87, 5.57],
  "Himachal Pradesh": [115, 48.12, 2.39],
  "Jammu & Kashmir": [73, 68.96, 1.06],
  "Karnataka": [5837, 424.25, 13.76],
  "Kerala": [6726, 284.75, 23.62],
  "Madhya Pradesh": [4181, 598.13, 6.99],
  "Maharashtra": [5051, 713.33, 7.08],
  "Manipur": [62, 16.61, 3.73],
  "Meghalaya": [35, 15.88, 2.2],
  "Mizoram": [24, 6.29, 3.82],
  "Nagaland": [8, 9.96, 0.8],
  "Orissa": [2508, 295.47, 8.49],
  "Punjab": [283, 189.08, 1.5],
  "Rajasthan": [1196, 405.85, 2.95],
  "Sikkim": [25, 3.98, 6.28],
  "Tamil Nadu": [9248, 536.53, 17.24],
  "Tripura": [540, 23.95, 22.55],
  "Uttar Pradesh": [2147, 1264.78, 1.7],
  "West Bengal": [8954, 617.72, 14.5],
  "TOTAL (STATES)": [57497, 7714.99, 7.45],
 },
 "U.Ts.": {
  "A & N Islands": [77, 2.53, 30.44],
  "Chandigarh": [31, 6.32, 4.91],
  "D & N Haveli": [28, 1.22, 23.0],
  "Daman & Diu": [3, 0.88, 3.41],
  "Delhi": [501, 80.39, 6.23],
  "Lakshadweep": [2, 0.44, 4.55],
  "Pondicherry": [429, 6.97, 61.55],
  "TOTAL (U.TS.)": [1071, 98.75, 10.85],
 },
 "Grand": {
  "GRAND TOTAL": [58568, 7813.74, 7.5],
 },
 "Cities": {
  "Ahmedabad": [196, 23.56, 8.32],
  "Bangalore": [833, 32.9, 25.32],
  "Bombay": [546, 99.78, 5.47],
  "Calcutta": [117, 33.63, 3.48],
  "Delhi": [373, 75.83, 4.92],
  "Hyderabad": [204, 24.26, 8.41],
  "Jaipur": [85, 13.0, 6.54],
  "Kanpur": [80, 17.22, 4.65],
  "Lucknow": [78, 9.95, 7.84],
  "Madras": [936, 39.14, 23.91],
  "Nagpur": [152, 14.95, 10.17],
  "Pune": [162, 14.73, 11.0],
  "TOTAL (CITIES)": [3762, 398.95, 9.43],
 },
}
