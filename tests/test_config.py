from scripts.common import load_yaml


def test_research_design_is_specific():
    config = load_yaml("config/project_config.yaml")
    design = config["research_design"]
    assert design["topic"] == "Seguridad y desempeño económico"
    assert design["countries"] == ["ECU", "COL", "PER", "CRI"]
    assert len(design["indicators"]) == 4
    assert design["interpretation_scope"].endswith("non_causal")


def test_required_agents_exist():
    config = load_yaml("config/agents.yaml")
    assert "coordinator" in config["agents"]
    assert len(config["agents"]) >= 9
    assert "audit_agent" in config["agents"]
