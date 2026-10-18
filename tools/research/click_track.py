"""Mix a short click at every tap time into the song so a human can hear chart/audio alignment.
Decode = ffmpeg gapless (identical to Chrome decodeAudioData, verified sample-exact). Click: 20 ms 2.5 kHz tick
with a 1 ms attack, so its start is the tap time. Usage: click_track.py <audio.mp3> <chart.json> <out.mp3>"""
import sys, json, subprocess, numpy as np
src, chart, out = sys.argv[1:4]; SR = 44100
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
y = np.frombuffer(raw, np.float32).reshape(-1, 2).copy() * 0.75
n = int(0.02 * SR); tt = np.arange(n) / SR
click = (np.sin(2 * np.pi * 2500 * tt) + 0.5 * np.sin(2 * np.pi * 5000 * tt)) * np.minimum(1, tt / 0.001) * np.exp(-tt / 0.006) * 0.55
for x in json.load(open(chart))['taps']:
    i = int(round(x['t'] * SR))
    if 0 <= i < len(y) - n: y[i:i + n] += click[:, None]
y = np.clip(y, -1, 1)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-', '-c:a', 'libmp3lame', '-b:a', '192k', out], input=y.astype(np.float32).tobytes(), check=True)
print(out, len(json.load(open(chart))['taps']), 'clicks')
