# ADSI 1982, Appendix II: road accident deaths, States / UTs / cities (raw/adsi/1982/table_content/appendix-2_1982.pdf, pages 1-4).
# Read from the page images. This edition prints no State-wise number of road accidents or persons injured, only the
# deaths: Persons killed is the 'On Roads' (road accident deaths) Male and Female columns; the table prints no Total, so Persons killed = Male + Female and every Male and every Female column was first checked against the printed Total (States), Total (UTs), Grand Total and Total (Cities).
# Road accidents (cases) and Persons injured are None (not printed).
# Madras city is printed as 8 road accident deaths (8 male, nil female) -- as printed; Lucknow is N.A.
KIND, YEAR, PUB = "traffic", 1982, "adsi"
SOURCE = "raw/adsi/1982/table_content/appendix-2_1982.pdf"
PAGES = "1-4"
TITLE = "Appendix II: State-wise Distribution of Accidental Deaths due to Other Causes during 1982"
CHECK = "columns"
CATS = ['Road accidents (cases)', 'Persons injured', 'Persons killed']
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ('TOTAL (CITIES)', 'Persons killed'): (3609, None, 'printed 3,031 males + 578 females = 3,609; Lucknow is printed N.A., yet the place rows add to 2,936 + 570 only: the 95 + 8 difference is figures in the printed total that the page does not show for any city, so the total is left out of the column check'),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [None, None, 2700],
  "Assam": [None, None, 212],
  "Bihar": [None, None, 658],
  "Gujarat": [None, None, 318],
  "Haryana": [None, None, 329],
  "Himachal Pradesh": [None, None, 146],
  "Jammu & Kashmir": [None, None, 158],
  "Karnataka": [None, None, 1592],
  "Kerala": [None, None, 490],
  "Madhya Pradesh": [None, None, 2162],
  "Maharashtra": [None, None, 2016],
  "Manipur": [None, None, 79],
  "Meghalaya": [None, None, 34],
  "Nagaland": [None, None, 72],
  "Orissa": [None, None, 435],
  "Punjab": [None, None, 546],
  "Rajasthan": [None, None, 751],
  "Sikkim": [None, None, 54],
  "Tamil Nadu": [None, None, 3284],
  "Tripura": [None, None, 49],
  "Uttar Pradesh": [None, None, 2829],
  "West Bengal": [None, None, 1975],
  "TOTAL (STATES)": [None, None, 20889],
 },
 "U.Ts.": {
  "A & N Islands": [None, None, 23],
  "Arunachal Pradesh": [None, None, 14],
  "Chandigarh": [None, None, 22],
  "D & N Haveli": [None, None, 1],
  "Delhi": [None, None, 1105],
  "Goa, Daman & Diu": [None, None, 59],
  "Lakshadweep": [None, None, 0],
  "Mizoram": [None, None, 33],
  "Pondicherry": [None, None, 53],
  "TOTAL (U.TS.)": [None, None, 1310],
 },
 "Cities": {
  "Ahmedabad": [None, None, 27],
  "Bangalore": [None, None, 293],
  "Bombay": [None, None, 1071],
  "Calcutta": [None, None, 420],
  "Delhi": [None, None, 960],
  "Hyderabad": [None, None, 289],
  "Jaipur": [None, None, 222],
  "Kanpur": [None, None, 10],
  "Lucknow": [None, None, None],
  "Madras": [None, None, 8],
  "Nagpur": [None, None, 68],
  "Pune": [None, None, 138],
  "TOTAL (CITIES)": [None, None, None],
 },
 "Grand": {"GRAND TOTAL": [None, None, 22199]},
}
