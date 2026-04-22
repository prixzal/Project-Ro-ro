from backend.audio import record_with_vad
from backend.stt import transcribe
from backend.llm import generate
from backend.tts import speak

def main():
    audio = record_with_vad()

    text = transcribe(audio)
    print("User said:", text)

    response = generate(text)
    print("AI says:", response)

    speak(response)

if __name__ == "__main__":
    main()