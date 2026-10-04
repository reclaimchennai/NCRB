# ADSI 1978, Table II: incidence of suicides, volume of suicides per lakh of population, States / U.Ts. / cities
# (raw/adsi/1978/year_wise/suicides-1978.pdf, pages 5-6; printed pages 21-22). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in (000); converted here to lakh
# (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not transcribed.
# Madras' population has a blotted last digit, read 3236: the cities add to the printed total 26999 with it, and
# 148 / 32.36 = 4.57 (printed rate).
KIND, YEAR, PUB = "suicide_incidence", 1978, "adsi"
SOURCE = "raw/adsi/1978/year_wise/suicides-1978.pdf"
PAGES = "5-6"
TITLE = 'Table II: Incidence of Suicides, Volume of Suicides per lakh of population during 1978'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Andhra Pradesh", "Rate of suicides per lakh"): (6.49, None, "printed 6.49 (also on the chart, page 4; the same figure as 1977's); the count 2881 is confirmed by the States total (39518) and its share (7.2% of 40207), and the population 49282 thousand by the States population total, and 2881 / 492.82 = 5.85, so the printed rate is a misprint; left unread"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2881, 492.82, None],
  "Assam": [1979, 184.11, 10.75],
  "Bihar": [1199, 649.95, 1.84],
  "Gujarat": [1974, 312.91, 6.31],
  "Haryana": [492, 117.72, 4.18],
  "Himachal Pradesh": [57, 40.2, 1.42],
  "Jammu & Kashmir": [40, 55.97, 0.71],
  "Karnataka": [4892, 338.77, 14.44],
  "Kerala": [3590, 247.87, 14.48],
  "Madhya Pradesh": [2381, 501.6, 4.75],
  "Maharashtra": [3162, 580.95, 5.44],
  "Manipur": [9, 13.52, 0.67],
  "Meghalaya": [53, 12.33, 4.3],
  "Nagaland": [8, 6.58, 1.22],
  "Orissa": [1457, 256.78, 5.67],
  "Punjab": [266, 153.36, 1.73],
  "Rajasthan": [876, 313.19, 2.8],
  "Sikkim": [12, 2.43, 4.94],
  "Tamil Nadu": [3905, 457.16, 8.54],
  "Tripura": [280, 19.48, 14.37],
  "Uttar Pradesh": [3262, 1008.32, 3.24],
  "West Bengal": [6743, 528.85, 12.75],
  "TOTAL (STATES)": [39518, 6294.87, 6.28],
 },
 "U.Ts.": {
  "A. & N. Islands": [38, 1.68, 22.62],
  "Arunachal Pradesh": [11, 5.88, 1.87],
  "Chandigarh": [19, 4.33, 4.39],
  "D. & N. Haveli": [14, 0.85, 16.47],
  "Delhi": [205, 55.47, 3.7],
  "Goa, Daman & Diu": [70, 10.75, 6.51],
  "Lakshadweep": [1, 0.35, 2.86],
  "Mizoram": [4, 4.18, 0.96],
  "Pondicherry": [327, 5.6, 58.39],
  "TOTAL (U.TS.)": [689, 89.09, 7.73],
 },
 "Grand": {
  "GRAND TOTAL": [40207, 6383.96, 6.3],
 },
 "Cities": {
  "Ahmedabad": [166, 20.21, 8.21],
  "Bangalore": [945, 19.32, 48.91],
  "Bombay": [186, 78.67, 2.36],
  "Calcutta": [29, 33.22, 0.87],
  "Delhi": [189, 50.9, 3.71],
  "Hyderabad": [96, 21.17, 4.53],
  "Kanpur": [72, 14.14, 5.09],
  "Madras": [148, 32.36, 4.57],
  "TOTAL (CITIES)": [1831, 269.99, 6.78],
 },
}
