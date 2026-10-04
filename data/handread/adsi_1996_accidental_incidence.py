# ADSI 1996: the chapter's own Table-2(A) (incidence and rate of accidental deaths, State, UT & City-wise), cited on page
# 4 of raw/adsi/1996/year_wise/accidental-deaths-1996.pdf, is NOT among the PDFs we hold (the chapter PDF skips from page 4
# to charts). The accidental-death counts and the 1996 mid-year populations are instead read from Table-1.2 of the
# "Profile of Fatalities" part (raw/adsi/1996/year_wise/fatalities_0_1996.pdf, PDF page 6): "Number of Inopportune Deaths
# and its Share and Rate During 1995 and 1996 (State, UT & City-wise)", columns 8 (Accidents 1996) and 11 (Estimated
# mid-year population 1996, in lakh). That table prints no accidental-death rate (its rate, col. 12, is of suicides +
# accidents together), so the rate is None throughout. Read from the page image; every row was verified outside the
# checker: Suicides (col. 7) + Accidents (col. 8) = printed Total (col. 9) on every row, Total / population = the printed
# col. 12 rate on every row, the suicide column equals archived Table-2(S) (table-2s.pdf), and the State and UT columns
# (suicides, accidents, total, population) add to the printed TOTAL rows; the all-India 2,20,094 matches Table-2.2 on
# page 4 of the chapter. The city part has no printed total (cities add to 28,740 accidental deaths). The 1995 columns
# are not transcribed. Delhi appears as "Delhi (UT)" and "Delhi (City)"; "Total (All-India)" is entered as GRAND TOTAL.
KIND, YEAR, PUB = "accidental_incidence", 1996, "adsi"
SOURCE = 'raw/adsi/1996/year_wise/fatalities_0_1996.pdf'
PAGES = '6'
TITLE = 'Table-1.2: Number of Inopportune Deaths and its Share and Rate During 1995 and 1996 (State, UT & City-wise) -- Accidents 1996 and Estimated Mid-Year Population 1996 columns'
CHECK = "incidence"
CATS = ["Number of accidental deaths", "Estimated mid-year population (lakh)", "Rate of accidental deaths per lakh"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
ROWS = {
 "States": {
  'Andhra Pradesh': [17195, 728.8, None],
  'Arunachal Pradesh': [228, 9.9, None],
  'Assam': [3528, 251.1, None],
  'Bihar': [7589, 968.7, None],
  'Goa': [826, 13.0, None],
  'Gujarat': [14508, 453.8, None],
  'Haryana': [3428, 184.3, None],
  'Himachal Pradesh': [1298, 57.2, None],
  'Jammu & Kashmir': [1322, 86.9, None],
  'Karnataka': [11034, 487.3, None],
  'Kerala': [6070, 313.2, None],
  'Madhya Pradesh': [26348, 734.9, None],
  'Maharashtra': [50224, 875.5, None],
  'Manipur': [165, 20.8, None],
  'Meghalaya': [195, 20.1, None],
  'Mizoram': [129, 8.1, None],
  'Nagaland': [99, 14.3, None],
  'Orissa': [5732, 348.7, None],
  'Punjab': [3657, 219.2, None],
  'Rajasthan': [12515, 491.4, None],
  'Sikkim': [135, 4.8, None],
  'Tamil Nadu': [18917, 588.3, None],
  'Tripura': [206, 31.2, None],
  'Uttar Pradesh': [17536, 1526.2, None],
  'West Bengal': [10283, 744.3, None],
  'TOTAL (STATES)': [213167, 9182.0, None],
 },
 "U.Ts.": {
  'A & N Islands': [120, 3.4, None],
  'Chandigarh': [233, 8.1, None],
  'D & N Haveli': [90, 1.6, None],
  'Daman & Diu': [48, 1.1, None],
  'Delhi (UT)': [5873, 113.6, None],
  'Lakshadweep': [0, 0.6, None],
  'Pondicherry': [563, 9.0, None],
  'TOTAL (U.TS.)': [6927, 137.4, None],
 },
 "Grand": {
  'GRAND TOTAL': [220094, 9319.4, None],
 },
 "Cities": {
  'Ahmedabad': [1387, 38.1, None],
  'Bangalore': [2140, 49.7, None],
  'Bhopal': [285, 13.9, None],
  'Bombay': [6452, 157.9, None],
  'Calcutta': [690, 121.4, None],
  'Coimbatore': [329, 12.1, None],
  'Delhi (City)': [4978, 103.4, None],
  'Hyderabad': [1242, 57.8, None],
  'Indore': [988, 13.0, None],
  'Jaipur': [880, 18.8, None],
  'Kanpur': [1059, 22.8, None],
  'Kochi': [289, 15.0, None],
  'Lucknow': [442, 21.8, None],
  'Ludhiana': [138, 13.9, None],
  'Madras': [1964, 61.4, None],
  'Madurai': [252, 11.9, None],
  'Nagpur': [1221, 19.0, None],
  'Patna': [286, 12.1, None],
  'Pune': [1403, 30.7, None],
  'Surat': [835, 19.9, None],
  'Vadodara': [510, 14.1, None],
  'Varanasi': [495, 11.8, None],
  'Vishakhapatnam': [475, 14.3, None],
 },
}
