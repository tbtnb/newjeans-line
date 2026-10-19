// macOS WebKit in iPhone dimensions; NOT a physical iPhone test.
import {webkit,devices} from '@playwright/test';
import {mkdirSync,writeFileSync} from 'node:fs';
const out='evidence/webkit';mkdirSync(out,{recursive:true});
const b=await webkit.launch({headless:true});const ctx=await b.newContext({...devices['iPhone 13']});const p=await ctx.newPage(),logs=[];
p.on('console',m=>{if(['warning','error'].includes(m.type()))logs.push(m.type()+': '+m.text())});p.on('pageerror',e=>logs.push(e.message));
await p.goto(process.env.PLAYWRIGHT_BASE_URL ?? 'http://127.0.0.1:4173/?level=omg&debug');await p.waitForFunction(()=>window.__nj?.audio.ready,null,{timeout:90000});
await p.locator('#menu').tap({position:{x:195,y:500}});await p.waitForFunction(()=>window.__nj.state==='ready');
await p.locator('#stage').tap({position:{x:195,y:650}});await p.waitForFunction(()=>window.__nj.audio.state==='running'&&window.__nj.audio.songTime()>.3);
const result=await p.evaluate(()=>({engine:'macOS WebKit',state:window.__nj.audio.state,songTime:window.__nj.audio.songTime(),playing:window.__nj.audio.playing,buffer:window.__nj.audio.buffer?.duration,sourceStarted:!!window.__nj.audio.source}));
await p.screenshot({path:`${out}/audio-start.png`});
for(const [name,width,height] of [['portrait',390,844],['landscape',844,390],['desktop',1280,800]]){
 await p.setViewportSize({width,height});await p.evaluate(()=>window.__nj.preview(45.65));await p.waitForTimeout(700);await p.screenshot({path:`${out}/${name}.png`});
}
writeFileSync(`${out}/result.json`,JSON.stringify({result,logs},null,2));console.log(JSON.stringify({result,logs}));await ctx.close();await b.close();
