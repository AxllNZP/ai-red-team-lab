import requests
import os
from output_guardrail import sanitize_response

_VERSION = os.environ.get("SYSTEM_PROMPT_VERSION", "v1")
_FILENAME = "system_prompt.txt" if _VERSION == "v1" else f"system_prompt_{_VERSION}.txt"
_SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), _FILENAME)

with open(_SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:1.5b"

def ask_ollama(messages):
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False}
    )
    response.raise_for_status()
    data = response.json()
    raw_text = data["message"]["content"]

    sanitized_text, detected = sanitize_response(raw_text)
    if detected:
        print(f"⚠️  Guardrail bloqueó una fuga: {detected}")

    return sanitized_text


if __name__ == "__main__":
    respuesta = ask_ollama([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hola, ¿qué productos venden?"}
    ])
    print(respuesta)