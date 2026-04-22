import sounddevice as sd
import numpy as np
import queue
import threading
import time

from backend.stt import transcribe
from backend.llm import generate
from backend.tts import speak

samplerate = 16000
block_duration = 0.5  # seconds per chunk
block_size = int(samplerate * block_duration)

audio_queue = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    audio_queue.put(indata.copy())

def process_audio():
    buffer = []

    while True:
        data = audio_queue.get()
        buffer.append(data)

        # process every ~2 seconds
        if len(buffer) >= 4:
            audio = np.concatenate(buffer)
            buffer = []

            text = transcribe(audio)

            if text.strip() != "":
                print("User:", text)

                response = generate(text)
                print("AI:", response)

                # speak in separate thread (non-blocking)
                speak(response)

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