from __future__ import annotations

import re

import yaml

from scripts.common import ROOT, utc_now, write_json

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "config/agents.yaml",
    "config/tasks.yaml",
    "config/sources.yaml",
    "docs/arquitectura_multiagente.md",
    "docs/bitacora_agentes.md",
    "docs/diccionario_datos.md",
    "data/processed/indicators.csv",
    "dashboard/public/data/indicators.json",
    "outputs/reports/informe_final.pdf",
]

MARKERS = ["[DEFINIR]", "[NOMBRES", "[URL_", "[PENDIENTE DE CITA]"]
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password)\s*=\s*[^\s]*[A-Za-z0-9]{12,}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
]


def audit() -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists() or (path.is_file() and path.stat().st_size == 0):
            errors.append(f"Falta archivo obligatorio: {relative}")

    for relative in ["README.md", "reports/informe_final.qmd"]:
        path = ROOT / relative
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in MARKERS:
                if marker in text:
                    errors.append(f"Marcador pendiente '{marker}' en {relative}")

    candidates = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "node_modules" not in path.parts
        and ".venv" not in path.parts
        and ".next" not in path.parts
        and path.stat().st_size < 1_000_000
    ]
    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"Posible credencial en {path.relative_to(ROOT)}")

    sources = yaml.safe_load((ROOT / "config/sources.yaml").read_text(encoding="utf-8"))
    used = next((item for item in sources["sources"] if item["id"] == "world_bank_wdi"), {})
    if used.get("status") != "verified":
        errors.append("La fuente world_bank_wdi no está verificada.")
    if not used.get("consultation_date"):
        errors.append("Falta fecha de consulta de world_bank_wdi.")

    return {
        "generated_at": utc_now(),
        "status": "blocked" if errors else ("approved_with_warnings" if warnings else "approved"),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> None:
    report = audit()
    write_json("outputs/logs/audit_report.json", report)
    print(f"Auditoría: {report['status']} | errores={len(report['errors'])}")
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
