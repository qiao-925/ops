"""仓库同步任务 — 调用 clone-faster 同步所有仓库。"""

from __future__ import annotations

import subprocess

from ops.task import Task, TaskContext, TaskResult

CLONE_FASTER_URL = (
    "https://raw.githubusercontent.com/qiao-925/clone-faster/main/clone_faster.py"
)


class RepoSync(Task):
    name = "repo-sync"
    description = "同步所有仓库 (clone-faster)"

    def run(self, ctx: TaskContext) -> TaskResult:
        cmd = [
            "bash", "-c",
            f'curl -fsSL "{CLONE_FASTER_URL}" | python3 - --output "{ctx.sync_dir}"',
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)

        # 从 stdout 提取仓库数量 (clone-faster 最终输出 "N ok, N failed / N repos")
        summary = proc.stdout.strip().split("\n")[-1] if proc.stdout.strip() else ""

        return TaskResult(
            success=(proc.returncode == 0),
            summary=summary or ("完成" if proc.returncode == 0 else f"失败 (exit {proc.returncode})"),
        )

    def status(self, ctx: TaskContext) -> str:
        # clone-faster 没有 status 命令，返回目录存在性检查
        count = sum(1 for _ in ctx.sync_dir.iterdir()) if ctx.sync_dir.exists() else 0
        return f"同步目录: {ctx.sync_dir} ({count} 个顶层条目)"
