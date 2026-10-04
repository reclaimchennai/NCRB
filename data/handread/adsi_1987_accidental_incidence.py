# ADSI 1987, Table II: incidence of accidental deaths, population, volume of accidental deaths per lakh of population and
# percentage distribution to the all-India total, States / U.Ts. / cities (raw/adsi/1987/year_wise/accidental-deaths-87.pdf,
# PDF pages 6 and 8; page 7 is a bar chart). Read from the page images; checked by scripts/check_handread.py.
# Population is printed "In (000)" (thousands); converted to lakh (thousands / 100). The percentage column is not
# transcribed. Printed with misplaced digit-group commas: Total (Cities) count "1,76,11" (= 17611) and population
# "3,9895" (= 39895). The all-India population 7,81,374 carries an asterisk with no footnote on these pages.
# "Total (All-India)" is entered as GRAND TOTAL.
KIND, YEAR, PUB = "accidental_incidence", 1987, "adsi"
SOURCE = 'raw/adsi/1987/year_wise/accidental-deaths-87.pdf'
PAGES = '6,8'
TITLE = 'Table II: Incidence Of Accidental Deaths, Population, Volume Of Accidental Deaths Per Lakh Of Population And Percentage Distribution Of Accidental Deaths To All-India Total During The Year 1987'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Punjab", "Estimated mid-year population (lakh)"): (180.98, 189.08, "printed 18,098 thousand (clear), digits transposed; the State populations add to the printed Total 7,71,499 only with 18,908, and 1688/189.08 = 8.93 = the printed rate"),
}
ROWS = {
 "States": {
  'Andhra Pradesh': [10170, 602.88, 16.87],
  'Arunachal Pradesh': [171, 7.54, 22.68],
  'Assam': [2520, 230.12, 10.95],
  'Bihar': [6688, 800.02, 8.36],
  'Goa': [507, 11.75, 43.15],
  'Gujarat': [7391, 386.17, 19.14],
  'Haryana': [2145, 152.87, 14.03],
  'Himachal Pradesh': [791, 48.12, 16.44],
  'Jammu & Kashmir': [892, 68.96, 12.94],
  'Karnataka': [9683, 424.25, 22.82],
  'Kerala': [4215, 284.75, 14.80],
  'Madhya Pradesh': [22143, 598.13, 37.02],
  'Maharashtra': [30637, 713.33, 42.95],
  'Manipur': [111, 16.61, 6.68],
  'Meghalaya': [190, 15.88, 11.96],
  'Mizoram': [67, 6.29, 10.65],
  'Nagaland': [51, 9.96, 5.12],
  'Orissa': [5044, 295.47, 17.07],
  'Punjab': [1688, 189.08, 8.93],
  'Rajasthan': [5762, 405.85, 14.20],
  'Sikkim': [108, 3.98, 27.14],
  'Tamil Nadu': [14339, 536.53, 26.73],
  'Tripura': [94, 23.95, 3.92],
  'Uttar Pradesh': [13878, 1264.78, 10.97],
  'West Bengal': [8675, 617.72, 14.04],
  'TOTAL (STATES)': [147960, 7714.99, 19.18],
 },
 "U.Ts.": {
  'A & N Islands': [108, 2.53, 42.69],
  'Chandigarh': [123, 6.32, 19.46],
  'D & N Haveli': [18, 1.22, 14.75],
  'Daman & Diu': [9, 0.88, 10.23],
  'Delhi': [3832, 80.39, 47.67],
  'Lakshadweep': [2, 0.44, 4.55],
  'Pondicherry': [262, 6.97, 37.59],
  'TOTAL (U.TS.)': [4354, 98.75, 44.09],
 },
 "Grand": {
  'GRAND TOTAL': [152314, 7813.74, 19.49],
 },
 "Cities": {
  'Ahmedabad': [961, 23.56, 40.79],
  'Bangalore': [1518, 32.9, 46.14],
  'Bombay': [7153, 99.78, 71.69],
  'Calcutta': [629, 33.63, 18.70],
  'Delhi': [2941, 75.83, 38.78],
  'Hyderabad': [574, 24.26, 23.66],
  'Jaipur': [536, 13.0, 41.23],
  'Kanpur': [446, 17.22, 25.90],
  'Lucknow': [429, 9.95, 43.12],
  'Madras': [968, 39.14, 24.73],
  'Nagpur': [345, 14.95, 23.08],
  'Pune': [1111, 14.73, 75.42],
  'TOTAL (CITIES)': [17611, 398.95, 44.14],
 },
}
