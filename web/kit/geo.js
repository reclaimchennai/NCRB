/* State and UT boundaries as they stood in a given year.
 *
 * web/geo/eras.json lists one boundary file per era, 1951-2024 (Part A/B/C
 * States, the 1956 reorganisation, Maharashtra and Gujarat in 1960, Punjab and
 * Haryana in 1966, the North-East in 1972, Sikkim, the 2000 States, Telangana,
 * Ladakh, the 2020 DNH & DD merger; see web/geo/README.md). A year takes the
 * map in force on 31 December. Each feature's `std` is the name the data rows
 * use (Madras -> Tamil Nadu; Bombay State and PEPSU keep their own), `name` is
 * the name it bore then.
 *
 * mapFor(year, redraw) returns the loaded map, or the last one loaded while
 * the right one is still on its way (redraw is called when it lands), so a
 * chart playing through the years never blinks.
 */

import { getJSON } from './util.js?v=c96e3ffe6c';

const BASE = '../geo/';
let eras = null, erasP = null, last = null, outline = null, outlineP = null;
const maps = {}, loading = {};

export function eraOf(year) {
  if (!eras) return null;
  return eras.find(e => year >= e.from && year <= e.to) || (year < eras[0].from ? eras[0] : eras.at(-1));
}

export function mapFor(year, redraw) {
  if (!eras) {
    erasP ||= getJSON(`${BASE}eras.json`).then(e => { eras = e; redraw?.(); });
    return last;
  }
  const e = eraOf(year);
  if (maps[e.file]) return (last = maps[e.file]);
  loading[e.file] ||= getJSON(`${BASE}${e.file}`).then(g => { maps[e.file] = g; redraw?.(); });
  return last;
}

export function outlineMap(redraw) {
  if (outline) return outline;
  outlineP ||= getJSON(`${BASE}india-outline.geojson`).then(g => { outline = g; redraw?.(); });
  return null;
}

/** A line for the map's note: whose boundaries these are. */
export function boundaryNote(year) {
  const e = eraOf(year);
  return e ? `Boundaries as on 31 December ${year} (map of ${e.from === e.to ? e.from : `${e.from}–${e.to}`}), drawn from 2011 census districts; see the sources below.` : '';
}
