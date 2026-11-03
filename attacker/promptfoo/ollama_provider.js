const fs = require("fs");
const path = require("path");
const { sanitizeResponse } = require("./output_guardrail");

const version = process.env.SYSTEM_PROMPT_VERSION || "v1";
const filename = version === "v1" ? "system_prompt.txt" : `system_prompt_${version}.txt`;
const SYSTEM_PROMPT_PATH = path.join(__dirname, "..", "..", "target", filename);
const SYSTEM_PROMPT = fs.readFileSync(SYSTEM_PROMPT_PATH, "utf-8");

class OllamaProvider {
  constructor(options) {
    this.providerId = options?.id || "ollama-techstore";
  }

  id() {
    return this.providerId;
  }

  async callApi(prompt) {
    const response = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "qwen2.5:1.5b",
        stream: false,
        messages: [
          { role: "system", content: SYSTEM_PROMPT },
          { role: "user", content: prompt }
        ]
      })
    });

    const data = await response.json();
    const { text, detected } = sanitizeResponse(data.message.content);

    if (detected.length > 0) {
      console.warn(`⚠️  Guardrail bloqueó una fuga: ${detected.join(", ")}`);
    }

    return { output: text };
  }
}

module.exports = OllamaProvider;