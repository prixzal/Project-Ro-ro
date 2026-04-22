import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-8.1-full_build\bin"

import whisper
import numpy as np

print("Loading Whisper model...")
model = whisper.load_model("base.en")  # better accuracy than tiny

def transcribe(audio):
    print("Transcribing audio...")

    if audio.size == 0:
        return ""

    # 🔥 Convert int16 → float32
    audio = audio.astype(np.float32)

    # 🔥 Normalize safely
    max_val = np.max(np.abs(audio)) + 1e-6
    audio = audio / max_val

    # 🔥 Light gain (avoid distortion)
    audio = audio * 1.5

    # 🔥 Clip to valid range
    audio = np.clip(audio, -1.0, 1.0)

    # 🔥 Flatten (Whisper expects 1D)
    audio = audio.flatten()

    # ❌ DO NOT trim silence (it breaks speech continuity)

    result = model.transcribe(audio)

    return result["text"].strip()