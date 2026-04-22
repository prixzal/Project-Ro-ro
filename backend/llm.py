def generate(text):
    text = text.lower()

    print(f"LLM received: {text}")

    if "hello" in text or "hi" in text:
        return "Hello! How can I help you?"

    elif "your name" in text:
        return "I am Roro, your personal AI assistant."

    elif "time" in text:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        return f"The time is {now}"

    elif "bye" in text:
        return "Goodbye! See you soon."

    elif text.strip() == "":
        return "I didn't catch that clearly."

    else:
        return "I understood something, but I am still learning."