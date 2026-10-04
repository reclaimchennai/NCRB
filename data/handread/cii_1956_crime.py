# Crime in India 1956, Appendices I, III, V, ... XXIII (the "-CASES" appendices): cognizable crime cases reported during
# the year, by State, Union Territory and city, under each head (raw/cii/1956/year_wise/1679311613APPENDIX-ALL0.pdf, the
# left-hand pages 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45). The 1956 edition prints no single State x head table:
# each head has its own appendix (I Total cognizable crime, III Murder, V Kidnapping & abduction, VII Dacoity, IX Robbery,
# XI House breaking, XIII Cattle theft, XV Ordinary theft, XVII Riots, XIX C. B. of trust, XXI Cheating, XXIII Counterfeit
# coins and notes), each printing States, Union Territories (with a Grand Total) and Cities (with their own Total) on one
# page; each column here is that appendix's "Cases reported during the year". The heads printed do not cover all IPC
# crime, so they do not add up to the total: CHECK = "columns", each head checked against the printed totals. '..' (nil)
# is 0. Delhi is printed both as a Union Territory and as a city with the same figures. Appendix I prints the first city
# as "Bangaolre".
KIND, YEAR, PUB = "crime", 1956, "cii"
SOURCE = "raw/cii/1956/year_wise/1679311613APPENDIX-ALL0.pdf"
PAGES = "1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45"
TITLE = "Appendices I-XXIII (cases): Total cognizable crime and each head - cases reported during the year, by State / Union Territory / city, 1956"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House breaking", "Cattle theft", "Ordinary theft", "Riots", "Criminal breach of trust", "Cheating", "Counterfeit coins and notes", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [770, 169, 151, 269, 7811, 1691, 13574, 1798, 1134, 511, 29, 37429],
  "Assam": [309, 308, 291, 193, 5179, 370, 4747, 1092, 307, 164, 35, 17665],
  "Bihar": [830, 439, 1251, 792, 20122, 533, 17644, 3768, 812, 498, 164, 56802],
  "Bombay": [2016, 770, 1061, 2569, 21776, 3022, 46428, 3407, 3619, 2216, 58, 116377],
  "Jammu & Kashmir": [48, 107, 53, 70, 944, 189, 510, 257, 122, 28, 0, 3567],
  "Kerala": [168, 41, 17, 70, 1243, 155, 2386, 474, 199, 96, 11, 8718],
  "Madhya Pradesh": [1130, 627, 621, 686, 16958, 3127, 25901, 1385, 1248, 998, 50, 66841],
  "Madras": [797, 469, 94, 397, 7662, 2836, 22716, 2092, 1990, 826, 23, 55011],
  "Mysore": [569, 175, 92, 291, 4505, 843, 8662, 726, 632, 243, 20, 22493],
  "Orissa": [268, 111, 58, 207, 4672, 522, 8439, 896, 424, 344, 10, 19789],
  "Punjab": [589, 418, 16, 176, 4517, 691, 4922, 269, 452, 597, 27, 19578],
  "Rajasthan": [381, 591, 91, 420, 4975, 1768, 3864, 1078, 341, 510, 9, 19032],
  "Uttar Pradesh": [1599, 793, 932, 562, 19060, 3506, 23057, 3087, 2574, 1020, 62, 67693],
  "West Bengal": [458, 663, 622, 822, 13255, 553, 28247, 4149, 1286, 1088, 83, 63200],
  "TOTAL (STATES)": [9932, 5681, 5350, 7524, 132679, 19806, 211097, 24478, 15140, 9139, 581, 574195],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [5, 2, 0, 0, 22, 0, 57, 0, 6, 1, 0, 139],
  "Delhi": [56, 107, 3, 39, 1193, 44, 4433, 79, 193, 298, 10, 7796],
  "Himachal Pradesh": [11, 43, 5, 28, 262, 18, 233, 30, 67, 31, 2, 1236],
  "Manipur": [11, 53, 5, 7, 123, 37, 218, 28, 42, 43, 2, 815],
  "Tripura": [10, 19, 34, 20, 277, 19, 252, 85, 18, 7, 1, 1036],
  "TOTAL (U.TS.)": [93, 224, 47, 94, 1877, 118, 5193, 222, 326, 380, 15, 11022],
 },
 "Grand": {
  "GRAND TOTAL": [10025, 5905, 5397, 7618, 134556, 19924, 216290, 24700, 15466, 9519, 596, 585217],
 },
 "Cities": {
  "Bangalore": [16, 36, 0, 16, 644, 57, 2300, 22, 186, 67, 5, 3903],
  "Bombay": [131, 131, 295, 279, 2162, 0, 9117, 319, 1015, 849, 6, 17277],
  "Calcutta": [49, 107, 8, 32, 1020, 75, 6929, 260, 408, 275, 19, 10977],
  "Kanpur": [4, 26, 0, 2, 219, 5, 973, 12, 245, 64, 4, 1819],
  "Madras": [16, 29, 1, 35, 620, 41, 5663, 28, 382, 278, 4, 8516],
  "Delhi": [56, 107, 3, 39, 1193, 44, 4433, 79, 193, 298, 10, 7796],
  "Hyderabad": [15, 23, 1, 17, 939, 22, 1482, 18, 201, 150, 1, 3353],
  "TOTAL (CITIES)": [287, 459, 308, 420, 6797, 244, 30897, 738, 2630, 1981, 49, 53641],
 },
}
