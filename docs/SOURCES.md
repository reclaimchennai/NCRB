# Sources

Everything comes from the National Crime Records Bureau website,
<https://www.ncrb.gov.in>. The crawler reads these listing pages, once per year
offered in each page's year filter:

| Publication | Listing (`listing` in the data) | Page |
|---|---|---|
| Crime in India | `year_wise` | <https://www.ncrb.gov.in/crime-in-india-year-wise.html> |
| | `table_content` | <https://www.ncrb.gov.in/crime-in-india-table-content.html> |
| | `additional_table` | <https://www.ncrb.gov.in/crime-in-india-additional-table.html> |
| | `table_chapter` | <https://www.ncrb.gov.in/crime-in-india-table-chapter.html> |
| Prison Statistics India | `year_wise` | <https://www.ncrb.gov.in/prison-statistics-india-year-wise.html> |
| | `table_content` | <https://www.ncrb.gov.in/table-contents-of-psi-reports.html> |
| Accidental Deaths & Suicides in India | `year_wise` | <https://www.ncrb.gov.in/accidental-deaths-suicides-in-india-year-wise.html> |
| | `table_content` | <https://www.ncrb.gov.in/accidental-deaths-suicides-in-india-table-content.html> |
| | `additional_table` | <https://www.ncrb.gov.in/accidental-death-and-suicides-additional-table.html> |

The landing pages (<https://www.ncrb.gov.in/crime-in-india.html>,
`prison-statistics-india.html`, `accidental-deaths-suicides-in-india-adsi.html`)
and the "all previous publications" pages only link to the year-wise pages
above, so they add no files.

What each listing holds:

- **year_wise**: the report as NCRB splits it for a given year: complete
  volumes where available, chapters, snapshots, maps, forewords, glossaries.
  For the earliest years (Crime in India 1953–1963, ADSI 1967 onwards) this is
  the only form in which the report exists.
- **table_content**: one file per table of the report, with the table's title
  and the chapter it belongs to. This is the main source of the data.
- **additional_table**: tables NCRB publishes only on the website, mostly
  Excel from 2014 onwards (crime-head-wise detail, city-wise breakdowns).
- **table_chapter**: Crime in India chapters and appendices of the older
  volumes, where tables were not split out individually.

`catalog/catalog.csv` records, for every file, the listing page URL it was
found on; `catalog/listing_html/` keeps the pages as fetched.

Not collected: NCRB's other publications (Finger Prints in India, Missing
Women & Children, Crime Statistics, journals), which are outside the pages
listed above.
