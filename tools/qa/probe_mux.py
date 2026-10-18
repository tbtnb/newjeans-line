"""Mux the song onto a silent ?syncprobe recording (e.g. Playwright GPU capture) so picture and music line up.
usage: probe_mux.py VIDEO H SONG.mp3 CHART.json OUT.mp4
Finds the constant shift s that best maps chart tap times onto probe-flash times (flash = first rendered frame at/after
each tap on the game's audio clock), places the song at video time s, and hides the probe square."""
import subprocess, numpy as np, json, sys
V, H, SONG, CHART, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-vf', f'crop=16:16:4:{H-20},scale=1:1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
lum = np.frombuffer(raw, np.uint8).astype(float)
pts = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'frame=pts_time', '-of', 'csv=p=0', V], capture_output=True, text=True).stdout.split()
pts = np.array([float(x.strip(',')) for x in pts if x.strip(',')]); n = min(len(lum), len(pts)); lum, pts = lum[:n], pts[:n]
on = lum > 128; rises = pts[1:][on[1:] & ~on[:-1]]
taps = np.array([x['t'] for x in json.load(open(CHART))['taps']])
def resid(s):
    e = taps + s; i = np.clip(np.searchsorted(rises, e), 1, len(rises) - 1)
    return np.median(np.minimum(np.abs(rises[i] - e), np.abs(rises[i - 1] - e)))
coarse = min((resid(s), s) for s in np.arange(0, pts[-1] - taps[-1], 0.01))[1]
r, s = min((resid(s), s) for s in np.arange(coarse - 0.05, coarse + 0.05, 0.001))
# flashes land on the first frame AT/AFTER the tap, so on average half a frame late: correct by half the frame interval
fi = np.median(np.diff(pts)); s0 = s - fi / 2
print(json.dumps({ 'flashes': int(len(rises)), 'shift_s': round(float(s), 4), 'frame_ms': round(float(fi) * 1000, 1), 'median_resid_ms': round(float(r) * 1000, 1), 'song_at_s': round(float(s0), 4) }))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', V, '-itsoffset', f'{s0:.4f}', '-i', SONG, '-map', '0:v', '-map', '1:a',
  '-vf', f'delogo=x=1:y={H-31}:w=30:h=30,fps=30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', OUT], check=True)
