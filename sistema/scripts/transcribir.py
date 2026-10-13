import glob, os, json
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
for f in sorted(glob.glob("sistema/transcribir/*.mp3")):
    out = f[:-4] + ".txt"
    if os.path.exists(out):
        continue
    segs, info = model.transcribe(f, word_timestamps=True)
    lines = [f"# idioma: {info.language}"]
    words = []
    for s in segs:
        lines.append(f"[{s.start:6.2f} - {s.end:6.2f}] {s.text.strip()}")
        for w in (s.words or []):
            words.append({"start": round(w.start, 2), "end": round(w.end, 2), "word": w.word})
    open(out, "w").write("\n".join(lines) + "\n")
    json.dump(words, open(f[:-4] + "_palabras.json", "w"), ensure_ascii=False, indent=0)
    print("ok", f)
