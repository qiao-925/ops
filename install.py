#!/usr/bin/env python3
"""ops 一键安装（已有则先卸载再重装）。

用法: curl -fsSL <url>/install.py | python3
"""

import os
import shutil
import subprocess
from pathlib import Path

REPO = "qiao-925/ops"
OPS_INSTALL_DIR = Path.home() / ".local" / "share" / "ops"
BIN_LINK = Path.home() / ".local" / "bin" / "ops"


def log(icon: str, msg: str) -> None:
    print(f"[{icon}] {msg}")


def main() -> None:
    print("=== ops 安装 ===")
    print()

    # 1. 已有则先卸载
    if BIN_LINK.is_symlink() or BIN_LINK.exists():
        BIN_LINK.unlink()
        log("ok", "移除旧链接")
    if OPS_INSTALL_DIR.exists():
        shutil.rmtree(OPS_INSTALL_DIR)
        log("ok", "删除旧安装")

    # 2. 克隆 ops 仓库
    OPS_INSTALL_DIR.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["gh", "repo", "clone", REPO, str(OPS_INSTALL_DIR)], check=True)
    log("ok", f"克隆 ops 仓库 → {OPS_INSTALL_DIR}")

    # 3. 创建全局命令链接
    BIN_LINK.parent.mkdir(parents=True, exist_ok=True)
    BIN_LINK.symlink_to(OPS_INSTALL_DIR / "bin" / "ops")
    log("ok", f"创建链接 {BIN_LINK}")

    # 4. 检查 PATH
    local_bin = str(Path.home() / ".local" / "bin")
    if local_bin in os.environ.get("PATH", "").split(":"):
        log("ok", "~/.local/bin 已在 PATH")
    else:
        print('[!!] 请将 export PATH="$HOME/.local/bin:$PATH" 加入 ~/.bashrc')

    # 5. 创建数据目录
    data_dir = Path.home() / ".local" / "share" / "repos"
    data_dir.mkdir(parents=True, exist_ok=True)
    log("ok", f"数据目录 {data_dir}")

    print()
    print("=== 安装完成 ===")


if __name__ == "__main__":
    main()
