/* Browse: the index of everything on the site. A search box with suggestions, the three reports broken into
 * themes, and under each theme its tables with a coverage strip (one cell a year: printed, read from a scan, or
 * no figure). At the foot, what is held of each edition. Data: web/data/catalog.json (analysis/catalog.py). */

import { $, el, icon, esc, initTheme, debounce, fmtN } from '../kit/util.js?v=621fd152db';
import { segmented } from '../kit/cards.js?v=621fd152db';
import { footerHtml } from '../kit/footer.js?v=621fd152db';
import { mountSearch, loadCatalog, suggest, hrefOf } from '../kit/search.js?v=621fd152db';

const BASE = '../';
const PUB = { cii: 'Crime in India', adsi: 'Accidental Deaths & Suicides in India', psi: 'Prison Statistics India' };
const PUB_SHORT = { cii: 'Crime', adsi: 'Accidents & suicides', psi: 'Prisons' };
const START = { cii: 1953, adsi: 1967, psi: 1995 };
const GEO = { state: 'States & UTs', city: 'Cities', india: 'All India' };
const S = { C: null, pub: 'cii', topic: null, geo: 'all', span: 'all', q: '' };
const ui = {};

/* -------------------------------------------------------- coverage strip */
/** One cell a year from y0 to y1: printed, read from a scan, or no figure. */
export function strip(t, y0, y1, w = 5, h = 14) {
  const has = new Set(t.ys), sc = new Set(t.sc);
  let r = '';
  for (let y = y0; y <= y1; y++) r += `<rect class="${has.has(y) ? (sc.has(y) ? 's' : 't') : 'n'}" x="${(y - y0) * (w + 1)}" y="0" width="${w}" height="${h}" rx="1"><title>${y}: ${has.has(y) ? (sc.has(y) ? 'read from a scanned edition' : 'printed figures') : 'no figure'}</title></rect>`;
  const W = (y1 - y0 + 1) * (w + 1);
  return `<svg class="cov" width="${W}" height="${h + 11}" viewBox="0 0 ${W} ${h + 11}" role="img" aria-label="Years covered: ${t.ys.length} of ${y1 - y0 + 1}">${r}<text x="0" y="${h + 10}">${y0}</text><text x="${W}" y="${h + 10}" text-anchor="end">${y1}</text></svg>`;
}
const inSpan = t => { const lo = t.ys[0], hi = t.ys.at(-1); const full = hi - lo + 1; return { lo, hi, full, miss: full - t.ys.length }; };

/* ------------------------------------------------------------- the list */
function filtered() {
  const q = S.q.toLowerCase().split(/\s+/).filter(Boolean);
  return S.C.tables.filter(t => (S.pub === 'all' || t.pub === S.pub || (t.k !== 'x' && S.pub !== 'psi' && t.pub === S.pub))
    && (S.geo === 'all' || t.geo === S.geo)
    && (S.span === 'all' || (S.span === 'long' ? t.ys.length >= 10 : S.span === 'now' ? t.ys.at(-1) >= 2022 : t.ys.length < 3))
    && (!q.length || q.every(w => t._t.includes(w) || t._c.some(c => c.includes(w)))));
}
function drawThemes() {
  const list = filtered();
  const by = new Map();
  for (const t of list) by.set(t.topic, (by.get(t.topic) || 0) + 1);
  const topics = [...by.keys()].sort((a, b) => (a.startsWith('Dashboards') ? -1 : b.startsWith('Dashboards') ? 1 : a.localeCompare(b)));
  if (S.topic !== '*' && !by.has(S.topic)) S.topic = S.q ? '*' : topics[0] ?? '*';
  $('#themes').innerHTML = `<div class="grp">${S.pub === 'all' ? 'All reports' : esc(PUB[S.pub])}</div>
    <button type="button" data-t="*" aria-current="${S.topic === '*'}"><span>All themes</span><span>${list.length}</span></button>`
    + topics.map(tp => `<button type="button" data-t="${esc(tp)}" aria-current="${S.topic === tp}"><span>${esc(tp)}</span><span>${by.get(tp)}</span></button>`).join('');
  drawList(list);
}
function drawList(list) {
  const rows = list.filter(t => S.topic === '*' || t.topic === S.topic)
    .sort((a, b) => (a.k !== 'x' ? -1 : 0) - (b.k !== 'x' ? -1 : 0) || ({ state: 0, city: 1, india: 2 }[a.geo] - { state: 0, city: 1, india: 2 }[b.geo]) || b.ys.length - a.ys.length || a.title.localeCompare(b.title));
  const y0 = S.pub === 'all' ? 1953 : START[S.pub], y1 = 2024;
  const shown = rows.slice(0, 250);
  const q = S.q.toLowerCase().split(/\s+/).filter(Boolean);
  $('#tlist').innerHTML = `<div class="tlist-head"><h2>${esc(S.topic === '*' ? (S.q ? `Matching “${S.q}”` : 'All themes') : S.topic)}</h2>
      <p>${fmtN(rows.length)} table${rows.length === 1 ? '' : 's'}${rows.length > shown.length ? `, first ${shown.length} shown: narrow with the filters above` : ''}. Each strip runs ${y0}–${y1}, one cell a year.</p>
      <div class="cov-key"><span><i class="t"></i>printed figures (text or spreadsheet)</span><span><i class="s"></i>read from a scanned edition</span><span><i class="n"></i>no figure: not printed that year, or not yet read</span></div></div>`
    + (shown.map(t => {
      const s = inSpan(t);
      const hit = q.length ? t.cats.map((c, i) => ({ c, i })).filter(x => q.some(w => x.c.toLowerCase().includes(w))) : [];
      const cats = (hit.length ? hit : t.cats.map((c, i) => ({ c, i }))).slice(0, 60);
      return `<div class="trow"><div><a class="t" href="${hrefOf(BASE, t)}">${esc(t.title)}</a>
          <div class="m"><span class="chip">${esc(t.k === 'x' ? GEO[t.geo] : 'Dashboard')}</span><span>${s.lo}–${s.hi}</span><span>${t.ys.length} year${t.ys.length === 1 ? '' : 's'}${s.miss ? `, ${s.miss} missing in between` : ', none missing in between'}</span>${t.sc.length ? `<span>${t.sc.length} from scans</span>` : ''}<span>${t.cats.length ? `${t.cats.length} indicators` : ''}</span><span>${t.rows} ${t.geo === 'india' ? 'rows' : 'places'}</span>${S.pub === 'all' ? `<span>${esc(PUB_SHORT[t.pub])}</span>` : ''}</div></div>
        <div>${strip(t, y0, y1)}</div>
        ${t.cats.length ? `<details${hit.length ? ' open' : ''}><summary>${hit.length ? `${hit.length} matching indicator${hit.length === 1 ? '' : 's'}` : `Its ${t.cats.length} indicators`}</summary><div class="inds">${cats.map(x => `<a href="${hrefOf(BASE, t, t.k === 'x' ? x.i : null)}">${esc(x.c)}</a>`).join('')}${t.cats.length > cats.length && !hit.length ? `<a href="${hrefOf(BASE, t)}">… all ${t.cats.length}</a>` : ''}</div></details>` : ''}</div>`;
    }).join('') || '<div class="empty">No table matches these filters.</div>');
}

/* ---------------------------------------------------- what is held, by edition */
function drawHeld() {
  const cov = S.C.coverage, led = S.C.ledger || {};
  const tot = k => Object.values(cov).reduce((a, ys) => a + Object.values(ys).reduce((b, c) => b + (c[k] || 0), 0), 0);
  const rows = ['cii', 'adsi', 'psi'].map(p => {
    const ys = cov[p] || {};
    const years = []; for (let y = START[p]; y <= 2024; y++) years.push(y);
    const mx = Math.max(1, ...years.map(y => ys[y]?.tables || 0));
    const cells = years.map(y => {
      const c = ys[y];
      if (!c || !c.files) return `<span class="none" style="height:3px" title="${y}: no edition on NCRB's site"></span>`;
      const tip = `${y}: ${c.files} files listed${c.not_served ? `, ${c.not_served} not served by NCRB` : ''}; ${c.tables || 0} tables read (${c.joined || 0} in series, ${c.district || 0} district-wise, ${c.single || 0} not joined)`;
      return `<span class="${(c.tables || 0) === 0 ? 'none' : (c.scanned || 0) > 0.5 * (c.with_tables || 1) ? 'part' : ''}" style="height:${Math.max(4, Math.round(60 * Math.sqrt((c.tables || 0) / mx)))}px" title="${tip}"></span>`;
    }).join('');
    const none = years.filter(y => !ys[y]?.tables);
    return `<div class="edrow"><h3>${esc(PUB[p])}</h3><div class="cells">${cells}</div><div class="axis"><span>${START[p]}</span><span>${none.length ? `no tables for ${none.join(', ')}` : 'every edition read'}</span><span>2024</span></div></div>`;
  }).join('');
  const L = k => fmtN(led[k] || 0);
  $('#held').innerHTML = `<div class="card-head"><div class="titles"><div class="kicker">Completeness</div><h2>What is held of each edition</h2>
      <p>One bar an edition: its height is the number of tables read from it (square-root scale); lighter bars are editions that are mostly scans. Hover for the count.</p></div></div>
    <div class="card-body"><div class="edmatrix">${rows}</div>
    <p class="note">Of ${fmtN(tot('files'))} files NCRB lists, ${fmtN(tot('not_served'))} are no longer served by its site (most were recovered from the Internet Archive where a copy exists). ${fmtN(tot('tables'))} tables were read:
      ${L('in a family')} carry the series on these pages, ${fmtN((led['another printing of a year in a family'] || 0) + (led['reprint of a table of the same year'] || 0))} are second printings of the same figures (a chapter and its table file),
      ${L('district-wise (Tables page)')} are district-wise (on the Tables page), and ${fmtN(Object.entries(led).filter(([k]) => !/family|reprint|district/.test(k)).reduce((a, [, v]) => a + v, 0))} could not be joined into a series (scanned one-off tables, unreadable headings); every one of those is still on the Tables page.</p></div>`;
}

function drawTiles() {
  const X = S.C.tables.filter(t => t.k === 'x');
  const ind = S.C.tables.reduce((a, t) => a + Math.max(1, t.cats.length), 0);
  const long = X.filter(t => t.ys.length >= 20).length;
  const t = [
    { k: 'Indicators', i: 'line', v: fmtN(ind), d: 'a category of a table, charted over the years' },
    { k: 'Tables joined across editions', i: 'table', v: fmtN(X.length), d: `${fmtN(long)} run 20 years or more` },
    { k: 'Editions read', i: 'calendar', v: fmtN(Object.values(S.C.coverage).reduce((a, ys) => a + Object.values(ys).filter(c => c.tables).length, 0)), d: 'Crime 1953–, ADSI 1967–, Prisons 1995–' },
    { k: 'Dashboards', i: 'chart', v: String(S.C.tables.filter(t2 => t2.k !== 'x').length), d: 'crashes, suicides, dowry: places compared' },
  ];
  $('#tiles').innerHTML = t.map(x => `<div class="tile"><div class="k">${icon(x.i)}<span>${x.k}</span></div><div class="v">${x.v}</div><div class="d">${esc(x.d)}</div></div>`).join('');
}

/* ---------------------------------------------------------- hero search */
function heroSearch() {
  const inp = $('#hs-q'), drop = $('#hs-drop');
  let act = 0;
  const paint = () => {
    const q = inp.value.trim();
    if (!q) { drop.hidden = true; return; }
    const { ind, tab } = suggest(q, { limit: 10 });
    const row = (t, i) => `<a class="omni-row" href="${hrefOf(BASE, t, i)}">${icon(i != null ? 'line' : 'table')}<span><b>${esc(i != null ? t.cats[i].split(' · ').slice(-2).join(' · ') : t.title)}</b><small>${esc(i != null ? `${t.title} · ${GEO[t.geo]}` : `${t.topic} · ${GEO[t.geo]}`)}</small></span><span class="yr">${t.ys[0]}–${t.ys.at(-1)}<small>${esc(PUB_SHORT[t.pub])}</small></span></a>`;
    drop.innerHTML = (ind.length ? '<div class="grp">Indicators</div>' + ind.map(x => row(x.t, x.i)).join('') : '')
      + (tab.length ? '<div class="grp">Tables and dashboards</div>' + tab.slice(0, 5).map(x => row(x.t, null)).join('') : '')
      || `<div class="empty">Nothing matches “${esc(q)}”.</div>`;
    drop.hidden = false; act = 0; mark();
  };
  const mark = () => [...drop.querySelectorAll('.omni-row')].forEach((a, k) => a.classList.toggle('active', k === act));
  inp.addEventListener('input', () => { paint(); S.q = inp.value.trim(); drawThemesSoon(); });
  inp.addEventListener('focus', paint);
  inp.addEventListener('keydown', e => {
    const n = drop.querySelectorAll('.omni-row').length;
    if (e.key === 'ArrowDown') { e.preventDefault(); act = Math.min(n - 1, act + 1); mark(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); act = Math.max(0, act - 1); mark(); }
    else if (e.key === 'Enter') { const a = drop.querySelectorAll('.omni-row')[act]; if (a && !drop.hidden) location.href = a.href; }
    else if (e.key === 'Escape') { drop.hidden = true; }
  });
  document.addEventListener('pointerdown', e => { if (!$('#hs').contains(e.target)) drop.hidden = true; });
}
const drawThemesSoon = debounce(() => { S.topic = S.q ? '*' : S.topic; drawThemes(); writeHash(); }, 180);

function writeHash() {
  history.replaceState(null, '', `#${new URLSearchParams({ r: S.pub, ...(S.topic && S.topic !== '*' ? { th: S.topic } : {}), ...(S.geo !== 'all' ? { g: S.geo } : {}), ...(S.span !== 'all' ? { s: S.span } : {}), ...(S.q ? { q: S.q } : {}) })}`);
}

async function boot() {
  initTheme(() => {});
  $('#foot').innerHTML = footerHtml();
  S.C = await loadCatalog(BASE);
  mountSearch({ base: BASE });
  const h = new URLSearchParams(location.hash.slice(1));
  if (['cii', 'adsi', 'psi', 'all'].includes(h.get('r'))) S.pub = h.get('r');
  if (h.get('th')) S.topic = h.get('th');
  if (h.get('g')) S.geo = h.get('g');
  if (h.get('s')) S.span = h.get('s');
  if (h.get('q')) { S.q = h.get('q'); $('#hs-q').value = S.q; S.topic = '*'; }
  const bar = $('#controls');
  ui.pub = segmented({ label: 'Report', value: S.pub, options: [{ value: 'cii', label: 'Crime', icon: 'database' }, { value: 'adsi', label: 'Accidents & suicides', icon: 'activity' }, { value: 'psi', label: 'Prisons', icon: 'building' }, { value: 'all', label: 'All' }], onChange: v => { S.pub = v; S.topic = null; drawThemes(); writeHash(); } });
  ui.geo = segmented({ label: 'Geography', value: S.geo, options: [{ value: 'all', label: 'Any geography' }, { value: 'state', label: 'States & UTs' }, { value: 'city', label: 'Cities' }, { value: 'india', label: 'All India' }], onChange: v => { S.geo = v; drawThemes(); writeHash(); } });
  ui.span = segmented({ label: 'Length', value: S.span, options: [{ value: 'all', label: 'Any length' }, { value: 'long', label: '10+ years' }, { value: 'now', label: 'Up to 2022–24' }, { value: 'short', label: '1–2 editions' }], onChange: v => { S.span = v; drawThemes(); writeHash(); } });
  bar.append(ui.pub.el, ui.geo.el, ui.span.el);
  $('#themes').addEventListener('click', e => { const b = e.target.closest('button[data-t]'); if (!b) return; S.topic = b.dataset.t; drawThemes(); writeHash(); $('#tlist').scrollIntoView({ block: 'nearest' }); });
  heroSearch();
  drawTiles(); drawThemes(); drawHeld();
}
boot().catch(e => { console.error(e); $('#tlist').innerHTML = `<div class="empty">Could not load the catalog: ${esc(e.message)}</div>`; });
