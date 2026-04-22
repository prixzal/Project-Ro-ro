import sounddevice as sd
import numpy as np
import queue
import time

from backend.stt import transcribe
from backend.llm import generate
from backend.tts import speak

# =========================
# CONFIG
# =========================
samplerate = 16000
block_duration = 0.5
block_size = int(samplerate * block_duration)

audio_queue = queue.Queue()

# =========================
# STATE
# =========================
is_speaking = False
last_text = ""
last_time = 0


# =========================
# AUDIO INPUT
# =========================
def audio_callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy())


# =========================
# PIPELINE STAGES
# =========================
def should_process(text):
    text = text.strip().lower()

    if not text:
        return False

    # remove garbage
    if len(text.split()) < 2:
        return False

    return True


def should_respond(text):
    # trigger word (can change later)
    if "roro" in text.lower():
        return True

    return False


# =========================
# MAIN PROCESS LOOP
# =========================
def process_audio():
    global is_speaking, last_text, last_time

    buffer = []

    while True:
        data = audio_queue.get()
        buffer.append(data)

        # process ~2 sec chunks
        if len(buffer) >= 4:
            audio = np.concatenate(buffer)
            buffer = []

            # 🔥 prevent self-loop
            if is_speaking:
                continue

            # ===== STT =====
            text = transcribe(audio)
            print("RAW:", text)

            # ===== VALIDATION =====
            if not should_process(text):
                continue

            # prevent repeats
            if text.lower() == last_text:
                continue

            # cooldown
            if time.time() - last_time < 1:
                continue

            last_text = text.lower()
            last_time = time.time()

            print("User:", text)

            # ===== DECISION =====
            if not should_respond(text):
                print("AI: (ignored)")
                continue

            # ===== LLM =====
            response = generate(text)

            if not response:
                print("AI: (no response)")
                continue

            print("AI:", response)

            # ===== OUTPUT =====
            is_speaking = True
            speak(response)
            time.sleep(1.2)
            is_speaking = False


# =========================
# ENTRY
# =========================
def start_stream():
    print("Starting real-time assistant...")

    stream = sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype='int16',
        blocksize=block_size,
        callback=audio_callback
    )

    with stream:
        process_audio()