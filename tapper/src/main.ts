import './style.css';
import SONGS from './songs.json';
import { Player, peaks, IS_IOS, HAS_AUDIO_SESSION } from './audio';

type TType = 'tap' | 'drum' | 'vocal';
interface Tap { id: number; t_raw: number; t: number; type: TType; edited?: boolean; }
interface Song { id: string; title: string; album: string; accent: string; duration: number | null; bpm: number | null; period: number | null; beat0: number | null; barBeat: number; gridSource: string | null; local?: boolean; }

const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const LS = 'nj-tapper:v1:';
const player = new Player();
const S = {
  song: null as Song | null, taps: [] as Tap[], sel: new Set<number>(), nextId: 1,
  undo: [] as string[], redo: [] as string[],
  view: { t0: 0, pps: 120 }, grid: { period: 0, beat0: 0, barBeat: 0 },
  calibMs: +(localStorage.getItem(LS + 'calib') ?? 0) || 0,
  A: null as number | null, B: null as number | null,
  rec: null as null | { mode: 'rec' | 'ab'; pass: Tap[]; passStart: number },
  pk: null as ReturnType<typeof peaks> | null, loading: false,
};
const audioUrl = (id: string) => new URL(`../audio/${id}.mp3`, location.href).toString();
const toast = (m: string) => { const t = $('toast'); t.textContent = m; t.classList.add('show'); clearTimeout((toast as any).h); (toast as any).h = setTimeout(() => t.classList.remove('show'), 1800); };
const fmt = (t: number, ms = true) => { const s = Math.max(0, t); const m = Math.floor(s / 60); const r = s - m * 60; return `${m}:${(ms ? r.toFixed(3) : Math.floor(r).toString()).padStart(ms ? 6 : 2, '0')}`; };

// ---------------- song picker ----------------
const songSel = $<HTMLSelectElement>('song');
for (const s of SONGS as Song[]) { const o = document.createElement('option'); o.value = s.id; o.textContent = `${s.title} · ${s.album}`; songSel.append(o); }
songSel.onchange = () => void loadSong((SONGS as Song[]).find(s => s.id === songSel.value)!);
$<HTMLInputElement>('localfile').onchange = async e => {
  const f = (e.target as HTMLInputElement).files?.[0]; if (!f) return;
  const id = 'local:' + f.name.replace(/\s+/g, '_').slice(0, 60);
  const o = document.createElement('option'); o.value = id; o.textContent = `📁 ${f.name}`; songSel.append(o); songSel.value = id;
  await loadSong({ id, title: f.name, album: '本地文件', accent: '#8a5cf6', duration: null, bpm: null, period: null, beat0: null, barBeat: 0, gridSource: null, local: true }, f);
};

async function loadSong(s: Song, file?: File) {
  stopAll(); S.loading = true; setStatus('加载音频…');
  try {
    const buf = file ? await file.arrayBuffer() : await (await fetch(audioUrl(s.id))).arrayBuffer();
    // game songs: the <audio> element (slow playback) streams the real URL; blob: only for local files
    await player.load(buf, file ? URL.createObjectURL(file) : audioUrl(s.id));
  } catch (e) { setStatus('音频加载失败：' + (e as Error).message); S.loading = false; return; }
  S.song = { ...s, duration: player.duration };
  const saved = JSON.parse(localStorage.getItem(LS + 'grid:' + s.id) ?? 'null');
  S.grid = { period: saved?.period ?? s.period ?? 0, beat0: saved?.beat0 ?? s.beat0 ?? 0, barBeat: saved?.barBeat ?? s.barBeat ?? 0 };
  $<HTMLInputElement>('bpm').value = S.grid.period ? (60 / S.grid.period).toFixed(3) : '';
  $<HTMLInputElement>('beat0').value = S.grid.period ? S.grid.beat0.toFixed(3) : '';
  S.pk = peaks(player.buffer!);
  const st = JSON.parse(localStorage.getItem(LS + 'song:' + s.id) ?? 'null');
  S.taps = (st?.taps ?? []).map((t: Tap, i: number) => ({ ...t, id: i + 1 })); S.nextId = S.taps.length + 1; S.sel.clear(); S.undo = []; S.redo = [];
  S.A = st?.A ?? null; S.B = st?.B ?? null;
  S.view.t0 = 0; S.view.pps = Math.max(40, Math.min(400, tl.clientWidth / 8));
  localStorage.setItem(LS + 'last', s.id);
  S.loading = false; updateInfo(); setStatus(`已加载 ${s.title}（${fmt(player.duration, false)}）· 已有 ${S.taps.length} 个点`); draw();
}
function updateInfo() {
  const s = S.song; if (!s) return;
  $('info').textContent = S.grid.period ? `${(60 / S.grid.period).toFixed(3)} BPM · 第一拍 ${S.grid.beat0.toFixed(3)} s · ${s.gridSource === 'chart' ? '来自关卡谱面' : s.gridSource === 'analysis' ? '来自音频分析' : '手动'}` : '未知 BPM（可在 ⚙ 里填写）';
  $('tdur').textContent = '/ ' + fmt(player.duration, false);
}
const gridInput = () => {
  const b = parseFloat($<HTMLInputElement>('bpm').value), z = parseFloat($<HTMLInputElement>('beat0').value);
  if (b > 20 && b < 400) { S.grid.period = 60 / b; S.grid.beat0 = isFinite(z) ? z : 0; if (S.song) { S.song.gridSource = 'manual'; localStorage.setItem(LS + 'grid:' + S.song.id, JSON.stringify(S.grid)); } }
  updateInfo(); draw();
};
$('bpm').onchange = gridInput; $('beat0').onchange = gridInput;

// ---------------- history / save ----------------
const snap = () => JSON.stringify(S.taps);
function commit(before: string) { S.undo.push(before); if (S.undo.length > 300) S.undo.shift(); S.redo = []; save(); }
function restore(js: string) { S.taps = JSON.parse(js); S.nextId = Math.max(0, ...S.taps.map(t => t.id)) + 1; S.sel = new Set([...S.sel].filter(id => S.taps.some(t => t.id === id))); save(); draw(); }
function undo() { const u = S.undo.pop(); if (u === undefined) return; S.redo.push(snap()); restore(u); toast('已撤销'); }
function redo() { const r = S.redo.pop(); if (r === undefined) return; S.undo.push(snap()); restore(r); toast('已重做'); }
let saveT = 0;
function save() {
  clearTimeout(saveT); saveT = window.setTimeout(() => { if (!S.song) return;
    localStorage.setItem(LS + 'song:' + S.song.id, JSON.stringify({ taps: S.taps.map(({ id, ...r }) => r), A: S.A, B: S.B, updated: Date.now() }));
    $('saveinfo').textContent = `已自动保存 · ${S.taps.length} 个点 · ${new Date().toLocaleTimeString()}`; }, 300);
}
const sortTaps = () => S.taps.sort((a, b) => a.t - b.t);
const mkTap = (t_raw: number, type: TType, edited = false): Tap => ({ id: S.nextId++, t_raw: +t_raw.toFixed(4), t: +(t_raw - S.calibMs / 1000).toFixed(4), type, ...(edited ? { edited } : {}) });
function setT(tp: Tap, t: number) { tp.t = +Math.max(0, t).toFixed(4); tp.t_raw = +(tp.t + S.calibMs / 1000).toFixed(4); tp.edited = true; }

// ---------------- transport ----------------
const setStatus = (m: string, live = false) => { const e = $('status'); e.textContent = m; e.classList.toggle('live', live); };
async function togglePlay() { if (!S.song) return; player.unlock(); if (player.playing) stopAll(); else { if (!player.mediaPath && !player.readyNow) await player.ready(); player.play(player.position >= player.duration - 0.05 ? 0 : player.position); clickCursor = -1; } syncButtons(); }
function stopAll() {
  if (S.rec) finishRec(); player.stop(); syncButtons();
}
player.onEnded = () => { if (S.rec) finishRec(); syncButtons(); draw(); };
$('play').onclick = () => void togglePlay();
$('tostart').onclick = () => { player.seek(0); S.view.t0 = 0; draw(); };
$<HTMLSelectElement>('rate').onchange = e => { const was = player.playing, p = player.position; player.stop(); player.rate = +(e.target as HTMLSelectElement).value; player.seek(p); if (was) player.play(p); };
$<HTMLInputElement>('keeppitch').onchange = e => { const was = player.playing, p = player.position; player.stop(); player.keepPitch = (e.target as HTMLInputElement).checked; player.seek(p); if (was) player.play(p); };
function syncButtons() { $('play').textContent = player.playing ? '⏸' : '▶'; $('rec').classList.toggle('on', S.rec?.mode === 'rec'); $('recab').classList.toggle('on', S.rec?.mode === 'ab'); }

// ---------------- recording ----------------
const dual = () => $<HTMLInputElement>('dual').checked;
$('dual').onchange = () => $('pad').classList.toggle('dual', dual());
async function startRec(mode: 'rec' | 'ab') {
  if (!S.song) return;
  if (mode === 'ab' && (S.A === null || S.B === null || S.B - S.A < 0.3)) { toast('请先设置 A 和 B（或框选后点「选区→A–B」）'); return; }
  player.unlock(); if (!player.mediaPath && !player.readyNow) await player.ready(); player.stop();
  const from = mode === 'ab' ? Math.max(0, S.A! - 1.5) : player.position;
  S.rec = { mode, pass: [], passStart: from }; player.play(from); clickCursor = -1; syncButtons();
  setStatus(mode === 'ab' ? `重录 A–B：循环中，每一遍打完会替换 ${fmt(S.A!)}–${fmt(S.B!)} 内的点` : '录制中… 跟着音乐打点（Esc 停止）', true);
}
$('rec').onclick = () => (S.rec ? stopAll() : void startRec('rec'));
$('recab').onclick = () => (S.rec ? stopAll() : void startRec('ab'));
$('stop').onclick = stopAll;
function finishPass() {
  const r = S.rec!; if (r.mode !== 'ab') return;
  const inRange = r.pass.filter(t => t.t >= S.A! - 0.03 && t.t <= S.B! + 0.03);
  if (inRange.length) {
    const before = snap(); S.taps = S.taps.filter(t => t.t < S.A! - 0.03 || t.t > S.B! + 0.03).concat(inRange); sortTaps(); commit(before);
    toast(`A–B 已替换为本遍的 ${inRange.length} 个点`);
  }
  r.pass = [];
}
function finishRec() {
  const r = S.rec!; S.rec = null;
  if (r.mode === 'rec' && r.pass.length) { const before = JSON.stringify(S.taps.filter(t => !r.pass.includes(t))); commit(before); }
  else if (r.mode === 'ab') finishPass();
  setStatus(`已停止 · 共 ${S.taps.length} 个点`); syncButtons(); draw();
}
function recordTap(perf: number, type: TType) {
  flashPad(type);
  if (!S.rec || !player.playing) return;
  const t_raw = player.songAtPerf(perf); const tp = mkTap(t_raw, type);
  S.rec.pass.push(tp);
  if (S.rec.mode === 'rec') { S.taps.push(tp); sortTaps(); }
  setStatus(`录制中… ${S.rec.mode === 'rec' ? '共 ' + S.taps.length : '本遍 ' + S.rec.pass.length} 个点 · 最近 ${fmt(tp.t)}`, true);
}
function flashPad(type: TType) {
  const pad = $('pad'); const el = dual() ? pad.querySelector(type === 'drum' ? '.half.l' : '.half.r')! : pad;
  el.classList.remove('hit'); void (el as HTMLElement).offsetWidth; el.classList.add('hit');
}
const pad = $('pad');
pad.addEventListener('pointerdown', e => { e.preventDefault(); const r = pad.getBoundingClientRect(); const type: TType = dual() ? (e.clientX - r.left < r.width / 2 ? 'drum' : 'vocal') : 'tap';
  if (calib.active) calib.tap(e.timeStamp); else recordTap(e.timeStamp, type); });

// ---------------- keyboard ----------------
const LEFT = new Set(['KeyF', 'KeyD', 'KeyS', 'KeyA', 'KeyG', 'KeyV', 'KeyC', 'KeyX', 'KeyZ']);
// text-like fields keep their keys; buttons / checkboxes / selects never react to Space (it is play or a tap here)
const isTextField = (el: EventTarget | null) => { const t = el as HTMLElement | null; if (!t || !t.tagName) return false;
  if (t.tagName === 'TEXTAREA' || t.isContentEditable) return true;
  return t.tagName === 'INPUT' && !['checkbox', 'radio', 'button', 'submit', 'file', 'range'].includes((t as HTMLInputElement).type); };
const sheetOpen = () => !!document.querySelector('dialog.sheet[open]');
window.addEventListener('keydown', e => {
  if (calib.active) { if (e.code === 'Escape') return; e.preventDefault(); if (!e.repeat) calib.tap(e.timeStamp); return; }
  if (S.rec) {
    e.preventDefault();
    if (document.activeElement instanceof HTMLElement && document.activeElement !== document.body) document.activeElement.blur();
    if (e.code === 'Escape' || e.code === 'Enter') { stopAll(); return; }
    if (e.repeat || e.metaKey || e.ctrlKey) return;
    recordTap(e.timeStamp, dual() ? (LEFT.has(e.code) ? 'drum' : 'vocal') : 'tap'); return;
  }
  if (isTextField(e.target) || sheetOpen() || $<HTMLDialogElement>('calibdlg').open) return;
  const mod = e.ctrlKey || e.metaKey;
  if (mod && e.code === 'KeyZ') { e.preventDefault(); e.shiftKey ? redo() : undo(); }
  else if (mod && e.code === 'KeyY') { e.preventDefault(); redo(); }
  else if (mod && e.code === 'KeyA') { e.preventDefault(); S.sel = new Set(S.taps.map(t => t.id)); draw(); }
  else if (e.code === 'Space') { e.preventDefault(); void togglePlay(); }
  else if (e.code === 'Delete' || e.code === 'Backspace') { e.preventDefault(); delSel(); }
  else if (e.code === 'BracketLeft') setA(player.position); else if (e.code === 'BracketRight') setB(player.position);
  else if ((e.code === 'ArrowLeft' || e.code === 'ArrowRight') && S.sel.size) { e.preventDefault(); const d = (e.code === 'ArrowLeft' ? -1 : 1) * (e.altKey ? 0.001 : 0.005); const before = snap(); for (const t of S.taps) if (S.sel.has(t.id)) setT(t, t.t + d); sortTaps(); commit(before); draw(); }
  else if (e.code === 'Escape') { S.sel.clear(); draw(); }
});
function delSel() { if (!S.sel.size) return; const before = snap(); const n = S.sel.size; S.taps = S.taps.filter(t => !S.sel.has(t.id)); S.sel.clear(); commit(before); draw(); toast(`删除了 ${n} 个点`); }
$('del').onclick = delSel; $('undo').onclick = undo; $('redo').onclick = redo;
const setA = (t: number) => { S.A = +t.toFixed(3); if (S.B !== null && S.B <= S.A) S.B = null; save(); draw(); };
const setB = (t: number) => { S.B = +t.toFixed(3); if (S.A !== null && S.A >= S.B) S.A = null; save(); draw(); };
$('seta').onclick = () => setA(player.position); $('setb').onclick = () => setB(player.position);
$('clrab').onclick = () => { S.A = S.B = null; save(); draw(); };
$('selab').onclick = () => { if (selRange) { S.A = +selRange[0].toFixed(3); S.B = +selRange[1].toFixed(3); } else { const ts = S.taps.filter(t => S.sel.has(t.id)).map(t => t.t); if (ts.length) { S.A = +(Math.min(...ts) - 0.1).toFixed(3); S.B = +(Math.max(...ts) + 0.1).toFixed(3); } else { toast('先框选一段'); return; } } save(); draw(); };

// ---------------- timeline ----------------
const tl = $<HTMLCanvasElement>('timeline'), mini = $<HTMLCanvasElement>('mini');
const RULER = 22;
let selRange: [number, number] | null = null;
const x2t = (x: number) => S.view.t0 + x / S.view.pps, t2x = (t: number) => (t - S.view.t0) * S.view.pps;
const COL: Record<TType, string> = { tap: '#8a5cf6', drum: '#3b6ff5', vocal: '#ff5fa2' };
const snapDiv = () => +$<HTMLSelectElement>('snap').value;
function snapT(t: number, div: number) { const g = S.grid; if (!g.period || !div) return t; const sub = g.period / div; return g.beat0 + Math.round((t - g.beat0) / sub) * sub; }
function clampView() { const dur = player.duration || 1; const w = tl.clientWidth / S.view.pps; S.view.t0 = Math.max(-0.5, Math.min(S.view.t0, dur - w + 0.5)); }
function draw() {
  const dpr = devicePixelRatio || 1; const W = tl.clientWidth, H = tl.clientHeight;
  if (tl.width !== Math.round(W * dpr) || tl.height !== Math.round(H * dpr)) { tl.width = Math.round(W * dpr); tl.height = Math.round(H * dpr); }
  const c = tl.getContext('2d')!; c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
  c.fillStyle = '#fbfcff'; c.fillRect(0, 0, W, H); c.fillStyle = '#f1f4fc'; c.fillRect(0, 0, W, RULER);
  const t0 = S.view.t0, t1 = x2t(W), pps = S.view.pps;
  // A–B
  if (S.A !== null || S.B !== null) { const a = S.A ?? t0 - 1, b = S.B ?? t1 + 1; c.fillStyle = 'rgba(255,190,90,.16)'; c.fillRect(t2x(a), RULER, t2x(b) - t2x(a), H - RULER);
    c.fillStyle = '#f0a33c'; c.font = '600 11px sans-serif'; if (S.A !== null) { c.fillRect(t2x(S.A) - 1, RULER, 2, H - RULER); c.fillText('A', t2x(S.A) + 3, RULER + 12); } if (S.B !== null) { c.fillRect(t2x(S.B) - 1, RULER, 2, H - RULER); c.fillText('B', t2x(S.B) + 3, RULER + 12); } }
  if (selRange) { c.fillStyle = 'rgba(79,124,246,.12)'; c.fillRect(t2x(selRange[0]), RULER, t2x(selRange[1]) - t2x(selRange[0]), H - RULER); }
  // grid
  const g = S.grid; c.font = '11px sans-serif';
  if (g.period) {
    const sub = g.period / 2; const k0 = Math.floor((t0 - g.beat0) / sub) - 1, k1 = Math.ceil((t1 - g.beat0) / sub) + 1;
    for (let k = k0; k <= k1; k++) {
      const t = g.beat0 + k * sub; const x = t2x(t); const beat = k / 2; const isBeat = k % 2 === 0; const isBar = isBeat && (((beat - g.barBeat) % 4) + 4) % 4 === 0;
      if (!isBeat && sub * pps < 7) continue; if (isBeat && !isBar && g.period * pps < 6) continue;
      c.fillStyle = isBar ? 'rgba(80,90,160,.42)' : isBeat ? 'rgba(80,90,160,.2)' : 'rgba(80,90,160,.08)'; c.fillRect(Math.round(x), isBar ? 0 : RULER, isBar ? 1.5 : 1, H);
      if (isBar) { const bar = Math.round((beat - g.barBeat) / 4) + 1; if (g.period * 4 * pps > 26 || bar % 4 === 1) { c.fillStyle = '#5a6080'; c.fillText(String(bar), x + 3, 14); } }
    }
  } else {
    const step = pps > 60 ? 1 : pps > 15 ? 5 : 15; for (let t = Math.ceil(t0 / step) * step; t < t1; t += step) { c.fillStyle = 'rgba(80,90,160,.2)'; c.fillRect(t2x(t), 0, 1, H); c.fillStyle = '#5a6080'; c.fillText(fmt(t, false), t2x(t) + 3, 14); }
  }
  // waveform
  const pk = S.pk; const mid = RULER + (H - RULER) / 2, amp = (H - RULER) / 2 - 6;
  if (pk) { c.fillStyle = 'rgba(122,140,210,.45)'; for (let x = 0; x < W; x++) { const a = Math.floor(x2t(x) * pk.perSec), b = Math.max(a + 1, Math.floor(x2t(x + 1) * pk.perSec)); let lo = 0, hi = 0; for (let i = Math.max(0, a); i < Math.min(pk.mn.length, b); i++) { if (pk.mn[i] < lo) lo = pk.mn[i]; if (pk.mx[i] > hi) hi = pk.mx[i]; } c.fillRect(x, mid - hi * amp, 1, Math.max(1, (hi - lo) * amp)); } }
  // taps (+ snap preview)
  const div = snapDiv();
  for (const tp of S.taps) {
    if (tp.t < t0 - 1 || tp.t > t1 + 1) continue; const x = t2x(tp.t); const sel = S.sel.has(tp.id); const col = COL[tp.type] ?? COL.tap;
    if (div && g.period) { const st = snapT(tp.t, div); const d = Math.abs(st - tp.t); const sx = t2x(st); c.strokeStyle = d > 0.06 ? '#e5484d' : 'rgba(40,170,120,.9)'; c.setLineDash([3, 3]); c.beginPath(); c.moveTo(sx, RULER + 4); c.lineTo(sx, H - 4); c.stroke(); c.setLineDash([]); c.beginPath(); c.moveTo(x, H - 14); c.lineTo(sx, H - 14); c.stroke(); }
    c.fillStyle = col; c.globalAlpha = sel ? 1 : 0.85; c.fillRect(x - (sel ? 1.5 : 1), RULER, sel ? 3 : 2, H - RULER);
    const yh = tp.type === 'drum' ? H - 22 : RULER + 2; c.beginPath(); c.moveTo(x - 6, yh); c.lineTo(x + 6, yh); c.lineTo(x, yh + 10); c.closePath(); c.fill();
    if (sel) { c.strokeStyle = '#24263a'; c.lineWidth = 1.5; c.stroke(); c.lineWidth = 1; }
    c.globalAlpha = 1;
  }
  // playhead
  const ph = player.position; const px = t2x(ph); c.fillStyle = '#24263a'; c.fillRect(px - 1, 0, 2, H); c.beginPath(); c.moveTo(px - 6, 0); c.lineTo(px + 6, 0); c.lineTo(px, 8); c.fill();
  $('tnow').textContent = fmt(ph);
  $('selinfo').textContent = S.sel.size ? `已选 ${S.sel.size} 个` : `${S.taps.length} 个点`;
  drawMini();
}
function drawMini() {
  const dpr = devicePixelRatio || 1; const W = mini.clientWidth, H = mini.clientHeight; if (mini.width !== Math.round(W * dpr)) { mini.width = Math.round(W * dpr); mini.height = Math.round(H * dpr); }
  const c = mini.getContext('2d')!; c.setTransform(dpr, 0, 0, dpr, 0, 0); c.fillStyle = '#eef2fb'; c.fillRect(0, 0, W, H);
  const dur = player.duration || 1; c.fillStyle = 'rgba(138,92,246,.55)'; for (const t of S.taps) c.fillRect((t.t / dur) * W, 4, 1, H - 8);
  c.fillStyle = 'rgba(79,124,246,.18)'; c.strokeStyle = '#4f7cf6'; const a = (S.view.t0 / dur) * W, w = (tl.clientWidth / S.view.pps / dur) * W; c.fillRect(a, 0, w, H); c.strokeRect(a + .5, .5, w - 1, H - 1);
  c.fillStyle = '#24263a'; c.fillRect((player.position / dur) * W - 1, 0, 2, H);
}
mini.addEventListener('pointerdown', e => { const r = mini.getBoundingClientRect(); const go = (cx: number) => { S.view.t0 = ((cx - r.left) / r.width) * player.duration - tl.clientWidth / S.view.pps / 2; clampView(); draw(); }; go(e.clientX); mini.setPointerCapture(e.pointerId); mini.onpointermove = ev => go(ev.clientX); mini.onpointerup = () => { mini.onpointermove = null; }; });
function zoom(f: number, cx = tl.clientWidth / 2) { const t = x2t(cx); S.view.pps = Math.max(8, Math.min(3000, S.view.pps * f)); S.view.t0 = t - cx / S.view.pps; clampView(); draw(); }
$('zoomin').onclick = () => zoom(1.5); $('zoomout').onclick = () => zoom(1 / 1.5);
tl.addEventListener('wheel', e => { e.preventDefault(); if (e.ctrlKey || e.metaKey) zoom(Math.exp(-e.deltaY * 0.004), e.offsetX); else { S.view.t0 += (Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY) / S.view.pps; clampView(); draw(); } }, { passive: false });
const ptrs = new Map<number, { x: number; y: number }>(); let pinch: { d: number; pps: number; t: number; cx: number } | null = null;
let drag: null | { kind: 'move' | 'pan' | 'box' | 'seek'; x0: number; y0: number; t0: number; moved: boolean; before?: string; orig?: Map<number, number>; shift: boolean; hit?: Tap } = null;
function hitTap(x: number) { let best: Tap | undefined, bd = 9; for (const t of S.taps) { const d = Math.abs(t2x(t.t) - x); if (d < bd) { bd = d; best = t; } } return best; }
tl.addEventListener('pointerdown', e => {
  const r = tl.getBoundingClientRect(); const x = e.clientX - r.left, y = e.clientY - r.top; tl.setPointerCapture(e.pointerId); ptrs.set(e.pointerId, { x, y });
  if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; pinch = { d: Math.abs(a.x - b.x) || 1, pps: S.view.pps, t: x2t((a.x + b.x) / 2), cx: (a.x + b.x) / 2 }; drag = null; return; }
  const shift = e.shiftKey;
  if (y < RULER) { drag = { kind: 'seek', x0: x, y0: y, t0: S.view.t0, moved: false, shift }; player.seek(Math.max(0, x2t(x))); draw(); return; }
  const hit = hitTap(x);
  if (hit) {
    if (shift) { S.sel.has(hit.id) ? S.sel.delete(hit.id) : S.sel.add(hit.id); } else if (!S.sel.has(hit.id)) { S.sel = new Set([hit.id]); }
    drag = { kind: 'move', x0: x, y0: y, t0: S.view.t0, moved: false, shift, hit, orig: new Map(S.taps.filter(t => S.sel.has(t.id)).map(t => [t.id, t.t])) }; draw(); return;
  }
  drag = { kind: shift || $<HTMLInputElement>('boxmode').checked ? 'box' : 'pan', x0: x, y0: y, t0: S.view.t0, moved: false, shift };
});
tl.addEventListener('pointermove', e => {
  const r = tl.getBoundingClientRect(); const x = e.clientX - r.left, y = e.clientY - r.top; if (ptrs.has(e.pointerId)) ptrs.set(e.pointerId, { x, y });
  if (pinch && ptrs.size === 2) { const [a, b] = [...ptrs.values()]; S.view.pps = Math.max(8, Math.min(3000, pinch.pps * (Math.abs(a.x - b.x) || 1) / pinch.d)); S.view.t0 = pinch.t - ((a.x + b.x) / 2) / S.view.pps; clampView(); draw(); return; }
  if (!drag) { tl.style.cursor = y < RULER ? 'col-resize' : hitTap(x) ? 'ew-resize' : 'crosshair'; return; }
  if (Math.abs(x - drag.x0) > 3 || Math.abs(y - drag.y0) > 3) drag.moved = true; if (!drag.moved) return;
  if (drag.kind === 'seek') { player.seek(Math.max(0, x2t(x))); draw(); }
  else if (drag.kind === 'pan') { S.view.t0 = drag.t0 - (x - drag.x0) / S.view.pps; clampView(); draw(); }
  else if (drag.kind === 'box') { const a = x2t(Math.min(x, drag.x0)), b = x2t(Math.max(x, drag.x0)); selRange = [a, b]; S.sel = new Set(S.taps.filter(t => t.t >= a && t.t <= b).map(t => t.id)); draw(); }
  else if (drag.kind === 'move') { if (!drag.before) drag.before = snap(); const d = (x - drag.x0) / S.view.pps; for (const t of S.taps) { const o = drag.orig!.get(t.id); if (o !== undefined) setT(t, o + d); } draw(); }
});
const endPtr = (e: PointerEvent) => {
  ptrs.delete(e.pointerId); if (ptrs.size < 2) pinch = null; if (!drag) return; const dd = drag; drag = null;
  if (dd.kind === 'move' && dd.before) { sortTaps(); commit(dd.before); }
  else if (dd.kind === 'pan' && !dd.moved) { // click on empty space = add a tap here
    const before = snap(); const t = Math.max(0, x2t(dd.x0)); const tp = mkTap(t + S.calibMs / 1000, $<HTMLSelectElement>('addtype').value as TType, true); S.taps.push(tp); sortTaps(); S.sel = new Set([tp.id]); selRange = null; commit(before); }
  else if (dd.kind === 'box' && !dd.moved) { S.sel.clear(); selRange = null; }
  draw();
};
tl.addEventListener('pointerup', endPtr); tl.addEventListener('pointercancel', endPtr);
new ResizeObserver(() => draw()).observe(tl);

// ---------------- review clicks + render loop ----------------
let clickCursor = -1;
function scheduleClicks() {
  if (!player.playing || !$<HTMLInputElement>('clicks').checked || S.rec) { clickCursor = -1; return; }
  const now = player.songNow(); const ahead = now + 0.2 * player.rate;
  if (clickCursor < 0) clickCursor = S.taps.findIndex(t => t.t >= now - 0.005); if (clickCursor < 0) return;
  while (clickCursor < S.taps.length && S.taps[clickCursor].t <= ahead) { const tp = S.taps[clickCursor++]; if (tp.t >= now - 0.01) player.click(player.ctxForSong(tp.t), tp.type); }
}
$('clicks').onchange = () => { clickCursor = -1; };
function frame() {
  if (player.playing) {
    scheduleClicks();
    const p = player.position;
    if (S.rec?.mode === 'ab' && S.B !== null && p > S.B + 0.4) { finishPass(); const from = Math.max(0, S.A! - 1.5); player.play(from); }
    if ($<HTMLInputElement>('follow').checked && !drag) { const W = tl.clientWidth / S.view.pps; if (p > S.view.t0 + W * 0.8 || p < S.view.t0) { S.view.t0 = p - W * 0.2; clampView(); } }
    draw();
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

// ---------------- calibration ----------------
const calib = {
  active: false, clicks: [] as number[], taps: [] as number[], result: null as number | null, timer: 0,
  open() { $<HTMLDialogElement>('calibdlg').showModal(); this.renderBeats(-1); $('calres').textContent = `当前校准：${S.calibMs.toFixed(0)} ms`; },
  async start() {
    player.unlock(); const ctx = player.ensure(); player.stop(); syncButtons(); await player.ready();
    const bpm = 100, p = 60 / bpm, t0 = ctx.currentTime + 0.6; this.clicks = []; this.taps = []; this.result = null; this.active = true; ($('calsave') as HTMLButtonElement).disabled = true;
    for (let i = 0; i < 20; i++) { const t = t0 + i * p; player.click(t, i < 4 ? 'metroHi' : 'metro'); if (i >= 4) this.clicks.push(t); }
    $('calres').textContent = '预备… 第 5 下开始跟着打';
    const tick = () => { const now = player.heardCtxAt(performance.now()); const i = Math.floor((now - t0) / p + 0.5); this.renderBeats(i); if (now < t0 + 20 * p + 0.4) this.timer = requestAnimationFrame(tick); else this.finish(); };
    cancelAnimationFrame(this.timer); this.timer = requestAnimationFrame(tick);
  },
  tap(perf: number) { if (!this.active) return; const h = player.heardCtxAt(perf); this.taps.push(h); const b = $('calpad'); b.classList.remove('hit'); void b.offsetWidth; b.classList.add('hit'); },
  finish() {
    this.active = false; const diffs: number[] = [];
    for (const c of this.clicks) { let best = Infinity; for (const t of this.taps) if (Math.abs(t - c) < Math.abs(best)) best = t - c; if (Math.abs(best) < 0.3) diffs.push(best * 1000); }
    if (diffs.length < 8) { $('calres').textContent = `只对上了 ${diffs.length} 下，至少需要 8 下，请重试。`; return; }
    diffs.sort((a, b) => a - b); const med = diffs[Math.floor(diffs.length / 2)]; const mad = [...diffs.map(d => Math.abs(d - med))].sort((a, b) => a - b)[Math.floor(diffs.length / 2)];
    this.result = Math.round(med); ($('calsave') as HTMLButtonElement).disabled = false;
    $('calres').innerHTML = `结果：你平均比节拍<b>${med >= 0 ? '晚' : '早'} ${Math.abs(med).toFixed(0)} ms</b>（${diffs.length}/16 下有效，离散 ±${mad.toFixed(0)} ms）。点「保存」应用。`;
  },
  renderBeats(i: number) { const b = $('beats'); if (!b.children.length) for (let k = 0; k < 20; k++) { const e = document.createElement('i'); if (k < 4) e.className = 'pre'; b.append(e); } [...b.children].forEach((e, k) => e.classList.toggle('on', k === i)); },
};
$('calib').onclick = () => calib.open(); $('calstart').onclick = () => void calib.start(); $('calclose').onclick = () => { calib.active = false; $<HTMLDialogElement>('calibdlg').close(); };
$('calpad').addEventListener('pointerdown', e => { e.preventDefault(); calib.tap(e.timeStamp); });
$('calsave').onclick = () => { if (calib.result === null) return; applyCalib(calib.result); $<HTMLDialogElement>('calibdlg').close(); toast(`已保存校准 ${calib.result} ms`); };
function applyCalib(ms: number) {
  const before = snap(); S.calibMs = ms; localStorage.setItem(LS + 'calib', String(ms));
  for (const t of S.taps) { if (t.edited) t.t_raw = +(t.t + ms / 1000).toFixed(4); else t.t = +(t.t_raw - ms / 1000).toFixed(4); }
  if (S.taps.length) { sortTaps(); commit(before); } $('calibms').textContent = `${ms} ms`; draw();
}
$('calibms').textContent = `${S.calibMs} ms`;

// ---------------- export / import ----------------
function exportObj() {
  const s = S.song!; return { format: 'nj-tapper', version: 1, song: s.id, title: s.title, audio_duration: +player.duration.toFixed(3),
    bpm: S.grid.period ? +(60 / S.grid.period).toFixed(4) : null, beat_period: S.grid.period || null, beat0: S.grid.period ? +S.grid.beat0.toFixed(4) : null, bar_beat: S.grid.barBeat, grid_source: s.gridSource,
    calibration_ms: S.calibMs, exported: new Date().toISOString(), tool: location.href.split('?')[0],
    taps: S.taps.map(t => ({ t_raw: t.t_raw, t: t.t, type: t.type, ...(t.edited ? { edited: true } : {}) })) };
}
$('export').onclick = () => { if (!S.song) return; const js = JSON.stringify(exportObj(), null, 1); const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([js], { type: 'application/json' })); a.download = `taps-${S.song.id.replace(/[^\w.-]+/g, '_')}-${new Date().toISOString().slice(0, 16).replace(/[:T]/g, '')}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); toast('已导出'); };
$('copy').onclick = async () => { if (!S.song) return; const js = JSON.stringify(exportObj(), null, 1); try { await navigator.clipboard.writeText(js); toast('已复制到剪贴板'); } catch { const ta = document.createElement('textarea'); ta.value = js; document.body.append(ta); ta.select(); document.execCommand('copy'); ta.remove(); toast('已复制'); } };
$<HTMLInputElement>('importfile').onchange = async e => {
  const f = (e.target as HTMLInputElement).files?.[0]; if (!f) return; (e.target as HTMLInputElement).value = '';
  try { const d = JSON.parse(await f.text()); if (!Array.isArray(d.taps)) throw new Error('没有 taps'); await importObj(d); } catch (err) { toast('导入失败：' + (err as Error).message); }
};
async function importObj(d: any) {
  if (d.song && d.song !== S.song?.id && (SONGS as Song[]).some(s => s.id === d.song)) { songSel.value = d.song; await loadSong((SONGS as Song[]).find(s => s.id === d.song)!); }
  const before = snap(); const cal = typeof d.calibration_ms === 'number' ? d.calibration_ms : S.calibMs;
  S.taps = d.taps.map((t: any) => { const tp = mkTap(t.t_raw ?? (t.t + cal / 1000), (['tap', 'drum', 'vocal'].includes(t.type) ? t.type : 'tap') as TType); tp.t = +(t.t ?? tp.t_raw - cal / 1000).toFixed(4); if (t.edited) tp.edited = true; return tp; });
  sortTaps(); S.sel.clear(); commit(before); draw(); toast(`导入了 ${S.taps.length} 个点`);
}
$('clear').onclick = () => { if (!S.taps.length || !confirm('清空本曲所有点？（可以撤销）')) return; const before = snap(); S.taps = []; S.sel.clear(); commit(before); draw(); };

// ---------------- touch / focus guards (no page movement, no selection, no zoom) ----------------
window.addEventListener('keyup', e => { if ((e.code === 'Space' || ((S.rec || calib.active) && e.code === 'Enter')) && !isTextField(e.target)) e.preventDefault(); });
document.addEventListener('click', e => { const b = (e.target as Element).closest?.('button, label.btn, .chk'); if (b) setTimeout(() => { const a = document.activeElement as HTMLElement | null; if (a && a !== document.body && !isTextField(a) && a.tagName !== 'SELECT') a.blur(); }, 0); });
document.addEventListener('change', e => { const t = e.target as HTMLInputElement; if (t.type === 'checkbox' || t.tagName === 'SELECT') t.blur(); });
for (const el of [pad, $('calpad')]) {
  el.addEventListener('touchstart', e => e.preventDefault(), { passive: false });
  el.addEventListener('touchend', e => e.preventDefault(), { passive: false });
  el.addEventListener('contextmenu', e => e.preventDefault());
}
document.addEventListener('touchmove', e => { const t = e.target as Element; if (!t.closest?.('.scroll, dialog')) e.preventDefault(); }, { passive: false });
document.addEventListener('dblclick', e => { if (!isTextField(e.target)) e.preventDefault(); }, { passive: false });
for (const g of ['gesturestart', 'gesturechange', 'gestureend']) document.addEventListener(g, e => e.preventDefault(), { passive: false } as AddEventListenerOptions);
document.addEventListener('selectstart', e => { if (!isTextField(e.target)) e.preventDefault(); });
document.addEventListener('contextmenu', e => { if (!isTextField(e.target) && !(e.target as Element).closest?.('.help')) e.preventDefault(); });
window.addEventListener('scroll', () => { if (window.scrollY || window.scrollX) window.scrollTo(0, 0); });
for (const d of document.querySelectorAll<HTMLDialogElement>('dialog.sheet')) {
  d.querySelector('[data-close]')?.addEventListener('click', () => d.close());
  d.addEventListener('click', e => { if (e.target === d) d.close(); });   // tap on the backdrop closes
}
// ---------------- audio unlock (iOS / Safari) ----------------
// every gesture re-unlocks synchronously (touchend / click / keydown count as activation on iOS; pointerdown does not)
for (const ev of ['touchend', 'click', 'keydown', 'pointerup']) document.addEventListener(ev, () => { if (player.locked || ev === 'touchend' || ev === 'click') player.unlock(); }, { capture: true, passive: true });
const pill = $('unlock');
function syncLock() {
  const st = player.state; const show = st !== 'running';
  pill.hidden = !show;
  pill.textContent = st === 'interrupted' ? '🔇 声音被系统打断，点一下恢复' : '🔇 点一下解锁声音';
}
player.onState = () => syncLock(); syncLock();
player.onBlocked = () => { if (S.rec) finishRec(); syncButtons(); toast('浏览器拦截了播放，请再点一次 ▶'); };
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { if (player.playing || S.rec) { stopAll(); syncButtons(); } return; }
  if (player.ctx && player.state !== 'running') { try { void player.ctx.resume().catch(() => {}); } catch { /* */ } }
  syncLock();
});
if (IS_IOS && !HAS_AUDIO_SESSION) $('silentnote').hidden = false;
// ?diag: live audio diagnostics line (for checking phones / simulators from a screenshot)
if (new URLSearchParams(location.search).has('diag')) {
  const d = document.createElement('div'); d.id = 'diag'; document.body.append(d); let an: AnalyserNode | null = null; const buf = new Float32Array(1024);
  setInterval(() => {
    const P: any = player; if (P.ctx && !an) { const a = P.ctx.createAnalyser() as AnalyserNode; a.fftSize = 1024; P.gain.connect(a); P.clickGain.connect(a); an = a; }
    let rms = 0; if (an) { an.getFloatTimeDomainData(buf); rms = Math.sqrt(buf.reduce((a, v) => a + v * v, 0) / buf.length); }
    const el = P.el as HTMLAudioElement | null;
    d.textContent = `ctx=${player.state} sr=${P.ctx?.sampleRate ?? '-'} t=${P.ctx ? P.ctx.currentTime.toFixed(2) : '-'} session=${(navigator as any).audioSession?.type ?? 'n/a'} ios=${IS_IOS} play=${player.playing} pos=${player.position.toFixed(2)} rms=${rms.toFixed(3)} el=${el ? (el.paused ? 'paused' : 'playing') + '/' + el.readyState + (el.muted ? '/muted' : '') : '-'}`;
  }, 250);
}
$('morebtn').onclick = () => $<HTMLDialogElement>('sheet').showModal();
$('helpbtn').onclick = () => $<HTMLDialogElement>('helpsheet').showModal();

// test / automation hook (read-mostly)
(window as any).__tapper = { S, player, exportObj, importObj, loadSongById: (id: string) => { songSel.value = id; return loadSong((SONGS as Song[]).find(s => s.id === id)!); }, draw, calib, x2t, t2x };

const first = new URLSearchParams(location.search).get('song') ?? localStorage.getItem(LS + 'last') ?? 'omg';
const s0 = (SONGS as Song[]).find(s => s.id === first) ?? (SONGS as Song[])[0]; songSel.value = s0.id;
void loadSong(s0);
