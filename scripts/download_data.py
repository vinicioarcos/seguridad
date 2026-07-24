from __future__ import annotations

import os
from typing import Any

import requests

from scripts.common import (
    assert_approved,
    load_yaml,
    project_paths,
    source_by_id,
    utc_now,
    write_json,
)


def fetch_indicator(
    api_base: str,
    countries: list[str],
    indicator_code: str,
    start_year: int,
    end_year: int,
) -> list[Any]:
    country_path = ";".join(countries)
    url = f"{api_base}/country/{country_path}/indicator/{indicator_code}"
    response = requests.get(
        url,
        params={"date": f"{start_year}:{end_year}", "format": "json", "per_page": 20000},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        raise RuntimeError(f"Respuesta inesperada para {indicator_code}")
    return payload


def main() -> None:
    assert_approved("approve_design")
    assert_approved("identify_sources")
    source = source_by_id("world_bank_wdi")
    if source.get("status") != "verified":
        raise RuntimeError("La fuente world_bank_wdi debe cambiar a status: verified.")

    config = load_yaml("config/project_config.yaml")
    design = config["research_design"]
    paths = project_paths()
    api_base = os.getenv("WORLD_BANK_API_BASE", source["url"]).rstrip("/")
    retrieved_at = utc_now()

    responses: dict[str, Any] = {}
    for indicator in design["indicators"]:
        code = indicator["code"]
        responses[code] = fetch_indicator(
            api_base,
            design["countries"],
            code,
            int(design["start_year"]),
            int(design["end_year"]),
        )

    write_json(
        paths["raw_data"],
        {
            "source_id": "world_bank_wdi",
            "retrieved_at": retrieved_at,
            "request": {
                "countries": design["countries"],
                "start_year": design["start_year"],
                "end_year": design["end_year"],
                "indicators": [item["code"] for item in design["indicators"]],
            },
            "responses": responses,
        },
    )
    write_json(
        paths["metadata"],
        {
            "source_id": "world_bank_wdi",
            "source_url": api_base,
            "retrieved_at": retrieved_at,
            "countries": design["countries"],
            "period": [design["start_year"], design["end_year"]],
            "indicator_codes": list(responses),
            "raw_file": paths["raw_data"],
            "transformations": [],
        },
    )
    print(f"Descarga completada: {paths['raw_data']}")


if __name__ == "__main__":
    main()
