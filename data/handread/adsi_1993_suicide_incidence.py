# ADSI 1993, Table 7: incidence and rate of suicides during 1993 (State & UT-wise; City-wise in Table 7 concluded)
# (raw/adsi/1993/year_wise/suicides-1993.pdf, pages 4-5; printed pages 39-40). Read from the page images; checked by
# scripts/check_handread.py. The table prints the number of suicides, the percentage share (not transcribed), the
# estimated mid-year population already in lakh (one decimal) and the rate of suicides (col.3 / col.5) to one decimal.
# 23 cities are printed, with no cities' total.
# The UTs' populations as printed add to 124.1 lakh against the printed Total (UTs) 124.0 (rounding of the
# one-decimal figures); left as printed.
KIND, YEAR, PUB = "suicide_incidence", 1993, "adsi"
SOURCE = "raw/adsi/1993/year_wise/suicides-1993.pdf"
PAGES = "4-5"
TITLE = 'Table-7: Incidence And Rate Of Suicides During 1993 (State & UT-wise / City-wise)'
CHECK = "incidence"
CATS = ["Number of suicides", "Estimated mid-year population (lakh)", "Rate of suicides per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [7850, 693.4, 11.3],
  "Arunachal Pradesh": [56, 9.2, 6.1],
  "Assam": [2557, 235.9, 10.8],
  "Bihar": [1643, 909.5, 1.8],
  "Goa": [203, 12.2, 16.6],
  "Gujarat": [3431, 430.9, 8.0],
  "Haryana": [1254, 173.4, 7.2],
  "Himachal Pradesh": [170, 54.0, 3.1],
  "Jammu & Kashmir": [70, 81.3, 0.9],
  "Karnataka": [8055, 466.7, 17.3],
  "Kerala": [8124, 300.7, 27.0],
  "Madhya Pradesh": [6251, 694.1, 9.0],
  "Maharashtra": [10338, 826.3, 12.5],
  "Manipur": [19, 19.4, 1.0],
  "Meghalaya": [71, 18.7, 3.8],
  "Mizoram": [25, 7.4, 3.4],
  "Nagaland": [20, 13.0, 1.5],
  "Orissa": [3345, 330.6, 10.1],
  "Punjab": [493, 210.1, 2.3],
  "Rajasthan": [2729, 462.8, 5.9],
  "Sikkim": [48, 4.4, 10.9],
  "Tamil Nadu": [7895, 571.9, 13.8],
  "Tripura": [543, 29.1, 18.7],
  "Uttar Pradesh": [5947, 1450.6, 4.1],
  "West Bengal": [11381, 708.7, 16.1],
  "TOTAL (STATES)": [82518, 8714.3, 9.5],
 },
 "U.Ts.": {
  "A & N Islands": [110, 3.1, 35.5],
  "Chandigarh": [58, 7.1, 8.2],
  "D & N Haveli": [39, 1.5, 26.0],
  "Daman & Diu": [20, 1.1, 18.2],
  "Delhi": [883, 102.2, 8.6],
  "Lakshadweep": [0, 0.6, 0.0],
  "Pondicherry": [616, 8.5, 72.5],
  "TOTAL (U.TS.)": [1726, 124.0, 13.9],
 },
 "Grand": {
  "GRAND TOTAL": [84244, 8838.3, 9.5],
 },
 "Cities": {
  "Ahmedabad": [363, 35.2, 10.3],
  "Bangalore": [798, 44.8, 17.8],
  "Bhopal": [166, 12.1, 13.7],
  "Bombay": [1105, 139.1, 7.9],
  "Calcutta": [239, 115.1, 2.1],
  "Coimbatore": [203, 11.5, 17.7],
  "Delhi": [723, 92.1, 7.9],
  "Hyderabad": [540, 49.2, 11.0],
  "Indore": [261, 11.9, 21.9],
  "Jaipur": [204, 16.7, 12.2],
  "Kanpur": [621, 21.3, 29.2],
  "Kochi": [218, 12.8, 17.0],
  "Lucknow": [160, 18.8, 8.5],
  "Ludhiana": [15, 11.8, 1.3],
  "Madras": [1156, 57.3, 20.2],
  "Madurai": [290, 11.3, 25.7],
  "Nagpur": [277, 17.6, 15.7],
  "Patna": [30, 11.5, 2.6],
  "Pune": [352, 27.3, 12.9],
  "Surat": [111, 17.1, 6.5],
  "Vadodara": [124, 12.4, 10.0],
  "Varanasi": [242, 11.0, 22.0],
  "Vishakhapatnam": [175, 12.0, 14.6],
 },
}
