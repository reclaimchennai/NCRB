/* Explore: every NCRB table printed in three or more editions, joined over the years.
 *
 * Data: web/data/explore/ (analysis/families.py). A family is one table
 * followed across editions. Its columns are split into a category ("Murder",
 * "Bankruptcy or indebtedness") and a breakdown (Total / Male / Female ...);
 * its rows are States, UTs and cities, or its own row labels. Totals and
 * subtotals are flagged, shown last and kept off the colour scales.
 */

import { $, el, icon, esc, getJSON, initTheme, debounce, fmtN, fmt1, fmtShort, SERIES, lerp } from '../kit/util.js?v=77a1ee7583';
import { lineChart, barRows, heatmap, choropleth, emptyChart } from '../kit/grapher.js?v=77a1ee7583';
import { segmented, select, toggle, Timeline, at, card, bindCapture } from '../kit/cards.js?v=77a1ee7583';
import { footerHtml, creditLine } from '../kit/footer.js?v=77a1ee7583';
import { explain, explainAll } from '../kit/legal.js?v=77a1ee7583';
import { notesFor } from '../kit/notes.js?v=77a1ee7583';
import { mapFor, outlineMap, boundaryNote } from '../kit/geo.js?v=77a1ee7583';

const DATA = '../data/explore';
const TYPE_LABEL = { total: 'India', state: 'States', ut: 'Union Territories', city: 'Cities', row: 'Rows' };
const GEO_LABEL = { state: 'States & UTs', city: 'Cities', india: 'All India', '': 'All India' };
const S = { index: null, fam: null, pub: 'cii', topic: null, id: null, cat: 0, brk: 0, row: 0, rankType: 'state', compare: true, perLakh: false };
let POP = {};   // 'Tamil Nadu|state' -> {year: population in lakhs}, as NCRB printed it (analysis/population.py)
const tl = new Timeline({ speed: 1.2 });
const ui = {}, C = {};

/* ------------------------------------------------------------------ data */

const fams = () => S.index.families.filter(f => f.pub === S.pub);
const topics = () => [...new Set(fams().map(f => f.topic))];
const report = () => S.index.reports[S.pub];
function series(r, c = S.cat, b = S.brk) {
  const a = S.fam.d[`${r}.${c}.${b}`];
  if (!a) return {};
  const o = {};
  // per lakh people: the count divided by NCRB's population for that place and year (years without one are left out)
  const pop = S.perLakh && canPerLakh(c) ? POP[`${S.fam.rows[r]?.name}|${S.fam.rows[r]?.type}`] : null;
  for (let i = 0; i < a.length; i += 2) {
    if (!pop) o[a[i]] = a[i + 1];
    else if (pop[a[i]]) o[a[i]] = Math.round((a[i + 1] / pop[a[i]]) * 100) / 100;
  }
  if (S.perLakh && canPerLakh(c) && !pop) return {};
  return o;
}
/** A count of a place (not a rate, share or population) can be shown per lakh people. */
function canPerLakh(c = S.cat) {
  return places() && !isRateCat(c) && !/population|lakh|crore|rupees|₹|\brs\b|expenditure|budget|capacity|strength|rank/i.test(`${catName(c)} ${S.fam.title}`);
}
const places = () => S.fam.mode === 'places';
const rowName = r => S.fam.rows[r]?.name ?? '';
const catName = c => S.fam.cats[c]?.name ?? '';
const brkName = b => S.fam.brks[b] ?? '';
/** What is shown, in words: "Bankruptcy or Indebtedness, male". */
function measure(c = S.cat, b = S.brk) {
  const bn = brkName(b);
  const split = S.fam.brks.some(x => x && x !== 'Total');   // only say 'all' where there is a male/female/... to set it against
  return `${catName(c)}${bn && bn !== 'Total' ? `, ${bn.toLowerCase()}` : bn === 'Total' && split ? ', all' : ''}`;
}
/** The y axis unit, in words, from the category and the table title. */
function unitOf(c = S.cat) {
  const n = catName(c), t = S.fam.title;
  if (S.perLakh && canPerLakh(c)) return `${unitOfCount(c)} per lakh people`;
  return unitOfCount(c);
}
function unitOfCount(c = S.cat) {
  const n = catName(c), t = S.fam.title;
  if (/per lakh|crime rate|^rate\b|\brate\b/i.test(n)) return /population|per lakh|crime rate/i.test(n + t) ? 'per lakh population' : 'rate';
  if (/%|percent|share/i.test(n)) return '% (as printed by NCRB)';
  if (/\blakhs?\b/i.test(n)) return 'lakh';
  if (/\bcrores?\b|\brs\b\.?|rupees|expenditure|budget|₹/i.test(n)) return 'as printed (₹)';
  const what = /suicid/i.test(n + t) ? 'suicides' : /died|deaths?|killed/i.test(n + t) ? 'deaths' : /prisoner|inmate|convict|undertrial|detenu/i.test(n + t) ? 'persons' :
    /arrest|apprehend|offender|accused|persons|victims|juvenile|recidiv/i.test(n + t) ? 'persons' : /crashes|accidents/i.test(n + t) ? 'crashes' : /cases|crime|incidence/i.test(n + t) ? 'cases' : 'number';
  return what;
}
const isRateCat = (c = S.cat) => /rate|percent|%|share|ratio|average|per lakh/i.test(catName(c)) || brkName(S.brk) === 'Rate';
const isRate = () => isRateCat() || (S.perLakh && canPerLakh());
const fmtV = v => (v == null ? '–' : isRate() || !Number.isInteger(v) ? fmt1(v) : fmtN(v));
const rowsOfType = types => S.fam.rows.map((r, i) => ({ ...r, i })).filter(r => types.includes(r.type));
const brksFor = c => S.fam.brks.map((b, i) => ({ b, i })).filter(({ i }) => S.fam.rows.some((_, r) => S.fam.d[`${r}.${c}.${i}`]));
const geoLabel = () => GEO_LABEL[S.fam.geo] ?? '';

function rankPool() {
  return rowsOfType(S.rankType === 'state' ? ['state', 'ut'] : [S.rankType]).filter(r => !r.total);
}
/** Years in which the shown figure exists for any row of the current comparison, or for the chosen row. */
function shownYears() {
  const ys = new Set();
  for (const r of rankPool()) for (const y of Object.keys(series(r.i))) ys.add(Number(y));
  for (const y of Object.keys(series(S.row))) ys.add(Number(y));
  return [...ys].sort((a, b) => a - b);
}

function credit(years) {
  return creditLine({ tables: S.fam.sources, year_sources: {} }, years, null, report());
}
function metaFor(c, withYear) {
  return () => ({
    kicker: `${S.fam.topic} · ${report()}`,
    title: $('h2', c.el).textContent,
    subtitle: $('.titles p', c.el).textContent,
    year: withYear ? tl.year : null,
    source: credit(withYear ? [tl.year] : shownYears()),
    notes: c === C.trend ? trendNotes.map(n => `(${n.n}) ${n.year}: ${n.text}`) : [],
  });
}

/* -------------------------------------------------------------- controls */

function buildControls() {
  const bar = $('#controls');
  ui.pub = segmented({
    label: 'Report', value: S.pub,
    options: [{ value: 'cii', label: 'Crime', icon: 'database' }, { value: 'adsi', label: 'Crashes & suicides', icon: 'activity' }, { value: 'psi', label: 'Prisons', icon: 'building' }],
    onChange: v => { S.pub = v; S.topic = topics()[0]; pickTopic(); },
  });
  ui.topic = select({ label: 'Topic', lead: 'layers', small: 'TOPIC', options: [], onChange: v => { S.topic = v; pickTopic(); } });
  ui.table = select({ label: 'Table', lead: 'table', small: 'TABLE', options: [], onChange: v => loadFamily(v) });
  ui.cat = select({ label: 'Category', small: 'SHOW', options: [], onChange: v => { S.cat = Number(v); syncBrk(); afterChange(); } });
  ui.brk = segmented({ label: 'Breakdown', options: [], onChange: v => { S.brk = Number(v); afterChange(); } });
  ui.row = select({ label: 'Place or row', lead: 'map-pin', small: 'FOR', options: [], onChange: v => { S.row = Number(v); refresh(); } });
  ui.per = segmented({ label: 'Count or rate', options: [{ value: 'n', label: 'Number' }, { value: 'l', label: 'Per lakh people' }],
                       onChange: v => { S.perLakh = v === 'l'; afterChange(); } });
  const tlWrap = el('div', { class: 'tlbar', style: 'flex:1 1 100%' });
  tl.root.style.padding = '0';
  tlWrap.append(tl.root);
  bar.append(ui.pub.el, ui.topic.el, ui.table.el, ui.cat.el, ui.brk.el, ui.per.el, ui.row.el, tlWrap);
  ui.table.el.style.maxWidth = 'min(640px, 100%)';
  ui.cat.el.style.maxWidth = 'min(520px, 100%)';
}

function pickTopic(id = null) {
  ui.topic.options(topics().map(t => ({ value: t, label: `${t} (${fams().filter(f => f.topic === t).length})` })), S.topic);
  const list = fams().filter(f => f.topic === S.topic);
  const byGeo = {};
  for (const f of list) (byGeo[GEO_LABEL[f.geo] ?? 'All India'] ||= []).push(f);
  ui.table.options(Object.entries(byGeo).map(([g, l]) => ({ group: g, options: l.map(f => ({ value: f.id, label: `${f.title} · ${f.y0}–${f.y1}` })) })), id || list[0]?.id);
  loadFamily(id || list[0]?.id);
}

async function loadFamily(id) {
  const meta = S.index.families.find(f => f.id === id && f.pub === S.pub);
  if (!meta) return;
  S.id = id;
  S.fam = await getJSON(`${DATA}/${S.pub}/${id}.json`);
  ui.table.set(id);
  // default category: the first non-total, non-rate category filled in most years; breakdown Total
  const filled = c => { let n = 0; S.fam.rows.forEach((_, r) => S.fam.brks.forEach((__, b) => { const a = S.fam.d[`${r}.${c}.${b}`]; if (a) n += a.length / 2; })); return n; };
  let best = 0, bestN = -1;
  S.fam.cats.forEach((c, i) => {
    const n = filled(i) * (c.total ? 0.6 : 1) * (/percent|%|share|rate|rank|ratio|variation|change/i.test(c.name) ? 0.3 : 1);
    if (n > bestN) { best = i; bestN = n; }
  });
  S.cat = S.want?.c != null && S.fam.cats[S.want.c] ? S.want.c : best;
  ui.cat.options(catOptions(), S.cat);
  syncBrk(S.want?.b);
  const groups = {};
  S.fam.rows.forEach((r, i) => (groups[r.type] ||= []).push({ value: i, label: r.name }));
  ui.row.options(['total', 'state', 'ut', 'city', 'row'].filter(t => groups[t]).map(t => ({ group: TYPE_LABEL[t], options: groups[t] })));
  const want = S.want?.p != null ? S.want.p : S.fam.rows.findIndex(r => r.name === 'Tamil Nadu');
  S.row = want >= 0 && S.fam.rows[want] ? want : Math.max(0, S.fam.rows.findIndex(r => r.type === 'total'));
  ui.row.set(S.row);
  ui.row.el.hidden = S.fam.rows.length < 2;
  S.rankType = S.fam.rows.some(r => r.type === 'state') ? 'state' : S.fam.rows.some(r => r.type === 'city') ? 'city' : 'row';
  const wy = S.want?.y;
  S.want = null;
  tl.setYears(shownYears(), true);
  if (wy) tl.gotoYear(wy, false);
  refresh();
}
/** Categories grouped under their parent heading ("Offences under I.T. Act" › "Tampering ..."); totals at the end of each group. */
function catOptions() {
  const groups = new Map();
  S.fam.cats.forEach((c, i) => {
    const parts = c.name.split(' · ');
    const g = parts.length > 1 ? parts.slice(0, -1).join(' · ') : '';
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push({ value: i, label: `${c.total ? '∑ ' : ''}${parts.at(-1)}`.slice(0, 110), total: c.total });
  });
  const sortT = l => l.filter(o => !o.total).concat(l.filter(o => o.total));
  if (groups.size === 1) return sortT([...groups.values()][0]);
  return [...groups.entries()].map(([g, l]) => ({ group: g || 'Overall', options: sortT(l) }));
}
function syncBrk(want) {
  const avail = brksFor(S.cat);
  if (want != null && avail.some(a => a.i === want)) S.brk = want;
  else if (!avail.some(a => a.i === S.brk)) S.brk = (avail.find(a => a.b === 'Total') || avail[0] || { i: 0 }).i;
  ui.brk.options(avail.map(({ b, i }) => ({ value: i, label: b === 'Total' ? (avail.some(x => x.b === 'Victims' || x.b === 'Rate') ? 'Cases' : 'All') : b === 'Rate' ? 'Rate per lakh' : b || 'Value' })), S.brk);
  ui.brk.el.hidden = avail.length < 2;
}
function afterChange() { tl.setYears(shownYears(), true); refresh(); }

/* ----------------------------------------------------------------- cards */

function buildCards() {
  const root = $('#cards');
  C.law = el('section', { class: 'card law', id: 'x-law', hidden: true });
  root.append(C.law);
  C.trend = card(root, { id: 'x-trend', kicker: 'Over the years' });
  bindCapture(C.trend, { meta: metaFor(C.trend, false), name: 'ncrb-explore-trend' });
  C.cmp = toggle({ label: 'Show the largest too', value: S.compare, onChange: v => { S.compare = v; drawTrend(); } });
  C.trend.toolbar.append(C.cmp.el);

  const g = el('div', { class: 'grid2' });
  root.append(g);
  C.rank = card(g, { id: 'x-rank', kicker: 'Compare', rec: true });
  bindCapture(C.rank, { meta: metaFor(C.rank, true), record: { timeline: tl, render: p => drawRank(p) }, name: 'ncrb-explore-compare' });
  C.rankType = segmented({ label: 'Which rows', options: [], onChange: v => { S.rankType = v; tl.setYears(shownYears(), true); refresh(); } });
  C.rank.toolbar.append(C.rankType.el);
  C.map = card(g, { id: 'x-map', kicker: 'India', rec: true });
  bindCapture(C.map, { meta: metaFor(C.map, true), record: { timeline: tl, render: p => drawMap(p) }, name: 'ncrb-explore-map' });

  C.heat = card(root, { id: 'x-heat', kicker: 'Every category, every year' });
  bindCapture(C.heat, { meta: metaFor(C.heat, false), name: 'ncrb-explore-table' });
  tl.on(pos => { drawRank(pos); drawMap(pos); markTrend(pos); });
  tl.on((pos, settled) => { if (settled) { drawHeat(); writeHash(); } });
  let lastW = innerWidth;
  addEventListener('resize', debounce(() => { if (innerWidth !== lastW) { lastW = innerWidth; refresh(); } }, 120));
}

function refresh() {
  if (!S.fam) return;
  ui.per.el.hidden = !canPerLakh();
  ui.per.set(S.perLakh ? 'l' : 'n');
  writeHash();
  drawTiles();
  drawLaw();
  drawTrend();
  drawRank(tl.pos);
  drawMap(tl.pos);
  drawHeat();
}

function drawTiles() {
  const s = series(S.row);
  const ys = Object.keys(s).map(Number).sort((a, b) => a - b);
  const last = ys.at(-1), prev = ys.at(-2);
  const v = s[last], p = s[prev];
  const t = [
    { k: measure() + (S.perLakh && canPerLakh() ? ' per lakh people' : ''), i: 'hash', v: fmtV(v), d: `${rowName(S.row)}, ${last ?? 'no figure'}` },
    { k: 'Change', i: 'trend-up', v: v != null && p ? `${v >= p ? '+' : ''}${(((v - p) / p) * 100).toFixed(1)}%` : '–', d: prev ? `against ${prev}` : '' },
    { k: 'Years with figures', i: 'calendar', v: String(ys.length), d: ys.length ? `${ys[0]}–${last}` : '' },
    { k: 'Table', i: 'table', v: `${S.fam.cats.length}`, d: `categories · ${S.fam.rows.length} ${places() ? 'places' : 'rows'} · ${geoLabel()}` },
  ];
  $('#tiles').innerHTML = t.map(x => `<div class="tile"><div class="k">${icon(x.i)}<span>${esc(x.k)}</span></div><div class="v">${x.v}</div><div class="d">${esc(x.d)}</div></div>`).join('');
}

/* the law behind the figure */
function drawLaw() {
  const ctx = `${S.fam.title} ${S.fam.topic}`;
  const here = explain(catName(S.cat), ctx);
  const all = explainAll(S.fam.cats.map(c => c.name).concat([S.fam.title]), ctx).filter(e => !here.some(h => h.label === e.label));
  if (!here.length && !all.length) { C.law.hidden = true; return; }
  C.law.hidden = false;
  C.law.innerHTML = `<div class="card-head"><div class="titles"><div class="kicker">What the law says</div>
    <h2>${esc(here.length ? catName(S.cat) : 'Laws named in this table')}</h2></div></div>
    <div class="card-body">${here.length ? `<dl class="law-list">${here.map(e => `<dt>${esc(e.label)}</dt><dd>${esc(e.text)}</dd>`).join('')}</dl>` : ''}
    ${all.length ? `<details${here.length ? '' : ' open'}><summary>Other sections and Acts in this table (${all.length})</summary><dl class="law-list">${all.map(e => `<dt>${esc(e.label)}</dt><dd>${esc(e.text)}</dd>`).join('')}</dl></details>` : ''}
    <p class="note">Plain-language summaries, not the text of the law. IPC sections apply to crimes up to 30 June 2024; the Bharatiya Nyaya Sanhita (BNS) after.</p></div>`;
}

/* 1. over the years */
let trendArgs = null, trendNotes = [];
function drawTrend() {
  const c = C.trend;
  const list = [{ key: 'sel', label: rowName(S.row), color: 'var(--critical)', values: series(S.row) }];
  if (S.compare && S.fam.rows.length > 1) {
    const type = S.fam.rows[S.row]?.type;
    const pool = rowsOfType(type === 'total' || type === 'ut' ? ['state', 'ut'] : [type]).filter(r => r.i !== S.row && !r.total);
    const lastOf = r => { const s = series(r.i); const ys = Object.keys(s).map(Number); return ys.length ? s[Math.max(...ys)] : -1; };
    pool.map(r => ({ r, v: lastOf(r) })).filter(x => x.v >= 0).sort((a, b) => b.v - a.v).slice(0, places() ? 5 : 7)
      .forEach((b, k) => list.push({ key: b.r.i, label: b.r.name, color: SERIES(k), values: series(b.r.i) }));
  }
  // the x axis spans only the years that something drawn has a figure for
  const ys = [...new Set(list.flatMap(s => Object.keys(s.values).map(Number)))].sort((a, b) => a - b);
  if (!ys.length) { emptyChart(c.svg, `No figures for ${rowName(S.row)} under ${measure()}.`); trendArgs = null; }
  else {
    const xs = []; for (let y = ys[0]; y <= ys.at(-1); y++) xs.push(y);
    // annotations on the place shown: known causes of unusual years, and jumps that need checking
    const scannedYear = y => (S.fam.sources?.[y] || []).some(x => !['pdf_text', 'excel'].includes(x.method));
    trendNotes = notesFor(series(S.row), { place: rowName(S.row), what: `${catName(S.cat)} ${S.fam.topic}`, fmt: fmtV, scanned: scannedYear });
    trendArgs = { xs, series: list, fmt: fmtV, yFmt: v => (isRate() ? fmt1(v) : fmtShort(v)), unit: unitOf(),
                  marks: trendNotes.map(n => ({ key: 'sel', x: n.year, n: n.n, kind: n.kind })) };
    markTrend(tl.pos);
  }
  c.setLegend(list.map(s => ({ label: s.label, color: s.color, line: true })));
  const perNote = S.perLakh && canPerLakh() ? ' · per lakh people, on the population NCRB printed for each year' : '';
  c.set({ title: `${measure()}${S.perLakh && canPerLakh() ? ' per lakh people' : ''}: ${rowName(S.row)}`, sub: `${S.fam.title} · ${geoLabel()}${perNote}${S.compare && list.length > 1 ? ' · with the largest in their latest year' : ''}` });
  const own = Object.keys(series(S.row)).map(Number);
  const gaps = trendArgs ? trendArgs.xs.filter(y => !own.includes(y)) : [];
  const noteRows = trendArgs ? trendNotes.map(n => `<li class="${n.kind}"><span class="nmark">${n.n}</span><b>${n.year}</b> ${esc(n.text)}</li>`).join('') : '';
  const gapText = gaps.length ? `<p>No figure for ${esc(rowName(S.row))} in ${gaps.length} of ${trendArgs.xs.length} years (${span(gaps)}): not printed in that edition, the category was not in the table then, or a scanned page did not add up to its totals.</p>` : '';
  // what NCRB's road-crash breakdowns mean (2014-2020 tables count by the vehicle at fault and the one hit)
  const bn = brkName(S.brk);
  const brkHelp = /^(Offenders|Victims|Offenders \+ victims)$/.test(bn)
    ? '<p><b>Offenders</b> are deaths in crashes where this vehicle was the one held responsible; <b>Victims</b> are deaths in crashes where this vehicle (or a pedestrian) was the one hit; <b>Offenders + victims</b> is NCRB\'s total of the two. NCRB printed these in 2014–2020; from 2021 it counts the people injured and killed travelling in each vehicle instead, so the two are not one series.</p>'
    : /^(Died|Injured)$/.test(bn) && S.fam.brks.includes('Offenders') ? '<p>From 2021 NCRB counts the people injured and killed travelling in each vehicle; 2014–2020 counted by the vehicle at fault and the one hit (see the Offenders and Victims breakdowns), so the years before 2021 are not on this line.</p>' : '';
  c.set({ note: (noteRows ? `<ul class="chart-notes">${noteRows}</ul>` : '') + gapText + brkHelp });
}
function markTrend(pos) {
  if (!trendArgs) return;
  const xs = trendArgs.xs, ys = tl.years;
  if (!ys.length) return lineChart(C.trend.svg, trendArgs);
  const i0 = Math.floor(pos), f = pos - i0;
  const yr = lerp(ys[i0], ys[Math.min(ys.length - 1, i0 + 1)], f);
  const k = xs.indexOf(Math.floor(yr));
  lineChart(C.trend.svg, { ...trendArgs, pos: k >= 0 ? k + (yr - Math.floor(yr)) : null, zeroBase: true });
}
function span(ys) {
  const out = []; let s = ys[0], p = ys[0];
  for (const y of ys.slice(1).concat(null)) { if (y === p + 1) { p = y; continue; } out.push(s === p ? `${s}` : `${s}–${p}`); s = p = y; }
  return out.join(', ');
}

/* 2. compare */
function drawRank(pos) {
  const c = C.rank, ys = tl.years;
  const types = [...new Set(S.fam.rows.map(r => r.type))];
  const opts = [];
  if (types.includes('state') || types.includes('ut')) opts.push({ value: 'state', label: 'States & UTs', icon: 'map-pin' });
  if (types.includes('city')) opts.push({ value: 'city', label: 'Cities', icon: 'building' });
  if (types.includes('row')) opts.push({ value: 'row', label: 'Rows', icon: 'table' });
  if (!opts.some(o => o.value === S.rankType)) S.rankType = opts[0]?.value;
  C.rankType.options(opts, S.rankType);
  C.rankType.el.hidden = opts.length < 2;
  const pool = rankPool();
  if (!ys.length || !pool.length) { emptyChart(c.svg); return; }
  const y = ys[Math.round(pos)];
  const i0 = Math.floor(pos), i1 = Math.min(ys.length - 1, i0 + 1), f = pos - i0;
  const val = (r, yy) => series(r.i)[yy];
  const ord = yy => new Map(pool.map(r => [r.i, val(r, yy)]).filter(([, v]) => v != null).sort((a, b) => b[1] - a[1]).map(([k], n) => [k, n]));
  const o0 = ord(ys[i0]), o1 = ord(ys[i1]);
  const limit = 30;
  const rows = pool.map(r => {
    const a = val(r, ys[i0]), b = val(r, ys[i1]);
    const v = a != null && b != null ? lerp(a, b, f) : f < .5 ? a : b;
    const k = o0.has(r.i) && o1.has(r.i) ? lerp(o0.get(r.i), o1.get(r.i), f) : (o0.get(r.i) ?? o1.get(r.i));
    return { key: r.i, label: r.name, value: v, rank: k, hl: r.i === S.row, color: r.i === S.row ? 'var(--critical)' : 'var(--series-1)' };
  }).filter(r => r.value != null && r.rank != null && (r.rank < limit || r.hl));
  rows.forEach(r => { if (r.hl && r.rank >= limit) r.rank = limit; });
  let gmax = 0; for (const r of pool) for (const yy of ys) gmax = Math.max(gmax, val(r, yy) || 0);
  if (!rows.length) emptyChart(c.svg, `Nothing printed for ${y}.`);
  else barRows(c.svg, { rows, max: gmax, fmt: fmtV, bigYear: y });
  const who = S.rankType === 'row' ? 'every row' : S.rankType === 'city' ? 'the cities' : 'States and UTs';
  c.set({ title: `${measure()}, ${y}`, sub: `${who}${pool.length > limit ? `, largest ${limit}` : ''} · ${S.fam.title}` });
}

/* 3. map: the State boundaries of the year shown */
function drawMap(pos) {
  const c = C.map;
  const st = rowsOfType(['state', 'ut']);
  if (!places() || st.length < 10) { c.el.hidden = true; return; }
  c.el.hidden = false;
  const ys = tl.years;
  if (!ys.length) return;
  const y = ys[Math.round(pos)];
  const geo = mapFor(y, () => drawMap(tl.pos)), outline = outlineMap(() => drawMap(tl.pos));
  if (!geo || !outline) return;
  const values = {};
  let gmax = 0;
  for (const r of st) {
    const s = series(r.i);
    const v = at(s, ys, pos);
    if (v != null) values[r.name] = v;
    for (const yy of ys) gmax = Math.max(gmax, s[yy] || 0);
  }
  const hl = ['state', 'ut'].includes(S.fam.rows[S.row]?.type) ? rowName(S.row) : null;
  choropleth(c.svg, { geo, outline, values, max: gmax, year: y, fmt: fmtV, hl, label: measure() });
  c.set({ title: `${measure()} by State and UT, ${y}`, sub: `${S.fam.title} · colour scale fixed across ${ys[0]}–${ys.at(-1)}`, note: boundaryNote(y) });
}

/* 4. every category, every year (for the chosen breakdown) */
function drawHeat() {
  const c = C.heat;
  const cats = S.fam.cats.map((cat, i) => ({ ...cat, i })).filter(x => Object.keys(series(S.row, x.i)).length);
  if (!cats.length) { c.el.hidden = true; return; }
  c.el.hidden = false;
  // only the years with a figure for the row shown
  const ys = [...new Set(cats.flatMap(x => Object.keys(series(S.row, x.i)).map(Number)))].sort((a, b) => a - b);
  const ordered = cats.filter(x => !x.total).concat(cats.filter(x => x.total));
  const totalRows = new Set(ordered.map((x, k) => (x.total ? k : -1)).filter(k => k >= 0));
  const rate = x => /rate|percent|%|share|ratio|average|per lakh/i.test(x.name);
  // one colour scale for the counts; rates and percentages each on their own range
  const max = Math.max(1, ...ordered.filter(x => !x.total && !rate(x)).flatMap(x => Object.values(series(S.row, x.i))));
  const rowMax = ordered.map(x => (rate(x) ? Math.max(...Object.values(series(S.row, x.i)), 0) : max));
  const hl = ys.indexOf(tl.year);
  heatmap(c.svg, {
    rows: ordered.map(x => x.name), cols: ys, rowMax, max, totalRows, hlCol: hl >= 0 ? hl : null, showPct: false,
    get: (i, j) => { const v = series(S.row, ordered[i].i)[ys[j]]; return v == null ? null : { v, p: null }; },
    fmt: v => (Number.isInteger(v) ? fmtN(v) : fmt1(v)), onCol: j => tl.gotoYear(ys[j]),
  });
  const bn = brkName(S.brk);
  c.set({ title: `${S.fam.title}: ${rowName(S.row)}`, sub: `every category${bn && bn !== 'Total' ? `, ${bn.toLowerCase()}` : bn === 'Total' && S.fam.brks.some(x => x && x !== 'Total') ? ', all' : ''} · ${geoLabel()} · totals at the foot, in grey, off the colour scale`, note: 'Stronger red is a larger number (darker on a light page, brighter on a dark one); rates and percentages are coloured on their own range. Click a year to move the timeline there.' });
  c.setLegend([{ label: 'smaller', color: 'var(--heat-1)' }, { label: 'larger', color: 'var(--heat-7)' }, { label: 'total', color: 'var(--surface-3)' }]);
}

/* ------------------------------------------------------- search and hash */

function bindSearch() {
  const ov = $('#search-overlay'), inp = $('#search'), res = $('#search-results');
  const open = () => { ov.hidden = false; inp.value = ''; list(''); inp.focus(); };
  const close = () => { ov.hidden = true; };
  const list = qv => {
    const words = qv.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = S.index.families.filter(f => words.every(w => `${f.title} ${f.topic} ${(f.also || []).join(' ')}`.toLowerCase().includes(w))).slice(0, 80);
    const by = {};
    for (const f of hits) (by[f.pub] ||= []).push(f);
    res.innerHTML = Object.entries(by).map(([pub, l]) => `<div class="grp">${esc(S.index.reports[pub])}</div>` + l.map(f =>
      `<button type="button" data-p="${f.pub}" data-k="${f.id}">${icon('table')}<span>${esc(f.title)}<br><small style="color:var(--ink-muted)">${esc(f.topic)} · ${esc(GEO_LABEL[f.geo] ?? '')}</small></span><span class="yr">${f.y0}–${f.y1}</span></button>`).join('')).join('') || '<div class="empty">No table matches.</div>';
  };
  $('#search-open').addEventListener('click', open);
  $('#search-close').addEventListener('click', close);
  ov.addEventListener('click', e => { if (e.target === ov) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !ov.hidden) close(); if (e.key === '/' && ov.hidden && document.activeElement?.tagName !== 'INPUT') { e.preventDefault(); open(); } });
  inp.addEventListener('input', () => list(inp.value));
  res.addEventListener('click', e => {
    const b = e.target.closest('button[data-k]');
    if (!b) return;
    close();
    const f = S.index.families.find(x => x.id === b.dataset.k && x.pub === b.dataset.p);
    S.pub = f.pub; ui.pub.set(f.pub); S.topic = f.topic;
    pickTopic(f.id);
  });
}

function writeHash() {
  if (!S.fam) return;
  history.replaceState(null, '', `#${new URLSearchParams({ r: S.pub, t: S.id, c: String(S.cat), b: String(S.brk), p: String(S.row), y: String(tl.year ?? ''), ...(S.perLakh ? { k: 'l' } : {}) })}`);
}

async function boot() {
  initTheme(refresh);
  $('#foot').innerHTML = footerHtml({ extra: '<li>Explore joins a table across editions by its title and its columns by their headings, including across NCRB\'s redesigns (most Crime in India tables were renamed in 2014, many Prison Statistics tables in 2016). Where NCRB split or merged categories, figures before and after are not comparable, and a category may start or stop part-way. District-wise tables are on the Tables page.</li>' });
  S.index = await getJSON(`${DATA}/index.json`);
  try { POP = (await getJSON(`${DATA}/population.json`)).places || {}; } catch { POP = {}; }
  buildControls();
  buildCards();
  bindSearch();
  const h = new URLSearchParams(location.hash.slice(1));
  if (h.get('r') && S.index.reports[h.get('r')]) S.pub = h.get('r');
  S.perLakh = h.get('k') === 'l';
  ui.pub.set(S.pub);
  const f = h.get('t') && S.index.families.find(x => x.id === h.get('t') && x.pub === S.pub);
  if (f) S.want = { c: h.get('c') != null ? Number(h.get('c')) : null, b: h.get('b') != null ? Number(h.get('b')) : null, p: h.get('p') != null ? Number(h.get('p')) : null, y: Number(h.get('y')) || null };
  S.topic = f ? f.topic : topics().find(t => /women|suicide|overcrowd/i.test(t)) || topics()[0];
  pickTopic(f?.id);
}
addEventListener('hashchange', () => location.reload());
boot().catch(e => { console.error(e); $('#cards').innerHTML = `<div class="card"><div class="empty">Could not load: ${esc(e.message)}</div></div>`; });
