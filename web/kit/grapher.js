/* SVG charts, hand rolled, in the manner of cpi.reclaimchennai.city's charts.js:
 * no charting library, the SVG sized to its box (viewBox = real width, so
 * nothing is scaled), hairline grids, labels de-collided, hover tooltips.
 *
 * Every chart is a pure function of its inputs. Animation is the caller's
 * job: it passes values interpolated between two years and calls again on
 * each frame. That keeps playback, scrubbing and video recording on one path,
 * and makes every recorded frame exactly what the screen showed.
 *
 *   lineChart   one line per category across the years, a marker at the year
 *   barRows     one bar per row (composition of a year, or a ranking of places)
 *   stackRows   stacked horizontal bars, by count or by share
 *   heatmap     category x year cells carrying the number and its share
 *   clocks      two 12-hour dials, day (06-18) and night (18-06), one wedge per 3 hours
 */

import { svg, clear, scaleLinear, ticks, fmtN, fmtPct, fmtShort, hover, esc, heatStep, inkOn, lerp } from './util.js?v=bbe340d7cd';

/* ------------------------------------------------------------------ utils */

function size(el, minH = 200) {
  const w = Math.max(300, el.parentElement?.clientWidth || 700);
  return { w, narrow: w < 620, tight: w < 430, minH };
}
function frame(el, w, h) {
  clear(el);
  el.setAttribute('viewBox', `0 0 ${w} ${h}`);
  el.setAttribute('width', w);
  el.setAttribute('height', h);
  el.style.width = '100%';
  el.style.height = 'auto';
  el.classList.add('chart');
}
export function emptyChart(el, text = 'Nothing published for this choice.') {
  const { w } = size(el);
  frame(el, w, 120);
  el.append(svg('text', { x: w / 2, y: 64, class: 'tick', 'text-anchor': 'middle' }, text));
}

function decollide(ys, gap, top, bottom) {
  const order = ys.map((y, i) => ({ i, y })).sort((a, b) => a.y - b.y);
  let prev = -Infinity;
  for (const o of order) { o.y = Math.max(o.y, prev + gap); prev = o.y; }
  const over = order.length ? order[order.length - 1].y - bottom : 0;
  if (over > 0) {
    let next = Infinity;
    for (let k = order.length - 1; k >= 0; k--) { order[k].y = Math.min(order[k].y - over, next - gap); next = order[k].y; }
  }
  const out = new Array(ys.length);
  for (const o of order) out[o.i] = Math.max(top, o.y);
  return out;
}

function fitText(node, full, maxW) {
  node.textContent = full;
  if (maxW <= 0 || node.getComputedTextLength() <= maxW) return;
  let lo = 1, hi = full.length;
  while (lo < hi) {
    const mid = Math.ceil((lo + hi) / 2);
    node.textContent = `${full.slice(0, mid).trimEnd()}…`;
    if (node.getComputedTextLength() <= maxW) lo = mid; else hi = mid - 1;
  }
  node.textContent = `${full.slice(0, lo).trimEnd()}…`;
}

/** A bar rounded only on its outward (right) end, as cpi's capsuleBar does vertically. */
function hbar(x, y, w, h, roundRight = true) {
  const r = Math.max(0, Math.min(h / 2, w / 2, 5));
  if (!roundRight || w < 2) return `M${x} ${y}h${Math.max(0, w)}v${h}h${-Math.max(0, w)}Z`;
  return `M${x} ${y}H${x + w - r}A${r} ${r} 0 0 1 ${x + w} ${y + r}V${y + h - r}A${r} ${r} 0 0 1 ${x + w - r} ${y + h}H${x}Z`;
}

/* ======================================================================
   lineChart
   ====================================================================== */

/**
 * xs: years. series: [{key, label, color, values: {year: v}, dash}].
 * pos: fractional index into xs for the year marker (or null).
 */
export function lineChart(el, { xs, series, pos = null, fmt = fmtN, yFmt = fmtShort, height, hl = null, unit = '', zeroBase = true }) {
  const { w, narrow } = size(el);
  const all = series.flatMap(s => xs.map(x => s.values[x]).filter(v => v != null && Number.isFinite(v)));
  if (!all.length) return emptyChart(el);
  const h = height || (narrow ? 280 : 340);
  const labelW = narrow ? 92 : 150;
  const m = { top: 18, right: labelW + 10, bottom: 28, left: 46 };
  frame(el, w, h);
  const lo = zeroBase ? 0 : Math.min(...all), hi = Math.max(...all) * 1.06 || 1;
  const x = scaleLinear([xs[0], xs[xs.length - 1]], [m.left, w - m.right]);
  const y = scaleLinear([lo, hi], [h - m.bottom, m.top]);
  for (const t of ticks(lo, hi, 5)) {
    el.append(svg('line', { x1: m.left, x2: w - m.right, y1: y(t), y2: y(t), class: 'grid-line' }));
    el.append(svg('text', { x: m.left - 7, y: y(t) + 3.5, class: 'tick', 'text-anchor': 'end' }, yFmt(t)));
  }
  el.append(svg('line', { x1: m.left, x2: w - m.right, y1: h - m.bottom, y2: h - m.bottom, class: 'axis-line' }));
  // x ticks: every year fits on a wide chart, otherwise every 2nd/5th, never touching
  const span = xs[xs.length - 1] - xs[0];
  const step = [1, 2, 5, 10].find(s => (span / s) * 34 < w - m.left - m.right) || 10;
  let last = -Infinity;
  for (const yr of xs) {
    if (yr % step && yr !== xs[0] && yr !== xs[xs.length - 1]) continue;
    if (x(yr) - last < 30) continue;
    last = x(yr);
    el.append(svg('text', { x: x(yr), y: h - m.bottom + 16, class: 'tick', 'text-anchor': 'middle' }, String(yr)));
  }
  // lines, broken at missing years
  const ends = [];
  series.forEach((s, i) => {
    let d = '', pen = false, lastPt = null;
    for (const yr of xs) {
      const v = s.values[yr];
      if (v == null || !Number.isFinite(v)) { pen = false; continue; }
      d += `${pen ? 'L' : 'M'}${x(yr).toFixed(1)} ${y(v).toFixed(1)}`;
      pen = true; lastPt = [yr, v];
    }
    const dim = hl && hl !== s.key;
    el.append(svg('path', { d, class: `series-line${dim ? ' dim' : ''}`, stroke: s.color, 'stroke-dasharray': s.dash || null, 'stroke-width': hl === s.key ? 2.6 : null }));
    // lone points (a year with no neighbours) still show
    xs.forEach((yr, k) => {
      const v = s.values[yr];
      if (v == null) return;
      const prev = s.values[xs[k - 1]], next = s.values[xs[k + 1]];
      if (prev == null && next == null) el.append(svg('circle', { cx: x(yr), cy: y(v), r: 3, fill: s.color, opacity: dim ? .25 : 1 }));
    });
    if (lastPt) ends.push({ s, y: y(lastPt[1]), v: lastPt[1], dim });
  });
  // end labels, pushed apart
  const ys = decollide(ends.map(e => e.y), 13, m.top, h - m.bottom);
  ends.forEach((e, i) => {
    const t = svg('text', { x: w - m.right + 8, y: ys[i] + 4, class: 'end-label', fill: e.s.color, opacity: e.dim ? .35 : 1 });
    el.append(t);
    fitText(t, e.s.label, labelW);
  });
  // year marker
  if (pos != null) {
    const i0 = Math.floor(pos), i1 = Math.min(xs.length - 1, i0 + 1), f = pos - i0;
    const yr = lerp(xs[i0], xs[i1], f);
    el.append(svg('line', { x1: x(yr), x2: x(yr), y1: m.top - 4, y2: h - m.bottom, class: 'year-mark' }));
    el.append(svg('text', { x: x(yr), y: m.top - 6, class: 'year-tag', 'text-anchor': 'middle' }, String(Math.round(yr))));
  }
  // hover: nearest year, every series' value
  const cross = svg('line', { y1: m.top, y2: h - m.bottom, class: 'crosshair', visibility: 'hidden' });
  el.append(cross);
  const hit = svg('rect', { x: m.left, y: m.top, width: w - m.left - m.right, height: h - m.top - m.bottom, class: 'hit' });
  el.append(hit);
  const near = ev => {
    const r = el.getBoundingClientRect();
    const px = ((ev.clientX - r.left) / r.width) * w;
    const yr = Math.round(x.invert(px));
    return xs.reduce((a, b) => (Math.abs(b - yr) < Math.abs(a - yr) ? b : a), xs[0]);
  };
  hover(hit, () => '');
  hit.addEventListener('pointermove', ev => {
    const yr = near(ev);
    cross.setAttribute('x1', x(yr)); cross.setAttribute('x2', x(yr)); cross.setAttribute('visibility', 'visible');
    const rows = series.map(s => ({ s, v: s.values[yr] })).filter(r => r.v != null).sort((a, b) => b.v - a.v);
    const tip = document.getElementById('tip');
    if (tip) {
      tip.innerHTML = `<div class="t">${yr}</div><dl>${rows.slice(0, 12).map(r =>
        `<dt><span class="sw" style="background:${r.s.color}"></span>${esc(r.s.label)}</dt><dd>${fmt(r.v)}${unit}</dd>`).join('')}</dl>`;
    }
  });
  hit.addEventListener('pointerleave', () => cross.setAttribute('visibility', 'hidden'));
}

/* ======================================================================
   barRows: composition of one year, or a ranking of places
   ====================================================================== */

/**
 * rows: [{key, label, value, color, hl, rank}] -- rank (fractional) places the
 * row; without it rows are drawn in the given order. total: for the % label.
 */
export function barRows(el, { rows, max, total = null, fmt = fmtN, label = r => r.label, rowH: rh, bigYear = null, unit = '' }) {
  const { w, narrow, tight } = size(el);
  if (!rows.length) return emptyChart(el);
  const rowH = rh || (narrow ? 26 : 28);
  const n = rows.length;
  const left = tight ? 104 : narrow ? 132 : 190;
  const valW = total ? 98 : 64;
  const m = { top: 6, right: valW + 6, bottom: 6, left };
  const h = m.top + n * rowH + m.bottom;
  frame(el, w, h);
  const mx = max || Math.max(...rows.map(r => r.value || 0), 1);
  const x = scaleLinear([0, mx], [m.left, w - m.right]);
  if (bigYear != null) el.append(svg('text', { x: w - m.right, y: h - 14, class: 'big-year', 'text-anchor': 'end' }, String(bigYear)));
  rows.forEach((r, i) => {
    const k = r.rank ?? i;
    if (k > n + 1) return;
    const y0 = m.top + k * rowH;
    const g = svg('g', { transform: `translate(0 ${y0.toFixed(2)})` });
    const t = svg('text', { x: m.left - 8, y: rowH / 2 + 4, class: `row-label${r.hl ? ' hl' : ''}`, 'text-anchor': 'end' });
    g.append(t);
    el.append(g);
    fitText(t, label(r), m.left - 12);
    const bw = Math.max(0, x(r.value || 0) - m.left);
    const bar = svg('path', { d: hbar(m.left, 4, bw, rowH - 8), fill: r.color || 'var(--series-1)', opacity: r.dim ? .35 : 1 });
    g.append(bar);
    const pct = total ? ` · ${fmtPct((100 * (r.value || 0)) / total)}` : '';
    g.append(svg('text', { x: m.left + bw + 6, y: rowH / 2 + 4, class: 'val-label' }, r.value == null ? 'not printed' : `${fmt(r.value)}${unit}${pct}`));
    hover(bar, () => `<div class="t">${esc(label(r))}</div><dl><dt>${esc(r.sub || 'Value')}</dt><dd>${r.value == null ? '–' : fmt(r.value) + unit}</dd>${total ? `<dt>Share</dt><dd>${fmtPct((100 * (r.value || 0)) / total)}</dd>` : ''}</dl>`);
  });
}

/* ======================================================================
   stackRows: stacked horizontal bars (age profile, composition per place)
   ====================================================================== */

/**
 * rows: [{key, label, values: [v per part], hl}]; parts: [{key, label, color}].
 * mode 'share' scales every bar to 100%; 'count' to the largest row.
 */
export function stackRows(el, { rows, parts, mode = 'share', fmt = fmtN, rowH: rh, bigYear = null }) {
  const { w, narrow, tight } = size(el);
  if (!rows.length) return emptyChart(el);
  const rowH = rh || (narrow ? 34 : 40);
  const left = tight ? 92 : narrow ? 112 : 150;
  const m = { top: 8, right: mode === 'count' ? 64 : 14, bottom: 26, left };
  const h = m.top + rows.length * rowH + m.bottom;
  frame(el, w, h);
  const totals = rows.map(r => r.values.reduce((a, b) => a + (b || 0), 0));
  const mx = mode === 'share' ? 100 : Math.max(...totals, 1);
  const x = scaleLinear([0, mx], [m.left, w - m.right]);
  for (const t of ticks(0, mx, narrow ? 4 : 5)) {
    el.append(svg('line', { x1: x(t), x2: x(t), y1: m.top, y2: h - m.bottom, class: 'grid-line' }));
    el.append(svg('text', { x: x(t), y: h - m.bottom + 15, class: 'tick', 'text-anchor': 'middle' }, mode === 'share' ? `${t}%` : fmtShort(t)));
  }
  rows.forEach((r, i) => {
    const y0 = m.top + (r.rank ?? i) * rowH;
    const t = svg('text', { x: m.left - 8, y: y0 + rowH / 2 + 4, class: `row-label${r.hl ? ' hl' : ''}`, 'text-anchor': 'end' });
    el.append(t);
    fitText(t, r.label, m.left - 12);
    const tot = totals[i] || 1;
    let acc = 0;
    r.values.forEach((v, k) => {
      const val = mode === 'share' ? (100 * (v || 0)) / tot : (v || 0);
      const x0 = x(acc), x1 = x(acc + val);
      acc += val;
      if (x1 - x0 <= 0.2) return;
      const seg = svg('rect', { x: x0, y: y0 + 5, width: Math.max(0, x1 - x0 - 1.5), height: rowH - 10, fill: parts[k].color, rx: 2 });
      el.append(seg);
      const share = (100 * (v || 0)) / tot;
      const txt = mode === 'share' ? `${share.toFixed(share < 10 ? 1 : 0)}%` : fmtShort(v);
      if (x1 - x0 > txt.length * 6.4 + 6) {
        el.append(svg('text', { x: (x0 + x1) / 2, y: y0 + rowH / 2 + 4, class: 'in-label', 'text-anchor': 'middle', fill: inkOn(parts[k].color), 'pointer-events': 'none' }, txt));
      }
      hover(seg, () => `<div class="t">${esc(r.label)}</div><div class="s">${esc(parts[k].label)}</div><dl><dt>Number</dt><dd>${fmt(v)}</dd><dt>Share</dt><dd>${fmtPct(share)}</dd></dl>`);
    });
    if (mode === 'count') el.append(svg('text', { x: x(totals[i]) + 6, y: y0 + rowH / 2 + 4, class: 'val-label' }, fmtShort(totals[i])));
  });
}

/* ======================================================================
   heatmap: category x year, each cell the number and its share
   ====================================================================== */

/**
 * rows: category labels; cols: years; get(r, c) -> {v, p} (p = share of the
 * column total, %) or null. hlCol: index of the year to outline.
 */
export function heatmap(el, { rows, cols, get, max, hlCol = null, fmt = fmtN, showPct = true, colLabel = String, onCol = null }) {
  const { w, narrow, tight } = size(el);
  if (!rows.length || !cols.length) return emptyChart(el);
  const left = tight ? 104 : narrow ? 130 : 180;
  const cellW = Math.max(narrow ? 40 : 46, (w - left - 8) / cols.length);
  const cellH = showPct ? 34 : 26;
  const width = Math.max(w, left + cellW * cols.length + 8);
  const m = { top: 26, left };
  const h = m.top + rows.length * cellH + 6;
  frame(el, width, h);
  el.style.width = width > w ? `${width}px` : '100%';
  cols.forEach((c, j) => {
    const t = svg('text', { x: m.left + j * cellW + cellW / 2, y: 16, class: 'tick', 'text-anchor': 'middle', 'font-weight': j === hlCol ? 760 : null, fill: j === hlCol ? 'var(--ink)' : null }, colLabel(c));
    if (onCol) { t.style.cursor = 'pointer'; t.addEventListener('click', () => onCol(j)); }
    el.append(t);
  });
  rows.forEach((r, i) => {
    const y0 = m.top + i * cellH;
    const t = svg('text', { x: m.left - 8, y: y0 + cellH / 2 + 4, class: 'row-label', 'text-anchor': 'end' });
    el.append(t);
    fitText(t, r, m.left - 12);
    cols.forEach((c, j) => {
      const cell = get(i, j);
      const x0 = m.left + j * cellW;
      const step = heatStep(cell?.v, max);
      const fill = `var(--heat-${step})`;
      const rect = svg('rect', { x: x0 + 1, y: y0 + 1, width: cellW - 2, height: cellH - 2, rx: 3, fill });
      el.append(rect);
      if (cell && cell.v != null) {
        const ink = inkOn(fill);
        el.append(svg('text', { x: x0 + cellW / 2, y: y0 + (showPct ? 15 : cellH / 2 + 4), class: 'cell-n', 'text-anchor': 'middle', fill: ink, 'pointer-events': 'none' }, cellW < 44 ? fmtShort(cell.v) : fmt(cell.v)));
        if (showPct && cell.p != null) el.append(svg('text', { x: x0 + cellW / 2, y: y0 + 27, class: 'cell-p', 'text-anchor': 'middle', fill: ink, 'pointer-events': 'none' }, fmtPct(cell.p, cell.p < 10 ? 1 : 0)));
        hover(rect, () => `<div class="t">${esc(r)}</div><div class="s">${esc(colLabel(c))}</div><dl><dt>Number</dt><dd>${fmt(cell.v)}</dd>${cell.p != null ? `<dt>Share of the year</dt><dd>${fmtPct(cell.p)}</dd>` : ''}</dl>`);
      }
    });
  });
  if (hlCol != null) {
    el.append(svg('rect', { x: m.left + hlCol * cellW + .5, y: m.top - 2, width: cellW - 1, height: rows.length * cellH + 3, rx: 4, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 1.6 }));
  }
}

/* ======================================================================
   clocks: day and night on two real 12-hour dials
   ====================================================================== */

/* The eight NCRB slots, split the way NCRB itself labels them: 06-18 is day,
 * 18-06 night. Each half is exactly twelve hours, so each fills one ordinary
 * clock face: on the day dial 06-09 runs from the 6 to the 9, 12-15 from the
 * 12 to the 3, and so on. */
const DIALS = [
  { key: 'day', title: 'Day', sub: '6 am – 6 pm', slots: ['06-09', '09-12', '12-15', '15-18'], color: 'var(--day)', soft: 'var(--day-soft)' },
  { key: 'night', title: 'Night', sub: '6 pm – 6 am', slots: ['18-21', '21-24', '00-03', '03-06'], color: 'var(--night)', soft: 'var(--night-soft)' },
];
// clock position (hours on a 12h face) where each slot starts
const START = { '06-09': 6, '09-12': 9, '12-15': 0, '15-18': 3, '18-21': 6, '21-24': 9, '00-03': 0, '03-06': 3 };
const SLOT_NAME = {
  '00-03': 'midnight – 3 am', '03-06': '3 am – 6 am', '06-09': '6 am – 9 am', '09-12': '9 am – noon',
  '12-15': 'noon – 3 pm', '15-18': '3 pm – 6 pm', '18-21': '6 pm – 9 pm', '21-24': '9 pm – midnight',
};

function polar(cx, cy, r, hours) {
  const a = (hours / 12) * 2 * Math.PI - Math.PI / 2;
  return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
}
function wedge(cx, cy, r0, r1, h0, h1) {
  const [a, b] = polar(cx, cy, r1, h0), [c, d] = polar(cx, cy, r1, h1);
  const [e, f] = polar(cx, cy, r0, h1), [g, k] = polar(cx, cy, r0, h0);
  return `M${a} ${b}A${r1} ${r1} 0 0 1 ${c} ${d}L${e} ${f}A${r0} ${r0} 0 0 0 ${g} ${k}Z`;
}

/**
 * values: {slot: v}; ghost: {slot: v} drawn as a dashed outline (a reference year);
 * max: the value a full-radius wedge stands for (shared across years so play shows change).
 */
export function clocks(el, { values, ghost = null, ghostLabel = '', max, mode = 'count', fmt = fmtN, unit = '', year = null }) {
  const { w, narrow } = size(el);
  const stacked = w < 560;
  const R = stacked ? Math.min(w / 2 - 26, 170) : Math.min((w - 60) / 4, 190);
  const h = stacked ? (R * 2 + 92) * 2 : R * 2 + 100;
  frame(el, w, h);
  const total = Object.values(values).reduce((a, b) => a + (b || 0), 0) || 1;
  const val = s => (mode === 'share' ? (100 * (values[s] || 0)) / total : values[s] || 0);
  const gtotal = ghost ? Object.values(ghost).reduce((a, b) => a + (b || 0), 0) || 1 : 1;
  const gval = s => (mode === 'share' ? (100 * (ghost[s] || 0)) / gtotal : ghost[s] || 0);
  const r0 = R * 0.26;
  const rad = v => r0 + (R - r0) * Math.sqrt(Math.max(0, v) / (max || 1));   // area-true
  DIALS.forEach((D, di) => {
    const cx = stacked ? w / 2 : w / 4 + (di ? w / 2 : 0);
    const cy = stacked ? 40 + R + di * (R * 2 + 92) : 44 + R;
    el.append(svg('circle', { cx, cy, r: R + 14, class: 'dial' }));
    for (let hr = 0; hr < 12; hr++) {
      const [x1, y1] = polar(cx, cy, R + 14, hr), [x2, y2] = polar(cx, cy, R + 7, hr);
      el.append(svg('line', { x1, y1, x2, y2, class: 'dial-tick' }));
      const [tx, ty] = polar(cx, cy, R + 27, hr);
      el.append(svg('text', { x: tx, y: ty + 4, class: 'dial-num', 'text-anchor': 'middle' }, String(hr === 0 ? 12 : hr)));
    }
    let half = 0;
    D.slots.forEach(s => {
      half += values[s] || 0;
      const h0 = START[s] + 0.06, h1 = START[s] + 3 - 0.06;
      const r = rad(val(s));
      const p = svg('path', { d: wedge(cx, cy, r0, Math.max(r0 + 1, r), h0, h1), fill: D.color, opacity: .92 });
      el.append(p);
      const sh = (100 * (values[s] || 0)) / total;
      hover(p, () => `<div class="t">${SLOT_NAME[s]}${year ? `, ${year}` : ''}</div><dl><dt>Number</dt><dd>${fmt(values[s])}${unit}</dd><dt>Share of the day</dt><dd>${fmtPct(sh)}</dd>${ghost ? `<dt>${esc(ghostLabel)}</dt><dd>${fmt(ghost[s])}${unit}</dd>` : ''}</dl>`);
      if (ghost && ghost[s] != null) {
        el.append(svg('path', { d: wedge(cx, cy, r0, Math.max(r0 + 1, rad(gval(s))), h0, h1), class: 'ghost', 'pointer-events': 'none' }));
      }
      // label at the wedge's middle hour, outside the wedge if it is small
      const mid = START[s] + 1.5;
      const inside = r - r0 > 46;
      const [lx, ly] = polar(cx, cy, inside ? (r0 + r) / 2 + 4 : r + 16, mid);
      const lab = svg('text', { x: lx, y: ly - 2, 'text-anchor': 'middle', class: 'cell-n', fill: inside ? inkOn(D.color) : 'var(--ink)', 'pointer-events': 'none' });
      lab.append(svg('tspan', { x: lx, dy: 0 }, mode === 'share' ? fmtPct(sh, 0) : fmt(values[s])));
      lab.append(svg('tspan', { x: lx, dy: 12, class: 'cell-p' }, mode === 'share' ? fmt(values[s]) : fmtPct(sh, 0)));
      el.append(lab);
    });
    el.append(svg('circle', { cx, cy, r: r0 - 2, fill: 'var(--surface)', stroke: 'var(--ring-2)' }));
    el.append(svg('text', { x: cx, y: cy - 2, class: 'dial-title', 'text-anchor': 'middle' }, D.title));
    el.append(svg('text', { x: cx, y: cy + 13, class: 'dial-sub', 'text-anchor': 'middle' }, fmtPct((100 * half) / total, 0)));
    el.append(svg('text', { x: cx, y: cy + R + 44, class: 'dial-sub', 'text-anchor': 'middle' }, `${D.sub} · ${fmt(half)}${unit}`));
  });
}

export const SLOT_LABELS = SLOT_NAME;
