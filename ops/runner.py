"""并行执行引擎 — 调度所有任务并发运行。"""

from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ops.task import Task, TaskContext, TaskResult

console = Console()


def run_tasks(tasks: list[Task], ctx: TaskContext) -> dict[str, TaskResult]:
    """并行执行所有任务，返回 {task.name: TaskResult}。"""

    results: dict[str, TaskResult] = {}

    if not tasks:
        console.print("[yellow]没有注册任何任务[/yellow]")
        return results

    console.print(Panel(f"[bold]开始执行 {len(tasks)} 个任务[/bold]", style="blue"))
    console.print()

    start = time.time()

    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        future_map = {pool.submit(task.run, ctx): task for task in tasks}

        for future in as_completed(future_map):
            task = future_map[future]
            try:
                result = future.result()
            except Exception as exc:
                result = TaskResult(success=False, summary=f"异常: {exc}")

            results[task.name] = result
            _print_task_result(task.name, result)

    elapsed = time.time() - start
    _print_summary(results, elapsed)

    return results


def _print_task_result(name: str, result: TaskResult) -> None:
    """打印单个任务结果。"""
    icon = "[green]✓[/green]" if result.success else "[red]✗[/red]"
    console.print(f"  {icon} {name}: {result.summary}")


def _print_summary(results: dict[str, TaskResult], elapsed: float) -> None:
    """打印执行摘要。"""
    ok = sum(1 for r in results.values() if r.success)
    fail = len(results) - ok
    console.print()

    parts = [f"[green]{ok} 成功[/green]"]
    if fail:
        parts.append(f"[red]{fail} 失败[/red]")
    parts.append(f"耗时 {elapsed:.1f}s")

    console.print(Panel(" | ".join(parts), style="blue"))


def compute_exit_code(results: dict[str, TaskResult]) -> int:
    """所有任务成功返回 0，否则返回 1。"""
    return 0 if all(r.success for r in results.values()) else 1
