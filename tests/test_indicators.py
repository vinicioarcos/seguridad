import json
from pathlib import Path

from scripts.common import ROOT


def test_dashboard_seed_has_no_fabricated_values():
    path = ROOT / "dashboard/public/data/indicators.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["meta"]["status"] == "awaiting_validated_data"
    assert payload["data"] == []
    assert len(payload["countries"]) == 4
    assert len(payload["indicators"]) == 4


def test_dashboard_contains_interpretation_and_sources():
    page = (ROOT / "dashboard/app/page.tsx").read_text(encoding="utf-8")
    assert "Asociación ≠ causalidad" in page
    assert "Fuente:" in page
    assert "Última observación disponible" in page
