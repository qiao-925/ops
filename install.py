#!/usr/bin/env python3
"""ops 一键安装。

用法: curl -fsSL <url>/install.py | python3
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = "qiao-925/ops"
OPS_DIR = Path.home() / ".local" / "share" / "ops"
BIN_LINK = Path.home() / ".local" / "bin" / "ops"


def log(icon: str, msg: str) -> None:
    print(f"[{icon}] {msg}")


def main() -> None:
    print("=== ops 一键安装 ===")
    print()

    # 1. 克隆 ops 仓库
    if OPS_DIR.exists():
        log("ok", "ops 仓库已存在")
    else:
        OPS_DIR.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["gh", "repo", "clone", REPO, str(OPS_DIR)], check=True)
        log("ok", "克隆 ops 仓库")

    # 2. 创建全局命令链接
    BIN_LINK.parent.mkdir(parents=True, exist_ok=True)
    ops_bin = OPS_DIR / "bin" / "ops"
    if BIN_LINK.exists() or BIN_LINK.is_symlink():
        BIN_LINK.unlink()
    BIN_LINK.symlink_to(ops_bin)
    log("ok", f"创建链接 {BIN_LINK}")

    # 3. 检查 PATH
    path_dirs = os.environ.get("PATH", "").split(":")
    local_bin = str(Path.home() / ".local" / "bin")
    if local_bin in path_dirs:
        log("ok", "~/.local/bin 已在 PATH")
    else:
        print('[!!] 请将 export PATH="$HOME/.local/bin:$PATH" 加入 ~/.bashrc')

    # 4. 创建同步目录
    sync_dir = OPS_DIR / "repos"
    sync_dir.mkdir(parents=True, exist_ok=True)
    log("ok", f"同步目录 {sync_dir}")

    print()
    print("=== 安装完成 ===")
    print("现在可以从任意目录执行: ops sync / ops status")


if __name__ == "__main__":
    main()
