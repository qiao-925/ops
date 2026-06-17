"""Claude 会话同步任务 — 调用 claude-session-sync 的 make sync。"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ops.task import Task, TaskContext, TaskResult


class SessionSync(Task):
    name = "session-sync"
    description = "Claude 会话同步 (claude-session-sync)"

    def run(self, ctx: TaskContext) -> TaskResult:
        session_dir = ctx.sync_dir / "qiao-925" / "claude-session-sync"

        if not session_dir.exists():
            return TaskResult(
                success=False,
                summary="claude-session-sync 未克隆",
            )

        proc = subprocess.run(
            ["make", "sync"],
            cwd=str(session_dir),
            capture_output=True,
            text=True,
        )

        # 从 stderr 提取关键信息
        output = proc.stderr.strip() or proc.stdout.strip()
        summary = self._extract_summary(output)

        return TaskResult(
            success=(proc.returncode == 0),
            summary=summary or ("完成" if proc.returncode == 0 else f"失败 (exit {proc.returncode})"),
        )

    def status(self, ctx: TaskContext) -> str:
        session_dir = ctx.sync_dir / "qiao-925" / "claude-session-sync"
        if not session_dir.exists():
            return "claude-session-sync 未克隆"

        proc = subprocess.run(
            ["make", "-s", "status"],
            cwd=str(session_dir),
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip() if proc.returncode == 0 else "(无法获取)"

    @staticmethod
    def _extract_summary(output: str) -> str:
        """从 make 输出中提取摘要行。"""
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
            # make sync 的关键输出通常包含 "同步" 或 "commit" 等关键词
            if any(kw in line.lower() for kw in ["同步", "sync", "commit", "push", "already up to date"]):
                return line
        return ""
