import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
const html=readFileSync('index.html','utf8'),css=readFileSync('src/style.css','utf8'),main=readFileSync('src/main.ts','utf8');
test('completion has no persistent fullscreen white flash layer',()=>{assert.ok(!html.includes('id="flash"'));assert.ok(!main.includes("setProperty('--flash'"));assert.ok(!css.includes('opacity: var(--flash)'));});
test('all restart actions have an outlined recognizable arrow and visible text label',()=>{
 for(const id of ['btn-retry','btn-replay','btn-restart-p']){const tag=html.match(new RegExp('<button[^>]*id="'+id+'"[^>]*>.*?</button>'))?.[0]??'';assert.match(tag,/aria-label="重新开始"/);assert.match(tag,/class="restart-icon"/);}
 for(const id of ['fail','pause','clear']){const section=html.split('id="'+id+'"')[1].split('</section>')[0];assert.match(section,/<span>重新开始<\/span>/);}
 assert.match(css,/\.hex-btn svg\.restart-icon\s*\{[^}]*fill: none;[^}]*stroke: currentColor/);
});
test('primary buttons keep fixed dark background and light glyphs regardless of sky theme',()=>{
 assert.match(css,/\.hex-btn\.big\s*\{[^}]*background: #2c2a28; color: #fff;/);
 assert.match(css,/\[hidden\]\s*\{ display: none !important; \}/);
});
