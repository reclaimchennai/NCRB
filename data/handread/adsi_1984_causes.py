# ADSI 1984, Appendix V: statewise distribution of suicidal deaths under different causes with percentage to total
# deaths, pages 1-9 (printed sideways; pages 1-3 columns 3-8, pages 4-6 columns 9-14, pages 7-9 columns 15-19). Read
# from the page images; "—" (nil) is 0; the bracketed percentages are not recorded. "NA" (not available, printed
# "NA(0·0)") is None: Andhra Pradesh, Bihar and Madhya Pradesh print NA for dowry disputes, illegitimate pregnancy
# and causes not known, Haryana for causes not known, Hyderabad for all three and Delhi (city) for illegitimate
# pregnancy; their rows add up to their printed Totals without them. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1984, "adsi"
SOURCE = "raw/adsi/1984/table_content/1680162435appendix-51984.pdf"
PAGES = "1-9"
TITLE = ("Appendix V: Statewise Distribution of Suicidal Deaths under Different Causes with Percentage to Total Deaths "
         "During the Year 1984")
CATS = ["Failure in examination", "Quarrel with parents-in-law", "Quarrel with spouse", "Poverty", "Love affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of dear person", "Fall in social reputation",
        "Dowry disputes", "Illegitimate pregnancy", "Causes not known", "Other causes", "Total"]
N = None
CORRECTIONS = {
    ("Meghalaya", "Quarrel with parents-in-law"): (1, 0, "printed '1(0·0)'; the percentage is 0.0 (1 would be 2.9% of 35, as printed for the row's other 1s), the row then adds up to the printed 35 and the States' column to the printed 4,460"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [41, 186, 163, 114, 95, 43, 100, 1089, 21, 15, 23, 24, N, N, N, 1744, 3658],
  "Assam": [46, 33, 43, 55, 129, 62, 39, 162, 9, 49, 19, 9, 0, 3, 723, 205, 1586],
  "Bihar": [22, 27, 39, 20, 35, 30, 52, 85, 15, 7, 2, 0, N, N, N, 281, 615],
  "Gujarat": [25, 164, 340, 69, 106, 195, 11, 248, 64, 51, 35, 56, 2, 7, 153, 367, 1893],
  "Haryana": [19, 37, 69, 29, 21, 28, 36, 106, 13, 1, 15, 11, 26, 4, N, 115, 530],
  "Himachal Pradesh": [2, 0, 1, 1, 4, 5, 1, 18, 0, 4, 1, 7, 0, 1, 0, 32, 77],
  "Jammu & Kashmir": [1, 4, 1, 3, 4, 2, 2, 1, 5, 0, 0, 0, 0, 0, 0, 11, 34],
  "Karnataka": [107, 226, 201, 253, 236, 224, 149, 1071, 112, 66, 40, 26, 60, 18, 716, 1357, 4862],
  "Kerala": [61, 247, 180, 33, 196, 178, 98, 626, 37, 262, 27, 119, 1, 8, 158, 3386, 5617],
  "Madhya Pradesh": [65, 480, 210, 33, 99, 105, 76, 620, 34, 20, 16, 22, N, N, N, 1307, 3087],
  "Maharashtra": [62, 317, 343, 83, 134, 163, 92, 655, 64, 39, 16, 13, 26, 5, 211, 1898, 4121],
  "Manipur": [2, 1, 1, 2, 5, 3, 5, 1, 0, 4, 0, 0, 0, 0, 15, 25, 64],
  "Meghalaya": [0, 0, 4, 0, 1, 0, 0, 9, 0, 1, 1, 1, 0, 0, 17, 1, 35],
  "Nagaland": [0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 31, 36],
  "Orissa": [37, 427, 200, 26, 144, 42, 20, 300, 11, 17, 17, 5, 10, 5, 134, 358, 1753],
  "Punjab": [8, 29, 15, 18, 8, 7, 10, 17, 3, 9, 6, 1, 21, 0, 52, 49, 253],
  "Rajasthan": [30, 114, 83, 35, 24, 77, 28, 109, 8, 30, 16, 23, 7, 7, 51, 243, 885],
  "Sikkim": [2, 0, 1, 2, 0, 1, 0, 3, 0, 0, 0, 1, 0, 1, 4, 3, 18],
  "Tamil Nadu": [79, 533, 383, 166, 288, 115, 136, 1670, 98, 35, 51, 22, 11, 7, 685, 3192, 7471],
  "Tripura": [0, 33, 14, 11, 117, 26, 7, 69, 5, 0, 0, 13, 0, 0, 0, 144, 439],
  "Uttar Pradesh": [46, 239, 129, 66, 89, 194, 140, 329, 34, 27, 6, 21, 37, 8, 221, 1035, 2621],
  "West Bengal": [505, 1361, 1450, 123, 1017, 393, 215, 772, 95, 9, 131, 63, 14, 2, 5, 3757, 9912],
  "TOTAL (STATES)": [1160, 4460, 3870, 1142, 2753, 1893, 1217, 7962, 628, 646, 422, 437, 215, 76, 3145, 19541, 49567],
 },
 "U.Ts.": {
  "A & N Islands": [0, 23, 22, 9, 3, 0, 2, 5, 0, 2, 0, 0, 0, 0, 0, 14, 80],
  "Arunachal Pradesh": [0, 1, 0, 0, 4, 1, 0, 2, 0, 0, 0, 3, 0, 0, 12, 2, 25],
  "Chandigarh": [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 14, 0, 17],
  "D & N Haveli": [0, 2, 3, 1, 0, 12, 0, 3, 0, 0, 0, 0, 0, 0, 0, 7, 28],
  "Delhi": [9, 58, 8, 3, 27, 9, 3, 66, 9, 0, 8, 3, 10, 0, 156, 64, 433],
  "Goa, Daman & Diu": [1, 4, 6, 4, 10, 12, 0, 12, 1, 1, 1, 0, 1, 0, 14, 54, 121],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
  "Mizoram": [0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0, 12],
  "Pondicherry": [3, 65, 64, 5, 9, 0, 0, 135, 5, 0, 1, 0, 0, 0, 0, 0, 287],
  "TOTAL (U.TS.)": [13, 153, 103, 22, 54, 36, 5, 226, 15, 3, 10, 10, 11, 0, 201, 142, 1004],
 },
 "Cities": {
  "Ahmedabad": [1, 3, 35, 2, 8, 10, 1, 18, 5, 8, 4, 2, 0, 0, 0, 114, 211],
  "Bangalore": [6, 1, 2, 25, 17, 16, 0, 73, 16, 0, 0, 1, 11, 0, 197, 389, 754],
  "Bombay": [9, 18, 27, 16, 36, 25, 2, 32, 18, 9, 2, 0, 5, 1, 111, 92, 403],
  "Calcutta": [2, 1, 3, 9, 4, 5, 1, 5, 1, 1, 0, 0, 0, 0, 4, 2, 38],
  "Delhi": [9, 57, 7, 1, 25, 9, 3, 48, 9, 0, 6, 3, 10, N, 141, 56, 384],
  "Hyderabad": [5, 4, 12, 7, 6, 3, 3, 27, 2, 3, 1, 1, N, N, N, 189, 263],
  "Jaipur": [14, 5, 2, 2, 5, 8, 0, 6, 1, 2, 0, 0, 0, 0, 1, 0, 46],
  "Kanpur": [3, 8, 0, 2, 5, 0, 10, 0, 0, 0, 0, 1, 0, 0, 0, 21, 50],
  "Lucknow": [3, 6, 15, 7, 3, 6, 3, 23, 0, 0, 0, 0, 0, 0, 36, 102, 204],
  "Madras": [11, 9, 19, 19, 18, 3, 0, 98, 9, 8, 5, 4, 0, 0, 51, 412, 666],
  "Nagpur": [10, 8, 5, 0, 8, 0, 0, 7, 0, 0, 0, 0, 0, 0, 6, 195, 239],
  "Pune": [2, 15, 7, 2, 6, 5, 1, 5, 5, 1, 2, 1, 0, 0, 0, 100, 152],
  "TOTAL (CITIES)": [75, 135, 134, 92, 141, 90, 24, 342, 66, 32, 20, 13, 26, 1, 547, 1672, 3410],
 },
 "Grand": {"GRAND TOTAL": [1173, 4613, 3973, 1164, 2807, 1929, 1222, 8188, 643, 649, 432, 447, 226, 76, 3346, 19683, 50571]},
}
