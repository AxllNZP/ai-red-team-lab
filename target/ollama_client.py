import os
import requests

# Cargar el system prompt de forma dinámica desde system_prompt.txt
_SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
with open(_SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:1.5b"

def ask_ollama(messages):
    """
    messages: lista de dicts tipo [{"role": "user", "content": "..."}]
    Devuelve el texto de la respuesta del modelo.
    """
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False
        }
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]


if __name__ == "__main__":
    respuesta = ask_ollama([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hola, ¿qué productos venden?"}
    ])
    print(respuesta)