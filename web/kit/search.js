/* The site-wide search: one box that finds any indicator (a category of a table), table, or dashboard, with
 * suggestions as you type. The catalog (web/data/catalog.json, analysis/catalog.py) is loaded on first use and
 * searched in the browser: every word must match, in the indicator's name or its table's title and topic; results
 * are ranked by where the words match and how many years the series runs.
 *
 *   mountSearch({ base: '../' })   binds the header's #search-open button (and the '/' key)
 */

import { el, icon, esc, getJSON } from './util.js?v=621fd152db';

const GEO = { state: 'States & UTs', city: 'Cities', india: 'All India' };
const PUB = { cii: 'Crime in India', adsi: 'Accidents & suicides', psi: 'Prisons' };
let CAT = null, loading = null;

export function loadCatalog(base) {
  if (CAT) return Promise.resolve(CAT);
  loading ||= getJSON(`${base}data/catalog.json`).then(c => {
    for (const t of c.tables) {
      t._t = `${t.title} ${t.topic} ${(t.also || []).join(' ')} ${PUB[t.pub] || ''}`.toLowerCase();
      t._c = t.cats.map(x => x.toLowerCase());
    }
    CAT = c;
    return c;
  });
  return loading;
}

export function hrefOf(base, t, ci = null) {
  if (t.k === 't') return `${base}trends/#d=${t.id}`;
  if (t.k === 'd') return `${base}dowry/#r=${t.id}`;
  return `${base}explore/#r=${t.pub}&t=${encodeURIComponent(t.id)}${ci != null ? `&c=${ci}` : ''}`;
}
const span = ys => (ys.length ? `${ys[0]}–${ys.at(-1)}` : '');

/** Ranked suggestions for a query: indicators (a category within a table) first, then whole tables. */
export function suggest(q, { limit = 14 } = {}) {
  const words = q.toLowerCase().split(/[^a-z0-9%.]+/).filter(w => w.length > 1 || /\d/.test(w));
  if (!words.length || !CAT) return { ind: [], tab: [] };
  const ind = [], tab = [];
  for (const t of CAT.tables) {
    const inTitle = words.filter(w => t._t.includes(w));
    if (inTitle.length === words.length) tab.push({ t, s: 40 + Math.min(30, t.ys.length) + (t._t.startsWith(words[0]) ? 15 : 0) + (t.k !== 'x' ? 25 : 0) + (t.geo === 'state' ? 4 : 0) });
    // indicators: every word in the category name or the table's title, at least one in the category
    for (let i = 0; i < t._c.length; i++) {
      const c = t._c[i];
      let inCat = 0, ok = true;
      for (const w of words) { if (c.includes(w)) inCat++; else if (!t._t.includes(w)) { ok = false; break; } }
      if (!ok || !inCat) continue;
      const exact = c === words.join(' ') ? 30 : c.startsWith(words[0]) ? 14 : 0;
      ind.push({ t, i, s: 20 * (inCat / words.length) + exact + Math.min(30, t.ys.length) * 0.8 - Math.min(12, c.length / 12) + (t.geo === 'state' ? 5 : 0) + (/^total|total$/.test(c) ? -3 : 0) });
    }
  }
  ind.sort((a, b) => b.s - a.s);
  tab.sort((a, b) => b.s - a.s);
  // one category name once per topic and geography (the longest-running table wins)
  const seen = new Set(), out = [];
  for (const x of ind) {
    const k = `${x.t._c[x.i]}|${x.t.topic}|${x.t.geo}`;
    if (seen.has(k)) continue;
    seen.add(k); out.push(x);
    if (out.length >= limit) break;
  }
  return { ind: out, tab: tab.slice(0, 8) };
}

export function mountSearch({ base = '../' } = {}) {
  const btn = document.getElementById('search-open');
  if (!btn) return;
  btn.setAttribute('aria-label', 'Search every indicator and table');
  let ov = document.getElementById('omni');
  if (!ov) {
    ov = el('div', { class: 'overlay', id: 'omni', hidden: true });
    ov.innerHTML = `<div class="overlay-panel omni" role="dialog" aria-modal="true" aria-label="Search every indicator and table">
      <div class="overlay-head">${icon('search', 'ic-lead')}
        <input type="search" placeholder="Search: murder, undertrial prisoners, suicides by farmers, over-speeding…" autocomplete="off" spellcheck="false" aria-label="Search">
        <button class="icon-btn" type="button" aria-label="Close">${icon('close')}</button></div>
      <div class="results" role="listbox"></div>
      <div class="omni-foot"><span><kbd>↑</kbd><kbd>↓</kbd> to move · <kbd>Enter</kbd> to open · <kbd>Esc</kbd> to close</span><a href="${base}browse/">Browse everything →</a></div></div>`;
    document.body.append(ov);
  }
  const inp = ov.querySelector('input'), res = ov.querySelector('.results');
  let items = [], act = 0;
  const paint = () => {
    const q = inp.value.trim();
    if (!CAT) { res.innerHTML = '<div class="empty">Loading the catalog…</div>'; return; }
    if (!q) {
      const dash = CAT.tables.filter(t => t.k !== 'x');
      items = dash.map(t => ({ t }));
      res.innerHTML = `<div class="grp">Dashboards</div>` + items.map((x, k) => row(x, k)).join('')
        + `<div class="grp">Try</div><div class="omni-try">${['murder', 'rape', 'undertrial', 'road accidents', 'suicides farmers', 'cyber', 'juveniles', 'dowry', 'prison capacity'].map(w => `<button type="button" data-try="${w}">${w}</button>`).join('')}</div>`;
      mark(); return;
    }
    const { ind, tab } = suggest(q);
    items = [...ind.map(x => ({ t: x.t, i: x.i })), ...tab.map(x => ({ t: x.t }))];
    res.innerHTML = (ind.length ? `<div class="grp">Indicators</div>` + ind.map((x, k) => row({ t: x.t, i: x.i }, k)).join('') : '')
      + (tab.length ? `<div class="grp">Tables and dashboards</div>` + tab.map((x, k) => row({ t: x.t }, ind.length + k)).join('') : '')
      || `<div class="empty">Nothing matches “${esc(q)}”. Try fewer or different words, or <a href="${base}browse/">browse everything</a>.</div>`;
    act = 0; mark();
  };
  const row = (x, k) => {
    const t = x.t, kind = t.k === 'x' ? 'table' : t.k === 't' ? 'chart' : 'users';
    const name = x.i != null ? t.cats[x.i].split(' · ').slice(-2).join(' · ') : t.title;
    const sub = x.i != null ? `${t.title} · ${GEO[t.geo] || ''}` : `${t.topic} · ${GEO[t.geo] || ''}${t.cats.length ? ` · ${t.cats.length} indicators` : ''}`;
    return `<a class="omni-row" href="${hrefOf(base, t, x.i ?? null)}" data-k="${k}" role="option">${icon(x.i != null ? 'line' : kind)}<span><b>${esc(name)}</b><small>${esc(sub)}</small></span><span class="yr">${span(t.ys)}<small>${PUB[t.pub] || ''}</small></span></a>`;
  };
  const mark = () => { [...res.querySelectorAll('.omni-row')].forEach((a, k) => a.classList.toggle('active', k === act)); res.querySelector('.omni-row.active')?.scrollIntoView({ block: 'nearest' }); };
  const open = () => { ov.hidden = false; inp.value = ''; paint(); inp.focus(); loadCatalog(base).then(paint); };
  const close = () => { ov.hidden = true; };
  btn.addEventListener('click', open);
  ov.querySelector('.overlay-head .icon-btn').addEventListener('click', close);
  ov.addEventListener('click', e => { if (e.target === ov) close(); const b = e.target.closest('[data-try]'); if (b) { inp.value = b.dataset.try; paint(); inp.focus(); } });
  inp.addEventListener('input', paint);
  inp.addEventListener('keydown', e => {
    const n = res.querySelectorAll('.omni-row').length;
    if (e.key === 'ArrowDown') { e.preventDefault(); act = Math.min(n - 1, act + 1); mark(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); act = Math.max(0, act - 1); mark(); }
    else if (e.key === 'Enter') { const a = res.querySelectorAll('.omni-row')[act]; if (a) { close(); if (a.href.split('#')[0] === location.href.split('#')[0]) { location.href = a.href; location.reload(); } else location.href = a.href; } }
  });
  res.addEventListener('click', e => { const a = e.target.closest('.omni-row'); if (a && a.href.split('#')[0] === location.href.split('#')[0]) { e.preventDefault(); close(); location.href = a.href; location.reload(); } });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !ov.hidden) close();
    if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && ov.hidden && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '')) { e.preventDefault(); open(); }
  });
}
