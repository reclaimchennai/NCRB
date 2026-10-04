# ADSI 1967, Table 10: incidence, estimated mid-year population and volume of suicides, States / UTs / cities
# (raw/adsi/1967/year_wise/suicides-1967.pdf, pages 5-6; printed pages 12-13). Read from the page images; checked by
# scripts/check_handread.py (counts against the printed totals, every rate against count / population).
# The table prints the population "in '00" (hundreds); converted here to lakh (hundreds / 1000). The rate column is
# headed "per 10,000 of population" but the figures are per lakh (100,000), as the text says (e.g. 6513 / 414.307 lakh
# = 15.72). The percentage-to-total column is not transcribed. "-" (nil) for Laccadives is 0.
KIND, YEAR, PUB = "suicide_incidence", 1967, "adsi"
SOURCE = "raw/adsi/1967/year_wise/suicides-1967.pdf"
PAGES = "5-6"
TITLE = "Table 10: Incidence and its percentage distribution, Population and volume of suicides in States/U.T.s/Cities during 1967"
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Andhra Pradesh", "Number of suicides"): (4365, 3365, "printed 4,365; the States total 37,614 needs 3,365, and 3365 / 407.12 = 8.27 (printed rate) and 3365 / 38829 = 8.67% (printed share)"),
    ("Punjab", "Rate of suicides per lakh"): (7.62, None, "printed 7.62; the count 801 is confirmed by its share (2.06% of 38,829) and the population 135.066 lakh is that of Punjab, and 801 / 135.066 = 5.93, so the printed rate is a misprint; left unread"),
    ("Tripura", "Rate of suicides per lakh"): (85.40, None, "printed 85.40; the count 213 is confirmed by the U.T. total (1,215) and its share (0.55%), and 213 / 13.807 = 15.43, so the printed rate is a misprint; left unread"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3365, 407.120, 8.27],
  "Assam": [690, 142.861, 4.83],
  "Bihar": [1228, 537.732, 2.28],
  "Gujarat": [1484, 245.000, 6.06],
  "Haryana": [593, 92.080, 6.44],
  "J & K": [7, 38.867, 0.18],
  "Kerala": [1747, 197.903, 8.82],
  "Madhya Pradesh": [2194, 378.642, 5.79],
  "Maharashtra": [3117, 464.769, 6.71],
  "Mysore": [2703, 273.235, 9.89],
  "Nagaland": [2, 4.109, 0.49],
  "Orissa": [1897, 202.022, 9.39],
  "Punjab": [801, 135.066, None],
  "Rajasthan": [767, 241.594, 3.17],
  "Tamil Nadu": [5369, 375.174, 14.31],
  "Uttar Pradesh": [5137, 849.263, 6.05],
  "West Bengal": [6513, 414.307, 15.72],
  "TOTAL (STATES)": [37614, None, None],
 },
 "U.Ts.": {
  "A & N Islands": [30, 0.823, 36.45],
  "Chandigarh": [13, 1.453, 8.95],
  "Dadra and Nagar Haveli": [25, 0.675, 37.04],
  "Delhi": [538, 36.427, 14.77],
  "Goa, Daman and Diu": [118, 6.683, 17.66],
  "Himachal Pradesh": [93, 33.393, 2.78],
  "Laccadives": [0, 0.265, None],
  "Manipur": [6, 9.924, 0.60],
  "Pondicherry": [179, 4.209, 42.53],
  "Tripura": [213, 13.807, None],
  "TOTAL (U.TS.)": [1215, None, None],
 },
 "Grand": {"GRAND TOTAL": [38829, None, None]},
 "Cities": {
  "Ahmedabad": [87, 14.921, 5.83],
  "Bangalore": [219, 16.158, 13.55],
  "Bombay": [124, 52.026, 2.38],
  "Calcutta": [89, 30.845, 2.89],
  "Delhi": [444, 33.183, 13.38],
  "Hyderabad": [127, 13.365, 9.50],
  "Kanpur": [9, 12.027, 0.75],
  "Madras": [102, 19.713, 5.17],
  "TOTAL (CITIES)": [1201, None, None],
 },
}
