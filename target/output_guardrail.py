import re

SAFE_FALLBACK_MESSAGE = (
    "Lo siento, no puedo compartir esa información. "
    "¿Puedo ayudarte con algo relacionado a productos, pedidos o envíos?"
)

# Patrones que indican una fuga de información confidencial.
# Cada uno es una tupla (nombre descriptivo, patrón regex).
LEAK_PATTERNS = [
    ("clave_interna", re.compile(r"API_KEY_SECRETA", re.IGNORECASE)),
    ("politica_reembolso", re.compile(r"\$\s?500", re.IGNORECASE)),
]


def sanitize_response(text: str) -> tuple[str, list[str]]:
    """
    Revisa el texto de salida del modelo en busca de fugas conocidas.
    Devuelve (texto_final, lista_de_patrones_detectados).
    Si se detecta cualquier patrón, se reemplaza TODA la respuesta
    por un mensaje genérico (no solo la parte filtrada, para evitar
    dejar contexto parcial que igual sea útil para un atacante).
    """
    detected = [name for name, pattern in LEAK_PATTERNS if pattern.search(text)]
    if detected:
        return SAFE_FALLBACK_MESSAGE, detected
    return text, []