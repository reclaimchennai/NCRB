# ADSI 1979, Table II: incidence of accidental deaths, population, volume of accidental deaths per lakh of population and
# percentage distribution to the all-India total, States / U.Ts. / cities (raw/adsi/1979/year_wise/accidental-deaths-1979.pdf,
# PDF pages 6-7). Read from the page images; checked by scripts/check_handread.py. The errata sheet (errata_0_1979.pdf)
# does not touch this table. Population is printed "in (000)" (thousands); converted to lakh (thousands / 100).
# Lakshadweep's count is printed as a dash (nil) with 0.0 per cent and rate 0.0; entered as 0.
# The percentage-distribution column is not transcribed. The State and City populations add to 1 thousand more than the printed totals (rounding).
KIND, YEAR, PUB = "accidental_incidence", 1979, "adsi"
SOURCE = 'raw/adsi/1979/year_wise/accidental-deaths-1979.pdf'
PAGES = '6-7'
TITLE = 'Table II: Incidence of Accidental Deaths, Population, Volume of Accidental Deaths per lakh of population and percentage Distribution of Accidental Deaths to all-India Total during 1979'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  'Andhra Pradesh': [8475, 500.73, 16.93],
  'Assam': [2276, 189.74, 12.00],
  'Bihar': [4311, 662.15, 6.51],
  'Gujarat': [5581, 319.54, 17.47],
  'Haryana': [1583, 120.38, 13.15],
  'Himachal Pradesh': [659, 40.98, 16.08],
  'Jammu & Kashmir': [499, 57.4, 8.69],
  'Karnataka': [8555, 345.26, 24.78],
  'Kerala': [2363, 252.27, 9.37],
  'Madhya Pradesh': [10299, 512.26, 20.11],
  'Maharashtra': [25071, 591.24, 42.40],
  'Manipur': [81, 13.93, 5.81],
  'Meghalaya': [112, 12.66, 8.85],
  'Nagaland': [54, 6.79, 7.95],
  'Orissa': [4234, 262.04, 16.16],
  'Punjab': [1620, 156.07, 10.38],
  'Rajasthan': [4080, 321.14, 12.70],
  'Sikkim': [50, 2.47, 20.24],
  'Tamil Nadu': [7961, 463.25, 17.19],
  'Tripura': [276, 20.06, 13.76],
  'Uttar Pradesh': [10562, 1026.71, 10.29],
  'West Bengal': [7320, 540.23, 13.55],
  'TOTAL (STATES)': [106022, 6417.29, 16.52],
 },
 "U.Ts.": {
  'A & N Islands': [62, 1.75, 35.43],
  'Arunachal Pradesh': [29, 6.06, 4.79],
  'Chandigarh': [69, 4.63, 14.90],
  'D & N Haveli': [14, 0.86, 16.28],
  'Delhi': [2107, 57.8, 36.45],
  'Goa Daman & Diu': [411, 11.07, 37.13],
  'Lakshadweep': [0, 0.35, 0.0],
  'Mizoram': [56, 4.31, 12.99],
  'Pondicherry': [217, 5.72, 37.94],
  'TOTAL (U.TS.)': [2965, 92.55, 32.04],
 },
 "Grand": {
  'GRAND TOTAL': [108987, 6509.82, 16.74],
 },
 "Cities": {
  'Ahmedabad': [554, 20.81, 26.62],
  'Bangalore': [1077, 19.86, 54.23],
  'Bombay': [5295, 81.28, 65.15],
  'Calcutta': [836, 33.45, 24.99],
  'Delhi': [1936, 52.89, 36.60],
  'Hyderabad': [501, 21.87, 22.91],
  'Kanpur': [173, 14.5, 11.93],
  'Madras': [654, 33.42, 19.57],
  'TOTAL (CITIES)': [11026, 278.07, 39.65],
 },
}
