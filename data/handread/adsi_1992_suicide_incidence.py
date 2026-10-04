# ADSI 1992, Table 7: incidence and rate of suicides during 1992 (State & UT-wise; City-wise in Table 7 concluded)
# (raw/adsi/1992/year_wise/suicides-1992.pdf, pages 4-5; printed pages 33-34). Read from the page images; checked by
# scripts/check_handread.py. The table prints the number of suicides, the percentage share (not transcribed), the
# estimated mid-year population already in lakh (one decimal) and the rate of suicides (col.3 / col.5) to one decimal.
# 23 cities are printed, with no cities' total. Patna and Varanasi are "NR" (data not received): rows kept with None,
# so they are left out of the data.
KIND, YEAR, PUB = "suicide_incidence", 1992, "adsi"
SOURCE = "raw/adsi/1992/year_wise/suicides-1992.pdf"
PAGES = "4-5"
TITLE = 'Table 7: Incidence And Rate Of Suicides During 1992 (State & UT-wise / City-wise)'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [6525, 681.3, 9.6],
  "Arunachal Pradesh": [82, 8.9, 9.2],
  "Assam": [2967, 230.8, 12.9],
  "Bihar": [1236, 889.8, 1.4],
  "Goa": [174, 12.0, 14.5],
  "Gujarat": [3542, 423.3, 8.4],
  "Haryana": [698, 169.7, 4.1],
  "Himachal Pradesh": [136, 53.0, 2.6],
  "Jammu & Kashmir": [59, 79.5, 0.7],
  "Karnataka": [8136, 459.5, 17.7],
  "Kerala": [8103, 296.6, 27.3],
  "Madhya Pradesh": [7230, 680.3, 10.6],
  "Maharashtra": [9058, 810.3, 11.2],
  "Manipur": [34, 18.9, 1.8],
  "Meghalaya": [70, 18.3, 3.8],
  "Mizoram": [3, 7.2, 0.4],
  "Nagaland": [35, 12.6, 2.8],
  "Orissa": [3140, 324.6, 9.7],
  "Punjab": [511, 207.0, 2.5],
  "Rajasthan": [2251, 453.0, 5.0],
  "Sikkim": [47, 4.2, 11.2],
  "Tamil Nadu": [7981, 566.3, 14.1],
  "Tripura": [422, 28.4, 14.9],
  "Uttar Pradesh": [3324, 1425.1, 2.3],
  "West Bengal": [12797, 696.6, 18.4],
  "TOTAL (STATES)": [78561, 8557.2, 9.2],
 },
 "U.Ts.": {
  "A & N Islands": [125, 2.9, 43.1],
  "Chandigarh": [37, 6.8, 5.4],
  "D & N Haveli": [43, 1.4, 30.7],
  "Daman & Diu": [11, 1.0, 11.0],
  "Delhi": [787, 98.7, 8.0],
  "Lakshadweep": [0, 0.5, 0.0],
  "Pondicherry": [585, 8.3, 70.5],
  "TOTAL (U.TS.)": [1588, 119.6, 13.3],
 },
 "Grand": {
  "GRAND TOTAL": [80149, 8676.8, 9.2],
 },
 "Cities": {
  "Ahmedabad": [334, 33.9, 9.9],
  "Bangalore": [1311, 42.0, 31.2],
  "Bhopal": [61, 11.0, 5.5],
  "Bombay": [1186, 130.0, 9.1],
  "Calcutta": [237, 111.7, 2.1],
  "Coimbatore": [220, 11.6, 19.0],
  "Delhi": [601, 87.9, 6.8],
  "Hyderabad": [518, 44.3, 11.7],
  "Indore": [272, 11.4, 23.9],
  "Jaipur": [175, 15.7, 11.1],
  "Kanpur": [701, 21.7, 32.3],
  "Kochi": [225, 11.8, 19.1],
  "Lucknow": [158, 17.0, 9.3],
  "Ludhiana": [7, 10.4, 0.7],
  "Madras": [537, 54.6, 9.8],
  "Madurai": [270, 11.1, 24.3],
  "Nagpur": [306, 17.1, 17.9],
  "Patna": [None, 11.3, None],
  "Pune": [345, 25.7, 13.4],
  "Surat": [230, 15.7, 14.6],
  "Vadodara": [57, 11.5, 5.0],
  "Varanasi": [None, 10.5, None],
  "Vishakhapatnam": [177, 10.9, 16.2],
 },
}
