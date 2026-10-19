import test from 'node:test';import assert from 'node:assert/strict';
import {AudioTransport} from '../src/audio';
function setup(){
 let resolve!:()=>void;const resumed=new Promise<void>(r=>resolve=r);let created=0;
 const gain={value:1,cancelScheduledValues(){},setValueAtTime(){},linearRampToValueAtTime(){}};
 const ctx={state:'suspended',currentTime:10,outputLatency:0,baseLatency:0,resume:()=>resumed,createBufferSource:()=>{created++;return {buffer:null,connect(){},start(){},stop(){},disconnect(){},onended:null};}};
 const a:any=new AudioTransport();a.ctx=ctx;a.buffer={duration:160};a.gain={gain};return {a,ctx,resolve,get created(){return created;}};
}
test('a suspended old start cannot restart audio after stop',async()=>{
 const f=setup(),p=f.a.play(90);f.a.stop();f.resolve();assert.equal(await p,false);assert.equal(f.created,0);assert.equal(f.a.playing,false);assert.equal(f.a.songTime(),0);
});
test('an old delayed resume cannot replace a newer attempt source or clock',async()=>{
 const f=setup(),old=f.a.play(90);f.a.stop();f.ctx.state='running';assert.equal(await f.a.play(0),true);const source=f.a.source;f.resolve();assert.equal(await old,false);assert.equal(f.a.source,source);assert.equal(f.created,1);assert.equal(f.a.songTime(),0);
});
