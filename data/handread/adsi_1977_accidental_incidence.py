# ADSI 1977, Table II: incidence of accidental deaths, population, volume of accidental deaths per lakh of population and
# percentage distribution to the all-India total, States / U.Ts. / metropolitan cities
# (raw/adsi/1977/year_wise/accidental-deaths-1977.pdf, PDF pages 6-7). Read from the page images; checked by
# scripts/check_handread.py. Population is printed "in (000)" (thousands); converted to lakh (thousands / 100).
# The percentage-distribution column is not transcribed.
KIND, YEAR, PUB = "accidental_incidence", 1977, "adsi"
SOURCE = 'raw/adsi/1977/year_wise/accidental-deaths-1977.pdf'
PAGES = '6-7'
TITLE = 'Table II: Incidence of Accidental Deaths, Population, Volume of Accidental Deaths per lakh of Population and Percentage Distribution of Accidental Deaths to all India Total during 1977'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  'Andhra Pradesh': [14695, 484.93, 30.30],
  'Assam': [2643, 178.59, 14.80],
  'Bihar': [5974, 637.78, 9.36],
  'Gujarat': [5295, 306.3, 17.29],
  'Haryana': [1579, 115.11, 13.72],
  'Himachal Pradesh': [391, 39.42, 9.92],
  'Jammu & Kashmir': [520, 54.56, 9.53],
  'Karnataka': [6070, 332.28, 18.27],
  'Kerala': [2721, 243.41, 11.18],
  'Madhya Pradesh': [13957, 490.83, 28.44],
  'Maharashtra': [24990, 570.57, 43.80],
  'Manipur': [48, 13.11, 3.66],
  'Meghalaya': [106, 12.0, 8.83],
  'Nagaland': [32, 6.37, 5.02],
  'Orissa': [4243, 251.5, 16.87],
  'Punjab': [1482, 150.67, 9.84],
  'Rajasthan': [3894, 305.31, 12.75],
  'Sikkim': [78, 2.39, 32.64],
  'Tamil Nadu': [7272, 450.98, 16.12],
  'Tripura': [268, 18.91, 14.17],
  'Uttar Pradesh': [10377, 990.1, 10.48],
  'West Bengal': [7292, 517.39, 14.09],
  'TOTAL (STATES)': [113927, 6172.51, 18.46],
 },
 "U.Ts.": {
  'A & N Islands': [59, 1.6, 36.88],
  'Arunachal Pradesh': [46, 5.71, 8.06],
  'Chandigarh': [74, 4.05, 18.27],
  'D & N Haveli': [62, 0.83, 74.70],
  'Delhi': [2580, 53.21, 48.49],
  'Goa, Daman & Diu': [352, 10.43, 33.75],
  'Lakshadweep': [1, 0.34, 2.94],
  'Mizoram': [57, 4.06, 14.04],
  'Pondicherry': [180, 5.48, 32.85],
  'TOTAL (U.TS.)': [3411, 85.71, 39.80],
 },
 "Grand": {
  'GRAND TOTAL': [117338, 6258.22, 18.75],
 },
 "Cities": {
  'Ahmedabad': [630, 19.61, 32.13],
  'Bangalore': [955, 18.78, 50.85],
  'Bombay': [5775, 76.05, 75.94],
  'Calcutta': [701, 32.97, 21.26],
  'Delhi': [2383, 48.91, 48.72],
  'Hyderabad': [351, 20.46, 17.16],
  'Kanpur': [374, 13.78, 27.14],
  'Madras': [678, 31.3, 21.66],
  'TOTAL (CITIES)': [11847, 261.86, 45.24],
 },
}
