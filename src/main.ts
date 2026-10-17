import './style.css';
import rawLevels from './levels.json';
import { GameEngine } from './engine';
import { AudioTransport } from './audio';
import { WorldRenderer } from './world';
import { getLevelArt } from './level-design';
import { emptyRecord, loadSave, persistSave, validateSave } from './storage';
import type { GameSnapshot, Level, LevelRecord } from './types';

const levels = (rawLevels as Level[]).filter(level => !level.instrumental);
if (!levels.length) throw new Error('歌曲资源尚未准备好。');
const initial = levels.find(level => /new jeans/i.test(level.title)) ?? levels[0];
let save = loadSave(levels.map(level => level.id), initial.id);
let selected = levels.findIndex(level => level.id === save.selected);
// Album imagery and authored captions are resolved once, never in the render loop.
const levelArt = new Map(levels.map(song => [song.id, getLevelArt(song.id)]));
let selectedArt = levelArt.get(levels[selected].id)!;
let practice = false;
let mode: 'menu' | 'game' = 'menu';
let loading = false;
let requestId = 0;
let finished = false;
let showing: 'library' | 'records' | 'settings' | 'pause' | 'result' | null = null;
let search = '';
let album = 'all';
let toastTimer = 0;
let lastRatingKey = '';
const level = () => levels[selected];
const record = (id = level().id): LevelRecord => save.records[id] ?? emptyRecord();
const percent = (value: number) => `${Math.floor(value * 100)}%`;
const duration = (seconds: number) => `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
const escapeHtml = (text: string) => text.replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]!));
const paths: Record<string, string> = {
  play: '<path d="m9 5 11 7-11 7z"/>', pause: '<path d="M9 5v14M15 5v14"/>',
  left: '<path d="m15 5-7 7 7 7"/>', right: '<path d="m9 5 7 7-7 7"/>', close: '<path d="m6 6 12 12M18 6 6 18"/>',
  crown: '<path d="m3 6 5 4 4-6 4 6 5-4-3 13H6z"/>', diamond: '<path d="m12 3 9 7-9 11L3 10zM3 10h18M8 4l4 17 4-17"/>',
  settings: '<path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"/><path d="m9 3-1 3-3 1-2 3 2 3-1 3 3 2 3-1 2 3 3-1 1-3 3-1 1-3-2-2 1-3-3-2-3 1z"/>',
  journey: '<path d="m4 20 5-5-3-4 5-5M15 4h5v5M15 9l5-5"/><circle cx="4" cy="20" r="1"/>',
  music: '<path d="M9 18V5l12-2v13M9 9l12-2"/><ellipse cx="6" cy="18" rx="3" ry="3"/><ellipse cx="18" cy="16" rx="3" ry="3"/>',
  trophy: '<path d="M8 3h8v6a4 4 0 0 1-8 0zM8 5H4v3a4 4 0 0 0 4 4M16 5h4v3a4 4 0 0 1-4 4M12 13v7M8 21h8"/>',
  repeat: '<path d="M3 10a8 8 0 1 1 1 7M3 4v6h6"/>', home: '<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3z"/>',
  volume: '<path d="M11 4 6 8H3v8h3l5 4zM15 8a6 6 0 0 1 0 8M18 5a10 10 0 0 1 0 14"/>',
  download: '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>', upload: '<path d="M12 16V4m-5 5 5-5 5 5M4 16v5h16v-5"/>',
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>', check: '<path d="m5 12 4 4L19 6"/>', arrow: '<path d="M4 12h16m-6-6 6 6-6 6"/>',
};
const icon = (name: string, cls = '') => `<svg class="icon ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name] ?? ''}</svg>`;
const crowns = (count: number) => Array.from({ length: 3 }, (_, i) => `<span class="crown-slot ${i < count ? 'earned' : ''}" aria-hidden="true">${icon('crown')}</span>`).join('');
const diamonds = (count: number) => Array.from({ length: 10 }, (_, i) => `<i class="diamond-pip ${i < count ? 'earned' : ''}"></i>`).join('');

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <canvas id="world" aria-label="音乐道路场景，游戏中轻点转弯" tabindex="0" data-testid="game-canvas"></canvas>
  <div class="scene-vignette"></div>
  <main class="menu" id="menu">
    <header class="topbar">
      <div class="collection" aria-label="本地收集进度"><span>${icon('crown')}<b id="total-crowns">0</b><small>/ ${levels.length * 3}</small></span><span>${icon('diamond')}<b id="total-diamonds">0</b><small>/ ${levels.length * 10}</small></span></div>
      <button class="icon-button settings-button" data-action="settings" aria-label="游戏设置" data-testid="settings-button">${icon('settings')}</button>
    </header>
    <div class="wordmark"><div class="edition"><span></span> NEWJEANS EDITION <span></span></div><h1>跳舞的线</h1><p>DANCING LINE</p></div>
    <div class="scene-caption" aria-hidden="true"><span id="chapter-label">01 / 16</span><i></i><span>FOLLOW THE MUSIC</span></div>
    <section class="song-stage" aria-label="选择歌曲">
      <button class="song-arrow previous" data-action="previous" aria-label="上一首" data-testid="previous-song">${icon('left')}</button>
      <div class="song-info"><div class="song-album"><img id="song-cover" class="song-cover" alt="" width="30" height="30"><div class="song-meta" id="song-meta"></div></div><h2 id="song-title" data-testid="song-title"></h2><p class="song-artist">NewJeans <span>·</span> <span id="song-duration"></span></p><p class="song-scene" id="song-scene"></p><p class="song-description" id="song-description"></p><div class="crowns" id="song-crowns"></div><div class="song-progress"><div class="diamond-row" id="song-diamonds" aria-hidden="true"></div><span id="song-best"></span></div></div>
      <button class="song-arrow next" data-action="next" aria-label="下一首" data-testid="next-song">${icon('right')}</button>
      <div class="start-area"><button class="start-button" data-action="start" data-testid="start-button">${icon('play')}<span>开始旅程</span></button><label class="practice-switch"><input id="practice" type="checkbox" data-testid="practice-toggle"><span class="switch-track"></span><span>练习模式</span><small>失误后继续前行</small></label></div>
    </section>
    <div class="level-dots" id="level-dots" aria-label="曲目进度"></div>
    <nav class="bottom-nav" aria-label="主导航"><button class="active" data-action="journey" aria-current="page">${icon('journey')}<span>旅程</span></button><button data-action="library" data-testid="nav-library">${icon('music')}<span>曲库</span></button><button data-action="records" data-testid="nav-records">${icon('trophy')}<span>记录</span></button></nav>
    <span class="local-note">音乐在耳边，旅程在指尖。</span>
  </main>
  <section class="hud" id="hud" hidden aria-label="游戏状态">
    <div class="hud-top"><div class="hud-song"><span id="hud-song"></span><small id="hud-practice"></small></div><button class="icon-button" data-action="pause" aria-label="暂停游戏" data-testid="pause-button">${icon('pause')}</button></div>
    <div class="hud-progress" data-testid="hud-progress" role="progressbar" aria-label="歌曲进度" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="hud-progress-fill" id="hud-fill"></div><span class="crown-marker" style="left:30%">${icon('crown')}</span><span class="crown-marker" style="left:60%">${icon('crown')}</span><span class="crown-marker" style="left:100%">${icon('crown')}</span></div>
    <div class="hud-numbers"><span id="hud-percent" data-testid="hud-percent">0%</span><span>${icon('diamond')}<b id="hud-diamonds" data-testid="hud-diamonds">0</b><small>/ 10</small></span></div>
    <div class="rating" id="rating" aria-hidden="true"></div>
    <div class="turn-hint" id="turn-hint">跟随音乐，在拐角轻点<span>点击屏幕 / 空格键转弯 · Esc 暂停</span></div>
    <div class="hud-bottom"><span id="hud-section"></span><span id="hud-combo"></span></div>
  </section>
  <div class="loading-screen" id="loading" hidden role="status"><div class="loading-art"><img id="loading-concept" alt="" width="960" height="640"><span>关卡概念图 · 游戏原创演绎</span></div><div class="loading-copy"><div class="loading-orbit" aria-hidden="true"></div><p class="eyebrow">NEXT LANDSCAPE</p><h2 id="loading-scene">让音乐就位</h2><p id="loading-title"></p><p id="loading-description" class="loading-description"></p><button class="text-button" data-action="cancel-load">返回旅程</button></div></div>
  <dialog id="dialog" aria-labelledby="dialog-title"><div id="dialog-content"></div></dialog>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <input type="file" id="import-file" accept="application/json,.json" hidden>
`;

const $ = <T extends HTMLElement = HTMLElement>(selector: string) => document.querySelector<T>(selector)!;
const canvas = $<HTMLCanvasElement>('#world');
const dialog = $<HTMLDialogElement>('#dialog');
const audio = new AudioTransport();
audio.setVolume(save.settings.volume);
let engine = new GameEngine(level(), { practice, offsetMs: save.settings.offsetMs });
let snapshot: GameSnapshot = engine.snapshot();
let world: WorldRenderer | null = null;
try { world = new WorldRenderer(canvas); world.load(level()); } catch (error) { toast('当前浏览器无法显示 3D 场景，请开启硬件加速后重试。'); console.error(error); }

function store() {
  if (!persistSave(save)) toast('浏览器暂时无法保存记录。可在设置中导出存档。');
}
function toast(message: string) {
  if (dialog.open) {
    let feedback = dialog.querySelector<HTMLParagraphElement>('.dialog-feedback');
    if (!feedback) { feedback = document.createElement('p'); feedback.className = 'dialog-feedback'; feedback.setAttribute('role', 'status'); $('#dialog-content').append(feedback); }
    feedback.textContent = message;
    feedback.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    return;
  }
  $('#toast').textContent = message;
  $('#toast').classList.add('visible');
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => $('#toast').classList.remove('visible'), 4200);
}
function totals() {
  const records = Object.values(save.records);
  return { crowns: records.reduce((sum, r) => sum + r.crowns, 0), diamonds: records.reduce((sum, r) => sum + r.diamonds, 0), completed: records.filter(r => r.completed).length, attempts: records.reduce((sum, r) => sum + r.attempts, 0) };
}
function updateMenu() {
  const song = level();
  const best = record();
  document.documentElement.style.setProperty('--accent', selectedArt.colors.accent);
  document.documentElement.style.setProperty('--scene-ink', selectedArt.dark ? '#FFF6E8' : `color-mix(in srgb, ${selectedArt.colors.ink} 78%, #0D1630)`);
  document.documentElement.style.setProperty('--scene-background', selectedArt.colors.background);
  document.body.dataset.art = selectedArt.family;
  document.body.dataset.dark = String(selectedArt.dark);
  const cover = $<HTMLImageElement>('#song-cover');
  cover.src = selectedArt.cover;
  cover.alt = `${song.album} 专辑封面`;
  $('#song-scene').textContent = selectedArt.subtitle;
  $('#song-description').textContent = selectedArt.description;
  $('#song-title').textContent = song.title;
  $('#song-meta').textContent = `${song.album}  /  ${['', '轻盈', '轻快', '进阶', '挑战', '极限'][song.difficulty]}`;
  $('#song-duration').textContent = duration(song.duration);
  $('#song-crowns').innerHTML = crowns(best.crowns);
  $('#song-crowns').setAttribute('aria-label', `已收集 ${best.crowns} / 3 皇冠`);
  $('#song-diamonds').innerHTML = diamonds(best.diamonds);
  $('#song-best').textContent = `${best.diamonds} / 10  ·  ${percent(best.best)}${best.completed ? ' 已完成' : ''}`;
  $('#chapter-label').textContent = `${String(selected + 1).padStart(2, '0')} / ${String(levels.length).padStart(2, '0')}`;
  $('#total-crowns').textContent = String(totals().crowns);
  $('#total-diamonds').textContent = String(totals().diamonds);
  $('#level-dots').innerHTML = levels.map((song, i) => `<button class="${i === selected ? 'current' : ''} ${record(song.id).completed ? 'completed' : ''}" data-song="${i}" aria-label="选择 ${escapeHtml(song.title)}" ${i === selected ? 'aria-current="true"' : ''}></button>`).join('');
  $<HTMLInputElement>('#practice').checked = practice;
}
function choose(index: number) {
  if (loading || mode === 'game') return;
  selected = (index + levels.length) % levels.length;
  selectedArt = levelArt.get(level().id)!;
  save.selected = level().id;
  store();
  engine = new GameEngine(level(), { practice, offsetMs: save.settings.offsetMs });
  snapshot = engine.snapshot();
  world?.load(level());
  updateMenu();
}
function closeDialog() {
  if (dialog.open) dialog.close();
  showing = null;
  document.querySelectorAll('.bottom-nav button').forEach(button => { button.classList.toggle('active', button.getAttribute('data-action') === 'journey'); button.removeAttribute('aria-current'); });
  $('.bottom-nav button').setAttribute('aria-current', 'page');
}
function openDialog(type: NonNullable<typeof showing>, html: string, compact = false) {
  showing = type;
  dialog.className = compact ? 'compact-dialog' : 'sheet-dialog';
  $('#dialog-content').innerHTML = html;
  if (!dialog.open) dialog.showModal();
  document.querySelectorAll('.bottom-nav button').forEach(button => {
    const active = button.getAttribute('data-action') === type;
    button.classList.toggle('active', active);
    if (active) button.setAttribute('aria-current', 'page'); else button.removeAttribute('aria-current');
  });
}
const sheetHead = (eyebrow: string, title: string, description: string) => `<header class="sheet-head"><div><p class="eyebrow">${eyebrow}</p><h2 id="dialog-title">${title}</h2><p>${description}</p></div><button class="icon-button" data-action="close" aria-label="关闭">${icon('close')}</button></header>`;

function showLibrary() {
  openDialog('library', `${sheetHead('THE COLLECTION', '每首歌，一段新风景', `${levels.length} 首完整人声曲目 · 所有旅程均已开放`)}<div class="library-tools"><label class="search-box">${icon('search')}<input id="song-search" aria-label="搜索歌曲" placeholder="寻找你的那首歌" value="${escapeHtml(search)}" data-testid="song-search"></label><label class="album-select"><span class="sr-only">专辑筛选</span><select id="album-filter"><option value="all">全部专辑</option>${[...new Set(levels.map(l => l.album))].map(a => `<option value="${escapeHtml(a)}" ${a === album ? 'selected' : ''}>${escapeHtml(a)}</option>`).join('')}</select></label></div><div id="library-list" class="song-list"></div><p class="sheet-footnote">封面来自对应专辑 · 场景与故事为本游戏的原创演绎。</p>`);
  renderLibrary();
}
function renderLibrary() {
  const filtered = levels.filter(song => (album === 'all' || song.album === album) && `${song.title} ${song.album}`.toLowerCase().includes(search.toLowerCase().trim()));
  $('#library-list').innerHTML = filtered.length ? filtered.map(song => {
    const i = levels.indexOf(song), best = record(song.id), art = levelArt.get(song.id)!;
    return `<button class="song-row ${i === selected ? 'selected' : ''}" data-song="${i}" data-testid="song-row"><span class="track-art"><img src="${escapeHtml(art.cover)}" alt="" width="49" height="49" loading="lazy"><span>${String(i + 1).padStart(2, '0')}</span></span><span class="track-text"><strong>${escapeHtml(song.title)}</strong><small>${escapeHtml(art.subtitle)} <span>·</span> ${duration(song.duration)}</small><span class="track-description">${escapeHtml(art.description)}</span></span><span class="track-record"><span class="tiny-crowns">${crowns(best.crowns)}</span><small>${percent(best.best)}</small></span>${icon(i === selected ? 'check' : 'right')}</button>`;
  }).join('') : '<div class="empty-state">没有找到这首歌。<small>试试歌曲名或另一个专辑。</small></div>';
}
function showRecords() {
  const total = totals();
  openDialog('records', `${sheetHead('YOUR JOURNEY', '每一步，都算数', '这里只记录普通模式的成绩。练习，留给自由发挥。')}<div class="record-summary"><div><b>${total.completed}<small> / ${levels.length}</small></b><span>完整旅程</span></div><div><b>${total.crowns}<small> / ${levels.length * 3}</small></b><span>收集皇冠</span></div><div><b>${total.diamonds}<small> / ${levels.length * 10}</small></b><span>收集钻石</span></div></div><div class="record-list">${levels.map((song, i) => {
    const best = record(song.id), art = levelArt.get(song.id)!;
    return `<button class="record-row" data-song="${i}"><span class="record-index">${String(i + 1).padStart(2, '0')}</span><img class="record-cover" src="${escapeHtml(art.cover)}" alt="" width="35" height="35" loading="lazy"><span class="record-track"><strong>${escapeHtml(song.title)}</strong><span class="record-bar"><i style="width:${best.best * 100}%;background:${art.colors.accent}"></i></span></span><span class="record-value">${percent(best.best)}<small>${best.attempts ? `${best.attempts} 次尝试` : '等待出发'}</small></span>${best.completed ? icon('check') : icon('right')}</button>`;
  }).join('')}</div><p class="sheet-footnote">已出发 ${total.attempts} 次 · 记录保存在当前浏览器中</p>`);
}
function showSettings() {
  const s = save.settings;
  openDialog('settings', `${sheetHead('MAKE IT YOURS', '找到你的节奏', '戴上耳机，跟着旋律前行。')}<div class="settings-list"><div class="setting-range"><label for="volume">${icon('volume')}音乐音量 <output id="volume-value">${Math.round(s.volume * 100)}%</output></label><input type="range" id="volume" min="0" max="100" value="${Math.round(s.volume * 100)}" data-testid="volume-slider"></div><div class="setting-range"><label for="offset">节奏校准 <output id="offset-value">${s.offsetMs > 0 ? '+' : ''}${s.offsetMs} ms</output></label><input type="range" id="offset" min="-500" max="500" step="10" value="${s.offsetMs}" data-testid="latency-slider"><p>正值让道路进度晚于音乐。蓝牙耳机可尝试调整；0 ms 为默认。</p></div><label class="setting-toggle"><span><strong>轻量画质</strong><small>降低分辨率，减少设备负担</small></span><input type="checkbox" id="quality" ${s.quality === 'low' ? 'checked' : ''}><span class="switch-track"></span></label><label class="setting-toggle"><span><strong>触感反馈</strong><small>成功转弯时轻振（设备支持时）</small></span><input type="checkbox" id="vibration" ${s.vibration ? 'checked' : ''}><span class="switch-track"></span></label><label class="setting-toggle"><span><strong>道路引导</strong><small>在道路上显示转弯标记</small></span><input type="checkbox" id="guide" ${s.guide ? 'checked' : ''} data-testid="guide-toggle"><span class="switch-track"></span></label></div><div class="save-section"><p class="eyebrow">ONLY ON THIS DEVICE</p><h3>把旅程留在身边</h3><p>设置和成绩仅保存在当前浏览器。导出一份存档，就能在其他设备导入；导入会替换当前记录。</p><div class="save-actions"><button class="secondary-button" data-action="export" data-testid="export-save">${icon('download')}导出存档</button><button class="secondary-button" data-action="import" data-testid="import-save">${icon('upload')}导入存档</button></div></div>`);
}

async function startGame(asPractice = practice) {
  if (loading) return;
  practice = asPractice;
  closeDialog();
  const operation = ++requestId;
  loading = true;
  finished = false;
  audio.stop();
  $('#menu').hidden = true;
  $('#hud').hidden = true;
  $('#loading').hidden = false;
  $('#loading-title').textContent = `${level().title} · ${duration(level().duration)}`;
  $<HTMLImageElement>('#loading-concept').src = selectedArt.concept;
  $('#loading-scene').textContent = selectedArt.subtitle;
  $('#loading-description').textContent = selectedArt.description;
  const song = level();
  try {
    const url = new URL(song.audio, document.baseURI).href;
    await audio.load(url);
    if (operation !== requestId) return;
    if (Math.abs(audio.duration - song.duration) > 0.2) throw new Error('歌曲与道路时长不匹配，请刷新后重试。');
    audio.setVolume(save.settings.volume);
    await audio.play(0);
    if (operation !== requestId) { audio.stop(); return; }
    engine = new GameEngine(song, { practice, offsetMs: save.settings.offsetMs });
    snapshot = engine.start();
    mode = 'game';
    loading = false;
    $('#loading').hidden = true;
    $('#hud').hidden = false;
    $('#hud-song').textContent = song.title;
    $('#hud-practice').textContent = practice ? '练习模式 · 不计入记录' : 'FOLLOW THE MUSIC';
    $('#turn-hint').hidden = totals().attempts > 2;
    if (!practice) { save.records[song.id] = { ...record(song.id), attempts: record(song.id).attempts + 1 }; store(); }
    document.body.dataset.mode = 'game';
    lastRatingKey = '';
    canvas.focus({ preventScroll: true });
    updateHud();
  } catch (error) {
    if (operation !== requestId) return;
    loading = false;
    audio.stop();
    $('#loading').hidden = true;
    $('#menu').hidden = false;
    toast(`音乐加载失败：${error instanceof Error ? error.message : '请检查音频文件后重试'}`);
  }
}
function goHome() {
  saveRun();
  requestId++;
  loading = false;
  audio.stop();
  mode = 'menu';
  closeDialog();
  $('#loading').hidden = true;
  $('#hud').hidden = true;
  $('#menu').hidden = false;
  document.body.dataset.mode = 'menu';
  engine = new GameEngine(level(), { practice, offsetMs: save.settings.offsetMs });
  snapshot = engine.snapshot();
  world?.load(level());
  updateMenu();
}
function pauseGame() {
  if (mode !== 'game' || snapshot.status !== 'playing') return;
  snapshot = engine.update(musicTime());
  if (snapshot.status !== 'playing') { endGame(); return; }
  audio.pause();
  snapshot = engine.pause();
  saveRun();
  openDialog('pause', `<div class="result-content"><p class="eyebrow">TAKE A BREATH</p><h2 id="dialog-title">让旋律等一等</h2><p>${escapeHtml(level().title)} · ${percent(snapshot.progress)}${practice ? ' · 练习中' : ''}</p><button class="start-button" data-action="resume" data-testid="resume-button">${icon('play')}继续旅程</button><div class="result-actions"><button data-action="restart">${icon('repeat')}重新开始</button><button data-action="home" data-testid="home-button">${icon('home')}返回旅程</button></div></div>`, true);
}
async function resumeGame() {
  if (snapshot.status !== 'paused') return;
  const operation = requestId;
  try { await audio.play(); if (operation !== requestId) return; snapshot = engine.resume(); closeDialog(); canvas.focus({ preventScroll: true }); }
  catch { toast('音乐暂时无法播放，请再次点击继续。'); }
}
function endGame() {
  if (finished || (snapshot.status !== 'failed' && snapshot.status !== 'complete')) return;
  finished = true;
  audio.pause();
  const complete = snapshot.status === 'complete';
  const previous = record();
  const newBest = !practice && Math.floor(snapshot.progress * 100) > Math.floor(previous.best * 100);
  saveRun();
  const headline = complete ? (practice ? '练习，也是旅程' : '这一路，为你加冕') : '再听一次，再近一点';
  const note = complete ? '旋律有终点，喜欢没有。' : (snapshot.failureReason ?? '在拐角到来的那一刻，轻点屏幕。');
  openDialog('result', `<div class="result-content"><p class="eyebrow">${practice ? 'PRACTICE SESSION' : complete ? 'JOURNEY COMPLETE' : newBest ? 'A NEW PERSONAL BEST' : 'ONE MORE TRY'}</p><h2 id="dialog-title">${headline}</h2><p class="result-song"><img class="result-cover" src="${escapeHtml(selectedArt.cover)}" alt="${escapeHtml(level().album)} 专辑封面" width="32" height="32"><span>${escapeHtml(level().title)}</span></p><p class="result-scene">${escapeHtml(selectedArt.subtitle)}</p><div class="result-crowns" aria-label="${snapshot.crowns} 皇冠">${crowns(snapshot.crowns)}</div><div class="result-percent" data-testid="result-percent">${percent(snapshot.progress)}</div><div class="result-stats"><span>${icon('diamond')}${snapshot.diamonds} / 10</span><span>节奏准确率 ${snapshot.accuracy.toFixed(1)}%</span></div><p class="result-note">${escapeHtml(note)}</p>${practice ? '<p class="practice-note">练习成绩不计入普通模式记录</p>' : ''}<button class="start-button" data-action="${complete ? 'next-level' : 'restart'}" data-testid="retry-button">${icon(complete ? 'arrow' : 'repeat')}${complete ? '下一段旅程' : '再来一次'}</button><div class="result-actions">${complete ? `<button data-action="restart">${icon('repeat')}再次挑战</button>` : !practice ? `<button data-action="practice">${icon('music')}先练习一下</button>` : ''}<button data-action="home" data-testid="home-button">${icon('home')}返回旅程</button></div></div>`, true);
}
function saveRun() {
  if (mode !== 'game' || practice) return;
  const previous = record();
  if (snapshot.progress <= previous.best) return;
  save.records[level().id] = { ...previous, best: snapshot.progress, diamonds: Math.max(previous.diamonds, snapshot.diamonds), crowns: Math.max(previous.crowns, snapshot.crowns), completed: previous.completed || snapshot.status === 'complete' };
  store();
}
function updateHud() {
  $('#hud-percent').textContent = percent(snapshot.progress);
  $('#hud-fill').style.width = `${snapshot.progress * 100}%`;
  $('[data-testid="hud-progress"]').setAttribute('aria-valuenow', String(Math.floor(snapshot.progress * 100)));
  $('#hud-diamonds').textContent = String(snapshot.diamonds);
  const section = level().sections.filter(section => section.at <= snapshot.time).at(-1);
  $('#hud-section').textContent = section?.label ?? '';
  $('#hud-combo').textContent = snapshot.combo > 1 ? `${snapshot.combo} 连续转弯` : '';
  if (snapshot.turnsHit >= 2 || snapshot.time > 12) $('#turn-hint').hidden = true;
  const key = `${snapshot.turnsHit}:${snapshot.lastRating}:${snapshot.status}`;
  if (key !== lastRatingKey && snapshot.lastRating) {
    lastRatingKey = key;
    const rating = $('#rating');
    rating.textContent = snapshot.lastRating === 'perfect' ? 'PERFECT' : snapshot.lastRating === 'good' ? 'NICE' : practice ? '继续前行' : '';
    rating.classList.remove('pop');
    void rating.offsetWidth;
    rating.classList.add('pop');
    if (save.settings.vibration && snapshot.lastRating !== 'miss') navigator.vibrate?.(12);
  }
  document.querySelectorAll<HTMLElement>('.crown-marker').forEach((marker, i) => marker.classList.toggle('earned', i < snapshot.crowns));
}
function musicTime() {
  const time = audio.currentTime;
  return audio.duration > 0 && time >= audio.duration && Math.abs(audio.duration - level().duration) <= 0.2 ? level().duration : time;
}
function tap() {
  if (loading || dialog.open || mode !== 'game' || snapshot.status !== 'playing') return;
  snapshot = engine.tap(musicTime());
  updateHud();
  endGame();
}
canvas.addEventListener('pointerdown', event => { if (event.button !== 0) return; event.preventDefault(); tap(); });
window.addEventListener('keydown', event => {
  if (event.target instanceof HTMLInputElement || event.target instanceof HTMLSelectElement || event.target instanceof HTMLTextAreaElement) return;
  if (event.code === 'Space' && mode === 'game' && !dialog.open) { event.preventDefault(); if (!event.repeat) tap(); }
  if (event.key === 'Escape' && mode === 'game' && !dialog.open) { event.preventDefault(); pauseGame(); }
  if (mode === 'menu' && !dialog.open && !loading && (event.key === 'ArrowLeft' || event.key === 'ArrowRight')) { event.preventDefault(); choose(selected + (event.key === 'ArrowLeft' ? -1 : 1)); }
});
document.addEventListener('visibilitychange', () => { if (document.hidden) { if (loading) goHome(); else pauseGame(); } });
window.addEventListener('blur', () => { if (!loading) pauseGame(); });
window.addEventListener('resize', () => world?.resize());
dialog.addEventListener('cancel', event => { event.preventDefault(); if (showing === 'pause') void resumeGame(); else if (showing === 'result') goHome(); else closeDialog(); });
dialog.addEventListener('click', event => { if (event.target === dialog && showing !== 'pause' && showing !== 'result') closeDialog(); });

document.addEventListener('click', event => {
  const target = (event.target as HTMLElement).closest<HTMLElement>('[data-action], [data-song]');
  if (!target) return;
  if (target.dataset.song !== undefined) { const index = Number(target.dataset.song); closeDialog(); choose(index); return; }
  switch (target.dataset.action) {
    case 'previous': choose(selected - 1); break;
    case 'next': choose(selected + 1); break;
    case 'start': void startGame(); break;
    case 'journey': closeDialog(); break;
    case 'library': showLibrary(); break;
    case 'records': showRecords(); break;
    case 'settings': showSettings(); break;
    case 'close': closeDialog(); break;
    case 'pause': pauseGame(); break;
    case 'resume': void resumeGame(); break;
    case 'restart': void startGame(); break;
    case 'practice': void startGame(true); break;
    case 'home': case 'cancel-load': goHome(); break;
    case 'next-level': goHome(); choose(selected + 1); void startGame(); break;
    case 'export': {
      const blob = new Blob([JSON.stringify(save, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob), a = document.createElement('a');
      a.href = url; a.download = `newjeans-line-${new Date().toISOString().slice(0, 10)}.json`; a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000); toast('旅程已导出。'); break;
    }
    case 'import': $<HTMLInputElement>('#import-file').click(); break;
  }
});
document.addEventListener('input', event => {
  const input = event.target as HTMLInputElement;
  if (input.id === 'song-search') { search = input.value; renderLibrary(); return; }
  if (input.id === 'volume') { save.settings.volume = Number(input.value) / 100; audio.setVolume(save.settings.volume); $('#volume-value').textContent = `${input.value}%`; store(); }
  if (input.id === 'offset') { save.settings.offsetMs = Number(input.value); $('#offset-value').textContent = `${Number(input.value) > 0 ? '+' : ''}${input.value} ms`; store(); }
});
document.addEventListener('change', event => {
  const input = event.target as HTMLInputElement;
  if (input.id === 'practice') practice = input.checked;
  if (input.id === 'album-filter') { album = input.value; renderLibrary(); }
  if (input.id === 'quality') { save.settings.quality = input.checked ? 'low' : 'high'; store(); }
  if (input.id === 'vibration') { save.settings.vibration = input.checked; store(); }
  if (input.id === 'guide') { save.settings.guide = input.checked; store(); }
});
$<HTMLInputElement>('#import-file').addEventListener('change', async event => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;
  try {
    if (file.size > 1024 * 1024) throw new Error('存档文件过大，请选择游戏导出的 JSON 文件。');
    const imported = validateSave(JSON.parse(await file.text()), levels.map(song => song.id));
    save = imported; selected = levels.findIndex(song => song.id === save.selected); audio.setVolume(save.settings.volume);
    closeDialog(); choose(selected); toast('旅程已导入，欢迎回来。');
  } catch (error) { toast(error instanceof Error ? error.message : '无法读取这份存档。'); }
  input.value = '';
});

updateMenu();
document.body.dataset.mode = 'menu';
const startedAt = performance.now();
function frame(now: number) {
  if (mode === 'game' && snapshot.status === 'playing') { snapshot = engine.update(musicTime()); updateHud(); endGame(); }
  world?.render(snapshot, { mode, elapsed: (now - startedAt) / 1000, quality: save.settings.quality, guide: save.settings.guide });
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.addEventListener('pagehide', () => { audio.pause(); saveRun(); });
