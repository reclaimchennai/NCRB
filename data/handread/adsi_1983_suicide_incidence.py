# ADSI 1983, Table II: incidence of suicides, volume of suicides per lakh of population, States / UTs / cities
# (raw/adsi/1983/year_wise/suicides-1983.pdf, pages 4-5; printed pages 20-21). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in 1000 first, then the number of
# suicides; converted here to lakh (thousands / 100). Rate = volume of suicides per lakh of population. The percentage
# column is not transcribed. Lucknow's count and rate are N.A. (row kept with None, so it is left out of the data; the
# cities' count total excludes it).
KIND, YEAR, PUB = "suicide_incidence", 1983, "adsi"
SOURCE = "raw/adsi/1983/year_wise/suicides-1983.pdf"
PAGES = "4-5"
TITLE = 'Table II: Incidence of Suicides, Volume of Suicides per Lakh of Population during 1983'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3383, 560.35, 6.04],
  "Assam": [2436, 210.69, 11.57],
  "Bihar": [754, 735.02, 1.03],
  "Gujarat": [1775, 358.13, 4.96],
  "Haryana": [594, 137.87, 4.31],
  "Himachal Pradesh": [166, 44.79, 3.71],
  "Jammu & Kashmir": [41, 62.98, 0.66],
  "Karnataka": [4730, 391.17, 12.1],
  "Kerala": [5241, 265.33, 19.76],
  "Madhya Pradesh": [3157, 549.13, 5.75],
  "Maharashtra": [3744, 660.5, 5.67],
  "Manipur": [53, 15.08, 3.52],
  "Meghalaya": [24, 14.27, 1.69],
  "Nagaland": [4, 8.55, 0.47],
  "Orissa": [2405, 274.88, 8.75],
  "Punjab": [311, 176.31, 1.77],
  "Rajasthan": [1044, 365.45, 2.86],
  "Sikkim": [34, 3.46, 9.83],
  "Tamil Nadu": [5362, 502.78, 10.67],
  "Tripura": [499, 21.84, 22.85],
  "Uttar Pradesh": [2503, 1165.67, 2.15],
  "West Bengal": [7316, 571.95, 12.8],
  "TOTAL (STATES)": [45576, 7096.2, 6.43],
 },
 "U.Ts.": {
  "A & N Islands": [49, 2.11, 23.23],
  "Arunachal Pradesh": [33, 6.75, 4.89],
  "Chandigarh": [18, 5.14, 3.51],
  "D & N Haveli": [31, 1.11, 27.93],
  "Delhi": [432, 68.52, 6.31],
  "Goa, Daman & Diu": [99, 11.47, 8.64],
  "Lakshadweep": [1, 0.41, 2.44],
  "Mizoram": [17, 5.44, 3.13],
  "Pondicherry": [323, 6.38, 50.63],
  "TOTAL (U.TS.)": [1003, 107.33, 9.35],
 },
 "Grand": {
  "GRAND TOTAL": [46579, 7203.53, 6.47],
 },
 "Cities": {
  "Ahmedabad": [213, 21.71, 9.82],
  "Bangalore": [754, 27.54, 27.38],
  "Bombay": [297, 88.86, 3.35],
  "Calcutta": [57, 33.3, 1.72],
  "Delhi": [382, 53.12, 7.2],
  "Hyderabad": [253, 22.15, 11.43],
  "Jaipur": [54, 10.86, 4.98],
  "Kanpur": [91, 15.64, 5.82],
  "Lucknow": [None, 9.3, None],
  "Madras": [898, 35.03, 25.64],
  "Nagpur": [246, 13.2, 18.64],
  "Pune": [139, 13.02, 10.68],
  "TOTAL (CITIES)": [3384, 343.73, 9.85],
 },
}
