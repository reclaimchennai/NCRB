# Crime in India 1957, Appendices I, III, V, ... XXIII (the "-CASES" appendices): cognizable crime cases reported during
# the year, by State, Union Territory and city, under each head (raw/cii/1957/year_wise/1689765744appendicesall5.pdf, the
# left-hand pages 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45). The 1957 edition prints no single State x head table:
# each head has its own appendix (I Total cognizable crime, III Murder, V Kidnapping & abduction, VII Dacoity, IX Robbery,
# XI House breaking, XIII Cattle theft, XV Ordinary thefts, XVII Riot, XIX Criminal breach of trust, XXI Cheating, XXIII
# Counterfeit coins and notes), each printing States, Union Territories (with a Grand Total) and Cities (with their own
# Total) on one page; each column here is that appendix's column 5, "Cases reported during the year". The heads printed
# do not cover all IPC crime, so they do not add up to the total: CHECK = "columns", each head checked against the printed
# totals. '..' and '-' (nil) are 0. Delhi is printed both as a Union Territory and as a city with the same figures.
# Appendix I misprints the cities Delhi and Hyderabad as "Helhi" and "Dyderabad" (named correctly in every other appendix).
KIND, YEAR, PUB = "crime", 1957, "cii"
SOURCE = "raw/cii/1957/year_wise/1689765744appendicesall5.pdf"
PAGES = "1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45"
TITLE = "Appendices I-XXIII (cases): Total cognizable crime and each head - cases reported during the year, by State / Union Territory / city, 1957"
CATS = ["Murder", "Kidnapping & abduction", "Dacoity", "Robbery", "House breaking", "Cattle theft", "Ordinary thefts", "Riot", "Criminal breach of trust", "Cheating", "Counterfeit coins and notes", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {
}
ROWS = {
 "States": {
  "Andhra Pradesh": [955, 168, 130, 231, 7158, 1797, 13769, 2034, 979, 530, 14, 38610],
  "Assam": [340, 315, 323, 205, 4634, 347, 4584, 1057, 288, 220, 63, 17223],
  "Bihar": [880, 386, 1862, 974, 23013, 629, 19173, 3922, 859, 440, 146, 62668],
  "Bombay": [2010, 792, 762, 2460, 19128, 3105, 43076, 2014, 3231, 2167, 44, 107450],
  "Jammu & Kashmir": [65, 92, 61, 83, 998, 233, 464, 243, 76, 35, 1, 3624],
  "Kerala": [259, 49, 22, 112, 1936, 203, 2598, 870, 223, 84, 7, 12103],
  "Madhya Pradesh": [1166, 563, 531, 691, 15149, 2921, 25475, 1327, 1230, 1045, 82, 63807],
  "Madras": [756, 445, 99, 281, 7114, 2784, 21178, 2047, 1959, 752, 19, 52300],
  "Mysore": [643, 201, 122, 251, 4758, 995, 8846, 709, 777, 313, 22, 24051],
  "Orissa": [239, 91, 49, 178, 4353, 574, 7814, 879, 624, 375, 58, 19476],
  "Punjab": [603, 401, 10, 132, 4153, 663, 4889, 356, 465, 439, 5, 19058],
  "Rajasthan": [414, 479, 61, 349, 4610, 1880, 3722, 999, 419, 325, 29, 18599],
  "Uttar Pradesh": [1468, 780, 907, 517, 17975, 3303, 22135, 3002, 2323, 939, 53, 64857],
  "West Bengal": [496, 713, 510, 810, 12250, 729, 28673, 3988, 1520, 1249, 72, 63609],
  "TOTAL (STATES)": [10294, 5475, 5449, 7274, 127229, 20163, 206396, 23447, 14973, 8913, 615, 567435],
 },
 "U.Ts.": {
  "Andaman & Nicobar Islands": [3, 1, 0, 0, 34, 3, 56, 2, 4, 1, 0, 170],
  "Delhi": [54, 165, 1, 57, 1372, 64, 5519, 84, 273, 383, 11, 9736],
  "Himachal Pradesh": [18, 32, 5, 36, 290, 25, 280, 29, 42, 23, 1, 1255],
  "Manipur": [19, 115, 29, 7, 122, 40, 246, 38, 33, 61, 1, 1013],
  "Tripura": [20, 19, 35, 23, 564, 45, 354, 119, 23, 5, 0, 1534],
  "Naga Hills & Tuensang Area": [11, 14, 41, 11, 21, 0, 48, 31, 14, 2, 1, 228],
  "TOTAL (U.TS.)": [125, 346, 111, 134, 2403, 177, 6503, 303, 389, 475, 14, 13936],
 },
 "Grand": {
  "GRAND TOTAL": [10419, 5821, 5560, 7408, 129632, 20340, 212899, 23750, 15362, 9388, 629, 581371],
 },
 "Cities": {
  "Bangalore": [18, 41, 1, 17, 755, 64, 2339, 22, 196, 96, 7, 4234],
  "Bombay": [125, 134, 15, 167, 1687, 41, 9000, 97, 941, 842, 5, 15892],
  "Calcutta": [49, 123, 4, 32, 1009, 80, 6662, 220, 477, 401, 13, 10725],
  "Delhi": [54, 165, 1, 57, 1372, 64, 5519, 84, 273, 383, 11, 9736],
  "Hyderabad": [10, 45, 4, 8, 1022, 42, 1839, 16, 206, 147, 1, 4025],
  "Kanpur": [16, 27, 0, 0, 155, 9, 804, 7, 179, 37, 3, 1461],
  "Madras": [12, 26, 3, 14, 341, 47, 4884, 15, 379, 235, 1, 7145],
  "TOTAL (CITIES)": [284, 561, 28, 295, 6341, 347, 31047, 461, 2651, 2141, 41, 53218],
 },
}
