// Screenshot a level at given song times via the ?debug preview hook (static frames; NOT proof of motion).
// CAUTION: preview frames show the ready prompt ('轻点开始') and NO trail, because the level is paused at a restart point.
// For frames that look like real play use: node tools/qa/play.mjs --level N --shots 20,45,90 --shotdir DIR (scripted play).
// usage: node tools/qa/snap.mjs --url URL --level 5 --times 10,40,80 --w 540 --h 960 --out /tmp/shots/ditto
import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';
const A = Object.fromEntries(process.argv.slice(2).reduce((acc, v, i, arr) => (v.startsWith('--') ? [...acc, [v.slice(2), arr[i + 1]]] : acc), []));
const W = +(A.w ?? 540), H = +(A.h ?? 960); mkdirSync(A.out, { recursive: true });
const b = await chromium.launch({ headless: true, executablePath: '/usr/bin/google-chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'] });
const page = await (await b.newContext({ viewport: { width: W, height: H }, hasTouch: true })).newPage();
const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await page.goto(A.url ?? 'http://127.0.0.1:4180/?debug'); await page.waitForFunction(() => window.__nj);
await page.evaluate(i => window.__nj.selectLevel(i), +(A.level ?? 5));
await page.waitForFunction(() => window.__nj.level && window.__nj.audio.ready, null, { timeout: 60000 });
await page.waitForTimeout(800);
if (A.menu) await page.screenshot({ path: `${A.out}/menu.png` });
for (const t of (A.times ?? '10').split(',').map(Number)) {
  await page.evaluate(t => window.__nj.preview(t), t); await page.waitForTimeout(1600);
  await page.screenshot({ path: `${A.out}/t${String(Math.round(t)).padStart(3, '0')}.png` });
}
console.log(JSON.stringify({ stats: await page.evaluate(() => window.__nj.stats?.()), errs }));
await b.close();
