# ADSI 2000, Table-13: number of traffic accidents by time of occurrence, ROAD ACCIDENTS column group (cols 3-11),
# States / UTs / cities (raw/adsi/2000/table_content/table-13_2000.pdf, page 1 = printed page 105). Read from the page
# images; every row is checked against its printed Total and every column against the printed Total States,
# Total UTs, Total All-India and Total (Cities) by scripts/check_handread.py. "Total All-India" is entered as
# GRAND TOTAL. Delhi appears as "Delhi (UT)" and "Delhi (City)".
#
# CITY ROWS SHIFTED: as on the Total page, this Road page prints the city NAMES in "Calcutta" alphabetical order but
# the FIGURES in "Kolkata" order. Each row's Total was compared with the printed Total of the same edition's month
# table (raw/adsi/2000/table_content/table-12_2000.pdf, which prints the names in Kolkata order), and every figure
# row is entered here under the place whose month-table Total it matches:
#   printed row "Calcutta"   (Total 4878) -> Chennai     (month table Chennai 4878)
#   printed row "Chennai"    (Total 1275) -> Coimbatore  (month table Coimbatore 1275)
#   printed row "Coimbatore" (Total 8930) -> Delhi (City) (month table Delhi 8930)
#   printed row "Delhi"      (Total 2331) -> Hyderabad   (month table Hyderabad 2331)
#   printed row "Hyderabad"  (Total 2019) -> Indore      (month table Indore 2019)
#   printed row "Indore"     (Total 2474) -> Jaipur      (month table Jaipur 2474)
#   printed row "Jaipur"     (Total 860)  -> Kanpur      (month table Kanpur 860)
#   printed row "Kanpur"     (Total 2862) -> Kochi       (month table Kochi 2862)
#   printed row "Kochi"      (Total 2271) -> Calcutta    (month table Kolkata 2271)
# Every other city, and every State and UT, has the same Total in both tables, so those rows are as printed.
# The rows below are in printed (figure) order.
KIND, YEAR, PUB = "traffic_time", 2000, "adsi"
SOURCE = "raw/adsi/2000/table_content/table-13_2000.pdf"
PAGES = "1"
TITLE = "Table-13: Number of Traffic Accidents by Time of Occurrence during 2000 (State, UT & City-wise)"
GROUP = "Road"
CATS = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24", "Total"]
# corrections: (place, category): (printed, corrected, why)
CORRECTIONS = {
    ("TOTAL (STATES)", "Total"): (29618, 296183, "printed 29618, the sixth digit cut off by the cell border; the row adds to 296183 and Total All-India 308260 - Total UTs 12077 = 296183"),
    ("GRAND TOTAL", "Total"): (30826, 308260, "printed 30826, the sixth digit cut off by the cell border; the row adds to 308260 = Total States 296183 + Total UTs 12077"),
    ("Chennai", "row"): ("printed against Calcutta", "Chennai", "names printed in Calcutta order, figures in Kolkata order; Total 4878 = month table Chennai"),
    ("Coimbatore", "row"): ("printed against Chennai", "Coimbatore", "Total 1275 = month table Coimbatore"),
    ("Delhi (City)", "row"): ("printed against Coimbatore", "Delhi (City)", "Total 8930 = month table Delhi"),
    ("Hyderabad", "row"): ("printed against Delhi", "Hyderabad", "Total 2331 = month table Hyderabad"),
    ("Indore", "row"): ("printed against Hyderabad", "Indore", "Total 2019 = month table Indore"),
    ("Jaipur", "row"): ("printed against Indore", "Jaipur", "Total 2474 = month table Jaipur"),
    ("Kanpur", "row"): ("printed against Jaipur", "Kanpur", "Total 860 = month table Kanpur"),
    ("Kochi", "row"): ("printed against Kanpur", "Kochi", "Total 2862 = month table Kochi"),
    ("Calcutta", "row"): ("printed against Kochi", "Calcutta", "Total 2271 = month table Kolkata"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [2453, 3198, 3100, 3258, 3073, 3290, 3492, 2498, 24362],
  "Arunachal Pradesh": [12, 25, 30, 49, 41, 40, 33, 22, 252],
  "Assam": [138, 195, 265, 287, 316, 316, 254, 149, 1920],
  "Bihar": [469, 590, 606, 609, 467, 507, 408, 344, 4000],
  "Goa": [47, 37, 171, 252, 285, 294, 269, 163, 1518],
  "Gujarat": [1417, 1543, 2727, 3563, 3461, 3508, 3688, 2336, 22243],
  "Haryana": [593, 585, 970, 1054, 839, 890, 936, 796, 6663],
  "Himachal Pradesh": [80, 154, 197, 257, 260, 362, 404, 284, 1998],
  "Jammu & Kashmir": [306, 490, 538, 1025, 849, 737, 419, 162, 4526],
  "Karnataka": [2631, 2823, 3595, 4841, 4523, 4969, 4506, 3263, 31151],
  "Kerala": [1131, 1515, 4781, 6514, 5621, 7632, 5466, 2693, 35353],
  "Madhya Pradesh": [1514, 2369, 3450, 3508, 2877, 3062, 3011, 2050, 21841],
  "Maharashtra": [3524, 4040, 4681, 5330, 5197, 5192, 5384, 4925, 38273],
  "Manipur": [0, 8, 111, 192, 66, 102, 22, 5, 506],
  "Meghalaya": [6, 13, 22, 20, 25, 33, 33, 17, 169],
  "Mizoram": [4, 3, 4, 8, 17, 17, 5, 5, 63],
  "Nagaland": [4, 4, 13, 11, 20, 11, 10, 6, 79],
  "Orissa": [597, 880, 890, 1051, 816, 953, 787, 637, 6611],
  "Punjab": [140, 150, 227, 241, 203, 207, 253, 186, 1607],
  "Rajasthan": [1904, 2709, 2596, 2674, 2901, 2872, 2539, 1737, 19932],
  "Sikkim": [3, 3, 12, 9, 19, 24, 15, 9, 94],
  "Tamil Nadu": [4789, 5301, 6611, 7525, 6762, 7016, 6473, 4446, 48923],
  "Tripura": [10, 14, 94, 128, 123, 72, 45, 38, 524],
  "Uttar Pradesh": [797, 1716, 2060, 2032, 1735, 1891, 1889, 1027, 13147],
  "West Bengal": [693, 1051, 1385, 1715, 1561, 1621, 1562, 840, 10428],
  "TOTAL (STATES)": [23262, 29416, 39136, 46153, 42057, 45618, 41903, 28638, 296183],
 },
 "U.Ts.": {
  "A & N Islands": [1, 4, 24, 29, 39, 35, 21, 5, 158],
  "Chandigarh": [20, 2, 33, 68, 98, 75, 102, 57, 455],
  "D & N Haveli": [1, 1, 6, 7, 13, 15, 27, 14, 84],
  "Daman & Diu": [1, 0, 5, 10, 10, 10, 21, 9, 66],
  "Delhi (UT)": [848, 520, 886, 1284, 1263, 1627, 2047, 1785, 10260],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [30, 38, 121, 201, 152, 197, 211, 104, 1054],
  "TOTAL (U.TS.)": [901, 565, 1075, 1599, 1575, 1959, 2429, 1974, 12077],
 },
 "Cities": {
  "Ahmedabad": [11, 12, 28, 30, 23, 38, 34, 37, 213],
  "Bangalore": [525, 465, 1245, 1525, 1268, 1522, 1255, 587, 8392],
  "Bhopal": [32, 79, 426, 555, 373, 506, 279, 133, 2383],
  "Chennai": [352, 451, 701, 776, 754, 726, 627, 491, 4878],
  "Coimbatore": [40, 43, 158, 203, 219, 237, 222, 153, 1275],
  "Delhi (City)": [655, 434, 761, 1112, 1107, 1443, 1845, 1573, 8930],
  "Hyderabad": [166, 169, 318, 444, 324, 332, 299, 279, 2331],
  "Indore": [65, 124, 473, 217, 164, 253, 496, 227, 2019],
  "Jaipur": [134, 129, 247, 386, 487, 515, 319, 257, 2474],
  "Kanpur": [64, 73, 143, 115, 121, 132, 132, 80, 860],
  "Kochi": [51, 195, 411, 408, 400, 511, 508, 378, 2862],
  "Calcutta": [175, 239, 236, 397, 308, 254, 441, 221, 2271],
  "Lucknow": [99, 81, 107, 87, 79, 124, 137, 134, 848],
  "Ludhiana": [5, 2, 14, 6, 3, 6, 4, 9, 49],
  "Madurai": [18, 65, 81, 141, 218, 146, 186, 21, 876],
  "Mumbai": [341, 384, 611, 797, 791, 747, 734, 544, 4949],
  "Nagpur": [95, 63, 139, 282, 274, 267, 337, 294, 1751],
  "Patna": [9, 12, 28, 35, 20, 33, 23, 12, 172],
  "Pune": [27, 22, 31, 44, 37, 40, 53, 46, 300],
  "Surat": [62, 39, 136, 185, 212, 215, 208, 153, 1210],
  "Vadodara": [57, 254, 217, 353, 264, 272, 346, 153, 1916],
  "Varanasi": [20, 17, 22, 17, 19, 15, 21, 19, 150],
  "Vishakhapatnam": [22, 36, 93, 131, 124, 149, 157, 97, 809],
  "TOTAL (CITIES)": [3025, 3388, 6626, 8246, 7589, 8483, 8663, 5898, 51918],
 },
 "Grand": {"GRAND TOTAL": [24163, 29981, 40211, 47752, 43632, 47577, 44332, 30612, 308260]},
}
