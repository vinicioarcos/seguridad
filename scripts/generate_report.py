from __future__ import annotations

import os
import shutil
import subprocess
import sys

from scripts.common import ROOT, assert_approved


def main() -> None:
    assert_approved("calculate_indicators")
    assert_approved("estimate_model")
    quarto = shutil.which("quarto")
    if not quarto:
        raise RuntimeError(
            "Quarto no está instalado. Instálelo desde https://quarto.org."
        )
    output_dir = ROOT / "outputs/reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env.setdefault("QUARTO_PYTHON", sys.executable)

    # Se usa el motor Typst (no LaTeX): este proyecto no asume una
    # distribución LaTeX instalada; Typst ya viene con Quarto y produce PDF
    # directamente. Requiere que `_quarto.yml` exista en la raíz del
    # repositorio para que Typst resuelva rutas como references/references.bib.
    subprocess.run(
        [
            quarto,
            "render",
            str(ROOT / "reports/informe_final.qmd"),
            "--to",
            "typst",
        ],
        cwd=ROOT,
        check=True,
        env=env,
    )

    rendered = ROOT / "reports/informe_final.pdf"
    intermediate = ROOT / "reports/informe_final.typ"
    if not rendered.exists():
        raise RuntimeError(f"Quarto no generó {rendered}")
    final_path = output_dir / "informe_final.pdf"
    shutil.move(str(rendered), str(final_path))
    intermediate.unlink(missing_ok=True)
    print(f"Informe generado en {final_path}")


if __name__ == "__main__":
    main()
