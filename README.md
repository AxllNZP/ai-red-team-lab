# 🔴 AI Red Team Lab

Un laboratorio de AI Security Engineering donde construyo mi propio chatbot vulnerable,
lo ataco con herramientas automatizadas de red teaming para LLMs, y genero un reporte
de vulnerabilidades mapeado al **OWASP LLM Top 10** — incluyendo mitigaciones probadas
y medidas antes/después.

## 🎯 ¿Qué hace este proyecto?

El repo tiene 3 piezas que trabajan juntas:

- **`target/`** — Un chatbot de atención al cliente ("TechStore") construido con Streamlit,
  corriendo contra un modelo local vía Ollama, con un system prompt que guarda secretos
  simulados (una clave de acceso y una política interna) deliberadamente vulnerables.
- **`attacker/`** — Dos frameworks de ataque automatizado (Promptfoo y Garak) que lanzan
  decenas de técnicas de prompt injection, jailbreaks y fuga de información contra el
  chatbot, mapeadas a categorías específicas del OWASP LLM Top 10.
- **`reports/`** — Un generador de reportes en Python que consolida los hallazgos de ambas
  herramientas en un reporte legible (HTML + PDF), con severidad y mitigación recomendada
  por cada vulnerabilidad encontrada.

## 🛠️ Stack

| Parte | Herramienta |
|---|---|
| Modelo local | Ollama + `qwen2.5:1.5b` |
| App objetivo | Python + Streamlit |
| Motor de ataque | Promptfoo + Garak |
| Reporte | Python (Jinja2 + xhtml2pdf) |

## 🚀 Instalación y uso

### 1. Requisitos
- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) instalado, con el modelo descargado:ollama pull qwen2.5:1.5b


### 2. Clonar y configurar el entorno
```powershell
git clone https://github.com/AxllNZP/ai-red-team-lab.git
cd ai-red-team-lab
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Levantar el chatbot vulnerable (target)
```powershell
streamlit run target/app.py
```

### 4. Correr los ataques
```powershell
cd attacker/promptfoo
npm install -g promptfoo
npm run attack
```
Para Garak:
```powershell
pip install garak
python -m garak --target_type ollama --target_name qwen2.5:1.5b --config attacker/garak/garak_config.yaml --spec "probes.dan,probes.promptinject,probes.encoding"
```

### 5. Generar el reporte
```powershell
python reports/generate_report.py
```

## 📊 Resultados / Hallazgos destacados

Se documentaron **8 hallazgos** mapeados a OWASP LLM01 (Prompt Injection) y LLM06
(Sensitive Information Disclosure), incluyendo jailbreaks clásicos tipo DAN con hasta
**89% de tasa de éxito de ataque**, y fuga de secretos vía traducción e inyección directa.

👉 Ver el [reporte completo](reports/vulnerability_report.html) para el detalle de cada
hallazgo, evidencia y mitigación recomendada.

## 🛡️ Mitigaciones probadas

Se midió el efecto de dos mitigaciones aplicadas de forma incremental:

| Configuración | Tasa de éxito de ataque |
|---|---|
| Línea base (sin mitigaciones) | 22.5% |
| + System prompt reforzado | 35% ⚠️ (empeoró en algunos vectores) |
| + Guardrail de salida (defensa en profundidad) | **2.5%** ✅ |

Hallazgo interesante: reforzar el system prompt por sí solo **no garantiza mejora** —
en un modelo pequeño, puede incluso empeorar ciertos vectores de ataque. El guardrail
de salida (filtrado post-generación) resultó ser la mitigación más confiable.

## 📖 La historia detrás del proyecto

Soy Axell, un programador en formación. Este es mi primer proyecto enfocado en
ciberseguridad / AI Security Engineering — apenas la punta del iceberg de lo que
quiero aprender y mostrarle al mundo de lo que ahora soy capaz.

Con este proyecto aprendí cómo se vulnera una IA. Aprendí que no basta con darle
instrucciones y asumir que todo estará bien para siempre. A veces pensamos que la IA
"ya lo tiene todo resuelto", pero este proyecto demuestra lo contrario — sobre todo si
usas modelos que ya existen, como hice yo con Ollama. Da igual si es un modelo de pago
o uno entrenado por ti mismo: las principales vulnerabilidades las generamos nosotros
mismos como desarrolladores, y eso hace que los ataques dirigidos a las IA sean
sorprendentemente fáciles de ejecutar.

Por eso decidí especializarme en AI Security: para reducir ese riesgo lo más cerca
posible de cero.

## 📚 Documentación

Ver [`docs/SRS.md`](docs/SRS.md) para los requisitos funcionales completos del proyecto
(las 4 fases, incluyendo mitigaciones).

## ⚠️ Disclaimer

Este es un proyecto **educativo** de AI Security Engineering. Los secretos (`API_KEY_SECRETA`,
política de reembolsos) son completamente simulados. No usar este código ni sus patrones
de mitigación en un sistema de producción sin una revisión de seguridad adecuada.