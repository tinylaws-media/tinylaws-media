"""Can a listener understand every line? Transcribe the narration with Whisper and compare it with the script.

    python3 listen.py ep004fr          # after voice.py: one line per spoken line, then the overall score

The owner's direction (28 Oct 2026): the French of the first TikTok versions was "affligeant", hard to understand,
with disjointed sentences, whatever the language this must never happen again. So every version passes this gate
before rendering: Whisper (small, multilingual, via sherpa-onnx) transcribes each line of out/<ep>_voice.wav, and the
word error rate (WER) against the written line is printed. A line above 20 % is flagged with !!; the episode passes
when the overall WER is at most 8 % and no line is flagged. Rewrite flagged lines in plainer words (shorter sentences,
no slang a voice garbles, numbers the voice says clearly), then run voice.py and listen.py again.
Numbers are compared as words (num2words), punctuation and case are ignored.

Install: pip install --break-system-packages sherpa-onnx num2words jiwer (the model, ~640 MB, comes from the
sherpa-onnx GitHub release on first use; Hugging Face is not reachable from the workspace).
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
MODEL_DIR = os.path.join(HERE, "tts", "sherpa-onnx-whisper-small")
MODEL_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2"
LINE_MAX, OVERALL_MAX = 0.20, 0.08


def ensure_model():
    if not os.path.exists(os.path.join(MODEL_DIR, "small-encoder.int8.onnx")):
        os.makedirs(os.path.dirname(MODEL_DIR), exist_ok=True)
        tb = MODEL_DIR + ".tar.bz2"
        subprocess.run(["curl", "-sSfL", "-o", tb, MODEL_URL], check=True)
        subprocess.run(["tar", "xjf", tb, "-C", os.path.dirname(MODEL_DIR)], check=True)
        os.remove(tb)


def recognizer(lang):
    import sherpa_onnx
    ensure_model()
    d = MODEL_DIR
    return sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=os.path.join(d, "small-encoder.int8.onnx"), decoder=os.path.join(d, "small-decoder.int8.onnx"),
        tokens=os.path.join(d, "small-tokens.txt"), language=lang, task="transcribe", num_threads=2)


def transcribe(rec, audio, sr):
    if sr != 16000:
        audio = signal.resample_poly(audio, 16000, sr).astype(np.float32)
    pad = np.zeros(8000, np.float32)            # half a second of silence each side: Whisper drops a final word without it
    audio = np.concatenate([pad, np.asarray(audio, np.float32), pad])
    s = rec.create_stream()
    s.accept_waveform(16000, audio)
    rec.decode_stream(s)
    return s.result.text


def norm(t, lang):
    from num2words import num2words
    t = unicodedata.normalize("NFC", t.lower().replace("’", "'"))
    t = re.sub(r"(\d)[\s  ,](?=\d{3}\b)", r"\1", t) if lang == "fr" else re.sub(r"(\d),(?=\d{3}\b)", r"\1", t)
    if lang == "fr":                              # "42e" -> "quarante-deuxième", "1er" -> "premier"
        t = re.sub(r"\b(\d+)(e|ème|er|re)\b", lambda m: " " + num2words(int(m.group(1)), lang="fr", to="ordinal") + " ", t)
    t = re.sub(r"\d+([.,]\d+)?", lambda m: " " + num2words(float(m.group(0).replace(",", ".")) if m.group(1)
                                                             else int(m.group(0)), lang=lang) + " ", t)
    units = {"fr": {"km": "kilomètres", "cm": "centimètres", "mm": "millimètres", "kg": "kilos"},
             "en": {"km": "kilometers", "cm": "centimeters", "mm": "millimeters", "kg": "kilograms"}}.get(lang, {})
    t = re.sub(r"\b(km|cm|mm|kg)\b", lambda m: units.get(m.group(1), m.group(1)), t)
    t = re.sub(r"[-'’]", " ", t)
    t = re.sub(r"[^\w\s]", " ", t)
    return " ".join(t.split())


def main(epname):
    import jiwer
    info = json.load(open(os.path.join(OUT, f"{epname}_lines.json"), encoding="utf-8"))
    lang = (info.get("lang") or "en-us")[:2]
    sr, track = wavfile.read(os.path.join(OUT, f"{epname}_voice.wav"))
    track = track.astype(np.float32) / 32768.0
    if track.ndim > 1:
        track = track.mean(axis=1)
    rec = recognizer(lang)
    errs, words, flagged, rows = 0.0, 0, 0, []
    for l in info["lines"]:
        a, b = int((l["t"] - 0.05) * sr), int((l["t"] + l["dur"] + 0.1) * sr)
        hyp = transcribe(rec, track[max(0, a):b], sr)
        ref_n, hyp_n = norm(l["text"], lang), norm(hyp, lang)
        n = max(1, len(ref_n.split()))
        w = jiwer.wer(ref_n, hyp_n) if ref_n else 0.0
        errs += w * n
        words += n
        flag = "  !!" if w > LINE_MAX else ""
        flagged += bool(flag)
        rows.append({"t": l["t"], "text": l["text"], "heard": hyp, "wer": round(w, 3)})
        print(f"{l['t']:6.2f}  {w:4.0%}{flag}  {l['text']}\n        heard: {hyp}")
    overall = errs / max(1, words)
    ok = overall <= OVERALL_MAX and flagged == 0
    print(f"\nOVERALL WER {overall:.1%} ({words} words), {flagged} line(s) over {LINE_MAX:.0%}: "
          + ("PASS" if ok else "FAIL: rewrite the flagged lines"))
    json.dump({"overall": round(overall, 4), "flagged": flagged, "pass": ok, "lines": rows},
              open(os.path.join(OUT, f"{epname}_listen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1]) else 1)
