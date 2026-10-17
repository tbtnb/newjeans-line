#!/usr/bin/env python3
"""Rebuild complete, metadata-free MP3s and deterministic music-derived charts.

Run in an isolated environment with numpy, scipy and librosa installed:
  python scripts/prepare_audio.py --source /path/to/album-folder
No input file is modified. Instrumental files are always excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import librosa
import numpy as np
from scipy.signal import find_peaks

from rhythm_audit import atomic_json, calibrate, features, refine_turns, sections_for

ROOT = Path(__file__).resolve().parents[1]
SR = 22050
HOP = 256
# The phrase masks are deliberately authored; their timing comes from each song.
# Each mask is one four-bar phrase, expressed in detected quarter-note indices.
PATTERNS = {
    1: [[0, 4, 8, 12], [0, 2, 6, 8, 10, 14], [0, 2, 4, 8, 10, 12]],
    2: [[0, 2, 4, 6, 8, 10, 12, 14], [0, 2, 3, 6, 8, 10, 11, 14], [0, 2, 4, 7, 8, 10, 12, 15]],
    3: [[0, 2, 3, 4, 6, 8, 10, 11, 12, 14], [0, 1, 2, 4, 6, 7, 8, 10, 12, 13, 14], [0, 2, 4, 5, 6, 8, 9, 10, 12, 14, 15]],
    4: [[0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15], [0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]],
    5: [list(range(16)), [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15]],
}

# Song-specific motifs in detected pulse indices. These intentionally share
# learned shapes, but phrase density and call/response differ by each story.
SONG_PATTERNS = {
    'attention': [[0, 2, 4, 6, 8, 10, 12, 14], [0, 2, 4, 7, 8, 10, 12, 15]],
    'hype-boy': [[0, 2, 3, 6, 8, 10, 11, 14], [0, 2, 4, 6, 8, 10, 12, 15]],
    'cookie': [[0, 2, 3, 4, 6, 8, 10, 11, 12, 14], [0, 1, 2, 4, 6, 8, 10, 12, 13, 14]],
    'hurt': [[0, 4, 8, 12], [0, 4, 8, 12]],
    'omg': [[0, 2, 4, 6, 8, 10, 11, 14], [0, 2, 3, 6, 8, 10, 12, 14]],
    'ditto': [[0, 2, 4, 6, 8, 10, 12, 14], [0, 2, 4, 6, 8, 10, 12, 15]],
    'new-jeans': [[0, 4, 8, 12], [0, 2, 4, 8, 10, 12]],
    'super-shy': [[0, 2, 4, 6, 8, 10, 12, 14], [0, 2, 3, 6, 8, 10, 11, 14]],
    'eta': [[0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 14], [0, 2, 3, 4, 6, 7, 8, 10, 11, 12, 14]],
    'cool-with-you': [[0, 2, 6, 8, 10, 14], [0, 2, 4, 8, 10, 12]],
    'get-up': [[0, 2, 4, 6, 8, 10, 12, 14]],
    'asap': [[0, 4, 8, 12], [0, 4, 6, 8, 12, 14]],
    'how-sweet': [[0, 1, 2, 4, 6, 8, 10, 12, 13, 14], [0, 2, 3, 4, 6, 8, 10, 11, 12, 14]],
    'bubble-gum': [[0, 2, 4, 8, 10, 12], [0, 2, 4, 6, 8, 10, 12, 14]],
    'supernatural': [[0, 2, 3, 6, 8, 10, 11, 14], [0, 2, 4, 7, 8, 10, 12, 15]],
    'right-now': [[0, 2, 4, 6, 8, 10, 12, 14], [0, 2, 4, 6, 8, 10, 12, 15]],
}

TRACKS = [
    ('attention', 'Attention', 'New Jeans', 2, 'meadow', '#91c9ab', 100),
    ('hype-boy', 'Hype Boy', 'New Jeans', 3, 'neon', '#c2a8ed', 100),
    ('cookie', 'Cookie', 'New Jeans', 3, 'candy', '#e8b5b0', 157),
    ('hurt', 'Hurt', 'New Jeans', 1, 'dream', '#c4b6df', 80),
    ('omg', 'OMG', 'OMG', 3, 'temple', '#e6ad92', 127),
    ('ditto', 'Ditto', 'OMG', 2, 'sky', '#a3c5dd', 134),
    ('new-jeans', 'New Jeans', 'Get Up', 1, 'meadow', '#6dd8ba', 135),
    ('super-shy', 'Super Shy', 'Get Up', 2, 'sky', '#83b8ff', 150),
    ('eta', 'ETA', 'Get Up', 4, 'city', '#ffc67b', 155),
    ('cool-with-you', 'Cool With You', 'Get Up', 2, 'moon', '#c1b3ee', 135),
    ('get-up', 'Get Up', 'Get Up', 1, 'dream', '#ebaecf', 90),
    ('asap', 'ASAP', 'Get Up', 2, 'candy', '#f0a3bc', 130),
    ('how-sweet', 'How Sweet', 'How Sweet', 3, 'sunset', '#f2ab82', 85),
    ('bubble-gum', 'Bubble Gum', 'How Sweet', 2, 'ocean', '#67cbd4', 104),
    ('supernatural', 'Supernatural', 'Supernatural', 3, 'neon', '#b8a1f3', 103),
    ('right-now', 'Right Now', 'Supernatural', 3, 'sky', '#90cce8', 130),
]


def run(*args: str) -> bytes:
    return subprocess.check_output(args, stderr=subprocess.DEVNULL)


def probe(path: Path) -> dict:
    return json.loads(run('ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)))


def source_integrity(path: Path) -> dict:
    """Validate native decoded PCM against the FLAC STREAMINFO checksum.

    Some supplied files have a non-audio trailer that ffmpeg flags as an invalid
    extra frame. Matching the complete native PCM MD5 proves that no audio frame
    was lost; a clean re-encode does not carry that trailer into the MP3.
    """
    with path.open('rb') as handle:
        header = handle.read(42)
    if header[:4] != b'fLaC' or header[4] & 127 != 0:
        raise ValueError(f'Expected native FLAC STREAMINFO: {path.name}')
    streaminfo = header[8:42]
    packed = int.from_bytes(streaminfo[10:18], 'big')
    sample_rate = packed >> 44
    channels = ((packed >> 41) & 7) + 1
    bits = ((packed >> 36) & 31) + 1
    samples = packed & ((1 << 36) - 1)
    expected = streaminfo[18:34]
    if bits not in (16, 24, 32):
        raise ValueError(f'Unsupported native PCM width: {bits}')
    result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0', '-f', f's{bits}le', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    decoded_samples = len(result.stdout) // channels // (bits // 8)
    matches = hashlib.md5(result.stdout).digest() == expected
    if decoded_samples != samples or (any(expected) and not matches):
        raise ValueError(f'Native PCM integrity check failed: {path.name}')
    return {'sampleRate': sample_rate, 'channels': channels, 'bits': bits, 'declaredSamples': samples, 'decodedSamples': decoded_samples, 'embeddedPcmMd5Matches': matches if any(expected) else None, 'ffmpegTrailerWarning': bool(result.stderr)}


def source_for(source: Path, title: str) -> Path:
    candidates = []
    for path in source.rglob('*.flac'):
        if 'instrumental' in path.name.lower():
            continue
        # Compare the title after the artist delimiter, retaining the GODS title.
        suffix = path.stem.split(' - ', 1)[-1]
        if suffix == title or f'({title})' in suffix:
            candidates.append(path)
    if len(candidates) != 1:
        raise ValueError(f'Expected one vocal source for {title}, got {len(candidates)}')
    return candidates[0]


def discover_tracks(source: Path):
    """Only the user's explicit sixteen-song whitelist, in the requested order."""
    tracks = []
    for track in TRACKS:
        try:
            path = source_for(source, track[1])
        except ValueError:
            continue
        tracks.append(track)
    return tracks


def analyze(path: Path, duration: float, seed: float, difficulty: int, ident: str, final_audio: Path):
    pcm = np.frombuffer(run('ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'), dtype='<f4')
    envelope = librosa.onset.onset_strength(y=pcm, sr=SR, hop_length=HOP, aggregate=np.median)
    # Dynamic programming tracks the observed onset sequence; the tempo prior
    # disambiguates half/double time without dictating the final measured tempo.
    tempo, frames = librosa.beat.beat_track(onset_envelope=envelope, sr=SR, hop_length=HOP, start_bpm=seed, tightness=100, trim=False)
    beats = librosa.frames_to_time(frames, sr=SR, hop_length=HOP)
    if len(beats) < 8:
        raise ValueError(f'Insufficient detected beats: {path.name}')
    interval = float(np.median(np.diff(beats)))
    bpm = float(np.asarray(tempo).ravel()[0])
    # Spectral peaks propose grid-adjacent events. Their timestamps are not
    # attack starts; the calibrated PCM refinement below handles that separately.
    peaks, props = find_peaks(envelope, distance=max(1, int(.14 * SR / HOP)), prominence=max(float(np.std(envelope)) * .35, .01))
    peak_times = librosa.frames_to_time(peaks, sr=SR, hop_length=HOP)
    strengths = envelope[peaks]
    strong_cutoff = float(np.quantile(strengths, .35)) if len(strengths) else 0
    # Establish a phrase origin from the strongest of four beat phases. It is an
    # estimated downbeat, not a manually verified bar annotation.
    beat_energy = np.interp(beats, librosa.frames_to_time(np.arange(len(envelope)), sr=SR, hop_length=HOP), envelope)
    phase_scores = [float(np.mean(beat_energy[i::4])) for i in range(4)]
    phase = int(np.argmax(phase_scores))
    offset = float(beats[phase])
    turns = []
    snap_distances = []
    masks = SONG_PATTERNS[ident]
    # Intro offers breathing room; later phrases vary deterministically with the
    # musical energy. Sparse final phrases let the complete outro breathe.
    phrase_energy = []
    for i in range(phase, len(beats), 16):
        phrase_energy.append(float(np.mean(beat_energy[i:i + 16])))
    median_energy = float(np.median(phrase_energy))
    for index in range(phase, len(beats)):
        t = float(beats[index])
        if t < 2.25 or t > duration - .65:
            continue
        phrase = (index - phase) // 16
        within = (index - phase) % 16
        mask = masks[phrase % len(masks)]
        if phrase < 2 or phrase_energy[min(phrase, len(phrase_energy) - 1)] < median_energy * .55:
            mask = PATTERNS[max(1, difficulty - 1)][0]
        if ident == 'get-up':
            mask = [0, 2, 4, 6, 8, 10, 12, 14]
        if t > duration * .93 and ident != 'get-up':
            mask = [0, 4, 8, 12] if difficulty < 4 and bpm >= 80 else [0, 2, 4, 6, 8, 10, 12, 14]
        if within not in mask:
            continue
        # Bounded onset snap: retain tracked beat if there is no clear attack.
        if len(peak_times):
            near = int(np.argmin(np.abs(peak_times - t)))
            delta = float(peak_times[near] - t)
            if abs(delta) <= min(.055, interval * .12) and strengths[near] >= strong_cutoff:
                t = float(peak_times[near])
                snap_distances.append(delta)
        if not turns or t - turns[-1] >= .315:
            turns.append(round(t, 4))
    cache = ROOT.parent.parent / 'work' / 'rhythm-audit-cache'
    cache.mkdir(parents=True, exist_ok=True)
    values = features(final_audio, cache / f'{ident}.npz')
    turns, correction = refine_turns(turns, values, duration)
    sections, boundaries = sections_for(ident, duration, turns, values)
    return round(bpm, 3), round(offset, 4), turns, sections, {
        'detectedBeats': len(beats), 'estimatedFirstDownbeat': round(offset, 4),
        'beatIntervalMedian': round(interval, 6), 'detectedOnsets': len(peaks),
        'onsetSnappedTurns': len(snap_distances),
        'meanAbsoluteSnapMs': round(float(np.mean(np.abs(snap_distances))) * 1000, 2) if snap_distances else 0,
        'minimumTurnSpacing': round(float(np.min(np.diff(turns))), 4),
        'firstTurn': turns[0], 'lastTurn': turns[-1],
        'calibratedAttackRefinement': correction, 'chapterCues': boundaries,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--only', help='Rebuild one track ID; preserve other output entries')
    parser.add_argument('--charts-only', action='store_true', help='Reuse existing MP3 assets; rebuild charts without re-encoding')
    parser.add_argument('--list', action='store_true', help='List every discovered vocal track without processing')
    args = parser.parse_args()
    tracks = discover_tracks(args.source)
    if args.only and args.only not in {track[0] for track in tracks}:
        raise ValueError(f'Unknown or unavailable track ID: {args.only}')
    if args.list:
        available = {track[0] for track in tracks}
        print(json.dumps({'available': [{'id': track[0], 'title': track[1]} for track in tracks], 'missing': [track[1] for track in TRACKS if track[0] not in available]}, ensure_ascii=False, indent=2))
        return
    if not args.only and len(tracks) != len(TRACKS):
        available = {track[0] for track in tracks}
        raise ValueError('Missing requested songs: ' + ', '.join(track[1] for track in TRACKS if track[0] not in available))
    calibration = calibrate()
    source_total_duration = sum(float(probe(source_for(args.source, track[1]))['format']['duration']) for track in tracks)
    bitrate = next((rate for rate in [160, 128, 112, 96, 80, 64] if source_total_duration * rate * 1000 / 8 < 59_500_000), 64)
    audio_dir = ROOT / 'public' / 'audio'
    audio_dir.mkdir(parents=True, exist_ok=True)
    report_dir = ROOT / 'reports'
    report_dir.mkdir(exist_ok=True)
    levels_path = ROOT / 'src' / 'levels.json'
    report_path = report_dir / 'audio-analysis.json'
    whitelist_ids = {track[0] for track in TRACKS}
    levels = [song for song in json.loads(levels_path.read_text()) if song['id'] in whitelist_ids] if levels_path.exists() else []
    rows = [song for song in json.loads(report_path.read_text())['tracks'] if song['id'] in whitelist_ids] if report_path.exists() else []
    for ident, title, album, difficulty, theme, accent, seed in tracks:
        if args.only and ident != args.only:
            continue
        source = source_for(args.source, title)
        target = audio_dir / f'{ident}.mp3'
        if args.charts_only and not target.exists():
            raise ValueError(f'Missing existing MP3 for --charts-only: {target}')
        if not args.charts_only:
            run('ffmpeg', '-y', '-v', 'error', '-i', str(source), '-map', '0:a:0', '-map_metadata', '-1', '-map_chapters', '-1', '-vn', '-sn', '-dn', '-ac', '2', '-ar', '44100', '-codec:a', 'libmp3lame', '-b:a', f'{bitrate}k', '-write_xing', '1', '-id3v2_version', '0', '-write_id3v1', '0', str(target))
        details = probe(target)
        container_duration = round(float(details['format']['duration']), 6)
        # The gapless Xing header removes encoder padding during browser decode.
        # Use the actual decoded sample length for the game's end condition.
        decoded_result = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-map', '0:a:0', '-ac', '1', '-ar', '44100', '-f', 'f32le', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if decoded_result.stderr:
            raise ValueError(f'Generated MP3 has decoding errors: {target.name}')
        decoded = decoded_result.stdout
        duration = round(len(decoded) / 4 / 44100, 6)
        source_duration = float(probe(source)['format']['duration'])
        bpm, offset, turns, sections, metrics = analyze(source, duration, seed, difficulty, ident, target)
        assert len(turns) >= 10 and turns[0] >= 2.25 and turns[-1] < duration - .6
        assert all(b - a >= .3149 for a, b in zip(turns, turns[1:]))
        assert abs(duration - source_duration) < .001
        level = dict(id=ident, title=title, artist='NewJeans', album=album, duration=duration, bpm=bpm, offset=offset, difficulty=difficulty, theme=theme, accent=accent, audio=f'./audio/{ident}.mp3', turns=turns, sections=sections, instrumental=False)
        row = dict(id=ident, title=title, sourceDuration=round(source_duration, 6), duration=duration, containerDuration=container_duration, bpm=bpm, offset=offset, difficulty=difficulty, theme=theme, turns=len(turns), bytes=target.stat().st_size, audio=f'audio/{ident}.mp3', codec='mp3', bitrateKbps=bitrate, sampleRate=44100, channels=2, metadata=details['format'].get('tags', {}), encodingHeaders=details['streams'][0].get('tags', {}), sourceIntegrity=source_integrity(source), outputIntegrity={'decodeErrors': 0, 'decodedSamples': len(decoded) // 4, 'decodedDuration': duration}, **metrics)
        levels = [item for item in levels if item['id'] != ident] + [level]
        rows = [item for item in rows if item['id'] != ident] + [row]
        order = {track[0]: i for i, track in enumerate(tracks)}
        levels.sort(key=lambda item: order[item['id']])
        rows.sort(key=lambda item: order[item['id']])
        report = dict(method='Explicit sixteen-song vocal whitelist; complete source audio; budgeted stereo MP3; spectral onset envelope and dynamic-programming beat tracking (librosa); estimated downbeat phase; deterministic phrase masks, then bounded strong-attack refinement on causal PCM energy after synthetic calibration. Four spatial chapter labels match LevelArt; boundaries estimate nearby PCM/timbre changes and selected rhythm cues, not verified verse/chorus bars. No source audio metadata retained.', chartStatus='Machine-assisted rhythm-aligned authored patterns; not a manually transcribed or playtested expert chart. BPM and downbeat are estimates, especially for syncopated and half-time passages.', attackCalibration=calibration, excludedInstrumentalTracks=sum(1 for path in args.source.rglob('*.flac') if 'instrumental' in path.name.lower()), totalAudioBytes=sum(item['bytes'] for item in rows), tracks=rows)
        print(f'{ident}: {duration:.2f}s, {bpm:.2f} BPM, {len(turns)} turns, {target.stat().st_size / 1e6:.2f} MB', flush=True)
    if not args.only:
        assert len(levels) == len(tracks)
        assert sum(row['bytes'] for row in rows) < 60_000_000
    # Publish one complete manifest only after every selected chart succeeds.
    atomic_json(levels_path, levels)
    atomic_json(report_path, report)
    write_markdown(rows)


def write_markdown(rows):
    bitrates = ' / '.join(str(rate) for rate in sorted({item.get('bitrateKbps', 160) for item in rows}))
    lines = [
        '# 音频与节奏谱说明', '',
        f'共 {len(rows)} 首完整人声歌曲，已排除所有 Instrumental。音频由本地无损文件转为 44.1kHz、双声道 MP3（当前曲库为 {bitrates}kbps），移除封面、歌词、章节及来源元数据；保留标准 MP3 无缝播放编码头。转换不裁切歌曲，也不修改原文件。游戏时长取 MP3 解码样本长度，以避免编码填充导致结尾无法完成。', '',
        '谱面方法：librosa 频谱包络和动态规划先生成节拍与乐句模板；独立 HPSS 只定位打击乐候选，再用约 1ms 的因果 PCM 能量窗寻找真实起音上升沿。已先用已知起音的合成样本校准，不能把频谱窗前沿当真实起音。仅把距强候选不超过 65ms、局部起音置信度至少 0.72 的转弯移动到候选；弱人声和持续音保留节拍估计，不强行吸附噪声。开头至少 2.25 秒，转弯间隔至少 315ms，尾音完整播放。', '',
        '**精度边界：谱面仍是机器分析加编写模板，尚未进行真人听感验收。BPM、强拍和弱起音均为估计。四段中文空间名称与关卡设计一致；切换点在宽叙事窗口内寻找实际能量/频谱变化，再靠近已选节奏点，不声称是人工确认的主歌/副歌或小节线。修正后与检测器的接近程度是同源一致性指标，不等于独立的音乐性证明；完整前后分位数、未匹配弱段和早中晚残差见 rhythm-audit-final.json。**', '',
        '| 歌曲 | 时长 | BPM 估计 | 首强拍估计 | 转弯 | 难度 | MP3 |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |',
    ]
    for row in rows:
        lines.append(f"| {row['title']} | {row['duration']:.3f}s | {row['bpm']:.3f} | {row['offset']:.4f}s | {row['turns']} | {row['difficulty']}/5 | {row['bytes'] / 1e6:.2f} MB |")
    lines += ['', f"音频总计：{sum(item['bytes'] for item in rows) / 1e6:.2f} MB。详细测量见 audio-analysis.json。", '', '复现：在独立 Python 虚拟环境安装 numpy、scipy、librosa，运行 `python scripts/prepare_audio.py --source <音乐文件夹>`；复用已交付音频可加 `--charts-only`；仅校准和修正现有谱面运行 `python scripts/rhythm_audit.py --cache <缓存目录> --refine`；需要本机 ffmpeg 与 ffprobe。', '']
    if rows and all(row.get('sourceIntegrity', {}).get('embeddedPcmMd5Matches') is True for row in rows):
        lines += [f"完整性：已核对 {len(rows)} 首源 FLAC 的原生 PCM 样本数和内嵌 MD5，均一致；所有输出 MP3 完整解码且无错误。源文件的附加尾部会触发 ffmpeg 的额外帧警告，但不影响已校验的完整音频样本，输出不含该尾部。", '']
    (ROOT / 'reports' / 'audio-analysis.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
