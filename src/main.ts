import './style.css';
import { LoadingProgress } from './loading';
import { FramePacer } from './framepacing';
import { SONGS, loadLevel, hasLevel } from './catalog';
import { AudioTransport } from './audio';
import { Game, LATE_GRACE, LATE_GRACE_MAX } from './core/game';
import type { LevelData } from './core/types';
import { World } from './render/world';
import { loadSave, persistSave, parseSave, mergeRecord, type SaveData } from './storage';
import { hex } from './render/prefabs';
import { initSkinUI } from './skinui';

type State = 'menu' | 'loading' | 'ready' | 'playing' | 'paused' | 'failed' | 'complete';
const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T;
const ids = SONGS.map(s => s.id);
const save: SaveData = loadSave(ids, 'attention');
const audio = new AudioTransport();
const canvas = $<HTMLCanvasElement>('scene');
const world = new World(canvas);
let state: State = 'menu';
// initial song: ?level=<slug> deep link, else the saved selection, else the first song that has level data
const firstPlayable = Math.max(0, ids.findIndex(id => hasLevel(id)));
const qLevel = new URLSearchParams(location.search).get('level');
let index = qLevel && ids.includes(qLevel) ? ids.indexOf(qLevel) : hasLevel(save.selected) ? ids.indexOf(save.selected) : firstPlayable;
let level: LevelData | null = null;
let game: Game | null = null;
let readyFrom = 0;           // song time the next start/resume begins at
let readyKind: 'start' | 'resume' | 'checkpoint' = 'start';
let failTimer = 0, clearTimer = 0;
let loadToken = 0, loadingAttempt = 0;
let runVersion=0, startPending=false, inputArmedAt=0;

let lastSky='';
world.onSky = (top, bottom) => {
  const key=top+'|'+bottom;if(key===lastSky)return;lastSky=key;
  const r = document.documentElement.style;
  r.setProperty('--sky-top', top); r.setProperty('--sky-bottom', bottom);
  const c = hex(top), d = hex(bottom); const lum = (c.r + c.g + c.b + d.r * 2 + d.g * 2 + d.b * 2) / 9;
  document.body.classList.toggle('dark', lum < 0.42);
};

world.onBackdrop = url => {
  const el = $('sky');
  el.style.backgroundImage = url ? `url("${url}"), linear-gradient(180deg, var(--sky-top) 0%, var(--sky-bottom) 72%)` : '';
  el.style.backgroundSize = url ? 'cover, auto' : ''; el.style.backgroundPosition = url ? 'center bottom, 0 0' : '';
};

function show(id: string, on: boolean) { $(id).classList.toggle('on', on); }
function setState(s: State) {
  if(s!=='playing'){runVersion++;startPending=false;}
  state = s;
  document.body.className = document.body.className.replace(/\b(menu|loading|ready|playing|paused|failed|complete)\b/g, '').trim() + ' ' + s;
  show('menu', s === 'menu'); show('hud', s === 'ready' || s === 'playing' || s === 'paused');
  show('pause', s === 'paused'); show('fail', false); show('clear', false); show('loading', s === 'loading');
  world.mode = s === 'menu' || s === 'loading' ? 'menu' : 'play';
}
function toast(msg: string) { const t = $('toast'); t.textContent = msg; t.classList.add('on'); clearTimeout((toast as any).h); (toast as any).h = setTimeout(() => t.classList.remove('on'), 2600); }
function persist() { if (!persistSave(save)) toast('浏览器拒绝保存进度（可能处于隐私模式）'); }
const crownsHtml = (n: number, total = 3) => Array.from({ length: total }, (_, i) => `<i class="${i < n ? 'on' : ''}"></i>`).join('');

// ---------------- level select ----------------
function renderCard() {
  const s = SONGS[index]; const r = save.records[s.id];
  $('lv-index').textContent = `${String(index + 1).padStart(2, '0')} / ${SONGS.length}`;
  $('lv-title').textContent = s.title; $('lv-album').textContent = s.album;
  const best = Math.floor((r?.best ?? 0) * 100);
  $('lv-pct').textContent = `${best}%`; ($('lv-bar').style.width = `${best}%`);
  $('lv-gems').textContent = String(r?.diamonds ?? 0); $('lv-crowns').innerHTML = crownsHtml(r?.crowns ?? 0);
  document.documentElement.style.setProperty('--accent', s.accent);
  const soon = !hasLevel(s.id);
  $('level-card').classList.toggle('soon', soon); document.body.classList.toggle('soon', soon);
  $('start-label').textContent = soon ? '即将上线 · 左右滑动选择其他歌曲' : '轻点开始';
}

async function selectLevel(i: number, dir = 0) {
  index = (i + SONGS.length) % SONGS.length;
  save.selected = SONGS[index].id; persist();
  const card = $('level-card');
  if (dir) { card.classList.add(dir < 0 ? 'swap-r' : 'swap-l'); setTimeout(() => { renderCard(); card.classList.remove('swap-l', 'swap-r'); }, 180); } else renderCard();
  const token = ++loadToken;
  if (!hasLevel(SONGS[index].id)) { level = null; game = null; return; }   // 'coming soon' card, nothing to load
  try {
    const data = await loadLevel(SONGS[index].id);
    if (token !== loadToken) return;
    level = data; game = makeGame(data);
    world.load(data, game);
    audio.load(data.audio).catch(() => {});
  } catch (e) { toast(String((e as Error).message ?? e)); }
}

function makeGame(data: LevelData) {
  const g = new Game(data, { centerAssist: save.settings.centerAssist });
  g.onEvent = ev => {
    if (ev.type === 'turn') { world.onTurn(ev.t as number); if (save.settings.vibration && navigator.vibrate) navigator.vibrate(6); }
    else if (ev.type === 'diamond') { world.onDiamond(ev.index as number, ev.t as number); bumpGems(); }
    else if (ev.type === 'crown') { world.onCrown(ev.index as number, ev.t as number); }
    else if (ev.type === 'fail') onFail(ev.kind as string, ev.t as number);
    else if (ev.type === 'complete') onComplete();
  };
  g.prepare(0);
  return g;
}

function startLoading(){
  const token=loadToken, attempt=++loadingAttempt;
  const progress=new LoadingProgress((percent,detail)=>{
    if(state!=='loading'||token!==loadToken||attempt!==loadingAttempt)return;
    $('loading-fill').style.width=`${percent}%`;
    $('loading-progress').setAttribute('aria-valuenow',String(percent));
    $('loading-pct').textContent=`${percent}%`;
    $('loading-msg').textContent=detail;
  });
  progress.update('audio',audio.ready?1:0,'正在加载歌曲与场景');
  return progress;
}

// ---------------- game flow ----------------
async function enterLevel() {
  if(state==='loading')return;
  if (!hasLevel(SONGS[index].id)) { toast(`${SONGS[index].title} 即将上线`); return; }
  if (!level || !game) return;
  clearTimeout(failTimer); clearTimeout(clearTimer);
  lastInputPerf = -1;
  audio.stop();audio.unlock();
  game.setCenterAssist(save.settings.centerAssist);game.prepare(0);world.clearAttemptVisuals();
  setState('loading');
  const token=loadToken, activeGame=game;
  const progress=startLoading();
  audio.onProgress=(f,n)=>{
    if(token!==loadToken||state!=='loading')return;
    progress.update('audio',f>=0?f*0.9:-1,f>=1?'歌曲解码中':`歌曲下载 ${f>=0?Math.round(f*100)+'%':(n/1048576).toFixed(1)+' MB'}`);
  };
  try {
    // Audio decoding and scene preparation overlap; 100% means both are ready.
    await Promise.all([
      audio.load(level.audio).then(()=>progress.update('audio',1,'歌曲就绪')),
      world.prepareScenery(0,(stage,f,detail)=>progress.update(stage,f,detail))
    ]);
  } catch(e) {
    if(token===loadToken){setState('menu');toast(`加载失败：${(e as Error).message || '请重试'}`);}
    return;
  } finally {if(token===loadToken)audio.onProgress=null;}
  if(token!==loadToken||game!==activeGame||(state as State)!=='loading')return;
  game.checkpointsUsed.clear(); game.diamondsTaken.clear(); game.crownsReached.clear();
  game.setCenterAssist(save.settings.centerAssist); game.prepare(0); world.mode = 'play'; world.seek(0);
  readyFrom = 0; readyKind = 'start';
  setReady();
}

function setReady() {
  setState('ready');
  world.snapCamera();
  $('ready-label').textContent = readyKind === 'resume' ? '轻点继续' : readyKind === 'checkpoint' ? '轻点从皇冠处出发' : '轻点开始';
  updateHud();
}

async function beginRun() {
  if (!game || !level || state!=='ready' || startPending) return;
  const version=runVersion, activeGame=game, from=readyFrom;
  startPending=true;
  clearTimeout(failTimer); clearTimeout(clearTimer);
  audio.setEnd(level.audioDuration ? level.duration : null, level.endFade ?? 1.5);
  try {
    const started=await audio.play(from);
    if(!started || version!==runVersion || game!==activeGame || (state as State)!=='ready')return;
    lastInputPerf=-1;
    const safeStartGap=((activeGame.taps[activeGame.cursor]??Infinity)-from-(activeGame.earlyWindows[activeGame.cursor]??0)-.05)*1000;
    inputArmedAt=performance.now()+Math.max(0,Math.min(120,safeStartGap));
    activeGame.start();setState('playing');
  } catch(e) {if(version===runVersion)toast(String((e as Error).message));}
  finally {if(version===runVersion)startPending=false;}
}

function pause() {
  if (state !== 'playing' || !game) return;
  audio.pause(); game.pause();
  $('pause-title').textContent = level!.title; $('pause-pct').textContent = `${Math.floor(game.progress * 100)}%`;
  setState('paused');
}

/** Resume rewinds ~1.6 s to a straight stretch so the player re-enters with the music, never mid-corner. */
function resume() {
  if (!game) return;
  const t = game.time; let r = Math.max(game.startTime, t - 1.6);
  for (let guard = 0; guard < 20; guard++) { const near = game.taps.find(x => Math.abs(x - r) < 0.18); if (near === undefined) break; r = Math.max(game.startTime, near - 0.25); if (r === game.startTime) break; }
  game.setCenterAssist(save.settings.centerAssist); game.prepare(r, true); world.mode = 'play'; world.seek(r);
  readyFrom = r; readyKind = 'resume'; setReady();
}

function restart() { clearTimeout(failTimer); clearTimeout(clearTimer); audio.stop(); void enterLevel(); }
function toMenu() { audio.stop(); clearTimeout(failTimer); clearTimeout(clearTimer); if (game) { game.prepare(0); world.seek(0); } renderCard(); setState('menu'); }

function recordRun(completed: boolean) {
  if (!game || !level) return;
  const crowns = completed ? game.crownsEarned() : 0;
  save.records[level.id] = mergeRecord(save.records[level.id], { progress: completed ? 1 : game.progress, diamonds: game.diamondsTaken.size, crowns, completed, perfect: game.perfect, taps: game.taps.length });
  persist();
}

function onFail(_kind: string, _t: number) {
  if (!game || !level) return;
  world.onFail(game.failTime, game.failKind ?? 'late');
  audio.fadeOut(0.5);
  recordRun(false);
  failTimer = window.setTimeout(() => {
    setState('failed');
    const pct = Math.floor(game!.progress * 100);
    $('fail-title').textContent = level!.title; $('fail-pct').textContent = `${pct}%`; $('fail-bar').style.width = `${pct}%`;
    $('fail-gems').textContent = String(game!.diamondsTaken.size);
    $('fail-marks').innerHTML = level!.layout.crowns.map((c, i) => `<i class="${game!.crownsReached.has(i) ? 'on' : ''}" style="left:${c.t / level!.duration * 100}%"></i>`).join('') + `<i style="left:100%"></i>`;
    const cp = game!.latestCheckpoint();
    $('btn-checkpoint').hidden = cp < 0;
    show('fail', true);
  }, 1100);
}

async function continueFromCheckpoint() {
  if (!game || !level) return;
  const cp = game.latestCheckpoint(); if (cp < 0) return;
  const t = level.layout.crowns[cp].t;
  game.checkpointsUsed.add(cp);
  if(state==='loading')return;
  clearTimeout(failTimer);clearTimeout(clearTimer);audio.stop();
  game.setCenterAssist(save.settings.centerAssist);game.prepare(t,true,true);world.clearAttemptVisuals();
  setState('loading');const version=runVersion,activeGame=game; const progress=startLoading();progress.update('audio',1,'歌曲已就绪');
  try { await world.prepareScenery(t,(stage,f,detail)=>progress.update(stage,f,detail)); } catch(e) {if(version===runVersion){setState('menu');toast('场景准备失败，请重试');}return;}
  if(version!==runVersion||game!==activeGame||(state as State)!=='loading')return;
  game.setCenterAssist(save.settings.centerAssist); game.prepare(t, true, true); world.mode = 'play'; world.seek(t);
  readyFrom = t; readyKind = 'checkpoint'; setReady();
}

function onComplete() {
  if (!game || !level) return;
  recordRun(true);
  clearTimeout(clearTimer);
  const fl = $('flash'); fl.style.setProperty('--flash', '0.85'); document.documentElement.style.setProperty('--flash', '0.85');
  setTimeout(() => document.documentElement.style.setProperty('--flash', '0'), 380);
  clearTimer = window.setTimeout(() => {
    setState('complete');
    $('clear-title').textContent = level!.title; $('clear-gems').textContent = String(game!.diamondsTaken.size);
    const earned = game!.crownsEarned();
    $('clear-crowns').innerHTML = crownsHtml(earned);
    const total = game!.perfect + game!.good;
    $('clear-stats').innerHTML = `<span>转弯 ${total}</span><span>完美 ${game!.perfect}</span><span>平均偏差 ${total ? Math.round(game!.errorSum / total * 1000) : 0} ms</span>`;
    show('clear', true);
    [...$('clear-crowns').children].forEach((el, i) => setTimeout(() => el.classList.add('show'), 250 + i * 260));
  }, 1600);
}

let gemsShown = -1;
function bumpGems() { const g = $('hud-gems').parentElement!; g.classList.remove('bump'); void g.offsetWidth; g.classList.add('bump'); }
function updateHud() {
  if (!game) return;
  const pct = Math.floor(game.progress * 100);
  $('hud-pct').textContent = `${pct}%`; $('hud-bar').style.width = `${game.progress * 100}%`;
  if (gemsShown !== game.diamondsTaken.size) { gemsShown = game.diamondsTaken.size; $('hud-gems').textContent = String(gemsShown); }
  $('hud-crowns').innerHTML = crownsHtml(game.crownsReached.size);
}

// ---------------- input ----------------
let lastInputPerf = -1;
function onPlayInput(perfTime: number) {
  if (state === 'ready') { void beginRun(); return; }
  if (state !== 'playing' || !game) return;
  if(perfTime<inputArmedAt)return; // do not turn the start gesture / double-tap into an immediate early death
  if (perfTime === lastInputPerf) return; // same physical event delivered twice
  lastInputPerf = perfTime;
  const t = audio.songTime(perfTime) - save.settings.offsetMs / 1000;
  game.tap(t);
}
const stage = $('stage');
stage.addEventListener('pointerdown', e => { e.preventDefault(); onPlayInput(e.timeStamp); }, { passive: false });
stage.addEventListener('contextmenu', e => e.preventDefault());
window.addEventListener('keydown', e => {
  if (e.repeat) return;
  if (['Space', 'Enter', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'KeyF', 'KeyJ'].includes(e.code)) {
    if (state === 'menu' && e.code === 'ArrowLeft') return void selectLevel(index - 1, -1);
    if (state === 'menu' && e.code === 'ArrowRight') return void selectLevel(index + 1, 1);
    if (state === 'menu' && (e.code === 'Space' || e.code === 'Enter')) { e.preventDefault(); return void enterLevel(); }
    if (state === 'ready' || state === 'playing') { e.preventDefault(); onPlayInput(e.timeStamp); }
  }
  if (e.code === 'Escape' || e.code === 'KeyP') { if (state === 'playing') pause(); else if (state === 'paused') resume(); }
});
document.addEventListener('visibilitychange', () => { if (document.hidden && state === 'playing') pause(); });

// menu: tap to start, swipe to change
const menu = $('menu');
let swipe: { x: number; y: number } | null = null;
menu.addEventListener('pointerdown', e => { if ((e.target as HTMLElement).closest('button')) return; swipe = { x: e.clientX, y: e.clientY }; });
menu.addEventListener('pointerup', e => {
  if (!swipe || (e.target as HTMLElement).closest('button')) { swipe = null; return; }
  const dx = e.clientX - swipe.x, dy = e.clientY - swipe.y; swipe = null;
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) void selectLevel(index + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
  else if (Math.hypot(dx, dy) < 12) void enterLevel();
});
$('btn-prev').onclick = () => selectLevel(index - 1, -1);
$('btn-next').onclick = () => selectLevel(index + 1, 1);
$('btn-pause').onclick = () => pause();
$('btn-resume').onclick = () => resume();
$('btn-restart-p').onclick = () => restart();
$('btn-home-p').onclick = () => toMenu();
$('btn-retry').onclick = () => restart();
$('btn-home-f').onclick = () => toMenu();
$('btn-checkpoint').onclick = () => continueFromCheckpoint();
$('btn-settings-f').onclick = () => openSettings();
$('btn-replay').onclick = () => restart();
$('btn-home-c').onclick = () => toMenu();
$('btn-next-c').onclick = async () => { toMenu(); await selectLevel(index + 1, 1); };

// ---------------- library ----------------
function renderLibrary() {
  $('song-list').innerHTML = SONGS.map((s, i) => {
    const r = save.records[s.id];
    return `<li data-i="${i}" class="${i === index ? 'sel' : ''}${hasLevel(s.id) ? '' : ' soon'}"><span class="no">${String(i + 1).padStart(2, '0')}</span><img src="${s.cover}" alt="" loading="lazy"/><div><div class="t">${s.title}</div><div class="a">${s.album}</div></div><div class="r"><span>${hasLevel(s.id) ? Math.floor((r?.best ?? 0) * 100) + '%' : '即将上线'}</span><span class="crowns mini">${crownsHtml(r?.crowns ?? 0)}</span></div></li>`;
  }).join('');
}
$('btn-library').onclick = () => { renderLibrary(); show('library', true); };
$('btn-close-lib').onclick = () => show('library', false);
$('song-list').addEventListener('click', e => { const li = (e.target as HTMLElement).closest('li'); if (!li) return; show('library', false); void selectLevel(Number(li.dataset.i)); });

// ---------------- settings ----------------
function openSettings() {
  const s = save.settings;
  $<HTMLInputElement>('set-volume').value = String(s.volume);
  $<HTMLInputElement>('set-offset').value = String(s.offsetMs); $('set-offset-val').textContent = `${s.offsetMs} ms`;
  $<HTMLInputElement>('set-vibration').checked = s.vibration;
  for (const b of $('set-quality').querySelectorAll('button')) b.classList.toggle('on', b.dataset.v === s.quality);
  for(const b of $('set-fps').querySelectorAll('button'))b.classList.toggle('on',Number(b.dataset.v)===s.targetFps);
  $<HTMLInputElement>('set-show-fps').checked=s.showFps;
  $<HTMLInputElement>('set-center-assist').checked=s.centerAssist;
  show('settings', true);
}
$('btn-settings').onclick = () => openSettings();
$('btn-close-set').onclick = () => show('settings', false);
$<HTMLInputElement>('set-volume').oninput = e => { save.settings.volume = Number((e.target as HTMLInputElement).value); audio.setVolume(save.settings.volume); persist(); };
$<HTMLInputElement>('set-offset').oninput = e => { save.settings.offsetMs = Number((e.target as HTMLInputElement).value); $('set-offset-val').textContent = `${save.settings.offsetMs} ms`; persist(); };
$<HTMLInputElement>('set-vibration').onchange = e => { save.settings.vibration = (e.target as HTMLInputElement).checked; persist(); };
$('set-quality').onclick = e => { const b = (e.target as HTMLElement).closest('button'); if (!b) return; try { localStorage.setItem('nj-quality-picked', '1'); } catch { /* */ } save.settings.quality = b.dataset.v as 'high' | 'low'; world.setQuality(save.settings.quality); persist(); openSettings(); };
$('set-fps').onclick=e=>{const b=(e.target as HTMLElement).closest('button');if(!b)return;save.settings.targetFps=Number(b.dataset.v)===120?120:60;save.settings.showFps=true;world.setTargetFps(save.settings.targetFps);pacer.reset();persist();openSettings();};
$<HTMLInputElement>('set-show-fps').onchange=e=>{save.settings.showFps=(e.target as HTMLInputElement).checked;persist();};
$<HTMLInputElement>('set-center-assist').onchange=e=>{save.settings.centerAssist=(e.target as HTMLInputElement).checked;persist();};
$('btn-export').onclick = () => {
  const blob = new Blob([JSON.stringify(save, null, 2)], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `newjeans-line-save-${new Date().toISOString().slice(0, 10)}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  toast('存档已导出');
};
$<HTMLInputElement>('file-import').onchange = async e => {
  const f = (e.target as HTMLInputElement).files?.[0]; if (!f) return;
  try { const data = parseSave(JSON.parse(await f.text()), ids, SONGS[index].id); Object.assign(save, data); persist(); audio.setVolume(save.settings.volume); world.setSkin(save.settings.skin); world.setQuality(save.settings.quality);world.setTargetFps(save.settings.targetFps);pacer.reset();skinUI.refresh(); openSettings(); renderCard(); toast('存档已导入'); }
  catch (err) { toast((err as Error).message || '无法读取存档'); }
  (e.target as HTMLInputElement).value = '';
};

// latency calibration: 8 clicks at 100 BPM synthesized on the audio clock
$('btn-calibrate').onclick = () => {
  show('settings', false); show('calib', true);
  audio.unlock(); const ctx = audio.context();
  const start = ctx.currentTime + 0.6; const beat = 0.6; const clicks: number[] = []; const errors: number[] = [];
  for (let i = 0; i < 16; i++) { const o = ctx.createOscillator(); const g = ctx.createGain(); o.frequency.value = i % 4 ? 880 : 1320; g.gain.setValueAtTime(0.0001, start + i * beat); g.gain.exponentialRampToValueAtTime(0.5, start + i * beat + 0.002); g.gain.exponentialRampToValueAtTime(0.0001, start + i * beat + 0.08); o.connect(g).connect(ctx.destination); o.start(start + i * beat); o.stop(start + i * beat + 0.1); clicks.push(start + i * beat); }
  const dot = $('calib-dot');
  const ts0 = ctx.getOutputTimestamp?.();
  const heard = (perf: number) => { const ts = ctx.getOutputTimestamp?.(); return ts && ts.contextTime ? ts.contextTime + (perf - (ts.performanceTime ?? perf)) / 1000 : ctx.currentTime - (ctx.outputLatency || 0); };
  void ts0;
  const iv = setInterval(() => { const h = heard(performance.now()); const near = clicks.some(c => h >= c && h < c + 0.1); dot.classList.toggle('beat', near); }, 16);
  const onTap = (e: PointerEvent) => { if ((e.target as HTMLElement).closest('button')) return; const h = heard(e.timeStamp); const c = clicks.reduce((a, b) => (Math.abs(b - h) < Math.abs(a - h) ? b : a)); if (Math.abs(h - c) < 0.3 && c >= clicks[3]) errors.push(h - c); $('calib-msg').textContent = `已记录 ${errors.length} / 10`; if (errors.length >= 10) finish(); };
  const finish = () => {
    clearInterval(iv); $('calib').removeEventListener('pointerdown', onTap);
    if (errors.length >= 5) { const sorted = [...errors].sort((a, b) => a - b); const med = sorted[Math.floor(sorted.length / 2)]; save.settings.offsetMs = Math.max(-300, Math.min(300, Math.round(med * 1000 / 5) * 5)); persist(); toast(`音画延迟已设为 ${save.settings.offsetMs} ms`); }
    show('calib', false); $('calib-msg').textContent = '听到节拍时轻点屏幕'; openSettings();
  };
  $('calib').addEventListener('pointerdown', onTap);
  $('btn-calib-cancel').onclick = () => { errors.length = 0; finish(); };
  setTimeout(() => { if ($('calib').classList.contains('on')) finish(); }, (16 * beat + 2) * 1000);
};

// ---------------- sync probe (QA only, ?syncprobe) ----------------
// A small corner square that turns white on the first rendered frame at/after each tap time (the same frame in which
// the line's turn first becomes visible), so a screen recording can be checked against the recorded audio.
const PROBE = new URLSearchParams(location.search).has('syncprobe');
let probeEl: HTMLDivElement | null = null; let probeIdx = -1; let probeOn = 0;
function syncProbe(t: number) {
  if (!probeEl) { probeEl = document.createElement('div'); probeEl.style.cssText = 'position:fixed;left:0;bottom:0;width:28px;height:28px;background:#000;z-index:99999;pointer-events:none'; document.body.appendChild(probeEl); }
  const taps = level!.chart.taps; let i = probeIdx;
  while (i + 1 < taps.length && taps[i + 1].t <= t) i++;
  if (i !== probeIdx) { if (i >= 0 && t - taps[i].t < 0.25) probeOn = 2; probeIdx = i; }
  probeEl.style.background = probeOn > 0 ? '#fff' : '#000'; if (probeOn > 0) probeOn--;
}

// Adaptive quality: phones start on the saved quality (high by default); if high cannot hold ~40 fps while playing (frame EMA over
// 24 ms for 4 s) it drops to low for this session, once. A quality the player picked in settings is never overridden.
let slowSince = 0, autoDropped = false;
function autoTier(nowMs: number) {
  if (autoDropped || state !== 'playing' || save.settings.quality !== 'high' || localStorage.getItem('nj-quality-picked')) { slowSince = 0; return; }
  if (frameEma > 0.024) { if (!slowSince) slowSince = nowMs; else if (nowMs - slowSince > 4000) { autoDropped = true; world.setQuality('low'); console.info('[nj] auto quality: high -> low (frame', (frameEma * 1000).toFixed(1), 'ms)'); (window as any).__njAutoLow = true; } }
  else slowSince = 0;
}

// ---------------- main loop ----------------
const pacer=new FramePacer();let fpsHudAt=0;
let lastHudMs=0; let lastLoop = 0; let frameEma = 1 / 60;
let callbackCount=0, callbackStart=0, callbackHz=0;
function loop(nowMs: number) {
  requestAnimationFrame(loop);
  if(!callbackStart)callbackStart=nowMs;
  callbackCount++;if(nowMs-callbackStart>=1000){callbackHz=callbackCount*1000/(nowMs-callbackStart);callbackCount=0;callbackStart=nowMs;}
  if (lastLoop) frameEma += (Math.min(0.25, (nowMs - lastLoop) / 1000) - frameEma) * 0.1; lastLoop = nowMs;
  if (!game) { return; }
  // input events arrive at most ~2 frames late: never declare a miss before a queued, in-time tap could be processed
  game.lateGrace = Math.min(LATE_GRACE_MAX, Math.max(LATE_GRACE, 0.05 + 2.5 * frameEma));
  let t = game.time;
  if (state === 'playing') {
    // predict ~1.5 frames ahead: a frame drawn now reaches the screen 1-2 vsyncs later (capped so pending corners never visibly overshoot)
    // A free-turn head must not be rendered ahead of input: changing an already-predicted
    // future segment at the next tap looks like a snap even without centreline projection.
    t = (game.route.freeTurns ? audio.songTime() : audio.renderTime(Math.min(0.07, 1.5 * frameEma))) - save.settings.offsetMs / 1000;
    game.update(t);
    if (game.status === 'playing' && !audio.playing && audio.songTime() >= level!.duration - 0.05) game.update(level!.duration);
    t = game.status === 'failed' ? game.failTime : game.time;
  } else if (state === 'complete' || (state === 'failed')) t = game.time;
  // Input/physics keep the audio clock even when a 60-fps cap skips a render.
  if(pacer.due(nowMs,save.settings.targetFps))world.frame(t);
  if(nowMs-fpsHudAt>500){fpsHudAt=nowMs;const el=$('fps-counter');el.hidden=!save.settings.showFps;
    if(save.settings.showFps)el.textContent=`${Math.round(world.fps)} FPS · 回调 ${Math.round(callbackHz)} Hz · 目标 ${save.settings.targetFps}`;
  }
  autoTier(nowMs);
  if (PROBE && level) syncProbe(t);
  if(nowMs-lastHudMs>=100&&(state==='playing'||state==='ready')){lastHudMs=nowMs;updateHud();}
}

window.addEventListener('resize', () => world.resize());
audio.setVolume(save.settings.volume);
world.setQuality(save.settings.quality);
world.setTargetFps(save.settings.targetFps);
world.setSkin(save.settings.skin);
const skinUI = initSkinUI({ getSkin: () => save.settings.skin, setSkin: id => { save.settings.skin = id; world.setSkin(id); persist(); }, lineColor: () => level?.layout.palette.line ?? '#6f8fb0' });
setState('menu');
renderCard();
void selectLevel(index);
requestAnimationFrame(loop);

// Inspection hook used by the automated browser checks (read-only state; does not affect play).
const DEBUG = new URLSearchParams(location.search).has('debug');
(window as any).__nj = {
  ...(DEBUG ? { preview: (t: number) => { if (!game) return; game.prepare(t); world.seek(t); readyFrom = t; readyKind = 'start'; setReady(); } } : {}), get state() { return state; }, get game() { return game; }, audio, world, get level() { return level; }, save, selectLevel: (i: number) => selectLevel(i), stats: () => world.stats() };

// Stale-build guard: index.html can be cached by the browser/CDN (GitHub Pages max-age 600). If the deployed build.json names a
// newer build than this bundle, reload once with a cache-busting query so players never sit on an old build.
declare const __BUILD__: string;
(async () => {
  try {
    const r = await fetch(`build.json?t=${Date.now()}`, { cache: 'no-store' }); if (!r.ok) return;
    const j = await r.json(); const want = String(j.preview_of ?? j.build ?? '').split('@').pop();
    if (!want || want === __BUILD__ || sessionStorage.getItem('nj-reloaded') === want) return;
    sessionStorage.setItem('nj-reloaded', want); const u = new URL(location.href); u.searchParams.set('v', want); location.replace(u.toString());
  } catch { /* offline or no build.json: keep running */ }
})();

// iOS / Safari: every gesture re-unlocks audio synchronously (touchend / click / keydown are activations; pointerdown is not),
// which also recovers the iOS-only 'interrupted' state after calls, Siri or the lock screen.
for (const ev of ['touchend', 'click', 'keydown']) document.addEventListener(ev, () => { if (audio.state !== 'running') audio.unlock(); }, { capture: true, passive: true });
