# ADSI 1975, Table 5: incidence of suicides and volume of suicides per one lakh of population, States / U.Ts. /
# cities (raw/adsi/1975/year_wise/suicides-1975.pdf, pages 9-10; printed pages 27-28). Read from the page images;
# checked by scripts/check_handread.py. The table prints the estimated mid-year population "in 000"; converted here to
# lakh (thousands / 100). Rate = volume of suicides per 100,000 of population. The percentage column is not
# transcribed. The 1975 errata sheet has no entry for this table.
KIND, YEAR, PUB = "suicide_incidence", 1975, "adsi"
SOURCE = "raw/adsi/1975/year_wise/suicides-1975.pdf"
PAGES = "9-10"
TITLE = 'Table 5: Incidence of Suicides, Volume of suicides per one lakh of population during 1975'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3391, 468.56, 7.24],
  "Assam": [1215, 164.74, 7.38],
  "Bihar": [580, 611.28, 0.95],
  "Gujarat": [1346, 292.62, 4.6],
  "Haryana": [555, 110.82, 5.01],
  "Himachal Pradesh": [91, 37.7, 2.41],
  "Jammu & Kashmir": [2, 51.6, 0.04],
  "Karnataka": [4729, 317.56, 14.89],
  "Kerala": [4225, 231.87, 18.22],
  "Madhya Pradesh": [2464, 466.02, 5.29],
  "Maharashtra": [3544, 550.86, 6.43],
  "Manipur": [12, 12.27, 0.98],
  "Meghalaya": [29, 11.33, 2.56],
  "Nagaland": [17, 5.95, 2.86],
  "Orissa": [2283, 239.29, 9.54],
  "Punjab": [237, 146.78, 1.61],
  "Rajasthan": [424, 287.79, 1.47],
  "Sikkim": [4, 2.28, 1.75],
  "Tamil Nadu": [4840, 437.41, 11.07],
  "Tripura": [409, 17.73, 23.07],
  "Uttar Pradesh": [4228, 952.16, 4.44],
  "West Bengal": [7611, 488.38, 15.58],
  "TOTAL (STATES)": [42236, 5905.0, 7.15],
 },
 "U.Ts.": {
  "A & N Islands": [23, 1.46, 15.75],
  "Arunachal Pradesh": [8, 5.31, 1.51],
  "Chandigarh": [13, 3.43, 3.79],
  "D & N Haveli": [12, 0.81, 14.81],
  "Delhi": [204, 48.73, 4.19],
  "Goa, Daman & Diu": [81, 9.78, 8.28],
  "Lakshadweep": [3, 0.36, 8.33],
  "Mizoram": [2, 3.74, 0.53],
  "Pondicherry": [308, 5.31, 58.0],
  "TOTAL (U.TS.)": [654, 78.93, 8.29],
 },
 "Grand": {
  "GRAND TOTAL": [42890, 5983.93, 7.17],
 },
 "Cities": {
  "Ahmedabad": [91, 18.41, 4.94],
  "Bangalore": [372, 17.7, 21.02],
  "Bombay": [164, 70.82, 2.32],
  "Calcutta": [41, 32.5, 1.26],
  "Delhi": [159, 44.93, 3.54],
  "Hyderabad": [161, 19.06, 8.45],
  "Kanpur": [48, 13.07, 3.67],
  "Madras": [563, 29.19, 19.29],
  "TOTAL (CITIES)": [1599, 245.68, 6.51],
 },
}
