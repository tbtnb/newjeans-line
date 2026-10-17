#!/usr/bin/env python3
"""Calibrated independent final-MP3 audit and bounded chart refinement.

HPSS identifies percussion candidates; short causal PCM energy windows locate
attack starts without treating an STFT window's leading edge as a real attack.
No audio is changed. --refine writes charts only after calibration passes.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import librosa
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import correlate, find_peaks

ROOT = Path(__file__).resolve().parents[1]
SR = 22050
HOP = 128
DETECTOR_VERSION = 2


def atomic_json(path, value):
    staging = path.with_name(path.name + '.tmp')
    staging.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    staging.replace(path)


def decode(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']), dtype='<f4')


def pcm_attack_starts(y, peak_times):
    """Refine candidates on 1ms PCM energy, no centered windows or phase filter.

    A two-frame causal energy average minus the preceding eight-frame floor
    locates each rapid rise. Backtrack within 15ms to the 12%-of-rise crossing.
    Confidence is local rise/final energy; sustained/noisy passages score lower.
    """
    width = round(.001 * SR)
    dt = width / SR
    energy = np.pad(y.astype(float) ** 2, (0, (-len(y)) % width)).reshape(-1, width).mean(axis=1)
    current = (energy + np.r_[0, energy[:-1]]) / 2
    floor = np.convolve(energy, np.ones(8) / 8, 'full')[:len(energy)]
    floor = np.r_[np.zeros(2), floor[:-2]]
    rise = np.maximum(current - floor, 0)
    starts, confidence = [], []
    for t in peak_times:
        lo, hi = max(1, round((t - .045) / dt)), min(len(energy) - 1, round((t + .025) / dt))
        if hi <= lo:
            starts.append(float(t)); confidence.append(0); continue
        peak = lo + int(np.argmax(rise[lo:hi]))
        left = max(0, peak - 15)
        minimum = left + int(np.argmin(energy[left:peak + 1]))
        maximum = peak + int(np.argmax(energy[peak:min(len(energy), peak + 5)]))
        bottom, top = energy[minimum], energy[maximum]
        crossed = np.flatnonzero(energy[minimum:maximum + 1] >= bottom + (top - bottom) * .12)
        starts.append((minimum + (int(crossed[0]) if len(crossed) else 0)) * dt)
        confidence.append((top - bottom) / max(top, 1e-12))
    return np.asarray(starts), np.asarray(confidence), energy, dt


def holdout_attacks(y):
    """Held-out first-difference PCM detector; no HPSS peaks or snap inputs.

    High-frequency waveform changes emphasize sharp consonants/percussion. This
    is deliberately a different signal than the broadband energy snapper.
    """
    width = round(.001 * SR)
    dt = width / SR
    difference = np.diff(y.astype(float), prepend=y[0])
    energy = np.pad(difference ** 2, (0, (-len(difference)) % width)).reshape(-1, width).mean(axis=1)
    current = (energy + np.r_[0, energy[:-1]]) / 2
    preceding = np.convolve(energy, np.ones(8) / 8, 'full')[:len(energy)]
    preceding = np.r_[np.zeros(2), preceding[:-2]]
    rise = np.maximum(current - preceding, 0)
    scale = max(float(np.quantile(current, .95)), 1e-12)
    peaks, _ = find_peaks(rise / scale, distance=round(.08 / dt), prominence=.025, height=.035)
    starts, confidence, strengths = [], [], []
    for peak in peaks:
        left = max(0, peak - 12)
        minimum = left + int(np.argmin(energy[left:peak + 1]))
        maximum = peak + int(np.argmax(energy[peak:min(len(energy), peak + 4)]))
        bottom, top = energy[minimum], energy[maximum]
        crossed = np.flatnonzero(energy[minimum:maximum + 1] >= bottom + (top - bottom) * .20)
        starts.append((minimum + int(crossed[0] if len(crossed) else 0)) * dt)
        confidence.append((top - bottom) / max(top, 1e-12))
        strengths.append(rise[peak] / scale)
    return np.asarray(starts), np.asarray(confidence), np.asarray(strengths)


def spectral_candidates(y):
    spec = librosa.stft(y, n_fft=1024, hop_length=HOP)
    _, perc = librosa.decompose.hpss(spec, kernel_size=(31, 31), margin=(2, 2))
    mag = np.abs(perc)
    freq = librosa.fft_frequencies(sr=SR, n_fft=1024)
    band_flux = []
    for low, high in [(60, 350), (350, 2000), (2000, 10000)]:
        logged = np.log1p(mag[(freq >= low) & (freq < high)] * 100)
        flux = np.maximum(np.diff(logged, axis=1, prepend=logged[:, :1]), 0).mean(axis=0)
        band_flux.append(flux / max(np.quantile(flux, .95), 1e-7))
    envelope = gaussian_filter1d(np.maximum.reduce(band_flux), .5)
    peaks, _ = find_peaks(envelope, distance=round(.09 * SR / HOP), prominence=.18, height=.25)
    return envelope, peaks, np.asarray(band_flux)


def features(path, cache):
    fingerprint = hashlib.sha256(path.read_bytes()).hexdigest()
    if cache.exists():
        values = dict(np.load(cache))
        if int(values.get('version', 0)) == DETECTOR_VERSION and str(values.get('source_sha256', '')) == fingerprint and 'holdout_times' in values:
            return values
        if 'source_sha256' in values and str(values['source_sha256']) != fingerprint:
            values = {}
    else:
        values = {}
    y = decode(path)
    # Old spectral-only cache is usable, but never reuse its biased onset times.
    if 'peak_times' in values and 'band_flux' in values:
        envelope, peak_times, strengths, band_flux = (values[k] for k in ['envelope', 'peak_times', 'strengths', 'band_flux'])
    else:
        envelope, peaks, band_flux = spectral_candidates(y)
        peak_times, strengths = peaks * HOP / SR, envelope[peaks]
    starts, confidence, energy, dt = pcm_attack_starts(y, peak_times)
    values = dict(version=DETECTOR_VERSION, source_sha256=np.asarray(fingerprint), envelope=np.asarray(envelope, dtype='float32'), onset_times=starts, peak_times=peak_times, strengths=strengths, confidence=confidence, band_flux=np.asarray(band_flux, dtype='float32'))
    # One-second PCM/timbre summaries locate chapter changes, never lyric labels.
    seconds = np.arange(0, len(y) / SR, 1.)
    holdout_times, holdout_confidence, holdout_strengths = holdout_attacks(y)
    values.update(holdout_times=holdout_times, holdout_confidence=holdout_confidence, holdout_strengths=holdout_strengths)
    values['summary_times'] = seconds
    values['summary_rms'] = np.asarray([np.sqrt(np.mean(y[round(t * SR):min(len(y), round((t + 1) * SR))].astype(float) ** 2)) for t in seconds])
    np.savez_compressed(cache, **values)
    return values


def quantiles(values):
    return {name: round(float(value), 2) for name, value in zip(['p10', 'p25', 'median', 'p75', 'p90', 'p95'], np.quantile(values, [.1, .25, .5, .75, .9, .95]))} if len(values) else {}


def calibrate():
    """Known attacks: bass/noise bursts, varied fades, levels and sustained bed."""
    rng = np.random.default_rng(2307)
    truth = np.arange(.5, 16., .5)
    time = np.arange(round(16.5 * SR)) / SR
    y = .008 * np.sin(2 * np.pi * 233 * time)
    for index, at in enumerate(truth):
        t = np.arange(round(.16 * SR)) / SR
        fade = [.001, .004, .008][index % 3]
        env = np.minimum(t / fade, 1) * np.exp(-t / .035)
        pulse = (np.sin(2 * np.pi * [80, 190, 1100][index % 3] * t) + rng.normal(size=len(t)) * .4) * env * [.25, .6, 1][index % 3]
        start = round(at * SR)
        y[start:start + len(t)] += pulse
    _, peaks, _ = spectral_candidates(y)
    detected, confidence, _, _ = pcm_attack_starts(y, peaks * HOP / SR)
    matched = np.argmin(abs(truth[:, None] - detected[None, :]), axis=1)
    residual = (detected[matched] - truth) * 1000
    result = {'fixture': '31 known PCM burst starts; bass/mid/high tone + seeded noise; 1/4/8ms attack ramps, three levels, sustained background. No global compensation fitted.', 'events': len(truth), 'signedDetectorResidualMs': quantiles(residual), 'absoluteDetectorResidualMs': quantiles(abs(residual)), 'maximumAbsoluteErrorMs': round(float(max(abs(residual))), 3), 'matchedConfidenceMinimum': round(float(min(confidence[matched])), 4), 'passed': bool(np.quantile(abs(residual), .95) < 8 and max(abs(residual)) < 12)}
    independent, _, _ = holdout_attacks(y)
    independent_error = (independent[np.argmin(abs(truth[:, None] - independent[None, :]), axis=1)] - truth) * 1000
    result['heldOutDetector'] = {'signal': 'first-difference PCM energy; independent peaks; 20% rise crossing; never used for snapping', 'signedResidualMs': quantiles(independent_error), 'absoluteResidualMs': quantiles(abs(independent_error)), 'maximumAbsoluteErrorMs': round(float(max(abs(independent_error))), 3), 'passed': bool(np.quantile(abs(independent_error), .95) < 10)}
    result['passed'] = result['passed'] and result['heldOutDetector']['passed']
    if not result['passed']:
        raise ValueError(f'PCM attack calibration failed: {result}')
    return result


def strong_events(values):
    cutoff = np.quantile(values['strengths'], .25)
    keep = (values['strengths'] >= cutoff) & (values['confidence'] >= .72)
    return values['onset_times'][keep]


def refine_turns(turns, values, duration):
    """Only move to a nearby strong attack; never snap weak vocal/noise events."""
    events = strong_events(values)
    result, changes = [], []
    for index, original in enumerate(turns):
        event = float(events[np.argmin(abs(events - original))]) if len(events) else original
        proposal = round(event, 4) if abs(event - original) <= .065 else original
        previous = result[-1] if result else 0
        following = turns[index + 1] if index + 1 < len(turns) else duration
        if proposal < 2.25 or proposal > duration - .65 or proposal - previous < .315 or following - proposal < .315:
            proposal = original
        result.append(proposal)
        if proposal != original:
            changes.append((proposal - original) * 1000)
    return result, {'movedTurns': len(changes), 'retainedTurns': len(turns) - len(changes), 'signedChangeMs': quantiles(changes), 'maximumSnapMs': 65, 'confidenceMinimum': .72}


def chapter_labels():
    text = (ROOT / 'src/level-design.ts').read_text()
    result = {}
    for ident, chapters in re.findall(r"profile\(\{id:'([^']+)'.*?chapters:\[(.*?)\]", text):
        result[ident] = re.findall(r"'([^']+)'", chapters)
    if len(result) != 16 or any(len(v) != 4 for v in result.values()):
        raise ValueError('Expected sixteen authored four-chapter art profiles')
    return result


def sections_for(ident, duration, turns, values):
    labels = chapter_labels()[ident]
    bands = values['band_flux']
    # Compare 2s windows on either side: percussion density, frequency balance,
    # and loudness. Search only within narrative ordering windows.
    summary_t = values['summary_times']
    rms = np.log1p(values['summary_rms'] * 100)
    flux = np.asarray([np.interp(summary_t, np.arange(bands.shape[1]) * HOP / SR, band) for band in bands])
    matrix = np.vstack([rms, flux])
    matrix = (matrix - matrix.mean(axis=1, keepdims=True)) / np.maximum(matrix.std(axis=1, keepdims=True), .05)
    novelty = np.zeros(len(summary_t))
    for i in range(2, len(summary_t) - 2):
        novelty[i] = np.linalg.norm(matrix[:, i:i + 2].mean(axis=1) - matrix[:, i - 2:i].mean(axis=1))
    sections, evidence = [{'at': 0, 'label': labels[0]}], []
    # Sections are spatial stages, not claims of detected verse/chorus bars.
    for label, ratio in zip(labels[1:], [.26, .53, .78]):
        low, high = duration * (ratio - .09), duration * (ratio + .09)
        indices = np.flatnonzero((summary_t >= low) & (summary_t <= high))
        scores = novelty[indices] - abs(summary_t[indices] / duration - ratio) * 3
        second = float(summary_t[indices[int(np.argmax(scores))]])
        # Stage transitions happen at actual selected attack/beat cues if nearby.
        cues = np.asarray(turns)
        nearest = float(cues[np.argmin(abs(cues - second))])
        at = nearest if abs(nearest - second) <= 1.3 else second
        sections.append({'at': round(at, 4), 'label': label})
        evidence.append({'label': label, 'at': round(at, 4), 'noveltySecond': second, 'localChangeScore': round(float(novelty[round(second)]), 4), 'nearSelectedRhythmCue': abs(nearest - second) <= 1.3})
    return sections, evidence


def tempo_candidates(env):
    centered = env - np.mean(env)
    ac = correlate(centered, centered, method='fft', mode='full')[len(env) - 1:]
    peaks, _ = find_peaks(ac)
    peaks = [peak for peak in peaks if 55 <= 60 * SR / HOP / peak <= 200]
    return [{'bpm': round(60 * SR / HOP / peak, 2), 'normalizedAutocorrelation': round(float(ac[peak] / max(ac[0], 1e-8)), 4)} for peak in sorted(peaks, key=lambda peak: ac[peak], reverse=True)[:5]]


def holdout_audit(song, values):
    keep = (values['holdout_confidence'] >= .65) & (values['holdout_strengths'] >= np.quantile(values['holdout_strengths'], .25))
    events = values['holdout_times'][keep]
    turns = np.asarray(song['turns'])
    residual = (turns - events[np.argmin(abs(turns[:, None] - events[None, :]), axis=1)]) * 1000
    segments = []
    for name, low, high in [('early', .05, .30), ('middle', .35, .65), ('late', .70, .95)]:
        selected = residual[(turns >= low * song['duration']) & (turns < high * song['duration'])]
        matched = selected[abs(selected) <= 100]
        segments.append({'region': name, 'signedAttackResidualMs': quantiles(selected), 'matchedWithin100msSignedResidualMs': quantiles(matched), 'absoluteAttackResidualMs': quantiles(abs(selected))})
    medians = [s['matchedWithin100msSignedResidualMs'].get('median') for s in segments]
    medians = [m for m in medians if m is not None]
    return {'detector': 'Independent first-difference PCM energy, own peak detection; no HPSS candidates, no chart input, never used for snapping. >=.65 local rise confidence and strongest 75% rises. High-frequency attacks may not exist on bass-only/melodic turns.', 'detectedStrongAttacks': len(events), 'signedAttackResidualMs': quantiles(residual), 'absoluteAttackResidualMs': quantiles(abs(residual)), 'within50msPercent': round(float(np.mean(abs(residual) <= 50)) * 100, 2), 'within100msPercent': round(float(np.mean(abs(residual) <= 100)) * 100, 2), 'regionalMatchedMedianRangeMs': round(max(medians) - min(medians), 2) if medians else None, 'segments': segments}, residual


def audit(song, values):
    onset = strong_events(values)
    turns = np.asarray(song['turns'])
    nearest = np.argmin(abs(turns[:, None] - onset[None, :]), axis=1)
    delta = (turns - onset[nearest]) * 1000
    segments = []
    env = values['envelope']
    for name, low, high in [('early', .05, .30), ('middle', .35, .65), ('late', .70, .95)]:
        selection = (turns >= low * song['duration']) & (turns < high * song['duration'])
        part = delta[selection]
        matched = part[abs(part) <= 100]
        partial = env[round(low * song['duration'] * SR / HOP):round(high * song['duration'] * SR / HOP)]
        segments.append({'region': name, 'turnCount': int(sum(selection)), 'signedAttackResidualMs': quantiles(part), 'matchedWithin100msSignedResidualMs': quantiles(matched), 'absoluteAttackResidualMs': quantiles(abs(part)), 'within50msPercent': round(float(np.mean(abs(part) <= 50)) * 100, 2) if len(part) else None, 'tempoCandidates': tempo_candidates(partial)})
    regional_medians = [r['matchedWithin100msSignedResidualMs'].get('median') for r in segments]
    usable = [x for x in regional_medians if x is not None]
    return {'id': song['id'], 'title': song['title'], 'chartBpm': song['bpm'], 'turnCount': len(turns), 'detectedPercussiveCandidates': len(values['onset_times']), 'confidentAttacks': len(onset), 'signedAttackResidualMs': quantiles(delta), 'absoluteAttackResidualMs': quantiles(abs(delta)), 'within50msPercent': round(float(np.mean(abs(delta) <= 50)) * 100, 2), 'within100msPercent': round(float(np.mean(abs(delta) <= 100)) * 100, 2), 'unmatchedOver100msTurns': int(sum(abs(delta) > 100)), 'regionalMatchedMedianRangeMs': round(max(usable) - min(usable), 2) if usable else None, 'segments': segments}, delta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--only')
    parser.add_argument('--refine', action='store_true')
    parser.add_argument('--baseline', type=Path, help='Compare original chart snapshot to the delivered chart; counts may differ')
    args = parser.parse_args()
    calibration = calibrate()
    print('Calibration:', calibration, flush=True)
    path = ROOT / 'src/levels.json'
    levels = json.loads(path.read_text())
    baseline = {song['id']: song for song in json.loads(args.baseline.read_text())} if args.baseline else {}
    rows, all_before, all_after, held_before, held_after = [], [], [], [], []
    args.cache.mkdir(parents=True, exist_ok=True)
    for song in levels:
        if args.only and song['id'] != args.only:
            continue
        values = features(ROOT / 'public' / song['audio'].removeprefix('./'), args.cache / f"{song['id']}.npz")
        before, residual = audit(baseline.get(song['id'], song), values)
        all_before.extend(residual.tolist())
        change = None
        if args.refine:
            song['turns'], change = refine_turns(song['turns'], values, song['duration'])
            song['sections'], boundaries = sections_for(song['id'], song['duration'], song['turns'], values)
            change['chapterCues'] = boundaries
        after, residual = audit(song, values)
        all_after.extend(residual.tolist())
        independent_before, independent_residual = holdout_audit(baseline.get(song['id'], song), values)
        held_before.extend(independent_residual.tolist())
        independent_after, independent_residual = holdout_audit(song, values)
        held_after.extend(independent_residual.tolist())
        rows.append({'before': before, 'after': after, 'refinement': change, 'heldOutBefore': independent_before, 'heldOutAfter': independent_after})
        print(song['id'], 'median', before['signedAttackResidualMs']['median'], '->', after['signedAttackResidualMs']['median'], 'p90', before['absoluteAttackResidualMs']['p90'], '->', after['absoluteAttackResidualMs']['p90'], 'moved', change['movedTurns'] if change else 0, flush=True)
    def overall(values):
        values = np.asarray(values)
        return {'signedAttackResidualMs': quantiles(values), 'absoluteAttackResidualMs': quantiles(abs(values)), 'within50msPercent': round(float(np.mean(abs(values) <= 50)) * 100, 2), 'within100msPercent': round(float(np.mean(abs(values) <= 100)) * 100, 2)}
    report = {'method': 'Final decoded MP3; independent HPSS multiband spectral candidate detection (1024/128), then causal ~1ms PCM energy attack-start refinement. Strong events require upper 75% spectral strength and >=0.72 local energy-rise confidence. Calibration uses known PCM starts and applies no fitted global correction. Signed residual = chart minus nearest strong attack. Snap bounded to 65ms and minimum 315ms spacing. Unmatched weak passages retain their beat-derived timing.', 'limitations': 'Nearest percussion proximity is not perceptual beat correctness. Dense syncopation can make event identity ambiguous. Slow vocal ramps and weak/sustained music do not provide precise physical attack ground truth; unmatched turns remain estimates. Same detector guides refinement and after measurement, so improved proximity is a consistency metric, not independent proof. No human listening/playtest claim. Chapter cues estimate PCM/timbre changes within broad story windows, not manual bar/verse annotations. Tempo autocorrelation can contain half/double and syncopated pulses.', 'chartsMutated': args.refine, 'baselineChartSnapshot': str(args.baseline) if args.baseline else None, 'beforeAfterCountsMayDiffer': bool(args.baseline), 'calibration': calibration, 'before': overall(all_before), 'after': overall(all_after), 'heldOutBefore': overall(held_before), 'heldOutAfter': overall(held_after), 'tracks': rows}
    report['chartSha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    report['finalTurnCount'] = sum(row['after']['turnCount'] for row in rows)
    report['baselineTurnCount'] = sum(row['before']['turnCount'] for row in rows)
    report['chartGeneration'] = 'Song-specific masks and bounded attack snaps. Original/final turn counts may differ; comparison is between distributions, not matched event pairs.'
    audio_report = json.loads((ROOT / 'reports/audio-analysis.json').read_text())
    report['outputAudioBytes'] = audio_report['totalAudioBytes']
    generated = {row['id']: row for row in audio_report['tracks']}
    for row in rows:
        generation = generated.get(row['after']['id'], {})
        row['generationRefinement'] = generation.get('calibratedAttackRefinement')
        row['chapterCues'] = generation.get('chapterCues')
    destination = ROOT / 'reports' / ('rhythm-audit-final.json' if not args.only else f'rhythm-audit-{args.only}-calibrated.json')
    if args.refine:
        atomic_json(path, levels)
        report['chartSha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    atomic_json(destination, report)


if __name__ == '__main__':
    main()
