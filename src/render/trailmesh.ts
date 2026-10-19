import {Mesh,Vector3,VertexData} from './bjs';
export interface TrailRun { a:Vector3; b:Vector3; }
/** One extruded ribbon. Corners share a mitred cross-section and continuous UVs;
 * there are no end faces inside a bend and no stacked/coplanar boxes. */
export function trailGeometry(runs:TrailRun[],width=1,height=.9,arcOffset=0) {
  const positions:number[]=[],normals:number[]=[],uvs:number[]=[],indices:number[]=[];
  const quad=(p:Vector3[],uv:number[],normal?:Vector3)=>{
    const n=normal??Vector3.Cross(p[1].subtract(p[0]),p[2].subtract(p[0])).normalize();
    const k=positions.length/3;for(const v of p){positions.push(v.x,v.y,v.z);normals.push(n.x,n.y,n.z);}uvs.push(...uv);indices.push(k,k+2,k+1,k,k+3,k+2);
  };
  let arc=arcOffset;
  for(let start=0;start<runs.length;){
    let end=start;while(end+1<runs.length&&Vector3.DistanceSquared(runs[end].b,runs[end+1].a)<1e-8)end++;
    const pts=[runs[start].a.clone(),...runs.slice(start,end+1).map(r=>r.b.clone())];
    const dirs=pts.slice(1).map((p,i)=>{const d=p.subtract(pts[i]);d.y=0;return d.normalize();});
    const sections:{l:Vector3;r:Vector3;s:number}[]=[];
    for(let i=0;i<pts.length;i++){
      const prev=dirs[Math.max(0,i-1)],next=dirs[Math.min(i,dirs.length-1)];
      const n0=new Vector3(prev.z,0,-prev.x),n1=new Vector3(next.z,0,-next.x);
      const denom=1+Vector3.Dot(n0,n1);const offset=denom>1e-5?n0.add(n1).scale(width*.5/denom):n1.scale(width*.5);
      const p=pts[i].clone();if(i===0)p.subtractInPlace(next.scale(width*.5));if(i===pts.length-1)p.addInPlace(prev.scale(width*.5));
      if(i>0)arc+=Vector3.Distance(pts[i-1],pts[i]);
      sections.push({l:p.subtract(offset),r:p.add(offset),s:arc});
    }
    const y=new Vector3(0,height*.5,0);
    for(let i=1;i<sections.length;i++){
      const a=sections[i-1],b=sections[i];
      quad([a.l.add(y),b.l.add(y),b.r.add(y),a.r.add(y)],[0,a.s,0,b.s,1,b.s,1,a.s],Vector3.Up());
      quad([a.r.subtract(y),b.r.subtract(y),b.l.subtract(y),a.l.subtract(y)],[1,a.s,1,b.s,0,b.s,0,a.s],Vector3.Down());
      quad([a.l.subtract(y),b.l.subtract(y),b.l.add(y),a.l.add(y)],[0,a.s,0,b.s,1,b.s,1,a.s],new Vector3(-dirs[i-1].z,0,dirs[i-1].x));
      quad([a.r.add(y),b.r.add(y),b.r.subtract(y),a.r.subtract(y)],[1,a.s,1,b.s,0,b.s,0,a.s],new Vector3(dirs[i-1].z,0,-dirs[i-1].x));
    }
    const a=sections[0],b=sections[sections.length-1];
    quad([a.r.subtract(y),a.l.subtract(y),a.l.add(y),a.r.add(y)],[1,0,0,0,0,1,1,1],dirs[0].negate());
    quad([b.l.subtract(y),b.r.subtract(y),b.r.add(y),b.l.add(y)],[0,0,1,0,1,1,0,1],dirs[dirs.length-1]);
    start=end+1;
  }
  return {positions,normals,uvs,indices};
}
const state=new WeakMap<Mesh,{count:number;arcOffset:number;first:Vector3;start:Vector3;end:Vector3;positions:Float32Array;uvs:Float32Array}>();
export function updateTrailMesh(mesh:Mesh,runs:TrailRun[],arcOffset=0){
  mesh.setEnabled(runs.length>0);if(!runs.length){mesh.setIndices([]);state.delete(mesh);return;}
  const last=runs[runs.length-1],old=state.get(mesh);
  // Between taps only the terminal cross-section moves. Keep GPU allocations and
  // all completed corners intact instead of rebuilding hundreds of boxes per frame.
  if(old&&old.arcOffset===arcOffset&&old.count===runs.length&&old.first.equals(runs[0].a)&&old.start.equals(last.a)){
    const delta=last.b.subtract(old.end),ds=Vector3.Distance(last.a,last.b)-Vector3.Distance(last.a,old.end);
    const base=old.positions.length/3-24;
    const move=(i:number)=>{old.positions[i*3]+=delta.x;old.positions[i*3+1]+=delta.y;old.positions[i*3+2]+=delta.z;old.uvs[i*2+1]+=ds;};
    for(let q=0;q<4;q++){move(base+q*4+1);move(base+q*4+2);}
    for(let i=base+20;i<base+24;i++){old.positions[i*3]+=delta.x;old.positions[i*3+1]+=delta.y;old.positions[i*3+2]+=delta.z;}
    mesh.updateVerticesData('position',old.positions,true,false);mesh.updateVerticesData('trailUV',old.uvs);old.end.copyFrom(last.b);return;
  }
  const data=trailGeometry(runs,1,.9,arcOffset),v=new VertexData();Object.assign(v,data);v.applyToMesh(mesh,true);
  const positions=Float32Array.from(data.positions),uvs=Float32Array.from(data.uvs);
  mesh.setVerticesData('trailUV',uvs,true,2);
  state.set(mesh,{count:runs.length,arcOffset,first:runs[0].a.clone(),start:last.a.clone(),end:last.b.clone(),positions,uvs});
}
