import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { VertexBuffer } from '@babylonjs/core/Buffers/buffer';
import { Color3 } from '@babylonjs/core/Maths/math.color';
import type { Scene } from '@babylonjs/core/scene';
import type { Material } from '@babylonjs/core/Materials/material';
import type { Point } from './types';

/** One continuous prism: the perpendicular offsets meet at exact mitered corners. */
export class RoutePrism {
  readonly mesh:Mesh;
  private readonly positions:Float32Array;
  private readonly normals:Float32Array;
  constructor(scene:Scene,name:string,private capacity:number,material:Material,topColor:string,sideColor:string) {
    this.mesh=new Mesh(name,scene);
    this.positions=new Float32Array(capacity*8*3);
    this.normals=new Float32Array(capacity*8*3);
    const colors=new Float32Array(capacity*8*4),indices:number[]=[];
    const top=Color3.FromHexString(topColor),side=Color3.FromHexString(sideColor);
    for(let i=0;i<capacity;i++)for(let k=0;k<8;k++) {
      const c=k<2?top:side;colors.set([c.r,c.g,c.b,1],(i*8+k)*4);
    }
    for(let i=0;i<capacity-1;i++)for(let face=0;face<4;face++) {
      const a=i*8+face*2,b=a+8;indices.push(a,b,a+1,a+1,b,b+1);
    }
    // End caps are always attached to the first and last (padded) cross sections.
    indices.push(0,1,2,1,3,2);
    const last=(capacity-1)*8;indices.push(last,last+2,last+1,last+1,last+2,last+3);
    const data=new VertexData();data.positions=this.positions;data.normals=this.normals;data.colors=colors;data.indices=indices;
    data.applyToMesh(this.mesh,true);this.mesh.material=material;this.mesh.isPickable=false;
    this.mesh.alwaysSelectAsActiveMesh=true;
  }
  update(points:readonly Point[],width:number,top:number,depth:number):void {
    if(points.length<2){this.mesh.setEnabled(false);return;}
    this.mesh.setEnabled(true);
    const count=Math.min(points.length,this.capacity),half=width/2;
    for(let i=0;i<this.capacity;i++) {
      const j=Math.min(i,count-1),p=points[j];
      let before=j-1,after=j+1;
      while(before>=0&&Math.hypot(p.x-points[before].x,p.z-points[before].z)<.0001)before--;
      while(after<count&&Math.hypot(p.x-points[after].x,p.z-points[after].z)<.0001)after++;
      const a=points[before>=0?before:j],b=points[after<count?after:j];
      let ax=p.x-a.x,az=p.z-a.z,bx=b.x-p.x,bz=b.z-p.z;
      const al=Math.hypot(ax,az),bl=Math.hypot(bx,bz);
      if(al){ax/=al;az/=al;}else if(bl){ax=bx/bl;az=bz/bl;}
      if(bl){bx/=bl;bz/=bl;}else{bx=ax;bz=az;}
      let nx=-az-bz,nz=ax+bx;const nl=Math.hypot(nx,nz)||1;nx/=nl;nz/=nl;
      const denominator=Math.max(.5,nx*(-bz)+nz*bx),miter=half/denominator;
      const lx=p.x+nx*miter,lz=p.z+nz*miter,rx=p.x-nx*miter,rz=p.z-nz*miter;
      const offset=i*24;
      this.positions.set([lx,top,lz,rx,top,rz,lx,top-depth,lz,rx,top-depth,rz,
        lx,top,lz,lx,top-depth,lz,rx,top-depth,rz,rx,top,rz],offset);
      this.normals.set([0,1,0,0,1,0,0,-1,0,0,-1,0,nx,0,nz,nx,0,nz,-nx,0,-nz,-nx,0,-nz],offset);
    }
    this.mesh.updateVerticesData(VertexBuffer.PositionKind,this.positions,false,false);
    this.mesh.updateVerticesData(VertexBuffer.NormalKind,this.normals,false,false);
  }
  dispose():void {this.mesh.dispose();}
}

// Native thin instances keep the supporting district to three draw calls.
import '@babylonjs/core/Meshes/thinInstanceMesh';
import { CreateBox } from '@babylonjs/core/Meshes/Builders/boxBuilder';
export class TerrainBoxes {
  readonly mesh:Mesh;
  private matrices:Float32Array;
  private count=0;
  constructor(scene:Scene,name:string,material:Material,private capacity=512) {
    this.mesh=CreateBox(name,{size:1},scene);this.mesh.material=material;this.mesh.isPickable=false;
    this.mesh.alwaysSelectAsActiveMesh=true;this.matrices=new Float32Array(capacity*16);
    this.mesh.thinInstanceSetBuffer('matrix',this.matrices,16,false);this.mesh.thinInstanceCount=0;this.mesh.setEnabled(false);
  }
  begin():void {this.count=0;}
  box(x:number,top:number,z:number,w:number,h:number,d:number):void {
    if(this.count>=this.capacity)return;const o=this.count++*16,m=this.matrices;
    m[o]=w;m[o+1]=0;m[o+2]=0;m[o+3]=0;m[o+4]=0;m[o+5]=h;m[o+6]=0;m[o+7]=0;
    m[o+8]=0;m[o+9]=0;m[o+10]=d;m[o+11]=0;m[o+12]=x;m[o+13]=top-h/2;m[o+14]=z;m[o+15]=1;
  }
  finish():void {this.mesh.thinInstanceCount=this.count;this.mesh.setEnabled(this.count>0);this.mesh.thinInstanceBufferUpdated('matrix');if(this.count)this.mesh.thinInstanceRefreshBoundingInfo();}
}
