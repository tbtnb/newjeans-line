/** Only runs of at least three taps with <=340ms gaps receive dense-section help. */
export function denseWindows(taps:number[]):[number,number][]{
 const out:[number,number][]=[];
 for(let start=0;start<taps.length;){let end=start;while(end+1<taps.length&&taps[end+1]-taps[end]<=.34)end++;
   if(end-start>=2)out.push([taps[start]-.18,taps[end]+.18]);start=end+1;
 }return out;
}
export function inDenseWindow(windows:[number,number][],t:number){
 let lo=0,hi=windows.length-1;
 while(lo<=hi){const m=(lo+hi)>>1;if(t<windows[m][0])hi=m-1;else if(t>windows[m][1])lo=m+1;else return true;}return false;
}
export const EDGE_DISTANCE=.35, EDGE_SECONDS=.12;
/** No position correction: this only delays a wall verdict for a small, brief excursion. */
export class EdgeGrace {
 private since:number|null=null;
 reset(){this.since=null;}
 survives(t:number,distance:number,dense:boolean){
   if(distance<=1e-6){this.reset();return true;}
   if(!dense||distance>EDGE_DISTANCE+1e-6)return false;
   if(this.since===null)this.since=t;
   return t-this.since<=EDGE_SECONDS+1e-6;
 }
}
