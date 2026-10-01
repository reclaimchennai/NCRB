/* Shared helpers: DOM, fetching, formatting, colour, tooltip. No external requests. */

export const SVG_NS = 'http://www.w3.org/2000/svg';
export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

export function svg(tag, attrs = {}, text) {
  const n = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v !== null && v !== undefined) n.setAttribute(k, v);
  if (text !== undefined) n.textContent = text;
  return n;
}

/** Element with attributes and text. Text is always set with textContent: labels come from PDFs. */
export function el(tag, attrs = {}, text) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'dataset') Object.assign(n.dataset, v);
    else if (k.startsWith('on') && typeof v === 'function') n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v === true ? '' : v);
  }
  if (text !== undefined && text !== null) n.textContent = text;
  return n;
}

export function clear(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
  return node;
}

/* ---------------------------------------------------------------- fetching */

const BASE = new URL('.', document.baseURI).pathname.replace(/\/$/, '');
const cache = new Map();

/** GET a JSON endpoint under /api, memoised for the session. */
export async function api(path, params = {}) {
  const q = new URLSearchParams(Object.entries(params).filter(([, v]) => v !== null && v !== undefined && v !== ''));
  const url = `${BASE}/api/${path}${q.toString() ? `?${q}` : ''}`;
  if (!cache.has(url)) {
    cache.set(url, fetch(url).then(r => {
      if (!r.ok) throw new Error(`${r.status} ${url}`);
      return r.json();
    }).catch(e => { cache.delete(url); throw e; }));
  }
  return cache.get(url);
}
export const apiUrl = path => `${BASE}/api/${path}`;

/* -------------------------------------------------------------- formatting */

const nf0 = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 });
const nf1 = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 1 });
const nf2 = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 2 });

/** Indian digit grouping, decimals only where the source had them. */
export function fmt(v) {
  if (v === null || v === undefined || Number.isNaN(v)) return '–';
  const a = Math.abs(v);
  if (Number.isInteger(v)) return nf0.format(v);
  return a >= 100 ? nf1.format(v) : nf2.format(v);
}
export function fmtCompact(v) {
  if (v === null || v === undefined) return '–';
  const a = Math.abs(v);
  if (a >= 1e7) return `${nf1.format(v / 1e7)} cr`;
  if (a >= 1e5) return `${nf1.format(v / 1e5)} lakh`;
  if (a >= 1e3) return `${nf1.format(v / 1e3)}k`;
  return fmt(v);
}
export const pct = (a, b) => (b ? `${nf1.format((100 * a) / b)}%` : '–');

export const PUB_NAME = {
  cii: 'Crime in India',
  adsi: 'Accidental Deaths & Suicides',
  psi: 'Prison Statistics',
};
export const PUB_SHORT = { cii: 'Crime', adsi: 'ADSI', psi: 'Prisons' };

/** Methods readers should know about: text and Excel are copied, OCR is recognised. */
export function methodInfo(m) {
  if (m === 'excel') return { label: 'Excel', tier: 'good', note: 'Read from NCRB’s spreadsheet: figures are copied, not recognised.' };
  if (m === 'pdf_text') return { label: 'Text PDF', tier: 'good', note: 'Read from the PDF’s text layer: figures are copied, not recognised.' };
  if (m === 'pdf_vlm') return { label: 'AI OCR', tier: 'warn', note: 'Scanned page read by a document AI model. Check figures against the PDF before quoting them.' };
  return { label: 'OCR', tier: 'serious', note: 'Scanned page read by OCR. Digits can be wrong or missing; check against the PDF.' };
}

/* ------------------------------------------------------------------ colour */

export const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
export const seriesColor = i => css(`--series-${(i % 8) + 1}`);

/** Sequential ramp step (1..7) for t in [0, 1]. */
export const seq = t => css(`--seq-${Math.max(1, Math.min(7, 1 + Math.round(t * 6)))}`);

export function niceTicks(min, max, n = 5) {
  if (min === max) { max = min + 1; }
  const span = max - min;
  const step0 = 10 ** Math.floor(Math.log10(span / n));
  const err = (span / n) / step0;
  const step = step0 * (err >= 7.5 ? 10 : err >= 3.5 ? 5 : err >= 1.5 ? 2 : 1);
  const t = [];
  for (let v = Math.floor(min / step) * step; v <= max + step * 1e-9; v += step) t.push(+v.toFixed(10));
  return t;
}

/* ----------------------------------------------------------------- tooltip */

let tip;
export function showTip(build, ev) {
  if (!tip) tip = $('#tip');
  clear(tip);
  build(tip);
  tip.classList.add('on');
  moveTip(ev);
}
export function moveTip(ev) {
  if (!tip || !ev) return;
  const pad = 14;
  const r = tip.getBoundingClientRect();
  let x = ev.clientX + pad, y = ev.clientY + pad;
  if (x + r.width > innerWidth - 8) x = ev.clientX - r.width - pad;
  if (y + r.height > innerHeight - 8) y = ev.clientY - r.height - pad;
  tip.style.transform = `translate(${Math.max(8, x)}px, ${Math.max(8, y)}px)`;
}
export function hideTip() { tip?.classList.remove('on'); }

/** One tooltip row: value first (strong), label after (muted), keyed by a short line of colour. */
export function tipRow(parent, value, label, color) {
  const row = el('div', { class: 'tip-row' });
  if (color) row.append(el('span', { class: 'tip-key', style: `background:${color}` }));
  row.append(el('strong', {}, value), el('span', {}, label));
  parent.append(row);
}

export function debounce(fn, ms = 200) {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}
