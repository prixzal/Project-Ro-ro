import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("Speaking...")
    engine.say(text)
    engine.runAndWait()