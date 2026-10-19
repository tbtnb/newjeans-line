import test from 'node:test';import assert from 'node:assert/strict';
import {FramePacer} from '../src/framepacing';
test('120-Hz display renders 120 or 60 actual callbacks according to mode',()=>{
 for(const target of [60,120] as const){const p=new FramePacer();let frames=0;for(let i=0;i<120;i++)if(p.due(i*1000/120,target))frames++;assert.equal(frames,target);}
});
test('120-fps mode cannot invent refreshes on a 60-Hz browser, and resumes after a stall',()=>{
 const p=new FramePacer();let frames=0;for(let i=0;i<60;i++)if(p.due(i*1000/60,120))frames++;assert.equal(frames,60);assert.ok(p.due(10000,120));assert.ok(p.due(10001,120));p.reset();assert.ok(p.due(10001,120));
});

test('120 mode never drops uneven high-refresh callbacks',()=>{const p=new FramePacer();let t=0;for(let i=0;i<240;i++){t+=i%2?9.6:7.06;assert.ok(p.due(t,120));}});
