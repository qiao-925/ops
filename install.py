#!/usr/bin/env python3
"""ops 一键安装。

用法: curl -fsSL <url>/install.py | python3

目录结构:
  ~/.local/share/ops/          ops 安装
  ~/.local/share/repos/        数据仓库 (与 ops 齐平，互不影响)
  ~/.local/bin/ops             全局命令链接
"""

import os
import subprocess
import sys
from pathlib import Path

REPO = "qiao-925/ops"
OPS_INSTALL_DIR = Path.home() / ".local" / "share" / "ops"
DATA_DIR = Path.home() / ".local" / "share" / "repos"
BIN_LINK = Path.home() / ".local" / "bin" / "ops"


def log(icon: str, msg: str) -> None:
    print(f"[{icon}] {msg}")


def main() -> None:
    print("=== ops 一键安装 ===")
    print()

    # 1. 克隆 ops 仓库
    ops_bin = OPS_INSTALL_DIR / "bin" / "ops"
    if ops_bin.exists():
        log("ok", "ops 仓库已存在")
    else:
        import shutil
        if OPS_INSTALL_DIR.exists():
            shutil.rmtree(OPS_INSTALL_DIR)
        OPS_INSTALL_DIR.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["gh", "repo", "clone", REPO, str(OPS_INSTALL_DIR)], check=True)
        log("ok", f"克隆 ops 仓库 → {OPS_INSTALL_DIR}")

    # 2. 创建全局命令链接
    BIN_LINK.parent.mkdir(parents=True, exist_ok=True)
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

    # 4. 创建数据仓库目录 (与 ops 安装目录分离)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    log("ok", f"数据目录 {DATA_DIR}")

    print()
    print("=== 安装完成 ===")
    print("现在可以从任意目录执行: ops sync / ops status")


if __name__ == "__main__":
    main()
