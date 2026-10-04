# ADSI 1969, Table 10: population, incidence of suicidal deaths, volume of suicides and percentage distribution,
# States / UTs / cities (raw/adsi/1969/year_wise/suicides-1969.pdf, page 7; printed page 20). Read from the page image;
# checked by scripts/check_handread.py. The table prints the estimated mid-year population "in '000"; converted here
# to lakh (thousands / 100). Rate = volume of suicides per 1,00,000 of population. The percentage column is not
# transcribed.
KIND, YEAR, PUB = "suicide_incidence", 1969, "adsi"
SOURCE = "raw/adsi/1969/year_wise/suicides-1969.pdf"
PAGES = "7"
TITLE = 'Table 10: Population, incidence of suicidal deaths, volume of suicides and percentage distribution of suicides in States/UTs/Cities during 1969'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3606, 424.25, 8.5],
  "Assam": [932, 152.03, 6.13],
  "Bihar": [1800, 564.43, 3.19],
  "Gujarat": [2117, 258.91, 8.18],
  "Haryana": [802, 97.96, 8.19],
  "Jammu & Kashmir": [14, 39.94, 0.35],
  "Kerala": [3205, 208.13, 15.4],
  "Madhya Pradesh": [2891, 398.05, 7.26],
  "Maharashtra": [4234, 488.99, 8.66],
  "Mysore": [3188, 286.66, 11.12],
  "Nagaland": [21, 4.26, 4.93],
  "Orissa": [2509, 211.59, 11.86],
  "Punjab": [662, 143.69, 4.61],
  "Rajasthan": [329, 255.88, 1.29],
  "Tamil Nadu": [4967, 388.59, 12.78],
  "Uttar Pradesh": [5699, 889.11, 6.41],
  "West Bengal": [5613, 437.74, 12.82],
  "TOTAL (STATES)": [42589, 5250.21, 8.11],
 },
 "U.Ts.": {
  "A. & N. Islands": [22, 0.9, 24.44],
  "Chandigarh": [11, 1.55, 7.1],
  "Dadra & Nagar Haveli": [11, 0.71, 15.49],
  "Delhi": [118, 40.41, 2.92],
  "Goa, Daman & Diu": [43, 6.81, 6.31],
  "Himachal Pradesh": [98, 35.27, 2.77],
  "Laccadives": [4, 0.27, 14.81],
  "Manipur": [38, 10.77, 3.53],
  "Pondicherry": [277, 4.39, 63.1],
  "Tripura": [422, 14.68, 28.75],
  "TOTAL (U.TS.)": [1044, 115.76, 9.01],
 },
 "Grand": {
  "GRAND TOTAL": [43633, 5365.97, 8.13],
 },
 "Cities": {
  "Ahmedabad": [87, 15.83, 5.5],
  "Bangalore": [695, 17.45, 39.83],
  "Bombay": [98, 55.34, 1.77],
  "Calcutta": [68, 31.34, 2.17],
  "Delhi": [99, 36.21, 2.73],
  "Hyderabad": [223, 13.63, 16.36],
  "Kanpur": [252, 12.76, 19.75],
  "Madras": [143, 20.48, 6.98],
  "TOTAL (CITIES)": [1665, 203.04, 8.2],
 },
}
