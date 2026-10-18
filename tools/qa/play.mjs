// Scripted player + optional real-audio screen recording (Xvfb + PulseAudio null sink + ffmpeg).
// THIS IS A SCRIPTED SIMULATION (CDP Input.dispatchTouchEvent), NOT physical-device play, and NOT proof of music sync.
// usage: DISPLAY=:99 node tools/qa/play.mjs --url URL --level 5 --w 540 --h 960 [--from 0] [--to 999] [--record out.mp4]
//        [--jitter 0.008] [--miss T] [--double T] [--extra T] [--pauseAt T] [--log out.json] [--verbose]
import { mkdirSync } from 'node:fs';
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const A = Object.fromEntries(process.argv.slice(2).reduce((acc, v, i, arr) => (v.startsWith('--') ? [...acc, [v.slice(2), arr[i + 1] === undefined || arr[i + 1].startsWith('--') ? '1' : arr[i + 1]]] : acc), []));
const dbg = (...a) => { if (A.verbose) console.error('[play]', ...a); };
const W = +(A.w ?? 540), H = +(A.h ?? 960), level = +(A.level ?? 5);
const DISPLAY = process.env.DISPLAY ?? ':99';
const browser = await chromium.launch({ headless: !A.record && !A.headed, executablePath: '/usr/bin/google-chrome', env: { ...process.env, DISPLAY },
  args: ['--autoplay-policy=no-user-gesture-required', '--window-position=0,0', `--window-size=${W},${H + 140}`, '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', '--disable-infobars', '--disable-features=Translate,TranslateUI', '--lang=zh-CN'] });
const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, hasTouch: true });
const page = await ctx.newPage();
const logs = []; page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') logs.push(m.type() + ': ' + m.text()); }); page.on('pageerror', e => logs.push('PAGEERROR ' + e.message));
await page.goto(A.url ?? 'http://127.0.0.1:4180/?debug');
await page.waitForFunction(() => window.__nj);
await page.evaluate(i => window.__nj.selectLevel(i), level);
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 60000 });
// optional render-cost knobs for smoother software-rendered captures: --quality low (no shadows), --scale 1.5 (render at 1/1.5 res, upscaled)
if (A.quality || A.scale || A.camScale) await page.evaluate(([q, sc, cs]) => { const w = window.__nj.world; if (q) w.setQuality(q); if (sc) w.engine.setHardwareScalingLevel(+sc); if (cs) w.__camScale = +cs; }, [A.quality, A.scale, A.camScale]);
await page.waitForTimeout(1500);
const cdp = await ctx.newCDPSession(page);
// Fire-and-forget: the browser stamps the event when it receives it (measured 0.4-4 ms after send);
// awaiting the reply would serialize taps behind slow software-rendered frames (50-120 ms).
const pending = [];
const touch = (x = W / 2, y = H * 0.6) => {
  pending.push(cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y, id: 1 }] }));
  pending.push(cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }));
};
let ff = null;
if (A.record) {
  const geo = await page.evaluate(() => ({ x: window.screenX, y: window.screenY + (window.outerHeight - window.innerHeight), ow: window.outerWidth, iw: window.innerWidth }));
  const ox = Math.max(0, geo.x + Math.round((geo.ow - geo.iw) / 2)), oy = Math.max(0, geo.y);
  ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-thread_queue_size', '1024', '-f', 'x11grab', '-draw_mouse', '0', '-framerate', '30', '-video_size', `${W}x${H}`, '-i', `${DISPLAY}+${ox},${oy}`,
    '-thread_queue_size', '1024', ...(A.frag ? ['-fragment_size', A.frag] : []), ...(A.pulsewc ? ['-wallclock', A.pulsewc] : []), '-f', 'pulse', '-i', A.pulse ?? 'rec.monitor', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', A.record], { stdio: ['pipe', 'inherit', 'inherit'] });
  await page.waitForTimeout(800);
}
await page.waitForTimeout(+(A.menuHold ?? 1200));
const from = +(A.from ?? 0);
if (from > 0) await page.evaluate(t => window.__nj.preview(t), from);
else await page.mouse.click(W / 2, H * 0.55);
await page.waitForFunction(() => window.__nj.state === 'ready', null, { timeout: 60000 });
await page.waitForTimeout(900);
const taps = await page.evaluate(() => window.__nj.game.taps);
const to = Math.min(+(A.to ?? 1e9), await page.evaluate(() => window.__nj.level.duration));
await page.evaluate(() => { window.__runlog = { fails: [], turns: null }; setInterval(() => { const g = window.__nj.game; if (!g) return; if (g.status === 'failed' && !window.__runlog.fails.some(f => f.t === g.failTime)) window.__runlog.fails.push({ t: g.failTime, kind: g.failKind, cursor: g.cursor, next: g.taps[g.cursor] }); if (g.turns.length) window.__runlog.turns = g.turns.map(r => [r.chartT, r.tapT]); }, 20); });
dbg('start tap'); touch();
// Same machine => both processes share the wall clock; map via timeOrigin (no round-trip bias).
const sync = async () => { const r = await page.evaluate(() => ({ s: window.__nj.audio.songTime(), e: performance.timeOrigin + performance.now(), st: window.__nj.game.status })); return { song: r.s, node: r.e - performance.timeOrigin, status: r.st }; };
await page.waitForFunction(() => window.__nj.audio.playing && window.__nj.audio.songTime() > 0.15, null, { timeout: 10000, polling: 5 });
let ref = await sync(); dbg('synced', ref);
const songNow = () => ref.song + (performance.now() - ref.node) / 1000;
const jitter = +(A.jitter ?? 0);
const gauss = () => { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
const missAt = A.miss ? +A.miss : null, dblAt = A.double ? +A.double : null, extraAt = A.extra ? +A.extra : null, pauseAt = A.pauseAt ? +A.pauseAt : null;
const plan = [];
for (const t of taps) { if (t <= from + 0.01 || t > to) continue; if (missAt !== null && Math.abs(t - missAt) < 0.12) continue; plan.push({ t: t + jitter * gauss(), kind: 'tap' }); if (dblAt !== null && Math.abs(t - dblAt) < 0.12) plan.push({ t: t + 0.012, kind: 'double' }); }
if (extraAt !== null) plan.push({ t: extraAt, kind: 'extra' });
// --shots 20,45,90 --shotdir dir : screenshots taken during real (scripted) play, so they show the trail, live scenery
// and the real HUD (unlike snap.mjs, whose static debug preview shows the ready prompt and no trail)
const shotTimes = A.shots ? A.shots.split(',').map(Number) : [];
if (shotTimes.length) { mkdirSync(A.shotdir ?? 'shots', { recursive: true }); for (const t of shotTimes) plan.push({ t, kind: 'shot' }); }
const shotJobs = [];
plan.sort((a, b) => a.t - b.t);
const sent = []; let lastSync = performance.now(); let paused = false;
const busyUntil = async target => { for (;;) { const dt = (target - songNow()) * 1000; if (dt < 8) break; await new Promise(r => setTimeout(r, Math.min(dt - 6, 50))); } while (songNow() < target) { /* spin */ } };
for (let i = 0; i < plan.length; i++) {
  const p = plan[i];
  if (pauseAt !== null && !paused && p.t > pauseAt) {
    paused = true; await busyUntil(pauseAt);
    await page.click('#btn-pause'); await page.waitForTimeout(1200);
    await page.click('#btn-resume'); await page.waitForTimeout(800);
    touch(); await page.waitForFunction(() => window.__nj.audio.playing && window.__nj.state === 'playing'); ref = await sync();
    const resumeFrom = await page.evaluate(() => window.__nj.game.startTime); sent.push({ kind: 'resume', at: resumeFrom });
    const redo = taps.filter(t => t > resumeFrom + 0.01 && t < p.t - 0.05).map(t => ({ t, kind: 'tap' }));
    plan.splice(i, 0, ...redo); i--; continue;
  }
  if (performance.now() - lastSync > 600 && p.t - songNow() > 0.2) { ref = await sync(); lastSync = performance.now(); if (ref.status !== 'playing') break; }
  await busyUntil(p.t);
  if (p.kind === 'shot') { shotJobs.push(page.screenshot({ path: `${A.shotdir ?? 'shots'}/play-t${String(Math.round(p.t)).padStart(3, '0')}.png` })); continue; }
  touch(); sent.push({ kind: p.kind, planned: p.t }); if (sent.length % 50 === 0) dbg('sent', sent.length, p.t.toFixed(2));
}
await Promise.all(shotJobs); dbg('plan done');
for (;;) { const s = await page.evaluate(() => ({ t: window.__nj.game.time, gs: window.__nj.game.status })); if (s.gs !== 'playing' || s.t >= to) break; await page.waitForTimeout(250); }
await page.waitForTimeout(+(A.tail ?? 4500));
const result = await page.evaluate(() => { const g = window.__nj.game; const rl = window.__runlog || { fails: [], turns: [] }; return { fails: rl.fails, turns: rl.turns || [], state: window.__nj.state, status: g.status, failKind: g.failKind, failTime: g.failTime, time: g.time, cursor: g.cursor, taps: g.taps.length, perfect: g.perfect, good: g.good, diamonds: g.diamondsTaken.size, ignoredDuplicates: g.ignoredDuplicates, fps: window.__nj.world.fps, save: JSON.parse(localStorage.getItem('newjeans-line.save.v2') || 'null') }; });
if (A.shot) await page.screenshot({ path: A.shot });
await Promise.allSettled(pending);
if (ff) { ff.stdin.write('q'); await new Promise(r => ff.on('close', r)); }
const errs = result.turns.map(([c, t]) => Math.round((t - c) * 1000));
const mean = errs.reduce((a, b) => a + b, 0) / Math.max(1, errs.length); const sd = Math.sqrt(errs.reduce((a, b) => a + (b - mean) ** 2, 0) / Math.max(1, errs.length));
const summary = { ...result, turns: undefined, judged: errs.length, errorMeanMs: +mean.toFixed(1), errorSdMs: +sd.toFixed(1), errorMaxAbsMs: Math.max(0, ...errs.map(Math.abs)), sent: sent.length, logs };
console.log(JSON.stringify(summary, null, 1));
if (A.log) writeFileSync(A.log, JSON.stringify({ summary, errors: errs, sent }, null, 1));
await browser.close();
