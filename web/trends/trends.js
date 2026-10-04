/* The trends dashboard: one dataset, one place, every year.
 *
 * Data comes from web/data/trends/ (built by analysis/export.py): a catalog,
 * one index per dataset (places, categories, every place's headline series)
 * and one file per place with its full breakdown by category, sex, age and
 * group. Every card redraws from the same selection; the timeline in the
 * control bar drives the year-by-year cards and plays them through.
 */

import { $, el, icon, esc, getJSON, initTheme, debounce, fmtN, fmt1, fmtPct, SERIES, lerp } from '../kit/util.js?v=77a1ee7583';
import { lineChart, barRows, stackRows, heatmap, clocks, seasonChart, choropleth, emptyChart } from '../kit/grapher.js?v=77a1ee7583';
import { segmented, select, Timeline, at, card, bindCapture } from '../kit/cards.js?v=77a1ee7583';
import { notesFor } from '../kit/notes.js?v=77a1ee7583';
import { mapFor, outlineMap, boundaryNote } from '../kit/geo.js?v=77a1ee7583';
import { footerHtml, creditLine } from '../kit/footer.js?v=77a1ee7583';

const DATA = '../data/trends';
const GROUPS = [
  { group: 'Traffic crashes', ids: ['traffic_time', 'traffic_month'] },
  { group: 'Persons killed in traffic crashes', ids: ['road_deaths_time', 'road_deaths_month'] },
  { group: 'Suicides', ids: ['suicide_means', 'suicide_profession', 'suicide_causes', 'suicide_education', 'suicide_sex_age', 'suicide_rate'] },
];
const SEX_LABEL = { Total: 'Both sexes', Male: 'Male', Female: 'Female', Transgender: 'Transgender', '': '' };
const TYPE_LABEL = { total: 'India', state: 'States', ut: 'Union Territories', city: 'Cities' };
const AGE_LABEL = a => (a === 'all ages' ? 'All ages' : a === '60+' ? '60 and over' : `${a} years`);
const SLOT_TXT = { '00-03': '00–03', '03-06': '03–06', '06-09': '06–09', '09-12': '09–12', '12-15': '12–15', '15-18': '15–18', '18-21': '18–21', '21-24': '21–24' };

const S = {
  catalog: null, meta: null, place: null, index: new Map(),
  ds: 'traffic_time', key: null, sex: 0, age: 0, group: 0, mode: 'count',
  rankType: 'state', rankCat: 'all', ghost: false,
};
const tl = new Timeline({ speed: 1.2 });
const C = {};          // cards
const ui = {};         // controls

/* --------------------------------------------------------------- the data */

const kind = () => (/_time$/.test(S.ds) ? 'time' : /_month$/.test(S.ds) ? 'month' : S.ds === 'suicide_rate' ? 'rate' : S.ds === 'suicide_sex_age' ? 'sexage' : 'cats');
const unit = () => S.meta?.unit || '';
const metaPlace = key => S.meta.places.find(p => p.key === key);

function indexRows(rows) {
  const m = new Map();
  for (const [y, g, c, s, a, v] of rows) {
    const k = `${g}|${c}|${s}|${a}`;
    let o = m.get(k);
    if (!o) m.set(k, (o = {}));
    o[y] = v;
  }
  return m;
}
/** {year: v} for a category under the current sex, age and group. */
const series = (ci, { sex = S.sex, age = S.age, group = S.group } = {}) => S.index.get(`${group}|${ci}|${sex}|${age}`) || {};
const allAgesIdx = () => Math.max(0, S.meta.ages.indexOf('all ages'));

/** The categories to draw: everything except a dataset's own 'all ages' total row. */
function cats() {
  return S.meta.cats.map((label, ci) => ({ ci, label })).filter(c => !(kind() === 'sexage' && c.label === 'all ages'));
}
function yearTotal(y, opts) {
  if (kind() === 'sexage') {
    const t = series(S.meta.cats.indexOf('all ages'), opts)[y];
    if (t != null) return t;
  }
  let s = 0, any = false;
  for (const c of cats()) { const v = series(c.ci, opts)[y]; if (v != null) { s += v; any = true; } }
  return any ? s : null;
}
/** Categories in a fixed order (largest first over the whole history), so a colour follows its category. */
function ordered() {
  const tot = c => Object.values(series(c.ci)).reduce((a, b) => a + b, 0);
  const list = cats().map(c => ({ ...c, tot: tot(c) })).filter(c => c.tot > 0);
  if (kind() === 'time' || kind() === 'month' || kind() === 'sexage') return list;   // natural order
  return list.sort((a, b) => b.tot - a.tot);
}
const colorOf = (k, n) => (k < 8 ? SERIES(k) : 'var(--other)');
function label(c) {
  if (kind() === 'time') return `${SLOT_TXT[c.label] || c.label} h`;
  if (kind() === 'sexage') return AGE_LABEL(c.label);
  return c.label;
}
function placeYears() {
  const ys = new Set();
  for (const c of cats()) for (const y of Object.keys(series(c.ci))) ys.add(Number(y));
  return [...ys].sort((a, b) => a - b);
}
const placeName = () => (S.place ? S.place.place : '');
function selectionText({ year = false } = {}) {
  const bits = [];
  if (S.meta.groups.length > 1 && S.meta.groups[S.group]) bits.push(S.meta.groups[S.group] === 'Total traffic' ? 'all traffic' : `${S.meta.groups[S.group].toLowerCase()} crashes`);
  if (S.meta.sexes.length > 1) bits.push(SEX_LABEL[S.meta.sexes[S.sex]].toLowerCase());
  if (S.meta.ages.length > 1 && S.meta.ages[S.age] !== 'all ages') bits.push(`aged ${S.meta.ages[S.age]}`);
  if (year) bits.push(String(tl.year));
  return bits.join(', ');
}
/** What a saved frame says about itself; the credit names the tables and sources behind exactly what it shows. */
function captureMeta(c, withYear, scope = 'place') {
  return () => ({
    kicker: `${scope === 'place' ? `${placeName()} · ` : ''}${S.meta.title}`,
    title: c.el.querySelector('h2').textContent,
    subtitle: c.el.querySelector('.titles p').textContent,
    year: withYear ? tl.year : null,
    source: creditLine(S.meta, withYear ? [tl.year] : placeYears(), scope === 'place' ? S.place.sources : null),
    notes: c === C.trend && !trendArgs?.season ? trendNotes.map(n => `(${n.n}) ${n.year}: ${n.text}`) : [],
  });
}

/* --------------------------------------------------------------- controls */

function buildControls() {
  const bar = $('#controls');
  const byId = Object.fromEntries(S.catalog.datasets.map(d => [d.id, d]));
  ui.ds = select({
    label: 'Dataset', lead: 'layers',
    options: GROUPS.map(g => ({ group: g.group, options: g.ids.filter(id => byId[id]).map(id => ({ value: id, label: `${byId[id].title.replace(/^Persons killed in traffic crashes/, 'Deaths')} (${byId[id].years.join('–')})` })) })),
    value: S.ds, onChange: v => loadDataset(v),
  });
  ui.place = select({ label: 'Place', lead: 'map-pin', options: [], onChange: v => loadPlace(v) });
  ui.sex = segmented({ label: 'Sex', options: [], onChange: v => { S.sex = Number(v); refresh(); } });
  ui.age = select({ label: 'Age group', small: 'AGE', options: [], onChange: v => { S.age = Number(v); refresh(); } });
  ui.group = segmented({ label: 'Kind of crash', options: [], onChange: v => { S.group = Number(v); refresh(); } });
  ui.mode = segmented({
    label: 'Number or share', value: S.mode,
    options: [{ value: 'count', label: 'Number', icon: 'hash' }, { value: 'share', label: 'Share', icon: 'percent' }],
    onChange: v => { S.mode = v; refresh(); },
  });
  bar.append(ui.ds.el, ui.place.el, ui.sex.el, ui.age.el, ui.group.el, ui.mode.el);
  const tlWrap = el('div', { class: 'tlbar', style: 'flex:1 1 100%' });
  tl.root.style.padding = '0';
  tlWrap.append(tl.root);
  bar.append(tlWrap);
}

function syncControls() {
  const m = S.meta;
  const groups = {};
  for (const p of m.places) (groups[p.type] ||= []).push(p);
  ui.place.options(['total', 'state', 'ut', 'city'].filter(t => groups[t]).map(t => ({
    group: TYPE_LABEL[t], options: groups[t].map(p => ({ value: p.key, label: `${p.name}` })),
  })), S.key);
  ui.sex.options(m.sexes.map((s, i) => ({ value: i, label: SEX_LABEL[s] })), S.sex);
  ui.sex.el.hidden = m.sexes.length < 2;
  ui.age.options(m.ages.map((a, i) => ({ value: i, label: AGE_LABEL(a) })), S.age);
  ui.age.el.hidden = m.ages.length < 2;
  ui.group.options(m.groups.map((g, i) => ({ value: i, label: g === 'Total traffic' ? 'All traffic' : g })), S.group);
  ui.group.el.hidden = m.groups.length < 2;
  ui.mode.el.hidden = kind() === 'rate';
}

/* ------------------------------------------------------------ loading */

async function loadDataset(id) {
  S.ds = id;
  S.meta = await getJSON(`${DATA}/${id}/index.json`);
  S.sex = 0; S.group = 0; S.age = allAgesIdx(); S.rankCat = 'all';
  const want = S.key && S.meta.places.some(p => p.key === S.key) ? S.key
    : (S.meta.places.find(p => p.key === 'state-tamil-nadu') || S.meta.places.find(p => p.type === 'state') || S.meta.places[0]).key;
  await loadPlace(want, false);
}

async function loadPlace(key, keepYear = true) {
  S.key = key;
  S.place = await getJSON(`${DATA}/${S.ds}/${key}.json`);
  S.index = indexRows(S.place.rows);
  const mp = metaPlace(key);
  if (mp && mp.type !== 'total') S.rankType = mp.type === 'city' ? 'city' : 'state';
  syncControls();
  tl.setYears(placeYears(), keepYear);
  refresh();
}

/* ---------------------------------------------------------------- cards */

function buildCards() {
  const root = $('#cards');
  C.trend = card(root, { id: 'c-trend', kicker: 'Over the years', snap: true, rec: true });
  bindCapture(C.trend, { meta: () => captureMeta(C.trend, kind() === 'month' && (tl.playing || tl.recording))(), record: { timeline: tl, render: p => markTrend(p) }, name: 'ncrb-trend' });

  C.year = card(root, { id: 'c-year', kicker: 'One year', rec: true });
  bindCapture(C.year, { meta: captureMeta(C.year, true), record: { timeline: tl, render: p => drawYear(p) }, name: 'ncrb-year' });
  C.ghost = el('button', { type: 'button', class: 'switch', role: 'switch', 'aria-checked': 'false' }, `<span class="knob"></span><span>Outline the first year</span>`);
  C.ghost.addEventListener('click', () => { S.ghost = !S.ghost; C.ghost.setAttribute('aria-checked', String(S.ghost)); drawYear(tl.pos); });
  C.year.toolbar.append(C.ghost);

  const g = el('div', { class: 'grid2' });
  root.append(g);
  C.rank = card(g, { id: 'c-rank', kicker: 'Compare places', rec: true });
  bindCapture(C.rank, { meta: captureMeta(C.rank, true, 'all'), record: { timeline: tl, render: p => drawRank(p) }, name: 'ncrb-compare' });
  C.rankType = segmented({ label: 'Places', value: S.rankType, options: [{ value: 'state', label: 'States & UTs', icon: 'map-pin' }, { value: 'city', label: 'Cities', icon: 'building' }], onChange: v => { S.rankType = v; drawRank(tl.pos); } });
  C.rankCat = select({ label: 'Category', small: 'SHOW', options: [], onChange: v => { S.rankCat = v; drawRank(tl.pos); } });
  C.rank.toolbar.append(C.rankType.el, C.rankCat.el);

  C.map = card(g, { id: 'c-map', kicker: 'India', rec: true });
  bindCapture(C.map, { meta: captureMeta(C.map, true, 'all'), record: { timeline: tl, render: p => drawMap(p) }, name: 'ncrb-map' });
  C.map.set({ note: 'The category and the number/share choice follow Compare places. Boundaries: datameet (pre-2019 lines; Ladakh is drawn with Jammu & Kashmir, Telangana is shaded with Andhra Pradesh before 2014).' });

  C.age = card(root, { id: 'c-age', kicker: 'By age group', rec: true });
  bindCapture(C.age, { meta: () => captureMeta(C.age, true, kind() === 'sexage' ? 'all' : 'place')(), record: { timeline: tl, render: p => drawAge(p) }, name: 'ncrb-age' });

  C.heat = card(root, { id: 'c-heat', kicker: 'Every year, every category' });
  bindCapture(C.heat, { meta: captureMeta(C.heat, false), name: 'ncrb-table' });

  let lastW = innerWidth;
  addEventListener('resize', debounce(() => { if (innerWidth !== lastW) { lastW = innerWidth; refresh(true); } }, 120));
}

function refresh(resizeOnly = false) {
  if (!S.meta || !S.place) return;
  if (!resizeOnly) writeHash();
  drawTiles();
  drawTrend();
  drawYear(tl.pos);
  drawRank(tl.pos);
  drawAge(tl.pos);
  drawHeat();
}
tl.on(pos => { drawYear(pos); drawRank(pos); drawAge(pos); drawTilesLight(); markTrend(pos); });

/* tiles */
function drawTiles() {
  const y = tl.year, ys = placeYears();
  const k = ys.indexOf(y);
  const tot = kind() === 'rate' ? series(0)[y] : yearTotal(y);
  const prevY = ys[k - 1];
  const prev = prevY ? (kind() === 'rate' ? series(0)[prevY] : yearTotal(prevY)) : null;
  const top = kind() === 'rate' ? null : ordered().map(c => ({ c, v: series(c.ci)[y] })).filter(x => x.v != null).sort((a, b) => b.v - a.v)[0];
  const tiles = [
    { k: kind() === 'rate' ? 'Suicide rate' : `Total ${unit()}`, i: 'hash', v: tot == null ? '–' : kind() === 'rate' ? fmt1(tot) : fmtN(tot), d: `${placeName()}, ${y}${selectionText() ? ` · ${selectionText()}` : ''}` },
    { k: 'Change', i: 'trend-up', v: tot != null && prev ? fmtPct((100 * (tot - prev)) / prev).replace(/^(?!-)/, '+') : '–', d: prevY ? `against ${prevY}` : 'first year' },
    { k: kind() === 'rate' ? 'Suicides' : 'Largest', i: 'bars', v: kind() === 'rate' ? fmtN(series(1)[y]) : top ? fmtPct((100 * top.v) / tot, 0) : '–', d: kind() === 'rate' ? `population ${fmt1(series(2)[y])} lakh` : top ? label(top.c) : '' },
    { k: 'Years', i: 'calendar', v: `${ys.length}`, d: ys.length ? `${ys[0]}–${ys.at(-1)}${ys.length < ys.at(-1) - ys[0] + 1 ? ', with gaps' : ''}` : '' },
  ];
  $('#tiles').innerHTML = tiles.map(t => `<div class="tile"><div class="k">${icon(t.i)}<span>${t.k}</span></div><div class="v">${t.v}</div><div class="d">${esc(t.d)}</div></div>`).join('');
}
let tilesYear = null;
function drawTilesLight() { if (tl.year !== tilesYear) { tilesYear = tl.year; drawTiles(); } }

/* 1. over the years */
let trendArgs = null, trendNotes = [];
function drawTrend() {
  const c = C.trend, k = kind(), ys = placeYears();
  if (!ys.length) { emptyChart(c.svg); return; }
  const xs = []; for (let y = ys[0]; y <= ys.at(-1); y++) xs.push(y);
  let list = [];
  if (k === 'rate') {
    const india = S.meta.places.find(p => p.key === 'total-all-india');
    const cities = S.meta.places.find(p => p.name === 'Total (Cities)');
    list.push({ key: 'p', label: placeName(), color: 'var(--critical)', values: series(0) });
    if (india && S.key !== india.key) list.push({ key: 'in', label: 'All India', color: 'var(--series-1)', values: india.head[0] || {} });
    if (cities && metaPlace(S.key)?.type === 'city') list.push({ key: 'ci', label: 'All big cities', color: 'var(--series-3)', values: cities.head[0] || {} });
    c.set({ title: `Suicide rate: ${placeName()}`, sub: 'suicides per lakh people, as NCRB printed them' });
  } else if (k === 'month') {
    // one line per year across the months; the year on the timeline in red
    trendArgs = { season: true, ys };
    c.setLegend([{ label: 'the year on the timeline', color: 'var(--critical)', line: true }, { label: 'every other year', color: 'var(--axis)', line: true }]);
    markTrend(tl.pos);
    const gaps = xs.filter(y => !ys.includes(y));
    c.set({ note: gaps.length ? `No figures for ${compact(gaps)}: ${gapReason(gaps)}` : 'Drag the timeline to pick out a year; play or record to watch the years arrive one by one.' });
    return;
  } else {
    const ord = ordered();
    const share = S.mode === 'share';
    const totals = {}; for (const y of ys) totals[y] = yearTotal(y);
    const conv = vals => (share ? Object.fromEntries(Object.entries(vals).filter(([y]) => totals[y]).map(([y, v]) => [y, (100 * v) / totals[y]])) : vals);
    const top = ord.slice(0, k === 'time' || k === 'sexage' ? 8 : 7);
    list = top.map((cat, i) => ({ key: cat.ci, label: label(cat), color: colorOf(i), values: conv(series(cat.ci)) }));
    const rest = ord.slice(top.length);
    if (rest.length) {
      const o = {}; for (const y of ys) { let s = 0, any = false; for (const r of rest) { const v = series(r.ci)[y]; if (v != null) { s += v; any = true; } } if (any) o[y] = s; }
      list.push({ key: 'other', label: 'All other', color: 'var(--other)', values: conv(o) });
    }
    c.set({ title: `${S.meta.title} in ${placeName()}`, sub: `${share ? 'share of each year\'s total, %' : unit()}${selectionText() ? ` · ${selectionText()}` : ''}` });
  }
  c.setLegend(list.map(s => ({ label: s.label, color: s.color, line: true })));
  // annotations from the place's yearly total: known causes (the 2020 lockdown ...) and jumps to check
  const tot = {}; for (const y of ys) { const v = yearTotal(y); if (v) tot[y] = v; }
  trendNotes = notesFor(tot, { place: placeName(), what: `${S.meta.title} ${S.meta.id || ''}`, fmt: fmtN });
  trendArgs = { xs, series: list, unit: k === 'rate' ? '' : S.mode === 'share' && k !== 'month' ? '%' : '', fmt: k === 'rate' || (S.mode === 'share' && k !== 'month') ? fmt1 : fmtN,
                marks: trendNotes.map(n => ({ x: n.year, n: n.n, kind: n.kind, top: true })) };
  markTrend(tl.pos);
  const gaps = xs.filter(y => !ys.includes(y));
  const noteRows = trendNotes.map(n => `<li class="${n.kind}"><span class="nmark">${n.n}</span><b>${n.year}</b> ${esc(n.text)}</li>`).join('');
  c.set({ note: (noteRows ? `<ul class="chart-notes">${noteRows}</ul>` : '') + (gaps.length ? `<p>No figures for ${compact(gaps)}: ${gapReason(gaps)}</p>` : '') });
}
function markTrend(pos) {
  if (!trendArgs) return;
  if (trendArgs.season) {
    const ys = trendArgs.ys, share = S.mode === 'share';
    const tot = Object.fromEntries(ys.map(y => [y, yearTotal(y)]));
    const byLabel = Object.fromEntries(cats().map(c => [c.label, c.ci]));
    const get = (y, m) => { const v = series(byLabel[m])[y]; return v == null ? null : share ? (tot[y] ? (100 * v) / tot[y] : null) : v; };
    seasonChart(C.trend.svg, { cats: cats().map(c => c.label), years: ys, get, pos, reveal: tl.playing || tl.recording, fmt: share ? fmt1 : fmtN, unit: share ? '%' : '' });
    const y = ys[tl.playing || tl.recording ? Math.floor(pos) : Math.round(pos)];
    C.trend.set({ title: `${S.meta.title} in ${placeName()}: each year, month by month`, sub: `${share ? "share of each year's total, %" : unit()}${selectionText() ? ` · ${selectionText()}` : ''} · ${y} in red` });
    return;
  }
  const ys = placeYears(), xs = trendArgs.xs;
  const yr = lerp(ys[Math.floor(pos)] ?? xs[0], ys[Math.min(ys.length - 1, Math.floor(pos) + 1)] ?? xs[0], pos - Math.floor(pos));
  lineChart(C.trend.svg, { ...trendArgs, pos: xs.indexOf(Math.floor(yr)) + (yr - Math.floor(yr)) });
}
function compact(ys) {
  const out = []; let s = ys[0], p = ys[0];
  for (const y of ys.slice(1).concat(null)) { if (y === p + 1) { p = y; continue; } out.push(s === p ? `${s}` : `${s}–${p}`); s = p = y; }
  return out.join(', ');
}
function gapReason(gaps) {
  const k = kind(), t = metaPlace(S.key)?.type;
  if (k === 'sexage' && gaps.some(y => y >= 2016 && y <= 2020)) return 'NCRB printed suicides by age and sex only for all India in 2016–2020.';
  if (t === 'city' && (k === 'cats' || k === 'sexage') && gaps.some(y => y > 2015)) return 'NCRB stopped printing this table city-wise after 2015.';
  return 'not published for this place in those years, or the scanned table did not add up to its printed totals.';
}

/* 2. one year */
function drawYear(pos) {
  const c = C.year, k = kind(), ys = placeYears();
  C.ghost.hidden = k !== 'time';
  if (!ys.length || k === 'rate') { c.el.hidden = k === 'rate'; if (k !== 'rate') emptyChart(c.svg); return; }
  c.el.hidden = false;
  const y = ys[Math.round(pos)];
  const share = S.mode === 'share';
  if (k === 'time') {
    const vals = {}, ghost = {};
    let mx = 0;
    for (const cat of cats()) {
      vals[cat.label] = at(series(cat.ci), ys, pos) ?? 0;
      if (S.ghost) ghost[cat.label] = series(cat.ci)[ys[0]] ?? 0;
    }
    // the radius scale is fixed across all years, so play shows real change
    for (const yy of ys) {
      const t = yearTotal(yy) || 1;
      for (const cat of cats()) { const v = series(cat.ci)[yy] || 0; mx = Math.max(mx, share ? (100 * v) / t : v); }
    }
    clocks(c.svg, { values: vals, ghost: S.ghost ? ghost : null, ghostLabel: `In ${ys[0]}`, max: mx, mode: S.mode, unit: '', year: y });
    c.set({ title: `${S.meta.title.replace(/ by time of day$/, '')} by time of day, ${placeName()}`, sub: `${y}${selectionText() ? ` · ${selectionText()}` : ''} · wedge area shows ${share ? 'share of the day' : unit()}` });
    c.setLegend([{ label: 'Day, 6 am – 6 pm', color: 'var(--day)' }, { label: 'Night, 6 pm – 6 am', color: 'var(--night)' }, ...(S.ghost ? [{ label: `Outline: ${ys[0]}`, color: 'var(--ink-2)' }] : [])]);
    return;
  }
  if (k === 'sexage') {
    const parts = cats().map((cat, i) => ({ key: cat.ci, label: AGE_LABEL(cat.label), color: colorOf(i) }));
    const sexes = S.meta.sexes.map((s, si) => ({ s, si })).filter(x => x.s !== 'Transgender');
    const rows = sexes.map(({ s, si }) => ({ key: s, label: SEX_LABEL[s], values: cats().map(cat => at(series(cat.ci, { sex: si }), ys, pos) ?? 0) }))
      .filter(r => r.values.some(v => v > 0));
    stackRows(c.svg, { rows, parts, mode: share ? 'share' : 'count', bigYear: y });
    c.set({ title: `Suicides by age group, ${placeName()}`, sub: `${y} · ${share ? 'share of each sex\'s suicides' : 'number of suicides'}` });
    c.setLegend(parts.filter((p, i) => rows.some(r => r.values[i] > 0)));
    return;
  }
  // month and category datasets: one bar per category
  const ord = ordered();
  const tot = at(Object.fromEntries(ys.map(yy => [yy, yearTotal(yy)])), ys, pos);
  const i0 = Math.floor(pos), i1 = Math.min(ys.length - 1, i0 + 1), f = pos - i0;
  const rankAt = yy => {
    if (k === 'month') return new Map(ord.map((c2, i) => [c2.ci, i]));
    const arr = ord.map(c2 => ({ ci: c2.ci, v: series(c2.ci)[yy] ?? -1 })).sort((a, b) => b.v - a.v);
    return new Map(arr.map((x, i) => [x.ci, i]));
  };
  const r0 = rankAt(ys[i0]), r1 = rankAt(ys[i1]);
  const rows = ord.map((cat, i) => {
    const v = at(series(cat.ci), ys, pos);
    return { key: cat.ci, label: label(cat), value: v, color: k === 'month' ? 'var(--critical)' : colorOf(i), rank: lerp(r0.get(cat.ci), r1.get(cat.ci), f) };
  }).filter(r => r.value != null);
  const max = Math.max(...ys.flatMap(yy => ord.map(c2 => series(c2.ci)[yy] || 0)), 1);
  barRows(c.svg, { rows, max, total: tot, bigYear: y });
  c.set({ title: `${S.meta.title} in ${placeName()}, ${y}`, sub: `${unit()} and share of the year${selectionText() ? ` · ${selectionText()}` : ''}` });
  c.setLegend([]);
}

/** A place's headline value in a year for the category chosen under Compare places (and its share, in Share mode). */
function headValue(p, yy) {
  const k = kind(), m = S.meta, head = p.head || {};
  const share = S.mode === 'share' && k !== 'rate' && S.rankCat !== 'all';
  if (k === 'rate') return head[S.rankCat]?.[yy] ?? null;
  const sum = () => { let s = 0, any = false; for (const [ci, ser] of Object.entries(head)) { if (k === 'sexage' && m.cats[ci] === 'all ages') continue; const v = ser[yy]; if (v != null) { s += v; any = true; } } return any ? s : null; };
  if (S.rankCat === 'all') return k === 'sexage' ? (head[m.cats.indexOf('all ages')]?.[yy] ?? sum()) : sum();
  const v = head[S.rankCat]?.[yy];
  if (v == null) return null;
  if (!share) return v;
  const t = k === 'sexage' ? head[m.cats.indexOf('all ages')]?.[yy] : sum();
  return t ? (100 * v) / t : null;
}

/* 3. compare places */
function drawRank(pos) {
  const c = C.rank, k = kind(), m = S.meta;
  C.rankType.set(S.rankType);
  const ys = placeYears();
  if (!ys.length) return emptyChart(c.svg);
  const y = ys[Math.round(pos)];
  const i0 = Math.floor(pos), i1 = Math.min(ys.length - 1, i0 + 1), f = pos - i0;
  const y0 = ys[i0], y1 = ys[i1];
  // category list for the selector
  const catOpts = k === 'rate' ? [{ value: '0', label: 'Suicide rate' }, { value: '1', label: 'Number of suicides' }]
    : [{ value: 'all', label: `All ${unit()}` }, ...ordered().map(cat => ({ value: String(cat.ci), label: label(cat) }))];
  if (!catOpts.some(o => o.value === S.rankCat)) S.rankCat = catOpts[0].value;
  C.rankCat.options(catOpts, S.rankCat);
  const types = S.rankType === 'city' ? ['city'] : ['state', 'ut'];
  const places = m.places.filter(p => types.includes(p.type));
  const share = S.mode === 'share' && k !== 'rate' && S.rankCat !== 'all';
  const valueAt = headValue;
  const vals = places.map(p => ({ p, a: valueAt(p, y0), b: valueAt(p, y1) }));
  const order = key => {
    const arr = vals.filter(v => v[key] != null).sort((x, z) => z[key] - x[key]);
    return new Map(arr.map((v, i) => [v.p.key, i]));
  };
  const oa = order('a'), ob = order('b');
  const limit = S.rankType === 'city' ? 25 : 40;
  let rows = vals.map(v => {
    const ra = oa.get(v.p.key), rb = ob.get(v.p.key);
    const value = v.a != null && v.b != null ? lerp(v.a, v.b, f) : f < .5 ? v.a : v.b;
    const rank = ra != null && rb != null ? lerp(ra, rb, f) : ra ?? rb;
    return { key: v.p.key, label: v.p.name, value, rank, hl: v.p.key === S.key, color: v.p.key === S.key ? 'var(--critical)' : 'var(--series-1)' };
  }).filter(r => r.value != null && r.rank != null && (r.rank < limit || r.hl));
  rows.forEach(r => { if (r.hl && r.rank >= limit) r.rank = limit; });
  const max = Math.max(...vals.flatMap(v => [v.a || 0, v.b || 0]), 1);
  // the scale is held across the whole history so bars grow and shrink as the years play
  let gmax = 0;
  for (const p of places) for (const yy of ys) gmax = Math.max(gmax, valueAt(p, yy) || 0);
  drawMap(pos);
  barRows(c.svg, { rows, max: Math.max(max, gmax), fmt: k === 'rate' && S.rankCat === '0' ? fmt1 : share ? fmt1 : fmtN, unit: share ? '%' : '', bigYear: y });
  const what = catOpts.find(o => o.value === S.rankCat)?.label || '';
  c.set({ title: `${what}: ${S.rankType === 'city' ? 'the big cities' : 'States and UTs'}, ${y}`, sub: `${share ? `share of each place's ${unit()}` : k === 'rate' && S.rankCat === '0' ? 'per lakh people' : unit()}${k === 'cats' || k === 'sexage' ? ' · both sexes, all ages' : ''}${m.groups.length > 1 ? ` · ${m.groups[0].toLowerCase()} crashes` : ''} · ${placeName()} highlighted` });
  c.set({ note: rows.length < 3 ? 'Few or no places have this figure for the year.' : '' });
}

/* 3b. India map: the State boundaries of the year shown */
function drawMap(pos) {
  const c = C.map, k = kind(), m = S.meta;
  const places = m.places.filter(p => p.type === 'state' || p.type === 'ut');
  const ys = placeYears();
  if (!places.length || !ys.length) { c.el.hidden = true; return; }
  c.el.hidden = false;
  const y = ys[Math.round(pos)];
  const geo = mapFor(y, () => drawMap(tl.pos)), outline = outlineMap(() => drawMap(tl.pos));
  if (!geo || !outline) return;
  const values = {};
  for (const p of places) {
    const v = at(Object.fromEntries(ys.map(yy => [yy, headValue(p, yy)]).filter(([, v2]) => v2 != null)), ys, pos);
    if (v != null) values[p.name] = v;
  }
  let gmax = 0;
  for (const p of places) for (const yy of ys) gmax = Math.max(gmax, headValue(p, yy) || 0);
  const share = S.mode === 'share' && k !== 'rate' && S.rankCat !== 'all';
  const isRate = k === 'rate' && S.rankCat === '0';
  const mp = metaPlace(S.key);
  choropleth(c.svg, { geo, outline, values, max: gmax, year: y, fmt: isRate || share ? fmt1 : fmtN, unit: share ? '%' : '', hl: mp && mp.type !== 'city' ? mp.name : null, label: C.rankCat.select.selectedOptions[0]?.textContent || '' });
  const what = C.rankCat.select.selectedOptions[0]?.textContent || '';
  c.set({ title: `${what} by State and UT, ${y}`, sub: `${share ? `share of each State's ${unit()}` : isRate ? 'suicides per lakh people' : unit()} · colour scale fixed across ${ys[0]}–${ys.at(-1)}`, note: boundaryNote(y) });
}

/* 4. by age group */
function drawAge(pos) {
  const c = C.age, k = kind(), m = S.meta;
  const ys = placeYears();
  const ages = m.ages.map((a, ai) => ({ a, ai })).filter(x => x.a !== 'all ages');
  if (k === 'sexage') {
    // the age profile of every place of the same kind, the chart that animates best
    c.el.hidden = false;
    const types = S.rankType === 'city' ? ['city'] : ['state', 'ut'];
    const tot = m.cats.indexOf('all ages');
    const parts = cats().map((cat, i) => ({ key: cat.ci, label: AGE_LABEL(cat.label), color: colorOf(i) }));
    const y = ys[Math.round(pos)];
    // top places by suicides in the year shown, with the chosen place always in
    const pl = m.places.filter(p => types.includes(p.type));
    const big = pl.map(p => ({ p, t: p.head[tot]?.[y] ?? 0 })).sort((a, b) => b.t - a.t).slice(0, 12).map(x => x.p);
    if (!big.some(p => p.key === S.key) && metaPlace(S.key)) big.unshift(metaPlace(S.key));
    const rows = big.map(p => ({ key: p.key, label: p.name, hl: p.key === S.key, values: cats().map(cat => at(p.head[cat.ci], ys, pos) ?? 0) }))
      .filter(r => r.values.some(v => v > 0));
    stackRows(c.svg, { rows, parts, mode: 'share', bigYear: y });
    c.set({ kicker: 'Age profile', title: `Age profile of suicides: ${S.rankType === 'city' ? 'the big cities' : 'the largest States'}, ${y}`, sub: 'share of each place\'s suicides by age group · both sexes · use Compare places to switch States and cities' });
    c.setLegend(parts.filter((p, i) => rows.some(r => r.values[i] > 0)));
    c.set({ note: 'The age groups were re-cut in 2014 (15–29 became 14–17 and 18–29), so the bars change shape at 2014 for that reason as well.' });
    return;
  }
  if (k !== 'cats' || ages.length < 2) { c.el.hidden = true; return; }
  const ays = ys.filter(yy => ages.some(({ ai }) => cats().some(cat => series(cat.ci, { age: ai })[yy] != null)));
  if (!ays.length) { c.el.hidden = true; return; }
  c.el.hidden = false;
  const y = ys[Math.round(pos)];
  const has = ays.includes(y);
  const parts = ages.map(({ a, ai }, i) => ({ key: ai, label: AGE_LABEL(a), color: colorOf(i) }));
  const rows = ordered().map(cat => ({ key: cat.ci, label: label(cat), values: ages.map(({ ai }) => at(series(cat.ci, { age: ai }), ys, pos) ?? 0) }))
    .filter(r => r.values.some(v => v > 0));
  if (!rows.length) emptyChart(c.svg, `No age breakdown for ${y}: it is printed for ${compact(ays)}.`);
  else stackRows(c.svg, { rows, parts, mode: S.mode === 'share' ? 'share' : 'count', bigYear: y });
  const why = 'State-wise age breakdowns exist for 2001–2012 (NCRB\'s dataset on data.gov.in) and from 2021; NCRB printed none for States in 2013–2020.';
  c.set({ kicker: 'By age group', title: `${S.meta.title} and age group, ${placeName()}, ${y}`, sub: `${S.mode === 'share' ? 'share of each category by age' : 'number by age group'}${S.meta.sexes.length > 1 ? ` · ${SEX_LABEL[S.meta.sexes[S.sex]].toLowerCase()}` : ''}`, note: has ? `Age groups are printed for ${compact(ays)}. ${why}` : `No age breakdown for ${y}. ${why}` });
  c.setLegend(parts.filter((p, i) => rows.some(r => r.values[i] > 0)));
}

/* 5. every year, every category */
function drawHeat() {
  const c = C.heat, k = kind();
  const ys = placeYears();
  if (k === 'rate' || !ys.length) { c.el.hidden = true; return; }
  c.el.hidden = false;
  const ord = ordered();
  const tots = Object.fromEntries(ys.map(y => [y, yearTotal(y)]));
  let max = 0;
  for (const cat of ord) for (const y of ys) max = Math.max(max, series(cat.ci)[y] || 0);
  heatmap(c.svg, {
    rows: ord.map(label), cols: ys, max, hlCol: tl.index,
    get: (i, j) => { const v = series(ord[i].ci)[ys[j]]; return v == null ? null : { v, p: tots[ys[j]] ? (100 * v) / tots[ys[j]] : null }; },
    onCol: j => tl.goto(j),
  });
  c.set({ title: `${S.meta.title} in ${placeName()}, every year`, sub: `each cell: the number, and its share of that year's total${selectionText() ? ` · ${selectionText()}` : ''}` });
  c.setLegend([{ label: 'fewer', color: 'var(--heat-1)' }, { label: 'more', color: 'var(--heat-7)' }]);
  c.set({ note: 'Stronger red is a larger number (darker on a light page, brighter on a dark one). Click a year to move the timeline there.' });
}
tl.on((pos, settled) => { if (settled) drawHeat(); });

/* ----------------------------------------------------------- search, hash */

function bindSearch() {
  const ov = $('#search-overlay'), inp = $('#search'), res = $('#search-results');
  const open = () => { ov.hidden = false; inp.value = ''; list(''); inp.focus(); };
  const close = () => { ov.hidden = true; };
  const list = q => {
    const ql = q.trim().toLowerCase();
    const groups = {};
    for (const p of S.meta.places) if (!ql || p.name.toLowerCase().includes(ql)) (groups[p.type] ||= []).push(p);
    res.innerHTML = ['total', 'state', 'ut', 'city'].filter(t => groups[t]).map(t => `<div class="grp">${TYPE_LABEL[t]}</div>` + groups[t].map(p =>
      `<button type="button" data-k="${p.key}">${icon(t === 'city' ? 'building' : 'map-pin')}<span>${esc(p.name)}</span><span class="yr">${p.years[0]}–${p.years.at(-1)}</span></button>`).join('')).join('') || '<div class="empty">No place by that name in this dataset.</div>';
  };
  $('#search-open').addEventListener('click', open);
  $('#search-close').addEventListener('click', close);
  ov.addEventListener('click', e => { if (e.target === ov) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !ov.hidden) close(); if (e.key === '/' && ov.hidden && document.activeElement?.tagName !== 'INPUT') { e.preventDefault(); open(); } });
  inp.addEventListener('input', () => list(inp.value));
  res.addEventListener('click', e => { const b = e.target.closest('button[data-k]'); if (b) { close(); loadPlace(b.dataset.k); } });
}

function writeHash() {
  const p = new URLSearchParams({ d: S.ds, p: S.key, y: String(tl.year ?? '') });
  if (S.sex) p.set('s', S.meta.sexes[S.sex]);
  if (S.meta.ages[S.age] && S.meta.ages[S.age] !== 'all ages') p.set('a', S.meta.ages[S.age]);
  if (S.group) p.set('g', String(S.group));
  if (S.mode !== 'count') p.set('m', S.mode);
  history.replaceState(null, '', `#${p}`);
}
function readHash() {
  const p = new URLSearchParams(location.hash.slice(1));
  return { d: p.get('d'), p: p.get('p'), y: Number(p.get('y')) || null, s: p.get('s'), a: p.get('a'), g: Number(p.get('g')) || 0, m: p.get('m') };
}
tl.on((pos, settled) => { if (settled) writeHash(); });

/* ------------------------------------------------------------------- boot */

async function boot() {
  initTheme(() => refresh(true));
  $('#foot').innerHTML = footerHtml();
  S.catalog = await getJSON(`${DATA}/catalog.json`);
  const h = readHash();
  if (h.d && S.catalog.datasets.some(d => d.id === h.d)) S.ds = h.d;
  if (h.p) S.key = h.p;
  if (h.m === 'share') S.mode = 'share';
  buildControls();
  buildCards();
  bindSearch();
  await loadDataset(S.ds);
  ui.ds.set(S.ds);
  let changed = false;
  if (h.s && S.meta.sexes.includes(h.s)) { S.sex = S.meta.sexes.indexOf(h.s); changed = true; }
  if (h.a && S.meta.ages.includes(h.a)) { S.age = S.meta.ages.indexOf(h.a); changed = true; }
  if (h.g && S.meta.groups[h.g]) { S.group = h.g; changed = true; }
  if (changed) { syncControls(); tl.setYears(placeYears()); }
  if (h.y) tl.gotoYear(h.y, false);
  refresh();
}

// a pasted or edited link: start again from it (replaceState, used for our own updates, does not fire this)
addEventListener('hashchange', () => location.reload());

boot().catch(err => {
  console.error(err);
  $('#cards').innerHTML = `<div class="card"><div class="empty">Could not load the data: ${esc(err.message)}</div></div>`;
});
