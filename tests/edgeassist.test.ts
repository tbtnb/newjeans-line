import test from 'node:test';import assert from 'node:assert/strict';
import {denseWindows,inDenseWindow,EdgeGrace} from '../src/core/edgeassist';
test('dense assistance only covers three-or-more fast taps, not isolated doubles',()=>{
 const w=denseWindows([1,1.24,2,3,3.24,3.48,4,5,5.24,5.48]);assert.equal(w.length,2);assert.ok(inDenseWindow(w,3.3));assert.ok(!inDenseWindow(w,1.2));assert.ok(!inDenseWindow(w,4));
});
test('brief edge skim survives, but excessive distance and sustained or sparse departure fail',()=>{
 const g=new EdgeGrace();assert.ok(g.survives(1,.2,true));assert.ok(g.survives(1.1,.3,true));assert.ok(!g.survives(1.13,.2,true));g.reset();assert.ok(!g.survives(2,.36,true));assert.ok(!g.survives(2,.1,false));
 g.reset();assert.ok(g.survives(3,.3,true));assert.ok(g.survives(3.05,0,true));assert.ok(g.survives(3.1,.3,true));assert.ok(g.survives(3.2,.3,true));assert.ok(!g.survives(3.23,.3,true));
});
