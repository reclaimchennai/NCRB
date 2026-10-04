# CII 1973, Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads
# of the Indian Penal Code during 1973, States / UTs / cities (raw/cii/1973/table_content/table-5-1973.pdf, pages 1-4).
# Read from the page images; only the incidence (I) columns are kept, the volume per lakh (V) columns skipped. '—' is
# entered as 0. The scan is faint and carries hand corrections; every figure was compared with Table 6 of the same
# volume (incidence during 1972 and 1973, raw/cii/1973/table_chapter/survey-of-crime.pdf pages 20-23), which prints the
# same 1973 figures more clearly: blurred digits were read with it and the printed V column (Robbery: Karnataka 224,
# Maharashtra 2,598, Tripura 44, Goa, Daman & Diu 20; West Bengal Murder 889 and Kanpur Kidnapping 165 are written in by
# hand on the page and agree with Table 6). The table prints selected heads and the total cognizable crime, with no
# 'other IPC crimes' column, so each column is checked against the printed totals (CHECK = "columns").
KIND, YEAR, PUB = "crime", 1973, "cii"
SOURCE = "raw/cii/1973/table_content/table-5-1973.pdf"
PAGES = "1-4"
TITLE = ("Table 5: Incidence of cognizable crime and volume of crime per one lakh of population under important heads "
         "of Indian Penal Code during 1973")
CATS = ["Murder", "C.H. not amounting to murder", "Rape", "Kidnapping & abduction", "Dacoity", "Robbery", "Burglary",
        "Thefts", "Riots", "Criminal breach of trust", "Cheating", "Counterfeiting", "Total cognizable crimes (IPC)"]
CHECK = "columns"
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [1247, 15, 56, 159, 191, 221, 6383, 12437, 3144, 598, 570, 65, 51268],
  "Assam": [466, 32, 122, 472, 253, 351, 5723, 8432, 3819, 459, 377, 6, 32007],
  "Bihar": [1716, 280, 265, 713, 1973, 1420, 18410, 29499, 12498, 1315, 775, 66, 92068],
  "Gujarat": [765, 4, 57, 317, 130, 530, 5185, 15424, 915, 1111, 743, 6, 45421],
  "Haryana": [216, 97, 64, 129, 6, 30, 1618, 2664, 105, 273, 160, 3, 9388],
  "Himachal Pradesh": [66, 12, 16, 66, 1, 29, 458, 615, 144, 97, 67, 0, 3342],
  "Jammu & Kashmir": [90, 3, 24, 226, 14, 10, 925, 1117, 671, 93, 63, 0, 6622],
  "Karnataka": [712, 5, 35, 133, 260, 224, 8287, 13554, 2877, 677, 783, 34, 44401],
  "Kerala": [523, 10, 44, 80, 49, 186, 4574, 5270, 5695, 499, 275, 47, 41848],
  "Madhya Pradesh": [1737, 27, 493, 700, 372, 1333, 22526, 40499, 3259, 1138, 1265, 20, 110811],
  "Maharashtra": [1455, 26, 253, 595, 723, 2598, 21707, 59965, 2552, 3857, 2034, 77, 128992],
  "Manipur": [44, 5, 11, 169, 12, 21, 274, 530, 169, 55, 89, 1, 2201],
  "Meghalaya": [48, 1, 12, 26, 9, 23, 155, 412, 86, 37, 20, 0, 1322],
  "Nagaland": [46, 6, 10, 32, 36, 61, 166, 441, 37, 42, 41, 0, 918],
  "Orissa": [406, 54, 35, 105, 152, 357, 6140, 12512, 1807, 544, 563, 4, 31252],
  "Punjab": [714, 183, 107, 311, 8, 55, 1561, 2639, 50, 385, 298, 7, 12511],
  "Rajasthan": [699, 44, 144, 1175, 149, 1146, 7503, 10728, 5807, 691, 776, 8, 44229],
  "Tamil Nadu": [970, 9, 65, 256, 24, 100, 7255, 23329, 5473, 1003, 929, 58, 72443],
  "Tripura": [13, 5, 7, 17, 48, 44, 622, 1088, 239, 15, 175, 1, 3009],
  "Uttar Pradesh": [4063, 1094, 741, 3161, 4932, 8567, 48695, 84356, 13635, 6717, 2455, 79, 220567],
  "West Bengal": [889, 356, 300, 772, 1255, 1103, 9189, 32209, 9743, 1550, 1180, 15, 82312],
  "TOTAL (STATES)": [16885, 2268, 2861, 9614, 10597, 18409, 177356, 357720, 72725, 21156, 13638, 497, 1036932],
 },
 "U.Ts.": {
  "A. & N. Islands": [4, 0, 0, 6, 0, 3, 71, 126, 15, 12, 4, 0, 484],
  "Chandigarh": [2, 1, 5, 12, 0, 1, 112, 752, 10, 29, 30, 0, 1334],
  "D. & N. Haveli": [1, 0, 1, 0, 0, 1, 15, 26, 3, 6, 3, 0, 84],
  "Delhi": [152, 139, 46, 570, 27, 417, 3319, 19748, 454, 555, 673, 81, 34174],
  "Goa, Daman & Diu": [21, 0, 2, 10, 2, 20, 386, 424, 37, 37, 29, 1, 1595],
  "Lakshadweep": [1, 0, 0, 0, 0, 0, 1, 4, 2, 1, 0, 0, 9],
  "Pondicherry": [6, 0, 4, 11, 1, 6, 173, 612, 142, 41, 15, 3, 2569],
  "TOTAL (U.TS.)": [187, 140, 58, 609, 30, 448, 4077, 21692, 663, 681, 754, 85, 40249],
 },
 "Grand": {
  "GRAND TOTAL": [17072, 2408, 2919, 10223, 10627, 18857, 181433, 379412, 73388, 21837, 14392, 582, 1077181],
 },
 "Cities": {
  "Ahmedabad": [39, 0, 5, 72, 15, 13, 418, 1857, 164, 97, 178, 4, 4730],
  "Bangalore": [25, 0, 3, 18, 0, 17, 1612, 4792, 126, 128, 333, 10, 9356],
  "Bombay": [167, 2, 33, 215, 89, 405, 2626, 16806, 416, 1195, 768, 57, 31920],
  "Calcutta": [63, 1, 13, 152, 9, 68, 727, 5462, 746, 489, 395, 5, 11555],
  "Delhi": [136, 127, 41, 553, 26, 385, 3060, 19169, 419, 535, 660, 81, 32722],
  "Hyderabad": [29, 2, 6, 34, 3, 26, 877, 2709, 49, 108, 180, 8, 4855],
  "Kanpur": [69, 26, 18, 165, 42, 267, 1635, 5139, 310, 739, 365, 4, 10003],
  "Madras": [27, 0, 6, 6, 2, 16, 614, 6026, 223, 328, 497, 7, 14204],
  "TOTAL (CITIES)": [555, 158, 125, 1215, 186, 1197, 11569, 61960, 2453, 3619, 3376, 176, 119345],
 },
}
