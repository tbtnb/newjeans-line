/** Production WebKit smoke: mobile emulation on macOS, not a physical iPhone. */
import { webkit, devices, expect } from '@playwright/test';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';

const base = process.env.PLAYWRIGHT_BASE_URL || 'http://127.0.0.1:4175/';
const levels = JSON.parse(readFileSync('src/levels.json', 'utf8'));
const song = levels.find(level => level.title === 'Get Up');
const report = { at: new Date().toISOString(), base, scope: 'Playwright WebKit on macOS with iPhone 13 emulation; not a physical iPhone', checks: [], errors: [] };
mkdirSync('reports/screenshots', { recursive: true });
const browser = await webkit.launch({ headless: true });
const context = await browser.newContext({ ...devices['iPhone 13'] });
const page = await context.newPage();
page.setDefaultTimeout(15000);
page.on('pageerror', error => report.errors.push(error.message));
page.on('console', message => { if (message.type() === 'error') report.errors.push(message.text()); });
page.on('response', response => { if (response.status() === 404) report.errors.push(`404 ${response.url()}`); });
await page.addInitScript(() => {
  const observed = { draws: 0, touches: 0, starts: [], stops: 0 };
  window.__webkitAudit = observed;
  for (const context of [WebGLRenderingContext, WebGL2RenderingContext]) {
    for (const name of ['drawElements', 'drawArrays', 'drawElementsInstanced', 'drawArraysInstanced']) {
      const draw = context.prototype[name]; if (!draw) continue;
      context.prototype[name] = function (...args) { observed.draws++; return draw.apply(this, args); };
    }
  }
  document.addEventListener('pointerdown', event => { if (event.target.matches?.('[data-testid="game-canvas"]') && event.pointerType === 'touch') observed.touches++; });
  const start = AudioBufferSourceNode.prototype.start, stop = AudioBufferSourceNode.prototype.stop;
  AudioBufferSourceNode.prototype.start = function (...args) {
    start.apply(this, args);
    observed.context = this.context;
    observed.started = this.context.currentTime - (args[1] || 0);
    observed.starts.push({ duration: this.buffer.duration, rate: this.playbackRate.value, wall: performance.now(), offset: args[1] || 0 });
  };
  AudioBufferSourceNode.prototype.stop = function (...args) { observed.stops++; return stop.apply(this, args); };
});
async function select(title) {
  await page.getByRole('button', { name: '曲库', exact: true }).click();
  await page.getByTestId('song-search').fill(title);
  await page.getByTestId('song-row').filter({ has: page.locator('strong', { hasText: new RegExp(`^${title}$`) }) }).click();
  await expect(page.getByTestId('song-title')).toHaveText(title);
}
async function checkLayout(width, height) {
  await page.setViewportSize({ width, height });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  await expect(page.getByTestId('start-button')).toBeInViewport();
  await expect(page.getByTestId('settings-button')).toBeInViewport();
}
try {
  await page.goto(base);
  await page.waitForFunction(() => window.__webkitAudit.draws > 10);
  report.checks.push('Native WebKit WebGL landscape draws');
  await page.getByRole('button', { name: '曲库', exact: true }).click();
  await expect(page.getByTestId('song-row')).toHaveCount(16);
  await page.getByRole('button', { name: '关闭', exact: true }).click();
  for (const [width, height] of [[390, 844], [375, 667], [844, 390]]) await checkLayout(width, height);
  await page.setViewportSize({ width: 390, height: 844 });
  report.checks.push('16-song library and three mobile viewport layouts');
  await select('Get Up');
  await page.locator('.practice-switch').click();
  const before = Date.now();
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud')).toBeVisible();
  await expect.poll(async () => parseInt(await page.getByTestId('hud-percent').innerText())).toBeGreaterThan(5);
  await page.getByTestId('pause-button').click();
  const paused = await page.getByTestId('hud-percent').innerText();
  await page.waitForTimeout(700);
  await expect(page.getByTestId('hud-percent')).toHaveText(paused);
  expect(await page.evaluate(() => window.__webkitAudit.stops)).toBeGreaterThan(0);
  await page.getByTestId('resume-button').click();
  await expect(page.getByTestId('result-percent')).toHaveText('100%', { timeout: 45000 });
  await expect(page.locator('#dialog-title')).toHaveText('练习，也是旅程');
  const audio = await page.evaluate(() => ({ starts: window.__webkitAudit.starts, elapsed: (performance.now() - window.__webkitAudit.starts[0].wall) / 1000 }));
  expect(audio.starts).toHaveLength(2);
  expect(audio.starts.every(start => start.rate === 1)).toBe(true);
  expect(Math.abs(audio.starts[0].duration - song.duration)).toBeLessThan(.2);
  expect(audio.elapsed).toBeGreaterThan(song.duration - .5);
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('newjeans-line.save.v1')).records)).toEqual({});
  await page.screenshot({ path: 'reports/screenshots/webkit-practice-complete.png' });
  report.practice = { wallSeconds: (Date.now() - before) / 1000, audio };
  report.checks.push('Full real MP3 at 1x, pause/resume and practice completion without normal records');
  await page.locator('[data-action="home"]').click();
  await page.locator('.practice-switch').click();
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud')).toBeVisible();
  const box = await page.getByTestId('game-canvas').boundingBox();
  for (const at of song.turns.slice(0, 2)) {
    await page.waitForFunction(at => window.__webkitAudit.context.currentTime - window.__webkitAudit.started >= at - .045, at, { polling: 'raf' });
    await page.touchscreen.tap(box.x + box.width / 2, box.y + box.height / 2);
    await expect(page.locator('#dialog')).not.toBeVisible();
  }
  await expect(page.locator('#hud-combo')).toHaveText('2 连续转弯');
  expect(await page.evaluate(() => window.__webkitAudit.touches)).toBe(2);
  await page.screenshot({ path: 'reports/screenshots/webkit-touch-turns.png' });
  await expect(page.getByTestId('result-percent')).toBeVisible({ timeout: 15000 });
  await expect(page.locator('#dialog-title')).toHaveText('再听一次，再近一点');
  await page.locator('[data-action="home"]').click();
  await page.reload();
  await expect(page.getByTestId('song-title')).toHaveText('Get Up');
  const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('newjeans-line.save.v1')));
  expect(saved.records[song.id].attempts).toBe(1);
  expect(saved.records[song.id].best).toBeGreaterThan(0);
  report.checks.push('Two native touch turns, no-input failure and refresh-persistent normal record');
  await select('Supernatural');
  await expect(page.locator('body')).toHaveAttribute('data-dark', 'true');
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'reports/screenshots/webkit-supernatural-menu.png' });
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud')).toBeVisible();
  await expect(page.locator('#hud-percent')).toHaveCSS('color', 'rgb(255, 246, 232)');
  await page.getByTestId('pause-button').click();
  await expect(page.getByTestId('resume-button')).toBeVisible();
  report.checks.push('Night-level real audio, readable HUD and pause control');
  expect(report.errors).toEqual([]);
  report.passed = true;
} catch (error) {
  report.passed = false;
  report.failure = error.stack || String(error);
  await page.screenshot({ path: 'reports/screenshots/webkit-failure.png' }).catch(() => {});
  throw error;
} finally {
  await browser.close();
  writeFileSync('reports/webkit-production.json', JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
}
