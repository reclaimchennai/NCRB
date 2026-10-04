# ADSI 1991, Table-2: incidence and volume of accidental deaths, State & UT-wise and City-wise
# (raw/adsi/1991/year_wise/accidental-deaths-1991.pdf, PDF page 5, printed page 5). Read from the page image; checked by
# scripts/check_handread.py. Population is printed in lakh (estimated mid-year). The percentage-share column is not
# transcribed. The city part has no printed total. "Total (All - India)" is entered as GRAND TOTAL.
KIND, YEAR, PUB = "accidental_incidence", 1991, "adsi"
SOURCE = "raw/adsi/1991/year_wise/accidental-deaths-1991.pdf"
PAGES = "5"
TITLE = "Table-2: Incidence and Volume of Accidental Deaths during 1991 (State, UT & City-wise)"
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [13860, 667.7, 20.8],
  "Arunachal Pradesh": [114, 8.7, 13.1],
  "Assam": [1736, 224.7, 7.7],
  "Bihar": [7559, 869.1, 8.7],
  "Goa": [700, 11.7, 59.8],
  "Gujarat": [9326, 413.8, 22.5],
  "Haryana": [1722, 164.4, 10.5],
  "Himachal Pradesh": [958, 51.4, 18.6],
  "Jammu & Kashmir": [940, 77.8, 12.1],
  "Karnataka": [11222, 450.3, 24.9],
  "Kerala": [4883, 291.2, 16.8],
  "Madhya Pradesh": [23884, 666.9, 35.8],
  "Maharashtra": [38761, 793.3, 48.9],
  "Manipur": [214, 18.4, 11.6],
  "Meghalaya": [229, 17.8, 12.9],
  "Mizoram": [61, 6.9, 8.8],
  "Nagaland": [41, 12.3, 3.3],
  "Orissa": [5358, 317.1, 16.9],
  "Punjab": [2509, 203.0, 12.4],
  "Rajasthan": [7246, 441.8, 16.4],
  "Sikkim": [138, 4.1, 33.7],
  "Tamil Nadu": [16969, 558.8, 30.4],
  "Tripura": [175, 27.7, 6.3],
  "Uttar Pradesh": [21084, 1397.2, 15.1],
  "West Bengal": [12095, 685.1, 17.7],
  "TOTAL (STATES)": [181784, 8381.3, 21.7],
 },
 "U.Ts.": {
  "A & N Islands": [137, 2.8, 48.9],
  "Chandigarh": [132, 6.5, 20.3],
  "D & N Haveli": [43, 1.4, 30.7],
  "Daman & Diu": [35, 1.0, 35.0],
  "Delhi": [5369, 94.9, 56.6],
  "Lakshadweep": [2, 0.5, 4.0],
  "Pondicherry": [501, 8.0, 62.6],
  "TOTAL (U.TS.)": [6219, 115.1, 54.0],
 },
 "Grand": {
  "GRAND TOTAL": [188003, 8496.4, 22.1],
 },
 "Cities": {
  "Ahmedabad": [1169, 33.3, 35.1],
  "Bangalore": [1737, 41.3, 42.1],
  "Bombay": [6933, 127.5, 54.4],
  "Calcutta": [674, 109.8, 6.1],
  "Delhi": [4396, 84.8, 51.8],
  "Hyderabad": [1053, 43.6, 24.2],
  "Jaipur": [785, 15.4, 51.0],
  "Kanpur": [545, 21.3, 25.6],
  "Lucknow": [832, 16.7, 49.8],
  "Madras": [933, 54.0, 17.3],
  "Nagpur": [854, 16.8, 50.8],
  "Pune": [1855, 25.2, 73.6],
 },
}
