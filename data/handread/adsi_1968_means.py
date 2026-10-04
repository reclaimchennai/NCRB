# ADSI 1968, Appendix VI: suicides by means adopted, States / UTs / cities (raw/adsi/1968/table_content/1680151746appendix-619681.pdf,
# pages 1-2: page 1 the States, page 2 the UTs, Grand Total and cities). Read from the page images; '—' (nil) is 0.
# The cities' totals row is printed without a label. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1968, "adsi"
SOURCE = "raw/adsi/1968/table_content/1680151746appendix-619681.pdf"
PAGES = "1-2"
TITLE = "Appendix VI: Statement of Number of suicides in States/U. Ts./Cities during 1968 (By means adopted for committing suicides)"
CATS = ["By Railways", "By Machine", "By Fire-Arms", "By Weapons", "By Taking poison", "By Fire", "By Drowning",
        "By Hanging", "By Jumping", "By Other ways", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [312, 5, 3, 4, 519, 133, 1360, 469, 66, 478, 3349],
  "Assam": [67, 0, 8, 0, 11, 8, 125, 412, 7, 177, 815],
  "Bihar": [567, 3, 3, 12, 81, 120, 397, 123, 65, 866, 2237],
  "Gujarat": [85, 4, 7, 6, 247, 276, 383, 194, 111, 410, 1723],
  "Haryana": [60, 6, 2, 0, 0, 21, 208, 157, 35, 214, 703],
  "Jammu & Kashmir": [0, 0, 0, 0, 1, 1, 41, 0, 0, 0, 43],
  "Kerala": [124, 1, 4, 3, 789, 22, 654, 914, 77, 333, 2921],
  "Madhya Pradesh": [139, 4, 23, 29, 116, 257, 609, 550, 65, 442, 2234],
  "Maharashtra": [169, 4, 6, 7, 730, 343, 1086, 355, 140, 592, 3432],
  "Mysore": [18, 0, 9, 1, 637, 112, 1109, 532, 131, 534, 3083],
  "Nagaland": [0, 0, 3, 1, 0, 0, 7, 2, 0, 3, 16],
  "Orissa": [310, 1, 0, 3, 650, 22, 355, 677, 12, 319, 2349],
  "Punjab": [46, 11, 12, 6, 17, 19, 52, 55, 3, 80, 301],
  "Rajasthan": [142, 7, 14, 4, 24, 50, 289, 47, 7, 131, 715],
  "Tamil Nadu": [73, 1, 3, 9, 2343, 154, 1257, 938, 91, 748, 5617],
  "Uttar Pradesh": [653, 60, 132, 136, 159, 398, 906, 558, 191, 1278, 4471],
  "West Bengal": [172, 76, 102, 18, 1723, 131, 580, 1642, 21, 1279, 5744],
  "TOTAL (STATES)": [2937, 183, 331, 239, 8047, 2067, 9418, 7625, 1022, 7884, 39753],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 1, 0, 8, 0, 1, 17, 0, 0, 27],
  "Chandigarh": [0, 0, 0, 0, 2, 4, 2, 0, 1, 1, 10],
  "Dadra & Nagar Haveli": [0, 0, 0, 0, 2, 0, 3, 11, 1, 15, 32],
  "Delhi": [56, 0, 2, 0, 20, 25, 21, 17, 5, 16, 162],
  "Goa, Daman & Diu": [0, 0, 0, 1, 8, 14, 16, 12, 0, 3, 54],
  "Himachal Pradesh": [0, 1, 5, 0, 2, 0, 14, 9, 1, 27, 59],
  "Laccadives": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Manipur": [0, 0, 0, 0, 3, 0, 14, 14, 0, 14, 45],
  "Pondicherry": [3, 0, 0, 1, 107, 5, 52, 35, 12, 62, 277],
  "Tripura": [0, 0, 1, 0, 20, 9, 95, 84, 16, 44, 269],
  "TOTAL (U.TS.)": [59, 1, 9, 2, 172, 57, 218, 199, 36, 182, 935],
 },
 "Cities": {
  "Ahmedabad": [0, 0, 1, 0, 35, 29, 32, 1, 16, 44, 158],
  "Bangalore": [0, 0, 0, 0, 14, 3, 78, 6, 4, 23, 128],
  "Bombay": [0, 0, 0, 1, 40, 21, 9, 5, 7, 35, 118],
  "Calcutta": [0, 0, 0, 3, 10, 11, 1, 50, 3, 1, 79],
  "Delhi": [56, 0, 2, 0, 20, 23, 18, 15, 4, 14, 152],
  "Hyderabad": [0, 0, 1, 0, 35, 37, 34, 3, 1, 97, 208],
  "Kanpur": [2, 0, 2, 0, 4, 15, 0, 10, 6, 19, 58],
  "Madras": [0, 0, 0, 0, 71, 1, 14, 24, 0, 3, 113],
  "TOTAL (CITIES)": [58, 0, 6, 4, 229, 140, 186, 114, 41, 236, 1014],
 },
 "Grand": {"GRAND TOTAL": [2996, 184, 340, 241, 8219, 2124, 9636, 7824, 1058, 8066, 40688]},
}
