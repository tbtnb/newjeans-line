/** requestAnimationFrame is the refresh source; never synthesize 120 frames with a timer. */
export class FramePacer {
  private last = -Infinity;
  reset(){this.last=-Infinity;}
  due(now:number,target:60|120){
    // High-refresh mode must not halve jittery 120-Hz callback streams.
    if(target===120){this.last=now;return true;}
    const interval=1000/target,elapsed=now-this.last;
    if(elapsed<interval-.75)return false;
    this.last=Number.isFinite(this.last)&&elapsed<interval*2 ? now-(elapsed%interval<.75?elapsed%interval:0) : now;
    return true;
  }
}
