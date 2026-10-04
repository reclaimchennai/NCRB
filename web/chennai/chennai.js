/* Chennai over time: the report page.
 *
 * The same data and charts as the trends dashboard (web/data/trends, built by
 * analysis/export.py), arranged as a story about Chennai and Tamil Nadu. Every
 * chart that changes with the year has its own timeline: play, scrub, and a
 * video button that records it through the years.
 */

import { $, el, icon, esc, initTheme, debounce, getJSON, fmtN, fmt1, fmtPct, SERIES, lerp } from '../kit/util.js?v=77a1ee7583';
import { lineChart, stackChart, barRows, stackRows, heatmap, clocks, seasonChart, choropleth, emptyChart } from '../kit/grapher.js?v=77a1ee7583';
import { segmented, Timeline, at, card, bindCapture } from '../kit/cards.js?v=77a1ee7583';
import { place, loadIndex, yearsWith } from '../kit/data.js?v=77a1ee7583';
import { mapFor, outlineMap, boundaryNote } from '../kit/geo.js?v=77a1ee7583';
import { footerHtml, SOURCE_LINE, creditLine } from '../kit/footer.js?v=77a1ee7583';

const SLOTS = ['00-03', '03-06', '06-09', '09-12', '12-15', '15-18', '18-21', '21-24'];
const DAY = ['06-09', '09-12', '12-15', '15-18'];
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const AGE_LABEL = a => (a === '60+' ? '60 and over' : `${a}`);
const METROS = ['Chennai', 'Delhi', 'Mumbai', 'Kolkata', 'Bengaluru', 'Hyderabad', 'Ahmedabad', 'Pune'];
const redraws = [];
const root = () => $('#report');

function section(title, prose) {
  root().append(el('h2', { class: 'section-title' }, esc(title)));
  if (prose) root().append(el('div', { class: 'prose' }, prose));
}
function span(ys) {
  if (!ys.length) return '';
  const out = []; let s = ys[0], p = ys[0];
  for (const y of ys.slice(1).concat(null)) { if (y === p + 1) { p = y; continue; } out.push(s === p ? `${s}` : `${s}–${p}`); s = p = y; }
  return out.join(', ');
}
/** A card that follows its own timeline, with play and video. */
function yearCard(parent, { id, kicker, years, render, meta, name, start = 'last' }) {
  const c = card(parent, { id, kicker, rec: true });
  const tl = new Timeline({ years, speed: 1.2 });
  if (start === 'first') tl.set(0, true);
  c.toolbar.after(tl.root);
  tl.on(pos => render(pos));
  bindCapture(c, { meta: () => ({ kicker, title: $('h2', c.el).textContent, subtitle: $('.titles p', c.el).textContent, year: tl.year, source: meta ? meta(tl.year) : SOURCE_LINE }), record: { timeline: tl, render }, name });
  redraws.push(() => render(tl.pos));
  return { c, tl };
}
function plainCard(parent, { id, kicker, render, meta, name }) {
  const c = card(parent, { id, kicker });
  bindCapture(c, { meta: () => ({ kicker, title: $('h2', c.el).textContent, subtitle: $('.titles p', c.el).textContent, source: meta?.() || SOURCE_LINE }), name });
  redraws.push(render);
  return c;
}

/* ================================================================ sections */

async function trafficTime() {
  const P = await place('traffic_time', 'city-chennai');
  const ys = yearsWith(P, { group: 'Road' });
  const day = {}, night = {}, tot = {};
  for (const y of ys) {
    const t = P.total(y, { group: 'Road' });
    tot[y] = t;
    const d = DAY.reduce((a, s) => a + (P.get(s, { group: 'Road' })[y] || 0), 0);
    day[y] = (100 * d) / t; night[y] = 100 - day[y];
  }
  const peak = ys.reduce((a, b) => (tot[b] > tot[a] ? b : a), ys[0]);
  const last = ys.at(-1);
  section('Road crashes in Chennai, by the clock',
    `<p>NCRB counts Chennai's road crashes in eight three-hour slots, every year since ${ys[0]}. Split the way NCRB labels them, day (6 am to 6 pm) and night (6 pm to 6 am) each fill one ordinary clock face. The area of each wedge is the number of crashes in those three hours.</p>
     <p>Road crashes peaked at <b>${fmtN(tot[peak])}</b> in ${peak} and were <b>${fmtN(tot[last])}</b> in ${last}. The night's share was ${fmtPct(night[ys[0]], 0)} in ${ys[0]} and ${fmtPct(night[last], 0)} in ${last}.</p>`);
  let mode = 'count', ghost = false;
  const mx = { count: 0, share: 0 };
  for (const y of ys) for (const s of SLOTS) { const v = P.get(s, { group: 'Road' })[y] || 0; mx.count = Math.max(mx.count, v); mx.share = Math.max(mx.share, (100 * v) / tot[y]); }
  const { c, tl } = yearCard(root(), {
    id: 'chn-clock', kicker: 'Chennai · road crashes by time of day', years: ys, name: 'chennai-clock', meta: y => creditLine(P.meta, [y], P.sources),
    render: pos => {
      const y = ys[Math.round(pos)];
      const vals = Object.fromEntries(SLOTS.map(s => [s, at(P.get(s, { group: 'Road' }), ys, pos) ?? 0]));
      const g = ghost ? Object.fromEntries(SLOTS.map(s => [s, P.get(s, { group: 'Road' })[ys[0]] ?? 0])) : null;
      clocks(c.svg, { values: vals, ghost: g, ghostLabel: `In ${ys[0]}`, max: mx[mode], mode, year: y });
      c.set({ title: `Road crashes in Chennai by time of day, ${y}`, sub: `wedge area shows ${mode === 'share' ? "share of the day's crashes" : 'number of crashes'}${ghost ? ` · dashed outline: ${ys[0]}` : ''}` });
    },
  });
  const seg = segmented({ label: 'Number or share', value: mode, options: [{ value: 'count', label: 'Number', icon: 'hash' }, { value: 'share', label: 'Share of the day', icon: 'percent' }], onChange: v => { mode = v; tl.emit(); } });
  const sw = el('button', { type: 'button', class: 'switch', role: 'switch', 'aria-checked': 'false' }, `<span class="knob"></span><span>Outline ${ys[0]}</span>`);
  sw.addEventListener('click', () => { ghost = !ghost; sw.setAttribute('aria-checked', String(ghost)); tl.emit(); });
  c.toolbar.append(seg.el, sw);
  c.setLegend([{ label: 'Day, 6 am – 6 pm', color: 'var(--day)' }, { label: 'Night, 6 pm – 6 am', color: 'var(--night)' }]);
  const gaps = []; for (let y = ys[0]; y <= last; y++) if (!ys.includes(y)) gaps.push(y);
  c.set({ note: gaps.length ? `No reliable figures for ${span(gaps)}.` : '' });

  const H = {};
  H.card = yearCard(root(), {
    id: 'chn-hour-lines', kicker: 'Chennai · road crashes by time of day', years: ys, name: 'chennai-hour-lines', meta: () => creditLine(P.meta, ys, P.sources),
    render: pos => {
      const tl = H.card?.tl;
      const rev = !!(tl && (tl.playing || tl.recording));
      seasonChart(H.card.c.svg, { cats: SLOTS, years: ys, get: (y, sl) => P.get(sl, { group: 'Road' })[y] ?? null, pos, reveal: rev, xLabel: sl => `${sl.slice(0, 2)}–${sl.slice(3)} h` });
      H.card.c.set({ title: `Road crashes in Chennai, hour by hour: ${ys[rev ? Math.floor(pos) : Math.round(pos)]} against every other year`, sub: 'number of road crashes in each three-hour slot · each grey line is one year' });
    },
  });
  H.card.c.setLegend([{ label: 'the year on the timeline', color: 'var(--critical)', line: true }, { label: 'every other year', color: 'var(--axis)', line: true }]);
  const xs = []; for (let y = ys[0]; y <= last; y++) xs.push(y);
  const c2 = plainCard(root(), {
    id: 'chn-daynight', kicker: 'Chennai · road crashes', name: 'chennai-day-night', meta: () => creditLine(P.meta, ys, P.sources),
    render: () => {
      lineChart(c2.svg, { xs, series: [{ key: 'n', label: 'Night (6 pm – 6 am)', color: 'var(--night)', values: night }, { key: 'd', label: 'Day (6 am – 6 pm)', color: 'var(--day)', values: day }], fmt: fmt1, unit: '%', yFmt: v => `${v}%` });
    },
  });
  c2.set({ title: 'Day and night: share of Chennai\'s road crashes', sub: '% of each year\'s road crashes' });
  c2.setLegend([{ label: 'Night', color: 'var(--night)', line: true }, { label: 'Day', color: 'var(--day)', line: true }]);
  const c3 = plainCard(root(), {
    id: 'chn-total', kicker: 'Chennai · road crashes', name: 'chennai-road-crashes', meta: () => creditLine(P.meta, ys, P.sources),
    render: () => lineChart(c3.svg, { xs, series: [{ key: 't', label: 'Road crashes', color: 'var(--critical)', values: tot }], height: 260 }),
  });
  c3.set({ title: 'Road crashes in Chennai, every year', sub: 'number of road crashes' });
}

async function trafficMonth() {
  const P = await place('traffic_month', 'city-chennai');
  const ys = yearsWith(P, { group: 'Road' });
  const share = {};
  for (const m of MONTHS) share[m] = [];
  for (const y of ys) { const t = P.total(y, { group: 'Road' }); for (const m of MONTHS) { const v = P.get(m, { group: 'Road' })[y]; if (v != null && t) share[m].push((100 * v) / t); } }
  const avg = Object.fromEntries(MONTHS.map(m => [m, share[m].reduce((a, b) => a + b, 0) / (share[m].length || 1)]));
  const hi = MONTHS.reduce((a, b) => (avg[b] > avg[a] ? b : a)), lo = MONTHS.reduce((a, b) => (avg[b] < avg[a] ? b : a));
  section('Month by month', `<p>Month tables for Chennai cover ${span(ys)}. On average ${hi} has had the largest share of the year's road crashes (${fmtPct(avg[hi])}) and ${lo} the smallest (${fmtPct(avg[lo])}); an even spread would be 8.3% a month. Each cell carries the number and its share of the year.</p>`);
  const S = {};
  S.card = yearCard(root(), {
    id: 'chn-month-lines', kicker: 'Chennai · road crashes by month', years: ys, name: 'chennai-month-lines', meta: () => creditLine(P.meta, ys, P.sources),
    render: pos => {
      const tl = S.card?.tl;
      seasonChart(S.card.c.svg, { cats: MONTHS, years: ys, get: (y, m) => P.get(m, { group: 'Road' })[y] ?? null, pos, reveal: !!(tl && (tl.playing || tl.recording)) });
      const y = ys[tl && (tl.playing || tl.recording) ? Math.floor(pos) : Math.round(pos)];
      S.card.c.set({ title: `Road crashes in Chennai, month by month: ${y} against every other year`, sub: 'number of road crashes · each grey line is one year' });
    },
  });
  S.card.c.setLegend([{ label: 'the year on the timeline', color: 'var(--critical)', line: true }, { label: 'every other year', color: 'var(--axis)', line: true }]);
  S.card.c.set({ note: 'Drag the timeline to pick out a year. Play, or record a video, to watch the years arrive one by one: each year draws itself in red, then joins the others in grey.' });
  const c = plainCard(root(), {
    id: 'chn-month', kicker: 'Chennai · road crashes by month', name: 'chennai-month', meta: () => creditLine(P.meta, ys, P.sources),
    render: () => {
      let max = 0; for (const m of MONTHS) for (const y of ys) max = Math.max(max, P.get(m, { group: 'Road' })[y] || 0);
      const tots = Object.fromEntries(ys.map(y => [y, P.total(y, { group: 'Road' })]));
      // years down the side, months across: the shape of a calendar
      heatmap(c.svg, { rows: ys.map(String), cols: MONTHS, max, get: (i, j) => { const v = P.get(MONTHS[j], { group: 'Road' })[ys[i]]; return v == null ? null : { v, p: (100 * v) / tots[ys[i]] }; } });
    },
  });
  c.set({ title: 'Road crashes in Chennai by month', sub: 'number of road crashes, and % of the year' });
  c.setLegend([{ label: 'fewer', color: 'var(--heat-1)' }, { label: 'more', color: 'var(--heat-7)' }]);
}

async function roadDeaths() {
  const P = await place('road_deaths_time', 'state-tamil-nadu');
  const ys = yearsWith(P, { group: 'Road' });
  section('Road deaths in Tamil Nadu by time of day', `<p>Deaths by time of day are printed only State-wise, and only from ${ys[0]}; for Chennai NCRB gives the number of crashes by hour and, separately, a yearly count of persons killed.</p>`);
  const tot = Object.fromEntries(ys.map(y => [y, P.total(y, { group: 'Road' })]));
  let mx = 0; for (const y of ys) for (const s of SLOTS) mx = Math.max(mx, P.get(s, { group: 'Road' })[y] || 0);
  const { c } = yearCard(root(), {
    id: 'tn-deaths', kicker: 'Tamil Nadu · persons killed in road crashes', years: ys, name: 'tn-road-deaths-clock', meta: y => creditLine(P.meta, [y], P.sources),
    render: pos => {
      const y = ys[Math.round(pos)];
      clocks(c.svg, { values: Object.fromEntries(SLOTS.map(s => [s, at(P.get(s, { group: 'Road' }), ys, pos) ?? 0])), max: mx, year: y });
      c.set({ title: `Persons killed in road crashes in Tamil Nadu by time of day, ${y}`, sub: `${fmtN(tot[y])} deaths · wedge area shows deaths` });
    },
  });
  c.setLegend([{ label: 'Day, 6 am – 6 pm', color: 'var(--day)' }, { label: 'Night, 6 pm – 6 am', color: 'var(--night)' }]);
}

async function means() {
  const P = await place('suicide_means', 'state-tamil-nadu');
  const ys = yearsWith(P);
  const order = P.cats.map(c => ({ c, t: ys.reduce((a, y) => a + (P.get(c)[y] || 0), 0) })).sort((a, b) => b.t - a.t).map(x => x.c);
  const top = order.slice(0, 7);
  const shares = c => Object.fromEntries(ys.map(y => [y, P.total(y) ? (100 * (P.get(c)[y] || 0)) / P.total(y) : null]).filter(([, v]) => v != null));
  const first = ys.find(y => y >= 2001) ?? ys[0], last = ys.at(-1);
  const h = shares('Hanging');
  section('Suicides in Tamil Nadu by means', `<p>Hanging was ${fmtPct(h[first], 0)} of suicides in ${first} and ${fmtPct(h[last], 0)} in ${last}. NCRB's names for the means change between editions; they are mapped to one list here.</p>`);
  const xs = []; for (let y = ys[0]; y <= last; y++) xs.push(y);
  // the seven largest means each get a band; the rest are one grey 'All other' band
  const rest = Object.fromEntries(ys.map(y => [y, Math.max(0, 100 - top.reduce((a, c) => a + (shares(c)[y] || 0), 0))]));
  let view = 'stack';
  const c1 = plainCard(root(), {
    id: 'tn-means-lines', kicker: 'Tamil Nadu · suicides by means', name: 'tn-means-share', meta: () => creditLine(P.meta, ys, P.sources),
    render: () => {
      const bands = top.map((c, i) => ({ key: c, label: c, color: SERIES(i), values: shares(c) }));
      if (view === 'stack') stackChart(c1.svg, { xs, series: bands.concat([{ key: 'rest', label: 'All other', color: 'var(--other)', values: rest }]), unit: "% of the year's suicides" });
      else lineChart(c1.svg, { xs, series: bands, fmt: fmt1, unit: '%', yFmt: v => `${v}%` });
      c1.setLegend(top.map((c, i) => ({ label: c, color: SERIES(i), line: view !== 'stack' })).concat(view === 'stack' ? [{ label: 'All other', color: 'var(--other)' }] : []));
    },
  });
  c1.set({ title: 'Means adopted, share of all suicides in Tamil Nadu', sub: `${ys[0]}–${last} · % of each year's suicides, both sexes` });
  const segV = segmented({ label: 'Chart', value: view, options: [{ value: 'stack', label: 'Stacked' }, { value: 'lines', label: 'Lines' }], onChange: v => { view = v; redrawAll(); } });
  c1.toolbar.append(segV.el);
  const missing = []; for (let y = ys[0]; y <= last; y++) if (!ys.includes(y)) missing.push(y);
  c1.set({ note: (missing.length ? `No means-wise figures for Tamil Nadu in ${span(missing)}: for 1992–2000 the appendix with the State-wise means table is not among the files NCRB's site and the Internet Archive give. ` : '')
    + (ys.includes(2009) ? 'In 2009 Tamil Nadu reported every poisoning as insecticides (NCRB printed 4,483 by insecticides and 0 by other poison), so the two poison bands swap that year; together they are in line with the years around it.' : '') });
  const { c } = yearCard(root(), {
    id: 'tn-means-year', kicker: 'Tamil Nadu · suicides by means', years: ys, name: 'tn-means-year', meta: y => creditLine(P.meta, [y], P.sources),
    render: pos => {
      const y = ys[Math.round(pos)];
      const i0 = Math.floor(pos), i1 = Math.min(ys.length - 1, i0 + 1), f = pos - i0;
      const rank = yy => new Map(order.map(cc => [cc, P.get(cc)[yy] ?? -1]).sort((a, b) => b[1] - a[1]).map(([cc], k) => [cc, k]));
      const r0 = rank(ys[i0]), r1 = rank(ys[i1]);
      const rows = order.map((cc, k) => ({ key: cc, label: cc, value: at(P.get(cc), ys, pos), color: k < 8 ? SERIES(k) : 'var(--other)', rank: lerp(r0.get(cc), r1.get(cc), f) })).filter(r => r.value != null);
      const max = Math.max(...ys.flatMap(yy => order.map(cc => P.get(cc)[yy] || 0)));
      barRows(c.svg, { rows, max, total: at(Object.fromEntries(ys.map(yy => [yy, P.total(yy)])), ys, pos), bigYear: y });
      c.set({ title: `Suicides in Tamil Nadu by means, ${y}`, sub: 'number and share of the year, both sexes' });
    },
  });
}

async function profession() {
  const P = await place('suicide_profession', 'state-tamil-nadu');
  const ys = yearsWith(P);
  const order = P.cats.map(c => ({ c, t: ys.reduce((a, y) => a + (P.get(c)[y] || 0), 0) })).filter(x => x.t > 0).sort((a, b) => b.t - a.t).map(x => x.c);
  const ages = P.meta.ages.filter(a => a !== 'all ages');
  const ageYears = yearsWith(P, { age: ages.includes('15-29') ? '15-29' : ages[0] }).concat(yearsWith(P, { age: '18-29' }));
  const ay = [...new Set(ageYears)].sort((a, b) => a - b);
  section('Suicides in Tamil Nadu by profession', `<p>Profession tables run ${span(ys)}. Tables by profession, sex <i>and</i> age exist for ${span(ay)}: up to 2012 from the dataset NCRB gave data.gov.in, from 2021 in NCRB's own State-wise tables. In 2014 NCRB split the 'others' group into new professions (daily wage earners, agricultural labourers…), which is why 'Other / not known' shrinks that year.</p>`);
  let sex = 'Total';
  const c = plainCard(root(), {
    id: 'tn-prof-heat', kicker: 'Tamil Nadu · suicides by profession', name: 'tn-profession-years', meta: () => creditLine(P.meta, ys, P.sources),
    render: () => {
      let max = 0; for (const cc of order) for (const y of ys) max = Math.max(max, P.get(cc, { sex })[y] || 0);
      const tots = Object.fromEntries(ys.map(y => [y, P.total(y, { sex })]));
      heatmap(c.svg, { rows: order, cols: ys, max, get: (i, j) => { const v = P.get(order[i], { sex })[ys[j]]; return v == null ? null : { v, p: tots[ys[j]] ? (100 * v) / tots[ys[j]] : null }; } });
      c.set({ title: `Suicides in Tamil Nadu by profession, ${ys[0]}–${ys.at(-1)}`, sub: `${sex === 'Total' ? 'both sexes' : sex.toLowerCase()} · each cell: the number and its share of the year` });
    },
  });
  const segSex = segmented({ label: 'Sex', value: sex, options: P.meta.sexes.filter(s => s !== 'Transgender').map(s => ({ value: s, label: s === 'Total' ? 'Both sexes' : s })), onChange: v => { sex = v; c.redraw?.(); redrawAll(); } });
  c.toolbar.append(segSex.el);
  c.setLegend([{ label: 'fewer', color: 'var(--heat-1)' }, { label: 'more', color: 'var(--heat-7)' }]);

  // profession x sex x age, the breakdown in the reader's own 2001-2012 chart
  let sex2 = 'Female', mode = 'count';
  const { c: c2 } = yearCard(root(), {
    id: 'tn-prof-age', kicker: 'Tamil Nadu · suicides by profession, sex and age group', years: ay, name: 'tn-profession-age', meta: y => creditLine(P.meta, [y], P.sources),
    render: pos => {
      const y = ay[Math.round(pos)];
      const present = ages.filter(a => order.some(cc => P.get(cc, { sex: sex2, age: a })[y] != null));
      const parts = present.map((a, i) => ({ key: a, label: AGE_LABEL(a), color: SERIES(i) }));
      const rows = order.map(cc => ({ key: cc, label: cc, values: present.map(a => at(P.get(cc, { sex: sex2, age: a }), ay, pos) ?? 0) })).filter(r => r.values.some(v => v > 0));
      if (!rows.length) emptyChart(c2.svg, `No age breakdown for ${y}.`);
      else stackRows(c2.svg, { rows, parts, mode, bigYear: y });
      c2.set({ title: `${sex2 === 'Total' ? 'All' : sex2} suicides in Tamil Nadu by profession and age group, ${y}`, sub: mode === 'share' ? 'share of each profession by age group' : 'number of suicides by age group' });
      c2.setLegend(parts);
    },
    start: 'first',
  });
  const s2 = segmented({ label: 'Sex', value: sex2, options: ['Total', 'Male', 'Female'].map(s => ({ value: s, label: s === 'Total' ? 'Both sexes' : s })), onChange: v => { sex2 = v; redrawAll(); } });
  const m2 = segmented({ label: 'Number or share', value: mode, options: [{ value: 'count', label: 'Number', icon: 'hash' }, { value: 'share', label: 'Share', icon: 'percent' }], onChange: v => { mode = v; redrawAll(); } });
  c2.toolbar.append(s2.el, m2.el);
  c2.set({ note: 'The age groups were re-cut in 2014: up to 2013 they were 0–14, 15–29, 30–44, 45–59, 60+; from 2014 0–14 (or under 18), 14–17, 18–29, 30–44, 45–59, 60+.' });
}

async function ageSex() {
  const TN = await place('suicide_sex_age', 'state-tamil-nadu');
  const CH = await place('suicide_sex_age', 'city-chennai');
  const meta = await loadIndex('suicide_sex_age');
  const tys = yearsWith(TN), cys = yearsWith(CH);
  const male = P => Object.fromEntries(yearsWith(P).map(y => [y, P.get('all ages', { sex: 'Total' })[y] ? (100 * (P.get('all ages', { sex: 'Male' })[y] || 0)) / P.get('all ages', { sex: 'Total' })[y] : null]).filter(([, v]) => v != null));
  const mt = male(TN), mc = male(CH);
  section('Suicides by age group and sex', `<p>Suicides by age and sex are printed State-wise for ${span(tys)} and for the big cities, Chennai among them, for ${span(cys)}. Between 2016 and 2020 NCRB printed them only for all India, and the city tables have not returned. Men were ${fmtPct(mt[tys[0]], 0)} of Tamil Nadu's suicides in ${tys[0]} and ${fmtPct(mt[tys.at(-1)], 0)} in ${tys.at(-1)}; in Chennai ${fmtPct(mc[cys[0]], 0)} in ${cys[0]} and ${fmtPct(mc[cys.at(-1)], 0)} in ${cys.at(-1)}.</p>`);
  const ageOrder = meta.cats.filter(c => c !== 'all ages');
  // TN and Chennai, by sex, animated
  const ys = [...new Set([...tys, ...cys])].sort((a, b) => a - b);
  let mode = 'share';
  const { c } = yearCard(root(), {
    id: 'age-profile', kicker: 'Tamil Nadu and Chennai · suicides by age group', years: ys, name: 'tn-chennai-age-profile', start: 'first', meta: y => creditLine(meta, [y]),
    render: pos => {
      const y = ys[Math.round(pos)];
      const present = ageOrder.filter(a => [TN, CH].some(P => ['Male', 'Female'].some(s => P.get(a, { sex: s })[y] != null)));
      const parts = present.map((a, i) => ({ key: a, label: AGE_LABEL(a), color: SERIES(i) }));
      const rows = [];
      for (const [P, nm] of [[TN, 'Tamil Nadu'], [CH, 'Chennai']]) {
        for (const s of ['Male', 'Female']) {
          const vals = present.map(a => at(P.get(a, { sex: s }), ys, pos) ?? 0);
          if (vals.some(v => v > 0)) rows.push({ key: `${nm}${s}`, label: `${nm}, ${s.toLowerCase()}`, values: vals });
        }
      }
      if (!rows.length) emptyChart(c.svg, `Not printed for ${y}.`); else stackRows(c.svg, { rows, parts, mode, bigYear: y });
      c.set({ title: `Suicides by age group, Tamil Nadu and Chennai, ${y}`, sub: mode === 'share' ? 'share of each group\'s suicides' : 'number of suicides' });
      c.setLegend(parts);
    },
  });
  const m = segmented({ label: 'Number or share', value: mode, options: [{ value: 'share', label: 'Share', icon: 'percent' }, { value: 'count', label: 'Number', icon: 'hash' }], onChange: v => { mode = v; redrawAll(); } });
  c.toolbar.append(m.el);

  // the metros, animated: the age profile of each city
  const cities = meta.places.filter(p => p.type === 'city' && METROS.includes(p.name));
  const mys = [...new Set(cities.flatMap(p => p.years))].sort((a, b) => a - b);
  const { c: c2 } = yearCard(root(), {
    id: 'metros-age', kicker: 'The metros · suicides by age group', years: mys, name: 'metros-age-profile', start: 'first', meta: y => creditLine(meta, [y]),
    render: pos => {
      const y = mys[Math.round(pos)];
      const present = ageOrder.filter(a => cities.some(p => p.head[meta.cats.indexOf(a)]?.[y] != null));
      const parts = present.map((a, i) => ({ key: a, label: AGE_LABEL(a), color: SERIES(i) }));
      const rows = METROS.map(nm => cities.find(p => p.name === nm)).filter(Boolean).map(p => ({ key: p.key, label: p.name, hl: p.name === 'Chennai', values: present.map(a => at(p.head[meta.cats.indexOf(a)], mys, pos) ?? 0) })).filter(r => r.values.some(v => v > 0));
      stackRows(c2.svg, { rows, parts, mode: 'share', bigYear: y });
      c2.set({ title: `Age profile of suicides in the metros, ${y}`, sub: 'share of each city\'s suicides by age group · both sexes' });
      c2.setLegend(parts);
    },
  });
  c2.set({ note: `City tables by age and sex exist for ${span(mys)}. A 2019 table of suicidal deaths in major cities by sex and age with ICD-10 codes (S00–T98) comes from the Registrar General's <i>Medical Certification of Cause of Death</i> report, not from NCRB.` });
}

async function rates() {
  const meta = await loadIndex('suicide_rate');
  const get = nm => meta.places.find(p => p.name === nm && (nm !== 'Chennai' || p.type === 'city'));
  const ch = get('Chennai'), tn = get('Tamil Nadu'), india = get('All India'), cities = get('Total (Cities)');
  const ri = meta.cats.indexOf('Rate');
  const all = [ch, tn, india, cities].filter(Boolean);
  const ys = [...new Set(all.flatMap(p => Object.keys(p.head[ri] || {}).map(Number)))].sort((a, b) => a - b);
  const last = ys.at(-1);
  const states = meta.places.filter(p => p.type === 'state' || p.type === 'ut');
  const rank = states.map(p => ({ p, v: p.head[ri]?.[last] })).filter(x => x.v != null).sort((a, b) => b.v - a.v);
  const k = rank.findIndex(x => x.p.name === 'Tamil Nadu') + 1;
  // years whose rate was worked out here (NCRB's count over NCRB's population) rather than printed by NCRB
  const comp = {};
  for (const p of all) {
    const f = await place('suicide_rate', p.key);
    comp[p.name] = Object.entries(f.sources || {}).filter(([, s]) => s.includes('computed')).map(([y]) => Number(y));
  }
  const split = (p, computed) => Object.fromEntries(Object.entries(p.head[ri] || {}).filter(([y]) => comp[p.name].includes(Number(y)) === computed));
  const anyComp = Object.values(comp).some(l => l.length);
  section('Suicide rate', `<p>Rates are suicides per lakh people, for ${span(ys)}: as NCRB printed them, and${anyComp ? ' (dashed)' : ''} worked out from NCRB's own count of suicides and the population it printed for the year where it printed no rate. In ${last} Tamil Nadu's rate was <b>${fmt1(tn.head[ri][last])}</b> against ${fmt1(india.head[ri][last])} for India, ${k}${['th', 'st', 'nd', 'rd'][k % 10 > 3 || [11, 12, 13].includes(k % 100) ? 0 : k % 10]} of ${rank.length} States and UTs. Chennai's was ${fmt1(ch.head[ri][last])}.</p>`);
  const xs = []; for (let y = ys[0]; y <= last; y++) xs.push(y);
  const c = plainCard(root(), {
    id: 'rates-lines', kicker: 'Suicide rate', name: 'suicide-rate-chennai-tn-india', meta: () => creditLine(meta, ys),
    render: () => lineChart(c.svg, { xs, series: [
      { key: 'c', label: 'Chennai', color: 'var(--critical)', values: split(ch, false) },
      { key: 't', label: 'Tamil Nadu', color: 'var(--series-2)', values: split(tn, false) },
      { key: 'i', label: 'All India', color: 'var(--series-1)', values: split(india, false) },
      ...(cities ? [{ key: 'b', label: 'All big cities', color: 'var(--series-3)', values: split(cities, false) }] : []),
      // worked-out years, dashed, with no label of their own
      ...[[ch, 'var(--critical)'], [tn, 'var(--series-2)'], [india, 'var(--series-1)']].filter(([p]) => comp[p.name].length)
        .map(([p, col]) => ({ key: `${p.name}-c`, label: '', color: col, dash: '4 4', values: split(p, true) })),
    ], fmt: fmt1, yFmt: v => String(v) }),
  });
  c.set({ title: 'Suicide rate: Chennai, Tamil Nadu and India', sub: 'suicides per lakh people' });
  c.setLegend([{ label: 'Chennai', color: 'var(--critical)', line: true }, { label: 'Tamil Nadu', color: 'var(--series-2)', line: true }, { label: 'All India', color: 'var(--series-1)', line: true }, { label: 'All big cities', color: 'var(--series-3)', line: true }]);
  c.set({ note: `City rates use a fixed census population, so a change in a city's rate is a change in its number of suicides.${anyComp ? ` Dashed: worked out here from NCRB's count and population (${['Chennai', 'Tamil Nadu', 'All India'].filter(n => comp[n]?.length).map(n => `${n} ${span(comp[n].sort((a, b) => a - b))}`).join('; ')}). Chennai's 1989 rate of 38.1 is what NCRB printed (1,568 suicides that year against 885 in 1988 and 729 in 1990).` : ''}` });

  const rys = [...new Set(states.flatMap(p => Object.keys(p.head[ri] || {}).map(Number)))].filter(y => states.filter(p => p.head[ri]?.[y] != null).length >= 15).sort((a, b) => a - b);
  let gmax = 0; for (const p of states) for (const y of rys) gmax = Math.max(gmax, p.head[ri]?.[y] || 0);
  const { c: c2 } = yearCard(root(), {
    id: 'rates-rank', kicker: 'Suicide rate · States and UTs', years: rys, name: 'suicide-rate-states', start: 'first', meta: y => creditLine(meta, [y]),
    render: pos => {
      const y = rys[Math.round(pos)];
      const i0 = Math.floor(pos), i1 = Math.min(rys.length - 1, i0 + 1), f = pos - i0;
      const ord = yy => new Map(states.map(p => [p.key, p.head[ri]?.[yy]]).filter(([, v]) => v != null).sort((a, b) => b[1] - a[1]).map(([kk], n) => [kk, n]));
      const o0 = ord(rys[i0]), o1 = ord(rys[i1]);
      const rows = states.map(p => {
        const a = p.head[ri]?.[rys[i0]], b = p.head[ri]?.[rys[i1]];
        const v = a != null && b != null ? lerp(a, b, f) : f < .5 ? a : b;
        const r = o0.has(p.key) && o1.has(p.key) ? lerp(o0.get(p.key), o1.get(p.key), f) : (o0.get(p.key) ?? o1.get(p.key));
        return { key: p.key, label: p.name, value: v, rank: r, hl: p.name === 'Tamil Nadu', color: p.name === 'Tamil Nadu' ? 'var(--critical)' : 'var(--series-1)' };
      }).filter(r => r.value != null && r.rank != null);
      barRows(c2.svg, { rows, max: gmax, fmt: fmt1, bigYear: y });
      c2.set({ title: `Suicide rate by State and UT, ${y}`, sub: 'suicides per lakh people · Tamil Nadu highlighted' });
    },
  });
}

async function rateMap() {
  const meta = await loadIndex('suicide_rate');
  const ri = meta.cats.indexOf('Rate');
  const states = meta.places.filter(p => p.type === 'state' || p.type === 'ut');
  const ys = [...new Set(states.flatMap(p => Object.keys(p.head[ri] || {}).map(Number)))].filter(y => states.filter(p => p.head[ri]?.[y] != null).length >= 15).sort((a, b) => a - b);
  let gmax = 0; for (const p of states) for (const y of ys) gmax = Math.max(gmax, p.head[ri]?.[y] || 0);
  const { c } = yearCard(root(), {
    id: 'rates-map', kicker: 'Suicide rate · India', years: ys, name: 'suicide-rate-map', start: 'first', meta: y => creditLine(meta, [y]),
    render: pos => {
      const y = ys[Math.round(pos)];
      const values = {};
      for (const p of states) { const v = at(p.head[ri], ys, pos); if (v != null) values[p.name] = v; }
      const again = () => redraws.forEach(f => f()), geo = mapFor(y, again), outline = outlineMap(again);
      if (!geo || !outline) return;
      choropleth(c.svg, { geo, outline, values, max: gmax, year: y, fmt: fmt1, hl: 'Tamil Nadu', label: 'Suicides per lakh people' });
      c.set({ title: `Suicide rate by State and UT, ${y}`, sub: `suicides per lakh people · colour scale fixed across ${ys[0]}–${ys.at(-1)} · Tamil Nadu outlined`, note: boundaryNote(y) });
    },
  });
}

/* ================================================================== boot */

function redrawAll() { for (const f of redraws) f(); }

async function tiles() {
  const [T, R, S] = await Promise.all([place('traffic_time', 'city-chennai'), loadIndex('suicide_rate'), place('suicide_sex_age', 'state-tamil-nadu')]);
  const ty = yearsWith(T, { group: 'Road' }).at(-1);
  const ri = R.cats.indexOf('Rate'), si = R.cats.indexOf('Suicides');
  const ch = R.places.find(p => p.name === 'Chennai' && p.type === 'city'), tn = R.places.find(p => p.name === 'Tamil Nadu');
  const ry = Math.max(...Object.keys(ch.head[ri]).map(Number));
  const items = [
    { k: 'Chennai road crashes', i: 'car', v: fmtN(T.total(ty, { group: 'Road' })), d: `${ty}` },
    { k: 'Chennai suicides', i: 'heart', v: fmtN(ch.head[si]?.[ry]), d: `${ry} · rate ${fmt1(ch.head[ri][ry])} per lakh` },
    { k: 'Tamil Nadu suicides', i: 'users', v: fmtN(tn.head[si]?.[ry]), d: `${ry} · rate ${fmt1(tn.head[ri][ry])} per lakh` },
    { k: 'Oldest record here', i: 'calendar', v: '1967', d: 'first ADSI edition; series start where tables survive' },
  ];
  $('#tiles').innerHTML = items.map(t => `<div class="tile"><div class="k">${icon(t.i)}<span>${t.k}</span></div><div class="v">${t.v}</div><div class="d">${esc(t.d)}</div></div>`).join('');
}

async function boot() {
  initTheme(redrawAll);
  $('#foot').innerHTML = footerHtml();
  await tiles();
  for (const f of [trafficTime, trafficMonth, roadDeaths, means, profession, ageSex, rates, rateMap]) {
    try { await f(); } catch (e) { console.error(e); root().append(el('div', { class: 'card' }, `<div class="empty">Could not draw this section: ${esc(e.message)}</div>`)); }
  }
  redrawAll();
  let lastW = innerWidth;
  addEventListener('resize', debounce(() => { if (innerWidth !== lastW) { lastW = innerWidth; redrawAll(); } }, 120));
}
boot();
