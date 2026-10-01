/* Reading web/data/trends/: one dataset's index and one place's breakdown,
 * with lookups by label rather than by index. */

import { getJSON } from './util.js?v=bbe340d7cd';

const BASE = new URL('../data/trends/', import.meta.url).href;
const cache = new Map();

export function loadIndex(ds) {
  if (!cache.has(ds)) cache.set(ds, getJSON(`${BASE}${ds}/index.json`));
  return cache.get(ds);
}

/**
 * place(ds, key) -> {meta, name, years, get(cat, opts) -> {year: v}, total(year, opts), cats}
 * opts: {sex: 'Total', age: 'all ages', group: first}
 */
export async function place(ds, key) {
  const meta = await loadIndex(ds);
  const p = await getJSON(`${BASE}${ds}/${key}.json`);
  const idx = new Map();
  for (const [y, g, c, s, a, v] of p.rows) {
    const k = `${g}|${c}|${s}|${a}`;
    let o = idx.get(k);
    if (!o) idx.set(k, (o = {}));
    o[y] = v;
  }
  const gi = g => Math.max(0, g == null ? 0 : meta.groups.indexOf(g));
  const si = s => Math.max(0, s == null ? 0 : meta.sexes.indexOf(s));
  const ai = a => Math.max(0, meta.ages.indexOf(a ?? 'all ages'));
  const get = (cat, { sex, age, group } = {}) => idx.get(`${gi(group)}|${meta.cats.indexOf(cat)}|${si(sex)}|${ai(age)}`) || {};
  const cats = meta.cats.filter(c => c !== 'all ages');
  const years = [...new Set(p.rows.map(r => r[0]))].sort((a, b) => a - b);
  const total = (y, opts = {}) => {
    if (meta.cats.includes('all ages')) { const t = get('all ages', opts)[y]; if (t != null) return t; }
    let s = 0, any = false;
    for (const c of cats) { const v = get(c, opts)[y]; if (v != null) { s += v; any = true; } }
    return any ? s : null;
  };
  return { meta, name: p.place, type: p.type, years, get, total, cats };
}

/** Years that have at least one value under opts. */
export function yearsWith(P, opts = {}, cats = P.cats) {
  const ys = new Set();
  for (const c of cats) for (const y of Object.keys(P.get(c, opts))) ys.add(Number(y));
  return [...ys].sort((a, b) => a - b);
}
