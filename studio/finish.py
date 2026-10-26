"""Mux an episode: python3 finish.py ep001 TinyLaws_001_SquareCube
Measures the soundtrack, normalises it to -14 LUFS (true peak -1.5 dB) and encodes a
platform-ready MP4 (H.264, ~10 Mb/s max, AAC 192k) plus a thumbnail at the law card."""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def measure(wav):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))


def main(ep, name, thumb_t=None):
    video = os.path.join(OUT, f"{ep}_video.mp4")
    wav = os.path.join(OUT, f"{ep}_audio.wav")
    m = measure(wav)
    # one static gain to -14 LUFS, then a gentle peak limiter (no dynamic loudness riding,
    # which would pump the music and drag the effects up in quiet moments)
    gain = -14.0 - float(m["input_i"])
    limit = 10 ** (-2.0 / 20)
    af = (f"volume={gain:.2f}dB,alimiter=limit={limit:.4f}:attack=5:release=60:level=false,"
          "aresample=48000")
    dst = os.path.join(OUT, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", video, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-af", af,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "10M", "-bufsize", "20M",
                    "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", dst], check=True)
    if thumb_t is not None:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(thumb_t), "-i", video,
                        "-frames:v", "1", os.path.join(OUT, f"{name}_thumbnail.png")], check=True)
    print("wrote", dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else None)
