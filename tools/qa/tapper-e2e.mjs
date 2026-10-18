// Scripted (synthetic) end-to-end test of the tapper page. NOT human input: key presses are dispatched by Playwright
// at computed times, with a simulated 40 ms player lateness + Gaussian jitter.
// usage: node tools/qa/tapper-e2e.mjs [URL] [outdir]
import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
const URL_ = process.argv[2] ?? 'http://127.0.0.1:4390/tapper/';
const OUT = process.argv[3] ?? 'deliverables/tapper'; mkdirSync(OUT, { recursive: true });
const LATE = 0.040, JIT = 0.012;
const gauss = () => { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
const nowEpoch = () => performance.timeOrigin + performance.now();
const sleepUntil = async ep => { for (;;) { const d = ep - nowEpoch(); if (d <= 1.5) break; await new Promise(r => setTimeout(r, Math.min(d - 1, 20))); } while (nowEpoch() < ep) { /* spin */ } };
const R = { steps: [] }; const ok = (name, cond, extra = {}) => { R.steps.push({ name, pass: !!cond, ...extra }); console.log(cond ? 'PASS' : 'FAIL', name, JSON.stringify(extra)); };

const b = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--autoplay-policy=no-user-gesture-required'] });
const ctx = await b.newContext({ viewport: { width: 1366, height: 860 }, acceptDownloads: true, permissions: ['clipboard-read', 'clipboard-write'] });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.goto(URL_ + '?song=omg'); await p.evaluate(() => localStorage.clear()); await p.reload();
await p.waitForFunction(() => window.__tapper?.S.pk && window.__tapper.S.song?.id === 'omg', null, { timeout: 30000 });
const nSongs = await p.locator('#song option').count(); const info = await p.textContent('#info');
ok('song list has the 16 game songs and OMG grid', nSongs === 16 && /127\.003 BPM/.test(info), { nSongs, info });

// ---- calibration: press Space 40 ms (+jitter) after each metronome click
await p.click('#calib'); await p.click('#calstart'); await p.waitForFunction(() => window.__tapper.calib.active);
const cal = await p.evaluate(() => { const T = window.__tapper; const now = performance.now(); return { clicks: T.calib.clicks, ctxNow: T.player.heardCtxAt(now), epoch: performance.timeOrigin + now }; });
// re-read the page's own heard-clock mapping before each press (headless fake audio output can re-anchor its clock)
const ctxMap = () => p.evaluate(() => { const T = window.__tapper; const now = performance.now(); return { ctxNow: T.player.heardCtxAt(now), epoch: performance.timeOrigin + now }; });
for (const c of cal.clicks) { const at = c + LATE + JIT * gauss(); const mm = await ctxMap(); await sleepUntil(mm.epoch + (at - mm.ctxNow) * 1000); await p.keyboard.press('Space'); }
await p.waitForFunction(() => !window.__tapper.calib.active, null, { timeout: 8000 });
const calRes = await p.evaluate(() => window.__tapper.calib.result);
await p.click('#calsave');
ok('calibration ≈ simulated 40 ms lateness', calRes !== null && Math.abs(calRes - 40) <= 12, { calibration_ms: calRes });

// ---- record OMG 10–22 s against the shipped chart (ground truth) with the same lateness + jitter
const truth = JSON.parse(readFileSync('levels-src/omg/chart.json', 'utf8')).taps.map(t => t.t).filter(t => t > 10.5 && t < 22);
await p.evaluate(() => window.__tapper.player.seek(10)); await p.click('#rec'); await p.waitForFunction(() => window.__tapper.S.rec && window.__tapper.player.playing); await p.waitForTimeout(300);
const m = await p.evaluate(() => { const T = window.__tapper; const now = performance.now(); return { song: T.player.songAtPerf(now), epoch: performance.timeOrigin + now }; });
const pressed = [];
const songMap = () => p.evaluate(() => { const T = window.__tapper; const now = performance.now(); return { song: T.player.songAtPerf(now), epoch: performance.timeOrigin + now }; });
for (const t of truth) { const at = t + LATE + JIT * gauss(); const mm = await songMap(); await sleepUntil(mm.epoch + (at - mm.song) * 1000); await p.keyboard.press('Space'); pressed.push(at); }
await p.waitForTimeout(300); await p.keyboard.press('Escape');
const rec = await p.evaluate(() => window.__tapper.S.taps.map(t => ({ ...t })));
const errsMs = rec.map((r, i) => (r.t - truth[i]) * 1000);
const mean = errsMs.reduce((a, b) => a + b, 0) / errsMs.length, sd = Math.sqrt(errsMs.reduce((a, b) => a + (b - mean) ** 2, 0) / errsMs.length);
ok('recorded every synthetic tap; calibrated times centred on the truth', rec.length === truth.length && Math.abs(mean) < 15, { taps: rec.length, expected: truth.length, meanErrMs: +mean.toFixed(1), sdMs: +sd.toFixed(1) });

// ---- edit: zoom to the recorded span, add, move, delete, box delete, undo/redo
await p.evaluate(() => { const T = window.__tapper; T.S.view.t0 = 10; T.S.view.pps = 110; T.draw(); });
const box = await p.locator('#timeline').boundingBox();
const xOf = t => p.evaluate(t => window.__tapper.t2x(t), t);
const count = () => p.evaluate(() => window.__tapper.S.taps.length);
const n0 = await count();
const emptyT = 10.25; await p.mouse.click(box.x + await xOf(emptyT), box.y + box.height * 0.6);
ok('click on empty timeline adds a tap', (await count()) === n0 + 1);
const tgt = rec[3]; const tx = box.x + await xOf(tgt.t);
await p.mouse.move(tx, box.y + box.height * 0.5); await p.mouse.down(); await p.mouse.move(tx + 22, box.y + box.height * 0.5, { steps: 5 }); await p.mouse.up();
const moved = await p.evaluate(id => window.__tapper.S.taps.find(t => t.id === id), tgt.id);
ok('drag moves the selected tap', moved && Math.abs(moved.t - (tgt.t + 22 / 110)) < 0.02, { from: tgt.t, to: moved?.t });
await p.keyboard.press('Delete');
ok('Delete removes the selected tap', (await count()) === n0);
const a = box.x + await xOf(14), z = box.x + await xOf(16);
await p.keyboard.down('Shift'); await p.mouse.move(a, box.y + box.height * 0.5); await p.mouse.down(); await p.mouse.move(z, box.y + box.height * 0.5, { steps: 6 }); await p.mouse.up(); await p.keyboard.up('Shift');
const selN = await p.evaluate(() => window.__tapper.S.sel.size); await p.keyboard.press('Delete'); const n1 = await count();
ok('range select (Shift+drag) + Delete removes the range', selN > 0 && n1 === n0 - selN, { selected: selN });
await p.keyboard.press('Control+z'); const nu = await count(); await p.keyboard.press('Control+Shift+z'); const nr = await count();
ok('undo / redo', nu === n0 && nr === n1, { afterUndo: nu, afterRedo: nr });
await p.keyboard.press('Control+z');

// ---- snap preview + review click toggle (visual), A–B from selection
await p.click('#morebtn'); await p.selectOption('#snap', '2'); await p.check('#clicks'); await p.click('#sheet [data-close]');
await p.evaluate(() => { const T = window.__tapper; T.S.sel = new Set(T.S.taps.filter(t => t.t > 16 && t.t < 18).map(t => t.id)); T.draw(); }); await p.click('#selab');
const ab = await p.evaluate(() => [window.__tapper.S.A, window.__tapper.S.B]);
ok('A–B from selection', ab[0] > 15.5 && ab[1] < 18.5, { A: ab[0], B: ab[1] });
await p.evaluate(() => { const T = window.__tapper; T.S.view.t0 = 13; T.S.view.pps = 140; T.draw(); });
await p.screenshot({ path: `${OUT}/desktop.png` });

// ---- export (download + clipboard)
await p.click('#morebtn'); const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#export')]);
const path = `${OUT}/sample-export.json`; await dl.saveAs(path); const ex = JSON.parse(readFileSync(path, 'utf8'));
await p.click('#copy'); await p.waitForTimeout(300); await p.click('#sheet [data-close]'); const clip = await p.evaluate(() => navigator.clipboard.readText());
ok('export JSON (download + clipboard)', ex.song === 'omg' && ex.taps.length === n0 && ex.calibration_ms === calRes && ex.bpm > 126.9 && JSON.parse(clip).taps.length === n0 && 't_raw' in ex.taps[0],
  { file: path, taps: ex.taps.length, keys: Object.keys(ex) });
// autosave survives reload
await p.reload(); await p.waitForFunction(() => window.__tapper?.S.pk, null, { timeout: 30000 }); await p.waitForTimeout(300);
ok('autosave per song (survives reload)', (await count()) === n0, { taps: await count() });
ok('no page errors', errs.length === 0, { errs });

// phone / tablet layout screenshots + no-scroll checks: tools/qa/tapper-layout.mjs
R.summary = { pass: R.steps.filter(s => s.pass).length, total: R.steps.length };
writeFileSync(`${OUT}/e2e-result.json`, JSON.stringify(R, null, 1)); console.log(JSON.stringify(R.summary));
await b.close();
