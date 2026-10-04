# ADSI 1970, Appendix II (raw/adsi/1970/table_content/appendix-2_1970.pdf, pages 1). Read from the page images.
# The edition prints no State-wise count of road accidents or of persons injured: only the accidental deaths 'On Roads'
# by sex (Male, Female) in the 'other causes' appendix. Persons killed = Male + Female; the other two columns are None.
# Both sex columns were checked against the printed Total (States), Total (U.Ts.), Grand Total and Total (Cities).
# The page with the States (part 1 of the appendix, which carries the On Roads columns) is not in this PDF (its pages 2-3 are the later cause columns), so only U.Ts., Grand Total and Cities are given; the States are not available.
KIND, YEAR, PUB = "traffic", 1970, "adsi"
SOURCE = "raw/adsi/1970/table_content/appendix-2_1970.pdf"
PAGES = "1"
TITLE = "Appendix II: Statement of number of accidental deaths in States/U.Ts./Cities, 1970 (by other causes: On Roads, by sex; U.Ts. and Cities only, the States page is not in the PDF)"
CHECK = "columns"
CATS = ["Road accidents (cases)", "Persons injured", "Persons killed"]
# corrections: (place, column): (printed, corrected, why)
CORRECTIONS = {}
# the deaths on roads as printed, by sex: place -> [Male, Female]; Persons killed above = Male + Female
ROADS_BY_SEX = {
 "U.Ts.": {
  "Andaman & Nicobar Islands": [1, 0],
  "Chandigarh": [3, 1],
  "Dadra & Nagar Haveli": [0, 0],
  "Delhi": [177, 12],
  "Goa, Daman & Diu": [8, 1],
  "Laccadives": [0, 0],
  "Pondicherry": [15, 3],
  "TOTAL (U.TS.)": [204, 17],
 },
 "Grand": {
  "GRAND TOTAL": [6139, 1149],
 },
 "Cities": {
  "Ahmedabad": [12, 4],
  "Bangalore": [34, 4],
  "Bombay": [611, 106],
  "Calcutta": [50, 9],
  "Delhi": [163, 8],
  "Hyderabad": [8, 0],
  "Kanpur": [57, 11],
  "Madras": [4, 0],
  "TOTAL (CITIES)": [939, 142],
 },
}
ROWS = {
 "U.Ts.": {
  "Andaman & Nicobar Islands": [None, None, 1],
  "Chandigarh": [None, None, 4],
  "Dadra & Nagar Haveli": [None, None, 0],
  "Delhi": [None, None, 189],
  "Goa, Daman & Diu": [None, None, 9],
  "Laccadives": [None, None, 0],
  "Pondicherry": [None, None, 18],
  "TOTAL (U.TS.)": [None, None, 221],
 },
 "Grand": {
  "GRAND TOTAL": [None, None, 7288],
 },
 "Cities": {
  "Ahmedabad": [None, None, 16],
  "Bangalore": [None, None, 38],
  "Bombay": [None, None, 717],
  "Calcutta": [None, None, 59],
  "Delhi": [None, None, 171],
  "Hyderabad": [None, None, 8],
  "Kanpur": [None, None, 68],
  "Madras": [None, None, 4],
  "TOTAL (CITIES)": [None, None, 1081],
 },
}
