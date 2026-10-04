# ADSI 1982, Table II: incidence of accidental deaths, population, volume of accidental deaths per lakh of population and
# percentage distribution to the all-India total, States / U.Ts. / cities (raw/adsi/1982/year_wise/accidental-deaths-1982.pdf,
# PDF pages 5-6). Read from the page images; checked by scripts/check_handread.py. Population is printed "(In 000)"
# (thousands); converted to lakh (thousands / 100). Per the table's note these are the actual census figures as on
# 1-3-1981, not 1982 mid-year estimates (which were not available). The percentage-distribution column is not transcribed.
# Uttar Pradesh population is printed "11,0886" (= 110886 thousand).
# Lucknow population is printed 816 thousand and its printed rate 48.53 = 396/8.16 uses it, but the City populations then
# add to 32,881 against the printed Total 32,961 (the 1981 census figure for Lucknow city is 896; the same 816 appears in
# the 1981 table, where its rate and the total both confirm 896). Left as printed here because the printed rate agrees.
# Bihar population is printed 69,832 here (69,823 in the 1981 table); the State populations add to the printed Total only
# with 69,823 (a 9-thousand difference) -- see the pop check; left as printed.
KIND, YEAR, PUB = "accidental_incidence", 1982, "adsi"
SOURCE = 'raw/adsi/1982/year_wise/accidental-deaths-1982.pdf'
PAGES = '5-6'
TITLE = 'Table II: Incidence of Accidental Deaths, Population, Volume of Accidental Deaths per Lakh of Population and Percentage Distribution of Accidental Deaths To All India Total During 1982'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Kerala", "Number of accidental deaths"): (2557, 2757, "printed 2,557 (clear); the State counts add to the printed Total 1,21,570 only with 2,757, 2757/254.03 = 10.85 = the printed rate, and 2757/125993 = 2.2% = the printed share"),
}
ROWS = {
 "States": {
  'Andhra Pradesh': [9500, 535.93, 17.73],
  'Assam': [2220, 199.03, 11.15],
  'Bihar': [4167, 698.32, 5.97],
  'Gujarat': [6114, 339.61, 18.00],
  'Haryana': [1518, 128.51, 11.81],
  'Himachal Pradesh': [523, 42.38, 12.34],
  'J & K': [536, 59.54, 9.01],
  'Karnataka': [7967, 370.44, 21.51],
  'Kerala': [2757, 254.03, 10.85],
  'Madhya Pradesh': [18133, 521.39, 34.78],
  'Maharashtra': [28167, 627.15, 44.91],
  'Manipur': [109, 14.12, 7.72],
  'Meghalaya': [96, 13.28, 7.23],
  'Nagaland': [84, 7.73, 10.81],
  'Orissa': [4203, 262.72, 16.00],
  'Punjab': [1888, 166.7, 11.33],
  'Rajasthan': [4358, 341.08, 12.78],
  'Sikkim': [104, 3.15, 33.02],
  'Tamil Nadu': [10367, 482.97, 21.47],
  'Tripura': [317, 20.47, 15.49],
  'Uttar Pradesh': [11470, 1108.86, 10.34],
  'West Bengal': [6972, 544.86, 12.80],
  'TOTAL (STATES)': [121570, 6742.18, 18.03],
 },
 "U.Ts.": {
  'A & N Islands': [90, 1.88, 47.87],
  'Arunachal Pradesh': [61, 6.28, 9.71],
  'Chandigarh': [110, 4.5, 24.44],
  'D & N Haveli': [16, 1.04, 15.38],
  'Delhi': [3556, 61.96, 57.39],
  'Goa & Daman & Diu': [363, 10.82, 33.55],
  'Lakshadweep': [3, 0.4, 7.50],
  'Mizoram': [56, 4.88, 11.48],
  'Pondicherry': [168, 6.04, 27.81],
  'TOTAL (U.TS.)': [4423, 97.8, 45.23],
 },
 "Grand": {
  'GRAND TOTAL': [125993, 6839.98, 18.42],
 },
 "Cities": {
  'Ahmedabad': [674, 20.25, 33.28],
  'Bangalore': [1103, 24.83, 44.42],
  'Bombay': [5211, 82.27, 63.34],
  'Calcutta': [862, 32.92, 26.18],
  'Delhi': [3269, 57.14, 57.21],
  'Hyderabad': [781, 21.42, 36.46],
  'Jaipur': [526, 9.67, 54.40],
  'Kanpur': [59, 15.31, 3.85],
  'Lucknow': [396, 8.16, 48.53],
  'Madras': [627, 32.66, 19.20],
  'Nagpur': [635, 12.15, 52.26],
  'Pune': [1397, 12.03, 116.13],
  'TOTAL (CITIES)': [15540, 329.61, 47.15],
 },
}
