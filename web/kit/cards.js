/* Controls and cards shared by the dashboard and the report: segmented
 * buttons, labelled dropdowns, switches, the year timeline (play, scrub,
 * smooth transitions), and a chart card with snapshot and record buttons. */

import { el, $, icon, ease } from './util.js?v=178d455447';
import { createCapture } from './capture.js?v=178d455447';

/* --------------------------------------------------------------- controls */

/** Pill segmented control. options: [{value, label, icon, disabled}] */
export function segmented({ options, value, onChange, label = '' }) {
  const root = el('div', { class: 'segmented', role: 'group', 'aria-label': label });
  let cur = value;
  const paint = () => [...root.children].forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === String(cur))));
  const build = opts => {
    root.innerHTML = '';
    for (const o of opts) {
      const b = el('button', { type: 'button', dataset: { v: o.value }, disabled: o.disabled || null }, `${o.icon ? icon(o.icon) : ''}<span>${o.label}</span>`);
      b.addEventListener('click', () => { if (String(cur) === String(o.value)) return; cur = o.value; paint(); onChange?.(o.value); });
      root.append(b);
    }
    paint();
  };
  build(options);
  return { el: root, get value() { return cur; }, set(v) { cur = v; paint(); }, options(opts, v) { if (v !== undefined) cur = v; build(opts); } };
}

/** A dropdown in cpi's pill field. options: [{value, label}] or groups [{group, options}] */
export function select({ options, value, onChange, label = '', lead = null, small = '' }) {
  const wrap = el('label', { class: 'field' });
  wrap.innerHTML = `${lead ? icon(lead, 'ic-lead') : ''}${small ? `<span class="lab">${small}</span>` : ''}<span class="sr-only">${label}</span><select></select>${icon('chevron-down', 'chev')}`;
  const s = wrap.querySelector('select');
  const fill = (opts, v) => {
    s.innerHTML = '';
    for (const o of opts) {
      if (o.group) {
        const g = el('optgroup', { label: o.group });
        for (const x of o.options) g.append(el('option', { value: x.value }, x.label));
        s.append(g);
      } else s.append(el('option', { value: o.value }, o.label));
    }
    if (v !== undefined) s.value = String(v);
  };
  fill(options, value);
  s.addEventListener('change', () => onChange?.(s.value));
  return { el: wrap, select: s, get value() { return s.value; }, set(v) { s.value = String(v); }, options: fill };
}

/** On/off switch. */
export function toggle({ label, value = false, onChange }) {
  const b = el('button', { type: 'button', class: 'switch', role: 'switch', 'aria-checked': String(value) }, `<span class="knob"></span><span>${label}</span>`);
  let cur = value;
  b.addEventListener('click', () => { cur = !cur; b.setAttribute('aria-checked', String(cur)); onChange?.(cur); });
  return { el: b, get value() { return cur; }, set(v) { cur = v; b.setAttribute('aria-checked', String(v)); } };
}

/* --------------------------------------------------------------- timeline */

/**
 * Years on a slider, with play. `pos` is a fractional index into `years`, so
 * everything listening can draw the in-between frames of a transition.
 * Listeners are called on every frame with (pos); `settled` is true once the
 * movement has stopped.
 */
export class Timeline {
  constructor({ years = [], speed = 1.1 } = {}) {
    this.years = years;
    this.pos = Math.max(0, years.length - 1);
    this.speed = speed;               // years per second while playing
    this.listeners = new Set();
    this.playing = false;
    this.root = el('div', { class: 'timeline' });
    this.root.innerHTML = `<div class="tl-row">
        <button class="ctl tl-play" type="button" aria-label="Play through the years" aria-pressed="false">${icon('play')}</button>
        <input type="range" class="tl-slider" min="0" max="0" step="1" value="0" aria-label="Year">
        <output class="tl-year num"></output>
      </div><div class="tl-scale num"><span class="tl-first"></span><span class="tl-last"></span></div>`;
    this.btn = $('.tl-play', this.root);
    this.slider = $('.tl-slider', this.root);
    this.out = $('.tl-year', this.root);
    this.btn.addEventListener('click', () => (this.playing ? this.stop() : this.play()));
    this.slider.addEventListener('input', () => { this.stop(); this.goto(Number(this.slider.value), true); });
    this.setYears(years);
  }
  setYears(years, keepYear = true) {
    const yr = this.year;
    this.years = years;
    this.slider.max = String(Math.max(0, years.length - 1));
    $('.tl-first', this.root).textContent = years[0] ?? '';
    $('.tl-last', this.root).textContent = years[years.length - 1] ?? '';
    const k = keepYear && yr != null ? years.indexOf(yr) : -1;
    this.pos = k >= 0 ? k : Math.max(0, years.length - 1);
    this.root.hidden = years.length < 2;
    this.paint();
  }
  get year() { return this.years[Math.round(this.pos)]; }
  get index() { return Math.round(this.pos); }
  on(fn) { this.listeners.add(fn); return () => this.listeners.delete(fn); }
  emit(settled = false) { for (const f of this.listeners) f(this.pos, settled); }
  paint() {
    this.slider.value = String(Math.round(this.pos));
    this.out.textContent = this.years.length ? String(this.year) : '';
  }
  set(pos, settled = true) { this.pos = Math.max(0, Math.min(this.years.length - 1, pos)); this.paint(); this.emit(settled); }
  /** Move to index k, sliding there over a short transition. */
  goto(k, animate = true) {
    cancelAnimationFrame(this.raf);
    const from = this.pos, to = Math.max(0, Math.min(this.years.length - 1, k));
    if (!animate || from === to || matchMedia('(prefers-reduced-motion: reduce)').matches) { this.set(to); return; }
    const t0 = performance.now(), dur = Math.min(700, 260 + 90 * Math.abs(to - from));
    const step = now => {
      const f = Math.min(1, (now - t0) / dur);
      this.pos = from + (to - from) * ease(f);
      this.paint(); this.emit(f >= 1);
      if (f < 1) this.raf = requestAnimationFrame(step);
    };
    this.raf = requestAnimationFrame(step);
  }
  gotoYear(y, animate = true) { const k = this.years.indexOf(Number(y)); if (k >= 0) this.goto(k, animate); }
  play() {
    if (this.years.length < 2) return;
    cancelAnimationFrame(this.raf);
    this.playing = true;
    this.btn.setAttribute('aria-pressed', 'true');
    this.btn.setAttribute('aria-label', 'Pause');
    this.btn.querySelector('use').setAttribute('href', '#i-pause');
    if (this.pos >= this.years.length - 1) this.pos = 0;
    let last = performance.now();
    const step = now => {
      if (!this.playing) return;
      const dt = Math.min(250, now - last); last = now;
      const p = this.pos + (dt / 1000) * this.speed;
      if (p >= this.years.length - 1) { this.set(this.years.length - 1); this.stop(); return; }
      this.pos = p; this.paint(); this.emit(false);
      this.raf = requestAnimationFrame(step);
    };
    this.raf = requestAnimationFrame(step);
  }
  stop() {
    if (!this.playing) return;
    this.playing = false;
    cancelAnimationFrame(this.raf);
    this.btn.setAttribute('aria-pressed', 'false');
    this.btn.setAttribute('aria-label', 'Play through the years');
    this.btn.querySelector('use').setAttribute('href', '#i-play');
    this.set(Math.round(this.pos));
  }
}

/** Interpolated value of a {year: v} map at a fractional index into years. */
export function at(values, years, pos) {
  if (!values) return null;
  const i0 = Math.floor(pos), i1 = Math.min(years.length - 1, i0 + 1), f = pos - i0;
  const a = values[years[i0]], b = values[years[i1]];
  if (a == null && b == null) return null;
  if (a == null) return f > .5 ? b : null;
  if (b == null) return f < .5 ? a : null;
  return a + (b - a) * f;
}

/* ------------------------------------------------------------------- card */

/**
 * A chart card: head (kicker, title, subtitle, capture buttons), toolbar,
 * legend, body holding one or more SVGs, a note, flash and toast.
 * `capture`: { meta: () => ({...}), record: { timeline, render } } wires the buttons.
 */
export function card(parent, { id, kicker = '', title = '', sub = '', svgs = 1, snap = true, rec = false }) {
  const root = el('section', { class: 'card', id });
  root.innerHTML = `<div class="card-head"><div class="titles">${kicker ? `<div class="kicker"></div>` : ''}<h2></h2><p></p></div>
    <div class="card-tools">${snap ? `<button type="button" class="snap" aria-label="Save a picture of this chart" title="Save a picture">${icon('camera')}</button>` : ''}
    ${rec ? `<button type="button" class="rec" aria-label="Record this chart through the years" aria-pressed="false" title="Record a video through the years">${icon('video')}</button>` : ''}</div></div>
    <div class="toolbar"></div><div class="legend"></div><div class="card-body"></div>
    <div class="flash" aria-hidden="true"></div><p class="toast" role="status" hidden></p>`;
  const body = $('.card-body', root);
  const svgEls = [];
  for (let i = 0; i < svgs; i++) {
    const wrap = el('div', { class: 'chart-wrap' });
    const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('class', 'chart'); s.setAttribute('role', 'img');
    wrap.append(s); body.append(wrap); svgEls.push(s);
  }
  const note = el('p', { class: 'note' });
  body.append(note);
  parent.append(root);
  const c = {
    el: root, body, svgs: svgEls, svg: svgEls[0], note,
    toolbar: $('.toolbar', root), legend: $('.legend', root),
    set(t = {}) {
      if (t.kicker !== undefined && $('.kicker', root)) $('.kicker', root).textContent = t.kicker;
      if (t.title !== undefined) $('h2', root).textContent = t.title;
      if (t.sub !== undefined) $('.titles p', root).textContent = t.sub;
      if (t.note !== undefined) { note.innerHTML = t.note; note.hidden = !t.note; }
      return c;
    },
    toast(text) {
      const n = $('.toast', root); n.textContent = text; n.hidden = false;
      clearTimeout(c._t); c._t = setTimeout(() => { n.hidden = true; }, 3200);
    },
    flash() { const f = $('.flash', root); f.classList.remove('on'); void f.offsetWidth; f.classList.add('on'); },
    setLegend(items) {
      c.legendItems = items;
      c.legend.innerHTML = items.map(i => `<span class="legend-item"><span class="swatch${i.line ? ' line' : ''}" style="background:${i.color}"></span>${i.label}</span>`).join('');
    },
    legendItems: [],
  };
  c.set({ kicker, title, sub, note: '' });
  return c;
}

/**
 * Wire a card's camera and video buttons.
 * meta() -> {kicker, title, subtitle, year, legend, source}
 * record: {timeline, render(pos)} -- render draws the card at a fractional year, synchronously.
 */
export function bindCapture(c, { meta, record = null, name }) {
  const cap = createCapture({ getSvgs: () => c.svgs.filter(s => s.childNodes.length), meta: () => ({ legend: c.legendItems, ...meta() }), name });
  $('.snap', c.el)?.addEventListener('click', async () => {
    c.flash();
    try { c.toast((await cap.snapshot()) === 'shared' ? 'Picture shared.' : 'Picture saved to your downloads.'); }
    catch (e) { c.toast(`Could not save the picture: ${e.message}`); }
  });
  const btn = $('.rec', c.el);
  if (!btn || !record) return cap;
  btn.addEventListener('click', async () => {
    if (cap.recording) { cap.stop(); return; }
    const tl = record.timeline;
    if (tl.years.length < 2) { c.toast('Only one year here: nothing to record.'); return; }
    tl.stop();
    // from the year shown to the last; from the start if already at the end
    const from = tl.index >= tl.years.length - 1 ? 0 : tl.index;
    const span = tl.years.length - 1 - from;
    const perYear = Math.max(6, Math.min(24, Math.floor((cap.maxSeconds * cap.fps - 45) / span)));
    const frames = span * perYear + 45;           // a 1.5 s hold on the last year
    const pos0 = tl.pos;
    btn.setAttribute('aria-pressed', 'true');
    btn.querySelector('use').setAttribute('href', '#i-stop');
    c.toast(`Recording ${tl.years[from]}–${tl.years[tl.years.length - 1]}…`);
    let lastPct = -1;
    try {
      const how = await cap.record({
        frames,
        onFrame: async i => { const p = Math.min(tl.years.length - 1, from + i / perYear); tl.pos = p; tl.paint(); record.render(p); },
        onProgress: f => { const pct = Math.round(f * 100); if (pct % 10 === 0 && pct !== lastPct) { lastPct = pct; c.toast(`Recording… ${pct}%`); } },
      });
      c.toast(how === 'shared' ? 'Video shared.' : 'Video saved to your downloads.');
    } catch (e) { c.toast(`Could not record: ${e.message}`); }
    finally {
      btn.setAttribute('aria-pressed', 'false');
      btn.querySelector('use').setAttribute('href', '#i-video');
      tl.set(Math.round(pos0));
    }
  });
  return cap;
}
