# ADSI 1981, Table II: incidence of accidental deaths, population, volume of accidental deaths per lakh of population and
# percentage distribution to the all-India total, States / U.Ts. / cities (raw/adsi/1981/year_wise/accidental-deaths-1981.pdf,
# PDF pages 5, 6 and 8; page 7 is a bar chart). Read from the page images; checked by scripts/check_handread.py.
# Population is printed "in '000" (thousands); converted to lakh (thousands / 100).
# Lakshadweep's count is printed as a dash (nil) with rate 0.0; entered as 0.
# The percentage-distribution column is not transcribed.
KIND, YEAR, PUB = "accidental_incidence", 1981, "adsi"
SOURCE = 'raw/adsi/1981/year_wise/accidental-deaths-1981.pdf'
PAGES = '5,6,8'
TITLE = 'Table II: Incidence of Accidental Deaths, Population, Volume of Accidental Deaths per lakh of Population and Percentage Distribution of Accidental Deaths to All India Total During 1981'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Lucknow", "Estimated mid-year population (lakh)"): (8.16, 8.96, "printed 816 thousand (clear on the page); the City populations then add to 32,961 thousand as printed in the Total (Cities) only with 896, and 593/8.96 = 66.18 = the printed rate"),
}
ROWS = {
 "States": {
  'Andhra Pradesh': [7256, 535.93, 13.54],
  'Assam': [1967, 199.03, 9.88],
  'Bihar': [3907, 698.23, 5.60],
  'Gujarat': [5897, 339.61, 17.36],
  'Haryana': [1447, 128.51, 11.26],
  'Himachal Pradesh': [548, 42.38, 12.93],
  'Jammu & Kashmir': [527, 59.54, 8.85],
  'Karnataka': [8631, 370.44, 23.30],
  'Kerala': [2561, 254.03, 10.08],
  'Madhya Pradesh': [16405, 521.39, 31.46],
  'Maharashtra': [29478, 627.15, 47.00],
  'Manipur': [48, 14.12, 3.40],
  'Meghalaya': [133, 13.28, 10.02],
  'Nagaland': [83, 7.73, 10.74],
  'Orissa': [4184, 262.72, 15.93],
  'Punjab': [1885, 166.7, 11.31],
  'Rajasthan': [4556, 341.08, 13.36],
  'Sikkim': [105, 3.15, 33.33],
  'Tamil Nadu': [9689, 482.97, 20.06],
  'Tripura': [306, 20.47, 14.95],
  'Uttar Pradesh': [12230, 1108.86, 11.03],
  'West Bengal': [6396, 544.86, 11.74],
  'TOTAL (STATES)': [118239, 6742.18, 17.54],
 },
 "U.Ts.": {
  'A & N Islands': [54, 1.88, 28.72],
  'Arunachal Pradesh': [71, 6.28, 11.31],
  'Chandigarh': [107, 4.5, 23.78],
  'D & N Haveli': [16, 1.04, 15.38],
  'Delhi': [3084, 61.96, 49.77],
  'Goa Daman & Diu': [435, 10.82, 40.20],
  'Lakshadweep': [0, 0.4, 0.0],
  'Mizoram': [77, 4.88, 15.78],
  'Pondicherry': [138, 6.04, 22.85],
  'TOTAL (U.TS.)': [3982, 97.8, 40.72],
 },
 "Grand": {
  'GRAND TOTAL': [122221, 6839.98, 17.87],
 },
 "Cities": {
  'Ahmedabad': [618, 20.25, 30.52],
  'Bangalore': [1647, 24.83, 66.33],
  'Bombay': [7820, 82.27, 95.05],
  'Calcutta': [757, 32.92, 23.00],
  'Delhi': [2811, 57.14, 49.20],
  'Hyderabad': [509, 21.42, 23.76],
  'Jaipur': [267, 9.67, 27.61],
  'Kanpur': [159, 15.31, 10.39],
  'Lucknow': [593, 8.96, 66.18],
  'Madras': [845, 32.66, 25.87],
  'Nagpur': [930, 12.15, 76.54],
  'Pune': [1117, 12.03, 92.85],
  'TOTAL (CITIES)': [18073, 329.61, 54.83],
 },
}
