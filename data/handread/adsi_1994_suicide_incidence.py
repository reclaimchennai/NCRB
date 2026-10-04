# ADSI 1994, Table 7: incidence and rate of suicides during 1994 (State & UT-wise; City-wise in Table 7 concluded)
# (raw/adsi/1994/archived/suicides-94.pdf, pages 4-5; printed pages 56-57). Read from the page images; checked by
# scripts/check_handread.py. The table prints the number of suicides, the percentage share (not transcribed), the
# estimated mid-year population already in lakh (one decimal) and the rate of suicides (col.3 / col.5) to one decimal.
# 23 cities are printed, with no cities' total.
KIND, YEAR, PUB = "suicide_incidence", 1994, "adsi"
SOURCE = "raw/adsi/1994/archived/suicides-94.pdf"
PAGES = "4-5"
TITLE = 'Table 7: Incidence And Rate Of Suicides During 1994 (State & UT-wise / City-wise)'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [7231, 705.3, 10.3],
  "Arunachal Pradesh": [51, 9.4, 5.4],
  "Assam": [2564, 241.1, 10.6],
  "Bihar": [1436, 929.3, 1.5],
  "Goa": [237, 12.5, 19.0],
  "Gujarat": [3793, 438.5, 8.6],
  "Haryana": [938, 177.1, 5.3],
  "Himachal Pradesh": [272, 55.1, 4.9],
  "Jammu & Kashmir": [44, 83.2, 0.5],
  "Karnataka": [9050, 473.7, 19.1],
  "Kerala": [8533, 304.9, 28.0],
  "Madhya Pradesh": [7024, 707.8, 9.9],
  "Maharashtra": [10782, 842.7, 12.8],
  "Manipur": [34, 19.8, 1.7],
  "Meghalaya": [50, 19.2, 2.6],
  "Mizoram": [42, 7.7, 5.5],
  "Nagaland": [37, 13.4, 2.8],
  "Orissa": [3013, 336.6, 9.0],
  "Punjab": [545, 213.1, 2.6],
  "Rajasthan": [2691, 472.5, 5.7],
  "Sikkim": [57, 4.5, 12.7],
  "Tamil Nadu": [9248, 577.4, 16.0],
  "Tripura": [518, 29.8, 17.4],
  "Uttar Pradesh": [6938, 1476.0, 4.7],
  "West Bengal": [12389, 720.8, 17.2],
  "TOTAL (STATES)": [87517, 8871.4, 9.9],
 },
 "U.Ts.": {
  "A & N Islands": [122, 3.2, 38.1],
  "Chandigarh": [119, 7.4, 16.1],
  "D & N Haveli": [37, 1.5, 24.7],
  "Daman & Diu": [7, 1.1, 6.4],
  "Delhi": [803, 105.9, 7.6],
  "Lakshadweep": [1, 0.6, 1.7],
  "Pondicherry": [589, 8.6, 68.5],
  "TOTAL (U.TS.)": [1678, 128.3, 13.1],
 },
 "Grand": {
  "GRAND TOTAL": [89195, 8999.7, 9.9],
 },
 "Cities": {
  "Ahmedabad": [384, 36.2, 10.6],
  "Bangalore": [1116, 46.4, 24.1],
  "Bhopal": [235, 12.7, 18.5],
  "Bombay": [1334, 145.1, 9.2],
  "Calcutta": [235, 117.1, 2.0],
  "Coimbatore": [250, 11.7, 21.4],
  "Delhi": [588, 95.7, 6.1],
  "Hyderabad": [564, 51.9, 10.9],
  "Indore": [270, 12.2, 22.1],
  "Jaipur": [248, 17.4, 14.3],
  "Kanpur": [663, 21.8, 30.4],
  "Kochi": [242, 13.5, 17.9],
  "Lucknow": [63, 19.8, 3.2],
  "Ludhiana": [12, 12.5, 1.0],
  "Madras": [1007, 58.6, 17.2],
  "Madurai": [214, 11.5, 18.6],
  "Nagpur": [152, 18.1, 8.4],
  "Patna": [125, 11.7, 10.7],
  "Pune": [353, 28.4, 12.4],
  "Surat": [182, 18.0, 10.1],
  "Vadodara": [150, 12.9, 11.6],
  "Varanasi": [328, 11.2, 29.3],
  "Vishakhapatnam": [163, 12.7, 12.8],
 },
}
