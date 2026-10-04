# ADSI 1993, Appendix V: suicides by means adopted and sex, States / UTs / cities
# (raw/adsi/1993/archived/appendix-5_1993.pdf, pages 1-10; printed pages N.C.R.B.-114 to 123). Pages 1-4 carry three
# categories each by Male / Female / Total for every State and UT, page 5 the Grand Total (State & UT-wise); pages 6-9
# repeat the twelve categories for the 23 cities and page 10 their Grand Total. No %share is printed in this appendix.
# Only the Total column of each category is recorded. Read from the page images: Male, Female and Total were all
# transcribed, and every printed Male + Female equals its Total; the Male, Female and Total columns each add up to the
# printed Total (States) and Total (UTs), States + UTs = Total (All-India), and every row's categories add up to its
# Grand Total in Male, Female and Total alike, for the cities too. The cities carry no totals row. Every place's Grand
# Total equals the number of suicides in Table 7 (adsi_1993_suicide_incidence.py). The All-India Drowning Total is
# read 8466 (4416 + 4050; the shading makes its last digit look like an 8). Nothing is N.A.; no figure is changed.
# Appendix VII (percentage distribution by means) agrees where spot-checked. Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "means", 1993, "adsi"
SOURCE = "raw/adsi/1993/archived/appendix-5_1993.pdf"
PAGES = "1-10"
TITLE = "Appendix V: Distribution of Suicide by Means Adopted and Sex during 1993 (State & UT-wise / City-wise)"
CATS = ["By Railways", "By Machine", "By Firearm", "By Weapon", "By Poison", "By Fire", "By Drowning", "By Hanging",
        "By Jumping", "By Taking Sleeping Pills", "By Touching Electric Wire", "By Other Causes", "Total"]
CORRECTIONS = {}
ROWS = {
 "States": {
  "Andhra Pradesh": [322, 2, 52, 1, 3134, 753, 946, 1344, 53, 27, 54, 1162, 7850],
  "Arunachal Pradesh": [0, 0, 1, 0, 5, 3, 7, 39, 0, 0, 1, 0, 56],
  "Assam": [51, 3, 26, 6, 263, 82, 202, 1162, 8, 7, 24, 723, 2557],
  "Bihar": [255, 19, 24, 10, 310, 210, 190, 342, 27, 34, 26, 196, 1643],
  "Goa": [1, 0, 2, 6, 23, 36, 43, 79, 2, 1, 0, 10, 203],
  "Gujarat": [148, 20, 8, 2, 1276, 799, 376, 463, 71, 18, 15, 235, 3431],
  "Haryana": [25, 3, 3, 4, 522, 154, 72, 202, 16, 16, 22, 215, 1254],
  "Himachal Pradesh": [0, 0, 3, 0, 88, 19, 16, 26, 16, 0, 0, 2, 170],
  "Jammu & Kashmir": [0, 0, 0, 1, 26, 8, 3, 12, 1, 0, 0, 19, 70],
  "Karnataka": [93, 0, 13, 7, 3239, 617, 1195, 1779, 18, 44, 53, 997, 8055],
  "Kerala": [336, 0, 2, 4, 3379, 264, 728, 3256, 11, 8, 9, 127, 8124],
  "Madhya Pradesh": [373, 22, 77, 100, 1787, 884, 511, 1724, 254, 28, 64, 427, 6251],
  "Maharashtra": [231, 2, 24, 26, 3377, 1956, 1548, 1737, 140, 14, 23, 1260, 10338],
  "Manipur": [0, 0, 1, 0, 3, 0, 2, 9, 0, 0, 0, 4, 19],
  "Meghalaya": [0, 0, 1, 0, 3, 0, 8, 37, 0, 0, 2, 20, 71],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 25],
  "Nagaland": [0, 0, 1, 1, 1, 0, 2, 15, 0, 0, 0, 0, 20],
  "Orissa": [161, 1, 2, 2, 1209, 79, 181, 1004, 9, 11, 46, 640, 3345],
  "Punjab": [146, 0, 8, 1, 92, 35, 15, 76, 1, 4, 0, 115, 493],
  "Rajasthan": [239, 23, 6, 4, 591, 244, 463, 439, 53, 39, 70, 558, 2729],
  "Sikkim": [0, 0, 0, 0, 2, 0, 3, 40, 1, 0, 0, 2, 48],
  "Tamil Nadu": [131, 1, 16, 10, 3293, 909, 734, 1155, 21, 87, 47, 1491, 7895],
  "Tripura": [0, 0, 0, 0, 210, 2, 0, 208, 0, 0, 0, 123, 543],
  "Uttar Pradesh": [618, 51, 411, 277, 848, 721, 451, 847, 96, 30, 99, 1498, 5947],
  "West Bengal": [215, 15, 20, 72, 4679, 1208, 717, 3938, 78, 171, 95, 173, 11381],
  "TOTAL (STATES)": [3345, 162, 701, 534, 28360, 8983, 8413, 19958, 876, 539, 650, 9997, 82518],
 },
 "U.Ts.": {
  "A & N Islands": [0, 0, 0, 0, 17, 6, 3, 84, 0, 0, 0, 0, 110],
  "Chandigarh": [0, 0, 0, 0, 18, 17, 7, 12, 0, 0, 0, 4, 58],
  "D & N Haveli": [0, 0, 0, 0, 5, 2, 1, 30, 1, 0, 0, 0, 39],
  "Daman & Diu": [0, 0, 0, 0, 5, 3, 3, 5, 0, 0, 0, 4, 20],
  "Delhi": [2, 0, 11, 3, 139, 295, 28, 196, 34, 1, 23, 151, 883],
  "Lakshadweep": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "Pondicherry": [2, 0, 0, 0, 198, 67, 11, 338, 0, 0, 0, 0, 616],
  "TOTAL (U.TS.)": [4, 0, 11, 3, 382, 390, 53, 665, 35, 1, 23, 159, 1726],
 },
 "Cities": {
  "Ahmedabad": [1, 0, 1, 0, 67, 102, 74, 87, 5, 2, 0, 24, 363],
  "Bangalore": [0, 0, 1, 4, 217, 187, 73, 223, 2, 25, 7, 59, 798],
  "Bhopal": [21, 0, 2, 0, 45, 44, 39, 15, 0, 0, 0, 0, 166],
  "Bombay": [0, 0, 13, 11, 236, 483, 40, 243, 60, 12, 4, 3, 1105],
  "Calcutta": [0, 7, 0, 0, 25, 36, 26, 20, 14, 30, 13, 68, 239],
  "Coimbatore": [0, 0, 0, 0, 149, 8, 14, 32, 0, 0, 0, 0, 203],
  "Delhi": [2, 0, 10, 3, 99, 246, 22, 139, 34, 0, 22, 146, 723],
  "Hyderabad": [0, 0, 0, 0, 93, 155, 115, 48, 4, 0, 2, 123, 540],
  "Indore": [12, 0, 1, 1, 112, 82, 16, 35, 2, 0, 0, 0, 261],
  "Jaipur": [16, 0, 0, 1, 81, 23, 1, 28, 6, 4, 4, 40, 204],
  "Kanpur": [39, 2, 12, 19, 89, 127, 28, 59, 21, 0, 0, 225, 621],
  "Kochi": [9, 0, 0, 0, 50, 24, 11, 121, 2, 0, 0, 1, 218],
  "Lucknow": [10, 10, 4, 8, 19, 8, 17, 28, 18, 9, 3, 26, 160],
  "Ludhiana": [0, 0, 0, 0, 8, 1, 0, 6, 0, 0, 0, 0, 15],
  "Madras": [0, 1, 0, 2, 234, 225, 70, 357, 7, 10, 8, 242, 1156],
  "Madurai": [0, 0, 0, 0, 117, 34, 5, 14, 0, 8, 0, 112, 290],
  "Nagpur": [3, 1, 0, 0, 22, 20, 44, 34, 2, 1, 1, 149, 277],
  "Patna": [0, 0, 0, 0, 13, 0, 5, 3, 4, 0, 0, 5, 30],
  "Pune": [3, 0, 1, 0, 74, 89, 37, 119, 11, 0, 0, 18, 352],
  "Surat": [0, 0, 2, 1, 27, 28, 10, 15, 2, 0, 9, 17, 111],
  "Vadodara": [1, 0, 0, 0, 37, 37, 13, 25, 2, 2, 0, 7, 124],
  "Varanasi": [37, 2, 1, 0, 44, 36, 20, 45, 1, 0, 3, 53, 242],
  "Vishakhapatnam": [1, 0, 0, 0, 67, 23, 29, 47, 1, 4, 0, 3, 175],
 },
 "Grand": {
  "GRAND TOTAL": [3349, 162, 712, 537, 28742, 9373, 8466, 20623, 911, 540, 673, 10156, 84244],
 },
}
