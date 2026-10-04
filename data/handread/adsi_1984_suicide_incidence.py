# ADSI 1984, Table II: incidence of suicides, volume of suicides per lakh of population, States / UTs / cities
# (raw/adsi/1984/year_wise/suicides-1984.pdf, pages 3-4; printed pages 23-24). Read from the page images; checked by
# scripts/check_handread.py. The table prints the estimated mid-year population in 1000; converted here to lakh
# (thousands / 100). Rate = volume of suicides per lakh of population. The percentage column is not transcribed.
KIND, YEAR, PUB = "suicide_incidence", 1984, "adsi"
SOURCE = "raw/adsi/1984/year_wise/suicides-1984.pdf"
PAGES = "3-4"
TITLE = 'Table II: Incidence of Suicides, Volume of Suicides per lakh of Population during the year-1984'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3658, 570.88, 6.41],
  "Assam": [1586, 215.35, 7.36],
  "Bihar": [615, 750.61, 0.82],
  "Gujarat": [1893, 365.3, 5.18],
  "Haryana": [530, 141.82, 3.74],
  "Himachal Pradesh": [77, 45.65, 1.69],
  "Jammu & Kashmir": [34, 64.49, 0.53],
  "Karnataka": [4862, 399.5, 12.17],
  "Kerala": [5617, 270.33, 20.78],
  "Madhya Pradesh": [3087, 561.36, 5.5],
  "Maharashtra": [4121, 674.81, 6.11],
  "Manipur": [64, 15.47, 4.14],
  "Meghalaya": [35, 14.68, 2.38],
  "Nagaland": [36, 8.89, 4.05],
  "Orissa": [1753, 280.0, 6.26],
  "Punjab": [253, 179.82, 1.41],
  "Rajasthan": [885, 375.23, 2.36],
  "Sikkim": [18, 3.59, 5.01],
  "Tamil Nadu": [7471, 511.53, 14.61],
  "Tripura": [439, 22.38, 19.62],
  "Uttar Pradesh": [2621, 1189.48, 2.2],
  "West Bengal": [9912, 583.33, 16.99],
  "TOTAL (STATES)": [49567, 7244.5, 6.84],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [80, 2.22, 36.04],
  "Arunachal Pradesh": [25, 6.95, 3.6],
  "Chandigarh": [17, 5.42, 3.14],
  "Dadra & Nagar Haveli": [28, 1.14, 24.56],
  "Delhi": [433, 71.36, 6.07],
  "Goa, Daman & Diu": [121, 11.77, 10.28],
  "Lakshadweep": [1, 0.43, 2.33],
  "Mizoram": [12, 5.65, 2.12],
  "Pondicherry": [287, 6.54, 43.88],
  "TOTAL (U.TS.)": [1004, 111.48, 9.01],
 },
 "Grand": {
  "GRAND TOTAL": [50571, 7355.98, 6.87],
 },
 "Cities": {
  "Ahmedabad": [211, 22.18, 9.51],
  "Bangalore": [754, 28.8, 26.18],
  "Bombay": [403, 91.64, 4.4],
  "Calcutta": [38, 33.39, 1.14],
  "Delhi": [384, 54.99, 6.98],
  "Hyderabad": [263, 22.67, 11.6],
  "Jaipur": [46, 11.35, 4.05],
  "Kanpur": [50, 16.01, 3.12],
  "Lucknow": [204, 9.45, 21.59],
  "Madras": [666, 36.04, 18.48],
  "Nagpur": [239, 13.65, 17.51],
  "Pune": [152, 13.46, 11.29],
  "TOTAL (CITIES)": [3410, 353.63, 9.64],
 },
}
