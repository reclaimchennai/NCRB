# ADSI 1992, Table-2: incidence and rate of accidental deaths, State & UT-wise and City-wise
# (raw/adsi/1992/year_wise/accidental-deaths-1992.pdf, PDF pages 7-8). Read from the page images; checked by
# scripts/check_handread.py. Population is printed in lakh (estimated mid-year). The percentage-share column is not
# transcribed. The city part has no printed total. Patna and Varanasi: NR (data not received) -> None.
# "Total (All-India)" is entered as GRAND TOTAL.
KIND, YEAR, PUB = "accidental_incidence", 1992, "adsi"
SOURCE = 'raw/adsi/1992/year_wise/accidental-deaths-1992.pdf'
PAGES = '7-8'
TITLE = 'Table-2: Incidence And Rate Of Accidental Deaths During 1992 (State & UT-wise; City-wise)'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {
    ("Madras", "Rate of accidental deaths per lakh"): (13.6, 13.8, "printed 13.6 (clear); count 754 agrees with Table-5 of the same PDF (page 28, read from the image: 542 + 212 = 754) and Appendix I + II (14 natural + 740 un-natural), population 54.6 lakh agrees with CII 1992 (13174 IPC crimes at 241.3 per lakh), and 754/54.6 = 13.8"),
}
ROWS = {
 "States": {
  'Andhra Pradesh': [13175, 681.3, 19.3],
  'Arunachal Pradesh': [202, 8.9, 22.7],
  'Assam': [2604, 230.8, 11.3],
  'Bihar': [6974, 889.8, 7.8],
  'Goa': [712, 12.0, 59.3],
  'Gujarat': [11107, 423.3, 26.2],
  'Haryana': [2468, 169.7, 14.5],
  'Himachal Pradesh': [769, 53.0, 14.5],
  'Jammu & Kashmir': [1009, 79.5, 12.7],
  'Karnataka': [12924, 459.5, 28.1],
  'Kerala': [5501, 296.6, 18.5],
  'Madhya Pradesh': [26227, 680.3, 38.6],
  'Maharashtra': [41233, 810.3, 50.9],
  'Manipur': [122, 18.9, 6.5],
  'Meghalaya': [214, 18.3, 11.7],
  'Mizoram': [129, 7.2, 17.9],
  'Nagaland': [24, 12.6, 1.9],
  'Orissa': [4528, 324.6, 13.9],
  'Punjab': [2028, 207.0, 9.8],
  'Rajasthan': [7566, 453.0, 16.7],
  'Sikkim': [177, 4.2, 42.1],
  'Tamil Nadu': [13751, 566.3, 24.3],
  'Tripura': [235, 28.4, 8.3],
  'Uttar Pradesh': [22890, 1425.1, 16.1],
  'West Bengal': [12233, 696.6, 17.6],
  'TOTAL (STATES)': [188802, 8557.2, 22.1],
 },
 "U.Ts.": {
  'A & N Islands': [120, 2.9, 41.4],
  'Chandigarh': [113, 6.8, 16.6],
  'D & N Haveli': [43, 1.4, 30.7],
  'Daman & Diu': [29, 1.0, 29.0],
  'Delhi': [5507, 98.7, 55.8],
  'Lakshadweep': [2, 0.5, 4.0],
  'Pondicherry': [294, 8.3, 35.4],
  'TOTAL (U.TS.)': [6108, 119.6, 51.1],
 },
 "Grand": {
  'GRAND TOTAL': [194910, 8676.8, 22.5],
 },
 "Cities": {
  'Ahmedabad': [1091, 33.9, 32.2],
  'Bangalore': [1872, 42.0, 44.6],
  'Bhopal': [214, 11.0, 19.5],
  'Bombay': [8997, 130.0, 69.2],
  'Calcutta': [596, 111.7, 5.3],
  'Coimbatore': [443, 11.6, 38.2],
  'Delhi': [4481, 87.9, 51.0],
  'Hyderabad': [1120, 44.3, 25.3],
  'Indore': [629, 11.4, 55.2],
  'Jaipur': [857, 15.7, 54.6],
  'Kanpur': [802, 21.7, 37.0],
  'Kochi': [235, 11.8, 19.9],
  'Lucknow': [523, 17.0, 30.8],
  'Ludhiana': [48, 10.4, 4.6],
  'Madras': [754, 54.6, 13.8],
  'Madurai': [329, 11.1, 29.6],
  'Nagpur': [986, 17.1, 57.7],
  'Patna': [None, 11.3, None],
  'Pune': [1959, 25.7, 76.2],
  'Surat': [597, 15.7, 38.0],
  'Vadodara': [391, 11.5, 34.0],
  'Varanasi': [None, 10.5, None],
  'Vishakhapatnam': [379, 10.9, 34.8],
 },
}
