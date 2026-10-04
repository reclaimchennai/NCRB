# ADSI 1970, Table IV: incidence of accidental deaths, population, volume of accidental deaths per one lakh of population
# and percentage distribution to the all-India total, States / U.Ts. / cities (raw/adsi/1970/year_wise/accidental-deaths-1970.pdf,
# PDF pages 6 and 8; page 7 is a bar chart). Read from the page images; checked by scripts/check_handread.py.
# Population is printed "in 000" (thousands); converted to lakh here (thousands / 100), e.g. 43317 -> 433.17.
# The percentage-distribution column is not transcribed.
KIND, YEAR, PUB = "accidental_incidence", 1970, "adsi"
SOURCE = 'raw/adsi/1970/year_wise/accidental-deaths-1970.pdf'
PAGES = '6,8'
TITLE = 'Table IV: Incidence of Accidental Deaths, Population, Volume of Accidental Deaths per one lakh of Population and Percentage Distribution of Accidental Deaths to All India Total, 1970'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  'Andhra Pradesh': [8975, 433.17, 20.72],
  'Assam': [2542, 156.75, 16.22],
  'Bihar': [7739, 578.26, 13.38],
  'Gujarat': [7740, 266.08, 29.09],
  'Haryana': [1410, 100.98, 13.96],
  'Himachal Pradesh': [796, 36.25, 21.96],
  'Jammu & Kashmir': [1460, 40.5, 36.04],
  'Kerala': [3237, 213.43, 15.17],
  'Madhya Pradesh': [18207, 408.11, 44.61],
  'Maharashtra': [24944, 501.52, 49.74],
  'Manipur': [59, 11.2, 5.27],
  'Mysore': [7670, 293.62, 26.12],
  'Nagaland': [70, 4.33, 16.17],
  'Orissa': [7738, 216.57, 35.73],
  'Punjab': [1811, 148.12, 12.23],
  'Rajasthan': [3351, 263.24, 12.73],
  'Tamil Nadu': [7222, 395.6, 18.26],
  'Tripura': [132, 15.13, 8.72],
  'Uttar Pradesh': [19915, 909.8, 21.89],
  'West Bengal': [12436, 449.83, 27.65],
  'TOTAL (STATES)': [137454, 5442.49, 25.26],
 },
 "U.Ts.": {
  'A & N Islands': [72, 0.93, 77.42],
  'Chandigarh': [35, 1.59, 22.01],
  'Dadra & Nagar Haveli': [20, 0.73, 27.40],
  'Delhi': [1582, 42.41, 37.30],
  'Goa, Daman & Diu': [231, 6.88, 33.58],
  'Laccadives': [2, 0.28, 7.14],
  'Pondicherry': [356, 4.49, 79.29],
  'TOTAL (U.TS.)': [2298, 57.31, 40.10],
 },
 "Grand": {
  'GRAND TOTAL': [139752, 5499.8, 25.41],
 },
 "Cities": {
  'Ahmedabad': [673, 16.28, 41.34],
  'Bangalore': [610, 18.09, 33.72],
  'Bombay': [6141, 57.0, 107.74],
  'Calcutta': [388, 31.59, 12.28],
  'Delhi': [1415, 39.02, 36.26],
  'Hyderabad': [553, 13.77, 40.16],
  'Kanpur': [790, 13.12, 60.21],
  'Madras': [718, 20.86, 34.42],
  'TOTAL (CITIES)': [11288, 209.73, 53.82],
 },
}
