import pyttsx3
import queue
import threading

tts_queue = queue.Queue()

def tts_worker():
    engine = pyttsx3.init()  # 🔥 create engine INSIDE thread

    while True:
        text = tts_queue.get()

        if text is None:
            break

        try:
            print("Speaking:", text)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("TTS Error:", e)

        tts_queue.task_done()


# start worker ONCE
threading.Thread(target=tts_worker, daemon=True).start()


def speak(text):
    # avoid flooding
    if text and text.strip():
        tts_queue.put(text)