# ADSI 1994, Table-2: incidence and rate of accidental deaths, State & UT-wise and City-wise
# (raw/adsi/1994/year_wise/accidental-deaths-1994.pdf, PDF pages 7-8, printed pages 22-23). Read from the page images;
# checked by scripts/check_handread.py. Population is printed in lakh (estimated mid-year). The percentage-share column
# is not transcribed. The city part has no printed total. "Total (All-India)" is entered as GRAND TOTAL.
KIND, YEAR, PUB = "accidental_incidence", 1994, "adsi"
SOURCE = "raw/adsi/1994/year_wise/accidental-deaths-1994.pdf"
PAGES = "7-8"
TITLE = "Table-2: Incidence And Rate Of Accidental Deaths During 1994 (State & UT-wise; City-wise)"
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [13211, 705.3, 18.7],
  "Arunachal Pradesh": [95, 9.4, 10.1],
  "Assam": [2392, 241.1, 9.9],
  "Bihar": [6836, 929.3, 7.4],
  "Goa": [955, 12.5, 76.4],
  "Gujarat": [12001, 438.5, 27.4],
  "Haryana": [1836, 177.1, 10.4],
  "Himachal Pradesh": [1011, 55.1, 18.3],
  "Jammu & Kashmir": [826, 83.2, 9.9],
  "Karnataka": [12464, 473.7, 26.3],
  "Kerala": [5455, 304.9, 17.9],
  "Madhya Pradesh": [25537, 707.8, 36.1],
  "Maharashtra": [33419, 842.7, 39.7],
  "Manipur": [136, 19.8, 6.9],
  "Meghalaya": [174, 19.2, 9.1],
  "Mizoram": [89, 7.7, 11.6],
  "Nagaland": [44, 13.4, 3.3],
  "Orissa": [4707, 336.6, 14.0],
  "Punjab": [3424, 213.1, 16.1],
  "Rajasthan": [9051, 472.5, 19.2],
  "Sikkim": [65, 4.5, 14.4],
  "Tamil Nadu": [17576, 577.4, 30.4],
  "Tripura": [244, 29.8, 8.2],
  "Uttar Pradesh": [19483, 1476.0, 13.2],
  "West Bengal": [11586, 720.8, 16.1],
  "TOTAL (STATES)": [182617, 8871.4, 20.6],
 },
 "U.Ts.": {
  "A & N Islands": [116, 3.2, 36.3],
  "Chandigarh": [187, 7.4, 25.3],
  "D & N Haveli": [52, 1.5, 34.7],
  "Daman & Diu": [53, 1.1, 48.2],
  "Delhi": [6894, 105.9, 65.1],
  "Lakshadweep": [4, 0.6, 6.7],
  "Pondicherry": [512, 8.6, 59.5],
  "TOTAL (U.TS.)": [7818, 128.3, 60.9],
 },
 "Grand": {
  "GRAND TOTAL": [190435, 8999.7, 21.2],
 },
 "Cities": {
  "Ahmedabad": [1024, 36.2, 28.3],
  "Bangalore": [1498, 46.4, 32.3],
  "Bhopal": [498, 12.7, 39.2],
  "Bombay": [8361, 145.1, 57.6],
  "Calcutta": [697, 117.1, 6.0],
  "Coimbatore": [478, 11.7, 40.9],
  "Delhi": [5652, 95.7, 59.1],
  "Hyderabad": [1152, 51.9, 22.2],
  "Indore": [732, 12.2, 60.0],
  "Jaipur": [795, 17.4, 45.7],
  "Kanpur": [848, 21.8, 38.9],
  "Kochi": [281, 13.5, 20.8],
  "Lucknow": [488, 19.8, 24.6],
  "Ludhiana": [91, 12.5, 7.3],
  "Madras": [1298, 58.6, 22.2],
  "Madurai": [135, 11.5, 11.7],
  "Nagpur": [1141, 18.1, 63.0],
  "Patna": [156, 11.7, 13.3],
  "Pune": [1692, 28.4, 59.6],
  "Surat": [666, 18.0, 37.0],
  "Vadodara": [484, 12.9, 37.5],
  "Varanasi": [704, 11.2, 62.9],
  "Vishakhapatnam": [389, 12.7, 30.6],
 },
}
