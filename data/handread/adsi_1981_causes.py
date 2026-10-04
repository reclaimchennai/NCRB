# ADSI 1981, Appendix V: distribution of suicidal deaths due to different causes with percentage to total suicidal
# deaths in the States / U.Ts. / cities, pages 1-8 (printed sideways; pages 1-4 columns 3-9: States 1-10, States
# 11-22, U.Ts., cities; pages 5-8 columns 10-16 in the same order). Read from the page images; "—" (nil) is 0; the
# bracketed percentages are not recorded. Lucknow is printed "Not Available" across the row (None). The cities' list
# grows to 12 this year (Jaipur, Lucknow, Nagpur and Pune added). Checked by scripts/check_handread.py.
KIND, YEAR, PUB = "causes", 1981, "adsi"
SOURCE = "raw/adsi/1981/table_content/1680161161appendix-51881.pdf"
PAGES = "1-8"
TITLE = ("Appendix V: Distribution of Suicidal Deaths due to Different Causes with Percentage to Total Suicidal Deaths "
         "in the States/U.Ts./Cities during the Year 1981")
CATS = ["Failure in examination", "Quarrel with Parents-in-laws", "Quarrel with Spouse", "Poverty", "Love Affairs",
        "Insanity", "Dispute over property", "Dreadful diseases", "Unemployment",
        "Bankruptcy or sudden change in economic position", "Death of Dear persons", "Fall in Social reputation",
        "Other causes", "Total"]
# Pune, Other causes is printed "4?(38.8)" with the second digit lost; 43 is the figure that makes the row add up to
# its printed Total 111 (43/111 = 38.7%) and the cities' column to the printed 1,618, so it is read as 43.
CORRECTIONS = {
    ("Madhya Pradesh", "Dispute over property"): ("10 4", 109, "printed '10  4' with the bracket and decimal of the percentage lost (a third digit dropped); 109 is what makes the row add up to its printed Total 2,544 and the States' column to the printed 1,280 (Grand Total 1,290 = 1,280 + 10 for the U.Ts.), and 109/2544 = 4.3%, the '4' left of the percentage"),
    ("D. & N. Haveli", "Death of Dear persons"): (2, 1, "printed '2(6.2)'; 1/16 = 6.2% (2 would be 12.5%), the row then adds up to its printed Total 16 and the U.Ts.' column to the printed 8 (Grand Total 245 = 237 + 8)"),
    ("Hyderabad", "Insanity"): (8, 3, "printed '8(2.1)' (clear); 3/141 = 2.1% (8 would be 5.7%), the row then adds up to its printed Total 141 and the cities' column to the printed 65"),
}
ROWS = {
 "States": {
  "Andhra Pradesh": [69, 110, 215, 189, 168, 151, 140, 558, 33, 9, 6, 28, 1239, 2915],
  "Assam": [66, 41, 12, 82, 108, 28, 24, 211, 26, 18, 0, 16, 1309, 1941],
  "Bihar": [23, 44, 8, 37, 35, 7, 27, 62, 9, 4, 5, 11, 168, 440],
  "Gujarat": [14, 126, 169, 53, 58, 111, 12, 176, 55, 13, 17, 18, 803, 1625],
  "Haryana": [16, 100, 32, 33, 19, 20, 20, 54, 14, 23, 6, 16, 247, 600],
  "Himachal Pradesh": [0, 6, 0, 4, 6, 0, 0, 12, 1, 4, 1, 2, 49, 85],
  "Jammu & Kashmir": [2, 2, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 11, 19],
  "Karnataka": [61, 120, 90, 171, 115, 106, 86, 553, 41, 38, 40, 32, 2489, 3942],
  "Kerala": [46, 355, 261, 30, 254, 209, 126, 397, 16, 22, 6, 47, 2327, 4096],
  "Madhya Pradesh": [52, 377, 146, 19, 48, 76, 109, 524, 15, 21, 13, 33, 1111, 2544],
  "Maharashtra": [36, 280, 258, 55, 75, 155, 96, 548, 38, 61, 24, 31, 1603, 3260],
  "Manipur": [0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6],
  "Meghalaya": [2, 1, 6, 2, 2, 2, 0, 5, 1, 0, 1, 0, 9, 31],
  "Nagaland": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 12],
  "Orissa": [11, 210, 291, 36, 132, 20, 8, 215, 3, 5, 0, 0, 949, 1880],
  "Punjab": [16, 35, 31, 17, 22, 8, 2, 48, 8, 3, 2, 2, 87, 281],
  "Rajasthan": [13, 165, 67, 24, 24, 59, 7, 90, 7, 11, 9, 26, 337, 839],
  "Sikkim": [0, 0, 0, 14, 0, 3, 0, 4, 0, 0, 0, 0, 0, 21],
  "Tamil Nadu": [66, 351, 187, 128, 254, 45, 164, 1036, 86, 9, 38, 33, 2439, 4836],
  "Tripura": [23, 69, 52, 19, 104, 12, 5, 37, 0, 0, 2, 13, 100, 436],
  "Uttar Pradesh": [110, 247, 151, 105, 88, 130, 295, 275, 36, 18, 31, 65, 1526, 3077],
  "West Bengal": [201, 559, 626, 137, 648, 284, 159, 750, 53, 28, 36, 32, 3031, 6544],
  "TOTAL (STATES)": [827, 3198, 2604, 1158, 2162, 1426, 1280, 5555, 443, 288, 237, 405, 19847, 39430],
 },
 "U.Ts.": {
  "A. & N. Islands": [1, 6, 8, 1, 2, 1, 0, 4, 0, 0, 0, 3, 13, 39],
  "Arunachal Pradesh": [0, 0, 0, 1, 0, 2, 0, 2, 0, 0, 1, 0, 14, 20],
  "Chandigarh": [2, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 8, 17],
  "D. & N. Haveli": [0, 0, 8, 0, 0, 3, 0, 2, 0, 0, 1, 0, 2, 16],
  "Delhi": [12, 64, 31, 6, 22, 3, 8, 44, 6, 2, 5, 1, 193, 397],
  "Goa, Daman & Diu": [1, 3, 5, 4, 3, 7, 2, 19, 3, 3, 0, 1, 35, 86],
  "Lakshadweep": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  "Mizoram": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14],
  "Pondicherry": [1, 26, 85, 6, 3, 1, 0, 68, 3, 0, 1, 0, 31, 225],
  "TOTAL (U.TS.)": [17, 99, 138, 18, 30, 17, 10, 146, 12, 5, 8, 5, 310, 815],
 },
 "Cities": {
  "Ahmedabad": [4, 38, 0, 3, 13, 7, 0, 36, 4, 1, 1, 1, 70, 178],
  "Bangalore": [2, 2, 0, 2, 1, 8, 0, 26, 1, 0, 1, 0, 647, 690],
  "Bombay": [4, 11, 11, 5, 4, 16, 6, 20, 9, 3, 0, 2, 110, 201],
  "Calcutta": [0, 1, 3, 0, 1, 1, 0, 7, 0, 0, 0, 0, 12, 25],
  "Delhi": [11, 59, 22, 6, 22, 3, 8, 38, 6, 1, 0, 1, 169, 346],
  "Hyderabad": [7, 12, 12, 5, 12, 3, 0, 14, 2, 0, 0, 4, 70, 141],
  "Jaipur": [0, 9, 8, 0, 5, 2, 0, 8, 2, 4, 0, 11, 38, 87],
  "Kanpur": [8, 10, 2, 8, 10, 3, 4, 0, 3, 1, 0, 1, 0, 50],
  "Lucknow": [None, None, None, None, None, None, None, None, None, None, None, None, None, None],
  "Madras": [0, 35, 14, 27, 64, 6, 2, 142, 7, 2, 0, 0, 397, 696],
  "Nagpur": [2, 11, 6, 1, 3, 6, 0, 41, 3, 3, 14, 1, 62, 153],
  "Pune": [3, 8, 2, 0, 10, 10, 0, 11, 8, 13, 3, 0, 43, 111],
  "TOTAL (CITIES)": [41, 196, 80, 57, 145, 65, 20, 343, 45, 28, 19, 21, 1618, 2678],
 },
 "Grand": {"GRAND TOTAL": [844, 3297, 2742, 1176, 2192, 1443, 1290, 5701, 455, 293, 245, 410, 20157, 40245]},
}
