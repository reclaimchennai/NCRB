# ADSI 1986, Table II: incidence of accidental deaths, population, volume of accidental deaths per lakh of population and
# percentage distribution of accidental deaths to the all-India total, States / U.Ts. / cities
# (raw/adsi/1986/year_wise/accidental-deaths-1986.pdf, PDF pages 6 and 8 = printed pp. 4 and 6; page 7 is a bar chart).
# Read from the page images; checked by scripts/check_handread.py.
# Population is printed "In (000)" (thousands); converted to lakh (thousands / 100). The percentage column is not
# transcribed. Printed with a full stop or a stray space/comma for the digit-group comma: Andhra Pradesh count "10.551"
# (= 10551), Bihar population "78.308" (= 78308), Gujarat population "37.933" (= 37933), Maharashtra population
# "70, 138" (= 70138), Total (Cities) population "38.766" (= 38766); Manipur's rate is printed "7,57" (= 7.57).
# Lakshadweep's count and rate are printed as a dash (nil; the text on printed p. 3 says no accidental death was
# reported there during 1986), with 0.0 per cent; entered as 0.
KIND, YEAR, PUB = "accidental_incidence", 1986, "adsi"
SOURCE = 'raw/adsi/1986/year_wise/accidental-deaths-1986.pdf'
PAGES = '6,8'
TITLE = 'Table II: Incidence Of Accidental Deaths, Population, Volume Of Accidental Deaths Per Lakh Of Population And Percentage Distribution Of Accidental Deaths To All India Total During The Year 1986'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  'Andhra Pradesh': [10551, 592.16, 17.82],
  'Arunachal Pradesh': [138, 7.34, 18.80],
  'Assam': [2341, 225.02, 10.40],
  'Bihar': [4384, 783.08, 5.60],
  'Gujarat': [7378, 379.33, 19.45],
  'Haryana': [1988, 149.37, 13.31],
  'Himachal Pradesh': [591, 47.30, 12.49],
  'Jammu & Kashmir': [719, 67.48, 10.66],
  'Karnataka': [10712, 416.04, 25.75],
  'Kerala': [3561, 280.08, 12.71],
  'Madhya Pradesh': [18776, 585.92, 32.05],
  'Maharashtra': [30520, 701.38, 43.51],
  'Manipur': [123, 16.24, 7.57],
  'Meghalaya': [140, 15.49, 9.04],
  'Mizoram': [89, 6.08, 14.64],
  'Nagaland': [47, 9.60, 4.90],
  'Orissa': [4431, 290.32, 15.26],
  'Punjab': [1935, 186.22, 10.39],
  'Rajasthan': [5129, 395.40, 12.97],
  'Sikkim': [130, 3.85, 33.77],
  'Tamil Nadu': [16007, 528.49, 30.29],
  'Tripura': [145, 23.43, 6.19],
  'Uttar Pradesh': [14353, 1238.92, 11.59],
  'West Bengal': [8055, 606.25, 13.29],
  'TOTAL (STATES)': [142243, 7554.79, 18.83],
 },
 "U.Ts.": {
  'A & N Islands': [96, 2.43, 39.51],
  'Chandigarh': [102, 6.01, 16.97],
  'D & N Haveli': [26, 1.19, 21.85],
  'Delhi': [3811, 77.30, 49.30],
  'Goa, Daman & Diu': [492, 12.36, 39.81],
  'Lakshadweep': [0, 0.44, 0.0],
  'Pondicherry': [253, 6.83, 37.04],
  'TOTAL (U.TS.)': [4780, 106.56, 44.86],
 },
 "Grand": {
  'GRAND TOTAL': [147023, 7661.35, 19.19],
 },
 "Cities": {
  'Ahmedabad': [1127, 23.10, 48.78],
  'Bangalore': [1650, 31.48, 52.41],
  'Bombay': [6702, 97.13, 69.00],
  'Calcutta': [499, 33.56, 14.87],
  'Delhi': [3487, 72.72, 47.95],
  'Hyderabad': [830, 23.73, 34.98],
  'Jaipur': [501, 12.43, 40.31],
  'Kanpur': [661, 16.80, 39.35],
  'Lucknow': [279, 9.77, 28.56],
  'Madras': [1511, 38.10, 39.66],
  'Nagpur': [422, 14.52, 29.06],
  'Pune': [1552, 14.32, 108.38],
  'TOTAL (CITIES)': [19221, 387.66, 49.58],
 },
}
