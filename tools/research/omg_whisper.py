import json, sys, time
from faster_whisper import WhisperModel
name = sys.argv[1]
m = WhisperModel(name, device='cpu', compute_type='int8', cpu_threads=6)
t = time.time()
prompt = "이 노래는 it's about you, baby. Oh my, oh my God, 예상했어 나. I was really hoping that he will come through. They keep on asking me, who is he?"
import soundfile as sf; A = sf.read('omg-vocals-16k.wav', dtype='float32')[0]
segs, info = m.transcribe(A, language='ko', word_timestamps=True, vad_filter=False, initial_prompt=prompt, condition_on_previous_text=False, beam_size=5)
out = []
for s in segs:
    out.append({'start': s.start, 'end': s.end, 'text': s.text, 'words': [{'w': w.word, 's': w.start, 'e': w.end, 'p': w.probability} for w in s.words]})
    print(f'{s.start:7.2f} {s.end:7.2f} {s.text}', flush=True)
json.dump(out, open(f'whisper-{name}.json', 'w'), ensure_ascii=False, indent=0)
print('took', time.time() - t)
