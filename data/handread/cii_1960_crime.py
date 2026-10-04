# Crime in India 1960, Appendices I, III, V, ... XXIII (the "-CASES" appendices): cognizable crime cases reported during
# the year, by State, Union Territory and city, under each head (raw/cii/1960/year_wise/1689772159appendicesall1.pdf, the
# left-hand pages 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45). The 1960 edition prints no single State x head table:
# each head has its own appendix (I Total cognizable crime, III Murder, V Kidnapping and abduction, VII Dacoity, IX Robbery,
# XI House breaking, XIII Theft cattle, XV Thefts ordinary, XVII Riots, XIX Criminal breach of trust, XXI Cheating, XXIII
# Counterfeiting), each printing States, Union Territories (with a Grand Total) and Cities (with their own Total) on one
# page; each column here is that appendix's column 5, "Cases reported during the year". The heads printed do not cover all
# IPC crime, so they do not add up to the total: CHECK = "columns", each head checked against the printed totals. '..'
# and '-' (nil) are 0. Delhi is printed both as a Union Territory and as a city with the same figures.
KIND, YEAR, PUB = "crime", 1960, "cii"
SOURCE = "raw/cii/1960/year_wise/1689772159appendicesall1.pdf"
PAGES = "1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45"
TITLE = "Appendices I-XXIII (cases): Total cognizable crime and each head - cases reported during the year, by State / Union Territory / city, 1960"
CATS = ["Murder", "Kidnapping and abduction", "Dacoity", "Robbery", "House breaking", "Theft cattle", "Thefts ordinary", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
    ('Kanpur', 'Thefts ordinary'): (116, 1116, "printed 116; the Cities total (33,160) needs 1,116, and so does the row's own disposal: 97 pending investigation + 211 pending in court + 1,116 reported - 310 not investigated = 1,114 true cases, as printed"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [900, 145, 75, 172, 6229, 1510, 12195, 2370, 762, 388, 25, 35157],
  "Assam": [432, 389, 241, 198, 3803, 300, 4857, 2490, 374, 279, 15, 20411],
  "Bihar": [888, 473, 755, 583, 18401, 623, 18388, 4359, 1089, 426, 55, 59598],
  "Gujarat": [776, 249, 87, 602, 5555, 865, 9539, 446, 796, 493, 78, 31213],
  "Jammu & Kashmir": [68, 111, 52, 83, 862, 186, 646, 325, 68, 48, 2, 4014],
  "Kerala": [250, 47, 19, 103, 2259, 163, 3065, 1114, 358, 165, 14, 16244],
  "Madhya Pradesh": [1396, 687, 466, 882, 15675, 3407, 27999, 1649, 1408, 1112, 44, 75643],
  "Madras": [755, 536, 69, 265, 7434, 2569, 21771, 2511, 2234, 740, 51, 62706],
  "Mysore": [648, 190, 90, 140, 4555, 899, 8252, 1035, 685, 460, 27, 25364],
  "Maharashtra": [1192, 454, 387, 1271, 10862, 1403, 30646, 967, 2411, 1484, 95, 70161],
  "Orissa": [349, 115, 53, 197, 4579, 539, 8186, 1103, 680, 319, 8, 22384],
  "Punjab": [542, 336, 6, 72, 3302, 665, 4210, 206, 497, 410, 25, 18337],
  "Rajasthan": [452, 566, 64, 354, 4399, 2006, 4111, 953, 485, 352, 29, 20925],
  "Uttar Pradesh": [1656, 814, 952, 542, 14463, 3159, 21949, 2743, 2268, 1038, 23, 64131],
  "West Bengal": [463, 569, 530, 668, 9827, 672, 26641, 4123, 1343, 1042, 43, 63938],
  "TOTAL (STATES)": [10767, 5681, 3846, 6132, 112205, 18966, 202455, 26394, 15458, 8756, 534, 590226],
 },
 "U.Ts.": {
  "A & N. Islands": [1, 4, 0, 3, 32, 5, 65, 4, 5, 4, 0, 213],
  "Delhi": [57, 184, 3, 25, 1198, 53, 5471, 63, 274, 335, 15, 10072],
  "Himachal Pradesh": [16, 23, 4, 31, 226, 16, 206, 36, 43, 6, 3, 1151],
  "Manipur": [31, 92, 77, 23, 224, 69, 433, 170, 41, 71, 1, 1733],
  "Tripura": [30, 33, 38, 40, 609, 108, 898, 214, 32, 33, 1, 2699],
  "L.M. & A. Islands": [0, 0, 0, 0, 2, 0, 21, 0, 0, 1, 0, 33],
  "Nagaland": [8, 7, 13, 9, 44, 5, 71, 9, 9, 1, 0, 240],
  "TOTAL (U.TS.)": [143, 343, 135, 131, 2335, 256, 7165, 496, 404, 451, 20, 16141],
 },
 "Grand": {
  "GRAND TOTAL": [10910, 6024, 3981, 6263, 114540, 19222, 209620, 26890, 15862, 9207, 554, 606367],
 },
 "Cities": {
  "Bangalore": [8, 58, 0, 5, 585, 33, 2202, 10, 163, 264, 12, 4066],
  "Bombay": [134, 156, 19, 225, 1682, 52, 10372, 156, 1130, 780, 40, 18524],
  "Calcutta": [51, 123, 2, 21, 854, 38, 6841, 248, 392, 438, 11, 13071],
  "Delhi": [57, 184, 3, 25, 1198, 53, 5471, 63, 274, 335, 15, 10072],
  "Hyderabad": [11, 30, 0, 11, 585, 32, 1965, 44, 120, 95, 1, 3536],
  "Kanpur": [16, 51, 0, 7, 235, 13, 1116, 14, 183, 85, 3, 2567],
  "Madras": [16, 25, 0, 14, 146, 41, 3801, 23, 514, 239, 8, 6013],
  "Ahmedabad": [31, 34, 1, 31, 475, 37, 1392, 33, 160, 95, 15, 3157],
  "TOTAL (CITIES)": [324, 661, 25, 339, 5760, 299, 33160, 591, 2936, 2331, 105, 61006],
 },
}
