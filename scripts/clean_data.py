from __future__ import annotations

import pandas as pd

from scripts.common import load_yaml, project_paths, read_json


def normalize_payload(raw: dict, config: dict) -> pd.DataFrame:
    design = config["research_design"]
    definitions = {item["code"]: item for item in design["indicators"]}
    records: list[dict] = []

    for indicator_code, payload in raw["responses"].items():
        definition = definitions[indicator_code]
        for item in payload[1]:
            value = item.get("value")
            records.append(
                {
                    "country_code": item.get("countryiso3code"),
                    "country": (item.get("country") or {}).get("value"),
                    "year": int(item["date"]),
                    "indicator_code": indicator_code,
                    "indicator": definition["label"],
                    "dimension": definition["dimension"],
                    "value": value,
                    "unit": definition["unit"],
                    "source_id": raw["source_id"],
                    "retrieved_at": raw["retrieved_at"],
                    "is_missing": value is None,
                    "is_outlier": False,
                }
            )

    columns = [
        "country_code",
        "country",
        "year",
        "indicator_code",
        "indicator",
        "dimension",
        "value",
        "unit",
        "source_id",
        "retrieved_at",
        "is_missing",
        "is_outlier",
    ]
    frame = pd.DataFrame(records, columns=columns)
    if frame.empty:
        raise RuntimeError("La descarga no contiene observaciones.")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    frame["is_missing"] = frame["value"].isna()
    return frame.sort_values(["indicator_code", "country_code", "year"]).reset_index(drop=True)


def main() -> None:
    config = load_yaml("config/project_config.yaml")
    paths = project_paths()
    raw = read_json(paths["raw_data"])
    frame = normalize_payload(raw, config)
    output = __import__("pathlib").Path(__file__).resolve().parents[1] / paths["processed_data"]
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    print(f"Base procesada: {output.relative_to(output.parents[2])} ({len(frame)} filas)")


if __name__ == "__main__":
    main()
