# ADSI 1982, Table 2: incidence of suicides, volume of suicides per lakh of population, States / UTs / cities
# (raw/adsi/1982/year_wise/suicides-1982.pdf, pages 4-5; printed pages 20-21). Read from the page images; checked by
# scripts/check_handread.py. The population column is headed "estimated mid-year population in 1000", but the note on
# the page says the figures are the actual census figures as on 1-3-1981 (mid-year estimates for 1982 were not
# available) and the volume per lakh is based on them; converted here to lakh (thousands / 100). Rate = volume of
# suicides per 100000 of population. The percentage column is not transcribed. Lucknow's count is N.A. (row kept with
# None, so it is left out of the data; the cities' total excludes it).
KIND, YEAR, PUB = "suicide_incidence", 1982, "adsi"
SOURCE = "raw/adsi/1982/year_wise/suicides-1982.pdf"
PAGES = "4-5"
TITLE = 'Table 2: Incidence of Suicides, Volume of Suicides per Lakh of Population during 1982'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Assam", "Number of suicides"): (1905, 1705, "printed 1905; the States add to the printed Total (States) 43,720 only with 1705, 1705 / 199.03 = 8.57 (printed rate; 1905 would give 9.57) and 1705 / 44732 = 3.8% (printed share)"),
    ("Gujarat", "Estimated mid-year population (lakh)"): (239.61, 339.61, "printed 23961 (thousand); the States' populations add to the printed Total (States) 674218 only with 33961, and 1793 / 339.61 = 5.28 (printed rate; 239.61 would give 7.48)"),
    ("TOTAL (U.TS.)", "Estimated mid-year population (lakh)"): (27.80, 97.80, "printed 2780 (thousand); the UTs' populations add to 9780, Total (States) 674218 + 9780 = the printed Grand Total 683998, and 1012 / 97.80 = 10.35 (printed rate)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2990, 535.93, 5.58],
  "Assam": [1705, 199.03, 8.57],
  "Bihar": [714, 698.23, 1.02],
  "Gujarat": [1793, 339.61, 5.28],
  "Haryana": [461, 128.51, 3.59],
  "Himachal Pradesh": [90, 42.38, 2.12],
  "J & K.": [22, 59.54, 0.37],
  "Karnataka": [5295, 370.44, 14.29],
  "Kerala": [4613, 254.03, 18.16],
  "Madhya Pradesh": [3051, 521.39, 5.85],
  "Maharashtra": [3890, 627.15, 6.2],
  "Manipur": [41, 14.12, 2.9],
  "Meghalaya": [36, 13.28, 2.71],
  "Nagaland": [5, 7.73, 0.65],
  "Orissa": [2303, 262.72, 8.77],
  "Punjab": [359, 166.7, 2.15],
  "Rajasthan": [937, 341.08, 2.75],
  "Sikkim": [17, 3.15, 5.4],
  "Tamil Nadu": [5490, 482.97, 11.37],
  "Tripura": [550, 20.47, 26.87],
  "Uttar Pradesh": [2477, 1108.86, 2.24],
  "West Bengal": [6881, 544.86, 12.63],
  "TOTAL (STATES)": [43720, 6742.18, 6.48],
 },
 "U.Ts.": {
  "A. & N. Islands": [72, 1.88, 38.3],
  "Arunachal Pradesh": [23, 6.28, 3.66],
  "Chandigarh": [21, 4.5, 4.67],
  "D. & N. Haveli": [15, 1.04, 14.42],
  "Delhi": [435, 61.96, 7.02],
  "Goa, Daman & Diu": [86, 10.82, 7.95],
  "Lakshadweep": [1, 0.4, 2.5],
  "Mizoram": [7, 4.88, 1.44],
  "Pondicherry": [352, 6.04, 58.28],
  "TOTAL (U.TS.)": [1012, 97.8, 10.35],
 },
 "Grand": {
  "GRAND TOTAL": [44732, 6839.98, 6.54],
 },
 "Cities": {
  "Ahmedabad": [185, 20.25, 9.14],
  "Bangalore": [718, 24.83, 28.92],
  "Bombay": [207, 82.27, 2.52],
  "Calcutta": [41, 32.92, 1.25],
  "Delhi": [417, 57.14, 7.3],
  "Hyderabad": [188, 21.42, 8.78],
  "Jaipur": [126, 9.67, 13.03],
  "Kanpur": [44, 15.31, 2.87],
  "Lucknow": [None, 8.96, None],
  "Madras": [462, 32.66, 14.15],
  "Nagpur": [196, 12.15, 16.13],
  "Pune": [140, 12.03, 11.64],
  "TOTAL (CITIES)": [2724, 329.61, 8.26],
 },
}
