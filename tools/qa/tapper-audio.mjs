// Scripted audio-unlock test for the tapper page (scripted simulation; real browser autoplay policy, gestures from Playwright).
// Checks: locked notice before any gesture, a tap/click on ▶ unlocks the AudioContext and the song graph produces signal,
// slow (0.75x, keep pitch) playback runs on the <audio> element, review clicks + metronome produce signal, a simulated
// interruption (ctx.suspend) shows the notice again and the next tap restores sound. Uses either Chromium or WebKit.
// usage: node tools/qa/tapper-audio.mjs [URL] [chromium|webkit] [outjson]  (on the Mac: PW_MODULE=playwright-core)
const mod = await import(process.env.PW_MODULE ?? '@playwright/test');
const URL_ = process.argv[2] ?? 'http://127.0.0.1:4390/tapper/';
const which = process.argv[3] ?? 'chromium'; const OUTJ = process.argv[4];
const bt = mod[which];
const opts = which === 'chromium' && process.env.CHROME ? { executablePath: process.env.CHROME } : {};
const b = await bt.launch({ headless: true, ...opts });
const touch = which === 'webkit' && process.env.MOBILE === '1';
const ctx = await b.newContext(touch ? { viewport: { width: 390, height: 664 }, isMobile: true, hasTouch: true, deviceScaleFactor: 3,
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' } : { viewport: { width: 1280, height: 800 } });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
const R = { browser: which + (touch ? ' (iPhone UA, touch)' : ''), version: b.version(), steps: [] };
const ok = (name, cond, extra = {}) => { R.steps.push({ name, pass: !!cond, ...extra }); console.log(cond ? 'PASS' : 'FAIL', name, JSON.stringify(extra)); };
const tap = async sel => { if (touch) await p.tap(sel); else await p.click(sel); };
await p.goto(URL_ + '?song=omg'); await p.evaluate(() => localStorage.clear()); await p.reload();
await p.waitForFunction(() => window.__tapper?.S.pk && window.__tapper.player.duration > 100, null, { timeout: 60000 });
const st0 = await p.evaluate(() => ({ state: window.__tapper.player.state, pill: !document.getElementById('unlock').hidden, session: navigator.audioSession ? navigator.audioSession.type : 'unsupported' }));
ok('before any gesture: audio locked and the notice is shown', st0.state !== 'running' && st0.pill, st0);
// RMS probe on the song gain and the click gain
const probe = () => p.evaluate(() => new Promise(res => {
  const P = window.__tapper.player; const c = P.ctx; const mk = node => { const a = c.createAnalyser(); a.fftSize = 2048; node.connect(a); return a; };
  const A = window.__probe ??= { song: mk(P.gain), click: mk(P.clickGain) };
  let ms = 0, mc = 0; const buf = new Float32Array(2048); let n = 0;
  const step = () => { A.song.getFloatTimeDomainData(buf); ms = Math.max(ms, Math.sqrt(buf.reduce((s, v) => s + v * v, 0) / buf.length));
    A.click.getFloatTimeDomainData(buf); mc = Math.max(mc, Math.max(...buf.map(Math.abs))); if (++n < 25) setTimeout(step, 40); else res({ song: +ms.toFixed(4), click: +mc.toFixed(4) }); };
  step();
}));
const tp0 = Date.now(); await tap('#play'); await p.waitForFunction(() => window.__tapper.player.playing, null, { timeout: 5000 }).catch(() => {}); const startMs = Date.now() - tp0; await p.waitForTimeout(900);
const s1 = await p.evaluate(() => ({ state: window.__tapper.player.state, playing: window.__tapper.player.playing, pos: window.__tapper.player.position, pill: !document.getElementById('unlock').hidden, session: navigator.audioSession ? navigator.audioSession.type : 'unsupported' }));
const r1 = await probe();
ok('tap ▶ unlocks: context running, song plays and the graph carries signal', s1.state === 'running' && s1.playing && s1.pos > 0.5 && !s1.pill && r1.song > 0.005, { ...s1, firstStartMs: startMs, rms: r1 });
await tap('#play');
// slow playback with pitch kept: plays the <audio> element directly
await p.selectOption('#rate', '0.75'); await tap('#play'); await p.waitForTimeout(2500);
const e0 = await p.evaluate(() => [window.__tapper.player.el.currentTime, performance.now()]); await p.waitForTimeout(3000);
const s2 = await p.evaluate(e0 => { const P = window.__tapper.player; const el = P.el; return { fixes: P.rateProbe?.fixes, speed: +((el.currentTime - e0[0]) / ((performance.now() - e0[1]) / 1000)).toFixed(3), mediaPath: P.mediaPath, paused: el.paused, muted: el.muted, t: el.currentTime, rate: el.playbackRate, pos: P.position, readyState: el.readyState, src: el.src.slice(0, 60) }; }, e0);
ok('0.75x keep-pitch playback runs on the <audio> element (not muted, advancing at 0.75x)', s2.mediaPath && !s2.paused && !s2.muted && s2.t > 0.3 && Math.abs(s2.rate - 0.75) < 1e-6 && Math.abs(s2.speed - 0.75) < 0.08, s2);
await tap('#play'); await p.selectOption('#rate', '1');
// review clicks over the music
await p.evaluate(() => { const T = window.__tapper; T.S.taps = [3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75].map((t, i) => ({ id: 900 + i, t, t_raw: t, type: i % 2 ? 'vocal' : 'drum' })); T.player.seek(2.8); });
await tap('#morebtn'); await p.check('#clicks'); await tap('#sheet [data-close]');
await tap('#play'); const r3 = await probe(); await tap('#play');
ok('review click sounds produce signal', r3.click > 0.05, { rms: r3 });
// metronome during calibration
await tap('#calib'); await tap('#calstart'); await p.waitForTimeout(800); const r4 = await probe();
await p.evaluate(() => { window.__tapper.calib.active = false; document.getElementById('calibdlg').close(); });
ok('calibration metronome produces signal', r4.click > 0.05, { rms: r4 });
// simulated interruption (iOS 'interrupted' / suspended after a call or lock screen): notice back, next tap restores
await p.evaluate(() => window.__tapper.player.ctx.suspend()); await p.waitForTimeout(300);
const s5 = await p.evaluate(() => ({ state: window.__tapper.player.state, pill: !document.getElementById('unlock').hidden }));
await tap('#pad'); await p.waitForTimeout(400);
const s6 = await p.evaluate(() => ({ state: window.__tapper.player.state, pill: !document.getElementById('unlock').hidden }));
ok('after an interruption the notice shows and one tap restores audio', s5.state !== 'running' && s5.pill && s6.state === 'running' && !s6.pill, { before: s5, after: s6 });
ok('no page errors', errs.length === 0, { errs });
R.pass = R.steps.every(s => s.pass); console.log(R.pass ? 'ALL PASS' : 'SOME FAILED', which, R.version);
if (OUTJ) (await import('node:fs')).writeFileSync(OUTJ, JSON.stringify(R, null, 1));
await b.close(); process.exit(R.pass ? 0 : 1);
