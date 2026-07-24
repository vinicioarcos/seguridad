from scripts.common import load_yaml


def test_task_dependencies_reference_existing_tasks():
    tasks = load_yaml("config/tasks.yaml")["tasks"]
    for task in tasks.values():
        for dependency in task.get("depends_on", []):
            assert dependency in tasks


def test_every_task_has_acceptance_criterion():
    tasks = load_yaml("config/tasks.yaml")["tasks"]
    assert all(task.get("acceptance") for task in tasks.values())
