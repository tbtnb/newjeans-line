// Scripted player + optional real-audio screen recording (Xvfb + PulseAudio + ffmpeg).
// THIS IS A SCRIPTED SIMULATION (CDP touch events), NOT physical-device play, and NOT a proof of music sync.
// usage: node tools/qa/play.mjs --url URL --level 5 --w 540 --h 960 [--from 0] [--to 999] [--record out.mp4]
//        [--jitter 0.012] [--miss 120.5] [--double 80.2] [--extra 30.0] [--pauseAt 60] [--log out.json]
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const A = Object.fromEntries(process.argv.slice(2).reduce((acc, v, i, arr) => (v.startsWith('--') ? [...acc, [v.slice(2), arr[i + 1]?.startsWith('--') || arr[i + 1] === undefined ? '1' : arr[i + 1]]] : acc), []));
const dbg = (...a) => { if (A.verbose) console.error('[play]', ...a); };
const W = +(A.w ?? 540), H = +(A.h ?? 960), level = +(A.level ?? 5);
const headless = !A.record && !A.headed;
const browser = await chromium.launch({ headless, executablePath: '/usr/bin/google-chrome', env: { ...process.env, DISPLAY: process.env.DISPLAY ?? ':99' },
  args: ['--autoplay-policy=no-user-gesture-required', '--window-position=0,0', `--window-size=${W},${H + 120}`, '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-features=Translate', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-infobars'] });
const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, hasTouch: true, isMobile: !!A.mobile });
const page = await ctx.newPage();
const logs = []; page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') logs.push(m.type() + ': ' + m.text()); }); page.on('pageerror', e => logs.push('PAGEERROR ' + e.message));
await page.goto(A.url ?? 'http://127.0.0.1:4173/?debug');
await page.waitForFunction(() => window.__nj);
await page.evaluate(i => window.__nj.selectLevel(i), level);
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 60000 });
await page.waitForTimeout(1500);
const cdp = await ctx.newCDPSession(page);
// Fire-and-forget: the browser stamps the event when it receives it (measured within ~1-4 ms of send);
// awaiting the reply would serialize taps behind slow software-rendered frames.
const pending = [];
const touch = (x = W / 2, y = H * 0.6) => {
  pending.push(cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y, id: 1 }] }));
  pending.push(cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }));
};
let ff = null;
if (A.record) {
  const geo = await page.evaluate(() => ({ x: window.screenX, y: window.screenY + (window.outerHeight - window.innerHeight), ow: window.outerWidth, oh: window.outerHeight, iw: window.innerWidth, ih: window.innerHeight }));
  const ox = Math.max(0, geo.x + Math.round((geo.ow - geo.iw) / 2)), oy = Math.max(0, geo.y);
  ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-thread_queue_size', '1024', '-f', 'x11grab', '-draw_mouse', '0', '-framerate', '30', '-video_size', `${W}x${H}`, '-i', `${process.env.DISPLAY ?? ':99'}+${ox},${oy}`,
    '-thread_queue_size', '1024', '-f', 'pulse', '-i', 'rec.monitor', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', A.record], { stdio: ['pipe', 'inherit', 'inherit'] });
  await page.waitForTimeout(800);
}
// menu shot, then enter level (tap on menu), optionally from a checkpoint-like start
await page.waitForTimeout(+(A.menuHold ?? 1200));
const from = +(A.from ?? 0);
if (from > 0) await page.evaluate(t => window.__nj.preview(t), from);
else await page.mouse.click(W / 2, H * 0.55);
await page.waitForFunction(() => window.__nj.state === 'ready', null, { timeout: 60000 });
await page.waitForTimeout(900);
const taps = await page.evaluate(() => window.__nj.game.taps);
const to = Math.min(+(A.to ?? 1e9), await page.evaluate(() => window.__nj.level.duration));
await page.evaluate(() => { window.__runlog = { fails: [], turns: null }; setInterval(() => { const g = window.__nj.game; if (!g) return; if (g.status === 'failed' && !window.__runlog.fails.some(f => f.t === g.failTime)) window.__runlog.fails.push({ t: g.failTime, kind: g.failKind, cursor: g.cursor, next: g.taps[g.cursor], errors: g.turns.slice(-6).map(r => Math.round((r.tapT - r.chartT) * 1000)) }); if (g.turns.length) window.__runlog.turns = g.turns.map(r => [r.chartT, r.tapT]); }, 20); });
dbg('start tap'); touch(); // start tap
// clock sync node<->page
// Same machine => both processes share the wall clock; map via timeOrigin (no round-trip bias).
const sync = async () => { const r = await page.evaluate(() => ({ s: window.__nj.audio.songTime(), e: performance.timeOrigin + performance.now(), st: window.__nj.game.status })); return { song: r.s, node: r.e - performance.timeOrigin, status: r.st }; };
await page.waitForFunction(() => window.__nj.audio.playing && window.__nj.audio.songTime() > 0.15, null, { timeout: 10000, polling: 5 });
let ref = await sync(); dbg('synced', ref);
const songNow = () => ref.song + (performance.now() - ref.node) / 1000;
const jitter = +(A.jitter ?? 0);
const gauss = () => { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
const plan = [];
const missAt = A.miss ? +A.miss : null, dblAt = A.double ? +A.double : null, extraAt = A.extra ? +A.extra : null, pauseAt = A.pauseAt ? +A.pauseAt : null;
for (const t of taps) { if (t <= from + 0.01 || t > to) continue; if (missAt !== null && Math.abs(t - missAt) < 0.12) continue; plan.push({ t: t + jitter * gauss(), kind: 'tap' }); if (dblAt !== null && Math.abs(t - dblAt) < 0.12) plan.push({ t: t + 0.012, kind: 'double' }); }
if (extraAt !== null) plan.push({ t: extraAt, kind: 'extra' });
plan.sort((a, b) => a.t - b.t);
const sent = []; let lastSync = performance.now(); let paused = false;
const busyUntil = async target => { while (songNow() < target - 0.004) { const dt = (target - songNow()) * 1000; await new Promise(r => setTimeout(r, Math.max(0, Math.min(dt - 6, 50)))); if (dt < 8) break; } while (songNow() < target) { /* spin */ } };
for (const p of plan) {
  if (pauseAt !== null && !paused && p.t > pauseAt) {
    paused = true; await busyUntil(pauseAt);
    await page.click('#btn-pause'); await page.waitForTimeout(1200);
    await page.click('#btn-resume'); await page.waitForTimeout(800);
    await touch(); await page.waitForFunction(() => window.__nj.audio.playing); ref = await sync();
    const resumeFrom = await page.evaluate(() => window.__nj.game.startTime); sent.push({ kind: 'resume', at: resumeFrom });
    // re-plan: taps after resume point need to be re-done
    const redo = taps.filter(t => t > resumeFrom + 0.01 && t <= p.t).map(t => ({ t, kind: 'tap' })); plan.splice(plan.indexOf(p), 0, ...redo.filter(r => !plan.some(q => Math.abs(q.t - r.t) < 1e-3 && plan.indexOf(q) >= plan.indexOf(p))));
  }
  if (performance.now() - lastSync > 600 && p.t - songNow() > 0.2) { ref = await sync(); lastSync = performance.now(); if (ref.status !== 'playing') break; }
  await busyUntil(p.t);
  touch(); sent.push({ kind: p.kind, planned: p.t }); if (sent.length % 20 === 0) dbg('sent', sent.length, p.t.toFixed(2));
}
dbg('plan done');
// let the song run to the end (or to `to`)
while (true) {
  const s = await page.evaluate(() => ({ st: window.__nj.state, t: window.__nj.game.time, gs: window.__nj.game.status }));
  if (s.gs !== 'playing' || s.t >= to) break;
  await page.waitForTimeout(250);
}
await page.waitForTimeout(+(A.tail ?? 4500));
const result = await page.evaluate(() => { const g = window.__nj.game; return { runlog: window.__runlog.fails, allTurns: window.__runlog.turns, state: window.__nj.state, status: g.status, failKind: g.failKind, failTime: g.failTime, time: g.time, cursor: g.cursor, taps: g.taps.length, perfect: g.perfect, good: g.good, diamonds: g.diamondsTaken.size, ignoredDuplicates: g.ignoredDuplicates,
  errors: (window.__runlog.turns || []).filter(r => r[1] !== r[0]).map(r => Math.round((r[1] - r[0]) * 1000)), fps: window.__nj.world.fps, save: JSON.parse(localStorage.getItem('newjeans-line.save.v2') || 'null') }; });
if (A.shot) await page.screenshot({ path: A.shot });
await Promise.allSettled(pending);
if (ff) { ff.stdin.write('q'); await new Promise(r => ff.on('close', r)); }
const errs = result.errors; const mean = errs.reduce((a, b) => a + b, 0) / Math.max(1, errs.length); const sd = Math.sqrt(errs.reduce((a, b) => a + (b - mean) ** 2, 0) / Math.max(1, errs.length));
const summary = { ...result, errors: undefined, allTurns: undefined, errorMeanMs: Math.round(mean * 10) / 10, errorSdMs: Math.round(sd * 10) / 10, errorMaxAbsMs: Math.max(0, ...errs.map(Math.abs)), sent: sent.length, logs };
console.log(JSON.stringify(summary, null, 1));
if (A.log) writeFileSync(A.log, JSON.stringify({ summary, errors: errs, sent }, null, 1));
await browser.close();
