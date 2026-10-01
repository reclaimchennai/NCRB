/* The footer: sources, how the figures were read, and every caveat, in one
 * place so the charts themselves can stay clean. */

export const SOURCE_LINE = 'Data: National Crime Records Bureau (NCRB), Accidental Deaths & Suicides in India; "Suicides in India 2001–2012" (NCRB, data.gov.in). Figures as published; categories harmonised across editions.';

export function footerHtml({ extra = '' } = {}) {
  return `
  <p><b>Made by <a href="https://reclaimchennai.city">@reclaimchennai</a>.</b> Every picture and video saved from these charts carries the same credit and source.</p>
  <h3>Sources</h3>
  <ul>
    <li><a href="https://www.ncrb.gov.in/accidental-deaths-suicides-in-india-table-content.html" target="_blank" rel="noopener">National Crime Records Bureau, <i>Accidental Deaths &amp; Suicides in India</i></a> (ADSI), every edition from 1967 to 2024: the tables NCRB publishes for each year, the additional tables, and the full reports.</li>
    <li><i>Suicides in India 2001–2012</i>, the State-wise dataset NCRB contributed to the Open Government Data platform (<a href="https://data.gov.in" target="_blank" rel="noopener">data.gov.in</a>). It fills 2001–2003, which NCRB's site does not carry as tables, and gives an age breakdown for every suicide table up to 2012. Where NCRB's own table exists for a year, that table is used.</li>
  </ul>
  <h3>How the figures were read and checked</h3>
  <ul>
    <li>Editions from about 2001 are digital: figures are copied from the PDF's text or the spreadsheet, digit for digit. Older editions are scanned books, read with OCR and with an AI document model (GLM-OCR); for each table the reading whose figures add up to NCRB's printed totals is kept.</li>
    <li>Every year of every place is checked against the totals printed with it (the sexes against the total, the hours or months against the year). A year that does not add up is left out rather than shown, so a gap in a line means either NCRB did not publish that figure or the scan could not be read reliably.</li>
    <li>NCRB rewords and regroups its categories between editions ("Poison (consuming insecticides)" in 2004, "By consuming insecticides" in 2014). They are mapped to one list; the printed labels are kept in the downloadable data.</li>
    <li>Age groups changed in 2014: up to 2013 they were up to 14, 15–29, 30–44, 45–59 and 60+; from 2014 below 14, 14–17, 18–29, 30–44, 45–59 and 60+. 30–44, 45–59 and 60+ run unbroken.</li>
    <li>In 2014 NCRB split the 'others' professions into new groups (daily wage earners, agricultural labourers…), so shares before and after 2014 are not comparable for those groups.</li>
    <li>City-wise tables of suicides by means, profession and education stop in 2015, and by age and sex in 2015 (State-wise age and sex is printed again from 2021). Traffic accidents are counted by time and month for every State and big city; deaths by time and month are printed only State-wise, from 2021.</li>
    <li>Rates are suicides per lakh people as NCRB printed them. City rates use a fixed census population (2001 census up to 2010, 2011 census from 2011), so a change in a city's rate is a change in its count.</li>
    <li>For 1993–2000 NCRB's website carries only the accident tables; its suicide chapters for those years hold the text and summary tables, not the State and city tables, so State-wise suicide figures for 1993–2000 are not available from NCRB online. 2001–2003 come from the data.gov.in dataset; the rate itself (which needs the population) is printed from 2004.</li>
    <li>Places are named as they are today (Madras is Chennai, Bombay is Mumbai, Allahabad is Prayagraj). A State's figures before and after a split (Andhra Pradesh and Telangana, 2014) cover different areas.</li>
    ${extra}
  </ul>
  <p>Data and code: <a href="https://github.com/reclaimchennai/NCRB" target="_blank" rel="noopener">github.com/reclaimchennai/NCRB</a>. This site reformats NCRB's published statistics; it is not an official NCRB product. Cite NCRB and the report year, and check figures against the source before relying on them.</p>
  <p class="credits">Icons from <a href="https://lucide.dev" target="_blank" rel="noopener">Lucide</a> (ISC) and <a href="https://tabler.io/icons" target="_blank" rel="noopener">Tabler</a> (MIT). Video written with <a href="https://github.com/Vanilagy/mp4-muxer" target="_blank" rel="noopener">mp4-muxer</a> (MIT). Design shared with <a href="https://cpi.reclaimchennai.city" target="_blank" rel="noopener">cpi.reclaimchennai.city</a>. Part of <a href="https://reclaimchennai.city">reclaimchennai.city</a>.</p>`;
}
