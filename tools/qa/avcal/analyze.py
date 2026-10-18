import numpy as np, subprocess, sys
V = sys.argv[1]
def rises_at(x):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-vf', f'crop=16:16:{x}:4,scale=1:1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).astype(float)
pts = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'frame=pts_time', '-of', 'csv=p=0', V], capture_output=True, text=True).stdout.split()
pts = np.array([float(x.strip(',')) for x in pts if x.strip(',')])
def R(x):
    lum = rises_at(x); n = min(len(lum), len(pts)); lum, p = lum[:n], pts[:n]; on = lum > 128; return p[1:][on[1:] & ~on[:-1]]
rises = R(22); rises_ct = R(122)
sr = 8000; a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
e = np.abs(a) > 0.2; idx = np.where(e[1:] & ~e[:-1])[0] / sr
beeps = [idx[0]] if len(idx) else []
for x in idx[1:]:
    if x - beeps[-1] > 0.5: beeps.append(x)
print('heard-clock flashes', np.round(rises, 3)); print('currentTime flashes', np.round(rises_ct, 3)); print('beeps', np.round(beeps, 3))
d = [ (r - min(beeps, key=lambda b: abs(b - r))) * 1000 for r in rises ]
print('heard-flash minus beep (ms):', np.round(d), 'median', np.median(d) if d else None)
d2 = [ (r - min(beeps, key=lambda b: abs(b - r))) * 1000 for r in rises_ct ]; print('currentTime-flash minus beep (ms):', np.round(d2), 'median', np.median(d2) if d2 else None)
