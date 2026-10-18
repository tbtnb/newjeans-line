// Capture-pipeline A/V calibration: a page beeps (WebAudio, scheduled) and flashes a top-left square when the
// beep is *heard* according to getOutputTimestamp (the same clock model the game uses). Recorded with the same
// x11grab+pulse ffmpeg pipeline as tools/qa/play.mjs. flash-minus-beep = capture offset + render latency.
import { chromium } from '@playwright/test'; import { spawn } from 'node:child_process';
const out = process.argv[2] ?? '/tmp/avcal-out.mp4';
const b = await chromium.launch({ headless: false, executablePath: '/usr/bin/google-chrome', env: { ...process.env, DISPLAY: process.env.DISPLAY ?? ':99' }, args: ['--autoplay-policy=no-user-gesture-required', '--window-position=0,0', '--window-size=540,1100', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--hide-scrollbars'] });
const page = await (await b.newContext({ viewport: null })).newPage();
await page.goto('file://' + new URL('./index.html', import.meta.url).pathname); await page.waitForTimeout(800);
const geo = await page.evaluate(() => ({ x: window.screenX, y: window.screenY + (window.outerHeight - window.innerHeight) }));
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-thread_queue_size', '1024', '-f', 'x11grab', '-draw_mouse', '0', '-framerate', '30', '-video_size', '540x960', '-i', `${process.env.DISPLAY ?? ':99'}+${geo.x},${geo.y}`, '-thread_queue_size', '1024', ...(process.env.FRAG ? ['-fragment_size', process.env.FRAG] : []), '-f', 'pulse', '-i', 'rec.monitor', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', out], { stdio: ['pipe', 'inherit', 'inherit'] });
await page.waitForTimeout(1500); await page.evaluate(() => window.go()); await page.waitForTimeout(17500);
console.log(JSON.stringify(await page.evaluate(() => window.info())));
ff.stdin.write('q'); await new Promise(r => ff.on('close', r)); await b.close();
