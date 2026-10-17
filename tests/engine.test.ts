import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { GameEngine, buildPath, positionAt, SPEED } from '../src/engine';
import { AudioTransport } from '../src/audio';
import type { Level } from '../src/types';

const level: Level = { id:'test', title:'Test', artist:'NewJeans', album:'Test', duration:5, bpm:120, offset:0, difficulty:1, theme:'meadow', accent:'#85c6b1', audio:'test.mp3', turns:[1,2,3,4], sections:[], instrumental:false };
function perfectRun(song: Level): GameEngine {
  const engine = new GameEngine(song);
  engine.start();
  for (const time of song.turns) {
    engine.update(Math.max(0, time - 0.2));
    const snapshot = engine.tap(time);
    assert.equal(snapshot.status, 'playing', `${song.title}: turn at ${time}`);
    assert.equal(snapshot.lastRating, 'perfect');
  }
  return engine;
}

test('authored path has physical lengths and alternates x / negative z', () => {
  assert.deepEqual(buildPath(level), [
    {x:0,z:0,time:0}, {x:6,z:0,time:1}, {x:6,z:-6,time:2},
    {x:12,z:-6,time:3}, {x:12,z:-12,time:4}, {x:18,z:-12,time:5},
  ]);
  assert.deepEqual(positionAt(level,1.5), {x:6,z:-3});
  assert.deepEqual(positionAt(level,99), {x:18,z:-12});
  assert.deepEqual(positionAt(level,-1), {x:0,z:0});
  assert.throws(() => buildPath({...level,turns:[1,1]}));
});

test('perfect run earns 100 accuracy, ten diamonds and three crowns', () => {
  const result = perfectRun(level).update(level.duration);
  assert.equal(result.status,'complete');
  assert.equal(result.progress,1);
  assert.equal(result.turnsHit,4);
  assert.equal(result.combo,4);
  assert.equal(result.accuracy,100);
  assert.equal(result.diamonds,10);
  assert.equal(result.crowns,3);
  assert.equal(result.nextTurn,null);
  assert.deepEqual(result.position,positionAt(level,level.duration));
});

test('normal mode never auto turns and stops at the corner boundary on a miss', () => {
  const engine = new GameEngine(level); engine.start();
  const result = engine.update(4);
  assert.equal(result.status,'failed');
  assert.equal(result.direction,0);
  assert.equal(result.turnsHit,0);
  assert.equal(result.nextTurn,1);
  assert.match(result.failureReason!,/太晚/);
  assert.ok(Math.abs(result.position.x-6.6)<1e-6);
  assert.deepEqual(engine.tap(4.1),result);
});

test('early, late and repeated taps fail; both timing boundaries succeed', () => {
  const early = new GameEngine(level); early.start();
  assert.match(early.tap(0.89).failureReason!,/太早/);
  const late = new GameEngine(level); late.start();
  assert.match(late.tap(1.11).failureReason!,/太晚/);
  for (const time of [0.9,1.1]) {
    const boundary = new GameEngine(level); boundary.start();
    const result = boundary.tap(time);
    assert.equal(result.status,'playing');
    assert.equal(result.direction,1);
    assert.equal(result.lastRating,'good');
    assert.equal(boundary.tap(time).status,'failed');
  }
});

test('valid timing variation never accumulates position drift', () => {
  const engine = new GameEngine(level); engine.start();
  for (const time of level.turns) {
    const result = engine.tap(time+0.08);
    assert.equal(result.status,'playing');
    assert.deepEqual(result.position,positionAt(level,time));
  }
  assert.equal(engine.update(5).status,'complete');
});

test('alternating early and late accepted taps stay within each corner footprint', () => {
  const engine = new GameEngine(level); engine.start();
  engine.tap(0.9);
  // Before the next late tap the line may extend only 0.6 units past its corner.
  const beforeLate=engine.update(2.099999);
  assert.ok(Math.abs(beforeLate.position.z+6)<=0.600001);
  assert.equal(engine.tap(2.1).status,'playing');
  assert.equal(engine.tap(2.9).status,'playing');
  const nextLate=engine.update(4.099999);
  assert.ok(Math.abs(nextLate.position.z+12)<=0.600001);
  assert.equal(engine.tap(4.1).status,'playing');
  const completed=engine.update(5);
  assert.equal(completed.status,'complete');
  assert.deepEqual(completed.position,positionAt(level,5));
});

test('negative latency and end-of-song latency retain the authored route', () => {
  const engine = new GameEngine(level,{offsetMs:-100}); engine.start();
  for (const time of level.turns) assert.equal(engine.tap(time-0.1).lastRating,'perfect');
  assert.equal(engine.update(4.9).status,'playing','negative latency must not cut off the final audio');
  assert.equal(engine.update(5).status,'complete');
  assert.deepEqual(engine.snapshot().position,positionAt(level,5));
});

test('pause freezes time and taps; resume and reset preserve their contract', () => {
  const engine = new GameEngine(level); engine.start(); engine.tap(1);
  const paused = engine.pause();
  assert.equal(paused.status,'paused');
  assert.deepEqual(engine.update(2),paused);
  assert.deepEqual(engine.tap(2),paused);
  engine.resume();
  assert.equal(engine.tap(2).turnsHit,2);
  const reset = engine.reset();
  assert.equal(reset.status,'ready');
  assert.equal(reset.time,0);
  assert.equal(reset.turnsHit,0);
  assert.equal(reset.nextTurn,1);
  assert.equal(reset.failureReason,null);
  assert.deepEqual(reset.position,{x:0,z:0});
  engine.reset(2.5); engine.start();
  assert.equal(engine.tap(3).status,'playing');
});

test('practice recovers missed corners and counts only real hits', () => {
  const engine = new GameEngine(level,{practice:true}); engine.start();
  assert.equal(engine.tap(0.2).status,'playing');
  engine.update(1.05);
  const recovery = engine.update(2.5);
  assert.equal(recovery.status,'playing');
  assert.equal(recovery.lastRating,'miss');
  assert.deepEqual(recovery.position,positionAt(level,2.5));
  engine.tap(3);
  const result = engine.update(5);
  assert.equal(result.status,'complete');
  assert.equal(result.turnsHit,1);
  assert.ok(result.accuracy<100);
  assert.equal(result.crowns,3);
});

test('latency shifts inputs and movement together and completes at audio end', () => {
  const engine = new GameEngine(level,{offsetMs:150}); engine.start();
  assert.equal(engine.update(0.65).time,0.5);
  for (const time of level.turns) assert.equal(engine.tap(time+0.15).lastRating,'perfect');
  assert.equal(engine.update(5).status,'complete');
});

test('snapshot objects are isolated and long-song trails remain bounded', () => {
  const engine = new GameEngine({...level,duration:300,turns:[]}); engine.start();
  for (let frame=1;frame<=18000;frame++) engine.update(frame/60);
  const result = engine.snapshot();
  assert.equal(result.status,'complete');
  assert.ok(result.trail.length<=180);
  result.position.x=-100; result.trail[0].x=-100;
  assert.ok(Math.abs(engine.snapshot().position.x-300*SPEED)<1e-6);
  assert.notEqual(engine.snapshot().trail[0].x,-100);
});

test('all sixteen delivered full-song charts complete deterministically', async () => {
  const songs: Level[] = JSON.parse(await readFile(new URL('../src/levels.json',import.meta.url),'utf8'));
  assert.equal(songs.length,16);
  assert.ok(songs.every(song=>!song.instrumental));
  for (const song of songs) {
    const path=buildPath(song);
    for (let index=1;index<path.length;index++) {
      const a=path[index-1],b=path[index];
      assert.ok(Math.abs(Math.hypot(b.x-a.x,b.z-a.z)-(b.time-a.time)*SPEED)<1e-6);
    }
    const result=perfectRun(song).update(song.duration);
    assert.equal(result.status,'complete',song.title);
    assert.equal(result.turnsHit,song.turns.length,song.title);
    assert.equal(result.accuracy,100,song.title);
    assert.equal(result.diamonds,10,song.title);
    assert.equal(result.crowns,3,song.title);
  }
});

test('audio uses its clock, unlocks on load, pauses and resumes exactly', async () => {
  const previousAudio=globalThis.AudioContext,previousFetch=globalThis.fetch;
  let instance: FakeContext;
  class FakeSource { buffer:unknown; onended:(()=>void)|null=null; connect(){} disconnect(){} stop(){} start(){} }
  class FakeContext {
    currentTime=0; state='suspended'; resumes=0;
    constructor(){instance=this;}
    createGain(){return {gain:{value:0,setTargetAtTime(){}},connect(){},disconnect(){}};}
    createBufferSource(){return new FakeSource();}
    async resume(){this.resumes++;this.state='running';}
    async close(){this.state='closed';}
    async decodeAudioData(){return {duration:5};}
  }
  Object.defineProperty(globalThis,'AudioContext',{configurable:true,writable:true,value:FakeContext});
  globalThis.fetch=async()=>new Response(new Uint8Array([1,2,3]));
  try {
    const transport=new AudioTransport();
    const loading=transport.load('song.mp3');
    assert.equal(instance!.resumes,1,'unlock occurs before the network await');
    await loading;
    assert.equal(transport.duration,5);
    await transport.play();
    instance!.currentTime=1.25;
    assert.equal(transport.currentTime,1.25);
    transport.pause(); instance!.currentTime=10;
    assert.equal(transport.currentTime,1.25);
    await transport.play(); instance!.currentTime=11;
    assert.equal(transport.currentTime,2.25);
    transport.setVolume(0.4); transport.stop();
    assert.equal(transport.currentTime,0);
    globalThis.fetch=async()=>new Response('',{status:503});
    await assert.rejects(transport.load('broken.mp3'),/HTTP 503/);
    assert.equal(transport.duration,0);
    let release: (response: Response)=>void = ()=>{};
    let oldSignal: AbortSignal|null|undefined;
    globalThis.fetch=async(url,init)=> {
      if (url==='slow.mp3') {
        oldSignal=init?.signal;
        return new Promise<Response>(resolve=>{release=resolve;});
      }
      return new Response(new Uint8Array([1,2,3]));
    };
    const old=transport.load('slow.mp3').catch(error=>error as Error);
    await transport.load('new.mp3');
    assert.equal(oldSignal?.aborted,true);
    release(new Response(new Uint8Array([1,2,3])));
    assert.equal((await old as Error).name,'AbortError');
    assert.equal(transport.duration,5,'a stale load cannot clear the new decoded song');
    transport.destroy();
    assert.equal(instance!.state,'closed');
    await assert.rejects(transport.play(),/已关闭/);
  } finally {
    Object.defineProperty(globalThis,'AudioContext',{configurable:true,writable:true,value:previousAudio});
    globalThis.fetch=previousFetch;
  }
});
