# Crime in India 1958, Appendices I, III, V, ... XXIII (the "-CASES" appendices): cognizable crime cases reported during
# the year, by State, Union Territory and city, under each head (raw/cii/1958/year_wise/1689773342appendicesall3-1958.pdf,
# the left-hand pages 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46). The 1958 edition prints no single State x head
# table: each head has its own appendix (I Total cognizable crime, III Murder, V Kidnapping and abduction, VII Dacoity,
# IX Robbery, XI House breaking, XIII Cattle thefts, XV Ordinary thefts, XVII Riots, XIX Criminal breach of trust, XXI
# Cheating, XXIII Counterfeiting), each printing States, Union Territories (with a Grand Total) and Cities (with their own
# Total) on one page; each column here is that appendix's column 5, "Cases reported during the year". The heads printed
# do not cover all IPC crime, so they do not add up to the total: CHECK = "columns", each head checked against the printed
# totals. '..' (nil) is 0. Delhi is printed both as a Union Territory and as a city with the same figures. Some figures on
# the Appendix I and Appendix V pages carry hand marks on the scan; every figure read agrees with the printed totals.
KIND, YEAR, PUB = "crime", 1958, "cii"
SOURCE = "raw/cii/1958/year_wise/1689773342appendicesall3-1958.pdf"
PAGES = "2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46"
TITLE = "Appendices I-XXIII (cases): Total cognizable crime and each head - cases reported during the year, by State / Union Territory / city, 1958"
CATS = ["Murder", "Kidnapping and abduction", "Dacoity", "Robbery", "House breaking", "Cattle thefts", "Ordinary thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
    ('Kerala', 'Kidnapping and abduction'): (61, 51, "printed 61, the first digit retouched by hand on the scan; the States total (5,719) needs 51, and so does the row's own disposal: 2 pending investigation + 19 pending in court + 51 reported = 40 not investigated + 6 not detected + 9 convicted + 17 acquitted"),
}
ROWS = {
 "States": {
  "A. Pradesh": [898, 147, 91, 189, 6684, 1834, 12348, 1910, 953, 507, 20, 35762],
  "Assam": [337, 313, 260, 208, 4397, 364, 4648, 1163, 225, 221, 86, 17261],
  "Bihar": [924, 411, 1463, 919, 20389, 840, 18837, 3597, 961, 521, 151, 59208],
  "Bombay": [1955, 754, 598, 2253, 18199, 3012, 41375, 1963, 3373, 1976, 31, 104930],
  "Jammu & Kashmir": [75, 100, 59, 91, 1111, 205, 563, 251, 93, 36, 2, 3938],
  "Kerala": [295, 51, 29, 111, 2032, 191, 3218, 1478, 272, 122, 5, 15586],
  "M. Pradesh": [1203, 693, 414, 768, 16328, 3755, 27596, 1595, 1348, 1224, 70, 70741],
  "Madras": [809, 546, 79, 305, 7276, 4394, 20036, 2335, 1954, 748, 46, 54612],
  "Mysore": [643, 190, 99, 199, 4100, 962, 8046, 933, 732, 288, 8, 23418],
  "Orissa": [281, 110, 76, 208, 4714, 635, 8406, 916, 634, 385, 23, 20895],
  "Punjab": [596, 397, 12, 115, 4012, 631, 4906, 203, 500, 428, 5, 19128],
  "Rajasthan": [428, 459, 75, 408, 4733, 1960, 3845, 1004, 310, 329, 6, 19156],
  "U. Pradesh": [1637, 797, 825, 477, 17264, 3890, 23089, 3045, 2430, 1010, 49, 66154],
  "W. Bengal": [467, 751, 503, 747, 10928, 879, 28201, 4321, 1800, 1284, 45, 65290],
  "TOTAL (STATES)": [10548, 5719, 4583, 6998, 122167, 23552, 205114, 24714, 15585, 9079, 547, 576079],
 },
 "U.Ts.": {
  "A. & N. Islands": [4, 0, 0, 0, 26, 4, 59, 3, 4, 4, 0, 196],
  "Delhi": [65, 192, 2, 43, 1429, 62, 5931, 68, 343, 333, 3, 10357],
  "H. Pradesh": [13, 24, 7, 22, 240, 14, 265, 26, 37, 26, 0, 1102],
  "Manipur": [10, 74, 28, 10, 118, 55, 220, 25, 23, 41, 0, 851],
  "Tripura": [14, 34, 27, 38, 663, 141, 626, 105, 18, 16, 3, 2201],
  "Naga Hills": [7, 0, 11, 9, 52, 4, 56, 1, 7, 4, 2, 201],
  "TOTAL (U.TS.)": [113, 324, 75, 122, 2528, 280, 7157, 228, 432, 424, 8, 14908],
 },
 "Grand": {
  "GRAND TOTAL": [10661, 6043, 4658, 7120, 124695, 23832, 212271, 24942, 16017, 9503, 555, 590987],
 },
 "Cities": {
  "Bangalore": [23, 57, 0, 19, 585, 64, 2324, 34, 178, 100, 1, 4100],
  "Bombay": [112, 147, 11, 150, 1533, 32, 8819, 80, 986, 710, 3, 15781],
  "Calcutta": [37, 142, 4, 19, 1000, 78, 6636, 339, 538, 452, 28, 12247],
  "Delhi": [65, 192, 2, 43, 1429, 62, 5931, 68, 343, 333, 3, 10357],
  "Hyderabad": [8, 30, 0, 5, 792, 53, 1694, 42, 196, 102, 0, 3542],
  "Kanpur": [14, 35, 2, 1, 189, 9, 1027, 12, 195, 69, 4, 1828],
  "Madras": [10, 36, 1, 13, 205, 63, 4118, 28, 375, 211, 0, 6288],
  "TOTAL (CITIES)": [269, 639, 20, 250, 5733, 361, 30549, 603, 2811, 1977, 39, 54143],
 },
}
