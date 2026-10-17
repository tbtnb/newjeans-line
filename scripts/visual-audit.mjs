/** Native Babylon deterministic-state captures. These are not full playthroughs. */
import { chromium } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
const base=process.env.PLAYWRIGHT_BASE_URL||'http://127.0.0.1:4173';
const out='reports/screenshots/babylon-final';mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{}),args:['--enable-webgl']});
const watchdog=setTimeout(()=>{console.error('Visual audit exceeded four-minute bound; closing owned browser.');browser.close();process.exitCode=1;},240000);
const errors=[];const report={chromeVersion:await browser.version(),capturedAt:new Date().toISOString(),base,chartSHA256:createHash('sha256').update(readFileSync('src/levels.json')).digest('hex'),sourceSHA256:Object.fromEntries(['world.ts','world-geometry.ts','world-models.ts','level-design.ts','main.ts','style.css'].map(file=>[file,createHash('sha256').update(readFileSync(`src/${file}`)).digest('hex')])),kind:'Real native Babylon renderer; deterministic states and egg inspection camera; no audio or full-playthrough claim',scenes:[],resources:[],performance:[],errors};
try{
 const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});page.setDefaultTimeout(30000);
 page.on('response',response=>{if(response.status()>=400)errors.push(`HTTP ${response.status()}: ${response.url()}`);});
 page.on('pageerror',error=>errors.push(error.message));page.on('console',message=>{if(message.type()==='error')errors.push(message.text());});
 await page.goto(`${base}/tests/scene-capture.html`);await page.waitForFunction(()=>window.audit?.ready,{timeout:30000});
 const profiles=await page.evaluate(()=>window.audit.profiles);
 for(const profile of profiles){
   await page.evaluate(id=>window.audit.load(id,'menu','menu'),profile.id);await page.evaluate(()=>window.audit.waitReady());await page.waitForTimeout(150);
   await page.screenshot({path:`${out}/${profile.id}-menu.png`});
   await page.evaluate(id=>window.audit.load(id,'egg','game'),profile.id);await page.evaluate(()=>window.audit.waitReady());await page.waitForTimeout(150);
   const stats=await page.evaluate(()=>window.audit.stats());
   if(stats.webGL!==2||!stats.egg?.children||!stats.egg.enabled)throw Error(`Native geometry/egg missing in ${profile.id}`);
   await page.screenshot({path:`${out}/${profile.id}-story.png`});
   await page.evaluate(()=>window.audit.focusEgg());await page.waitForTimeout(100);
   await page.screenshot({path:`${out}/${profile.id}-egg.png`});
   const eggInspection=await page.evaluate(()=>window.audit.stats().egg);
   if(!eggInspection.activeChildren)throw Error(`No egg geometry was rendered in inspection camera for ${profile.id}`);
   report.scenes.push({...profile,stats,eggInspection,images:[`${profile.id}-menu.png`,`${profile.id}-story.png`,`${profile.id}-egg.png`]});
 }
 // Revisit the same level between complete cycles so model complexity is equal.
 for(let cycle=0;cycle<3;cycle++){
   for(const profile of profiles)await page.evaluate(id=>window.audit.load(id,'egg','game'),profile.id);
   await page.evaluate(()=>window.audit.load('new-jeans','egg','game'));await page.waitForTimeout(100);
   report.resources.push({cycle,...await page.evaluate(()=>window.audit.stats())});
 }
 for(const viewport of [{width:1440,height:900},{width:390,height:844},{width:375,height:667},{width:844,height:390}]){
   await page.setViewportSize(viewport);await page.evaluate(()=>window.audit.load('supernatural','egg','game'));
   await page.waitForTimeout(700);
   report.performance.push({viewport,...await page.evaluate(()=>window.audit.frames(150))});
   await page.screenshot({path:`${out}/supernatural-${viewport.width}x${viewport.height}-game.png`});
 }
 const first=report.resources[0];for(const item of report.resources.slice(1))for(const key of ['meshes','geometries','materials','textures','nodes'])if(item[key]!==first[key])errors.push(`Repeated-load resource drift ${key}: ${first[key]} -> ${item[key]}`);
 await page.evaluate(()=>window.audit.dispose());
 await page.setViewportSize({width:1440,height:1120});
 for(const kind of ['menu','story','egg']){
   await page.setContent(`<link rel="icon" href="${base}/icon.svg"><style>body{margin:12px;background:#e7edf0;color:#14233b;font:12px system-ui}main{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}figure{margin:0}img{width:100%;display:block}figcaption{padding:5px 2px}</style><h3>Native Babylon ${kind} — deterministic states, not full playthroughs</h3><main>${report.scenes.map(scene=>`<figure><img src="${base}/${out}/${scene.id}-${kind}.png"><figcaption>${scene.title} · ${scene.art.family}${kind==='egg'?` · ${scene.art.egg.name}`:''}</figcaption></figure>`).join('')}</main>`);
   await page.waitForFunction(()=>[...document.images].every(image=>image.complete&&image.naturalWidth>0));
   await page.screenshot({path:`${out}/contact-${kind}.png`,fullPage:true});
 }
}catch(error){errors.push(error?.stack||String(error));throw error;}finally{clearTimeout(watchdog);await browser.close();writeFileSync('reports/babylon-visual-audit.json',JSON.stringify(report,null,2));}
if(errors.length)throw Error(errors.join('\n'));
writeFileSync(`${out}/index.html`, `<!doctype html><meta charset="utf-8"><title>Native Babylon deterministic scene audit</title><style>body{font:14px system-ui;background:#eef2f3;color:#14233b;margin:24px}section{margin:28px 0}h2{font-size:18px}div{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}img{width:100%}figure{margin:0}figcaption{padding:8px}</style><h1>Native Babylon scene audit</h1><p>Deterministic states and egg inspection cameras. These images do not claim full audio playthroughs.</p>${report.scenes.map(scene=>`<section><h2>${scene.title} · ${scene.art.family} · ${scene.art.egg.name}</h2><div>${scene.images.map((file,i)=>`<figure><a href="${file}"><img src="${file}"></a><figcaption>${['Menu','Authored egg-time game state','Egg inspection camera'][i]}</figcaption></figure>`).join('')}</div></section>`).join('')}`);
console.log(JSON.stringify({scenes:report.scenes.length,resources:report.resources,performance:report.performance,errors},null,2));
