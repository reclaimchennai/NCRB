# ADSI 1985, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1985/table_content/appendix-2_1985.pdf, pages 1-3).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'On Roads' (road accident deaths) Male and Female columns; the table prints no Total, so Persons killed = Male + Female and every Male and every Female column was first checked against the printed Total (States), Total (UTs), Grand Total and Total (Cities).
# Road accidents (cases) and Persons injured are None (not printed).
KIND, YEAR, PUB = "traffic", 1985, "adsi"
SOURCE = "raw/adsi/1985/table_content/appendix-2_1985.pdf"
PAGES = "1-3"
TITLE = "Appendix II: State-wise Distribution of Accidental Deaths due to Other Causes during 1985"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ('Kanpur', 'Persons killed'): (194, 294, "Total road accident deaths, males, printed 168; the row's own (a) motor accidents 238 + (b) other road accidents 30 = 268, and with 268 the Cities male column adds to the printed Total (Cities) 3,876 (no percentage is printed in this table); Persons killed = males + females = 268 + 26"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 2988],
  "Assam": [None, None, 276],
  "Bihar": [None, None, 936],
  "Gujarat": [None, None, 419],
  "Haryana": [None, None, 412],
  "Himachal Pradesh": [None, None, 149],
  "Jammu & Kashmir": [None, None, 409],
  "Karnataka": [None, None, 2036],
  "Kerala": [None, None, 986],
  "Madhya Pradesh": [None, None, 2588],
  "Maharashtra": [None, None, 2350],
  "Manipur": [None, None, 86],
  "Meghalaya": [None, None, 61],
  "Nagaland": [None, None, 19],
  "Orissa": [None, None, 549],
  "Punjab": [None, None, 592],
  "Rajasthan": [None, None, 912],
  "Sikkim": [None, None, 47],
  "Tamil Nadu": [None, None, 5841],
  "Tripura": [None, None, 80],
  "Uttar Pradesh": [None, None, 4014],
  "West Bengal": [None, None, 2423],
  "TOTAL (STATES)": [None, None, 28173],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 12],
  "Arunachal Pradesh": [None, None, 35],
  "Chandigarh": [None, None, 32],
  "D & N Haveli": [None, None, 1],
  "Delhi": [None, None, 1369],
  "Goa, Daman & Diu": [None, None, 119],
  "Lakshadweep": [None, None, 1],
  "Mizoram": [None, None, 37],
  "Pondicherry": [None, None, 52],
  "TOTAL (U.TS.)": [None, None, 1658],
 },
 "Cities": {
  "Ahmedabad": [None, None, 34],
  "Bangalore": [None, None, 212],
  "Bombay": [None, None, 1142],
  "Calcutta": [None, None, 420],
  "Delhi": [None, None, 1181],
  "Hyderabad": [None, None, 243],
  "Jaipur": [None, None, 156],
  "Kanpur": [None, None, 294],
  "Lucknow": [None, None, 176],
  "Madras": [None, None, 391],
  "Nagpur": [None, None, 130],
  "Pune": [None, None, 178],
  "TOTAL (CITIES)": [None, None, 4557],
 },
 "Grand": {"GRAND TOTAL": [None, None, 29831]},
}
