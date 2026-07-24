from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from scripts.common import ROOT, append_machine_log, load_yaml, save_yaml, utc_now


def task_registry() -> dict:
    return load_yaml("config/tasks.yaml")["tasks"]


def approvals_registry() -> dict:
    return load_yaml("config/approvals.yaml")


def output_exists(path: str) -> bool:
    target = ROOT / path
    return target.exists() and (not target.is_file() or target.stat().st_size > 0)


def list_tasks() -> None:
    tasks = task_registry()
    approvals = approvals_registry()["approvals"]
    print(f"{'TAREA':26} {'AGENTE':26} {'ESTADO':18} DEPENDENCIAS")
    for task_id, task in tasks.items():
        status = approvals.get(task_id, {}).get("status", "missing")
        deps = ", ".join(task.get("depends_on", [])) or "-"
        print(f"{task_id:26} {task['agent']:26} {status:18} {deps}")


def check_dependencies(task_id: str, task: dict, approvals: dict) -> None:
    pending = [
        dependency
        for dependency in task.get("depends_on", [])
        if approvals.get(dependency, {}).get("status") != "approved"
    ]
    if pending:
        raise RuntimeError(f"{task_id} está bloqueada por: {', '.join(pending)}")


def run_task(task_id: str) -> None:
    tasks = task_registry()
    if task_id not in tasks:
        raise KeyError(f"Tarea desconocida: {task_id}")
    task = tasks[task_id]
    approvals_doc = approvals_registry()
    approvals = approvals_doc["approvals"]
    check_dependencies(task_id, task, approvals)
    command = task.get("command")
    if not command:
        raise RuntimeError(f"{task_id} requiere trabajo y aprobación humana; no tiene comando.")

    append_machine_log({"task": task_id, "agent": task["agent"], "status": "started"})
    try:
        subprocess.run(command, cwd=ROOT, shell=True, check=True)
    except Exception as exc:
        append_machine_log(
            {"task": task_id, "agent": task["agent"], "status": "failed", "error": str(exc)}
        )
        raise

    missing = [path for path in task.get("outputs", []) if not output_exists(path)]
    if missing:
        append_machine_log(
            {"task": task_id, "agent": task["agent"], "status": "failed", "missing": missing}
        )
        raise RuntimeError(f"Salidas ausentes: {', '.join(missing)}")

    status = "pending_human_validation" if task.get("human_gate") else "approved"
    approvals[task_id] = {
        **approvals.get(task_id, {}),
        "status": status,
        "approved_by": "automatic_pipeline" if status == "approved" else None,
        "approved_at": utc_now() if status == "approved" else None,
    }
    save_yaml("config/approvals.yaml", approvals_doc)
    append_machine_log({"task": task_id, "agent": task["agent"], "status": status})
    print(f"{task_id}: {status}")


def approve_task(task_id: str, approved_by: str, notes: str) -> None:
    tasks = task_registry()
    if task_id not in tasks:
        raise KeyError(f"Tarea desconocida: {task_id}")
    task = tasks[task_id]
    approvals_doc = approvals_registry()
    approvals = approvals_doc["approvals"]
    check_dependencies(task_id, task, approvals)
    missing = [path for path in task.get("outputs", []) if not output_exists(path)]
    if missing:
        raise RuntimeError(f"No puede aprobarse; faltan: {', '.join(missing)}")

    approvals[task_id] = {
        **approvals.get(task_id, {}),
        "status": "approved",
        "approved_by": approved_by,
        "approved_at": utc_now(),
        "notes": notes,
    }
    if task_id == "approve_design":
        project = load_yaml("config/project_config.yaml")
        project["research_design"]["status"] = "approved"
        save_yaml("config/project_config.yaml", project)
    save_yaml("config/approvals.yaml", approvals_doc)
    append_machine_log(
        {"task": task_id, "agent": task["agent"], "status": "approved", "by": approved_by}
    )
    print(f"{task_id}: aprobado por {approved_by}")


def run_all() -> None:
    for task_id, task in task_registry().items():
        status = approvals_registry()["approvals"].get(task_id, {}).get("status")
        if status == "approved":
            continue
        if not task.get("command"):
            raise RuntimeError(f"Flujo detenido: primero apruebe manualmente {task_id}.")
        run_task(task_id)
        if task.get("human_gate"):
            raise RuntimeError(f"Flujo detenido para validación humana de {task_id}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Orquestador auditable del proyecto.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--run", metavar="TASK_ID")
    group.add_argument("--run-all", action="store_true")
    group.add_argument("--approve", metavar="TASK_ID")
    parser.add_argument("--by", help="Nombre del responsable humano.")
    parser.add_argument("--notes", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.list:
        list_tasks()
    elif args.run:
        run_task(args.run)
    elif args.run_all:
        run_all()
    elif args.approve:
        if not args.by:
            raise RuntimeError("--approve requiere --by 'Nombre'.")
        approve_task(args.approve, args.by, args.notes)


if __name__ == "__main__":
    main()
