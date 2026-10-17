/** Verify the actual Pages project path, shipped bytes and full real-audio normal gameplay. */
import { chromium, devices, expect } from '@playwright/test';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
const base = process.env.PLAYWRIGHT_BASE_URL || 'https://tbtnb.github.io/newjeans-line/';
const levels = JSON.parse(readFileSync('src/levels.json', 'utf8'));
const song = levels.find(level => level.title === 'Get Up');
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const report = { at: new Date().toISOString(), base, checks: [], assets: [], errors: [] };
const browser = await chromium.launch({ headless: true, ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}), args: ['--enable-webgl'] });
report.browser = browser.version();
mkdirSync('reports/screenshots', { recursive: true });
function observe(page) {
  page.on('pageerror', error => report.errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') report.errors.push(message.text()); });
  page.on('response', response => { if (response.status() >= 400) report.errors.push(`${response.status()} ${response.url()}`); });
  page.setDefaultTimeout(20000);
}
async function select(page, title) {
  await page.getByRole('button', { name: '曲库', exact: true }).click();
  await page.getByTestId('song-search').fill(title);
  await page.getByTestId('song-row').filter({ has: page.locator('strong', { hasText: new RegExp(`^${title}$`) }) }).click();
  await expect(page.getByTestId('song-title')).toHaveText(title);
}
try {
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage(); observe(page);
  await page.addInitScript(({ turns }) => {
    const original = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function (...args) {
      original.apply(this, args);
      const source = this, started = source.context.currentTime;
      const audit = window.__publicAudio = { rate: source.playbackRate.value, duration: source.buffer.duration, wall: performance.now(), errors: [] };
      let next = 0;
      const timer = setInterval(() => {
        const at = source.context.currentTime - started + (args[1] || 0);
        if (next < turns.length && at >= turns[next]) {
          audit.errors.push(at - turns[next]);
          window.dispatchEvent(new KeyboardEvent('keydown', { code: 'Space', key: ' ', bubbles: true }));
          next++;
        }
        if (next === turns.length) clearInterval(timer);
      }, 3);
    };
  }, { turns: song.turns });
  const response = await page.goto(base);
  expect(response.status()).toBe(200);
  await expect(page.getByTestId('song-title')).toHaveText('New Jeans');
  const build = await page.request.get(new URL(`build.json?audit=${Date.now()}`, base).href);
  expect(build.status()).toBe(200); report.build = await build.json();
  const html = await response.text();
  const entry = html.match(/<script[^>]+src="([^"]+)"/)[1];
  const shipped = await page.request.get(new URL(entry, base).href);
  expect(shipped.status()).toBe(200);
  report.entry = { path: entry, sha256: sha256(await shipped.body()) };
  expect(report.entry.sha256).toBe(sha256(readFileSync(`dist/${entry.replace(/^\.\//, '')}`)));
  report.checks.push('Public HTML, build receipt and entry JavaScript bytes match the verified local production build');
  for (const level of levels) {
    const response = await page.request.head(new URL(level.audio, base).href);
    expect(response.status()).toBe(200);
    const bytes = Number(response.headers()['content-length']);
    expect(bytes).toBe(readFileSync(`public/${level.audio.replace(/^\.\//, '')}`).length);
    report.assets.push({ title: level.title, status: response.status(), bytes });
  }
  report.checks.push('All sixteen public MP3s return 200 with the exact shipped file sizes');
  await select(page, 'Get Up');
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud')).toBeVisible();
  await expect(page.getByTestId('result-percent')).toHaveText('100%', { timeout: 50000 });
  await expect(page.locator('#dialog-title')).toHaveText('这一路，为你加冕');
  report.audio = await page.evaluate(() => ({ ...window.__publicAudio, elapsed: (performance.now() - window.__publicAudio.wall) / 1000 }));
  expect(report.audio.rate).toBe(1);
  expect(Math.abs(report.audio.duration - song.duration)).toBeLessThan(.2);
  expect(report.audio.elapsed).toBeGreaterThan(song.duration - .5);
  expect(report.audio.errors).toHaveLength(song.turns.length);
  expect(Math.max(...report.audio.errors.map(Math.abs))).toBeLessThan(.1);
  await page.screenshot({ path: 'reports/screenshots/public-normal-complete.png' });
  await page.locator('[data-action="home"]').click();
  await page.reload();
  await expect(page.locator('#song-best')).toContainText('100% 已完成');
  report.record = await page.evaluate(id => JSON.parse(localStorage.getItem('newjeans-line.save.v1')).records[id], song.id);
  expect(report.record).toMatchObject({ best: 1, diamonds: 10, crowns: 3, attempts: 1, completed: true });
  report.checks.push('Entire public Get Up MP3, all 16 ordinary timed key turns, normal 100% completion and refresh-persistent 3-crown/10-diamond record');
  await context.close();
  const mobile = await browser.newContext({ ...devices['iPhone 13'], defaultBrowserType: undefined });
  const phone = await mobile.newPage(); observe(phone);
  await phone.goto(base);
  await phone.getByRole('button', { name: '曲库', exact: true }).click();
  await expect(phone.getByTestId('song-row')).toHaveCount(16);
  for (const row of await phone.getByTestId('song-row').all()) {
    await row.scrollIntoViewIfNeeded();
    await expect.poll(() => row.locator('img').evaluate(image => image.complete && image.naturalWidth > 20)).toBe(true);
  }
  await phone.getByRole('button', { name: '关闭', exact: true }).click();
  await select(phone, 'Supernatural');
  for (const viewport of [{ width: 390, height: 844 }, { width: 844, height: 390 }]) {
    await phone.setViewportSize(viewport);
    await expect(phone.getByTestId('start-button')).toBeInViewport();
    expect(await phone.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    await phone.waitForTimeout(500);
    await phone.screenshot({ path: `reports/screenshots/public-mobile-${viewport.width}x${viewport.height}.png` });
  }
  await mobile.close();
  report.checks.push('Public mobile library, all sixteen cover images, night scene and portrait/landscape controls');
  expect(report.errors).toEqual([]);
  report.passed = true;
} catch (error) {
  report.passed = false; report.failure = error.stack || String(error); throw error;
} finally {
  await browser.close();
  writeFileSync('reports/public-deployment.json', JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
}
