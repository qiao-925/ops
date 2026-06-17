"""任务自动发现 — 扫描本目录下所有 Task 子类。"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from ops.task import Task

_tasks: list[Task] | None = None


def discover() -> list[Task]:
    """发现并返回所有已注册的任务实例。"""

    global _tasks
    if _tasks is not None:
        return _tasks

    _tasks = []
    pkg_dir = Path(__file__).parent

    for finder, module_name, is_pkg in pkgutil.iter_modules([str(pkg_dir)]):
        if module_name.startswith("_"):
            continue
        module = importlib.import_module(f"ops.tasks.{module_name}")
        for attr in dir(module):
            obj = getattr(module, attr)
            if (
                isinstance(obj, type)
                and issubclass(obj, Task)
                and obj is not Task
                and obj.name
            ):
                _tasks.append(obj())

    return _tasks
