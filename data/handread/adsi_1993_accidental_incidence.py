# ADSI 1993, Table-2: incidence and rate of accidental deaths, State & UT-wise and City-wise
# (raw/adsi/1993/year_wise/accidental-deaths-1993.pdf, PDF pages 7-8). Read from the page images; checked by
# scripts/check_handread.py. Population is printed in lakh (estimated mid-year). The percentage-share column is not
# transcribed. The city part has no printed total. "Total (All - India)" is entered as GRAND TOTAL.
KIND, YEAR, PUB = "accidental_incidence", 1993, "adsi"
SOURCE = 'raw/adsi/1993/year_wise/accidental-deaths-1993.pdf'
PAGES = '7-8'
TITLE = 'Table-2: Incidence And Rate Of Accidental Deaths During 1993 (State & UT-wise; City-wise)'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  'Andhra Pradesh': [12472, 693.4, 18.0],
  'Arunachal Pradesh': [63, 9.2, 6.8],
  'Assam': [2331, 235.9, 9.9],
  'Bihar': [6913, 909.5, 7.7],
  'Goa': [811, 12.2, 66.5],
  'Gujarat': [11299, 430.9, 26.2],
  'Haryana': [2022, 173.4, 11.7],
  'Himachal Pradesh': [788, 54.0, 14.6],
  'Jammu & Kashmir': [634, 81.3, 7.8],
  'Karnataka': [11027, 466.7, 23.6],
  'Kerala': [5194, 300.7, 17.3],
  'Madhya Pradesh': [24600, 694.1, 35.4],
  'Maharashtra': [47364, 826.3, 57.3],
  'Manipur': [196, 19.4, 10.1],
  'Meghalaya': [295, 18.7, 15.8],
  'Mizoram': [75, 7.4, 10.1],
  'Nagaland': [36, 13.0, 2.8],
  'Orissa': [4686, 330.6, 14.2],
  'Punjab': [2632, 210.1, 12.5],
  'Rajasthan': [7775, 462.8, 16.8],
  'Sikkim': [98, 4.4, 22.3],
  'Tamil Nadu': [15928, 571.9, 27.9],
  'Tripura': [234, 29.1, 8.0],
  'Uttar Pradesh': [16446, 1450.6, 11.3],
  'West Bengal': [12186, 708.7, 17.2],
  'TOTAL (STATES)': [186105, 8714.3, 21.4],
 },
 "U.Ts.": {
  'A & N Islands': [110, 3.1, 35.5],
  'Chandigarh': [102, 7.1, 14.4],
  'D & N Haveli': [34, 1.5, 22.7],
  'Daman & Diu': [48, 1.1, 43.6],
  'Delhi': [5600, 102.2, 54.8],
  'Lakshadweep': [0, 0.6, 0.0],
  'Pondicherry': [358, 8.5, 42.1],
  'TOTAL (U.TS.)': [6252, 124.0, 50.4],
 },
 "Grand": {
  'GRAND TOTAL': [192357, 8838.3, 21.8],
 },
 "Cities": {
  'Ahmedabad': [1110, 35.2, 31.5],
  'Bangalore': [1351, 44.8, 30.2],
  'Bhopal': [454, 12.1, 37.5],
  'Bombay': [7653, 139.1, 55.0],
  'Calcutta': [629, 115.1, 5.5],
  'Coimbatore': [410, 11.5, 35.7],
  'Delhi': [4683, 92.1, 50.8],
  'Hyderabad': [1237, 49.2, 25.1],
  'Indore': [640, 11.9, 53.8],
  'Jaipur': [856, 16.7, 51.3],
  'Kanpur': [791, 21.3, 37.1],
  'Kochi': [250, 12.8, 19.5],
  'Lucknow': [704, 18.8, 37.4],
  'Ludhiana': [90, 11.8, 7.6],
  'Madras': [738, 57.3, 12.9],
  'Madurai': [205, 11.3, 18.1],
  'Nagpur': [1039, 17.6, 59.0],
  'Patna': [124, 11.5, 10.8],
  'Pune': [2086, 27.3, 76.4],
  'Surat': [640, 17.1, 37.4],
  'Vadodara': [419, 12.4, 33.8],
  'Varanasi': [772, 11.0, 70.2],
  'Vishakhapatnam': [366, 12.0, 30.5],
 },
}
