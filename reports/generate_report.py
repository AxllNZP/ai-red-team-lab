import yaml
from pathlib import Path
from datetime import datetime
from collections import Counter
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

REPORTS_DIR = Path(__file__).parent
FINDINGS_PATH = REPORTS_DIR / "findings.yaml"
TEMPLATE_DIR = REPORTS_DIR
OUTPUT_HTML = REPORTS_DIR / "vulnerability_report.html"
OUTPUT_PDF = REPORTS_DIR / "vulnerability_report.pdf"

MODEL_NAME = "qwen2.5:1.5b (vía Ollama)"

# Orden en el que queremos mostrar la severidad en el resumen,
# de más a menos grave (no alfabético, por eso lo definimos a mano)
SEVERITY_ORDER = ["Crítica", "Alta", "Media", "Baja"]


def load_findings():
    with open(FINDINGS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_severity_summary(findings):
    counts = Counter(f["severity"] for f in findings)
    # Solo incluimos en el resumen las severidades que realmente aparecen,
    # pero respetando el orden de gravedad definido arriba
    return {level: counts[level] for level in SEVERITY_ORDER if counts[level] > 0}


def render_html(findings, severity_summary):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("template.html")
    html = template.render(
        findings=findings,
        severity_summary=severity_summary,
        model_name=MODEL_NAME,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    return html


def render_pdf(html):
    with open(OUTPUT_PDF, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file, encoding="utf-8")
    if pisa_status.err:
        print("⚠️  Hubo errores al generar el PDF (revisa el HTML primero).")
    else:
        print(f"✅ PDF generado: {OUTPUT_PDF}")


if __name__ == "__main__":
    findings = load_findings()
    severity_summary = build_severity_summary(findings)

    html = render_html(findings, severity_summary)
    print(f"✅ HTML generado: {OUTPUT_HTML}")

    render_pdf(html)

    print(f"\nTotal de hallazgos: {len(findings)}")
    for level, count in severity_summary.items():
        print(f"  {level}: {count}")