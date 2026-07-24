from __future__ import annotations

import math

import pandas as pd
import statsmodels.formula.api as smf

from scripts.common import ROOT, assert_approved, load_yaml, project_paths, utc_now, write_json

SAFE_NAMES = {
    "VC.IHR.PSRC.P5": "homicide_rate",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "NE.GDI.FTOT.ZS": "fixed_capital",
    "BX.KLT.DINV.WD.GD.ZS": "fdi_gdp",
}


def _finite(value: float) -> float | None:
    return round(float(value), 6) if math.isfinite(float(value)) else None


def estimate_models(frame: pd.DataFrame) -> dict:
    panel = (
        frame.pivot_table(
            index=["country_code", "country", "year"],
            columns="indicator_code",
            values="value",
            aggfunc="first",
        )
        .reset_index()
        .rename(columns=SAFE_NAMES)
        .sort_values(["country_code", "year"])
    )
    if "homicide_rate" not in panel:
        raise RuntimeError("Falta el indicador principal de seguridad.")

    panel["homicide_lag1"] = panel.groupby("country_code")["homicide_rate"].shift(1)
    panel["year_centered"] = panel["year"] - panel["year"].min()
    results: list[dict] = []

    for outcome in ["gdp_growth", "fixed_capital", "fdi_gdp"]:
        if outcome not in panel:
            continue
        for exposure in ["homicide_rate", "homicide_lag1"]:
            sample = panel.dropna(subset=[outcome, exposure]).copy()
            if len(sample) < 12 or sample["country_code"].nunique() < 3:
                results.append(
                    {
                        "outcome": outcome,
                        "exposure": exposure,
                        "status": "insufficient_sample",
                        "n": int(len(sample)),
                    }
                )
                continue
            formula = f"{outcome} ~ {exposure} + year_centered + C(country_code)"
            model = smf.ols(formula, data=sample).fit(cov_type="HC1")
            results.append(
                {
                    "outcome": outcome,
                    "exposure": exposure,
                    "status": "estimated_non_causal",
                    "formula": formula,
                    "n": int(model.nobs),
                    "r_squared": _finite(model.rsquared),
                    "coefficient": _finite(model.params[exposure]),
                    "std_error_hc1": _finite(model.bse[exposure]),
                    "p_value": _finite(model.pvalues[exposure]),
                    "confidence_interval_95": [
                        _finite(model.conf_int().loc[exposure, 0]),
                        _finite(model.conf_int().loc[exposure, 1]),
                    ],
                    "interpretation_guardrail": (
                        "Asociación condicional exploratoria; no identifica efecto causal."
                    ),
                }
            )
    return {
        "generated_at": utc_now(),
        "method": "OLS pooled con efectos fijos de país, tendencia lineal y errores HC1",
        "models": results,
        "limitations": [
            "Panel pequeño y potencialmente desbalanceado.",
            "Posible simultaneidad y variables omitidas.",
            "La tasa de homicidios no resume todas las dimensiones de seguridad.",
        ],
    }


def main() -> None:
    assert_approved("validate_data")
    config = load_yaml("config/project_config.yaml")
    paths = project_paths()
    frame = pd.read_csv(ROOT / paths["processed_data"])
    output = estimate_models(frame)
    write_json(paths["econometric_results"], output)
    print(f"Modelos registrados: {len(output['models'])}")


if __name__ == "__main__":
    main()
