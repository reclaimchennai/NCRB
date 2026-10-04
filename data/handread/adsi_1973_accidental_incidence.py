# ADSI 1973, Table IV: Statewise distribution of accidental deaths and volume of accidental deaths per one lakh of
# population, States / U.Ts. / cities (raw/adsi/1973/year_wise/accidental-deaths-1973.pdf, PDF pages 7-8). Read from
# the page images; checked by scripts/check_handread.py. The errata sheet (errata_3_1973.pdf) does not touch this table.
# Population is printed "in (000)" (thousands); converted to lakh here (thousands / 100), e.g. 45428 -> 454.28.
# The percentage-distribution column is not transcribed.
KIND, YEAR, PUB = "accidental_incidence", 1973, "adsi"
SOURCE = 'raw/adsi/1973/year_wise/accidental-deaths-1973.pdf'
PAGES = '7-8'
TITLE = 'Table IV: Statewise distribution of Accidental Deaths and Volume of Accidental Deaths per one lakh of population during 1973'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Manipur", "Rate of accidental deaths per lakh"): (25.75, 2.58, "printed 25.75, the decimal point misplaced; count 29 and population 1126 thousand are both confirmed by the State column totals, and 29/11.26 = 2.58"),
}
ROWS = {
 "States": {
  'Andhra Pradesh': [6907, 454.28, 15.20],
  'Assam': [2523, 156.29, 16.14],
  'Bihar': [5675, 586.96, 9.67],
  'Gujarat': [5819, 282.27, 20.62],
  'Haryana': [1424, 105.46, 13.50],
  'Himachal Pradesh': [391, 35.47, 11.02],
  'Jammu & Kashmir': [589, 48.31, 12.19],
  'Karnataka': [6607, 306.46, 21.56],
  'Kerala': [2598, 224.74, 11.56],
  'Madhya Pradesh': [13901, 440.1, 31.59],
  'Maharashtra': [23601, 529.5, 44.57],
  'Manipur': [29, 11.26, 2.58],
  'Meghalaya': [104, 10.59, 9.82],
  'Nagaland': [18, 5.33, 3.38],
  'Orissa': [4197, 229.89, 18.26],
  'Punjab': [1250, 141.36, 8.84],
  'Rajasthan': [2868, 271.54, 10.56],
  'Tamil Nadu': [6480, 430.35, 15.06],
  'Tripura': [274, 16.31, 16.80],
  'Uttar Pradesh': [9602, 917.32, 10.47],
  'West Bengal': [8863, 465.84, 19.03],
  'TOTAL (STATES)': [103720, 5669.63, 18.29],
 },
 "U.Ts.": {
  'A & N Islands': [66, 1.2, 55.00],
  'Arunachal Pradesh': [16, 4.9, 3.27],
  'Chandigarh': [89, 2.68, 33.21],
  'Dadra & Nagar Haveli': [29, 0.78, 37.18],
  'Delhi': [1784, 45.15, 39.51],
  'Goa, Daman & Diu': [293, 8.99, 32.59],
  'Lakshadweep': [1, 0.34, 2.94],
  'Mizoram': [20, 3.55, 5.63],
  'Pondicherry': [336, 4.94, 68.02],
  'TOTAL (U.TS.)': [2634, 72.53, 36.32],
 },
 "Grand": {
  'GRAND TOTAL': [106354, 5742.16, 18.52],
 },
 "Cities": {
  'Ahmedabad': [699, 17.21, 40.62],
  'Bangalore': [533, 16.62, 32.07],
  'Bombay': [4450, 65.59, 67.85],
  'Calcutta': [614, 32.02, 19.18],
  'Delhi': [1630, 40.95, 39.80],
  'Hyderabad': [261, 17.65, 14.79],
  'Kanpur': [72, 12.35, 5.83],
  'Madras': [977, 27.07, 36.09],
  'TOTAL (CITIES)': [9236, 229.46, 40.25],
 },
}
