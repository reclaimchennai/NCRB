/* Dowry deaths in India: NCRB's figures on dowry deaths (Sec. 304B IPC / Sec. 80 BNS), the Dowry Prohibition Act,
 * victims, the rate per lakh women, police and court disposal, and suicides over dowry disputes.
 *
 * Data: web/data/dowry/dowry.json (analysis/dowry.py): places, and for each measure {place index: [year, value, ...]}.
 * The places picked at the top drive the line charts; the ranking and the map show every State, UT or city.
 */

import { desk, $, el, icon, esc, getJSON, initTheme, debounce, fmtN, fmt1, lerp } from '../kit/util.js?v=7797e2be75';
import { lineChart, barRows, choropleth, emptyChart } from '../kit/grapher.js?v=7797e2be75';
import { segmented, select, entityPicker, Timeline, at, card, bindCapture } from '../kit/cards.js?v=7797e2be75';
import { mapFor, outlineMap, boundaryNote } from '../kit/geo.js?v=7797e2be75';
import { footerHtml } from '../kit/footer.js?v=7797e2be75';
import { mountSearch } from '../kit/search.js?v=7797e2be75';

const TYPE_LABEL = { total: 'India', state: 'States', ut: 'Union Territories', city: 'Cities' };
const SOURCE = 'Data: National Crime Records Bureau, Crime in India and Accidental Deaths & Suicides in India, every edition 1988–2024; female population 1990–2011 from the Census of India (1991, 2001, 2011), a straight line between censuses.';
const M = {
  death_cases: { label: 'Dowry deaths', unit: 'cases', fmt: fmtN },
  death_rate_women: { label: 'Dowry deaths per lakh women', unit: 'per lakh women', fmt: fmt1 },
  death_victims: { label: 'Victims of dowry deaths', unit: 'victims', fmt: fmtN },
  dpa_cases: { label: 'Dowry Prohibition Act cases', unit: 'cases', fmt: fmtN },
  suicides_dowry: { label: 'Suicides over dowry disputes', unit: 'suicides', fmt: fmtN },
  death_cs_rate: { label: 'Charge-sheeting rate, dowry deaths', unit: '% of cases disposed of by police', fmt: fmt1 },
  death_conv_rate: { label: 'Conviction rate, dowry deaths', unit: '% of trials completed', fmt: fmt1 },
  dpa_cs_rate: { label: 'Charge-sheeting rate, Dowry Prohibition Act', unit: '%', fmt: fmt1 },
  dpa_conv_rate: { label: 'Conviction rate, Dowry Prohibition Act', unit: '%', fmt: fmt1 },
};
const S = { D: null, keys: ['Tamil Nadu|state', 'All India|total'], m1: 'death_rate_women', rankM: 'death_rate_women', rankType: 'state', kind: 'death', stRate: 'cs_rate' };
const C = {}, ui = {};
const tl = new Timeline({ speed: 1.2 });

/* ---------------------------------------------------------------- data */
const keyOf = p => `${p.name}|${p.type}`;
let PI = new Map();
function ser(m, key) {
  const a = S.D.data[m]?.[PI.get(key)];
  const o = {};
  if (a) for (let i = 0; i < a.length; i += 2) o[a[i]] = a[i + 1];
  return o;
}
const nameOf = key => key.split('|')[0];
const censusYear = (key, y) => S.D.rateCensus.has(`${PI.get(key)}.${y}`);
function yearsOf(list) {
  const ys = new Set();
  for (const s of list) for (const y of Object.keys(s.values)) ys.add(Number(y));
  const a = [...ys].sort((x, z) => x - z);
  const xs = []; if (a.length) for (let y = a[0]; y <= a.at(-1); y++) xs.push(y);
  return xs;
}
function span(ys) {
  if (!ys.length) return '';
  const out = []; let s = ys[0], p = ys[0];
  for (const y of ys.slice(1).concat(null)) { if (y === p + 1) { p = y; continue; } out.push(s === p ? `${s}` : `${s}–${p}`); s = p = y; }
  return out.join(', ');
}
function gapsOf(list) {
  return list.map(s => { const own = Object.keys(s.values).map(Number).sort((a, b) => a - b); if (!own.length) return ''; const g = []; for (let y = own[0]; y <= own.at(-1); y++) if (!own.includes(y)) g.push(y); return g.length ? `${s.label} ${span(g)}` : ''; }).filter(Boolean);
}
const colour = key => ui.places.colour(key);

/* ------------------------------------------------------------- controls */
function buildControls() {
  const bar = $('#controls');
  const groups = {};
  for (const p of S.D.places) (groups[p.type] ||= []).push(p);
  ui.places = entityPicker({ label: 'Places to compare', max: 10, addLabel: 'Add a place', onChange: v => { S.keys = v; refresh(); } });
  ui.places.options(['total', 'state', 'ut', 'city'].filter(t => groups[t]).map(t => ({ group: TYPE_LABEL[t], options: groups[t].map(p => ({ value: keyOf(p), label: p.name })) })), S.keys);
  const pl = el('div', { class: 'picker-row', style: 'flex:1 1 100%' });
  pl.append(ui.places.el);
  bar.append(pl);
}

/* ---------------------------------------------------------------- cards */
function linesCard(c, measures, { title, sub, note = '', dashCensus = false }) {
  const list = [];
  for (const key of S.keys) {
    for (const m of measures) {
      const v = ser(m, key);
      if (!Object.keys(v).length) continue;
      const label = measures.length > 1 ? `${nameOf(key)}: ${M[m]?.label || m}` : nameOf(key);
      if (dashCensus) {
        // census-based years dashed (and their printed neighbours, so the line joins), NCRB's own solid
        const solid = Object.fromEntries(Object.entries(v).filter(([y]) => !censusYear(key, Number(y))));
        const dash = Object.fromEntries(Object.entries(v).filter(([y]) => { const n = Number(y); return censusYear(key, n) || censusYear(key, n - 1) || censusYear(key, n + 1); }));
        list.push({ key, label, color: colour(key), values: solid });
        if (Object.keys(dash).length) list.push({ key: `${key}-c`, label: '', color: colour(key), dash: '4 4', values: dash });
      } else list.push({ key: `${key}-${m}`, label, color: colour(key), dash: measures.indexOf(m) ? '5 4' : null, values: v });
    }
  }
  const xs = yearsOf(list);
  if (!xs.length) { emptyChart(c.svg, 'None of the places chosen has this figure.'); c.set({ title, sub, note }); return; }
  const fmt = M[measures[0]]?.fmt || fmtN;
  lineChart(c.svg, { xs, series: list, fmt, yFmt: fmt === fmt1 ? fmt1 : undefined });
  c.setLegend(list.filter(s => s.label).map(s => ({ label: s.label, color: s.color, line: true })));
  const g = gapsOf(list.filter(s => s.label));
  c.set({ title, sub, note: (g.length ? `<p>No figure for ${esc(g.join('; '))}.</p>` : '') + note });
}

function buildCards() {
  const root = $('#cards');
  // 1. dowry deaths
  C.deaths = card(root, { id: 'dw-deaths', kicker: 'Dowry deaths' });
  bindCapture(C.deaths, { meta: () => meta(C.deaths), name: 'dowry-deaths' });
  C.m1 = segmented({ label: 'Measure', value: S.m1, options: [{ value: 'death_rate_women', label: 'Per lakh women' }, { value: 'death_cases', label: 'Cases' }, { value: 'death_victims', label: 'Victims (2014–)' }], onChange: v => { S.m1 = v; drawDeaths(); } });
  C.deaths.toolbar.append(C.m1.el);

  // 2. ranking and map
  const g = el('div', { class: 'grid2' });
  root.append(g);
  C.rank = card(g, { id: 'dw-rank', kicker: 'Compare places', rec: true });
  bindCapture(C.rank, { meta: () => meta(C.rank, true), record: { timeline: tl, render: p => drawRank(p) }, name: 'dowry-rank' });
  C.rankM = select({ label: 'Measure', small: 'SHOW', options: Object.entries(M).map(([k, v]) => ({ value: k, label: v.label })), value: S.rankM, onChange: v => { S.rankM = v; syncYears(); drawRank(tl.pos); drawMap(tl.pos); } });
  C.rankT = segmented({ label: 'Places', value: S.rankType, options: [{ value: 'state', label: 'States' }, { value: 'ut', label: 'Union Territories' }, { value: 'city', label: 'Cities' }], onChange: v => { S.rankType = v; syncYears(); drawRank(tl.pos); } });
  C.rank.toolbar.append(C.rankM.el, C.rankT.el);
  C.rank.toolbar.after(tl.root);
  C.map = card(g, { id: 'dw-map', kicker: 'India', rec: true });
  bindCapture(C.map, { meta: () => meta(C.map, true), record: { timeline: tl, render: p => drawMap(p) }, name: 'dowry-map' });
  tl.on(pos => { drawRank(pos); drawMap(pos); });

  // 3. Dowry Prohibition Act
  C.dpa = card(root, { id: 'dw-dpa', kicker: 'Dowry Prohibition Act, 1961' });
  bindCapture(C.dpa, { meta: () => meta(C.dpa), name: 'dowry-prohibition-act' });

  // 4. police and courts, All India
  C.ai = card(root, { id: 'dw-ai', kicker: 'Police and courts · All India' });
  bindCapture(C.ai, { meta: () => meta(C.ai), name: 'dowry-police-courts-india' });
  C.kind = segmented({ label: 'Offence', value: S.kind, options: [{ value: 'death', label: 'Dowry deaths' }, { value: 'dpa', label: 'Dowry Prohibition Act' }], onChange: v => { S.kind = v; drawAI(); } });
  C.ai.toolbar.append(C.kind.el);
  C.aiN = card(root, { id: 'dw-ai-n', kicker: 'Police and courts · All India' });
  bindCapture(C.aiN, { meta: () => meta(C.aiN), name: 'dowry-police-courts-counts' });

  // 5. police and courts by State, 2000-2013
  C.st = card(root, { id: 'dw-st', kicker: 'Police and courts · States' });
  bindCapture(C.st, { meta: () => meta(C.st), name: 'dowry-police-courts-states' });
  C.stR = segmented({ label: 'Rate', value: S.stRate, options: [{ value: 'cs_rate', label: 'Charge-sheeting rate' }, { value: 'conv_rate', label: 'Conviction rate' }], onChange: v => { S.stRate = v; drawStates(); } });
  C.st.toolbar.append(C.stR.el);

  // 6. suicides over dowry disputes
  C.sui = card(root, { id: 'dw-sui', kicker: 'Suicides over dowry disputes' });
  bindCapture(C.sui, { meta: () => meta(C.sui), name: 'dowry-suicides' });

  desk.redraw = refresh;
  let lastW = innerWidth;
  addEventListener('resize', debounce(() => { if (innerWidth !== lastW) { lastW = innerWidth; refresh(); } }, 120));
}
function meta(c, withYear = false) {
  return { kicker: $('.kicker', c.el)?.textContent || 'Dowry', title: $('h2', c.el).textContent, subtitle: $('.titles p', c.el).textContent, year: withYear ? tl.year : null, source: SOURCE, notes: [] };
}

function drawDeaths() {
  const m = S.m1;
  const census = m === 'death_rate_women';
  const cy = S.keys.flatMap(k => Object.keys(ser(m, k)).map(Number).filter(y => censusYear(k, y)));
  linesCard(C.deaths, [m], {
    title: `${M[m].label}: ${S.keys.map(nameOf).join(', ')}`,
    sub: m === 'death_rate_women' ? 'cases registered per lakh women' : m === 'death_cases' ? 'cases registered under Sec. 304B IPC (Sec. 80 BNS from July 2024)' : 'women who died, as NCRB counts victims (printed from 2014)',
    dashCensus: census,
    note: census ? `<p>Per lakh women on the female population NCRB printed (2012 on, and in some years before)${cy.length ? `; dashed: ${span([...new Set(cy)].sort((a, b) => a - b))}, on the Census of India's female population (1991, 2001, 2011), a straight line between censuses` : ''}.</p>` : '',
  });
}

function rankPool() { return S.D.places.filter(p => p.type === S.rankType); }
function syncYears() {
  const ys = new Set();
  for (const p of S.D.places) for (const y of Object.keys(ser(S.rankM, keyOf(p)))) ys.add(Number(y));
  tl.setYears([...ys].sort((a, b) => a - b), true);
}
function drawRank(pos) {
  const c = C.rank, ys = tl.years, m = S.rankM;
  C.rankT.set(S.rankType);
  if (!ys.length) return emptyChart(c.svg);
  const y = ys[Math.round(pos)], i0 = Math.floor(pos), i1 = Math.min(ys.length - 1, i0 + 1), f = pos - i0;
  const pool = rankPool();
  const val = (p, yy) => ser(m, keyOf(p))[yy];
  const ord = yy => new Map(pool.map(p => [keyOf(p), val(p, yy)]).filter(([, v]) => v != null).sort((a, b) => b[1] - a[1]).map(([k], n) => [k, n]));
  const o0 = ord(ys[i0]), o1 = ord(ys[i1]);
  const rows = pool.map(p => {
    const k = keyOf(p), a = val(p, ys[i0]), b = val(p, ys[i1]);
    const v = a != null && b != null ? lerp(a, b, f) : f < .5 ? a : b;
    const r = o0.has(k) && o1.has(k) ? lerp(o0.get(k), o1.get(k), f) : (o0.get(k) ?? o1.get(k));
    const chosen = S.keys.includes(k);
    return { key: k, label: p.name, value: v, rank: r, hl: chosen, color: chosen ? colour(k) : 'var(--other)' };
  }).filter(r => r.value != null && r.rank != null && (r.rank < 36 || r.hl));
  let gmax = 0; for (const p of pool) for (const yy of ys) gmax = Math.max(gmax, val(p, yy) || 0);
  if (!rows.length) emptyChart(c.svg, `No ${S.rankType === 'city' ? 'city' : S.rankType === 'ut' ? 'UT' : 'State'} has this figure for ${y}.`);
  else barRows(c.svg, { rows, max: gmax, fmt: M[m].fmt, bigYear: y });
  c.set({ title: `${M[m].label}: ${S.rankType === 'city' ? 'the big cities' : S.rankType === 'ut' ? 'Union Territories' : 'States'}, ${y}`, sub: `${M[m].unit} · the places chosen above in their colours`, note: S.rankType === 'ut' ? 'A Union Territory has a few lakh people: a handful of cases moves its rate a long way.' : '' });
}
function drawMap(pos) {
  const c = C.map, ys = tl.years, m = S.rankM;
  if (!ys.length) return;
  const y = ys[Math.round(pos)];
  const geo = mapFor(y, () => drawMap(tl.pos)), outline = outlineMap(() => drawMap(tl.pos));
  if (!geo || !outline) return;
  const values = {}, domain = [];
  for (const p of S.D.places.filter(q => q.type === 'state' || q.type === 'ut')) {
    const s = ser(m, keyOf(p));
    const v = at(s, ys, pos);
    if (v != null) values[p.name] = v;
    if (p.type === 'state') for (const yy of ys) if (s[yy] != null) domain.push(s[yy]);
  }
  const hl = S.keys.map(k => k.split('|')).find(([, t]) => t === 'state' || t === 'ut')?.[0] || null;
  choropleth(c.svg, { geo, outline, values, domain, year: y, fmt: M[m].fmt, hl, label: M[m].label });
  c.set({ title: `${M[m].label} by State and UT, ${y}`, sub: `${M[m].unit} · colour scale fixed across ${ys[0]}–${ys.at(-1)}, set from the States`, note: boundaryNote(y) });
}

function drawDPA() {
  linesCard(C.dpa, ['dpa_cases'], { title: `Cases under the Dowry Prohibition Act: ${S.keys.map(nameOf).join(', ')}`, sub: 'cases registered for giving, taking or demanding dowry (the Act of 1961, one series throughout)',
    note: '<p>NCRB counts these under its Special and Local Laws; the State-wise figures begin with the 1989 edition (All India 1988).</p>' });
}

function aiSeries(kind) {
  const ai = 'All India|total';
  const cs = { ...ser(`${kind}_cs_rate`, ai), ...ser(`${kind}_ai_cs_rate`, ai) };
  const conv = { ...ser(`${kind}_conv_rate`, ai), ...ser(`${kind}_ai_conv_rate`, ai) };
  // where no conviction rate is printed: convicted over trials completed (convicted + acquitted), dashed
  const cv = { ...ser(`${kind}_st_convicted`, ai), ...ser(`${kind}_ai_convicted`, ai) }, aq = { ...ser(`${kind}_st_acquitted`, ai), ...ser(`${kind}_ai_acquitted`, ai) }, worked = {};
  for (const y of Object.keys(cv)) if (conv[y] == null && aq[y] != null && cv[y] + aq[y] > 0) worked[y] = Math.round((1000 * cv[y]) / (cv[y] + aq[y])) / 10;
  // the crime-head tables first; the State workbooks' All-India rows (2001-2015) where those are missing
  const both = m => ({ ...ser(`${kind}_st_${m}`, ai), ...ser(`${kind}_ai_${m}`, ai) });
  return { cs, conv, worked, counts: { chargesheeted: both('chargesheeted'), convicted: both('convicted'), acquitted: both('acquitted'), pending_trial: both('pending_trial'), pending_investigation: ser(`${kind}_ai_pending_investigation`, ai) } };
}
function drawAI() {
  const k = S.kind, A = aiSeries(k), what = k === 'death' ? 'dowry deaths' : 'Dowry Prohibition Act cases';
  const wy = Object.keys(A.worked).map(Number);
  const dash = Object.fromEntries(Object.entries({ ...A.worked }).concat(Object.entries(A.conv).filter(([y]) => A.worked[Number(y) - 1] != null || A.worked[Number(y) + 1] != null)));
  const list = [
    { key: 'cs', label: 'Charge-sheeting rate', color: 'var(--series-1)', values: A.cs },
    { key: 'conv', label: 'Conviction rate', color: 'var(--series-2)', values: A.conv },
    ...(wy.length ? [{ key: 'conv-w', label: '', color: 'var(--series-2)', dash: '4 4', values: dash }] : []),
  ];
  const xs = yearsOf(list);
  if (!xs.length) emptyChart(C.ai.svg); else lineChart(C.ai.svg, { xs, series: list, fmt: fmt1, unit: '%', yFmt: v => `${v}%` });
  C.ai.setLegend(list.filter(s => s.label).map(s => ({ label: s.label, color: s.color, line: true })));
  C.ai.set({ title: `Police and courts: ${what}, All India`, sub: 'charge-sheeting rate: % of cases the police disposed of that went to court with a charge-sheet · conviction rate: % of completed trials ending in conviction',
    note: `<p>1990s–2013: NCRB's State-wise tables' All-India totals; from 2014 its crime-head tables.${wy.length ? ` Dashed (${span(wy.sort((a, b) => a - b))}): no rate printed, worked out here as cases convicted over cases convicted or acquitted.` : ''}</p>` });
  const names = { chargesheeted: 'Cases charge-sheeted', convicted: 'Cases convicted', acquitted: 'Cases acquitted or discharged', pending_trial: 'Cases pending trial at the year\'s end', pending_investigation: 'Cases pending investigation at the year\'s end' };
  const cols = { chargesheeted: 'var(--series-1)', convicted: 'var(--series-3)', acquitted: 'var(--series-4)', pending_trial: 'var(--series-2)', pending_investigation: 'var(--series-7)' };
  const l2 = Object.entries(A.counts).filter(([, v]) => Object.keys(v).length).map(([key, v]) => ({ key, label: names[key], color: cols[key], values: v }));
  const x2 = yearsOf(l2);
  if (!x2.length) emptyChart(C.aiN.svg); else lineChart(C.aiN.svg, { xs: x2, series: l2, fmt: fmtN });
  C.aiN.setLegend(l2.map(s => ({ label: s.label, color: s.color, line: true })));
  const g = gapsOf(l2);
  C.aiN.set({ title: `What happened to ${what}, All India`, sub: 'cases each year, from NCRB\'s tables of disposal by the police and by the courts', note: g.length ? `<p>Not printed: ${esc(g.join('; '))}.</p>` : '' });
}

function drawStates() {
  const r = S.stRate;
  // years whose rate is worked out here from NCRB's counts (no rate printed)
  const wk = S.keys.flatMap(k => [...S.D.worked].filter(x => x.startsWith(`death_${r}|${k}|`)).map(x => `${nameOf(k)} ${x.split('|').at(-1)}`));
  linesCard(C.st, [`death_${r}`], { title: `${r === 'cs_rate' ? 'Charge-sheeting' : 'Conviction'} rate, dowry deaths: ${S.keys.map(nameOf).join(', ')}`,
    sub: r === 'cs_rate' ? '% of cases disposed of by the police that went to court with a charge-sheet' : '% of completed trials that ended in conviction',
    note: `<p>NCRB printed the rates State by State for 2000–2013; for 2001–2015 its workbooks also give each State's cases charge-sheeted, sent to final report, convicted and tried, and where no rate was printed it is worked out from those with NCRB's own definitions${wk.length ? ` (here: ${esc(wk.join(', '))})` : ''}. From 2016 NCRB's disposal tables by crime head are for All India only (above).</p>` });
}

function drawSuicides() {
  linesCard(C.sui, ['suicides_dowry'], { title: `Suicides over dowry disputes: ${S.keys.map(nameOf).join(', ')}`, sub: 'suicides recorded with dowry as the cause (both sexes)',
    note: `<p>NCRB (Accidental Deaths &amp; Suicides in India) prints the cause as 'Dowry dispute' up to 2013 and as 'Marriage related issues: dowry related' from 2014.${S.D.suiSum?.length ? ` All India ${span(S.D.suiSum)}: the States and UTs added up (no All-India figure printed).` : ''}</p>` });
}

function drawTiles() {
  const k = S.keys[0];
  const last = (m) => { const s = ser(m, k); const ys = Object.keys(s).map(Number).sort((a, b) => a - b); return ys.length ? { y: ys.at(-1), v: s[ys.at(-1)], p: s[ys.at(-2)], py: ys.at(-2) } : null; };
  const t = [['death_cases', 'Dowry deaths', 'trend-up'], ['death_rate_women', 'Per lakh women', 'users'], ['dpa_cases', 'Dowry Prohibition Act', 'book'], ['suicides_dowry', 'Suicides over dowry', 'heart']].map(([m, lab, ic]) => {
    const x = last(m);
    return { k: lab, i: ic, v: x ? M[m].fmt(x.v) : '–', d: x ? `${nameOf(k)}, ${x.y}${x.p ? ` · ${x.v >= x.p ? '+' : ''}${(((x.v - x.p) / x.p) * 100).toFixed(0)}% on ${x.py}` : ''}` : `${nameOf(k)}: not printed` };
  });
  $('#tiles').innerHTML = t.map(x => `<div class="tile"><div class="k">${icon(x.i)}<span>${esc(x.k)}</span></div><div class="v">${x.v}</div><div class="d">${esc(x.d)}</div></div>`).join('');
}

function refresh() {
  if (!S.D) return;
  writeHash();
  drawTiles(); drawDeaths(); drawRank(tl.pos); drawMap(tl.pos); drawDPA(); drawAI(); drawStates(); drawSuicides();
}
function writeHash() {
  history.replaceState(null, '', `#${new URLSearchParams({ p: S.keys.join(','), m: S.m1, r: S.rankM, t: S.rankType })}`);
}

async function boot() {
  mountSearch({ base: '../' });
  initTheme(refresh);
  $('#foot').innerHTML = footerHtml({ extra: '<li>Dowry deaths are cases registered under Section 304B IPC (Section 80 of the Bharatiya Nyaya Sanhita from 1 July 2024; NCRB\'s 2024 figures add the two). Cases are counted by the year they were registered, victims from 2014. The rate per lakh women uses the female population NCRB printed; for years it did not, the Census of India\'s female population (1991, 2001, 2011, a straight line between censuses), drawn dashed.</li>' });
  const D = await getJSON('../data/dowry/dowry.json');
  D.rateCensus = new Set(D.rate_census || []);
  D.worked = new Set(D.worked || []);
  D.suiSum = D.suicides_india_summed || [];
  S.D = D;
  PI = new Map(D.places.map((p, i) => [keyOf(p), i]));
  const h = new URLSearchParams(location.hash.slice(1));
  if (h.get('p')) { const ks = h.get('p').split(',').filter(k => PI.has(k)); if (ks.length) S.keys = ks; }
  if (h.get('m') && M[h.get('m')]) S.m1 = h.get('m');
  if (h.get('r') && M[h.get('r')]) S.rankM = h.get('r');
  if (['state', 'ut', 'city'].includes(h.get('t'))) S.rankType = h.get('t');
  S.keys = S.keys.filter(k => PI.has(k));
  buildControls();
  buildCards();
  C.m1.set(S.m1); C.rankM.set(S.rankM);
  syncYears();
  refresh();
}
addEventListener('hashchange', () => location.reload());
boot().catch(e => { console.error(e); $('#cards').innerHTML = `<div class="card"><div class="empty">Could not load: ${esc(e.message)}</div></div>`; });
