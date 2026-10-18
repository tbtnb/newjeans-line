"""Frame-vs-audio check for a ?syncprobe recording.
usage: syncan.py VIDEO H SONG.mp3 CHART.json
The probe square (bottom-left) turns white on the first rendered frame at/after each chart tap (game audio clock).
Audio track of the video is aligned to the song file per 5 s window (raw-waveform cross-correlation, +-200 ms),
then each probe flash is compared with where that tap's audio sits in the video."""
import subprocess, numpy as np, json, sys
V, H, SONG, CHART = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-vf', f'crop=16:16:4:{H-20},scale=1:1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
lum = np.frombuffer(raw, np.uint8).astype(float)
pts = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'frame=pts_time', '-of', 'csv=p=0', V], capture_output=True, text=True).stdout.split()
pts = np.array([float(x.strip(',')) for x in pts if x.strip(',')]); n = min(len(lum), len(pts)); lum, pts = lum[:n], pts[:n]
on = lum > 128; rises = pts[1:][on[1:] & ~on[:-1]]
sr = 8000
load = lambda p: np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
r, o = load(V), load(SONG)
def xc(a, b, maxlag):
    m = len(a) + len(b); c = np.fft.irfft(np.fft.rfft(a, m) * np.conj(np.fft.rfft(b, m)), m)
    lags = np.r_[np.arange(0, maxlag), np.arange(-maxlag, 0)]; v = np.r_[c[:maxlag], c[-maxlag:]]; return lags[np.argmax(v)]
def env(x): x = np.abs(x); k = len(x) // 80 * 80; e = x[:k].reshape(-1, 80).mean(1); return e - e.mean()   # 100 Hz envelope
g0 = xc(env(r[:sr * 60]), env(o[sr * 5:sr * 45]), 1500) / 100 - 5   # coarse, on a 40 s chunk away from the silent intro
a = r[int((g0 + 10) * sr):int((g0 + 30) * sr)]; b = o[10 * sr:30 * sr]; g = g0 + xc(a, b, int(0.3 * sr)) / sr
win = []
for t in np.arange(2, len(o) / sr - 6, 5.0):
    a = r[int((t + g) * sr):int((t + g + 5) * sr)]; b = o[int(t * sr):int((t + 5) * sr)]
    if len(a) < len(b): break
    win.append((t + 2.5, xc(a, b, int(0.2 * sr)) / sr))
win = np.array(win)
taps = np.array([x['t'] for x in json.load(open(CHART))['taps']])
L = np.interp(taps, win[:, 0], win[:, 1]); exp = g + taps + L
d = []
for t, e in zip(taps, exp):
    k = np.argmin(np.abs(rises - e)); dd = rises[k] - e
    if abs(dd) < 0.15: d.append((t, dd * 1000))
d = np.array(d); x = d[:, 1]
print(f'song starts at {g:.3f}s in the video; audio-vs-song residual per 5 s window: min {win[:,1].min()*1000:.0f} ms, max {win[:,1].max()*1000:.0f} ms, steps>20ms at',
      [round(win[i, 0]) for i in range(1, len(win)) if abs(win[i, 1] - win[i - 1, 1]) > 0.02])
print(f'probe flashes {len(rises)}, matched {len(d)}/{len(taps)} taps')
for lo, hi in [(0, 70), (70, 140), (140, 999)]:
    y = x[(d[:, 0] >= lo) & (d[:, 0] < hi)]
    if len(y): print(f'{lo}-{hi}s: picture minus audio median {np.median(y):.0f} ms, p10 {np.percentile(y,10):.0f}, p90 {np.percentile(y,90):.0f}, n={len(y)}')
print(f'all: median {np.median(x):.0f} ms, mean {x.mean():.0f}, p10 {np.percentile(x,10):.0f}, p90 {np.percentile(x,90):.0f}, |max| {np.abs(x).max():.0f}')
json.dump({'song_start': g, 'window_residual_s': win.tolist(), 'pairs_ms': d.tolist()}, open(V.replace('.mp4', '.sync.json'), 'w'))
