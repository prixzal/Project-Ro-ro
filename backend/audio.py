import sounddevice as sd
import numpy as np
import webrtcvad
from collections import deque
import time

vad = webrtcvad.Vad(0)  # more sensitive

def record_with_vad():
    samplerate = 16000
    frame_duration = 30  # ms
    frame_size = int(samplerate * frame_duration / 1000)

    print("Mic active... waiting for speech")

    audio_buffer = []
    pre_buffer = deque(maxlen=10)  # ~300ms

    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='int16')
    stream.start()

    try:
        speech_detected = False
        silence_counter = 0
        start_time = time.time()

        while True:
            # timeout safety
            if time.time() - start_time > 10:
                print("Timeout: no speech detected")
                break

            frame, _ = stream.read(frame_size)
            frame_bytes = frame.tobytes()

            is_speech = vad.is_speech(frame_bytes, samplerate)

            if not speech_detected:
                pre_buffer.append(frame)

            if is_speech:
                if not speech_detected:
                    print("Speech detected")
                    speech_detected = True
                    audio_buffer.extend(pre_buffer)

                audio_buffer.append(frame)
                silence_counter = 0

            else:
                if speech_detected:
                    audio_buffer.append(frame)
                    silence_counter += 1

                    # stop after ~1 sec silence
                    if silence_counter > 15:
                        break

    finally:
        stream.stop()
        stream.close()

    if len(audio_buffer) == 0:
        return np.array([])

    audio = np.concatenate(audio_buffer)
    print("Captured speech:", audio.shape)

    return audio