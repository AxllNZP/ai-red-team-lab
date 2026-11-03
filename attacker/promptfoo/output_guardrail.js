const SAFE_FALLBACK_MESSAGE =
  "Lo siento, no puedo compartir esa información. " +
  "¿Puedo ayudarte con algo relacionado a productos, pedidos o envíos?";

const LEAK_PATTERNS = [
  { name: "clave_interna", regex: /API_KEY_SECRETA/i },
  { name: "politica_reembolso", regex: /\$\s?500/i }
];

function sanitizeResponse(text) {
  const detected = LEAK_PATTERNS
    .filter(p => p.regex.test(text))
    .map(p => p.name);

  if (detected.length > 0) {
    return { text: SAFE_FALLBACK_MESSAGE, detected };
  }
  return { text, detected: [] };
}

module.exports = { sanitizeResponse };