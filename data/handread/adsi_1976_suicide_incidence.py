# ADSI 1976, Table 5: incidence of suicides, volume of suicides per lakh of population, States / U.Ts. / cities
# (raw/adsi/1976/year_wise/suicides-1976.pdf, pages 9-10; printed pages 27-28). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in '000; converted here to lakh
# (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not transcribed.
# Andhra Pradesh's population is printed "4,7944" (comma misplaced), read as 47944.
KIND, YEAR, PUB = "suicide_incidence", 1976, "adsi"
SOURCE = "raw/adsi/1976/year_wise/suicides-1976.pdf"
PAGES = "9-10"
TITLE = 'Table 5: Incidence of suicides, volume of suicides per lakh of Population during 1976'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [4219, 479.44, 8.8],
  "Assam": [1213, 169.69, 7.15],
  "Bihar": [613, 617.9, 1.0],
  "Gujarat": [1476, 302.69, 4.88],
  "Haryana": [647, 112.21, 5.77],
  "Himachal Pradesh": [74, 36.67, 2.02],
  "Jammu & Kashmir": [49, 51.2, 0.96],
  "Karnataka": [4278, 324.48, 13.18],
  "Kerala": [3557, 239.55, 14.85],
  "Madhya Pradesh": [2301, 471.67, 4.88],
  "Maharashtra": [3903, 563.41, 6.93],
  "Manipur": [11, 11.95, 0.92],
  "Meghalaya": [42, 11.25, 3.73],
  "Nagaland": [5, 5.57, 0.9],
  "Orissa": [1947, 243.91, 7.99],
  "Punjab": [281, 149.54, 1.88],
  "Rajasthan": [593, 290.05, 2.04],
  "Sikkim": [12, 2.33, 5.15],
  "Tamil Nadu": [4822, 454.34, 10.61],
  "Tripura": [425, 17.31, 24.55],
  "Uttar Pradesh": [2613, 961.72, 2.72],
  "West Bengal": [7665, 497.88, 15.4],
  "TOTAL (STATES)": [40746, 6014.76, 6.77],
 },
 "U.Ts.": {
  "A & N Islands": [71, 1.28, 55.47],
  "Arunachal Pradesh": [8, 5.2, 1.54],
  "Chandigarh": [21, 2.85, 7.37],
  "D & N Haveli": [17, 0.83, 20.48],
  "Delhi": [240, 51.16, 4.69],
  "Goa, Daman & Diu": [76, 9.54, 7.97],
  "Lakshadweep": [1, 0.36, 2.78],
  "Mizoram": [7, 3.85, 1.82],
  "Pondicherry": [228, 5.24, 43.51],
  "TOTAL (U.TS.)": [669, 80.31, 8.33],
 },
 "Grand": {
  "GRAND TOTAL": [41415, 6095.07, 6.79],
 },
 "Cities": {
  "Ahmedabad": [115, 19.01, 6.05],
  "Bangalore": [323, 18.24, 17.71],
  "Bombay": [209, 73.44, 2.85],
  "Calcutta": [44, 32.74, 1.34],
  "Delhi": [180, 45.92, 3.92],
  "Hyderabad": [103, 19.76, 5.21],
  "Kanpur": [39, 13.42, 2.91],
  "Madras": [335, 30.24, 11.08],
  "TOTAL (CITIES)": [1348, 252.77, 5.33],
 },
}
