"""Task 基类 — 所有运维任务的统一接口。"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TaskContext:
    """任务执行上下文，包含共享的路径和配置。"""

    sync_dir: Path  # 仓库根目录，如 ~/.local/share/ops/repos
    ops_dir: Path  # ops 自身目录
    log_file: Path  # 同步日志文件


@dataclass
class TaskResult:
    """任务执行结果。"""

    success: bool
    summary: str = ""
    details: dict = field(default_factory=dict)


class Task:
    """运维任务基类。

    子类需定义 name、description，并实现 run / status。
    """

    name: str = ""
    description: str = ""

    def run(self, ctx: TaskContext) -> TaskResult:
        """执行任务。"""
        raise NotImplementedError

    def status(self, ctx: TaskContext) -> str:
        """返回状态信息。"""
        return "(未实现)"

    @staticmethod
    def exec_cmd(
        cmd: list[str],
        *,
        cwd: str | None = None,
        check: bool = False,
        capture: bool = False,
    ) -> subprocess.CompletedProcess:
        """统一的子进程调用。"""
        return subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            check=check,
        )
