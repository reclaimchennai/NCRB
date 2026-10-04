/* Annotations for unusual points in a series: known causes, and jumps that need checking.
 *
 * A point is flagged when it is far from its neighbours: more than 1.6 times, or under 0.6 times, the
 * median of the years within three either side (and the difference is not trivially small). A flagged
 * point gets the reason from EVENTS when one fits its year, place and category; otherwise a plain
 * "check the source" note. A few EVENTS are shown whenever their year is on the chart (they change
 * what the figure means even without a jump): the IPC being replaced by the BNS, a State being split.
 *
 * Reasons are what is on the public record (NCRB's own notes, the laws and reorganisation Acts); they
 * say "likely" where NCRB does not state the cause itself.
 */

const IPC = /ipc|cognizable|murder|rape|kidnap|abduct|dacoit|robber|burglar|theft|riot|cheat|breach|counterfeit|arson|hurt|dowry|modesty|cruelty|crime/i;
const WOMEN = /rape|modesty|molest|women|sexual|cruelty|dowry|354/i;
const TRAFFIC = /traffic|\broad|crash|vehicle|transport/i;

// {years, places (array, or null for every place), what (regex on category + table title), text, always}
export const EVENTS = [
  { years: [2020], what: IPC, always: true, text: 'COVID-19 lockdown: violations of prohibitory orders were booked under IPC Sections 188, 269 and 270, which swelled total IPC cases in 2020; Tamil Nadu\'s rose 5.3 times over 2019 and Gujarat\'s 2.7 times (Crime in India 2020).' },
  { years: [2021], what: /ipc|cognizable|total/i, text: 'Lockdown-related cases (IPC Sections 188, 269, 270) were still booked in 2021, though fewer than in 2020.' },
  { years: [2020], what: TRAFFIC, always: true, text: 'COVID-19 lockdown: far less traffic on the roads for months, so fewer crashes and deaths in 2020.' },
  { years: [2024], what: IPC, always: true, text: 'From 1 July 2024 crimes are booked under the Bharatiya Nyaya Sanhita (BNS) instead of the IPC; 2024 figures combine both, and some heads were renumbered or regrouped, so they may not match earlier years.' },
  { years: [2013], what: WOMEN, text: 'The Criminal Law (Amendment) Act, 2013 widened the definition of rape and added new offences against women (Sections 354A–D), after December 2012; more cases were registered from 2013.' },
  { years: [2014], what: IPC, text: 'NCRB redesigned Crime in India in 2014, adding, splitting and redefining several crime heads, so some 2014 figures are not directly comparable with 2013.' },
  { years: [2014], places: ['Andhra Pradesh', 'Telangana'], what: /./, always: true, text: 'Telangana was formed on 2 June 2014; Andhra Pradesh\'s figures before 2014 include it.' },
  { years: [2000, 2001], places: ['Bihar', 'Jharkhand'], what: /./, always: true, text: 'Jharkhand was carved out of Bihar on 15 November 2000.' },
  { years: [2000, 2001], places: ['Madhya Pradesh', 'Chhattisgarh'], what: /./, always: true, text: 'Chhattisgarh was carved out of Madhya Pradesh on 1 November 2000.' },
  { years: [2000, 2001], places: ['Uttar Pradesh', 'Uttarakhand'], what: /./, always: true, text: 'Uttarakhand (then Uttaranchal) was carved out of Uttar Pradesh on 9 November 2000.' },
  { years: [2019, 2020], places: ['Jammu & Kashmir', 'Ladakh'], what: /./, always: true, text: 'Jammu & Kashmir became a Union Territory and Ladakh a separate one on 31 October 2019.' },
  { years: [1953, 1954], places: ['Tamil Nadu', 'Andhra Pradesh', 'Andhra State'], what: /./, always: true, text: 'Andhra State was separated from Madras State on 1 October 1953; Madras (Tamil Nadu) figures up to 1953 include the Andhra districts.' },
  { years: [1956, 1957], places: ['Tamil Nadu', 'Kerala', 'Karnataka'], what: /./, always: true, text: 'States Reorganisation, 1 November 1956: Malabar went from Madras to the new Kerala, South Kanara to Mysore, and Kanyakumari came to Madras.' },
  { years: [1960, 1961], places: ['Maharashtra', 'Gujarat', 'Bombay State'], what: /./, always: true, text: 'Bombay State was split into Maharashtra and Gujarat on 1 May 1960.' },
  { years: [1966, 1967], places: ['Punjab', 'Haryana', 'Himachal Pradesh', 'Chandigarh'], what: /./, always: true, text: 'Punjab was reorganised on 1 November 1966: Haryana and Chandigarh were formed and the hill districts went to Himachal Pradesh.' },
];

const CIRCLED = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳';
export const circled = n => CIRCLED[n - 1] || `(${n})`;

function median(a) {
  const s = [...a].sort((x, y) => x - y);
  return s.length ? (s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2) : null;
}

/** Points far from their neighbours: [{year, v, m, dir}] */
export function outliers(values) {
  const ys = Object.keys(values).map(Number).filter(y => Number.isFinite(values[y])).sort((a, b) => a - b);
  const out = [];
  for (const y of ys) {
    const v = values[y];
    const near = ys.filter(x => x !== y && Math.abs(x - y) <= 3).map(x => values[x]);
    if (near.length < 2) continue;
    const m = median(near);
    if (!(m > 0)) continue;
    const r = v / m;
    // small counts swing a lot from year to year: under 100 a year, only a halving or doubling (and 25 or more) counts
    const far = m >= 100 ? (r > 1.6 || r < 0.6) && Math.abs(v - m) > 0.1 * m : (r > 2 || r < 0.5) && Math.abs(v - m) >= 25;
    if (far) out.push({ year: y, v, m, dir: r > 1 ? 'high' : 'low' });
  }
  return out;
}

/**
 * Notes for one series: [{n, year, text, kind}] in year order, numbered.
 * ctx: {place, what (category name + topic, not the table title), fmt, scanned (year -> read from a scanned page)}
 */
export function notesFor(values, { place = '', what = '', fmt = v => String(v), scanned = () => false } = {}) {
  const fits = (e, y) => e.years.includes(y) && (!e.places || e.places.includes(place)) && e.what.test(what);
  const ys = Object.keys(values).map(Number);
  const notes = new Map();
  for (const o of outliers(values)) {
    const e = EVENTS.find(ev => fits(ev, o.year));
    notes.set(o.year, {
      year: o.year, kind: e ? 'event' : 'check',
      text: e ? e.text
        : scanned(o.year)
          ? `Unusually ${o.dir} against the years around it (about ${fmt(Math.round(o.m))}), and read from a scanned page: check it against the source table. A misreading, a change in what NCRB counted, or a boundary change are the usual causes.`
          : `Unusually ${o.dir} against the years around it (about ${fmt(Math.round(o.m))}). This is the figure NCRB printed; its table gives no reason. A change in what was counted or a boundary change is the usual cause.`,
    });
  }
  for (const e of EVENTS) {
    if (!e.always) continue;
    const y = e.years.find(yy => ys.includes(yy) && fits(e, yy));
    if (y != null && !notes.has(y) && ![...notes.values()].some(n => n.text === e.text)) notes.set(y, { year: y, kind: 'event', text: e.text });
  }
  return [...notes.values()].sort((a, b) => a.year - b.year).map((n, i) => ({ ...n, n: i + 1 }));
}
