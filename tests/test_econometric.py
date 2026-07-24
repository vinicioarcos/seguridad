import pandas as pd

from scripts.econometric_model import SAFE_NAMES, estimate_models


def test_econometric_models_are_labeled_non_causal():
    rows = []
    countries = ["ECU", "COL", "PER", "CRI"]
    codes = list(SAFE_NAMES)
    for country_index, country in enumerate(countries):
        for year in range(2014, 2024):
            values = {
                "VC.IHR.PSRC.P5": 5 + country_index * 2 + (year - 2014) * 0.4,
                "NY.GDP.MKTP.KD.ZG": 4 - country_index * 0.2 - (year - 2014) * 0.05,
                "NE.GDI.FTOT.ZS": 20 - country_index * 0.3,
                "BX.KLT.DINV.WD.GD.ZS": 3 - country_index * 0.1,
            }
            for code in codes:
                rows.append(
                    {
                        "country_code": country,
                        "country": country,
                        "year": year,
                        "indicator_code": code,
                        "value": values[code],
                    }
                )
    result = estimate_models(pd.DataFrame(rows))
    estimated = [model for model in result["models"] if model["status"] == "estimated_non_causal"]
    assert estimated
    assert all("no identifica efecto causal" in model["interpretation_guardrail"] for model in estimated)
