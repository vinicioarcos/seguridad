from scripts.clean_data import normalize_payload


def test_normalize_payload_preserves_missing_values():
    config = {
        "research_design": {
            "indicators": [
                {
                    "code": "VC.IHR.PSRC.P5",
                    "label": "Homicidios",
                    "unit": "por 100.000",
                    "dimension": "security",
                }
            ]
        }
    }
    raw = {
        "source_id": "world_bank_wdi",
        "retrieved_at": "2026-07-24T00:00:00+00:00",
        "responses": {
            "VC.IHR.PSRC.P5": [
                {"page": 1},
                [
                    {
                        "countryiso3code": "ECU",
                        "country": {"value": "Ecuador"},
                        "date": "2024",
                        "value": None,
                    }
                ],
            ]
        },
    }
    frame = normalize_payload(raw, config)
    assert len(frame) == 1
    assert bool(frame.loc[0, "is_missing"])
    assert frame.loc[0, "country_code"] == "ECU"
