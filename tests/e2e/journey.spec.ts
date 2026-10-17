import { test, expect, type Page, type TestInfo } from '@playwright/test';
import { readFileSync, mkdirSync } from 'node:fs';
import type { Level } from '../../src/types';
import { getLevelArt } from '../../src/level-design';

const levels = (JSON.parse(readFileSync(new URL('../../src/levels.json', import.meta.url), 'utf8')) as Level[]).filter(song => !song.instrumental);
const getUp = levels.find(song => song.title === 'Get Up')!;
const initial = levels.find(song => song.title === 'New Jeans') ?? levels[0];
const saveKey = 'newjeans-line.save.v1';
const faults = new WeakMap<Page, string[]>();

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    const audit = { draws: 0, frameDraws: 0, maxFrameDraws: 0 }; (window as any).__renderAudit = audit;
    for (const context of [WebGLRenderingContext, WebGL2RenderingContext]) for (const name of ['drawElements', 'drawArrays', 'drawElementsInstanced', 'drawArraysInstanced']) {
      const prototype = context.prototype as any, draw = prototype[name]; if (!draw) continue;
      prototype[name] = function (...args: any[]) { audit.draws++; audit.frameDraws++; return draw.apply(this, args); };
    }
    const frame = () => { audit.maxFrameDraws = Math.max(audit.maxFrameDraws, audit.frameDraws); audit.frameDraws = 0; requestAnimationFrame(frame); }; requestAnimationFrame(frame);
  });
  const errors: string[] = [];
  faults.set(page, errors);
  page.on('pageerror', error => errors.push(`Page error: ${error.message}`));
  page.on('console', message => {
    if (message.type() === 'error') errors.push(`Console: ${message.text()}`);
  });
  page.on('response', response => {
    if (response.status() === 404) errors.push(`404: ${response.url()}`);
  });
});

test.afterEach(async ({ page }, info) => {
  const errors = faults.get(page) ?? [];
  const unexpected = info.title.includes('failed audio request')
    ? errors.filter(error => !error.includes('503 (Service Unavailable)')) : errors;
  expect(unexpected, 'no browser exceptions, console errors or missing assets').toEqual([]);
});

async function open(page: Page) {
  await page.goto('./');
  await expect(page.getByTestId('song-title')).toHaveText(initial.title);
  await expect(page.getByTestId('game-canvas')).toBeVisible();
  await expect.poll(() => page.evaluate(() => (window as any).__renderAudit.maxFrameDraws), { timeout: 20000, message: 'native WebGL actually draws the multi-mesh landscape' }).toBeGreaterThan(5);
}

async function selectSong(page: Page, title: string) {
  await page.getByRole('button', { name: '曲库', exact: true }).click();
  await page.getByTestId('song-search').fill(title);
  await page.getByTestId('song-row').filter({ has: page.locator('strong', { hasText: new RegExp(`^${title}$`) }) }).click();
  await expect(page.getByTestId('song-title')).toHaveText(title);
}

async function screenshot(page: Page, info: TestInfo, name: string) {
  mkdirSync('reports/screenshots', { recursive: true });
  await page.screenshot({ path: `reports/screenshots/${info.project.name}-${name}.png` });
}

async function assertNoOverflow(page: Page) {
  const bounds = await page.evaluate(() => ({ viewport: innerWidth, page: document.documentElement.scrollWidth }));
  expect(bounds.page).toBeLessThanOrEqual(bounds.viewport + 1);
}

test('song navigation, searchable complete library and album filter work', async ({ page }, info) => {
  await open(page);
  await screenshot(page, info, 'journey');
  await page.getByTestId('next-song').click();
  await expect(page.getByTestId('song-title')).toHaveText(levels[(levels.indexOf(initial) + 1) % levels.length].title);
  await page.getByTestId('previous-song').click();
  await expect(page.getByTestId('song-title')).toHaveText(initial.title);
  await page.getByRole('button', { name: '曲库', exact: true }).click();
  await expect(page.getByTestId('song-row')).toHaveCount(levels.length);
  await screenshot(page, info, 'library');
  const album = getUp.album;
  await page.locator('#album-filter').selectOption(album);
  await expect(page.getByTestId('song-row')).toHaveCount(levels.filter(song => song.album === album).length);
  await page.getByTestId('song-search').fill('there-is-no-such-track');
  await expect(page.locator('.empty-state')).toBeVisible();
  await page.getByTestId('song-search').fill('Get Up');
  await expect(page.getByTestId('song-row')).toHaveCount(levels.filter(song => song.album === album && `${song.title} ${song.album}`.toLowerCase().includes('get up')).length);
  await page.getByTestId('song-row').filter({ has: page.locator('strong', { hasText: /^Get Up$/ }) }).click();
  await expect(page.getByTestId('song-title')).toHaveText('Get Up');
  await page.reload();
  await expect(page.getByTestId('song-title')).toHaveText('Get Up');
  await assertNoOverflow(page);
});

test('settings persist and a corrupt imported file preserves existing progress', async ({ page }, info) => {
  await open(page);
  await page.getByTestId('settings-button').click();
  await page.getByTestId('volume-slider').fill('37');
  await page.getByTestId('latency-slider').fill('120');
  await page.getByText('轻量画质', { exact: true }).click();
  await page.getByText('触感反馈', { exact: true }).click();
  await page.getByText('道路引导', { exact: true }).click();
  await screenshot(page, info, 'settings');
  await page.reload();
  await page.getByTestId('settings-button').click();
  await expect(page.getByTestId('volume-slider')).toHaveValue('37');
  await expect(page.getByTestId('latency-slider')).toHaveValue('120');
  await expect(page.locator('#quality')).toBeChecked();
  await expect(page.locator('#vibration')).not.toBeChecked();
  await expect(page.getByTestId('guide-toggle')).not.toBeChecked();
  const before = await page.evaluate(key => localStorage.getItem(key), saveKey);
  const chooserEvent = page.waitForEvent('filechooser');
  await page.getByTestId('import-save').click();
  const chooser = await chooserEvent;
  await chooser.setFiles({ name: 'corrupt.json', mimeType: 'application/json', buffer: Buffer.from('{"version":1,"records":null}') });
  await expect(page.locator('#dialog .dialog-feedback')).toContainText('不是有效');
  expect(await page.evaluate(key => localStorage.getItem(key), saveKey)).toBe(before);
  const downloadEvent = page.waitForEvent('download');
  await page.getByTestId('export-save').click();
  const download = await downloadEvent;
  expect(download.suggestedFilename()).toMatch(/^newjeans-line-.*\.json$/);
  await assertNoOverflow(page);
});

test('real MP3 starts, progress advances, pause freezes, resume, no-input failure and retry work', async ({ page }, info) => {
  await page.addInitScript(() => {
    const observer = { starts: [] as number[], stops: 0 }; (window as any).__pauseAudio = observer;
    const start = AudioBufferSourceNode.prototype.start, stop = AudioBufferSourceNode.prototype.stop;
    AudioBufferSourceNode.prototype.start = function (...args: Parameters<AudioBufferSourceNode['start']>) { observer.starts.push(args[1] ?? 0); return start.apply(this, args); };
    AudioBufferSourceNode.prototype.stop = function (...args: Parameters<AudioBufferSourceNode['stop']>) { observer.stops++; return stop.apply(this, args); };
  });
  await open(page);
  await selectSong(page, 'Get Up');
  const audioResponse = page.waitForResponse(response => response.url().endsWith(getUp.audio.slice(1)) && response.status() === 200);
  await page.getByTestId('start-button').click();
  const response = await audioResponse;
  expect(Number(response.headers()['content-length'])).toBeGreaterThan(100000);
  await expect(page.locator('#hud')).toBeVisible();
  await expect.poll(async () => parseInt(await page.getByTestId('hud-percent').innerText())).toBeGreaterThan(0);
  await page.getByTestId('pause-button').click();
  await expect(page.getByTestId('resume-button')).toBeVisible();
  const paused = await page.getByTestId('hud-percent').innerText();
  await screenshot(page, info, 'pause');
  await page.waitForTimeout(300);
  const frozenScene = await page.getByTestId('game-canvas').screenshot();
  const pausedAudio = await page.evaluate(() => (window as any).__pauseAudio);
  expect(pausedAudio.stops).toBeGreaterThan(0);
  await page.waitForTimeout(800);
  await expect(page.getByTestId('hud-percent')).toHaveText(paused);
  expect((await page.getByTestId('game-canvas').screenshot()).equals(frozenScene), 'the paused Babylon frame stays pixel-identical').toBe(true);
  expect(await page.evaluate(() => (window as any).__pauseAudio)).toEqual(pausedAudio);
  await page.getByTestId('resume-button').click();
  await expect.poll(() => page.evaluate(() => (window as any).__pauseAudio.starts.length)).toBe(2);
  expect(await page.evaluate(() => (window as any).__pauseAudio.starts[1])).toBeGreaterThan(0);
  await expect(page.locator('#dialog')).not.toBeVisible();
  await expect(page.getByTestId('result-percent')).toBeVisible({ timeout: (getUp.turns[0] + 4) * 1000 });
  await expect(page.locator('#dialog-title')).toHaveText('再听一次，再近一点');
  await screenshot(page, info, 'failure');
  const firstResult = parseInt(await page.getByTestId('result-percent').innerText());
  expect(firstResult).toBeGreaterThan(0);
  expect(firstResult).toBeLessThan(100);
  await page.getByTestId('retry-button').click();
  await expect(page.locator('#hud')).toBeVisible();
  await expect(page.locator('#dialog')).not.toBeVisible();
  await page.getByTestId('game-canvas').click({ position: { x: 30, y: 300 } });
  await expect(page.locator('.result-note')).toContainText('转弯太早');
  await page.locator('[data-action="home"]').click();
  await expect(page.getByTestId('start-button')).toBeVisible();
  await expect(page.getByTestId('song-title')).toHaveText('Get Up');
  await page.reload();
  const stored = await page.evaluate(key => JSON.parse(localStorage.getItem(key)!), saveKey);
  expect(stored.records[getUp.id].attempts).toBe(2);
  expect(stored.records[getUp.id].best).toBeGreaterThan(0);
});

test('practice plays the entire real Get Up song and never writes normal records', async ({ page }, info) => {
  await open(page);
  await selectSong(page, 'Get Up');
  await page.locator('.practice-switch').click();
  await expect(page.getByTestId('practice-toggle')).toBeChecked();
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud-practice')).toContainText('不计入记录');
  await expect.poll(async () => parseInt(await page.getByTestId('hud-percent').innerText())).toBeGreaterThan(10);
  await screenshot(page, info, 'practice-playing');
  await expect(page.getByTestId('result-percent')).toHaveText('100%', { timeout: (getUp.duration + 8) * 1000 });
  await expect(page.locator('#dialog-title')).toHaveText('练习，也是旅程');
  await expect(page.locator('.practice-note')).toBeVisible();
  await screenshot(page, info, 'practice-complete');
  const stored = await page.evaluate(key => JSON.parse(localStorage.getItem(key)!), saveKey);
  expect(stored.records).toEqual({});
  await page.locator('[data-action="home"]').click();
  await page.getByRole('button', { name: '记录', exact: true }).click();
  await expect(page.locator('.record-summary')).toContainText(`0 / ${levels.length}`);
});

test('normal mode accepts timed key turns through a full unmodified real-audio song', async ({ page }, info) => {
  // Observe native source starts and send ordinary Space events against its real
  // clock. The audio, chart, playback rate and application state stay untouched.
  await page.addInitScript(({ turns }) => {
    const nativeStart = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function (...args: Parameters<AudioBufferSourceNode['start']>) {
      nativeStart.apply(this, args);
      const source = this;
      const started = source.context.currentTime;
      const observation = { playbackRate: source.playbackRate.value, bufferDuration: source.buffer?.duration, wallStarted: performance.now(), context: source.context, started, errors: [] as number[] };
      (window as any).__normalAudio = observation;
      let next = 0;
      const timer = window.setInterval(() => {
        const at = source.context.currentTime - started + (args[1] ?? 0);
        if (next < turns.length && at >= turns[next]) {
          observation.errors.push(at - turns[next]);
          window.dispatchEvent(new KeyboardEvent('keydown', { code: 'Space', key: ' ', bubbles: true }));
          next++;
        }
        if (next === turns.length) window.clearInterval(timer);
      }, 3);
    };
  }, { turns: getUp.turns });
  await open(page);
  await selectSong(page, 'Get Up');
  await page.getByTestId('settings-button').click();
  await page.getByText('轻量画质', { exact: true }).click();
  await page.getByRole('button', { name: '关闭', exact: true }).click();
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud-combo')).toContainText('连续转弯', { timeout: (getUp.turns[1] + 4) * 1000 });
  await screenshot(page, info, 'normal-turns');
  await expect(page.getByTestId('result-percent')).toHaveText('100%', { timeout: (getUp.duration + 8) * 1000 });
  await expect(page.locator('#dialog-title')).toHaveText('这一路，为你加冕');
  const audio = await page.evaluate(() => { const a = (window as any).__normalAudio; return { playbackRate: a.playbackRate, bufferDuration: a.bufferDuration, elapsed: (performance.now() - a.wallStarted) / 1000, errors: a.errors }; });
  expect(audio.playbackRate).toBe(1);
  expect(Math.abs(audio.bufferDuration - getUp.duration)).toBeLessThan(.2);
  expect(audio.elapsed, 'whole song elapsed in real wall-clock time').toBeGreaterThan(getUp.duration - .5);
  expect(audio.errors).toHaveLength(getUp.turns.length);
  expect(Math.max(...audio.errors.map(Math.abs))).toBeLessThan(.1);
  await screenshot(page, info, 'normal-complete');
  const stored = await page.evaluate(key => JSON.parse(localStorage.getItem(key)!), saveKey);
  expect(stored.records[getUp.id]).toMatchObject({ best: 1, diamonds: 10, crowns: 3, attempts: 1, completed: true });
  await page.locator('[data-action="home"]').click();
  await page.reload();
  await expect(page.locator('#song-best')).toContainText('100% 已完成');
});

test('failed audio request has a visible recovery path and a later real load succeeds', async ({ page }) => {
  await open(page);
  await selectSong(page, 'Get Up');
  await page.route('**/audio/*.mp3', route => route.fulfill({ status: 503, body: 'Temporary test failure' }));
  await page.getByTestId('start-button').click();
  await expect(page.locator('#toast')).toContainText('音乐加载失败');
  await expect(page.getByTestId('start-button')).toBeVisible();
  await page.unroute('**/audio/*.mp3');
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud')).toBeVisible();
  await page.getByTestId('pause-button').click();
  await page.locator('[data-action="home"]').click();
  await expect(page.getByTestId('start-button')).toBeVisible();
});

test('small portrait and landscape controls stay inside the viewport', async ({ page }, info) => {
  test.skip(info.project.name !== 'mobile', 'phone layout coverage');
  await open(page);
  for (const viewport of [{ width: 390, height: 844 }, { width: 375, height: 667 }, { width: 844, height: 390 }]) {
    await page.setViewportSize(viewport);
    await assertNoOverflow(page);
    await expect(page.getByTestId('start-button')).toBeInViewport();
    await expect(page.getByTestId('settings-button')).toBeInViewport();
    await expect(page.getByRole('button', { name: '曲库', exact: true })).toBeInViewport();
    await screenshot(page, info, `${viewport.width}x${viewport.height}`);
    await page.getByRole('button', { name: '曲库', exact: true }).click();
    await expect(page.getByTestId('song-search')).toBeInViewport();
    await assertNoOverflow(page);
    await page.getByRole('button', { name: '关闭', exact: true }).click();
  }
});


test('all sixteen album covers load and selected scene captions match the album design', async ({ page }) => {
  await open(page);
  await page.getByRole('button', { name: '曲库', exact: true }).click();
  for (const song of levels) {
    const row = page.getByTestId('song-row').filter({ has: page.locator('strong', { hasText: new RegExp(`^${song.title}$`) }) });
    await row.scrollIntoViewIfNeeded();
    await expect.poll(() => row.locator('img').evaluate((image: HTMLImageElement) => image.complete && image.naturalWidth > 20)).toBe(true);
    await expect(row.locator('img')).toHaveAttribute('src', getLevelArt(song.id).cover);
  }
  await page.getByRole('button', { name: '关闭', exact: true }).click();
  for (const song of levels) {
    await page.getByRole('button', { name: `选择 ${song.title}`, exact: true }).click();
    await expect(page.getByTestId('song-title')).toHaveText(song.title);
    await expect(page.locator('#song-scene')).toHaveText(getLevelArt(song.id).subtitle);
    await expect.poll(() => page.locator('#song-cover').evaluate((image: HTMLImageElement) => image.complete && image.naturalWidth > 20)).toBe(true);
    await expect(page.locator('#song-cover')).toHaveAttribute('src', getLevelArt(song.id).cover);
    await expect(page.locator('body')).toHaveAttribute('data-dark', String(getLevelArt(song.id).dark));
  }
});

test('night scene keeps menu, loading artwork, HUD and pause text readable', async ({ page }, info) => {
  await open(page);
  await selectSong(page, 'Supernatural');
  await screenshot(page, info, 'supernatural-night-menu');
  const contrast = await page.evaluate(() => {
    const canvas = document.createElement('canvas'); canvas.width = canvas.height = 1;
    const ctx = canvas.getContext('2d')!;
    const rgb = (color: string) => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = color; ctx.fillRect(0, 0, 1, 1); return [...ctx.getImageData(0, 0, 1, 1).data].slice(0, 3); };
    const luminance = (color: number[]) => color.map(value => { const x = value / 255; return x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4; }).reduce((sum, value, i) => sum + value * [.2126, .7152, .0722][i], 0);
    const fg = luminance(rgb(getComputedStyle(document.querySelector('#song-title')!).color));
    const bg = luminance(rgb(getComputedStyle(document.documentElement).getPropertyValue('--scene-background')));
    return (Math.max(fg, bg) + .05) / (Math.min(fg, bg) + .05);
  });
  expect(contrast, 'title against the night scene background').toBeGreaterThan(4.5);
  await page.route('**/audio/*.mp3', async route => { await new Promise(resolve => setTimeout(resolve, 1500)); await route.continue(); });
  await page.getByTestId('start-button').click();
  await expect(page.locator('#loading')).toBeVisible();
  await expect.poll(() => page.locator('#loading-concept').evaluate((image: HTMLImageElement) => image.complete && image.naturalWidth > 100)).toBe(true);
  await screenshot(page, info, 'supernatural-loading-concept');
  await expect(page.locator('#hud')).toBeVisible();
  await expect(page.locator('#hud-song')).toHaveText('Supernatural');
  await expect(page.locator('#hud-percent')).toHaveCSS('color', 'rgb(255, 246, 232)');
  await screenshot(page, info, 'supernatural-night-hud');
  await page.getByTestId('pause-button').click();
  await expect(page.getByTestId('resume-button')).toBeVisible();
  await screenshot(page, info, 'supernatural-night-pause');
  await page.getByTestId('home-button').click();
});

test('real mobile touchscreen turns twice with one pointer event per tap', async ({ page }, info) => {
  test.skip(info.project.name !== 'mobile', 'native Chromium touch event coverage');
  await page.addInitScript(() => {
    const observed = window as typeof window & { __touchClock?: { context: BaseAudioContext; started: number }; __touchEvents: number };
    observed.__touchEvents = 0;
    document.addEventListener('pointerdown', event => { if ((event.target as HTMLElement).dataset.testid === 'game-canvas' && event.pointerType === 'touch') observed.__touchEvents++; });
    const nativeStart = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function (...args: Parameters<AudioBufferSourceNode['start']>) {
      nativeStart.apply(this, args);
      observed.__touchClock = { context: this.context, started: this.context.currentTime - (args[1] ?? 0) };
    };
  });
  await open(page);
  await selectSong(page, 'Get Up');
  await page.getByTestId('start-button').click();
  await expect(page.locator('#hud')).toBeVisible();
  const box = await page.getByTestId('game-canvas').boundingBox();
  expect(box).not.toBeNull();
  for (const at of getUp.turns.slice(0, 2)) {
    await page.waitForFunction(at => {
      const clock = (window as any).__touchClock;
      return clock && clock.context.currentTime - clock.started >= at - .045;
    }, at, { polling: 'raf' });
    await page.touchscreen.tap(box!.x + box!.width / 2, box!.y + box!.height / 2);
    await expect(page.locator('#dialog')).not.toBeVisible();
  }
  await expect(page.locator('#hud-combo')).toHaveText('2 连续转弯');
  expect(await page.evaluate(() => (window as any).__touchEvents)).toBe(2);
  await screenshot(page, info, 'real-touch-turns');
  await page.getByTestId('pause-button').click();
});
