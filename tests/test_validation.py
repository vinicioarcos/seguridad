import pandas as pd

from scripts.common import load_yaml
from scripts.validate_data import validate_frame


def base_frame():
    return pd.DataFrame(
        [
            {
                "country_code": "ECU",
                "country": "Ecuador",
                "year": 2020,
                "indicator_code": "VC.IHR.PSRC.P5",
                "indicator": "Homicidios",
                "value": 10.0,
                "unit": "por 100.000",
                "source_id": "world_bank_wdi",
            }
        ]
    )


def test_validation_blocks_negative_homicide_rate():
    frame = base_frame()
    frame.loc[0, "value"] = -1
    report = validate_frame(frame, load_yaml("config/project_config.yaml"))
    assert report["status"] == "blocked"
    assert any("negativas" in error for error in report["errors"])


def test_validation_blocks_duplicate_keys():
    frame = pd.concat([base_frame(), base_frame()], ignore_index=True)
    report = validate_frame(frame, load_yaml("config/project_config.yaml"))
    assert report["status"] == "blocked"
    assert report["duplicate_rows"] == 2
