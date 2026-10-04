# ADSI 1995, Table-2(A): incidence and rate of accidental deaths, State, UT & City-wise
# (raw/adsi/1995/year_wise/accidental-deaths-1995.pdf, PDF page 6). Read from the page images (faint print, contrast
# enhanced); checked by scripts/check_handread.py. Population is printed in lakh (estimated mid-year). The
# percentage-share column is not transcribed. "Total (All-India)" is entered as GRAND TOTAL.
# Ahmedabad and Vadodara: printed 1342 (rate 36.15) and 586 (rate 43.56); the printed rates fit 1341 and 588, which is what
# the 1995 column of Table-1.2 in fatalities_0_1996.pdf prints, but the City counts add to the printed Total 29,049 only
# as printed here (1341 + 588 would give 29,050), so the counts are left as printed.
KIND, YEAR, PUB = "accidental_incidence", 1995, "adsi"
SOURCE = 'raw/adsi/1995/year_wise/accidental-deaths-1995.pdf'
PAGES = '6'
TITLE = 'Table-2(A): Incidence And Rate of Accidental Deaths During 1995 (State, UT & City-wise)'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Arunachal Pradesh", "Estimated mid-year population (lakh)"): (0.05, 9.6, "row printed shifted one column right: share column 114 (the count repeated), population column 0.05 (the share), rate column 9.6; 9.6 is the population -- the State populations add to the printed Total 9027.2 only with 9.6 (1993: 9.2) -- and the rate (114/9.6 = 11.9) is not printed, so it is left None"),
}
ROWS = {
 "States": {
  'Andhra Pradesh': [12293, 717.1, 17.14],
  'Arunachal Pradesh': [114, 9.6, None],
  'Assam': [2591, 246.1, 10.53],
  'Bihar': [7899, 949.1, 8.32],
  'Goa': [902, 12.7, 71.02],
  'Gujarat': [13617, 446.1, 30.52],
  'Haryana': [3987, 180.7, 22.06],
  'Himachal Pradesh': [1204, 56.1, 21.46],
  'Jammu & Kashmir': [1253, 85.1, 14.72],
  'Karnataka': [13622, 480.5, 28.35],
  'Kerala': [6096, 309.1, 19.72],
  'Madhya Pradesh': [25692, 721.4, 35.61],
  'Maharashtra': [54945, 859.1, 63.96],
  'Manipur': [239, 20.3, 11.77],
  'Meghalaya': [210, 19.6, 10.71],
  'Mizoram': [117, 7.9, 14.81],
  'Nagaland': [78, 13.9, 5.61],
  'Orissa': [5419, 342.7, 15.81],
  'Punjab': [3658, 216.0, 16.94],
  'Rajasthan': [12422, 482.1, 25.77],
  'Sikkim': [153, 4.7, 32.55],
  'Tamil Nadu': [17421, 582.9, 29.89],
  'Tripura': [304, 30.5, 9.97],
  'Uttar Pradesh': [20147, 1501.2, 13.42],
  'West Bengal': [11515, 732.7, 15.72],
  'TOTAL (STATES)': [215898, 9027.2, 23.92],
 },
 "U.Ts.": {
  'A & N Islands': [108, 3.3, 32.73],
  'Chandigarh': [259, 7.8, 33.21],
  'D & N Haveli': [82, 1.6, 51.25],
  'Daman & Diu': [76, 1.1, 69.09],
  'Delhi': [5547, 109.7, 50.57],
  'Lakshadweep': [6, 0.6, 10],
  'Pondicherry': [511, 8.8, 58.07],
  'TOTAL (U.TS.)': [6589, 132.9, 49.58],
 },
 "Grand": {
  'GRAND TOTAL': [222487, 9160.1, 24.29],
 },
 "Cities": {
  'Ahmedabad': [1342, 37.1, 36.15],
  'Bangalore': [1642, 48.0, 34.21],
  'Bhopal': [497, 13.3, 37.37],
  'Bombay': [6295, 151.4, 41.58],
  'Calcutta': [771, 119.2, 6.47],
  'Coimbatore': [372, 11.9, 31.26],
  'Delhi': [4589, 99.5, 46.12],
  'Hyderabad': [1096, 54.8, 20],
  'Indore': [898, 12.6, 71.27],
  'Jaipur': [898, 18.1, 49.61],
  'Kanpur': [1242, 22.3, 55.7],
  'Kochi': [289, 14.2, 20.35],
  'Lucknow': [253, 20.8, 12.16],
  'Ludhiana': [92, 13.2, 6.97],
  'Madras': [1154, 60.0, 19.23],
  'Madurai': [388, 11.7, 33.16],
  'Nagpur': [2508, 18.5, 135.57],
  'Patna': [354, 11.9, 29.75],
  'Pune': [1477, 29.6, 49.9],
  'Surat': [892, 18.9, 47.2],
  'Vadodara': [586, 13.5, 43.56],
  'Varanasi': [1168, 11.5, 101.57],
  'Vishakhapatnam': [246, 13.5, 18.22],
  'TOTAL (CITIES)': [29049, 825.5, 35.19],
 },
}
