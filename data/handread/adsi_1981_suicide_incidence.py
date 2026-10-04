# ADSI 1981, Table II: incidence of suicides, volume of suicides per lakh of population, States / UTs / cities
# (raw/adsi/1981/year_wise/suicides-1981.pdf, pages 3-4; printed pages 23-24). Read from the page images; checked by
# scripts/check_handread.py. The table prints the population in '000 first, then the number of suicides; converted here
# to lakh (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not
# transcribed. Lucknow's count is N.A. (row kept with None, so it is left out of the data; the cities' count total
# excludes it). Madras's rate is printed "2131" with the decimal point missing; recorded as 21.31 (696 / 32.66 = 21.31).
KIND, YEAR, PUB = "suicide_incidence", 1981, "adsi"
SOURCE = "raw/adsi/1981/year_wise/suicides-1981.pdf"
PAGES = "3-4"
TITLE = 'Table II: Incidence of Suicides, Volume of Suicides per Lakh of Population During 1981'
CHECK = "incidence"
CATS = ["Number of suicides", "Population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ('Bangalore', 'Number of suicides'): (680, 690, 'printed 680; the cities add to the printed Total (Cities) 2,678 only with 690, 690 / 24.83 = 27.79 (printed rate; 680 would give 27.39) and 690 / 2678 = 25.8% (printed share; 680 would give 25.4%)'),
    ('Madras', 'Rate of suicides per lakh'): (2131, 21.31, 'printed 2131 with the decimal point missing; 696 / 32.66 = 21.31'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2915, 535.93, 5.44],
  "Assam": [1941, 199.03, 9.75],
  "Bihar": [440, 698.23, 0.63],
  "Gujarat": [1625, 339.61, 4.78],
  "Haryana": [600, 128.51, 4.67],
  "Himachal Pradesh": [85, 42.38, 2.01],
  "Jammu & Kashmir": [19, 59.54, 0.32],
  "Karnataka": [3942, 370.44, 10.64],
  "Kerala": [4096, 254.03, 16.12],
  "Madhya Pradesh": [2544, 521.39, 4.88],
  "Maharashtra": [3260, 627.15, 5.2],
  "Manipur": [6, 14.12, 0.43],
  "Meghalaya": [31, 13.28, 2.33],
  "Nagaland": [12, 7.73, 1.55],
  "Orissa": [1880, 262.72, 7.16],
  "Punjab": [281, 166.7, 1.69],
  "Rajasthan": [839, 341.08, 2.46],
  "Sikkim": [21, 3.15, 6.67],
  "Tamil Nadu": [4836, 482.97, 10.01],
  "Tripura": [436, 20.47, 21.3],
  "Uttar Pradesh": [3077, 1108.86, 2.77],
  "West Bengal": [6544, 544.86, 12.01],
  "TOTAL (STATES)": [39430, 6742.18, 5.85],
 },
 "U.Ts.": {
  "A & N Islands": [39, 1.88, 20.74],
  "Arunachal Pradesh": [20, 6.28, 3.18],
  "Chandigarh": [17, 4.5, 3.78],
  "D & N Haveli": [16, 1.04, 15.38],
  "Delhi": [397, 61.96, 6.41],
  "Goa Daman & Diu": [86, 10.82, 7.95],
  "Lakshadweep": [1, 0.4, 2.5],
  "Mizoram": [14, 4.88, 2.87],
  "Pondicherry": [225, 6.04, 37.25],
  "TOTAL (U.TS.)": [815, 97.8, 8.33],
 },
 "Grand": {
  "GRAND TOTAL": [40245, 6839.98, 5.88],
 },
 "Cities": {
  "Ahmedabad": [178, 20.25, 8.79],
  "Bangalore": [690, 24.83, 27.79],
  "Bombay": [201, 82.27, 2.44],
  "Calcutta": [25, 32.92, 0.76],
  "Delhi": [346, 57.14, 6.06],
  "Hyderabad": [141, 21.42, 6.58],
  "Jaipur": [87, 9.67, 9.0],
  "Kanpur": [50, 15.31, 3.27],
  "Lucknow": [None, 8.96, None],
  "Madras": [696, 32.66, 21.31],
  "Nagpur": [153, 12.15, 12.59],
  "Pune": [111, 12.03, 9.23],
  "TOTAL (CITIES)": [2678, 329.61, 8.12],
 },
}
