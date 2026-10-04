# ADSI 1968, Appendix V: number of suicides in States / U.Ts. / cities by causes, pages 1-2. Read from the page images;
# "—" (nil) is 0. This table prints no percentages. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1968, "adsi"
SOURCE = "raw/adsi/1968/table_content/1680151773appendix-51968.pdf"
PAGES = "1-2"
TITLE = "Appendix V: Statement of Number of suicides in States/U.Ts./Cities during 1968 (By causes of suicides)"
CATS = ["Failure in examination", "Quarrel with parents/in-laws", "Quarrel with married partner", "Poverty",
        "Love Affairs", "Insanity", "Dispute over property", "Dreadful Disease", "Other causes", "Total"]
# This table prints no percentages; the one change below rests on the row sum and the column total instead.
CORRECTIONS = {
    ("Punjab", "Total"): (30, 301, "printed 30, a digit dropped; the categories add up to 301 and the States' Totals add up to the printed 39,753 only with 301 (no percentages printed in this table)"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [31, 184, 163, 186, 33, 40, 153, 1167, 1392, 3349],
  "Assam": [10, 41, 25, 28, 59, 22, 1, 112, 517, 815],
  "Bihar": [35, 59, 76, 23, 26, 64, 0, 50, 1904, 2237],
  "Gujarat": [42, 145, 110, 74, 37, 148, 13, 227, 927, 1723],
  "Haryana": [32, 121, 24, 62, 25, 9, 0, 97, 333, 703],
  "Jammu & Kashmir": [42, 1, 0, 0, 0, 0, 0, 0, 0, 43],
  "Kerala": [157, 324, 118, 386, 221, 107, 41, 264, 1303, 2921],
  "Madhya Pradesh": [37, 209, 193, 48, 43, 69, 54, 463, 1118, 2234],
  "Maharashtra": [36, 203, 202, 158, 49, 139, 55, 649, 1941, 3432],
  "Mysore": [84, 140, 182, 273, 96, 53, 55, 524, 1676, 3083],
  "Nagaland": [0, 0, 0, 0, 1, 0, 0, 0, 15, 16],
  "Orissa": [38, 330, 154, 41, 91, 34, 32, 365, 1264, 2349],
  "Punjab": [9, 42, 14, 11, 9, 19, 18, 22, 157, 301],
  "Rajasthan": [9, 62, 40, 16, 11, 18, 2, 96, 461, 715],
  "Tamil Nadu": [87, 361, 318, 211, 230, 67, 64, 1349, 2930, 5617],
  "Uttar Pradesh": [364, 282, 219, 150, 116, 213, 83, 588, 2456, 4471],
  "West Bengal": [526, 808, 627, 84, 272, 204, 12, 958, 2253, 5744],
  "TOTAL (STATES)": [1539, 3312, 2465, 1751, 1319, 1206, 583, 6931, 20647, 39753],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 2, 2, 1, 5, 0, 0, 17, 27],
  "Chandigarh": [0, 0, 1, 0, 0, 0, 0, 2, 7, 10],
  "Dadra & Nagar Haveli": [0, 5, 1, 2, 0, 2, 0, 2, 20, 32],
  "Delhi": [16, 10, 14, 5, 7, 8, 2, 31, 69, 162],
  "Goa, Daman & Diu": [1, 5, 5, 0, 2, 9, 0, 10, 22, 54],
  "Himachal Pradesh": [3, 1, 5, 1, 3, 3, 0, 4, 39, 59],
  "Laccadives": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Manipur": [0, 1, 0, 5, 2, 1, 0, 8, 28, 45],
  "Pondicherry": [1, 14, 21, 7, 3, 0, 23, 56, 152, 277],
  "Tripura": [14, 2, 4, 6, 3, 2, 0, 14, 224, 269],
  "TOTAL (U.TS.)": [35, 38, 53, 28, 21, 30, 25, 127, 578, 935],
 },
 "Cities": {
  "Ahmedabad": [1, 8, 7, 10, 4, 2, 1, 15, 110, 158],
  "Bangalore": [51, 0, 1, 15, 0, 0, 0, 10, 51, 128],
  "Bombay": [2, 8, 5, 16, 11, 4, 1, 13, 58, 118],
  "Calcutta": [3, 5, 4, 6, 6, 3, 1, 19, 32, 79],
  "Delhi": [15, 10, 14, 5, 7, 8, 1, 31, 61, 152],
  "Hyderabad": [2, 31, 2, 5, 3, 2, 0, 27, 136, 208],
  "Kanpur": [6, 1, 0, 1, 0, 0, 0, 2, 48, 58],
  "Madras": [4, 2, 17, 8, 12, 2, 0, 32, 36, 113],
  "TOTAL (CITIES)": [84, 65, 50, 66, 43, 21, 4, 149, 532, 1014],
 },
 "Grand": {"GRAND TOTAL": [1574, 3350, 2518, 1779, 1340, 1236, 608, 7058, 21225, 40688]},
}
