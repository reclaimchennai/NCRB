/* NCRB data explorer: find a table, read it as printed, chart it, follow it across years. */

import { $, el, clear, api, apiUrl, fmt, fmtCompact, pct, PUB_NAME, PUB_SHORT, methodInfo, seriesColor, debounce, hideTip } from './util.js?v=9f23c9d7d8';
import { bars, lines, choropleth, quality } from './charts.js?v=39b181c7a7';

const state = {
  pub: '', year: '', topic: '', q: '', listing: 'individual', offset: 0,
  table: null, column: null, view: 'bars', showTotals: false,
  series: null, seriesColumn: null, seriesNames: [],
};
let META = null;

/* ------------------------------------------------------------------ hero */

function renderHero() {
  const box = clear($('#kpis'));
  const order = { cii: 0, adsi: 1, psi: 2 };
  for (const p of [...META.publications].sort((a, b) => order[a.publication] - order[b.publication])) {
    const card = el('article', { class: 'kpi', dataset: { pub: p.publication } });
    card.append(
      el('div', { class: 'kpi-label' }, PUB_NAME[p.publication]),
      el('div', { class: 'kpi-value' }, fmtCompact(p.tables)),
      el('div', { class: 'kpi-sub' }, `tables · ${p.first_year}–${p.last_year}`),
      el('div', { class: 'kpi-foot' }, `${fmtCompact(p.cells)} figures · totals check ${pct(p.passed_text, p.checks_text)} (text) · ${pct(p.passed_ocr, p.checks_ocr)} (OCR)`),
    );
    card.addEventListener('click', () => { setPub(p.publication); $('#find').scrollIntoView({ behavior: 'smooth' }); });
    box.append(card);
  }
}

/* --------------------------------------------------------------- filters */

function renderFilters() {
  const seg = clear($('#pub-seg'));
  for (const [k, label] of [['', 'All'], ['cii', 'Crime'], ['adsi', 'ADSI'], ['psi', 'Prisons']]) {
    seg.append(el('button', { type: 'button', 'aria-pressed': String(state.pub === k), onclick: () => setPub(k) }, label));
  }
  const years = [...new Set(META.years.filter(y => !state.pub || y.publication === state.pub).map(y => y.year))].sort((a, b) => b - a);
  const ys = clear($('#year'));
  ys.append(el('option', { value: '' }, 'All years'));
  for (const y of years) ys.append(el('option', { value: y, selected: String(y) === String(state.year) }, y));
  const ts = clear($('#topic'));
  ts.append(el('option', { value: '' }, 'All topics'));
  const topics = META.topics.filter(t => !state.pub || t.publication === state.pub);
  const seen = new Set();
  for (const t of topics) {
    if (seen.has(t.topic)) continue;
    seen.add(t.topic);
    ts.append(el('option', { value: t.topic, selected: t.topic === state.topic }, `${t.topic} (${t.first_year}–${t.last_year})`));
  }
}

function setPub(p) {
  state.pub = p; state.topic = ''; state.year = ''; state.offset = 0;
  renderFilters(); search();
}

async function search(append = false) {
  const list = $('#results');
  list.classList.add('loading');
  const res = await api('tables', { pub: state.pub, year: state.year, topic: state.topic, q: state.q, listing: state.listing, offset: state.offset, limit: 40 });
  list.classList.remove('loading');
  if (!append) clear(list);
  $('#result-count').textContent = `${res.total.toLocaleString('en-IN')} tables`;
  for (const t of res.items) list.append(resultItem(t));
  const more = $('#more');
  more.hidden = state.offset + res.items.length >= res.total;
  if (!res.items.length && !append) list.append(el('li', { class: 'empty' }, 'No tables match. Try fewer words, or another year.'));
}

function resultItem(t) {
  const mi = methodInfo(t.method);
  const li = el('li', { class: 'result' });
  const a = el('a', { href: `#t=${encodeURIComponent(t.table_id)}` });
  a.append(
    el('span', { class: 'r-year' }, t.year),
    el('span', { class: 'r-title' }, t.title || '(untitled table)'),
  );
  const meta = el('span', { class: 'r-meta' });
  meta.append(el('span', { class: `pill pub-${t.publication}` }, PUB_SHORT[t.publication]));
  if (t.table_no) meta.append(el('span', { class: 'muted' }, `Table ${t.table_no}`));
  if (t.topic) meta.append(el('span', { class: 'muted' }, t.topic));
  meta.append(el('span', { class: `badge ${mi.tier}` }, mi.label));
  if (t.checks_total) meta.append(el('span', { class: `badge ${t.checks_passed === t.checks_total ? 'good' : 'warn'}` }, `totals ${t.checks_passed}/${t.checks_total}`));
  meta.append(el('span', { class: 'muted' }, `${t.n_rows} × ${t.n_cols}`));
  a.append(meta);
  li.append(a);
  return li;
}

/* ----------------------------------------------------------------- table */

async function openTable(id) {
  const panel = $('#table-panel');
  panel.hidden = false;
  panel.classList.add('loading');
  let data;
  try {
    data = await api(`table/${id}`);
  } catch {
    panel.classList.remove('loading');
    clear($('#t-title')).textContent = 'Table not found';
    return;
  }
  panel.classList.remove('loading');
  state.table = data;
  const t = data.table;
  const mi = methodInfo(t.method);
  $('#t-kicker').textContent = `${PUB_NAME[t.publication]} ${t.year}${t.table_no ? ` · Table ${t.table_no}` : ''}${t.topic ? ` · ${t.topic}` : ''}`;
  $('#t-title').textContent = t.title || t.pdf_title || 'Untitled table';
  const chips = clear($('#t-chips'));
  chips.append(el('span', { class: `badge ${mi.tier}`, title: mi.note }, mi.label));
  if (t.checks_total) chips.append(el('span', { class: `badge ${t.checks_passed === t.checks_total ? 'good' : 'warn'}`, title: 'Printed TOTAL rows compared with the sum of the rows above them' }, `totals check ${t.checks_passed}/${t.checks_total}`));
  else chips.append(el('span', { class: 'badge neutral', title: 'This table has no State/UT/city total rows to check against' }, 'no totals to check'));
  const pg = Array.isArray(t.pages) ? (t.pages.length > 1 ? `pages ${t.pages[0]}–${t.pages[t.pages.length - 1]}` : t.pages.length ? `page ${t.pages[0]}` : '') : (t.pages ? `page ${t.pages}` : '');
  chips.append(el('a', { class: 'chip-link', href: t.source_url, target: '_blank', rel: 'noopener' }, `Source ${/\.xlsx?$/i.test(t.source_url) ? 'spreadsheet' : 'PDF'}${pg ? `, ${pg}` : ''} ↗`));
  chips.append(el('a', { class: 'chip-link', href: apiUrl(`table/${t.table_id}.csv`) }, 'Download CSV'));
  $('#t-note').textContent = mi.tier === 'good' ? '' : mi.note;
  $('#t-note').hidden = mi.tier === 'good';

  // series link
  const sl = clear($('#t-series'));
  for (const s of data.series) {
    sl.append(el('a', { class: 'btn', href: `#s=${encodeURIComponent(s.series_id)}` }, `Follow this table across ${s.n_years} years (${s.first_year}–${s.last_year}) →`));
  }

  // column picker: numeric columns only, most-filled first
  const numeric = data.columns.map((c, i) => ({ c, i, n: data.rows.filter(r => typeof r.v[i] === 'number').length })).filter(x => x.n > 0);
  const sel = clear($('#t-column'));
  for (const x of numeric) sel.append(el('option', { value: x.i }, x.c.name));
  const prefer = numeric.find(x => /total/i.test(x.c.header?.[x.c.header.length - 1] || x.c.name)) || numeric[0];
  state.column = prefer ? prefer.i : null;
  if (prefer) sel.value = prefer.i;
  const states = data.rows.filter(r => r.entity_type === 'state' || r.entity_type === 'ut').length;
  $('#view-map').disabled = states < 8;
  if (states < 8 && state.view === 'map') state.view = 'bars';
  syncViewButtons();
  drawTableChart();
  renderGrid(data);
  const notes = clear($('#t-notes'));
  for (const n of t.notes || []) notes.append(el('li', {}, n));
  $('#t-notes-wrap').hidden = !(t.notes || []).length;
  if (t.checks?.failures?.length) {
    const f = clear($('#t-failures'));
    for (const x of t.checks.failures) f.append(el('li', {}, x));
    $('#t-failures-wrap').hidden = false;
  } else $('#t-failures-wrap').hidden = true;
  panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function syncViewButtons() {
  for (const b of document.querySelectorAll('#view-seg button')) b.setAttribute('aria-pressed', String(b.dataset.view === state.view));
  $('#totals-toggle').checked = state.showTotals;
}

function drawTableChart() {
  const d = state.table;
  const node = $('#t-chart'), legend = $('#t-legend');
  clear(legend);
  if (!d || state.column === null) { clear(node).append(el('p', { class: 'empty' }, 'This table has no numeric columns.')); return; }
  const i = state.column;
  const rows = d.rows.filter(r => typeof r.v[i] === 'number' && (state.showTotals || !r.is_total))
    .map(r => ({ label: r.name || r.section || `row ${r.row}`, name: r.name_std, value: r.v[i], raw: r.raw[i], total: !!r.is_total }));
  if (state.view === 'map') choropleth(node, rows.filter(r => !r.total), { legend });
  else bars(node, rows.slice(0, 120));
  $('#t-chart-cap').textContent = `${d.columns[i].name}${rows.length > 120 && state.view !== 'map' ? ' · largest 120 rows' : ''}`;
}

function renderGrid(d) {
  const wrap = clear($('#t-grid'));
  const table = el('table', { class: 'grid-table' });
  const thead = el('thead');
  const depth = Math.max(1, ...d.columns.map(c => (c.header || []).length));
  // header rows: merge equal neighbouring cells at each level, as printed
  for (let lvl = 0; lvl < depth; lvl++) {
    const tr = el('tr');
    if (lvl === 0) tr.append(el('th', { rowspan: depth, class: 'sticky' }, d.table.row_label?.split(' / ').pop() || ''));
    let k = 0;
    while (k < d.columns.length) {
      const h = d.columns[k].header || [d.columns[k].name];
      const text = lvl < h.length ? h[lvl] : (lvl === depth - 1 ? '' : null);
      let span = 1;
      while (k + span < d.columns.length) {
        const h2 = d.columns[k + span].header || [];
        if (lvl < h.length - 1 && JSON.stringify(h2.slice(0, lvl + 1)) === JSON.stringify(h.slice(0, lvl + 1))) span++;
        else break;
      }
      if (text !== null) tr.append(el('th', { colspan: span > 1 ? span : null }, text));
      else tr.append(el('th', {}));
      k += span;
    }
    thead.append(tr);
  }
  const tb = el('tbody');
  let section = null;
  for (const r of d.rows) {
    if (r.section && r.section !== section) {
      section = r.section;
      const sr = el('tr', { class: 'section-row' });
      sr.append(el('td', { colspan: d.columns.length + 1 }, section));
      tb.append(sr);
    }
    const tr = el('tr', { class: r.is_total ? 'total-row' : null });
    tr.append(el('th', { class: 'sticky', scope: 'row' }, `${r.sl_no ? `${r.sl_no}. ` : ''}${r.name}`));
    r.raw.forEach((raw, i) => {
      const td = el('td', { class: typeof r.v[i] === 'number' ? 'num' : 'txt' }, raw ?? '');
      tr.append(td);
    });
    if (r.conf !== null && r.conf < 0.6) tr.classList.add('low-conf');
    tb.append(tr);
  }
  table.append(thead, tb);
  wrap.append(table);
}

/* ---------------------------------------------------------------- series */

async function openSeries(id, column) {
  const panel = $('#series-panel');
  panel.hidden = false;
  const data = await api(`series/${id}`);
  state.series = data;
  const s = data.series;
  $('#s-kicker').textContent = `${PUB_NAME[s.publication]} · ${s.first_year}–${s.last_year} · ${s.n_years} editions`;
  $('#s-title').textContent = s.title;
  const cs = clear($('#s-column'));
  for (const c of data.columns) cs.append(el('option', { value: c.column }, `${c.column} (${c.years} yrs)`));
  state.seriesColumn = column && data.columns.some(c => c.column === column) ? column : data.columns[0]?.column;
  cs.value = state.seriesColumn;
  // default selection: the total row if there is one, else the most frequent labels
  const allIndia = data.names.find(n => n.name_std === 'All India');
  const totals = data.names.filter(n => n.is_total || n.entity_type === 'total');
  state.seriesNames = (allIndia ? [allIndia] : totals.length ? totals.slice(0, 1) : data.names.slice(0, 3)).map(n => n.name_std);
  renderNamePicker();
  const ml = clear($('#s-members'));
  const seenYear = new Set();
  for (const m of data.members) {
    if (seenYear.has(m.year)) continue;  // a table published both individually and online
    seenYear.add(m.year);
    const mi = methodInfo(m.method);
    const li = el('li');
    li.append(el('a', { href: `#t=${encodeURIComponent(m.table_id)}` }, String(m.year)), el('span', { class: `badge ${mi.tier}` }, mi.label));
    ml.append(li);
  }
  await drawSeries();
  panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderNamePicker() {
  const box = clear($('#s-names'));
  const names = state.series.names;
  for (const n of state.seriesNames) {
    const i = state.seriesNames.indexOf(n);
    const chip = el('button', { type: 'button', class: 'name-chip', title: 'Remove' });
    chip.append(el('span', { class: 'chip-key', style: `background:${seriesColor(i)}` }), document.createTextNode(n), el('span', { class: 'x' }, '×'));
    chip.addEventListener('click', () => { state.seriesNames = state.seriesNames.filter(x => x !== n); renderNamePicker(); drawSeries(); });
    box.append(chip);
  }
  const add = el('select', { 'aria-label': 'Add a row' });
  add.append(el('option', { value: '' }, state.seriesNames.length >= 8 ? 'Up to 8 lines' : '+ Add a State, city or row'));
  for (const n of names) if (!state.seriesNames.includes(n.name_std)) add.append(el('option', { value: n.name_std }, `${n.name_std} (${n.years} yrs)`));
  add.disabled = state.seriesNames.length >= 8;
  add.addEventListener('change', () => { if (add.value) { state.seriesNames.push(add.value); renderNamePicker(); drawSeries(); } });
  box.append(add);
}

async function drawSeries() {
  const node = $('#s-chart');
  node.classList.add('loading');
  const data = await api(`series/${state.series.series.series_id}/data`, { column: state.seriesColumn, names: state.seriesNames.join('|') });
  node.classList.remove('loading');
  const ocrYears = new Set(state.series.members.filter(m => ['pdf_ocr', 'pdf_mixed', 'pdf_vlm'].includes(m.method)).map(m => m.year));
  const series = state.seriesNames.map((n, i) => ({
    name: n, color: seriesColor(i),
    points: data.filter(d => d.name_std === n).map(d => ({ year: d.year, value: d.value, raw: d.raw })),
  }));
  lines(node, series, { ocrYears });
  $('#s-ocr-note').hidden = !ocrYears.size;
}

/* ---------------------------------------------------------------- routing */

function route() {
  const h = new URLSearchParams(location.hash.slice(1));
  hideTip();
  if (h.get('t')) openTable(h.get('t'));
  if (h.get('s')) openSeries(h.get('s'), h.get('c'));
}

/* ------------------------------------------------------------------ init */

async function init() {
  const theme = localStorageGet('theme');
  if (theme) document.documentElement.dataset.theme = theme;
  $('#theme').addEventListener('click', () => {
    const cur = document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    localStorageSet('theme', next);
    if (state.table) drawTableChart();
    if (state.series) drawSeries();
    api('quality').then(q => quality($('#q-chart'), q));
  });
  META = await api('meta');
  renderHero();
  renderFilters();
  $('#year').addEventListener('change', e => { state.year = e.target.value; state.offset = 0; search(); });
  $('#topic').addEventListener('change', e => { state.topic = e.target.value; state.offset = 0; search(); });
  $('#q').addEventListener('input', debounce(e => { state.q = e.target.value; state.offset = 0; search(); }, 250));
  $('#volumes').addEventListener('change', e => { state.listing = e.target.checked ? 'all' : 'individual'; state.offset = 0; search(); });
  $('#more').addEventListener('click', () => { state.offset += 40; search(true); });
  $('#t-column').addEventListener('change', e => { state.column = +e.target.value; drawTableChart(); });
  for (const b of document.querySelectorAll('#view-seg button')) b.addEventListener('click', () => { if (b.disabled) return; state.view = b.dataset.view; syncViewButtons(); drawTableChart(); });
  $('#totals-toggle').addEventListener('change', e => { state.showTotals = e.target.checked; drawTableChart(); });
  $('#s-column').addEventListener('change', e => { state.seriesColumn = e.target.value; drawSeries(); });
  addEventListener('hashchange', route);
  addEventListener('resize', debounce(() => { if (state.table) drawTableChart(); if (state.series) drawSeries(); }, 200));
  search();
  api('quality').then(q => quality($('#q-chart'), q));
  route();
}

function localStorageGet(k) { try { return localStorage.getItem(k); } catch { return null; } }
function localStorageSet(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } }

init();
