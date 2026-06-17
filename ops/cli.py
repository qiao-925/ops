"""ops CLI — 集成面板入口。"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console

from ops.runner import compute_exit_code, run_tasks
from ops.task import TaskContext
from ops.tasks import discover

console = Console()

OPS_DIR = Path(__file__).resolve().parent.parent
SYNC_DIR = Path.home() / ".local" / "share" / "ops" / "repos"
LOG_FILE = OPS_DIR / ".sync.log"


def _build_ctx() -> TaskContext:
    """构建任务上下文。"""
    return TaskContext(
        sync_dir=SYNC_DIR,
        ops_dir=OPS_DIR,
        log_file=LOG_FILE,
    )


def _write_log(line: str) -> None:
    """追加日志。"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


@click.group()
def cli():
    """ops — 个人运维集成面板"""
    pass


@cli.command()
def sync():
    """并行执行所有同步任务。"""
    ctx = _build_ctx()
    tasks = discover()

    ts = datetime.now().strftime("%F %T")
    _write_log(f"sync-start: {ts}")

    results = run_tasks(tasks, ctx)

    ts = datetime.now().strftime("%F %T")
    for name, result in results.items():
        status = "ok" if result.success else "fail"
        _write_log(f"[{name}] {ts} status={status} summary={result.summary}")

    _write_log(f"sync-end: {ts}")

    sys.exit(compute_exit_code(results))


@cli.command()
def status():
    """查看同步状态和各任务状态。"""
    import re

    ctx = _build_ctx()

    console.print("[bold]===== 同步状态 =====[/bold]")
    console.print()

    # 最近同步记录
    console.print("[bold]--- 最近同步记录 ---[/bold]")
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > 0:
        lines = LOG_FILE.read_text().strip().split("\n")
        for line in lines[-20:]:
            console.print(f"  {line}")
    else:
        console.print("  (暂无记录，执行 ops sync 后生成)")
    console.print()

    # 同步摘要
    console.print("[bold]--- 同步摘要 ---[/bold]")
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > 0:
        text = LOG_FILE.read_text()
        starts = re.findall(r"sync-start: (.+)", text)
        ends = re.findall(r"sync-end: (.+)", text)

        if ends:
            last_end_str = ends[-1]
            try:
                last_end = datetime.strptime(last_end_str, "%Y-%m-%d %H:%M:%S")
                ago = datetime.now() - last_end
                ago_total = int(ago.total_seconds())
                if ago_total < 60:
                    ago_str = f"{ago_total}秒"
                elif ago_total < 3600:
                    ago_str = f"{ago_total // 60}分"
                else:
                    ago_str = f"{ago_total // 3600}时{(ago_total % 3600) // 60}分"
                console.print(f"  上次同步完成: {last_end_str} ({ago_str}前)")
            except ValueError:
                console.print(f"  上次同步完成: {last_end_str}")

            if starts and ends:
                try:
                    last_start = datetime.strptime(starts[-1], "%Y-%m-%d %H:%M:%S")
                    duration = int((last_end - last_start).total_seconds())
                    console.print(f"  耗时: {duration}秒")
                except ValueError:
                    pass

        console.print(f"  总同步次数: {len(starts) if starts else 0}")
    console.print()

    # 各任务状态
    tasks = discover()
    for task in tasks:
        console.print(f"[bold]--- {task.name} ---[/bold]")
        console.print(f"  {task.status(ctx)}")
        console.print()


@cli.command()
def log():
    """查看完整同步日志。"""
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > 0:
        console.print(LOG_FILE.read_text())
    else:
        console.print("(空)")


@cli.command()
def tasks():
    """列出所有已注册的任务。"""
    task_list = discover()
    console.print(f"[bold]已注册 {len(task_list)} 个任务:[/bold]")
    for t in task_list:
        console.print(f"  • {t.name}: {t.description}")


def main():
    cli()


if __name__ == "__main__":
    main()
