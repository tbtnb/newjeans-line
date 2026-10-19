import test from 'node:test';import assert from 'node:assert/strict';
import {NullEngine} from '@babylonjs/core/Engines/nullEngine';
import {Scene,Mesh,Vector3,VertexData} from '../src/render/bjs';
import {trailGeometry,updateTrailMesh} from '../src/render/trailmesh';
const v=(x:number,z:number)=>new Vector3(x,.45,z);
test('ribbon bend has joined top positions and UVs, with only two external caps',()=>{
 for(const sign of [-1,1]){
  const g=trailGeometry([{a:v(0,0),b:v(0,4)},{a:v(0,4),b:v(sign*3,4)}]);
  assert.equal(g.indices.length/3,20); // two four-sided runs + two caps; no corner end wall
  const point=(i:number)=>g.positions.slice(i*3,i*3+3),uv=(i:number)=>g.uvs.slice(i*2,i*2+2);
  assert.deepEqual(point(1),point(16));assert.deepEqual(point(2),point(19));
  assert.deepEqual(uv(1),uv(16));assert.deepEqual(uv(2),uv(19));
  const n:number[]=[];VertexData.ComputeNormals(g.positions,g.indices,n);assert.equal(n[1],1);
 }
});
test('ribbon incremental growth matches full geometry without reallocating buffers',()=>{
 const e=new NullEngine(),s=new Scene(e),m=new Mesh('line',s);
 try {const r=[{a:v(0,0),b:v(0,4)},{a:v(0,4),b:v(2,4)}];updateTrailMesh(m,r);
 const buffer=m.getVertexBuffer('position');r[1].b=v(2.25,4);updateTrailMesh(m,r);
 assert.equal(m.getVertexBuffer('position'),buffer);
 const expected=trailGeometry(r),actual=m.getVerticesData('position')!;
 for(let i=0;i<actual.length;i++)assert.ok(Math.abs(actual[i]-expected.positions[i])<1e-5);
 const uv=m.getVerticesData('trailUV')!;for(let i=0;i<uv.length;i++)assert.ok(Math.abs(uv[i]-expected.uvs[i])<1e-5);
 updateTrailMesh(m,[]);assert.equal(m.isEnabled(),false);assert.equal(m.getTotalIndices(),0);
 }finally{s.dispose();e.dispose();}
});
test('a gap remains a gap rather than linking across an airborne span',()=>{
 const g=trailGeometry([{a:v(0,0),b:v(0,3)},{a:v(0,7),b:v(0,10)}]);assert.equal(g.indices.length/3,24);
});
