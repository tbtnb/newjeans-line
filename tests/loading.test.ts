import test from 'node:test';
import assert from 'node:assert/strict';
import {LoadingProgress} from '../src/loading';
test('combined loading reaches 100 only after audio decode and all scene tasks',()=>{
 const out:number[]=[];const p=new LoadingProgress(n=>out.push(n));
 p.update('audio',.9,'download complete');p.update('models',1,'models ready');p.update('road',1,'road ready');p.update('render',1,'GPU ready');
 assert.equal(out.at(-1),96);assert.ok(!out.includes(100));
 p.update('audio',1,'decoded');assert.equal(out.at(-1),100);
});
test('parallel callbacks and unknown file sizes never move the bar backward',()=>{
 const out:number[]=[];const p=new LoadingProgress(n=>out.push(n));
 p.update('models',.7,'models');p.update('audio',.8,'music');p.update('audio',-1,'unknown size');p.update('models',.2,'late callback');p.update('road',.5,'road');p.update('audio',NaN,'unknown');
 assert.ok(out.every((n,i)=>!i||n>=out[i-1]));assert.ok(out.every(n=>Number.isFinite(n)&&n<100));
});
test('cached audio leaves room for scenery and retries start a new progress session',()=>{
 const a:number[]=[],b:number[]=[];const p=new LoadingProgress(n=>a.push(n));p.update('audio',1,'cache');assert.equal(a[0],40);
 p.update('models',1,'cached');p.update('road',1,'prepared');p.update('render',.99,'compiling');assert.equal(a.at(-1),99);
 const retry=new LoadingProgress(n=>b.push(n));retry.update('audio',0,'retry');assert.equal(b[0],0);
});
