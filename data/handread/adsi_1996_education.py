# ADSI 1996, Appendix VII: educational status of suicide victims, States / UTs / cities
# (raw/adsi/1996/archived/appendix-7_1996.pdf, pages 1-6, printed pages 161-166: pages 1-2 Male, 3-4 Female, 5-6 Total
# (Male + Female); each level printed as a number and "% to Total" of the row's Total (M+F), col. 53). Only the Total
# (Male + Female) figures of pages 5-6 are recorded. Read from the page images (scanned at 150 dpi, rendered at zoom 3-5):
# every Male, Female and Total cell was transcribed and checked: Male + Female = Total in every cell; each row's eight
# levels add to its Total for Male, Female and Total alike; every column of the States adds to Total States and of the
# UTs to Total UTs; Total States + Total UTs = Total All-India (entered as GRAND TOTAL, 88,241). Rows: States 1-25,
# Total States, UTs 26-32, Total UTs, Total All-India, Cities 33-55; the cities have no printed totals row. Every row's
# Total equals that place's Total in Appendix V (causes) of 1996. All of this held as printed except one cell, Total
# All-India Matric/Secondary on page 5 (see CORRECTIONS). Pages 3 and 6 are printed heavier and blurrier than the
# rest but every figure there checks. Lakshadweep is printed with 0 in every column.
# Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "education", 1996, "adsi"
SOURCE = "raw/adsi/1996/archived/appendix-7_1996.pdf"
PAGES = "1-6"
TITLE = "Appendix VII: Educational Status of Suicide Victims during 1996 (State, UT & City-wise)"
NA = None
CATS = ["No Education", "Primary", "Middle", "Matric/Secondary", "Hr.Sec./Inter/Pre-Uni.", "Diploma", "Graduate",
        "Post Graduate & above", "Total"]
CORRECTIONS = {
    ("GRAND TOTAL", "Matric/Secondary"): (12894, 12694, "printed 12,894 (14.39%) on page 5; 12694/88241 = 14.39% (12894 would be 14.61%), Male 8,151 + Female 4,543 = 12,694, Total States 12,194 + Total UTs 500 = 12,694, and the Total All-India row then adds up to 88,241"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [3309, 1706, 1389, 752, 294, 25, 61, 7, 7543],
  "Arunachal Pradesh": [7, 10, 13, 19, 1, 0, 0, 1, 51],
  "Assam": [824, 592, 588, 310, 122, 26, 26, 4, 2492],
  "Bihar": [334, 172, 149, 180, 45, 3, 20, 4, 907],
  "Goa": [140, 158, 130, 115, 4, 0, 2, 0, 549],
  "Gujarat": [961, 1563, 818, 621, 163, 15, 38, 3, 4182],
  "Haryana": [473, 149, 183, 235, 44, 18, 28, 24, 1154],
  "Himachal Pradesh": [52, 33, 39, 64, 19, 2, 2, 0, 211],
  "Jammu & Kashmir": [16, 3, 1, 11, 3, 0, 4, 2, 40],
  "Karnataka": [3173, 2370, 1566, 903, 496, 105, 158, 49, 8820],
  "Kerala": [1132, 2335, 2304, 1631, 522, 53, 79, 30, 8086],
  "Madhya Pradesh": [2181, 1773, 1296, 983, 401, 33, 83, 20, 6770],
  "Maharashtra": [2949, 3209, 2068, 2136, 731, 51, 53, 19, 11216],
  "Manipur": [0, 2, 9, 6, 1, 0, 0, 0, 18],
  "Meghalaya": [35, 11, 20, 6, 0, 0, 0, 0, 72],
  "Mizoram": [1, 12, 20, 1, 0, 0, 0, 0, 34],
  "Nagaland": [19, 9, 3, 2, 0, 0, 1, 0, 34],
  "Orissa": [764, 689, 737, 485, 172, 14, 84, 17, 2962],
  "Punjab": [134, 118, 82, 110, 26, 29, 24, 67, 590],
  "Rajasthan": [1012, 598, 456, 373, 140, 11, 22, 7, 2619],
  "Sikkim": [35, 23, 10, 6, 0, 0, 0, 0, 74],
  "Tamil Nadu": [2741, 2179, 1956, 961, 756, 173, 170, 67, 9003],
  "Tripura": [77, 131, 120, 145, 72, 3, 7, 0, 555],
  "Uttar Pradesh": [1711, 796, 663, 624, 476, 35, 82, 84, 4471],
  "West Bengal": [2721, 4799, 3257, 1515, 898, 285, 479, 128, 14082],
  "TOTAL (STATES)": [24801, 23440, 17877, 12194, 5386, 881, 1423, 533, 86535],
 },
 "U.Ts.": {
  "A & N Islands": [39, 36, 31, 24, 13, 0, 6, 0, 149],
  "Chandigarh": [8, 6, 7, 7, 0, 0, 0, 0, 28],
  "D & N Haveli": [22, 3, 8, 4, 1, 0, 1, 0, 39],
  "Daman & Diu": [2, 4, 5, 2, 0, 0, 0, 0, 13],
  "Delhi (UT)": [168, 181, 258, 253, 77, 7, 11, 3, 958],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [49, 28, 168, 210, 63, 0, 0, 1, 519],
  "TOTAL (U.TS.)": [288, 258, 477, 500, 154, 7, 18, 4, 1706],
 },
 "Cities": {
  "Ahmedabad": [59, 142, 95, 105, 26, 0, 10, 0, 437],
  "Bangalore": [161, 144, 121, 187, 120, 29, 55, 23, 840],
  "Bhopal": [24, 26, 25, 54, 70, 1, 11, 2, 213],
  "Bombay": [117, 318, 306, 269, 70, 5, 1, 0, 1086],
  "Calcutta": [27, 37, 55, 28, 18, 2, 11, 0, 178],
  "Coimbatore": [39, 76, 69, 22, 23, 5, 13, 3, 250],
  "Delhi (City)": [126, 153, 216, 214, 70, 7, 10, 3, 799],
  "Hyderabad": [150, 63, 66, 87, 36, 1, 12, 5, 420],
  "Indore": [55, 34, 42, 55, 34, 4, 11, 2, 237],
  "Jaipur": [90, 38, 23, 11, 0, 0, 3, 2, 167],
  "Kanpur": [141, 106, 100, 77, 54, 4, 6, 0, 488],
  "Kochi": [6, 49, 62, 51, 8, 0, 9, 1, 186],
  "Lucknow": [12, 4, 6, 16, 22, 2, 17, 2, 81],
  "Ludhiana": [2, 1, 3, 2, 0, 0, 0, 0, 8],
  "Madras": [255, 132, 359, 85, 58, 5, 12, 6, 912],
  "Madurai": [65, 129, 30, 5, 13, 0, 1, 1, 244],
  "Nagpur": [56, 60, 121, 79, 22, 1, 5, 0, 344],
  "Patna": [15, 25, 15, 16, 2, 0, 2, 0, 75],
  "Pune": [85, 98, 106, 87, 27, 1, 3, 0, 407],
  "Surat": [26, 144, 50, 32, 8, 0, 0, 0, 260],
  "Vadodara": [21, 70, 27, 19, 0, 1, 2, 3, 143],
  "Varanasi": [32, 22, 11, 11, 3, 0, 0, 0, 79],
  "Vishakhapatnam": [31, 18, 22, 15, 17, 2, 8, 0, 113],
 },
 "Grand": {
  "GRAND TOTAL": [25089, 23698, 18354, 12694, 5540, 888, 1441, 537, 88241],
 },
}
