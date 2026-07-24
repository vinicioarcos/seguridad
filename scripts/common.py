from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def save_yaml(relative_path: str, payload: dict[str, Any]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, allow_unicode=True, sort_keys=False)


def write_json(relative_path: str, payload: Any) -> Path:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return path


def read_json(relative_path: str) -> Any:
    with (ROOT / relative_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def project_paths() -> dict[str, str]:
    return load_yaml("config/project_config.yaml")["paths"]


def source_by_id(source_id: str) -> dict[str, Any]:
    sources = load_yaml("config/sources.yaml").get("sources", [])
    for source in sources:
        if source.get("id") == source_id:
            return source
    raise KeyError(f"Fuente no registrada: {source_id}")


def assert_approved(task_id: str) -> None:
    approvals = load_yaml("config/approvals.yaml").get("approvals", {})
    status = approvals.get(task_id, {}).get("status")
    if status != "approved":
        raise RuntimeError(
            f"La puerta humana '{task_id}' está en estado '{status or 'ausente'}'. "
            "Revise la evidencia y apruébela con scripts/orchestrate.py."
        )


def append_machine_log(event: dict[str, Any]) -> None:
    path = ROOT / "outputs/logs/agent_runs.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {"timestamp": utc_now(), **event}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
