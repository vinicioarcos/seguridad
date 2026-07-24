from __future__ import annotations

import json

import pandas as pd

from scripts.common import ROOT, assert_approved, load_yaml, project_paths, read_json, utc_now


def build_dashboard_payload(frame: pd.DataFrame, config: dict, validation: dict) -> dict:
    design = config["research_design"]
    definitions = {item["code"]: item for item in design["indicators"]}
    clean = frame.copy()
    clean["value"] = pd.to_numeric(clean["value"], errors="coerce")

    records = []
    for row in clean.itertuples(index=False):
        records.append(
            {
                "countryCode": row.country_code,
                "country": row.country,
                "year": int(row.year),
                "indicatorCode": row.indicator_code,
                "indicator": row.indicator,
                "dimension": row.dimension,
                "value": None if pd.isna(row.value) else round(float(row.value), 4),
                "unit": row.unit,
                "sourceId": row.source_id,
            }
        )

    latest_ecu = (
        clean[(clean["country_code"] == "ECU") & clean["value"].notna()]
        .sort_values("year")
        .groupby("indicator_code", as_index=False)
        .tail(1)
    )
    kpis = [
        {
            "indicatorCode": row.indicator_code,
            "label": definitions[row.indicator_code]["label"],
            "value": round(float(row.value), 2),
            "unit": row.unit,
            "year": int(row.year),
        }
        for row in latest_ecu.itertuples(index=False)
    ]

    return {
        "meta": {
            "status": "human_validated",
            "generatedAt": utc_now(),
            "title": design["title"],
            "period": [design["start_year"], design["end_year"]],
            "source": "World Development Indicators, Banco Mundial",
            "validationCoverage": validation.get("coverage"),
            "interpretationScope": design["interpretation_scope"],
        },
        "countries": [
            {"code": code, "name": design["country_names"][code]} for code in design["countries"]
        ],
        "indicators": [
            {
                "code": item["code"],
                "label": item["label"],
                "unit": item["unit"],
                "dimension": item["dimension"],
            }
            for item in design["indicators"]
        ],
        "kpis": kpis,
        "data": records,
        "interpretation": (
            "Los valores describen evolución y asociaciones. No constituyen por sí mismos "
            "evidencia causal sobre el efecto de la inseguridad."
        ),
    }


def main() -> None:
    assert_approved("validate_data")
    config = load_yaml("config/project_config.yaml")
    paths = project_paths()
    validation = read_json(paths["validation_report"])
    frame = pd.read_csv(ROOT / paths["processed_data"])
    payload = build_dashboard_payload(frame, config, validation)

    dashboard_path = ROOT / paths["dashboard_data"]
    dashboard_path.parent.mkdir(parents=True, exist_ok=True)
    dashboard_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = (
        frame.groupby(["country_code", "indicator_code"])["value"]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
    )
    summary_path = ROOT / "outputs/tables/summary.csv"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(summary_path, index=False)
    print(f"Datos del dashboard: {dashboard_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
