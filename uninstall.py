#!/usr/bin/env python3
"""ops 一键卸载。

用法: curl -fsSL <url>/uninstall.py | python3
"""

import shutil
from pathlib import Path

OPS_INSTALL_DIR = Path.home() / ".local" / "share" / "ops"
BIN_LINK = Path.home() / ".local" / "bin" / "ops"


def log(icon: str, msg: str) -> None:
    print(f"[{icon}] {msg}")


def main() -> None:
    print("=== ops 一键卸载 ===")
    print()

    # 1. 移除全局命令链接
    if BIN_LINK.is_symlink() or BIN_LINK.exists():
        BIN_LINK.unlink()
        log("ok", f"移除链接 {BIN_LINK}")
    else:
        log("ok", "链接不存在，无需移除")

    # 2. 删除 ops 安装目录
    if OPS_INSTALL_DIR.exists():
        shutil.rmtree(OPS_INSTALL_DIR)
        log("ok", f"删除 {OPS_INSTALL_DIR}")
    else:
        log("ok", "目录不存在，无需删除")

    print()
    print("=== 卸载完成 ===")


if __name__ == "__main__":
    main()
