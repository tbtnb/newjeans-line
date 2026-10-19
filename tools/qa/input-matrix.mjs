import {chromium} from '@playwright/test';
import {mkdirSync,writeFileSync} from 'node:fs';
const [url,out]=process.argv.slice(2);mkdirSync(out,{recursive:true});
const b=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--use-angle=metal','--enable-gpu']});
const ctx=await b.newContext({viewport:{width:390,height:844},hasTouch:true});const trials=[];
for(const [offset,blocked] of [...[-150,-100,-50,-20,0,20,50,100,150].map(x=>[x,false]),[-50,true]]){
 const p=await ctx.newPage(),logs=[];p.on('pageerror',e=>logs.push(e.message));
 await p.goto(url);await p.waitForFunction(()=>window.__nj?.audio.ready,null,{timeout:90000});
 await p.evaluate(()=>{window.__nj.preview(1);const g=window.__nj.game,orig=g.tap.bind(g);window.__inputs=[];g.tap=t=>{const delivered=window.__nj.audio.songTime(),r=orig(t);window.__inputs.push({t,delivered,delayMs:(delivered-t)*1000,result:r,errorMs:(t-1.901)*1000,fail:g.failKind,cursor:g.cursor});return r;};});
 const cdp=await ctx.newCDPSession(p);const touch=async()=>{await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:195,y:650,id:1}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});};
 await touch();await p.waitForFunction(()=>window.__nj.audio.playing&&window.__nj.audio.songTime()>1.4);
 const sync=await p.evaluate(blocked=>{const n=window.__nj,now=performance.now(),s=n.audio.songTime();if(blocked)setTimeout(()=>{const end=performance.now()+180;while(performance.now()<end){}},Math.max(0,(1.8-s)*1000));return {s,wall:performance.timeOrigin+now};},blocked);
 const target=sync.wall+(1.901+offset/1000-sync.s)*1000;
 while(Date.now()<target)await new Promise(r=>setTimeout(r,Math.min(12,Math.max(1,target-Date.now()))));
 await touch();await p.waitForTimeout(70);
 trials.push({offset,blocked,...await p.evaluate(()=>({inputs:window.__inputs,status:window.__nj.game.status})),logs});
 await p.close();writeFileSync(`${out}/matrix.json`,JSON.stringify(trials,null,2));
}
await ctx.close();await b.close();console.log(JSON.stringify(trials));
