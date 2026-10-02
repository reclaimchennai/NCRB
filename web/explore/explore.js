/* Explore: every NCRB table printed in three or more editions, joined over the years.
 *
 * Data: web/data/explore/ (analysis/families.py). One family is one table
 * followed across editions; its rows are States/UTs/cities ("places") or its
 * own row labels ("categories"), its columns NCRB's columns, matched by
 * heading. The charts are the same as on the trends page.
 */

import { $, el, icon, esc, getJSON, initTheme, debounce, fmtN, fmt1, SERIES, lerp } from '../kit/util.js?v=fff293a896';
import { lineChart, barRows, heatmap, choropleth, emptyChart } from '../kit/grapher.js?v=fff293a896';
import { segmented, select, toggle, Timeline, at, card, bindCapture } from '../kit/cards.js?v=fff293a896';
import { footerHtml, creditLine } from '../kit/footer.js?v=fff293a896';

const DATA = '../data/explore';
const TYPE_LABEL = { total: 'India', state: 'States', ut: 'Union Territories', city: 'Cities', row: 'Rows' };
const S = { index: null, fam: null, pub: 'cii', topic: null, id: null, col: 0, row: 0, rankType: 'state', compare: true };
const tl = new Timeline({ speed: 1.2 });
const ui = {}, C = {};

/* ------------------------------------------------------------------ data */

const fams = () => S.index.families.filter(f => f.pub === S.pub);
const topics = () => [...new Set(fams().map(f => f.topic))];
const series = (r, c) => {
  const a = S.fam.d[`${r}.${c}`];
  if (!a) return {};
  const o = {};
  for (let i = 0; i < a.length; i += 2) o[a[i]] = a[i + 1];
  return o;
};
const places = () => S.fam.mode === 'places';
const rowName = r => S.fam.rows[r]?.name ?? '';
const colName = c => S.fam.cols[c] ?? '';
const isRate = () => /rate|percent|%|share|ratio|average/i.test(colName(S.col));
const fmtV = v => (isRate() || (v != null && !Number.isInteger(v)) ? fmt1(v) : fmtN(v));
const rowsOfType = types => S.fam.rows.map((r, i) => ({ ...r, i })).filter(r => types.includes(r.type));
function yearsOf(r = S.row, c = S.col) { return Object.keys(series(r, c)).map(Number).sort((a, b) => a - b); }
function allYears() { return S.fam.years; }
const report = () => S.index.reports[S.pub];

function credit(years) {
  return creditLine({ tables: S.fam.sources, year_sources: {} }, years, null, report());
}
function metaFor(c, withYear) {
  return () => ({
    kicker: `${places() && S.fam.rows[S.row]?.type !== 'row' ? `${rowName(S.row)} · ` : ''}${report()}`,
    title: $('h2', c.el).textContent,
    subtitle: $('.titles p', c.el).textContent,
    year: withYear ? tl.year : null,
    source: credit(withYear ? [tl.year] : allYears()),
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
  ui.topic = select({ label: 'Topic', lead: 'layers', options: [], onChange: v => { S.topic = v; pickTopic(); } });
  ui.table = select({ label: 'Table', lead: 'table', options: [], onChange: v => loadFamily(v) });
  ui.col = select({ label: 'Column', small: 'SHOW', options: [], onChange: v => { S.col = Number(v); afterColumn(); } });
  ui.row = select({ label: 'Place or row', lead: 'map-pin', options: [], onChange: v => { S.row = Number(v); refresh(); } });
  const tlWrap = el('div', { class: 'tlbar', style: 'flex:1 1 100%' });
  tl.root.style.padding = '0';
  tlWrap.append(tl.root);
  bar.append(ui.pub.el, ui.topic.el, ui.table.el, ui.col.el, ui.row.el, tlWrap);
  ui.table.el.style.maxWidth = 'min(560px, 100%)';
}

function pickTopic(id = null) {
  ui.topic.options(topics().map(t => ({ value: t, label: t })), S.topic);
  const list = fams().filter(f => f.topic === S.topic);
  ui.table.options(list.map(f => ({ value: f.id, label: `${f.title} (${f.y0}–${f.y1})` })), id || list[0]?.id);
  loadFamily(id || list[0]?.id);
}

async function loadFamily(id) {
  const meta = S.index.families.find(f => f.id === id && f.pub === S.pub);
  if (!meta) return;
  S.id = id;
  S.fam = await getJSON(`${DATA}/${S.pub}/${id}.json`);
  ui.table.set(id);
  // default column: a count (cases, persons, deaths, totals) that is filled in most years, not a share or a rank
  const fill = i => { let n = 0; for (let r = 0; r < S.fam.rows.length; r++) n += Object.keys(series(r, i)).length; return n; };
  const score = (c, i) => fill(i) * (/total|incidence|number|cases|persons|died|deaths|inmates|population|registered|victims/i.test(c) ? 1.5 : 1)
    * (/percent|%|share|rate|rank|ratio|variation|change/i.test(c) ? 0.3 : 1);
  const best = S.fam.cols.map((c, i) => [score(c, i), i]).sort((a, b) => b[0] - a[0])[0]?.[1] ?? 0;
  S.col = S.wantCol != null && S.fam.cols[S.wantCol] ? S.wantCol : best;
  S.wantCol = null;
  ui.col.options(S.fam.cols.map((c, i) => ({ value: i, label: c.length > 90 ? `${c.slice(0, 88)}…` : c })), S.col);
  const groups = {};
  S.fam.rows.forEach((r, i) => (groups[r.type] ||= []).push({ value: i, label: r.name }));
  ui.row.options(['total', 'state', 'ut', 'city', 'row'].filter(t => groups[t]).map(t => ({ group: TYPE_LABEL[t], options: groups[t] })));
  // default row: Tamil Nadu, else All India, else the first
  const want = S.wantRow != null ? S.wantRow : S.fam.rows.findIndex(r => r.name === 'Tamil Nadu');
  S.row = want >= 0 && S.fam.rows[want] ? want : Math.max(0, S.fam.rows.findIndex(r => r.type === 'total'));
  S.wantRow = null;
  ui.row.set(S.row);
  S.rankType = S.fam.rows.some(r => r.type === 'state') ? 'state' : S.fam.rows.some(r => r.type === 'city') ? 'city' : 'row';
  tl.setYears(allYears(), true);
  refresh();
}
function afterColumn() { refresh(); }

/* ----------------------------------------------------------------- cards */

function buildCards() {
  const root = $('#cards');
  C.trend = card(root, { id: 'x-trend', kicker: 'Over the years' });
  bindCapture(C.trend, { meta: metaFor(C.trend, false), name: 'ncrb-explore-trend' });
  C.cmp = toggle({ label: 'Show the largest too', value: S.compare, onChange: v => { S.compare = v; drawTrend(); } });
  C.trend.toolbar.append(C.cmp.el);

  const g = el('div', { class: 'grid2' });
  root.append(g);
  C.rank = card(g, { id: 'x-rank', kicker: 'Compare', rec: true });
  bindCapture(C.rank, { meta: metaFor(C.rank, true), record: { timeline: tl, render: p => drawRank(p) }, name: 'ncrb-explore-compare' });
  C.rankType = segmented({ label: 'Which rows', options: [], onChange: v => { S.rankType = v; drawRank(tl.pos); } });
  C.rank.toolbar.append(C.rankType.el);
  C.map = card(g, { id: 'x-map', kicker: 'India', rec: true });
  bindCapture(C.map, { meta: metaFor(C.map, true), record: { timeline: tl, render: p => drawMap(p) }, name: 'ncrb-explore-map' });
  C.map.set({ note: 'Boundaries: datameet (pre-2019 lines; Ladakh drawn with Jammu & Kashmir; Telangana shaded with Andhra Pradesh before 2014).' });

  C.heat = card(root, { id: 'x-heat', kicker: 'Every column, every year' });
  bindCapture(C.heat, { meta: metaFor(C.heat, false), name: 'ncrb-explore-table' });
  tl.on(pos => { drawRank(pos); drawMap(pos); markTrend(pos); });
  tl.on((pos, settled) => { if (settled) { drawHeat(); writeHash(); } });
  let lastW = innerWidth;
  addEventListener('resize', debounce(() => { if (innerWidth !== lastW) { lastW = innerWidth; refresh(); } }, 120));
}

function refresh() {
  if (!S.fam) return;
  writeHash();
  drawTiles();
  drawTrend();
  drawRank(tl.pos);
  drawMap(tl.pos);
  drawHeat();
}

function drawTiles() {
  const ys = yearsOf();
  const s = series(S.row, S.col);
  const last = ys.at(-1), prev = ys.at(-2);
  const v = s[last], p = s[prev];
  const t = [
    { k: colName(S.col).split('|').pop().slice(0, 40) || 'Value', i: 'hash', v: v == null ? '–' : fmtV(v), d: `${rowName(S.row)}, ${last ?? '–'}` },
    { k: 'Change', i: 'trend-up', v: v != null && p ? `${v >= p ? '+' : ''}${(((v - p) / p) * 100).toFixed(1)}%` : '–', d: prev ? `against ${prev}` : '' },
    { k: 'Years', i: 'calendar', v: String(S.fam.years.length), d: `${S.fam.years[0]}–${S.fam.years.at(-1)}` },
    { k: places() ? 'Places' : 'Rows', i: places() ? 'map-pin' : 'table', v: String(S.fam.rows.length), d: `${S.fam.cols.length} columns` },
  ];
  $('#tiles').innerHTML = t.map(x => `<div class="tile"><div class="k">${icon(x.i)}<span>${esc(x.k)}</span></div><div class="v">${x.v}</div><div class="d">${esc(x.d)}</div></div>`).join('');
}

/* 1. over the years */
let trendArgs = null;
function drawTrend() {
  const c = C.trend, ys = allYears();
  const xs = []; for (let y = ys[0]; y <= ys.at(-1); y++) xs.push(y);
  const list = [{ key: 'sel', label: rowName(S.row), color: 'var(--critical)', values: series(S.row, S.col) }];
  if (S.compare) {
    const type = S.fam.rows[S.row]?.type;
    const pool = rowsOfType(type === 'total' ? ['state', 'ut'] : type === 'ut' ? ['state', 'ut'] : [type]).filter(r => r.i !== S.row);
    const lastY = ys.at(-1);
    const big = pool.map(r => ({ r, v: series(r.i, S.col)[lastY] ?? -1 })).sort((a, b) => b.v - a.v).slice(0, places() ? 5 : 7);
    big.forEach((b, k) => list.push({ key: b.r.i, label: b.r.name, color: SERIES(k), values: series(b.r.i, S.col) }));
  }
  trendArgs = { xs, series: list, fmt: fmtV, yFmt: v => fmtV(v) };
  c.setLegend(list.map(s => ({ label: s.label, color: s.color, line: true })));
  c.set({ title: `${S.fam.title}: ${rowName(S.row)}`, sub: `${colName(S.col)}${S.compare ? ' · with the largest in the latest year' : ''}` });
  const gaps = xs.filter(y => !yearsOf().includes(y));
  c.set({ note: gaps.length ? `No figure for ${rowName(S.row)} in ${span(gaps)}: the table was not printed, the column was not in it, or a scanned year did not add up to its printed totals.` : '' });
  markTrend(tl.pos);
}
function markTrend(pos) {
  if (!trendArgs) return;
  const ys = allYears(), xs = trendArgs.xs;
  const i0 = Math.floor(pos), f = pos - i0;
  const yr = lerp(ys[i0], ys[Math.min(ys.length - 1, i0 + 1)], f);
  lineChart(C.trend.svg, { ...trendArgs, pos: xs.indexOf(Math.floor(yr)) + (yr - Math.floor(yr)), zeroBase: !isRate() || true });
}
function span(ys) {
  const out = []; let s = ys[0], p = ys[0];
  for (const y of ys.slice(1).concat(null)) { if (y === p + 1) { p = y; continue; } out.push(s === p ? `${s}` : `${s}–${p}`); s = p = y; }
  return out.join(', ');
}

/* 2. compare */
function drawRank(pos) {
  const c = C.rank, ys = allYears();
  const types = [...new Set(S.fam.rows.map(r => r.type))];
  const opts = [];
  if (types.includes('state') || types.includes('ut')) opts.push({ value: 'state', label: 'States & UTs', icon: 'map-pin' });
  if (types.includes('city')) opts.push({ value: 'city', label: 'Cities', icon: 'building' });
  if (types.includes('row')) opts.push({ value: 'row', label: 'Rows', icon: 'table' });
  if (!opts.some(o => o.value === S.rankType)) S.rankType = opts[0]?.value;
  C.rankType.options(opts, S.rankType);
  C.rankType.el.hidden = opts.length < 2;
  const pool = rowsOfType(S.rankType === 'state' ? ['state', 'ut'] : [S.rankType]);
  const y = ys[Math.round(pos)];
  const i0 = Math.floor(pos), i1 = Math.min(ys.length - 1, i0 + 1), f = pos - i0;
  const val = (r, yy) => series(r.i, S.col)[yy];
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
  c.set({ title: `${colName(S.col).split('|').pop()}, ${y}`, sub: `${S.fam.title} · ${S.rankType === 'row' ? 'every row' : S.rankType === 'city' ? 'the cities' : 'States and UTs'}${pool.length > limit ? `, largest ${limit}` : ''}` });
}

/* 3. map */
let GEO = null;
function drawMap(pos) {
  const c = C.map;
  const st = rowsOfType(['state', 'ut']);
  if (!places() || st.length < 10) { c.el.hidden = true; return; }
  c.el.hidden = false;
  if (!GEO) { GEO = Promise.all([getJSON('../geo/india-states.geojson'), getJSON('../geo/india-outline.geojson')]).then(g => { GEO = g; drawMap(tl.pos); }); return; }
  if (GEO instanceof Promise) return;
  const ys = allYears(), y = ys[Math.round(pos)];
  const values = {};
  let gmax = 0;
  for (const r of st) {
    const s = series(r.i, S.col);
    const v = at(s, ys, pos);
    if (v != null) values[r.name] = v;
    for (const yy of ys) gmax = Math.max(gmax, s[yy] || 0);
  }
  choropleth(c.svg, { geo: GEO[0], outline: GEO[1], values, max: gmax, year: y, fmt: fmtV, hl: S.fam.rows[S.row]?.type === 'state' || S.fam.rows[S.row]?.type === 'ut' ? rowName(S.row) : null, label: colName(S.col).split('|').pop() });
  c.set({ title: `${colName(S.col).split('|').pop()} by State and UT, ${y}`, sub: `${S.fam.title} · colour scale fixed across ${ys[0]}–${ys.at(-1)}` });
}

/* 4. every column */
function drawHeat() {
  const c = C.heat, ys = allYears();
  const cols = S.fam.cols.map((name, i) => ({ name, i })).filter(x => Object.keys(series(S.row, x.i)).length);
  if (!cols.length) { emptyChart(c.svg); return; }
  const rowMax = cols.map(x => Math.max(...Object.values(series(S.row, x.i)), 0));
  heatmap(c.svg, {
    rows: cols.map(x => x.name.replace(/\s*\|\s*/g, ' · ')), cols: ys, rowMax, max: 1, hlCol: tl.index, showPct: false,
    get: (i, j) => { const v = series(S.row, cols[i].i)[ys[j]]; return v == null ? null : { v, p: null }; },
    fmt: v => (Number.isInteger(v) ? fmtN(v) : fmt1(v)), onCol: j => tl.goto(j),
  });
  c.set({ title: `${S.fam.title}: ${rowName(S.row)}, every column`, sub: 'each row coloured on its own range, darker = larger · click a year to move the timeline' });
  c.setLegend([{ label: 'smaller', color: 'var(--heat-1)' }, { label: 'larger', color: 'var(--heat-7)' }]);
}

/* ------------------------------------------------------- search and hash */

function bindSearch() {
  const ov = $('#search-overlay'), inp = $('#search'), res = $('#search-results');
  const open = () => { ov.hidden = false; inp.value = ''; list(''); inp.focus(); };
  const close = () => { ov.hidden = true; };
  const list = qv => {
    const words = qv.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = S.index.families.filter(f => words.every(w => `${f.title} ${f.topic}`.toLowerCase().includes(w))).slice(0, 80);
    const by = {};
    for (const f of hits) (by[f.pub] ||= []).push(f);
    res.innerHTML = Object.entries(by).map(([pub, l]) => `<div class="grp">${esc(S.index.reports[pub])}</div>` + l.map(f =>
      `<button type="button" data-p="${f.pub}" data-k="${f.id}">${icon('table')}<span>${esc(f.title)}<br><small style="color:var(--ink-muted)">${esc(f.topic)}</small></span><span class="yr">${f.y0}–${f.y1}</span></button>`).join('')).join('') || '<div class="empty">No table matches.</div>';
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
  history.replaceState(null, '', `#${new URLSearchParams({ r: S.pub, t: S.id, c: String(S.col), p: String(S.row), y: String(tl.year ?? '') })}`);
}

async function boot() {
  initTheme(refresh);
  $('#foot').innerHTML = footerHtml({ extra: '<li>Explore joins a table across editions by its title, ignoring years, numbering and small rewordings, and its columns by their headings. Where NCRB changed a table\'s columns, a column may start or stop part-way; where it split or merged categories, figures before and after are not comparable. District-wise tables are not included here; they are on the Tables page.</li>' });
  S.index = await getJSON(`${DATA}/index.json`);
  buildControls();
  buildCards();
  bindSearch();
  const h = new URLSearchParams(location.hash.slice(1));
  if (h.get('r') && S.index.reports[h.get('r')]) S.pub = h.get('r');
  ui.pub.set(S.pub);
  const f = h.get('t') && S.index.families.find(x => x.id === h.get('t') && x.pub === S.pub);
  if (h.get('c')) S.wantCol = Number(h.get('c'));
  if (h.get('p')) S.wantRow = Number(h.get('p'));
  S.topic = f ? f.topic : topics().find(t => /murder|crime against women|suicide|inmate/i.test(t)) || topics()[0];
  pickTopic(f?.id);
  if (h.get('y')) setTimeout(() => tl.gotoYear(Number(h.get('y')), false), 300);
}
addEventListener('hashchange', () => location.reload());
boot().catch(e => { console.error(e); $('#cards').innerHTML = `<div class="card"><div class="empty">Could not load: ${esc(e.message)}</div></div>`; });
