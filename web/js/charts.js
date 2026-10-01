/* Hand-drawn SVG charts: ranked bars, lines over years, a State/UT map, quality dots. */

import { svg, el, clear, fmt, fmtCompact, niceTicks, showTip, moveTip, hideTip, tipRow, seriesColor, seq, css } from './util.js';

const width = node => Math.max(300, node.clientWidth || 640);

/* ------------------------------------------------------------- ranked bars */

/**
 * Horizontal bars, largest first. rows: [{label, value, total?}].
 * Negative values (percentage changes) draw left of a zero line.
 */
export function bars(node, rows, { unit = '' } = {}) {
  clear(node);
  const data = rows.filter(r => r.value !== null && r.value !== undefined);
  if (!data.length) { node.append(el('p', { class: 'empty' }, 'No numeric values in this column.')); return; }
  data.sort((a, b) => b.value - a.value);
  const W = width(node), rowH = 22, labelW = Math.min(190, W * 0.36), valW = 64;
  const H = data.length * rowH + 28;
  const lo = Math.min(0, ...data.map(d => d.value)), hi = Math.max(0, ...data.map(d => d.value));
  const x = v => labelW + ((v - lo) / (hi - lo || 1)) * (W - labelW - valW - 8);
  const s = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, class: 'chart', role: 'img' });
  for (const t of niceTicks(lo, hi, 4)) {
    if (t < lo || t > hi) continue;
    s.append(svg('line', { x1: x(t), x2: x(t), y1: 0, y2: H - 22, class: t === 0 ? 'axis' : 'grid' }));
    s.append(svg('text', { x: x(t), y: H - 6, class: 'tick', 'text-anchor': 'middle' }, fmtCompact(t)));
  }
  data.forEach((d, i) => {
    const y = i * rowH + 3, h = rowH - 6;
    const g = svg('g', { class: 'bar', tabindex: 0 });
    const x0 = x(Math.min(0, d.value)), x1 = x(Math.max(0, d.value));
    g.append(svg('rect', { x: 0, y: y - 3, width: W, height: rowH, class: 'hit' }));
    g.append(svg('rect', { x: x0, y, width: Math.max(1, x1 - x0), height: h, rx: 2, fill: d.total ? css('--ink-muted') : css('--series-1') }));
    g.append(svg('text', { x: labelW - 8, y: y + h - 4, class: 'label', 'text-anchor': 'end' }, d.label.length > 28 ? `${d.label.slice(0, 27)}…` : d.label));
    g.append(svg('text', { x: x1 + 6, y: y + h - 4, class: 'value' }, fmt(d.value)));
    const tipFn = ev => showTip(t => { tipRow(t, `${fmt(d.value)}${unit}`, d.label); if (d.raw && d.raw !== String(d.value)) t.append(el('div', { class: 'tip-note' }, `printed as “${d.raw}”`)); }, ev);
    g.addEventListener('pointermove', tipFn);
    g.addEventListener('focus', ev => tipFn({ clientX: g.getBoundingClientRect().right, clientY: g.getBoundingClientRect().top }));
    g.addEventListener('pointerleave', hideTip);
    g.addEventListener('blur', hideTip);
    s.append(g);
  });
  node.append(s);
}

/* ------------------------------------------------------------ line chart */

/**
 * Lines over years. series: [{name, color, points: [{year, value, raw, ocr}]}].
 * One y axis; a crosshair snaps to the nearest year and lists every series.
 */
export function lines(node, series, { ocrYears = new Set() } = {}) {
  clear(node);
  const pts = series.flatMap(s => s.points.filter(p => p.value !== null));
  if (!pts.length) { node.append(el('p', { class: 'empty' }, 'No values for this selection.')); return; }
  const years = [...new Set(pts.map(p => p.year))].sort((a, b) => a - b);
  const W = width(node), H = Math.min(380, Math.max(260, W * 0.45));
  const m = { l: 56, r: 120, t: 12, b: 28 };
  const y0 = Math.min(0, ...pts.map(p => p.value)), y1 = Math.max(...pts.map(p => p.value));
  const yt = niceTicks(y0, y1, 5);
  const ymin = Math.min(y0, yt[0]), ymax = Math.max(y1, yt[yt.length - 1]);
  const xmin = years[0], xmax = years[years.length - 1] === years[0] ? years[0] + 1 : years[years.length - 1];
  const X = yr => m.l + ((yr - xmin) / (xmax - xmin)) * (W - m.l - m.r);
  const Y = v => m.t + (1 - (v - ymin) / (ymax - ymin || 1)) * (H - m.t - m.b);
  const s = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, class: 'chart', role: 'img' });

  // scanned years are shaded so OCR figures never pass for verified ones
  for (const yr of years) {
    if (!ocrYears.has(yr)) continue;
    const half = (X(xmax) - X(xmin)) / Math.max(1, (xmax - xmin)) / 2;
    s.append(svg('rect', { x: X(yr) - half, y: m.t, width: half * 2, height: H - m.t - m.b, class: 'ocr-band' }));
  }
  for (const t of yt) {
    s.append(svg('line', { x1: m.l, x2: W - m.r, y1: Y(t), y2: Y(t), class: t === 0 ? 'axis' : 'grid' }));
    s.append(svg('text', { x: m.l - 8, y: Y(t) + 4, class: 'tick', 'text-anchor': 'end' }, fmtCompact(t)));
  }
  const step = Math.max(1, Math.ceil(years.length / Math.max(2, Math.floor((W - m.l - m.r) / 52))));
  years.forEach((yr, i) => {
    if (i % step && i !== years.length - 1) return;
    s.append(svg('text', { x: X(yr), y: H - 8, class: 'tick', 'text-anchor': 'middle' }, String(yr)));
  });

  const labels = [];
  for (const sr of series) {
    const p = sr.points.filter(q => q.value !== null).sort((a, b) => a.year - b.year);
    if (!p.length) continue;
    // break the line where a year is missing rather than drawing across the gap
    let d = '', prev = null;
    for (const q of p) {
      const gap = prev !== null && q.year - prev > 1;  // a missing edition is a gap, not a straight line
      d += `${d && !gap ? 'L' : 'M'}${X(q.year).toFixed(1)} ${Y(q.value).toFixed(1)}`;
      prev = q.year;
    }
    s.append(svg('path', { d, class: 'line', stroke: sr.color }));
    for (const q of p) s.append(svg('circle', { cx: X(q.year), cy: Y(q.value), r: p.length > 30 ? 2 : 3, fill: sr.color, class: 'dot' }));
    const last = p[p.length - 1];
    labels.push({ y: Y(last.value), x: X(last.year), text: sr.name, color: sr.color });
  }
  // direct labels at the line ends, nudged apart
  labels.sort((a, b) => a.y - b.y);
  for (let i = 1; i < labels.length; i++) if (labels[i].y - labels[i - 1].y < 13) labels[i].y = labels[i - 1].y + 13;
  if (series.length <= 6) for (const l of labels) {
    s.append(svg('text', { x: l.x + 8, y: l.y + 4, class: 'end-label' }, l.text.length > 16 ? `${l.text.slice(0, 15)}…` : l.text));
  }

  const hair = svg('line', { y1: m.t, y2: H - m.b, class: 'crosshair', visibility: 'hidden' });
  s.append(hair);
  const hit = svg('rect', { x: m.l, y: m.t, width: W - m.l - m.r, height: H - m.t - m.b, fill: 'transparent' });
  s.append(hit);
  const at = ev => {
    const r = s.getBoundingClientRect();
    const px = ((ev.clientX - r.left) / r.width) * W;
    const yr = years.reduce((a, b) => (Math.abs(X(b) - px) < Math.abs(X(a) - px) ? b : a));
    hair.setAttribute('x1', X(yr)); hair.setAttribute('x2', X(yr)); hair.setAttribute('visibility', 'visible');
    showTip(t => {
      t.append(el('div', { class: 'tip-title' }, `${yr}${ocrYears.has(yr) ? ' · OCR, unverified' : ''}`));
      for (const sr of series) {
        const q = sr.points.find(z => z.year === yr);
        if (q) tipRow(t, fmt(q.value), sr.name, sr.color);
      }
    }, ev);
  };
  hit.addEventListener('pointermove', at);
  hit.addEventListener('pointerleave', () => { hair.setAttribute('visibility', 'hidden'); hideTip(); });
  node.append(s);
}

/* ------------------------------------------------------------------- map */

const GEO_ALIAS = {
  'Odisha': 'Orissa', 'Uttarakhand': 'Uttaranchal', 'Andaman & Nicobar Islands': 'Andaman and Nicobar',
  'Jammu & Kashmir': 'Jammu and Kashmir', 'Dadra & Nagar Haveli': 'Dadra and Nagar Haveli', 'Daman & Diu': 'Daman and Diu',
};
let geoCache;
async function geo() {
  if (!geoCache) {
    const base = new URL('geo/', document.baseURI);
    geoCache = Promise.all([fetch(new URL('india-states.geojson', base)).then(r => r.json()), fetch(new URL('india-outline.geojson', base)).then(r => r.json())]);
  }
  return geoCache;
}

function projector(outline, W, H) {
  let lon0 = 180, lat0 = 90, lon1 = -180, lat1 = -90;
  const visit = c => {
    if (typeof c[0] === 'number') { lon0 = Math.min(lon0, c[0]); lon1 = Math.max(lon1, c[0]); lat0 = Math.min(lat0, c[1]); lat1 = Math.max(lat1, c[1]); return; }
    c.forEach(visit);
  };
  outline.features.forEach(f => visit(f.geometry.coordinates));
  const my = lat => (Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI) / 360)) * 180) / Math.PI;
  const k = Math.min((W - 8) / (lon1 - lon0), (H - 8) / (my(lat1) - my(lat0)));
  const ox = (W - k * (lon1 - lon0)) / 2, oy = (H - k * (my(lat1) - my(lat0))) / 2;
  return ([lon, lat]) => [ox + (lon - lon0) * k, oy + (my(lat1) - my(lat)) * k];
}

function pathOf(geometry, project) {
  const ring = r => r.map((c, i) => { const [x, y] = project(c); return `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`; }).join('') + 'Z';
  const polys = geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates;
  return polys.map(p => p.map(ring).join('')).join('');
}

/** States/UTs shaded by value on one sequential ramp. rows: [{name, value, raw}] with standard names. */
export async function choropleth(node, rows, { legend } = {}) {
  clear(node);
  const [states, outline] = await geo();
  const W = Math.min(width(node), 560), H = W * 1.08;
  const project = projector(outline, W, H);
  const byName = new Map();
  for (const r of rows) {
    if (r.value === null || r.value === undefined) continue;
    const names = r.name === 'Dadra & Nagar Haveli and Daman & Diu' ? ['Dadra and Nagar Haveli', 'Daman and Diu'] : [GEO_ALIAS[r.name] || r.name];
    for (const n of names) byName.set(n, r);
  }
  const vals = [...byName.values()].map(r => r.value).sort((a, b) => a - b);
  // trim the colour scale at the 5th and 95th percentile so one outlier does not flatten the rest
  const q = p => vals[Math.min(vals.length - 1, Math.max(0, Math.round(p * (vals.length - 1))))];
  const lo = q(0.05), hi = q(0.95);
  const s = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, class: 'chart map', role: 'img' });
  for (const f of outline.features) s.append(svg('path', { d: pathOf(f.geometry, project), class: 'land' }));
  for (const f of states.features) {
    const name = f.properties.NAME_1;
    const r = byName.get(name);
    const t = r ? (hi > lo ? (Math.min(hi, Math.max(lo, r.value)) - lo) / (hi - lo) : 0.5) : null;
    const p = svg('path', { d: pathOf(f.geometry, project), class: r ? 'state' : 'state none', fill: r ? seq(t) : null, tabindex: r ? 0 : null });
    p.addEventListener('pointermove', ev => showTip(tt => { if (r) tipRow(tt, fmt(r.value), r.label || r.name); else tt.append(el('div', {}, `${name}: not in this table`)); }, ev));
    p.addEventListener('pointerleave', hideTip);
    s.append(p);
  }
  node.append(s);
  if (legend) {
    clear(legend);
    const bar = el('div', { class: 'ramp' });
    for (let i = 1; i <= 7; i++) bar.append(el('span', { style: `background:var(--seq-${i})` }));
    legend.append(el('span', { class: 'muted' }, fmtCompact(lo)), bar, el('span', { class: 'muted' }, fmtCompact(hi)),
      el('span', { class: 'swatch-none' }), el('span', { class: 'muted' }, 'not reported / new boundary'));
  }
}

/* ---------------------------------------------------------------- quality */

/** Share of checked totals that match, per year, one row of dots per publication and tier. */
export function quality(node, rows) {
  clear(node);
  const W = width(node), m = { l: 120, r: 16, t: 8, b: 26 };
  const groups = [];
  for (const pub of ['cii', 'adsi', 'psi']) {
    for (const tier of ['text', 'ocr']) groups.push({ pub, tier });
  }
  const yrs = rows.map(r => r.year);
  const xmin = Math.min(...yrs), xmax = Math.max(...yrs);
  const rowH = 34, H = m.t + groups.length * rowH + m.b;
  const X = y => m.l + ((y - xmin) / (xmax - xmin)) * (W - m.l - m.r);
  const s = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, class: 'chart', role: 'img' });
  for (let y = Math.ceil(xmin / 10) * 10; y <= xmax; y += 10) {
    s.append(svg('line', { x1: X(y), x2: X(y), y1: m.t, y2: H - m.b, class: 'grid' }));
    s.append(svg('text', { x: X(y), y: H - 8, class: 'tick', 'text-anchor': 'middle' }, String(y)));
  }
  const names = { cii: 'Crime', adsi: 'ADSI', psi: 'Prisons' };
  groups.forEach((g, i) => {
    const cy = m.t + i * rowH + rowH / 2;
    s.append(svg('text', { x: m.l - 10, y: cy + 4, class: 'label', 'text-anchor': 'end' }, `${names[g.pub]} · ${g.tier === 'text' ? 'text/Excel' : 'OCR'}`));
    for (const r of rows.filter(z => z.publication === g.pub)) {
      const tot = +r[`checks_total_${g.tier}`], ok = +r[`checks_passed_${g.tier}`];
      if (!tot) continue;
      const share = ok / tot;
      const c = svg('circle', { cx: X(r.year), cy, r: 4 + Math.min(6, Math.log10(tot + 1) * 1.4), fill: share >= 0.98 ? css('--good') : share >= 0.8 ? css('--warning') : css('--critical'), class: 'qdot', tabindex: 0 });
      c.addEventListener('pointermove', ev => showTip(t => {
        t.append(el('div', { class: 'tip-title' }, `${names[g.pub]} ${r.year}`));
        tipRow(t, `${(100 * share).toFixed(1)}%`, `of ${tot.toLocaleString('en-IN')} checked totals match`);
        tipRow(t, String(r.tables), 'tables');
      }, ev));
      c.addEventListener('pointerleave', hideTip);
      s.append(c);
    }
  });
  node.append(s);
}
