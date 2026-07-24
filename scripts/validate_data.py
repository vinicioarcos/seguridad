from __future__ import annotations

import pandas as pd

from scripts.common import ROOT, load_yaml, project_paths, utc_now, write_json

REQUIRED_COLUMNS = {
    "country_code",
    "country",
    "year",
    "indicator_code",
    "indicator",
    "value",
    "unit",
    "source_id",
}


def validate_frame(frame: pd.DataFrame, config: dict) -> dict:
    design = config["research_design"]
    expected_countries = set(design["countries"])
    expected_indicators = {item["code"] for item in design["indicators"]}
    expected_years = int(design["end_year"]) - int(design["start_year"]) + 1
    expected_rows = len(expected_countries) * len(expected_indicators) * expected_years

    errors: list[str] = []
    warnings: list[str] = []
    missing_columns = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing_columns:
        errors.append(f"Columnas faltantes: {missing_columns}")
        return {"status": "blocked", "errors": errors, "warnings": warnings}

    duplicate_count = int(
        frame.duplicated(["country_code", "year", "indicator_code"], keep=False).sum()
    )
    if duplicate_count:
        errors.append(f"{duplicate_count} filas participan en claves duplicadas.")

    unexpected_countries = sorted(set(frame["country_code"].dropna()) - expected_countries)
    unexpected_indicators = sorted(set(frame["indicator_code"].dropna()) - expected_indicators)
    if unexpected_countries:
        errors.append(f"Países inesperados: {unexpected_countries}")
    if unexpected_indicators:
        errors.append(f"Indicadores inesperados: {unexpected_indicators}")

    homicide_code = design["security_indicator"]
    negative_homicides = int(
        (
            (frame["indicator_code"] == homicide_code)
            & frame["value"].notna()
            & (frame["value"] < 0)
        ).sum()
    )
    if negative_homicides:
        errors.append(f"{negative_homicides} tasas de homicidio son negativas.")

    missing_count = int(frame["value"].isna().sum())
    coverage = 0 if expected_rows == 0 else (expected_rows - missing_count) / expected_rows
    if missing_count:
        warnings.append(f"{missing_count} valores faltantes; no fueron imputados.")
    if coverage < float(config["quality"]["minimum_country_year_coverage"]):
        warnings.append(
            f"Cobertura global {coverage:.1%}, inferior al umbral "
            f"{config['quality']['minimum_country_year_coverage']:.0%}."
        )

    return {
        "status": "blocked" if errors else "review_required",
        "generated_at": utc_now(),
        "rows": int(len(frame)),
        "expected_rows": expected_rows,
        "coverage": round(coverage, 4),
        "missing_values": missing_count,
        "duplicate_rows": duplicate_count,
        "errors": errors,
        "warnings": warnings,
        "decision": "Requiere aprobación humana incluso cuando no existan errores críticos.",
    }


def main() -> None:
    config = load_yaml("config/project_config.yaml")
    paths = project_paths()
    frame = pd.read_csv(ROOT / paths["processed_data"])
    report = validate_frame(frame, config)
    write_json(paths["validation_report"], report)
    print(f"Validación: {report['status']} | errores={len(report['errors'])}")
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
