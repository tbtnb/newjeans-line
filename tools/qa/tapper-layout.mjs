// Scripted layout / touch test of the tapper page with Playwright device emulation (Chromium; scripted simulation, not a physical device).
// Per device: no document scroll (scrollHeight <= innerHeight, scrollWidth <= innerWidth), essential controls fully on screen and
// not covered, window.scrollY stays 0 and visual viewport unzoomed after 50 rapid taps on the pad and 50 on buttons, no text selection,
// Space with a focused button / checkbox while recording records a tap and does not activate it. Screenshots to deliverables/tapper/.
// usage: node tools/qa/tapper-layout.mjs [URL] [outdir]
import { chromium, devices } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
const URL_ = process.argv[2] ?? 'http://127.0.0.1:4390/tapper/';
const OUT = process.argv[3] ?? 'deliverables/tapper'; mkdirSync(`${OUT}/layout`, { recursive: true });
const strip = d => { const { defaultBrowserType, ...rest } = d; return rest; };
const DEV = [
  ['iphone13-portrait', strip(devices['iPhone 13']), 'phone-portrait'],
  ['iphone13-landscape', strip(devices['iPhone 13 landscape']), 'phone-landscape'],
  ['iphone14-portrait', strip(devices['iPhone 14'])],
  ['iphone14-landscape', strip(devices['iPhone 14 landscape'])],
  ['android-360x640', { viewport: { width: 360, height: 640 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, userAgent: devices['Galaxy S8'].userAgent }, 'small-android'],
  ['android-640x360', { viewport: { width: 640, height: 360 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, userAgent: devices['Galaxy S8'].userAgent }],
  ['ipad-portrait', strip(devices['iPad (gen 7)'])],
  ['ipad-landscape', strip(devices['iPad (gen 7) landscape'])],
  ['desktop-1366x768', { viewport: { width: 1366, height: 768 } }, 'desktop'],
  ['desktop-1920x1080', { viewport: { width: 1920, height: 1080 } }],
];
const ESSENTIAL = ['song', 'calib', 'morebtn', 'helpbtn', 'play', 'tostart', 'tnow', 'info', 'rate', 'mini', 'timeline', 'zoomout', 'zoomin', 'undo', 'redo', 'del', 'boxmode', 'seta', 'setb', 'selab', 'clrab', 'rec', 'recab', 'stop', 'status', 'pad'];
const sample = JSON.parse(readFileSync(`${OUT}/sample-export.json`, 'utf8'));
const b = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--autoplay-policy=no-user-gesture-required'] });
const results = []; let allOk = true;
for (const [name, opts, shot] of DEV) {
  const ctx = await b.newContext({ ...opts }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(URL_ + '?song=omg');
  await p.evaluate(js => { localStorage.clear(); localStorage.setItem('nj-tapper:v1:song:omg', js); }, JSON.stringify({ taps: sample.taps, A: 16.225, B: 17.844 }));
  await p.reload(); await p.waitForFunction(() => window.__tapper?.S.pk && window.__tapper.player.duration > 100, null, { timeout: 30000 });
  await p.evaluate(() => { const T = window.__tapper; T.S.view.t0 = 13; T.S.view.pps = innerWidth < 700 ? 80 : 140; T.draw(); });
  const touch = !!opts.hasTouch;
  const measure = () => p.evaluate(ids => {
    const se = document.scrollingElement; const vv = window.visualViewport;
    const bad = [];
    for (const id of ids) {
      const el = document.getElementById(id); const r = el.getBoundingClientRect();
      if (r.width < 4 || r.height < 4) { bad.push(id + ':empty'); continue; }
      if (r.left < -0.5 || r.top < -0.5 || r.right > innerWidth + 0.5 || r.bottom > innerHeight + 0.5) { bad.push(`${id}:offscreen ${r.left|0},${r.top|0},${r.right|0},${r.bottom|0}`); continue; }
      const probe = el.type === 'checkbox' ? el.parentElement : el; const pr = probe.getBoundingClientRect();
      const hit = document.elementFromPoint(pr.left + pr.width / 2, pr.top + pr.height / 2);
      if (!hit || !(probe === hit || probe.contains(hit) || hit.contains(probe))) bad.push(id + ':covered');
    }
    const sel = getSelection();
    return { iw: innerWidth, ih: innerHeight, sh: se.scrollHeight, sw: se.scrollWidth, scrollY: window.scrollY, scrollTop: se.scrollTop,
      vvScale: vv ? +vv.scale.toFixed(3) : 1, vvTop: vv ? Math.round(vv.offsetTop) : 0, selection: sel ? sel.toString() : '', bad,
      timelineH: Math.round(document.getElementById('timeline').getBoundingClientRect().height), padH: Math.round(document.getElementById('pad').getBoundingClientRect().height) };
  }, ESSENTIAL);
  const m0 = await measure();
  if (shot) await p.screenshot({ path: `${OUT}/${shot}.png` });
  await p.screenshot({ path: `${OUT}/layout/${name}.png` });
  // 50 rapid taps on the pad while recording, then 50 rapid taps on buttons
  const center = async sel => { const r = await p.locator(sel).boundingBox(); return [r.x + r.width / 2, r.y + r.height / 2]; };
  const tapAt = async ([x, y]) => { if (touch) await p.touchscreen.tap(x, y); else await p.mouse.click(x, y); };
  const n0 = await p.evaluate(() => window.__tapper.S.taps.length);
  await tapAt(await center('#rec')); await p.waitForFunction(() => window.__tapper.S.rec && window.__tapper.player.playing, null, { timeout: 8000 });
  const pc = await center('#pad'); let maxScroll = 0;
  for (let i = 0; i < 50; i++) { await tapAt([pc[0] + ((i % 5) - 2) * 15, pc[1] + ((i % 3) - 1) * 10]); if (i % 10 === 9) maxScroll = Math.max(maxScroll, await p.evaluate(() => window.scrollY + document.scrollingElement.scrollTop)); }
  // Space while a button / checkbox has focus during recording: must record, must not click / toggle
  const pps0 = await p.evaluate(() => window.__tapper.S.view.pps);
  await p.focus('#zoomin'); for (let i = 0; i < 3; i++) { await p.keyboard.press('Space'); await p.waitForTimeout(60); }
  await p.focus('#boxmode'); await p.keyboard.press('Space'); await p.waitForTimeout(60);
  const spaceState = await p.evaluate(() => ({ pps: window.__tapper.S.view.pps, box: document.getElementById('boxmode').checked, rec: !!window.__tapper.S.rec }));
  await p.keyboard.press('Escape'); await p.waitForTimeout(150);
  const n1 = await p.evaluate(() => window.__tapper.S.taps.length);
  const zi = await center('#zoomin'), zo = await center('#zoomout'), un = await center('#undo'), re = await center('#redo');
  for (let i = 0; i < 50; i++) { await tapAt([zi, zo, un, re][i % 4]); if (i % 10 === 9) maxScroll = Math.max(maxScroll, await p.evaluate(() => window.scrollY + document.scrollingElement.scrollTop)); }
  // try to scroll the page by wheel / touch-drag on the header (must stay put)
  await p.mouse.move(m0.iw / 2, 20); await p.mouse.wheel(0, 600); await p.waitForTimeout(100);
  const m1 = await measure();
  // settings sheet: opens, fits, scrolls only inside itself
  await tapAt(await center('#morebtn')); await p.waitForTimeout(150);
  const sheet = await p.evaluate(() => { const d = document.getElementById('sheet'); const r = d.getBoundingClientRect(); const body = d.querySelector('.sheetbody'); body.scrollTop = 9999;
    return { open: d.open, top: Math.round(r.top), bottom: Math.round(r.bottom), fits: r.top >= -0.5 && r.bottom <= innerHeight + 0.5, inner: body.scrollHeight > body.clientHeight, pageY: window.scrollY }; });
  if (name === 'iphone13-portrait') await p.screenshot({ path: `${OUT}/phone-settings-sheet.png` });
  await p.evaluate(() => document.getElementById('sheet').close());
  const res = { name, viewport: `${m0.iw}x${m0.ih}`, touch,
    noDocScroll: m0.sh <= m0.ih && m0.sw <= m0.iw && m1.sh <= m1.ih && m1.sw <= m1.iw, scrollHeight: m0.sh, scrollWidth: m0.sw,
    scrollYAfterTaps: Math.max(maxScroll, m1.scrollY, m1.scrollTop), vvScale: m1.vvScale, vvTop: m1.vvTop,
    selectionEmpty: m1.selection === '', essentialVisible: m0.bad.length === 0 && m1.bad.length === 0, bad: [...new Set([...m0.bad, ...m1.bad])],
    timelineH: m0.timelineH, padH: m0.padH, padTapsRecorded: n1 - n0, spaceDuringRec: spaceState,
    spaceOk: spaceState.pps === pps0 && spaceState.box === false && spaceState.rec, sheet, errs };
  res.pass = res.noDocScroll && res.scrollYAfterTaps === 0 && res.vvScale === 1 && res.vvTop === 0 && res.selectionEmpty && res.essentialVisible &&
    res.padTapsRecorded === 54 && res.spaceOk && sheet.open && sheet.fits && sheet.pageY === 0 && res.timelineH >= 70 && res.padH >= 90 && errs.length === 0;
  allOk &&= res.pass; results.push(res);
  console.log(res.pass ? 'PASS' : 'FAIL', name, JSON.stringify({ vp: res.viewport, sh: res.scrollHeight, y: res.scrollYAfterTaps, sel: res.selectionEmpty, bad: res.bad, tl: res.timelineH, pad: res.padH, taps: res.padTapsRecorded, space: res.spaceOk, sheet: sheet.fits }));
  await ctx.close();
}
writeFileSync(`${OUT}/layout-result.json`, JSON.stringify({ label: 'scripted simulation (Playwright device emulation in Chromium), not physical devices', pass: allOk, results }, null, 1));
console.log(allOk ? 'ALL PASS' : 'SOME FAILED'); await b.close(); process.exit(allOk ? 0 : 1);
