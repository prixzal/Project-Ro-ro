from backend.audio import record_with_vad
from backend.stt import transcribe
from backend.llm import generate
from backend.tts import speak
from backend.stream import start_stream


def batch_mode():
    """Old mode: record once → process → respond"""
    audio = record_with_vad()

    text = transcribe(audio)
    print("User said:", text)

    response = generate(text)
    print("AI says:", response)

    speak(response)


def stream_mode():
    """New mode: real-time streaming"""
    start_stream()


if __name__ == "__main__":
    mode = "stream"  # change to "batch" if needed

    if mode == "stream":
        stream_mode()
    else:
        batch_mode()