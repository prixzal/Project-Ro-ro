from llama_cpp import Llama

# =========================
# LOAD MODEL
# =========================
llm = Llama(
    model_path="models/tinyllama.gguf",
    n_ctx=2048,
    n_threads=4
)

# =========================
# MEMORY
# =========================
conversation_history = []
MAX_MEMORY = 6  # last few turns


def generate(text):
    global conversation_history

    print(f"LLM received: {text}")

    # 🔥 Add user input to memory
    conversation_history.append(f"User: {text}")

    # keep memory small
    if len(conversation_history) > MAX_MEMORY:
        conversation_history = conversation_history[-MAX_MEMORY:]

    # 🔥 Build context
    context = "\n".join(conversation_history)

    # 🔥 SYSTEM PROMPT
    prompt = f"""
You are Roro, a real-time call assistant.

Context of conversation:
{context}

Rules:
- Only respond if helpful
- Keep answers short
- If no response needed, reply: NONE

Assistant:
"""

    output = llm(
        prompt,
        max_tokens=80,
        stop=["User:", "\n\n"]
    )

    response = output["choices"][0]["text"].strip()

    # 🔥 Control silence
    if response.upper().startswith("NONE"):
        return None

    # 🔥 Save AI response to memory
    conversation_history.append(f"Assistant: {response}")

    return response