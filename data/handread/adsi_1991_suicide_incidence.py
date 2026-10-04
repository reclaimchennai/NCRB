# ADSI 1991, Table 7: incidence and volume of suicides during 1991 (State, UT & City-wise)
# (raw/adsi/1991/year_wise/suicides-1991.pdf, page 5; printed page 23). Read from the page image; checked by
# scripts/check_handread.py. The table prints the number of suicides, the percentage share (not transcribed), the
# estimated mid-year population already in lakh (one decimal) and the volume of suicides (col.3 / col.5) to one decimal.
# No total is printed for the cities.
# The States' populations as printed add to 8381.2 lakh against the printed Total (States) 8381.3 (rounding of
# the one-decimal figures); left as printed.
KIND, YEAR, PUB = "suicide_incidence", 1991, "adsi"
SOURCE = "raw/adsi/1991/year_wise/suicides-1991.pdf"
PAGES = "5"
TITLE = 'Table 7: Incidence and Volume of Suicides during 1991 (State, UT & City-wise)'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [6143, 667.7, 9.2],
  "Arunachal Pradesh": [69, 8.7, 7.9],
  "Assam": [2286, 224.7, 10.2],
  "Bihar": [1208, 869.1, 1.4],
  "Goa": [243, 11.7, 20.8],
  "Gujarat": [3052, 413.8, 7.4],
  "Haryana": [1117, 164.4, 6.8],
  "Himachal Pradesh": [159, 51.4, 3.1],
  "Jammu & Kashmir": [49, 77.8, 0.6],
  "Karnataka": [8313, 450.3, 18.5],
  "Kerala": [8409, 291.2, 28.9],
  "Madhya Pradesh": [5703, 666.9, 8.6],
  "Maharashtra": [8820, 793.3, 11.1],
  "Manipur": [29, 18.4, 1.6],
  "Meghalaya": [74, 17.8, 4.2],
  "Mizoram": [34, 6.9, 4.9],
  "Nagaland": [18, 12.3, 1.5],
  "Orissa": [3105, 317.1, 9.8],
  "Punjab": [589, 203.0, 2.9],
  "Rajasthan": [1931, 441.8, 4.4],
  "Sikkim": [38, 4.1, 9.3],
  "Tamil Nadu": [9670, 558.8, 17.3],
  "Tripura": [476, 27.7, 17.2],
  "Uttar Pradesh": [2842, 1397.2, 2.0],
  "West Bengal": [12354, 685.1, 18.0],
  "TOTAL (STATES)": [76731, 8381.3, 9.2],
 },
 "U.Ts.": {
  "A & N Islands": [126, 2.8, 45.0],
  "Chandigarh": [54, 6.5, 8.3],
  "D & N Haveli": [20, 1.4, 14.3],
  "Daman & Diu": [20, 1.0, 20.0],
  "Delhi": [988, 94.9, 10.4],
  "Lakshadweep": [0, 0.5, 0.0],
  "Pondicherry": [511, 8.0, 63.9],
  "TOTAL (U.TS.)": [1719, 115.1, 14.9],
 },
 "Grand": {
  "GRAND TOTAL": [78450, 8496.4, 9.2],
 },
 "Cities": {
  "Ahmedabad": [304, 33.3, 9.1],
  "Bangalore": [1096, 41.3, 26.5],
  "Bombay": [1022, 127.5, 8.0],
  "Calcutta": [214, 109.8, 1.9],
  "Delhi": [815, 84.8, 9.6],
  "Hyderabad": [380, 43.6, 8.7],
  "Jaipur": [163, 15.4, 10.6],
  "Kanpur": [128, 21.3, 6.0],
  "Lucknow": [119, 16.7, 7.1],
  "Madras": [782, 54.0, 14.5],
  "Nagpur": [282, 16.8, 16.8],
  "Pune": [283, 25.2, 11.2],
 },
}
