# ADSI 1980, Table II: incidence of accidental deaths, population, volume of accidental deaths per lakh of population and
# percentage distribution to the all-India total, States / U.Ts. / cities (raw/adsi/1980/year_wise/accidental-deaths-1980.pdf,
# PDF pages 6-7). Read from the page images; checked by scripts/check_handread.py. Population is printed "in ('000)"
# (thousands); converted to lakh (thousands / 100). The percentage-distribution column is not transcribed.
KIND, YEAR, PUB = "accidental_incidence", 1980, "adsi"
SOURCE = 'raw/adsi/1980/year_wise/accidental-deaths-1980.pdf'
PAGES = '6-7'
TITLE = 'Table II: Incidence of Accidental Deaths, Population, Volume of Accidental Deaths per lakh of Population and Percentage Distribution of accidental Deaths to All India Total during 1980'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  'Andhra Pradesh': [5489, 508.72, 10.79],
  'Assam': [2428, 195.49, 12.42],
  'Bihar': [3907, 674.34, 5.79],
  'Gujarat': [5922, 326.15, 18.16],
  'Haryana': [1515, 123.05, 12.31],
  'Himachal Pradesh': [510, 41.76, 12.21],
  'Jammu & Kashmir': [634, 58.84, 10.77],
  'Karnataka': [11648, 351.73, 33.12],
  'Kerala': [2445, 256.66, 9.53],
  'Madhya Pradesh': [15708, 523.1, 30.03],
  'Maharashtra': [25050, 601.45, 41.64],
  'Manipur': [77, 14.35, 5.37],
  'Meghalaya': [128, 12.99, 9.85],
  'Nagaland': [30, 7.0, 4.29],
  'Orissa': [4423, 267.23, 16.55],
  'Punjab': [1585, 158.76, 9.98],
  'Rajasthan': [4214, 329.16, 12.80],
  'Sikkim': [44, 2.51, 17.53],
  'Tamil Nadu': [8205, 469.18, 17.49],
  'Tripura': [348, 20.64, 16.86],
  'Uttar Pradesh': [12248, 1045.09, 11.72],
  'West Bengal': [7345, 551.63, 13.32],
  'TOTAL (STATES)': [113903, 6539.83, 17.42],
 },
 "U.Ts.": {
  'Andaman & Nicobar Islands': [68, 1.83, 37.16],
  'Arunachal Pradesh': [39, 6.23, 6.26],
  'Chandigarh': [89, 4.95, 17.98],
  'Dadra and Nagar Haveli': [18, 0.87, 20.69],
  'Delhi': [2134, 60.21, 35.44],
  'Goa, Daman & Diu': [404, 11.39, 35.47],
  'Lakshadweep': [5, 0.36, 13.89],
  'Mizoram': [39, 4.44, 8.78],
  'Pondicherry': [213, 5.85, 36.41],
  'TOTAL (U.TS.)': [3009, 96.13, 31.30],
 },
 "Grand": {
  'GRAND TOTAL': [116912, 6635.96, 17.62],
 },
 "Cities": {
  'Ahmedabad': [781, 21.41, 36.48],
  'Bangalore': [1162, 20.4, 56.96],
  'Bombay': [5113, 83.9, 60.94],
  'Calcutta': [620, 33.69, 18.40],
  'Delhi': [1941, 54.88, 35.37],
  'Hyderabad': [464, 22.57, 20.56],
  'Kanpur': [219, 14.86, 14.74],
  'Madras': [574, 34.47, 16.65],
  'TOTAL (CITIES)': [10874, 286.18, 38.00],
 },
}
