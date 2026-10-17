import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,statSync,readdirSync} from 'node:fs';
import {resolve} from 'node:path';
import type {Level} from '../src/types';

const levels=JSON.parse(readFileSync(new URL('../src/levels.json',import.meta.url),'utf8')) as Level[];
const expected=['Attention','Hype Boy','Cookie','Hurt','OMG','Ditto','New Jeans','Super Shy','ETA','Cool With You','Get Up','ASAP','How Sweet','Bubble Gum','Supernatural','Right Now'];
test('exactly the 16 requested vocal tracks are published, with no instrumentals',()=>{
 assert.equal(levels.length,16);
 assert.deepEqual(levels.map(l=>l.title),expected);
 assert.equal(new Set(levels.map(l=>l.id)).size,16);
 assert.equal(readdirSync(resolve('public/audio')).filter(f=>f.endsWith('.mp3')).length,16);
 assert.ok(levels.every(l=>!l.instrumental&&!/instrumental/i.test(l.title)));
});
test('every full song has a valid playable chart and real audio asset',()=>{
 let bytes=0;
 for(const l of levels){
  assert.ok(l.duration>30&&l.duration<300,l.title+' duration');
  assert.ok(l.bpm>=50&&l.bpm<=220,l.title+' bpm');
  assert.ok(l.turns.length>=10,l.title+' chart');
  assert.ok(l.turns[0]>=2,l.title+' lead-in');
  assert.ok(l.turns.at(-1)!<l.duration,l.title+' final turn');
  l.turns.forEach((t,i)=>assert.ok(Number.isFinite(t)&&(i===0||t-l.turns[i-1]>=0.24),l.title+' spacing'));
  assert.ok(/^\.\/audio\/[a-z0-9-]+\.mp3$/.test(l.audio),l.title+' base-path safe');
  const size=statSync(resolve('public',l.audio)).size;
  assert.ok(size>l.duration*13000,l.title+' full audio size');
  assert.ok(size<10*1024*1024,l.title+' mobile file size');
  bytes+=size;
 }
 assert.ok(bytes<60*1024*1024,'total audio budget');
});
