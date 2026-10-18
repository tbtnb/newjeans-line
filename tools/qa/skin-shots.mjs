// Line-skin screenshots: for each skin, scripted play (SIMULATION via CDP touch) from a preview point in OMG, a shot just
// after a turn (trail + corner + turn burst), then a deliberate miss and a shot of the death shatter.
// Also the skin picker in portrait / landscape / desktop.
// usage: node tools/qa/skin-shots.mjs --url http://127.0.0.1:4195/?debug --out deliverables/skins [--level 4] [--from 18]
import { mkdirSync, writeFileSync } from 'node:fs';
import { chromium } from '@playwright/test';
const A = Object.fromEntries(process.argv.slice(2).reduce((acc, v, i, arr) => (v.startsWith('--') ? [...acc, [v.slice(2), arr[i + 1] === undefined || arr[i + 1].startsWith('--') ? '1' : arr[i + 1]]] : acc), []));
const OUT = A.out ?? 'deliverables/skins'; mkdirSync(OUT, { recursive: true });
const URL = A.url ?? 'http://127.0.0.1:4195/?debug';
const LEVEL = +(A.level ?? 4), FROM = +(A.from ?? 18), SHOT_AFTER = +(A.turnShot ?? 22.45);
const browser = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--autoplay-policy=no-user-gesture-required', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--hide-scrollbars', '--lang=zh-CN'] });
const report = { play: [], picker: [], errors: [] };

async function open(w, h, skin) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, hasTouch: true });
  if (skin) await ctx.addInitScript(id => { try { const k = 'newjeans-line.save.v2'; const s = JSON.parse(localStorage.getItem(k) || 'null') || { version: 2, selected: 'omg', records: {}, settings: { volume: 0.8, offsetMs: 0, quality: 'high', vibration: true } }; s.settings.skin = id; localStorage.setItem(k, JSON.stringify(s)); } catch {} }, skin);
  const page = await ctx.newPage();
  page.on('pageerror', e => report.errors.push(`${skin}: ${e.message}`)); page.on('console', m => { if (m.type() === 'error') report.errors.push(`${skin}: ${m.text()}`); });
  await page.goto(URL); await page.waitForFunction(() => window.__nj);
  return { ctx, page };
}

const skins = await (async () => { const { ctx, page } = await open(400, 400); const ids = await page.evaluate(() => import('/src/skins.ts').then(m => m.SKINS.map(s => s.id)).catch(() => null)); await ctx.close(); return ids; })()
  ?? (A.skins ?? 'classic,bunny,denim,bubble-gum,phoning,film,supernatural').split(',');

const W = +(A.w ?? 540), H = +(A.h ?? 960);
for (const skin of skins) {
  const { ctx, page } = await open(W, H, skin);
  await page.evaluate(i => window.__nj.selectLevel(i), LEVEL);
  await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 60000 });
  const saved = await page.evaluate(() => window.__nj.save.settings.skin);
  await page.waitForTimeout(800);
  await page.evaluate(t => window.__nj.preview(t), FROM);
  await page.waitForFunction(() => window.__nj.state === 'ready');
  await page.waitForTimeout(500);
  const cdp = await ctx.newCDPSession(page);
  const touch = () => { cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: W / 2, y: H * 0.6, id: 1 }] }); cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); };
  const taps = await page.evaluate(() => window.__nj.game.taps);
  touch();
  await page.waitForFunction(() => window.__nj.audio.playing && window.__nj.audio.songTime() > 0.1, null, { polling: 5 }).catch(() => {});
  const sync = async () => { const r = await page.evaluate(() => ({ s: window.__nj.audio.songTime(), e: performance.timeOrigin + performance.now() })); return { song: r.s, node: r.e - performance.timeOrigin }; };
  let ref = await sync(); const now = () => ref.song + (performance.now() - ref.node) / 1000;
  const until = async t => { for (;;) { const d = (t - now()) * 1000; if (d < 6) break; await new Promise(r => setTimeout(r, Math.min(d - 4, 40))); } while (now() < t) {} };
  const plan = taps.filter(t => t > FROM + 0.05 && t <= SHOT_AFTER + 1e-3);
  for (const t of plan) { await until(t); touch(); }
  await until(SHOT_AFTER + 0.16);
  const turnShot = `${OUT}/play-${skin}.png`; await page.screenshot({ path: turnShot });
  // stop tapping: the next corner is missed -> fail -> shatter
  await page.waitForFunction(() => window.__nj.game.status === 'failed', null, { timeout: 5000 }).catch(() => {});
  const failInfo = await page.evaluate(() => ({ status: window.__nj.game.status, kind: window.__nj.game.failKind, t: window.__nj.game.failTime, turns: window.__nj.game.turns.length, perfect: window.__nj.game.perfect, good: window.__nj.game.good }));
  await page.waitForTimeout(430);
  const deathShot = `${OUT}/death-${skin}.png`; await page.screenshot({ path: deathShot });
  const stats = await page.evaluate(() => window.__nj.stats());
  report.play.push({ skin, saved, turnShot, deathShot, plannedTaps: plan.length, ...failInfo, stats });
  console.log(skin, JSON.stringify(report.play.at(-1)));
  await ctx.close();
}

// picker in three viewports
for (const [name, w, h] of [['portrait', 390, 844], ['landscape', 844, 390], ['desktop', 1440, 900]]) {
  const { ctx, page } = await open(w, h, 'bubble-gum');
  await page.waitForFunction(() => window.__nj.level, null, { timeout: 60000 });
  await page.waitForTimeout(600);
  await page.click('#btn-skins'); await page.waitForTimeout(700);
  // pick a skin through the UI, confirm it persisted
  await page.click('.skin-card[data-id="supernatural"]'); await page.waitForTimeout(1600);
  const path = `${OUT}/picker-${name}.png`; await page.screenshot({ path });
  const st = await page.evaluate(() => ({ save: JSON.parse(localStorage.getItem('newjeans-line.save.v2')).settings.skin, world: window.__nj.world.skin.def.id, cards: document.querySelectorAll('.skin-card').length, overflowX: document.querySelector('.skin-grid').scrollWidth > document.querySelector('.skin-grid').clientWidth + 1, gridScrolls: document.querySelector('.skin-grid').scrollHeight > document.querySelector('.skin-grid').clientHeight }));
  report.picker.push({ name, w, h, path, ...st }); console.log(name, JSON.stringify(st));
  await ctx.close();
}
writeFileSync(`${OUT}/report.json`, JSON.stringify(report, null, 1));
console.log('errors', report.errors.length, report.errors.slice(0, 10));
await browser.close();
