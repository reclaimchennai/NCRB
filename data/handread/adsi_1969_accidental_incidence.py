# ADSI 1969, Table 4: incidence of accidental deaths, population, volume of accidental deaths per one lakh of population
# and percentage distribution to the all-India total, States / U.Ts. / cities (raw/adsi/1969/year_wise/accidental-deaths-1969.pdf,
# PDF pages 7 and 9, printed pages 8 and 10; PDF page 8 is a bar chart). Read from the page images; checked by
# scripts/check_handread.py. Population is printed "in 000" with Indian digit grouping (4,24,25 = 42,425 thousand);
# converted to lakh here (thousands / 100), e.g. 4,24,25 -> 424.25. The percentage-distribution column is not transcribed.
# Himachal Pradesh, Manipur and Tripura are printed among the Union Territories in 1969 and are kept there.
# Laccadives: rate printed with its first digit smudged ('?.70'; 1 / 0.27 = 3.70), entered as None.
# Rajasthan: printed rate 10.42 against 2676 / 255.88 = 10.46 (count confirmed by the State total, population by the
# printed population total 52,50,21); left as printed. Maharashtra 46.70 against 46.68, left as printed.
# Every population column also adds exactly to its printed total (States 5250.21, UTs 115.76, cities 203.04).
KIND, YEAR, PUB = "accidental_incidence", 1969, "adsi"
SOURCE = "raw/adsi/1969/year_wise/accidental-deaths-1969.pdf"
PAGES = "7,9"
TITLE = "Table 4: Incidence of Accidental deaths, population, volume of accidental deaths per one lakh of population and percentage distribution of accidental deaths to All-India total, 1969"
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [8094, 424.25, 19.08],
  "Assam": [2272, 152.03, 14.94],
  "Bihar": [9629, 564.43, 17.06],
  "Gujarat": [7241, 258.91, 27.97],
  "Haryana": [1738, 97.96, 17.74],
  "Jammu & Kashmir": [463, 39.94, 11.59],
  "Kerala": [3117, 208.13, 14.98],
  "Madhya Pradesh": [15541, 398.05, 39.04],
  "Maharashtra": [22825, 488.99, 46.7],
  "Mysore": [7629, 286.66, 26.61],
  "Nagaland": [38, 4.26, 8.92],
  "Orissa": [5889, 211.59, 27.83],
  "Punjab": [1987, 143.69, 13.82],
  "Rajasthan": [2676, 255.88, 10.42],
  "Tamil Nadu": [7473, 388.59, 19.23],
  "Uttar Pradesh": [17796, 889.11, 20.02],
  "West Bengal": [13135, 437.74, 30.01],
  "TOTAL (STATES)": [127543, 5250.21, 24.29],
 },
 "U.Ts.": {
  "A & N Islands": [40, 0.9, 44.44],
  "Chandigarh": [29, 1.55, 18.71],
  "Dadra & Nagar Haveli": [30, 0.71, 42.25],
  "Delhi": [1320, 40.41, 32.67],
  "Goa, Daman & Diu": [245, 6.81, 35.98],
  "Himachal Pradesh": [580, 35.27, 16.44],
  "Laccadives": [1, 0.27, None],
  "Manipur": [38, 10.77, 3.53],
  "Pondicherry": [379, 4.39, 86.33],
  "Tripura": [550, 14.68, 37.47],
  "TOTAL (U.TS.)": [3212, 115.76, 27.74],
 },
 "Grand": {
  "GRAND TOTAL": [130755, 5365.97, 24.36],
 },
 "Cities": {
  "Ahmedabad": [621, 15.83, 39.23],
  "Bangalore": [695, 17.45, 39.83],
  "Bombay": [4028, 55.34, 72.79],
  "Calcutta": [706, 31.34, 22.53],
  "Delhi": [1176, 36.21, 32.48],
  "Hyderabad": [395, 13.63, 28.98],
  "Kanpur": [533, 12.76, 41.77],
  "Madras": [810, 20.48, 39.55],
  "TOTAL (CITIES)": [8964, 203.04, 44.15],
 },
}
