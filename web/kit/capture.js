/* Snapshot (PNG) and recording (MP4, WebM fallback) of a chart card.
 *
 * After cpi.reclaimchennai.city's web/js/capture.js, which does this for its
 * map. A chart here is a small SVG, so every frame is assembled the simple way:
 * the SVG is serialised with its computed styles written in as presentation
 * attributes (a standalone SVG carries no stylesheet), rasterised, and painted
 * onto a canvas between a header and a credit band.
 *
 * Every saved file says what it is on its own: title, place, year, legend,
 * the source of the figures, and @reclaimchennai as its author.
 */

import { fixWebmDuration } from './webm.js?v=178d455447';
import { cssVar } from './util.js?v=178d455447';

const OUT_FPS = 30;
const CODECS = ['avc1.640028', 'avc1.4d0028', 'avc1.42003c', 'avc1.42E01E'];
const MAX_SECONDS = 30;
const W = 1080;
const PAD = 48;
const SITE = 'cpi.reclaimchennai.city/ncrb';
const AUTHOR = '@reclaimchennai';

const INLINE_PROPS = [
  'fill', 'fill-opacity', 'stroke', 'stroke-width', 'stroke-opacity', 'stroke-linejoin', 'stroke-linecap',
  'stroke-dasharray', 'opacity', 'font-family', 'font-size', 'font-weight', 'text-anchor', 'paint-order',
  'visibility', 'letter-spacing', 'dominant-baseline',
];
const KEEP_NONE = new Set(['fill', 'stroke']);

function inlineStyles(src, clone) {
  const a = [src, ...src.querySelectorAll('*')];
  const b = [clone, ...clone.querySelectorAll('*')];
  for (let i = 0; i < a.length; i++) {
    const n = b[i];
    if (n.namespaceURI !== 'http://www.w3.org/2000/svg') continue;
    const cs = getComputedStyle(a[i]);
    n.removeAttribute('style');
    n.removeAttribute('class');
    for (const p of INLINE_PROPS) {
      const v = cs.getPropertyValue(p);
      if (!v) continue;
      if (!KEEP_NONE.has(p) && (v === 'none' || v === 'normal' || v === 'auto')) continue;
      n.setAttribute(p, v);
    }
  }
}

function rasterise(svgEl) {
  const vb = svgEl.viewBox.baseVal;
  const clone = svgEl.cloneNode(true);
  inlineStyles(svgEl, clone);
  // inlineStyles strips class attributes, so the marks to drop are found on the live tree by position
  const live = [svgEl, ...svgEl.querySelectorAll('*')], copy = [clone, ...clone.querySelectorAll('*')];
  live.forEach((n, i) => { if (n.classList?.contains('big-year') || n.classList?.contains('hit') || n.classList?.contains('crosshair')) copy[i].setAttribute('data-drop', '1'); });
  clone.querySelectorAll('[data-drop]').forEach(n => n.remove());
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.setAttribute('width', vb.width);
  clone.setAttribute('height', vb.height);
  const xml = new XMLSerializer().serializeToString(clone);
  const img = new Image();
  img.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(xml)}`;
  return img.decode().then(() => ({ img, w: vb.width, h: vb.height }));
}

function wrap(ctx, text, maxW) {
  const words = String(text || '').split(/\s+/);
  const lines = [];
  let cur = '';
  for (const wd of words) {
    const t = cur ? `${cur} ${wd}` : wd;
    if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = wd; } else cur = t;
  }
  if (cur) lines.push(cur);
  return lines;
}

const FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif';

export function createCapture({ getSvgs, meta, name = 'ncrb-chart' }) {
  const out = document.createElement('canvas');
  let locked = null;
  let recording = null;

  async function drawFrame() {
    const info = meta();
    const shots = await Promise.all(getSvgs().filter(Boolean).map(rasterise));
    const ctx = out.getContext('2d');
    const inner = W - PAD * 2;
    // measure the header first: wrapped title and subtitle decide where the chart starts
    ctx.font = `700 40px ${FONT}`;
    const titleLines = wrap(ctx, info.title, inner - (info.year ? 190 : 0));
    ctx.font = `400 22px ${FONT}`;
    const subLines = wrap(ctx, info.subtitle, inner);
    const headH = 46 + titleLines.length * 48 + subLines.length * 30 + 18;
    const charts = shots.map(s => ({ ...s, scale: Math.min(2.2, inner / s.w) }));
    const chartH = charts.reduce((a, c) => a + c.h * c.scale + 14, 0);
    ctx.font = `500 19px ${FONT}`;
    let legendRows = 0;
    if (info.legend?.length) {
      let x = 0; legendRows = 1;
      for (const l of info.legend) {
        const lw = 26 + ctx.measureText(l.label).width + 24;
        if (x + lw > inner) { legendRows++; x = 0; }
        x += lw;
      }
    }
    const legendH = legendRows ? legendRows * 30 + 8 : 0;
    ctx.font = `400 17px ${FONT}`;
    const srcLines = wrap(ctx, info.source, inner);
    const footH = 34 + 32 + srcLines.length * 24 + 26;
    let H = Math.round(headH + chartH + legendH + footH);
    if (H % 2) H += 1;
    if (locked) H = locked;
    if (out.width !== W || out.height !== H) { out.width = W; out.height = H; }

    ctx.fillStyle = cssVar('--surface') || '#fff';
    ctx.fillRect(0, 0, W, H);
    const ink = cssVar('--ink') || '#111', muted = cssVar('--ink-muted') || '#777', ink2 = cssVar('--ink-2') || '#444';
    let y = 50;
    ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
    ctx.fillStyle = muted; ctx.font = `650 19px ${FONT}`;
    ctx.fillText(String(info.kicker || '').toUpperCase(), PAD, y);
    if (info.year != null) {
      ctx.textAlign = 'right'; ctx.fillStyle = cssVar('--critical') || '#c62f2f'; ctx.font = `760 76px ${FONT}`;
      ctx.fillText(String(info.year), W - PAD, y + 62);
      ctx.textAlign = 'left';
    }
    ctx.fillStyle = ink; ctx.font = `700 40px ${FONT}`;
    for (const l of titleLines) { y += 48; ctx.fillText(l, PAD, y); }
    ctx.fillStyle = ink2; ctx.font = `400 22px ${FONT}`;
    for (const l of subLines) { y += 30; ctx.fillText(l, PAD, y); }
    y += 22;
    for (const c of charts) {
      ctx.drawImage(c.img, PAD, y, c.w * c.scale, c.h * c.scale);
      y += c.h * c.scale + 14;
    }
    if (legendRows) {
      ctx.font = `500 19px ${FONT}`;
      let x = PAD; y += 8;
      for (const l of info.legend) {
        const lw = 26 + ctx.measureText(l.label).width + 24;
        if (x + lw > W - PAD) { x = PAD; y += 30; }
        ctx.fillStyle = l.color.startsWith('var(') ? cssVar(l.color.slice(4, -1)) : l.color;
        ctx.beginPath(); ctx.roundRect ? ctx.roundRect(x, y - 15, 18, 18, 4) : ctx.rect(x, y - 15, 18, 18); ctx.fill();
        ctx.fillStyle = ink2; ctx.fillText(l.label, x + 26, y);
        x += lw;
      }
      y += 22;
    }
    // credit band: who made it, where it lives, where the figures come from
    const fy = H - footH + 12;
    ctx.strokeStyle = cssVar('--ring-2') || '#ccc'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(PAD, fy); ctx.lineTo(W - PAD, fy); ctx.stroke();
    ctx.fillStyle = ink; ctx.font = `760 26px ${FONT}`;
    ctx.fillText(AUTHOR, PAD, fy + 40);
    ctx.textAlign = 'right'; ctx.fillStyle = muted; ctx.font = `550 19px ${FONT}`;
    ctx.fillText(SITE, W - PAD, fy + 40);
    ctx.textAlign = 'left'; ctx.font = `400 17px ${FONT}`;
    let sy = fy + 72;
    for (const l of srcLines) { ctx.fillText(l, PAD, sy); sy += 24; }
    return out;
  }

  function stamp() {
    const d = new Date(), p = n => String(n).padStart(2, '0');
    return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
  }
  async function deliver(blob, fname) {
    const file = new File([blob], fname, { type: blob.type });
    if (navigator.canShare?.({ files: [file] }) && matchMedia('(pointer: coarse)').matches) {
      try { await navigator.share({ files: [file] }); return 'shared'; } catch { /* fall through */ }
    }
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = fname; a.rel = 'noopener';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 20000);
    return 'saved';
  }

  async function snapshot() {
    const c = await drawFrame();
    const blob = await new Promise(r => c.toBlob(r, 'image/png'));
    if (!blob) throw new Error('could not encode the picture');
    return deliver(blob, `${name}-${stamp()}.png`);
  }

  async function pickCodec(width, height) {
    for (const codec of CODECS) {
      const config = { codec, width, height, bitrate: 8_000_000, framerate: OUT_FPS, avc: { format: 'avc' } };
      try { if ((await VideoEncoder.isConfigSupported(config)).supported) return config; } catch { /* next */ }
    }
    return null;
  }

  async function recordMp4({ frames, onFrame, onProgress }) {
    if (typeof VideoEncoder === 'undefined' || typeof VideoFrame === 'undefined' || typeof Mp4Muxer === 'undefined') return null;
    await onFrame(0);
    const first = await drawFrame();
    locked = first.height;
    const config = await pickCodec(first.width, first.height);
    if (!config) return null;
    const target = new Mp4Muxer.ArrayBufferTarget();
    const muxer = new Mp4Muxer.Muxer({ target, video: { codec: 'avc', width: first.width, height: first.height, frameRate: OUT_FPS }, fastStart: 'in-memory' });
    let failure = null, n = 0;
    const enc = new VideoEncoder({ output: (chunk, m) => muxer.addVideoChunk(chunk, m), error: e => { failure = e; } });
    enc.configure(config);
    for (let i = 0; i < frames && !recording.stop && !failure; i++) {
      if (i) await onFrame(i);
      const c = await drawFrame();
      const f = new VideoFrame(c, { timestamp: Math.round((i * 1e6) / OUT_FPS), duration: Math.round(1e6 / OUT_FPS) });
      enc.encode(f, { keyFrame: i % (OUT_FPS * 2) === 0 });
      f.close(); n++;
      onProgress?.(i / frames);
      while (enc.encodeQueueSize > 20 && !failure) await new Promise(r => setTimeout(r, 4));
    }
    try { await enc.flush(); muxer.finalize(); } catch (e) { failure = e; }
    try { enc.close(); } catch { /* closed */ }
    if (failure || n < 2) return null;
    return new Blob([target.buffer], { type: 'video/mp4' });
  }

  async function recordMediaRecorder({ frames, onFrame, onProgress }) {
    if (typeof MediaRecorder === 'undefined') throw new Error('this browser cannot record video');
    await onFrame(0);
    const first = await drawFrame();
    locked = first.height;
    const surface = document.createElement('canvas');
    surface.width = first.width; surface.height = first.height;
    const sctx = surface.getContext('2d');
    sctx.drawImage(out, 0, 0);
    const stream = surface.captureStream(OUT_FPS);
    const mime = ['video/mp4;codecs=avc1', 'video/mp4', 'video/webm;codecs=vp9', 'video/webm'].find(m => MediaRecorder.isTypeSupported?.(m)) || '';
    const rec = new MediaRecorder(stream, { ...(mime ? { mimeType: mime } : {}), videoBitsPerSecond: 6_000_000 });
    const chunks = [];
    rec.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
    const done = new Promise(res => { rec.onstop = res; });
    rec.start();
    const t0 = performance.now();
    for (let i = 0; i < frames && !recording.stop; i++) {
      if (i) await onFrame(i);
      await drawFrame();
      sctx.drawImage(out, 0, 0);
      onProgress?.(i / frames);
      const wait = t0 + ((i + 1) * 1000) / OUT_FPS - performance.now();
      if (wait > 0) await new Promise(r => setTimeout(r, wait));
    }
    const elapsed = performance.now() - t0;
    rec.stop(); await done;
    stream.getTracks().forEach(t => t.stop());
    if (!chunks.length) throw new Error('the recorder produced no frames');
    let blob = new Blob(chunks, { type: chunks[0].type || mime || 'video/webm' });
    if (blob.type.includes('webm')) blob = await fixWebmDuration(blob, elapsed);
    return blob;
  }

  async function record(opts) {
    recording = { stop: false };
    try {
      let blob = await recordMp4(opts);
      if (!blob) { locked = null; blob = await recordMediaRecorder(opts); }
      if (!blob?.size) throw new Error('the recorder produced no frames');
      return deliver(blob, `${name}-${stamp()}.${blob.type.includes('mp4') ? 'mp4' : 'webm'}`);
    } finally { recording = null; locked = null; }
  }

  return {
    snapshot, record, drawFrame,
    stop() { if (recording) recording.stop = true; },
    get recording() { return !!recording; },
    fps: OUT_FPS, maxSeconds: MAX_SECONDS,
  };
}
